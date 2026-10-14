# 实现依赖专题：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::draw::get_fdots_pos_format"]:::abstraction
  F1["blender::draw::get_fdots_nor_format_subdiv"]:::compute
  F2["blender::draw::extract_face_dot_positions_mesh"]:::compute
  F3["blender::draw::extract_face_dot_positions_bm"]:::compute
  F4["blender::draw::extract_face_dots_position"]:::compute
  F5["blender::draw::extract_face_dots_subdiv"]:::compute
  F4 -->|"显式调用"| F0
  F4 -->|"显式调用"| F2
  F4 -->|"显式调用"| F3
  F5 -->|"显式调用"| F1
  F5 -->|"显式调用"| F0
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
  F["extract_mesh_vbo_fdots_pos.cc实现"]:::compute
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

<a id="f-cf0bed593c42c855"></a>

### `blender::draw::get_fdots_pos_format`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc) · L17—L22。

**教学注释版**

<!-- annotated:f1be566cc99cfe -->

```cpp
static const GPUVertFormat &get_fdots_pos_format()
{
  static const GPUVertFormat format = GPU_vertformat_from_attribute(
      "pos", gpu::VertAttrType::SFLOAT_32_32_32);
  return format;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc · L17—L22</summary>

<!-- original:f1be566cc99cfe:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc:17:22 -->

```cpp
static const GPUVertFormat &get_fdots_pos_format()
{
  static const GPUVertFormat format = GPU_vertformat_from_attribute(
      "pos", gpu::VertAttrType::SFLOAT_32_32_32);
  return format;
}
```

</details>

**结果出口**

- `return format;`

**继续追踪实现**

- `GPU_vertformat_from_attribute` → [blender::GPU_vertformat_from_attribute · L427](../../../gpu/intern/gpu_vertex_format.cc.md#f-2643d25087989f8e)。

<a id="f-e16ee9bcb46ea363"></a>

### `blender::draw::get_fdots_nor_format_subdiv`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc) · L24—L29。

**教学注释版**

<!-- annotated:f5bfd72d3a01ca -->

```cpp
static const GPUVertFormat &get_fdots_nor_format_subdiv()
{
  static const GPUVertFormat format = GPU_vertformat_from_attribute(
      "norAndFlag", gpu::VertAttrType::SFLOAT_32_32_32_32);
  return format;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc · L24—L29</summary>

<!-- original:f5bfd72d3a01ca:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc:24:29 -->

```cpp
static const GPUVertFormat &get_fdots_nor_format_subdiv()
{
  static const GPUVertFormat format = GPU_vertformat_from_attribute(
      "norAndFlag", gpu::VertAttrType::SFLOAT_32_32_32_32);
  return format;
}
```

</details>

**结果出口**

- `return format;`

**继续追踪实现**

- `GPU_vertformat_from_attribute` → [blender::GPU_vertformat_from_attribute · L427](../../../gpu/intern/gpu_vertex_format.cc.md#f-2643d25087989f8e)。

<a id="f-a2e01eda74418d2e"></a>

### `blender::draw::extract_face_dot_positions_mesh`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc) · L31—L60。

接口参数：

- `const MeshRenderData &mr`
- `MutableSpan<float3> vbo_data`

**教学注释版**

<!-- annotated:4756f0aab1cb37 -->

```cpp
static void extract_face_dot_positions_mesh(const MeshRenderData &mr, MutableSpan<float3> vbo_data)
{
  const Span<float3> positions = mr.vert_positions;
  const OffsetIndices faces = mr.faces;
  const Span<int> corner_verts = mr.corner_verts;
  if (mr.use_subsurf_fdots) {
    const BitSpan facedot_tags = mr.mesh->runtime->subsurf_face_dot_tags;
    threading::parallel_for(faces.index_range(), 4096, [&](const IndexRange range) {
      for (const int face : range) {
        // [讲解] corner_verts.slice：建立原连续范围的子视图。
        const Span<int> face_verts = corner_verts.slice(faces[face]);
        // [讲解] face_verts.begin：返回借用范围的地址。
        const int *vert = std::find_if(face_verts.begin(), face_verts.end(), [&](const int vert) {
          return facedot_tags[vert].test();
        });
        // [讲解] face_verts.end：返回借用范围的地址。
        if (vert == face_verts.end()) {
          vbo_data[face] = float3(0);
        }
        else {
          vbo_data[face] = positions[*vert];
        }
      }
    });
  }
  else {
    threading::parallel_for(faces.index_range(), 4096, [&](const IndexRange range) {
      for (const int face : range) {
        vbo_data[face] = bke::mesh::face_center_calc(positions, corner_verts.slice(faces[face]));
      }
    });
  }
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc · L31—L60</summary>

<!-- original:4756f0aab1cb37:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc:31:60 -->

```cpp
static void extract_face_dot_positions_mesh(const MeshRenderData &mr, MutableSpan<float3> vbo_data)
{
  const Span<float3> positions = mr.vert_positions;
  const OffsetIndices faces = mr.faces;
  const Span<int> corner_verts = mr.corner_verts;
  if (mr.use_subsurf_fdots) {
    const BitSpan facedot_tags = mr.mesh->runtime->subsurf_face_dot_tags;
    threading::parallel_for(faces.index_range(), 4096, [&](const IndexRange range) {
      for (const int face : range) {
        const Span<int> face_verts = corner_verts.slice(faces[face]);
        const int *vert = std::find_if(face_verts.begin(), face_verts.end(), [&](const int vert) {
          return facedot_tags[vert].test();
        });
        if (vert == face_verts.end()) {
          vbo_data[face] = float3(0);
        }
        else {
          vbo_data[face] = positions[*vert];
        }
      }
    });
  }
  else {
    threading::parallel_for(faces.index_range(), 4096, [&](const IndexRange range) {
      for (const int face : range) {
        vbo_data[face] = bke::mesh::face_center_calc(positions, corner_verts.slice(faces[face]));
      }
    });
  }
}
```

</details>

**沿实际写入检查状态**

- `vbo_data[face] = float3(0);`
- `vbo_data[face] = positions[*vert];`
- `vbo_data[face] = bke::mesh::face_center_calc(positions, corner_verts.slice(faces[face]));`

**结果出口**

- `return facedot_tags[vert].test();`

**继续追踪实现**

- `threading::parallel_for` → [blender::threading::parallel_for · L68](../../../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-838294754c24426c)。
- `faces.index_range` → [blender::offset_indices::OffsetIndices::index_range · L77](../../../../../05-几何存储与拓扑映射/02-OffsetIndices完整接口.md#f-19b5ca1456de007d)。
- `corner_verts.slice` → [blender::Span::slice · L141](../../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-380a0e8fdcbd53cc)；[blender::Span::slice · L149](../../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-9b9c15e78dd54eec)。同名重载需按实参类型选择。
- `std::find_if` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `face_verts.begin` → [blender::Span::begin · L224](../../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-415883b512284f46)。
- `face_verts.end` → [blender::Span::end · L228](../../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-a7d8b9e494c291a7)。
- `facedot_tags[vert].test` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L42。
- `float3` → [float3 · L641](../../../compositor/algorithms/intern/smaa.cc.md#m-0ea8254cfdb4)。宏定义由构建条件选择。
- `bke::mesh::face_center_calc` → [blender::bke::mesh::face_center_calc · L45](../../../../02-BKE几何与数据/intern/mesh_evaluate.cc.md#f-b983d3456bc87786)。

<a id="f-b914550b985e9d2b"></a>

### `blender::draw::extract_face_dot_positions_bm`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc) · L62—L76。

接口参数：

- `const MeshRenderData &mr`
- `MutableSpan<float3> vbo_data`

**教学注释版**

<!-- annotated:14b5c33ba92b85 -->

```cpp
static void extract_face_dot_positions_bm(const MeshRenderData &mr, MutableSpan<float3> vbo_data)
{
  const BMesh &bm = *mr.bm;
  threading::parallel_for(IndexRange(bm.totface), 2048, [&](const IndexRange range) {
    for (const int face_index : range) {
      const BMFace &face = *BM_face_at_index(&const_cast<BMesh &>(bm), face_index);
      if (mr.bm_vert_coords.is_empty()) {
        BM_face_calc_center_median(&face, vbo_data[face_index]);
      }
      else {
        BM_face_calc_center_median_vcos(&bm, &face, vbo_data[face_index], mr.bm_vert_coords);
      }
    }
  });
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc · L62—L76</summary>

<!-- original:14b5c33ba92b85:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc:62:76 -->

```cpp
static void extract_face_dot_positions_bm(const MeshRenderData &mr, MutableSpan<float3> vbo_data)
{
  const BMesh &bm = *mr.bm;
  threading::parallel_for(IndexRange(bm.totface), 2048, [&](const IndexRange range) {
    for (const int face_index : range) {
      const BMFace &face = *BM_face_at_index(&const_cast<BMesh &>(bm), face_index);
      if (mr.bm_vert_coords.is_empty()) {
        BM_face_calc_center_median(&face, vbo_data[face_index]);
      }
      else {
        BM_face_calc_center_median_vcos(&bm, &face, vbo_data[face_index], mr.bm_vert_coords);
      }
    }
  });
}
```

</details>

**继续追踪实现**

- `threading::parallel_for` → [blender::threading::parallel_for · L68](../../../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-838294754c24426c)。
- `IndexRange` → [blender::IndexRange](../../../../01-BLI基础库/BLI_index_range.hh.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](../../../gpu/shader_tool/utils.hh.md#t-82d2bd4ea71c)；[blender::IndexRange](../../../makesdna/DNA_node_types.h.md#t-0448cc889d39)。
- `BM_face_at_index` → [blender::BM_face_at_index · L122](../../../bmesh/intern/bmesh_mesh.hh.md#f-366df62c166d5094)。
- `mr.bm_vert_coords.is_empty` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L68。
- `BM_face_calc_center_median` → [blender::BM_face_calc_center_median · L655](../../../bmesh/intern/bmesh_polygon.cc.md#f-ca9310cae0d0c57b)。
- `BM_face_calc_center_median_vcos` → [blender::BM_face_calc_center_median_vcos · L1056](../../../bmesh/intern/bmesh_polygon.cc.md#f-0600122e8a2f3696)。

<a id="f-cb47eb2b2020f0c6"></a>

### `blender::draw::extract_face_dots_position`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc) · L78—L90。

接口参数：

- `const MeshRenderData &mr`

**教学注释版**

<!-- annotated:6088727ad598c2 -->

```cpp
gpu::VertBufPtr extract_face_dots_position(const MeshRenderData &mr)
{
  gpu::VertBufPtr vbo = gpu::VertBufPtr(GPU_vertbuf_create_with_format(get_fdots_pos_format()));
  GPU_vertbuf_data_alloc(*vbo, mr.corners_num + mr.loose_indices_num);
  MutableSpan vbo_data = vbo->data<float3>();
  if (mr.extract_type == MeshExtractType::Mesh) {
    extract_face_dot_positions_mesh(mr, vbo_data);
  }
  else {
    extract_face_dot_positions_bm(mr, vbo_data);
  }
  return vbo;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc · L78—L90</summary>

<!-- original:6088727ad598c2:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc:78:90 -->

```cpp
gpu::VertBufPtr extract_face_dots_position(const MeshRenderData &mr)
{
  gpu::VertBufPtr vbo = gpu::VertBufPtr(GPU_vertbuf_create_with_format(get_fdots_pos_format()));
  GPU_vertbuf_data_alloc(*vbo, mr.corners_num + mr.loose_indices_num);
  MutableSpan vbo_data = vbo->data<float3>();
  if (mr.extract_type == MeshExtractType::Mesh) {
    extract_face_dot_positions_mesh(mr, vbo_data);
  }
  else {
    extract_face_dot_positions_bm(mr, vbo_data);
  }
  return vbo;
}
```

</details>

**结果出口**

- `return vbo;`

**继续追踪实现**

- `gpu::VertBufPtr` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L80。
- `GPU_vertbuf_create_with_format` → [blender::GPU_vertbuf_create_with_format · L71](../../../gpu/GPU_vertex_buffer.hh.md#f-bd43fe034e852138)。
- `get_fdots_pos_format` → [blender::draw::get_fdots_pos_format · L17](extract_mesh_vbo_fdots_pos.cc.md#f-cf0bed593c42c855)。
- `GPU_vertbuf_data_alloc` → [blender::GPU_vertbuf_data_alloc · L172](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-8ee5cf106e0f2b0f)。
- `vbo->data<float3>` → [blender::draw::data · L124](../DRW_gpu_wrapper.hh.md#f-dc115dc22e0c9f33)；[blender::draw::data · L129](../DRW_gpu_wrapper.hh.md#f-5f325cb75387045c)。同名重载需按实参类型选择。
- `extract_face_dot_positions_mesh` → [blender::draw::extract_face_dot_positions_mesh · L31](extract_mesh_vbo_fdots_pos.cc.md#f-a2e01eda74418d2e)。
- `extract_face_dot_positions_bm` → [blender::draw::extract_face_dot_positions_bm · L62](extract_mesh_vbo_fdots_pos.cc.md#f-b914550b985e9d2b)。

<a id="f-c5740533a53688db"></a>

### `blender::draw::extract_face_dots_subdiv`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc) · L92—L108。

接口参数：

- `const DRWSubdivCache &subdiv_cache`
- `gpu::VertBufPtr &fdots_pos`
- `gpu::VertBufPtr *fdots_nor`
- `gpu::IndexBufPtr &fdots`

**教学注释版**

<!-- annotated:976ce43dd3ff5a -->

```cpp
void extract_face_dots_subdiv(const DRWSubdivCache &subdiv_cache,
                              gpu::VertBufPtr &fdots_pos,
                              gpu::VertBufPtr *fdots_nor,
                              gpu::IndexBufPtr &fdots)
{
  /* We "extract" positions, normals, and indices at once. */
  /* The normals may not be requested. */
  if (fdots_nor) {
    *fdots_nor = gpu::VertBufPtr(GPU_vertbuf_create_on_device(get_fdots_nor_format_subdiv(),
                                                              subdiv_cache.num_coarse_faces));
  }
  fdots_pos = gpu::VertBufPtr(
      GPU_vertbuf_create_on_device(get_fdots_pos_format(), subdiv_cache.num_coarse_faces));
  fdots = gpu::IndexBufPtr(GPU_indexbuf_build_on_device(subdiv_cache.num_coarse_faces));
  draw_subdiv_build_fdots_buffers(
      subdiv_cache, fdots_pos.get(), fdots_nor ? fdots_nor->get() : nullptr, fdots.get());
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc · L92—L108</summary>

<!-- original:976ce43dd3ff5a:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_fdots_pos.cc:92:108 -->

```cpp
void extract_face_dots_subdiv(const DRWSubdivCache &subdiv_cache,
                              gpu::VertBufPtr &fdots_pos,
                              gpu::VertBufPtr *fdots_nor,
                              gpu::IndexBufPtr &fdots)
{
  /* We "extract" positions, normals, and indices at once. */
  /* The normals may not be requested. */
  if (fdots_nor) {
    *fdots_nor = gpu::VertBufPtr(GPU_vertbuf_create_on_device(get_fdots_nor_format_subdiv(),
                                                              subdiv_cache.num_coarse_faces));
  }
  fdots_pos = gpu::VertBufPtr(
      GPU_vertbuf_create_on_device(get_fdots_pos_format(), subdiv_cache.num_coarse_faces));
  fdots = gpu::IndexBufPtr(GPU_indexbuf_build_on_device(subdiv_cache.num_coarse_faces));
  draw_subdiv_build_fdots_buffers(
      subdiv_cache, fdots_pos.get(), fdots_nor ? fdots_nor->get() : nullptr, fdots.get());
}
```

</details>

**沿实际写入检查状态**

- `fdots_pos = gpu::VertBufPtr(`
- `fdots = gpu::IndexBufPtr(GPU_indexbuf_build_on_device(subdiv_cache.num_coarse_faces));`

**继续追踪实现**

- `gpu::VertBufPtr` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L100。
- `GPU_vertbuf_create_on_device` → [blender::GPU_vertbuf_create_on_device · L137](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-abf244a18691f929)。
- `get_fdots_nor_format_subdiv` → [blender::draw::get_fdots_nor_format_subdiv · L24](extract_mesh_vbo_fdots_pos.cc.md#f-e16ee9bcb46ea363)。
- `get_fdots_pos_format` → [blender::draw::get_fdots_pos_format · L17](extract_mesh_vbo_fdots_pos.cc.md#f-cf0bed593c42c855)。
- `gpu::IndexBufPtr` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L105。
- `GPU_indexbuf_build_on_device` → [blender::GPU_indexbuf_build_on_device · L83](../../../gpu/intern/gpu_index_buffer.cc.md#f-d79a15f80e7a5700)。
- `draw_subdiv_build_fdots_buffers` → [blender::draw::draw_subdiv_build_fdots_buffers · L1253](../draw_cache_impl_subdivision.cc.md#f-67c5077dd844193f)。
- `fdots_pos.get` → [blender::draw::GSplatEvalCache::get · L545](../draw_cache_impl_gsplat.cc.md#f-3fb704a0b74cb9e4)。
- `fdots_nor->get` → [blender::draw::GSplatEvalCache::get · L545](../draw_cache_impl_gsplat.cc.md#f-3fb704a0b74cb9e4)。
- `fdots.get` → [blender::draw::GSplatEvalCache::get · L545](../draw_cache_impl_gsplat.cc.md#f-3fb704a0b74cb9e4)。
