# 实现依赖专题：source/blender/makesdna/DNA_brush_enums.h

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_brush_enums.h"]:::abstraction
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
  F["DNA_brush_enums.h实现"]:::compute
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

<a id="t-255914efa391"></a>

### `blender::eGp_Vertex_Mode`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L267—L274。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:d7e87eea100061 -->

```cpp
enum eGp_Vertex_Mode : int {
  /* Affect to Stroke only. */
  GPPAINT_MODE_STROKE = 0,
  /* Affect to Fill only. */
  GPPAINT_MODE_FILL = 1,
  /* Affect to both. */
  GPPAINT_MODE_BOTH = 2,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L267—L274</summary>

<!-- original:d7e87eea100061:source/blender/makesdna/DNA_brush_enums.h:267:274 -->

```cpp
enum eGp_Vertex_Mode : int {
  /* Affect to Stroke only. */
  GPPAINT_MODE_STROKE = 0,
  /* Affect to Fill only. */
  GPPAINT_MODE_FILL = 1,
  /* Affect to both. */
  GPPAINT_MODE_BOTH = 2,
};
```

</details>


<a id="t-02cefe434ba3"></a>

### `blender::eGP_Sculpt_Flag`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L277—L282。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:b394fc80e9ea0d -->

```cpp
enum eGP_Sculpt_Flag : int {
  /* invert the effect of the brush */
  GP_SCULPT_FLAG_INVERT = (1 << 0),
  /* temporary invert action */
  GP_SCULPT_FLAG_TMP_INVERT = (1 << 3),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L277—L282</summary>

<!-- original:b394fc80e9ea0d:source/blender/makesdna/DNA_brush_enums.h:277:282 -->

```cpp
enum eGP_Sculpt_Flag : int {
  /* invert the effect of the brush */
  GP_SCULPT_FLAG_INVERT = (1 << 0),
  /* temporary invert action */
  GP_SCULPT_FLAG_TMP_INVERT = (1 << 3),
};
```

</details>


<a id="t-86bfa367869c"></a>

### `blender::eAutomasking_flag`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L298—L314。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:c4cc512b6e7038 -->

```cpp
enum eAutomasking_flag : int {
  BRUSH_AUTOMASKING_TOPOLOGY = (1 << 0),
  BRUSH_AUTOMASKING_FACE_SETS = (1 << 1),
  BRUSH_AUTOMASKING_BOUNDARY_EDGES = (1 << 2),
  BRUSH_AUTOMASKING_BOUNDARY_FACE_SETS = (1 << 3),
  BRUSH_AUTOMASKING_CAVITY_NORMAL = (1 << 4),

  /* NOTE: normal and inverted are mutually exclusive,
   * inverted has priority if both bits are set. */
  BRUSH_AUTOMASKING_CAVITY_INVERTED = (1 << 5),
  BRUSH_AUTOMASKING_CAVITY_ALL = (1 << 4) | (1 << 5),
  BRUSH_AUTOMASKING_CAVITY_USE_CURVE = (1 << 6),
  /* (1 << 7) - unused. */
  BRUSH_AUTOMASKING_BRUSH_NORMAL = (1 << 8),
  BRUSH_AUTOMASKING_VIEW_NORMAL = (1 << 9),
  BRUSH_AUTOMASKING_VIEW_OCCLUSION = (1 << 10),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L298—L314</summary>

<!-- original:c4cc512b6e7038:source/blender/makesdna/DNA_brush_enums.h:298:314 -->

```cpp
enum eAutomasking_flag : int {
  BRUSH_AUTOMASKING_TOPOLOGY = (1 << 0),
  BRUSH_AUTOMASKING_FACE_SETS = (1 << 1),
  BRUSH_AUTOMASKING_BOUNDARY_EDGES = (1 << 2),
  BRUSH_AUTOMASKING_BOUNDARY_FACE_SETS = (1 << 3),
  BRUSH_AUTOMASKING_CAVITY_NORMAL = (1 << 4),

