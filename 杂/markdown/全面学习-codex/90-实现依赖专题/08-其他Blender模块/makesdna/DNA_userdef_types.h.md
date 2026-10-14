# 实现依赖专题：source/blender/makesdna/DNA_userdef_types.h

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_userdef_types.h"]:::abstraction
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
  F["DNA_userdef_types.h实现"]:::compute
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

<a id="t-d62dd6c87436"></a>

### `blender::eUserPref_Flag`

原始声明：[source/blender/makesdna/DNA_userdef_types.h](../../../../../../../source/blender/makesdna/DNA_userdef_types.h) · L33—L64。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:76012376cc90a4 -->

```cpp
enum eUserPref_Flag : int {
  USER_AUTOSAVE = (1 << 0),
  USER_FLAG_NUMINPUT_ADVANCED = (1 << 1),
  USER_FLAG_RECENT_SEARCHES_DISABLE = (1 << 2),
  USER_MENU_CLOSE_LEAVE = (1 << 3),
  USER_FLAG_UNUSED_4 = (1 << 4), /* cleared */
  USER_TRACKBALL = (1 << 5),
  USER_FLAG_UNUSED_6 = (1 << 6), /* cleared */
  USER_FLAG_UNUSED_7 = (1 << 7), /* cleared */
  USER_MAT_ON_OB = (1 << 8),
  USER_INTERNET_ALLOW = (1 << 9),
  USER_DEVELOPER_UI = (1 << 10),
  USER_TOOLTIPS = (1 << 11),
  USER_TWOBUTTONMOUSE = (1 << 12),
  USER_NONUMPAD = (1 << 13),
  USER_ADD_CURSORALIGNED = (1 << 14),
  USER_FILECOMPRESS = (1 << 15),
  USER_FLAG_UNUSED_5 = (1 << 16), /* dirty */
  USER_CUSTOM_RANGE = (1 << 17),
  USER_ADD_EDITMODE = (1 << 18),
  USER_ADD_VIEWALIGNED = (1 << 19),
  USER_RELPATHS = (1 << 20),
  USER_RELEASECONFIRM = (1 << 21),
  /** See #G_FLAG_SCRIPT_AUTOEXEC for an overview of auto-execution. */
  USER_SCRIPT_AUTOEXEC_DISABLE = (1 << 22),
  USER_FILENOUI = (1 << 23),
  USER_NONEGFRAMES = (1 << 24),
  USER_TXT_TABSTOSPACES_DISABLE = (1 << 25),
  USER_TOOLTIPS_PYTHON = (1 << 26),
  USER_FLAG_UNUSED_27 = (1 << 27), /* dirty */
  USER_HIDE_DOT_DATABLOCK = (1 << 28),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_userdef_types.h · L33—L64</summary>

<!-- original:76012376cc90a4:source/blender/makesdna/DNA_userdef_types.h:33:64 -->

```cpp
enum eUserPref_Flag : int {
  USER_AUTOSAVE = (1 << 0),
  USER_FLAG_NUMINPUT_ADVANCED = (1 << 1),
  USER_FLAG_RECENT_SEARCHES_DISABLE = (1 << 2),
  USER_MENU_CLOSE_LEAVE = (1 << 3),
  USER_FLAG_UNUSED_4 = (1 << 4), /* cleared */
  USER_TRACKBALL = (1 << 5),
  USER_FLAG_UNUSED_6 = (1 << 6), /* cleared */
  USER_FLAG_UNUSED_7 = (1 << 7), /* cleared */
  USER_MAT_ON_OB = (1 << 8),
  USER_INTERNET_ALLOW = (1 << 9),
  USER_DEVELOPER_UI = (1 << 10),
  USER_TOOLTIPS = (1 << 11),
  USER_TWOBUTTONMOUSE = (1 << 12),
  USER_NONUMPAD = (1 << 13),
  USER_ADD_CURSORALIGNED = (1 << 14),
  USER_FILECOMPRESS = (1 << 15),
  USER_FLAG_UNUSED_5 = (1 << 16), /* dirty */
  USER_CUSTOM_RANGE = (1 << 17),
  USER_ADD_EDITMODE = (1 << 18),
  USER_ADD_VIEWALIGNED = (1 << 19),
  USER_RELPATHS = (1 << 20),
  USER_RELEASECONFIRM = (1 << 21),
  /** See #G_FLAG_SCRIPT_AUTOEXEC for an overview of auto-execution. */
  USER_SCRIPT_AUTOEXEC_DISABLE = (1 << 22),
  USER_FILENOUI = (1 << 23),
  USER_NONEGFRAMES = (1 << 24),
  USER_TXT_TABSTOSPACES_DISABLE = (1 << 25),
  USER_TOOLTIPS_PYTHON = (1 << 26),
  USER_FLAG_UNUSED_27 = (1 << 27), /* dirty */
  USER_HIDE_DOT_DATABLOCK = (1 << 28),
};
```

</details>


<a id="t-2212acf544bc"></a>

### `blender::eUserpref_MiniAxisType`

原始声明：[source/blender/makesdna/DNA_userdef_types.h](../../../../../../../source/blender/makesdna/DNA_userdef_types.h) · L126—L130。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:ab64cfa88f3a5d -->

```cpp
enum eUserpref_MiniAxisType : char {
  USER_MINI_AXIS_TYPE_GIZMO = 0,
  USER_MINI_AXIS_TYPE_MINIMAL = 1,
  USER_MINI_AXIS_TYPE_NONE = 2,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_userdef_types.h · L126—L130</summary>

<!-- original:ab64cfa88f3a5d:source/blender/makesdna/DNA_userdef_types.h:126:130 -->

```cpp
enum eUserpref_MiniAxisType : char {
  USER_MINI_AXIS_TYPE_GIZMO = 0,
  USER_MINI_AXIS_TYPE_MINIMAL = 1,
  USER_MINI_AXIS_TYPE_NONE = 2,
};
```

</details>


<a id="t-e0c06ddc69d5"></a>

### `blender::eUserpref_UI_Flag`

原始声明：[source/blender/makesdna/DNA_userdef_types.h](../../../../../../../source/blender/makesdna/DNA_userdef_types.h) · L140—L179。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:cb784680ce46dd -->

```cpp
enum eUserpref_UI_Flag : uint32_t {
  USER_NO_MULTITOUCH_GESTURES = (1 << 0),
  USER_REDUCE_MOTION = (1 << 1),
  USER_WHEELZOOMDIR = (1 << 2),
  USER_FILTERFILEEXTS = (1 << 3),
  USER_DRAWVIEWINFO = (1 << 4),
  USER_PLAINMENUS = (1 << 5),
  USER_LOCK_CURSOR_ADJUST = (1 << 6),
  USER_HEADER_BOTTOM = (1 << 7),
  /** Otherwise use header alignment from the file. */
  USER_HEADER_FROM_PREF = (1 << 8),
  USER_MENUOPENAUTO = (1 << 9),
  USER_DEPTH_CURSOR = (1 << 10),
  USER_AUTOPERSP = (1 << 11),
  USER_NODE_AUTO_OFFSET = (1 << 12),
  USER_GLOBALUNDO = (1 << 13),
  USER_ORBIT_SELECTION = (1 << 14),
  USER_DEPTH_NAVIGATE = (1 << 15),
  USER_HIDE_DOT = (1 << 16),
  USER_SHOW_GIZMO_NAVIGATE = (1 << 17),
  USER_SHOW_VIEWPORTNAME = (1 << 18),
  USER_AREA_CORNER_HANDLE = (1 << 19),
  USER_ZOOM_TO_MOUSEPOS = (1 << 20),
  USER_SHOW_FPS = (1 << 21),
  USER_REGISTER_ALL_USERS = (1 << 22),
  /** Actually implemented in .py. */
  USER_FILTER_BRUSHES_BY_TOOL = (1 << 23),
  USER_CONTINUOUS_MOUSE = (1 << 24),
  USER_ZOOM_INVERT = (1 << 25),
  USER_ZOOM_HORIZ = (1 << 26), /* for CONTINUE and DOLLY zoom */
  USER_SPLASH_DISABLE = (1 << 27),
  USER_HIDE_RECENT = (1 << 28),
#ifdef DNA_DEPRECATED_ALLOW
  /* Deprecated: We're just trying if there's much desire for this feature,
   * or if we can make it go for good. Should be cleared if so - Julian, Oct. 2019. */
  USER_SHOW_THUMBNAILS = (1 << 29),
#endif
  USER_SAVE_PROMPT = (1 << 30),
  USER_HIDE_SYSTEM_BOOKMARKS = (1u << 31),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_userdef_types.h · L140—L179</summary>

<!-- original:cb784680ce46dd:source/blender/makesdna/DNA_userdef_types.h:140:179 -->

```cpp
enum eUserpref_UI_Flag : uint32_t {
  USER_NO_MULTITOUCH_GESTURES = (1 << 0),
  USER_REDUCE_MOTION = (1 << 1),
  USER_WHEELZOOMDIR = (1 << 2),
  USER_FILTERFILEEXTS = (1 << 3),
  USER_DRAWVIEWINFO = (1 << 4),
  USER_PLAINMENUS = (1 << 5),
  USER_LOCK_CURSOR_ADJUST = (1 << 6),
  USER_HEADER_BOTTOM = (1 << 7),
  /** Otherwise use header alignment from the file. */
  USER_HEADER_FROM_PREF = (1 << 8),
  USER_MENUOPENAUTO = (1 << 9),
  USER_DEPTH_CURSOR = (1 << 10),
  USER_AUTOPERSP = (1 << 11),
  USER_NODE_AUTO_OFFSET = (1 << 12),
  USER_GLOBALUNDO = (1 << 13),
  USER_ORBIT_SELECTION = (1 << 14),
  USER_DEPTH_NAVIGATE = (1 << 15),
  USER_HIDE_DOT = (1 << 16),
  USER_SHOW_GIZMO_NAVIGATE = (1 << 17),
  USER_SHOW_VIEWPORTNAME = (1 << 18),
  USER_AREA_CORNER_HANDLE = (1 << 19),
  USER_ZOOM_TO_MOUSEPOS = (1 << 20),
  USER_SHOW_FPS = (1 << 21),
  USER_REGISTER_ALL_USERS = (1 << 22),
  /** Actually implemented in .py. */
  USER_FILTER_BRUSHES_BY_TOOL = (1 << 23),
  USER_CONTINUOUS_MOUSE = (1 << 24),
  USER_ZOOM_INVERT = (1 << 25),
  USER_ZOOM_HORIZ = (1 << 26), /* for CONTINUE and DOLLY zoom */
  USER_SPLASH_DISABLE = (1 << 27),
  USER_HIDE_RECENT = (1 << 28),
#ifdef DNA_DEPRECATED_ALLOW
  /* Deprecated: We're just trying if there's much desire for this feature,
   * or if we can make it go for good. Should be cleared if so - Julian, Oct. 2019. */
  USER_SHOW_THUMBNAILS = (1 << 29),
#endif
  USER_SAVE_PROMPT = (1 << 30),
  USER_HIDE_SYSTEM_BOOKMARKS = (1u << 31),
};
```

</details>


<a id="t-6855a02642c3"></a>

### `blender::eAutokey_Mode`

原始声明：[source/blender/makesdna/DNA_userdef_types.h](../../../../../../../source/blender/makesdna/DNA_userdef_types.h) · L261—L271。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:bd2a22b9a48643 -->

```cpp
enum eAutokey_Mode : short {
  /* AUTOKEY_ON is a bit-flag. */
  AUTOKEY_ON = 1,

