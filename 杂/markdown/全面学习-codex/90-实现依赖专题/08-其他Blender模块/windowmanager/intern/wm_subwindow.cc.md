# 实现依赖专题：source/blender/windowmanager/intern/wm_subwindow.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::wmOrtho2"]:::abstraction
  F1["blender::wmOrtho2_offset"]:::compute
  F2["blender::wmOrtho2_region_pixelspace"]:::compute
  F3["blender::wmGetProjectionMatrix"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F1
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
  F["wm_subwindow.cc实现"]:::compute
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

<a id="f-5dd5c1d1033d899e"></a>

### `blender::wmOrtho2`

实现位置：[source/blender/windowmanager/intern/wm_subwindow.cc](../../../../../../../../source/blender/windowmanager/intern/wm_subwindow.cc) · L108—L120。

接口参数：

- `float x1`
- `float x2`
- `float y1`
- `float y2`

**教学注释版**

<!-- annotated:ad647bd3b9232e -->

```cpp
void wmOrtho2(float x1, float x2, float y1, float y2)
{
  /* Prevent opengl from generating errors. */
  if (x2 == x1) {
    x2 += 1.0f;
  }
  if (y2 == y1) {
    y2 += 1.0f;
  }

  GPU_matrix_ortho_set(
      x1, x2, y1, y2, GPU_MATRIX_ORTHO_CLIP_NEAR_DEFAULT, GPU_MATRIX_ORTHO_CLIP_FAR_DEFAULT);
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_subwindow.cc · L108—L120</summary>

<!-- original:ad647bd3b9232e:source/blender/windowmanager/intern/wm_subwindow.cc:108:120 -->

```cpp
void wmOrtho2(float x1, float x2, float y1, float y2)
{
  /* Prevent opengl from generating errors. */
  if (x2 == x1) {
    x2 += 1.0f;
  }
  if (y2 == y1) {
    y2 += 1.0f;
  }

  GPU_matrix_ortho_set(
      x1, x2, y1, y2, GPU_MATRIX_ORTHO_CLIP_NEAR_DEFAULT, GPU_MATRIX_ORTHO_CLIP_FAR_DEFAULT);
}
```

</details>

**沿实际写入检查状态**

- `x2 += 1.0f;`
- `y2 += 1.0f;`

**继续追踪实现**

- `GPU_matrix_ortho_set` → [blender::GPU_matrix_ortho_set · L400](../../gpu/intern/gpu_matrix.cc.md#f-0bb5e2d8c02c2c99)。

<a id="f-68ef06d4bfc44951"></a>

### `blender::wmOrtho2_offset`

实现位置：[source/blender/windowmanager/intern/wm_subwindow.cc](../../../../../../../../source/blender/windowmanager/intern/wm_subwindow.cc) · L122—L125。

接口参数：

- `const float x`
- `const float y`
- `const float ofs`

**教学注释版**

<!-- annotated:7ce600dd14c769 -->

```cpp
static void wmOrtho2_offset(const float x, const float y, const float ofs)
{
  wmOrtho2(ofs, x + ofs, ofs, y + ofs);
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_subwindow.cc · L122—L125</summary>

<!-- original:7ce600dd14c769:source/blender/windowmanager/intern/wm_subwindow.cc:122:125 -->

```cpp
static void wmOrtho2_offset(const float x, const float y, const float ofs)
{
  wmOrtho2(ofs, x + ofs, ofs, y + ofs);
}
```

</details>

**继续追踪实现**

- `wmOrtho2` → [blender::wmOrtho2 · L108](wm_subwindow.cc.md#f-5dd5c1d1033d899e)。

<a id="f-81f42b31d31e8f75"></a>

### `blender::wmOrtho2_region_pixelspace`

实现位置：[source/blender/windowmanager/intern/wm_subwindow.cc](../../../../../../../../source/blender/windowmanager/intern/wm_subwindow.cc) · L127—L130。

接口参数：

- `const ARegion *region`

**教学注释版**

<!-- annotated:2ce2d50d058924 -->

```cpp
void wmOrtho2_region_pixelspace(const ARegion *region)
{
  wmOrtho2_offset(region->winx, region->winy, -0.01f);
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_subwindow.cc · L127—L130</summary>

<!-- original:2ce2d50d058924:source/blender/windowmanager/intern/wm_subwindow.cc:127:130 -->

```cpp
void wmOrtho2_region_pixelspace(const ARegion *region)
{
  wmOrtho2_offset(region->winx, region->winy, -0.01f);
}
```

</details>

**继续追踪实现**

- `wmOrtho2_offset` → [blender::wmOrtho2_offset · L122](wm_subwindow.cc.md#f-68ef06d4bfc44951)。

<a id="f-f789df2154feaf25"></a>

### `blender::wmGetProjectionMatrix`

实现位置：[source/blender/windowmanager/intern/wm_subwindow.cc](../../../../../../../../source/blender/windowmanager/intern/wm_subwindow.cc) · L137—L148。

接口参数：

- `float mat[4][4]`
- `const rcti *winrct`

**教学注释版**

<!-- annotated:7da2b5f17603a2 -->

```cpp
void wmGetProjectionMatrix(float mat[4][4], const rcti *winrct)
{
  int width = BLI_rcti_size_x(winrct) + 1;
  int height = BLI_rcti_size_y(winrct) + 1;
  orthographic_m4(mat,
                  -GLA_PIXEL_OFS,
                  float(width) - GLA_PIXEL_OFS,
                  -GLA_PIXEL_OFS,
                  float(height) - GLA_PIXEL_OFS,
                  GPU_MATRIX_ORTHO_CLIP_NEAR_DEFAULT,
                  GPU_MATRIX_ORTHO_CLIP_FAR_DEFAULT);
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_subwindow.cc · L137—L148</summary>

<!-- original:7da2b5f17603a2:source/blender/windowmanager/intern/wm_subwindow.cc:137:148 -->

```cpp
void wmGetProjectionMatrix(float mat[4][4], const rcti *winrct)
{
  int width = BLI_rcti_size_x(winrct) + 1;
  int height = BLI_rcti_size_y(winrct) + 1;
  orthographic_m4(mat,
                  -GLA_PIXEL_OFS,
                  float(width) - GLA_PIXEL_OFS,
                  -GLA_PIXEL_OFS,
                  float(height) - GLA_PIXEL_OFS,
                  GPU_MATRIX_ORTHO_CLIP_NEAR_DEFAULT,
                  GPU_MATRIX_ORTHO_CLIP_FAR_DEFAULT);
}
```

</details>

**继续追踪实现**

- `BLI_rcti_size_x` → [blender::BLI_rcti_size_x · L203](../../../01-BLI基础库/BLI_rect.hh.md#f-7a8fb2c54a829be6)。
- `BLI_rcti_size_y` → [blender::BLI_rcti_size_y · L207](../../../01-BLI基础库/BLI_rect.hh.md#f-ac87d6c708d502ad)。
- `orthographic_m4` → [blender::orthographic_m4 · L4712](../../../01-BLI基础库/intern/math_geom.cc.md#f-d52906a632ea05bc)。
