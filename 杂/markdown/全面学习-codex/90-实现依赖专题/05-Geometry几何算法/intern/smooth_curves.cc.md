# 实现依赖专题：source/blender/geometry/intern/smooth_curves.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::geometry::gaussian_blur_1D"]:::abstraction
  F1["blender::geometry::gaussian_blur_1D"]:::compute
  F2["blender::geometry::smooth_curve_attribute"]:::compute
  F3["blender::geometry::smooth_curve_attribute"]:::compute
  F1 -->|"显式调用"| F0
  F1 -->|"显式调用"| F1
  F2 -->|"显式调用"| F0
  F2 -->|"显式调用"| F1
  F3 -->|"显式调用"| F2
  F3 -->|"显式调用"| F3
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
  F["smooth_curves.cc实现"]:::compute
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

<a id="f-7e3f1bb47a09fed9"></a>

### `blender::geometry::gaussian_blur_1D`

实现位置：[source/blender/geometry/intern/smooth_curves.cc](../../../../../../../source/blender/geometry/intern/smooth_curves.cc) · L24—L152。

接口参数：

- `const Span<T> src`
- `const int iterations`
- `const VArray<float> &influence_by_point`
- `const bool smooth_ends`
- `const bool keep_shape`
- `const bool is_cyclic`
- `MutableSpan<T> dst`

**教学注释版**

<!-- annotated:5654c2fec1ea88 -->

