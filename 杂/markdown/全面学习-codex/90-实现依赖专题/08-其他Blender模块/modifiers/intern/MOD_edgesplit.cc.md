# 实现依赖专题：source/blender/modifiers/intern/MOD_edgesplit.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::doEdgeSplit"]:::abstraction
  F1["blender::modify_mesh"]:::compute
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
  F["MOD_edgesplit.cc实现"]:::compute
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

<a id="f-9bd852998740a6eb"></a>

### `blender::doEdgeSplit`

实现位置：[source/blender/modifiers/intern/MOD_edgesplit.cc](../../../../../../../../source/blender/modifiers/intern/MOD_edgesplit.cc) · L43—L109。

接口参数：

- `const Mesh *mesh`
- `EdgeSplitModifierData *emd`

**教学注释版**

<!-- annotated:55cb00d7a41847 -->

```cpp
Mesh *doEdgeSplit(const Mesh *mesh, EdgeSplitModifierData *emd)
{
  Mesh *result;
  BMesh *bm;
  BMIter iter;
  BMEdge *e;
  const float threshold = cosf(emd->split_angle + 0.000000175f);
  const bool do_split_angle = (emd->flags & MOD_EDGESPLIT_FROMANGLE) != 0 &&
                              emd->split_angle < float(M_PI);
  const bool do_split_all = do_split_angle && emd->split_angle < FLT_EPSILON;
  const bool calc_face_normals = do_split_angle && !do_split_all;

  BMeshCreateParams create_params{};
  BMeshFromMeshParams convert_params{};
  convert_params.calc_face_normal = calc_face_normals;
  convert_params.calc_vert_normal = false;
  convert_params.add_key_index = false;
  convert_params.use_shapekey = false;
  convert_params.active_shapekey = 0;
  convert_params.cd_mask_extra.vmask = CD_MASK_ORIGINDEX;
  convert_params.cd_mask_extra.emask = CD_MASK_ORIGINDEX;
  convert_params.cd_mask_extra.pmask = CD_MASK_ORIGINDEX;

  bm = BKE_mesh_to_bmesh_ex(mesh, &create_params, &convert_params);

  if (do_split_angle) {
    BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
      /* check for 1 edge having 2 face users */
      BMLoop *l1 = e->l;
      BMLoop *l2 = (e->l) ? e->l->radial_next : nullptr;
      if (l1 && l2 != l1) {
        if (/* 3+ faces on this edge, always split */
            UNLIKELY(l1 != l2->radial_next) ||
            /* O degree angle setting, we want to split on all edges. */
            do_split_all ||
            /* 2 face edge - check angle. */
            (dot_v3v3(l1->f->no, l2->f->no) < threshold))
        {
          BM_elem_flag_enable(e, BM_ELEM_TAG);
        }
      }
    }
  }

  if (emd->flags & MOD_EDGESPLIT_FROMFLAG) {
    BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
      /* check for 2 or more edge users */
      if ((e->l) && (e->l->next != e->l)) {
        if (!BM_elem_flag_test(e, BM_ELEM_SMOOTH)) {
          BM_elem_flag_enable(e, BM_ELEM_TAG);
        }
      }
    }
  }

  BM_mesh_edgesplit(bm, false, true, false);

  /* Uncomment for troubleshooting. */
  // BM_mesh_is_valid(bm);

  result = BKE_mesh_from_bmesh_for_eval_nomain(bm, nullptr, mesh);
  BM_mesh_free(bm);

  geometry::debug_randomize_mesh_order(result);

  return result;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_edgesplit.cc · L43—L109</summary>

<!-- original:55cb00d7a41847:source/blender/modifiers/intern/MOD_edgesplit.cc:43:109 -->

```cpp
Mesh *doEdgeSplit(const Mesh *mesh, EdgeSplitModifierData *emd)
{
  Mesh *result;
  BMesh *bm;
  BMIter iter;
  BMEdge *e;
  const float threshold = cosf(emd->split_angle + 0.000000175f);
  const bool do_split_angle = (emd->flags & MOD_EDGESPLIT_FROMANGLE) != 0 &&
                              emd->split_angle < float(M_PI);
  const bool do_split_all = do_split_angle && emd->split_angle < FLT_EPSILON;
  const bool calc_face_normals = do_split_angle && !do_split_all;

  BMeshCreateParams create_params{};
  BMeshFromMeshParams convert_params{};
  convert_params.calc_face_normal = calc_face_normals;
  convert_params.calc_vert_normal = false;
  convert_params.add_key_index = false;
  convert_params.use_shapekey = false;
  convert_params.active_shapekey = 0;
  convert_params.cd_mask_extra.vmask = CD_MASK_ORIGINDEX;
  convert_params.cd_mask_extra.emask = CD_MASK_ORIGINDEX;
  convert_params.cd_mask_extra.pmask = CD_MASK_ORIGINDEX;

  bm = BKE_mesh_to_bmesh_ex(mesh, &create_params, &convert_params);

  if (do_split_angle) {
    BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
      /* check for 1 edge having 2 face users */
      BMLoop *l1 = e->l;
      BMLoop *l2 = (e->l) ? e->l->radial_next : nullptr;
      if (l1 && l2 != l1) {
        if (/* 3+ faces on this edge, always split */
            UNLIKELY(l1 != l2->radial_next) ||
            /* O degree angle setting, we want to split on all edges. */
            do_split_all ||
            /* 2 face edge - check angle. */
            (dot_v3v3(l1->f->no, l2->f->no) < threshold))
        {
          BM_elem_flag_enable(e, BM_ELEM_TAG);
        }
      }
    }
  }

  if (emd->flags & MOD_EDGESPLIT_FROMFLAG) {
    BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
      /* check for 2 or more edge users */
      if ((e->l) && (e->l->next != e->l)) {
        if (!BM_elem_flag_test(e, BM_ELEM_SMOOTH)) {
          BM_elem_flag_enable(e, BM_ELEM_TAG);
        }
      }
    }
  }

  BM_mesh_edgesplit(bm, false, true, false);

  /* Uncomment for troubleshooting. */
  // BM_mesh_is_valid(bm);

  result = BKE_mesh_from_bmesh_for_eval_nomain(bm, nullptr, mesh);
  BM_mesh_free(bm);

  geometry::debug_randomize_mesh_order(result);

  return result;
}
```

</details>

**沿实际写入检查状态**

- `convert_params.calc_face_normal = calc_face_normals;`
- `convert_params.calc_vert_normal = false;`
- `convert_params.add_key_index = false;`
- `convert_params.use_shapekey = false;`
- `convert_params.active_shapekey = 0;`
- `convert_params.cd_mask_extra.vmask = CD_MASK_ORIGINDEX;`
- `convert_params.cd_mask_extra.emask = CD_MASK_ORIGINDEX;`
- `convert_params.cd_mask_extra.pmask = CD_MASK_ORIGINDEX;`
- `bm = BKE_mesh_to_bmesh_ex(mesh, &create_params, &convert_params);`
- `result = BKE_mesh_from_bmesh_for_eval_nomain(bm, nullptr, mesh);`

**结果出口**

- `return result;`

**继续追踪实现**

- `cosf` → [cosf · L20](../../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-cee9ebf67d86)；[cosf · L42](../../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-346533627567)；[cosf · L73](../../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-e01b94a43b72)；[cosf · L24](../../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-c317cb08dec6)；[cosf · L46](../../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-93325b515297)；[cosf · L77](../../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-d3058af0b490)；[cosf · L20](../../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-4c6aea22a560)；[cosf · L42](../../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-1fd6a5414477)；[cosf · L73](../../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-de2402f85270)；[cosf · L186](../../../07-Intern运行时与平台/cycles/kernel/device/oneapi/compat.h.md#m-7fdbd99009e0)；[cosf · L288](../../../07-Intern运行时与平台/cycles/kernel/device/metal/compat.h.md#m-68fe984e8b68)；[cosf · L93](../../../07-Intern运行时与平台/cycles/kernel/device/hip/compat.h.md#m-21bb557a23f1)；[cosf · L91](../../../07-Intern运行时与平台/cycles/kernel/device/cuda/compat.h.md#m-7721be419a49)；[cosf · L43](../../gpu/GPU_shader_shared_utils.hh.md#m-25d02fd11b3b)；[cosf · L64](../../gpu/GPU_shader_shared_utils.hh.md#m-698fc51ccda3)。宏定义由构建条件选择。
- `BKE_mesh_to_bmesh_ex` → [BKE_mesh_to_bmesh_ex · L1583](../../../../05-几何存储与拓扑映射/03-MPoly迁移与兼容.md#f-dd2f413684da0188)。
- `BM_ITER_MESH` → [BM_ITER_MESH · L72](../../bmesh/intern/bmesh_iterators.hh.md#m-cfc837c73218)。宏定义由构建条件选择。
- `UNLIKELY` → [UNLIKELY · L52](../../../07-Intern运行时与平台/guardedalloc/intern/mallocn_intern.hh.md#m-b66d81651173)；[UNLIKELY · L55](../../../07-Intern运行时与平台/guardedalloc/intern/mallocn_intern.hh.md#m-43069123e9fe)；[UNLIKELY · L108](../../../07-Intern运行时与平台/cycles/util/defines.h.md#m-c50729f638e8)；[UNLIKELY · L111](../../../07-Intern运行时与平台/cycles/util/defines.h.md#m-08e633831622)；[UNLIKELY · L25](../../../01-BLI基础库/intern/math_base_inline.cc.md#m-beab6e34c61e)；[UNLIKELY · L27](../../../01-BLI基础库/intern/math_base_inline.cc.md#m-9b279ffdd95b)；[UNLIKELY · L544](../../../01-BLI基础库/BLI_utildefines.hh.md#m-74644b8209a0)；[UNLIKELY · L547](../../../01-BLI基础库/BLI_utildefines.hh.md#m-3a47ebab6298)。宏定义由构建条件选择。
- `dot_v3v3` → [blender::dot_v3v3 · L646](../../../01-BLI基础库/intern/math_vector_inline.cc.md#f-c88befa67d07591a)。
- `BM_elem_flag_enable` → [BM_elem_flag_enable · L23](../../bmesh/intern/bmesh_inline.hh.md#m-4400242f1540)。宏定义由构建条件选择。
- `BM_elem_flag_test` → [BM_elem_flag_test · L21](../../bmesh/intern/bmesh_inline.hh.md#m-2431d1179b41)。宏定义由构建条件选择。
- `BM_mesh_edgesplit` → [blender::BM_mesh_edgesplit · L22](../../bmesh/tools/bmesh_edgesplit.cc.md#f-bcfd49ce12d30fa9)。
- `BKE_mesh_from_bmesh_for_eval_nomain` → [BKE_mesh_from_bmesh_for_eval_nomain · L1620](../../../../05-几何存储与拓扑映射/03-MPoly迁移与兼容.md#f-92b713674a1be50c)。
- `BM_mesh_free` → [blender::BM_mesh_free · L264](../../bmesh/intern/bmesh_mesh.cc.md#f-3871ddd58daba48c)。
- `geometry::debug_randomize_mesh_order` → [blender::geometry::debug_randomize_mesh_order · L305](../../../05-Geometry几何算法/intern/randomize.cc.md#f-268bd8d8f3608806)。

<a id="f-a36e9239c8ee43f5"></a>

### `blender::modify_mesh`

实现位置：[source/blender/modifiers/intern/MOD_edgesplit.cc](../../../../../../../../source/blender/modifiers/intern/MOD_edgesplit.cc) · L117—L129。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *`
- `Mesh *mesh`

