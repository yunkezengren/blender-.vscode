# 实现依赖专题：source/blender/gpu/intern/gpu_uniform_buffer.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::GPU_uniformbuf_create_ex"]:::abstraction
  F1["blender::GPU_uniformbuf_free"]:::compute
  F2["blender::GPU_uniformbuf_update"]:::compute
  F3["blender::GPU_uniformbuf_bind"]:::compute
  F4["blender::GPU_uniformbuf_debug_unbind_all"]:::compute
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
  F["gpu_uniform_buffer.cc实现"]:::compute
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

<a id="f-a0ba5479ae2a63ac"></a>

### `blender::GPU_uniformbuf_create_ex`

实现位置：[source/blender/gpu/intern/gpu_uniform_buffer.cc](../../../../../source/blender/gpu/intern/gpu_uniform_buffer.cc) · L302—L316。

接口参数：

- `size_t size`
- `const void *data`
- `const char *name`

**教学注释版**

<!-- annotated:297cae4294a912 -->

```cpp
gpu::UniformBuf *GPU_uniformbuf_create_ex(size_t size, const void *data, const char *name)
{
  UniformBuf *ubo = GPUBackend::get()->uniformbuf_alloc(size, name);
  /* Direct init. */
  if (data != nullptr) {
    ubo->update(data);
  }
  else if (G.debug & G_DEBUG_GPU) {
    /* Fill the buffer with poison values.
     * (NaN for floats, -1 for `int` and "max value" for `uint`). */
    Vector<uchar> uninitialized_data(size, 0xFF);
    // [讲解] uninitialized_data.data：提供当前存储或有效范围的地址。
    ubo->update(uninitialized_data.data());
  }
  return ubo;
}
```

<details>
<summary>核对原始源码：source/blender/gpu/intern/gpu_uniform_buffer.cc · L302—L316</summary>

<!-- original:297cae4294a912:source/blender/gpu/intern/gpu_uniform_buffer.cc:302:316 -->

```cpp
gpu::UniformBuf *GPU_uniformbuf_create_ex(size_t size, const void *data, const char *name)
{
  UniformBuf *ubo = GPUBackend::get()->uniformbuf_alloc(size, name);
  /* Direct init. */
  if (data != nullptr) {
    ubo->update(data);
  }
  else if (G.debug & G_DEBUG_GPU) {
    /* Fill the buffer with poison values.
     * (NaN for floats, -1 for `int` and "max value" for `uint`). */
    Vector<uchar> uninitialized_data(size, 0xFF);
    ubo->update(uninitialized_data.data());
  }
  return ubo;
}
```

</details>

**结果出口**

- `return ubo;`

**继续追踪实现**

