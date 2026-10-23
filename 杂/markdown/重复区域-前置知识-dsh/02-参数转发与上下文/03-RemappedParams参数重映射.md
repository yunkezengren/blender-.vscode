# 03 · RemappedParams 参数重映射

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:16px 0 20px;padding:10px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px">
<span style="font-size:11px;font-weight:700;letter-spacing:.1em;color:#64748B;margin-right:2px">导航</span>
<a href="../README.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0">前置知识总入口</a>
<a href="./README.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE">本章 02-参数转发与上下文</a>
<a href="./01-Context存储与UserData.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE">‹ 01-Context存储与UserData</a>
</div>

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;margin:18px 0 22px;padding:14px 18px;background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:10px">

基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `RemappedParams`——嵌套惰性函数之间的参数转发器。主要源码：[`FN_lazy_function_execute.hh`](../../../source/blender/functions/FN_lazy_function_execute.hh) L49-L75。

</div>

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## 先回答一个具体问题

一个惰性函数内部藏了另一个惰性函数，内层跑起来时向"自己的参数表"要第 j 个输入、设第 k 个输出。但真正的数据在外层参数表里，而且两边的编号对不上。怎么解决？

答案是 `RemappedParams`：一个带换算表的 `Params` 转发器。

`[讲解]` 它是 Repeat Zone 最不能跳过的一个类。正篇 04-01 的核心代码：

```cpp
lf::RemappedParams eval_graph_params{*eval_storage.graph_executor,
                                     params,
                                     eval_storage.input_index_map,
                                     eval_storage.output_index_map,
                                     eval_storage.multi_threading_enabled};
lf::Context eval_graph_context{
    eval_storage.graph_executor_storage, context.user_data, context.local_user_data};
eval_storage.graph_executor->execute(eval_graph_params, eval_graph_context);
```

这三行里，第一行就是在造 `RemappedParams`。不理解它，这三行就是黑箱。

## 类定义

```cpp
/**
 * Wraps an existing #Params. This should be used when a lazy-function internally contains another
 * lazy-function that handles a subset or the inputs and outputs.
 */
class RemappedParams : public Params {
 private:
  Params &base_params_;
  Span<int> input_map_;
  Span<int> output_map_;
  bool &multi_threading_enabled_;

 public:
  RemappedParams(const LazyFunction &fn,
                 Params &base_params,
                 Span<int> input_map,
                 Span<int> output_map,
                 bool &multi_threading_enabled);

  void *try_get_input_data_ptr_impl(const int index) const override;
  void *try_get_input_data_ptr_or_request_impl(const int index) override;
  void *get_output_data_ptr_impl(const int index) override;
  void output_set_impl(const int index) override;
  bool output_was_set_impl(const int index) const override;
  ValueUsage get_output_usage_impl(const int index) const override;
  void set_input_unused_impl(const int index) override;
  bool try_enable_multi_threading_impl() override;
};
```

`[讲解]` 四个字段，每个都很关键：

| 字段 | 类型 | 语义 |
| --- | --- | --- |
| `base_params_` | `Params &`（引用） | 真正的数据在外层这里 |
| `input_map_` | `Span<int>` | 内层第 i 个输入 → 外层第 `input_map_[i]` 个 |
| `output_map_` | `Span<int>` | 内层第 j 个输出 → 外层第 `output_map_[j]` 个 |
| `multi_threading_enabled_` | `bool &`（引用） | 并联，多方共享同一个开关 |

`[讲解]` 三个观察：

1. **`base_params_` 是引用不是拷贝**。它必须活到 `RemappedParams` 用完——这决定了 `RemappedParams` 通常是栈上临时对象（正篇里就是一个局部变量）。
2. **两个 map 的方向相反**。输入是"内层→外层"（要数据时往外找），输出也是"内层→外层"（设值时往外写）。**两个方向都指向外层**，别搞反。
3. **`multi_threading_enabled_` 是引用**。为什么？因为这是**共享状态**：内层申请并行成功后，外层也要知道（否则外层仍会限制）。

## 注释里的关键一句

> "This should be used when a lazy-function internally contains another lazy-function that handles a subset or the inputs and outputs."

`[讲解]` 两个词值得注意：

- **"a subset of"**：内层只处理外层输入输出的一个子集。这正是 Repeat 的情况——内层图不处理 `Iterations` 输入（它已被消费）。
- **"internally contains another lazy-function"**：嵌套关系。`GraphExecutor` 是 `LazyFunction`，所以它可以被当作一个节点塞进父图，也可以自己执行一张内层图。

## 为什么需要重映射

`[讲解]` 核心原因：**两套参数表的编号体系不同**。

内层图（`eval_storage.graph_executor`）有自己的输入输出列表：

