# 实现依赖专题：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::draw::get_sculpt_data_format"]:::abstraction
  F1["blender::draw::extract_sculpt_data"]:::compute
  F2["blender::draw::extract_sculpt_data_subdiv"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F0
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
  F["extract_mesh_vbo_sculpt_data.cc实现"]:::compute
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

<a id="f-d3b26d9af7c379ba"></a>

### `blender::draw::get_sculpt_data_format`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc) · L21—L30。

**教学注释版**

<!-- annotated:4be044f3e37e5a -->

```cpp
static const GPUVertFormat &get_sculpt_data_format()
{
  static const GPUVertFormat format = []() {
    GPUVertFormat format{};
    GPU_vertformat_attr_add(&format, "fset", gpu::VertAttrType::UNORM_8_8_8_8);
    GPU_vertformat_attr_add(&format, "msk", gpu::VertAttrType::SFLOAT_32);
    return format;
  }();
  return format;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc · L21—L30</summary>

<!-- original:4be044f3e37e5a:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc:21:30 -->

```cpp
static const GPUVertFormat &get_sculpt_data_format()
{
  static const GPUVertFormat format = []() {
    GPUVertFormat format{};
    GPU_vertformat_attr_add(&format, "fset", gpu::VertAttrType::UNORM_8_8_8_8);
    GPU_vertformat_attr_add(&format, "msk", gpu::VertAttrType::SFLOAT_32);
    return format;
  }();
  return format;
}
```

</details>

**结果出口**

- `return format;`

**继续追踪实现**

- `[]() { GPUVertFormat format{}; GPU_vertformat_attr_add(&format, "fset", gpu::VertAttrType::UNORM_8_8_8_8); GPU_vertformat_attr_add(&format, "msk", gpu::VertAttrType::SFLOAT_32); return format; }` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L23。
- `GPU_vertformat_attr_add` → [blender::GPU_vertformat_attr_add · L389](../../../gpu/intern/gpu_vertex_format.cc.md#f-a36e23f37b97fff4)。

<a id="f-b0ed6732d6b6f6f8"></a>

### `blender::draw::extract_sculpt_data`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc) · L32—L104。

接口参数：

- `const MeshRenderData &mr`

**教学注释版**

<!-- annotated:2e66fef2cebf2d -->

```cpp
gpu::VertBufPtr extract_sculpt_data(const MeshRenderData &mr)
{
  gpu::VertBufPtr vbo = gpu::VertBufPtr(GPU_vertbuf_create_with_format(get_sculpt_data_format()));
  GPU_vertbuf_data_alloc(*vbo, mr.corners_num);

  struct gpuSculptData {
    uchar4 face_set_color;
    float mask;
  };

  MutableSpan vbo_data = vbo->data<gpuSculptData>();

  const int default_face_set = mr.mesh->face_sets_color_default;
  const int face_set_seed = mr.mesh->face_sets_color_seed;
  if (mr.extract_type == MeshExtractType::BMesh) {
    const BMesh &bm = *mr.bm;
    const int mask_offset = CustomData_get_offset_named(
        &mr.bm->vdata, CD_PROP_FLOAT, ".sculpt_mask");
    const int face_set_offset = CustomData_get_offset_named(
        &mr.bm->pdata, CD_PROP_INT32, ".sculpt_face_set");
    threading::parallel_for(IndexRange(bm.totface), 2048, [&](const IndexRange range) {
      for (const int face_index : range) {
        const BMFace &face = *BM_face_at_index(&const_cast<BMesh &>(bm), face_index);
        const IndexRange face_range(BM_elem_index_get(BM_FACE_FIRST_LOOP(&face)), face.len);

        uchar4 face_set_color(UCHAR_MAX);
        if (face_set_offset != -1) {
          const int face_set_id = BM_ELEM_CD_GET_INT(&face, face_set_offset);
          if (face_set_id != default_face_set) {
            BKE_paint_face_set_overlay_color_get(face_set_id, face_set_seed, face_set_color);
          }
        }
        // [讲解] vbo_data.slice：建立原连续范围的子视图。
        vbo_data.slice(face_range).fill(gpuSculptData{face_set_color, 0.0f});

        if (mask_offset != -1) {
          const BMLoop *loop = BM_FACE_FIRST_LOOP(&face);
          for ([[maybe_unused]] const int i : IndexRange(face.len)) {
            const int index = BM_elem_index_get(loop);
            vbo_data[index].mask = BM_ELEM_CD_GET_FLOAT(loop->v, mask_offset);
            loop = loop->next;
          }
        }
      }
    });
  }
  else {
    const OffsetIndices faces = mr.faces;
    const Span<int> corner_verts = mr.corner_verts;
    const bke::AttributeAccessor attributes = mr.mesh->attributes();
    const VArraySpan mask = *attributes.lookup<float>(".sculpt_mask", bke::AttrDomain::Point);
    const VArraySpan face_set = *attributes.lookup<int>(".sculpt_face_set", bke::AttrDomain::Face);
    threading::parallel_for(faces.index_range(), 1024, [&](const IndexRange range) {
      for (const int face_index : range) {
        const IndexRange face = faces[face_index];
        uchar4 face_set_color(UCHAR_MAX);
        if (!face_set.is_empty()) {
          const int face_set_id = face_set[face_index];
          if (face_set_id != default_face_set) {
            BKE_paint_face_set_overlay_color_get(face_set_id, face_set_seed, face_set_color);
          }
        }
        vbo_data.slice(face).fill(gpuSculptData{face_set_color, 0.0f});

        if (!mask.is_empty()) {
          for (const int corner : face) {
            vbo_data[corner].mask = mask[corner_verts[corner]];
          }
        }
      }
    });
  }
  return vbo;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc · L32—L104</summary>

<!-- original:2e66fef2cebf2d:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc:32:104 -->

```cpp
gpu::VertBufPtr extract_sculpt_data(const MeshRenderData &mr)
{
  gpu::VertBufPtr vbo = gpu::VertBufPtr(GPU_vertbuf_create_with_format(get_sculpt_data_format()));
  GPU_vertbuf_data_alloc(*vbo, mr.corners_num);

  struct gpuSculptData {
    uchar4 face_set_color;
    float mask;
  };

  MutableSpan vbo_data = vbo->data<gpuSculptData>();

  const int default_face_set = mr.mesh->face_sets_color_default;
  const int face_set_seed = mr.mesh->face_sets_color_seed;
  if (mr.extract_type == MeshExtractType::BMesh) {
    const BMesh &bm = *mr.bm;
    const int mask_offset = CustomData_get_offset_named(
        &mr.bm->vdata, CD_PROP_FLOAT, ".sculpt_mask");
    const int face_set_offset = CustomData_get_offset_named(
        &mr.bm->pdata, CD_PROP_INT32, ".sculpt_face_set");
    threading::parallel_for(IndexRange(bm.totface), 2048, [&](const IndexRange range) {
      for (const int face_index : range) {
        const BMFace &face = *BM_face_at_index(&const_cast<BMesh &>(bm), face_index);
        const IndexRange face_range(BM_elem_index_get(BM_FACE_FIRST_LOOP(&face)), face.len);

        uchar4 face_set_color(UCHAR_MAX);
        if (face_set_offset != -1) {
          const int face_set_id = BM_ELEM_CD_GET_INT(&face, face_set_offset);
          if (face_set_id != default_face_set) {
            BKE_paint_face_set_overlay_color_get(face_set_id, face_set_seed, face_set_color);
          }
        }
        vbo_data.slice(face_range).fill(gpuSculptData{face_set_color, 0.0f});

        if (mask_offset != -1) {
          const BMLoop *loop = BM_FACE_FIRST_LOOP(&face);
          for ([[maybe_unused]] const int i : IndexRange(face.len)) {
            const int index = BM_elem_index_get(loop);
            vbo_data[index].mask = BM_ELEM_CD_GET_FLOAT(loop->v, mask_offset);
            loop = loop->next;
          }
        }
      }
    });
  }
  else {
    const OffsetIndices faces = mr.faces;
    const Span<int> corner_verts = mr.corner_verts;
    const bke::AttributeAccessor attributes = mr.mesh->attributes();
    const VArraySpan mask = *attributes.lookup<float>(".sculpt_mask", bke::AttrDomain::Point);
    const VArraySpan face_set = *attributes.lookup<int>(".sculpt_face_set", bke::AttrDomain::Face);
    threading::parallel_for(faces.index_range(), 1024, [&](const IndexRange range) {
      for (const int face_index : range) {
        const IndexRange face = faces[face_index];
        uchar4 face_set_color(UCHAR_MAX);
        if (!face_set.is_empty()) {
          const int face_set_id = face_set[face_index];
          if (face_set_id != default_face_set) {
            BKE_paint_face_set_overlay_color_get(face_set_id, face_set_seed, face_set_color);
          }
        }
        vbo_data.slice(face).fill(gpuSculptData{face_set_color, 0.0f});

        if (!mask.is_empty()) {
          for (const int corner : face) {
            vbo_data[corner].mask = mask[corner_verts[corner]];
          }
        }
      }
    });
  }
  return vbo;
}
```

</details>

**沿实际写入检查状态**

- `vbo_data[index].mask = BM_ELEM_CD_GET_FLOAT(loop->v, mask_offset);`
- `loop = loop->next;`
- `vbo_data[corner].mask = mask[corner_verts[corner]];`

**结果出口**

- `return vbo;`

**继续追踪实现**

- `gpu::VertBufPtr` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L34。
- `GPU_vertbuf_create_with_format` → [blender::GPU_vertbuf_create_with_format · L71](../../../gpu/GPU_vertex_buffer.hh.md#f-bd43fe034e852138)。
- `get_sculpt_data_format` → [blender::draw::get_sculpt_data_format · L21](extract_mesh_vbo_sculpt_data.cc.md#f-d3b26d9af7c379ba)。
- `GPU_vertbuf_data_alloc` → [blender::GPU_vertbuf_data_alloc · L172](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-8ee5cf106e0f2b0f)。
- `vbo->data<gpuSculptData>` → [blender::draw::data · L124](../DRW_gpu_wrapper.hh.md#f-dc115dc22e0c9f33)；[blender::draw::data · L129](../DRW_gpu_wrapper.hh.md#f-5f325cb75387045c)。同名重载需按实参类型选择。
- `CustomData_get_offset_named` → [blender::CustomData_get_offset_named · L3398](../../../../02-BKE几何与数据/intern/customdata.cc.md#f-fe199f3da62e9c30)。
- `threading::parallel_for` → [blender::threading::parallel_for · L68](../../../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-838294754c24426c)。
- `IndexRange` → [blender::IndexRange](../../../../01-BLI基础库/BLI_index_range.hh.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](../../../gpu/shader_tool/utils.hh.md#t-82d2bd4ea71c)；[blender::IndexRange](../../../makesdna/DNA_node_types.h.md#t-0448cc889d39)。
- `BM_face_at_index` → [blender::BM_face_at_index · L122](../../../bmesh/intern/bmesh_mesh.hh.md#f-366df62c166d5094)。
- `BM_elem_index_get` → [BM_elem_index_get · L120](../../../bmesh/intern/bmesh_inline.hh.md#m-201981cdc62d)。宏定义由构建条件选择。
- `BM_FACE_FIRST_LOOP` → [BM_FACE_FIRST_LOOP · L697](../../../bmesh/bmesh_class.hh.md#m-c7e10ffb38e6)；[BM_FACE_FIRST_LOOP · L699](../../../bmesh/bmesh_class.hh.md#m-76a054cc4770)。宏定义由构建条件选择。
- `BM_ELEM_CD_GET_INT` → [BM_ELEM_CD_GET_INT · L582](../../../bmesh/bmesh_class.hh.md#m-d722975f4396)。宏定义由构建条件选择。
- `BKE_paint_face_set_overlay_color_get` → [blender::BKE_paint_face_set_overlay_color_get · L2783](../../../../02-BKE几何与数据/intern/paint.cc.md#f-5a0b84737fe7a33f)。
- `vbo_data.slice(face_range).fill` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L64。
- `vbo_data.slice` → [blender::MutableSpan::slice · L579](../../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-6808b4aefbf58808)；[blender::MutableSpan::slice · L587](../../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-c05b010821861e4f)。同名重载需按实参类型选择。
- `BM_ELEM_CD_GET_FLOAT` → [BM_ELEM_CD_GET_FLOAT · L630](../../../bmesh/bmesh_class.hh.md#m-f02a9920f7a0)。宏定义由构建条件选择。
- `mr.mesh->attributes` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L80。
- `attributes.lookup<float>` → [blender::bke::AttributeAccessor::lookup · L401](../../../../02-BKE几何与数据/intern/attribute_access.cc.md#f-4673351b7bb3b651)；[blender::bke::AttributeAccessor::lookup · L585](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-432b90c796a80893)；[blender::bke::AttributeAccessor::lookup · L602](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-a60c1a45b85155d9)；[blender::bke::AttributeAccessor::lookup · L611](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-16ca459803fc30a6)；[blender::bke::AttributeAccessor::lookup · L620](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-403fd8a9d1a16c6d)。同名重载需按实参类型选择。
- `attributes.lookup<int>` → [blender::bke::AttributeAccessor::lookup · L401](../../../../02-BKE几何与数据/intern/attribute_access.cc.md#f-4673351b7bb3b651)；[blender::bke::AttributeAccessor::lookup · L585](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-432b90c796a80893)；[blender::bke::AttributeAccessor::lookup · L602](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-a60c1a45b85155d9)；[blender::bke::AttributeAccessor::lookup · L611](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-16ca459803fc30a6)；[blender::bke::AttributeAccessor::lookup · L620](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-403fd8a9d1a16c6d)。同名重载需按实参类型选择。
- `faces.index_range` → [blender::offset_indices::OffsetIndices::index_range · L77](../../../../../05-几何存储与拓扑映射/02-OffsetIndices完整接口.md#f-19b5ca1456de007d)。
- `face_set.is_empty` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：由接收对象具体类型或运行时策略提供实现。调用位置L87。
- `vbo_data.slice(face).fill` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L93。
- `mask.is_empty` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：由接收对象具体类型或运行时策略提供实现。调用位置L95。

<a id="f-7d41573d2bf828cc"></a>

### `blender::draw::extract_sculpt_data_subdiv`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc) · L106—L185。

接口参数：

- `const MeshRenderData &mr`
- `const DRWSubdivCache &subdiv_cache`

**教学注释版**

<!-- annotated:625cb4702d8fbf -->

```cpp
gpu::VertBufPtr extract_sculpt_data_subdiv(const MeshRenderData &mr,
                                           const DRWSubdivCache &subdiv_cache)
{
  const Mesh &coarse_mesh = *mr.mesh;
  const int subdiv_corners_num = subdiv_cache.num_subdiv_loops;

  /* First, interpolate mask if available. */
  gpu::VertBuf *mask_vbo = nullptr;
  gpu::VertBuf *subdiv_mask_vbo = nullptr;

  const bke::AttributeAccessor attributes = coarse_mesh.attributes();

  if (const VArray mask = *attributes.lookup<float>(".sculpt_mask", bke::AttrDomain::Point)) {
    GPUVertFormat mask_format = {0};
    GPU_vertformat_attr_add(&mask_format, "msk", gpu::VertAttrType::SFLOAT_32);
    const Span<int> corner_verts = coarse_mesh.corner_verts();
    mask_vbo = GPU_vertbuf_calloc();
    GPU_vertbuf_init_with_format(*mask_vbo, mask_format);
    // [讲解] corner_verts.size：查询视图长度或生成对应有效索引区间。
    GPU_vertbuf_data_alloc(*mask_vbo, corner_verts.size());

    MutableSpan mask_vbo_data = mask_vbo->data<float>();
    array_utils::gather(mask, corner_verts, mask_vbo_data);

    subdiv_mask_vbo = GPU_vertbuf_calloc();
    GPU_vertbuf_init_build_on_device(*subdiv_mask_vbo, mask_format, subdiv_corners_num);

    draw_subdiv_interp_custom_data(subdiv_cache, *mask_vbo, *subdiv_mask_vbo, GPU_COMP_F32, 1, 0);
  }

  /* Then, gather face sets. */
  GPUVertFormat face_set_format = {0};
  GPU_vertformat_attr_add(&face_set_format, "msk", gpu::VertAttrType::UNORM_8_8_8_8);

  gpu::VertBuf *face_set_vbo = GPU_vertbuf_calloc();
  GPU_vertbuf_init_with_format(*face_set_vbo, face_set_format);
  GPU_vertbuf_data_alloc(*face_set_vbo, subdiv_corners_num);

  struct gpuFaceSet {
    uchar4 color;
  };

  MutableSpan face_set_vbo_data = face_set_vbo->data<gpuFaceSet>();
  const VArraySpan face_sets = *attributes.lookup<int>(".sculpt_face_set", bke::AttrDomain::Face);
  if (face_sets.is_empty()) {
    // [讲解] face_set_vbo_data.fill：修改已有目标元素，不改变底层容器长度。
    face_set_vbo_data.fill({uchar4{UCHAR_MAX}});
  }
  else {
    const Span<int> subdiv_loop_face_index(subdiv_cache.subdiv_loop_face_index,
                                           subdiv_corners_num);
    const int default_face_set = coarse_mesh.face_sets_color_default;
    const int face_set_seed = coarse_mesh.face_sets_color_seed;
    threading::parallel_for(IndexRange(subdiv_corners_num), 4096, [&](const IndexRange range) {
      for (const int i : range) {
        const int face_index = subdiv_loop_face_index[i];

        uchar4 face_set_color(UCHAR_MAX);
        const int face_set_id = face_sets[face_index];
        /* Skip for the default color face set to render it white. */
        if (face_set_id != default_face_set) {
          BKE_paint_face_set_overlay_color_get(face_set_id, face_set_seed, face_set_color);
        }

        copy_v3_v3_uchar(face_set_vbo_data[i].color, face_set_color);
      }
    });
  }

  /* Finally, interleave mask and face sets. */
  gpu::VertBufPtr vbo = gpu::VertBufPtr(
      GPU_vertbuf_create_on_device(get_sculpt_data_format(), subdiv_corners_num));

  draw_subdiv_build_sculpt_data_buffer(subdiv_cache, subdiv_mask_vbo, face_set_vbo, vbo.get());

  if (mask_vbo) {
    GPU_vertbuf_discard(mask_vbo);
    GPU_vertbuf_discard(subdiv_mask_vbo);
  }
  GPU_vertbuf_discard(face_set_vbo);
  return vbo;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc · L106—L185</summary>

<!-- original:625cb4702d8fbf:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_sculpt_data.cc:106:185 -->

```cpp
gpu::VertBufPtr extract_sculpt_data_subdiv(const MeshRenderData &mr,
                                           const DRWSubdivCache &subdiv_cache)
{
  const Mesh &coarse_mesh = *mr.mesh;
  const int subdiv_corners_num = subdiv_cache.num_subdiv_loops;

  /* First, interpolate mask if available. */
  gpu::VertBuf *mask_vbo = nullptr;
  gpu::VertBuf *subdiv_mask_vbo = nullptr;

  const bke::AttributeAccessor attributes = coarse_mesh.attributes();

  if (const VArray mask = *attributes.lookup<float>(".sculpt_mask", bke::AttrDomain::Point)) {
    GPUVertFormat mask_format = {0};
    GPU_vertformat_attr_add(&mask_format, "msk", gpu::VertAttrType::SFLOAT_32);
    const Span<int> corner_verts = coarse_mesh.corner_verts();
    mask_vbo = GPU_vertbuf_calloc();
    GPU_vertbuf_init_with_format(*mask_vbo, mask_format);
    GPU_vertbuf_data_alloc(*mask_vbo, corner_verts.size());

    MutableSpan mask_vbo_data = mask_vbo->data<float>();
    array_utils::gather(mask, corner_verts, mask_vbo_data);

    subdiv_mask_vbo = GPU_vertbuf_calloc();
    GPU_vertbuf_init_build_on_device(*subdiv_mask_vbo, mask_format, subdiv_corners_num);

    draw_subdiv_interp_custom_data(subdiv_cache, *mask_vbo, *subdiv_mask_vbo, GPU_COMP_F32, 1, 0);
  }

  /* Then, gather face sets. */
  GPUVertFormat face_set_format = {0};
  GPU_vertformat_attr_add(&face_set_format, "msk", gpu::VertAttrType::UNORM_8_8_8_8);

  gpu::VertBuf *face_set_vbo = GPU_vertbuf_calloc();
  GPU_vertbuf_init_with_format(*face_set_vbo, face_set_format);
  GPU_vertbuf_data_alloc(*face_set_vbo, subdiv_corners_num);

  struct gpuFaceSet {
    uchar4 color;
  };

  MutableSpan face_set_vbo_data = face_set_vbo->data<gpuFaceSet>();
  const VArraySpan face_sets = *attributes.lookup<int>(".sculpt_face_set", bke::AttrDomain::Face);
  if (face_sets.is_empty()) {
    face_set_vbo_data.fill({uchar4{UCHAR_MAX}});
  }
  else {
    const Span<int> subdiv_loop_face_index(subdiv_cache.subdiv_loop_face_index,
                                           subdiv_corners_num);
    const int default_face_set = coarse_mesh.face_sets_color_default;
    const int face_set_seed = coarse_mesh.face_sets_color_seed;
    threading::parallel_for(IndexRange(subdiv_corners_num), 4096, [&](const IndexRange range) {
      for (const int i : range) {
        const int face_index = subdiv_loop_face_index[i];

        uchar4 face_set_color(UCHAR_MAX);
        const int face_set_id = face_sets[face_index];
        /* Skip for the default color face set to render it white. */
        if (face_set_id != default_face_set) {
          BKE_paint_face_set_overlay_color_get(face_set_id, face_set_seed, face_set_color);
        }

        copy_v3_v3_uchar(face_set_vbo_data[i].color, face_set_color);
      }
    });
  }

  /* Finally, interleave mask and face sets. */
  gpu::VertBufPtr vbo = gpu::VertBufPtr(
      GPU_vertbuf_create_on_device(get_sculpt_data_format(), subdiv_corners_num));

  draw_subdiv_build_sculpt_data_buffer(subdiv_cache, subdiv_mask_vbo, face_set_vbo, vbo.get());

  if (mask_vbo) {
    GPU_vertbuf_discard(mask_vbo);
    GPU_vertbuf_discard(subdiv_mask_vbo);
  }
  GPU_vertbuf_discard(face_set_vbo);
  return vbo;
}
```

</details>

**沿实际写入检查状态**

- `mask_vbo = GPU_vertbuf_calloc();`
- `subdiv_mask_vbo = GPU_vertbuf_calloc();`

**结果出口**

- `return vbo;`

**继续追踪实现**

- `coarse_mesh.attributes` → [Mesh::attributes · L1298](../../../../../05-几何存储与拓扑映射/03-MPoly迁移与兼容.md#f-607bbfe3e57cfc7f)。
- `attributes.lookup<float>` → [blender::bke::AttributeAccessor::lookup · L401](../../../../02-BKE几何与数据/intern/attribute_access.cc.md#f-4673351b7bb3b651)；[blender::bke::AttributeAccessor::lookup · L585](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-432b90c796a80893)；[blender::bke::AttributeAccessor::lookup · L602](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-a60c1a45b85155d9)；[blender::bke::AttributeAccessor::lookup · L611](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-16ca459803fc30a6)；[blender::bke::AttributeAccessor::lookup · L620](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-403fd8a9d1a16c6d)。同名重载需按实参类型选择。
- `GPU_vertformat_attr_add` → [blender::GPU_vertformat_attr_add · L389](../../../gpu/intern/gpu_vertex_format.cc.md#f-a36e23f37b97fff4)。
- `coarse_mesh.corner_verts` → [Mesh::corner_verts · L1238](../../../../../05-几何存储与拓扑映射/03-MPoly迁移与兼容.md#f-a59c61f583b64bc4)。
- `GPU_vertbuf_calloc` → [blender::GPU_vertbuf_calloc · L112](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-bddd6e0944c513f4)。
- `GPU_vertbuf_init_with_format` → [GPU_vertbuf_init_with_format · L277](../../../gpu/GPU_vertex_buffer.hh.md#m-7100390733f1)。宏定义由构建条件选择。
- `GPU_vertbuf_data_alloc` → [blender::GPU_vertbuf_data_alloc · L172](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-8ee5cf106e0f2b0f)。
- `corner_verts.size` → [blender::Span::size · L256](../../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-5f80fa006089c998)。
- `mask_vbo->data<float>` → [blender::gpu::VertBuf::data · L220](../../../gpu/GPU_vertex_buffer.hh.md#f-e72412fdddda8bf5)。
- `array_utils::gather` → [blender::array_utils::gather · L187](../../../../../01-基础容器与现代CPP/20-容器选择与独立实现.md#f-1760adec5858a42f)；[blender::array_utils::gather · L209](../../../../../01-基础容器与现代CPP/20-容器选择与独立实现.md#f-a9f65820788454bf)；[blender::array_utils::gather · L225](../../../../../01-基础容器与现代CPP/20-容器选择与独立实现.md#f-279764b4196f0b63)；[blender::array_utils::gather · L237](../../../../../01-基础容器与现代CPP/20-容器选择与独立实现.md#f-e310fd489b49341b)；[blender::array_utils::gather · L268](../../../../../01-基础容器与现代CPP/20-容器选择与独立实现.md#f-7b21c29791903615)；[blender::array_utils::gather · L63](../../../../01-BLI基础库/intern/array_utils.cc.md#f-5c2b501b03ddbb1f)；[blender::array_utils::gather · L82](../../../../01-BLI基础库/intern/array_utils.cc.md#f-ea4dd9e673fe81e4)。同名重载需按实参类型选择。
- `GPU_vertbuf_init_build_on_device` → [blender::GPU_vertbuf_init_build_on_device · L131](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-715cf1b164e85ce8)。
- `draw_subdiv_interp_custom_data` → [blender::draw::draw_subdiv_interp_custom_data · L1101](../draw_cache_impl_subdivision.cc.md#f-ceae47d7fb7a30da)。
- `face_set_vbo->data<gpuFaceSet>` → [blender::gpu::VertBuf::data · L220](../../../gpu/GPU_vertex_buffer.hh.md#f-e72412fdddda8bf5)。
- `attributes.lookup<int>` → [blender::bke::AttributeAccessor::lookup · L401](../../../../02-BKE几何与数据/intern/attribute_access.cc.md#f-4673351b7bb3b651)；[blender::bke::AttributeAccessor::lookup · L585](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-432b90c796a80893)；[blender::bke::AttributeAccessor::lookup · L602](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-a60c1a45b85155d9)；[blender::bke::AttributeAccessor::lookup · L611](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-16ca459803fc30a6)；[blender::bke::AttributeAccessor::lookup · L620](../../../../../05-几何存储与拓扑映射/08-AttributeAccessor接口.md#f-403fd8a9d1a16c6d)。同名重载需按实参类型选择。
- `face_sets.is_empty` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：由接收对象具体类型或运行时策略提供实现。调用位置L149。
- `face_set_vbo_data.fill` → [blender::MutableSpan::fill · L523](../../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-8daedd52c727ec26)。
- `threading::parallel_for` → [blender::threading::parallel_for · L68](../../../../../11-Depsgraph与并行任务系统/07-任务池与TBB接入.md#f-838294754c24426c)。
- `IndexRange` → [blender::IndexRange](../../../../01-BLI基础库/BLI_index_range.hh.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](../../../gpu/shader_tool/utils.hh.md#t-82d2bd4ea71c)；[blender::IndexRange](../../../makesdna/DNA_node_types.h.md#t-0448cc889d39)。
- `BKE_paint_face_set_overlay_color_get` → [blender::BKE_paint_face_set_overlay_color_get · L2783](../../../../02-BKE几何与数据/intern/paint.cc.md#f-5a0b84737fe7a33f)。
- `copy_v3_v3_uchar` → [blender::copy_v3_v3_uchar · L85](../../../../01-BLI基础库/intern/math_vector_inline.cc.md#f-5d8d4ac0d4d3489c)。
- `gpu::VertBufPtr` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L174。
- `GPU_vertbuf_create_on_device` → [blender::GPU_vertbuf_create_on_device · L137](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-abf244a18691f929)。
- `get_sculpt_data_format` → [blender::draw::get_sculpt_data_format · L21](extract_mesh_vbo_sculpt_data.cc.md#f-d3b26d9af7c379ba)。
- `draw_subdiv_build_sculpt_data_buffer` → [blender::draw::draw_subdiv_build_sculpt_data_buffer · L1166](../draw_cache_impl_subdivision.cc.md#f-e66d469365c43ab8)。
- `vbo.get` → [blender::draw::GSplatEvalCache::get · L545](../draw_cache_impl_gsplat.cc.md#f-3fb704a0b74cb9e4)。
- `GPU_vertbuf_discard` → [blender::GPU_vertbuf_discard · L154](../../../gpu/intern/gpu_vertex_buffer.cc.md#f-05a0c4598ede18a4)。
