# 05 · VectorSet 稳定索引

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:16px 0 20px;padding:10px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px">
<span style="font-size:11px;font-weight:700;letter-spacing:.1em;color:#64748B;margin-right:2px">导航</span>
<a href="../README.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0">前置知识总入口</a>
<a href="./README.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE">本章 03-BLI容器与视图</a>
<a href="./02-Span只读视图.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE">‹ 02-Span只读视图</a>
</div>

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;margin:18px 0 22px;padding:14px 18px;background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:10px">

基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `VectorSet<T>`——一个既是向量又是集合的容器。它是 Repeat Zone 身份机制的基石。主要源码：[`BLI_vector_set.hh`](../../../source/blender/blenlib/BLI_vector_set.hh)（1168 行）。

</div>

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## 先回答一个具体问题

Repeat 的循环体节点被执行 N 次，系统怎么知道"现在跑的是第几轮"？

答案是 `VectorSet` 的 `index_of_try`。正篇 04-02 的核心代码：

```cpp
const int iteration = lf_body_nodes_->index_of_try(const_cast<lf::FunctionNode *>(&node));
```

`[讲解]` 一行代码，完成一件事：**从节点指针反查它第一次插入时的下标**。这个下标就是迭代号。

如果只用普通 `Vector`，你得遍历查找（O(N)）；如果只用普通 `Set`，它不保证顺序。`VectorSet` 两者兼得：**O(1) 插入 + O(1) 按值查下标 + 稳定顺序**。

这就是为什么正篇说它"同时是图结构的一部分和运行时身份识别器"。

## VectorSet 的双重身份

`[讲解]` 源码头注释（L37-L40 附近）明确推荐用 `add_new` / `remove_contained` 而不是 `add` / `remove`：

> "The methods `add_new` and `remove_contained` should be used instead of `add` and `remove`"

原因是前者有前置条件断言（"我确信它不在里面"），能更早暴露逻辑错误。

`[讲解]` `VectorSet` 内部结构大致是：

```text
┌─────────────────────────────────────┐
│ elements_     ─→ [A, B, C, D]       │  Vector：保序、可按下标访问
│ index_map_     ─→ {A:0, B:1, C:2, D:3} │  Hash map：值 → 下标
└─────────────────────────────────────┘
```

两个容器同步维护：

- `elements_` 提供"第 i 个是谁"；
- `index_map_` 提供"某值在第几个"。

**关键不变量**：一旦插入，下标**永不改变**（除非删除中间元素——那时后面的会前移）。

## 核心接口

`[讲解]` 按使用频率排序：

| 方法 | 语义 | 复杂度 |
| --- | --- | --- |
| `add_new(key)` | 追加（断言不存在） | O(1) 均摊 |
| `add(key)` | 追加或返回已存在的下标 | O(1) 均摊 |
| `index_of(key)` | 查下标（断言存在） | O(1) |
| **`index_of_try(key)`** | 查下标，不存在返回 -1 | O(1) |
| `contains(key)` | 是否存在 | O(1) |
| `as_span()` | 转只读视图 | O(1) |
| `size()` / `is_empty()` | 大小 | O(1) |
| `[i]` | 按下标访问 | O(1) |
| `remove_contained(key)` | 删除（断言存在） | O(N)（要搬移后续元素） |

`[讲解]` 注意最后一行：**删除是 O(N)**。因为要保持顺序，删中间元素必须把后面的全部前移。这是"稳定顺序"的代价。

源码注释（L477 附近）对 `index_of` 与 `index_of_try` 的分工说得很清楚：

> "set. If this is not necessarily the case, use `index_of_try`."

意思是：如果你不确定元素在里面，用 `index_of_try`（返回 -1 而不是断言崩溃）。

### `index_of_try` 的签名

```cpp
int64_t index_of_try(const Key &key) const
{
  return this->index_of_try_as(key);
}
```

`[讲解]` 返回 `int64_t` 而不是 `int`。但正篇里赋值给 `int iteration`，会隐式截断。

