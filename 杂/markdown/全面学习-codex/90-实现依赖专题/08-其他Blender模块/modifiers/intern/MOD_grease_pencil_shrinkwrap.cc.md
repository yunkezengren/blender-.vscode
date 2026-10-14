# 实现依赖专题：source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::foreach_ID_link"]:::abstraction
  F1["blender::is_disabled"]:::compute
  F2["blender::update_depsgraph"]:::compute
  F3["blender::modify_drawing"]:::compute
  F4["blender::ensure_shrinkwrap_cache_data"]:::compute
  F5["blender::modify_geometry_set"]:::compute
  F5 -->|"显式调用"| F4
  F5 -->|"显式调用"| F3
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
  F["MOD_grease_pencil_shrinkwrap.cc实现"]:::compute
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

<a id="f-c27b5c4b02a06aaf"></a>

### `blender::foreach_ID_link`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc) · L77—L83。

接口参数：

- `ModifierData *md`
- `Object *ob`
- `IDWalkFunc walk`
- `void *user_data`

**教学注释版**

<!-- annotated:909ca1fcc845c6 -->

```cpp
static void foreach_ID_link(ModifierData *md, Object *ob, IDWalkFunc walk, void *user_data)
{
  auto *smd = reinterpret_cast<GreasePencilShrinkwrapModifierData *>(md);
  modifier::greasepencil::foreach_influence_ID_link(&smd->influence, ob, walk, user_data);
  walk(user_data, ob, reinterpret_cast<ID **>(&smd->target), IDWALK_CB_NOP);
  walk(user_data, ob, reinterpret_cast<ID **>(&smd->aux_target), IDWALK_CB_NOP);
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc · L77—L83</summary>

<!-- original:909ca1fcc845c6:source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc:77:83 -->

```cpp
static void foreach_ID_link(ModifierData *md, Object *ob, IDWalkFunc walk, void *user_data)
{
  auto *smd = reinterpret_cast<GreasePencilShrinkwrapModifierData *>(md);
  modifier::greasepencil::foreach_influence_ID_link(&smd->influence, ob, walk, user_data);
  walk(user_data, ob, reinterpret_cast<ID **>(&smd->target), IDWALK_CB_NOP);
  walk(user_data, ob, reinterpret_cast<ID **>(&smd->aux_target), IDWALK_CB_NOP);
}
```

</details>

**继续追踪实现**

- `modifier::greasepencil::foreach_influence_ID_link` → [blender::modifier::greasepencil::foreach_influence_ID_link · L69](MOD_grease_pencil_util.cc.md#f-247ba56fa4c4e56f)。
- `walk` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L81。

<a id="f-b004accafec24111"></a>

### `blender::is_disabled`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc) · L85—L101。

接口参数：

- `const Scene *`
- `ModifierData *md`
- `bool`

**教学注释版**

<!-- annotated:43f4c85bcee4f6 -->

```cpp
static bool is_disabled(const Scene * /*scene*/, ModifierData *md, bool /*use_render_params*/)
{
  auto *smd = reinterpret_cast<GreasePencilShrinkwrapModifierData *>(md);

  /* The object type check is only needed here in case we have a placeholder
   * object assigned (because the library containing the mesh is missing).
   *
   * In other cases it should be impossible to have a type mismatch.
   */
  if (smd->target == nullptr || smd->target->type != OB_MESH) {
    return true;
  }
  if (smd->aux_target != nullptr && smd->aux_target->type != OB_MESH) {
    return true;
  }
  return false;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc · L85—L101</summary>

<!-- original:43f4c85bcee4f6:source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc:85:101 -->

```cpp
static bool is_disabled(const Scene * /*scene*/, ModifierData *md, bool /*use_render_params*/)
{
  auto *smd = reinterpret_cast<GreasePencilShrinkwrapModifierData *>(md);

  /* The object type check is only needed here in case we have a placeholder
   * object assigned (because the library containing the mesh is missing).
   *
   * In other cases it should be impossible to have a type mismatch.
   */
  if (smd->target == nullptr || smd->target->type != OB_MESH) {
    return true;
  }
  if (smd->aux_target != nullptr && smd->aux_target->type != OB_MESH) {
    return true;
  }
  return false;
}
```

</details>

**结果出口**

- `return true;`
- `return false;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-1a3690c8ca7b9c0f"></a>

### `blender::update_depsgraph`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc) · L103—L127。

接口参数：

- `ModifierData *md`
- `const ModifierUpdateDepsgraphContext *ctx`

**教学注释版**

<!-- annotated:1f08c9c66dee81 -->

```cpp
static void update_depsgraph(ModifierData *md, const ModifierUpdateDepsgraphContext *ctx)
{
  auto *smd = reinterpret_cast<GreasePencilShrinkwrapModifierData *>(md);

  if (smd->target != nullptr) {
    DEG_add_object_relation(
        ctx->node, smd->target, DEG_OB_COMP_TRANSFORM, "Grease Pencil Shrinkwrap Modifier");
    DEG_add_object_relation(
        ctx->node, smd->target, DEG_OB_COMP_GEOMETRY, "Grease Pencil Shrinkwrap Modifier");
    if (smd->shrink_type == MOD_SHRINKWRAP_TARGET_PROJECT) {
      DEG_add_special_eval_flag(ctx->node, &smd->target->id, DAG_EVAL_NEED_SHRINKWRAP_BOUNDARY);
    }
  }
  if (smd->aux_target != nullptr) {
    DEG_add_object_relation(
        ctx->node, smd->aux_target, DEG_OB_COMP_TRANSFORM, "Grease Pencil Shrinkwrap Modifier");
    DEG_add_object_relation(
        ctx->node, smd->aux_target, DEG_OB_COMP_GEOMETRY, "Grease Pencil Shrinkwrap Modifier");
    if (smd->shrink_type == MOD_SHRINKWRAP_TARGET_PROJECT) {
      DEG_add_special_eval_flag(
          ctx->node, &smd->aux_target->id, DAG_EVAL_NEED_SHRINKWRAP_BOUNDARY);
    }
  }
  DEG_add_depends_on_transform_relation(ctx->node, "Grease Pencil Shrinkwrap Modifier");
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc · L103—L127</summary>

<!-- original:1f08c9c66dee81:source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc:103:127 -->

```cpp
static void update_depsgraph(ModifierData *md, const ModifierUpdateDepsgraphContext *ctx)
{
  auto *smd = reinterpret_cast<GreasePencilShrinkwrapModifierData *>(md);

  if (smd->target != nullptr) {
    DEG_add_object_relation(
        ctx->node, smd->target, DEG_OB_COMP_TRANSFORM, "Grease Pencil Shrinkwrap Modifier");
    DEG_add_object_relation(
        ctx->node, smd->target, DEG_OB_COMP_GEOMETRY, "Grease Pencil Shrinkwrap Modifier");
    if (smd->shrink_type == MOD_SHRINKWRAP_TARGET_PROJECT) {
      DEG_add_special_eval_flag(ctx->node, &smd->target->id, DAG_EVAL_NEED_SHRINKWRAP_BOUNDARY);
    }
  }
  if (smd->aux_target != nullptr) {
    DEG_add_object_relation(
        ctx->node, smd->aux_target, DEG_OB_COMP_TRANSFORM, "Grease Pencil Shrinkwrap Modifier");
    DEG_add_object_relation(
        ctx->node, smd->aux_target, DEG_OB_COMP_GEOMETRY, "Grease Pencil Shrinkwrap Modifier");
    if (smd->shrink_type == MOD_SHRINKWRAP_TARGET_PROJECT) {
      DEG_add_special_eval_flag(
          ctx->node, &smd->aux_target->id, DAG_EVAL_NEED_SHRINKWRAP_BOUNDARY);
    }
  }
  DEG_add_depends_on_transform_relation(ctx->node, "Grease Pencil Shrinkwrap Modifier");
}
```

</details>

**继续追踪实现**

- `DEG_add_object_relation` → [blender::DEG_add_object_relation · L123](../../../06-Depsgraph依赖图/intern/depsgraph_build.cc.md#f-f570cffae97e273c)。
- `DEG_add_special_eval_flag` → [blender::DEG_add_special_eval_flag · L253](../../../06-Depsgraph依赖图/intern/depsgraph_build.cc.md#f-d68e9c73ded33dd2)。
- `DEG_add_depends_on_transform_relation` → [blender::DEG_add_depends_on_transform_relation · L240](../../../06-Depsgraph依赖图/intern/depsgraph_build.cc.md#f-47c32a354defa20d)。

<a id="f-86d177ae9d24f3cb"></a>

### `blender::modify_drawing`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc) · L129—L182。

接口参数：

- `const GreasePencilShrinkwrapModifierData &smd`
- `const ModifierEvalContext &ctx`
- `bke::greasepencil::Drawing &drawing`

**教学注释版**

<!-- annotated:251b760a4fb253 -->

```cpp
static void modify_drawing(const GreasePencilShrinkwrapModifierData &smd,
                           const ModifierEvalContext &ctx,
                           bke::greasepencil::Drawing &drawing)
{
  modifier::greasepencil::ensure_no_bezier_curves(drawing);
  bke::CurvesGeometry &curves = drawing.strokes_for_write();
  const OffsetIndices<int> points_by_curve = curves.points_by_curve();
  const Span<MDeformVert> dverts = curves.deform_verts();
  const MutableSpan<float3> positions = curves.positions_for_write();
  const int defgrp_idx = BKE_object_defgroup_name_index(ctx.object,
                                                        smd.influence.vertex_group_name);

  /* Selected source curves. */
  IndexMaskMemory curve_mask_memory;
  const IndexMask curves_mask = modifier::greasepencil::get_filtered_stroke_mask(
      ctx.object, drawing.strokes(), smd.influence, curve_mask_memory);

  ShrinkwrapParams params;
  params.target = smd.target;
  params.aux_target = smd.aux_target;
  params.invert_vertex_weights = smd.influence.flag & GREASE_PENCIL_INFLUENCE_INVERT_VERTEX_GROUP;
  params.keep_distance = smd.keep_dist;
  params.shrink_type = smd.shrink_type;
  params.shrink_options = smd.shrink_opts;
  params.shrink_mode = smd.shrink_mode;
  params.projection_limit = smd.proj_limit;
  params.projection_axis = smd.proj_axis;
  params.subsurf_levels = smd.subsurf_levels;

  curves_mask.foreach_index([&](const int curve_i) {
    const IndexRange points = points_by_curve[curve_i];
    // [讲解] dverts.is_empty：查询视图长度或生成对应有效索引区间。
    const Span<MDeformVert> curve_dverts = dverts.is_empty() ? dverts : dverts.slice(points);
    // [讲解] positions.slice：建立原连续范围的子视图。
    const MutableSpan<float3> curve_positions = positions.slice(points);

    shrinkwrapParams_deform(
        params, *ctx.object, *smd.cache_data, curve_dverts, defgrp_idx, curve_positions);
  });

  /* Optional smoothing after shrinkwrap. */
  const VArray<bool> point_selection = VArray<bool>::from_single(true, curves.points_num());
  const bool smooth_ends = false;
  const bool keep_shape = true;
  geometry::smooth_curve_attribute(curves_mask,
                                   points_by_curve,
                                   point_selection,
                                   curves.cyclic(),
                                   smd.smooth_step,
                                   smd.smooth_factor,
                                   smooth_ends,
                                   keep_shape,
                                   positions);

  drawing.tag_positions_changed();
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc · L129—L182</summary>

<!-- original:251b760a4fb253:source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc:129:182 -->

```cpp
static void modify_drawing(const GreasePencilShrinkwrapModifierData &smd,
                           const ModifierEvalContext &ctx,
                           bke::greasepencil::Drawing &drawing)
{
  modifier::greasepencil::ensure_no_bezier_curves(drawing);
  bke::CurvesGeometry &curves = drawing.strokes_for_write();
  const OffsetIndices<int> points_by_curve = curves.points_by_curve();
  const Span<MDeformVert> dverts = curves.deform_verts();
  const MutableSpan<float3> positions = curves.positions_for_write();
  const int defgrp_idx = BKE_object_defgroup_name_index(ctx.object,
                                                        smd.influence.vertex_group_name);

  /* Selected source curves. */
  IndexMaskMemory curve_mask_memory;
  const IndexMask curves_mask = modifier::greasepencil::get_filtered_stroke_mask(
      ctx.object, drawing.strokes(), smd.influence, curve_mask_memory);

  ShrinkwrapParams params;
  params.target = smd.target;
  params.aux_target = smd.aux_target;
  params.invert_vertex_weights = smd.influence.flag & GREASE_PENCIL_INFLUENCE_INVERT_VERTEX_GROUP;
  params.keep_distance = smd.keep_dist;
  params.shrink_type = smd.shrink_type;
  params.shrink_options = smd.shrink_opts;
  params.shrink_mode = smd.shrink_mode;
  params.projection_limit = smd.proj_limit;
  params.projection_axis = smd.proj_axis;
  params.subsurf_levels = smd.subsurf_levels;

  curves_mask.foreach_index([&](const int curve_i) {
    const IndexRange points = points_by_curve[curve_i];
    const Span<MDeformVert> curve_dverts = dverts.is_empty() ? dverts : dverts.slice(points);
    const MutableSpan<float3> curve_positions = positions.slice(points);

    shrinkwrapParams_deform(
        params, *ctx.object, *smd.cache_data, curve_dverts, defgrp_idx, curve_positions);
  });

  /* Optional smoothing after shrinkwrap. */
  const VArray<bool> point_selection = VArray<bool>::from_single(true, curves.points_num());
  const bool smooth_ends = false;
  const bool keep_shape = true;
  geometry::smooth_curve_attribute(curves_mask,
                                   points_by_curve,
                                   point_selection,
                                   curves.cyclic(),
                                   smd.smooth_step,
                                   smd.smooth_factor,
                                   smooth_ends,
                                   keep_shape,
                                   positions);

  drawing.tag_positions_changed();
}
```

</details>

**沿实际写入检查状态**

- `params.target = smd.target;`
- `params.aux_target = smd.aux_target;`
- `params.invert_vertex_weights = smd.influence.flag & GREASE_PENCIL_INFLUENCE_INVERT_VERTEX_GROUP;`
- `params.keep_distance = smd.keep_dist;`
- `params.shrink_type = smd.shrink_type;`
- `params.shrink_options = smd.shrink_opts;`
- `params.shrink_mode = smd.shrink_mode;`
- `params.projection_limit = smd.proj_limit;`
- `params.projection_axis = smd.proj_axis;`
- `params.subsurf_levels = smd.subsurf_levels;`

**继续追踪实现**

- `modifier::greasepencil::ensure_no_bezier_curves` → [blender::modifier::greasepencil::ensure_no_bezier_curves · L432](MOD_grease_pencil_util.cc.md#f-1fde6483ac30d59b)。
- `drawing.strokes_for_write` → [blender::bke::greasepencil::Drawing::strokes_for_write · L1012](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-0649333785d0aa95)。
- `curves.points_by_curve` → [blender::bke::CurvesGeometry::points_by_curve · L1058](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-a0416697e10ec205)。
- `curves.deform_verts` → [blender::bke::CurvesGeometry::deform_verts · L611](../../../02-BKE几何与数据/intern/curves_geometry.cc.md#f-45589948eb3850fc)。
- `curves.positions_for_write` → [blender::bke::CurvesGeometry::positions_for_write · L328](../../../02-BKE几何与数据/intern/curves_geometry.cc.md#f-30e013e651e830c3)。
- `BKE_object_defgroup_name_index` → [blender::BKE_object_defgroup_name_index · L597](../../../02-BKE几何与数据/intern/deform.cc.md#f-ad856e5bba5cd758)。
- `modifier::greasepencil::get_filtered_stroke_mask` → [blender::modifier::greasepencil::get_filtered_stroke_mask · L285](MOD_grease_pencil_util.cc.md#f-30c219d04de7dec3)；[blender::modifier::greasepencil::get_filtered_stroke_mask · L326](MOD_grease_pencil_util.cc.md#f-970c3bc880e4f350)。同名重载需按实参类型选择。
- `drawing.strokes` → [blender::bke::greasepencil::Drawing::strokes · L1007](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-59e6522a8e8ac409)。
- `curves_mask.foreach_index` → [blender::index_mask::IndexMask::foreach_index · L855](../../../../04-虚拟数组与索引选择/09-分段存储与遍历.md#f-cd6cd317e2e2812c)。
- `dverts.is_empty` → [blender::Span::is_empty · L264](../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-8cc1d7ba8feb50e6)。
- `dverts.slice` → [blender::Span::slice · L141](../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-380a0e8fdcbd53cc)；[blender::Span::slice · L149](../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-9b9c15e78dd54eec)。同名重载需按实参类型选择。
- `positions.slice` → [blender::MutableSpan::slice · L579](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-6808b4aefbf58808)；[blender::MutableSpan::slice · L587](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-c05b010821861e4f)。同名重载需按实参类型选择。
- `shrinkwrapParams_deform` → [blender::shrinkwrapParams_deform · L1396](../../../02-BKE几何与数据/intern/shrinkwrap.cc.md#f-54495e488d1c3c4c)。
- `VArray<bool>::from_single` → [blender::GVArray::from_single · L880](../../../../04-虚拟数组与索引选择/05-GVArray运行时类型.md#f-1c85e09520e47c5a)。
- `curves.points_num` → [blender::bke::CurvesGeometry::points_num · L1001](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-049421b1f643c700)。
- `geometry::smooth_curve_attribute` → [blender::geometry::smooth_curve_attribute · L177](../../../05-Geometry几何算法/intern/smooth_curves.cc.md#f-501455310c3a0583)；[blender::geometry::smooth_curve_attribute · L230](../../../05-Geometry几何算法/intern/smooth_curves.cc.md#f-12e5671d56fad9b7)。同名重载需按实参类型选择。
- `curves.cyclic` → [blender::bke::CurvesGeometry::cyclic · L362](../../../02-BKE几何与数据/intern/curves_geometry.cc.md#f-ec08c2a1d6f3bfea)。
- `drawing.tag_positions_changed` → [blender::bke::greasepencil::Drawing::tag_positions_changed · L1095](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-cc348dc1ca18c109)；[blender::bke::greasepencil::Drawing::tag_positions_changed · L1229](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-36aaac52033b03bf)。同名重载需按实参类型选择。

<a id="f-e53fa617bab6ea7c"></a>

### `blender::ensure_shrinkwrap_cache_data`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc) · L184—L202。

接口参数：

- `GreasePencilShrinkwrapModifierData &smd`
- `const ModifierEvalContext &ctx`

**教学注释版**

<!-- annotated:00a84ed74a95d3 -->

```cpp
static void ensure_shrinkwrap_cache_data(GreasePencilShrinkwrapModifierData &smd,
                                         const ModifierEvalContext &ctx)
{
  if (smd.cache_data) {
    BKE_shrinkwrap_free_tree(smd.cache_data);
    MEM_delete(smd.cache_data);
    smd.cache_data = nullptr;
  }
  Object *target_ob = DEG_get_evaluated(ctx.depsgraph, smd.target);
  Mesh *target_mesh = BKE_modifier_get_evaluated_mesh_from_evaluated_object(target_ob);

  smd.cache_data = MEM_new<ShrinkwrapTreeData>(__func__);
  const bool tree_ok = BKE_shrinkwrap_init_tree(
      smd.cache_data, target_mesh, smd.shrink_type, smd.shrink_mode, false);
  if (!tree_ok) {
    MEM_delete(smd.cache_data);
    smd.cache_data = nullptr;
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc · L184—L202</summary>

<!-- original:00a84ed74a95d3:source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc:184:202 -->

```cpp
static void ensure_shrinkwrap_cache_data(GreasePencilShrinkwrapModifierData &smd,
                                         const ModifierEvalContext &ctx)
{
  if (smd.cache_data) {
    BKE_shrinkwrap_free_tree(smd.cache_data);
    MEM_delete(smd.cache_data);
    smd.cache_data = nullptr;
  }
  Object *target_ob = DEG_get_evaluated(ctx.depsgraph, smd.target);
  Mesh *target_mesh = BKE_modifier_get_evaluated_mesh_from_evaluated_object(target_ob);

  smd.cache_data = MEM_new<ShrinkwrapTreeData>(__func__);
  const bool tree_ok = BKE_shrinkwrap_init_tree(
      smd.cache_data, target_mesh, smd.shrink_type, smd.shrink_mode, false);
  if (!tree_ok) {
    MEM_delete(smd.cache_data);
    smd.cache_data = nullptr;
  }
}
```

</details>

**沿实际写入检查状态**

- `smd.cache_data = nullptr;`
- `smd.cache_data = MEM_new<ShrinkwrapTreeData>(__func__);`

**继续追踪实现**

- `BKE_shrinkwrap_free_tree` → [blender::BKE_shrinkwrap_free_tree · L144](../../../02-BKE几何与数据/intern/shrinkwrap.cc.md#f-803c1caa34293b9d)。
- `MEM_delete` → [MEM_delete · L400](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
- `DEG_get_evaluated` → [blender::DEG_get_evaluated · L106](../../../06-Depsgraph依赖图/DEG_depsgraph_query.hh.md#f-e70143fa875363bf)；[blender::DEG_get_evaluated · L112](../../../06-Depsgraph依赖图/DEG_depsgraph_query.hh.md#f-129df72cfb5a1bad)。同名重载需按实参类型选择。
- `BKE_modifier_get_evaluated_mesh_from_evaluated_object` → [blender::BKE_modifier_get_evaluated_mesh_from_evaluated_object · L1041](../../../02-BKE几何与数据/intern/modifier.cc.md#f-75729c35b147b115)。
- `MEM_new<ShrinkwrapTreeData>` → [MEM_new · L351](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-115f9b6784f89912)。
- `BKE_shrinkwrap_init_tree` → [blender::BKE_shrinkwrap_init_tree · L87](../../../02-BKE几何与数据/intern/shrinkwrap.cc.md#f-d6641b6a47bc4e77)。

<a id="f-46686f6c416f5e15"></a>

### `blender::modify_geometry_set`

实现位置：[source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc](../../../../../../../../source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc) · L204—L236。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `bke::GeometrySet *geometry_set`

**教学注释版**

<!-- annotated:9470d769428ed4 -->

```cpp
static void modify_geometry_set(ModifierData *md,
                                const ModifierEvalContext *ctx,
                                bke::GeometrySet *geometry_set)
{
  using bke::greasepencil::Drawing;
  using bke::greasepencil::Layer;
  using modifier::greasepencil::LayerDrawingInfo;

  auto &smd = *reinterpret_cast<GreasePencilShrinkwrapModifierData *>(md);
  BLI_assert(smd.target != nullptr);
  if (smd.target == ctx->object || smd.aux_target == ctx->object) {
    return;
  }
  if (!geometry_set->has_grease_pencil()) {
    return;
  }
  GreasePencil &grease_pencil = *geometry_set->get_grease_pencil_for_write();
  const int frame = grease_pencil.runtime->eval_frame;

  ensure_shrinkwrap_cache_data(smd, *ctx);
  if (!smd.cache_data) {
    return;
  }

  IndexMaskMemory mask_memory;
  const IndexMask layer_mask = modifier::greasepencil::get_filtered_layer_mask(
      grease_pencil, smd.influence, mask_memory);

  const Vector<Drawing *> drawings = modifier::greasepencil::get_drawings_for_write(
      grease_pencil, layer_mask, frame);
  threading::parallel_for_each(drawings,
                               [&](Drawing *drawing) { modify_drawing(smd, *ctx, *drawing); });
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc · L204—L236</summary>

<!-- original:9470d769428ed4:source/blender/modifiers/intern/MOD_grease_pencil_shrinkwrap.cc:204:236 -->

```cpp
static void modify_geometry_set(ModifierData *md,
                                const ModifierEvalContext *ctx,
                                bke::GeometrySet *geometry_set)
{
  using bke::greasepencil::Drawing;
  using bke::greasepencil::Layer;
  using modifier::greasepencil::LayerDrawingInfo;

  auto &smd = *reinterpret_cast<GreasePencilShrinkwrapModifierData *>(md);
  BLI_assert(smd.target != nullptr);
  if (smd.target == ctx->object || smd.aux_target == ctx->object) {
    return;
  }
  if (!geometry_set->has_grease_pencil()) {
    return;
  }
  GreasePencil &grease_pencil = *geometry_set->get_grease_pencil_for_write();
  const int frame = grease_pencil.runtime->eval_frame;

  ensure_shrinkwrap_cache_data(smd, *ctx);
  if (!smd.cache_data) {
    return;
  }

  IndexMaskMemory mask_memory;
  const IndexMask layer_mask = modifier::greasepencil::get_filtered_layer_mask(
      grease_pencil, smd.influence, mask_memory);

  const Vector<Drawing *> drawings = modifier::greasepencil::get_drawings_for_write(
      grease_pencil, layer_mask, frame);
  threading::parallel_for_each(drawings,
                               [&](Drawing *drawing) { modify_drawing(smd, *ctx, *drawing); });
}
```

</details>

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `geometry_set->has_grease_pencil` → [blender::bke::GeometrySet::has_grease_pencil · L415](../../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-357bcb62da7a8afd)。
- `geometry_set->get_grease_pencil_for_write` → [blender::bke::GeometrySet::get_grease_pencil_for_write · L622](../../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-bfc5e891a352651b)。
- `ensure_shrinkwrap_cache_data` → [blender::ensure_shrinkwrap_cache_data · L184](MOD_grease_pencil_shrinkwrap.cc.md#f-e53fa617bab6ea7c)。
- `modifier::greasepencil::get_filtered_layer_mask` → [blender::modifier::greasepencil::get_filtered_layer_mask · L213](MOD_grease_pencil_util.cc.md#f-6438bea51141f9db)；[blender::modifier::greasepencil::get_filtered_layer_mask · L268](MOD_grease_pencil_util.cc.md#f-e3d0f9748ecdf34b)。同名重载需按实参类型选择。
- `modifier::greasepencil::get_drawings_for_write` → [blender::modifier::greasepencil::get_drawings_for_write · L368](MOD_grease_pencil_util.cc.md#f-cef3871c31259376)。
- `threading::parallel_for_each` → [blender::threading::parallel_for_each · L30](../../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-d5604027445ef0f5)。
- `modify_drawing` → [blender::modify_drawing · L129](MOD_grease_pencil_shrinkwrap.cc.md#f-86d177ae9d24f3cb)。
