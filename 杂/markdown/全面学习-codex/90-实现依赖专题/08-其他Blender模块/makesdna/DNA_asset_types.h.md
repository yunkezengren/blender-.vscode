# 实现依赖专题：source/blender/makesdna/DNA_asset_types.h

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_asset_types.h"]:::abstraction
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
  F["DNA_asset_types.h实现"]:::compute
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

<a id="t-7571bb5757c1"></a>

### `blender::eAssetLibraryType`

原始声明：[source/blender/makesdna/DNA_asset_types.h](../../../../../../../source/blender/makesdna/DNA_asset_types.h) · L26—L42。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:319af527eabfc3 -->

```cpp
enum eAssetLibraryType : short {
  /** Display assets from the current session (current "Main"). */
  ASSET_LIBRARY_LOCAL = 1,
  ASSET_LIBRARY_ALL = 2,
  /** Display assets bundled with Blender by default. */
  ASSET_LIBRARY_ESSENTIALS = 3,
  /** Additions to the essentials library that are stored online - displayed in the UI as part of
   * the normal essentials library. */
  ASSET_LIBRARY_ONLINE_ESSENTIALS = 4,

  /** Display assets from custom asset libraries, as defined in the preferences
   * (#bUserAssetLibrary). The name will be taken from #FileSelectParams.asset_library_ref.idname
   * then.
   * In RNA, we add the index of the custom library to this to identify it by index. So keep
   * this last! */
  ASSET_LIBRARY_CUSTOM = 100,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_asset_types.h · L26—L42</summary>

<!-- original:319af527eabfc3:source/blender/makesdna/DNA_asset_types.h:26:42 -->

```cpp
enum eAssetLibraryType : short {
  /** Display assets from the current session (current "Main"). */
  ASSET_LIBRARY_LOCAL = 1,
  ASSET_LIBRARY_ALL = 2,
  /** Display assets bundled with Blender by default. */
  ASSET_LIBRARY_ESSENTIALS = 3,
  /** Additions to the essentials library that are stored online - displayed in the UI as part of
   * the normal essentials library. */
  ASSET_LIBRARY_ONLINE_ESSENTIALS = 4,

  /** Display assets from custom asset libraries, as defined in the preferences
   * (#bUserAssetLibrary). The name will be taken from #FileSelectParams.asset_library_ref.idname
   * then.
   * In RNA, we add the index of the custom library to this to identify it by index. So keep
   * this last! */
  ASSET_LIBRARY_CUSTOM = 100,
};
```

</details>


<a id="t-fa9b43bee74d"></a>

### `blender::AssetLibraryReference`

原始声明：[source/blender/makesdna/DNA_asset_types.h](../../../../../../../source/blender/makesdna/DNA_asset_types.h) · L176—L185。

成员布局：

- `eAssetLibraryType type`
- `char _pad1`
- `int custom_library_index`

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:15a9aa115b04d9 -->

```cpp
struct AssetLibraryReference {
  eAssetLibraryType type = ASSET_LIBRARY_LOCAL;
  char _pad1[2] = {};
  /**
   * If showing a custom asset library (#ASSET_LIBRARY_CUSTOM), this is the index of the
   * #bUserAssetLibrary within #UserDef.asset_libraries.
   * Should be ignored otherwise (but better set to -1 then, for sanity and debugging).
   */
  int custom_library_index = -1;
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_asset_types.h · L176—L185</summary>

<!-- original:15a9aa115b04d9:source/blender/makesdna/DNA_asset_types.h:176:185 -->

```cpp
struct AssetLibraryReference {
  eAssetLibraryType type = ASSET_LIBRARY_LOCAL;
  char _pad1[2] = {};
  /**
   * If showing a custom asset library (#ASSET_LIBRARY_CUSTOM), this is the index of the
   * #bUserAssetLibrary within #UserDef.asset_libraries.
   * Should be ignored otherwise (but better set to -1 then, for sanity and debugging).
   */
  int custom_library_index = -1;
};
```

</details>


## 完整成员与函数实现
