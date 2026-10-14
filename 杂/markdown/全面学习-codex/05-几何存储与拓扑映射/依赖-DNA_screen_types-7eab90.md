# 实现依赖专题：source/blender/makesdna/DNA_screen_types.h

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_screen_types.h"]:::abstraction
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
  F["DNA_screen_types.h实现"]:::compute
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

<a id="t-45a6a3977e7e"></a>

### `blender::euiList_LayoutType`

原始声明：[source/blender/makesdna/DNA_screen_types.h](../../../../../source/blender/makesdna/DNA_screen_types.h) · L327—L330。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:b02cb13b478377 -->

```cpp
enum euiList_LayoutType : int {
  UILST_LAYOUT_DEFAULT = 0,
  UILST_LAYOUT_COMPACT = 1,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_screen_types.h · L327—L330</summary>

<!-- original:b02cb13b478377:source/blender/makesdna/DNA_screen_types.h:327:330 -->

```cpp
enum euiList_LayoutType : int {
  UILST_LAYOUT_DEFAULT = 0,
  UILST_LAYOUT_COMPACT = 1,
};
```

</details>


<a id="t-be2ec445059c"></a>

### `blender::eRegion_Type`

原始声明：[source/blender/makesdna/DNA_screen_types.h](../../../../../source/blender/makesdna/DNA_screen_types.h) · L680—L704。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:f48503b1b5b673 -->

```cpp
enum eRegion_Type : short {
  RGN_TYPE_WINDOW = 0,
  RGN_TYPE_HEADER = 1,
  RGN_TYPE_CHANNELS = 2,
  RGN_TYPE_TEMPORARY = 3,
  RGN_TYPE_UI = 4,
  RGN_TYPE_TOOLS = 5,
  RGN_TYPE_TOOL_PROPS = 6,
  RGN_TYPE_PREVIEW = 7,
  RGN_TYPE_HUD = 8,
  /* Region to navigate the main region from (RGN_TYPE_WINDOW). */
  RGN_TYPE_NAV_BAR = 9,
  /* A place for buttons to trigger execution of something that was set up in other regions. */
  RGN_TYPE_EXECUTE = 10,
  RGN_TYPE_FOOTER = 11,
  RGN_TYPE_TOOL_HEADER = 12,
  /* Region type used exclusively by internal code and add-ons to register draw callbacks to the XR
   * context (surface, mirror view). Does not represent any real region. */
  RGN_TYPE_XR = 13,
  RGN_TYPE_ASSET_SHELF = 14,
  RGN_TYPE_ASSET_SHELF_HEADER = 15,
  RGN_TYPE_SCRUBBING = 16,

#define RGN_TYPE_NUM (RGN_TYPE_SCRUBBING + 1)
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_screen_types.h · L680—L704</summary>

<!-- original:f48503b1b5b673:source/blender/makesdna/DNA_screen_types.h:680:704 -->

```cpp
enum eRegion_Type : short {
  RGN_TYPE_WINDOW = 0,
  RGN_TYPE_HEADER = 1,
  RGN_TYPE_CHANNELS = 2,
  RGN_TYPE_TEMPORARY = 3,
  RGN_TYPE_UI = 4,
  RGN_TYPE_TOOLS = 5,
  RGN_TYPE_TOOL_PROPS = 6,
  RGN_TYPE_PREVIEW = 7,
  RGN_TYPE_HUD = 8,
  /* Region to navigate the main region from (RGN_TYPE_WINDOW). */
  RGN_TYPE_NAV_BAR = 9,
  /* A place for buttons to trigger execution of something that was set up in other regions. */
  RGN_TYPE_EXECUTE = 10,
  RGN_TYPE_FOOTER = 11,
  RGN_TYPE_TOOL_HEADER = 12,
  /* Region type used exclusively by internal code and add-ons to register draw callbacks to the XR
   * context (surface, mirror view). Does not represent any real region. */
  RGN_TYPE_XR = 13,
  RGN_TYPE_ASSET_SHELF = 14,
  RGN_TYPE_ASSET_SHELF_HEADER = 15,
  RGN_TYPE_SCRUBBING = 16,

#define RGN_TYPE_NUM (RGN_TYPE_SCRUBBING + 1)
};
```

</details>


<a id="t-18aac1164ff6"></a>

### `blender::eRegion_Flag`

原始声明：[source/blender/makesdna/DNA_screen_types.h](../../../../../source/blender/makesdna/DNA_screen_types.h) · L751—L782。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:28bd91a0ab372d -->

```cpp
enum eRegion_Flag : short {
  RGN_FLAG_HIDDEN = (1 << 0),
  RGN_FLAG_TOO_SMALL = (1 << 1),
  /** Enable dynamically changing the region size in the #ARegionType::layout() callback. */
  RGN_FLAG_DYNAMIC_SIZE = (1 << 2),
  /** Region data is NULL'd on read, never written. */
  RGN_FLAG_TEMP_REGIONDATA = (1 << 3),
  /** Region resizing by the user is disabled, but the region edge can still be dragged to
   * hide/unhide the region. */
  RGN_FLAG_NO_USER_RESIZE = (1 << 4),
  /** Size has been clamped (floating regions only). */
  RGN_FLAG_SIZE_CLAMP_X = (1 << 5),
  RGN_FLAG_SIZE_CLAMP_Y = (1 << 6),
  /** When the user sets the region is hidden,
   * needed for floating regions that may be hidden for other reasons. */
  RGN_FLAG_HIDDEN_BY_USER = (1 << 7),
  /** Property search filter is active. */
  RGN_FLAG_SEARCH_FILTER_ACTIVE = (1 << 8),
  /**
   * Update the expansion of the region's panels and switch contexts. Only Set
   * temporarily when the search filter is updated and cleared at the end of the
   * region's layout pass. so that expansion is still interactive,
   */
  RGN_FLAG_SEARCH_FILTER_UPDATE = (1 << 9),
  /** #ARegionType.poll() failed for the current context, and the region should be treated as if it
   * wouldn't exist. Runtime only flag. */
  RGN_FLAG_POLL_FAILED = (1 << 10),
  RGN_FLAG_RESIZE_RESPECT_BUTTON_SECTIONS = (1 << 11),
  RGN_FLAG_INDICATE_OVERFLOW = (1 << 12),

  RGN_FLAG_SEARCH_FILTER_SHOW = (1 << 13),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_screen_types.h · L751—L782</summary>

<!-- original:28bd91a0ab372d:source/blender/makesdna/DNA_screen_types.h:751:782 -->

```cpp
enum eRegion_Flag : short {
  RGN_FLAG_HIDDEN = (1 << 0),
  RGN_FLAG_TOO_SMALL = (1 << 1),
  /** Enable dynamically changing the region size in the #ARegionType::layout() callback. */
  RGN_FLAG_DYNAMIC_SIZE = (1 << 2),
  /** Region data is NULL'd on read, never written. */
  RGN_FLAG_TEMP_REGIONDATA = (1 << 3),
  /** Region resizing by the user is disabled, but the region edge can still be dragged to
   * hide/unhide the region. */
  RGN_FLAG_NO_USER_RESIZE = (1 << 4),
  /** Size has been clamped (floating regions only). */
  RGN_FLAG_SIZE_CLAMP_X = (1 << 5),
  RGN_FLAG_SIZE_CLAMP_Y = (1 << 6),
  /** When the user sets the region is hidden,
   * needed for floating regions that may be hidden for other reasons. */
  RGN_FLAG_HIDDEN_BY_USER = (1 << 7),
  /** Property search filter is active. */
  RGN_FLAG_SEARCH_FILTER_ACTIVE = (1 << 8),
  /**
   * Update the expansion of the region's panels and switch contexts. Only Set
   * temporarily when the search filter is updated and cleared at the end of the
   * region's layout pass. so that expansion is still interactive,
   */
  RGN_FLAG_SEARCH_FILTER_UPDATE = (1 << 9),
  /** #ARegionType.poll() failed for the current context, and the region should be treated as if it
   * wouldn't exist. Runtime only flag. */
  RGN_FLAG_POLL_FAILED = (1 << 10),
  RGN_FLAG_RESIZE_RESPECT_BUTTON_SECTIONS = (1 << 11),
  RGN_FLAG_INDICATE_OVERFLOW = (1 << 12),

