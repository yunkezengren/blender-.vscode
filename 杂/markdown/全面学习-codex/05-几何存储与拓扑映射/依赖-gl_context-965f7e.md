# 实现依赖专题：source/blender/gpu/opengl/gl_context.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::gpu::GLContext::get"]:::abstraction
  F1["blender::gpu::GLContext::state_manager_active_get"]:::compute
  F0 -->|"显式调用"| F0
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
  F["gl_context.hh实现"]:::compute
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

<a id="f-2d6c70989abeb59b"></a>

### `blender::gpu::GLContext::get`

实现位置：[source/blender/gpu/opengl/gl_context.hh](../../../../../source/blender/gpu/opengl/gl_context.hh) · L143—L146。

**教学注释版**

<!-- annotated:6422052f718a8a -->

```cpp
  static GLContext *get()
  {
    return static_cast<GLContext *>(Context::get());
  }
```

<details>
<summary>核对原始源码：source/blender/gpu/opengl/gl_context.hh · L143—L146</summary>

<!-- original:6422052f718a8a:source/blender/gpu/opengl/gl_context.hh:143:146 -->

```cpp
  static GLContext *get()
  {
    return static_cast<GLContext *>(Context::get());
  }
```

</details>

**结果出口**

- `return static_cast<GLContext *>(Context::get());`

**继续追踪实现**

- `Context::get` → [blender::gpu::GLContext::get · L143](%E4%BE%9D%E8%B5%96-gl_context-965f7e.md#f-2d6c70989abeb59b)。

<a id="f-bcf280500593b7e8"></a>

### `blender::gpu::GLContext::state_manager_active_get`

实现位置：[source/blender/gpu/opengl/gl_context.hh](../../../../../source/blender/gpu/opengl/gl_context.hh) · L148—L152。

**教学注释版**

<!-- annotated:33ae71e8c91e4e -->

```cpp
  static GLStateManager *state_manager_active_get()
  {
    GLContext *ctx = GLContext::get();
    return static_cast<GLStateManager *>(ctx->state_manager);
  };
```

<details>
<summary>核对原始源码：source/blender/gpu/opengl/gl_context.hh · L148—L152</summary>

<!-- original:33ae71e8c91e4e:source/blender/gpu/opengl/gl_context.hh:148:152 -->

```cpp
  static GLStateManager *state_manager_active_get()
  {
    GLContext *ctx = GLContext::get();
    return static_cast<GLStateManager *>(ctx->state_manager);
  };
```

</details>

**结果出口**

- `return static_cast<GLStateManager *>(ctx->state_manager);`

**继续追踪实现**

- `GLContext::get` → [blender::gpu::GLContext::get · L143](%E4%BE%9D%E8%B5%96-gl_context-965f7e.md#f-2d6c70989abeb59b)。
