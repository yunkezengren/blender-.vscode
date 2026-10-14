# 实现依赖专题：source/blender/bmesh/tools/bmesh_triangulate.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::bm_face_triangulate_mapping"]:::abstraction
  F1["blender::BM_mesh_triangulate"]:::compute
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
  F["bmesh_triangulate.cc实现"]:::compute
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

<a id="f-600a65b9fc732194"></a>

### `blender::bm_face_triangulate_mapping`

实现位置：[source/blender/bmesh/tools/bmesh_triangulate.cc](../../../../../../../../source/blender/bmesh/tools/bmesh_triangulate.cc) · L33—L78。

接口参数：

- `BMesh *bm`
- `BMFace *face`
- `const int quad_method`
- `const int ngon_method`
- `const bool use_tag`
- `BMOperator *op`
- `BMOpSlot *slot_facemap_out`
- `BMOpSlot *slot_facemap_double_out`
- `MemArena *pf_arena`
- `Heap *pf_heap`

**教学注释版**

<!-- annotated:6412f52fca531f -->

```cpp
static void bm_face_triangulate_mapping(BMesh *bm,
                                        BMFace *face,
                                        const int quad_method,
                                        const int ngon_method,
                                        const bool use_tag,
                                        BMOperator *op,
                                        BMOpSlot *slot_facemap_out,
                                        BMOpSlot *slot_facemap_double_out,

                                        MemArena *pf_arena,
                                        /* use for MOD_TRIANGULATE_NGON_BEAUTY only! */
                                        Heap *pf_heap)
{
  int faces_array_tot = face->len - 3;
  Array<BMFace *, BM_DEFAULT_NGON_STACK_SIZE> faces_array(faces_array_tot);
  LinkNode *faces_double = nullptr;
  BLI_assert(face->len > 3);

  BM_face_triangulate(bm,
                      face,
                      // [讲解] faces_array.data：提供数组的借用访问入口。
                      faces_array.data(),
                      &faces_array_tot,
                      nullptr,
                      nullptr,
                      &faces_double,
                      quad_method,
                      ngon_method,
                      use_tag,
                      pf_arena,
                      pf_heap);

  if (faces_array_tot) {
    int i;
    BMO_slot_map_elem_insert(op, slot_facemap_out, face, face);
    for (i = 0; i < faces_array_tot; i++) {
      BMO_slot_map_elem_insert(op, slot_facemap_out, faces_array[i], face);
    }

    while (faces_double) {
      LinkNode *next = faces_double->next;
      BMO_slot_map_elem_insert(op, slot_facemap_double_out, faces_double->link, face);
      MEM_delete(faces_double);
      faces_double = next;
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/bmesh/tools/bmesh_triangulate.cc · L33—L78</summary>

<!-- original:6412f52fca531f:source/blender/bmesh/tools/bmesh_triangulate.cc:33:78 -->

```cpp
static void bm_face_triangulate_mapping(BMesh *bm,
                                        BMFace *face,
                                        const int quad_method,
                                        const int ngon_method,
                                        const bool use_tag,
                                        BMOperator *op,
                                        BMOpSlot *slot_facemap_out,
                                        BMOpSlot *slot_facemap_double_out,

                                        MemArena *pf_arena,
                                        /* use for MOD_TRIANGULATE_NGON_BEAUTY only! */
                                        Heap *pf_heap)
{
  int faces_array_tot = face->len - 3;
  Array<BMFace *, BM_DEFAULT_NGON_STACK_SIZE> faces_array(faces_array_tot);
  LinkNode *faces_double = nullptr;
  BLI_assert(face->len > 3);

  BM_face_triangulate(bm,
                      face,
                      faces_array.data(),
                      &faces_array_tot,
                      nullptr,
                      nullptr,
                      &faces_double,
                      quad_method,
                      ngon_method,
                      use_tag,
                      pf_arena,
                      pf_heap);

  if (faces_array_tot) {
    int i;
    BMO_slot_map_elem_insert(op, slot_facemap_out, face, face);
    for (i = 0; i < faces_array_tot; i++) {
      BMO_slot_map_elem_insert(op, slot_facemap_out, faces_array[i], face);
    }

    while (faces_double) {
      LinkNode *next = faces_double->next;
      BMO_slot_map_elem_insert(op, slot_facemap_double_out, faces_double->link, face);
      MEM_delete(faces_double);
      faces_double = next;
    }
  }
}
```

</details>

**沿实际写入检查状态**

- `faces_double = next;`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `BM_face_triangulate` → [blender::BM_face_triangulate · L1105](../intern/bmesh_polygon.cc.md#f-8d73b1b09152f5c5)。
- `faces_array.data` → [blender::Array::data · L323](../../../../01-基础容器与现代CPP/08-Array复制移动与销毁.md#f-95648c799002f4ba)；[blender::Array::data · L327](../../../../01-基础容器与现代CPP/08-Array复制移动与销毁.md#f-50c18301f8c40f9e)。同名重载需按实参类型选择。
- `BMO_slot_map_elem_insert` → [blender::BMO_slot_map_elem_insert · L133](../intern/bmesh_operator_api_inline.hh.md#f-3c19d6917323bf82)。
- `MEM_delete` → [MEM_delete · L400](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。

<a id="f-234e032890f12d29"></a>

### `blender::BM_mesh_triangulate`

实现位置：[source/blender/bmesh/tools/bmesh_triangulate.cc](../../../../../../../../source/blender/bmesh/tools/bmesh_triangulate.cc) · L80—L157。

接口参数：

- `BMesh *bm`
- `const int quad_method`
- `const int ngon_method`
- `const int min_vertices`
- `const bool tag_only`
- `BMOperator *op`
- `BMOpSlot *slot_facemap_out`
- `BMOpSlot *slot_facemap_double_out`

**教学注释版**

<!-- annotated:4f3ad26e198ba4 -->

```cpp
void BM_mesh_triangulate(BMesh *bm,
                         const int quad_method,
                         const int ngon_method,
                         const int min_vertices,
                         const bool tag_only,
                         BMOperator *op,
                         BMOpSlot *slot_facemap_out,
                         BMOpSlot *slot_facemap_double_out)
{
  BMIter iter;
  BMFace *face;
  MemArena *pf_arena;
  Heap *pf_heap;

  pf_arena = BLI_memarena_new(BLI_POLYFILL_ARENA_SIZE, __func__);

  if (ngon_method == MOD_TRIANGULATE_NGON_BEAUTY) {
    pf_heap = BLI_heap_new_ex(BLI_POLYFILL_ALLOC_NGON_RESERVE);
  }
  else {
    pf_heap = nullptr;
  }

  if (slot_facemap_out) {
    /* same as below but call: bm_face_triangulate_mapping() */
    BM_ITER_MESH (face, &iter, bm, BM_FACES_OF_MESH) {
      if (face->len >= min_vertices) {
        if (tag_only == false || BM_elem_flag_test(face, BM_ELEM_TAG)) {
          bm_face_triangulate_mapping(bm,
                                      face,
                                      quad_method,
                                      ngon_method,
                                      tag_only,
                                      op,
                                      slot_facemap_out,
                                      slot_facemap_double_out,
                                      pf_arena,
                                      pf_heap);
        }
      }
    }
  }
  else {
    LinkNode *faces_double = nullptr;

    BM_ITER_MESH (face, &iter, bm, BM_FACES_OF_MESH) {
      if (face->len >= min_vertices) {
        if (tag_only == false || BM_elem_flag_test(face, BM_ELEM_TAG)) {
          BM_face_triangulate(bm,
                              face,
                              nullptr,
                              nullptr,
                              nullptr,
                              nullptr,
                              &faces_double,
                              quad_method,
                              ngon_method,
                              tag_only,
                              pf_arena,
                              pf_heap);
        }
      }
    }

    while (faces_double) {
      LinkNode *next = faces_double->next;
      BM_face_kill(bm, static_cast<BMFace *>(faces_double->link));
      MEM_delete(faces_double);
      faces_double = next;
    }
  }

  BLI_memarena_free(pf_arena);

  if (ngon_method == MOD_TRIANGULATE_NGON_BEAUTY) {
    BLI_heap_free(pf_heap, nullptr);
  }
}
```

<details>
<summary>核对原始源码：source/blender/bmesh/tools/bmesh_triangulate.cc · L80—L157</summary>

<!-- original:4f3ad26e198ba4:source/blender/bmesh/tools/bmesh_triangulate.cc:80:157 -->

```cpp
void BM_mesh_triangulate(BMesh *bm,
                         const int quad_method,
                         const int ngon_method,
                         const int min_vertices,
                         const bool tag_only,
                         BMOperator *op,
                         BMOpSlot *slot_facemap_out,
                         BMOpSlot *slot_facemap_double_out)
{
  BMIter iter;
  BMFace *face;
  MemArena *pf_arena;
  Heap *pf_heap;

  pf_arena = BLI_memarena_new(BLI_POLYFILL_ARENA_SIZE, __func__);

  if (ngon_method == MOD_TRIANGULATE_NGON_BEAUTY) {
    pf_heap = BLI_heap_new_ex(BLI_POLYFILL_ALLOC_NGON_RESERVE);
  }
  else {
    pf_heap = nullptr;
  }

  if (slot_facemap_out) {
    /* same as below but call: bm_face_triangulate_mapping() */
    BM_ITER_MESH (face, &iter, bm, BM_FACES_OF_MESH) {
      if (face->len >= min_vertices) {
        if (tag_only == false || BM_elem_flag_test(face, BM_ELEM_TAG)) {
          bm_face_triangulate_mapping(bm,
                                      face,
                                      quad_method,
                                      ngon_method,
                                      tag_only,
                                      op,
                                      slot_facemap_out,
                                      slot_facemap_double_out,
                                      pf_arena,
                                      pf_heap);
        }
      }
    }
  }
  else {
    LinkNode *faces_double = nullptr;

    BM_ITER_MESH (face, &iter, bm, BM_FACES_OF_MESH) {
      if (face->len >= min_vertices) {
        if (tag_only == false || BM_elem_flag_test(face, BM_ELEM_TAG)) {
          BM_face_triangulate(bm,
                              face,
                              nullptr,
                              nullptr,
                              nullptr,
                              nullptr,
                              &faces_double,
                              quad_method,
                              ngon_method,
                              tag_only,
                              pf_arena,
                              pf_heap);
        }
      }
    }

    while (faces_double) {
      LinkNode *next = faces_double->next;
      BM_face_kill(bm, static_cast<BMFace *>(faces_double->link));
      MEM_delete(faces_double);
      faces_double = next;
    }
  }

  BLI_memarena_free(pf_arena);

  if (ngon_method == MOD_TRIANGULATE_NGON_BEAUTY) {
    BLI_heap_free(pf_heap, nullptr);
  }
}
```

</details>

**沿实际写入检查状态**

- `pf_arena = BLI_memarena_new(BLI_POLYFILL_ARENA_SIZE, __func__);`
- `pf_heap = BLI_heap_new_ex(BLI_POLYFILL_ALLOC_NGON_RESERVE);`
- `pf_heap = nullptr;`
- `faces_double = next;`

**继续追踪实现**

- `BLI_memarena_new` → [blender::BLI_memarena_new · L73](../../../01-BLI基础库/intern/BLI_memarena.cc.md#f-590ef4f6ab548c98)。
- `BLI_heap_new_ex` → [blender::BLI_heap_new_ex · L173](../../../01-BLI基础库/intern/BLI_heap.cc.md#f-f7be2a63ad410ef3)。
- `BM_ITER_MESH` → [BM_ITER_MESH · L72](../intern/bmesh_iterators.hh.md#m-cfc837c73218)。宏定义由构建条件选择。
- `BM_elem_flag_test` → [BM_elem_flag_test · L21](../intern/bmesh_inline.hh.md#m-2431d1179b41)。宏定义由构建条件选择。
- `bm_face_triangulate_mapping` → [blender::bm_face_triangulate_mapping · L33](bmesh_triangulate.cc.md#f-600a65b9fc732194)。
- `BM_face_triangulate` → [blender::BM_face_triangulate · L1105](../intern/bmesh_polygon.cc.md#f-8d73b1b09152f5c5)。
- `BM_face_kill` → [blender::BM_face_kill · L957](../intern/bmesh_core.cc.md#f-fbdcd02b85e7db02)。
- `MEM_delete` → [MEM_delete · L400](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
- `BLI_memarena_free` → [blender::BLI_memarena_free · L103](../../../01-BLI基础库/intern/BLI_memarena.cc.md#f-a655794ad41d1bdf)。
- `BLI_heap_free` → [blender::BLI_heap_free · L193](../../../01-BLI基础库/intern/BLI_heap.cc.md#f-8460909856d9ccf1)。
