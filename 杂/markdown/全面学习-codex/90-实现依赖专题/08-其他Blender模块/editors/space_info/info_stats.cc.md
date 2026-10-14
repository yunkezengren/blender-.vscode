# 实现依赖专题：source/blender/editors/space_info/info_stats.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::stats_mesheval"]:::abstraction
  F1["blender::stats_object"]:::compute
  F2["blender::stats_object_edit"]:::compute
  F3["blender::stats_object_pose"]:::compute
  F4["blender::stats_is_object_dynamic_topology_sculpt"]:::compute
  F5["blender::stats_object_mesh_paint"]:::compute
  F6["blender::stats_update"]:::compute
  F7["blender::format_stats"]:::compute
  F1 -->|"显式调用"| F0
  F6 -->|"显式调用"| F2
  F6 -->|"显式调用"| F3
  F6 -->|"显式调用"| F5
  F6 -->|"显式调用"| F1
  F7 -->|"显式调用"| F6
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
  F["info_stats.cc实现"]:::compute
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

<a id="f-357409c603d3a27c"></a>

### `blender::stats_mesheval`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L108—L162。

接口参数：

- `const Mesh *mesh_eval`
- `bool is_selected`
- `SceneStats *stats`

**教学注释版**

<!-- annotated:6e770e42bf9483 -->