```text
内层图的输入（构造时由 lf_graph.add_input 决定）：
  [0] Geometry
  [1] Float
  [2] Usage: Geometry
  [3] Usage: Float
  [4] Border Link Usage
```

外层的 Repeat wrapper 有另一套：

```text
外层 wrapper 的输入（由 initialize_zone_wrapper 决定）：
  [0] Iterations          ← 内层图没有这个
  [1] Geometry
  [2] Float
  [3] Link from X
  [4] Usage: zone输出Geometry
  [5] Usage: zone输出Float
```

`[讲解]` 注意 `Iterations` 只在外层出现。因为它在图构建时被**消费**掉了（决定复制几个 body），之后就再也用不到了。

于是内层要第 0 个输入（Geometry）时，必须去外层取第 1 个。这个映射就是 `input_map_`。

## 映射的构造方式

`[讲解]` `input_index_map` / `output_index_map` 由 `initialize_execution_graph` 构造。看正篇的真实代码（L367-L385）：

```cpp
eval_storage.output_index_map.reinitialize(outputs_.size() - 1);
eval_storage.input_index_map.resize(inputs_.size() - 1);
array_utils::fill_index_range<int>(eval_storage.input_index_map, 1);

const int iteration_usage_index = zone_info_.indices.outputs.input_usages[0];
array_utils::fill_index_range<int>(
    eval_storage.output_index_map.as_mutable_span().take_front(iteration_usage_index));
array_utils::fill_index_range<int>(
    eval_storage.output_index_map.as_mutable_span().drop_front(iteration_usage_index),
    iteration_usage_index + 1);
```

`[讲解]` 逐行拆：

**输入侧**：`fill_index_range<int>(map, 1)` 把 map 填成 `[1, 2, 3, ...]`。这是"整体右移一格"——因为外层第 0 个（Iterations）被丢掉，剩下的从 1 开始。

**输出侧**分两段：

- `take_front(iteration_usage_index)` 填 `[0, 1, ...]`（前段原样）；
- `drop_front(iteration_usage_index)` 填 `[iteration_usage_index + 1, ...]`（后段跳过一格）。

`[讲解]` 这叫"**挖洞**"——外层的输出序列中，第 `iteration_usage_index` 个（"Usage: Iterations"）被挖掉，前后两段拼接。

## 两个方向的不对称

`[讲解]` 这是最容易搞混的地方。两种映射的"读法"不同：

### 输入映射：`input_map[i]` = 内层第 i 个输入去外层哪找

```
内层 index 0 → input_map[0] = 1 → 外层 index 1
内层 index 1 → input_map[1] = 2 → 外层 index 2
```

### 输出映射：`output_map[j]` = 内层第 j 个输出写到外层哪

```
内层 index 0 → output_map[0] = 0 → 外层 index 0
内层 index 1 → output_map[1] = 1 → 外层 index 1
内层 index 2 → output_map[2] = 3 → 外层 index 3   ← 跳过 2（Iterations usage）
```

`[讲解]` 两个方向都叫"内层→外层"，但**用途不同**：输入是"去外层取"，输出是"往外层写"。

## 实现套路：每个方法一行转发

`[讲解]` `RemappedParams` 的七个 `*_impl` 实现极其统一。以输入为例：

```cpp
void *try_get_input_data_ptr_impl(int index) const override
{
  return base_params_.try_get_input_data_ptr(input_map_[index]);
}
```

`[讲解]` 一行代码，三件事：

1. **翻译索引**：`input_map_[index]`；
2. **转发调用**：`base_params_.try_get_input_data_ptr(...)`；
3. **原样返回**：不需要任何额外处理。

输出同理：

```cpp
void *get_output_data_ptr_impl(int index) override
{
  return base_params_.get_output_data_ptr(output_map_[index]);
}
```

`[讲解]` 这个"逐方法转发"的模式叫**委托（delegation）**。它的好处是：

- 内层代码完全不知道有映射存在；
- 映射逻辑集中在一处；
- 加新的 `Params` 方法只需加一行转发。

**代价**：每次调用多一次虚函数跳转 + 一次数组索引。在热路径上有开销，但相比"复制整个参数表"仍然便宜得多。

## 多线程许可的转发

```cpp
bool try_enable_multi_threading_impl() override
{
  if (multi_threading_enabled_) {
    return true;   // 已经开了，直接返回
  }
  /* 向外层申请 */
  if (base_params_.try_enable_multi_threading()) {
    multi_threading_enabled_ = true;
    return true;
  }
  return false;
}
```

`[讲解]` 这是唯一一个"不只是转发"的方法：

