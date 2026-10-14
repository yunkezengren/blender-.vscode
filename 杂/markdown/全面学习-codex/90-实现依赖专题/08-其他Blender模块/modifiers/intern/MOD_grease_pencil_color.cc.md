# 实现依赖专题：source/blender/modifiers/intern/MOD_grease_pencil_color.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::foreach_ID_link"]:::abstraction
  F1["blender::apply_color_factor"]:::compute
  F2["blender::modify_stroke_color"]:::compute
  F3["blender::modify_fill_color"]:::compute
  F4["blender::modify_drawing"]:::compute
  F5["blender::modify_geometry_set"]:::compute
  F2 -->|"显式调用"| F1
  F3 -->|"显式调用"| F1
  F4 -->|"显式调用"| F2
  F4 -->|"显式调用"| F3
  F5 -->|"显式调用"| F4
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
  F["MOD_grease_pencil_color.cc实现"]:::compute
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

<a id="f-405e731e4b9631e3"></a>

### `blender::foreach_ID_link`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_color.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_color.cc) · L69—L73。

接口参数：

- `ModifierData *md`
- `Object *ob`
- `IDWalkFunc walk`
- `void *user_data`

**教学注释版**

<!-- annotated:a4c65e44ba1586 -->

```cpp
static void foreach_ID_link(ModifierData *md, Object *ob, IDWalkFunc walk, void *user_data)
{
  auto *cmd = reinterpret_cast<GreasePencilColorModifierData *>(md);
  modifier::greasepencil::foreach_influence_ID_link(&cmd->influence, ob, walk, user_data);
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_color.cc · L69—L73</summary>

<!-- original:a4c65e44ba1586:source/blender/modifiers/intern/MOD_grease_pencil_color.cc:69:73 -->

```cpp
static void foreach_ID_link(ModifierData *md, Object *ob, IDWalkFunc walk, void *user_data)
{
  auto *cmd = reinterpret_cast<GreasePencilColorModifierData *>(md);
  modifier::greasepencil::foreach_influence_ID_link(&cmd->influence, ob, walk, user_data);
}
```

</details>

**继续追踪实现**

- `modifier::greasepencil::foreach_influence_ID_link` → [blender::modifier::greasepencil::foreach_influence_ID_link · L69](MOD_grease_pencil_util.cc.md#f-247ba56fa4c4e56f)。

<a id="f-e9cdec3421bc238f"></a>

### `blender::apply_color_factor`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_color.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_color.cc) · L75—L92。

接口参数：

- `ColorGeometry4f &color`
- `const ColorGeometry4f &material_color`
- `const float3 factor`

**教学注释版**

<!-- annotated:7e859c85006269 -->

```cpp
static void apply_color_factor(ColorGeometry4f &color,
                               const ColorGeometry4f &material_color,
                               const float3 factor)
{
  float3 hsv;
  /* When input alpha is zero, replace with material color. */
  if (color.a == 0.0f && material_color.a > 0.0f) {
    color.a = 1.0f;
    rgb_to_hsv_v(material_color, hsv);
  }
  else {
    rgb_to_hsv_v(color, hsv);
  }
  hsv[0] = fractf(hsv[0] + factor[0] + 0.5f);
  hsv[1] = clamp_f(hsv[1] * factor[1], 0.0f, 1.0f);
  hsv[2] = hsv[2] * factor[2];
  hsv_to_rgb_v(hsv, color);
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_color.cc · L75—L92</summary>

<!-- original:7e859c85006269:source/blender/modifiers/intern/MOD_grease_pencil_color.cc:75:92 -->

```cpp
static void apply_color_factor(ColorGeometry4f &color,
                               const ColorGeometry4f &material_color,
                               const float3 factor)
{
  float3 hsv;
  /* When input alpha is zero, replace with material color. */
  if (color.a == 0.0f && material_color.a > 0.0f) {
    color.a = 1.0f;
    rgb_to_hsv_v(material_color, hsv);
  }
  else {
    rgb_to_hsv_v(color, hsv);
  }
  hsv[0] = fractf(hsv[0] + factor[0] + 0.5f);
  hsv[1] = clamp_f(hsv[1] * factor[1], 0.0f, 1.0f);
  hsv[2] = hsv[2] * factor[2];
  hsv_to_rgb_v(hsv, color);
}
```

</details>

**沿实际写入检查状态**

- `color.a = 1.0f;`
- `hsv[0] = fractf(hsv[0] + factor[0] + 0.5f);`
- `hsv[1] = clamp_f(hsv[1] * factor[1], 0.0f, 1.0f);`
- `hsv[2] = hsv[2] * factor[2];`

**继续追踪实现**

- `rgb_to_hsv_v` → [blender::rgb_to_hsv_v · L322](../../../01-BLI基础库/intern/math_color.cc.md#f-7312a69cee7c11bb)。
- `fractf` → [blender::fractf · L265](../../../01-BLI基础库/intern/math_base_inline.cc.md#f-0442cd3af22fc915)。
- `clamp_f` → [blender::clamp_f · L405](../../../01-BLI基础库/intern/math_base_inline.cc.md#f-abaf19ee32d97de2)。
- `hsv_to_rgb_v` → [blender::hsv_to_rgb_v · L61](../../../01-BLI基础库/intern/math_color.cc.md#f-d78b8d5b93aafd9e)。

<a id="f-39bf15b531511a28"></a>

### `blender::modify_stroke_color`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_color.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_color.cc) · L94—L131。

接口参数：

- `Object &ob`
- `const GreasePencilColorModifierData &cmd`
- `bke::CurvesGeometry &curves`
- `const IndexMask &curves_mask`
- `const MutableSpan<ColorGeometry4f> vertex_colors`

**教学注释版**

<!-- annotated:9118e6d046fdd8 -->

```cpp
static void modify_stroke_color(Object &ob,
                                const GreasePencilColorModifierData &cmd,
                                bke::CurvesGeometry &curves,
                                const IndexMask &curves_mask,
                                const MutableSpan<ColorGeometry4f> vertex_colors)
{
  const bool use_curve = (cmd.influence.flag & GREASE_PENCIL_INFLUENCE_USE_CUSTOM_CURVE);
  const OffsetIndices<int> points_by_curve = curves.points_by_curve();

  bke::AttributeAccessor attributes = curves.attributes();
  const VArray<int> stroke_materials = *attributes.lookup_or_default<int>(
      "material_index", bke::AttrDomain::Curve, 0);

  curves_mask.foreach_index(
      [&](const int64_t curve_i) {
        const Material *ma = BKE_object_material_get(&ob, stroke_materials[curve_i] + 1);
        const MaterialGPencilStyle *gp_style = ma ? ma->gp_style : nullptr;
        const ColorGeometry4f material_color = (gp_style ?
                                                    ColorGeometry4f(gp_style->stroke_rgba) :
                                                    ColorGeometry4f(0.0f, 0.0f, 0.0f, 0.0f));

        const IndexRange points = points_by_curve[curve_i];
        for (const int64_t i : points.index_range()) {
          const int64_t point_i = points[i];
          float3 factor = cmd.hsv;
          if (use_curve) {
            // [讲解] points.size：读取连续区间或分组的边界信息。
            const float curve_input = points.size() >= 2 ? (float(i) / float(points.size() - 1)) :
                                                           0.0f;
            const float curve_factor = BKE_curvemapping_evaluateF(
                cmd.influence.custom_curve, 0, curve_input);
            factor *= curve_factor;
          }

          apply_color_factor(vertex_colors[point_i], material_color, factor);
        }
      },
      exec_mode::grain_size(512));
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_color.cc · L94—L131</summary>

<!-- original:9118e6d046fdd8:source/blender/modifiers/intern/MOD_grease_pencil_color.cc:94:131 -->

```cpp
static void modify_stroke_color(Object &ob,
                                const GreasePencilColorModifierData &cmd,
                                bke::CurvesGeometry &curves,
                                const IndexMask &curves_mask,
                                const MutableSpan<ColorGeometry4f> vertex_colors)
{
  const bool use_curve = (cmd.influence.flag & GREASE_PENCIL_INFLUENCE_USE_CUSTOM_CURVE);
  const OffsetIndices<int> points_by_curve = curves.points_by_curve();

  bke::AttributeAccessor attributes = curves.attributes();
  const VArray<int> stroke_materials = *attributes.lookup_or_default<int>(
      "material_index", bke::AttrDomain::Curve, 0);

  curves_mask.foreach_index(
      [&](const int64_t curve_i) {
        const Material *ma = BKE_object_material_get(&ob, stroke_materials[curve_i] + 1);
        const MaterialGPencilStyle *gp_style = ma ? ma->gp_style : nullptr;
        const ColorGeometry4f material_color = (gp_style ?
                                                    ColorGeometry4f(gp_style->stroke_rgba) :
                                                    ColorGeometry4f(0.0f, 0.0f, 0.0f, 0.0f));

        const IndexRange points = points_by_curve[curve_i];
        for (const int64_t i : points.index_range()) {
          const int64_t point_i = points[i];
          float3 factor = cmd.hsv;
          if (use_curve) {
            const float curve_input = points.size() >= 2 ? (float(i) / float(points.size() - 1)) :
                                                           0.0f;
            const float curve_factor = BKE_curvemapping_evaluateF(
                cmd.influence.custom_curve, 0, curve_input);
            factor *= curve_factor;
          }

          apply_color_factor(vertex_colors[point_i], material_color, factor);
        }
      },
      exec_mode::grain_size(512));
}
```

</details>

**沿实际写入检查状态**

- `factor *= curve_factor;`

**继续追踪实现**

- `curves.points_by_curve` → [blender::bke::CurvesGeometry::points_by_curve · L1058](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-a0416697e10ec205)。
- `curves.attributes` → [blender::bke::CurvesGeometry::attributes · L1908](../../../02-BKE几何与数据/intern/curves_geometry.cc.md#f-8e24fbf758862a22)。
- `attributes.lookup_or_default<int>` → [blender::bke::AttributeAccessor::lookup_or_default · L415](../../../02-BKE几何与数据/intern/attribute_access.cc.md#f-a0cc3e316f1da4bd)；[blender::bke::AttributeAccessor::lookup_or_default · L643](../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-e3d2ed81ebe0af61)。同名重载需按实参类型选择。
- `curves_mask.foreach_index` → [blender::index_mask::IndexMask::foreach_index · L855](../../../../04-虚拟数组与索引选择/09-分段存储与遍历.md#f-cd6cd317e2e2812c)。
- `BKE_object_material_get` → [blender::BKE_object_material_get · L759](../../../02-BKE几何与数据/intern/material.cc.md#f-9e9ad276ccef84b3)。
- `ColorGeometry4f` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L112。
- `points.index_range` → [blender::IndexRange::index_range · L161](../../../../01-基础容器与现代CPP/04-IndexRange连续整数区间.md#f-fd83072b4b81bce5)。
- `points.size` → [blender::IndexRange::size · L156](../../../../01-基础容器与现代CPP/04-IndexRange连续整数区间.md#f-05f66c3ebb2fdfec)。
- `BKE_curvemapping_evaluateF` → [blender::BKE_curvemapping_evaluateF · L1177](../../../02-BKE几何与数据/intern/colortools.cc.md#f-014584e04eeb1392)。
- `apply_color_factor` → [blender::apply_color_factor · L75](MOD_grease_pencil_color.cc.md#f-e9cdec3421bc238f)。
- `exec_mode::grain_size` → [blender::exec_mode::grain_size · L79](../../../01-BLI基础库/BLI_execution_mode.hh.md#f-0b4fc2f9fa6e66e7)。

<a id="f-49cb2ea24f6de985"></a>

### `blender::modify_fill_color`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_color.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_color.cc) · L133—L156。

接口参数：

- `Object &ob`
- `const GreasePencilColorModifierData &cmd`
- `Drawing &drawing`
- `const IndexMask &curves_mask`

**教学注释版**

<!-- annotated:0a5eb6c92f9ea2 -->

```cpp
static void modify_fill_color(Object &ob,
                              const GreasePencilColorModifierData &cmd,
                              Drawing &drawing,
                              const IndexMask &curves_mask)
{
  const bke::CurvesGeometry &curves = drawing.strokes();
  const bke::AttributeAccessor attributes = curves.attributes();
  /* Fill color per stroke. */
  MutableSpan<ColorGeometry4f> fill_colors = drawing.fill_colors_for_write();
  const VArray<int> stroke_materials = *attributes.lookup_or_default<int>(
      "material_index", bke::AttrDomain::Curve, 0);

  curves_mask.foreach_index(
      [&](int64_t curve_i) {
        const Material *ma = BKE_object_material_get(&ob, stroke_materials[curve_i] + 1);
        const MaterialGPencilStyle *gp_style = ma ? ma->gp_style : nullptr;
        const ColorGeometry4f material_color = (gp_style ?
                                                    ColorGeometry4f(gp_style->fill_rgba) :
                                                    ColorGeometry4f(0.0f, 0.0f, 0.0f, 0.0f));

        apply_color_factor(fill_colors[curve_i], material_color, cmd.hsv);
      },
      exec_mode::grain_size(512));
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_color.cc · L133—L156</summary>

<!-- original:0a5eb6c92f9ea2:source/blender/modifiers/intern/MOD_grease_pencil_color.cc:133:156 -->

```cpp
static void modify_fill_color(Object &ob,
                              const GreasePencilColorModifierData &cmd,
                              Drawing &drawing,
                              const IndexMask &curves_mask)
{
  const bke::CurvesGeometry &curves = drawing.strokes();
  const bke::AttributeAccessor attributes = curves.attributes();
  /* Fill color per stroke. */
  MutableSpan<ColorGeometry4f> fill_colors = drawing.fill_colors_for_write();
  const VArray<int> stroke_materials = *attributes.lookup_or_default<int>(
      "material_index", bke::AttrDomain::Curve, 0);

  curves_mask.foreach_index(
      [&](int64_t curve_i) {
        const Material *ma = BKE_object_material_get(&ob, stroke_materials[curve_i] + 1);
        const MaterialGPencilStyle *gp_style = ma ? ma->gp_style : nullptr;
        const ColorGeometry4f material_color = (gp_style ?
                                                    ColorGeometry4f(gp_style->fill_rgba) :
                                                    ColorGeometry4f(0.0f, 0.0f, 0.0f, 0.0f));

        apply_color_factor(fill_colors[curve_i], material_color, cmd.hsv);
      },
      exec_mode::grain_size(512));
}
```

</details>

**继续追踪实现**

- `drawing.strokes` → [blender::bke::greasepencil::Drawing::strokes · L1007](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-59e6522a8e8ac409)。
- `curves.attributes` → [blender::bke::CurvesGeometry::attributes · L1908](../../../02-BKE几何与数据/intern/curves_geometry.cc.md#f-8e24fbf758862a22)。
- `drawing.fill_colors_for_write` → [blender::bke::greasepencil::Drawing::fill_colors_for_write · L1069](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-c1670c8b77b029fa)。
- `attributes.lookup_or_default<int>` → [blender::bke::AttributeAccessor::lookup_or_default · L415](../../../02-BKE几何与数据/intern/attribute_access.cc.md#f-a0cc3e316f1da4bd)；[blender::bke::AttributeAccessor::lookup_or_default · L643](../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-e3d2ed81ebe0af61)。同名重载需按实参类型选择。
- `curves_mask.foreach_index` → [blender::index_mask::IndexMask::foreach_index · L855](../../../../04-虚拟数组与索引选择/09-分段存储与遍历.md#f-cd6cd317e2e2812c)。
- `BKE_object_material_get` → [blender::BKE_object_material_get · L759](../../../02-BKE几何与数据/intern/material.cc.md#f-9e9ad276ccef84b3)。
- `ColorGeometry4f` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L150。
- `apply_color_factor` → [blender::apply_color_factor · L75](MOD_grease_pencil_color.cc.md#f-e9cdec3421bc238f)。
- `exec_mode::grain_size` → [blender::exec_mode::grain_size · L79](../../../01-BLI基础库/BLI_execution_mode.hh.md#f-0b4fc2f9fa6e66e7)。

<a id="f-8560cf47c9d501b1"></a>

### `blender::modify_drawing`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_color.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_color.cc) · L158—L184。

接口参数：

- `ModifierData &md`
- `const ModifierEvalContext &ctx`
- `Drawing &drawing`

**教学注释版**

<!-- annotated:5fd3003c83c4d6 -->

```cpp
static void modify_drawing(ModifierData &md, const ModifierEvalContext &ctx, Drawing &drawing)
{
  auto &cmd = reinterpret_cast<GreasePencilColorModifierData &>(md);

  bke::CurvesGeometry &curves = drawing.strokes_for_write();
  IndexMaskMemory mask_memory;
  const IndexMask curves_mask = modifier::greasepencil::get_filtered_stroke_mask(
      ctx.object, curves, cmd.influence, mask_memory);

  switch (cmd.color_mode) {
    case MOD_GREASE_PENCIL_COLOR_STROKE:
      modify_stroke_color(
          *ctx.object, cmd, curves, curves_mask, drawing.vertex_colors_for_write());
      break;
    case MOD_GREASE_PENCIL_COLOR_FILL:
      modify_fill_color(*ctx.object, cmd, drawing, curves_mask);
      break;
    case MOD_GREASE_PENCIL_COLOR_BOTH:
      modify_stroke_color(
          *ctx.object, cmd, curves, curves_mask, drawing.vertex_colors_for_write());
      modify_fill_color(*ctx.object, cmd, drawing, curves_mask);
      break;
    case MOD_GREASE_PENCIL_COLOR_HARDNESS:
      BLI_assert_unreachable();
      break;
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_color.cc · L158—L184</summary>

<!-- original:5fd3003c83c4d6:source/blender/modifiers/intern/MOD_grease_pencil_color.cc:158:184 -->

```cpp
static void modify_drawing(ModifierData &md, const ModifierEvalContext &ctx, Drawing &drawing)
{
  auto &cmd = reinterpret_cast<GreasePencilColorModifierData &>(md);

  bke::CurvesGeometry &curves = drawing.strokes_for_write();
  IndexMaskMemory mask_memory;
  const IndexMask curves_mask = modifier::greasepencil::get_filtered_stroke_mask(
      ctx.object, curves, cmd.influence, mask_memory);

  switch (cmd.color_mode) {
    case MOD_GREASE_PENCIL_COLOR_STROKE:
      modify_stroke_color(
          *ctx.object, cmd, curves, curves_mask, drawing.vertex_colors_for_write());
      break;
    case MOD_GREASE_PENCIL_COLOR_FILL:
      modify_fill_color(*ctx.object, cmd, drawing, curves_mask);
      break;
    case MOD_GREASE_PENCIL_COLOR_BOTH:
      modify_stroke_color(
          *ctx.object, cmd, curves, curves_mask, drawing.vertex_colors_for_write());
      modify_fill_color(*ctx.object, cmd, drawing, curves_mask);
      break;
    case MOD_GREASE_PENCIL_COLOR_HARDNESS:
      BLI_assert_unreachable();
      break;
  }
}
```

</details>

**继续追踪实现**

- `drawing.strokes_for_write` → [blender::bke::greasepencil::Drawing::strokes_for_write · L1012](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-0649333785d0aa95)。
- `modifier::greasepencil::get_filtered_stroke_mask` → [blender::modifier::greasepencil::get_filtered_stroke_mask · L285](MOD_grease_pencil_util.cc.md#f-30c219d04de7dec3)；[blender::modifier::greasepencil::get_filtered_stroke_mask · L326](MOD_grease_pencil_util.cc.md#f-970c3bc880e4f350)。同名重载需按实参类型选择。
- `modify_stroke_color` → [blender::modify_stroke_color · L94](MOD_grease_pencil_color.cc.md#f-39bf15b531511a28)。
- `drawing.vertex_colors_for_write` → [blender::bke::greasepencil::Drawing::vertex_colors_for_write · L1053](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-2d24b72934b99ac2)。
- `modify_fill_color` → [blender::modify_fill_color · L133](MOD_grease_pencil_color.cc.md#f-49cb2ea24f6de985)。
- `BLI_assert_unreachable` → [BLI_assert_unreachable · L77](../../../01-BLI基础库/BLI_assert.hh.md#m-7a2d91a67d8e)。宏定义由构建条件选择。

<a id="f-b7d9cea51cff81d7"></a>

### `blender::modify_geometry_set`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_color.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_color.cc) · L186—L205。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `bke::GeometrySet *geometry_set`

**教学注释版**

<!-- annotated:31eed5e9b1f901 -->

```cpp
static void modify_geometry_set(ModifierData *md,
                                const ModifierEvalContext *ctx,
                                bke::GeometrySet *geometry_set)
{
  auto *cmd = reinterpret_cast<GreasePencilColorModifierData *>(md);

  if (!geometry_set->has_grease_pencil()) {
    return;
  }
  GreasePencil &grease_pencil = *geometry_set->get_grease_pencil_for_write();
  const int frame = grease_pencil.runtime->eval_frame;

  IndexMaskMemory mask_memory;
  const IndexMask layer_mask = modifier::greasepencil::get_filtered_layer_mask(
      grease_pencil, cmd->influence, mask_memory);
  const Vector<Drawing *> drawings = modifier::greasepencil::get_drawings_for_write(
      grease_pencil, layer_mask, frame);
  threading::parallel_for_each(drawings,
                               [&](Drawing *drawing) { modify_drawing(*md, *ctx, *drawing); });
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_color.cc · L186—L205</summary>

<!-- original:31eed5e9b1f901:source/blender/modifiers/intern/MOD_grease_pencil_color.cc:186:205 -->

```cpp
static void modify_geometry_set(ModifierData *md,
                                const ModifierEvalContext *ctx,
                                bke::GeometrySet *geometry_set)
{
  auto *cmd = reinterpret_cast<GreasePencilColorModifierData *>(md);

  if (!geometry_set->has_grease_pencil()) {
    return;
  }
  GreasePencil &grease_pencil = *geometry_set->get_grease_pencil_for_write();
  const int frame = grease_pencil.runtime->eval_frame;

  IndexMaskMemory mask_memory;
  const IndexMask layer_mask = modifier::greasepencil::get_filtered_layer_mask(
      grease_pencil, cmd->influence, mask_memory);
  const Vector<Drawing *> drawings = modifier::greasepencil::get_drawings_for_write(
      grease_pencil, layer_mask, frame);
  threading::parallel_for_each(drawings,
                               [&](Drawing *drawing) { modify_drawing(*md, *ctx, *drawing); });
}
```

</details>

**继续追踪实现**

- `geometry_set->has_grease_pencil` → [blender::bke::GeometrySet::has_grease_pencil · L415](../../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-357bcb62da7a8afd)。
- `geometry_set->get_grease_pencil_for_write` → [blender::bke::GeometrySet::get_grease_pencil_for_write · L622](../../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-bfc5e891a352651b)。
- `modifier::greasepencil::get_filtered_layer_mask` → [blender::modifier::greasepencil::get_filtered_layer_mask · L213](MOD_grease_pencil_util.cc.md#f-6438bea51141f9db)；[blender::modifier::greasepencil::get_filtered_layer_mask · L268](MOD_grease_pencil_util.cc.md#f-e3d0f9748ecdf34b)。同名重载需按实参类型选择。
- `modifier::greasepencil::get_drawings_for_write` → [blender::modifier::greasepencil::get_drawings_for_write · L368](MOD_grease_pencil_util.cc.md#f-cef3871c31259376)。
- `threading::parallel_for_each` → [blender::threading::parallel_for_each · L30](../../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-d5604027445ef0f5)。
- `modify_drawing` → [blender::modify_drawing · L158](MOD_grease_pencil_color.cc.md#f-8560cf47c9d501b1)。
