# 实现依赖专题：source/blender/draw/intern/draw_manager.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::draw::Manager::hold_texture"]:::abstraction
  F1["blender::draw::Manager::unique_handle"]:::compute
  F2["blender::draw::Manager::resource_handle"]:::compute
  F3["blender::draw::Manager::resource_handle"]:::compute
  F4["blender::draw::Manager::resource_handle"]:::compute
  F5["blender::draw::Manager::resource_handle"]:::compute
  F1 -->|"显式调用"| F2
  F1 -->|"显式调用"| F3
  F1 -->|"显式调用"| F4
  F1 -->|"显式调用"| F5
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
  F["draw_manager.hh实现"]:::compute
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

<a id="f-e19110d0a07cdd4f"></a>

### `blender::draw::Manager::hold_texture`

实现位置：[source/blender/draw/intern/draw_manager.hh](../../../../../source/blender/draw/intern/draw_manager.hh) · L312—L317。

接口参数：

- `gpu::Texture *texture`

**教学注释版**

<!-- annotated:6f2c0069c1dead -->

```cpp
  void hold_texture(gpu::Texture *texture)
  {
    if (texture != nullptr) {
      // [讲解] acquired_textures.append：在尾部建立新元素，必要时先扩大存储。
      acquired_textures.append(texture);
    }
  }
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_manager.hh · L312—L317</summary>

<!-- original:6f2c0069c1dead:source/blender/draw/intern/draw_manager.hh:312:317 -->

```cpp
  void hold_texture(gpu::Texture *texture)
  {
    if (texture != nullptr) {
      acquired_textures.append(texture);
    }
  }
