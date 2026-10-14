# 实现依赖专题：source/blender/modifiers/intern/MOD_cloth.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::init_data"]:::abstraction
  F1["blender::deform_verts"]:::compute
  F2["blender::update_depsgraph"]:::compute
  F3["blender::required_data_mask"]:::compute
  F4["blender::depends_on_time"]:::compute
  F5["blender::foreach_ID_link"]:::compute
  F1 -->|"显式调用"| F0
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
  F["MOD_cloth.cc实现"]:::compute
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

<a id="f-2cc6a0bec5491812"></a>

### `blender::init_data`

实现位置：[source/blender/modifiers/intern/MOD_cloth.cc](../../../../../source/blender/modifiers/intern/MOD_cloth.cc) · L48—L70。

接口参数：

- `ModifierData *md`

**教学注释版**

<!-- annotated:8d42cd741b947a -->

```cpp
static void init_data(ModifierData *md)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);

  INIT_DEFAULT_STRUCT_AFTER(clmd, modifier);
  clmd->sim_parms = MEM_new<ClothSimSettings>(__func__);
  clmd->coll_parms = MEM_new<ClothCollSettings>(__func__);

  clmd->point_cache = BKE_ptcache_add(&clmd->ptcaches);

  /* check for alloc failing */
  if (!clmd->sim_parms || !clmd->coll_parms || !clmd->point_cache) {
    return;
  }

  if (!clmd->sim_parms->effector_weights) {
    clmd->sim_parms->effector_weights = BKE_effector_add_weights(nullptr);
  }

  if (clmd->point_cache) {
    clmd->point_cache->step = 1;
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_cloth.cc · L48—L70</summary>

<!-- original:8d42cd741b947a:source/blender/modifiers/intern/MOD_cloth.cc:48:70 -->

```cpp
static void init_data(ModifierData *md)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);

  INIT_DEFAULT_STRUCT_AFTER(clmd, modifier);
  clmd->sim_parms = MEM_new<ClothSimSettings>(__func__);
  clmd->coll_parms = MEM_new<ClothCollSettings>(__func__);

  clmd->point_cache = BKE_ptcache_add(&clmd->ptcaches);

  /* check for alloc failing */
  if (!clmd->sim_parms || !clmd->coll_parms || !clmd->point_cache) {
    return;
  }

  if (!clmd->sim_parms->effector_weights) {
    clmd->sim_parms->effector_weights = BKE_effector_add_weights(nullptr);
  }

  if (clmd->point_cache) {
    clmd->point_cache->step = 1;
  }
}
```

</details>

**沿实际写入检查状态**

- `clmd->sim_parms = MEM_new<ClothSimSettings>(__func__);`
- `clmd->coll_parms = MEM_new<ClothCollSettings>(__func__);`
- `clmd->point_cache = BKE_ptcache_add(&clmd->ptcaches);`
- `clmd->sim_parms->effector_weights = BKE_effector_add_weights(nullptr);`
- `clmd->point_cache->step = 1;`

**继续追踪实现**

- `INIT_DEFAULT_STRUCT_AFTER` → [INIT_DEFAULT_STRUCT_AFTER · L422](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_utildefines-293a0a.md#m-30b1f74075b1)。宏定义由构建条件选择。
- `MEM_new<ClothSimSettings>` → [MEM_new · L351](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-115f9b6784f89912)。
- `MEM_new<ClothCollSettings>` → [MEM_new · L351](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-115f9b6784f89912)。
- `BKE_ptcache_add` → [blender::BKE_ptcache_add · L2946](%E4%BE%9D%E8%B5%96-pointcache-0bc3be.md#f-38defead0f419693)。
- `BKE_effector_add_weights` → [blender::BKE_effector_add_weights · L63](%E4%BE%9D%E8%B5%96-effect-9eb97f.md#f-ce184d2946a57299)。

<a id="f-3cf7020249825dc5"></a>

### `blender::deform_verts`

实现位置：[source/blender/modifiers/intern/MOD_cloth.cc](../../../../../source/blender/modifiers/intern/MOD_cloth.cc) · L72—L119。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `Mesh *mesh`
- `MutableSpan<float3> positions`

**教学注释版**

<!-- annotated:c1f7bb838620fb -->

```cpp
static void deform_verts(ModifierData *md,
                         const ModifierEvalContext *ctx,
                         Mesh *mesh,
                         MutableSpan<float3> positions)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);
  Scene *scene = DEG_get_evaluated_scene(ctx->depsgraph);

  /* check for alloc failing */
  if (!clmd->sim_parms || !clmd->coll_parms) {
    init_data(md);

    if (!clmd->sim_parms || !clmd->coll_parms) {
      return;
    }
  }

  /* TODO(sergey): For now it actually duplicates logic from mesh_data_update.cc
   * and needs some more generic solution. But starting experimenting with
   * this so close to the release is not that nice..
   *
   * Also hopefully new cloth system will arrive soon..
   */
  if (mesh == nullptr && clmd->sim_parms->shapekey_rest) {
    KeyBlock *kb = BKE_keyblock_find_by_index(BKE_key_from_object(ctx->object),
                                              clmd->sim_parms->shapekey_rest);
    if (kb && kb->data != nullptr) {
      float (*layerorco)[3] = static_cast<float (*)[3]>(
          CustomData_get_layer_for_write(&mesh->vert_data, CD_CLOTH_ORCO, mesh->verts_num));
      if (!layerorco) {
        layerorco = static_cast<float (*)[3]>(CustomData_add_layer(
            &mesh->vert_data, CD_CLOTH_ORCO, CD_SET_DEFAULT, mesh->verts_num));
      }

      // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
      memcpy(layerorco, kb->data, sizeof(float[3]) * positions.size());
    }
  }

  mesh->vert_positions_for_write().copy_from(positions);
  mesh->tag_positions_changed();

  clothModifier_do(clmd,
                   ctx->depsgraph,
                   scene,
                   ctx->object,
                   mesh,
                   // [讲解] positions.data：返回借用范围的地址。
                   reinterpret_cast<float (*)[3]>(positions.data()));
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_cloth.cc · L72—L119</summary>

