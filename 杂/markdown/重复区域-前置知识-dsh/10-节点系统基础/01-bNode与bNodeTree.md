# 01 · bNode 与 bNodeTree

[前置知识总入口](../README.md) · [本章导航](README.md) · [下一篇](02-bNodeSocket与声明系统.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲节点系统的两个最基础结构：`bNode`（一个节点）与 `bNodeTree`（一棵树）。主要源码：[`DNA_node_types.h`](../../../source/blender/makesdna/DNA_node_types.h)（实测 4047 行，`bNode` 定义在其中）、[`BKE_node.hh`](../../../source/blender/blenkernel/BKE_node.hh)（实测 1141 行）、[`BKE_node_runtime.hh`](../../../source/blender/blenkernel/BKE_node_runtime.hh)（实测 990 行）。

## 先回答一个具体问题

Repeat Input 和 Repeat Output 是两个独立的节点，它们怎么知道彼此是一对？

**第一层答案**（本篇）：`NodeGeometryRepeatInput` 的 storage 里存着 `output_node_id`，指向 Output 节点的 `bNode.identifier`。

`[讲解]` 这里的关键是 `identifier`。它的定义与注释（DNA_node_types.h）值得逐字读：

```c
/**
 * A value that uniquely identifies a node in a node tree even when the name changes.
 * This also allows referencing nodes more efficiently than with strings.
 *
 * Must be set whenever a node is added to a tree, besides a simple tree copy.
 * Must always be positive.
 */
int32_t identifier = 0;
```

`[讲解]` 三条约束：

1. **即使改名也唯一**——所以不能用 `name` 作引用；
2. **必须为正数**——0 保留作"未设置"哨兵；
3. **加入树时必须设置**——除了简单的树复制（那种情况保留原 id）。

`[讲解]` 这就是 Repeat 配对能跨版本可靠的原因：**用整数不用指针**（05 章讲过的原则）。

## bNode 的字段逐个

`[讲解]` 完整字段（DNA_node_types.h）：

```c
struct bNode {
  struct bNode *next = nullptr, *prev = nullptr;
  ListBaseT<bNodeSocket> inputs, outputs;
  char name[64] = "";
  int32_t identifier = 0;
  eNode_Flag flag = {};
  char idname[64] = "";
  bke::bNodeType *typeinfo = nullptr;
  int16_t type_legacy = 0;
  int16_t ui_order = 0;
  int16_t custom1 = 0, custom2 = 0;
  float custom3 = 0, custom4 = 0;
  NodeWarningPropagation warning_propagation = NODE_WARNING_PROPAGATION_ALL;
  char _pad[7] = {};
  ...
};
```

`[讲解]` 分组读：

### 链表与 socket

| 字段 | 用途 |
| --- | --- |
| `next` / `prev` | 在 `bNodeTree.nodes` 链表里的前后指针 |
| `inputs` / `outputs` | 输入/输出 socket 的链表（`ListBaseT<bNodeSocket>`） |

`[讲解]` 注意：**socket 是链表不是数组**。原因：

- socket 数量动态变化（Repeat 的 item 会增删）；
- 链表插入/删除 O(1)。

代价：随机访问 O(N)。所以需要 `ensure_topology_cache()` 建索引（后文讲）。

### 三个标识

`[讲解]` 一个节点有**三个**身份标识，容易混淆：

| 字段 | 类型 | 用途 | 稳定性 |
| --- | --- | --- | --- |
| `name` | `char[64]` | 用户可见名 | 可改 |
| `identifier` | `int32_t` | **跨引用**用 | 稳定、正数 |
| `idname` | `char[64]` | 节点类型名（如 `"GeometryNodeRepeatInput"`） | 类型级 |
| `type_legacy` | `int16_t` | 旧的整数类型 | 部分稳定 |

`[讲解]` 四个字段的注释揭示了重要信息：

**`identifier`** 的注释上文已读——是"跨引用"的唯一选择。

**`idname`** 的注释说：

> "String identifier of the type like 'FunctionNodeCompare'. Stored in files to allow retrieving the node type for node types including custom nodes defined in Python by addons."

`[讲解]` **这是关键**：`idname` 是**字符串**，所以能持久化到文件里。自定义节点（Python 插件）的 `type_legacy` 在运行时生成、不稳定，但 `idname` 稳定。

`[讲解]` **`type_legacy`** 的注释特别长，说明它是个兼容遗留：

> "Legacy integer type for nodes. It does not uniquely identify a node type, only the `idname` does that. For example, all custom nodes use #NODE_CUSTOM but do have different idnames."

`[讲解]` 三句话：

1. **不唯一**——所有自定义节点都是 `NODE_CUSTOM`；
2. **主要用于兼容**——老文件里存的是这个整数；
3. **正在逐步淘汰**——注释给出"新代码应该用 idname 或访问器方法"。

`[讲解]` 但注释也说了保留它的理由：

> "A main benefit of this integer type over using idnames currently is that integer comparison is much cheaper than string comparison, especially if many idnames have the same prefix (e.g. 'GeometryNode')."

**整数比较比字符串快**，尤其当大量 idname 有相同前缀时。这是个务实的折衷。

### 类型信息缓存

```c
bke::bNodeType *typeinfo = nullptr;
```

`[讲解]` 注释（L 注释）说："Type information retrieved from the #idname. TODO: Move to runtime data."

**这行很重要**：`typeinfo` 是**运行时缓存**（从 `idname` 查出来的），但当前存在 DNA 结构里。

`[讲解]` 后果：

- 它**不能持久化**（指针）；
- 读文件后必须重新填充；
- 未来会移到 runtime data（注释里的 TODO）。

### UI 相关

| 字段 | 用途 |
| --- | --- |
| `ui_order` | 节点在编辑器里的堆叠顺序（最近选择的在前） |
| `custom1..4` | 内建节点的临时属性（无 storage 的那些） |
| `flag` | 各种标志位（`NODE_MUTED`、`NODE_SELECT` 等） |

`[讲解]` `custom1..4` 的注释："Used for some builtin nodes that store properties but don't have a storage struct."

**这就是为什么有些节点没有 storage**——它们用 `custom1` 之类的通用字段代替。

`[讲解]` **`flag` 里的 `NODE_MUTED`** 与 Repeat 直接相关：正篇 06 章讲过 `versioning_500.cc` 要把 Repeat 节点从 muted 状态清出来，因为 zone 接口节点禁止静音。

## bNodeTree 的结构

`[讲解]` `bNodeTree` 是节点树，关键字段：

| 字段 | 用途 |
| --- | --- |
| `nodes` | 节点链表 |
| `id` | ID 结构（所有 Blender 数据块的头） |
| `type` | 树类型（`NTREE_GEOMETRY` 等） |
| `interface` | 节点组接口（输入/输出声明） |
| `runtime` | **运行时数据**（见下） |

`[讲解]` 最后一个 `runtime` 是关键设计：**运行时数据与持久化数据分离**。

看 `BKE_node_runtime.hh` 的 `bNodeTreeRuntime`（990 行的头文件）：

```cpp
struct bNodeTreeRuntime {
  /** Allows logging zone graphs purely for debugging purposes. */
  std::unique_ptr<LoggedZoneGraphs> logged_zone_graphs;

  /** Storage of nodes based on their identifier. */
  Map<int32_t, bNode *> nodes_by_id;
  ...
};
```

`[讲解]` 两个字段特别值得注意：

### `nodes_by_id`

`[讲解]` 注释说："Storage of nodes based on their identifier. Also used as a contiguous array of nodes to allow simpler and more cache friendly iteration. Supports lookup by integer or by node."

`[讲解]` 这是**索引结构**。为什么需要？

因为节点链表只能顺序遍历。而按 id 查找（Repeat 的配对！）需要 O(1)。

**这就是 `tree.node_by_id(storage.output_node_id)` 的实现基础**——正篇里配对的第一步。

### `logged_zone_graphs`

`[讲解]` 上一章 12-02（图导出）讲过的调试设施。它存在 runtime 里，说明**不持久化**。

## 拓扑缓存

`[讲解]` 节点系统有大量"邻接查询"需求：

- 这个 socket 连到哪些 socket？
- 这个节点有哪些上游？

链表结构下这些都是 O(N)。所以 Blender 提供了 `ensure_topology_cache()`（`BKE_node_runtime.hh`）。

`[讲解]` 缓存内容（大致）：

| 缓存 | 内容 |
| --- | --- |
| `nodes_by_id` | id → 节点 |
| `nodes_by_type_map` | 类型 → 节点列表 |
| `links_by_socket` | socket → 连线列表 |
| `sorted_nodes` | 拓扑排序结果 |

`[讲解]` **关键约束**：缓存会失效。任何修改树结构的操作后都必须重建（或标脏）。

`[讲解]` 正篇 02-01 有一处直接相关：

```cpp
params.node_tree.ensure_topology_cache();
```

在 `node_gather_link_searches` 建完一对节点后调用——因为要立即用新结构查询。

## 节点的生命周期

`[讲解]` 一个节点从创建到销毁：

| 阶段 | 发生什么 | 谁负责 |
| --- | --- | --- |
| 创建 | `MEM_new<bNode>` + `node_init` 回调 | 节点系统 |
| 挂入树 | 加入 `nodes` 链表、设 `identifier` | `node_add` 类函数 |
| 编辑 | 改 socket、改属性、改连线 | 操作符 / UI |
| 求值 | 编译成 lf 图 | 节点求值器 |
| 销毁 | `node_free_storage` + 释放 socket | 节点系统 |

`[讲解]` 注意"挂入树"时的 **`identifier` 必须设置**——这是 DNA 注释里明确要求的：

> "Must be set whenever a node is added to a tree, besides a simple tree copy."

**为什么"树复制"例外？** 因为复制整棵树时保留所有 id 是合理的（副本是一份独立的图，内部引用关系不变）。

## Repeat 的配对机制全链路

`[讲解]` 现在能把正篇 01-01 的配对讲透了：

```text
第 1 层（DNA）：
  NodeGeometryRepeatInput::output_node_id  = 42
  （42 是 Repeat Output 节点的 bNode.identifier）

第 2 层（运行时索引）：
  bNodeTreeRuntime::nodes_by_id[42] → bNode*

第 3 层（节点协议）：
  RepeatZoneType::get_corresponding_output_id(node)
    返回 storage->output_node_id 的引用

第 4 层（通用算法）：
  find_zone_nodes() 用上面的协议找到配对的 Input/Output
```

`[讲解]` 四层分工：

| 层 | 提供什么 |
| --- | --- |
| DNA | 持久化的 id 数值 |
| Runtime | O(1) 的 id → 节点查找 |
| 节点协议 | "怎么从 Input 拿到 Output 的 id" |
| 通用算法 | "怎么用协议建 zone" |

`[讲解]` 这个分层设计的好处：**通用算法不需要知道 Repeat 的存在**。它只调 `get_corresponding_output_id()` 协议，Simulation / Foreach / Closure 各实现自己的版本。

## 用小数据走一遍

`[讲解]` 建一对 Repeat 节点，跟踪 id：

**第 1 步：创建 Repeat Output**

```text
节点系统分配 bNode：
  identifier = 42（下一个可用 id）
  idname = "GeometryNodeRepeatOutput"
  type_legacy = GEO_NODE_REPEAT_OUTPUT
  storage = NodeGeometryRepeatOutput{ items: [Geometry], items_num: 1, next_identifier: 1 }
```

**第 2 步：创建 Repeat Input**

```text
  identifier = 43
  idname = "GeometryNodeRepeatInput"
  storage = NodeGeometryRepeatInput{ output_node_id: 0 }   ← node_init 设为 0
```

**第 3 步：建立配对**

```text
input_storage.output_node_id = 42   ← 指向 Output
```

`[讲解]` 注意第 2 步的 `output_node_id = 0`——这正是 02-01 讲的"哨兵值"：

> "0 不是'指向第一个节点'，而是哨兵值（sentinel），表示'尚未配对'"

因为 id 必须为正数（DNA 注释），所以 0 是安全的"未设置"标记。

**第 4 步：查询**

```text
tree.runtime->nodes_by_id.lookup(42) → Repeat Output 的 bNode*
```

`[讲解]` O(1) 哈希查找。

## 反例与边界

### 反例 1：用 name 代替 identifier 做引用

name 可改，引用会断。DNA 注释明确说了 identifier 的用途是"即使改名也唯一"。

### 反例 2：以为 identifier 是从 0 开始连续分配

它只是"唯一且为正"，不保证连续。删除节点后 id 不回收。

### 反例 3：假设 `type_legacy` 唯一

不唯一——所有 Python 自定义节点都是 `NODE_CUSTOM`。

### 反例 4：`typeinfo` 持久化

它是指针，不能存文件。读文件后必须重新填充。

### 反例 5：以为 socket 是数组

是链表。随机访问要先用拓扑缓存。

### 反例 6：修改树后不重建拓扑缓存

用旧的 `nodes_by_id` 查会拿到已删除的节点。

## 对理解 Repeat 的帮助

`[讲解]` 本篇解释的三件事直接支撑正篇：

| 本篇概念 | Repeat 中的落点 | 正篇位置 |
| --- | --- | --- |
| `identifier` | `output_node_id` 指向它 | 01-01 第 1 层 |
| `nodes_by_id` | `tree.node_by_id()` 的实现 | 01-01 全篇 |
| `NODE_MUTED` | versioning 要清除的标志 | 06 章 |
| `ensure_topology_cache` | 建对后立即查询 | 02-01 |

`[讲解]` **最关键的一条**：Repeat 的配对**不是靠空间关系或名字**，而是靠一个持久化的整数 + 一次 O(1) 查表。这个设计让：

- 用户可以把两个节点拖到任意位置；
- 可以任意改名；
- 保存/重开文件后关系不变。

## 继续阅读

- [02-bNodeSocket与声明系统](02-bNodeSocket与声明系统.md) —— socket 与声明的关系
- [05-拓扑缓存与更新传播](05-拓扑缓存与更新传播.md) —— 缓存细节
- [03-NodeDeclarationBuilder](03-NodeDeclarationBuilder.md) —— 动态 socket 怎么声明
