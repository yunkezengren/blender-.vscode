# 06b · Map/Set 内存布局 —— 单容器路线与 VectorSet 对照

> 基于 `BLI_map.hh`（总行数 1383）、`BLI_map_slots.hh`（362 行）、`BLI_set_slots.hh`（378 行）、`BLI_hash_tables.hh` 的实测源码。配套：[Map 布局图解](06b_Map_内存布局_图解.html) · [Set 布局图解](06b_Set_内存布局_图解.html) · [Map 架构图](diagrams/06b1_Map_架构图.html) · [Set 架构图](diagrams/06b2_Set_架构图.html) · [06a_VectorSet_深度解析.md](06a_VectorSet_深度解析.md)（双容器路线对照）· [06_Map_Set.md](06_Map_Set.md)（接口与用法）

---

<style>.tip{background:#f5f3ff;border-left:4px solid #7c3aed;padding:10px 16px;border-radius:0 8px 8px 0}</style>

## 1. 一图总览

**Map/Set 与 VectorSet 的根本分野**：键值**直接存在槽里**，一张槽表就是容器的全部——没有第二数组、没有"第 i 个"概念、遍历顺序由哈希桶位决定。

```text
VectorSet（06a）：keys_ 数组(数据) + slots_ 槽表(存下标)     ← 双容器
Map/Set（本篇）：slots_ 槽表(键+值+状态都在槽内)              ← 单容器
```

| 你要什么 | Map/Set | VectorSet |
| --- | --- | --- |
| 按键查值 | O(1) 探测，槽里直接拿 | O(1) 探测取下标 → 再访问 keys_ |
| 按下标取"第 i 个" | ❌ 无此概念 | ✅ `keys_[i]` |
| 遍历顺序 | 槽位序（哈希决定，不确定） | 插入序（确定） |
| 删除 | 槽留墓碑，**无补位动作** | 末尾补位 → 下标乱 |

**判定口诀**：遍历顺序有意义 → VectorSet；只按键查 → Map/Set（更省一层间接）。

## 2. 对象头（BLI_map.hh L140-L172 实测）

与 VectorSet 几乎同构，只少 `keys_` 指针：

| 字段 | 本例值（int→float，3 元素 1 墓碑） | 说明 |
| --- | --- | --- |
| `slots_` | `Array<Slot, N>` | 内联容量 = `compute_total_slots(4, 1, 2)` → 同 VectorSet |
| `removed_slots_` | 1 | 墓碑计数 |
| `occupied_and_removed_slots_` | 4 | 真实元素 = 4−1 = 3 |
| `usable_slots_` | 8 | 负载上限；`max_load_factor_ = 1/2`（L163） |
| `inline_buffer_` | 栈上槽缓冲 | 默认容量公式 `default_inline_buffer_capacity(sizeof(K)+sizeof(V))`（`BLI_memory_utils.hh` L274：**<100B 给 4，否则 0**） |

Map 的内联门槛比 VectorSet 严：元素是"键+值"两个，`sizeof(K)+sizeof(V) ≥ 100` 时**直接放弃内联**（容量 0）。

## 3. 槽的两种形态（BLI_map_slots.hh 实测）

### 3.1 SimpleMapSlot——默认槽（L48-L57）

```cpp
enum State : uint8_t { Empty = 0, Occupied = 1, Removed = 2 };
State state_;
TypedBuffer<Key> key_buffer_;
TypedBuffer<Value> value_buffer_;
```

`Map<int,float>` 的槽 = 1+4+4 → 对齐后 **12~16 字节**。状态用独立枚举（VectorSet 是符号复用 int64，两种编码路线）。

### 3.2 IntrusiveMapSlot——指针键特化（L235 起 + `BLI_hash_tables.hh` L185-L199）

指针键（`Map<K*, V>`）换用侵入式槽：**状态编进指针值本身，零额外字节**：

```cpp
static Pointer get_empty() { return Pointer(UINTPTR_MAX);     }  // 空
static void remove(Pointer &p) { p = Pointer(UINTPTR_MAX - 1); } // 墓碑
```

合法用户指针永远到不了 `UINTPTR_MAX` 附近，这两个哨兵值绝对安全。节点系统里大量 `Map<lf::Socket*, ...>`、`Map<bNode*, ...>` 都吃这个红利。

**注意我此前讲 VectorSet 时说"Map 存哈希副本"——实测不成立**：两种 Map 槽都没有 `stored_hash_` 字段，与 VectorSet 同为"比较时现算"。存哈希副本的路线在本工作树的 `BLI_concurrent_set/map` 等并发容器里，不在 Map 主线。

## 4. 增删查动线

- **add/lookup/remove 的探测循环与 VectorSet 完全同构**（`hash & mask` 起、墓碑跳过、空槽终止）——`BLI_hash_tables.hh` 是两者的公共底座；
- **remove_contained**（`BLI_map.hh` L387-394）：`slot.remove(); removed_slots_++;` 两行完事——**没有末尾补位**，因为没有下标要维护。这是单容器路线意外的简洁红利；
- **异型键查找**：`lookup_ptr_as<ForwardKey>`（L508-528）支持用 `StringRef` 直查字符串键 Map，与 VectorSet 的 `CustomIDHash` 同思路但内建（`_as` 后缀族），不需要额外适配器。

## 5. 内存账（Key=int, Value=float）

| 元素数 | 槽 total | 槽表 | 内联？ |
| --- | --- | --- | --- |
| ≤4 | 8 | 8×12B ≈ 96B | ✅ 零堆 |
| 5 | 16 | 192B | ❌ 槽表转堆 |

对比 VectorSet 同键数：槽 8 字节/个但多一条 `keys_` 数组。**键小值小时 Map 更省；键值大时（≥100B）Map 放弃内联更早**。

## 6. 图解页与架构图

- [06b_Map_内存布局_图解.html](06b_Map_内存布局_图解.html) —— Map 字节级布局（对象头/双槽型/动线/内存账）
- [06b_Set_内存布局_图解.html](06b_Set_内存布局_图解.html) —— Set 字节级布局（与 Map 的精确差异全表/字符串键特化）
- [diagrams/06b1_Map_架构图.html](diagrams/06b1_Map_架构图.html) —— Map 详细架构图（add 家族语义表 / CPython 探测 / 双槽型）
- [diagrams/06b2_Set_架构图.html](diagrams/06b2_Set_架构图.html) —— Set 详细架构图（槽选择谱系 / HashedSetSlot 哈希副本 / 三容器谱系）
## 7. Repeat 中的落点

| 代码 | 类型 | 为什么用 Map 而非 VectorSet |
| --- | --- | --- |
| `group_node_map: Map<int, lf::FunctionNode *>`（NOD_geometry_nodes_lazy_function.hh L365） | 指针键 → Intrusive 槽 | 组节点 id 反查，遍历无意义 |
| `nodes_by_context: MultiValueMap<...>`（L150） | MultiValueMap = Map<K,Vector<V>> 语法糖 | 一键多值（多 Viewer 路径并集） |
| `iterations_by_iteration_zone`（L155） | 同上 | Repeat 副作用表的载体（正篇 04-03） |

## 继续阅读

- [06a_VectorSet_深度解析.md](06a_VectorSet_深度解析.md) —— 双容器路线（本篇的对照面）
- [06_Map_Set.md](06_Map_Set.md) —— 接口全表与用法
- [17_Allocator_深度解析.md](17_Allocator_深度解析.md) —— Allocator 模板参数