<!-- original:c1f7bb838620fb:source/blender/modifiers/intern/MOD_cloth.cc:72:119 -->

```cpp
static void deform_verts(ModifierData *md,
                         const ModifierEvalContext *ctx,
                         Mesh *mesh,
                         MutableSpan<float3> positions)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);
  Scene *scene = DEG_get_evaluated_scene(ctx->depsgraph);

  /* check for alloc failing */
  if (!clmd->sim_parms || !clmd->coll_parms) {
    init_data(md);

    if (!clmd->sim_parms || !clmd->coll_parms) {
      return;
    }
  }

  /* TODO(sergey): For now it actually duplicates logic from mesh_data_update.cc
   * and needs some more generic solution. But starting experimenting with
   * this so close to the release is not that nice..
   *
   * Also hopefully new cloth system will arrive soon..
   */
  if (mesh == nullptr && clmd->sim_parms->shapekey_rest) {
    KeyBlock *kb = BKE_keyblock_find_by_index(BKE_key_from_object(ctx->object),
                                              clmd->sim_parms->shapekey_rest);
    if (kb && kb->data != nullptr) {
      float (*layerorco)[3] = static_cast<float (*)[3]>(
          CustomData_get_layer_for_write(&mesh->vert_data, CD_CLOTH_ORCO, mesh->verts_num));
      if (!layerorco) {
        layerorco = static_cast<float (*)[3]>(CustomData_add_layer(
            &mesh->vert_data, CD_CLOTH_ORCO, CD_SET_DEFAULT, mesh->verts_num));
      }

      memcpy(layerorco, kb->data, sizeof(float[3]) * positions.size());
    }
  }

  mesh->vert_positions_for_write().copy_from(positions);
  mesh->tag_positions_changed();

  clothModifier_do(clmd,
                   ctx->depsgraph,
                   scene,
                   ctx->object,
                   mesh,
                   reinterpret_cast<float (*)[3]>(positions.data()));
}
```

</details>

**沿实际写入检查状态**

- `layerorco = static_cast<float (*)[3]>(CustomData_add_layer(`

**继续追踪实现**