- `GPUBackend::get()->uniformbuf_alloc` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L304。
- `GPUBackend::get` → [blender::GPUBackend::get · L642](%E4%BE%9D%E8%B5%96-gpu_context-77a234.md#f-c876dc1cb5bd7700)。
- `ubo->update` → [blender::update · L121](../09-LazyFunction%E4%B8%8E%E8%8A%82%E7%82%B9%E6%89%A7%E8%A1%8C%E6%9E%B6%E6%9E%84/%E4%BE%9D%E8%B5%96-node_texture_tree-b9c111.md#f-7591916c55b3dfe3)；[blender::update · L76](../09-LazyFunction%E4%B8%8E%E8%8A%82%E7%82%B9%E6%89%A7%E8%A1%8C%E6%9E%B6%E6%9E%84/%E4%BE%9D%E8%B5%96-node_texture_separate_color-ac4f58.md#f-f216062a9f7b7859)；[blender::update · L54](../09-LazyFunction%E4%B8%8E%E8%8A%82%E7%82%B9%E6%89%A7%E8%A1%8C%E6%9E%B6%E6%9E%84/%E4%BE%9D%E8%B5%96-node_texture_combine_color-871e59.md#f-9377b7191cf4cec4)；[blender::update · L106](../09-LazyFunction%E4%B8%8E%E8%8A%82%E7%82%B9%E6%89%A7%E8%A1%8C%E6%9E%B6%E6%9E%84/%E4%BE%9D%E8%B5%96-node_composite_tree-a763ff.md#f-7565befdaeb2a373)。同名重载需按实参类型选择。
- `uninitialized_data.data` → [blender::Vector::data · L954](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/12-Vector%E5%BC%82%E5%B8%B8%E5%AE%89%E5%85%A8%E4%B8%8E%E8%BE%B9%E7%95%8C.md#f-6e441591404715bc)；[blender::Vector::data · L962](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/12-Vector%E5%BC%82%E5%B8%B8%E5%AE%89%E5%85%A8%E4%B8%8E%E8%BE%B9%E7%95%8C.md#f-4bc78d4954c1021a)。同名重载需按实参类型选择。

<a id="f-db64ab63c2586626"></a>

### `blender::GPU_uniformbuf_free`

实现位置：[source/blender/gpu/intern/gpu_uniform_buffer.cc](../../../../../source/blender/gpu/intern/gpu_uniform_buffer.cc) · L339—L342。

接口参数：

- `gpu::UniformBuf *ubo`

**教学注释版**

<!-- annotated:521c5f0c9c6eef -->

```cpp
void GPU_uniformbuf_free(gpu::UniformBuf *ubo)
{
  delete ubo;
}
```

<details>
<summary>核对原始源码：source/blender/gpu/intern/gpu_uniform_buffer.cc · L339—L342</summary>

<!-- original:521c5f0c9c6eef:source/blender/gpu/intern/gpu_uniform_buffer.cc:339:342 -->

```cpp
void GPU_uniformbuf_free(gpu::UniformBuf *ubo)
{
  delete ubo;
}
```

</details>

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-b41c810e912d857a"></a>

### `blender::GPU_uniformbuf_update`

实现位置：[source/blender/gpu/intern/gpu_uniform_buffer.cc](../../../../../source/blender/gpu/intern/gpu_uniform_buffer.cc) · L344—L347。

接口参数：

- `gpu::UniformBuf *ubo`
- `const void *data`

**教学注释版**

<!-- annotated:7ba2a290df0fef -->

```cpp
void GPU_uniformbuf_update(gpu::UniformBuf *ubo, const void *data)
{
  ubo->update(data);
}
```

<details>
<summary>核对原始源码：source/blender/gpu/intern/gpu_uniform_buffer.cc · L344—L347</summary>

<!-- original:7ba2a290df0fef:source/blender/gpu/intern/gpu_uniform_buffer.cc:344:347 -->

```cpp
void GPU_uniformbuf_update(gpu::UniformBuf *ubo, const void *data)
{
  ubo->update(data);
}
```

</details>

**继续追踪实现**

- `ubo->update` → [blender::update · L121](../09-LazyFunction%E4%B8%8E%E8%8A%82%E7%82%B9%E6%89%A7%E8%A1%8C%E6%9E%B6%E6%9E%84/%E4%BE%9D%E8%B5%96-node_texture_tree-b9c111.md#f-7591916c55b3dfe3)；[blender::update · L76](../09-LazyFunction%E4%B8%8E%E8%8A%82%E7%82%B9%E6%89%A7%E8%A1%8C%E6%9E%B6%E6%9E%84/%E4%BE%9D%E8%B5%96-node_texture_separate_color-ac4f58.md#f-f216062a9f7b7859)；[blender::update · L54](../09-LazyFunction%E4%B8%8E%E8%8A%82%E7%82%B9%E6%89%A7%E8%A1%8C%E6%9E%B6%E6%9E%84/%E4%BE%9D%E8%B5%96-node_texture_combine_color-871e59.md#f-9377b7191cf4cec4)；[blender::update · L106](../09-LazyFunction%E4%B8%8E%E8%8A%82%E7%82%B9%E6%89%A7%E8%A1%8C%E6%9E%B6%E6%9E%84/%E4%BE%9D%E8%B5%96-node_composite_tree-a763ff.md#f-7565befdaeb2a373)。同名重载需按实参类型选择。

<a id="f-6f7028e200711532"></a>

### `blender::GPU_uniformbuf_bind`

实现位置：[source/blender/gpu/intern/gpu_uniform_buffer.cc](../../../../../source/blender/gpu/intern/gpu_uniform_buffer.cc) · L349—L352。

接口参数：

- `gpu::UniformBuf *ubo`
- `int slot`

**教学注释版**

<!-- annotated:169c6200ca1862 -->

```cpp
void GPU_uniformbuf_bind(gpu::UniformBuf *ubo, int slot)
{
  ubo->bind(slot);
}
```

<details>
<summary>核对原始源码：source/blender/gpu/intern/gpu_uniform_buffer.cc · L349—L352</summary>

<!-- original:169c6200ca1862:source/blender/gpu/intern/gpu_uniform_buffer.cc:349:352 -->

```cpp
void GPU_uniformbuf_bind(gpu::UniformBuf *ubo, int slot)
{
  ubo->bind(slot);
}
```

</details>

**继续追踪实现**

- `ubo->bind` → [blender::GLShader::bind · L1410](%E4%BE%9D%E8%B5%96-gl_shader-766737.md#f-7374ce386abefd3f)；[blender::GLBatch::bind · L239](%E4%BE%9D%E8%B5%96-gl_batch-d8877a.md#f-09d832d1583277b2)。同名重载需按实参类型选择。

<a id="f-f085c3d5621ec231"></a>

### `blender::GPU_uniformbuf_debug_unbind_all`

实现位置：[source/blender/gpu/intern/gpu_uniform_buffer.cc](../../../../../source/blender/gpu/intern/gpu_uniform_buffer.cc) · L364—L367。

**教学注释版**

<!-- annotated:ff8b3e757e796c -->

```cpp
void GPU_uniformbuf_debug_unbind_all()
{
  Context::get()->debug_unbind_all_ubo();
}
```

<details>
<summary>核对原始源码：source/blender/gpu/intern/gpu_uniform_buffer.cc · L364—L367</summary>

<!-- original:ff8b3e757e796c:source/blender/gpu/intern/gpu_uniform_buffer.cc:364:367 -->

```cpp
void GPU_uniformbuf_debug_unbind_all()
{
  Context::get()->debug_unbind_all_ubo();
}
```

</details>

**继续追踪实现**

- `Context::get()->debug_unbind_all_ubo` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L366。
- `Context::get` → [blender::gpu::Context::get · L127](%E4%BE%9D%E8%B5%96-gpu_context-77a234.md#f-7ca16707244f2d11)。
