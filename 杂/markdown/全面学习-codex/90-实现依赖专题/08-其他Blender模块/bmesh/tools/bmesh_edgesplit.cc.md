# 实现依赖专题：source/blender/bmesh/tools/bmesh_edgesplit.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::BM_mesh_edgesplit"]:::abstraction
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
  F["bmesh_edgesplit.cc实现"]:::compute
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

<a id="f-bcfd49ce12d30fa9"></a>

### `blender::BM_mesh_edgesplit`

实现位置：[source/blender/bmesh/tools/bmesh_edgesplit.cc](../../../../../../../../source/blender/bmesh/tools/bmesh_edgesplit.cc) · L22—L118。

接口参数：

- `BMesh *bm`
- `const bool use_verts`
- `const bool tag_only`
- `const bool copy_select`

**教学注释版**

<!-- annotated:27c0755c656b60 -->

```cpp
void BM_mesh_edgesplit(BMesh *bm,
                       const bool use_verts,
                       const bool tag_only,
                       const bool copy_select)
{
  BMIter iter;
  BMEdge *e;

  bool use_ese = false;
  Map<BMElem *, BMEditSelection *> ese_gh;

  if (copy_select && bm->selected.first()) {
    for (BMEditSelection &ese : bm->selected) {
      if (ese.htype != BM_FACE) {
        // [讲解] ese_gh.add：按哈希与相等关系加入键或键值。
        ese_gh.add(ese.ele, &ese);
      }
    }

    use_ese = true;
  }

  if (tag_only == false) {
    BM_mesh_elem_hflag_enable_all(bm, BM_EDGE | (use_verts ? BM_VERT : 0), BM_ELEM_TAG, false);
  }

  if (use_verts) {
    /* prevent one edge having both verts unflagged
     * we could alternately disable these edges, either way its a corner case.
     *
     * This is needed so we don't split off the edge but then none of its verts which
     * would leave a duplicate edge.
     */
    BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
      if (BM_elem_flag_test(e, BM_ELEM_TAG)) {
        if ((BM_elem_flag_test(e->v1, BM_ELEM_TAG) == false) &&
            (BM_elem_flag_test(e->v2, BM_ELEM_TAG) == false)) [[unlikely]]
        {
          BM_elem_flag_enable(e->v1, BM_ELEM_TAG);
          BM_elem_flag_enable(e->v2, BM_ELEM_TAG);
        }
      }
    }
  }
  else {
    BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
      if (BM_elem_flag_test(e, BM_ELEM_TAG)) {
        BM_elem_flag_enable(e->v1, BM_ELEM_TAG);
        BM_elem_flag_enable(e->v2, BM_ELEM_TAG);
      }
    }
  }

  BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
    if (BM_elem_flag_test(e, BM_ELEM_TAG)) {
      uint i;
      for (i = 0; i < 2; i++) {
        BMVert *v = ((&e->v1)[i]);
        if (BM_elem_flag_test(v, BM_ELEM_TAG)) {
          BM_elem_flag_disable(v, BM_ELEM_TAG);

          if (use_ese) {
            BMVert **vtar;
            int vtar_len;

            BM_vert_separate_hflag(bm, v, BM_ELEM_TAG, copy_select, &vtar, &vtar_len);

            /* first value is always in 'v' */
            if (vtar_len > 1) {
              // [讲解] ese_gh.lookup_default：按键查找对应项。
              BMEditSelection *ese = ese_gh.lookup_default(reinterpret_cast<BMElem *>(v), nullptr);
              BLI_assert(v == vtar[0]);
              if (ese) [[unlikely]] {
                int j;
                for (j = 1; j < vtar_len; j++) {
                  BLI_assert(v != vtar[j]);
                  BM_select_history_store_after_notest(bm, ese, vtar[j]);
                }
              }
            }
            MEM_delete(vtar);
          }
          else {
            BM_vert_separate_hflag(bm, v, BM_ELEM_TAG, copy_select, nullptr, nullptr);
          }
        }
      }
    }
  }

#ifndef NDEBUG
  /* ensure we don't have any double edges! */
  BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
    if (BM_elem_flag_test(e, BM_ELEM_TAG)) {
      BLI_assert(BM_edge_find_double(e) == nullptr);
    }
  }
#endif
}
```

<details>
<summary>核对原始源码：source/blender/bmesh/tools/bmesh_edgesplit.cc · L22—L118</summary>

<!-- original:27c0755c656b60:source/blender/bmesh/tools/bmesh_edgesplit.cc:22:118 -->

