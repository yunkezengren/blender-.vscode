# 实现依赖专题：source/blender/makesdna/DNA_array_utils.hh

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::dna::array::remove_index"]:::abstraction
  F1["blender::dna::array::clear"]:::compute
  F2["blender::dna::array::move_index"]:::compute
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  C["调用者提供参数与有效对象"]:::input
  F["DNA_array_utils.hh实现"]:::compute
  R["结果与被修改状态"]:::result
  C -->|"进入"| F
  F -->|"返回或提交"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  T["具体类型与模板实参"]:::abstraction
  B["分支与构建条件"]:::data
  I["匹配的实现"]:::compute
  E["标准库或系统契约边界"]:::result
  T -->|"静态选择"| I
  B -->|"配置选择"| I
  I -->|"到达外部接口"| E
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  S["完整源码单元"]:::input
  A["教学注释与推导"]:::abstraction
  D["被调用实现专题"]:::compute
  V["原文与token一致性检查"]:::result
  S -->|"就近阅读"| A
  A -->|"继续深入"| D
  A -->|"核对"| V
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

## 完整成员与函数实现

<a id="f-edce13296305a40f"></a>

### `blender::dna::array::remove_index`

实现位置：[source/blender/makesdna/DNA_array_utils.hh](../../../../../../../source/blender/makesdna/DNA_array_utils.hh) · L26—L55。

接口参数：

- `T **items`
- `int *items_num`
- `int *active_index`
- `const int index`
- `void (*destruct_item)(T *)`
- `T *`

**教学注释版**

<!-- annotated:e773fdc125c3b0 -->

```cpp
template<typename T>
inline void remove_index(
    T **items, int *items_num, int *active_index, const int index, void (*destruct_item)(T *))
{
  static_assert(std::is_trivially_copyable_v<T>);
  BLI_assert(index >= 0);
  BLI_assert(index < *items_num);

  const int old_items_num = *items_num;
  const int new_items_num = old_items_num - 1;

  T *old_items = *items;
  T *new_items = MEM_new_array<T>(new_items_num, __func__);

  std::copy_n(old_items, index, new_items);
  std::copy_n(old_items + index + 1, old_items_num - index - 1, new_items + index);

  destruct_item(&old_items[index]);
  MEM_delete(old_items);

  *items = new_items;
  *items_num = new_items_num;

  if (active_index) {
    const int old_active_index = active_index ? *active_index : 0;
    // [讲解] std::max：按比较关系选取较大值。本讲解中的增长公式同时满足最低请求和几何增长；若保存返回引用，还需注意实参寿命。
    const int new_active_index = std::max(
        0, old_active_index == new_items_num ? new_items_num - 1 : old_active_index);
    *active_index = new_active_index;
  }
}
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_array_utils.hh · L26—L55</summary>

<!-- original:e773fdc125c3b0:source/blender/makesdna/DNA_array_utils.hh:26:55 -->

```cpp
template<typename T>
inline void remove_index(
    T **items, int *items_num, int *active_index, const int index, void (*destruct_item)(T *))
{
  static_assert(std::is_trivially_copyable_v<T>);
  BLI_assert(index >= 0);
  BLI_assert(index < *items_num);

  const int old_items_num = *items_num;
  const int new_items_num = old_items_num - 1;

  T *old_items = *items;
  T *new_items = MEM_new_array<T>(new_items_num, __func__);

  std::copy_n(old_items, index, new_items);
  std::copy_n(old_items + index + 1, old_items_num - index - 1, new_items + index);

  destruct_item(&old_items[index]);
  MEM_delete(old_items);

  *items = new_items;
  *items_num = new_items_num;

  if (active_index) {
    const int old_active_index = active_index ? *active_index : 0;
    const int new_active_index = std::max(
        0, old_active_index == new_items_num ? new_items_num - 1 : old_active_index);
    *active_index = new_active_index;
  }
}
```

</details>

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `MEM_new_array<T>` → [MEM_new_array · L372](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-56b8fe3d391af460)。
- `std::copy_n` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `destruct_item` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L43。
- `MEM_delete` → [MEM_delete · L400](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
- `std::max` → [外部契约](https://eel.is/c++draft/alg.min.max)：按比较关系选取较大值。本讲解中的增长公式同时满足最低请求和几何增长；若保存返回引用，还需注意实参寿命。

<a id="f-7c1eed21b7767301"></a>

### `blender::dna::array::clear`

实现位置：[source/blender/makesdna/DNA_array_utils.hh](../../../../../../../source/blender/makesdna/DNA_array_utils.hh) · L82—L94。

接口参数：

- `T **items`
- `int *items_num`
- `int *active_index`
- `void (*destruct_item)(T *)`
- `T *`

**教学注释版**

<!-- annotated:0a8113fe998d59 -->

```cpp
template<typename T>
inline void clear(T **items, int *items_num, int *active_index, void (*destruct_item)(T *))
{
  static_assert(std::is_trivially_copyable_v<T>);
  for (const int i : IndexRange(*items_num)) {
    destruct_item(&(*items)[i]);
  }
  MEM_SAFE_DELETE(*items);
  *items_num = 0;
  if (active_index) {
    *active_index = 0;
  }
}
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_array_utils.hh · L82—L94</summary>

