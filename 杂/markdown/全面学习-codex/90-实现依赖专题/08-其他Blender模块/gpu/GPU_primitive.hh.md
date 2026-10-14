# 实现依赖专题：source/blender/gpu/GPU_primitive.hh

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::is_restart_compatible"]:::abstraction
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
  F["GPU_primitive.hh实现"]:::compute
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

## 相关类型布局与成员入口

<a id="t-ee1b2c574fda"></a>

### `blender::GPUPrimType`

原始声明：[source/blender/gpu/GPU_primitive.hh](../../../../../../../source/blender/gpu/GPU_primitive.hh) · L18—L34。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:c01468a473b074 -->

```cpp
enum GPUPrimType : int8_t {
  GPU_PRIM_POINTS,
  GPU_PRIM_LINES,
  GPU_PRIM_TRIS,
  GPU_PRIM_LINE_STRIP,
  GPU_PRIM_LINE_LOOP, /* GL has this, Vulkan and Metal do not */
  GPU_PRIM_TRI_STRIP,
  GPU_PRIM_TRI_FAN, /* Metal API does not support this. */

  /* Metal API does not support ADJ primitive types but
   * handled via the geometry-shader-alternative path. */
  GPU_PRIM_LINES_ADJ,
  GPU_PRIM_TRIS_ADJ,
  GPU_PRIM_LINE_STRIP_ADJ,

  GPU_PRIM_NONE,
};
```

<details>
<summary>核对原始源码：source/blender/gpu/GPU_primitive.hh · L18—L34</summary>

<!-- original:c01468a473b074:source/blender/gpu/GPU_primitive.hh:18:34 -->

```cpp
enum GPUPrimType : int8_t {
  GPU_PRIM_POINTS,
  GPU_PRIM_LINES,
  GPU_PRIM_TRIS,
  GPU_PRIM_LINE_STRIP,
  GPU_PRIM_LINE_LOOP, /* GL has this, Vulkan and Metal do not */
  GPU_PRIM_TRI_STRIP,
  GPU_PRIM_TRI_FAN, /* Metal API does not support this. */

  /* Metal API does not support ADJ primitive types but
   * handled via the geometry-shader-alternative path. */
  GPU_PRIM_LINES_ADJ,
  GPU_PRIM_TRIS_ADJ,
  GPU_PRIM_LINE_STRIP_ADJ,

  GPU_PRIM_NONE,
};
```

</details>


## 完整成员与函数实现

<a id="f-33c627850cd717a0"></a>

### `blender::is_restart_compatible`

实现位置：[source/blender/gpu/GPU_primitive.hh](../../../../../../../source/blender/gpu/GPU_primitive.hh) · L95—L116。

接口参数：

- `GPUPrimType type`

**教学注释版**

<!-- annotated:9116aacacd339d -->

```cpp
inline bool is_restart_compatible(GPUPrimType type)
{
  switch (type) {
    case GPU_PRIM_POINTS:
    case GPU_PRIM_LINES:
    case GPU_PRIM_TRIS:
    case GPU_PRIM_LINES_ADJ:
    case GPU_PRIM_TRIS_ADJ:
    case GPU_PRIM_NONE:
    default: {
      return false;
    }
    case GPU_PRIM_LINE_STRIP:
    case GPU_PRIM_LINE_LOOP:
    case GPU_PRIM_TRI_STRIP:
    case GPU_PRIM_TRI_FAN:
    case GPU_PRIM_LINE_STRIP_ADJ: {
      return true;
    }
  }
  return false;
}
```

<details>
<summary>核对原始源码：source/blender/gpu/GPU_primitive.hh · L95—L116</summary>

<!-- original:9116aacacd339d:source/blender/gpu/GPU_primitive.hh:95:116 -->

```cpp
inline bool is_restart_compatible(GPUPrimType type)
{
  switch (type) {
    case GPU_PRIM_POINTS:
    case GPU_PRIM_LINES:
    case GPU_PRIM_TRIS:
    case GPU_PRIM_LINES_ADJ:
    case GPU_PRIM_TRIS_ADJ:
    case GPU_PRIM_NONE:
    default: {
      return false;
    }
    case GPU_PRIM_LINE_STRIP:
    case GPU_PRIM_LINE_LOOP:
    case GPU_PRIM_TRI_STRIP:
    case GPU_PRIM_TRI_FAN:
    case GPU_PRIM_LINE_STRIP_ADJ: {
      return true;
    }
  }
  return false;
}
```

</details>

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