```cpp
template<typename T>
static void gaussian_blur_1D(const Span<T> src,
                             const int iterations,
                             const VArray<float> &influence_by_point,
                             const bool smooth_ends,
                             const bool keep_shape,
                             const bool is_cyclic,
                             MutableSpan<T> dst)
{
  /**
   * 1D Gaussian-like smoothing function.
   *
   * NOTE: This is the algorithm used by #BKE_gpencil_stroke_smooth_point (legacy),
   *       but generalized and written in C++.
   *
   * This function uses a binomial kernel, which is the discrete version of gaussian blur.
   * The weight for a value at the relative index is:
   * `w = nCr(n, j + n/2) / 2^n = (n/1 * (n-1)/2 * ... * (n-j-n/2)/(j+n/2)) / 2^n`.
   * All weights together sum up to 1.
   * This is equivalent to doing multiple iterations of averaging neighbors,
   * where: `n = iterations * 2 and -n/2 <= j <= n/2`.
   *
   * Now the problem is that `nCr(n, j + n/2)` is very hard to compute for `n > 500`, since even
   * double precision isn't sufficient. A very good robust approximation for `n > 20` is:
   * `nCr(n, j + n/2) / 2^n = sqrt(2/(pi*n)) * exp(-2*j*j/n)`.
   *
   * `keep_shape` is a new option to stop the points from severely deforming.
   * It uses different partially negative weights.
   * `w = 2 * (nCr(n, j + n/2) / 2^n) - (nCr(3*n, j + n) / 2^(3*n))`
   * `  ~ 2 * sqrt(2/(pi*n)) * exp(-2*j*j/n) - sqrt(2/(pi*3*n)) * exp(-2*j*j/(3*n))`
   * All weights still sum up to 1.
   * Note that these weights only work because the averaging is done in relative coordinates.
   */

  // [讲解] src.is_empty：查询视图长度或生成对应有效索引区间。
  BLI_assert(!src.is_empty());
  // [讲解] src.size：查询视图长度或生成对应有效索引区间。
  BLI_assert(src.size() == dst.size());

  /* Avoid computation if there is just one point. */
  if (src.size() == 1) {
    return;
  }

  /* Weight Initialization. */
  const int n_half = keep_shape ? (iterations * iterations) / 8 + iterations :
                                  (iterations * iterations) / 4 + 2 * iterations + 12;
  double w = keep_shape ? 2.0 : 1.0;
  double w2 = keep_shape ?
                  (1.0 / M_SQRT3) * exp((2 * iterations * iterations) / double(n_half * 3)) :
                  0.0;
  Array<double> total_weight(src.size(), 0.0);

  const int64_t total_points = src.size();
  const int64_t last_pt = total_points - 1;

  auto is_end_and_fixed = [smooth_ends, is_cyclic, last_pt](int index) {
    return !smooth_ends && !is_cyclic && ELEM(index, 0, last_pt);
  };

  /* Initialize at zero. */
  // [讲解] dst.index_range：查询视图长度或生成对应有效索引区间。
  threading::parallel_for(dst.index_range(), 1024, [&](const IndexRange range) {
    for (const int64_t index : range) {
      if (!is_end_and_fixed(index)) {
        dst[index] = T(0);
      }
    }
  });

  /* Compute weights. */
  for (const int64_t step : IndexRange(iterations)) {
    const int64_t offset = iterations - step;
    threading::parallel_for(dst.index_range(), 1024, [&](const IndexRange range) {
      for (const int64_t index : range) {
        /* Filter out endpoints. */
        if (is_end_and_fixed(index)) {
          continue;
        }

        double w_before = w - w2;
        double w_after = w - w2;

        /* Compute the neighboring points. */
        int64_t before = index - offset;
        int64_t after = index + offset;
        if (is_cyclic) {
          before = (before % total_points + total_points) % total_points;
          after = after % total_points;
        }
        else {
          if (!smooth_ends && (before < 0)) {
            w_before *= -before / float(index);
          }
          before = math::max(before, int64_t(0));

          if (!smooth_ends && (after > last_pt)) {
            w_after *= (after - (total_points - 1)) / float(total_points - 1 - index);
          }
          after = math::min(after, last_pt);
        }

        /* Add the neighboring values. */
        const T bval = src[before];
        const T aval = src[after];
        const T cval = src[index];

        dst[index] += (bval - cval) * w_before;
        dst[index] += (aval - cval) * w_after;

        /* Update the weight values. */
        total_weight[index] += w_before;
        total_weight[index] += w_after;
      }
    });

    w *= (n_half + offset) / double(n_half + 1 - offset);
    w2 *= (n_half * 3 + offset) / double(n_half * 3 + 1 - offset);
  }

  /* Normalize the weights. */
  devirtualize_varray(influence_by_point, [&](const auto influence_by_point) {
    threading::parallel_for(dst.index_range(), 1024, [&](const IndexRange range) {
      for (const int64_t index : range) {
        if (!is_end_and_fixed(index)) {
          total_weight[index] += w - w2;
          dst[index] = src[index] + influence_by_point[index] * dst[index] / total_weight[index];
        }
      }
    });
  });
}
```

<details>
<summary>核对原始源码：source/blender/geometry/intern/smooth_curves.cc · L24—L152</summary>

<!-- original:5654c2fec1ea88:source/blender/geometry/intern/smooth_curves.cc:24:152 -->

