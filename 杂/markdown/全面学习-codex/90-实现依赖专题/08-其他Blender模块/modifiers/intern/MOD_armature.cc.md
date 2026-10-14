# 实现依赖专题：source/blender/modifiers/intern/MOD_armature.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::required_data_mask"]:::abstraction
  F1["blender::is_disabled"]:::compute
  F2["blender::foreach_ID_link"]:::compute
  F3["blender::update_depsgraph"]:::compute
  F4["blender::deform_verts"]:::compute
  F5["blender::deform_verts_EM"]:::compute
  F6["blender::deform_matrices"]:::compute
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
  F["MOD_armature.cc实现"]:::compute
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

<a id="f-5ead046ebad2c1ff"></a>

### `blender::required_data_mask`

实现位置：[source/blender/modifiers/intern/MOD_armature.cc](../../../../../../../../source/blender/modifiers/intern/MOD_armature.cc) · L58—L62。

接口参数：

- `ModifierData *`
- `CustomData_MeshMasks *r_cddata_masks`

**教学注释版**

<!-- annotated:1e711c8cb46f77 -->

```cpp
static void required_data_mask(ModifierData * /*md*/, CustomData_MeshMasks *r_cddata_masks)
{
  /* Ask for vertex-groups. */
  r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_armature.cc · L58—L62</summary>

<!-- original:1e711c8cb46f77:source/blender/modifiers/intern/MOD_armature.cc:58:62 -->

```cpp
static void required_data_mask(ModifierData * /*md*/, CustomData_MeshMasks *r_cddata_masks)
{
  /* Ask for vertex-groups. */
  r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;
}
```

</details>

**沿实际写入检查状态**

- `r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-3524d00c8f6db35a"></a>

### `blender::is_disabled`

实现位置：[source/blender/modifiers/intern/MOD_armature.cc](../../../../../../../../source/blender/modifiers/intern/MOD_armature.cc) · L64—L74。

接口参数：

- `const Scene *`
- `ModifierData *md`
- `bool`

**教学注释版**

<!-- annotated:036cee4ca90c84 -->

```cpp
static bool is_disabled(const Scene * /*scene*/, ModifierData *md, bool /*use_render_params*/)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);

  /* The object type check is only needed here in case we have a placeholder
   * object assigned (because the library containing the armature is missing).
   *
   * In other cases it should be impossible to have a type mismatch.
   */
  return !amd->object || amd->object->type != OB_ARMATURE;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_armature.cc · L64—L74</summary>

<!-- original:036cee4ca90c84:source/blender/modifiers/intern/MOD_armature.cc:64:74 -->

```cpp
static bool is_disabled(const Scene * /*scene*/, ModifierData *md, bool /*use_render_params*/)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);

  /* The object type check is only needed here in case we have a placeholder
   * object assigned (because the library containing the armature is missing).
   *
   * In other cases it should be impossible to have a type mismatch.
   */
  return !amd->object || amd->object->type != OB_ARMATURE;
}
```

</details>

**结果出口**

- `return !amd->object || amd->object->type != OB_ARMATURE;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-af1634a00f579e50"></a>

### `blender::foreach_ID_link`

实现位置：[source/blender/modifiers/intern/MOD_armature.cc](../../../../../../../../source/blender/modifiers/intern/MOD_armature.cc) · L76—L81。

接口参数：

- `ModifierData *md`
- `Object *ob`
- `IDWalkFunc walk`
- `void *user_data`

**教学注释版**

<!-- annotated:15a877b29e9629 -->