```

</details>

**继续追踪实现**

- `acquired_textures.append` → [blender::Vector::append · L498](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-591e0b15e6308532)。同名重载需按实参类型选择。

<a id="f-1fe544aeb04550f1"></a>

### `blender::draw::Manager::unique_handle`

实现位置：[source/blender/draw/intern/draw_manager.hh](../../../../../source/blender/draw/intern/draw_manager.hh) · L367—L374。

接口参数：

- `const ObjectRef &ref`

**教学注释版**

<!-- annotated:652abb0378dfb6 -->

```cpp
inline ResourceHandleRange Manager::unique_handle(const ObjectRef &ref)
{
  if (!ref.handle_.is_valid()) {
    /* WORKAROUND: Instead of breaking const correctness everywhere, we only break it for this. */
    const_cast<ObjectRef &>(ref).handle_ = resource_handle(ref);
  }
  return ref.handle_;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_manager.hh · L367—L374</summary>

<!-- original:652abb0378dfb6:source/blender/draw/intern/draw_manager.hh:367:374 -->

```cpp
inline ResourceHandleRange Manager::unique_handle(const ObjectRef &ref)
{
  if (!ref.handle_.is_valid()) {
    /* WORKAROUND: Instead of breaking const correctness everywhere, we only break it for this. */
    const_cast<ObjectRef &>(ref).handle_ = resource_handle(ref);
  }
  return ref.handle_;
}
```

</details>

**结果出口**

- `return ref.handle_;`

**继续追踪实现**

- `ref.handle_.is_valid` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L369。
- `resource_handle` → [blender::draw::Manager::resource_handle · L376](%E4%BE%9D%E8%B5%96-draw_manager-326828.md#f-25cb1d2fc5038904)；[blender::draw::Manager::resource_handle · L419](%E4%BE%9D%E8%B5%96-draw_manager-326828.md#f-f4b6ee05df47f9fc)；[blender::draw::Manager::resource_handle · L448](%E4%BE%9D%E8%B5%96-draw_manager-326828.md#f-628b4cb9549be51b)；[blender::draw::Manager::resource_handle · L456](%E4%BE%9D%E8%B5%96-draw_manager-326828.md#f-d13903e016fd9dd4)。同名重载需按实参类型选择。

<a id="f-25cb1d2fc5038904"></a>

### `blender::draw::Manager::resource_handle`

实现位置：[source/blender/draw/intern/draw_manager.hh](../../../../../source/blender/draw/intern/draw_manager.hh) · L376—L417。

接口参数：

- `const ObjectRef &ref`
- `float inflate_bounds`

**教学注释版**

<!-- annotated:9f2fcc5abafcd3 -->

```cpp
inline ResourceHandleRange Manager::resource_handle(const ObjectRef &ref, float inflate_bounds)
{
  bool is_active_object = ref.is_active(object_active);
  bool is_active_edit_mode = object_active &&
                             (DRW_object_is_in_edit_mode(object_active) ||
                              ELEM(object_active->mode, OB_MODE_TEXTURE_PAINT, OB_MODE_SCULPT)) &&
                             ref.object->mode == object_active->mode;
  if (ref.duplis_) {
    uint start = resource_len_;

    ObjectBounds proto_bounds;
    proto_bounds.sync(*ref.object, inflate_bounds);

    ObjectInfos proto_info;
    proto_info.sync(ref, is_active_object, is_active_edit_mode);

    for (const DupliObject *dupli : *ref.duplis_) {
      const float4x4 dupli_mat(dupli->mat);
      matrix_buf.current().get_or_resize(resource_len_).sync(dupli_mat);
      bounds_buf.current().get_or_resize(resource_len_) = proto_bounds;

      ObjectInfos &info = infos_buf.current().get_or_resize(resource_len_);
      info = proto_info;
      info.random = dupli->random_id * (1.0f / float(0xFFFFFFFF));
      /* Normal offset is scaled by world transform, so it must be computed per instance. */
      info.shadow_terminator_normal_offset = shadow_terminator_normal_offset_get(*ref.object,
                                                                                 dupli_mat);

      resource_len_++;
    }
    return ResourceHandleRange(ResourceHandle(start, (ref.object->transflag & OB_NEG_SCALE) != 0),
                               resource_len_ - start);
  }
  else {
    matrix_buf.current().get_or_resize(resource_len_).sync(*ref.object);
    bounds_buf.current().get_or_resize(resource_len_).sync(*ref.object, inflate_bounds);
    infos_buf.current()
        .get_or_resize(resource_len_)
        .sync(ref, is_active_object, is_active_edit_mode);
    return ResourceHandle(resource_len_++, (ref.object->transflag & OB_NEG_SCALE) != 0);
  }
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_manager.hh · L376—L417</summary>

<!-- original:9f2fcc5abafcd3:source/blender/draw/intern/draw_manager.hh:376:417 -->

```cpp
inline ResourceHandleRange Manager::resource_handle(const ObjectRef &ref, float inflate_bounds)
{
  bool is_active_object = ref.is_active(object_active);
  bool is_active_edit_mode = object_active &&
                             (DRW_object_is_in_edit_mode(object_active) ||
                              ELEM(object_active->mode, OB_MODE_TEXTURE_PAINT, OB_MODE_SCULPT)) &&
                             ref.object->mode == object_active->mode;
  if (ref.duplis_) {
    uint start = resource_len_;

    ObjectBounds proto_bounds;
    proto_bounds.sync(*ref.object, inflate_bounds);

    ObjectInfos proto_info;
    proto_info.sync(ref, is_active_object, is_active_edit_mode);

    for (const DupliObject *dupli : *ref.duplis_) {
      const float4x4 dupli_mat(dupli->mat);
      matrix_buf.current().get_or_resize(resource_len_).sync(dupli_mat);
      bounds_buf.current().get_or_resize(resource_len_) = proto_bounds;

      ObjectInfos &info = infos_buf.current().get_or_resize(resource_len_);
      info = proto_info;
      info.random = dupli->random_id * (1.0f / float(0xFFFFFFFF));
      /* Normal offset is scaled by world transform, so it must be computed per instance. */
      info.shadow_terminator_normal_offset = shadow_terminator_normal_offset_get(*ref.object,
                                                                                 dupli_mat);

      resource_len_++;
    }
    return ResourceHandleRange(ResourceHandle(start, (ref.object->transflag & OB_NEG_SCALE) != 0),
                               resource_len_ - start);
  }
  else {
    matrix_buf.current().get_or_resize(resource_len_).sync(*ref.object);
    bounds_buf.current().get_or_resize(resource_len_).sync(*ref.object, inflate_bounds);
    infos_buf.current()
        .get_or_resize(resource_len_)
        .sync(ref, is_active_object, is_active_edit_mode);
    return ResourceHandle(resource_len_++, (ref.object->transflag & OB_NEG_SCALE) != 0);
  }
}
```

</details>

**沿实际写入检查状态**

- `info = proto_info;`
- `info.random = dupli->random_id * (1.0f / float(0xFFFFFFFF));`
- `info.shadow_terminator_normal_offset = shadow_terminator_normal_offset_get(*ref.object,`

**结果出口**

- `return ResourceHandleRange(ResourceHandle(start, (ref.object->transflag & OB_NEG_SCALE) != 0),`
- `return ResourceHandle(resource_len_++, (ref.object->transflag & OB_NEG_SCALE) != 0);`

**继续追踪实现**

- `ref.is_active` → [blender::draw::ObjectRef::is_active · L259](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-bcca4c61d1f23fbf)。
- `DRW_object_is_in_edit_mode` → [blender::DRW_object_is_in_edit_mode · L295](%E4%BE%9D%E8%B5%96-draw_context-58a534.md#f-fd88782141a3f346)。
- `ELEM` → [ELEM · L88](%E4%BE%9D%E8%B5%96-GHOST_utildefines-34b996.md#m-d28724a15928)；[ELEM · L135](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_utildefines-293a0a.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `proto_bounds.sync` → [blender::ObjectBounds::sync · L205](%E4%BE%9D%E8%B5%96-draw_resource-8750fb.md#f-92ea96898b110b99)；[blender::ObjectBounds::sync · L218](%E4%BE%9D%E8%B5%96-draw_resource-8750fb.md#f-5e36e738ecd5ee50)；[blender::ObjectBounds::sync · L251](%E4%BE%9D%E8%B5%96-draw_resource-8750fb.md#f-e3d52259fad47418)。同名重载需按实参类型选择。
- `proto_info.sync` → [blender::ObjectInfos::sync · L75](%E4%BE%9D%E8%B5%96-draw_resource-8750fb.md#f-734d5001a3f7cb7c)；[blender::ObjectInfos::sync · L91](%E4%BE%9D%E8%B5%96-draw_resource-8750fb.md#f-40c3d16ee64e894c)。同名重载需按实参类型选择。
- `matrix_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L394。
- `matrix_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L394。
- `matrix_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `bounds_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L395。
- `bounds_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `infos_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L397。
- `infos_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `shadow_terminator_normal_offset_get` → [blender::shadow_terminator_normal_offset_get · L65](%E4%BE%9D%E8%B5%96-draw_resource-8750fb.md#f-d7d5e711234ec5bd)。
- `ResourceHandleRange` → [blender::draw::ResourceHandleRange::ResourceHandleRange · L164](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-02feab2cde11028f)；[blender::draw::ResourceHandleRange::ResourceHandleRange · L167](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-fb61986e8583d984)；[blender::draw::ResourceHandleRange::ResourceHandleRange · L168](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-dde16b71f5282880)。同名重载需按实参类型选择。
- `ResourceHandle` → [blender::draw::ResourceHandle::ResourceHandle · L121](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-fefeb18e38acb5b1)；[blender::draw::ResourceHandle::ResourceHandle · L122](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-36b02c7ccc4c93ed)；[blender::draw::ResourceHandle::ResourceHandle · L125](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-920cd44f5cc3c6d4)。同名重载需按实参类型选择。
- `bounds_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L411。
- `infos_buf.current() .get_or_resize(resource_len_) .sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L412。
- `infos_buf.current() .get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L412。

<a id="f-f4b6ee05df47f9fc"></a>

### `blender::draw::Manager::resource_handle`

实现位置：[source/blender/draw/intern/draw_manager.hh](../../../../../source/blender/draw/intern/draw_manager.hh) · L419—L446。

接口参数：

- `const ObjectRef &ref`
- `const float4x4 *model_matrix`
- `const float3 *bounds_center`
- `const float3 *bounds_half_extent`

**教学注释版**

<!-- annotated:d15b6e3b182cfa -->

```cpp
inline ResourceHandleRange Manager::resource_handle(const ObjectRef &ref,
                                                    const float4x4 *model_matrix,
                                                    const float3 *bounds_center,
                                                    const float3 *bounds_half_extent)
{
  BLI_assert(!ref.duplis_);
  bool is_active_object = ref.is_active(object_active);
  bool is_active_edit_mode = object_active &&
                             (DRW_object_is_in_edit_mode(object_active) ||
                              ELEM(object_active->mode, OB_MODE_TEXTURE_PAINT, OB_MODE_SCULPT)) &&
                             ref.object->mode == object_active->mode;
  if (model_matrix) {
    matrix_buf.current().get_or_resize(resource_len_).sync(*model_matrix);
  }
  else {
    matrix_buf.current().get_or_resize(resource_len_).sync(*ref.object);
  }
  if (bounds_center && bounds_half_extent) {
    bounds_buf.current().get_or_resize(resource_len_).sync(*bounds_center, *bounds_half_extent);
  }
  else {
    bounds_buf.current().get_or_resize(resource_len_).sync(*ref.object);
  }
  infos_buf.current()
      .get_or_resize(resource_len_)
      .sync(ref, is_active_object, is_active_edit_mode);
  return ResourceHandle(resource_len_++, (ref.object->transflag & OB_NEG_SCALE) != 0);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_manager.hh · L419—L446</summary>

<!-- original:d15b6e3b182cfa:source/blender/draw/intern/draw_manager.hh:419:446 -->

```cpp
inline ResourceHandleRange Manager::resource_handle(const ObjectRef &ref,
                                                    const float4x4 *model_matrix,
                                                    const float3 *bounds_center,
                                                    const float3 *bounds_half_extent)
{
  BLI_assert(!ref.duplis_);
  bool is_active_object = ref.is_active(object_active);
  bool is_active_edit_mode = object_active &&
                             (DRW_object_is_in_edit_mode(object_active) ||
                              ELEM(object_active->mode, OB_MODE_TEXTURE_PAINT, OB_MODE_SCULPT)) &&
                             ref.object->mode == object_active->mode;
  if (model_matrix) {
    matrix_buf.current().get_or_resize(resource_len_).sync(*model_matrix);
  }
  else {
    matrix_buf.current().get_or_resize(resource_len_).sync(*ref.object);
  }
  if (bounds_center && bounds_half_extent) {
    bounds_buf.current().get_or_resize(resource_len_).sync(*bounds_center, *bounds_half_extent);
  }
  else {
    bounds_buf.current().get_or_resize(resource_len_).sync(*ref.object);
  }
  infos_buf.current()
      .get_or_resize(resource_len_)
      .sync(ref, is_active_object, is_active_edit_mode);
  return ResourceHandle(resource_len_++, (ref.object->transflag & OB_NEG_SCALE) != 0);
}
```

</details>

**结果出口**

- `return ResourceHandle(resource_len_++, (ref.object->transflag & OB_NEG_SCALE) != 0);`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `ref.is_active` → [blender::draw::ObjectRef::is_active · L259](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-bcca4c61d1f23fbf)。
- `DRW_object_is_in_edit_mode` → [blender::DRW_object_is_in_edit_mode · L295](%E4%BE%9D%E8%B5%96-draw_context-58a534.md#f-fd88782141a3f346)。
- `ELEM` → [ELEM · L88](%E4%BE%9D%E8%B5%96-GHOST_utildefines-34b996.md#m-d28724a15928)；[ELEM · L135](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_utildefines-293a0a.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `matrix_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L431。
- `matrix_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L431。
- `matrix_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `bounds_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L437。
- `bounds_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L437。
- `bounds_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `infos_buf.current() .get_or_resize(resource_len_) .sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L442。
- `infos_buf.current() .get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L442。
- `infos_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `ResourceHandle` → [blender::draw::ResourceHandle::ResourceHandle · L121](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-fefeb18e38acb5b1)；[blender::draw::ResourceHandle::ResourceHandle · L122](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-36b02c7ccc4c93ed)；[blender::draw::ResourceHandle::ResourceHandle · L125](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-920cd44f5cc3c6d4)。同名重载需按实参类型选择。

<a id="f-628b4cb9549be51b"></a>

### `blender::draw::Manager::resource_handle`

实现位置：[source/blender/draw/intern/draw_manager.hh](../../../../../source/blender/draw/intern/draw_manager.hh) · L448—L454。

接口参数：

- `const float4x4 &model_matrix`

**教学注释版**

<!-- annotated:c04709f7502dfc -->

```cpp
inline ResourceHandle Manager::resource_handle(const float4x4 &model_matrix)
{
  matrix_buf.current().get_or_resize(resource_len_).sync(model_matrix);
  bounds_buf.current().get_or_resize(resource_len_).sync();
  infos_buf.current().get_or_resize(resource_len_).sync();
  return ResourceHandle(resource_len_++, false);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_manager.hh · L448—L454</summary>

<!-- original:c04709f7502dfc:source/blender/draw/intern/draw_manager.hh:448:454 -->

```cpp
inline ResourceHandle Manager::resource_handle(const float4x4 &model_matrix)
{
  matrix_buf.current().get_or_resize(resource_len_).sync(model_matrix);
  bounds_buf.current().get_or_resize(resource_len_).sync();
  infos_buf.current().get_or_resize(resource_len_).sync();
  return ResourceHandle(resource_len_++, false);
}
```

</details>

**结果出口**

- `return ResourceHandle(resource_len_++, false);`

**继续追踪实现**

- `matrix_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L450。
- `matrix_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L450。
- `matrix_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `bounds_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L451。
- `bounds_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L451。
- `bounds_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `infos_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L452。
- `infos_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L452。
- `infos_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `ResourceHandle` → [blender::draw::ResourceHandle::ResourceHandle · L121](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-fefeb18e38acb5b1)；[blender::draw::ResourceHandle::ResourceHandle · L122](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-36b02c7ccc4c93ed)；[blender::draw::ResourceHandle::ResourceHandle · L125](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-920cd44f5cc3c6d4)。同名重载需按实参类型选择。

<a id="f-d13903e016fd9dd4"></a>

### `blender::draw::Manager::resource_handle`

实现位置：[source/blender/draw/intern/draw_manager.hh](../../../../../source/blender/draw/intern/draw_manager.hh) · L456—L464。

接口参数：

- `const float4x4 &model_matrix`
- `const float3 &bounds_center`
- `const float3 &bounds_half_extent`

**教学注释版**

<!-- annotated:171b824c00d806 -->

```cpp
inline ResourceHandle Manager::resource_handle(const float4x4 &model_matrix,
                                               const float3 &bounds_center,
                                               const float3 &bounds_half_extent)
{
  matrix_buf.current().get_or_resize(resource_len_).sync(model_matrix);
  bounds_buf.current().get_or_resize(resource_len_).sync(bounds_center, bounds_half_extent);
  infos_buf.current().get_or_resize(resource_len_).sync();
  return ResourceHandle(resource_len_++, false);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_manager.hh · L456—L464</summary>

<!-- original:171b824c00d806:source/blender/draw/intern/draw_manager.hh:456:464 -->

```cpp
inline ResourceHandle Manager::resource_handle(const float4x4 &model_matrix,
                                               const float3 &bounds_center,
                                               const float3 &bounds_half_extent)
{
  matrix_buf.current().get_or_resize(resource_len_).sync(model_matrix);
  bounds_buf.current().get_or_resize(resource_len_).sync(bounds_center, bounds_half_extent);
  infos_buf.current().get_or_resize(resource_len_).sync();
  return ResourceHandle(resource_len_++, false);
}
```

</details>

**结果出口**

- `return ResourceHandle(resource_len_++, false);`

**继续追踪实现**

- `matrix_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L460。
- `matrix_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L460。
- `matrix_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `bounds_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L461。
- `bounds_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L461。
- `bounds_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `infos_buf.current().get_or_resize(resource_len_).sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L462。
- `infos_buf.current().get_or_resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L462。
- `infos_buf.current` → [current · L1455](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-241f5fd248365b76)；[current · L1471](%E4%BE%9D%E8%B5%96-DRW_gpu_wrapper-c80c4f.md#f-b62e68c32f25a1a2)。同名重载需按实参类型选择。
- `ResourceHandle` → [blender::draw::ResourceHandle::ResourceHandle · L121](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-fefeb18e38acb5b1)；[blender::draw::ResourceHandle::ResourceHandle · L122](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-36b02c7ccc4c93ed)；[blender::draw::ResourceHandle::ResourceHandle · L125](%E4%BE%9D%E8%B5%96-draw_handle-b6355d.md#f-920cd44f5cc3c6d4)。同名重载需按实参类型选择。