```cpp
template<typename T>
static void gaussian_blur_1D(const Span<T> src,
                             const int iterations,
                             const VArray<float> &influence_by_point,
                             const bool smooth_ends,
                             const bool keep_shape,
                             const bool is_cyclic,
                             MutableSpan<T> dst)
{
  /**
   * 1D Gaussian-like smoothing function.
   *
   * NOTE: This is the algorithm used by #BKE_gpencil_stroke_smooth_point (legacy),
   *       but generalized and written in C++.
   *
   * This function uses a binomial kernel, which is the discrete version of gaussian blur.
   * The weight for a value at the relative index is:
   * `w = nCr(n, j + n/2) / 2^n = (n/1 * (n-1)/2 * ... * (n-j-n/2)/(j+n/2)) / 2^n`.
   * All weights together sum up to 1.
   * This is equivalent to doing multiple iterations of averaging neighbors,
   * where: `n = iterations * 2 and -n/2 <= j <= n/2`.
   *
   * Now the problem is that `nCr(n, j + n/2)` is very hard to compute for `n > 500`, since even
   * double precision isn't sufficient. A very good robust approximation for `n > 20` is:
   * `nCr(n, j + n/2) / 2^n = sqrt(2/(pi*n)) * exp(-2*j*j/n)`.
   *
   * `keep_shape` is a new option to stop the points from severely deforming.
   * It uses different partially negative weights.
   * `w = 2 * (nCr(n, j + n/2) / 2^n) - (nCr(3*n, j + n) / 2^(3*n))`
   * `  ~ 2 * sqrt(2/(pi*n)) * exp(-2*j*j/n) - sqrt(2/(pi*3*n)) * exp(-2*j*j/(3*n))`
   * All weights still sum up to 1.
   * Note that these weights only work because the averaging is done in relative coordinates.
   */

  BLI_assert(!src.is_empty());
  BLI_assert(src.size() == dst.size());

  /* Avoid computation if there is just one point. */
  if (src.size() == 1) {
    return;
  }

  /* Weight Initialization. */
  const int n_half = keep_shape ? (iterations * iterations) / 8 + iterations :
                                  (iterations * iterations) / 4 + 2 * iterations + 12;
  double w = keep_shape ? 2.0 : 1.0;
  double w2 = keep_shape ?
                  (1.0 / M_SQRT3) * exp((2 * iterations * iterations) / double(n_half * 3)) :
                  0.0;
  Array<double> total_weight(src.size(), 0.0);

  const int64_t total_points = src.size();
  const int64_t last_pt = total_points - 1;

  auto is_end_and_fixed = [smooth_ends, is_cyclic, last_pt](int index) {
    return !smooth_ends && !is_cyclic && ELEM(index, 0, last_pt);
  };

  /* Initialize at zero. */
  threading::parallel_for(dst.index_range(), 1024, [&](const IndexRange range) {
    for (const int64_t index : range) {
      if (!is_end_and_fixed(index)) {
        dst[index] = T(0);
      }
    }
  });

  /* Compute weights. */
  for (const int64_t step : IndexRange(iterations)) {
    const int64_t offset = iterations - step;
    threading::parallel_for(dst.index_range(), 1024, [&](const IndexRange range) {
      for (const int64_t index : range) {
        /* Filter out endpoints. */
        if (is_end_and_fixed(index)) {
          continue;
        }

        double w_before = w - w2;
        double w_after = w - w2;

        /* Compute the neighboring points. */
        int64_t before = index - offset;
        int64_t after = index + offset;
        if (is_cyclic) {
          before = (before % total_points + total_points) % total_points;
          after = after % total_points;
        }
        else {
          if (!smooth_ends && (before < 0)) {
            w_before *= -before / float(index);
          }
          before = math::max(before, int64_t(0));

          if (!smooth_ends && (after > last_pt)) {
            w_after *= (after - (total_points - 1)) / float(total_points - 1 - index);
          }
          after = math::min(after, last_pt);
        }

        /* Add the neighboring values. */
        const T bval = src[before];
        const T aval = src[after];
        const T cval = src[index];

        dst[index] += (bval - cval) * w_before;
        dst[index] += (aval - cval) * w_after;

        /* Update the weight values. */
        total_weight[index] += w_before;
        total_weight[index] += w_after;
      }
    });

    w *= (n_half + offset) / double(n_half + 1 - offset);
    w2 *= (n_half * 3 + offset) / double(n_half * 3 + 1 - offset);
  }

  /* Normalize the weights. */
  devirtualize_varray(influence_by_point, [&](const auto influence_by_point) {
    threading::parallel_for(dst.index_range(), 1024, [&](const IndexRange range) {
      for (const int64_t index : range) {
        if (!is_end_and_fixed(index)) {
          total_weight[index] += w - w2;
          dst[index] = src[index] + influence_by_point[index] * dst[index] / total_weight[index];
        }
      }
    });
  });
}
```

</details>

**沿实际写入检查状态**

