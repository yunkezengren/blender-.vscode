# 实现依赖专题：source/blender/io/usd/intern/usd_reader_pointinstancer.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::io::usd::USDPointInstancerReader::read_geometry"]:::abstraction
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
  F["usd_reader_pointinstancer.cc实现"]:::compute
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

<a id="f-d9e643c4f8504a40"></a>

### `blender::io::usd::USDPointInstancerReader::read_geometry`

实现位置：[source/blender/io/usd/intern/usd_reader_pointinstancer.cc](../../../../../source/blender/io/usd/intern/usd_reader_pointinstancer.cc) · L49—L156。

接口参数：

- `bke::GeometrySet &geometry_set`
- `USDMeshReadParams params`
- `const char **`

**教学注释版**

<!-- annotated:f7337c00ac8d28 -->

```cpp
void USDPointInstancerReader::read_geometry(bke::GeometrySet &geometry_set,
                                            USDMeshReadParams params,
                                            const char ** /*r_err_str*/)
{
  pxr::VtArray<pxr::GfVec3f> usd_positions;
  pxr::VtArray<pxr::GfVec3f> usd_scales;
  pxr::VtArray<pxr::GfQuath> usd_orientations;
  pxr::VtInt64Array usd_ids;
  pxr::VtArray<int> usd_proto_indices;
  std::vector<bool> usd_mask = point_instancer_prim_.ComputeMaskAtTime(params.motion_sample_time);

  point_instancer_prim_.GetPositionsAttr().Get(&usd_positions, params.motion_sample_time);
  point_instancer_prim_.GetScalesAttr().Get(&usd_scales, params.motion_sample_time);
  point_instancer_prim_.GetOrientationsAttr().Get(&usd_orientations, params.motion_sample_time);
  point_instancer_prim_.GetIdsAttr().Get(&usd_ids, params.motion_sample_time);
  point_instancer_prim_.GetProtoIndicesAttr().Get(&usd_proto_indices, params.motion_sample_time);

  PointCloud *pointcloud = geometry_set.get_pointcloud_for_write();
  if (pointcloud->totpoint != usd_positions.size()) {
    /* Size changed so we must reallocate. */
    pointcloud = BKE_pointcloud_new_nomain(PointCloudType::Points, usd_positions.size());
  }

  MutableSpan<float3> point_positions = pointcloud->positions_for_write();
  // [讲解] point_positions.copy_from：修改已有目标元素，不改变底层容器长度。
  point_positions.copy_from(Span(usd_positions.cdata(), usd_positions.size()).cast<float3>());

  bke::MutableAttributeAccessor attributes = pointcloud->attributes_for_write();

  bke::SpanAttributeWriter<float3> scales_attribute =
      attributes.lookup_or_add_for_write_only_span<float3>("scale", bke::AttrDomain::Point);

  /* Here and below, handle the case where instancing attributes are empty or
   * not of the expected size. */
  if (usd_scales.size() < usd_positions.size()) {
    scales_attribute.span.fill(float3(1.0f));
  }

  Span<pxr::GfVec3f> scales = Span(usd_scales.cdata(), usd_scales.size());
  // [讲解] std::min：按比较关系选取较小值；截断范围时还需先满足非负和可表示范围，min本身不会证明边界安全。
  for (const int i : IndexRange(std::min(usd_scales.size(), usd_positions.size()))) {
    scales_attribute.span[i] = float3(scales[i][0], scales[i][1], scales[i][2]);
  }

  scales_attribute.finish();

  bke::SpanAttributeWriter<math::Quaternion> orientations_attribute =
      attributes.lookup_or_add_for_write_only_span<math::Quaternion>("orientation",
                                                                     bke::AttrDomain::Point);

  if (usd_orientations.size() < usd_positions.size()) {
    orientations_attribute.span.fill(math::Quaternion::identity());
  }

  Span<pxr::GfQuath> orientations = Span(usd_orientations.cdata(), usd_orientations.size());
  for (const int i : IndexRange(std::min(usd_orientations.size(), usd_positions.size()))) {
    orientations_attribute.span[i] = math::Quaternion(orientations[i].GetReal(),
                                                      orientations[i].GetImaginary()[0],
                                                      orientations[i].GetImaginary()[1],
                                                      orientations[i].GetImaginary()[2]);
  }

  orientations_attribute.finish();

  if (!usd_ids.empty()) {
    bke::SpanAttributeWriter<int> ids_attribute =
        attributes.lookup_or_add_for_write_only_span<int>("id", bke::AttrDomain::Point);

    const Span<int64_t> usd_data(usd_ids.cdata(), usd_ids.size());
    // [讲解] usd_data.size：查询视图长度或生成对应有效索引区间。
    if (usd_data.size() < ids_attribute.span.size()) {
      ids_attribute.span.fill(0);
    }

    for (const int i : IndexRange(std::min(usd_data.size(), ids_attribute.span.size()))) {
      /* Blender only supports int ID attributes so we have to narrow the value. */
      ids_attribute.span[i] = int(usd_data[i]);
    }

    ids_attribute.finish();
  }

  bke::SpanAttributeWriter<int> proto_indices_attribute =
      attributes.lookup_or_add_for_write_only_span<int>("proto_index", bke::AttrDomain::Point);

  if (usd_proto_indices.size() < usd_positions.size()) {
    proto_indices_attribute.span.fill(0);
  }

  Span<int> proto_indices = Span(usd_proto_indices.cdata(), usd_proto_indices.size());
  for (const int i : IndexRange(std::min(usd_proto_indices.size(), usd_positions.size()))) {
    proto_indices_attribute.span[i] = proto_indices[i];
  }

  proto_indices_attribute.finish();

  bke::SpanAttributeWriter<bool> mask_attribute =
      attributes.lookup_or_add_for_write_only_span<bool>("mask", bke::AttrDomain::Point);

  if (usd_mask.size() < usd_positions.size()) {
    mask_attribute.span.fill(true);
  }

  for (const int i : IndexRange(std::min(usd_mask.size(), usd_positions.size()))) {
    mask_attribute.span[i] = usd_mask[i];
  }

  mask_attribute.finish();

  geometry_set.replace_pointcloud(pointcloud);
}
```