**为什么用 -1 而不是 optional？** 因为 -1 是"不可能的下标"，语义清晰且无需额外存储。这是 C 风格但实用的约定。

## 为什么 Repeat 必须用它

`[讲解]` 三个候选方案对比：

| 方案 | 查迭代号 | 保序 | 内存 |
| --- | --- | --- | --- |
| `Vector<FunctionNode*>` + 线性查找 | O(N) | ✅ | 小 |
| `Map<FunctionNode*, int>` | O(1) | ❌（无顺序概念） | 大 |
| **`VectorSet`** | **O(1)** | **✅** | **中** |

`[讲解]` 如果选 `Vector` + 线性查找，每次节点执行都要扫一遍 N 个节点。Repeat N=100 时，每轮 O(100)，总 O(10000)——不可接受。

如果选 `Map`，插入时没有稳定顺序，无法回答"第 i 个是谁"（而这正是构造 §3 需要的）。

`VectorSet` 同时满足"反查"（`index_of_try`）和"正查"（`as_span()[i]`），所以是唯一选择。

## 在 Repeat 中的三处用法

`[讲解]` 正篇里 `VectorSet<lf::FunctionNode *>` 出现在三个地方：

### 1. 构建期：按顺序插入

```cpp
VectorSet<lf::FunctionNode *> &lf_body_nodes = eval_storage.lf_body_nodes;
for ([[maybe_unused]] const int i : IndexRange(iterations)) {
  lf::FunctionNode &lf_node = lf_graph.add_function(*body_fn_.function);
  lf_body_nodes.add_new(&lf_node);
}
```

`[讲解]` 关键点：

- 循环变量 `i` 标了 `[[maybe_unused]]`——因为**顺序信息由 VectorSet 的位置隐式承载**，不需要显式记录；
- 第 i 次 `add_new` 插入的节点，其下标必然是 i。

**这是一个强约束**：插入必须严格按迭代顺序。如果乱序插入，迭代号就错了。

### 2. 执行期：反查迭代号（wrapper）

```cpp
const int iteration = lf_body_nodes_->index_of_try(const_cast<lf::FunctionNode *>(&node));
```

`[讲解]` 注意 `const_cast`。因为 `execute_node` 收到的是 `const FunctionNode &`，而 `index_of_try` 需要非 const 指针（VectorSet 的 Key 是 `FunctionNode*`，不是 `const FunctionNode*`）。

**为什么需要 const_cast？** 因为 VectorSet 存的是可变指针，而钩子接口签名用了 const 引用。这是"接口保守、容器灵活"的不匹配。

### 3. 执行期：下标映射（provider）

```cpp
Span<lf::FunctionNode *> lf_body_nodes_;

Vector<const lf::FunctionNode *> lf_nodes;
for (const int i : iterations_with_side_effects) {
  if (i >= 0 && i < lf_body_nodes_.size()) {
    lf_nodes.append(lf_body_nodes_[i]);   // 按迭代号取节点
  }
}
return lf_nodes;
```

`[讲解]` provider 只需要"按下标取"，所以它持有 `Span` 而不是 `VectorSet*`。

正篇 03-03 L943 对此有精辟总结：**wrapper 持 `VectorSet*`（要 `index_of_try`），provider 持 `Span`（只要下标访问）**。各自成员类型精确匹配访问模式。

## 与 MutableSpan / Span 的关系

`[讲解]` `VectorSet::as_span()` 返回 `Span<Key>`（只读视图）。这就是正篇里 `lf_body_nodes.as_span().last()` 的来历：

```cpp
lf::FunctionNode &lf_last_body_node = *lf_body_nodes.as_span().last();
```

`[讲解]` 三个转换：

| 从 | 到 | 方法 | 用途 |
| --- | --- | --- | --- |
| `VectorSet` | `Span` | `as_span()` | 只读遍历 |
| `VectorSet` | 元素指针 | `operator[]` | 下标访问 |
| `VectorSet` | 下标 | `index_of_try` | 反查 |

**注意**：`as_span()` 之后就不能再插入/删除了（否则 span 悬空）。这是"视图 vs 容器"的经典约束。

## 内存与复杂度

