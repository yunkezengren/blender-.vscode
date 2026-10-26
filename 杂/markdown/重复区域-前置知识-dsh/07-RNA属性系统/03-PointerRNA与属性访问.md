# 03 · PointerRNA 与属性访问

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](02-StructRNA与PropertyRNA.md) · [下一篇](04-RNA_def_struct_sdna映射.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `PointerRNA`——RNA 的"this 指针"，以及围绕它的属性访问函数族。Repeat 的 `node_layout_ex` 就靠它跨节点操作数据。主要源码：[`RNA_types.hh`](../../../source/blender/makesrna/RNA_types.hh)（总行数 1180，PointerRNA 定义在 L52）、[`RNA_access.hh`](../../../source/blender/makesrna/RNA_access.hh)（总行数 1159）、[`intern/rna_access.cc`](../../../source/blender/makesrna/intern/rna_access.cc)（总行数 8234，`RNA_pointer_create_discrete` 实现在 L181）。

## 先回答一个具体问题

`StructRNA` 描述的是类型——"RepeatItem 有 name、socket_type 这些属性"。那么"数组里第 1 个 item"这个**具体实例**，用什么表示？

答案是 `PointerRNA`。而 Repeat 的面板有个更棘手的需求：**在 Input 节点上，画 Output 节点的数据**。这就需要一个"指向不属于当前节点的实例"的 PointerRNA——`RNA_pointer_create_discrete` 正是为此而生。

## PointerRNA 的真实定义

`[讲解]` 源码（`RNA_types.hh` L52-L70+），四个字段，每个都带原文注释：

```cpp
struct PointerRNA {
  /**
   * The ID owning the referenced data. May be null when there is no owner ID. Generally, whenever
   * these is an owner ID this should be set though for things like rna paths and ancestors to
   * work.
   */
  ID *owner_id = nullptr;
  /**
   * Type of the referenced data. If there is any data, this has to be set. This may also be set in
   * some cases even if the data is null, leading to a "typed null" which is used in some cases.
   */
  StructRNA *type = nullptr;
  /**
   * Actual referenced data of the given #type. If set, the #type must also be set.
   */
  void *data = nullptr;

  /**
   * A chain of ancestors of this PointerRNA, if known. The last item is the closest ancestor.
   */
  ...（ancestors 字段，见下文）
};
```

`[讲解]` 逐个拆：

| 字段 | 类型 | 语义 | 可否为空 |
| --- | --- | --- | --- |
| `owner_id` | `ID *` | 哪个数据块拥有这块数据 | 可空（注释明说 "May be null"） |
| `type` | `StructRNA *` | 类型描述符 | 有 data 就必填；**可以 data 为空而 type 非空**（"typed null"） |
| `data` | `void *` | 实际数据指针 | 可空 |
| `ancestors` | 链 | 祖先指针链 | 可选（"if known"） |

`[讲解]` 注释里藏着两个不显然的设计：

**第一，"typed null"**：`type` 非空但 `data` 为空是合法状态。表示"我知道这里应该是个 RepeatItem，但现在没有"。UI 画"无活动项"时就是这个状态。

**第二，owner_id 的作用被注释点名**："for things like rna paths and ancestors to work"——没有 owner，路径解析和祖先链都失效。

## 为什么三件套缺一不可

`[讲解]` 用一个反证游戏：去掉任意一个字段会怎样。

| 去掉 | 后果 |
| --- | --- |
| 去掉 `type` | `RNA_property_string_get(ptr, prop)` 无从查起——`prop` 挂在 `StructRNA` 上，没有类型就没有属性表 |
| 去掉 `data` | 读不到任何实际值，属性系统退化为纯元数据 |
| 去掉 `owner_id` | 三处塌方：① IDProperty 无处安放（布尔属性的"是否被设过"存在 owner 的 ID 上）；② Python 包装无法管理引用计数（`pyRNA_struct` 要靠 owner 保命）；③ 路径解析（`nodes["X"].inputs[0]`）从哪个树根开始走不知道 |

`[讲解]` 第三条最容易被低估。一个 `bNodeSocket` 自己不知道自己属于哪棵树——DNA 里没有反向指针。`owner_id` 就是那根"回家"的线。

## PointerRNA 不拥有数据

`[讲解]` 这是使用侧最重要的纪律。看它的构造就明白：

```cpp
PointerRNA ptr{id, type, data};
```

三个裸指针，**没有任何引用计数、没有任何拷贝**。它是纯粹的"视图"：

| 问题 | 答案 |
| --- | --- |
| 析构 PointerRNA 会释放 data 吗 | ❌ 不会，它没有析构函数 |
| data 的生命周期谁管 | 拥有者（通常是 `owner_id` 指向的 ID 及其数据） |
| 能跨帧存吗 | ❌ data 可能随求值副本销毁而悬空 |
| 拷贝它安全吗 | ✅ 安全（就是个 24-40 字节的 POD），但拷的是"视图"，源数据没了两个都悬空 |

`[讲解]` 与智能指针的对照：`PointerRNA` ≈ "借用"（C++ 语义里的 borrow），永远不是"持有"。

## 属性访问函数族总览

`[讲解]` `RNA_access.hh`（1159 行）的函数极多，按用途分五组：

### 组一：构造

| 函数 | 特点 |
| --- | --- |
| `RNA_pointer_create(ID *id, StructRNA *type, void *data)` | 标准构造 |
| `RNA_pointer_create_discrete(...)` | 同名参数，**不建路径**（见下文专节） |
| `RNA_id_pointer_create(ID *id, PointerRNA *r_ptr)` | 从 ID 造"指向 ID 本身"的指针 |
| `RNA_path_resolve_session_id2(...)` | 从路径串解析出 PointerRNA |

### 组二：校验

```cpp
bool RNA_struct_pointer_validate(const PointerRNA *ptr, ID **r_id, StructRNA **r_type, void **r_data);
```

`[讲解]` 检查 pointer 的三件套是否自洽（data 非空则 type 必须非空等）。UI 层大量使用——数据可能已失效，先 validate 再读。

### 组三：属性定位

| 函数 | 返回 |
| --- | --- |
| `RNA_struct_find_property(ptr, identifier)` | 按名字找 `PropertyRNA*`，找不到返回 null |
| `RNA_struct_property_exists(ptr, identifier)` | bool 版 |
| `RNA_struct_find_property_at_index(ptr, index)` | 按声明序找 |

### 组四：按类型 get/set

`[讲解]` 全表（签名取自 `RNA_access.hh`）：

| 类型 | get | set |
| --- | --- | --- |
| boolean | `RNA_property_boolean_get(ptr, prop)` | `RNA_property_boolean_set(...)` |
| enum | `RNA_property_enum_get(...)` | `RNA_property_enum_set(...)` |
| int | `RNA_property_int_get(...)` | `RNA_property_int_set(...)` |
| float | `RNA_property_float_get(...)` | `RNA_property_float_set(...)` |
| string | `RNA_property_string_get_alloc(...)` | `RNA_property_string_set(...)` |
| pointer | `RNA_property_pointer_get(...)` | `RNA_property_pointer_set(...)` |
| collection | `RNA_property_collection_get(...)` | 增删走 `..._resize` 等 |

`[讲解]` 注意 string 的 `get_alloc`——**返回的缓冲区要调用方 free**。这是 C API 的内存纪律，忘记释放就是泄漏。

### 组五：写入的解耦（重要）

`[讲解]` `RNA_property_string_set`（`rna_access.cc` L4268-L4308）只做一件事：调 setter。**它不会触发 update 回调**。

`[讲解]` 通知由调用侧显式发起：UI 在 `interface_handlers.cc` 写完后调 `RNA_property_update`，Python 在 `bpy_rna.c` 同理。这就是"改数据"与"告诉世界数据变了"的两段式——05 篇整篇讲第二段，这里先立骨架。

## RNA_pointer_create_discrete：Repeat 的关键工具

`[讲解]` 实现全文（`rna_access.cc` L181-L189）：

```cpp
PointerRNA RNA_pointer_create_discrete(ID *id, StructRNA *type, void *data)
{
  PointerRNA ptr{id, type, data};

  if (data) {
    rna_pointer_refine(ptr);
  }

  return ptr;
}
```

`[讲解]` 五行。对比它和路径系的本质差别：

| | `RNA_pointer_create_discrete` | `RNA_path_resolve` 系 |
| --- | --- | --- |
| 输入 | 直接给 (id, type, data) 三件套 | 给路径串如 `nodes["Repeat Input"].outputs[0]` |
| 内部记录"怎么到达" | ❌ 不记录 | ✅ 全程记录 |
| 性能 | 构造 + refine | 逐段解析属性、每段可能走回调 |
| 数据能"非法"吗 | 调用方保证 | 路径不存在返回空 |

`[讲解]` "**discrete**"取"离散的、独立的"义：这个指针是**孤立的坐标**，只知道"在哪"，不知道"从哪来"。所以它适合表达**非标准的、路径系统描述不了的**引用。

## Repeat 实例：node_layout_ex 跨节点

`[讲解]` 完整场景（`node_geo_repeat.cc` L34-L66）：面板画在 Input 节点上，但 items 数据在 Output 节点上。

```cpp
static void node_layout_ex(ui::Layout &layout, bContext *C, PointerRNA *current_node_ptr)
{
  bNodeTree &ntree = *reinterpret_cast<bNodeTree *>(current_node_ptr->owner_id);
  bNode *current_node = static_cast<bNode *>(current_node_ptr->data);

  const bke::bNodeTreeZones *zones = ntree.zones();
  ...
  bNode &output_node = const_cast<bNode &>(*zone->output_node());
  PointerRNA output_node_ptr = RNA_pointer_create_discrete(
      current_node_ptr->owner_id, RNA_Node, &output_node);

  ...
  layout.prop(&output_node_ptr, "inspection_index", UI_ITEM_NONE, std::nullopt, ICON_NONE);
}
```

`[讲解]` 三个决定，逐个问"为什么"：

**为什么 owner 用 `current_node_ptr->owner_id`（还是那棵树）？** 因为 Output 节点和 Input 节点在同一棵 `bNodeTree`（一个 ID）里。owner 的正确语义是"数据归属于哪个可保存的数据块"，不是"当前 UI 聚焦谁"。

**为什么必须 discrete？** 假设用路径表达"从 Input 到 Output"：RNA 的路径语法沿**属性**走（`.inputs[0]`、`.name`），而"Input 节点的配对 Output"根本不是一个 RNA 属性——它是 `storage.output_node_id` 经 zone 解析出的**关系**。路径系统表达不了，只能直接把 data 递过去。

**为什么 `const_cast`？** `zone->output_node()` 返回 `const bNode *`（zone 缓存视为只读），而 `RNA_pointer_create_discrete` 的 `data` 参数是非 const `void *`，且后续 `layout.prop` 生成的控件要**写** `inspection_index`。这是 UI 编辑路径上"缓存只读、编辑可写"的接缝。

`[讲解]` 于是 `layout.prop(&output_node_ptr, "inspection_index", ...)` 画出的输入框，改的是**另一个节点**的字段。撤销记录会把它记成"对 Output 节点的属性修改"（owner + data 定位），完全合法。

## 用小数据走一遍

`[讲解]` 目标：从 RNA 读出 Repeat 第 2 个 item 的名字。

**起点数据**：

```text
Output 节点 identifier = 42
output_storage->items = [ {"Geometry",GEOMETRY,0}, {"Radius",FLOAT,1} ]
```

**五步**：

| 步 | 调用 | 结果 |
| --- | --- | --- |
| 1 | `RNA_pointer_create_discrete(tree_id, &RNA_RepeatItem, &items[1])` | ptr = {owner: 树ID, type: RepeatItem, data: &items[1]} |
| 2 | `RNA_struct_find_property(&ptr, "name")` | 查 `RNA_RepeatItem` 属性表 → `name` 的 PropertyRNA* |
| 3 | `RNA_property_string_get_alloc(&ptr, prop, NULL, 0, NULL)` | 走 04 篇机制：有 get 回调走回调；无则按生成的 `offsetof(NodeRepeatItem, name)` 读 `char*` 再拷贝 |
| 4 | 返回缓冲区 | `"Radius"`（调用方负责 free） |
| 5 | 用户输入 `"Size"` → `RNA_property_string_set` | 调 setter `set_item_name_and_make_unique`；**update 由 UI 侧另行触发**（05 篇） |

`[讲解]` 注意第 3 步：同一次读取，`RNA_RepeatItem.name` 在 RNA 定义里绑了自定义 setter（要去重名字），getter 是自动生成的字段直读——**读写两条路可以不对称**，这正是 02/04 篇讲过的属性系统弹性。

## 反例与边界

**1. 把 PointerRNA 当 owner 用。** 存一个 `PointerRNA` 成员跨帧引用 item，然后 items 数组 realloc——data 悬空，读它是未定义行为。指针只该在"同一次调用栈"内活命；跨帧要重查。

**2. owner 用错对象。** 给 `bNodeSocket` 造 pointer 时 owner 填了节点组树、data 却在求值副本树——IDProperty、动画、路径全挂错地方。判据：data 必须活在 owner 的数据里。

**3. 编辑树 pointer 塞进求值上下文。** 求值时同一棵树存在编辑版与求值版两份。`logged_zone_graphs` 用 `DEG_get_original` 写编辑树（12-02 篇），求值代码里的 pointer 则是副本树。混用=改错副本，用户看不见效果。

**4. 以为 `RNA_property_X_get` 永远安全。** data 为空的 typed null 上调 get 直接崩。UI 层先 `RNA_struct_pointer_validate` 再读，不是可选项。

**5. 以为 discrete pointer 能拼路径。** discrete 不记录到达方式；对它调 `RNA_path_from_id_property` 得不出有意义结果。需要路径就用 resolve 系构造。

**6. string get 忘了 free。** `RNA_property_string_get_alloc` 分配返回缓冲区。C 风格 API 里"alloc 后缀 = 调用方拥有"。

**7. set 之后不 update 就以为世界知道了。** 见组五——`RNA_property_string_set` 只写数据。自己调 setter 的 C 代码（如操作符 exec）必须补一次 update 或打标签（05 篇）。

**8. 用 `type` 与 `RNA_RepeatItem` 比地址判类型。** `StructRNA*` 全局唯一，比指针是对的；但**别比 `identifier` 字符串**——热路径上属性系统会被字符串比较拖垮，02 篇的 `nodes_by_type` 用指针键同此理。

## 对理解 Repeat 的帮助

| 正篇位置 | 本篇机制 |
| --- | --- |
| 02-01 `node_layout_ex` 跨节点画面板 | discrete pointer：路径表达不了的关系用裸三件套 |
| 02-01 `layout.prop(&output_node_ptr, "inspection_index")` | 按名字定位属性 → set → 撤销记录归 Output 节点 |
| 01-02 `socket_name_ptr(..., item_srna, &item, "name")` | 就是 `create_discrete(树ID, &RNA_RepeatItem, &item)` + 属性名"五子棋" |
| 02-03 `draw_active_item_props` | typed null 的用武之地：active_index 越界时画空不画崩 |

`[讲解]` **一句话收束**：Repeat 的 UI 层三大"违反直觉"——在 Input 上编辑 Output、socket 名字跟着 item 实时变、无活动项不崩溃——底下都是同一个 `PointerRNA`：`(owner, type, data)` 三件套随便拼，拼出路径系统表达不了的引用。

## 本篇速查

| 我想要 | 用什么 |
| --- | --- |
| 标准：把已知 (ID, 类型, 数据) 包成 RNA 对象 | `RNA_pointer_create` / `_discrete` |
| 从字符串路径定位 | `RNA_path_resolve_*` |
| 用前保险 | `RNA_struct_pointer_validate` |
| 拿属性描述符 | `RNA_struct_find_property` |
| 读写具体值 | `RNA_property_<type>_get/set` |
| 让"值变了"被世界知道 | `RNA_property_update`（本篇只指出存在，机制在 05 篇） |

## 继续阅读

- [04-RNA_def_struct_sdna映射](04-RNA_def_struct_sdna映射.md) —— 第 3 步里 `offsetof` 从哪来
- [05-属性变更与更新通知](05-属性变更与更新通知.md) —— set 与 update 解耦的下半段
- 正篇：[02-01 Repeat节点注册与UI](../../重复区域-dsh/02-Repeat区域数据模型/01-Repeat节点注册与UI.md) —— `node_layout_ex` 全解
