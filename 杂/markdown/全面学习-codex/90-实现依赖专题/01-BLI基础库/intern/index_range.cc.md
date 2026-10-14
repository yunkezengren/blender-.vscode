# 实现依赖专题：source/blender/blenlib/intern/index_range.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::split_index_range_by_alignment"]:::abstraction
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
  F["index_range.cc实现"]:::compute
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

<a id="f-2d9a3529ce0f2331"></a>

### `blender::split_index_range_by_alignment`

实现位置：[source/blender/blenlib/intern/index_range.cc](../../../../../../../source/blender/blenlib/intern/index_range.cc) · L16—L44。

接口参数：

- `const IndexRange range`
- `const int64_t alignment`

**教学注释版**

<!-- annotated:1858dc2c6f612c -->

```cpp
AlignedIndexRanges split_index_range_by_alignment(const IndexRange range, const int64_t alignment)
{
  BLI_assert(is_power_of_2(alignment));
  const int64_t mask = alignment - 1;

  AlignedIndexRanges aligned_ranges;

  // [讲解] range.start：读取连续区间或分组的边界信息。
  const int64_t start_chunk = range.start() & ~mask;
  // [讲解] range.one_after_last：读取连续区间或分组的边界信息。
  const int64_t end_chunk = range.one_after_last() & ~mask;
  if (start_chunk == end_chunk) {
    aligned_ranges.prefix = range;
  }
  else {
    int64_t prefix_size = 0;
    int64_t suffix_size = 0;
    if (range.start() != start_chunk) {
      prefix_size = alignment - (range.start() & mask);
    }
    if (range.one_after_last() != end_chunk) {
      suffix_size = range.one_after_last() - end_chunk;
    }
    aligned_ranges.prefix = IndexRange(range.start(), prefix_size);
    aligned_ranges.suffix = IndexRange(end_chunk, suffix_size);
    aligned_ranges.aligned = IndexRange(aligned_ranges.prefix.one_after_last(),
                                        // [讲解] range.size：读取连续区间或分组的边界信息。
                                        range.size() - prefix_size - suffix_size);
  }

  return aligned_ranges;
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/index_range.cc · L16—L44</summary>

<!-- original:1858dc2c6f612c:source/blender/blenlib/intern/index_range.cc:16:44 -->

```cpp
AlignedIndexRanges split_index_range_by_alignment(const IndexRange range, const int64_t alignment)
{
  BLI_assert(is_power_of_2(alignment));
  const int64_t mask = alignment - 1;

  AlignedIndexRanges aligned_ranges;

  const int64_t start_chunk = range.start() & ~mask;
  const int64_t end_chunk = range.one_after_last() & ~mask;
  if (start_chunk == end_chunk) {
    aligned_ranges.prefix = range;
  }
  else {
    int64_t prefix_size = 0;
    int64_t suffix_size = 0;
    if (range.start() != start_chunk) {
      prefix_size = alignment - (range.start() & mask);
    }
    if (range.one_after_last() != end_chunk) {
      suffix_size = range.one_after_last() - end_chunk;
    }
    aligned_ranges.prefix = IndexRange(range.start(), prefix_size);
    aligned_ranges.suffix = IndexRange(end_chunk, suffix_size);
    aligned_ranges.aligned = IndexRange(aligned_ranges.prefix.one_after_last(),
                                        range.size() - prefix_size - suffix_size);
  }

  return aligned_ranges;
}
```

</details>

**沿实际写入检查状态**

- `aligned_ranges.prefix = range;`
- `prefix_size = alignment - (range.start() & mask);`
- `suffix_size = range.one_after_last() - end_chunk;`
- `aligned_ranges.prefix = IndexRange(range.start(), prefix_size);`
- `aligned_ranges.suffix = IndexRange(end_chunk, suffix_size);`
- `aligned_ranges.aligned = IndexRange(aligned_ranges.prefix.one_after_last(),`

**结果出口**

- `return aligned_ranges;`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `is_power_of_2` → [blender::is_power_of_2 · L170](../BLI_utildefines.hh.md#f-276f4f171955e1e9)。
- `range.start` → [blender::IndexRange::start · L243](../../../01-基础容器与现代CPP/04-IndexRange连续整数区间.md#f-99d2195bd9cfd1f0)。
- `range.one_after_last` → [blender::IndexRange::one_after_last · L235](../../../01-基础容器与现代CPP/04-IndexRange连续整数区间.md#f-ed04bec9c731fc86)。
- `IndexRange` → [blender::IndexRange](../BLI_index_range.hh.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](../../08-其他Blender模块/gpu/shader_tool/utils.hh.md#t-82d2bd4ea71c)；[blender::IndexRange](../../08-其他Blender模块/makesdna/DNA_node_types.h.md#t-0448cc889d39)。
- `aligned_ranges.prefix.one_after_last` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L39。
- `range.size` → [blender::IndexRange::size · L156](../../../01-基础容器与现代CPP/04-IndexRange连续整数区间.md#f-05f66c3ebb2fdfec)。