  /* NOTE: normal and inverted are mutually exclusive,
   * inverted has priority if both bits are set. */
  BRUSH_AUTOMASKING_CAVITY_INVERTED = (1 << 5),
  BRUSH_AUTOMASKING_CAVITY_ALL = (1 << 4) | (1 << 5),
  BRUSH_AUTOMASKING_CAVITY_USE_CURVE = (1 << 6),
  /* (1 << 7) - unused. */
  BRUSH_AUTOMASKING_BRUSH_NORMAL = (1 << 8),
  BRUSH_AUTOMASKING_VIEW_NORMAL = (1 << 9),
  BRUSH_AUTOMASKING_VIEW_OCCLUSION = (1 << 10),
};
```

</details>


<a id="t-eb63f73df41e"></a>

### `blender::eBrushFlags`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L357—L391。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:b47462baf2ddd6 -->

```cpp
enum eBrushFlags : uint32_t {
  BRUSH_HARDNESS_PRESSURE = (1 << 0),
  BRUSH_INVERT_TO_SCRAPE_FILL = (1 << 1),
  BRUSH_ALPHA_PRESSURE = (1 << 2),
  BRUSH_SIZE_PRESSURE = (1 << 3),
  BRUSH_JITTER_PRESSURE = (1 << 4),
  BRUSH_SPACING_PRESSURE = (1 << 5),
  BRUSH_ORIGINAL_PLANE = (1 << 6),
  BRUSH_GRAB_ACTIVE_VERTEX = (1 << 7),
  BRUSH_UNUSED_2 = (1 << 8),
  BRUSH_DIR_IN = (1 << 9),
  BRUSH_UNUSED_3 = (1 << 10),
  BRUSH_SMOOTH_STROKE = (1 << 11),
  BRUSH_PERSISTENT = (1 << 12),
  BRUSH_ACCUMULATE = (1 << 13),
  BRUSH_LOCK_ALPHA = (1 << 14),
  BRUSH_ORIGINAL_NORMAL = (1 << 15),
  BRUSH_OFFSET_PRESSURE = (1 << 16),
  BRUSH_SCENE_SPACING = (1 << 17),
  BRUSH_SPACE_ATTEN = (1 << 18),
  BRUSH_ADAPTIVE_SPACE = (1 << 19),
  BRUSH_LOCK_SIZE = (1 << 20),
  BRUSH_USE_GRADIENT = (1 << 21),
  BRUSH_EDGE_TO_EDGE = (1 << 22),
  BRUSH_UNUSED_4 = (1 << 23),
  BRUSH_SMOOTH_PRESSURE = (1 << 24),
  /* Deprecated. To be removed in 6.0 - @Sean-Kim */
  BRUSH_UNUSED_7 = (1 << 25),
  BRUSH_PLANE_TRIM = (1 << 26),
  BRUSH_FRONTFACE = (1 << 27),
  BRUSH_UNUSED_8 = (1 << 28),
  BRUSH_UNUSED_5 = (1 << 29),
  BRUSH_ABSOLUTE_JITTER = (1 << 30),
  BRUSH_UNUSED_6 = (1u << 31),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L357—L391</summary>

<!-- original:b47462baf2ddd6:source/blender/makesdna/DNA_brush_enums.h:357:391 -->

```cpp
enum eBrushFlags : uint32_t {
  BRUSH_HARDNESS_PRESSURE = (1 << 0),
  BRUSH_INVERT_TO_SCRAPE_FILL = (1 << 1),
  BRUSH_ALPHA_PRESSURE = (1 << 2),
  BRUSH_SIZE_PRESSURE = (1 << 3),
  BRUSH_JITTER_PRESSURE = (1 << 4),
  BRUSH_SPACING_PRESSURE = (1 << 5),
  BRUSH_ORIGINAL_PLANE = (1 << 6),
  BRUSH_GRAB_ACTIVE_VERTEX = (1 << 7),
  BRUSH_UNUSED_2 = (1 << 8),
  BRUSH_DIR_IN = (1 << 9),
  BRUSH_UNUSED_3 = (1 << 10),
  BRUSH_SMOOTH_STROKE = (1 << 11),
  BRUSH_PERSISTENT = (1 << 12),
  BRUSH_ACCUMULATE = (1 << 13),
  BRUSH_LOCK_ALPHA = (1 << 14),
  BRUSH_ORIGINAL_NORMAL = (1 << 15),
  BRUSH_OFFSET_PRESSURE = (1 << 16),
  BRUSH_SCENE_SPACING = (1 << 17),
  BRUSH_SPACE_ATTEN = (1 << 18),
  BRUSH_ADAPTIVE_SPACE = (1 << 19),
  BRUSH_LOCK_SIZE = (1 << 20),
  BRUSH_USE_GRADIENT = (1 << 21),
  BRUSH_EDGE_TO_EDGE = (1 << 22),
  BRUSH_UNUSED_4 = (1 << 23),
  BRUSH_SMOOTH_PRESSURE = (1 << 24),
  /* Deprecated. To be removed in 6.0 - @Sean-Kim */
  BRUSH_UNUSED_7 = (1 << 25),
  BRUSH_PLANE_TRIM = (1 << 26),
  BRUSH_FRONTFACE = (1 << 27),
  BRUSH_UNUSED_8 = (1 << 28),
  BRUSH_UNUSED_5 = (1 << 29),
  BRUSH_ABSOLUTE_JITTER = (1 << 30),
  BRUSH_UNUSED_6 = (1u << 31),
};
```

</details>


<a id="t-79653e268fc9"></a>

### `blender::eBrushSculptType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L449—L489。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:1cf860181882f7 -->

```cpp
enum eBrushSculptType : char {
  SCULPT_BRUSH_TYPE_DRAW = 1,
  SCULPT_BRUSH_TYPE_SMOOTH = 2,
  SCULPT_BRUSH_TYPE_PINCH = 3,
  SCULPT_BRUSH_TYPE_INFLATE = 4,
  SCULPT_BRUSH_TYPE_GRAB = 5,
  SCULPT_BRUSH_TYPE_LAYER = 6,
#ifdef DNA_DEPRECATED_ALLOW
  SCULPT_BRUSH_TYPE_FLATTEN = 7,
#endif
  SCULPT_BRUSH_TYPE_CLAY = 8,
#ifdef DNA_DEPRECATED_ALLOW
  SCULPT_BRUSH_TYPE_FILL = 9,
  SCULPT_BRUSH_TYPE_SCRAPE = 10,
#endif
  SCULPT_BRUSH_TYPE_NUDGE = 11,
  SCULPT_BRUSH_TYPE_THUMB = 12,
  SCULPT_BRUSH_TYPE_SNAKE_HOOK = 13,
  SCULPT_BRUSH_TYPE_ROTATE = 14,
  SCULPT_BRUSH_TYPE_SIMPLIFY = 15,
  SCULPT_BRUSH_TYPE_CREASE = 16,
  SCULPT_BRUSH_TYPE_BLOB = 17,
  SCULPT_BRUSH_TYPE_CLAY_STRIPS = 18,
  SCULPT_BRUSH_TYPE_MASK = 19,
  SCULPT_BRUSH_TYPE_DRAW_SHARP = 20,
  SCULPT_BRUSH_TYPE_ELASTIC_DEFORM = 21,
  SCULPT_BRUSH_TYPE_POSE = 22,
  SCULPT_BRUSH_TYPE_MULTIPLANE_SCRAPE = 23,
  SCULPT_BRUSH_TYPE_SLIDE_RELAX = 24,
  SCULPT_BRUSH_TYPE_CLAY_THUMB = 25,
  SCULPT_BRUSH_TYPE_CLOTH = 26,
  SCULPT_BRUSH_TYPE_DRAW_FACE_SETS = 27,
  SCULPT_BRUSH_TYPE_PAINT = 28,
  SCULPT_BRUSH_TYPE_SMEAR = 29,
  SCULPT_BRUSH_TYPE_BOUNDARY = 30,
  SCULPT_BRUSH_TYPE_DISPLACEMENT_ERASER = 31,
  SCULPT_BRUSH_TYPE_DISPLACEMENT_SMEAR = 32,
  SCULPT_BRUSH_TYPE_PLANE = 33,
  SCULPT_BRUSH_TYPE_BLUR = 34,
  SCULPT_BRUSH_TYPE_SCENE_PROJECT = 35,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L449—L489</summary>

<!-- original:1cf860181882f7:source/blender/makesdna/DNA_brush_enums.h:449:489 -->

```cpp
enum eBrushSculptType : char {
  SCULPT_BRUSH_TYPE_DRAW = 1,
  SCULPT_BRUSH_TYPE_SMOOTH = 2,
  SCULPT_BRUSH_TYPE_PINCH = 3,
  SCULPT_BRUSH_TYPE_INFLATE = 4,
  SCULPT_BRUSH_TYPE_GRAB = 5,
  SCULPT_BRUSH_TYPE_LAYER = 6,
#ifdef DNA_DEPRECATED_ALLOW
  SCULPT_BRUSH_TYPE_FLATTEN = 7,
#endif
  SCULPT_BRUSH_TYPE_CLAY = 8,
#ifdef DNA_DEPRECATED_ALLOW
  SCULPT_BRUSH_TYPE_FILL = 9,
  SCULPT_BRUSH_TYPE_SCRAPE = 10,
#endif
  SCULPT_BRUSH_TYPE_NUDGE = 11,
  SCULPT_BRUSH_TYPE_THUMB = 12,
  SCULPT_BRUSH_TYPE_SNAKE_HOOK = 13,
  SCULPT_BRUSH_TYPE_ROTATE = 14,
  SCULPT_BRUSH_TYPE_SIMPLIFY = 15,
  SCULPT_BRUSH_TYPE_CREASE = 16,
  SCULPT_BRUSH_TYPE_BLOB = 17,
  SCULPT_BRUSH_TYPE_CLAY_STRIPS = 18,
  SCULPT_BRUSH_TYPE_MASK = 19,
  SCULPT_BRUSH_TYPE_DRAW_SHARP = 20,
  SCULPT_BRUSH_TYPE_ELASTIC_DEFORM = 21,
  SCULPT_BRUSH_TYPE_POSE = 22,
  SCULPT_BRUSH_TYPE_MULTIPLANE_SCRAPE = 23,
  SCULPT_BRUSH_TYPE_SLIDE_RELAX = 24,
  SCULPT_BRUSH_TYPE_CLAY_THUMB = 25,
  SCULPT_BRUSH_TYPE_CLOTH = 26,
  SCULPT_BRUSH_TYPE_DRAW_FACE_SETS = 27,
  SCULPT_BRUSH_TYPE_PAINT = 28,
  SCULPT_BRUSH_TYPE_SMEAR = 29,
  SCULPT_BRUSH_TYPE_BOUNDARY = 30,
  SCULPT_BRUSH_TYPE_DISPLACEMENT_ERASER = 31,
  SCULPT_BRUSH_TYPE_DISPLACEMENT_SMEAR = 32,
  SCULPT_BRUSH_TYPE_PLANE = 33,
  SCULPT_BRUSH_TYPE_BLUR = 34,
  SCULPT_BRUSH_TYPE_SCENE_PROJECT = 35,
};
```

</details>


<a id="t-74039708fa04"></a>

### `blender::eBrushCurvesSculptType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L492—L505。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:0a50fe3f6446d9 -->

```cpp
enum eBrushCurvesSculptType : char {
  CURVES_SCULPT_BRUSH_TYPE_COMB = 0,
  CURVES_SCULPT_BRUSH_TYPE_DELETE = 1,
  CURVES_SCULPT_BRUSH_TYPE_SNAKE_HOOK = 2,
  CURVES_SCULPT_BRUSH_TYPE_ADD = 3,
  CURVES_SCULPT_BRUSH_TYPE_GROW_SHRINK = 4,
  CURVES_SCULPT_BRUSH_TYPE_SELECTION_PAINT = 5,
  CURVES_SCULPT_BRUSH_TYPE_PINCH = 6,
  CURVES_SCULPT_BRUSH_TYPE_SMOOTH = 7,
  CURVES_SCULPT_BRUSH_TYPE_PUFF = 8,
  CURVES_SCULPT_BRUSH_TYPE_DENSITY = 9,
  CURVES_SCULPT_BRUSH_TYPE_SLIDE = 10,
  CURVES_SCULPT_BRUSH_TYPE_CUT = 11,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L492—L505</summary>

<!-- original:0a50fe3f6446d9:source/blender/makesdna/DNA_brush_enums.h:492:505 -->

```cpp
enum eBrushCurvesSculptType : char {
  CURVES_SCULPT_BRUSH_TYPE_COMB = 0,
  CURVES_SCULPT_BRUSH_TYPE_DELETE = 1,
  CURVES_SCULPT_BRUSH_TYPE_SNAKE_HOOK = 2,
  CURVES_SCULPT_BRUSH_TYPE_ADD = 3,
  CURVES_SCULPT_BRUSH_TYPE_GROW_SHRINK = 4,
  CURVES_SCULPT_BRUSH_TYPE_SELECTION_PAINT = 5,
  CURVES_SCULPT_BRUSH_TYPE_PINCH = 6,
  CURVES_SCULPT_BRUSH_TYPE_SMOOTH = 7,
  CURVES_SCULPT_BRUSH_TYPE_PUFF = 8,
  CURVES_SCULPT_BRUSH_TYPE_DENSITY = 9,
  CURVES_SCULPT_BRUSH_TYPE_SLIDE = 10,
  CURVES_SCULPT_BRUSH_TYPE_CUT = 11,
};
```

</details>


<a id="t-534582393ac0"></a>

### `blender::eBrushImagePaintType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L508—L515。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:f693f91a5e25cf -->

```cpp
enum eBrushImagePaintType : char {
  IMAGE_PAINT_BRUSH_TYPE_DRAW = 0,
  IMAGE_PAINT_BRUSH_TYPE_SOFTEN = 1,
  IMAGE_PAINT_BRUSH_TYPE_SMEAR = 2,
  IMAGE_PAINT_BRUSH_TYPE_CLONE = 3,
  IMAGE_PAINT_BRUSH_TYPE_FILL = 4,
  IMAGE_PAINT_BRUSH_TYPE_MASK = 5,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L508—L515</summary>

<!-- original:f693f91a5e25cf:source/blender/makesdna/DNA_brush_enums.h:508:515 -->

```cpp
enum eBrushImagePaintType : char {
  IMAGE_PAINT_BRUSH_TYPE_DRAW = 0,
  IMAGE_PAINT_BRUSH_TYPE_SOFTEN = 1,
  IMAGE_PAINT_BRUSH_TYPE_SMEAR = 2,
  IMAGE_PAINT_BRUSH_TYPE_CLONE = 3,
  IMAGE_PAINT_BRUSH_TYPE_FILL = 4,
  IMAGE_PAINT_BRUSH_TYPE_MASK = 5,
};
```

</details>


<a id="t-4f63101759d2"></a>

### `blender::eBrushVertexPaintType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L521—L526。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:b9884ba08799a2 -->

```cpp
enum eBrushVertexPaintType : char {
  VPAINT_BRUSH_TYPE_DRAW = 0,
  VPAINT_BRUSH_TYPE_BLUR = 1,
  VPAINT_BRUSH_TYPE_AVERAGE = 2,
  VPAINT_BRUSH_TYPE_SMEAR = 3,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L521—L526</summary>

<!-- original:b9884ba08799a2:source/blender/makesdna/DNA_brush_enums.h:521:526 -->

```cpp
enum eBrushVertexPaintType : char {
  VPAINT_BRUSH_TYPE_DRAW = 0,
  VPAINT_BRUSH_TYPE_BLUR = 1,
  VPAINT_BRUSH_TYPE_AVERAGE = 2,
  VPAINT_BRUSH_TYPE_SMEAR = 3,
};
```

</details>


<a id="t-0e7152a0c75f"></a>

### `blender::eBrushWeightPaintType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L530—L535。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:7301114fcbe8c6 -->

```cpp
enum eBrushWeightPaintType : char {
  WPAINT_BRUSH_TYPE_DRAW = 0,
  WPAINT_BRUSH_TYPE_BLUR = 1,
  WPAINT_BRUSH_TYPE_AVERAGE = 2,
  WPAINT_BRUSH_TYPE_SMEAR = 3,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L530—L535</summary>

<!-- original:7301114fcbe8c6:source/blender/makesdna/DNA_brush_enums.h:530:535 -->

```cpp
enum eBrushWeightPaintType : char {
  WPAINT_BRUSH_TYPE_DRAW = 0,
  WPAINT_BRUSH_TYPE_BLUR = 1,
  WPAINT_BRUSH_TYPE_AVERAGE = 2,
  WPAINT_BRUSH_TYPE_SMEAR = 3,
};
```

</details>


<a id="t-0cccfb414fad"></a>

### `blender::eBrushGPaintType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L538—L543。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:3dc1e42cc7520e -->

```cpp
enum eBrushGPaintType : char {
  GPAINT_BRUSH_TYPE_DRAW = 0,
  GPAINT_BRUSH_TYPE_FILL = 1,
  GPAINT_BRUSH_TYPE_ERASE = 2,
  GPAINT_BRUSH_TYPE_TINT = 3,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L538—L543</summary>

<!-- original:3dc1e42cc7520e:source/blender/makesdna/DNA_brush_enums.h:538:543 -->

```cpp
enum eBrushGPaintType : char {
  GPAINT_BRUSH_TYPE_DRAW = 0,
  GPAINT_BRUSH_TYPE_FILL = 1,
  GPAINT_BRUSH_TYPE_ERASE = 2,
  GPAINT_BRUSH_TYPE_TINT = 3,
};
```

</details>


<a id="t-dbc32878cca0"></a>

### `blender::eBrushGPVertexType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L546—L553。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:cecf1eaac799be -->

```cpp
enum eBrushGPVertexType : char {
  GPVERTEX_BRUSH_TYPE_DRAW = 0,
  GPVERTEX_BRUSH_TYPE_BLUR = 1,
  GPVERTEX_BRUSH_TYPE_AVERAGE = 2,
  GPVERTEX_BRUSH_TYPE_TINT = 3,
  GPVERTEX_BRUSH_TYPE_SMEAR = 4,
  GPVERTEX_BRUSH_TYPE_REPLACE = 5,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L546—L553</summary>

<!-- original:cecf1eaac799be:source/blender/makesdna/DNA_brush_enums.h:546:553 -->

```cpp
enum eBrushGPVertexType : char {
  GPVERTEX_BRUSH_TYPE_DRAW = 0,
  GPVERTEX_BRUSH_TYPE_BLUR = 1,
  GPVERTEX_BRUSH_TYPE_AVERAGE = 2,
  GPVERTEX_BRUSH_TYPE_TINT = 3,
  GPVERTEX_BRUSH_TYPE_SMEAR = 4,
  GPVERTEX_BRUSH_TYPE_REPLACE = 5,
};
```

</details>


<a id="t-c72f8fa90d69"></a>

### `blender::eBrushGPSculptType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L556—L566。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:1292127f3e167e -->

```cpp
enum eBrushGPSculptType : char {
  GPSCULPT_BRUSH_TYPE_SMOOTH = 0,
  GPSCULPT_BRUSH_TYPE_THICKNESS = 1,
  GPSCULPT_BRUSH_TYPE_STRENGTH = 2,
  GPSCULPT_BRUSH_TYPE_GRAB = 3,
  GPSCULPT_BRUSH_TYPE_PUSH = 4,
  GPSCULPT_BRUSH_TYPE_TWIST = 5,
  GPSCULPT_BRUSH_TYPE_PINCH = 6,
  GPSCULPT_BRUSH_TYPE_RANDOMIZE = 7,
  GPSCULPT_BRUSH_TYPE_CLONE = 8,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L556—L566</summary>

<!-- original:1292127f3e167e:source/blender/makesdna/DNA_brush_enums.h:556:566 -->

```cpp
enum eBrushGPSculptType : char {
  GPSCULPT_BRUSH_TYPE_SMOOTH = 0,
  GPSCULPT_BRUSH_TYPE_THICKNESS = 1,
  GPSCULPT_BRUSH_TYPE_STRENGTH = 2,
  GPSCULPT_BRUSH_TYPE_GRAB = 3,
  GPSCULPT_BRUSH_TYPE_PUSH = 4,
  GPSCULPT_BRUSH_TYPE_TWIST = 5,
  GPSCULPT_BRUSH_TYPE_PINCH = 6,
  GPSCULPT_BRUSH_TYPE_RANDOMIZE = 7,
  GPSCULPT_BRUSH_TYPE_CLONE = 8,
};
```

</details>


<a id="t-e763969ead9b"></a>

### `blender::eBrushGPWeightType`

原始声明：[source/blender/makesdna/DNA_brush_enums.h](../../../../../../../source/blender/makesdna/DNA_brush_enums.h) · L569—L574。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:8f7451713d56d6 -->

```cpp
enum eBrushGPWeightType : char {
  GPWEIGHT_BRUSH_TYPE_DRAW = 0,
  GPWEIGHT_BRUSH_TYPE_BLUR = 1,
  GPWEIGHT_BRUSH_TYPE_AVERAGE = 2,
  GPWEIGHT_BRUSH_TYPE_SMEAR = 3,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_brush_enums.h · L569—L574</summary>

<!-- original:8f7451713d56d6:source/blender/makesdna/DNA_brush_enums.h:569:574 -->

```cpp
enum eBrushGPWeightType : char {
  GPWEIGHT_BRUSH_TYPE_DRAW = 0,
  GPWEIGHT_BRUSH_TYPE_BLUR = 1,
  GPWEIGHT_BRUSH_TYPE_AVERAGE = 2,
  GPWEIGHT_BRUSH_TYPE_SMEAR = 3,
};
```

</details>


## 完整成员与函数实现