<details>
<summary>核对原始源码：source/blender/io/usd/intern/usd_reader_pointinstancer.cc · L49—L156</summary>

<!-- original:f7337c00ac8d28:source/blender/io/usd/intern/usd_reader_pointinstancer.cc:49:156 -->

```cpp
void USDPointInstancerReader::read_geometry(bke::GeometrySet &geometry_set,
                                            USDMeshReadParams params,
                                            const char ** /*r_err_str*/)
{
  pxr::VtArray<pxr::GfVec3f> usd_positions;
  pxr::VtArray<pxr::GfVec3f> usd_scales;
  pxr::VtArray<pxr::GfQuath> usd_orientations;
  pxr::VtInt64Array usd_ids;
  pxr::VtArray<int> usd_proto_indices;
  std::vector<bool> usd_mask = point_instancer_prim_.ComputeMaskAtTime(params.motion_sample_time);

  point_instancer_prim_.GetPositionsAttr().Get(&usd_positions, params.motion_sample_time);
  point_instancer_prim_.GetScalesAttr().Get(&usd_scales, params.motion_sample_time);
  point_instancer_prim_.GetOrientationsAttr().Get(&usd_orientations, params.motion_sample_time);
  point_instancer_prim_.GetIdsAttr().Get(&usd_ids, params.motion_sample_time);
  point_instancer_prim_.GetProtoIndicesAttr().Get(&usd_proto_indices, params.motion_sample_time);

  PointCloud *pointcloud = geometry_set.get_pointcloud_for_write();
  if (pointcloud->totpoint != usd_positions.size()) {
    /* Size changed so we must reallocate. */
    pointcloud = BKE_pointcloud_new_nomain(PointCloudType::Points, usd_positions.size());
  }

  MutableSpan<float3> point_positions = pointcloud->positions_for_write();
  point_positions.copy_from(Span(usd_positions.cdata(), usd_positions.size()).cast<float3>());

  bke::MutableAttributeAccessor attributes = pointcloud->attributes_for_write();

  bke::SpanAttributeWriter<float3> scales_attribute =
      attributes.lookup_or_add_for_write_only_span<float3>("scale", bke::AttrDomain::Point);

  /* Here and below, handle the case where instancing attributes are empty or
   * not of the expected size. */
  if (usd_scales.size() < usd_positions.size()) {
    scales_attribute.span.fill(float3(1.0f));
  }

  Span<pxr::GfVec3f> scales = Span(usd_scales.cdata(), usd_scales.size());
  for (const int i : IndexRange(std::min(usd_scales.size(), usd_positions.size()))) {
    scales_attribute.span[i] = float3(scales[i][0], scales[i][1], scales[i][2]);
  }

  scales_attribute.finish();

  bke::SpanAttributeWriter<math::Quaternion> orientations_attribute =
      attributes.lookup_or_add_for_write_only_span<math::Quaternion>("orientation",
                                                                     bke::AttrDomain::Point);

  if (usd_orientations.size() < usd_positions.size()) {
    orientations_attribute.span.fill(math::Quaternion::identity());
  }

  Span<pxr::GfQuath> orientations = Span(usd_orientations.cdata(), usd_orientations.size());
  for (const int i : IndexRange(std::min(usd_orientations.size(), usd_positions.size()))) {
    orientations_attribute.span[i] = math::Quaternion(orientations[i].GetReal(),
                                                      orientations[i].GetImaginary()[0],
                                                      orientations[i].GetImaginary()[1],
                                                      orientations[i].GetImaginary()[2]);
  }

  orientations_attribute.finish();

  if (!usd_ids.empty()) {
    bke::SpanAttributeWriter<int> ids_attribute =
        attributes.lookup_or_add_for_write_only_span<int>("id", bke::AttrDomain::Point);

    const Span<int64_t> usd_data(usd_ids.cdata(), usd_ids.size());
    if (usd_data.size() < ids_attribute.span.size()) {
      ids_attribute.span.fill(0);
    }

    for (const int i : IndexRange(std::min(usd_data.size(), ids_attribute.span.size()))) {
      /* Blender only supports int ID attributes so we have to narrow the value. */
      ids_attribute.span[i] = int(usd_data[i]);
    }

    ids_attribute.finish();
  }

  bke::SpanAttributeWriter<int> proto_indices_attribute =
      attributes.lookup_or_add_for_write_only_span<int>("proto_index", bke::AttrDomain::Point);

  if (usd_proto_indices.size() < usd_positions.size()) {
    proto_indices_attribute.span.fill(0);
  }

  Span<int> proto_indices = Span(usd_proto_indices.cdata(), usd_proto_indices.size());
  for (const int i : IndexRange(std::min(usd_proto_indices.size(), usd_positions.size()))) {
    proto_indices_attribute.span[i] = proto_indices[i];
  }

  proto_indices_attribute.finish();

  bke::SpanAttributeWriter<bool> mask_attribute =
      attributes.lookup_or_add_for_write_only_span<bool>("mask", bke::AttrDomain::Point);

  if (usd_mask.size() < usd_positions.size()) {
    mask_attribute.span.fill(true);
  }

  for (const int i : IndexRange(std::min(usd_mask.size(), usd_positions.size()))) {
    mask_attribute.span[i] = usd_mask[i];
  }

  mask_attribute.finish();

  geometry_set.replace_pointcloud(pointcloud);
}
```

