# 实现依赖专题：source/blender/makesdna/DNA_space_enums.h

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_space_enums.h"]:::abstraction
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
  F["DNA_space_enums.h实现"]:::compute
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

<a id="t-9357a943dafe"></a>

### `blender::eSpaceButtons_Context`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L95—L121。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:4bf26028d8e28b -->

```cpp
enum eSpaceButtons_Context : short {
  BCONTEXT_SEPARATOR = -1,
  BCONTEXT_RENDER = 0,
  BCONTEXT_SCENE = 1,
  BCONTEXT_WORLD = 2,
  BCONTEXT_OBJECT = 3,
  BCONTEXT_DATA = 4,
  BCONTEXT_MATERIAL = 5,
  BCONTEXT_TEXTURE = 6,
  BCONTEXT_PARTICLE = 7,
  BCONTEXT_PHYSICS = 8,
  BCONTEXT_BONE = 9,
  BCONTEXT_MODIFIER = 10,
  BCONTEXT_CONSTRAINT = 11,
  BCONTEXT_BONE_CONSTRAINT = 12,
  BCONTEXT_VIEW_LAYER = 13,
  BCONTEXT_TOOL = 14,
  BCONTEXT_SHADERFX = 15,
  BCONTEXT_OUTPUT = 16,
  BCONTEXT_COLLECTION = 17,
  BCONTEXT_STRIP = 18,
  BCONTEXT_STRIP_MODIFIER = 19,
  BCONTEXT_COMPOSITOR = 20,

  /* Keep last. */
  BCONTEXT_TOT,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L95—L121</summary>

<!-- original:4bf26028d8e28b:source/blender/makesdna/DNA_space_enums.h:95:121 -->

```cpp
enum eSpaceButtons_Context : short {
  BCONTEXT_SEPARATOR = -1,
  BCONTEXT_RENDER = 0,
  BCONTEXT_SCENE = 1,
  BCONTEXT_WORLD = 2,
  BCONTEXT_OBJECT = 3,
  BCONTEXT_DATA = 4,
  BCONTEXT_MATERIAL = 5,
  BCONTEXT_TEXTURE = 6,
  BCONTEXT_PARTICLE = 7,
  BCONTEXT_PHYSICS = 8,
  BCONTEXT_BONE = 9,
  BCONTEXT_MODIFIER = 10,
  BCONTEXT_CONSTRAINT = 11,
  BCONTEXT_BONE_CONSTRAINT = 12,
  BCONTEXT_VIEW_LAYER = 13,
  BCONTEXT_TOOL = 14,
  BCONTEXT_SHADERFX = 15,
  BCONTEXT_OUTPUT = 16,
  BCONTEXT_COLLECTION = 17,
  BCONTEXT_STRIP = 18,
  BCONTEXT_STRIP_MODIFIER = 19,
  BCONTEXT_COMPOSITOR = 20,

  /* Keep last. */
  BCONTEXT_TOT,
};
```

</details>


<a id="t-316e46d625de"></a>

### `blender::eSpaceOutliner_Filter`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L171—L210。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:e250e49827ada4 -->

```cpp
enum eSpaceOutliner_Filter : int {
  SO_FILTER_SEARCH = (1 << 0), /* Run-time flag. */
  SO_FILTER_CLEARED_1 = (1 << 1),
  SO_FILTER_NO_OBJECT = (1 << 2),
  SO_FILTER_NO_OB_CONTENT = (1 << 3), /* Not only mesh, but modifiers, constraints, ... */
  SO_FILTER_NO_CHILDREN = (1 << 4),

  SO_FILTER_UNUSED_5 = (1 << 5), /* cleared */
  /** Show overrides that are defined/controlled by Blender. */
  SO_FILTER_SHOW_SYSTEM_OVERRIDES = SO_FILTER_UNUSED_5, /* re-use */
  SO_FILTER_NO_OB_MESH = (1 << 6),
  SO_FILTER_NO_OB_ARMATURE = (1 << 7),
  SO_FILTER_NO_OB_EMPTY = (1 << 8),
  SO_FILTER_NO_OB_LAMP = (1 << 9),
  SO_FILTER_NO_OB_CAMERA = (1 << 10),
  SO_FILTER_NO_OB_OTHERS = (1 << 11),