  /**
   * AUTOKEY_ON + 2**n...  (i.e. AUTOKEY_MODE_NORMAL = AUTOKEY_ON + 2)
   * to preserve setting, even when auto-key turned off.
   */
  AUTOKEY_MODE_NORMAL = 3,
  AUTOKEY_MODE_EDITKEYS = 5,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_userdef_types.h · L261—L271</summary>

<!-- original:bd2a22b9a48643:source/blender/makesdna/DNA_userdef_types.h:261:271 -->

```cpp
enum eAutokey_Mode : short {
  /* AUTOKEY_ON is a bit-flag. */
  AUTOKEY_ON = 1,

  /**
   * AUTOKEY_ON + 2**n...  (i.e. AUTOKEY_MODE_NORMAL = AUTOKEY_ON + 2)
   * to preserve setting, even when auto-key turned off.
   */
  AUTOKEY_MODE_NORMAL = 3,
  AUTOKEY_MODE_EDITKEYS = 5,
};
```

</details>


<a id="m-0ab3ba53bfeb"></a>

## 宏 `NDOF_IS_ORBIT_AROUND_CENTER_MODE`

<!-- annotated:6b98b382dd2cca -->

```cpp
#define NDOF_IS_ORBIT_AROUND_CENTER_MODE(userdef) \
  ((userdef)->ndof_navigation_mode == NDOF_NAVIGATION_MODE_OBJECT)

```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_userdef_types.h · L497—L499</summary>

<!-- original:6b98b382dd2cca:source/blender/makesdna/DNA_userdef_types.h:497:499 -->

```cpp
#define NDOF_IS_ORBIT_AROUND_CENTER_MODE(userdef) \
  ((userdef)->ndof_navigation_mode == NDOF_NAVIGATION_MODE_OBJECT)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-ecbd9ffdd68a"></a>

## 宏 `USER_EXPERIMENTAL_TEST`

<!-- annotated:2787b32889682f -->

```cpp
#define USER_EXPERIMENTAL_TEST(userdef, member) (((userdef)->experimental).member)

```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_userdef_types.h · L924—L925</summary>

<!-- original:2787b32889682f:source/blender/makesdna/DNA_userdef_types.h:924:925 -->

```cpp
#define USER_EXPERIMENTAL_TEST(userdef, member) (((userdef)->experimental).member)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-86dc117d0e84"></a>

## 宏 `USER_DEVELOPER_TOOL_TEST`

<!-- annotated:33815580afe072 -->

```cpp
#define USER_DEVELOPER_TOOL_TEST(userdef, member) \
  (((userdef)->flag & USER_DEVELOPER_UI) && ((userdef)->experimental).member)

```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_userdef_types.h · L926—L928</summary>

<!-- original:33815580afe072:source/blender/makesdna/DNA_userdef_types.h:926:928 -->

```cpp
#define USER_DEVELOPER_TOOL_TEST(userdef, member) \
  (((userdef)->flag & USER_DEVELOPER_UI) && ((userdef)->experimental).member)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
