# Blender sRGB 转灰度算法解析

**文件路径**: `source\blender\blenlib\intern\math_color_inline.cc:209-236`

这段代码提供了将 **sRGB 色彩空间**（通常用于 UI 和主题）的颜色转换为 **灰度值（亮度/Luminance）** 的高效实现。

---

## 1. 核心警告 (Warning)

> **注意**：仅用于已知处于 **sRGB 空间** 的颜色（如用户界面、图标、主题颜色）。

*   **UI 使用**: 界面元素的变灰、计算文字对比度等。
*   **渲染禁用**: 3D 场景、材质渲染**不应**使用此函数。因为场景渲染通常在线性空间（Linear Space）下工作，应该使用颜色管理模块（Color Management）中的 `IMB_colormanagement_get_luminance`。

---

## 2. 浮点数版本 (`srgb_to_grayscale`)

用于处理 `0.0` 到 `1.0` 范围的浮点颜色。

```cpp
/** \name sRGB/Gray-Scale Functions
 * \warning Only use for colors known to be in sRGB space, like user interface and themes.
 * Scene color should use #IMB_colormanagement_get_luminance instead. */

MINLINE float srgb_to_grayscale(const float rgb[3])
{
  /* Real values are: `Y = 0.2126390059(R) + 0.7151686788(G) + 0.0721923154(B)`
   * according to: "Derivation of Basic Television Color Equations", RP 177-1993
   * As this sums slightly above 1.0, the document recommends to use: `0.2126(R) + 0.7152(G) + 0.0722(B)`, as used here. */
  return (0.2126f * rgb[0]) + (0.7152f * rgb[1]) + (0.0722f * rgb[2]);
}
```

### 算法原理
该公式基于人眼对不同颜色光亮度的敏感度（**Luma 转换公式**，基于 Rec. 709 标准）：
*   **0.7152 (绿)**: 人眼对绿色最敏感，权重最高。
*   **0.2126 (红)**: 敏感度次之。
*   **0.0722 (蓝)**: 人眼对蓝色最不敏感，权重最低。

**系数来源**: 引用自 "Derivation of Basic Television Color Equations" (RP 177-1993)。这三个系数相加正好等于 `1.0`，保证了能量守恒（即纯白色的亮度仍为 1.0）。

---

## 3. 字节版本 (`srgb_to_grayscale_byte`)

用于处理 `0` 到 `255` (`unsigned char`) 范围的整数颜色。通常用于位图处理或 UI 绘制优化。

```cpp
MINLINE unsigned char srgb_to_grayscale_byte(const unsigned char rgb[3])
{
  /* The high precision values are used to calculate the rounded byte weights so they add up to 255: `54(R) + 182(G) + 19(B)` */
  return (unsigned char)(
    (
        ((unsigned short)rgb[0] * 54) +
        ((unsigned short)rgb[1] * 182) +
        ((unsigned short)rgb[2] * 19)
    ) / 255);
}
```

### 优化逻辑
这是一个**定点数优化（Fixed-point optimization）**，为了避免昂贵的浮点运算：

1.  **整数权重**: 将浮点权重映射到 `0-255` 的整数空间：
    *   Red: $0.2126 \times 255 \approx 54.2 \to \mathbf{54}$
    *   Green: $0.7152 \times 255 \approx 182.3 \to \mathbf{182}$
    *   Blue: $0.0722 \times 255 \approx 18.4 \to \mathbf{19}$
    *   **校验**: $54 + 182 + 19 = 255$。

2.  **类型转换 (`unsigned short`)**:
    *   运算过程中，单项最大值可能达到 $182 \times 255 = 46410$。
    *   `unsigned char` (最大 255) 会溢出。
    *   因此强制转换为 `unsigned short` (最大 65535) 来存储中间乘积结果。

3.  **计算流程**:
    $$ \text{Gray} = \frac{(R \times 54) + (G \times 182) + (B \times 19)}{255} $$

此方法在保持极高运行速度的同时，提供了足够 UI 显示使用的灰度精度。