**教学注释版**

<!-- annotated:9dcedb39f044b6 -->

```cpp
static Mesh *modify_mesh(ModifierData *md, const ModifierEvalContext * /*ctx*/, Mesh *mesh)
{
  Mesh *result;
  EdgeSplitModifierData *emd = reinterpret_cast<EdgeSplitModifierData *>(md);

  if (!(emd->flags & (MOD_EDGESPLIT_FROMANGLE | MOD_EDGESPLIT_FROMFLAG))) {
    return mesh;
  }

  result = doEdgeSplit(mesh, emd);

  return result;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_edgesplit.cc · L117—L129</summary>

<!-- original:9dcedb39f044b6:source/blender/modifiers/intern/MOD_edgesplit.cc:117:129 -->

```cpp
static Mesh *modify_mesh(ModifierData *md, const ModifierEvalContext * /*ctx*/, Mesh *mesh)
{
  Mesh *result;
  EdgeSplitModifierData *emd = reinterpret_cast<EdgeSplitModifierData *>(md);

  if (!(emd->flags & (MOD_EDGESPLIT_FROMANGLE | MOD_EDGESPLIT_FROMFLAG))) {
    return mesh;
  }

  result = doEdgeSplit(mesh, emd);

  return result;
}
```

</details>

**沿实际写入检查状态**

- `result = doEdgeSplit(mesh, emd);`

**结果出口**

- `return mesh;`
- `return result;`

**继续追踪实现**

- `doEdgeSplit` → [blender::doEdgeSplit · L43](MOD_edgesplit.cc.md#f-9bd852998740a6eb)。