`[讲解]` `VectorSet` 比普通 `Vector` 多一个哈希表。代价：

| 操作 | Vector | VectorSet | 倍数 |
| --- | --- | --- | --- |
| 插入 | O(1) 均摊 | O(1) 均摊 | ~1.5x（哈希计算） |
| 查找 | O(N) | O(1) | 无法比较 |
| 内存 | N×sizeof(T) | N×sizeof(T) + 哈希表 | ~1.5-2x |

`[讲解]` 在 Repeat 场景下，N 通常不大（迭代数几十到几百），内存代价可以忽略；但反查带来的复杂度收益巨大。

## 用小数据走一遍

3 轮 Repeat，body 节点指针分别是 `P0, P1, P2`：

**插入阶段**：

| 步 | 操作 | elements_ | index_map_ |
| --- | --- | --- | --- |
| 1 | `add_new(P0)` | [P0] | {P0:0} |
| 2 | `add_new(P1)` | [P0,P1] | {P0:0, P1:1} |
| 3 | `add_new(P2)` | [P0,P1,P2] | {P0:0, P1:1, P2:2} |

**执行阶段**：

| 执行到 | `index_of_try(...)` | 得到 |
| --- | --- | --- |
| P0 | `index_of_try(P0)` | 0 |
| P1 | `index_of_try(P1)` | 1 |
| P2 | `index_of_try(P2)` | 2 |
| 某辅助节点 Q | `index_of_try(Q)` | **-1** |

`[讲解]` 最后一行是关键：**辅助节点（如 LogicalOr）返回 -1**，wrapper 据此判断"不是 body 节点，正常执行"。

## 反例与边界

### 反例 1：乱序插入

```cpp
// 危险：先插第 2 轮，再插第 0 轮
lf_body_nodes.add_new(&node2);
lf_body_nodes.add_new(&node0);
```

下标就变成了 `{node2:0, node0:1}`——迭代号全错。**插入顺序即迭代号**，这是不可违反的契约。

### 反例 2：以为 `index_of` 安全

```cpp
const int i = lf_body_nodes.index_of(&some_unknown_node);  // 断言失败
```

不确定存在就用 `index_of_try`。

### 反例 3：`as_span()` 之后再插入

```cpp
Span<...> s = vs.as_span();
vs.add_new(...);   // 可能 realloc，s 悬空
```

### 反例 4：以为删除保持下标

```cpp
vs.remove_contained(vs[1]);
// 原来的 vs[2] 现在变成 vs[1]
```

删除中间元素会让后续下标全部前移。Repeat 里从不删 body 节点，所以没这个问题。

### 反例 5：把 `index_of_try` 的 -1 当下标用

```cpp
const int i = vs.index_of_try(&x);   // 可能是 -1
vs[i];   // 越界！
```

必须检查 `i >= 0`。正篇的 provider 就是这么做的（`if (i >= 0 && i < size)`）。

### 反例 6：以为 `VectorSet` 线程安全

它不是。插入/删除必须单线程或加锁。Repeat 的插入发生在建图期（单线程），执行期只读，所以安全。

## 对理解 Repeat 的帮助

| 本篇概念 | Repeat 中的落点 |
| --- | --- |
| `add_new` 的顺序性 | 第 i 次插入 = 第 i 轮 |
| `index_of_try` | wrapper 反查迭代号 |
| `-1` 哨兵 | 非 body 节点（LogicalOr 等） |
| `as_span()` | 取最后一个 body 节点 |
| 插入后下标稳定 | 迭代号与节点指针绑定一次 |
| 只读无锁 | 执行期并发读安全 |

**最关键的一条**：Repeat 的迭代身份**不是存在节点里的字段**，而是**节点在 VectorSet 中的位置**。这是一个非常精妙的设计——省掉了并行维护编号的负担，但要求"插入顺序必须正确"。

理解了这一点，正篇 03-03 那句"`VectorSet` 在这里同时是图结构的一部分和运行时身份识别器"就有了具体含义。

## 继续阅读

