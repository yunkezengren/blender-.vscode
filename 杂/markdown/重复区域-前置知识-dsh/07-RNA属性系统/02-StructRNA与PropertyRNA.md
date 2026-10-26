# 02 · StructRNA 与 PropertyRNA

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](01-RNA三层结构与职责.md) · [下一篇](03-PointerRNA与属性访问.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇深入 RNA 的头两个类型：`StructRNA`（类型描述）与 `PropertyRNA`（属性描述）。主要源码：[`RNA_types.hh`](../../../source/blender/makesrna/RNA_types.hh)（总行数 1180，但其只有前向声明；真定义在 [`intern/rna_internal_types.hh`](../../../source/blender/makesrna/intern/rna_internal_types.hh) L671/L398）、[`RNA_define.hh`](../../../source/blender/makesrna/RNA_define.hh)（总行数 754）、[`intern/rna_internal.hh`](../../../source/blender/makesrna/intern/rna_internal.hh)（总行数 753）。

## 先回答一个具体问题

**`StructRNA` 和 C 结构体是什么关系？为什么需要两个东西描述同一份数据？**

因为它们回答两个完全不同的问题，而且回答的时间也不同。

C 结构体（DNA）回答"**这堆字节怎么摆**"：`NodeRepeatItem` 里有 `char *name`、`eNodeSocketDatatype socket_type`、`char _pad[2]`、`int identifier`，共多少字节、谁是第几个成员。这个答案必须编译期定死，因为它决定 `.blend` 里那串字节怎么切分——这是[第 05 章：DNA 与序列化](../05-DNA与序列化/README.md)的主题。

`StructRNA` 回答"**这堆字节怎么被使用**"：它叫什么名字（`RepeatItem`）、UI 显示成什么（`Repeat Item`）、有没有名字属性、能不能撤销、有哪些属性可读可写。这是运行时反射信息，供 UI 绘制、Python 绑定、动画系统、操作符参数共用。

两份描述靠一条**只在编译期存在的线**相连：`RNA_def_struct_sdna(srna, "NodeRepeatItem")` 说的是"这个 `StructRNA` 裹的是哪个 DNA 结构"。关键词是**只在编译期**——makesrna 在构建时读一遍 RNA 定义、生成 C 访问器代码、然后把自己扔掉；跑到游戏里的 `StructRNA` 里根本没有"我是哪个 DNA 结构"这种字段。

所以本篇有一个必须一开始就说清的实测结论，它和常见教程的写法不一致：

| 常见写法 | 本地工作树实测 | 位置 |
| --- | --- | --- |
| `StructRNA::dna_struct` | **不存在** | [`rna_internal_types.hh` L671-L751](../../../source/blender/makesrna/intern/rna_internal_types.hh#L671) |
| `StructRNA::properties` | 是 `cont.properties`，`ListBaseT<PropertyRNA>` | [L673](../../../source/blender/makesrna/intern/rna_internal_types.hh#L673)、[L369-L374](../../../source/blender/makesrna/intern/rna_internal_types.hh#L369) |
| `StructRNA::icon_id` | 字段名是 `icon`，类型 `int` | [L701](../../../source/blender/makesrna/intern/rna_internal_types.hh#L701) |
| `PropertyRNA::dna_prop` | **不存在** | [L398-L493](../../../source/blender/makesrna/intern/rna_internal_types.hh#L398) |

DNA 绑定全部住在 `StructDefRNA` / `PropertyDefRNA` 里（[`rna_internal.hh` L71-L115](../../../source/blender/makesrna/intern/rna_internal.hh#L71)），被 `#ifndef RNA_RUNTIME` 包着——**只存在于 makesrna 进程的内存里**。这不是细节洁癖，它直接解释"为什么改 `PropertyRNA` 的 `type` 改不动底层数据"（见反例 4）。

## StructRNA 字段逐个

`StructRNA` 实测 81 行定义（[L671-L751](../../../source/blender/makesrna/intern/rna_internal_types.hh#L671)）：

| 字段 | 类型 | 行号 | 作用 |
| --- | --- | --- | --- |
| `cont` | `ContainerRNA` | 673 | **必须排第一**：属性链表 + 名字查找表 |
| `identifier` | `UString` | 675 | 唯一标识，如 `RepeatItem` |
| `py_type` / `blender_type` | `void *` | 683 / 684 | 对应 Python 类型 / 派生共享的基类型 |
| `flag` | `StructFlag` | 687 | `STRUCT_ID` / `STRUCT_UNDO` 等 |
| `prop_tag_defines` | `const EnumPropertyItem *` | 692 | 本类型专属属性标签枚举 |
| `name` / `description` | `const char *` | 695 / 697 | 用户可读名 / tooltip 文本 |
| `translation_context` | `const char *` | 699 | 翻译上下文 |
| `icon` | `int` | 701 | 类型图标 ID |
| `nameproperty` | `PropertyRNA *` | 704 | **哪个属性是"名字"** |
| `iteratorproperty` | `PropertyRNA *` | 707 | 迭代本类型用的属性 |
| `base` / `nested` | `StructRNA *` | 710 / 718 | 父类型 / 嵌套分组 |
| `refine` / `path` | 函数指针 | 721 / 724 | 细化类型 / 求 RNA 路径 |
| `reg` / `unreg` / `instance` | 函数指针 | 727 / 729 / 741 | 注册 / 反注册 / 复用 Python 实例 |
| `idproperties` / `system_idproperties` | `IDPropertiesFunc` | 744 / 747 | 用户 / 系统 IDProperty 根 |
| `functions` | `Vector<unique_ptr<FunctionRNA>>` | 750 | 本类型函数表 |

### 重点一：`properties` 藏在 `cont` 后面

`StructRNA` 没把 `properties` 直接摊在身上，而是塞进 `ContainerRNA cont`（[L369-L374](../../../source/blender/makesrna/intern/rna_internal_types.hh#L369)）：

```cpp
struct ContainerRNA {
  CustomIDVectorSet<PropertyRNA *, PropertyRNAIdentifierGetter> *prop_lookup_set;
  ListBaseT<PropertyRNA> properties;
};
```

如此设计是为了让 `PropertyRNA` 能被**两种东西**共有：`StructRNA`（结构的属性）与 `FunctionRNA`（函数的形参与返回值，[L375-L396](../../../source/blender/makesrna/intern/rna_internal_types.hh#L375)）。两者第一成员都是 `ContainerRNA cont`，于是 `RNA_def_property(cont_, ...)` 的形参才能写成 `StructOrFunctionRNA *`——一个 `typedef void`（[`RNA_define.hh` L124](../../../source/blender/makesrna/RNA_define.hh#L124)），靠"第一成员是 cont"的约定做类型双关。

读代码时 `srna->cont.properties` 就是属性链表本身；`prop_lookup_set` 是它的索引，`RNA_struct_find_property` 优先走索引、没索引才线性扫链表（[`rna_access.cc` L874-L893](../../../source/blender/makesrna/intern/rna_access.cc#L874)）。

另有一条纪律写在注释里：`identifier` 必须紧跟 `cont`（"keep after `cont`"，L674）。`CONTAINER_RNA_ID` 宏正是靠这个布局，把 `ContainerRNA *` 往后跳一格强转成 `const char **` 取到标识符（[L775](../../../source/blender/makesrna/intern/rna_internal_types.hh#L775)），用于报错信息。

### 重点二：`dna_struct` 为什么不存在

DNA 绑定是**构建期事务**，不是运行期数据。三条证据：

1. `StructDefRNA` 整个结构被 `#ifndef RNA_RUNTIME` 包住（[`rna_internal.hh` L54-L121](../../../source/blender/makesrna/intern/rna_internal.hh#L54)），`RNA_RUNTIME` 版本里根本没有它；
2. `RNA_def_struct_sdna` 实现只有一句有效代码 `ds->dnaname = structname;`（[`rna_define.cc` L943-L963](../../../source/blender/makesrna/intern/rna_define.cc#L943)），写的是 `StructDefRNA`，不是 `StructRNA`；
3. `offsetof` 只出现在**生成的代码文本**里，不在运行时结构里（[`makesrna.cc` L1960-L1969](../../../source/blender/makesrna/intern/makesrna.cc#L1960)）。

那运行期怎么知道字段偏移？靠 `PropertyRNA::rawoffset` + `rawtype`（L476-L477）。但它**只在 raw access 场景**（批量数组读写，如几何属性拷贝）才被填充，且需 `PROP_INTERN_RAW_ACCESS` 内部标志；普通属性走生成好的 `get` / `set` 函数，偏移量早已被编译器折进代码（[`rna_access.cc` L5481-L5484](../../../source/blender/makesrna/intern/rna_access.cc#L5481)）。

### 重点三：`nameproperty` 是 Repeat 那条链的钥匙

`nameproperty`（L704）标注"哪个属性用来取本结构的名字"。`RNA_def_struct_name_property` 校验其类型必须是 `PROP_STRING`，且一个结构只能设一次（[`rna_define.cc` L991-L1010](../../../source/blender/makesrna/intern/rna_define.cc#L991)）。`RNA_RepeatItem` 正是这样把 `name` 登记为名字属性（[`rna_nodetree.cc` L4977](../../../source/blender/makesrna/intern/rna_nodetree.cc#L4977)）。

登记之后，任何"按名字取集合元素"的通用代码都能工作——`RNA_property_collection_lookup_string_has_nameprop` 检查的就是 `item_type->nameproperty` 非空（[`rna_access.cc` L5303-L5309](../../../source/blender/makesrna/intern/rna_access.cc#L5303)）。这是 socket 按 identifier 复用条目的反射层前提。

### 重点四：`flag` 中两个影响 Repeat 的位

- `STRUCT_UNDO`（L1058）：默认开，属性变更自动产生撤销步；`RNA_def_struct_ptr` 对非派生结构强制置上（[`rna_define.cc` L848](../../../source/blender/makesrna/intern/rna_define.cc#L848)）。
- `STRUCT_RUNTIME`（L1061）：只有运行时（Python 注册）定义的类型才有，静态 RNA 没有。
- 另有 `STRUCT_RNA_DEFINITION`（L1090）：标在 `Struct` / `Property` 这些元类型上，此时 `PointerRNA.data` 指向的是**定义本身**（一个 `StructRNA` 或 `PropertyRNA`），而非 DNA 数据，所以数据回调一律不许跑。

## PropertyRNA 字段逐个

`PropertyRNA` 实测 96 行（[L398-L493](../../../source/blender/makesrna/intern/rna_internal_types.hh#L398)），只装"与类型无关"的公共信息，类型专属槽位靠**派生结构**扩展：

| 字段 | 类型 | 行号 | 作用 |
| --- | --- | --- | --- |
| `next` / `prev` | `PropertyRNA *` | 399 | 链表指针 |
| `magic` | `int` | 402 | `RNA_MAGIC`，与 `IDProperty` 区分 |
| `identifier` | `UString` | 405 | 唯一标识，如 `name` |
| `flag` | `PropertyFlag` | 407 | `PROP_EDITABLE` / `PROP_ANIMATABLE` |
| `flag_override` / `flag_parameter` / `flag_internal` | 三个枚举 | 409 / 411 / 413 | 库覆盖 / 形参 / 内部标志 |
| `tags` | `short` | 415 | `prop_tag_defines` 的子集 |
| `path_template_type` | `PropertyPathTemplateType` | 424 | 路径模板变量支持级别 |
| `name` / `description` / `icon` | `const char *` / `int` | 427 / 429 / 431 | UI 名 / tooltip / 图标 |
| `translation_context` | `const char *` | 433 | 翻译上下文 |
| `deprecated` | `const DeprecatedRNA *` | 436 | 弃用信息 |
| `type` | `PropertyType` | 439 | **7 种之一，决定 UI 控件** |
| `subtype` | `PropertySubType` | 441 | **细化解释，决定控件长相** |
| `getlength` | `PropArrayLengthGetFunc` | 443 | 动态数组长度回调 |
| `arraydimension` | `unsigned int` | 445 | 0 = 标量，1..3 = 数组 |
| `arraylength[3]` / `totarraylength` | `unsigned int` | 447 / 448 | 各维长度 / 元素总数 |
| `update` / `noteflag` | `UpdateFunc` / `int` | 451 / 452 | 变更通知回调 / 标签 |
| `editable` / `itemeditable` | 函数指针 | 459 / 461 | 动态判可编辑（元素级） |
| `ui_name_func` / `ui_description_func` | `PropUINameFunc` | 464 / 467 | 动态覆写显示名 / tooltip |
| `override_diff` / `override_store` / `override_apply` | 函数指针 | 470-472 | 库覆盖三件套 |
| `rawoffset` / `rawtype` | `int` / `RawPropertyType` | 476 / 477 | **字段字节偏移**（仅 raw access）/ raw 类型 |
| `srna` | `StructRNA *` | 486 | 仅集合/数组：附加属性容器 |
| `py_data` | `void *` | 492 | Python 回调句柄 |

### 重点一：`type` 决定控件种类，`subtype` 决定控件长相

`type` 是粗粒度分类，只有 7 个值；`subtype` 在同一 `type` 内换"皮肤"。实测控件选择逻辑在 [`interface_utils.cc` L57-L293](../../../source/blender/editors/interface/interface_utils.cc#L57)：

- `PROP_INT` / `PROP_FLOAT` 默认 `ButtonType::Num`；`subtype` 为 `PROP_PERCENTAGE` / `PROP_FACTOR` 时升格 `NumSlider`；数组且 `subtype` 为 `PROP_COLOR(_GAMMA)` 时给 `Color`。
- `PROP_ENUM` 默认 `Menu`，`expand` 时改画一排按钮。
- `PROP_STRING` 默认 `Text`，带 search 回调时变 `SearchMenu`。
- `PROP_POINTER` 固定 `SearchMenu`，图标来自被指类型的 `RNA_struct_ui_icon`。
- `PROP_COLLECTION` **没有单按钮**，`uiDefAutoButR` 只画禁用的 `"%d items"` 标签（L279-L285），真正列表交给模板机制。

这条"控件由 RNA 元数据推导"正是 RNA 最大收益：`rna_nodetree.cc` 只写 `PROP_INT, PROP_UNSIGNED`，UI 自动得到数字输入框，零行绘制代码。

`subtype` 还能叠加单位：高 8 位是 `PropertyUnit`（`PROP_UNIT_LENGTH` 等，[`RNA_types.hh` L220-L237](../../../source/blender/makesrna/RNA_types.hh#L220)），所以 `PROP_DISTANCE = 18 | PROP_UNIT_LENGTH`（L313）。取值用 `RNA_SUBTYPE_UNIT` / `RNA_SUBTYPE_VALUE` 位掩码拆（L266-L268）。

### 重点二：`get` / `set` 不在 `PropertyRNA` 上

最容易读错的一处：`PropertyRNA` 里**没有任何 `get` / `set` 字段**，它们在各自派生结构里：

| 派生结构 | 行号 | 读写回调 |
| --- | --- | --- |
| `BoolPropertyRNA` | 502-522 | `get` / `set` / `getarray` / `setarray` |
| `IntPropertyRNA` | 524-551 | 同上 + `range` |
| `FloatPropertyRNA` | 553-582 | 同上 + `range`、`precision` |
| `StringPropertyRNA` | 584-619 | `get` / `length` / `set` / `search` |
| `EnumPropertyRNA` | 621-639 | `get` / `set` / `item_fn` |
| `PointerPropertyRNA` | 641-652 | `get` / `set` / `type_fn` / `poll` |
| `CollectionPropertyRNA` | 654-666 | `begin` / `next` / `end` / `get` / `length` / `lookupint` / `lookupstring` |

分配时按 `type` 选尺寸（`rna_property_type_sizeof`，[`rna_define.cc` L757](../../../source/blender/makesrna/intern/rna_define.cc#L757)），所以拿到 `PropertyRNA *` 必须先看 `type` 才知道能强转成谁。`RNA_property_boolean_get` 一进门就 `BLI_assert(RNA_property_type(prop) == PROP_BOOLEAN)` 再 `reinterpret_cast<BoolPropertyRNA *>`（[`rna_access.cc` L2682-L2691](../../../source/blender/makesrna/intern/rna_access.cc#L2682)）——这个顺序不能反。

派生结构里还有一批 `_ex` 回调（`get_ex` / `set_ex` / `get_transform` / `set_transform`），只给运行时属性（Python `bpy.props`）用，签名多带 `StructRNA *` 与 `PropertyRNA *`，并在取值后 / 设值前插入一层变换（[`RNA_define.hh` L610-L670](../../../source/blender/makesrna/RNA_define.hh#L610)）。静态 RNA 一律用不带 `_ex` 的那套。

### 重点三：`rawoffset` 是唯一的"偏移量"

`rawoffset`（L476）配合 `rawtype`（L477）就是 `PropertyDefRNA::dnaname` 在运行期的残余投影——`makesrna.cc` 把 `offsetof(NodeRepeatItem, name)` 这样的表达式**烘焙成字面量**写进生成代码（[L1964-L1968](../../../source/blender/makesrna/intern/makesrna.cc#L1964)），运行期只剩一个 `int`。

关键前提：`prop->flag_internal & PROP_INTERN_RAW_ACCESS` 才填，否则生成代码写 `0, PROP_RAW_UNSET`（[L3647-L3652](../../../source/blender/makesrna/intern/makesrna.cc#L3647)）。所以**不能用 `rawoffset` 算普通属性的地址**——它常常就是 0。

## PropertyType 枚举

七个值，[`RNA_types.hh` L209-L217](../../../source/blender/makesrna/RNA_types.hh#L209)：

```cpp
enum PropertyType {
  PROP_BOOLEAN = 0, PROP_INT = 1, PROP_FLOAT = 2, PROP_STRING = 3,
  PROP_ENUM = 4, PROP_POINTER = 5, PROP_COLLECTION = 6,
};
```

| 值 | 数值 | 默认 UI 控件 | 变化条件 | 典型 DNA 类型 |
| --- | --- | --- | --- | --- |
| `PROP_BOOLEAN` | 0 | `Checkbox` | 有图标且无标签 → `IconToggle` | `char` / `short` / `int` 的某一位 |
| `PROP_INT` | 1 | `Num` 数字框 | `PROP_PERCENTAGE` / `PROP_FACTOR` → `NumSlider` | `int` / `short` / `char` |
| `PROP_FLOAT` | 2 | `Num` 数字框 | 数组 + `PROP_COLOR(_GAMMA)` → `Color` | `float` / `double` |
| `PROP_STRING` | 3 | `Text` 输入框 | 有 search 回调 → `SearchMenu` | `char *` 或 `char[N]` |
| `PROP_ENUM` | 4 | `Menu` 下拉 | `expand` → 一排按钮 | `int` / `short` / `char` 枚举 |
| `PROP_POINTER` | 5 | `SearchMenu` 选择框 | —— | `T *` 指针 |
| `PROP_COLLECTION` | 6 | 无按钮，`"%d items"` 标签 | 交给列表模板 | `ListBase` 或 `T *` + `int` 计数 |

DNA 类型的合法性由 `is_dnatype_float_compat` / `is_dnatype_int_compat` / `is_dnatype_boolean_compat` 在生成期强校验（[`rna_internal_types.hh` L777-L797](../../../source/blender/makesrna/intern/rna_internal_types.hh#L777)）。写错就是构建错误，例如把 `float` 字段包成 `PROP_INT`。

还有一类非字段属性：`PROP_BOOLEAN` 可指向**某个整数字段里的第 N 位**，即 `RNA_def_property_boolean_sdna(prop, nullptr, "flag", NODE_GEO_VIEWER_ITEM_FLAG_AUTO_REMOVE)`（[`rna_nodetree.cc` L8107](../../../source/blender/makesrna/intern/rna_nodetree.cc#L8107)）。此时 DNA 字段名是 `flag`，RNA 属性名却是 `auto_remove`——两者完全不等，反例 1 会再提。

## RNA_def_struct 与 RNA_def_property

先纠正误解：`RNA_def_struct` 和 `RNA_def_property` **都不是宏，是普通函数**。`RNA_define.hh` 里 4 处 `#define` 只有真身 `RNA_MAX_ARRAY_DIMENSION`（L29）、`RNA_MAX_ARRAY_LENGTH`（L24/L26）、`RNA_DYN_DESCR_MAX`（L752），其余全是函数声明。所谓"宏"的印象来自调用点长得像 DSL——一串 `RNA_def_property_xxx(prop, ...)` 连续写下来。

### `RNA_def_struct` 做了哪几件事

声明在 [`RNA_define.hh` L76](../../../source/blender/makesrna/RNA_define.hh#L76)，实现在 [`rna_define.cc` L926-L941](../../../source/blender/makesrna/intern/rna_define.cc#L926)，只是薄壳，真正干活的是 `RNA_def_struct_ptr`。`RNA_RepeatItem` 的调用只有三行（[`rna_nodetree.cc` L8033-L8040](../../../source/blender/makesrna/intern/rna_nodetree.cc#L8033)）：

```cpp
StructRNA *srna = RNA_def_struct(brna, "RepeatItem", nullptr);
RNA_def_struct_ui_text(srna, "Repeat Item", "");
RNA_def_struct_sdna(srna, "NodeRepeatItem");
```

逐句：第三参数 `from` 是"派生自哪个 RNA 类型"，`nullptr` 表示全新类型；第一参数是全局 `BlenderRNA`（所有类型的登记册，[L758-L773](../../../source/blender/makesrna/intern/rna_internal_types.hh#L758)）。`RNA_def_struct_ui_text` 只写两个字段（[L1147-L1151](../../../source/blender/makesrna/intern/rna_define.cc#L1147)）。`RNA_def_struct_sdna` 只写 `ds->dnaname`，落在 `StructDefRNA` 上。

注意 `RNA_def_struct_ptr` 内部有一行隐式调用：创建完 `StructDefRNA` 后立刻执行 `RNA_def_struct_sdna(srna, srna->identifier.c_str())`（[L866-L867](../../../source/blender/makesrna/intern/rna_define.cc#L866)），即**默认假设 RNA 标识符等于 DNA 结构名**。`RepeatItem` ≠ `NodeRepeatItem`，所以第三行是必须的显式纠正；而 `NodeGeometryViewerItem` 两边同名，那行 `RNA_def_struct_sdna` 冗余但无害（[L8102](../../../source/blender/makesrna/intern/rna_nodetree.cc#L8102)）。

<details><summary>展开：RNA_def_struct_ptr 的七个关键步骤</summary>

```cpp
StructRNA *RNA_def_struct_ptr(BlenderRNA *brna, const char *identifier, StructRNA *srnafrom)
{
  /* 1. 校验标识符合法性，非法则置 DefRNA.error */
  if (!RNA_validate_identifier(identifier, false, &error)) { ... }

  /* 2. 分配 StructRNA，登记为 DefRNA.laststruct
   *    （后续 RNA_def_property 靠它找容器） */
  srna = srna_ptr.get();
  DefRNA.laststruct = srna;

  /* 3. 若派生：复制 flag / icon / refine / reg / path，父类型记到 base */
  if (srnafrom) {
    srna->flag = srnafrom->flag;
    srna->refine = srnafrom->refine;
    srna->reg = srnafrom->reg;
    srna->base = srnafrom;
  }

  /* 4. 填 identifier / name / description 默认值 */
  srna->identifier = UString(identifier);
  srna->name = identifier;  /* 之后可能被 RNA_def_struct_ui_text 覆写 */
  srna->icon = ICON_DOT;    /* 仅非派生 */
  RNA_def_struct_flag(srna, STRUCT_UNDO);  /* 仅非派生 */

  /* 5. 加进 BlenderRNA 的 structs 向量 */
  rna_brna_structs_add(brna, std::move(srna_ptr));

  /* 6. 创建 StructDefRNA，默认把 DNA 名当成 RNA 标识符 */
  StructDefRNA *ds = MEM_new<StructDefRNA>("StructDefRNA");
  ds->srna = srna;
  rna_addtail(&DefRNA.structs, ds);
  RNA_def_struct_sdna(srna, srna->identifier.c_str());

  /* 7. 非派生类型自动获得内置属性 rna_properties */
  prop = RNA_def_property(&srna->cont, "rna_properties", PROP_COLLECTION, PROP_NONE);
  prop->flag_internal |= PROP_INTERN_BUILTIN;

  return srna;
}
```

</details>

第 7 步解释了为什么每个 `StructRNA` 的属性链表里**第一条不是你以为的那个**——`name` 前面还有一条 `rna_properties`，带 `PROP_INTERN_BUILTIN`，被 `RNA_struct_find_property` 的线性分支显式跳过（[L884-L889](../../../source/blender/makesrna/intern/rna_access.cc#L884)），也从 `prop_lookup_set` 里被摘掉（[L883-L885](../../../source/blender/makesrna/intern/rna_define.cc#L883)）。

### `RNA_def_property` 的两段式人生

`RNA_def_property` 在 [`rna_define.cc` L1165-L1394](../../../source/blender/makesrna/intern/rna_define.cc#L1165) 有 230 行，被 `#ifndef RNA_RUNTIME` / `#else` 劈成两条完全不同的路。

**构建期（makesrna 进程内）**：校验标识符并查重名 → 分配 `PropertyDefRNA` 挂到 `dcont->properties` → 按 `type` 用 `rna_property_type_sizeof` 分配正确尺寸的派生结构（[L1218-L1219](../../../source/blender/makesrna/intern/rna_define.cc#L1218)）→ 按 `type` 填默认区间（`PROP_INT` 给 `hard/soft min/max` 与 `step`，`PROP_FLOAT` 再给 `precision = 3`，`PROP_STRING` 给 `defaultvalue = ""` 且置 `PROP_NEVER_NULL`，[L1233-L1284](../../../source/blender/makesrna/intern/rna_define.cc#L1233)）→ 填公共字段（`magic`、`identifier`、`type`、`subtype`、`name` 默认等于 identifier、`rawtype = -1`）→ 非 `POINTER` / `COLLECTION` 自动置 `PROP_EDITABLE`，非 `STRING` 再置 `PROP_ANIMATABLE`（[L1315-L1327](../../../source/blender/makesrna/intern/rna_define.cc#L1315)）→ **静默调用对应类型的 `_sdna` 函数**（[L1339-L1378](../../../source/blender/makesrna/intern/rna_define.cc#L1339)）→ 挂 fallback update 标签 → `rna_addtail(&cont->properties, prop)`。

**运行期**：上面全被 `#else` 跳过，只做 `PROP_IDPROPERTY` 标记 + `PROP_INTERN_RUNTIME` + 插入查找集 + 挂链表（[L1383-L1391](../../../source/blender/makesrna/intern/rna_define.cc#L1383)）。

第 7 步是枢纽：它在 `DefRNA.silent = true` 掩护下调用，把"属性名在 DNA 里找不到同名字段"这种常规报错压掉，留给后续显式 `_sdna` 纠正，或等生成访问器时由 `rna_def_property_get_func` 报 "has no valid dna info"（[`makesrna.cc` L619-L627](../../../source/blender/makesrna/intern/makesrna.cc#L619)）。

往下每个 `RNA_def_property_xxx` 都是**纯字段赋值**，没有魔法：`RNA_def_property_ui_text` → `prop->name = name; prop->description = description;`；`RNA_def_property_ui_icon` → `prop->icon = icon;`；`RNA_def_property_string_funcs` → 按 `PROP_STRING` 分支把三个 `const char *` 强转塞进 `get` / `length` / `set`；`RNA_def_property_struct_type` → `POINTER` 写 `pointer_type`、`COLLECTION` 写 `item_type`、别的类型直接报错。

回调参数为什么是 `const char *` 而非函数指针？因为这些调用写于 **makesrna 自己的编译期**，而回调函数属于 Blender 主程序——两者符号不共享，只能先传名字、后由 makesrna 把名字拼进生成的 C 源码。拼接规则极简单：`rna_construct_function_name` 就是 `"%s_%s_%s"`（结构名_属性名_get/set，[`makesrna.cc` L353-L357](../../../source/blender/makesrna/intern/makesrna.cc#L353)）。所以 `RepeatItem` 的 `name` 生成访问器叫 `RepeatItem_name_get`。

## StructDefRNA / PropertyDefRNA：与 DNA 的桥

这两个结构是 RNA 与 DNA 唯一接头，定义在 [`rna_internal.hh` L71-L115](../../../source/blender/makesrna/intern/rna_internal.hh#L71)，全部被 `#ifndef RNA_RUNTIME` 包住。

**`StructDefRNA`**（L102-L115）：`cont`（`ContainerDefRNA`，内含属性定义链表）、`srna`（反指 RNA 结构）、`filename`、`dnaname`（**DNA 结构名**）、`dnafromname` / `dnafromprop`（派生场景）、`functions`。`ContainerDefRNA` 只有 `next` / `prev` / `cont` / `properties`（[L55-L60](../../../source/blender/makesrna/intern/rna_internal.hh#L55)）；`cont` 指回运行期 `ContainerRNA`，`properties` 是本容器下所有 `PropertyDefRNA` 链表——这就是 `rna_find_struct_property_def` 从一个 `PropertyRNA *` 反查 DNA 信息的依据（[`rna_define.cc` L198-L222](../../../source/blender/makesrna/intern/rna_define.cc#L198)）。

**`PropertyDefRNA`**（L71-L100）：`cont` / `prop`（双向反指）、`dnastructname` / `dnastructfromname` / `dnastructfromprop`（结构名与派生路径）、`dnaname`（**DNA 字段名**，也可是 `a.b` / `a->b` 路径）、`dnatype`（如 `char` / `float`）、`dnaarraylength`、`dnapointerlevel`（`char **` 是 2）、`dnadefaultdata`、`dnalengthstructname` / `dnalengthname` / `dnalengthfixed`（集合长度）、`booleanbit` / `booleannegative`（位域）、`enumbitflags`。

### 三个关键概念

**`offset`（字节偏移）在 `PropertyDefRNA` 里没有独立字段**——它是 `dnastructname` + `dnaname` 的**函数**。真正算出来只发生在 makesrna 生成代码那一刻，产出 `offsetof(NodeRepeatItem, name)` 这样的字面表达式（[`makesrna.cc` L1960-L1969](../../../source/blender/makesrna/intern/makesrna.cc#L1960)）。offset 是**编译产物**，不是数据。这是理解"改运行期 RNA 改不动数据"的钥匙。

**`length`（数组长度）** 有两个互斥来源：结构体里写死的数组（`char name[64]`）→ `dnaarraylength` 直接来自 SDNA，顺手写进 `prop->arraylength[0]` 与 `totarraylength`（[`rna_define.cc` L2347-L2355](../../../source/blender/makesrna/intern/rna_define.cc#L2347)）；指针 + 配套计数变量（`NodeRepeatItem *items; int items_num;`）→ `dnalengthname = "items_num"`，运行期由 `CollectionPropertyRNA::length` 回调实时读（[L2946-L2963](../../../source/blender/makesrna/intern/rna_define.cc#L2946)）。`repeat_items` 走的正是第二条：`RNA_def_property_collection_sdna(prop, nullptr, "items", "items_num")`（[`rna_nodetree.cc` L8064](../../../source/blender/makesrna/intern/rna_nodetree.cc#L8064)）。

**`dna_name`（DNA 字段名）** 是三者里最"软"的：缺省值是属性名，但可显式改成完全不同的名字，甚至改成跨结构路径。`rna_find_sdna_member` 支持 `.`（嵌套）与 `->`（解引用）递归下钻（[`rna_define.cc` L331-L388](../../../source/blender/makesrna/intern/rna_define.cc#L331)），让一个 RNA 属性指向"隔着两层指针的那个字段"。

跨结构例子：`RNA_def_struct_sdna_from(srna, "NodeGeometryRepeatOutput", "storage")`（[`rna_nodetree.cc` L8061](../../../source/blender/makesrna/intern/rna_nodetree.cc#L8061)）意思是"这个 RNA 类型本体是 `bNode`，但属性字段要去 `bNode.storage` 解出来的地方找"。生成的 `rna_print_data_get` 正是照此拼的（[`makesrna.cc` L330-L348](../../../source/blender/makesrna/intern/makesrna.cc#L330)）：

```cpp
/* dnastructfromname 与 dnastructfromprop 都非空时 */
NodeGeometryRepeatOutput *data =
    (NodeGeometryRepeatOutput *)(((bNode *)ptr->data)->storage);
/* 否则 */
NodeGeometryRepeatOutput *data = (NodeGeometryRepeatOutput *)(ptr->data);
```

## 完整实例：RNA_RepeatItem

`RepeatItem` 的属性并不写在 `rna_def_geo_repeat_item` 里，而来自共享模板 `rna_def_node_item_array_socket_item_common`（[`rna_nodetree.cc` L4951-L5006](../../../source/blender/makesrna/intern/rna_nodetree.cc#L4951)）——整个几何节点系统十几个 item 类型共用它（Repeat、Viewer、Simulation、Bake、Closure……），靠模板参数区分。

```cpp
static void rna_def_node_item_array_socket_item_common(
    StructRNA *srna, const char *accessor, const bool add_socket_type,
    const bool add_vector_socket_dimensions = false)
{
  static LinearAllocator<> allocator;
  PropertyRNA *prop;

  char name_set_func[128];
  SNPRINTF(name_set_func, "rna_Node_ItemArray_item_name_set<%s>", accessor);
  char item_update_func[128];
  SNPRINTF(item_update_func, "rna_Node_ItemArray_item_update<%s>", accessor);
  const char *item_update_func_ptr = allocator.copy_string(item_update_func).c_str();
  char socket_type_itemf[128];
  SNPRINTF(socket_type_itemf, "rna_Node_ItemArray_socket_type_itemf<%s>", accessor);
  char color_get_func[128];
  SNPRINTF(color_get_func, "rna_Node_ItemArray_item_color_get<%s>", accessor);

  prop = RNA_def_property(srna, "name", PROP_STRING, PROP_NONE);
  RNA_def_property_string_funcs(
      prop, nullptr, nullptr, allocator.copy_string(name_set_func).c_str());
  RNA_def_property_ui_text(prop, "Name", "");
  RNA_def_struct_name_property(srna, prop);
  RNA_def_property_update(prop, NC_NODE | NA_EDITED, item_update_func_ptr);

  if (add_socket_type) {
    prop = RNA_def_property(srna, "socket_type", PROP_ENUM, PROP_NONE);
    RNA_def_property_enum_items(prop, rna_enum_node_socket_data_type_items);
    RNA_def_property_enum_funcs(
        prop, nullptr, nullptr, allocator.copy_string(socket_type_itemf).c_str());
    RNA_def_property_ui_text(prop, "Socket Type", "");
    RNA_def_property_clear_flag(prop, PROP_ANIMATABLE);
    RNA_def_property_update(prop, NC_NODE | NA_EDITED, item_update_func_ptr);
  }

  prop = RNA_def_property(srna, "color", PROP_FLOAT, PROP_COLOR_GAMMA);
  RNA_def_property_array(prop, 4);
  RNA_def_property_float_funcs(
      prop, allocator.copy_string(color_get_func).c_str(), nullptr, nullptr);
  RNA_def_property_clear_flag(prop, PROP_EDITABLE);
  RNA_def_property_ui_text(
      prop, "Color", "Color of the corresponding socket type in the node editor");
}
```

逐行对应到 UI 行为：

| 代码 | `PropertyRNA` 里的实际值 | UI / 运行期表现 |
| --- | --- | --- |
| `"name", PROP_STRING, PROP_NONE` | `type = PROP_STRING`，`flag` 自动含 `PROP_EDITABLE` | `ButtonType::Text`，可编辑文本框 |
| `string_funcs(prop, nullptr, nullptr, set)` | `get = nullptr`，`set = rna_Node_ItemArray_item_name_set<...>` | 读走**自动生成**的 `RepeatItem_name_get`（直读 DNA `name`），写走手写 setter |
| `ui_text(prop, "Name", "")` | `name = "Name"`，`description = ""` | 面板标签 `Name`，tooltip 为空 |
| `struct_name_property(srna, prop)` | `srna->nameproperty = prop` | 集合按名字查成员的通用路径打通 |
| `update(prop, NC_NODE \| NA_EDITED, ...)` | `noteflag = NC_NODE \| NA_EDITED` | 改名后发节点通知 → 声明重建 |
| `"socket_type", PROP_ENUM` | `type = PROP_ENUM` | `ButtonType::Menu` 下拉 |
| `enum_items(...)` | `item = rna_enum_node_socket_data_type_items` | 下拉候选列表 |
| `enum_funcs(prop, nullptr, nullptr, itemf)` | `item_fn = ...socket_type_itemf<...>` | 候选**动态过滤**（只列该树类型支持的 socket 类型） |
| `clear_flag(prop, PROP_ANIMATABLE)` | `flag` 去掉 `PROP_ANIMATABLE` | 该属性不出现在动画/驱动器菜单 |
| `"color", PROP_FLOAT, PROP_COLOR_GAMMA` | `type = PROP_FLOAT`，`subtype = PROP_COLOR_GAMMA` | 数组 4 元素 → `ButtonType::Color` 色板 |
| `array(prop, 4)` | `arraydimension = 1`，`arraylength[0] = 4` | 颜色四个通道 |
| `float_funcs(prop, get, nullptr, nullptr)` | `get = ...item_color_get<...>`，`set = nullptr` | 只读；颜色由 socket 类型**算**出来 |
| `clear_flag(prop, PROP_EDITABLE)` | `flag` 去掉 `PROP_EDITABLE` | 色块灰显、点不动 |

最易忽略的是 `color`：它既没有 DNA 字段（`NodeRepeatItem` 里只有 `name` / `socket_type` / `_pad` / `identifier`，见 [`DNA_node_types.h` L3543](../../../source/blender/makesdna/DNA_node_types.h#L3543)），又标了只读，纯靠 `get` 回调从 `socket_type` 反查颜色（[`rna_nodetree.cc` L3960-L3967](../../../source/blender/makesrna/intern/rna_nodetree.cc#L3960)）。这是"RNA 属性不必对应字段"的活样本。

至于 `RNA_RepeatItem` 这个全局变量：`RNA_def_struct` 的标识符是 `"RepeatItem"`，`RNA_RepeatItem` 是 makesrna **生成**的，规则一行（[`makesrna.cc` L2920-L2925](../../../source/blender/makesrna/intern/makesrna.cc#L2920)）：

```cpp
fprintf(f, "extern struct StructRNA *RNA_%s;\n", srna->identifier.c_str());
```

所以 `identifier = "RepeatItem"` ⇒ 生成 `extern StructRNA *RNA_RepeatItem;`。这也是 `RepeatItemsAccessor::item_srna = &RNA_RepeatItem`（正篇 02-01 L992）能成立的原因——它取的是那个生成变量的地址，不是某个 C++ 类对象。

## 为什么需要 get/set 回调

如果所有 RNA 属性都是"字段直读"，`PropertyRNA` 根本不需要回调指针，只要偏移量就够。实际"直读"只是**默认路径**，三类情况必须接管：

**第一类：要计算的值。** `color` 是典型——DNA 里没有颜色字段，颜色由 `socket_type` 决定，没有偏移量能指向它，只能现场算（[`rna_nodetree.cc` L3959-L3967](../../../source/blender/makesrna/intern/rna_nodetree.cc#L3959)）。同理 `CollectionPropertyRNA::length` 是动态长度：链表集合不知道有多长，必须遍历或读计数字段。二者都靠回调把"存储形态"翻译成"RNA 视图"。

**第二类：要副作用的写操作。** `name` 的 setter 是教科书：

```cpp
template<typename Accessor>
static void rna_Node_ItemArray_item_name_set(PointerRNA *ptr, const char *value)
{
  bNodeTree &ntree = *reinterpret_cast<bNodeTree *>(ptr->owner_id);
  ItemT &item = *static_cast<ItemT *>(ptr->data);
  bNode *node = nodes::socket_items::find_node_by_item<Accessor>(ntree, item);
  BLI_assert(node != nullptr);
  nodes::socket_items::set_item_name_and_make_unique<Accessor>(*node, item, value);
}
```

源码：[`rna_nodetree.cc` L3948-L3957](../../../source/blender/makesrna/intern/rna_nodetree.cc#L3948)。若走默认路径，写 `name` 只会 `BLI_strncpy_utf8` 到那个 `char *`，什么都不会发生。实际语义要复杂得多——名字改了必须保证全节点内唯一，否则 socket 的 identifier 复用会乱。三件事只有这里能做：**从 `ptr->owner_id` 拿到节点树**（DNA 字段里没有这个指针）、**从 item 反查所属节点**（item 嵌在节点里，不会记住父节点）、**做唯一化**（要扫同节点其它 item）。

注意 setter 签名里没有 `PropertyRNA *`、没有 `StructRNA *`——它只拿到 `PointerRNA *ptr` 和值，说明回调**不需要知道自己是哪个属性**，编译期已绑定死。这也是静态 RNA 比运行时 RNA 省一层开销的地方。

**第三类：跨结构 / 位域访问。** `RNA_def_property_boolean_sdna(prop, nullptr, "flag", BIT)` 让 `PROP_BOOLEAN` 指向整数某一位，生成代码要做掩码与移位，没法用"偏移 + 类型"两个整数表达。`dnalengthname` 指向另一结构的计数字段时也需要自定义迭代器（`rna_iterator_array_*`）。

**补充：三种取值来源的优先级。** 即使有回调，运行时也不会盲调。以字符串为例，`property_string_get` 的顺序是（[`rna_access.cc` L4165-L4190](../../../source/blender/makesrna/intern/rna_access.cc#L4165)）：① 有 `IDProperty`（动态自定义属性覆盖）→ 读 IDProperty；② `sprop->get` 非空 → 调它；③ `sprop->get_ex` → 调它（运行时属性）；④ `sprop->get_default` → 调默认值回调；⑤ 都没有 → 返回 `sprop->defaultvalue`。第 ① 条优先于第 ② 条意味着：**在 Python 里给某个已有属性赋过值，可能只是往 IDProperty 塞了一份覆盖，DNA 一点没动**——这是很多"我明明设了值但 C 里没变"的根源。

## 用小数据走一遍

跟踪一个具体的值：Repeat 输出节点上第 0 个 item 的名字 `"Value"`，从 RNA 定义一路走到 `NodeRepeatItem.name` 的字节。

**准备阶段（构建时，已固化）**

1. `rna_def_geo_repeat_item` 调 `RNA_def_struct(brna, "RepeatItem", nullptr)` → 得到 `StructRNA`，`identifier = "RepeatItem"`。
2. `RNA_def_struct_sdna(srna, "NodeRepeatItem")` → `StructDefRNA::dnaname = "NodeRepeatItem"`。**没有**写任何 `StructRNA` 字段。
3. `RNA_def_property(srna, "name", PROP_STRING, PROP_NONE)` → 分配 `StringPropertyRNA`，`identifier = "name"`，`type = PROP_STRING`，`flag |= PROP_EDITABLE`；默认 sdna 把 `dnaname` 也设成 `"name"`。
4. `RNA_def_property_string_funcs(prop, nullptr, nullptr, set)` → `sprop->set` 设为回调名串，`get` 保持 `nullptr`。
5. `RNA_def_struct_name_property(srna, prop)` → `srna->nameproperty = prop`。
6. makesrna 生成代码时发现 `get == nullptr` 但 DNA 信息齐全，于是自动生成 `RepeatItem_name_get`：

```cpp
void RepeatItem_name_get(PointerRNA *ptr, char *value)
{
  NodeRepeatItem *data = (NodeRepeatItem *)(ptr->data);
  if (data->name == nullptr) { *value = '\0'; return; }
  strcpy(value, data->name);
}
```

（模板见 [`makesrna.cc` L616-L723](../../../source/blender/makesrna/intern/makesrna.cc#L616)；`dnapointerlevel == 1` 时走 `char *` 分支。）

**查询阶段（运行时）**

7. 某处持有 `PointerRNA{owner_id = &ntree.id, type = &RNA_RepeatItem, data = &item}`。
8. `RNA_struct_find_property(&ptr, "name")` → 走 `ptr->type->cont.prop_lookup_set` 命中第 3 步那个 `PropertyRNA`（[`rna_access.cc` L874-L893](../../../source/blender/makesrna/intern/rna_access.cc#L874)）。找不到就沿 `srna->base` 上溯。
9. `RNA_property_string_get(&ptr, prop)` → `rna_property_rna_or_id_get` 先判断有无 IDProperty 覆盖（这里假设没有）。
10. 落到 `property_string_get`：`sprop->get` 非空 → 调 `sprop->get(ptr, string_ret.data())`。
11. `RepeatItem_name_get` 把 `ptr->data` 强转成 `NodeRepeatItem *`，`strcpy` 出 `"Value"`。

**一句话总结**：`PropertyRNA` 负责"名字对不对"，`StringPropertyRNA::get` 负责"怎么读"，生成代码里的 `NodeRepeatItem *` 强转负责"读哪里"。三者没有一个是运行时可改的——全部在 makesrna 跑完那一刻定死。

正篇 01-02 的 `socket_name_ptr(&tree->id, *RepeatItemsAccessor::item_srna, &item, "name")` 四个参数到这一步就完全对应上：`&tree->id` 变 `owner_id`、`*item_srna` 变 `type`、`&item` 变 `data`、`"name"` 成为第 8 步的查找键。详见 [`node_declaration.cc` L1005-L1014](../../../source/blender/nodes/intern/node_declaration.cc#L1005)。

## 反例与边界

**1. 以为 RNA 属性名等于 DNA 字段名。** 缺省确实如此（`RNA_def_property` 静默把 `dnaname` 设成 `identifier`），但反例就在同一文件：`RNA_def_property_boolean_sdna(prop, nullptr, "flag", NODE_GEO_VIEWER_ITEM_FLAG_AUTO_REMOVE)`（[`rna_nodetree.cc` L8107](../../../source/blender/makesrna/intern/rna_nodetree.cc#L8107)）。RNA 属性叫 `auto_remove`，DNA 字段叫 `flag`，值在 `flag` 的第 N 位。用 `grep auto_remove DNA_node_types.h` 永远找不到。

**2. 以为所有属性都是字段直读。** `color` 在 `NodeRepeatItem` 里没有对应字段（[`DNA_node_types.h` L3543-L3550](../../../source/blender/makesdna/DNA_node_types.h#L3543)），纯靠 `get` 回调计算。另一类是集合长度：`repeat_items` 的长度来自 `items_num`，运行期才读。

**3. 以为 `StructRNA` 是 C++ 类。** 它是纯 POD 聚合体，无虚函数、无构造函数、无基类，不能被继承（派生靠 `base` 指针 + 复制字段实现，见 `RNA_def_struct_ptr`）。`RNA_RepeatItem` 也只是个 `StructRNA *` 全局变量，不是类实例。因此 `typeid` / `dynamic_cast` 一律用不上，类型判断全靠比对 `StructRNA *` 指针或 `identifier`。

**4. 修改 `PropertyRNA` 的 `type` 不会改底层数据。** 运行时改 `prop->type` 只会让后续代码按错误的派生结构强转（`int` 属性被当成 `FloatPropertyRNA`），是纯粹的内存破坏；它既不改 DNA 布局（那是构建期编译进 `.blend` 读写路径的），也不重新生成访问器（生成代码早已编译进二进制）。想加属性只有一条正路：改 `rna_*.cc` → 重跑 makesrna → 重编译。

**5. 以为 `StructRNA::properties` 是第一个字段。** 链表第一条是自动生成的 `rna_properties`（带 `PROP_INTERN_BUILTIN`）。以"取链表头"的方式拿"第一个真实属性"会拿到它，而它被 `RNA_struct_find_property` 的线性分支显式跳过（[`rna_access.cc` L884-L889](../../../source/blender/makesrna/intern/rna_access.cc#L884)）。正确做法是用 `RNA_struct_find_property`，或遍历时检查 `flag_internal`。

**6. 以为 `rawoffset` 可以当通用偏移量用。** 它只在 `PROP_INTERN_RAW_ACCESS` 置位时有效，否则生成代码写死 `0, PROP_RAW_UNSET`（[`makesrna.cc` L3647-L3652](../../../source/blender/makesrna/intern/makesrna.cc#L3647)）。`rawoffset == 0` 既可能是"字段恰在结构体开头"，也可能是"根本没填"——两者无法仅凭该值区分，必须查 `flag_internal`。

**7. 以为 `subtype` 只是显示用的。** `subtype` 参与构建期校验：`PROP_FLOAT` 的 `subtype` 若不是 `PROP_COLOR_GAMMA`，必须匹配 `float` / `double` 才有资格生成访问器（[`makesrna.cc` L632-L646](../../../source/blender/makesrna/intern/makesrna.cc#L632)）；`PROP_INT` 若标 `PROP_DISTANCE` 直接构建报错；`PROP_BOOLEAN` 只允许 `PROP_LAYER_MEMBER`。写错 subtype 不是显示异常，是编译失败。

**8. 以为 `RNA_def_struct_sdna` 会校验 DNA 里真有没有这个结构。** 它的校验被 `#if 0` 关掉了，注释明说"太多结构压根没有合法 DNA 名"（[`rna_define.cc` L949-L960](../../../source/blender/makesrna/intern/rna_define.cc#L949)）。`RNA_def_struct_sdna_from` 才有真实校验（[L976-L982](../../../source/blender/makesrna/intern/rna_define.cc#L976)）。所以结构名写错，错误要到生成访问器时（"has no valid dna info"）才爆，甚至可能被 `DefRNA.silent` 吞掉。

**9. 以为 IDProperty 覆盖等于改了 DNA。** `property_string_get` 优先返回 IDProperty 的值（[`rna_access.cc` L4167-L4171](../../../source/blender/makesrna/intern/rna_access.cc#L4167)）。Python 侧赋过的值可能只存在于 IDProperty 层，DNA 字段原封未动。反过来，`RNA_RepeatItem.name` 有自定义 setter，走的是真写 DNA 的路径（`set_item_name_and_make_unique`），所以 Repeat 的改名是"真改"而非覆盖——这个差别是正篇 01-02"名字唯一事实源"结论的隐式前提。

## 对理解 Repeat 的帮助

**正篇 02-01 L992 的 `item_srna = &RNA_RepeatItem`。** 现在能说清它买了什么：一个 `StructRNA *` 就是整份"item 类型说明书"的入口。拿到它，就同时拿到 `name` / `socket_type` / `color` 的属性定义、`nameproperty` 登记、`NC_NODE | NA_EDITED` 的更新语义，以及 `RepeatItem_name_get` 这个访问器。`RepeatItemsAccessor` 之所以能对十几个不同 item 类型写成同一份模板代码，是因为所有类型差异都被压进了一个指针。

**正篇 02-03 的 `draw_active_item_props`。** 它做的正是三段式的第三段（[`NOD_socket_items_ui.hh` L107-L126](../../../source/blender/nodes/NOD_socket_items_ui.hh#L107)）：

```cpp
ItemT &item = (*ref.items)[*ref.active_index];
PointerRNA item_ptr = RNA_pointer_create_discrete(
    const_cast<ID *>(&tree.id), *Accessor::item_srna, &item);
draw_item(&item_ptr);
```

`item_srna` 在这里的作用是把"裸的 `NodeRepeatItem &`"升格成"带类型的 RNA 指针"。一旦有了 `item_ptr`，面板代码就能写 `layout->prop(&item_ptr, "socket_type")`，而完全不需要知道 `NodeRepeatItem` 的 C 布局——`PROP_ENUM` 自动给下拉，`item_fn` 自动过滤候选，`PROP_ANIMATABLE` 被清掉所以不出动画选项。这就是第 1 篇说的"StructRNA 是类、PropertyRNA 是成员变量、PointerRNA 是 this"的完整落地。

**正篇 01-02 L113 的 `socket_name_ptr(..., item_srna, &item, "name")` 四参数。** 四参数的意义现在是构造性的而非描述性的：`srna` 决定第 8 步在哪个 `prop_lookup_set` 里查、`data` 决定访问器把哪个地址当 `NodeRepeatItem *`、`"name"` 决定查哪一个——三者各自对应 `PointerRNA` 的一个字段（`type` / `data` / 查找键），而 `owner_id` 是第四个，它让 setter 能反查节点树做唯一化（见"为什么需要 get/set 回调"第二类）。**少了 `srna`，剩下三个参数凑不出一次合法的属性查询**——这就是它不可省的机制原因，而不只是"为了类型安全"。

顺带解释 01-02 那条结论的机制层依据：因为 `name` 是自定义 setter + 统一 update 回调，所以改 socket 标签必然走"真写 `NodeRepeatItem.name` → 发 `NC_NODE | NA_EDITED` → 重建声明"，不存在"只改了显示名"的旁路。名字的唯一事实源因此是结构保证的，不是约定。

## 继续阅读

- 上一篇 [01-RNA三层结构与职责](01-RNA三层结构与职责.md)：`BlenderRNA` / `StructRNA` / `PropertyRNA` / `PointerRNA` 四层分工。
- 下一篇 [03-PointerRNA与属性访问](03-PointerRNA与属性访问.md)：`PointerRNA` 的 `owner_id` / `type` / `data` 三元组与 `ancestors`，以及 `RNA_property_*_get/set` 的完整分派。
- 同章 [04-RNA_def_struct_sdna映射](04-RNA_def_struct_sdna映射.md)：`_sdna` / `_sdna_from` 的路径语法与跨结构绑定。
- 同章 [05-属性变更与更新通知](05-属性变更与更新通知.md)：`noteflag` → `BKE_ntree_update_tag_node_property` → 声明重建。
- 主系列 [02-Repeat区域数据模型](../../重复区域-dsh/02-Repeat区域数据模型/README.md)：`RNA_RepeatItem` 在 Repeat 中的实际使用。
- 主系列 [01-02-Zone输入输出与bundle迁移语义](../../重复区域-dsh/01-Zone系统基础/02-Zone输入输出与bundle迁移语义.md)：`socket_name_ptr` 与"名字唯一事实源"。
- 主系列 [02-03-SocketItems通用条目框架](../../重复区域-dsh/02-Repeat区域数据模型/03-SocketItems通用条目框架.md)：`RepeatItemsAccessor` 与 `draw_active_item_props`。
- 源码：[`RNA_types.hh`](../../../source/blender/makesrna/RNA_types.hh)、[`RNA_define.hh`](../../../source/blender/makesrna/RNA_define.hh)、[`rna_internal_types.hh`](../../../source/blender/makesrna/intern/rna_internal_types.hh)、[`rna_define.cc`](../../../source/blender/makesrna/intern/rna_define.cc)、[`makesrna.cc`](../../../source/blender/makesrna/intern/makesrna.cc)、[`rna_access.cc`](../../../source/blender/makesrna/intern/rna_access.cc)。
