# 实现依赖专题：source/blender/draw/intern/mesh_extractors/extract_mesh.hh

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::draw::editmesh_final_or_this"]:::abstraction
  F1["blender::draw::bm_original_face_get"]:::compute
  F2["blender::draw::bm_original_edge_get"]:::compute
  F3["blender::draw::bm_original_vert_get"]:::compute
  F4["blender::draw::bm_vert_co_get"]:::compute
  F5["blender::draw::bm_vert_no_get"]:::compute
  F6["blender::draw::bm_face_no_get"]:::compute
  F7["blender::draw::edge_from_corners"]:::compute
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
  F["extract_mesh.hh实现"]:::compute
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

<a id="f-944dcc47588a370b"></a>

### `blender::draw::editmesh_final_or_this`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L127—L136。

接口参数：

- `const Object &object`
- `const Mesh &mesh`

**教学注释版**

<!-- annotated:4fe7428cb07142 -->

```cpp
inline const Mesh &editmesh_final_or_this(const Object &object, const Mesh &mesh)
{
  if (mesh.runtime->edit_mesh != nullptr) {
    if (const Mesh *editmesh_eval_final = BKE_object_get_editmesh_eval_final(&object)) {
      return *editmesh_eval_final;
    }
  }

  return mesh;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L127—L136</summary>

<!-- original:4fe7428cb07142:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:127:136 -->

```cpp
inline const Mesh &editmesh_final_or_this(const Object &object, const Mesh &mesh)
{
  if (mesh.runtime->edit_mesh != nullptr) {
    if (const Mesh *editmesh_eval_final = BKE_object_get_editmesh_eval_final(&object)) {
      return *editmesh_eval_final;
    }
  }

  return mesh;
}
```

</details>

**结果出口**

- `return *editmesh_eval_final;`
- `return mesh;`

**继续追踪实现**

- `BKE_object_get_editmesh_eval_final` → [blender::BKE_object_get_editmesh_eval_final · L4477](../../../../02-BKE几何与数据/intern/object.cc.md#f-1788f7ea6bf8faec)。

<a id="f-50ae48e6025f345a"></a>

### `blender::draw::bm_original_face_get`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L138—L144。

接口参数：

- `const MeshRenderData &mr`
- `int idx`

**教学注释版**

<!-- annotated:9598916f3b7f99 -->

```cpp
BLI_INLINE BMFace *bm_original_face_get(const MeshRenderData &mr, int idx)
{
  return ((mr.orig_index_face != nullptr) && (mr.orig_index_face[idx] != ORIGINDEX_NONE) &&
          mr.bm) ?
             BM_face_at_index(mr.bm, mr.orig_index_face[idx]) :
             nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L138—L144</summary>

<!-- original:9598916f3b7f99:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:138:144 -->

```cpp
BLI_INLINE BMFace *bm_original_face_get(const MeshRenderData &mr, int idx)
{
  return ((mr.orig_index_face != nullptr) && (mr.orig_index_face[idx] != ORIGINDEX_NONE) &&
          mr.bm) ?
             BM_face_at_index(mr.bm, mr.orig_index_face[idx]) :
             nullptr;
}
```

</details>

**结果出口**

- `return ((mr.orig_index_face != nullptr) && (mr.orig_index_face[idx] != ORIGINDEX_NONE) &&`

**继续追踪实现**

- `BM_face_at_index` → [blender::BM_face_at_index · L122](../../../bmesh/intern/bmesh_mesh.hh.md#f-366df62c166d5094)。

<a id="f-5abdd93646642da5"></a>

### `blender::draw::bm_original_edge_get`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L146—L152。

接口参数：

- `const MeshRenderData &mr`
- `int idx`

**教学注释版**

<!-- annotated:d2869d38b32c86 -->

```cpp
BLI_INLINE BMEdge *bm_original_edge_get(const MeshRenderData &mr, int idx)
{
  return ((mr.orig_index_edge != nullptr) && (mr.orig_index_edge[idx] != ORIGINDEX_NONE) &&
          mr.bm) ?
             BM_edge_at_index(mr.bm, mr.orig_index_edge[idx]) :
             nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L146—L152</summary>

<!-- original:d2869d38b32c86:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:146:152 -->

```cpp
BLI_INLINE BMEdge *bm_original_edge_get(const MeshRenderData &mr, int idx)
{
  return ((mr.orig_index_edge != nullptr) && (mr.orig_index_edge[idx] != ORIGINDEX_NONE) &&
          mr.bm) ?
             BM_edge_at_index(mr.bm, mr.orig_index_edge[idx]) :
             nullptr;
}
```

</details>

**结果出口**

- `return ((mr.orig_index_edge != nullptr) && (mr.orig_index_edge[idx] != ORIGINDEX_NONE) &&`

**继续追踪实现**

- `BM_edge_at_index` → [blender::BM_edge_at_index · L116](../../../bmesh/intern/bmesh_mesh.hh.md#f-81d027fd9e6b4c84)。

<a id="f-45547245e3f51daa"></a>

### `blender::draw::bm_original_vert_get`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L154—L160。

接口参数：

- `const MeshRenderData &mr`
- `int idx`

**教学注释版**

<!-- annotated:cd005ec3e1eded -->

```cpp
BLI_INLINE BMVert *bm_original_vert_get(const MeshRenderData &mr, int idx)
{
  return ((mr.orig_index_vert != nullptr) && (mr.orig_index_vert[idx] != ORIGINDEX_NONE) &&
          mr.bm) ?
             BM_vert_at_index(mr.bm, mr.orig_index_vert[idx]) :
             nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L154—L160</summary>

<!-- original:cd005ec3e1eded:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:154:160 -->

```cpp
BLI_INLINE BMVert *bm_original_vert_get(const MeshRenderData &mr, int idx)
{
  return ((mr.orig_index_vert != nullptr) && (mr.orig_index_vert[idx] != ORIGINDEX_NONE) &&
          mr.bm) ?
             BM_vert_at_index(mr.bm, mr.orig_index_vert[idx]) :
             nullptr;
}
```

</details>

**结果出口**

- `return ((mr.orig_index_vert != nullptr) && (mr.orig_index_vert[idx] != ORIGINDEX_NONE) &&`

**继续追踪实现**

- `BM_vert_at_index` → [blender::BM_vert_at_index · L110](../../../bmesh/intern/bmesh_mesh.hh.md#f-aced0ebcd417a2f4)。

<a id="f-b669e5a0bcf94c9f"></a>

### `blender::draw::bm_vert_co_get`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L162—L168。

接口参数：

- `const MeshRenderData &mr`
- `const BMVert *eve`

**教学注释版**

<!-- annotated:0cae8edb7335ee -->

```cpp
BLI_INLINE const float *bm_vert_co_get(const MeshRenderData &mr, const BMVert *eve)
{
  if (!mr.bm_vert_coords.is_empty()) {
    return mr.bm_vert_coords[BM_elem_index_get(eve)];
  }
  return eve->co;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L162—L168</summary>

<!-- original:0cae8edb7335ee:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:162:168 -->

```cpp
BLI_INLINE const float *bm_vert_co_get(const MeshRenderData &mr, const BMVert *eve)
{
  if (!mr.bm_vert_coords.is_empty()) {
    return mr.bm_vert_coords[BM_elem_index_get(eve)];
  }
  return eve->co;
}
```

</details>

**结果出口**

- `return mr.bm_vert_coords[BM_elem_index_get(eve)];`
- `return eve->co;`

**继续追踪实现**

- `mr.bm_vert_coords.is_empty` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L164。
- `BM_elem_index_get` → [BM_elem_index_get · L120](../../../bmesh/intern/bmesh_inline.hh.md#m-201981cdc62d)。宏定义由构建条件选择。

<a id="f-c2d47f6477827d01"></a>

### `blender::draw::bm_vert_no_get`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L170—L179。

接口参数：

- `const MeshRenderData &mr`
- `const BMVert *eve`

**教学注释版**

<!-- annotated:3691d347343455 -->

```cpp
BLI_INLINE const float *bm_vert_no_get(const MeshRenderData &mr, const BMVert *eve)
{
  if (mr.bm_free_normal_offset_vert != -1) {
    return BM_ELEM_CD_GET_FLOAT_P(eve, mr.bm_free_normal_offset_vert);
  }
  if (!mr.bm_vert_normals.is_empty()) {
    return mr.bm_vert_normals[BM_elem_index_get(eve)];
  }
  return eve->no;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L170—L179</summary>

<!-- original:3691d347343455:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:170:179 -->

```cpp
BLI_INLINE const float *bm_vert_no_get(const MeshRenderData &mr, const BMVert *eve)
{
  if (mr.bm_free_normal_offset_vert != -1) {
    return BM_ELEM_CD_GET_FLOAT_P(eve, mr.bm_free_normal_offset_vert);
  }
  if (!mr.bm_vert_normals.is_empty()) {
    return mr.bm_vert_normals[BM_elem_index_get(eve)];
  }
  return eve->no;
}
```

</details>

**结果出口**

- `return BM_ELEM_CD_GET_FLOAT_P(eve, mr.bm_free_normal_offset_vert);`
- `return mr.bm_vert_normals[BM_elem_index_get(eve)];`
- `return eve->no;`

**继续追踪实现**

- `BM_ELEM_CD_GET_FLOAT_P` → [BM_ELEM_CD_GET_FLOAT_P · L635](../../../bmesh/bmesh_class.hh.md#m-544f72c45c1b)；[BM_ELEM_CD_GET_FLOAT_P · L661](../../../bmesh/bmesh_class.hh.md#m-c11efbe96e86)。宏定义由构建条件选择。
- `mr.bm_vert_normals.is_empty` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L175。
- `BM_elem_index_get` → [BM_elem_index_get · L120](../../../bmesh/intern/bmesh_inline.hh.md#m-201981cdc62d)。宏定义由构建条件选择。

<a id="f-40a3dcea78714956"></a>

### `blender::draw::bm_face_no_get`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L181—L190。

接口参数：

- `const MeshRenderData &mr`
- `const BMFace *efa`

**教学注释版**

<!-- annotated:c4027101ace661 -->

```cpp
BLI_INLINE const float *bm_face_no_get(const MeshRenderData &mr, const BMFace *efa)
{
  if (mr.bm_free_normal_offset_face != -1) {
    return BM_ELEM_CD_GET_FLOAT_P(efa, mr.bm_free_normal_offset_face);
  }
  if (!mr.bm_face_normals.is_empty()) {
    return mr.bm_face_normals[BM_elem_index_get(efa)];
  }
  return efa->no;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L181—L190</summary>

<!-- original:c4027101ace661:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:181:190 -->

```cpp
BLI_INLINE const float *bm_face_no_get(const MeshRenderData &mr, const BMFace *efa)
{
  if (mr.bm_free_normal_offset_face != -1) {
    return BM_ELEM_CD_GET_FLOAT_P(efa, mr.bm_free_normal_offset_face);
  }
  if (!mr.bm_face_normals.is_empty()) {
    return mr.bm_face_normals[BM_elem_index_get(efa)];
  }
  return efa->no;
}
```

</details>

**结果出口**

- `return BM_ELEM_CD_GET_FLOAT_P(efa, mr.bm_free_normal_offset_face);`
- `return mr.bm_face_normals[BM_elem_index_get(efa)];`
- `return efa->no;`

**继续追踪实现**

- `BM_ELEM_CD_GET_FLOAT_P` → [BM_ELEM_CD_GET_FLOAT_P · L635](../../../bmesh/bmesh_class.hh.md#m-544f72c45c1b)；[BM_ELEM_CD_GET_FLOAT_P · L661](../../../bmesh/bmesh_class.hh.md#m-c11efbe96e86)。宏定义由构建条件选择。
- `mr.bm_face_normals.is_empty` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L186。
- `BM_elem_index_get` → [BM_elem_index_get · L120](../../../bmesh/intern/bmesh_inline.hh.md#m-201981cdc62d)。宏定义由构建条件选择。

<a id="f-235a5dd9eb64ff86"></a>

### `blender::draw::edge_from_corners`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L240—L244。

接口参数：

- `const IndexRange face`
- `const int corner`

**教学注释版**

<!-- annotated:8f8275f190626f -->

```cpp
inline uint2 edge_from_corners(const IndexRange face, const int corner)
{
  const int corner_next = bke::mesh::face_corner_next(face, corner);
  return uint2(corner, corner_next);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L240—L244</summary>

<!-- original:8f8275f190626f:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:240:244 -->

```cpp
inline uint2 edge_from_corners(const IndexRange face, const int corner)
{
  const int corner_next = bke::mesh::face_corner_next(face, corner);
  return uint2(corner, corner_next);
}
```

</details>

**结果出口**

- `return uint2(corner, corner_next);`

**继续追踪实现**

- `bke::mesh::face_corner_next` → [blender::bke::mesh::face_corner_next · L315](../../../../../05-几何存储与拓扑映射/01-Mesh顶点边面角点.md#f-bf639df87b51fe48)。
- `uint2` → [uint2](../../../../07-Intern运行时与平台/cycles/util/types_uint2.h.md#t-acfae85419d8)。

<a id="f-0d5eeb9cb9333f7e"></a>

### `blender::draw::extract_mesh_loose_edge_data`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L246—L259。

接口参数：

- `const Span<T> vert_data`
- `const Span<int2> edges`
- `const IndexMask &loose_edges`
- `MutableSpan<T> gpu_data`

**教学注释版**

<!-- annotated:c81e7a4fa203d3 -->

```cpp
template<typename T>
void extract_mesh_loose_edge_data(const Span<T> vert_data,
                                  const Span<int2> edges,
                                  const IndexMask &loose_edges,
                                  MutableSpan<T> gpu_data)
{
  loose_edges.foreach_index_optimized<int>(
      [&](const int i, const int pos) {
        const int2 edge = edges[i];
        gpu_data[pos * 2 + 0] = vert_data[edge[0]];
        gpu_data[pos * 2 + 1] = vert_data[edge[1]];
      },
      exec_mode::grain_size(4096));
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L246—L259</summary>

<!-- original:c81e7a4fa203d3:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:246:259 -->

```cpp
template<typename T>
void extract_mesh_loose_edge_data(const Span<T> vert_data,
                                  const Span<int2> edges,
                                  const IndexMask &loose_edges,
                                  MutableSpan<T> gpu_data)
{
  loose_edges.foreach_index_optimized<int>(
      [&](const int i, const int pos) {
        const int2 edge = edges[i];
        gpu_data[pos * 2 + 0] = vert_data[edge[0]];
        gpu_data[pos * 2 + 1] = vert_data[edge[1]];
      },
      exec_mode::grain_size(4096));
}
```

</details>

**继续追踪实现**

- `loose_edges.foreach_index_optimized<int>` → [blender::index_mask::IndexMask::foreach_index_optimized · L937](../../../../../04-虚拟数组与索引选择/12-重构历史与基准练习.md#f-a2c3e7876407eaaf)。
- `exec_mode::grain_size` → [blender::exec_mode::grain_size · L79](../../../../01-BLI基础库/BLI_execution_mode.hh.md#f-0b4fc2f9fa6e66e7)。

<a id="f-1d43c35d50f54c24"></a>

### `blender::draw::loose_data_upload`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.hh](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.hh) · L289—L299。

接口参数：

- `const MeshRenderData &mr`
- `const Span<T> loose_data`
- `gpu::VertBuf &dst`

**教学注释版**

<!-- annotated:0bd20f3073d889 -->

```cpp
template<typename T>
void loose_data_upload(const MeshRenderData &mr, const Span<T> loose_data, gpu::VertBuf &dst)
{
  // [讲解] loose_data.is_empty：查询视图长度或生成对应有效索引区间。
  if (loose_data.is_empty()) {
    return;
  }
  BLI_assert(GPU_vertbuf_get_format(&dst)->stride == sizeof(T));
  GPU_vertbuf_use(&dst);
  GPU_vertbuf_update_sub(
      // [讲解] loose_data.data：返回借用范围的地址。
      &dst, mr.corners_num * sizeof(T), loose_data.size_in_bytes(), loose_data.data());
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.hh · L289—L299</summary>

<!-- original:0bd20f3073d889:source/blender/draw/intern/mesh_extractors/extract_mesh.hh:289:299 -->

```cpp
template<typename T>
void loose_data_upload(const MeshRenderData &mr, const Span<T> loose_data, gpu::VertBuf &dst)
{
  if (loose_data.is_empty()) {
    return;
  }
  BLI_assert(GPU_vertbuf_get_format(&dst)->stride == sizeof(T));
  GPU_vertbuf_use(&dst);
  GPU_vertbuf_update_sub(
      &dst, mr.corners_num * sizeof(T), loose_data.size_in_bytes(), loose_data.data());
}
```

</details>

**继续追踪实现**

- `loose_data.is_empty` → [blender::Span::is_empty · L264](../../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-8cc1d7ba8feb50e6)。
- `BLI_assert` → [BLI_assert · L48](../../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `GPU_vertbuf_get_format` → [blender::GPU_vertbuf_get_format · L265](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-7c66ff8de8245148)。
- `GPU_vertbuf_use` → [blender::GPU_vertbuf_use · L295](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-f2ce61da8df3615a)。
- `GPU_vertbuf_update_sub` → [blender::GPU_vertbuf_update_sub · L315](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-dbb703497ad88d1b)。
- `loose_data.size_in_bytes` → [blender::Span::size_in_bytes · L272](../../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-1369fbdcc037fcaf)。
- `loose_data.data` → [blender::Span::data · L219](../../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-10c5889198935800)。
