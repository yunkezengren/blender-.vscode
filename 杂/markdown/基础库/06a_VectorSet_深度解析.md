# 06a · BLI_vector_set 深度解析 —— 顺序数组与哈希索引的双容器
> 基于 `source/blender/blenlib/BLI_vector_set.hh`（总行数 1168）与 `BLI_vector_set_slots.hh` 的源码分析。配套图解页：[06a_VectorSet_内存布局_图解.html](06a_VectorSet_内存布局_图解.html)（字节级布局，浏览器打开）。

---

## 1. 它是什么，为什么自造

一句话：**`VectorSet = Vector + Set`**。数据本体住在紧凑数组 `keys_` 里（按下标 O(1) 取、保插入序），稀疏哈希槽表 `slots_` 只存"键在数组里的下标"（按值 O(1) 反查）。

`std::unordered_set` 缺的不是性能，是**"第 i 个元素"这个概念**。Blender 里三处硬需求只能靠它：

| 场景 | 需要 | 出处 |
| --- | --- | --- |
| 节点类型注册表 | 按 idname O(1) 查 + 遍历确定 | `node.cc` L2781 |
| Repeat body 身份映射 | body 节点 ↔ 迭代号 双向 | 正篇 03-03 |
| `bNodeTreeRuntime::nodes_by_id` | id 查 + 节点查 + 数组遍历 | `BKE_node_runtime.hh` L164 |

三条性质缺一不可：**有下标**（`operator[]`）/ **能反查**（`index_of_try`）/ **序确定**。`Vector` 缺第二条，`Map` 缺一三条，`std::unordered_set` 三条全缺。

**唯一陷阱**：删除用末尾补位，之后下标全变。"下标稳定"只在**只增不删**时成立——Repeat 从不删 body 节点，恰好满足。

## 2. 双容器结构

```text
  keys_ 数组（紧凑·保插入序）           slots_ 槽表（稀疏·2 的幂）
┌───┬───┬───┬───┐                 ┌────┬────┬────┬────┬────┬────┬────┬────┐
│ A │ B │ C │ … │                 │  0 │ -2 │  1 │ -1 │ -1 │  2 │ -1 │ -1 │
└───┴───┴───┴───┘                 └────┴────┴────┴────┴────┴────┴────┴────┘
  下标即"第几个插入"                 state_: -1 空 · -2 墓碑 · ≥0 即 keys_ 下标
```

- **`slots_` 不存键本体**，只存 `int64_t state_`；哈希也不存（`occupy` 的 hash 参数被忽略，注释 `/*hash*/`）——空间极简路线，8 字节/槽；
- **`keys_` 初始指向栈上 `inline_buffer_`**（内联 4 键），溢出转堆；
- 真实元素数 = `occupied_and_removed_slots_ − removed_slots_`。

为什么分开而不是像 `std::unordered_set` 那样节点串桶链：遍历变连续扫描（预取友好）、扩容只重插下标（键不搬家）、下标有意义。代价：每个键被"数组 + 槽表"两处记账。

## 3. 插入 `add_new` 五步

1. **`ensure_can_add()`** —— 负载将超 `1/2` 则先 `realloc_and_reinsert`；
2. **`hash_(key)`** —— 指针键 = 地址本身，零计算；
3. **探测** —— 从 `hash & (槽总数−1)` 线性探测：墓碑跳过、空槽停下（空槽 = 确定不存在）；
4. **`keys_` 追加** —— `index = size()`，placement new；**下标此刻分配、此后不变**，"插入序"的全部来源就是这行，没有任何排序逻辑；
5. **`slot.occupy(index, hash)`** —— `state_ = index`。收尾自检两条断言（重新哈希/比较安顿好的元素），防移动构造破坏原值。

## 4. 查找 / 删除 / 扩容

**查找** `index_of_try__impl`（L492-500）：探测中 `contains` 命中返回 `slot.index()`；遇**真空槽**返回 -1。因为查询键类型与存储键类型解耦（模板 `ForwardKey`），才有"裸 `StringRef` 直查节点表"的能力。

