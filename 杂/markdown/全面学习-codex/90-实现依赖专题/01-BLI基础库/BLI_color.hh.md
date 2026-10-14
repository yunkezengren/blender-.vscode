# 实现依赖专题：source/blender/blenlib/BLI_color.hh

[实现依赖导航](../README.md) · [符号索引](../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::color::decode"]:::abstraction
  F1["blender::color::premultiply_alpha"]:::compute
  F2["blender::color::unpremultiply_alpha"]:::compute
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
  F["BLI_color.hh实现"]:::compute
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

<a id="f-fd48169535f754fd"></a>

### `blender::color::decode`

实现位置：[source/blender/blenlib/BLI_color.hh](../../../../../../source/blender/blenlib/BLI_color.hh) · L76—L85。

接口参数：

- `const ColorSceneLinearByteEncoded4b<Alpha> &color`

**教学注释版**

<!-- annotated:939555f42b99fb -->

```cpp
template<eAlpha Alpha>
BLI_INLINE ColorSceneLinear4f<Alpha> decode(const ColorSceneLinearByteEncoded4b<Alpha> &color)
{
  ColorSceneLinear4f<Alpha> decoded;
  srgb_to_linearrgb_uchar4(decoded, color);
  if (!colorspace::scene_linear_is_rec709) {
    copy_v3_v3(decoded, colorspace::rec709_to_scene_linear * float3(decoded));
  }
  return decoded;
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_color.hh · L76—L85</summary>

<!-- original:939555f42b99fb:source/blender/blenlib/BLI_color.hh:76:85 -->

```cpp
template<eAlpha Alpha>
BLI_INLINE ColorSceneLinear4f<Alpha> decode(const ColorSceneLinearByteEncoded4b<Alpha> &color)
{
  ColorSceneLinear4f<Alpha> decoded;
  srgb_to_linearrgb_uchar4(decoded, color);
  if (!colorspace::scene_linear_is_rec709) {
    copy_v3_v3(decoded, colorspace::rec709_to_scene_linear * float3(decoded));
  }
  return decoded;
}
```

</details>

**结果出口**

- `return decoded;`

**继续追踪实现**

- `srgb_to_linearrgb_uchar4` → [blender::srgb_to_linearrgb_uchar4 · L105](intern/math_color_inline.cc.md#f-39048d10c45c927e)。
- `copy_v3_v3` → [调用协议](../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L82。
- `float3` → [float3 · L641](../08-其他Blender模块/compositor/algorithms/intern/smaa.cc.md#m-0ea8254cfdb4)。宏定义由构建条件选择。

<a id="f-9f692e7e848f8039"></a>

### `blender::color::premultiply_alpha`

实现位置：[source/blender/blenlib/BLI_color.hh](../../../../../../source/blender/blenlib/BLI_color.hh) · L92—L103。

接口参数：

- `const ColorSceneLinear4f<Alpha> &color`

**教学注释版**

<!-- annotated:06723d5deba0e1 -->

```cpp
template<eAlpha Alpha>
ColorSceneLinear4f<eAlpha::Premultiplied> premultiply_alpha(const ColorSceneLinear4f<Alpha> &color)
{
  if constexpr (Alpha == eAlpha::Straight) {
    ColorSceneLinear4f<eAlpha::Premultiplied> premultiplied;
    straight_to_premul_v4_v4(premultiplied, color);
    return premultiplied;
  }
  else {
    return color;
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_color.hh · L92—L103</summary>

<!-- original:06723d5deba0e1:source/blender/blenlib/BLI_color.hh:92:103 -->

```cpp
template<eAlpha Alpha>
ColorSceneLinear4f<eAlpha::Premultiplied> premultiply_alpha(const ColorSceneLinear4f<Alpha> &color)
{
  if constexpr (Alpha == eAlpha::Straight) {
    ColorSceneLinear4f<eAlpha::Premultiplied> premultiplied;
    straight_to_premul_v4_v4(premultiplied, color);
    return premultiplied;
  }
  else {
    return color;
  }
}
```

</details>

**结果出口**

- `return premultiplied;`
- `return color;`

**继续追踪实现**

- `straight_to_premul_v4_v4` → [blender::straight_to_premul_v4_v4 · L305](intern/math_color_inline.cc.md#f-7144705bbd89683c)。

<a id="f-9c65567863c88610"></a>

### `blender::color::unpremultiply_alpha`

实现位置：[source/blender/blenlib/BLI_color.hh](../../../../../../source/blender/blenlib/BLI_color.hh) · L110—L121。

接口参数：

- `const ColorSceneLinear4f<Alpha> &color`

**教学注释版**

<!-- annotated:cdb9fabafce8ed -->

```cpp
template<eAlpha Alpha>
ColorSceneLinear4f<eAlpha::Straight> unpremultiply_alpha(const ColorSceneLinear4f<Alpha> &color)
{
  if constexpr (Alpha == eAlpha::Premultiplied) {
    ColorSceneLinear4f<eAlpha::Straight> straighten;
    premul_to_straight_v4_v4(straighten, color);
    return straighten;
  }
  else {
    return color;
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_color.hh · L110—L121</summary>

<!-- original:cdb9fabafce8ed:source/blender/blenlib/BLI_color.hh:110:121 -->

```cpp
template<eAlpha Alpha>
ColorSceneLinear4f<eAlpha::Straight> unpremultiply_alpha(const ColorSceneLinear4f<Alpha> &color)
{
  if constexpr (Alpha == eAlpha::Premultiplied) {
    ColorSceneLinear4f<eAlpha::Straight> straighten;
    premul_to_straight_v4_v4(straighten, color);
    return straighten;
  }
  else {
    return color;
  }
}
```

</details>

**结果出口**

- `return straighten;`
- `return color;`

**继续追踪实现**

- `premul_to_straight_v4_v4` → [blender::premul_to_straight_v4_v4 · L283](intern/math_color_inline.cc.md#f-04964d02dcc5cfa0)。
