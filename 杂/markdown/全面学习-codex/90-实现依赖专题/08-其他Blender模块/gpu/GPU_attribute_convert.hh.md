# 实现依赖专题：source/blender/gpu/GPU_attribute_convert.hh

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::gpu::convert_normal"]:::abstraction
  F1["blender::gpu::convert_normal"]:::compute
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
  F["GPU_attribute_convert.hh实现"]:::compute
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

<a id="f-d24eef906ebcd8b5"></a>

### `blender::gpu::convert_normal`

实现位置：[source/blender/gpu/GPU_attribute_convert.hh](../../../../../../../source/blender/gpu/GPU_attribute_convert.hh) · L21—L24。

接口参数：

- `const float3 &src`

**教学注释版**

<!-- annotated:81129587494432 -->

```cpp
template<> inline int1010102_norm convert_normal(const float3 &src)
{
  return int1010102_norm(float4(src, 0.0f));
}
```

<details>
<summary>核对原始源码：source/blender/gpu/GPU_attribute_convert.hh · L21—L24</summary>

<!-- original:81129587494432:source/blender/gpu/GPU_attribute_convert.hh:21:24 -->

```cpp
template<> inline int1010102_norm convert_normal(const float3 &src)
{
  return int1010102_norm(float4(src, 0.0f));
}
```

</details>

**结果出口**

- `return int1010102_norm(float4(src, 0.0f));`

**继续追踪实现**

- `int1010102_norm` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L23。
- `float4` → [float4 · L56](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-f0908e385c5b)；[float4 · L60](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-7962dcdc288b)；[float4 · L56](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-adb8e9e87775)；[float4 · L642](../compositor/algorithms/intern/smaa.cc.md#m-9362daaa821c)。宏定义由构建条件选择。

<a id="f-40f0824f9b7edbbb"></a>

### `blender::gpu::convert_normal`

实现位置：[source/blender/gpu/GPU_attribute_convert.hh](../../../../../../../source/blender/gpu/GPU_attribute_convert.hh) · L26—L29。

接口参数：

- `const float3 &src`

**教学注释版**

<!-- annotated:1fbc4bf46e028b -->

```cpp
template<> inline short4 convert_normal(const float3 &src)
{
  // [讲解] std::numeric_limits<short>::max：按比较关系选取较大值。本讲解中的增长公式同时满足最低请求和几何增长；若保存返回引用，还需注意实参寿命。
  return short4(src * float(std::numeric_limits<short>::max()), 0);
}
```

<details>
<summary>核对原始源码：source/blender/gpu/GPU_attribute_convert.hh · L26—L29</summary>

<!-- original:1fbc4bf46e028b:source/blender/gpu/GPU_attribute_convert.hh:26:29 -->

```cpp
template<> inline short4 convert_normal(const float3 &src)
{
  return short4(src * float(std::numeric_limits<short>::max()), 0);
}
```

</details>

**结果出口**

- `return short4(src * float(std::numeric_limits<short>::max()), 0);`

**继续追踪实现**

- `short4` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L28。
- `std::numeric_limits<short>::max` → [外部契约](https://eel.is/c++draft/alg.min.max)：按比较关系选取较大值。本讲解中的增长公式同时满足最低请求和几何增长；若保存返回引用，还需注意实参寿命。