- [06-Map与MultiValueMap](06-Map与MultiValueMap.md) —— 另一类关联容器
- [03-Span与MutableSpan](03-Span与MutableSpan.md) —— `as_span()` 的来源
- 正篇：[03-03 执行图按迭代展开](../../重复区域-dsh/03-几何节点执行架构/03-执行图按迭代展开.md) 第 2 节
- 正篇：[04-02 ComputeContext 与迭代身份](../../重复区域-dsh/04-运行时机制/02-ComputeContext与迭代身份.md)


---

## 深读篇：VectorSet 的内部实现

前面讲的是"怎么用"，这篇讲"怎么实现的"——理解了内部结构，才能判断什么时候它不适合用。

### 双容器结构

```text
VectorSet<T>
├── Vector<T *> elements_        按插入序存元素指针
└── Map<T *, int64_t> index_map_  元素指针 → 下标
```

`[讲解]` 为什么存**指针**而不是值？

因为 `T` 可能很大（比如 `ZoneRelation` 结构体）。存指针让 `elements_` 只是个小数组，扩容成本低。

`[讲解]` 内存代价对比：

| 方案 | 每元素开销 |
| --- | --- |
| `Vector<T>` | `sizeof(T)` |
| `VectorSet<T>` | `sizeof(T*) + sizeof(T*) + int64` ≈ 20-24 字节额外 |

在 Repeat 场景下元素是 `lf::FunctionNode*`（本来就是个指针），所以额外开销只有哈希表部分。

### 插入流程

`[讲解]` `add_new(key)` 的两步：

```text
1. 检查 key 是否已存在（哈希查找）→ 存在则断言失败
2. elements_.append(&key) → 得到下标 i
   index_map_.add(&key, i)
```

`[讲解]` 注意第 2 步的顺序：**先 append 再登记**。因为下标要等 append 之后才知道。

**关键不变量**：`index_map_[elements_[i]] == i`，对所有 i 成立。

### 为什么插入后下标永不改变

`[讲解]` 这是 `VectorSet` 最重要的保证，也是 Repeat 身份机制的基础。

看它**不做什么**：

- 不排序（排序会让下标乱）；
- 不在删除时压缩（会全乱）——**删除时后续元素前移**，这点要注意。

`[讲解]` 所以严格说，保证是"**在没有删除的前提下**下标稳定"。Repeat 从不删 body 节点，所以成立。

如果代码中途删了中间元素呢？

```text
初始: [A, B, C]  → A:0, B:1, C:2
删除 B: [A, C]    → A:0, C:1（C 的下标从 2 变成 1！）
```

`[讲解]` 这就是为什么 `remove_contained` 是 O(N)——它要更新后面所有元素的下标。

### 查找流程

`[讲解]` `index_of_try(key)`：

```text
1. 在 index_map_ 里查 key → 得到下标或未找到
2. 未找到 → 返回 -1
```

`[讲解]` 两步变一步：哈希表直接给下标，不需要遍历 `elements_`。

**对比 `Vector` 的实现**：`Vector::first_index_try` 是线性扫描 O(N)。N=100 时，每次查找 100 次比较 vs 1 次哈希——**差距是两个数量级**。

### 哈希函数的来源

`[讲解]` `VectorSet` 需要 `Key` 可哈希。看它的模板约束（源码里应该要求 `default_hash` 可用）。

对 `lf::FunctionNode*`：

- 指针哈希 = 地址本身（最简单）；
- 无碰撞（地址唯一）；
- O(1) 恒定。

`[讲解]` **这是 Repeat 场景最有利的一点**：元素是指针，哈希就是地址，没有哈希计算成本。如果元素是结构体（比如 `ZoneRelation`），哈希就要遍历字段——成本高得多。

### as_span 的零成本

`[讲解]` `as_span()` 返回 `Span<Key>`：

```cpp
Span<Key> as_span() const { return elements_.as_span(); }
```

`[讲解]` 完全零成本——只是把 `Vector` 的 `data_` 和 `size_` 包一层。

**但有约束**：`as_span()` 之后不能插入/删除（可能 realloc）。正篇的用法都是"建完图后只读"，所以安全。