</details>

**沿实际写入检查状态**

- `pointcloud = BKE_pointcloud_new_nomain(PointCloudType::Points, usd_positions.size());`
- `scales_attribute.span[i] = float3(scales[i][0], scales[i][1], scales[i][2]);`
- `orientations_attribute.span[i] = math::Quaternion(orientations[i].GetReal(),`
- `ids_attribute.span[i] = int(usd_data[i]);`
- `proto_indices_attribute.span[i] = proto_indices[i];`
- `mask_attribute.span[i] = usd_mask[i];`

**继续追踪实现**

- `point_instancer_prim_.ComputeMaskAtTime` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L58。
- `point_instancer_prim_.GetPositionsAttr().Get` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L60。
- `point_instancer_prim_.GetPositionsAttr` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L60。
- `point_instancer_prim_.GetScalesAttr().Get` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L61。
- `point_instancer_prim_.GetScalesAttr` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L61。
- `point_instancer_prim_.GetOrientationsAttr().Get` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L62。
- `point_instancer_prim_.GetOrientationsAttr` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L62。
- `point_instancer_prim_.GetIdsAttr().Get` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L63。
- `point_instancer_prim_.GetIdsAttr` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L63。
- `point_instancer_prim_.GetProtoIndicesAttr().Get` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L64。
- `point_instancer_prim_.GetProtoIndicesAttr` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L64。
- `geometry_set.get_pointcloud_for_write` → [blender::bke::GeometrySet::get_pointcloud_for_write · L568](../06-%E9%9A%90%E5%BC%8F%E5%85%B1%E4%BA%AB%E4%B8%8E%E7%BC%93%E5%AD%98%E7%B3%BB%E7%BB%9F/05-GeometrySet%E8%AF%BB%E5%86%99%E4%B8%8E%E5%A4%8D%E5%88%B6.md#f-eae41fb2ed3be0d5)。
- `usd_positions.size` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L67。
- `BKE_pointcloud_new_nomain` → [blender::BKE_pointcloud_new_nomain · L228](%E4%BE%9D%E8%B5%96-pointcloud-49a366.md#f-8ee0d698049c08aa)。
- `pointcloud->positions_for_write` → [blender::PointCloud::positions_for_write · L204](%E4%BE%9D%E8%B5%96-pointcloud-49a366.md#f-638cb4413ae404ef)。
- `point_positions.copy_from` → [blender::MutableSpan::copy_from · L745](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-e4f099b1497adddb)。
- `Span(usd_positions.cdata(), usd_positions.size()).cast<float3>` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L73。
- `Span` → [blender::Span](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_span-6aa95f.md#t-8765a8e0c1d5)；[blender::Span](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_index_range-7d7cc5.md#t-86091874a1c0)；[blender::Span](%E4%BE%9D%E8%B5%96-DNA_pointcloud_types-cfb82c.md#t-112aa6ed842c)；[blender::Span](%E4%BE%9D%E8%B5%96-DNA_node_types-6708b9.md#t-49ec6fbb9b69)；[blender::Span](%E4%BE%9D%E8%B5%96-DNA_mesh_types-81f02e.md#t-184fd48fb638)；[blender::Span](%E4%BE%9D%E8%B5%96-DNA_anim_types-39c5d9.md#t-d841071994c2)；[blender::Span](%E4%BE%9D%E8%B5%96-RNA_path_fwd-79c989.md#t-4dbb08969e41)。
- `usd_positions.cdata` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L73。
- `pointcloud->attributes_for_write` → [blender::PointCloud::attributes_for_write · L312](%E4%BE%9D%E8%B5%96-pointcloud-49a366.md#f-308c3c12507fb7fb)。
- `attributes.lookup_or_add_for_write_only_span<float3>` → [blender::bke::MutableAttributeAccessor::lookup_or_add_for_write_only_span · L546](%E4%BE%9D%E8%B5%96-attribute_access-bceef3.md#f-97af899f7983a038)；[blender::bke::MutableAttributeAccessor::lookup_or_add_for_write_only_span · L891](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-ee8d09f75408ac4f)。同名重载需按实参类型选择。
- `usd_scales.size` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L82。
- `scales_attribute.span.fill` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L83。
- `float3` → [float3 · L641](%E4%BE%9D%E8%B5%96-smaa-b67bc2.md#m-0ea8254cfdb4)。宏定义由构建条件选择。
- `usd_scales.cdata` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L86。
- `IndexRange` → [blender::IndexRange](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_index_range-7d7cc5.md#t-caa3466d6776)；[blender::gpu::shader::parser::IndexRange](%E4%BE%9D%E8%B5%96-utils-06433d.md#t-82d2bd4ea71c)；[blender::IndexRange](%E4%BE%9D%E8%B5%96-DNA_node_types-6708b9.md#t-0448cc889d39)。
- `std::min` → [外部契约](https://eel.is/c++draft/alg.min.max)：按比较关系选取较小值；截断范围时还需先满足非负和可表示范围，min本身不会证明边界安全。
- `scales_attribute.finish` → [blender::bke::SpanAttributeWriter::finish · L279](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-585970a3b1bd4da4)。
- `attributes.lookup_or_add_for_write_only_span<math::Quaternion>` → [blender::bke::MutableAttributeAccessor::lookup_or_add_for_write_only_span · L546](%E4%BE%9D%E8%B5%96-attribute_access-bceef3.md#f-97af899f7983a038)；[blender::bke::MutableAttributeAccessor::lookup_or_add_for_write_only_span · L891](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-ee8d09f75408ac4f)。同名重载需按实参类型选择。
- `usd_orientations.size` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L97。
- `orientations_attribute.span.fill` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L98。
- `math::Quaternion::identity` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L98。
- `usd_orientations.cdata` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L101。
- `math::Quaternion` → [Quaternion · L9](%E4%BE%9D%E8%B5%96-types_quaternion-4c3c66.md#f-ce6dc5cf05b52aa4)。
- `orientations[i].GetReal` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L103。
- `orientations[i].GetImaginary` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L104。
- `orientations_attribute.finish` → [blender::bke::SpanAttributeWriter::finish · L279](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-585970a3b1bd4da4)。
- `usd_ids.empty` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L111。
- `attributes.lookup_or_add_for_write_only_span<int>` → [blender::bke::MutableAttributeAccessor::lookup_or_add_for_write_only_span · L546](%E4%BE%9D%E8%B5%96-attribute_access-bceef3.md#f-97af899f7983a038)；[blender::bke::MutableAttributeAccessor::lookup_or_add_for_write_only_span · L891](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-ee8d09f75408ac4f)。同名重载需按实参类型选择。
- `usd_ids.cdata` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L115。
- `usd_ids.size` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L115。
- `usd_data.size` → [blender::Span::size · L256](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-5f80fa006089c998)。
- `ids_attribute.span.size` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L116。
- `ids_attribute.span.fill` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L117。
- `ids_attribute.finish` → [blender::bke::SpanAttributeWriter::finish · L279](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-585970a3b1bd4da4)。
- `usd_proto_indices.size` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L131。
- `proto_indices_attribute.span.fill` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L132。
- `usd_proto_indices.cdata` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L135。
- `proto_indices_attribute.finish` → [blender::bke::SpanAttributeWriter::finish · L279](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-585970a3b1bd4da4)。
- `attributes.lookup_or_add_for_write_only_span<bool>` → [blender::bke::MutableAttributeAccessor::lookup_or_add_for_write_only_span · L546](%E4%BE%9D%E8%B5%96-attribute_access-bceef3.md#f-97af899f7983a038)；[blender::bke::MutableAttributeAccessor::lookup_or_add_for_write_only_span · L891](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-ee8d09f75408ac4f)。同名重载需按实参类型选择。
- `usd_mask.size` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `mask_attribute.span.fill` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L146。
- `mask_attribute.finish` → [blender::bke::SpanAttributeWriter::finish · L279](08-AttributeAccessor%E6%8E%A5%E5%8F%A3.md#f-585970a3b1bd4da4)。
- `geometry_set.replace_pointcloud` → [blender::bke::GeometrySet::replace_pointcloud · L519](../06-%E9%9A%90%E5%BC%8F%E5%85%B1%E4%BA%AB%E4%B8%8E%E7%BC%93%E5%AD%98%E7%B3%BB%E7%BB%9F/05-GeometrySet%E8%AF%BB%E5%86%99%E4%B8%8E%E5%A4%8D%E5%88%B6.md#f-02414356dff40c94)。