1. 先查本地开关（可能已经开了）；
2. 没开就向外层申请；
3. 申请成功则**同时更新本地开关**（因为是引用，多方可见）。

**为什么 `multi_threading_enabled_` 是引用而不是值？** 因为它是**三方共享的**：

- 外层 `Params` 的状态；
- `RemappedParams` 的本地缓存；
- Repeat 的 `RepeatEvalStorage::multi_threading_enabled` 字段。

正篇里这个字段从 storage 传进 `RemappedParams`，如果内层申请成功，storage 里的值也跟着变。这样"内层已经并行"这个事实，外层也能看到。

## 位置参数表

`[讲解]` 用一张表把 Repeat 的具体情况列清楚。场景：2 个 item（Geometry、Float）、1 条 border link、无 reference set。

**外层 wrapper 输入**：

| 外层 idx | 名称 | 内层 idx | input_map 值 |
| --- | --- | --- | --- |
| 0 | Iterations | —（不映射） | — |
| 1 | Geometry | 0 | 1 |
| 2 | Float | 1 | 2 |
| 3 | Link from X | 2 | 3 |
| 4 | Usage: zone输出Geometry | 3 | 4 |
| 5 | Usage: zone输出Float | 4 | 5 |

所以 `input_map = [_, 1, 2, 3, 4, 5]`（第 0 项不用）。

**外层 wrapper 输出**：

| 外层 idx | 名称 | 内层 idx | output_map 值 |
| --- | --- | --- | --- |
| 0 | Geometry | 0 | 0 |
| 1 | Float | 1 | 1 |
| 2 | **Usage: Iterations** | —（挖掉） | — |
| 3 | Usage: Geometry | 2 | 3 |
| 4 | Usage: Float | 3 | 4 |
| 5 | Border Link Usage | 4 | 5 |

所以 `output_map = [0, 1, 3, 4, 5]`（跳过 2）。

## 用小数据走一遍

内层图要设第 2 个输出（Usage: Geometry）：

```text
1. 内层代码调 params.set_output(2, ...)
2. RemappedParams::set_output_impl(2)
3. 查 output_map_[2] = 3
4. 转发：base_params_.set_output(3, ...)
5. 外层第 3 个输出（Usage: Geometry）被设置
```

`[讲解]` 如果直接转发（不查 map），就会设到外层的第 2 个（Usage: Iterations）——完全错误。

**这就是映射存在的全部理由**：让内层的"第几个"在外层对上号。

## 反例与边界

### 反例 1：把两个 map 混用

```cpp
// 错误：输入用了 output_map
return base_params_.try_get_input_data_ptr(output_map_[index]);
```

两个 map 的方向和长度都可能不同，混用会索引到错误的槽。

### 反例 2：以为 `RemappedParams` 拥有数据

它只有引用。`base_params_` 一旦销毁，它就悬空。所以它只能做局部临时对象。

### 反例 3：以为 map 的长度是固定的

`input_map` 长度 = 内层输入数，`output_map` 长度 = 内层输出数。而内层图是按迭代数动态生成的——虽然本场景下输入输出数与迭代数无关，但**图的节点数**是变化的。所以不能硬编码。

### 反例 4：在多线程下共享同一个 `RemappedParams`

`base_params_` 的转发调用会触及外层状态。多个线程同时用同一个 `RemappedParams` 需要外层允许并行。

### 反例 5：以为 `multi_threading_enabled_` 是纯输出参数

它既读又写。作为引用传入，意味着调用方也要能看到内层的申请结果。

## 对理解 Repeat 的帮助

| 本篇概念 | Repeat 中的落点 |
| --- | --- |
| `base_params_` | 外层 wrapper 的 `params` |
| `input_map_` | 跳过 Iterations 的整体右移 |
| `output_map_` | 挖掉 "Usage: Iterations" 的分段拼接 |
| `multi_threading_enabled_` | storage 字段，内外共享 |
| 委托模式 | 内层图完全不知道映射存在 |

**最关键的一条**：`RemappedParams` 是"**参数视图的视图**"。它让内层图可以假装自己的参数表就是完整的，从而复用所有已有的惰性函数代码。这是"包装而非修改"的经典应用——和 wrapper 钩子的思路一脉相承。

## 继续阅读

- [04-多线程许可与线程约束](04-多线程许可与线程约束.md)
- [02-BasicParams与参数内存布局](02-BasicParams与参数内存布局.md)
- 正篇：[03-03 执行图按迭代展开](../../重复区域-dsh/03-几何节点执行架构/03-执行图按迭代展开.md) 第 12 节
- 正篇：[04-01 RepeatEvalStorage 与一次求值](../../重复区域-dsh/04-运行时机制/01-RepeatEvalStorage与一次求值.md)

