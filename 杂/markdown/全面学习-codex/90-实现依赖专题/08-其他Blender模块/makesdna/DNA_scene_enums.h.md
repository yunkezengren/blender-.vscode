# 实现依赖专题：source/blender/makesdna/DNA_scene_enums.h

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_scene_enums.h"]:::abstraction
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
  F["DNA_scene_enums.h实现"]:::compute
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

<a id="t-469710adad0d"></a>

### `blender::eUnifiedPaintSettingsFlags`

原始声明：[source/blender/makesdna/DNA_scene_enums.h](../../../../../../../source/blender/makesdna/DNA_scene_enums.h) · L61—L77。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:f1354880eda27b -->

```cpp
enum eUnifiedPaintSettingsFlags : int {
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_SIZE */
  UNIFIED_PAINT_SIZE_DEPRECATED = (1 << 0),
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_ALPHA */
  UNIFIED_PAINT_ALPHA_DEPRECATED = (1 << 1),
  /** Only used if per-brush unified size is enabled, mirrors the brush flag #BRUSH_LOCK_SIZE. */
  UNIFIED_PAINT_BRUSH_LOCK_SIZE = (1 << 2),
  UNIFIED_PAINT_FLAG_UNUSED_0 = (1 << 3),
  UNIFIED_PAINT_FLAG_UNUSED_1 = (1 << 4),
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_WEIGHT */
  UNIFIED_PAINT_WEIGHT_DEPRECATED = (1 << 5),
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_COLOR */
  UNIFIED_PAINT_COLOR_DEPRECATED = (1 << 6),
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_INPUT_SAMPLES */
  UNIFIED_PAINT_INPUT_SAMPLES_DEPRECATED = (1 << 7),
  UNIFIED_PAINT_COLOR_JITTER = (1 << 8),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_scene_enums.h · L61—L77</summary>

<!-- original:f1354880eda27b:source/blender/makesdna/DNA_scene_enums.h:61:77 -->

```cpp
enum eUnifiedPaintSettingsFlags : int {
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_SIZE */
  UNIFIED_PAINT_SIZE_DEPRECATED = (1 << 0),
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_ALPHA */
  UNIFIED_PAINT_ALPHA_DEPRECATED = (1 << 1),
  /** Only used if per-brush unified size is enabled, mirrors the brush flag #BRUSH_LOCK_SIZE. */
  UNIFIED_PAINT_BRUSH_LOCK_SIZE = (1 << 2),
  UNIFIED_PAINT_FLAG_UNUSED_0 = (1 << 3),
  UNIFIED_PAINT_FLAG_UNUSED_1 = (1 << 4),
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_WEIGHT */
  UNIFIED_PAINT_WEIGHT_DEPRECATED = (1 << 5),
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_COLOR */
  UNIFIED_PAINT_COLOR_DEPRECATED = (1 << 6),
  /* DEPRECATED: migrated to per-brush flag BRUSH_USE_UNIFIED_PAINT_INPUT_SAMPLES */
  UNIFIED_PAINT_INPUT_SAMPLES_DEPRECATED = (1 << 7),
  UNIFIED_PAINT_COLOR_JITTER = (1 << 8),
};
```

</details>


<a id="t-d383d800204e"></a>

### `blender::eStereoDisplayMode`

原始声明：[source/blender/makesdna/DNA_scene_enums.h](../../../../../../../source/blender/makesdna/DNA_scene_enums.h) · L221—L227。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:fd30677e45f88c -->

```cpp
enum eStereoDisplayMode : char {
  S3D_DISPLAY_ANAGLYPH = 0,
  S3D_DISPLAY_INTERLACE = 1,
  S3D_DISPLAY_PAGEFLIP = 2,
  S3D_DISPLAY_SIDEBYSIDE = 3,
  S3D_DISPLAY_TOPBOTTOM = 4,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_scene_enums.h · L221—L227</summary>

<!-- original:fd30677e45f88c:source/blender/makesdna/DNA_scene_enums.h:221:227 -->

```cpp
enum eStereoDisplayMode : char {
  S3D_DISPLAY_ANAGLYPH = 0,
  S3D_DISPLAY_INTERLACE = 1,
  S3D_DISPLAY_PAGEFLIP = 2,
  S3D_DISPLAY_SIDEBYSIDE = 3,
  S3D_DISPLAY_TOPBOTTOM = 4,
};
```

</details>


<a id="t-a184353c1c92"></a>

### `blender::eStereo3dAnaglyphType`

原始声明：[source/blender/makesdna/DNA_scene_enums.h](../../../../../../../source/blender/makesdna/DNA_scene_enums.h) · L238—L242。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:978e1f2980e976 -->

```cpp
enum eStereo3dAnaglyphType : char {
  S3D_ANAGLYPH_REDCYAN = 0,
  S3D_ANAGLYPH_GREENMAGENTA = 1,
  S3D_ANAGLYPH_YELLOWBLUE = 2,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_scene_enums.h · L238—L242</summary>

<!-- original:978e1f2980e976:source/blender/makesdna/DNA_scene_enums.h:238:242 -->

```cpp
enum eStereo3dAnaglyphType : char {
  S3D_ANAGLYPH_REDCYAN = 0,
  S3D_ANAGLYPH_GREENMAGENTA = 1,
  S3D_ANAGLYPH_YELLOWBLUE = 2,
};
```

</details>


<a id="t-678c71b454f2"></a>

### `blender::eStereo3dInterlaceType`

原始声明：[source/blender/makesdna/DNA_scene_enums.h](../../../../../../../source/blender/makesdna/DNA_scene_enums.h) · L245—L249。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:bed71734c8a773 -->

```cpp
enum eStereo3dInterlaceType : char {
  S3D_INTERLACE_ROW = 0,
  S3D_INTERLACE_COLUMN = 1,
  S3D_INTERLACE_CHECKERBOARD = 2,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_scene_enums.h · L245—L249</summary>

<!-- original:bed71734c8a773:source/blender/makesdna/DNA_scene_enums.h:245:249 -->

```cpp
enum eStereo3dInterlaceType : char {
  S3D_INTERLACE_ROW = 0,
  S3D_INTERLACE_COLUMN = 1,
  S3D_INTERLACE_CHECKERBOARD = 2,
};
```

</details>


## 完整成员与函数实现
