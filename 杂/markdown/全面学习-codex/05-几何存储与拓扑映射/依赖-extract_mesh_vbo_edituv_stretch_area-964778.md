# 实现依赖专题：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::draw::area_ratio_get"]:::abstraction
  F1["blender::draw::compute_area_ratio"]:::compute
  F2["blender::draw::extract_edituv_stretch_area"]:::compute
  F3["blender::draw::extract_edituv_stretch_area_subdiv"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F1
  F3 -->|"显式调用"| F1
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
  F["extract_mesh_vbo_edituv_stretch_area.cc实<br/>现"]:::compute
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

<a id="f-7304aabc0e612c66"></a>

### `blender::draw::area_ratio_get`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc](../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc) · L21—L27。

接口参数：

- `float area`
- `float uvarea`

**教学注释版**

<!-- annotated:343fba127e3c05 -->

```cpp
BLI_INLINE float area_ratio_get(float area, float uvarea)
{
  if (area >= FLT_EPSILON && uvarea >= FLT_EPSILON) {
    return uvarea / area;
  }
  return 0.0f;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc · L21—L27</summary>

<!-- original:343fba127e3c05:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc:21:27 -->

```cpp
BLI_INLINE float area_ratio_get(float area, float uvarea)
{
  if (area >= FLT_EPSILON && uvarea >= FLT_EPSILON) {
    return uvarea / area;
  }
  return 0.0f;
}
```

</details>

**结果出口**

- `return uvarea / area;`
- `return 0.0f;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-a94e2bd8cd61aa1f"></a>

### `blender::draw::compute_area_ratio`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc](../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc) · L39—L92。

接口参数：

- `const MeshRenderData &mr`
- `MutableSpan<float> r_area_ratio`

**教学注释版**

<!-- annotated:5c2ab9416746b0 -->

```cpp
static AreaInfo compute_area_ratio(const MeshRenderData &mr, MutableSpan<float> r_area_ratio)
{
  if (mr.extract_type == MeshExtractType::BMesh) {
    const BMesh &bm = *mr.bm;
    const StringRef active_name = mr.mesh->active_uv_map_name();
    const int uv_offset = CustomData_get_offset_named(&bm.ldata, CD_PROP_FLOAT2, active_name);
    return threading::parallel_reduce(
        IndexRange(bm.totface),
        1024,
        AreaInfo{},
        [&](const IndexRange range, AreaInfo info) {
          for (const int face_index : range) {
            const BMFace &face = *BM_face_at_index(&const_cast<BMesh &>(bm), face_index);
            const float area = BM_face_calc_area(&face);
            const float uvarea = BM_face_calc_area_uv(&face, uv_offset);
            info.tot_area += area;
            info.tot_uv_area += uvarea;
            r_area_ratio[face_index] = area_ratio_get(area, uvarea);
          }
          return info;
        },
        [](const AreaInfo &a, const AreaInfo &b) {
          return AreaInfo{a.tot_area + b.tot_area, a.tot_uv_area + b.tot_uv_area};
        });
  }

  const Span<float3> positions = mr.vert_positions;
  const OffsetIndices<int> faces = mr.faces;
  const Span<int> corner_verts = mr.corner_verts;
  const Mesh &mesh = *mr.mesh;
  const bke::AttributeAccessor attributes = mesh.attributes();
  const StringRef name = mesh.active_uv_map_name();
  const VArraySpan uv_map = *attributes.lookup<float2>(name, bke::AttrDomain::Corner);

  return threading::parallel_reduce(
      faces.index_range(),
      1024,
      AreaInfo{},
      [&](const IndexRange range, AreaInfo info) {
        for (const int face_index : range) {
          const IndexRange face = faces[face_index];
          // [讲解] corner_verts.slice：建立原连续范围的子视图。
          const float area = bke::mesh::face_area_calc(positions, corner_verts.slice(face));
          // [讲解] face.start：读取连续区间或分组的边界信息。
          float uvarea = area_poly_v2(reinterpret_cast<const float (*)[2]>(&uv_map[face.start()]),
                                      // [讲解] face.size：读取连续区间或分组的边界信息。
                                      face.size());
          info.tot_area += area;
          info.tot_uv_area += uvarea;
          r_area_ratio[face_index] = area_ratio_get(area, uvarea);
        }
        return info;
      },
      [](const AreaInfo &a, const AreaInfo &b) {
        return AreaInfo{a.tot_area + b.tot_area, a.tot_uv_area + b.tot_uv_area};
      });
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc · L39—L92</summary>

<!-- original:5c2ab9416746b0:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc:39:92 -->

```cpp
static AreaInfo compute_area_ratio(const MeshRenderData &mr, MutableSpan<float> r_area_ratio)
{
  if (mr.extract_type == MeshExtractType::BMesh) {
    const BMesh &bm = *mr.bm;
    const StringRef active_name = mr.mesh->active_uv_map_name();
    const int uv_offset = CustomData_get_offset_named(&bm.ldata, CD_PROP_FLOAT2, active_name);
    return threading::parallel_reduce(
        IndexRange(bm.totface),
        1024,
        AreaInfo{},
        [&](const IndexRange range, AreaInfo info) {
          for (const int face_index : range) {
            const BMFace &face = *BM_face_at_index(&const_cast<BMesh &>(bm), face_index);
            const float area = BM_face_calc_area(&face);
            const float uvarea = BM_face_calc_area_uv(&face, uv_offset);
            info.tot_area += area;
            info.tot_uv_area += uvarea;
            r_area_ratio[face_index] = area_ratio_get(area, uvarea);
          }
          return info;
        },
        [](const AreaInfo &a, const AreaInfo &b) {
          return AreaInfo{a.tot_area + b.tot_area, a.tot_uv_area + b.tot_uv_area};
        });
  }

  const Span<float3> positions = mr.vert_positions;
  const OffsetIndices<int> faces = mr.faces;
  const Span<int> corner_verts = mr.corner_verts;
  const Mesh &mesh = *mr.mesh;
  const bke::AttributeAccessor attributes = mesh.attributes();
  const StringRef name = mesh.active_uv_map_name();
  const VArraySpan uv_map = *attributes.lookup<float2>(name, bke::AttrDomain::Corner);

  return threading::parallel_reduce(
      faces.index_range(),
      1024,
      AreaInfo{},
      [&](const IndexRange range, AreaInfo info) {
        for (const int face_index : range) {
          const IndexRange face = faces[face_index];
          const float area = bke::mesh::face_area_calc(positions, corner_verts.slice(face));
          float uvarea = area_poly_v2(reinterpret_cast<const float (*)[2]>(&uv_map[face.start()]),
                                      face.size());
          info.tot_area += area;
          info.tot_uv_area += uvarea;
          r_area_ratio[face_index] = area_ratio_get(area, uvarea);
        }
        return info;
      },
      [](const AreaInfo &a, const AreaInfo &b) {
        return AreaInfo{a.tot_area + b.tot_area, a.tot_uv_area + b.tot_uv_area};
      });
}
```

</details>

**沿实际写入检查状态**

- `info.tot_area += area;`
- `info.tot_uv_area += uvarea;`
- `r_area_ratio[face_index] = area_ratio_get(area, uvarea);`

**结果出口**

- `return threading::parallel_reduce(`
- `return info;`
- `return AreaInfo{a.tot_area + b.tot_area, a.tot_uv_area + b.tot_uv_area};`

**继续追踪实现**

- `mr.mesh->active_uv_map_name` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L43。
- `CustomData_get_offset_named` → [blender::CustomData_get_offset_named · L3398](%E4%BE%9D%E8%B5%96-customdata-2eef81.md#f-fe199f3da62e9c30)。
- `threading::parallel_reduce` → [blender::threading::parallel_reduce · L126](../11-Depsgraph%E4%B8%8E%E5%B9%B6%E8%A1%8C%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F/07-%E4%BB%BB%E5%8A%A1%E6%B1%A0%E4%B8%8ETBB%E6%8E%A5%E5%85%A5.md#f-9225ddb5efb97fcc)。
- `IndexRange` → [blender::IndexRange](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_index_range-7d7cc5.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](%E4%BE%9D%E8%B5%96-utils-06433d.md#t-82d2bd4ea71c)；[blender::IndexRange](%E4%BE%9D%E8%B5%96-DNA_node_types-6708b9.md#t-0448cc889d39)。
- `BM_face_at_index` → [blender::BM_face_at_index · L122](%E4%BE%9D%E8%B5%96-bmesh_mesh-df20c7.md#f-366df62c166d5094)。
- `BM_face_calc_area` → [blender::BM_face_calc_area · L214](%E4%BE%9D%E8%B5%96-bmesh_polygon-a8ec8c.md#f-68093575f608c8ea)。
- `BM_face_calc_area_uv` → [blender::BM_face_calc_area_uv · L264](%E4%BE%9D%E8%B5%96-bmesh_polygon-a8ec8c.md#f-d0a027e9bb559e5c)。
- `area_ratio_get` → [blender::draw::area_ratio_get · L21](%E4%BE%9D%E8%B5%96-extract_mesh_vbo_edituv_stretch_area-964778.md#f-7304aabc0e612c66)。
- `mesh.attributes` → [Mesh::attributes · L1298](03-MPoly%E8%BF%81%E7%A7%BB%E4%B8%8E%E5%85%BC%E5%AE%B9.md#f-607bbfe3e57cfc7f)。
- `mesh.active_uv_map_name` → [Mesh::active_uv_map_name · L1319](03-MPoly%E8%BF%81%E7%A7%BB%E4%B8%8E%E5%85%BC%E5%AE%B9.md#f-9b4762e851836e79)。
- `attributes.lookup<float2>` → [blender::bke::AttributeAccessor::lookup · L401](%E4%BE%9D%E8%B5%96-attribute_access-bceef3.md#f-4673351b7bb3b651)；[blender::bke::AttributeAccessor::lookup · L585](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-432b90c796a80893)；[blender::bke::AttributeAccessor::lookup · L602](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-a60c1a45b85155d9)；[blender::bke::AttributeAccessor::lookup · L611](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-16ca459803fc30a6)；[blender::bke::AttributeAccessor::lookup · L620](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-403fd8a9d1a16c6d)。同名重载需按实参类型选择。
- `faces.index_range` → [blender::offset_indices::OffsetIndices::index_range · L77](02-OffsetIndices%E5%AE%8C%E6%95%B4%E6%8E%A5%E5%8F%A3.md#f-19b5ca1456de007d)。
- `bke::mesh::face_area_calc` → [blender::bke::mesh::face_area_calc · L67](%E4%BE%9D%E8%B5%96-mesh_evaluate-427cfd.md#f-ce18cacfc44bbb37)。
- `corner_verts.slice` → [blender::Span::slice · L141](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-380a0e8fdcbd53cc)；[blender::Span::slice · L149](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-9b9c15e78dd54eec)。同名重载需按实参类型选择。
- `area_poly_v2` → [blender::area_poly_v2 · L186](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_geom-8d91a3.md#f-10e5cd7992ac6839)。
- `face.start` → [blender::IndexRange::start · L243](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/04-IndexRange%E8%BF%9E%E7%BB%AD%E6%95%B4%E6%95%B0%E5%8C%BA%E9%97%B4.md#f-99d2195bd9cfd1f0)。
- `face.size` → [blender::IndexRange::size · L156](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/04-IndexRange%E8%BF%9E%E7%BB%AD%E6%95%B4%E6%95%B0%E5%8C%BA%E9%97%B4.md#f-05f66c3ebb2fdfec)。

<a id="f-15d681f3e7b6b184"></a>

### `blender::draw::extract_edituv_stretch_area`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc](../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc) · L94—L132。

接口参数：

- `const MeshRenderData &mr`
- `float &tot_area`
- `float &tot_uv_area`

**教学注释版**

<!-- annotated:9e36ee7089e8cb -->

```cpp
gpu::VertBufPtr extract_edituv_stretch_area(const MeshRenderData &mr,
                                            float &tot_area,
                                            float &tot_uv_area)
{
  Array<float> area_ratio(mr.faces_num);
  const AreaInfo info = compute_area_ratio(mr, area_ratio);
  tot_area = info.tot_area;
  tot_uv_area = info.tot_uv_area;

  static const GPUVertFormat format = GPU_vertformat_from_attribute("ratio",
                                                                    gpu::VertAttrType::SFLOAT_32);
  gpu::VertBufPtr vbo = gpu::VertBufPtr(GPU_vertbuf_create_with_format(format));
  GPU_vertbuf_data_alloc(*vbo, mr.corners_num);
  MutableSpan<float> vbo_data = vbo->data<float>();

  // [讲解] area_ratio.as_span：提供数组的借用访问入口。
  const int64_t bytes = area_ratio.as_span().size_in_bytes() + vbo_data.size_in_bytes();
  threading::memory_bandwidth_bound_task(bytes, [&]() {
    if (mr.extract_type == MeshExtractType::BMesh) {
      const BMesh &bm = *mr.bm;
      threading::parallel_for(IndexRange(bm.totface), 2048, [&](const IndexRange range) {
        for (const int face_index : range) {
          const BMFace &face = *BM_face_at_index(&const_cast<BMesh &>(bm), face_index);
          const IndexRange face_range(BM_elem_index_get(BM_FACE_FIRST_LOOP(&face)), face.len);
          // [讲解] vbo_data.slice：建立原连续范围的子视图。
          vbo_data.slice(face_range).fill(area_ratio[face_index]);
        }
      });
    }
    else {
      BLI_assert(mr.extract_type == MeshExtractType::Mesh);
      const OffsetIndices<int> faces = mr.faces;
      threading::parallel_for(faces.index_range(), 2048, [&](const IndexRange range) {
        for (const int face : range) {
          vbo_data.slice(faces[face]).fill(area_ratio[face]);
        }
      });
    }
  });
  return vbo;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc · L94—L132</summary>

<!-- original:9e36ee7089e8cb:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc:94:132 -->

```cpp
gpu::VertBufPtr extract_edituv_stretch_area(const MeshRenderData &mr,
                                            float &tot_area,
                                            float &tot_uv_area)
{
  Array<float> area_ratio(mr.faces_num);
  const AreaInfo info = compute_area_ratio(mr, area_ratio);
  tot_area = info.tot_area;
  tot_uv_area = info.tot_uv_area;

  static const GPUVertFormat format = GPU_vertformat_from_attribute("ratio",
                                                                    gpu::VertAttrType::SFLOAT_32);
  gpu::VertBufPtr vbo = gpu::VertBufPtr(GPU_vertbuf_create_with_format(format));
  GPU_vertbuf_data_alloc(*vbo, mr.corners_num);
  MutableSpan<float> vbo_data = vbo->data<float>();

  const int64_t bytes = area_ratio.as_span().size_in_bytes() + vbo_data.size_in_bytes();
  threading::memory_bandwidth_bound_task(bytes, [&]() {
    if (mr.extract_type == MeshExtractType::BMesh) {
      const BMesh &bm = *mr.bm;
      threading::parallel_for(IndexRange(bm.totface), 2048, [&](const IndexRange range) {
        for (const int face_index : range) {
          const BMFace &face = *BM_face_at_index(&const_cast<BMesh &>(bm), face_index);
          const IndexRange face_range(BM_elem_index_get(BM_FACE_FIRST_LOOP(&face)), face.len);
          vbo_data.slice(face_range).fill(area_ratio[face_index]);
        }
      });
    }
    else {
      BLI_assert(mr.extract_type == MeshExtractType::Mesh);
      const OffsetIndices<int> faces = mr.faces;
      threading::parallel_for(faces.index_range(), 2048, [&](const IndexRange range) {
        for (const int face : range) {
          vbo_data.slice(faces[face]).fill(area_ratio[face]);
        }
      });
    }
  });
  return vbo;
}
```

</details>

**沿实际写入检查状态**

- `tot_area = info.tot_area;`
- `tot_uv_area = info.tot_uv_area;`

**结果出口**

- `return vbo;`

**继续追踪实现**

- `compute_area_ratio` → [blender::draw::compute_area_ratio · L39](%E4%BE%9D%E8%B5%96-extract_mesh_vbo_edituv_stretch_area-964778.md#f-a94e2bd8cd61aa1f)。
- `GPU_vertformat_from_attribute` → [blender::GPU_vertformat_from_attribute · L427](%E4%BE%9D%E8%B5%96-gpu_vertex_format-4f7148.md#f-2643d25087989f8e)。
- `gpu::VertBufPtr` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L105。
- `GPU_vertbuf_create_with_format` → [blender::GPU_vertbuf_create_with_format · L71](%E4%BE%9D%E8%B5%96-GPU_vertex_buffer-d7610b.md#f-bd43fe034e852138)。
- `GPU_vertbuf_data_alloc` → [blender::GPU_vertbuf_data_alloc · L172](%E4%BE%9D%E8%B5%96-gpu_vertex_buffer-eaa662.md#f-8ee5cf106e0f2b0f)。
- `vbo->data<float>` → [blender::draw::data · L124](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-dc115dc22e0c9f33)；[blender::draw::data · L129](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-5f325cb75387045c)。同名重载需按实参类型选择。
- `area_ratio.as_span().size_in_bytes` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L109。
- `area_ratio.as_span` → [blender::Array::as_span · L254](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/08-Array%E5%A4%8D%E5%88%B6%E7%A7%BB%E5%8A%A8%E4%B8%8E%E9%94%80%E6%AF%81.md#f-05fc77056a242032)。
- `vbo_data.size_in_bytes` → [blender::MutableSpan::size_in_bytes · L507](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-2e42823b970a8406)。
- `threading::memory_bandwidth_bound_task` → [blender::threading::memory_bandwidth_bound_task · L250](../11-Depsgraph%E4%B8%8E%E5%B9%B6%E8%A1%8C%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F/07-%E4%BB%BB%E5%8A%A1%E6%B1%A0%E4%B8%8ETBB%E6%8E%A5%E5%85%A5.md#f-aa412ccec656928d)。
- `threading::parallel_for` → [blender::threading::parallel_for · L68](../11-Depsgraph%E4%B8%8E%E5%B9%B6%E8%A1%8C%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F/07-%E4%BB%BB%E5%8A%A1%E6%B1%A0%E4%B8%8ETBB%E6%8E%A5%E5%85%A5.md#f-838294754c24426c)。
- `IndexRange` → [blender::IndexRange](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_index_range-7d7cc5.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](%E4%BE%9D%E8%B5%96-utils-06433d.md#t-82d2bd4ea71c)；[blender::IndexRange](%E4%BE%9D%E8%B5%96-DNA_node_types-6708b9.md#t-0448cc889d39)。
- `BM_face_at_index` → [blender::BM_face_at_index · L122](%E4%BE%9D%E8%B5%96-bmesh_mesh-df20c7.md#f-366df62c166d5094)。
- `BM_elem_index_get` → [BM_elem_index_get · L120](%E4%BE%9D%E8%B5%96-bmesh_inline-74f1be.md#m-201981cdc62d)。宏定义由构建条件选择。
- `BM_FACE_FIRST_LOOP` → [BM_FACE_FIRST_LOOP · L697](%E4%BE%9D%E8%B5%96-bmesh_class-4cf146.md#m-c7e10ffb38e6)；[BM_FACE_FIRST_LOOP · L699](%E4%BE%9D%E8%B5%96-bmesh_class-4cf146.md#m-76a054cc4770)。宏定义由构建条件选择。
- `vbo_data.slice(face_range).fill` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L117。
- `vbo_data.slice` → [blender::MutableSpan::slice · L579](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-6808b4aefbf58808)；[blender::MutableSpan::slice · L587](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-c05b010821861e4f)。同名重载需按实参类型选择。
- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `faces.index_range` → [blender::offset_indices::OffsetIndices::index_range · L77](02-OffsetIndices%E5%AE%8C%E6%95%B4%E6%8E%A5%E5%8F%A3.md#f-19b5ca1456de007d)。
- `vbo_data.slice(faces[face]).fill` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L126。

<a id="f-518b48740fc9e582"></a>

### `blender::draw::extract_edituv_stretch_area_subdiv`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc](../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc) · L134—L156。

接口参数：

- `const MeshRenderData &mr`
- `const DRWSubdivCache &subdiv_cache`
- `float &tot_area`
- `float &tot_uv_area`

**教学注释版**

<!-- annotated:891712a6f8042e -->

```cpp
gpu::VertBufPtr extract_edituv_stretch_area_subdiv(const MeshRenderData &mr,
                                                   const DRWSubdivCache &subdiv_cache,
                                                   float &tot_area,
                                                   float &tot_uv_area)
{
  static const GPUVertFormat format = GPU_vertformat_from_attribute("ratio",
                                                                    gpu::VertAttrType::SFLOAT_32);
  gpu::VertBufPtr vbo = gpu::VertBufPtr(
      GPU_vertbuf_create_on_device(format, subdiv_cache.num_subdiv_loops));

  gpu::VertBuf *coarse_vbo = GPU_vertbuf_calloc();
  GPU_vertbuf_init_with_format(*coarse_vbo, format);
  GPU_vertbuf_data_alloc(*coarse_vbo, mr.faces_num);
  MutableSpan coarse_vbo_data = coarse_vbo->data<float>();
  const AreaInfo info = compute_area_ratio(mr, coarse_vbo_data);
  tot_area = info.tot_area;
  tot_uv_area = info.tot_uv_area;

  draw_subdiv_build_edituv_stretch_area_buffer(subdiv_cache, coarse_vbo, vbo.get());

  GPU_vertbuf_discard(coarse_vbo);
  return vbo;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc · L134—L156</summary>

<!-- original:891712a6f8042e:source/blender/draw/intern/mesh_extractors/extract_mesh_vbo_edituv_stretch_area.cc:134:156 -->

```cpp
gpu::VertBufPtr extract_edituv_stretch_area_subdiv(const MeshRenderData &mr,
                                                   const DRWSubdivCache &subdiv_cache,
                                                   float &tot_area,
                                                   float &tot_uv_area)
{
  static const GPUVertFormat format = GPU_vertformat_from_attribute("ratio",
                                                                    gpu::VertAttrType::SFLOAT_32);
  gpu::VertBufPtr vbo = gpu::VertBufPtr(
      GPU_vertbuf_create_on_device(format, subdiv_cache.num_subdiv_loops));

  gpu::VertBuf *coarse_vbo = GPU_vertbuf_calloc();
  GPU_vertbuf_init_with_format(*coarse_vbo, format);
  GPU_vertbuf_data_alloc(*coarse_vbo, mr.faces_num);
  MutableSpan coarse_vbo_data = coarse_vbo->data<float>();
  const AreaInfo info = compute_area_ratio(mr, coarse_vbo_data);
  tot_area = info.tot_area;
  tot_uv_area = info.tot_uv_area;

  draw_subdiv_build_edituv_stretch_area_buffer(subdiv_cache, coarse_vbo, vbo.get());

  GPU_vertbuf_discard(coarse_vbo);
  return vbo;
}
```

</details>

**沿实际写入检查状态**

- `tot_area = info.tot_area;`
- `tot_uv_area = info.tot_uv_area;`

**结果出口**

- `return vbo;`

**继续追踪实现**

- `GPU_vertformat_from_attribute` → [blender::GPU_vertformat_from_attribute · L427](%E4%BE%9D%E8%B5%96-gpu_vertex_format-4f7148.md#f-2643d25087989f8e)。
- `gpu::VertBufPtr` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L141。
- `GPU_vertbuf_create_on_device` → [blender::GPU_vertbuf_create_on_device · L137](%E4%BE%9D%E8%B5%96-gpu_vertex_buffer-eaa662.md#f-abf244a18691f929)。
- `GPU_vertbuf_calloc` → [blender::GPU_vertbuf_calloc · L112](%E4%BE%9D%E8%B5%96-gpu_vertex_buffer-eaa662.md#f-bddd6e0944c513f4)。
- `GPU_vertbuf_init_with_format` → [GPU_vertbuf_init_with_format · L277](%E4%BE%9D%E8%B5%96-GPU_vertex_buffer-d7610b.md#m-7100390733f1)。宏定义由构建条件选择。
- `GPU_vertbuf_data_alloc` → [blender::GPU_vertbuf_data_alloc · L172](%E4%BE%9D%E8%B5%96-gpu_vertex_buffer-eaa662.md#f-8ee5cf106e0f2b0f)。
- `coarse_vbo->data<float>` → [blender::gpu::VertBuf::data · L220](%E4%BE%9D%E8%B5%96-GPU_vertex_buffer-d7610b.md#f-e72412fdddda8bf5)。
- `compute_area_ratio` → [blender::draw::compute_area_ratio · L39](%E4%BE%9D%E8%B5%96-extract_mesh_vbo_edituv_stretch_area-964778.md#f-a94e2bd8cd61aa1f)。
- `draw_subdiv_build_edituv_stretch_area_buffer` → [blender::draw::draw_subdiv_build_edituv_stretch_area_buffer · L1437](%E4%BE%9D%E8%B5%96-draw_cache_impl_subdivision-33125a.md#f-08a2f541eda625c5)。
- `vbo.get` → [blender::draw::GSplatEvalCache::get · L545](%E4%BE%9D%E8%B5%96-draw_cache_impl_gsplat-0b4128.md#f-3fb704a0b74cb9e4)。
- `GPU_vertbuf_discard` → [blender::GPU_vertbuf_discard · L154](%E4%BE%9D%E8%B5%96-gpu_vertex_buffer-eaa662.md#f-05a0c4598ede18a4)。
