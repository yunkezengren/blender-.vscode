# 02 · bNodeSocket 与声明系统

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](01-bNode与bNodeTree.md) · [下一篇](03-NodeDeclarationBuilder.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `bNodeSocket`（socket 实例）与 `SocketDeclaration`（socket 声明）的分离——这是 Repeat 动态 socket 能"重建而不断链接"的根本原因。主要源码：[`DNA_node_types.h`](../../../source/blender/makesdna/DNA_node_types.h) 的 `bNodeSocket` 定义、[``NOD_node_declaration.hh`](../../../source/blender/nodes/NOD_node_declaration.hh)（总行数 826）、[`intern/node_socket.cc`](../../../source/blender/nodes/intern/node_socket.cc)（`refresh_node_socket` 在 L219）。

## 先回答一个具体问题

Repeat Output 有 3 个 item。用户在面板上改了其中一个的名字。3 个 socket 的**连线一条都没断**，为什么？

`[讲解]` 表面答案："改名不影响连线"。

但真相更微妙：**改名会触发整个节点重新声明 socket**——旧 socket 对象被销毁、新对象被创建。如果只是"新建 socket"，连线必然全断。

所以真正的问题是：**重建时怎么把连线迁移过去？**

答案：按 `identifier` 匹配。

## 两层结构

`[讲解]` 这是本篇的核心概念：

| | `SocketDeclaration` | `bNodeSocket` |
| --- | --- | --- |
| 是什么 | 声明（意图） | 实例（事实） |
| 存在哪 | 每次 declare 临时生成 | 持久化在 `bNode.inputs/outputs` |
| 有内存吗 | 无（只是描述） | 有（含默认值、连线） |
| 生命周期 | 短暂 | 长期 |

`[讲解]` 用类比：

- **`SocketDeclaration` 是蓝图**："我要一个 float 输入，名字叫 Radius"
- **`bNodeSocket` 是房子**："这里真的有一个槽，里面存着 1.5，还连着一条线"

**为什么分开？** 因为节点需要"重新声明自己"而不丢失状态。Repeat 增加 item 时，声明的形状变了，但已有 socket 的数据要保留。

## bNodeSocket 的字段

`[讲解]` 完整定义（DNA_node_types.h）：

```c
struct bNodeSocket {
  struct bNodeSocket *next = nullptr, *prev = nullptr;
  IDProperty *prop = nullptr;
  char identifier[64] = "";
  char name[64] = "";
  void *storage = nullptr;
  eNodeSocketDatatype type = {};
  eNodeSocketFlag flag = {};
  short limit = 0;
  eNodeSocketInOut in_out = {};
  bke::bNodeSocketType *typeinfo = nullptr;
  char idname[64] = "";
  void *default_value = nullptr;
  int stack_index = 0;
  eNodeSocketDisplayShape display_shape = SOCK_DISPLAY_SHAPE_CIRCLE;
  char attribute_domain = 0;
  char _pad[2] = {};
  ...
};
```

`[讲解]` 分组：

### 两个标识（关键）

```c
char identifier[64] = "";   /* 唯一标识，用于匹配 */
char name[64] = "";          /* 用户可见名 */
```

`[讲解]` 注释只说第一行是 "Unique identifier for mapping"——**"for mapping"** 正是用途：重建时用它映射旧 socket。

`[讲解]` **Repeat 的 socket identifier 是什么？** 正篇 02-03 讲过：

```cpp
static std::string socket_identifier_for_item(const NodeRepeatItem &item)
{
  return "Item_" + std::to_string(item.identifier);
}
```

所以是 `"Item_0"`、`"Item_1"`……

`[讲解]` 这个格式的意义：

- `Item_` 前缀区分于固定 socket（如 `"Iterations"`）；
- 数字用 item 的**稳定 id**，不是数组下标。

### 类型与方向

| 字段 | 用途 |
| --- | --- |
| `type` | socket 数据类型（`SOCK_FLOAT` 等） |
| `in_out` | 输入还是输出 |
| `idname` | socket 类型名（如 `"NodeSocketFloat"`） |
| `typeinfo` | 运行时类型信息指针 |

`[讲解]` `typeinfo` 与 `bNode.typeinfo` 一样是**运行时缓存**（指针不持久化）。

### 默认值与连线

| 字段 | 用途 |
| --- | --- |
| `default_value` | 未连线时用什么值 |
| `limit` | 最多允许几条连线 |

`[讲解]` `limit` 的注释值得读：

> "Maximum number of links that can connect to the socket. Read via #nodeSocketLinkLimit, because the limit might be defined on the socket type, in which case this value does not have any effect."

**两个层次的限制**：

- socket 类型（`bNodeSocketType`）可以定义默认 limit；
- socket 实例可以覆盖。

所以应该调 `nodeSocketLinkLimit()` 而不是直接读字段。

### UI 相关

| 字段 | 用途 |
| --- | --- |
| `display_shape` | 画成圆/方/菱形 |
| `stack_index` | 执行器栈上的位置 |

`[讲解]` `stack_index` 注释说 "Local stack index for 'node_exec'"——这是老执行模型遗留，新 lf 模型不用。

## SocketDeclaration 的角色

`[讲解]` 声明在 `NOD_node_declaration.hh`（总行数 826）。核心类型：

```cpp
class SocketDeclaration {
 public:
  StringRefNull name;
  StringRefNull identifier;
  eNodeSocketInOut in_out;
  ...
};
```

`[讲解]` 注意 `identifier` 字段在声明里**也存在**。这是关键：

**声明的 identifier 会被复制到实例上**。所以重建时：

1. 节点重新 `declare`，产生新的声明列表；
2. 每个声明带 identifier；
3. 按 identifier 匹配旧实例，复用。

## 重建流程：refresh_node_socket

`[讲解]` 这是本篇最关键的函数（`intern/node_socket.cc` L219 起）。

`[讲解]` 大致流程：

```text
1. 保存旧 socket 列表（old_inputs / old_outputs）
2. 执行 node_declare，得到新 SocketDeclaration 列表
3. 按声明重建 socket 实例：
   for each decl:
     if 存在旧 socket 且 identifier 匹配:
       复用旧 socket，只更新 name/display 等显示字段
     else:
       新建 socket
4. 未被复用的旧 socket 被删除（连带其连线）
```

`[讲解]` **第 3 步的"复用"是核心**：保留旧对象的地址，所以：

- 连线还是指向同一个 socket 对象；
- 连线不断。

`[讲解]` 具体看源码里的匹配逻辑（L592-L596 附近的调用）：

```cpp
refresh_node_socket(*bmain, ntree, node, old_inputs, new_inputs, SOCK_IN, node_decl);
refresh_node_socket(*bmain, ntree, node, old_outputs, new_outputs, SOCK_OUT, node_decl);
```

`[讲解]` 两次调用分别处理输入和输出。

## 为什么"按 identifier 匹配"能成立

`[讲解]` 前提是 **identifier 在重建前后不变**。Repeat 的 item socket 怎么保证？

看 `RepeatItemsAccessor`（正篇 02-03）：

```cpp
static std::string socket_identifier_for_item(const NodeRepeatItem &item)
{
  return "Item_" + std::to_string(item.identifier);
}
```

`[讲解]` identifier 来自 `item.identifier`——一个**单调递增、永不复用**的整数。

所以：

| 操作 | item.identifier | socket identifier | 连线 |
| --- | --- | --- | --- |
| 初始 | 0, 1, 2 | `Item_0`, `Item_1`, `Item_2` | 正常 |
| 改 `Item_1` 的名字 | 不变 | 不变 | ✅ 复用，不断 |
| 交换 1、2 的顺序 | 不变（跟着 item 走） | 不变 | ✅ 复用，不断 |
| 删除 `Item_1` | 剩下的还是 0, 2 | `Item_0`, `Item_2` | ✅ 只断 Item_1 的 |
| 新建一个 item | 3（最大 +1） | `Item_3` | 新 socket，无连线 |

`[讲解]` 四行说明：**只要 identifier 稳定，重建就是无损的**。

## 动态 socket 的声明方式

`[讲解]` Repeat 的 `node_declare` 怎么生成这些 socket？正篇 02-01 讲过：

```cpp
for (const int i : IndexRange(output_storage.items_num)) {
  const NodeRepeatItem &item = output_storage.items[i];
  const eNodeSocketDatatype socket_type = item.socket_type;
  const UString name = item.name ? UString(item.name) : ""_ustr;
  const UString identifier(RepeatItemsAccessor::socket_identifier_for_item(item));

  auto &input_decl = b.add_input(socket_type, name, identifier)
                         .socket_name_ptr(...)
                         .structure_type(StructureType::Dynamic);
  b.add_output(socket_type, name, identifier)
      .align_with_previous()
      .propagate_all({input_decl.index()})
      .structure_type(StructureType::Dynamic);
}
```

`[讲解]` 关键参数 `b.add_input(type, name, identifier)` 的**第三个参数**：

**这就是把 identifier 传给声明的接口**。所以声明 → 实例 → 匹配 的链路打通。

## 一个容易忽略的点：name 可以变，identifier 不能

`[讲解]` `.socket_name_ptr(...)` 让 socket 的 `name` 字段**绑定到** `item.name`（RNA 属性指针）。

效果：

- 用户改 item 名字 → socket 的 `name` **实时跟着变**（甚至不需要重建）；
- 但 `identifier` 保持 `"Item_N"` 不变。

`[讲解]` 所以"改名不断链接"有**两条路径**：

| 场景 | 实际发生什么 |
| --- | --- |
| 只改名 | `name` 被 RNA 指针更新，**根本没重建** |
| 改名字 + 其他变更（如改类型） | 重建，但按 identifier 匹配复用 |

`[讲解]` 正篇 01-02 讲的是第二条路径（会触发 `BKE_ntree_update_tag_node_property`）。

## 用小数据走一遍

`[讲解]` 一个 Repeat Output，2 个 item，然后改名。

**初始状态**：

```text
node.outputs (链表):
  [0] { identifier: "Item_0", name: "Geometry", type: SOCK_GEOMETRY }
      ← 连线: 来自 Set Position 节点的 Geometry 输出
  [1] { identifier: "Item_1", name: "Radius",   type: SOCK_FLOAT }
      ← 连线: 来自 Value 节点
```

**用户把 "Radius" 改名为 "Size"**：

**第 1 步：RNA setter**

```text
rna_Node_ItemArray_item_name_set(...)
  → set_item_name_and_make_unique(...)
  → items[1].name = "Size"
  → BKE_ntree_update_tag_node_property(ntree, node)
```

**第 2 步：节点树更新**

```text
树更新 → 触发 node_declare 重跑
```

**第 3 步：重建**

| 新声明 | identifier | 匹配旧 socket？ | 动作 |
| --- | --- | --- | --- |
| {name: "Geometry", id: "Item_0"} | `Item_0` | ✅ 匹配 [0] | 复用，更新 name |
| {name: "Size", id: "Item_1"} | `Item_1` | ✅ 匹配 [1] | 复用，更新 name |

**第 4 步：结果**

```text
node.outputs:
  [0] { identifier: "Item_0", name: "Geometry", ... }  ← 同一对象
  [1] { identifier: "Item_1", name: "Size", ... }      ← 同一对象，只改了 name
```

`[讲解]` **连线一条没断**——因为 socket 对象的地址没变。

## 反例与边界

### 反例 1：用数组下标作 identifier

如果 identifier 是 `"Item_0"`、`"Item_1"` 按顺序分配，删除中间 item 后重建就会错位匹配——把连线连到错误的 item 上。

### 反例 2：以为改名一定会重建

如果只是 name 变更且用了 `socket_name_ptr`，可能根本不触发重建（只是 RNA 指针更新）。

### 反例 3：以为 identifier 可以随便改

改了就断链接。identifier 是"契约"，不是"标签"。

### 反例 4：在 `node_declare` 里做耗时计算

`node_declare` 会在每次节点更新时重跑。它是热路径。

### 反例 5：忽略 socket 顺序的重要性

虽然按 identifier 匹配，但 UI 显示顺序按声明顺序。Repeat 用 `use_custom_socket_order()` 让 socket 顺序可控。

### 反例 6：以为 socket 是数组

是链表。重建后顺序由声明顺序决定。

## 对理解 Repeat 的帮助

`[讲解]` 本篇解释的核心问题——"改名不断链接"——正篇 01-02 用了整整一节讲。现在能给出完整答案：

| 层 | 机制 | 对应正篇 |
| --- | --- | --- |
| identifier 的稳定性 | `item.identifier` 单调递增不复用 | 01-02、02-02 |
| socket identifier 格式 | `"Item_" + id` | 02-03 |
| 声明 → 实例 | `add_input(type, name, identifier)` | 02-01 |
| 重建时匹配 | `refresh_node_socket` 按 identifier | 01-02 |
| name 实时绑定 | `socket_name_ptr` | 01-02 |

`[讲解]` **最关键的一条**：Repeat 的"动态 socket"不是"每次不同"——它每次生成**相同的 identifier**，只是 `name` 可能不同。所以重建是"外观变化"，不是"结构变化"。

理解了这一点，正篇 02-03 那句"socket 只是 item 的投影"就有了具体含义。

## 继续阅读

- [03-NodeDeclarationBuilder](03-NodeDeclarationBuilder.md) —— 声明的构建接口
- [05-拓扑缓存与更新传播](05-拓扑缓存与更新传播.md) —— 更新标签与重建触发
- [01-bNode与bNodeTree](01-bNode与bNodeTree.md) —— 节点的三个标识
