# 实现依赖专题：source/blender/gpu/opengl/gl_index_buffer.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::gpu::GLIndexBuf::bind"]:::abstraction
  F1["blender::gpu::GLIndexBuf::upload_data"]:::compute
  F2["blender::gpu::GLIndexBuf::update_sub"]:::compute
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
  F["gl_index_buffer.cc实现"]:::compute
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

<a id="f-481744e33ea933d7"></a>

### `blender::gpu::GLIndexBuf::bind`

实现位置：[source/blender/gpu/opengl/gl_index_buffer.cc](../../../../../source/blender/gpu/opengl/gl_index_buffer.cc) · L20—L46。

**教学注释版**

<!-- annotated:9b84085043decb -->

```cpp
void GLIndexBuf::bind()
{
  if (is_subrange_) {
    static_cast<GLIndexBuf *>(src_)->bind();
    return;
  }

  const bool allocate_on_device = ibo_id_ == 0;
  if (allocate_on_device) {
    glGenBuffers(1, &ibo_id_);
  }

  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo_id_);

  if (data_ != nullptr || allocate_on_device) {
    size_t size = this->size_get();
    /* Pad the buffer to avoid out of bound reads when using vertex pulling mode. */
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ceil_to_multiple_ul(size, 16), nullptr, GL_STATIC_DRAW);

    if (data_ != nullptr) {
      /* Sends data to GPU. */
      glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, size, data_);
    }
    /* No need to keep copy of data in system memory. */
    MEM_SAFE_DELETE_VOID(data_);
  }
}
```

<details>
<summary>核对原始源码：source/blender/gpu/opengl/gl_index_buffer.cc · L20—L46</summary>

<!-- original:9b84085043decb:source/blender/gpu/opengl/gl_index_buffer.cc:20:46 -->

```cpp
void GLIndexBuf::bind()
{
  if (is_subrange_) {
    static_cast<GLIndexBuf *>(src_)->bind();
    return;
  }

  const bool allocate_on_device = ibo_id_ == 0;
  if (allocate_on_device) {
    glGenBuffers(1, &ibo_id_);
  }

  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo_id_);

  if (data_ != nullptr || allocate_on_device) {
    size_t size = this->size_get();
    /* Pad the buffer to avoid out of bound reads when using vertex pulling mode. */
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ceil_to_multiple_ul(size, 16), nullptr, GL_STATIC_DRAW);

    if (data_ != nullptr) {
      /* Sends data to GPU. */
      glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, size, data_);
    }
    /* No need to keep copy of data in system memory. */
    MEM_SAFE_DELETE_VOID(data_);
  }
}
```

</details>

**继续追踪实现**

- `static_cast<GLIndexBuf *>(src_)->bind` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L23。
- `glGenBuffers` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L29。
- `glBindBuffer` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L32。
- `this->size_get` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L35。
- `glBufferData` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L37。
- `ceil_to_multiple_ul` → [blender::ceil_to_multiple_ul · L250](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_base_inline-546b00.md#f-2d8b440555643252)。
- `glBufferSubData` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L41。
- `MEM_SAFE_DELETE_VOID` → [MEM_SAFE_DELETE_VOID · L448](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#m-66e7eff3d7bc)。宏定义由构建条件选择。

<a id="f-451dcc91a4f2ed45"></a>

### `blender::gpu::GLIndexBuf::upload_data`

实现位置：[source/blender/gpu/opengl/gl_index_buffer.cc](../../../../../source/blender/gpu/opengl/gl_index_buffer.cc) · L95—L98。

**教学注释版**

<!-- annotated:9a287a68fb0a8e -->

```cpp
void GLIndexBuf::upload_data()
{
  bind();
}
```

<details>
<summary>核对原始源码：source/blender/gpu/opengl/gl_index_buffer.cc · L95—L98</summary>

<!-- original:9a287a68fb0a8e:source/blender/gpu/opengl/gl_index_buffer.cc:95:98 -->

```cpp
void GLIndexBuf::upload_data()
{
  bind();
}
```

</details>

**继续追踪实现**

- `bind` → [blender::gpu::GLIndexBuf::bind · L20](%E4%BE%9D%E8%B5%96-gl_index_buffer-d8d78b.md#f-481744e33ea933d7)。

<a id="f-5753e4749840c965"></a>

### `blender::gpu::GLIndexBuf::update_sub`

实现位置：[source/blender/gpu/opengl/gl_index_buffer.cc](../../../../../source/blender/gpu/opengl/gl_index_buffer.cc) · L100—L103。

接口参数：

- `uint start`
- `uint len`
- `const void *data`

**教学注释版**

<!-- annotated:d81dd6e7e7a77b -->

```cpp
void GLIndexBuf::update_sub(uint start, uint len, const void *data)
{
  glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, start, len, data);
}
```

<details>
<summary>核对原始源码：source/blender/gpu/opengl/gl_index_buffer.cc · L100—L103</summary>

<!-- original:d81dd6e7e7a77b:source/blender/gpu/opengl/gl_index_buffer.cc:100:103 -->

```cpp
void GLIndexBuf::update_sub(uint start, uint len, const void *data)
{
  glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, start, len, data);
}
```

</details>

**继续追踪实现**

- `glBufferSubData` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L102。