```cpp
static void foreach_ID_link(ModifierData *md, Object *ob, IDWalkFunc walk, void *user_data)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);

  walk(user_data, ob, reinterpret_cast<ID **>(&amd->object), IDWALK_CB_NOP);
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_armature.cc · L76—L81</summary>

<!-- original:15a877b29e9629:source/blender/modifiers/intern/MOD_armature.cc:76:81 -->

```cpp
static void foreach_ID_link(ModifierData *md, Object *ob, IDWalkFunc walk, void *user_data)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);

  walk(user_data, ob, reinterpret_cast<ID **>(&amd->object), IDWALK_CB_NOP);
}
```

</details>

**继续追踪实现**

- `walk` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L80。

<a id="f-7e55879779d93145"></a>

### `blender::update_depsgraph`

实现位置：[source/blender/modifiers/intern/MOD_armature.cc](../../../../../../../../source/blender/modifiers/intern/MOD_armature.cc) · L83—L113。

接口参数：

- `ModifierData *md`
- `const ModifierUpdateDepsgraphContext *ctx`

**教学注释版**

<!-- annotated:5f003594728a51 -->

```cpp
static void update_depsgraph(ModifierData *md, const ModifierUpdateDepsgraphContext *ctx)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
  if (amd->object != nullptr) {
    /* If not using envelopes,
     * create relations to individual bones for more rigging flexibility. */
    if ((amd->deformflag & ARM_DEF_ENVELOPE) == 0 && (amd->object->pose != nullptr) &&
        ELEM(ctx->object->type, OB_MESH, OB_LATTICE))
    {
      /* If neither vertex groups nor envelopes are used, the modifier has no bone dependencies. */
      if ((amd->deformflag & ARM_DEF_VGROUP) != 0) {
        /* Enumerate groups that match existing bones. */
        const ListBaseT<bDeformGroup> *defbase = BKE_object_defgroup_list(ctx->object);
        for (bDeformGroup &dg : *defbase) {
          if (BKE_pose_channel_find_name(amd->object->pose, dg.name) != nullptr) {
            /* Can't check BONE_NO_DEFORM because it can be animated. */
            DEG_add_bone_relation(
                ctx->node, amd->object, dg.name, DEG_OB_COMP_BONE, "Armature Modifier");
          }
        }
      }
    }
    /* Otherwise require the whole pose to be complete. */
    else {
      DEG_add_object_relation(ctx->node, amd->object, DEG_OB_COMP_EVAL_POSE, "Armature Modifier");
    }

    DEG_add_object_relation(ctx->node, amd->object, DEG_OB_COMP_TRANSFORM, "Armature Modifier");
  }
  DEG_add_depends_on_transform_relation(ctx->node, "Armature Modifier");
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_armature.cc · L83—L113</summary>

<!-- original:5f003594728a51:source/blender/modifiers/intern/MOD_armature.cc:83:113 -->

```cpp
static void update_depsgraph(ModifierData *md, const ModifierUpdateDepsgraphContext *ctx)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
  if (amd->object != nullptr) {
    /* If not using envelopes,
     * create relations to individual bones for more rigging flexibility. */
    if ((amd->deformflag & ARM_DEF_ENVELOPE) == 0 && (amd->object->pose != nullptr) &&
        ELEM(ctx->object->type, OB_MESH, OB_LATTICE))
    {
      /* If neither vertex groups nor envelopes are used, the modifier has no bone dependencies. */
      if ((amd->deformflag & ARM_DEF_VGROUP) != 0) {
        /* Enumerate groups that match existing bones. */
        const ListBaseT<bDeformGroup> *defbase = BKE_object_defgroup_list(ctx->object);
        for (bDeformGroup &dg : *defbase) {
          if (BKE_pose_channel_find_name(amd->object->pose, dg.name) != nullptr) {
            /* Can't check BONE_NO_DEFORM because it can be animated. */
            DEG_add_bone_relation(
                ctx->node, amd->object, dg.name, DEG_OB_COMP_BONE, "Armature Modifier");
          }
        }
      }
    }
    /* Otherwise require the whole pose to be complete. */
    else {
      DEG_add_object_relation(ctx->node, amd->object, DEG_OB_COMP_EVAL_POSE, "Armature Modifier");
    }

    DEG_add_object_relation(ctx->node, amd->object, DEG_OB_COMP_TRANSFORM, "Armature Modifier");
  }
  DEG_add_depends_on_transform_relation(ctx->node, "Armature Modifier");
}
```

</details>

**继续追踪实现**