```cpp
void BM_mesh_edgesplit(BMesh *bm,
                       const bool use_verts,
                       const bool tag_only,
                       const bool copy_select)
{
  BMIter iter;
  BMEdge *e;

  bool use_ese = false;
  Map<BMElem *, BMEditSelection *> ese_gh;

  if (copy_select && bm->selected.first()) {
    for (BMEditSelection &ese : bm->selected) {
      if (ese.htype != BM_FACE) {
        ese_gh.add(ese.ele, &ese);
      }
    }

    use_ese = true;
  }

  if (tag_only == false) {
    BM_mesh_elem_hflag_enable_all(bm, BM_EDGE | (use_verts ? BM_VERT : 0), BM_ELEM_TAG, false);
  }

  if (use_verts) {
    /* prevent one edge having both verts unflagged
     * we could alternately disable these edges, either way its a corner case.
     *
     * This is needed so we don't split off the edge but then none of its verts which
     * would leave a duplicate edge.
     */
    BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
      if (BM_elem_flag_test(e, BM_ELEM_TAG)) {
        if ((BM_elem_flag_test(e->v1, BM_ELEM_TAG) == false) &&
            (BM_elem_flag_test(e->v2, BM_ELEM_TAG) == false)) [[unlikely]]
        {
          BM_elem_flag_enable(e->v1, BM_ELEM_TAG);
          BM_elem_flag_enable(e->v2, BM_ELEM_TAG);
        }
      }
    }
  }
  else {
    BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
      if (BM_elem_flag_test(e, BM_ELEM_TAG)) {
        BM_elem_flag_enable(e->v1, BM_ELEM_TAG);
        BM_elem_flag_enable(e->v2, BM_ELEM_TAG);
      }
    }
  }

  BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
    if (BM_elem_flag_test(e, BM_ELEM_TAG)) {
      uint i;
      for (i = 0; i < 2; i++) {
        BMVert *v = ((&e->v1)[i]);
        if (BM_elem_flag_test(v, BM_ELEM_TAG)) {
          BM_elem_flag_disable(v, BM_ELEM_TAG);

          if (use_ese) {
            BMVert **vtar;
            int vtar_len;

            BM_vert_separate_hflag(bm, v, BM_ELEM_TAG, copy_select, &vtar, &vtar_len);

            /* first value is always in 'v' */
            if (vtar_len > 1) {
              BMEditSelection *ese = ese_gh.lookup_default(reinterpret_cast<BMElem *>(v), nullptr);
              BLI_assert(v == vtar[0]);
              if (ese) [[unlikely]] {
                int j;
                for (j = 1; j < vtar_len; j++) {
                  BLI_assert(v != vtar[j]);
                  BM_select_history_store_after_notest(bm, ese, vtar[j]);
                }
              }
            }
            MEM_delete(vtar);
          }
          else {
            BM_vert_separate_hflag(bm, v, BM_ELEM_TAG, copy_select, nullptr, nullptr);
          }
        }
      }
    }
  }

#ifndef NDEBUG
  /* ensure we don't have any double edges! */
  BM_ITER_MESH (e, &iter, bm, BM_EDGES_OF_MESH) {
    if (BM_elem_flag_test(e, BM_ELEM_TAG)) {
      BLI_assert(BM_edge_find_double(e) == nullptr);
    }
  }
#endif
}
```

</details>

**沿实际写入检查状态**

- `use_ese = true;`

**继续追踪实现**

- `bm->selected.first` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L33。
- `ese_gh.add` → [blender::Map::add · L295](../../../../02-哈希表与关联数据结构/04-Map查找与键访问.md#f-8d38101abf162f88)；[blender::Map::add · L299](../../../../02-哈希表与关联数据结构/04-Map查找与键访问.md#f-1f59510cdfbd9f87)；[blender::Map::add · L303](../../../../02-哈希表与关联数据结构/04-Map查找与键访问.md#f-645e0522347aa018)；[blender::Map::add · L307](../../../../02-哈希表与关联数据结构/04-Map查找与键访问.md#f-03405db0730cedc0)。同名重载需按实参类型选择。
- `BM_mesh_elem_hflag_enable_all` → [blender::BM_mesh_elem_hflag_enable_all · L1490](../intern/bmesh_marking.cc.md#f-5b566fccb0a00869)。
- `BM_ITER_MESH` → [BM_ITER_MESH · L72](../intern/bmesh_iterators.hh.md#m-cfc837c73218)。宏定义由构建条件选择。
- `BM_elem_flag_test` → [BM_elem_flag_test · L21](../intern/bmesh_inline.hh.md#m-2431d1179b41)。宏定义由构建条件选择。
- `BM_elem_flag_enable` → [BM_elem_flag_enable · L23](../intern/bmesh_inline.hh.md#m-4400242f1540)。宏定义由构建条件选择。
- `BM_elem_flag_disable` → [BM_elem_flag_disable · L24](../intern/bmesh_inline.hh.md#m-e129d62b6353)。宏定义由构建条件选择。
- `BM_vert_separate_hflag` → [blender::BM_vert_separate_hflag · L2617](../intern/bmesh_core.cc.md#f-46e27171ed6c03a5)。
- `ese_gh.lookup_default` → [blender::Map::lookup_default · L570](../../../../02-哈希表与关联数据结构/05-Map插入与回调.md#f-40294aaf345f6a8b)。
- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `BM_select_history_store_after_notest` → [BM_select_history_store_after_notest · L184](../intern/bmesh_marking.hh.md#m-e79eb8084035)。宏定义由构建条件选择。
- `MEM_delete` → [MEM_delete · L400](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
- `BM_edge_find_double` → [blender::BM_edge_find_double · L1596](../intern/bmesh_query.cc.md#f-e8fe1abc12f9ca2c)。
