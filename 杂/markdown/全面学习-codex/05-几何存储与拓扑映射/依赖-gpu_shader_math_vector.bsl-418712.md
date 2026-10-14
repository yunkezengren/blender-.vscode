# 实现依赖专题：source/blender/gpu/shaders/common/gpu_shader_math_vector.bsl.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["length_squared"]:::abstraction
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
  F["gpu_shader_math_vector.bsl.hh实现"]:::compute
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

<a id="f-1bc529235547f337"></a>

### `length_squared`

实现位置：[source/blender/gpu/shaders/common/gpu_shader_math_vector.bsl.hh](../../../../../source/blender/gpu/shaders/common/gpu_shader_math_vector.bsl.hh) · L90—L93。

接口参数：

- `VecT a`

**教学注释版**

<!-- annotated:2bd4308d98f4f2 -->

```cpp
template<typename VecT> float length_squared(VecT a)
{
  return dot(a, a);
}
```

<details>
<summary>核对原始源码：source/blender/gpu/shaders/common/gpu_shader_math_vector.bsl.hh · L90—L93</summary>

<!-- original:2bd4308d98f4f2:source/blender/gpu/shaders/common/gpu_shader_math_vector.bsl.hh:90:93 -->

```cpp
template<typename VecT> float length_squared(VecT a)
{
  return dot(a, a);
}
```

</details>

**结果出口**

- `return dot(a, a);`

**继续追踪实现**

- `dot` → [dot · L341](%E4%BE%9D%E8%B5%96-sky_math-8091a6.md#f-1d1835d5ece907c2)；[dot · L371](%E4%BE%9D%E8%B5%96-sky_math-8091a6.md#f-f86883f9f73a3d45)；[dot · L401](%E4%BE%9D%E8%B5%96-sky_math-8091a6.md#f-7ea1a37447b2c515)；[dot · L50](%E4%BE%9D%E8%B5%96-math_quaternion-957b27.md#f-e434705e781b49d6)；[dot · L309](%E4%BE%9D%E8%B5%96-math_float8-4760ed.md#f-c00ff533ac3dcbbb)；[dot · L391](%E4%BE%9D%E8%B5%96-math_float4-2d91ea.md#f-66bab7788a88350d)；[dot · L254](%E4%BE%9D%E8%B5%96-math_float3-eb3e6f.md#f-1345479cbb5c64a8)；[dot · L131](%E4%BE%9D%E8%B5%96-math_float2-be3c03.md#f-c6c5b4937f8c1456)；[dot · L268](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-e1745c95ae876efd)。同名重载需按实参类型选择。