- `DEG_get_evaluated_scene` → [blender::DEG_get_evaluated_scene · L212](../11-Depsgraph%E4%B8%8E%E5%B9%B6%E8%A1%8C%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F/%E4%BE%9D%E8%B5%96-depsgraph_query-e8b1e4.md#f-be7729d26a71d3fd)。
- `init_data` → [blender::init_data · L48](%E4%BE%9D%E8%B5%96-MOD_cloth-232a0e.md#f-2cc6a0bec5491812)。
- `BKE_keyblock_find_by_index` → [blender::BKE_keyblock_find_by_index · L1425](%E4%BE%9D%E8%B5%96-key-2b3be3.md#f-0693ed595207ecc7)。
- `BKE_key_from_object` → [blender::BKE_key_from_object · L1311](%E4%BE%9D%E8%B5%96-key-2b3be3.md#f-c191304ae3a652d6)。
- `CustomData_get_layer_for_write` → [blender::CustomData_get_layer_for_write · L3318](%E4%BE%9D%E8%B5%96-customdata-2eef81.md#f-6af158905e2c1274)。
- `CustomData_add_layer` → [blender::CustomData_add_layer · L2851](%E4%BE%9D%E8%B5%96-customdata-2eef81.md#f-4c7988e825541059)。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
- `positions.size` → [blender::MutableSpan::size · L499](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-1de6a66839c304a8)；[blender::gpu::shader::parser::MutableSpan::size · L87](%E4%BE%9D%E8%B5%96-utils-06433d.md#f-5e684af6ee7990e9)。同名重载需按实参类型选择。
- `mesh->vert_positions_for_write().copy_from` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L110。
- `mesh->vert_positions_for_write` → [Mesh::vert_positions_for_write · L1199](03-MPoly%E8%BF%81%E7%A7%BB%E4%B8%8E%E5%85%BC%E5%AE%B9.md#f-ae8d77205112d843)。
- `mesh->tag_positions_changed` → [blender::Mesh::tag_positions_changed · L407](../06-%E9%9A%90%E5%BC%8F%E5%85%B1%E4%BA%AB%E4%B8%8E%E7%BC%93%E5%AD%98%E7%B3%BB%E7%BB%9F/10-%E5%B1%80%E9%83%A8%E6%9B%B4%E6%96%B0%E4%B8%8E%E5%A4%B1%E6%95%88%E4%BF%AE%E5%A4%8D.md#f-90e852663d44ad53)。
- `clothModifier_do` → [blender::clothModifier_do · L327](%E4%BE%9D%E8%B5%96-cloth-91d9f7.md#f-187ebaf7bab8982f)。
- `positions.data` → [blender::MutableSpan::data · L545](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-eb45a6e4d8211efd)；[blender::gpu::shader::parser::MutableSpan::data · L82](%E4%BE%9D%E8%B5%96-utils-06433d.md#f-ad0a09cec9741c65)。同名重载需按实参类型选择。

<a id="f-d787b79293fff917"></a>

### `blender::update_depsgraph`

实现位置：[source/blender/modifiers/intern/MOD_cloth.cc](../../../../../source/blender/modifiers/intern/MOD_cloth.cc) · L121—L137。

接口参数：

- `ModifierData *md`
- `const ModifierUpdateDepsgraphContext *ctx`

**教学注释版**

<!-- annotated:5205b0360de4a1 -->

```cpp
static void update_depsgraph(ModifierData *md, const ModifierUpdateDepsgraphContext *ctx)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);
  if (clmd != nullptr) {
    if (clmd->coll_parms->flags & CLOTH_COLLSETTINGS_FLAG_ENABLED) {
      DEG_add_collision_relations(ctx->node,
                                  ctx->object,
                                  clmd->coll_parms->group,
                                  eModifierType_Collision,
                                  nullptr,
                                  "Cloth Collision");
    }
    DEG_add_forcefield_relations(
        ctx->node, ctx->object, clmd->sim_parms->effector_weights, true, 0, "Cloth Field");
  }
  DEG_add_depends_on_transform_relation(ctx->node, "Cloth Modifier");
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_cloth.cc · L121—L137</summary>

<!-- original:5205b0360de4a1:source/blender/modifiers/intern/MOD_cloth.cc:121:137 -->

```cpp
static void update_depsgraph(ModifierData *md, const ModifierUpdateDepsgraphContext *ctx)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);
  if (clmd != nullptr) {
    if (clmd->coll_parms->flags & CLOTH_COLLSETTINGS_FLAG_ENABLED) {
      DEG_add_collision_relations(ctx->node,
                                  ctx->object,
                                  clmd->coll_parms->group,
                                  eModifierType_Collision,
                                  nullptr,
                                  "Cloth Collision");
    }
    DEG_add_forcefield_relations(
        ctx->node, ctx->object, clmd->sim_parms->effector_weights, true, 0, "Cloth Field");
  }
  DEG_add_depends_on_transform_relation(ctx->node, "Cloth Modifier");
}
```

</details>

**继续追踪实现**

- `DEG_add_collision_relations` → [blender::DEG_add_collision_relations · L112](../11-Depsgraph%E4%B8%8E%E5%B9%B6%E8%A1%8C%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F/%E4%BE%9D%E8%B5%96-depsgraph_physics-40d348.md#f-a8a23fb36db5feb5)。
- `DEG_add_forcefield_relations` → [blender::DEG_add_forcefield_relations · L203](../11-Depsgraph%E4%B8%8E%E5%B9%B6%E8%A1%8C%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F/%E4%BE%9D%E8%B5%96-depsgraph_physics-40d348.md#f-1a87e7be20724278)。
- `DEG_add_depends_on_transform_relation` → [blender::DEG_add_depends_on_transform_relation · L240](../11-Depsgraph%E4%B8%8E%E5%B9%B6%E8%A1%8C%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F/%E4%BE%9D%E8%B5%96-depsgraph_build-ea2fc8.md#f-47c32a354defa20d)。

<a id="f-09d56e8404c6885b"></a>

### `blender::required_data_mask`

实现位置：[source/blender/modifiers/intern/MOD_cloth.cc](../../../../../source/blender/modifiers/intern/MOD_cloth.cc) · L139—L150。

接口参数：

- `ModifierData *md`
- `CustomData_MeshMasks *r_cddata_masks`

**教学注释版**

<!-- annotated:cb9dfc88e6f5d3 -->

```cpp
static void required_data_mask(ModifierData *md, CustomData_MeshMasks *r_cddata_masks)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);

  if (cloth_uses_vgroup(clmd)) {
    r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;
  }

  if (clmd->sim_parms->shapekey_rest != 0) {
    r_cddata_masks->vmask |= CD_MASK_CLOTH_ORCO;
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_cloth.cc · L139—L150</summary>

<!-- original:cb9dfc88e6f5d3:source/blender/modifiers/intern/MOD_cloth.cc:139:150 -->

```cpp
static void required_data_mask(ModifierData *md, CustomData_MeshMasks *r_cddata_masks)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);

  if (cloth_uses_vgroup(clmd)) {
    r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;
  }

  if (clmd->sim_parms->shapekey_rest != 0) {
    r_cddata_masks->vmask |= CD_MASK_CLOTH_ORCO;
  }
}
```

</details>

**沿实际写入检查状态**

- `r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;`
- `r_cddata_masks->vmask |= CD_MASK_CLOTH_ORCO;`

**继续追踪实现**

- `cloth_uses_vgroup` → [blender::cloth_uses_vgroup · L599](%E4%BE%9D%E8%B5%96-cloth-91d9f7.md#f-ecde1d0a422584e4)。

<a id="f-c6403bc2d5884a87"></a>

### `blender::depends_on_time`

实现位置：[source/blender/modifiers/intern/MOD_cloth.cc](../../../../../source/blender/modifiers/intern/MOD_cloth.cc) · L193—L196。

接口参数：

- `Scene *`
- `ModifierData *`

**教学注释版**

<!-- annotated:7c39a83ba9282f -->

```cpp
static bool depends_on_time(Scene * /*scene*/, ModifierData * /*md*/)
{
  return true;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_cloth.cc · L193—L196</summary>

<!-- original:7c39a83ba9282f:source/blender/modifiers/intern/MOD_cloth.cc:193:196 -->

```cpp
static bool depends_on_time(Scene * /*scene*/, ModifierData * /*md*/)
{
  return true;
}
```

</details>

**结果出口**

- `return true;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-a5fd681b7408cce9"></a>

### `blender::foreach_ID_link`

实现位置：[source/blender/modifiers/intern/MOD_cloth.cc](../../../../../source/blender/modifiers/intern/MOD_cloth.cc) · L237—L251。

接口参数：

- `ModifierData *md`
- `Object *ob`
- `IDWalkFunc walk`
- `void *user_data`

**教学注释版**

<!-- annotated:93d349d76dd21f -->

```cpp
static void foreach_ID_link(ModifierData *md, Object *ob, IDWalkFunc walk, void *user_data)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);

  if (clmd->coll_parms) {
    walk(user_data, ob, reinterpret_cast<ID **>(&clmd->coll_parms->group), IDWALK_CB_NOP);
  }

  if (clmd->sim_parms && clmd->sim_parms->effector_weights) {
    walk(user_data,
         ob,
         reinterpret_cast<ID **>(&clmd->sim_parms->effector_weights->group),
         IDWALK_CB_USER);
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_cloth.cc · L237—L251</summary>

<!-- original:93d349d76dd21f:source/blender/modifiers/intern/MOD_cloth.cc:237:251 -->

```cpp
static void foreach_ID_link(ModifierData *md, Object *ob, IDWalkFunc walk, void *user_data)
{
  ClothModifierData *clmd = reinterpret_cast<ClothModifierData *>(md);

  if (clmd->coll_parms) {
    walk(user_data, ob, reinterpret_cast<ID **>(&clmd->coll_parms->group), IDWALK_CB_NOP);
  }

  if (clmd->sim_parms && clmd->sim_parms->effector_weights) {
    walk(user_data,
         ob,
         reinterpret_cast<ID **>(&clmd->sim_parms->effector_weights->group),
         IDWALK_CB_USER);
  }
}
```

</details>

**继续追踪实现**

- `walk` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L242。