**删除** `remove_key_internal`（L1006-1022）：末元素补位到被删位（O(1)），但 ①补位元素的槽要沿哈希链找到并改写下标；②被删槽留墓碑（`-2`）——改成 `-1` 会截断探测链，后续同哈希元素从此找不到；③墓碑堆积触发重建。

**扩容** `realloc_and_reinsert`（L1004 起）：

```cpp
min_usable_slots = std::max(min_usable_slots, this->size() * 2);   // 至少翻倍
```

槽总数由公式 `power_of_2_max(ceil(min_usable ÷ (1/2)))` 给出（`BLI_hash_tables.hh` L54，`LOAD_FACTOR = 1,2` 见 vector_set L132）。重建 = 遍历 `keys_` 重新探测进新槽表——**键本体不重排**，只重建索引层。

**内存账（可精确推导）**：`SimpleVectorSetSlot` 8 字节/槽。4 个 int：`total = power_of_2_max(8) = 8` 槽恰好等于 `Array` 内联容量 → 零堆分配；第 5 个：需求 10 → `total = 16` → 槽表转堆 128B + `keys_` 转堆（`usable_slots > InlineBufferCapacity=4`），合计约 160B。

## 5. CustomIDVectorSet：一个 Getter 换一整套注册表

```cpp
// L1124-1125
template<typename T, typename GetIDFn> struct CustomIDHash {
  using CustomIDType = decltype(GetIDFn{}(std::declval<T>()));   // 编译期推"键的类型"
  uint64_t operator()(const T &v) const             { return get_default_hash(GetIDFn{}(v)); }
  uint64_t operator()(const CustomIDType &v) const  { return get_default_hash(v); }  // 裸键直查！
};
```

第二个重载让查询键（`StringRef`）不必是存储类型（`bNodeType*`）。`CustomIDEqual` 更给三个重载：`(T,T)`/`(ID,T)`/`(T,ID)`，覆盖三种比较方向。node.cc 三张注册表（树类型 L2775 / 节点类型 L2781 / socket 类型 L2793）各供一个 Getter（`return value->idname;`），其余机制共享。**命名提醒**：这里的 "ID" 是"哈希键"的朴素义，与 Blender 的 `ID` 数据块基类无关。

## 6. 性能账与选型判决

| 操作 | 成本 | 备注 |
| --- | --- | --- |
| `add_new` / `add` | O(1) 均摊 | 触发重哈希时 O(n) |
| `index_of_try` | O(1) | 指针键哈希=地址 |
| `operator[](i)` | O(1) 裸数组 | 零哈希 |
| `remove_contained` | O(1) | 打乱后续下标 |
| `as_span()` | 零成本 | 包一层 `keys_` |
| 内存 | 槽 0.5 负载 + 键数组 | 每键额外约 16B（槽 8 + 指针账） |

**判决**：要"有下标 + 能反查 + 顺序确定"选它；只查重用 `Set`；只按键查值用 `Map`；频繁删除慎用。

## 7. 与 Repeat 的完整对应

| 正篇代码 | 机制 |
| --- | --- |
| `VectorSet<lf::FunctionNode *> lf_body_nodes` | 指针键，哈希=地址 |
| `add_new(&lf_node)` × N | 下标 = 迭代号 |
| `index_of_try(&node)` | 执行期 O(1) 反查，-1 = 直通 |
| `[i]` / `as_span().last()` | 裸数组访问；从不 remove |

## 8. 图解页

- [06a_VectorSet_内存布局_图解.html](06a_VectorSet_内存布局_图解.html) —— 字节级布局（对象头 / 槽表三态 / 双数组映射 / 增删流程动线）
- [diagrams/06a_VectorSet_架构图.html](diagrams/06a_VectorSet_架构图.html) —— 交互式机制架构图（Archify 生成，含源码行号锚点；源 JSON 同目录 candidate.json）

## 继续阅读

- [06_Map_Set.md](06_Map_Set.md) —— Map 的"存哈希副本"路线与本篇对照
- [17_Allocator_深度解析.md](17_Allocator_深度解析.md) —— `Allocator` 模板参数
- 前置知识系列 03 章：[03-05 VectorSet稳定索引](../重复区域-前置知识-dsh/03-BLI容器与视图/05-VectorSet稳定索引.md)
