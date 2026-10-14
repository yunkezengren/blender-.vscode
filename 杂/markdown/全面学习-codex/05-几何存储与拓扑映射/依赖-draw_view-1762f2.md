# 实现依赖专题：source/blender/draw/intern/draw_view.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::draw::View::bind"]:::abstraction
  F1["blender::draw::View::compute_visibility"]:::compute
  F2["blender::draw::View::get_visibility_buffer"]:::compute
  F3["blender::draw::View::default_get"]:::compute
  F4["blender::draw::View::default_set"]:::compute
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
  F["draw_view.cc实现"]:::compute
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

<a id="f-232f4cf894ce88d1"></a>

### `blender::draw::View::bind`

实现位置：[source/blender/draw/intern/draw_view.cc](../../../../../source/blender/draw/intern/draw_view.cc) · L226—L236。

**教学注释版**

<!-- annotated:4247a5f56d1169 -->

```cpp
void View::bind()
{
  if (dirty_ && !procedural_) {
    dirty_ = false;
    data_.push_update();
    culling_.push_update();
  }

  GPU_uniformbuf_bind(data_, DRW_VIEW_UBO_SLOT);
  GPU_uniformbuf_bind(culling_, DRW_VIEW_CULLING_UBO_SLOT);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_view.cc · L226—L236</summary>

<!-- original:4247a5f56d1169:source/blender/draw/intern/draw_view.cc:226:236 -->

```cpp
void View::bind()
{
  if (dirty_ && !procedural_) {
    dirty_ = false;
    data_.push_update();
    culling_.push_update();
  }

  GPU_uniformbuf_bind(data_, DRW_VIEW_UBO_SLOT);
  GPU_uniformbuf_bind(culling_, DRW_VIEW_CULLING_UBO_SLOT);
}
```

</details>

**沿实际写入检查状态**

- `dirty_ = false;`

**继续追踪实现**

- `data_.push_update` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L230。
- `culling_.push_update` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L231。
- `GPU_uniformbuf_bind` → [blender::GPU_uniformbuf_bind · L349](%E4%BE%9D%E8%B5%96-gpu_uniform_buffer-ef4877.md#f-6f7028e200711532)。

<a id="f-83043bd24debfa6a"></a>

### `blender::draw::View::compute_visibility`

实现位置：[source/blender/draw/intern/draw_view.cc](../../../../../source/blender/draw/intern/draw_view.cc) · L257—L310。

接口参数：

- `ObjectBoundsBuf &bounds`
- `ObjectInfosBuf &`
- `uint resource_len`
- `bool debug_freeze`

**教学注释版**

<!-- annotated:beaf0220552a23 -->

```cpp
void View::compute_visibility(ObjectBoundsBuf &bounds,
                              ObjectInfosBuf & /*infos*/,
                              uint resource_len,
                              bool debug_freeze)
{
  if (debug_freeze && frozen_ == false) {
    data_freeze_[0] = static_cast<ViewMatrices>(data_[0]);
    data_freeze_.push_update();
    culling_freeze_[0] = static_cast<ViewCullingData>(culling_[0]);
    culling_freeze_.push_update();
  }
  if (debug_freeze) {
    float4x4 persmat = data_freeze_[0].winmat * data_freeze_[0].viewmat;
    drw_debug_matrix_as_bbox(math::invert(persmat), float4(0, 1, 0, 1));
  }
  frozen_ = debug_freeze;

  GPU_debug_group_begin("View.compute_visibility");

  /* TODO(fclem): Early out if visibility hasn't changed. */

  uint word_per_draw = this->visibility_word_per_draw();
  /* Switch between tightly packed and set of whole word per instance. */
  uint words_len = (view_len_ == 1) ? divide_ceil_u(resource_len, 32) :
                                      resource_len * word_per_draw;
  words_len = ceil_to_multiple_u(max_ii(1, words_len), 4);
  /* TODO(fclem): Resize to nearest pow2 to reduce fragmentation. */
  visibility_buf_.resize(words_len);

  const uint32_t data = 0xFFFFFFFFu;
  GPU_storagebuf_clear(visibility_buf_, data);

  if (do_visibility_) {
    gpu::Shader *shader = DRW_shader_draw_visibility_compute_get();
    GPU_shader_bind(shader);
    GPU_shader_uniform_1i(shader, "resource_len", resource_len);
    GPU_shader_uniform_1i(shader, "view_len", view_len_);
    GPU_shader_uniform_1i(shader, "visibility_word_per_draw", word_per_draw);
    GPU_storagebuf_bind(bounds, GPU_shader_get_ssbo_binding(shader, "bounds_buf"));
    GPU_storagebuf_bind(visibility_buf_, GPU_shader_get_ssbo_binding(shader, "visibility_buf"));
    GPU_uniformbuf_bind(frozen_ ? data_freeze_ : data_, DRW_VIEW_UBO_SLOT);
    GPU_uniformbuf_bind(frozen_ ? culling_freeze_ : culling_, DRW_VIEW_CULLING_UBO_SLOT);
    GPU_compute_dispatch(shader, divide_ceil_u(resource_len, DRW_VISIBILITY_GROUP_SIZE), 1, 1);
    GPU_memory_barrier(GPU_BARRIER_SHADER_STORAGE);
  }

  if (frozen_) {
    /* Bind back the non frozen data. */
    GPU_uniformbuf_bind(data_, DRW_VIEW_UBO_SLOT);
    GPU_uniformbuf_bind(culling_, DRW_VIEW_CULLING_UBO_SLOT);
  }

  GPU_debug_group_end();
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_view.cc · L257—L310</summary>

<!-- original:beaf0220552a23:source/blender/draw/intern/draw_view.cc:257:310 -->

```cpp
void View::compute_visibility(ObjectBoundsBuf &bounds,
                              ObjectInfosBuf & /*infos*/,
                              uint resource_len,
                              bool debug_freeze)
{
  if (debug_freeze && frozen_ == false) {
    data_freeze_[0] = static_cast<ViewMatrices>(data_[0]);
    data_freeze_.push_update();
    culling_freeze_[0] = static_cast<ViewCullingData>(culling_[0]);
    culling_freeze_.push_update();
  }
  if (debug_freeze) {
    float4x4 persmat = data_freeze_[0].winmat * data_freeze_[0].viewmat;
    drw_debug_matrix_as_bbox(math::invert(persmat), float4(0, 1, 0, 1));
  }
  frozen_ = debug_freeze;

  GPU_debug_group_begin("View.compute_visibility");

  /* TODO(fclem): Early out if visibility hasn't changed. */

  uint word_per_draw = this->visibility_word_per_draw();
  /* Switch between tightly packed and set of whole word per instance. */
  uint words_len = (view_len_ == 1) ? divide_ceil_u(resource_len, 32) :
                                      resource_len * word_per_draw;
  words_len = ceil_to_multiple_u(max_ii(1, words_len), 4);
  /* TODO(fclem): Resize to nearest pow2 to reduce fragmentation. */
  visibility_buf_.resize(words_len);

  const uint32_t data = 0xFFFFFFFFu;
  GPU_storagebuf_clear(visibility_buf_, data);

  if (do_visibility_) {
    gpu::Shader *shader = DRW_shader_draw_visibility_compute_get();
    GPU_shader_bind(shader);
    GPU_shader_uniform_1i(shader, "resource_len", resource_len);
    GPU_shader_uniform_1i(shader, "view_len", view_len_);
    GPU_shader_uniform_1i(shader, "visibility_word_per_draw", word_per_draw);
    GPU_storagebuf_bind(bounds, GPU_shader_get_ssbo_binding(shader, "bounds_buf"));
    GPU_storagebuf_bind(visibility_buf_, GPU_shader_get_ssbo_binding(shader, "visibility_buf"));
    GPU_uniformbuf_bind(frozen_ ? data_freeze_ : data_, DRW_VIEW_UBO_SLOT);
    GPU_uniformbuf_bind(frozen_ ? culling_freeze_ : culling_, DRW_VIEW_CULLING_UBO_SLOT);
    GPU_compute_dispatch(shader, divide_ceil_u(resource_len, DRW_VISIBILITY_GROUP_SIZE), 1, 1);
    GPU_memory_barrier(GPU_BARRIER_SHADER_STORAGE);
  }

  if (frozen_) {
    /* Bind back the non frozen data. */
    GPU_uniformbuf_bind(data_, DRW_VIEW_UBO_SLOT);
    GPU_uniformbuf_bind(culling_, DRW_VIEW_CULLING_UBO_SLOT);
  }

  GPU_debug_group_end();
}
```

</details>

**沿实际写入检查状态**

- `data_freeze_[0] = static_cast<ViewMatrices>(data_[0]);`
- `culling_freeze_[0] = static_cast<ViewCullingData>(culling_[0]);`
- `frozen_ = debug_freeze;`
- `words_len = ceil_to_multiple_u(max_ii(1, words_len), 4);`

**继续追踪实现**

- `data_freeze_.push_update` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L264。
- `culling_freeze_.push_update` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L266。
- `drw_debug_matrix_as_bbox` → [blender::draw::drw_debug_matrix_as_bbox · L185](%E4%BE%9D%E8%B5%96-draw_debug-33d6c9.md#f-2b3f938ee8316e72)。
- `math::invert` → [blender::math::invert · L202](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_matrix-d7d8ee.md#f-222be9a4cab433f5)；[blender::math::invert · L234](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-BLI_math_quaternion-cf105d.md#f-7ba965075f461895)；[blender::math::invert · L648](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-BLI_math_matrix-b7b2b4.md#f-2b50b5262b2a9121)；[blender::math::invert · L460](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-BLI_math_basis_types-fc7090.md#f-76b56b37f151208d)。同名重载需按实参类型选择。
- `float4` → [float4 · L56](%E4%BE%9D%E8%B5%96-radial_tiling_shared-98abf9.md#m-f0908e385c5b)；[float4 · L60](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-radial_tiling_shared-7989a4.md#m-7962dcdc288b)；[float4 · L56](%E4%BE%9D%E8%B5%96-node_radial_tiling_shared-b14bc2.md#m-adb8e9e87775)；[float4 · L642](%E4%BE%9D%E8%B5%96-smaa-b67bc2.md#m-9362daaa821c)。宏定义由构建条件选择。
- `GPU_debug_group_begin` → [blender::GPU_debug_group_begin · L23](%E4%BE%9D%E8%B5%96-gpu_debug-248af2.md#f-c74a16ba40e0e7a7)。
- `this->visibility_word_per_draw` → [blender::draw::View::visibility_word_per_draw · L178](%E4%BE%9D%E8%B5%96-draw_view-94a480.md#f-48a8d3b058f349df)。
- `divide_ceil_u` → [blender::divide_ceil_u · L235](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_base_inline-546b00.md#f-9bfe95d830410fdd)。
- `ceil_to_multiple_u` → [blender::ceil_to_multiple_u · L245](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_base_inline-546b00.md#f-b6a8b97456313c88)。
- `max_ii` → [blender::max_ii · L368](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_base_inline-546b00.md#f-c45aa7b373adb94c)。
- `visibility_buf_.resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L284。
- `GPU_storagebuf_clear` → [blender::GPU_storagebuf_clear · L114](%E4%BE%9D%E8%B5%96-gpu_storage_buffer-1706c5.md#f-697dd35ae1aa8463)。
- `DRW_shader_draw_visibility_compute_get` → [blender::DRW_shader_draw_visibility_compute_get · L219](%E4%BE%9D%E8%B5%96-draw_shader-7ef611.md#f-d6cb53daf12b2619)。
- `GPU_shader_bind` → [blender::GPU_shader_bind · L387](%E4%BE%9D%E8%B5%96-gpu_shader-141cc9.md#f-a879eef1816db611)。
- `GPU_shader_uniform_1i` → [blender::GPU_shader_uniform_1i · L646](%E4%BE%9D%E8%B5%96-gpu_shader-141cc9.md#f-d02d234ed60d9de0)。
- `GPU_storagebuf_bind` → [blender::GPU_storagebuf_bind · L94](%E4%BE%9D%E8%B5%96-gpu_storage_buffer-1706c5.md#f-e795e74fcc758ac4)。
- `GPU_shader_get_ssbo_binding` → [blender::GPU_shader_get_ssbo_binding · L544](%E4%BE%9D%E8%B5%96-gpu_shader-141cc9.md#f-91a2bf7d4bbda1dc)。
- `GPU_uniformbuf_bind` → [blender::GPU_uniformbuf_bind · L349](%E4%BE%9D%E8%B5%96-gpu_uniform_buffer-ef4877.md#f-6f7028e200711532)。
- `GPU_compute_dispatch` → [blender::GPU_compute_dispatch · L16](%E4%BE%9D%E8%B5%96-gpu_compute-dbaa20.md#f-333af4920056a41a)。
- `GPU_memory_barrier` → [blender::GPU_memory_barrier · L305](%E4%BE%9D%E8%B5%96-gpu_state-82c525.md#f-5a91f15b51991eb7)。
- `GPU_debug_group_end` → [blender::GPU_debug_group_end · L34](%E4%BE%9D%E8%B5%96-gpu_debug-248af2.md#f-6d1ac356d118d5ac)。

<a id="f-85c9eb1e418b7a3c"></a>

### `blender::draw::View::get_visibility_buffer`

实现位置：[source/blender/draw/intern/draw_view.cc](../../../../../source/blender/draw/intern/draw_view.cc) · L312—L315。

**教学注释版**

<!-- annotated:e83d4c5d05e61c -->

```cpp
VisibilityBuf &View::get_visibility_buffer()
{
  return visibility_buf_;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_view.cc · L312—L315</summary>

<!-- original:e83d4c5d05e61c:source/blender/draw/intern/draw_view.cc:312:315 -->

```cpp
VisibilityBuf &View::get_visibility_buffer()
{
  return visibility_buf_;
}
```

</details>

**结果出口**

- `return visibility_buf_;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-1edfe36a27ed8fa6"></a>

### `blender::draw::View::default_get`

实现位置：[source/blender/draw/intern/draw_view.cc](../../../../../source/blender/draw/intern/draw_view.cc) · L317—L320。

**教学注释版**

<!-- annotated:411b5eac6795b5 -->

```cpp
draw::View &View::default_get()
{
  return *drw_get().data->default_view;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_view.cc · L317—L320</summary>

<!-- original:411b5eac6795b5:source/blender/draw/intern/draw_view.cc:317:320 -->

```cpp
draw::View &View::default_get()
{
  return *drw_get().data->default_view;
}
```

</details>

**结果出口**

- `return *drw_get().data->default_view;`

**继续追踪实现**

- `drw_get` → [blender::drw_get · L81](%E4%BE%9D%E8%B5%96-draw_context_private-b45cc2.md#f-8fd959a68d9e8cf0)。

<a id="f-4028261dbf15aded"></a>

### `blender::draw::View::default_set`

实现位置：[source/blender/draw/intern/draw_view.cc](../../../../../source/blender/draw/intern/draw_view.cc) · L322—L325。

接口参数：

- `const float4x4 &view_mat`
- `const float4x4 &win_mat`

**教学注释版**

<!-- annotated:ce7557e52e867e -->

```cpp
void View::default_set(const float4x4 &view_mat, const float4x4 &win_mat)
{
  drw_get().data->default_view->sync(view_mat, win_mat);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_view.cc · L322—L325</summary>

<!-- original:ce7557e52e867e:source/blender/draw/intern/draw_view.cc:322:325 -->

```cpp
void View::default_set(const float4x4 &view_mat, const float4x4 &win_mat)
{
  drw_get().data->default_view->sync(view_mat, win_mat);
}
```

</details>

**继续追踪实现**

- `drw_get().data->default_view->sync` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L324。
- `drw_get` → [blender::drw_get · L81](%E4%BE%9D%E8%B5%96-draw_context_private-b45cc2.md#f-8fd959a68d9e8cf0)。