### 与 std::unordered_set 的对比

`[讲解]` 一张表说清差异：

| 维度 | `VectorSet` | `std::unordered_set` |
| --- | --- | --- |
| 迭代顺序 | **插入序** | 未定义（取决于哈希桶） |
| 按值查下标 | **O(1) `index_of`** | ❌ 没有这个概念 |
| 按下标访问 | **O(1) `operator[]`** | ❌ 不能 |
| 删除复杂度 | O(N)（要前移） | O(1) 均摊 |
| 内存 | 指针数组 + 哈希表 | 哈希桶 |

`[讲解]` **核心差异是"有下标"**。`std::unordered_set` 没有"第 i 个元素"的概念——它只有"在不在"。

Repeat 需要的是"第 i 个"（正查）和"这个在第几个"（反查）——这正好是 `VectorSet` 的定义。

## 三个真实使用模式的代价分析

`[讲解]` 从正篇提炼，逐个算成本：

### 模式 1：建图期按序插入（N 次）

```cpp
for ([[maybe_unused]] const int i : IndexRange(iterations)) {
  lf::FunctionNode &lf_node = lf_graph.add_function(*body_fn_.function);
  lf_body_nodes.add_new(&lf_node);
}
```

`[讲解]` 成本：N 次 `add_new`，每次 = 1 次哈希插入 + 1 次数组追加。

总计 **O(N)**。N=100 时约 100 次哈希 + 100 次数组操作——微秒级。

### 模式 2：执行期反查（N 次）

```cpp
const int iteration = lf_body_nodes_->index_of_try(&node);
```

`[讲解]` 成本：每次执行一个节点做一次哈希查找。

**总计 N 次**（每个 body 节点执行一次）。

`[讲解]` 关键：这次查找发生在**每个节点执行之前**，属于热路径。但成本是一次哈希（指针哈希 = 地址本身），可以忽略。

### 模式 3：按迭代号取节点（副作用表）

```cpp
lf_nodes.append(lf_body_nodes_[i]);
```

`[讲解]` 成本：O(1) 下标访问。

**总计**：副作用迭代数（通常远小于 N）。

## 反例补遗

### 反例 7：以为 `VectorSet` 能排序

它保持插入序，不提供排序。要排序得自己重建（会打乱下标）。

### 反例 8：在 `as_span()` 后插入

```cpp
Span<Node*> span = vs.as_span();
vs.add_new(&new_node);   // 可能 realloc → span 悬空
```

### 反例 9：用非指针元素

```cpp
VectorSet<SomeStruct> vs;   // 哈希要遍历字段，成本高
```

如果元素是指针，哈希几乎免费；如果是结构体，要做好成本预期。

### 反例 10：以为 `index_of_try` 返回 optional

它返回 `int64_t`，-1 表示不存在。用 `int64_t` 而不是 `int` 是为了避免"下标超 int 范围"的假设。

## 与 Repeat 的完整对应

`[讲解]` 把本篇与正篇对齐：

| 正篇代码 | 本篇概念 |
| --- | --- |
| `VectorSet<lf::FunctionNode *> lf_body_nodes` | 元素是指针，哈希免费 |
| `lf_body_nodes.add_new(&lf_node)` | 按序插入，下标 = 迭代号 |
| `index_of_try(&node)` | O(1) 反查迭代号 |
| `-1` 判定 | 非 body 节点直通 |
| `as_span().last()` | 取最后一个 body |
| `lf_body_nodes_[i]` | 按迭代号取节点 |

## 本篇小结

`VectorSet` 的三条性质决定了它在 Repeat 里的地位：

1. **有下标**（`operator[]`）——正查迭代号；
2. **能反查**（`index_of_try`）——从节点找迭代号；
3. **插入序稳定**——下标即语义。

三条缺一不可。`Vector` 缺第 2 条，`Map` 缺第 1、3 条，`std::unordered_set` 三条都缺。

理解了这一点，正篇那句"`VectorSet` 在这里同时是图结构的一部分和运行时身份识别器"就不再是修辞，而是对数据结构的准确描述。
