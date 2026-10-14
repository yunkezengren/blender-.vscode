# 实现依赖专题：source/blender/blenlib/intern/length_parameterize.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::length_parameterize::sample_uniform"]:::abstraction
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
  F["length_parameterize.cc实现"]:::compute
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

<a id="f-f8dff656792f6adb"></a>

### `blender::length_parameterize::sample_uniform`

实现位置：[source/blender/blenlib/intern/length_parameterize.cc](../../../../../../../source/blender/blenlib/intern/length_parameterize.cc) · L15—L42。

接口参数：

- `const Span<float> accumulated_segment_lengths`
- `const bool include_last_point`
- `MutableSpan<int> r_segment_indices`
- `MutableSpan<float> r_factors`

**教学注释版**

<!-- annotated:bee37dcc5141f8 -->

```cpp
void sample_uniform(const Span<float> accumulated_segment_lengths,
                    const bool include_last_point,
                    MutableSpan<int> r_segment_indices,
                    MutableSpan<float> r_factors)
{
  // [讲解] r_segment_indices.size：查询视图长度或生成对应有效索引区间。
  const int count = r_segment_indices.size();
  BLI_assert(count > 0);
  BLI_assert(accumulated_segment_lengths.size() >= 1);
  BLI_assert(
      // [讲解] accumulated_segment_lengths.begin：返回借用范围的地址。
      std::is_sorted(accumulated_segment_lengths.begin(), accumulated_segment_lengths.end()));

  if (count == 1) {
    r_segment_indices[0] = 0;
    r_factors[0] = 0.0f;
    return;
  }
  // [讲解] accumulated_segment_lengths.last：按视图边界访问元素。
  const float total_length = accumulated_segment_lengths.last();
  const float step_length = total_length / (count - include_last_point);
  threading::parallel_for(IndexRange(count), 512, [&](const IndexRange range) {
    SampleSegmentHint hint;
    for (const int i : range) {
      /* Use minimum to avoid issues with floating point accuracy. */
      // [讲解] std::min：按比较关系选取较小值；截断范围时还需先满足非负和可表示范围，min本身不会证明边界安全。
      const float sample_length = std::min(total_length, i * step_length);
      sample_at_length(
          accumulated_segment_lengths, sample_length, r_segment_indices[i], r_factors[i], &hint);
    }
  });
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/length_parameterize.cc · L15—L42</summary>

<!-- original:bee37dcc5141f8:source/blender/blenlib/intern/length_parameterize.cc:15:42 -->

```cpp
void sample_uniform(const Span<float> accumulated_segment_lengths,
                    const bool include_last_point,
                    MutableSpan<int> r_segment_indices,
                    MutableSpan<float> r_factors)
{
  const int count = r_segment_indices.size();
  BLI_assert(count > 0);
  BLI_assert(accumulated_segment_lengths.size() >= 1);
  BLI_assert(
      std::is_sorted(accumulated_segment_lengths.begin(), accumulated_segment_lengths.end()));

  if (count == 1) {
    r_segment_indices[0] = 0;
    r_factors[0] = 0.0f;
    return;
  }
  const float total_length = accumulated_segment_lengths.last();
  const float step_length = total_length / (count - include_last_point);
  threading::parallel_for(IndexRange(count), 512, [&](const IndexRange range) {
    SampleSegmentHint hint;
    for (const int i : range) {
      /* Use minimum to avoid issues with floating point accuracy. */
      const float sample_length = std::min(total_length, i * step_length);
      sample_at_length(
          accumulated_segment_lengths, sample_length, r_segment_indices[i], r_factors[i], &hint);
    }
  });
}
```

</details>

**沿实际写入检查状态**

- `r_segment_indices[0] = 0;`
- `r_factors[0] = 0.0f;`

**继续追踪实现**

- `r_segment_indices.size` → [blender::MutableSpan::size · L499](../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-1de6a66839c304a8)；[blender::gpu::shader::parser::MutableSpan::size · L87](../../08-其他Blender模块/gpu/shader_tool/utils.hh.md#f-5e684af6ee7990e9)。同名重载需按实参类型选择。
- `BLI_assert` → [BLI_assert · L48](../BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `accumulated_segment_lengths.size` → [blender::Span::size · L256](../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-5f80fa006089c998)。
- `std::is_sorted` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `accumulated_segment_lengths.begin` → [blender::Span::begin · L224](../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-415883b512284f46)。
- `accumulated_segment_lengths.end` → [blender::Span::end · L228](../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-a7d8b9e494c291a7)。
- `accumulated_segment_lengths.last` → [blender::Span::last · L329](../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-a92146c285596891)。
- `threading::parallel_for` → [blender::threading::parallel_for · L68](../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-838294754c24426c)。
- `IndexRange` → [blender::IndexRange](../BLI_index_range.hh.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](../../08-其他Blender模块/gpu/shader_tool/utils.hh.md#t-82d2bd4ea71c)；[blender::IndexRange](../../08-其他Blender模块/makesdna/DNA_node_types.h.md#t-0448cc889d39)。
- `std::min` → [外部契约](https://eel.is/c++draft/alg.min.max)：按比较关系选取较小值；截断范围时还需先满足非负和可表示范围，min本身不会证明边界安全。
- `sample_at_length` → [blender::length_parameterize::sample_at_length · L97](../BLI_length_parameterize.hh.md#f-4f136286e9947282)。