  SO_FILTER_OB_STATE_SELECTABLE = (1 << 12), /* Not set via DNA. */
  SO_FILTER_OB_STATE_VISIBLE = (1 << 13),    /* Not set via DNA. */
  SO_FILTER_OB_STATE_INVERSE = (1 << 14),
  SO_FILTER_OB_STATE_SELECTED = (1 << 15), /* Not set via DNA. */
  SO_FILTER_OB_STATE_ACTIVE = (1 << 16),   /* Not set via DNA. */
  SO_FILTER_NO_COLLECTION = (1 << 17),
  SO_FILTER_NO_VIEW_LAYERS = (1 << 18),

  SO_FILTER_ID_TYPE = (1 << 19),

  SO_FILTER_NO_OB_GREASE_PENCIL = (1 << 20),

  SO_FILTER_NO_OB_DATA = (1 << 21),
  SO_FILTER_NO_OB_ANIMATION = (1 << 22),
  SO_FILTER_NO_OB_CONSTRAINTS = (1 << 23),
  SO_FILTER_NO_OB_SHAPE_KEYS = (1 << 24),
  SO_FILTER_NO_OB_MATERIAL = (1 << 25),
  SO_FILTER_NO_OB_DEFGROUP = (1 << 26),
  SO_FILTER_NO_OB_MODIFIERS = (1 << 27),
  SO_FILTER_NO_ARMATURE_BONE_COLLECTION = (1 << 28),
  SO_FILTER_NO_GREASE_PENCIL_EFFECTS = (1 << 29),
  SO_FILTER_NO_POSE_BONES = (1 << 30),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L171—L210</summary>

<!-- original:e250e49827ada4:source/blender/makesdna/DNA_space_enums.h:171:210 -->

```cpp
enum eSpaceOutliner_Filter : int {
  SO_FILTER_SEARCH = (1 << 0), /* Run-time flag. */
  SO_FILTER_CLEARED_1 = (1 << 1),
  SO_FILTER_NO_OBJECT = (1 << 2),
  SO_FILTER_NO_OB_CONTENT = (1 << 3), /* Not only mesh, but modifiers, constraints, ... */
  SO_FILTER_NO_CHILDREN = (1 << 4),

  SO_FILTER_UNUSED_5 = (1 << 5), /* cleared */
  /** Show overrides that are defined/controlled by Blender. */
  SO_FILTER_SHOW_SYSTEM_OVERRIDES = SO_FILTER_UNUSED_5, /* re-use */
  SO_FILTER_NO_OB_MESH = (1 << 6),
  SO_FILTER_NO_OB_ARMATURE = (1 << 7),
  SO_FILTER_NO_OB_EMPTY = (1 << 8),
  SO_FILTER_NO_OB_LAMP = (1 << 9),
  SO_FILTER_NO_OB_CAMERA = (1 << 10),
  SO_FILTER_NO_OB_OTHERS = (1 << 11),

  SO_FILTER_OB_STATE_SELECTABLE = (1 << 12), /* Not set via DNA. */
  SO_FILTER_OB_STATE_VISIBLE = (1 << 13),    /* Not set via DNA. */
  SO_FILTER_OB_STATE_INVERSE = (1 << 14),
  SO_FILTER_OB_STATE_SELECTED = (1 << 15), /* Not set via DNA. */
  SO_FILTER_OB_STATE_ACTIVE = (1 << 16),   /* Not set via DNA. */
  SO_FILTER_NO_COLLECTION = (1 << 17),
  SO_FILTER_NO_VIEW_LAYERS = (1 << 18),

  SO_FILTER_ID_TYPE = (1 << 19),

  SO_FILTER_NO_OB_GREASE_PENCIL = (1 << 20),

  SO_FILTER_NO_OB_DATA = (1 << 21),
  SO_FILTER_NO_OB_ANIMATION = (1 << 22),
  SO_FILTER_NO_OB_CONSTRAINTS = (1 << 23),
  SO_FILTER_NO_OB_SHAPE_KEYS = (1 << 24),
  SO_FILTER_NO_OB_MATERIAL = (1 << 25),
  SO_FILTER_NO_OB_DEFGROUP = (1 << 26),
  SO_FILTER_NO_OB_MODIFIERS = (1 << 27),
  SO_FILTER_NO_ARMATURE_BONE_COLLECTION = (1 << 28),
  SO_FILTER_NO_GREASE_PENCIL_EFFECTS = (1 << 29),
  SO_FILTER_NO_POSE_BONES = (1 << 30),
};
```

</details>


<a id="t-632360171f39"></a>

### `blender::eSpaceSeq_SequencerPreviewOverlay_Flag`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L398—L406。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:45991104839ca1 -->

```cpp
enum eSpaceSeq_SequencerPreviewOverlay_Flag : int {
  SEQ_PREVIEW_SHOW_2D_CURSOR = (1 << 1),
  SEQ_PREVIEW_SHOW_OUTLINE_SELECTED = (1 << 2),
  SEQ_PREVIEW_SHOW_SAFE_MARGINS = (1 << 3),
  SEQ_PREVIEW_SHOW_GPENCIL = (1 << 4),
  SEQ_PREVIEW_SHOW_SAFE_CENTER = (1 << 9),
  SEQ_PREVIEW_SHOW_METADATA = (1 << 10),
  SEQ_PREVIEW_SHOW_COMPOSITION_GUIDES = (1 << 11),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L398—L406</summary>

<!-- original:45991104839ca1:source/blender/makesdna/DNA_space_enums.h:398:406 -->

```cpp
enum eSpaceSeq_SequencerPreviewOverlay_Flag : int {
  SEQ_PREVIEW_SHOW_2D_CURSOR = (1 << 1),
  SEQ_PREVIEW_SHOW_OUTLINE_SELECTED = (1 << 2),
  SEQ_PREVIEW_SHOW_SAFE_MARGINS = (1 << 3),
  SEQ_PREVIEW_SHOW_GPENCIL = (1 << 4),
  SEQ_PREVIEW_SHOW_SAFE_CENTER = (1 << 9),
  SEQ_PREVIEW_SHOW_METADATA = (1 << 10),
  SEQ_PREVIEW_SHOW_COMPOSITION_GUIDES = (1 << 11),
};
```

</details>


<a id="t-d63b1fb11134"></a>

### `blender::eSpaceSeq_SequencerTimelineOverlay_Flag`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L410—L434。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:187d9d468c77e8 -->

```cpp
enum eSpaceSeq_SequencerTimelineOverlay_Flag : int {
  SEQ_TIMELINE_SHOW_STRIP_OFFSETS = (1 << 1),
  /** Show thumbnails only at ends of a strip. */
  SEQ_TIMELINE_STRIP_END_THUMBNAILS = (1 << 2),
  /** Use #Strip::color_tag */
  SEQ_TIMELINE_SHOW_STRIP_COLOR_TAG = (1 << 3),
  SEQ_TIMELINE_SHOW_STRIP_RETIMING = (1 << 4),
  SEQ_TIMELINE_SHOW_FCURVES = (1 << 5),
  /** Draw all wave-forms. */
  SEQ_TIMELINE_ALL_WAVEFORMS = (1 << 7),
  /** Draw no wave-forms. */
  SEQ_TIMELINE_NO_WAVEFORMS = (1 << 8),
  /** Draw only upper part of the waveform, showing absolute signal value. */
  SEQ_TIMELINE_WAVEFORMS_HALF = (1 << 9),
  SEQ_TIMELINE_SHOW_STRIP_NAME = (1 << 14),
  SEQ_TIMELINE_SHOW_STRIP_SOURCE = (1 << 15),
  SEQ_TIMELINE_SHOW_STRIP_DURATION = (1 << 16),
  SEQ_TIMELINE_SHOW_GRID = (1 << 18),
  /** Show continuous sequence of thumbnails. */
  SEQ_TIMELINE_CONTINUOUS_THUMBNAILS = (1 << 19),
  /** Show a single thumbnail in the middle. */
  SEQ_TIMELINE_MIDDLE_THUMBNAILS = (1 << 20),
  /** Draw thumbnails on strips. */
  SEQ_TIMELINE_SHOW_THUMBNAILS = (1 << 21),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L410—L434</summary>

<!-- original:187d9d468c77e8:source/blender/makesdna/DNA_space_enums.h:410:434 -->

```cpp
enum eSpaceSeq_SequencerTimelineOverlay_Flag : int {
  SEQ_TIMELINE_SHOW_STRIP_OFFSETS = (1 << 1),
  /** Show thumbnails only at ends of a strip. */
  SEQ_TIMELINE_STRIP_END_THUMBNAILS = (1 << 2),
  /** Use #Strip::color_tag */
  SEQ_TIMELINE_SHOW_STRIP_COLOR_TAG = (1 << 3),
  SEQ_TIMELINE_SHOW_STRIP_RETIMING = (1 << 4),
  SEQ_TIMELINE_SHOW_FCURVES = (1 << 5),
  /** Draw all wave-forms. */
  SEQ_TIMELINE_ALL_WAVEFORMS = (1 << 7),
  /** Draw no wave-forms. */
  SEQ_TIMELINE_NO_WAVEFORMS = (1 << 8),
  /** Draw only upper part of the waveform, showing absolute signal value. */
  SEQ_TIMELINE_WAVEFORMS_HALF = (1 << 9),
  SEQ_TIMELINE_SHOW_STRIP_NAME = (1 << 14),
  SEQ_TIMELINE_SHOW_STRIP_SOURCE = (1 << 15),
  SEQ_TIMELINE_SHOW_STRIP_DURATION = (1 << 16),
  SEQ_TIMELINE_SHOW_GRID = (1 << 18),
  /** Show continuous sequence of thumbnails. */
  SEQ_TIMELINE_CONTINUOUS_THUMBNAILS = (1 << 19),
  /** Show a single thumbnail in the middle. */
  SEQ_TIMELINE_MIDDLE_THUMBNAILS = (1 << 20),
  /** Draw thumbnails on strips. */
  SEQ_TIMELINE_SHOW_THUMBNAILS = (1 << 21),
};
```

</details>


<a id="t-ed8f998c72dd"></a>

### `blender::eSpaceSeq_RegionType`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L448—L454。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:c927f63ca0ae9e -->

```cpp
enum eSpaceSeq_RegionType : short {
  SEQ_DRAW_IMG_IMBUF = 1,
  SEQ_DRAW_IMG_WAVEFORM = 2,
  SEQ_DRAW_IMG_VECTORSCOPE = 3,
  SEQ_DRAW_IMG_HISTOGRAM = 4,
  SEQ_DRAW_IMG_RGBPARADE = 5,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L448—L454</summary>

<!-- original:c927f63ca0ae9e:source/blender/makesdna/DNA_space_enums.h:448:454 -->

```cpp
enum eSpaceSeq_RegionType : short {
  SEQ_DRAW_IMG_IMBUF = 1,
  SEQ_DRAW_IMG_WAVEFORM = 2,
  SEQ_DRAW_IMG_VECTORSCOPE = 3,
  SEQ_DRAW_IMG_HISTOGRAM = 4,
  SEQ_DRAW_IMG_RGBPARADE = 5,
};
```

</details>


<a id="t-c81619ada859"></a>

### `blender::eSpaceSeq_Flag`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L465—L483。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:2efad6f8fc08f2 -->

```cpp
enum eSpaceSeq_Flag : int {
  SEQ_DRAWFRAMES = (1 << 0),
  SEQ_MARKER_TRANS = (1 << 1),
  SEQ_DRAW_COLOR_SEPARATED_UNUSED_2 = (1 << 2),
  SEQ_CLAMP_VIEW = (1 << 3),
  SPACE_SEQ_DESELECT_STRIP_HANDLE = (1 << 4),
  SPACE_SEQ_FLAG_UNUSED_5 = (1 << 5),
  SEQ_USE_ALPHA = (1 << 6), /* use RGBA display mode for preview */
  SPACE_SEQ_FLAG_UNUSED_10 = (1 << 10),
  SEQ_SHOW_MARKERS = (1 << 11), /* show markers region */
  SEQ_ZOOM_TO_FIT = (1 << 12),
  SEQ_SHOW_OVERLAY = (1 << 13),
  SPACE_SEQ_FLAG_UNUSED_14 = (1 << 14),
  SPACE_SEQ_FLAG_UNUSED_15 = (1 << 15),
  SPACE_SEQ_FLAG_UNUSED_16 = (1 << 16),
  SEQ_USE_PROXIES = (1 << 17),
  SEQ_SHOW_GRID = (1 << 18),
  SEQ_SHOW_SCRUBBING_REGION = (1 << 19),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L465—L483</summary>

<!-- original:2efad6f8fc08f2:source/blender/makesdna/DNA_space_enums.h:465:483 -->

```cpp
enum eSpaceSeq_Flag : int {
  SEQ_DRAWFRAMES = (1 << 0),
  SEQ_MARKER_TRANS = (1 << 1),
  SEQ_DRAW_COLOR_SEPARATED_UNUSED_2 = (1 << 2),
  SEQ_CLAMP_VIEW = (1 << 3),
  SPACE_SEQ_DESELECT_STRIP_HANDLE = (1 << 4),
  SPACE_SEQ_FLAG_UNUSED_5 = (1 << 5),
  SEQ_USE_ALPHA = (1 << 6), /* use RGBA display mode for preview */
  SPACE_SEQ_FLAG_UNUSED_10 = (1 << 10),
  SEQ_SHOW_MARKERS = (1 << 11), /* show markers region */
  SEQ_ZOOM_TO_FIT = (1 << 12),
  SEQ_SHOW_OVERLAY = (1 << 13),
  SPACE_SEQ_FLAG_UNUSED_14 = (1 << 14),
  SPACE_SEQ_FLAG_UNUSED_15 = (1 << 15),
  SPACE_SEQ_FLAG_UNUSED_16 = (1 << 16),
  SEQ_USE_PROXIES = (1 << 17),
  SEQ_SHOW_GRID = (1 << 18),
  SEQ_SHOW_SCRUBBING_REGION = (1 << 19),
};
```

</details>


<a id="t-140c06c16c9b"></a>

### `blender::eSpaceSeq_Displays`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L487—L491。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:a3825a6b747642 -->

```cpp
enum eSpaceSeq_Displays : char {
  SEQ_VIEW_SEQUENCE = 1,
  SEQ_VIEW_PREVIEW = 2,
  SEQ_VIEW_SEQUENCE_PREVIEW = 3,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L487—L491</summary>

<!-- original:a3825a6b747642:source/blender/makesdna/DNA_space_enums.h:487:491 -->

```cpp
enum eSpaceSeq_Displays : char {
  SEQ_VIEW_SEQUENCE = 1,
  SEQ_VIEW_PREVIEW = 2,
  SEQ_VIEW_SEQUENCE_PREVIEW = 3,
};
```

</details>


<a id="t-54b54442e42f"></a>

### `blender::eSpaceSeq_Proxy_RenderSize`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L494—L502。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:ab431a7f7740e6 -->

```cpp
enum eSpaceSeq_Proxy_RenderSize : short {
  SEQ_RENDER_SIZE_NONE = -1,
  SEQ_RENDER_SIZE_SCENE = 0,
  SEQ_RENDER_SIZE_PROXY_25 = 25,
  SEQ_RENDER_SIZE_PROXY_50 = 50,
  SEQ_RENDER_SIZE_PROXY_75 = 75,
  SEQ_RENDER_SIZE_PROXY_100 = 99,
  SEQ_RENDER_SIZE_FULL_DEPRECATED = 100, /* deprecated, for versioning only */
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L494—L502</summary>

<!-- original:ab431a7f7740e6:source/blender/makesdna/DNA_space_enums.h:494:502 -->

```cpp
enum eSpaceSeq_Proxy_RenderSize : short {
  SEQ_RENDER_SIZE_NONE = -1,
  SEQ_RENDER_SIZE_SCENE = 0,
  SEQ_RENDER_SIZE_PROXY_25 = 25,
  SEQ_RENDER_SIZE_PROXY_50 = 50,
  SEQ_RENDER_SIZE_PROXY_75 = 75,
  SEQ_RENDER_SIZE_PROXY_100 = 99,
  SEQ_RENDER_SIZE_FULL_DEPRECATED = 100, /* deprecated, for versioning only */
};
```

</details>


<a id="t-646d2f640782"></a>

### `blender::eFileBrowse_Mode`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L558—L563。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:90958f33a77d70 -->

```cpp
enum eFileBrowse_Mode : char {
  /* Regular Blender File Browser */
  FILE_BROWSE_MODE_FILES = 0,
  /* Asset Browser */
  FILE_BROWSE_MODE_ASSETS = 1,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L558—L563</summary>

<!-- original:90958f33a77d70:source/blender/makesdna/DNA_space_enums.h:558:563 -->

```cpp
enum eFileBrowse_Mode : char {
  /* Regular Blender File Browser */
  FILE_BROWSE_MODE_FILES = 0,
  /* Asset Browser */
  FILE_BROWSE_MODE_ASSETS = 1,
};
```

</details>


<a id="t-5ea57712cb35"></a>

### `blender::eDirEntry_SelectFlag`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L732—L737。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:c69b81eae624ec -->

```cpp
enum eDirEntry_SelectFlag : char {
  // FILE_SEL_ACTIVE = (1 << 1), /* UNUSED */
  FILE_SEL_HIGHLIGHTED = (1 << 2),
  FILE_SEL_SELECTED = (1 << 3),
  FILE_SEL_EDITING = (1 << 4),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L732—L737</summary>

<!-- original:c69b81eae624ec:source/blender/makesdna/DNA_space_enums.h:732:737 -->

```cpp
enum eDirEntry_SelectFlag : char {
  // FILE_SEL_ACTIVE = (1 << 1), /* UNUSED */
  FILE_SEL_HIGHLIGHTED = (1 << 2),
  FILE_SEL_SELECTED = (1 << 3),
  FILE_SEL_EDITING = (1 << 4),
};
```

</details>


<a id="t-85e86963ce65"></a>

### `blender::eSpaceImage_Mode`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L791—L796。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:f047b1fd97d683 -->

```cpp
enum eSpaceImage_Mode : char {
  SI_MODE_VIEW = 0,
  SI_MODE_PAINT = 1,
  SI_MODE_MASK = 2,
  SI_MODE_UV = 3,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L791—L796</summary>

<!-- original:f047b1fd97d683:source/blender/makesdna/DNA_space_enums.h:791:796 -->

```cpp
enum eSpaceImage_Mode : char {
  SI_MODE_VIEW = 0,
  SI_MODE_PAINT = 1,
  SI_MODE_MASK = 2,
  SI_MODE_UV = 3,
};
```

</details>


<a id="t-cc00426cc15e"></a>

### `blender::SpaceNodeGeometryNodesType`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L967—L970。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:a74d34b1fb29e2 -->

```cpp
enum SpaceNodeGeometryNodesType : char {
  SNODE_GEOMETRY_MODIFIER = 0,
  SNODE_GEOMETRY_TOOL = 1,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L967—L970</summary>

<!-- original:a74d34b1fb29e2:source/blender/makesdna/DNA_space_enums.h:967:970 -->

```cpp
enum SpaceNodeGeometryNodesType : char {
  SNODE_GEOMETRY_MODIFIER = 0,
  SNODE_GEOMETRY_TOOL = 1,
};
```

</details>


<a id="t-b0987f17e073"></a>

### `blender::SpaceNodeCompositorNodesType`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L973—L976。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:594c949ea8dd04 -->

```cpp
enum SpaceNodeCompositorNodesType : char {
  SNODE_COMPOSITOR_SCENE = 0,
  SNODE_COMPOSITOR_SEQUENCER = 1,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L973—L976</summary>

<!-- original:594c949ea8dd04:source/blender/makesdna/DNA_space_enums.h:973:976 -->

```cpp
enum SpaceNodeCompositorNodesType : char {
  SNODE_COMPOSITOR_SCENE = 0,
  SNODE_COMPOSITOR_SEQUENCER = 1,
};
```

</details>


<a id="t-5ea20cb9d0ce"></a>

### `blender::eSpace_Type`

原始声明：[source/blender/makesdna/DNA_space_enums.h](../../../../../../../source/blender/makesdna/DNA_space_enums.h) · L1183—L1218。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:439f04135dba3d -->

```cpp
enum eSpace_Type : char {
  SPACE_EMPTY = 0,
  SPACE_VIEW3D = 1,
  SPACE_GRAPH = 2,
  SPACE_OUTLINER = 3,
  SPACE_PROPERTIES = 4,
  SPACE_FILE = 5,
  SPACE_IMAGE = 6,
  SPACE_INFO = 7,
  SPACE_SEQ = 8,
  SPACE_TEXT = 9,
#ifdef DNA_DEPRECATED_ALLOW
  SPACE_IMASEL = 10, /* Deprecated */
  SPACE_SOUND = 11,  /* Deprecated */
#endif
  SPACE_ACTION = 12,
  SPACE_NLA = 13,
  /* TODO: fully deprecate */
  SPACE_SCRIPT = 14, /* Deprecated */
#ifdef DNA_DEPRECATED_ALLOW
  SPACE_TIME = 15, /* Deprecated */
#endif
  SPACE_NODE = 16,
#ifdef DNA_DEPRECATED_ALLOW
  SPACE_LOGIC = 17, /* Deprecated */
#endif
  SPACE_CONSOLE = 18,
  SPACE_USERPREF = 19,
  SPACE_CLIP = 20,
  SPACE_TOPBAR = 21,
  SPACE_STATUSBAR = 22,
  SPACE_SPREADSHEET = 23,
  SPACE_PROJECT = 24

#define SPACE_TYPE_NUM (SPACE_PROJECT + 1)
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_space_enums.h · L1183—L1218</summary>

<!-- original:439f04135dba3d:source/blender/makesdna/DNA_space_enums.h:1183:1218 -->

```cpp
enum eSpace_Type : char {
  SPACE_EMPTY = 0,
  SPACE_VIEW3D = 1,
  SPACE_GRAPH = 2,
  SPACE_OUTLINER = 3,
  SPACE_PROPERTIES = 4,
  SPACE_FILE = 5,
  SPACE_IMAGE = 6,
  SPACE_INFO = 7,
  SPACE_SEQ = 8,
  SPACE_TEXT = 9,
#ifdef DNA_DEPRECATED_ALLOW
  SPACE_IMASEL = 10, /* Deprecated */
  SPACE_SOUND = 11,  /* Deprecated */
#endif
  SPACE_ACTION = 12,
  SPACE_NLA = 13,
  /* TODO: fully deprecate */
  SPACE_SCRIPT = 14, /* Deprecated */
#ifdef DNA_DEPRECATED_ALLOW
  SPACE_TIME = 15, /* Deprecated */
#endif
  SPACE_NODE = 16,
#ifdef DNA_DEPRECATED_ALLOW
  SPACE_LOGIC = 17, /* Deprecated */
#endif
  SPACE_CONSOLE = 18,
  SPACE_USERPREF = 19,
  SPACE_CLIP = 20,
  SPACE_TOPBAR = 21,
  SPACE_STATUSBAR = 22,
  SPACE_SPREADSHEET = 23,
  SPACE_PROJECT = 24

#define SPACE_TYPE_NUM (SPACE_PROJECT + 1)
};
```

</details>


## 完整成员与函数实现