<!-- original:0a8113fe998d59:source/blender/makesdna/DNA_array_utils.hh:82:94 -->

```cpp
template<typename T>
inline void clear(T **items, int *items_num, int *active_index, void (*destruct_item)(T *))
{
  static_assert(std::is_trivially_copyable_v<T>);
  for (const int i : IndexRange(*items_num)) {
    destruct_item(&(*items)[i]);
  }
  MEM_SAFE_DELETE(*items);
  *items_num = 0;
  if (active_index) {
    *active_index = 0;
  }
}
```

</details>

**继续追踪实现**

- `IndexRange` → [blender::IndexRange](../../01-BLI基础库/BLI_index_range.hh.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](../gpu/shader_tool/utils.hh.md#t-82d2bd4ea71c)；[blender::IndexRange](DNA_node_types.h.md#t-0448cc889d39)。
- `destruct_item` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L87。
- `MEM_SAFE_DELETE` → [MEM_SAFE_DELETE · L436](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#m-eadb3bc5b902)。宏定义由构建条件选择。

<a id="f-df5f0d61d8df196c"></a>

### `blender::dna::array::move_index`

实现位置：[source/blender/makesdna/DNA_array_utils.hh](../../../../../../../source/blender/makesdna/DNA_array_utils.hh) · L99—L127。

接口参数：

- `T *items`
- `const int items_num`
- `const int from_index`
- `const int to_index`

**教学注释版**

<!-- annotated:05d66c1922cb81 -->

```cpp
template<typename T>
inline void move_index(T *items, const int items_num, const int from_index, const int to_index)
{
  static_assert(std::is_trivially_copyable_v<T>);
  BLI_assert(from_index >= 0);
  BLI_assert(from_index < items_num);
  BLI_assert(to_index >= 0);
  BLI_assert(to_index < items_num);
  UNUSED_VARS_NDEBUG(items_num);

  if (from_index == to_index) {
    return;
  }

  if (from_index < to_index) {
    const T tmp = items[from_index];
    for (int i = from_index; i < to_index; i++) {
      items[i] = items[i + 1];
    }
    items[to_index] = tmp;
  }
  else if (from_index > to_index) {
    const T tmp = items[from_index];
    for (int i = from_index; i > to_index; i--) {
      items[i] = items[i - 1];
    }
    items[to_index] = tmp;
  }
}
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_array_utils.hh · L99—L127</summary>

<!-- original:05d66c1922cb81:source/blender/makesdna/DNA_array_utils.hh:99:127 -->

```cpp
template<typename T>
inline void move_index(T *items, const int items_num, const int from_index, const int to_index)
{
  static_assert(std::is_trivially_copyable_v<T>);
  BLI_assert(from_index >= 0);
  BLI_assert(from_index < items_num);
  BLI_assert(to_index >= 0);
  BLI_assert(to_index < items_num);
  UNUSED_VARS_NDEBUG(items_num);

  if (from_index == to_index) {
    return;
  }

  if (from_index < to_index) {
    const T tmp = items[from_index];
    for (int i = from_index; i < to_index; i++) {
      items[i] = items[i + 1];
    }
    items[to_index] = tmp;
  }
  else if (from_index > to_index) {
    const T tmp = items[from_index];
    for (int i = from_index; i > to_index; i--) {
      items[i] = items[i - 1];
    }
    items[to_index] = tmp;
  }
}
```

</details>

**沿实际写入检查状态**

- `items[i] = items[i + 1];`
- `items[to_index] = tmp;`
- `items[i] = items[i - 1];`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `UNUSED_VARS_NDEBUG` → [UNUSED_VARS_NDEBUG · L526](../../01-BLI基础库/BLI_utildefines.hh.md#m-fea439f7d366)；[UNUSED_VARS_NDEBUG · L528](../../01-BLI基础库/BLI_utildefines.hh.md#m-a8f8cfac06c0)。宏定义由构建条件选择。
