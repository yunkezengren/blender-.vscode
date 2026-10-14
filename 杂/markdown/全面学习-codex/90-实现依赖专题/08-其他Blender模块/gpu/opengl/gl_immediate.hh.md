# 实现依赖专题：source/blender/gpu/opengl/gl_immediate.hh

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::gpu::GLImmediate::vbo_id"]:::abstraction
  F1["blender::gpu::GLImmediate::buffer_offset"]:::compute
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
  F["gl_immediate.hh实现"]:::compute
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

<a id="f-fddfa219b940d285"></a>

### `blender::gpu::GLImmediate::vbo_id`

实现位置：[source/blender/gpu/opengl/gl_immediate.hh](../../../../../../../../source/blender/gpu/opengl/gl_immediate.hh) · L48—L51。

**教学注释版**

<!-- annotated:50e1c0c7fbae58 -->

```cpp
  GLuint &vbo_id()
  {
    return strict_vertex_len ? buffer_strict.vbo_id : buffer.vbo_id;
  };
```

<details>
<summary>核对原始源码：source/blender/gpu/opengl/gl_immediate.hh · L48—L51</summary>

<!-- original:50e1c0c7fbae58:source/blender/gpu/opengl/gl_immediate.hh:48:51 -->

```cpp
  GLuint &vbo_id()
  {
    return strict_vertex_len ? buffer_strict.vbo_id : buffer.vbo_id;
  };
```

</details>

**结果出口**

- `return strict_vertex_len ? buffer_strict.vbo_id : buffer.vbo_id;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-2d0b0b946653f649"></a>

### `blender::gpu::GLImmediate::buffer_offset`

实现位置：[source/blender/gpu/opengl/gl_immediate.hh](../../../../../../../../source/blender/gpu/opengl/gl_immediate.hh) · L53—L56。

**教学注释版**

<!-- annotated:63dd83b27a45c2 -->

```cpp
  size_t &buffer_offset()
  {
    return strict_vertex_len ? buffer_strict.buffer_offset : buffer.buffer_offset;
  };
```

<details>
<summary>核对原始源码：source/blender/gpu/opengl/gl_immediate.hh · L53—L56</summary>

<!-- original:63dd83b27a45c2:source/blender/gpu/opengl/gl_immediate.hh:53:56 -->

```cpp
  size_t &buffer_offset()
  {
    return strict_vertex_len ? buffer_strict.buffer_offset : buffer.buffer_offset;
  };
```

</details>

**结果出口**

- `return strict_vertex_len ? buffer_strict.buffer_offset : buffer.buffer_offset;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