- `ELEM` → [ELEM · L88](../../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-d28724a15928)；[ELEM · L135](../../../01-BLI基础库/BLI_utildefines.hh.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `BKE_object_defgroup_list` → [blender::BKE_object_defgroup_list · L591](../../../02-BKE几何与数据/intern/deform.cc.md#f-26f2f33daee59e8d)。
- `BKE_pose_channel_find_name` → [blender::BKE_pose_channel_find_name · L895](../../../02-BKE几何与数据/intern/action.cc.md#f-5997206551bfc9f9)。
- `DEG_add_bone_relation` → [blender::DEG_add_bone_relation · L189](../../../06-Depsgraph依赖图/intern/depsgraph_build.cc.md#f-39e93b3cc8a9913c)。
- `DEG_add_object_relation` → [blender::DEG_add_object_relation · L123](../../../06-Depsgraph依赖图/intern/depsgraph_build.cc.md#f-f570cffae97e273c)。
- `DEG_add_depends_on_transform_relation` → [blender::DEG_add_depends_on_transform_relation · L240](../../../06-Depsgraph依赖图/intern/depsgraph_build.cc.md#f-47c32a354defa20d)。

<a id="f-00659aeadfbf2ac6"></a>

### `blender::deform_verts`

实现位置：[source/blender/modifiers/intern/MOD_armature.cc](../../../../../../../../source/blender/modifiers/intern/MOD_armature.cc) · L115—L140。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `Mesh *mesh`
- `MutableSpan<float3> positions`

**教学注释版**

<!-- annotated:a3e7676504d785 -->

```cpp
static void deform_verts(ModifierData *md,
                         const ModifierEvalContext *ctx,
                         Mesh *mesh,
                         MutableSpan<float3> positions)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
  std::optional<Span<float3>> vert_coords_prev;
  if (amd->vert_coords_prev) {
    // [讲解] positions.size：查询视图长度或生成对应有效索引区间。
    vert_coords_prev = {reinterpret_cast<float3 *>(amd->vert_coords_prev), positions.size()};
  }

  /* if next modifier needs original vertices */
  // [讲解] positions.data：返回借用范围的地址。
  MOD_previous_vcos_store(md, reinterpret_cast<float (*)[3]>(positions.data()));

  BKE_armature_deform_coords_with_mesh(*amd->object,
                                       *ctx->object,
                                       positions,
                                       vert_coords_prev,
                                       std::nullopt,
                                       amd->deformflag,
                                       amd->defgrp_name,
                                       mesh);

  /* free cache */
  MEM_SAFE_DELETE(amd->vert_coords_prev);
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_armature.cc · L115—L140</summary>

<!-- original:a3e7676504d785:source/blender/modifiers/intern/MOD_armature.cc:115:140 -->

```cpp
static void deform_verts(ModifierData *md,
                         const ModifierEvalContext *ctx,
                         Mesh *mesh,
                         MutableSpan<float3> positions)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
  std::optional<Span<float3>> vert_coords_prev;
  if (amd->vert_coords_prev) {
    vert_coords_prev = {reinterpret_cast<float3 *>(amd->vert_coords_prev), positions.size()};
  }

  /* if next modifier needs original vertices */
  MOD_previous_vcos_store(md, reinterpret_cast<float (*)[3]>(positions.data()));

  BKE_armature_deform_coords_with_mesh(*amd->object,
                                       *ctx->object,
                                       positions,
                                       vert_coords_prev,
                                       std::nullopt,
                                       amd->deformflag,
                                       amd->defgrp_name,
                                       mesh);

  /* free cache */
  MEM_SAFE_DELETE(amd->vert_coords_prev);
}
```

</details>

**沿实际写入检查状态**

- `vert_coords_prev = {reinterpret_cast<float3 *>(amd->vert_coords_prev), positions.size()};`

**继续追踪实现**

- `positions.size` → [blender::MutableSpan::size · L499](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-1de6a66839c304a8)；[blender::gpu::shader::parser::MutableSpan::size · L87](../../gpu/shader_tool/utils.hh.md#f-5e684af6ee7990e9)。同名重载需按实参类型选择。
- `MOD_previous_vcos_store` → [blender::MOD_previous_vcos_store · L144](MOD_util.cc.md#f-3c67667357b76b7a)。
- `positions.data` → [blender::MutableSpan::data · L545](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-eb45a6e4d8211efd)；[blender::gpu::shader::parser::MutableSpan::data · L82](../../gpu/shader_tool/utils.hh.md#f-ad0a09cec9741c65)。同名重载需按实参类型选择。
- `BKE_armature_deform_coords_with_mesh` → [blender::BKE_armature_deform_coords_with_mesh · L657](../../../02-BKE几何与数据/intern/armature_deform.cc.md#f-eb8c52b76299642a)。
- `MEM_SAFE_DELETE` → [MEM_SAFE_DELETE · L436](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#m-eadb3bc5b902)。宏定义由构建条件选择。

<a id="f-74bd4b13e2fb3829"></a>

### `blender::deform_verts_EM`

实现位置：[source/blender/modifiers/intern/MOD_armature.cc](../../../../../../../../source/blender/modifiers/intern/MOD_armature.cc) · L142—L172。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `const BMEditMesh *`
- `Mesh *mesh`
- `MutableSpan<float3> positions`

**教学注释版**

<!-- annotated:5cd52f1fad231a -->

```cpp
static void deform_verts_EM(ModifierData *md,
                            const ModifierEvalContext *ctx,
                            const BMEditMesh * /*em*/,
                            Mesh *mesh,
                            MutableSpan<float3> positions)
{
  if (mesh->runtime->wrapper_type == ME_WRAPPER_TYPE_MDATA) {
    deform_verts(md, ctx, mesh, positions);
    return;
  }

  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
  std::optional<Span<float3>> vert_coords_prev;
  if (amd->vert_coords_prev) {
    // [讲解] positions.size：查询视图长度或生成对应有效索引区间。
    vert_coords_prev = {reinterpret_cast<float3 *>(amd->vert_coords_prev), positions.size()};
  }

  /* if next modifier needs original vertices */
  // [讲解] positions.data：返回借用范围的地址。
  MOD_previous_vcos_store(md, reinterpret_cast<float (*)[3]>(positions.data()));

  BKE_armature_deform_coords_with_editmesh(*amd->object,
                                           *ctx->object,
                                           positions,
                                           vert_coords_prev,
                                           std::nullopt,
                                           amd->deformflag,
                                           amd->defgrp_name);

  /* free cache */
  MEM_SAFE_DELETE(amd->vert_coords_prev);
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_armature.cc · L142—L172</summary>

<!-- original:5cd52f1fad231a:source/blender/modifiers/intern/MOD_armature.cc:142:172 -->

```cpp
static void deform_verts_EM(ModifierData *md,
                            const ModifierEvalContext *ctx,
                            const BMEditMesh * /*em*/,
                            Mesh *mesh,
                            MutableSpan<float3> positions)
{
  if (mesh->runtime->wrapper_type == ME_WRAPPER_TYPE_MDATA) {
    deform_verts(md, ctx, mesh, positions);
    return;
  }

  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
  std::optional<Span<float3>> vert_coords_prev;
  if (amd->vert_coords_prev) {
    vert_coords_prev = {reinterpret_cast<float3 *>(amd->vert_coords_prev), positions.size()};
  }

  /* if next modifier needs original vertices */
  MOD_previous_vcos_store(md, reinterpret_cast<float (*)[3]>(positions.data()));

  BKE_armature_deform_coords_with_editmesh(*amd->object,
                                           *ctx->object,
                                           positions,
                                           vert_coords_prev,
                                           std::nullopt,
                                           amd->deformflag,
                                           amd->defgrp_name);

  /* free cache */
  MEM_SAFE_DELETE(amd->vert_coords_prev);
}
```

</details>

**沿实际写入检查状态**

- `vert_coords_prev = {reinterpret_cast<float3 *>(amd->vert_coords_prev), positions.size()};`

**继续追踪实现**

- `deform_verts` → [blender::deform_verts · L115](MOD_armature.cc.md#f-00659aeadfbf2ac6)。
- `positions.size` → [blender::MutableSpan::size · L499](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-1de6a66839c304a8)；[blender::gpu::shader::parser::MutableSpan::size · L87](../../gpu/shader_tool/utils.hh.md#f-5e684af6ee7990e9)。同名重载需按实参类型选择。
- `MOD_previous_vcos_store` → [blender::MOD_previous_vcos_store · L144](MOD_util.cc.md#f-3c67667357b76b7a)。
- `positions.data` → [blender::MutableSpan::data · L545](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-eb45a6e4d8211efd)；[blender::gpu::shader::parser::MutableSpan::data · L82](../../gpu/shader_tool/utils.hh.md#f-ad0a09cec9741c65)。同名重载需按实参类型选择。
- `BKE_armature_deform_coords_with_editmesh` → [blender::BKE_armature_deform_coords_with_editmesh · L715](../../../02-BKE几何与数据/intern/armature_deform.cc.md#f-3bd9369aa741c352)。
- `MEM_SAFE_DELETE` → [MEM_SAFE_DELETE · L436](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#m-eadb3bc5b902)。宏定义由构建条件选择。

<a id="f-75ae734856c7c55e"></a>

### `blender::deform_matrices`

实现位置：[source/blender/modifiers/intern/MOD_armature.cc](../../../../../../../../source/blender/modifiers/intern/MOD_armature.cc) · L191—L206。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `Mesh *mesh`
- `MutableSpan<float3> positions`
- `MutableSpan<float3x3> matrices`

**教学注释版**

<!-- annotated:35c36f244e2454 -->

```cpp
static void deform_matrices(ModifierData *md,
                            const ModifierEvalContext *ctx,
                            Mesh *mesh,
                            MutableSpan<float3> positions,
                            MutableSpan<float3x3> matrices)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
  BKE_armature_deform_coords_with_mesh(*amd->object,
                                       *ctx->object,
                                       positions,
                                       std::nullopt,
                                       matrices,
                                       amd->deformflag,
                                       amd->defgrp_name,
                                       mesh);
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_armature.cc · L191—L206</summary>

<!-- original:35c36f244e2454:source/blender/modifiers/intern/MOD_armature.cc:191:206 -->

```cpp
static void deform_matrices(ModifierData *md,
                            const ModifierEvalContext *ctx,
                            Mesh *mesh,
                            MutableSpan<float3> positions,
                            MutableSpan<float3x3> matrices)
{
  ArmatureModifierData *amd = reinterpret_cast<ArmatureModifierData *>(md);
  BKE_armature_deform_coords_with_mesh(*amd->object,
                                       *ctx->object,
                                       positions,
                                       std::nullopt,
                                       matrices,
                                       amd->deformflag,
                                       amd->defgrp_name,
                                       mesh);
}
```

</details>

**继续追踪实现**

- `BKE_armature_deform_coords_with_mesh` → [blender::BKE_armature_deform_coords_with_mesh · L657](../../../02-BKE几何与数据/intern/armature_deform.cc.md#f-eb8c52b76299642a)。