- `dst[index] = T(0);`
- `before = (before % total_points + total_points) % total_points;`
- `after = after % total_points;`
- `w_before *= -before / float(index);`
- `before = math::max(before, int64_t(0));`
- `w_after *= (after - (total_points - 1)) / float(total_points - 1 - index);`
- `after = math::min(after, last_pt);`
- `dst[index] += (bval - cval) * w_before;`
- `dst[index] += (aval - cval) * w_after;`
- `total_weight[index] += w_before;`
- `total_weight[index] += w_after;`
- `w *= (n_half + offset) / double(n_half + 1 - offset);`
- `w2 *= (n_half * 3 + offset) / double(n_half * 3 + 1 - offset);`
- `total_weight[index] += w - w2;`
- `dst[index] = src[index] + influence_by_point[index] * dst[index] / total_weight[index];`

**结果出口**

- `return !smooth_ends && !is_cyclic && ELEM(index, 0, last_pt);`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `src.is_empty` → [blender::Span::is_empty · L264](../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-8cc1d7ba8feb50e6)。
- `src.size` → [blender::Span::size · L256](../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-5f80fa006089c998)。
- `dst.size` → [blender::MutableSpan::size · L499](../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-1de6a66839c304a8)；[blender::gpu::shader::parser::MutableSpan::size · L87](../../08-其他Blender模块/gpu/shader_tool/utils.hh.md#f-5e684af6ee7990e9)。同名重载需按实参类型选择。
- `exp` → [exp · L106](../../08-其他Blender模块/gpu/shaders/compat/gpu_shader_cxx_builtin.hh.md#m-dd7e1d600c32)。宏定义由构建条件选择。
- `ELEM` → [ELEM · L88](../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-d28724a15928)；[ELEM · L135](../../01-BLI基础库/BLI_utildefines.hh.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `threading::parallel_for` → [blender::threading::parallel_for · L68](../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-838294754c24426c)。
- `dst.index_range` → [blender::MutableSpan::index_range · L676](../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-f9a9d59a69ca64b5)。
- `is_end_and_fixed` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L85。
- `T` → [DiagSplit::T · L96](../../07-Intern运行时与平台/cycles/subd/split.cpp.md#f-d5d0885c790cc4e4)。
- `IndexRange` → [blender::IndexRange](../../01-BLI基础库/BLI_index_range.hh.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](../../08-其他Blender模块/gpu/shader_tool/utils.hh.md#t-82d2bd4ea71c)；[blender::IndexRange](../../08-其他Blender模块/makesdna/DNA_node_types.h.md#t-0448cc889d39)。
- `math::max` → [blender::math::max · L87](../../01-BLI基础库/BLI_math_vector.hh.md#f-9be564a293777d6b)；[blender::math::max · L96](../../01-BLI基础库/BLI_math_vector.hh.md#f-ce32dff37d0af3bc)；[blender::math::max · L112](../../01-BLI基础库/BLI_math_vector.hh.md#f-668eb1fcf1fa8292)；[blender::math::max · L49](../../01-BLI基础库/BLI_math_base.hh.md#f-a6991ca3d12937e1)。同名重载需按实参类型选择。
- `math::min` → [blender::math::min · L56](../../01-BLI基础库/BLI_math_vector.hh.md#f-ee6ead51e4bb3364)；[blender::math::min · L65](../../01-BLI基础库/BLI_math_vector.hh.md#f-f65ce48b3051cce3)；[blender::math::min · L81](../../01-BLI基础库/BLI_math_vector.hh.md#f-9c602d29fab41795)；[blender::math::min · L43](../../01-BLI基础库/BLI_math_base.hh.md#f-72ff0c229e6c09b0)。同名重载需按实参类型选择。
- `devirtualize_varray` → [blender::devirtualize_varray · L1183](../../../04-虚拟数组与索引选择/04-所有权与小对象优化.md#f-e8985eebdbe1038a)。

<a id="f-40ea19fbbc8a9189"></a>

### `blender::geometry::gaussian_blur_1D`

实现位置：[source/blender/geometry/intern/smooth_curves.cc](../../../../../../../source/blender/geometry/intern/smooth_curves.cc) · L154—L175。

接口参数：

- `const GSpan src`
- `const int iterations`
- `const VArray<float> &influence_by_point`
- `const bool smooth_ends`
- `const bool keep_shape`
- `const bool is_cyclic`
- `GMutableSpan dst`

**教学注释版**

<!-- annotated:515573cb8ba208 -->

```cpp
void gaussian_blur_1D(const GSpan src,
                      const int iterations,
                      const VArray<float> &influence_by_point,
                      const bool smooth_ends,
                      const bool keep_shape,
                      const bool is_cyclic,
                      GMutableSpan dst)
{
  bke::attribute_math::to_static_type(src.type(), [&]<typename T>() {
    /* Only allow smoothing of float, float2, or float3. */
    /* Reduces unnecessary code generation. */
    if constexpr (is_same_any_v<T, float, float2, float3>) {
      gaussian_blur_1D(src.typed<T>(),
                       iterations,
                       influence_by_point,
                       smooth_ends,
                       keep_shape,
                       is_cyclic,
                       dst.typed<T>());
    }
  });
}
```

<details>
<summary>核对原始源码：source/blender/geometry/intern/smooth_curves.cc · L154—L175</summary>

<!-- original:515573cb8ba208:source/blender/geometry/intern/smooth_curves.cc:154:175 -->

```cpp
void gaussian_blur_1D(const GSpan src,
                      const int iterations,
                      const VArray<float> &influence_by_point,
                      const bool smooth_ends,
                      const bool keep_shape,
                      const bool is_cyclic,
                      GMutableSpan dst)
{
  bke::attribute_math::to_static_type(src.type(), [&]<typename T>() {
    /* Only allow smoothing of float, float2, or float3. */
    /* Reduces unnecessary code generation. */
    if constexpr (is_same_any_v<T, float, float2, float3>) {
      gaussian_blur_1D(src.typed<T>(),
                       iterations,
                       influence_by_point,
                       smooth_ends,
                       keep_shape,
                       is_cyclic,
                       dst.typed<T>());
    }
  });
}
```

</details>

**继续追踪实现**

- `bke::attribute_math::to_static_type` → [blender::bke::attribute_math::to_static_type · L35](../../02-BKE几何与数据/BKE_attribute_math.hh.md#f-fdfaf0b86a24f278)；[blender::bke::attribute_math::to_static_type · L52](../../02-BKE几何与数据/BKE_attribute_math.hh.md#f-5346ade4e816ebd6)。同名重载需按实参类型选择。
- `src.type` → [blender::GSpan::type · L55](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-4c44cc0364dcf191)。
- `gaussian_blur_1D` → [blender::geometry::gaussian_blur_1D · L24](smooth_curves.cc.md#f-7e3f1bb47a09fed9)；[blender::geometry::gaussian_blur_1D · L154](smooth_curves.cc.md#f-40ea19fbbc8a9189)。同名重载需按实参类型选择。
- `src.typed<T>` → [blender::GSpan::typed · L92](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-aa54cf0d7a8dae2b)。
- `dst.typed<T>` → [blender::GMutableSpan::typed · L220](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-d66e288b393f6545)。

<a id="f-501455310c3a0583"></a>

### `blender::geometry::smooth_curve_attribute`

实现位置：[source/blender/geometry/intern/smooth_curves.cc](../../../../../../../source/blender/geometry/intern/smooth_curves.cc) · L177—L228。

接口参数：

- `const IndexMask &curves_to_smooth`
- `const OffsetIndices<int> points_by_curve`
- `const VArray<bool> &point_selection`
- `const VArray<bool> &cyclic`
- `const int iterations`
- `const VArray<float> &influence_by_point`
- `const bool smooth_ends`
- `const bool keep_shape`
- `GMutableSpan attribute_data`

**教学注释版**

<!-- annotated:fcf893b134b553 -->

```cpp
void smooth_curve_attribute(const IndexMask &curves_to_smooth,
                            const OffsetIndices<int> points_by_curve,
                            const VArray<bool> &point_selection,
                            const VArray<bool> &cyclic,
                            const int iterations,
                            const VArray<float> &influence_by_point,
                            const bool smooth_ends,
                            const bool keep_shape,
                            GMutableSpan attribute_data)
{
  VArraySpan<float> influences(influence_by_point);

  auto smooth_points_range =
      [&](const IndexRange range, const bool cyclic, Vector<std::byte> &orig_data) {
        GMutableSpan dst_data = attribute_data.slice(range);
        // [讲解] orig_data.resize：把有效元素数调整为new_size。增长路径构造新元素，缩小路径销毁尾部对象，最后才提交新的end_。
        orig_data.resize(dst_data.size_in_bytes());
        // [讲解] orig_data.data：提供当前存储或有效范围的地址。
        dst_data.type().copy_assign_n(dst_data.data(), orig_data.data(), range.size());
        // [讲解] range.size：读取连续区间或分组的边界信息。
        const GSpan src_data(dst_data.type(), orig_data.data(), range.size());

        gaussian_blur_1D(src_data,
                         iterations,
                         VArray<float>::from_span(influences.slice(range)),
                         smooth_ends,
                         keep_shape,
                         cyclic,
                         dst_data);
      };

  curves_to_smooth.foreach_index(
      [&](const int curve_i) {
        Vector<std::byte> orig_data;
        const IndexRange points = points_by_curve[curve_i];

        IndexMaskMemory memory;
        const IndexMask selection_mask = IndexMask::from_bools(points, point_selection, memory);
        if (selection_mask.is_empty()) {
          return;
        }

        const std::optional<IndexRange> selection_range = selection_mask.to_range();
        if (selection_range && *selection_range == points) {
          smooth_points_range(points, cyclic[curve_i], orig_data);
        }
        else {
          selection_mask.foreach_range([&](const IndexRange range) {
            /* Individual ranges should be treated as non-cyclic. */
            smooth_points_range(range, false, orig_data);
          });
        }
      },
      exec_mode::grain_size(512));
}
```

<details>
<summary>核对原始源码：source/blender/geometry/intern/smooth_curves.cc · L177—L228</summary>

<!-- original:fcf893b134b553:source/blender/geometry/intern/smooth_curves.cc:177:228 -->

```cpp
void smooth_curve_attribute(const IndexMask &curves_to_smooth,
                            const OffsetIndices<int> points_by_curve,
                            const VArray<bool> &point_selection,
                            const VArray<bool> &cyclic,
                            const int iterations,
                            const VArray<float> &influence_by_point,
                            const bool smooth_ends,
                            const bool keep_shape,
                            GMutableSpan attribute_data)
{
  VArraySpan<float> influences(influence_by_point);

  auto smooth_points_range =
      [&](const IndexRange range, const bool cyclic, Vector<std::byte> &orig_data) {
        GMutableSpan dst_data = attribute_data.slice(range);
        orig_data.resize(dst_data.size_in_bytes());
        dst_data.type().copy_assign_n(dst_data.data(), orig_data.data(), range.size());
        const GSpan src_data(dst_data.type(), orig_data.data(), range.size());

        gaussian_blur_1D(src_data,
                         iterations,
                         VArray<float>::from_span(influences.slice(range)),
                         smooth_ends,
                         keep_shape,
                         cyclic,
                         dst_data);
      };

  curves_to_smooth.foreach_index(
      [&](const int curve_i) {
        Vector<std::byte> orig_data;
        const IndexRange points = points_by_curve[curve_i];

        IndexMaskMemory memory;
        const IndexMask selection_mask = IndexMask::from_bools(points, point_selection, memory);
        if (selection_mask.is_empty()) {
          return;
        }

        const std::optional<IndexRange> selection_range = selection_mask.to_range();
        if (selection_range && *selection_range == points) {
          smooth_points_range(points, cyclic[curve_i], orig_data);
        }
        else {
          selection_mask.foreach_range([&](const IndexRange range) {
            /* Individual ranges should be treated as non-cyclic. */
            smooth_points_range(range, false, orig_data);
          });
        }
      },
      exec_mode::grain_size(512));
}
```

</details>

**继续追踪实现**

- `attribute_data.slice` → [blender::GMutableSpan::slice · L227](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-d7f8e350bc3a5156)；[blender::GMutableSpan::slice · L235](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-b1101d4d9009fa75)。同名重载需按实参类型选择。
- `orig_data.resize` → [blender::Vector::resize · L418](../../../01-基础容器与现代CPP/10-Vector扩容与增长.md#f-059312cabb8abe3a)；[blender::Vector::resize · L439](../../../01-基础容器与现代CPP/10-Vector扩容与增长.md#f-ab8f94924ebe2d12)。同名重载需按实参类型选择。
- `dst_data.size_in_bytes` → [blender::GMutableSpan::size_in_bytes · L203](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-78ac72dc14caccbc)。
- `dst_data.type().copy_assign_n` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L193。
- `dst_data.type` → [blender::GMutableSpan::type · L182](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-74385040046c86d5)。
- `dst_data.data` → [blender::GMutableSpan::data · L208](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-f951536a0bdbb159)。
- `orig_data.data` → [blender::Vector::data · L954](../../../01-基础容器与现代CPP/12-Vector异常安全与边界.md#f-6e441591404715bc)；[blender::Vector::data · L962](../../../01-基础容器与现代CPP/12-Vector异常安全与边界.md#f-4bc78d4954c1021a)。同名重载需按实参类型选择。
- `range.size` → [blender::IndexRange::size · L156](../../../01-基础容器与现代CPP/04-IndexRange连续整数区间.md#f-05f66c3ebb2fdfec)。
- `gaussian_blur_1D` → [blender::geometry::gaussian_blur_1D · L24](smooth_curves.cc.md#f-7e3f1bb47a09fed9)；[blender::geometry::gaussian_blur_1D · L154](smooth_curves.cc.md#f-40ea19fbbc8a9189)。同名重载需按实参类型选择。
- `VArray<float>::from_span` → [blender::GVArray::from_span · L895](../../../04-虚拟数组与索引选择/05-GVArray运行时类型.md#f-e8b978ca15febb67)；[blender::VArray::from_span · L768](../../../04-虚拟数组与索引选择/03-单值与Span表示.md#f-d9cf90c7ec1493b6)。同名重载需按实参类型选择。
- `influences.slice` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：由接收对象具体类型或运行时策略提供实现。调用位置L198。
- `curves_to_smooth.foreach_index` → [blender::index_mask::IndexMask::foreach_index · L855](../../../04-虚拟数组与索引选择/09-分段存储与遍历.md#f-cd6cd317e2e2812c)。
- `IndexMask::from_bools` → [blender::index_mask::IndexMask::from_bools · L593](../../../04-虚拟数组与索引选择/10-IndexMask构建与并行.md#f-1eccbfd39b11c6bc)；[blender::index_mask::IndexMask::from_bools · L598](../../../04-虚拟数组与索引选择/10-IndexMask构建与并行.md#f-3962fd5fd5aee616)；[blender::index_mask::IndexMask::from_bools · L613](../../../04-虚拟数组与索引选择/10-IndexMask构建与并行.md#f-5f32581e6bbdca9e)；[blender::index_mask::IndexMask::from_bools · L649](../../../04-虚拟数组与索引选择/10-IndexMask构建与并行.md#f-89ee3d007144c267)。同名重载需按实参类型选择。
- `selection_mask.is_empty` → [blender::index_mask::IndexMask::is_empty · L748](../../../04-虚拟数组与索引选择/09-分段存储与遍历.md#f-190ac996386064f4)。
- `selection_mask.to_range` → [blender::index_mask::IndexMask::to_range · L1136](../../../04-虚拟数组与索引选择/12-重构历史与基准练习.md#f-bcc016bae424bbaf)。
- `smooth_points_range` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L218。
- `selection_mask.foreach_range` → [blender::index_mask::IndexMask::foreach_range · L1046](../../../04-虚拟数组与索引选择/12-重构历史与基准练习.md#f-dab36a132dcb5bac)。
- `exec_mode::grain_size` → [blender::exec_mode::grain_size · L79](../../01-BLI基础库/BLI_execution_mode.hh.md#f-0b4fc2f9fa6e66e7)。

<a id="f-12e5671d56fad9b7"></a>

### `blender::geometry::smooth_curve_attribute`

实现位置：[source/blender/geometry/intern/smooth_curves.cc](../../../../../../../source/blender/geometry/intern/smooth_curves.cc) · L230—L249。

接口参数：

- `const IndexMask &curves_to_smooth`
- `const OffsetIndices<int> points_by_curve`
- `const VArray<bool> &point_selection`
- `const VArray<bool> &cyclic`
- `const int iterations`
- `const float influence`
- `const bool smooth_ends`
- `const bool keep_shape`
- `GMutableSpan attribute_data`

**教学注释版**

<!-- annotated:4f20b3aac808ec -->

```cpp
void smooth_curve_attribute(const IndexMask &curves_to_smooth,
                            const OffsetIndices<int> points_by_curve,
                            const VArray<bool> &point_selection,
                            const VArray<bool> &cyclic,
                            const int iterations,
                            const float influence,
                            const bool smooth_ends,
                            const bool keep_shape,
                            GMutableSpan attribute_data)
{
  smooth_curve_attribute(curves_to_smooth,
                         points_by_curve,
                         point_selection,
                         cyclic,
                         iterations,
                         VArray<float>::from_single(influence, points_by_curve.total_size()),
                         smooth_ends,
                         keep_shape,
                         attribute_data);
}
```

<details>
<summary>核对原始源码：source/blender/geometry/intern/smooth_curves.cc · L230—L249</summary>

<!-- original:4f20b3aac808ec:source/blender/geometry/intern/smooth_curves.cc:230:249 -->

```cpp
void smooth_curve_attribute(const IndexMask &curves_to_smooth,
                            const OffsetIndices<int> points_by_curve,
                            const VArray<bool> &point_selection,
                            const VArray<bool> &cyclic,
                            const int iterations,
                            const float influence,
                            const bool smooth_ends,
                            const bool keep_shape,
                            GMutableSpan attribute_data)
{
  smooth_curve_attribute(curves_to_smooth,
                         points_by_curve,
                         point_selection,
                         cyclic,
                         iterations,
                         VArray<float>::from_single(influence, points_by_curve.total_size()),
                         smooth_ends,
                         keep_shape,
                         attribute_data);
}
```

</details>

**继续追踪实现**

- `smooth_curve_attribute` → [blender::geometry::smooth_curve_attribute · L177](smooth_curves.cc.md#f-501455310c3a0583)；[blender::geometry::smooth_curve_attribute · L230](smooth_curves.cc.md#f-12e5671d56fad9b7)。同名重载需按实参类型选择。
- `VArray<float>::from_single` → [blender::GVArray::from_single · L880](../../../04-虚拟数组与索引选择/05-GVArray运行时类型.md#f-1c85e09520e47c5a)；[blender::VArray::from_single · L759](../../../04-虚拟数组与索引选择/03-单值与Span表示.md#f-ea0b7b864c7f4785)。同名重载需按实参类型选择。
- `points_by_curve.total_size` → [blender::offset_indices::OffsetIndices::total_size · L58](../../../05-几何存储与拓扑映射/02-OffsetIndices完整接口.md#f-c111ffdac7a19248)。