  RGN_FLAG_SEARCH_FILTER_SHOW = (1 << 13),
};
```

</details>


<a id="m-b654cb10a80d"></a>

## 宏 `AREAMAP_FROM_SCREEN`

<!-- annotated:e89f485aa9ecc2 -->

```cpp
#define AREAMAP_FROM_SCREEN(screen) ((ScrAreaMap *)&(screen)->vertbase)

```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_screen_types.h · L93—L94</summary>

<!-- original:e89f485aa9ecc2:source/blender/makesdna/DNA_screen_types.h:93:94 -->

```cpp
#define AREAMAP_FROM_SCREEN(screen) ((ScrAreaMap *)&(screen)->vertbase)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-8998f932a229"></a>

## 宏 `RGN_TYPE_IS_HEADER_ANY`

<!-- annotated:0c2714345ac8e6 -->

```cpp
#define RGN_TYPE_IS_HEADER_ANY(regiontype) \
  (((1 << (regiontype)) & \
    ((1 << RGN_TYPE_HEADER) | 1 << (RGN_TYPE_TOOL_HEADER) | (1 << RGN_TYPE_FOOTER) | \
     (1 << RGN_TYPE_ASSET_SHELF_HEADER) | (1 << RGN_TYPE_SCRUBBING))) != 0)

```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_screen_types.h · L710—L714</summary>

<!-- original:0c2714345ac8e6:source/blender/makesdna/DNA_screen_types.h:710:714 -->

```cpp
#define RGN_TYPE_IS_HEADER_ANY(regiontype) \
  (((1 << (regiontype)) & \
    ((1 << RGN_TYPE_HEADER) | 1 << (RGN_TYPE_TOOL_HEADER) | (1 << RGN_TYPE_FOOTER) | \
     (1 << RGN_TYPE_ASSET_SHELF_HEADER) | (1 << RGN_TYPE_SCRUBBING))) != 0)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-7267b0776dc7"></a>

## 宏 `RGN_ALIGN_ENUM_FROM_MASK`

<!-- annotated:1ea88e3a914978 -->

```cpp
#define RGN_ALIGN_ENUM_FROM_MASK(align) ((align) & eRegion_Alignment((1 << 4) - 1))
#define RGN_ALIGN_FLAG_FROM_MASK(align) ((align) & ~eRegion_Alignment((1 << 4) - 1))
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_screen_types.h · L747—L748</summary>

<!-- original:1ea88e3a914978:source/blender/makesdna/DNA_screen_types.h:747:748 -->

```cpp
#define RGN_ALIGN_ENUM_FROM_MASK(align) ((align) & eRegion_Alignment((1 << 4) - 1))
#define RGN_ALIGN_FLAG_FROM_MASK(align) ((align) & ~eRegion_Alignment((1 << 4) - 1))
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
