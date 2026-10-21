# 06 · GraphExecutor 调度机制

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](05-lf-Graph图结构.md) · [下一篇](07-执行钩子与副作用接口.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `GraphExecutor`——把一张静态的 `lf::Graph` 变成一次实际执行。主要源码：[`FN_lazy_function_graph_executor.hh`](../../../source/blender/functions/FN_lazy_function_graph_executor.hh)（155 行）与 [`intern/lazy_function_graph_executor_generic.hh`](../../../source/blender/functions/intern/lazy_function_graph_executor_generic.hh)（1503 行）。

## 先回答一个具体问题

一张几百个节点的图，执行器凭什么知道先跑谁、谁可以跳过、谁能并行？

答案藏在 `GraphExecutor` 的三个身份里：它是一个 `LazyFunction`（对外是一个节点）、它持有 `lf::Graph`（对内是一张图）、它调用 `GenericGraphExecutor`（真正干活的调度器）。三者叠加，把"静态图"变成"按需推进的执行过程"。

## 三个身份

`GraphExecutor` 继承自 `LazyFunction`（graph_executor.hh L91），这决定了它在父图里只是一个普通节点。但它的成员暴露了第二种身份：

```cpp
class GraphExecutor : public LazyFunction {
 private:
  const Graph &graph_;                                    // 被执行的图
  Vector<const GraphInputSocket *> graph_inputs_;         // 对外暴露的输入
  Vector<const GraphOutputSocket *> graph_outputs_;       // 对外暴露的输出
  Array<int> graph_input_index_by_socket_index_;          // 索引映射
  Array<int> graph_output_index_by_socket_index_;
  const Logger *logger_;                                  // 可选：日志钩子
  const SideEffectProvider *side_effect_provider_;        // 可选：副作用钩子
  const NodeExecuteWrapper *node_execute_wrapper_;        // 可选：执行包装钩子
  generic_graph_executor::PreprocessData preprocess_data_; // 预处理缓存
};
```

`[讲解]` 逐字段看：

| 字段 | 用途 | 为什么需要 |
| --- | --- | --- |
| `graph_` | 被执行的图 | 调度器要按拓扑顺序遍历节点 |
| `graph_inputs_` / `graph_outputs_` | 对外接口子集 | 图可能有几十个输入，但父图只连了其中几个 |
| 两个 `*_index_by_socket_index_` | 索引翻译表 | 图内部索引用 `socket.index()`，父图用"第几个连了的" |
| 三个可选钩子 | 日志/副作用/包装 | 见下一篇 |
| `preprocess_data_` | 预处理结果 | 拓扑序、需求传播表等只算一次 |

`[讲解]` 关键设计：**图的输入输出是"子集"**。`GraphExecutor` 的构造接受显式的 `graph_inputs` / `graph_outputs` 列表，而不是默认全图。原因：父图可能只连了这张图的某几个端口，其余端口应该被裁掉——这正是主系列 03-03 里 `drop_front(1)` / `take_front(...)` 那些切片操作的用途。

## 构造与两个重载

```cpp
GraphExecutor(const Graph &graph,
              const Logger *logger,
              const SideEffectProvider *side_effect_provider,
              const NodeExecuteWrapper *node_execute_wrapper);

GraphExecutor(const Graph &graph,
              Vector<const GraphInputSocket *> graph_inputs,
              Vector<const GraphOutputSocket *> graph_outputs,
              const Logger *logger,
              const SideEffectProvider *side_effect_provider,
              const NodeExecuteWrapper *node_execute_wrapper);
```

`[讲解]` 第一个重载"全连"（所有图输入输出都暴露），第二个"选择性连"。Repeat Zone 用的是第二个（见 geometry_nodes_repeat_zone.cc L394-L399），因为要把 `Usage: Iterations` 那个输出切掉。

**三个钩子全可传 nullptr**。这解释了一个常见疑问：为什么简单场景不用配钩子？因为它们是可选的，不传就是默认行为（直接 `fn.execute`、无副作用、无日志）。

## 存储管理

```cpp
void *init_storage(LinearAllocator<> &allocator) const override;
void destruct_storage(void *storage) const override;
```

`[讲解]` `GraphExecutor` 作为 `LazyFunction`，也遵守第 02 篇讲的 storage 契约：每次调用前后分配/销毁。storage 里装的是**节点状态机、值池、请求队列**这些执行期数据。

注意 `preprocess_data_` 是**成员而非 storage**——因为它是只读的，可以跨多次执行复用。这是"构建期 vs 执行期"分界线的又一个例子。

## 执行入口

```cpp
private:
  void execute_impl(Params &params, const Context &context) const override;
```

`[讲解]` 只有 10 行的接口，背后是 1503 行的 `generic_graph_executor`。这是**接口极简、实现极繁**的典型：`GraphExecutor` 是外壳，`GenericGraphExecutor` 是内核。

## 内核：GenericGraphExecutor

1503 行的实现文件里，核心是三个部分：节点状态机、需求队列、调度循环。

### 节点状态

每个节点在一次执行中有明确的状态。虽然源码里没有显式的 `enum`，但状态由几个布尔标记组合表达：

| 状态 | 含义 | 触发转移 |
| --- | --- | --- |
| 未请求 | 没人要它的输出 | → 等待中（当有人请求） |
| 等待中 | 已请求，但输入不全 | → 可执行（当最后一个输入就绪） |
| 可执行 | 所有需要的输入都就绪 | → 执行中（调度器选中） |
| 执行中 | 正在跑 `fn.execute` | → 已完成 或 → 等待中 |
| 已完成 | 所有需要的输出都已设 | 终态 |

`[讲解]` 最容易忽略的是"执行中 → 等待中"这条边。它的意思是：函数跑到一半发现某个输入没有，用 `try_get_input_data_ptr_or_request` 请求后 return。这不是失败，是正常推进。

### 调度循环的形状

```text
while 有可执行节点 or 有未就绪请求:
    取出一个可执行节点
    执行它（可能多次进出）
    处理它产生的输出
    唤醒下游
    如果所有请求的输出都就绪 → 结束
```

`[讲解]` 这不是递归，是**循环 + 队列**。好处：

1. **不会爆栈**——递归求值在深图里会把调用栈顶穿，循环不会；
2. **可以并行**——多个可执行节点可以分给不同线程；
3. **可以暂停/恢复**——请求未就绪时自然退回队列。

代价是状态管理复杂：必须显式记录每个节点"进行到哪了"。

### 需求从哪来

执行开始时，`execute_impl` 收到 `Params`，里面有"哪些输出被请求"的信息。调度器据此反问："产生这些输出的节点是谁？它们需要什么？"逐级向上。

```text
请求的 GraphOutput
  → 找到连到它的节点输出
  → 该节点需要哪些输入？
  → 这些输入来自哪些节点？
  → 递归...
```

`[讲解]` 这就是第 04 篇讲的"需求传播"在**执行期**的版本。与静态推断不同的是：执行期能看到 `ValueUsage` 的实际值，判断更精确。

### 静态 usage 初始化

执行开始前，调度器会做一次初始化：

```cpp
void initialize_static_value_usages();
```

它把第 04 篇静态推断的结论灌进执行期状态。这样调度器一上来就知道哪些节点"肯定不需要"，可以直接跳过。

`[讲解]` 为什么需要这一步？因为纯动态传播会"从输出倒推"，但在大图里倒推一次很贵。静态结论可以预先剪枝，减少倒推量。

## 多线程：谁决定并行

`GraphExecutor` 本身不创建线程。真正的并行由 `GenericGraphExecutor` 在调度循环里发起：当发现多个节点同时"可执行"，它可以分给线程池。

但有一个关键约束：**每个节点内部是否允许并行，由 `Params::try_enable_multi_threading` 谈判**（见第 03 篇）。所以并行是**两层**的：

| 层 | 粒度 | 谁控制 |
| --- | --- | --- |
| 节点间 | 多个独立节点同时跑 | 调度器 |
| 节点内 | 一个节点内部多线程 | `Params` 谈判 |

`[讲解]` Repeat 的保守选择（正篇 04-01 L590-L606）是：内层不开节点间并行（`multi_threading_enabled = false`）。因为 N 个 body 节点本来就串行依赖，开了也没用，反而增加调度开销。

## send_hint：一个常被误解的机制

总览篇提过：`lazy_threading::send_hint()` **不是"开始并行"**。现在看它的真实语义。

[`BLI_lazy_threading.hh`](../../../source/blender/blenlib/BLI_lazy_threading.hh)（88 行）的文件头注释说得很清楚：这是一个**协作式提示**机制。当一个节点知道自己要算很久，它调 `send_hint()` 告诉调度器"我这边要忙一阵，你可以先去别处找活干"。

`[讲解]` 三种理解，只有一种对：

| 理解 | 对不对 |
| --- | --- |
| "开始多线程" | ❌ 它不创建线程 |
| "我要等很久，你先去忙" | ✅ 正确 |
| "提高优先级" | ❌ 与优先级无关 |

**为什么 Repeat 在 iterations ≥ 10 时调它**（正篇 L210-L214）？因为构建展开图（复制 N 个 body 节点）是个 O(N) 的操作，N 大时会占住当前线程。这时候提示调度器"我这边有活，别人可以先去干别的"，能提高整体吞吐。

**它不改变循环体执行**。循环体仍然串行——因为有数据依赖。

## 一次执行的完整时序

三节点链 A → B → C，只请求 C 的输出：

```text
1. execute_impl 收到请求：C 的 output
2. 调度器：C 未就绪（缺输入），请求 B 的输出
3. 调度器：B 未就绪（缺输入），请求 A 的输出
4. 调度器：A 无输入依赖 → 可执行
5. 执行 A → A.output_set
6. 调度器：B 的输入就绪 → 可执行
7. 执行 B → B.output_set
8. 调度器：C 的输入就绪 → 可执行
9. 执行 C → C.output_set
10. 所有请求输出就绪 → 结束
```

`[讲解]` 注意第 2、3 步：**请求是"登记"不是"调用"**。调度器不会在请求时立刻递归执行 B，而是把"B 需要跑"记进队列，稍后统一处理。这是循环 vs 递归的根本区别。

## 与 Repeat Zone 的关系

Repeat 的 `execute_impl`（正篇 04-01 L153-L185）里：

```cpp
eval_storage.graph_executor->execute(eval_graph_params, eval_graph_context);
```

这一行就是一个完整的 `GraphExecutor::execute`。它内部会走上面那条完整时序。

`[讲解]` 三个值得注意的点：

1. **这是"一个大调用"不是"N 次小调用"**。N 个 body 节点在**一张图**里，由**一次** `execute` 驱动。串行顺序由数据依赖自然产生（body k 的输出是 body k+1 的输入），不是显式 for 循环。
2. **内层图有自己的 GraphExecutor**。外层图里 Repeat zone 节点是一个 `GraphExecutor`（它本身是 LazyFunction），内层展开图又是一个 `GraphExecutor`。**执行器是嵌套的**。
3. **多线程许可通过 RemappedParams 传下去**。`multi_threading_enabled` 从外层传进内层，决定内层是否允许并行。

## 预处理：只算一次的部分

`preprocess_data_` 是成员而非 storage，意味着它跨多次执行复用。装的是什么？

| 数据 | 用途 |
| --- | --- |
| 拓扑序 | 调度时知道"哪些节点在哪些之前" |
| 输入输出索引映射 | 快速从 socket 找到参数槽 |
| 节点元信息 | 哪些节点是函数节点、哪些是接口节点 |

`[讲解]` 这份预处理的开销是 O(V+E)，如果每次执行都算一遍，N 轮 Repeat 就要算 N 次。放成员里让"建图一次、执行 N 次"的成本结构成立——和正篇反复强调的"建图远快于执行"是同一个道理。

## 反例与边界

### 反例 1：以为执行顺序等于创建顺序

调度器按**需求**推进，不是按节点创建顺序。后创建的节点可能先执行。

### 反例 2：以为 `send_hint` 会开启并行

已经讲过。它只是提示，不创建线程。

### 反例 3：以为未使用的节点一定不执行

如果有副作用（Viewer、写属性），节点会被强制拉取执行。这是下一篇的主题。

### 反例 4：以为 `execute_impl` 只调用一次

惰性函数可能被调用多次。`GraphExecutor` 的 `execute_impl` 会驱动内层图跑完，但内层图中每个节点的函数可能被调用多次。

### 反例 5：以为多线程下 storage 可以随便写

`Params` 的多线程许可必须谈判。未经许可跨线程调非 const 方法 = 竞态。

### 反例 6：以为 `preprocess_data_` 可以改

它是 `const` 成员。改它会导致并发执行时数据竞争。

## 对理解 Repeat 的帮助

| 本篇概念 | Repeat 中的落点 |
| --- | --- |
| `graph_inputs_/outputs_` 子集 | 索引映射跳过 iterations（正篇 03-03 L367-L385） |
| 节点状态机 | N 个 body 节点串行推进 |
| 需求传播 | body k+1 请求 body k 的输出 |
| send_hint | iterations ≥ 10 时提示调度器 |
| 嵌套执行器 | 外层图 + 内层展开图 |
| `multi_threading_enabled` | 内层不开并行域 |
| 预处理复用 | 图构建一次、执行 N 轮 |

**最关键的一条**：Repeat 的"循环"不是 for 循环，而是**一张 N 节点链式图 + 一次 execute**。理解这一点，才能理解为什么正篇说"建图成本必须低于执行成本"——因为建图是每次求值都付一次的固定开销，而执行是真正的工作。

## 继续阅读

- [07-执行钩子与副作用接口](07-执行钩子与副作用接口.md) —— 三个钩子的细节
- [05-lf-Graph图结构](05-lf-Graph图结构.md) —— 图本身
- 正篇：[04-01 RepeatEvalStorage 与一次求值](../../04-运行时机制/01-RepeatEvalStorage与一次求值.md)