```cpp
static bool stats_mesheval(const Mesh *mesh_eval, bool is_selected, SceneStats *stats)
{
  if (mesh_eval == nullptr) {
    return false;
  }

  int totvert, totedge, totface, totloop;

  /* Get multires stats. */
  if (const std::unique_ptr<SubdivCCG> &subdiv_ccg = mesh_eval->runtime->subdiv_ccg) {
    BKE_subdiv_ccg_topology_counters(*subdiv_ccg, totvert, totedge, totface, totloop);
  }
  else {
    /* Get CPU subdivided mesh if it exists. */
    const SubsurfRuntimeData *subsurf_runtime_data = nullptr;
    if (mesh_eval->runtime->mesh_eval) {
      mesh_eval = mesh_eval->runtime->mesh_eval;
    }
    else {
      subsurf_runtime_data = mesh_eval->runtime->subsurf_runtime_data;
    }

    /* Get GPU subdivision stats if they exist. If there is no 3D viewport or the mesh is
     * hidden it will not be subdivided, fall back to unsubdivided in that case. */
    if (subsurf_runtime_data && subsurf_runtime_data->has_gpu_subdiv &&
        subsurf_runtime_data->stats_totvert)
    {
      totvert = subsurf_runtime_data->stats_totvert;
      totedge = subsurf_runtime_data->stats_totedge;
      totface = subsurf_runtime_data->stats_faces_num;
      totloop = subsurf_runtime_data->stats_totloop;
    }
    else {
      totvert = mesh_eval->verts_num;
      totedge = mesh_eval->edges_num;
      totface = mesh_eval->faces_num;
      totloop = mesh_eval->corners_num;
    }
  }

  stats->totvert += totvert;
  stats->totedge += totedge;
  stats->totface += totface;

  const int tottri = poly_to_tri_count(totface, totloop);
  stats->tottri += tottri;

  if (is_selected) {
    stats->totvertsel += totvert;
    stats->totedgesel += totedge;
    stats->totfacesel += totface;
    stats->tottrisel += tottri;
  }
  return true;
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L108—L162</summary>

<!-- original:6e770e42bf9483:source/blender/editors/space_info/info_stats.cc:108:162 -->

```cpp
static bool stats_mesheval(const Mesh *mesh_eval, bool is_selected, SceneStats *stats)
{
  if (mesh_eval == nullptr) {
    return false;
  }

  int totvert, totedge, totface, totloop;

  /* Get multires stats. */
  if (const std::unique_ptr<SubdivCCG> &subdiv_ccg = mesh_eval->runtime->subdiv_ccg) {
    BKE_subdiv_ccg_topology_counters(*subdiv_ccg, totvert, totedge, totface, totloop);
  }
  else {
    /* Get CPU subdivided mesh if it exists. */
    const SubsurfRuntimeData *subsurf_runtime_data = nullptr;
    if (mesh_eval->runtime->mesh_eval) {
      mesh_eval = mesh_eval->runtime->mesh_eval;
    }
    else {
      subsurf_runtime_data = mesh_eval->runtime->subsurf_runtime_data;
    }

    /* Get GPU subdivision stats if they exist. If there is no 3D viewport or the mesh is
     * hidden it will not be subdivided, fall back to unsubdivided in that case. */
    if (subsurf_runtime_data && subsurf_runtime_data->has_gpu_subdiv &&
        subsurf_runtime_data->stats_totvert)
    {
      totvert = subsurf_runtime_data->stats_totvert;
      totedge = subsurf_runtime_data->stats_totedge;
      totface = subsurf_runtime_data->stats_faces_num;
      totloop = subsurf_runtime_data->stats_totloop;
    }
    else {
      totvert = mesh_eval->verts_num;
      totedge = mesh_eval->edges_num;
      totface = mesh_eval->faces_num;
      totloop = mesh_eval->corners_num;
    }
  }

  stats->totvert += totvert;
  stats->totedge += totedge;
  stats->totface += totface;

  const int tottri = poly_to_tri_count(totface, totloop);
  stats->tottri += tottri;

  if (is_selected) {
    stats->totvertsel += totvert;
    stats->totedgesel += totedge;
    stats->totfacesel += totface;
    stats->tottrisel += tottri;
  }
  return true;
}
```

</details>

**沿实际写入检查状态**

- `mesh_eval = mesh_eval->runtime->mesh_eval;`
- `subsurf_runtime_data = mesh_eval->runtime->subsurf_runtime_data;`
- `totvert = subsurf_runtime_data->stats_totvert;`
- `totedge = subsurf_runtime_data->stats_totedge;`
- `totface = subsurf_runtime_data->stats_faces_num;`
- `totloop = subsurf_runtime_data->stats_totloop;`
- `totvert = mesh_eval->verts_num;`
- `totedge = mesh_eval->edges_num;`
- `totface = mesh_eval->faces_num;`
- `totloop = mesh_eval->corners_num;`
- `stats->totvert += totvert;`
- `stats->totedge += totedge;`
- `stats->totface += totface;`
- `stats->tottri += tottri;`
- `stats->totvertsel += totvert;`
- `stats->totedgesel += totedge;`
- `stats->totfacesel += totface;`
- `stats->tottrisel += tottri;`

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `BKE_subdiv_ccg_topology_counters` → [blender::BKE_subdiv_ccg_topology_counters · L890](../../../02-BKE几何与数据/intern/subdiv_ccg.cc.md#f-1126967ba29fc093)。
- `poly_to_tri_count` → [blender::poly_to_tri_count · L118](../../../01-BLI基础库/intern/math_geom_inline.cc.md#f-fd5a0e76d62e3b0b)。

<a id="f-24e070947cf1b34a"></a>

### `blender::stats_object`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L164—L236。

接口参数：

- `Object *ob`
- `const View3D *v3d_local`
- `SceneStats *stats`
- `Set<const Mesh *> &objects_gset`

**教学注释版**

<!-- annotated:d2fcf182db69c7 -->

```cpp
static void stats_object(Object *ob,
                         const View3D *v3d_local,
                         SceneStats *stats,
                         Set<const Mesh *> &objects_gset)
{
  if ((ob->base_flag & BASE_ENABLED_AND_VISIBLE_IN_DEFAULT_VIEWPORT) == 0) {
    return;
  }

  if (v3d_local && !BKE_object_is_visible_in_viewport(v3d_local, ob)) {
    return;
  }

  const bool is_selected = (ob->base_flag & BASE_SELECTED) != 0;

  stats->totobj++;
  if (is_selected) {
    stats->totobjsel++;
  }

  switch (ob->type) {
    case OB_MESH: {
      /* we assume evaluated mesh is already built, this strictly does stats now. */
      const Mesh *mesh_eval = BKE_object_get_evaluated_mesh_no_subsurf(ob);
      // [讲解] objects_gset.add：按哈希与相等关系加入键或键值。
      if (!objects_gset.add(mesh_eval)) {
        break;
      }
      stats_mesheval(mesh_eval, is_selected, stats);
      break;
    }
    case OB_LAMP:
      stats->totlamp++;
      if (is_selected) {
        stats->totlampsel++;
      }
      break;
    case OB_GREASE_PENCIL: {
      if (!is_selected) {
        break;
      }

      const GreasePencil *grease_pencil = id_cast<GreasePencil *>(ob->data);

      for (const GreasePencilDrawingBase *drawing_base : grease_pencil->drawings()) {
        const GreasePencilDrawing *drawing = reinterpret_cast<const GreasePencilDrawing *>(
            drawing_base);
        const bke::CurvesGeometry &curves = drawing->wrap().strokes();

        stats->totpoints += curves.points_num();
        stats->totgpstroke += curves.curves_num();
      }

      for (const bke::greasepencil::Layer *layer : grease_pencil->layers()) {
        stats->totgpframe += layer->frames().size();
      }

      stats->totgplayer += grease_pencil->layers().size();
      break;
    }
    case OB_CURVES: {
      const Curves &curves_id = *id_cast<Curves *>(ob->data);
      const bke::CurvesGeometry &curves = curves_id.geometry.wrap();
      stats->totpoints += curves.points_num();
      break;
    }
    case OB_POINTCLOUD:
    case OB_VOLUME: {
      break;
    }
    default:
      break;
  }
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L164—L236</summary>

<!-- original:d2fcf182db69c7:source/blender/editors/space_info/info_stats.cc:164:236 -->

```cpp
static void stats_object(Object *ob,
                         const View3D *v3d_local,
                         SceneStats *stats,
                         Set<const Mesh *> &objects_gset)
{
  if ((ob->base_flag & BASE_ENABLED_AND_VISIBLE_IN_DEFAULT_VIEWPORT) == 0) {
    return;
  }

  if (v3d_local && !BKE_object_is_visible_in_viewport(v3d_local, ob)) {
    return;
  }

  const bool is_selected = (ob->base_flag & BASE_SELECTED) != 0;

  stats->totobj++;
  if (is_selected) {
    stats->totobjsel++;
  }

  switch (ob->type) {
    case OB_MESH: {
      /* we assume evaluated mesh is already built, this strictly does stats now. */
      const Mesh *mesh_eval = BKE_object_get_evaluated_mesh_no_subsurf(ob);
      if (!objects_gset.add(mesh_eval)) {
        break;
      }
      stats_mesheval(mesh_eval, is_selected, stats);
      break;
    }
    case OB_LAMP:
      stats->totlamp++;
      if (is_selected) {
        stats->totlampsel++;
      }
      break;
    case OB_GREASE_PENCIL: {
      if (!is_selected) {
        break;
      }

      const GreasePencil *grease_pencil = id_cast<GreasePencil *>(ob->data);

      for (const GreasePencilDrawingBase *drawing_base : grease_pencil->drawings()) {
        const GreasePencilDrawing *drawing = reinterpret_cast<const GreasePencilDrawing *>(
            drawing_base);
        const bke::CurvesGeometry &curves = drawing->wrap().strokes();

        stats->totpoints += curves.points_num();
        stats->totgpstroke += curves.curves_num();
      }

      for (const bke::greasepencil::Layer *layer : grease_pencil->layers()) {
        stats->totgpframe += layer->frames().size();
      }

      stats->totgplayer += grease_pencil->layers().size();
      break;
    }
    case OB_CURVES: {
      const Curves &curves_id = *id_cast<Curves *>(ob->data);
      const bke::CurvesGeometry &curves = curves_id.geometry.wrap();
      stats->totpoints += curves.points_num();
      break;
    }
    case OB_POINTCLOUD:
    case OB_VOLUME: {
      break;
    }
    default:
      break;
  }
}
```

</details>

**沿实际写入检查状态**

- `stats->totpoints += curves.points_num();`
- `stats->totgpstroke += curves.curves_num();`
- `stats->totgpframe += layer->frames().size();`
- `stats->totgplayer += grease_pencil->layers().size();`

**继续追踪实现**

- `BKE_object_is_visible_in_viewport` → [blender::BKE_object_is_visible_in_viewport · L1702](../../../02-BKE几何与数据/intern/layer.cc.md#f-6be42a129fa5e016)。
- `BKE_object_get_evaluated_mesh_no_subsurf` → [blender::BKE_object_get_evaluated_mesh_no_subsurf · L4419](../../../02-BKE几何与数据/intern/object.cc.md#f-7f352b57780250ef)。
- `objects_gset.add` → [blender::Set::add · L248](../../../../02-哈希表与关联数据结构/08-Set与集合语义.md#f-c7498809c2327fba)；[blender::Set::add · L252](../../../../02-哈希表与关联数据结构/08-Set与集合语义.md#f-e3ac8d1c52c03c2b)。同名重载需按实参类型选择。
- `stats_mesheval` → [blender::stats_mesheval · L108](info_stats.cc.md#f-357409c603d3a27c)。
- `id_cast<GreasePencil *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `grease_pencil->drawings` → [blender::GreasePencil::drawings · L3338](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-4a9381efc430533a)；[blender::GreasePencil::drawings · L3343](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-75a528a69126428b)。同名重载需按实参类型选择。
- `drawing->wrap().strokes` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L210。
- `drawing->wrap` → [blender::GreasePencilDrawing::wrap · L1059](../../../02-BKE几何与数据/BKE_grease_pencil.hh.md#f-566c8db236585685)；[blender::GreasePencilDrawing::wrap · L1063](../../../02-BKE几何与数据/BKE_grease_pencil.hh.md#f-696df207288f4617)。同名重载需按实参类型选择。
- `curves.points_num` → [blender::bke::CurvesGeometry::points_num · L1001](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-049421b1f643c700)。
- `curves.curves_num` → [blender::bke::CurvesGeometry::curves_num · L1005](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-eabb3f0e5d3c57be)。
- `grease_pencil->layers` → [blender::GreasePencil::layers · L3983](../../../02-BKE几何与数据/intern/grease_pencil.cc.md#f-15d64ed11a2babc0)。
- `layer->frames().size` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L217。
- `layer->frames` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L217。
- `grease_pencil->layers().size` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L220。
- `id_cast<Curves *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `curves_id.geometry.wrap` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L225。

<a id="f-3b77c4dc123e782e"></a>

### `blender::stats_object_edit`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L238—L409。

接口参数：

- `Object *obedit`
- `SceneStats *stats`

**教学注释版**

<!-- annotated:c013b7722ef202 -->

```cpp
static void stats_object_edit(Object *obedit, SceneStats *stats)
{
  if (obedit->type == OB_MESH) {
    const BMesh *bm = BKE_editmesh_bmesh_get(obedit);

    stats->totvert += bm->totvert;
    stats->totvertsel += bm->totvertsel;

    stats->totedge += bm->totedge;
    stats->totedgesel += bm->totedgesel;

    stats->totface += bm->totface;
    stats->totfacesel += bm->totfacesel;

    stats->tottri += poly_to_tri_count(bm->totface, bm->totloop);
  }
  else if (obedit->type == OB_ARMATURE) {
    /* Armature Edit */
    bArmature *arm = id_cast<bArmature *>(obedit->data);

    for (EditBone &ebo : *arm->edbo) {
      stats->totbone++;

      if ((ebo.flag & BONE_CONNECTED) && ebo.parent) {
        stats->totvert--;
      }

      if (ebo.flag & BONE_TIPSEL) {
        stats->totvertsel++;
      }
      if (ebo.flag & BONE_ROOTSEL) {
        stats->totvertsel++;
      }

      if (ebo.flag & BONE_SELECTED) {
        stats->totbonesel++;
      }

      /* if this is a connected child and its parent is being moved, remove our root */
      if ((ebo.flag & BONE_CONNECTED) && (ebo.flag & BONE_ROOTSEL) && ebo.parent &&
          (ebo.parent->flag & BONE_TIPSEL))
      {
        stats->totvertsel--;
      }

      stats->totvert += 2;
    }
  }
  else if (ELEM(obedit->type, OB_CURVES_LEGACY, OB_SURF)) { /* OB_FONT has no cu->editnurb */
    /* Curve Edit */
    Curve *cu = id_cast<Curve *>(obedit->data);
    BezTriple *bezt;
    BPoint *bp;
    int a;
    ListBaseT<Nurb> *nurbs = BKE_curve_editNurbs_get(cu);

    for (Nurb &nu : *nurbs) {
      int selection_count = stats->totpointsel;
      if (nu.type == CU_BEZIER) {
        bezt = nu.bezt;
        a = nu.pntsu;
        while (a--) {
          stats->totpoints += 3;
          if (bezt->f1 & SELECT) {
            stats->totpointsel++;
          }
          if (bezt->f2 & SELECT) {
            stats->totpointsel++;
          }
          if (bezt->f3 & SELECT) {
            stats->totpointsel++;
          }
          bezt++;
        }
        selection_count = (stats->totpointsel - selection_count) == (nu.pntsu * 3);
      }
      else {
        bp = nu.bp;
        a = nu.pntsu * nu.pntsv;
        while (a--) {
          stats->totpoints++;
          if (bp->f1 & SELECT) {
            stats->totpointsel++;
          }
          bp++;
        }
        selection_count = (stats->totpointsel - selection_count) == (nu.pntsu * nu.pntsv);
      }
      stats->totcurves++;
      stats->totcurvesel += selection_count;
    }
  }
  else if (obedit->type == OB_MBALL) {
    /* MetaBall Edit */
    MetaBall *mball = id_cast<MetaBall *>(obedit->data);

    for (MetaElem &ml : *mball->editelems) {
      stats->totvert++;
      if (ml.flag & SELECT) {
        stats->totvertsel++;
      }
    }
  }
  else if (obedit->type == OB_LATTICE) {
    /* Lattice Edit */
    Lattice *lt = id_cast<Lattice *>(obedit->data);
    Lattice *editlatt = lt->editlatt->latt;
    BPoint *bp;
    int a;

    bp = editlatt->def;

    a = editlatt->pntsu * editlatt->pntsv * editlatt->pntsw;
    while (a--) {
      stats->totvert++;
      if (bp->f1 & SELECT) {
        stats->totvertsel++;
      }
      bp++;
    }
  }
  else if (obedit->type == OB_CURVES) {
    const Curves &curves_id = *id_cast<Curves *>(obedit->data);
    const bke::CurvesGeometry &curves = curves_id.geometry.wrap();
    if (const bke::AttributeReader selection = curves.attributes().lookup<bool>(".selection")) {
      const OffsetIndices points_by_curve = curves.points_by_curve();
      struct SelectionCounts {
        int point;
        int curve;
      };
      const SelectionCounts counts = threading::parallel_reduce(
          points_by_curve.index_range(),
          2048,
          SelectionCounts{0, 0},
          [&](const IndexRange range, SelectionCounts value) {
            for (const int curve : range) {
              if (selection.domain == bke::AttrDomain::Point) {
                const int selected_points = array_utils::count_booleans(*selection,
                                                                        points_by_curve[curve]);
                value.point += selected_points;
                value.curve += (selected_points > 0);
              }
              else {
                const bool selected = selection.varray[curve];
                value.point += selected ? points_by_curve[curve].size() : 0;
                value.curve += selected;
              }
            }
            return value;
          },
          [&](const SelectionCounts &a, const SelectionCounts &b) {
            return SelectionCounts{a.point + b.point, a.curve + b.curve};
          });
      stats->totpointsel += counts.point;
      stats->totcurvesel += counts.curve;
    }
    else {
      stats->totpointsel += curves.points_num();
      stats->totcurvesel += curves.curves_num();
    }

    stats->totpoints += curves.points_num();
    stats->totcurves += curves.curves_num();
  }
  else if (obedit->type == OB_POINTCLOUD) {
    PointCloud &pointcloud = *id_cast<PointCloud *>(obedit->data);
    const VArray<bool> selection = *pointcloud.attributes().lookup_or_default<bool>(
        ".selection", bke::AttrDomain::Point, true);
    stats->totvertsel = array_utils::count_booleans(selection);
    stats->totpoints = pointcloud.totpoint;
  }
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L238—L409</summary>

<!-- original:c013b7722ef202:source/blender/editors/space_info/info_stats.cc:238:409 -->

```cpp
static void stats_object_edit(Object *obedit, SceneStats *stats)
{
  if (obedit->type == OB_MESH) {
    const BMesh *bm = BKE_editmesh_bmesh_get(obedit);

    stats->totvert += bm->totvert;
    stats->totvertsel += bm->totvertsel;

    stats->totedge += bm->totedge;
    stats->totedgesel += bm->totedgesel;

    stats->totface += bm->totface;
    stats->totfacesel += bm->totfacesel;

    stats->tottri += poly_to_tri_count(bm->totface, bm->totloop);
  }
  else if (obedit->type == OB_ARMATURE) {
    /* Armature Edit */
    bArmature *arm = id_cast<bArmature *>(obedit->data);

    for (EditBone &ebo : *arm->edbo) {
      stats->totbone++;

      if ((ebo.flag & BONE_CONNECTED) && ebo.parent) {
        stats->totvert--;
      }

      if (ebo.flag & BONE_TIPSEL) {
        stats->totvertsel++;
      }
      if (ebo.flag & BONE_ROOTSEL) {
        stats->totvertsel++;
      }

      if (ebo.flag & BONE_SELECTED) {
        stats->totbonesel++;
      }

      /* if this is a connected child and its parent is being moved, remove our root */
      if ((ebo.flag & BONE_CONNECTED) && (ebo.flag & BONE_ROOTSEL) && ebo.parent &&
          (ebo.parent->flag & BONE_TIPSEL))
      {
        stats->totvertsel--;
      }

      stats->totvert += 2;
    }
  }
  else if (ELEM(obedit->type, OB_CURVES_LEGACY, OB_SURF)) { /* OB_FONT has no cu->editnurb */
    /* Curve Edit */
    Curve *cu = id_cast<Curve *>(obedit->data);
    BezTriple *bezt;
    BPoint *bp;
    int a;
    ListBaseT<Nurb> *nurbs = BKE_curve_editNurbs_get(cu);

    for (Nurb &nu : *nurbs) {
      int selection_count = stats->totpointsel;
      if (nu.type == CU_BEZIER) {
        bezt = nu.bezt;
        a = nu.pntsu;
        while (a--) {
          stats->totpoints += 3;
          if (bezt->f1 & SELECT) {
            stats->totpointsel++;
          }
          if (bezt->f2 & SELECT) {
            stats->totpointsel++;
          }
          if (bezt->f3 & SELECT) {
            stats->totpointsel++;
          }
          bezt++;
        }
        selection_count = (stats->totpointsel - selection_count) == (nu.pntsu * 3);
      }
      else {
        bp = nu.bp;
        a = nu.pntsu * nu.pntsv;
        while (a--) {
          stats->totpoints++;
          if (bp->f1 & SELECT) {
            stats->totpointsel++;
          }
          bp++;
        }
        selection_count = (stats->totpointsel - selection_count) == (nu.pntsu * nu.pntsv);
      }
      stats->totcurves++;
      stats->totcurvesel += selection_count;
    }
  }
  else if (obedit->type == OB_MBALL) {
    /* MetaBall Edit */
    MetaBall *mball = id_cast<MetaBall *>(obedit->data);

    for (MetaElem &ml : *mball->editelems) {
      stats->totvert++;
      if (ml.flag & SELECT) {
        stats->totvertsel++;
      }
    }
  }
  else if (obedit->type == OB_LATTICE) {
    /* Lattice Edit */
    Lattice *lt = id_cast<Lattice *>(obedit->data);
    Lattice *editlatt = lt->editlatt->latt;
    BPoint *bp;
    int a;

    bp = editlatt->def;

    a = editlatt->pntsu * editlatt->pntsv * editlatt->pntsw;
    while (a--) {
      stats->totvert++;
      if (bp->f1 & SELECT) {
        stats->totvertsel++;
      }
      bp++;
    }
  }
  else if (obedit->type == OB_CURVES) {
    const Curves &curves_id = *id_cast<Curves *>(obedit->data);
    const bke::CurvesGeometry &curves = curves_id.geometry.wrap();
    if (const bke::AttributeReader selection = curves.attributes().lookup<bool>(".selection")) {
      const OffsetIndices points_by_curve = curves.points_by_curve();
      struct SelectionCounts {
        int point;
        int curve;
      };
      const SelectionCounts counts = threading::parallel_reduce(
          points_by_curve.index_range(),
          2048,
          SelectionCounts{0, 0},
          [&](const IndexRange range, SelectionCounts value) {
            for (const int curve : range) {
              if (selection.domain == bke::AttrDomain::Point) {
                const int selected_points = array_utils::count_booleans(*selection,
                                                                        points_by_curve[curve]);
                value.point += selected_points;
                value.curve += (selected_points > 0);
              }
              else {
                const bool selected = selection.varray[curve];
                value.point += selected ? points_by_curve[curve].size() : 0;
                value.curve += selected;
              }
            }
            return value;
          },
          [&](const SelectionCounts &a, const SelectionCounts &b) {
            return SelectionCounts{a.point + b.point, a.curve + b.curve};
          });
      stats->totpointsel += counts.point;
      stats->totcurvesel += counts.curve;
    }
    else {
      stats->totpointsel += curves.points_num();
      stats->totcurvesel += curves.curves_num();
    }

    stats->totpoints += curves.points_num();
    stats->totcurves += curves.curves_num();
  }
  else if (obedit->type == OB_POINTCLOUD) {
    PointCloud &pointcloud = *id_cast<PointCloud *>(obedit->data);
    const VArray<bool> selection = *pointcloud.attributes().lookup_or_default<bool>(
        ".selection", bke::AttrDomain::Point, true);
    stats->totvertsel = array_utils::count_booleans(selection);
    stats->totpoints = pointcloud.totpoint;
  }
}
```

</details>

**沿实际写入检查状态**

- `stats->totvert += bm->totvert;`
- `stats->totvertsel += bm->totvertsel;`
- `stats->totedge += bm->totedge;`
- `stats->totedgesel += bm->totedgesel;`
- `stats->totface += bm->totface;`
- `stats->totfacesel += bm->totfacesel;`
- `stats->tottri += poly_to_tri_count(bm->totface, bm->totloop);`
- `stats->totvert += 2;`
- `bezt = nu.bezt;`
- `a = nu.pntsu;`
- `stats->totpoints += 3;`
- `selection_count = (stats->totpointsel - selection_count) == (nu.pntsu * 3);`
- `bp = nu.bp;`
- `a = nu.pntsu * nu.pntsv;`
- `selection_count = (stats->totpointsel - selection_count) == (nu.pntsu * nu.pntsv);`
- `stats->totcurvesel += selection_count;`
- `bp = editlatt->def;`
- `a = editlatt->pntsu * editlatt->pntsv * editlatt->pntsw;`
- `value.point += selected_points;`
- `value.curve += (selected_points > 0);`
- `value.point += selected ? points_by_curve[curve].size() : 0;`
- `value.curve += selected;`
- `stats->totpointsel += counts.point;`
- `stats->totcurvesel += counts.curve;`
- `stats->totpointsel += curves.points_num();`
- `stats->totcurvesel += curves.curves_num();`
- `stats->totpoints += curves.points_num();`
- `stats->totcurves += curves.curves_num();`
- `stats->totvertsel = array_utils::count_booleans(selection);`
- `stats->totpoints = pointcloud.totpoint;`

**结果出口**

- `return value;`
- `return SelectionCounts{a.point + b.point, a.curve + b.curve};`

**继续追踪实现**

- `BKE_editmesh_bmesh_get` → [blender::BKE_editmesh_bmesh_get · L65](../../../02-BKE几何与数据/intern/editmesh.cc.md#f-2afdd2773d3f0d88)；[blender::BKE_editmesh_bmesh_get · L71](../../../02-BKE几何与数据/intern/editmesh.cc.md#f-80631d704a7e9947)。同名重载需按实参类型选择。
- `poly_to_tri_count` → [blender::poly_to_tri_count · L118](../../../01-BLI基础库/intern/math_geom_inline.cc.md#f-fd5a0e76d62e3b0b)。
- `id_cast<bArmature *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `ELEM` → [ELEM · L88](../../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-d28724a15928)；[ELEM · L135](../../../01-BLI基础库/BLI_utildefines.hh.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `id_cast<Curve *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `BKE_curve_editNurbs_get` → [blender::BKE_curve_editNurbs_get · L441](../../../02-BKE几何与数据/intern/curve.cc.md#f-6e9579f439d8d1b1)。
- `id_cast<MetaBall *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `id_cast<Lattice *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `id_cast<Curves *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `curves_id.geometry.wrap` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L361。
- `curves.attributes().lookup<bool>` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L362。
- `curves.attributes` → [blender::bke::CurvesGeometry::attributes · L1908](../../../02-BKE几何与数据/intern/curves_geometry.cc.md#f-8e24fbf758862a22)。
- `curves.points_by_curve` → [blender::bke::CurvesGeometry::points_by_curve · L1058](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-a0416697e10ec205)。
- `threading::parallel_reduce` → [blender::threading::parallel_reduce · L126](../../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-9225ddb5efb97fcc)。
- `points_by_curve.index_range` → [blender::offset_indices::OffsetIndices::index_range · L77](../../../../05-几何存储与拓扑映射/02-OffsetIndices完整接口.md#f-19b5ca1456de007d)。
- `array_utils::count_booleans` → [blender::array_utils::count_booleans · L345](../../../01-BLI基础库/intern/array_utils.cc.md#f-1640c4115bd9bbf5)；[blender::array_utils::count_booleans · L477](../../../01-BLI基础库/intern/array_utils.cc.md#f-25e7ff6bc3c5eedf)。同名重载需按实参类型选择。
- `points_by_curve[curve].size` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L382。
- `curves.points_num` → [blender::bke::CurvesGeometry::points_num · L1001](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-049421b1f643c700)。
- `curves.curves_num` → [blender::bke::CurvesGeometry::curves_num · L1005](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-eabb3f0e5d3c57be)。
- `id_cast<PointCloud *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `pointcloud.attributes().lookup_or_default<bool>` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L404。
- `pointcloud.attributes` → [blender::PointCloud::attributes · L307](../../../02-BKE几何与数据/intern/pointcloud.cc.md#f-bf2e5928a63a6e15)。

<a id="f-b9dee896158f5de7"></a>

### `blender::stats_object_pose`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L411—L425。

接口参数：

- `const Object *ob`
- `SceneStats *stats`

**教学注释版**

<!-- annotated:dfae592acc5bbc -->

```cpp
static void stats_object_pose(const Object *ob, SceneStats *stats)
{
  if (ob->pose) {
    bArmature *arm = id_cast<bArmature *>(ob->data);

    for (bPoseChannel &pchan : ob->pose->chanbase) {
      stats->totbone++;
      if ((pchan.flag & POSE_SELECTED)) {
        if (BKE_pose_is_bonecoll_visible(arm, &pchan)) {
          stats->totbonesel++;
        }
      }
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L411—L425</summary>

<!-- original:dfae592acc5bbc:source/blender/editors/space_info/info_stats.cc:411:425 -->

```cpp
static void stats_object_pose(const Object *ob, SceneStats *stats)
{
  if (ob->pose) {
    bArmature *arm = id_cast<bArmature *>(ob->data);

    for (bPoseChannel &pchan : ob->pose->chanbase) {
      stats->totbone++;
      if ((pchan.flag & POSE_SELECTED)) {
        if (BKE_pose_is_bonecoll_visible(arm, &pchan)) {
          stats->totbonesel++;
        }
      }
    }
  }
}
```

</details>

**继续追踪实现**

- `id_cast<bArmature *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `BKE_pose_is_bonecoll_visible` → [blender::BKE_pose_is_bonecoll_visible · L981](../../../02-BKE几何与数据/intern/action.cc.md#f-8e96971f63db2ead)。

<a id="f-69d1d979a6347dc0"></a>

### `blender::stats_is_object_dynamic_topology_sculpt`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L427—L431。

接口参数：

- `const Object *ob`

**教学注释版**

<!-- annotated:e6d3066fca813b -->

```cpp
static bool stats_is_object_dynamic_topology_sculpt(const Object *ob)
{
  return (ob->mode == OB_MODE_SCULPT && ob->runtime->sculpt_session &&
          ob->runtime->sculpt_session->bm);
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L427—L431</summary>

<!-- original:e6d3066fca813b:source/blender/editors/space_info/info_stats.cc:427:431 -->

```cpp
static bool stats_is_object_dynamic_topology_sculpt(const Object *ob)
{
  return (ob->mode == OB_MODE_SCULPT && ob->runtime->sculpt_session &&
          ob->runtime->sculpt_session->bm);
}
```

</details>

**结果出口**

- `return (ob->mode == OB_MODE_SCULPT && ob->runtime->sculpt_session &&`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-7ace60727623ec65"></a>

### `blender::stats_object_mesh_paint`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L433—L457。

接口参数：

- `const Object *ob`
- `SceneStats *stats`

**教学注释版**

<!-- annotated:17bab9b8b789d1 -->

```cpp
static void stats_object_mesh_paint(const Object *ob, SceneStats *stats)
{
  const SculptSession *ss = ob->runtime->sculpt_session;
  const bke::pbvh::Tree *pbvh = bke::object::pbvh_get(*ob);
  if (ss == nullptr || pbvh == nullptr) {
    return;
  }

  switch (pbvh->type()) {
    case bke::pbvh::Type::Mesh: {
      const Mesh &mesh = *id_cast<const Mesh *>(ob->data);
      stats->totvertactive = mesh.verts_num;
      stats->totfaceactive = mesh.faces_num;
      break;
    }
    case bke::pbvh::Type::BMesh:
      stats->totvertactive = ob->runtime->sculpt_session->bm->totvert;
      stats->tottriactive = ob->runtime->sculpt_session->bm->totface;
      break;
    case bke::pbvh::Type::Grids:
      stats->totvertactive = BKE_sculpt_get_grid_num_verts(*ob);
      stats->totfaceactive = BKE_sculpt_get_grid_num_faces(*ob);
      break;
  }
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L433—L457</summary>

<!-- original:17bab9b8b789d1:source/blender/editors/space_info/info_stats.cc:433:457 -->

```cpp
static void stats_object_mesh_paint(const Object *ob, SceneStats *stats)
{
  const SculptSession *ss = ob->runtime->sculpt_session;
  const bke::pbvh::Tree *pbvh = bke::object::pbvh_get(*ob);
  if (ss == nullptr || pbvh == nullptr) {
    return;
  }

  switch (pbvh->type()) {
    case bke::pbvh::Type::Mesh: {
      const Mesh &mesh = *id_cast<const Mesh *>(ob->data);
      stats->totvertactive = mesh.verts_num;
      stats->totfaceactive = mesh.faces_num;
      break;
    }
    case bke::pbvh::Type::BMesh:
      stats->totvertactive = ob->runtime->sculpt_session->bm->totvert;
      stats->tottriactive = ob->runtime->sculpt_session->bm->totface;
      break;
    case bke::pbvh::Type::Grids:
      stats->totvertactive = BKE_sculpt_get_grid_num_verts(*ob);
      stats->totfaceactive = BKE_sculpt_get_grid_num_faces(*ob);
      break;
  }
}
```

</details>

**沿实际写入检查状态**

- `stats->totvertactive = mesh.verts_num;`
- `stats->totfaceactive = mesh.faces_num;`
- `stats->totvertactive = ob->runtime->sculpt_session->bm->totvert;`
- `stats->tottriactive = ob->runtime->sculpt_session->bm->totface;`
- `stats->totvertactive = BKE_sculpt_get_grid_num_verts(*ob);`
- `stats->totfaceactive = BKE_sculpt_get_grid_num_faces(*ob);`

**继续追踪实现**

- `bke::object::pbvh_get` → [blender::bke::object::pbvh_get · L2727](../../../02-BKE几何与数据/intern/paint.cc.md#f-39f0e75a118b3d6a)；[blender::bke::object::pbvh_get · L2735](../../../02-BKE几何与数据/intern/paint.cc.md#f-bf5e56d6c516443a)。同名重载需按实参类型选择。
- `pbvh->type` → [blender::bke::pbvh::Tree::type · L673](../../../02-BKE几何与数据/BKE_paint_bvh.hh.md#f-137ce3483b4da62c)。
- `id_cast<const Mesh *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `BKE_sculpt_get_grid_num_verts` → [blender::BKE_sculpt_get_grid_num_verts · L2299](../../../02-BKE几何与数据/intern/paint.cc.md#f-f6b84eb6497ffe26)。
- `BKE_sculpt_get_grid_num_faces` → [blender::BKE_sculpt_get_grid_num_faces · L2307](../../../02-BKE几何与数据/intern/paint.cc.md#f-bb573aae2c547ae0)。

<a id="f-f249dee1437dba1b"></a>

### `blender::stats_update`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L460—L531。

接口参数：

- `const Main *bmain`
- `Depsgraph *depsgraph`
- `const Scene *scene`
- `ViewLayer *view_layer`
- `View3D *v3d_local`
- `SceneStats *stats`

**教学注释版**

<!-- annotated:5030acf2d7e050 -->

```cpp
static void stats_update(const Main *bmain,
                         Depsgraph *depsgraph,
                         const Scene *scene,
                         ViewLayer *view_layer,
                         View3D *v3d_local,
                         SceneStats *stats)
{
  BKE_view_layer_synced_ensure(*bmain, scene, view_layer);
  const Object *ob = BKE_view_layer_active_object_get(view_layer);
  const Object *obedit = BKE_view_layer_edit_object_get(view_layer);

  // [讲解] memset：填充字节，不调用T构造函数，也不保证任意类型的全零表示是合法或期望值。
  memset(stats, 0x0, sizeof(*stats));

  if (obedit && (ob->type != OB_GREASE_PENCIL)) {
    /* Edit Mode. */
    FOREACH_OBJECT_BEGIN (bmain, scene, view_layer, ob_iter) {
      if (ob_iter->base_flag & BASE_ENABLED_AND_VISIBLE_IN_DEFAULT_VIEWPORT) {
        if (ob_iter->mode & OB_MODE_EDIT) {
          stats_object_edit(ob_iter, stats);
          stats->totobjsel++;
        }
        else {
          /* Skip hidden objects in local view that are not in edit-mode,
           * an exception for edit-mode, in most other modes these would be considered hidden. */
          if (v3d_local && !BKE_object_is_visible_in_viewport(v3d_local, ob_iter)) {
            continue;
          }
        }
        stats->totobj++;
      }
    }
    FOREACH_OBJECT_END;
  }
  else if (ob && (ob->mode & OB_MODE_POSE)) {
    /* Pose Mode. */
    FOREACH_OBJECT_BEGIN (bmain, scene, view_layer, ob_iter) {
      if (ob_iter->base_flag & BASE_ENABLED_AND_VISIBLE_IN_DEFAULT_VIEWPORT) {
        if (ob_iter->mode & OB_MODE_POSE) {
          stats_object_pose(ob_iter, stats);
          stats->totobjsel++;
        }
        else {
          /* See comment for edit-mode. */
          if (v3d_local && !BKE_object_is_visible_in_viewport(v3d_local, ob_iter)) {
            continue;
          }
        }
        stats->totobj++;
      }
    }
    FOREACH_OBJECT_END;
  }
  else if (ob && BKE_object_use_sculptsession(ob->mode)) {
    stats_object_mesh_paint(ob, stats);
  }
  else if (ob && ob->mode == OB_MODE_SCULPT_CURVES) {
    const Curves &curves_id = *id_cast<Curves *>(ob->data);
    const bke::CurvesGeometry &curves = curves_id.geometry.wrap();
    stats->totvertactive += curves.points_num();
  }
  else {
    /* Objects. */
    Set<const Mesh *> objects_gset;
    DEGObjectIterSettings deg_iter_settings{};
    deg_iter_settings.depsgraph = depsgraph;
    deg_iter_settings.flags = DEG_OBJECT_ITER_FOR_RENDER_ENGINE_FLAGS;
    DEG_OBJECT_ITER_BEGIN (&deg_iter_settings, ob_iter) {
      stats_object(ob_iter, v3d_local, stats, objects_gset);
    }
    DEG_OBJECT_ITER_END;
  }
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L460—L531</summary>

<!-- original:5030acf2d7e050:source/blender/editors/space_info/info_stats.cc:460:531 -->

```cpp
static void stats_update(const Main *bmain,
                         Depsgraph *depsgraph,
                         const Scene *scene,
                         ViewLayer *view_layer,
                         View3D *v3d_local,
                         SceneStats *stats)
{
  BKE_view_layer_synced_ensure(*bmain, scene, view_layer);
  const Object *ob = BKE_view_layer_active_object_get(view_layer);
  const Object *obedit = BKE_view_layer_edit_object_get(view_layer);

  memset(stats, 0x0, sizeof(*stats));

  if (obedit && (ob->type != OB_GREASE_PENCIL)) {
    /* Edit Mode. */
    FOREACH_OBJECT_BEGIN (bmain, scene, view_layer, ob_iter) {
      if (ob_iter->base_flag & BASE_ENABLED_AND_VISIBLE_IN_DEFAULT_VIEWPORT) {
        if (ob_iter->mode & OB_MODE_EDIT) {
          stats_object_edit(ob_iter, stats);
          stats->totobjsel++;
        }
        else {
          /* Skip hidden objects in local view that are not in edit-mode,
           * an exception for edit-mode, in most other modes these would be considered hidden. */
          if (v3d_local && !BKE_object_is_visible_in_viewport(v3d_local, ob_iter)) {
            continue;
          }
        }
        stats->totobj++;
      }
    }
    FOREACH_OBJECT_END;
  }
  else if (ob && (ob->mode & OB_MODE_POSE)) {
    /* Pose Mode. */
    FOREACH_OBJECT_BEGIN (bmain, scene, view_layer, ob_iter) {
      if (ob_iter->base_flag & BASE_ENABLED_AND_VISIBLE_IN_DEFAULT_VIEWPORT) {
        if (ob_iter->mode & OB_MODE_POSE) {
          stats_object_pose(ob_iter, stats);
          stats->totobjsel++;
        }
        else {
          /* See comment for edit-mode. */
          if (v3d_local && !BKE_object_is_visible_in_viewport(v3d_local, ob_iter)) {
            continue;
          }
        }
        stats->totobj++;
      }
    }
    FOREACH_OBJECT_END;
  }
  else if (ob && BKE_object_use_sculptsession(ob->mode)) {
    stats_object_mesh_paint(ob, stats);
  }
  else if (ob && ob->mode == OB_MODE_SCULPT_CURVES) {
    const Curves &curves_id = *id_cast<Curves *>(ob->data);
    const bke::CurvesGeometry &curves = curves_id.geometry.wrap();
    stats->totvertactive += curves.points_num();
  }
  else {
    /* Objects. */
    Set<const Mesh *> objects_gset;
    DEGObjectIterSettings deg_iter_settings{};
    deg_iter_settings.depsgraph = depsgraph;
    deg_iter_settings.flags = DEG_OBJECT_ITER_FOR_RENDER_ENGINE_FLAGS;
    DEG_OBJECT_ITER_BEGIN (&deg_iter_settings, ob_iter) {
      stats_object(ob_iter, v3d_local, stats, objects_gset);
    }
    DEG_OBJECT_ITER_END;
  }
}
```

</details>

**沿实际写入检查状态**

- `stats->totvertactive += curves.points_num();`
- `deg_iter_settings.depsgraph = depsgraph;`
- `deg_iter_settings.flags = DEG_OBJECT_ITER_FOR_RENDER_ENGINE_FLAGS;`

**继续追踪实现**

- `BKE_view_layer_synced_ensure` → [blender::BKE_view_layer_synced_ensure · L1035](../../../02-BKE几何与数据/intern/layer.cc.md#f-602c088654ebcb63)。
- `BKE_view_layer_active_object_get` → [blender::BKE_view_layer_active_object_get · L286](../../../02-BKE几何与数据/intern/layer_utils.cc.md#f-aa39df7416329726)。
- `BKE_view_layer_edit_object_get` → [blender::BKE_view_layer_edit_object_get · L292](../../../02-BKE几何与数据/intern/layer_utils.cc.md#f-c8613cfff236cca1)。
- `memset` → [外部契约](https://eel.is/c++draft/cstring.syn)：填充字节，不调用T构造函数，也不保证任意类型的全零表示是合法或期望值。
- `stats_object_edit` → [blender::stats_object_edit · L238](info_stats.cc.md#f-3b77c4dc123e782e)。
- `BKE_object_is_visible_in_viewport` → [blender::BKE_object_is_visible_in_viewport · L1702](../../../02-BKE几何与数据/intern/layer.cc.md#f-6be42a129fa5e016)。
- `stats_object_pose` → [blender::stats_object_pose · L411](info_stats.cc.md#f-b9dee896158f5de7)。
- `BKE_object_use_sculptsession` → [blender::BKE_object_use_sculptsession · L4328](../../../02-BKE几何与数据/intern/object.cc.md#f-295e9e178b4df6bc)。
- `stats_object_mesh_paint` → [blender::stats_object_mesh_paint · L433](info_stats.cc.md#f-7ace60727623ec65)。
- `id_cast<Curves *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `curves_id.geometry.wrap` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L517。
- `curves.points_num` → [blender::bke::CurvesGeometry::points_num · L1001](../../../../05-几何存储与拓扑映射/04-CurvesGeometry存储.md#f-049421b1f643c700)。
- `DEG_OBJECT_ITER_BEGIN` → [DEG_OBJECT_ITER_BEGIN · L301](../../../06-Depsgraph依赖图/DEG_depsgraph_query.hh.md#m-b026ee27aef3)。宏定义由构建条件选择。
- `stats_object` → [blender::stats_object · L164](info_stats.cc.md#f-24e070947cf1b34a)。

<a id="f-51dcb7b269284f05"></a>

### `blender::format_stats`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L559—L615。

接口参数：

- `Main *bmain`
- `Scene *scene`
- `ViewLayer *view_layer`
- `View3D *v3d_local`
- `SceneStatsFmt *stats_fmt`

**教学注释版**

<!-- annotated:6c7c0ed442d8c1 -->

```cpp
static bool format_stats(
    Main *bmain, Scene *scene, ViewLayer *view_layer, View3D *v3d_local, SceneStatsFmt *stats_fmt)
{
  /* Create stats if they don't already exist. */
  SceneStats **stats_p = (v3d_local) ? &v3d_local->runtime.local_stats : &view_layer->stats;
  if (*stats_p == nullptr) {
    /* Don't access dependency graph if interface is marked as locked. */
    wmWindowManager *wm = bmain->wm.first();
    if (wm->runtime->is_interface_locked) {
      return false;
    }
    Depsgraph *depsgraph = BKE_scene_ensure_depsgraph(bmain, scene, view_layer);
    *stats_p = MEM_new_uninitialized<SceneStats>(__func__);
    stats_update(bmain, depsgraph, scene, view_layer, v3d_local, *stats_p);
  }

  SceneStats *stats = *stats_p;

  /* Generate formatted numbers. */
#define SCENE_STATS_FMT_INT(_id) BLI_str_format_uint64_grouped(stats_fmt->_id, stats->_id)

  SCENE_STATS_FMT_INT(totvert);
  SCENE_STATS_FMT_INT(totvertsel);
  SCENE_STATS_FMT_INT(totvertactive);

  SCENE_STATS_FMT_INT(totedge);
  SCENE_STATS_FMT_INT(totedgesel);

  SCENE_STATS_FMT_INT(totface);
  SCENE_STATS_FMT_INT(totfacesel);
  SCENE_STATS_FMT_INT(totfaceactive);

  SCENE_STATS_FMT_INT(totbone);
  SCENE_STATS_FMT_INT(totbonesel);

  SCENE_STATS_FMT_INT(totobj);
  SCENE_STATS_FMT_INT(totobjsel);

  SCENE_STATS_FMT_INT(totlamp);
  SCENE_STATS_FMT_INT(totlampsel);

  SCENE_STATS_FMT_INT(tottri);
  SCENE_STATS_FMT_INT(tottrisel);
  SCENE_STATS_FMT_INT(tottriactive);

  SCENE_STATS_FMT_INT(totgplayer);
  SCENE_STATS_FMT_INT(totgpframe);
  SCENE_STATS_FMT_INT(totgpstroke);

  SCENE_STATS_FMT_INT(totpoints);
  SCENE_STATS_FMT_INT(totpointsel);
  SCENE_STATS_FMT_INT(totcurves);
  SCENE_STATS_FMT_INT(totcurvesel);

#undef SCENE_STATS_FMT_INT
  return true;
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L559—L615</summary>

<!-- original:6c7c0ed442d8c1:source/blender/editors/space_info/info_stats.cc:559:615 -->

```cpp
static bool format_stats(
    Main *bmain, Scene *scene, ViewLayer *view_layer, View3D *v3d_local, SceneStatsFmt *stats_fmt)
{
  /* Create stats if they don't already exist. */
  SceneStats **stats_p = (v3d_local) ? &v3d_local->runtime.local_stats : &view_layer->stats;
  if (*stats_p == nullptr) {
    /* Don't access dependency graph if interface is marked as locked. */
    wmWindowManager *wm = bmain->wm.first();
    if (wm->runtime->is_interface_locked) {
      return false;
    }
    Depsgraph *depsgraph = BKE_scene_ensure_depsgraph(bmain, scene, view_layer);
    *stats_p = MEM_new_uninitialized<SceneStats>(__func__);
    stats_update(bmain, depsgraph, scene, view_layer, v3d_local, *stats_p);
  }

  SceneStats *stats = *stats_p;

  /* Generate formatted numbers. */
#define SCENE_STATS_FMT_INT(_id) BLI_str_format_uint64_grouped(stats_fmt->_id, stats->_id)

  SCENE_STATS_FMT_INT(totvert);
  SCENE_STATS_FMT_INT(totvertsel);
  SCENE_STATS_FMT_INT(totvertactive);

  SCENE_STATS_FMT_INT(totedge);
  SCENE_STATS_FMT_INT(totedgesel);

  SCENE_STATS_FMT_INT(totface);
  SCENE_STATS_FMT_INT(totfacesel);
  SCENE_STATS_FMT_INT(totfaceactive);

  SCENE_STATS_FMT_INT(totbone);
  SCENE_STATS_FMT_INT(totbonesel);

  SCENE_STATS_FMT_INT(totobj);
  SCENE_STATS_FMT_INT(totobjsel);

  SCENE_STATS_FMT_INT(totlamp);
  SCENE_STATS_FMT_INT(totlampsel);

  SCENE_STATS_FMT_INT(tottri);
  SCENE_STATS_FMT_INT(tottrisel);
  SCENE_STATS_FMT_INT(tottriactive);

  SCENE_STATS_FMT_INT(totgplayer);
  SCENE_STATS_FMT_INT(totgpframe);
  SCENE_STATS_FMT_INT(totgpstroke);

  SCENE_STATS_FMT_INT(totpoints);
  SCENE_STATS_FMT_INT(totpointsel);
  SCENE_STATS_FMT_INT(totcurves);
  SCENE_STATS_FMT_INT(totcurvesel);

#undef SCENE_STATS_FMT_INT
  return true;
}
```

</details>

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `bmain->wm.first` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L566。
- `BKE_scene_ensure_depsgraph` → [blender::BKE_scene_ensure_depsgraph · L3654](../../../02-BKE几何与数据/intern/scene.cc.md#f-eb26d00ccbfb6c0a)。
- `MEM_new_uninitialized<SceneStats>` → [MEM_new_uninitialized · L590](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-c773b2e5b8fe70e4)；[MEM_new_uninitialized · L124](../../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-28a7e00a1e67f699)。同名重载需按实参类型选择。
- `stats_update` → [blender::stats_update · L460](info_stats.cc.md#f-f249dee1437dba1b)。
- `SCENE_STATS_FMT_INT` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L580。

<a id="f-2ba7a04d756ba5ef"></a>

### `blender::stats_row`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L853—L866。

接口参数：

- `int col1`
- `const char *key`
- `int col2`
- `const char *value1`
- `const char *value2`
- `int *y`
- `int height`

**教学注释版**

<!-- annotated:030778e5d0dda9 -->

```cpp
static void stats_row(int col1,
                      const char *key,
                      int col2,
                      const char *value1,
                      const char *value2,
                      int *y,
                      int height)
{
  *y -= height;
  BLF_draw_default(col1, *y, 0.0f, key, 128);
  char values[128];
  SNPRINTF_UTF8(values, (value2) ? "%s / %s" : "%s", value1, value2);
  BLF_draw_default(col2, *y, 0.0f, values, sizeof(values));
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L853—L866</summary>

<!-- original:030778e5d0dda9:source/blender/editors/space_info/info_stats.cc:853:866 -->

```cpp
static void stats_row(int col1,
                      const char *key,
                      int col2,
                      const char *value1,
                      const char *value2,
                      int *y,
                      int height)
{
  *y -= height;
  BLF_draw_default(col1, *y, 0.0f, key, 128);
  char values[128];
  SNPRINTF_UTF8(values, (value2) ? "%s / %s" : "%s", value1, value2);
  BLF_draw_default(col2, *y, 0.0f, values, sizeof(values));
}
```

</details>

**继续追踪实现**

- `BLF_draw_default` → [blender::BLF_draw_default · L54](../../blenfont/intern/blf_default.cc.md#f-81cd8e5978455a73)。
- `SNPRINTF_UTF8` → [SNPRINTF_UTF8 · L340](../../../01-BLI基础库/BLI_string_utf8.hh.md#m-5e57d7a30c64)。宏定义由构建条件选择。

<a id="f-686d31a24af941f5"></a>

### `blender::ED_info_draw_stats`

实现位置：[source/blender/editors/space_info/info_stats.cc](../../../../../../../../source/blender/editors/space_info/info_stats.cc) · L868—L1001。

接口参数：

- `Main *bmain`
- `Scene *scene`
- `ViewLayer *view_layer`
- `View3D *v3d_local`
- `int x`
- `int *y`
- `int height`

**教学注释版**

<!-- annotated:55d088b2641ff0 -->

```cpp
void ED_info_draw_stats(
    Main *bmain, Scene *scene, ViewLayer *view_layer, View3D *v3d_local, int x, int *y, int height)
{
  BLI_assert(v3d_local == nullptr || v3d_local->localvd != nullptr);
  SceneStatsFmt stats_fmt;
  if (!format_stats(bmain, scene, view_layer, v3d_local, &stats_fmt)) {
    return;
  }

  BKE_view_layer_synced_ensure(*bmain, scene, view_layer);
  Object *ob = BKE_view_layer_active_object_get(view_layer);
  eObjectMode object_mode = ob ? ob->mode : OB_MODE_OBJECT;
  const int font_id = BLF_default();

  /* Translated labels for each stat row. */
  enum {
    OBJ,
    VERTS,
    EDGES,
    FACES,
    TRIS,
    JOINTS,
    BONES,
    LAYERS,
    FRAMES,
    STROKES,
    POINTS,
    LIGHTS,
    CURVES,
    MAX_LABELS_COUNT
  };
  char labels[MAX_LABELS_COUNT][64];

  STRNCPY_UTF8(labels[OBJ], IFACE_("Objects"));
  STRNCPY_UTF8(labels[VERTS], IFACE_("Vertices"));
  STRNCPY_UTF8(labels[EDGES], IFACE_("Edges"));
  STRNCPY_UTF8(labels[FACES], IFACE_("Faces"));
  STRNCPY_UTF8(labels[TRIS], IFACE_("Triangles"));
  STRNCPY_UTF8(labels[JOINTS], IFACE_("Joints"));
  STRNCPY_UTF8(labels[BONES], IFACE_("Bones"));
  STRNCPY_UTF8(labels[LAYERS], IFACE_("Layers"));
  STRNCPY_UTF8(labels[FRAMES], IFACE_("Frames"));
  STRNCPY_UTF8(labels[STROKES], IFACE_("Strokes"));
  STRNCPY_UTF8(labels[POINTS], IFACE_("Points"));
  STRNCPY_UTF8(labels[LIGHTS], IFACE_("Lights"));
  STRNCPY_UTF8(labels[CURVES], IFACE_("Curves"));

  int longest_label = 0;
  for (int i = 0; i < MAX_LABELS_COUNT; ++i) {
    longest_label = max_ii(longest_label, BLF_width(font_id, labels[i], sizeof(labels[i])));
  }

  int col1 = x;
  int col2 = x + longest_label + (0.5f * U.widget_unit);

  /* Add some extra margin above this section. */
  *y -= (0.6f * height);

  bool any_objects = !STREQ(&stats_fmt.totobj[0], "0");
  bool any_selected = !STREQ(&stats_fmt.totobjsel[0], "0");

  if (any_selected) {
    stats_row(col1, labels[OBJ], col2, stats_fmt.totobjsel, stats_fmt.totobj, y, height);
  }
  else if (any_objects) {
    stats_row(col1, labels[OBJ], col2, stats_fmt.totobj, nullptr, y, height);
    /* Show scene totals if nothing is selected. */
    stats_row(col1, labels[VERTS], col2, stats_fmt.totvert, nullptr, y, height);
    stats_row(col1, labels[EDGES], col2, stats_fmt.totedge, nullptr, y, height);
    stats_row(col1, labels[FACES], col2, stats_fmt.totface, nullptr, y, height);
    stats_row(col1, labels[TRIS], col2, stats_fmt.tottri, nullptr, y, height);
    return;
  }
  else if (object_mode != OB_MODE_SCULPT_CURVES && !BKE_object_use_sculptsession(object_mode)) {
    /* No objects in scene. */
    stats_row(col1, labels[OBJ], col2, stats_fmt.totobj, nullptr, y, height);
    return;
  }

  if ((ob) && ob->type == OB_GREASE_PENCIL) {
    stats_row(col1, labels[LAYERS], col2, stats_fmt.totgplayer, nullptr, y, height);
    stats_row(col1, labels[FRAMES], col2, stats_fmt.totgpframe, nullptr, y, height);
    stats_row(col1, labels[STROKES], col2, stats_fmt.totgpstroke, nullptr, y, height);
    stats_row(col1, labels[POINTS], col2, stats_fmt.totpoints, nullptr, y, height);
  }
  else if (ob && ob->mode == OB_MODE_EDIT) {
    if (ob->type == OB_MESH) {
      stats_row(col1, labels[VERTS], col2, stats_fmt.totvertsel, stats_fmt.totvert, y, height);
      stats_row(col1, labels[EDGES], col2, stats_fmt.totedgesel, stats_fmt.totedge, y, height);
      stats_row(col1, labels[FACES], col2, stats_fmt.totfacesel, stats_fmt.totface, y, height);
      stats_row(col1, labels[TRIS], col2, stats_fmt.tottri, nullptr, y, height);
    }
    else if (ob->type == OB_ARMATURE) {
      stats_row(col1, labels[JOINTS], col2, stats_fmt.totvertsel, stats_fmt.totvert, y, height);
      stats_row(col1, labels[BONES], col2, stats_fmt.totbonesel, stats_fmt.totbone, y, height);
    }
    else if (ob->type == OB_POINTCLOUD) {
      stats_row(col1, labels[POINTS], col2, stats_fmt.totvertsel, stats_fmt.totpoints, y, height);
    }
    else if (ELEM(ob->type, OB_CURVES_LEGACY, OB_SURF, OB_CURVES)) {
      stats_row(col1, labels[POINTS], col2, stats_fmt.totpointsel, stats_fmt.totpoints, y, height);
      stats_row(col1, labels[CURVES], col2, stats_fmt.totcurvesel, stats_fmt.totcurves, y, height);
    }
    else if (ob->type != OB_FONT) {
      stats_row(col1, labels[VERTS], col2, stats_fmt.totvertsel, stats_fmt.totvert, y, height);
    }
  }
  else if (ob && BKE_object_use_sculptsession(object_mode)) {
    if (stats_is_object_dynamic_topology_sculpt(ob)) {
      stats_row(col1, labels[VERTS], col2, stats_fmt.totvertactive, nullptr, y, height);
      stats_row(col1, labels[TRIS], col2, stats_fmt.tottriactive, nullptr, y, height);
    }
    else {
      stats_row(col1, labels[VERTS], col2, stats_fmt.totvertactive, nullptr, y, height);
      stats_row(col1, labels[FACES], col2, stats_fmt.totfaceactive, nullptr, y, height);
    }
  }
  else if (ob && (object_mode & OB_MODE_SCULPT_CURVES)) {
    stats_row(col1, labels[VERTS], col2, stats_fmt.totvertactive, nullptr, y, height);
  }
  else if (ob && (object_mode & OB_MODE_POSE)) {
    stats_row(col1, labels[BONES], col2, stats_fmt.totbonesel, stats_fmt.totbone, y, height);
  }
  else if ((ob) && (ob->type == OB_LAMP)) {
    stats_row(col1, labels[LIGHTS], col2, stats_fmt.totlampsel, stats_fmt.totlamp, y, height);
  }
  else if ((object_mode == OB_MODE_OBJECT) && ob && ELEM(ob->type, OB_MESH, OB_FONT)) {
    /* Object mode with the active object a mesh or text object. */
    stats_row(col1, labels[VERTS], col2, stats_fmt.totvertsel, stats_fmt.totvert, y, height);
    stats_row(col1, labels[EDGES], col2, stats_fmt.totedgesel, stats_fmt.totedge, y, height);
    stats_row(col1, labels[FACES], col2, stats_fmt.totfacesel, stats_fmt.totface, y, height);
    stats_row(col1, labels[TRIS], col2, stats_fmt.tottrisel, stats_fmt.tottri, y, height);
  }
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_info/info_stats.cc · L868—L1001</summary>

<!-- original:55d088b2641ff0:source/blender/editors/space_info/info_stats.cc:868:1001 -->

```cpp
void ED_info_draw_stats(
    Main *bmain, Scene *scene, ViewLayer *view_layer, View3D *v3d_local, int x, int *y, int height)
{
  BLI_assert(v3d_local == nullptr || v3d_local->localvd != nullptr);
  SceneStatsFmt stats_fmt;
  if (!format_stats(bmain, scene, view_layer, v3d_local, &stats_fmt)) {
    return;
  }

  BKE_view_layer_synced_ensure(*bmain, scene, view_layer);
  Object *ob = BKE_view_layer_active_object_get(view_layer);
  eObjectMode object_mode = ob ? ob->mode : OB_MODE_OBJECT;
  const int font_id = BLF_default();

  /* Translated labels for each stat row. */
  enum {
    OBJ,
    VERTS,
    EDGES,
    FACES,
    TRIS,
    JOINTS,
    BONES,
    LAYERS,
    FRAMES,
    STROKES,
    POINTS,
    LIGHTS,
    CURVES,
    MAX_LABELS_COUNT
  };
  char labels[MAX_LABELS_COUNT][64];

  STRNCPY_UTF8(labels[OBJ], IFACE_("Objects"));
  STRNCPY_UTF8(labels[VERTS], IFACE_("Vertices"));
  STRNCPY_UTF8(labels[EDGES], IFACE_("Edges"));
  STRNCPY_UTF8(labels[FACES], IFACE_("Faces"));
  STRNCPY_UTF8(labels[TRIS], IFACE_("Triangles"));
  STRNCPY_UTF8(labels[JOINTS], IFACE_("Joints"));
  STRNCPY_UTF8(labels[BONES], IFACE_("Bones"));
  STRNCPY_UTF8(labels[LAYERS], IFACE_("Layers"));
  STRNCPY_UTF8(labels[FRAMES], IFACE_("Frames"));
  STRNCPY_UTF8(labels[STROKES], IFACE_("Strokes"));
  STRNCPY_UTF8(labels[POINTS], IFACE_("Points"));
  STRNCPY_UTF8(labels[LIGHTS], IFACE_("Lights"));
  STRNCPY_UTF8(labels[CURVES], IFACE_("Curves"));

  int longest_label = 0;
  for (int i = 0; i < MAX_LABELS_COUNT; ++i) {
    longest_label = max_ii(longest_label, BLF_width(font_id, labels[i], sizeof(labels[i])));
  }

  int col1 = x;
  int col2 = x + longest_label + (0.5f * U.widget_unit);

  /* Add some extra margin above this section. */
  *y -= (0.6f * height);

  bool any_objects = !STREQ(&stats_fmt.totobj[0], "0");
  bool any_selected = !STREQ(&stats_fmt.totobjsel[0], "0");

  if (any_selected) {
    stats_row(col1, labels[OBJ], col2, stats_fmt.totobjsel, stats_fmt.totobj, y, height);
  }
  else if (any_objects) {
    stats_row(col1, labels[OBJ], col2, stats_fmt.totobj, nullptr, y, height);
    /* Show scene totals if nothing is selected. */
    stats_row(col1, labels[VERTS], col2, stats_fmt.totvert, nullptr, y, height);
    stats_row(col1, labels[EDGES], col2, stats_fmt.totedge, nullptr, y, height);
    stats_row(col1, labels[FACES], col2, stats_fmt.totface, nullptr, y, height);
    stats_row(col1, labels[TRIS], col2, stats_fmt.tottri, nullptr, y, height);
    return;
  }
  else if (object_mode != OB_MODE_SCULPT_CURVES && !BKE_object_use_sculptsession(object_mode)) {
    /* No objects in scene. */
    stats_row(col1, labels[OBJ], col2, stats_fmt.totobj, nullptr, y, height);
    return;
  }

  if ((ob) && ob->type == OB_GREASE_PENCIL) {
    stats_row(col1, labels[LAYERS], col2, stats_fmt.totgplayer, nullptr, y, height);
    stats_row(col1, labels[FRAMES], col2, stats_fmt.totgpframe, nullptr, y, height);
    stats_row(col1, labels[STROKES], col2, stats_fmt.totgpstroke, nullptr, y, height);
    stats_row(col1, labels[POINTS], col2, stats_fmt.totpoints, nullptr, y, height);
  }
  else if (ob && ob->mode == OB_MODE_EDIT) {
    if (ob->type == OB_MESH) {
      stats_row(col1, labels[VERTS], col2, stats_fmt.totvertsel, stats_fmt.totvert, y, height);
      stats_row(col1, labels[EDGES], col2, stats_fmt.totedgesel, stats_fmt.totedge, y, height);
      stats_row(col1, labels[FACES], col2, stats_fmt.totfacesel, stats_fmt.totface, y, height);
      stats_row(col1, labels[TRIS], col2, stats_fmt.tottri, nullptr, y, height);
    }
    else if (ob->type == OB_ARMATURE) {
      stats_row(col1, labels[JOINTS], col2, stats_fmt.totvertsel, stats_fmt.totvert, y, height);
      stats_row(col1, labels[BONES], col2, stats_fmt.totbonesel, stats_fmt.totbone, y, height);
    }
    else if (ob->type == OB_POINTCLOUD) {
      stats_row(col1, labels[POINTS], col2, stats_fmt.totvertsel, stats_fmt.totpoints, y, height);
    }
    else if (ELEM(ob->type, OB_CURVES_LEGACY, OB_SURF, OB_CURVES)) {
      stats_row(col1, labels[POINTS], col2, stats_fmt.totpointsel, stats_fmt.totpoints, y, height);
      stats_row(col1, labels[CURVES], col2, stats_fmt.totcurvesel, stats_fmt.totcurves, y, height);
    }
    else if (ob->type != OB_FONT) {
      stats_row(col1, labels[VERTS], col2, stats_fmt.totvertsel, stats_fmt.totvert, y, height);
    }
  }
  else if (ob && BKE_object_use_sculptsession(object_mode)) {
    if (stats_is_object_dynamic_topology_sculpt(ob)) {
      stats_row(col1, labels[VERTS], col2, stats_fmt.totvertactive, nullptr, y, height);
      stats_row(col1, labels[TRIS], col2, stats_fmt.tottriactive, nullptr, y, height);
    }
    else {
      stats_row(col1, labels[VERTS], col2, stats_fmt.totvertactive, nullptr, y, height);
      stats_row(col1, labels[FACES], col2, stats_fmt.totfaceactive, nullptr, y, height);
    }
  }
  else if (ob && (object_mode & OB_MODE_SCULPT_CURVES)) {
    stats_row(col1, labels[VERTS], col2, stats_fmt.totvertactive, nullptr, y, height);
  }
  else if (ob && (object_mode & OB_MODE_POSE)) {
    stats_row(col1, labels[BONES], col2, stats_fmt.totbonesel, stats_fmt.totbone, y, height);
  }
  else if ((ob) && (ob->type == OB_LAMP)) {
    stats_row(col1, labels[LIGHTS], col2, stats_fmt.totlampsel, stats_fmt.totlamp, y, height);
  }
  else if ((object_mode == OB_MODE_OBJECT) && ob && ELEM(ob->type, OB_MESH, OB_FONT)) {
    /* Object mode with the active object a mesh or text object. */
    stats_row(col1, labels[VERTS], col2, stats_fmt.totvertsel, stats_fmt.totvert, y, height);
    stats_row(col1, labels[EDGES], col2, stats_fmt.totedgesel, stats_fmt.totedge, y, height);
    stats_row(col1, labels[FACES], col2, stats_fmt.totfacesel, stats_fmt.totface, y, height);
    stats_row(col1, labels[TRIS], col2, stats_fmt.tottrisel, stats_fmt.tottri, y, height);
  }
}
```

</details>

**沿实际写入检查状态**

- `longest_label = max_ii(longest_label, BLF_width(font_id, labels[i], sizeof(labels[i])));`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `format_stats` → [blender::format_stats · L559](info_stats.cc.md#f-51dcb7b269284f05)。
- `BKE_view_layer_synced_ensure` → [blender::BKE_view_layer_synced_ensure · L1035](../../../02-BKE几何与数据/intern/layer.cc.md#f-602c088654ebcb63)。
- `BKE_view_layer_active_object_get` → [blender::BKE_view_layer_active_object_get · L286](../../../02-BKE几何与数据/intern/layer_utils.cc.md#f-aa39df7416329726)。
- `BLF_default` → [blender::BLF_default · L39](../../blenfont/intern/blf_default.cc.md#f-bf89d50f903b84ce)。
- `STRNCPY_UTF8` → [STRNCPY_UTF8 · L335](../../../01-BLI基础库/BLI_string_utf8.hh.md#m-222967f0ab6a)。宏定义由构建条件选择。
- `IFACE_` → [IFACE_ · L49](../../blentranslation/BLT_translation.hh.md#m-378ed115fdc8)。宏定义由构建条件选择。
- `max_ii` → [blender::max_ii · L368](../../../01-BLI基础库/intern/math_base_inline.cc.md#f-c45aa7b373adb94c)。
- `BLF_width` → [blender::BLF_width · L835](../../blenfont/intern/blf.cc.md#f-5a3d5b80e418409f)。
- `STREQ` → [STREQ · L112](../../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-9549fb6aafd2)；[STREQ · L451](../../../01-BLI基础库/BLI_utildefines.hh.md#m-c7b745bcfad2)；[STREQ · L55](../../../07-Intern运行时与平台/clog/clog.cc.md#m-96e78f386894)。宏定义由构建条件选择。
- `stats_row` → [blender::stats_row · L853](info_stats.cc.md#f-2ba7a04d756ba5ef)。
- `BKE_object_use_sculptsession` → [blender::BKE_object_use_sculptsession · L4328](../../../02-BKE几何与数据/intern/object.cc.md#f-295e9e178b4df6bc)。
- `ELEM` → [ELEM · L88](../../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-d28724a15928)；[ELEM · L135](../../../01-BLI基础库/BLI_utildefines.hh.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `stats_is_object_dynamic_topology_sculpt` → [blender::stats_is_object_dynamic_topology_sculpt · L427](info_stats.cc.md#f-69d1d979a6347dc0)。
