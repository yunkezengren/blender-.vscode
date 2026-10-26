# 04 · bNodeType 注册

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](03-NodeDeclarationBuilder.md) · [下一篇](05-拓扑缓存与更新传播.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `bNodeType`——节点类型的注册结构。`node_register` 回调里的每一次赋值，都是在填这个结构体。主要源码：`BKE_node.hh`（总行数 1141，bNodeType 定义）、`node_geo_repeat.cc`（372 行，两个注册函数在 L220 之后）、`BKE_node_legacy_types.hh`。

> **行数复核说明**：本篇正文所有行数均用 `[System.IO.File]::ReadAllLines(path).Count` 实测（文件总行数，含空行与注释）。开头固定基准里写的 1141 是本章导航沿用的旧口径；当前工作树实测 [`BKE_node.hh`](../../../source/blender/blenkernel/BKE_node.hh) 为 **1363 行**，`bNodeType` 定义在 **L265–L475**。下文一律以实测为准。

## 先回答一个具体问题

**问题：我在 `source/blender/nodes/geometry/nodes/` 下新写了一个 `.cc`，定义了一个节点。Blender 是怎么知道这个节点该怎么初始化、该画什么、连线拖出来该搜到什么、存档时该写哪块内存的？**

`[讲解]` 答案是：你把这些答案全部写进了一个 `bke::bNodeType` 结构体，然后在程序启动时被调用一次的 `node_register()` 里，把它交给 `bke::node_register_type(ntype)` 登记到全局表里。此后每个 `bNode` 实例都通过 `node->typeinfo` 指回这个**唯一的、全局共享的类型对象**，所有"这个节点该怎么做"的问题都变成"去 `typeinfo` 里取对应字段并调用它"。

一句话总结：`bNode` 是**数据**（一条节点记录），`bNodeType` 是**这个类型的方法表 + 元数据**，`node_register()` 是**把方法表登记进全局注册表的动作**。Repeat Zone 的两个节点之所以行为差别那么大（一个持有一个 `int`，另一个持有堆上的 item 数组；一个不显示在连线搜索里，另一个显示两条），完全来自两个 `node_register()` 里赋值差异——没有别的机制。

---

## bNodeType 是什么

`[实测](../../../source/blender/blenkernel/BKE_node.hh#L259-L475)`：`BKE_node.hh` L265 开始，注释是 "Defines a node type. Initial attributes and constants for a node as well as callback functions implementing the node behavior."。结构体成员（不含末尾的 `is_type()` 成员函数）是 56 行成员声明，展开同行多声明（`height/minheight/maxheight` 一行三个、`inputs/outputs` 一行两个）后共 **59 个数据成员**，可以粗分成"数据字段"和"函数指针字段"两类。

它**不是**每个节点各有一份，而是**每个类型一份、全局共享**。所以标准写法是函数内 `static`：

```cpp
static void node_register()
{
  static bke::bNodeType ntype;              /* L151：进程级唯一，注册进全局表后一直活着 */
  common_node_type_base(&ntype, "GeometryNodeRepeatInput"_ustr, GEO_NODE_REPEAT_INPUT);
  ntype.ui_name = "Repeat Input";
  ntype.nclass = NODE_CLASS_INTERFACE;
  ntype.initfunc = node_init;
  /* ... 其余赋值 ... */
  bke::node_type_storage(
      ntype, "NodeGeometryRepeatInput", node_free_standard_storage, node_copy_standard_storage);
  bke::node_register_type(ntype);           /* L166：登记 */
}
NOD_REGISTER_NODE(node_register)           /* L168：让构建系统发现这个注册函数 */
```

`[讲解]` `static` 的三层含义：一是生命周期——`node_register_type` 存的是 `&nt`（指针），所以这个对象绝不能是栈上的临时变量；二是"只初始化一次"——C++ 保证函数局部 `static` 只初始化一次，重复调用 `node_register()`（比如单测里反复 `node_system_init`）不会把字段重置，但会重复 `add_new` 断言失败；三是免去 `MEM_new`——注册表退出时只对设置了 `free_self` 的类型才释放（[`node.cc`](../../../source/blender/blenkernel/intern/node.cc#L2901-L2918) L2914 注释："May be null if the type is statically allocated"）。

`[实测](../../../source/blender/nodes/geometry/nodes/node_geo_repeat.cc#L149-L167)`：Repeat Input 的注册函数体是 L149–L167，共 19 行；Output 在 L319–L339，共 21 行。这就是"注册一个节点"的全部代码量——剩下的都在别处定义的回调函数里。

---

## 字段分五组

`[提示]` 记 59 个字段的最好方式是按用途分组。绝大多数节点一辈子只碰其中 10~15 个。

### 第 1 组：身份（我是谁）

| 字段 | 声明位置 | Repeat Input | 作用 |
| --- | --- | --- | --- |
| `idname` | L266 | `GeometryNodeRepeatInput` | 全局唯一键，所有查表都按它（`node_type_find`） |
| `type_legacy` | L268 | `GEO_NODE_REPEAT_INPUT`(=2107) | 旧整数类型，DNA 里仍在写，大量分支判断依赖它 |
| `ui_name` | L270 | `"Repeat Input"` | 加节点菜单/搜索里显示的名字 |
| `ui_description` | L271 | 未设 | 悬停提示 |
| `ui_icon` | L272 | 未设 | 图标 |
| `enum_name_legacy` | L274 | `"REPEAT_INPUT"` | Python API 里的枚举名 |
| `storagename` | L287 | `"NodeGeometryRepeatInput"` | DNA 结构名，序列化按它反射读写 |

`[实测](../../../source/blender/blenkernel/BKE_node_legacy_types.hh#L479-L480)`：`GEO_NODE_REPEAT_INPUT 2107`、`GEO_NODE_REPEAT_OUTPUT 2108`。这两个宏定义在 `BKE_node_legacy_types.hh`（583 行），是该文件"legacy"注释里说的、仍在维护的整数枚举。

### 第 2 组：分类与标志（我在菜单长什么样、有哪些限制）

| 字段 | 声明位置 | 说明 |
| --- | --- | --- |
| `nclass` | L281 | 菜单分类与配色标签。Repeat 两个节点都是 `NODE_CLASS_INTERFACE`（=33，[L490](../../../source/blender/blenkernel/BKE_node.hh#L477-L494)） |
| `flag` | L282 | `eNode_Flag`，作为新节点初始 `bNode::flag` 的模板；`node_init` 里 `node->flag = NODE_SELECT \| NODE_OPTIONS \| (ntype->flag & ~NODE_PREVIEW)`（[node.cc L2603](../../../source/blender/blenkernel/intern/node.cc#L2603)）。Repeat 未设，合成器节点常用 `ntype.flag \|= NODE_PREVIEW` |
| `default_width` / `minwidth` / `maxwidth` | L276–L278 | 宽度，默认由 `NodeWidth`（L242–L257）给 140/100/700 |
| `height` / `minheight` / `maxheight` | L280 | 由 `node_type_base_defaults` 统一设为 100/30/FLT_MAX（[node.cc L5831-L5836](../../../source/blender/blenkernel/intern/node.cc#L5831-L5836)） |
| `no_muting` | L451 | **true 时该节点不能被静音**。Repeat 两个节点都设了（L161/L331），详见后文专节 |
| `ignore_inferred_input_socket_visibility` | L453 | 忽略推断出的 socket 可见性以改善体验（Switch/Menu Switch 等） |
| `deprecation_notice` | L455 | 非 null 表示仍可用但不推荐，绘制时加警示 tooltip（[node_draw.cc L2496-L2500](../../../source/blender/editors/space_node/node_draw.cc#L2496-L2500)） |

### 第 3 组：行为回调（我该做什么）

| 字段 | 声明位置 | 调用点 | Repeat Input |
| --- | --- | --- | --- |
| `declare` | L393 | `build_node_declaration`（[node_declaration.cc L35-L44](../../../source/blender/nodes/intern/node_declaration.cc#L35-L44)） | `node_declare`(L72) |
| `initfunc` | L320 | `node_init` [L2625-L2627](../../../source/blender/blenkernel/intern/node.cc#L2625-L2627) | `node_init`(L113) |
| `freefunc` | L328 | `node_free_node` [L5099-L5101](../../../source/blender/blenkernel/intern/node.cc#L5099-L5101) | 由 `node_type_storage` 填 |
| `copyfunc` | L330 | `node_copy_with_mapping` [L4397-L4399](../../../source/blender/blenkernel/intern/node.cc#L4397-L4399) | 由 `node_type_storage` 填 |
| `labelfunc` | L301 | `node_label` [L5738-L5741](../../../source/blender/blenkernel/intern/node.cc#L5732-L5745) | `node_label`(L121) |
| `insert_link` | L364 | 加连线时 [rna_nodetree.cc L1548 / node_relationships.cc L301](../../../source/blender/editors/space_node/node_relationships.cc#L301-L308) | `node_insert_link`(L129) |
| `gather_link_search_ops` | L409 | 连线拖拽搜索菜单 [link_drag_search.cc L296-L300](../../../source/blender/editors/space_node/link_drag_search.cc#L296-L300) | **显式置 nullptr**(L159) |
| `poll` / `poll_instance` | L352/L359 | 能否加入某棵树 | `common_poll_default` |
| `add_ui_poll` | L341 | 搜索菜单额外过滤 | 未设 |
| `draw_buttons` / `draw_buttons_ex` | L290/L292 | 节点上按钮 / 侧栏面板 | `draw_buttons_ex = node_layout_ex`(L162) |
| `draw_backdrop` | L295 | 背景绘制 | 未设 |
| `ui_class` / `ui_description_fn` | L307/L309 | 头部颜色类 / 动态描述 | 未设 |
| `updatefunc` | L312 | 编辑器里节点被改时（Repeat 用 `declare` + 声明刷新代替） | 未设 |
| `can_sync_sockets` | L462 | socket 集合随外部数据变化时显示 Sync 按钮 | 未设 |
| `register_operators` | L448 | 该类型自带算子（[node_ops.cc L127-L128](../../../source/blender/editors/space_node/node_ops.cc#L127-L128)） | Output 设 `node_operators`(L333) |
| `get_extra_info` | L412 | 节点下方附加信息（Group Output 用） | 未设 |
| `internally_linked_input` | L415 | 静音时输入内部接哪根线 | 未设 |
| `initfunc_api`/`freefunc_api`/`copyfunc_api` | L333–L335 | Python 注册版回调，与 C 回调叠加调用 | 未设 |

执行类回调（`init_exec_fn`/`exec_fn`/`gpu_fn`/`materialx_fn`/`build_multi_function`/`geometry_node_execute`/`get_compositor_operation`，L369–L385）与求值类（`eval_elem`/`eval_inverse_elem`/`eval_inverse`，L428–L441）也在这组。Repeat 两个节点只设了 `gpu_fn`（L163/L336）——几何侧的重复区域执行不在 `bNodeType` 上，而在 zone 构建器里，正篇 03 章讲。

### 第 4 组：存储（我的数据怎么活、怎么落盘）

| 字段 | 声明位置 | 说明 |
| --- | --- | --- |
| `storagename` | L287 | DNA 结构名；写盘按它反射（[node.cc L1322-L1325](../../../source/blender/blenkernel/intern/node.cc#L1322-L1329)），读盘同（[L1996-L2001](../../../source/blender/blenkernel/intern/node.cc#L1996-L2010)） |
| `freefunc` | L328 | 由 `node_type_storage` 填入 |
| `copyfunc` | L330 | 同上 |
| `blend_write_storage_content` | L421 | 存完结构体正文后**追加写**堆指针内容 |
| `blend_data_read_storage_content` | L422 | 读盘对应追加读 |
| `static_declaration` | L402 | 注册时用 `declare(nullptr,nullptr)` 建出的"脱离上下文"声明（后文） |
| `inputs`/`outputs` | L285 | 老式 `bNodeSocketTemplate` 静态模板表，只有纹理等旧节点还在用（`node_type_socket_templates`） |

### 第 5 组：zone 协议（怎么找到我的另一半）

`[实测]` **zone 协议不在 `bNodeType` 上**。`bNodeType` 里没有任何 `find_zone_input_id` / `get_corresponding_*` / `node_tree_socket_inference` 字段——本篇调研明确要求"以实测为准"，实测结论是：这套接口在**另一个类** `bke::bNodeZoneType`（[BKE_node.hh L1309-L1332](../../../source/blender/blenkernel/BKE_node.hh#L1304-L1332)，注意 L1304 的类注释：它存在的目的是"让代码对所有 kind 的 zone 自动生效，减少新增 zone 类型的样板"）：

| 字段/函数 | 位置 | 说明 |
| --- | --- | --- |
| `input_idname` / `output_idname` | L1311/L1312 | 两端 idname |
| `input_type` / `output_type` | L1313/L1314 | 两端 legacy 类型 |
| `theme_id` | L1315 | 区域配色（Repeat 用 `TH_NODE_ZONE_REPEAT`） |
| `get_corresponding_output_id(input_bnode)` | L1319 | **纯虚**，唯一必须由每个 zone 自己实现的 |
| `get_corresponding_input(tree, output_bnode)` | L1327/L1328 | 通用实现（基类提供） |
| `get_corresponding_output(tree, input_bnode)` | L1330/L1331 | 通用实现（基类提供） |
| `register_node_zone_type` | L1334 | 登记进全局 Vector |

`[勘误]` 任务提示里写的 `get_corresponding_input_ids`（复数、返回 id 列表）与 `find_zone_input_id` 在本工作树中**不存在**（全仓 grep 无命中）。实际形态是：Input 端只暴露 `get_corresponding_output_id`，Output→Input 的反查是**基类扫全树**实现的，见后文专节。

---

## 七个核心回调逐个

### 1. `declare` —— 我有哪些 socket

`[实测](../../../source/blender/nodes/intern/node_declaration.cc#L35-L44)`：签名 `void (*)(nodes::NodeDeclarationBuilder &builder)`（`NodeDeclareFunction`，[BKE_node.hh L125](../../../source/blender/blenkernel/BKE_node.hh#L125)）。两个调用时机：注册时建 `static_declaration`（传 `nullptr, nullptr`），以及任何实例刷新 socket 时（传真实 tree/node）。Repeat 的实现是 `node_declare`（Input L72–L111）。

**不写会怎样**：`node_add_sockets_from_type`（[node.cc L2562-L2584](../../../source/blender/blenkernel/intern/node.cc#L2562-L2584)）走 `else` 分支——没有 `declare` 就去读 `inputs`/`outputs` 模板表；两者都没有 = **一个 socket 都不生成**。现代节点（Repeat 在内）必须写。

### 2. `initfunc` —— 新实例的出生

`[实测](../../../source/blender/blenkernel/intern/node.cc#L2590-L2643)`：由内部 `node_init()` 调，先设 `flag`/`width`/`name`，再 `initfunc(ntree, node)`，再 `initfunc_api`，最后补 socket，然后打上 `NODE_INIT` 保证**只跑一次**。

Repeat Input 的实现（L113–L119）分配 storage 并**显式初始化关键字段**：

```cpp
static void node_init(bNodeTree * /*tree*/, bNode *node)
{
  NodeGeometryRepeatInput *data = MEM_new<NodeGeometryRepeatInput>(__func__);
  /* Needs to be initialized for the node to work. */
  data->output_node_id = 0;
  node->storage = data;
}
```

**不写会怎样**：`node->storage` 为 `nullptr`。而 `node_type_storage` 的声明注释警告得很直白（[BKE_node.hh L843-L847](../../../source/blender/blenkernel/BKE_node.hh#L843-L853)）："Nodes defining a storage type _must_ allocate this for new nodes. Otherwise nodes will reload as undefined (#46619)"——配套的守卫在 [node.cc L2664-L2669](../../../source/blender/blenkernel/intern/node.cc#L2664-L2669)：已带 `NODE_INIT` 的节点若有 `storagename` 却 `storage == nullptr`，直接**把 typeinfo 降级成 Undefined**。

### 3. `freefunc` —— 实例死亡

`[实测](../../../source/blender/blenkernel/intern/node.cc#L5099-L5101)`：`node_free_node` 里在释放 socket 之前调。Repeat Input 用的是通用的 `node_free_standard_storage`；Output 用自己的 `node_free_storage`（L226–L230）。注释（L324–L327）特别要求：**这里不要碰 `node->id`**，因为释放 `Main` 时它的状态未定义。

### 4. `copyfunc` —— 复制实例

`[实测](../../../source/blender/blenkernel/intern/node.cc#L4397-L4399)`：`node_copy_with_mapping` 中调用，签名带 `(dest_ntree, dest_node, src_node)`。注意它和 `freefunc` 一样是被 `node_type_storage` 统一填的——**这两者是配对出现的设计**。

### 5. `labelfunc` —— 头部显示什么

`[实测](../../../source/blender/blenkernel/intern/node.cc#L5732-L5745)`：`node_label()` 三级回退：`node->label`（用户改名）→ `typeinfo->labelfunc` → `IFACE_(typeinfo->ui_name)`。Repeat Input 的实现（L121–L127）不管 storage 内容一律写 `"Repeat"`，Output 直接**复用** Input 的函数：`ntype.labelfunc = repeat_input_node::node_label;`（L328）。这样区域两端头部都显示 "Repeat"。

**不写会怎样**：显示 `ui_name`，即 "Repeat Input"/"Repeat Output"。功能正常，只是不符合视觉设计。

### 6. `insert_link` —— 这根连线我同意吗

`[实测](../../../source/blender/blenkernel/intern/node.cc#L233-L239)`：入参 `NodeInsertLinkParams { ntree, node, link, C }`，返回 false 则**连线被拒绝**。调用点在 `rna_Node_links_new` 与 `node_relationships.cc` 三处。默认值由 `common_node_type_base` 填 `node_insert_link_default`（恒 true，[node_util.cc L223-L226](../../../source/blender/nodes/intern/node_util.cc#L223-L226)）。

Repeat Input 的实现（L129–L137）是它最巧的一段：把连到 `__extend__` 上的线**转成"新增一个 item"**：

```cpp
static bool node_insert_link(bke::NodeInsertLinkParams &params)
{
  bNode *output_node = params.ntree.node_by_id(node_storage(params.node).output_node_id);
  if (!output_node) {
    return true;                     /* 找不到 Output：放行，让系统正常建线 */
  }
  return socket_items::try_add_item_via_any_extend_socket<RepeatItemsAccessor>(
      params.ntree, params.node, *output_node, params.link);
}
```

注意它读 `output_node_id`——这就是 zone 配对字段在编辑期的第一个消费者。**Output 版本**（L241–L245）参数表里的 `node` 出现两次，因为 Output 自己就是 item 的宿主。

### 7. `gather_link_search_ops` —— 拖线菜单里的我

`[实测](../../../source/blender/editors/space_node/link_drag_search.cc#L285-L301)`：搜索时**遍历全部注册类型**（`node_types_get()`），逐个 poll 后调该回调收集候选项。默认值 `nodes::search_link_ops_for_basic_node`（[socket_search_link.cc L181-L189](../../../source/blender/nodes/intern/socket_search_link.cc#L181-L189)）——它直接用 `ntype.static_declaration` 里的 socket 列出生成条目。

Repeat Output 的实现（L252–L297）加了两个条目："Repeat ▸ Iterations" 与 "Repeat"，算子体里**手工建对**（`input_storage.output_node_id = output_node.identifier`）。

`[实测](../../../source/blender/nodes/geometry/nodes/node_geo_repeat.cc#L159)`：Repeat **Input** 显式 `ntype.gather_link_search_ops = nullptr;`——基类已设默认值，这里**手动抹掉**，因为 Input 单独出现在搜索菜单里没有意义（它必须和 Output 成对，由 Output 那条统一负责）。Simulation、For-Each 的 Input 也是同一写法（`node_geo_simulation.cc` L366、`node_geo_foreach_geometry_element.cc` L232）。

---

## zone 协议字段

`[实测](../../../source/blender/nodes/intern/node_register.cc#L74-L90)`：Repeat 的配对逻辑落在 `RepeatZoneType`，与 `bNodeType` 是两个对象：

```cpp
class RepeatZoneType : public bke::bNodeZoneType {
 public:
  RepeatZoneType()
  {
    this->input_idname = "GeometryNodeRepeatInput"_ustr;
    this->output_idname = "GeometryNodeRepeatOutput"_ustr;
    this->input_type = GEO_NODE_REPEAT_INPUT;
    this->output_type = GEO_NODE_REPEAT_OUTPUT;
    this->theme_id = TH_NODE_ZONE_REPEAT;
  }
  const int &get_corresponding_output_id(const bNode &input_bnode) const override
  {
    BLI_assert(input_bnode.type_legacy == this->input_type);
    return static_cast<NodeGeometryRepeatInput *>(input_bnode.storage)->output_node_id;
  }
};
```

**关键细节**：返回的是 `const int &`，即**指向 storage 内部字段的引用**，不是拷贝。这个签名（[BKE_node.hh L1319](../../../source/blender/blenkernel/BKE_node.hh#L1317-L1325)）强制每个实现"直接从节点的持久数据里读出 id"，零分配；且它**只在 Input 一侧**要求实现——Output 端不需要反向 id 字段，DNA 里 `NodeGeometryRepeatOutput`（[DNA_node_types.h L3561-L3575](../../../source/blender/makesdna/DNA_node_types.h#L3561-L3575)）没有任何指向 Input 的字段。配对是**单向数据 + 双向查询**。

Output→Input 怎么查？基类给通用实现（[node_tree_zones.cc L492-L502](../../../source/blender/blenkernel/intern/node_tree_zones.cc#L492-L508)）：

```cpp
const bNode *bNodeZoneType::get_corresponding_input(const bNodeTree &tree,
                                                    const bNode &output_bnode) const
{
  tree.ensure_topology_cache();
  for (const bNode *node : tree.nodes_by_type(this->input_idname)) {
    if (this->get_corresponding_output_id(*node) == output_bnode.identifier) {
      return node;
    }
  }
  return nullptr;
}
const bNode *bNodeZoneType::get_corresponding_output(const bNodeTree &tree,
                                                     const bNode &input_bnode) const
{
  return tree.node_by_id(this->get_corresponding_output_id(input_bnode));
}
```

`[总结]` 这就是"Output 扫全树找指向自己的 Input"的真身：**Output 端 O(所有 Input 数)，Input 端 O(1)**（`node_by_id` 走运行时 id 向量集，见 [`BKE_node_runtime.hh` L513-L536](../../../source/blender/blenkernel/BKE_node_runtime.hh#L513-L536)）。这也是为什么 `get_corresponding_input` 要先 `ensure_topology_cache()`，而 `get_corresponding_output` 不用。

**两个例外值得记**：`node_runtime.cc` 的 `get_implicit_origin_nodes`（[L296-L312](../../../source/blender/blenkernel/intern/node_runtime.cc#L296-L324)）在**正在建拓扑缓存**时被调用，所以它自己手写扫循环，注释明确写着 "Can't use `#zone_type.get_corresponding_input` because that expects the topology cache to be build already"；`node.cc` 的链路迭代器（[L4190-L4202](../../../source/blender/blenkernel/intern/node.cc#L4190-L4202)）把 zone 两端视为**隐式相连**，即使没有 `bNodeLink`。

区域构建本身也在扫这个协议：`find_zone_nodes`（[node_tree_zones.cc L34-L72](../../../source/blender/blenkernel/intern/node_tree_zones.cc#L34-L72)）先给每个 Output 建 zone，再按 Input 反查填 `input_node_id`，最后一步是**任何 zone 缺任一端就整棵树判定为无 zone**（L65-L70）。

登记时机在 `register_zone_types()`（[node_register.cc L147-L159](../../../source/blender/nodes/intern/node_register.cc#L147-L164)），`register_nodes()` 的**第一行**，早于任何节点类型注册。目前共 5 种：Simulation、Repeat、For Each Geometry Element、Closure、Light Iter Internal。

---

## node_type_storage 两种用法

`[实测](../../../source/blender/blenkernel/intern/node.cc#L6166-L6177)`：这是个便利函数，做三件事：

```cpp
void node_type_storage(bNodeType &ntype,
                       const std::optional<StringRefNull> storagename,
                       void (*freefunc)(bNode *node),
                       void (*copyfunc)(bNodeTree *dest_ntree,
                                        bNode *dest_node,
                                        const bNode *src_node))
{
  ntype.storagename = storagename.value_or("");
  ntype.copyfunc = copyfunc;
  ntype.freefunc = freefunc;
}
```

签名声明在 [BKE_node.hh L843-L853](../../../source/blender/blenkernel/BKE_node.hh#L843-L853)，注意 `storagename` 是 `std::optional`——注释说"some compositor nodes use non-DNA storage type"。它把"名字 + free + copy"绑成一个原子决定，**防止只写一半**。

### 用法 A：standard（纯 POD）

```cpp
/* node_util.cc L45-L62 */
void node_free_standard_storage(bNode *node)
{
  if (node->storage) {
    MEM_delete_void(node->storage);
  }
}
void node_copy_standard_storage(bNodeTree *, bNode *dest_node, const bNode *src_node)
{
  dest_node->storage = MEM_dupalloc_void(src_node->storage);
}
```

Repeat **Input** 用它（L164–L165），理由是 `NodeGeometryRepeatInput`（[L3554-L3559](../../../source/blender/makesdna/DNA_node_types.h#L3554-L3575)）只有一个 `int32_t output_node_id`——**裸内存复制就是正确的深拷贝**，落盘反射也只需要写这 4 字节。

### 用法 B：自定义（有堆指针）

Repeat **Output**（L337）：`bke::node_type_storage(ntype, "NodeGeometryRepeatOutput", node_free_storage, node_copy_storage);` 因为它的 storage 里有 `NodeRepeatItem *items`，每个 item 里还有 `char *name`（[L3543-L3552](../../../source/blender/makesdna/DNA_node_types.h#L3543-L3552)）——**memcpy 得到的是两个树共享同一块堆内存**，谁释放都出问题。

```cpp
/* L226-L239 */
static void node_free_storage(bNode *node)
{
  socket_items::destruct_array<RepeatItemsAccessor>(*node);
  MEM_delete(reinterpret_cast<NodeGeometryRepeatOutput *>(node->storage));
}
static void node_copy_storage(bNodeTree *, bNode *dst_node, const bNode *src_node)
{
  const NodeGeometryRepeatOutput &src_storage = node_storage(*src_node);
  auto *dst_storage = MEM_new<NodeGeometryRepeatOutput>(__func__, dna::shallow_copy(src_storage));
  dst_node->storage = dst_storage;
  socket_items::copy_array<RepeatItemsAccessor>(*src_node, *dst_node);
}
```

`[关键]` `dna::shallow_copy`（[DNA_defs.h L138-L150](../../../source/blender/makesdna/DNA_defs.h#L136-L155)）就是**故意的 memcpy**——注释原文 "The entire object is copied as-is using memory copy"。这里浅拷贝是**正确的**，因为紧随其后的 `socket_items::copy_array`（[NOD_socket_items.hh L119-L129](../../../source/blender/nodes/NOD_socket_items.hh#L119-L129)）会**重新分配 `items` 数组**并逐条走 `Accessor::copy_item`，而 `RepeatItemsAccessor::copy_item`（[NOD_geo_repeat.hh L43-L47](../../../source/blender/nodes/geometry/include/NOD_geo_repeat.hh#L37-L52)）里 `dst.name = BLI_strdup_null(dst.name)` 把字符串也复制了。顺序是"**先整体浅拷 → 立刻深拷所有指针字段**"。析构对称：`destruct_array` 对每条调 `destruct_item`（`MEM_SAFE_DELETE(item->name)`）再 `MEM_SAFE_DELETE(*ref.items)`。这与 05-DNA 章"浅拷贝是默认、深拷贝靠你补"的说法完全呼应。

### 用法 C：追加落盘内容

`storagename` 反射只能覆盖 POD 部分。堆指针内容靠 `blend_write_storage_content`/`blend_data_read_storage_content`（声明 L421–L422）：Output 注册了（L334–L335），实现是 `socket_items::blend_write/blend_read_data<RepeatItemsAccessor>`，逐条走 `Accessor::blend_write_item`（L350–L358 写 `item.name`）。调用点在 [node.cc L1322-L1329](../../../source/blender/blenkernel/intern/node.cc#L1322-L1330)（先结构体后内容，然后 **`return`** 跳过后面的 legacy 分支）与 L1996–L2010（同样 `return`）。Input 不需要这两个回调：`output_node_id` 是个 `int32_t`，反射已覆盖。

### `static_declaration`：注册时的一次 declare

`[实测](../../../source/blender/blenkernel/intern/node.cc#L2933-L2936)`：`node_register_type` 里，若设了 `declare`，`new nodes::NodeDeclaration()` 并以 `(nullptr, nullptr)` 跑一遍。Repeat 的 `node_declare` 里 `b.node_or_null()` 会把 `is_context_dependent = true`（[NOD_node_declaration.hh L675-L679](../../../source/blender/nodes/NOD_node_declaration.hh#L670-L680)），所以这份静态声明只包含不依赖 node 的部分（固定 socket + `__extend__`）。消费方是连线搜索 `search_link_ops_for_basic_node`（读 `static_declaration`）和 `node_declaration_ensure_on_outdated_node`（[node.cc L5558-L5576](../../../source/blender/blenkernel/intern/node.cc#L5558-L5576)）——只有**不**依赖上下文的声明才直接共享给实例。释放靠 `node_free_type` 里的 `delete nodetype->static_declaration`（L2911）。

---

## no_muting

`[实测](../../../source/blender/blenkernel/BKE_node.hh#L450-L451)`：一个普通 `bool`，注释 "True when the node cannot be muted."。Repeat 两个节点都设 true（L161、L331）。

三个消费点：

1. **编辑器算子**：`node_mute_exec`（[node_edit.cc L1643-L1648](../../../source/blender/editors/space_node/node_edit.cc#L1636-L1653)）——`if (node->is_selected() && !node->typeinfo->no_muting) { node->flag ^= NODE_MUTED; ... }`。M 键直接跳过。
2. **RNA 属性写入**：`rna_Node_mute_set`（[rna_nodetree.cc L2806-L2812](../../../source/blender/makesrna/intern/rna_nodetree.cc#L2806-L2812)）——同一个判断，所以 Python 里 `node.mute = True` 对 zone 节点**静默无效**。
3. **versioning 清理**：老文件里可能已经存了 `NODE_MUTED`（`1 << 9`，[DNA_node_types.h L217](../../../source/blender/makesdna/DNA_node_types.h#L205-L217)）。`versioning_500.cc` L4445–L4473 维护了一份**硬编码 idname 集合** `no_muting_nodes`（19 项，含 `GeometryNodeRepeatInput/Output`、Closure 两端、Simulation 两端、Group I/O、各 Output、Viewer），对 `!MAIN_VERSION_FILE_ATLEAST(bmain, 501, 4)` 的文件逐个 `node.flag &= ~NODE_MUTED`。

**为什么 zone 接口节点必须禁静音**：静音的语义是"数据从输入直穿到输出、节点逻辑跳过"。zone 的 Input/Output 不承载这个契约——它们定义**区域边界本身**。若允许静音，拓扑缓存构建（`find_zone_nodes` 要求两端都在）、结构类型推断、GPU 内联（`shader_nodes_inline.cc` 里 `RepeatZoneComputeContext` 分支）都要多处理一个"半失效区域"的状态机。

`[警告]` 第 3 点那个硬编码 Set 意味着**新增 `no_muting` 类型时必须手工同步 versioning_500.cc**——`bNodeType` 里没有任何机制替你登记。这是后文反例之一。

---

## 注册时机

`[实测](../../../source/blender/nodes/NOD_register.hh#L29-L47)`：宏本身只做两件事，函数体只有 3 行：

```cpp
#define NOD_REGISTER_NODE(REGISTER_FUNC) \
  void REGISTER_FUNC##_discover(); \
  void REGISTER_FUNC##_discover() \
  { \
    REGISTER_FUNC(); \
  }
```

它**不是**静态初始化器（不是全局对象构造函数那套魔法）。头注释列了三个用途：源码标记（给 `discover_nodes.py` 搜）、把 `static` 的注册函数包成非 static 的外部可见包装、让"这里发生了一件不寻常的事"在代码里显式。

真实链条是一条**构建期代码生成 + 启动期显式调用**：

```mermaid
flowchart LR
  A["源码里 NOD_REGISTER_NODE(node_register)"] --> B["discover_nodes.py 正则扫描"]
  B --> C["生成的 register_geometry_nodes.cc"]
  C --> D["register_geometry_nodes()"]
  D --> E["register_nodes()"]
  E --> F["node_system_init()"]
  F --> G["node_register_type 写入全局表"]
    class A input
    class B,D,E,F compute
    class C abstraction
    class G result
    classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
    classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
    classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
    classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
    classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
    classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```


1. [`discover_nodes.py`](../../../source/blender/nodes/intern/discover_nodes.py)（132 行）用一条正则同时匹配 `namespace X {`、`}  // namespace X` 和 `NOD_REGISTER_NODE(f)`，**按出现顺序维护命名空间栈**（L68-L107），生成 `blender::nodes::node_geo_repeat_cc::repeat_input_node::node_register_discover();` 这样的调用行。
2. [`nodes/CMakeLists.txt`](../../../source/blender/nodes/CMakeLists.txt) L9–L40 的 `add_node_discovery()` 把它接到 CMake；geometry 子目录在 L412–L417 生成 `register_geometry_nodes.cc` 编成 `bf_nodes_geometry_generated`。
3. [`node_register.cc`](../../../source/blender/nodes/intern/node_register.cc) L161–L184 的 `register_nodes()` 依次调：`register_zone_types()` → `register_undefined_types()` → `register_standard_node_socket_types()` → 树类型 → Frame/Reroute/Group I/O → 五个类别的节点。
4. [`node.cc` L6178-L6181](../../../source/blender/blenkernel/intern/node.cc#L6178-L6181) `node_system_init()` 只是 `register_nodes()` 的壳，由 [`creator.cc` L582](../../../source/blender/creator/creator.cc#L582) 在 `RNA_init()`、`RE_engines_init()` 之后调用；测试里手动调（`gtest_setup.cc` L71）。退出走 `node_system_exit()`（[node.cc L6183-L6213](../../../source/blender/blenkernel/intern/node.cc#L6183-L6213)），由 `blender.cc` L91 在 `Main` 释放流程里触发，逐个 `node_free_type`。

**注册表本体**：[`node.cc` L2779-L2783](../../../source/blender/blenkernel/intern/node.cc#L2773-L2795) 的 `get_node_type_map()`，函数内 `static CustomIDVectorSet<bNodeType *, NodeStructIDNameGetter<bNodeType>>`——按 `idname` 哈希又保插入序，因此 `node_types_get()`（L2951）返回 `Span` 可稳定遍历，`node_type_find(idname)`（L2883–L2890）O(1)。另有 alias 表（L2785，`node_register_alias` L2956）。

**注册时干了什么**（[node.cc L2920-L2943](../../../source/blender/blenkernel/intern/node.cc#L2920-L2943)）：断言 `idname` 非空且 `poll != nullptr` → 把 `ui_name`/`ui_description` 写进 RNA struct → `enum_name_legacy` 缺省用 `idname` → 建 `static_declaration` → `add_new` 入表 → `update_typeinfo(G_MAIN, nullptr, &nt, nullptr, false)` 遍历所有已存在的节点树，把 idname 匹配的节点 `typeinfo` 补上（L2711–L2746）。最后一步是"节点先于类型注册"（读文件早于注册完成、或 Python 动态类型）场景的补丁，`node_init` 的注释也提到这点（L2586–L2589）。

---

## 完整对照表：Repeat Input vs Output

`[实测](../../../source/blender/nodes/geometry/nodes/node_geo_repeat.cc#L149-L167)` 与 [L319–L339](../../../source/blender/nodes/geometry/nodes/node_geo_repeat.cc#L319-L340)。

| 字段 | Input（L149–167） | Output（L319–339） | 差异原因 |
| --- | --- | --- | --- |
| `common_node_type_base` | `GeometryNodeRepeatInput`, 2107 | `GeometryNodeRepeatOutput`, 2108 | 各自身份 |
| `ui_name` | `"Repeat Input"` | `"Repeat Output"` | 菜单名 |
| `enum_name_legacy` | `"REPEAT_INPUT"` | `"REPEAT_OUTPUT"` | Python 枚举 |
| `nclass` | `NODE_CLASS_INTERFACE` | 同 | **相同** |
| `initfunc` | `node_init`(L113) | `node_init`(L209) | Output 还建默认 Geometry item |
| `declare` | `node_declare`(L72) | `node_declare`(L176) | Input 靠 Output 的 items 生成 socket |
| `labelfunc` | `node_label`(L121) | `repeat_input_node::node_label` | Output 跨命名空间复用 |
| `insert_link` | `node_insert_link`(L129) | `node_insert_link`(L241) | Input 需先找 Output |
| `gather_link_search_ops` | **`nullptr`**(L159) | `node_gather_link_searches`(L252) | 只有 Output 提供一键建对 |
| `no_muting` | true(L161) | true(L331) | **相同** |
| `draw_buttons_ex` | `node_layout_ex`(L162) | `node_layout_ex`(L332) | **相同**，共享的 UI |
| `gpu_fn` | `node_shader_fn`(L139) | `node_shader_fn`(L309) | `REPEAT_BEGIN` vs `REPEAT_END` |
| `register_operators` | 未设 | `node_operators`(L333) | item 算子宿主是 Output |
| `blend_write_storage_content` | 未设 | `node_blend_write`(L334) | Output 有堆指针 |
| `blend_data_read_storage_content` | 未设 | `node_blend_read`(L335) | 同上 |
| `node_type_storage` 的 free/copy | standard / standard | 自定义 `node_free_storage` / `node_copy_storage` | POD vs 堆数组 |
| storagename | `"NodeGeometryRepeatInput"` | `"NodeGeometryRepeatOutput"` | DNA 结构名 |
| `ui_description` | 未设 | 未设 | 两者都没写 |
| `node_register_type` + `NOD_REGISTER_NODE` | L166/L168 | L338/L340 | **相同套路** |

`[观察]` 两者共用 `node_layout_ex`（L34–L66，定义在两个命名空间之外）不是巧合——那个函数从当前节点出发找 zone、取 `zone->output_node()`，然后一律画 Output 的 items 列表；因此 Input 面板上能看到并编辑 Output 的数据。注册结构对称 + UI 回调共享 + zone 单向 id，三件事合起来才让"一个区域两端"看起来像"一个节点"。

---

## 用小数据走一遍：从零写一个最小几何节点

`[练习]` 目标：`GeometryNodeMyDouble`，输入 Int，输出 "输入的两倍"。下面 6 行是**必写**的，其余都可省（示意代码，不保证能直接编译）：

```cpp
static void node_declare(NodeDeclarationBuilder &b)
{
  b.add_input<decl::Int>("Value");
  b.add_output<decl::Int>("Doubled").propagate_all();
}
static void node_register()
{
  static bke::bNodeType ntype;
  geo_node_type_base(&ntype, "GeometryNodeMyDouble", std::nullopt);
  ntype.ui_name = "My Double";
  ntype.declare = node_declare;
  ntype.geometry_node_execute = node_geometry_exec;   /* 真正算的东西 */
  bke::node_register_type(ntype);
}
NOD_REGISTER_NODE(node_register)
```

`geo_node_type_base`（[node_geometry_util.cc L136-L144](../../../source/blender/nodes/geometry/node_geometry_util.cc#L136-L144)）已经替你设好 `poll`（限 GeometryNodeTree）、`insert_link`（默认放行）、`gather_link_search_ops`（默认按 `static_declaration` 生成搜索项）。legacy type 传 `std::nullopt` 会走 `get_next_auto_legacy_type()`（[node.cc L5853-L5864](../../../source/blender/blenkernel/intern/node.cc#L5853-L5864)）——从 5000 起、**带随机起点**，注释解释这是防止代码依赖它的跨会话稳定性。

| 漏写 | 后果 | 严重度 |
| --- | --- | --- |
| `declare`（且无 `inputs/outputs` 模板） | 节点没有任何 socket，拖进去就是个空方块 | 致命 |
| `ui_name` | `register` 里传给 `RNA_def_struct_ui_text` 的是空串，菜单出现空条目 | 高 |
| `geometry_node_execute` | 能加、能连、能存，但求值时被跳过 | 高 |
| `node_type_storage` | 没事——纯 POD 才需要；只有当你开始往 `node->storage` 写东西才必须 | 视情况 |
| `initfunc` 分配了 storage 但没配 `node_type_storage` | 内存泄漏 + 读盘 `storagename` 空 → 走 untyped read | 高 |
| 两个 `node_register` 用同一个 idname | `add_new` 断言失败（`CustomIDVectorSet` 要求唯一） | 致命 |

`[验证]` 注册成功的最快自检：Python 里 `bpy.types.GeometryNodeMyDouble` 存在（`node_type_base` L5877-L5882 会 `RNA_struct_find(ntype.idname)` 并 `BLI_assert(srna != nullptr)`——**所以 idname 必须先有对应 RNA struct 定义**，这是内建节点走 `makesrna` 生成、不能随便自造名字的原因）。

---

## 反例与边界

`[反例 1]` **忘了 `node_type_storage` 但 `initfunc` 分配了 storage**。后果不只是泄漏：`node_set_typeinfo`（[node.cc L2664-L2669](../../../source/blender/blenkernel/intern/node.cc#L2664-L2669)）在 `storagename[0] == '\0'` 时不报错，文件**看起来存下来了**，但重开时 storage 走 `BLO_read_raw_address` 的非类型化路径（L2002–L2005），结构体字节序/对齐一变就静默损坏。修法：要么三者都交给 `node_type_storage`，要么根本不碰 storage。

`[反例 2]` **`no_muting` 忘了设，或设了但没同步 versioning**。硬编码 Set 在 `versioning_500.cc` L4447–L4466。新加一个 `no_muting = true` 的 zone 接口节点而没把 idname 加进那个 Set，老文件里已有的 `NODE_MUTED` 会残留，之后 `find_zone_nodes`、结构类型推断、GPU 内联全都按"被静音"处理，表现为**区域不工作但没有明显错误信息**。这条无法靠编译器发现。

`[反例 3]` **`freefunc` 和 `copyfunc` 不配对**。`node_type_storage` 强制你一起给，但给错内容没人管。Repeat Output 若把 copy 换成 `node_copy_standard_storage`（memcpy），`items` 数组被两个节点共享，删除其中一个后另一个读到已释放内存；反过来，若只补了 copy 没补 free，`items` 与每条 `name` 都泄漏。检查口诀：**storage 里每有一个 `*`，`free` 里就必须有一次对应的释放、`copy` 里必须有一次对应的重新分配**（`RepeatItemsAccessor` 的 `copy_item`/`destruct_item` 成对写在同一个头文件里 L43–L52，正是为了让这个检查局部化）。

`[反例 4]` **用 `type_legacy` 判类型，而节点是自动分配 legacy type 的**。`get_next_auto_legacy_type()` 的起点**每次启动都随机**（L5855–L5860）。任何形如 `if (node->type_legacy == 5013)` 的代码，或把自动生成的类型写进 DNA/版本逻辑，都是定时炸弹。判断类型的正道是 `node->is_type("GeometryNodeRepeatInput"_ustr)` / `ntype.is_type(idname)`（[BKE_node.hh L467-L474](../../../source/blender/blenkernel/BKE_node.hh#L467-L475)，注意它会 `BLI_assert(node_type_find(...))` 提前抓拼写错误）。反过来说，Repeat 这类**有官方 legacy 宏**（2107/2108）的旧节点，zone 协议才敢用 `input_type/output_type` 存整数——`zone_type_by_node_type()`（[node_tree_zones.cc L575-L583](../../../source/blender/blenkernel/intern/node_tree_zones.cc#L575-L583)）是线性扫，只能靠整数不能靠字符串比较。

`[反例 5]` **在 `node_register()` 里做重活**。它在启动路径（`creator.cc` L582）上，注册几千个类型时任何 IO / 大容器构建都直接进启动时间。而且此时 `G_MAIN` 可能刚建或即将销毁：`node_register_type` 末尾的 `update_typeinfo(G_MAIN, ...)` 已经要遍历所有节点树（[L2711-L2746](../../../source/blender/blenkernel/intern/node.cc#L2711-L2746)，且 `if (!bmain) return;`）。`register` 里应当只有字段赋值。`register_operators`（L448）之所以存在，就是把算子注册**推迟**到 `node_ops.cc` L127 被显式调用的时机。

`[反例 6]` **给 `declare(nullptr)` 传上下文依赖的代码**。注册时用 `(nullptr, nullptr)` 跑一遍 `declare`。Repeat 的实现是**正确范本**（L80–L104）：先 `b.node_or_null()` / `b.tree_or_null()`，两个都非空才读 storage 建动态 socket，否则只跳过。若在这里无条件 `node_storage(*node)`，注册阶段直接空指针解引用——而且崩在启动最早的阶段，栈几乎没有信息。

`[反例 7]` **`gather_link_search_ops` 忘了 `poll`/`add_ui_poll` 过滤**。搜索遍历全部类型（`link_drag_search.cc` L285–L292），只自动帮你查 `poll` 和 `add_ui_poll`；但你在回调里 `params.add_item_full_name(...)` 加的操作 lambda 里若假定了某种树/上下文，运行时会炸。Repeat 的做法是在回调**开头**判 `RepeatItemsAccessor::supports_socket_type(other_socket.type, params.node_tree().type)` 直接 return（L254–L257）。

`[边界 8]` **`is_type()` 的 assert**。它会断言传入 idname 已注册（[BKE_node.hh L469-L472](../../../source/blender/blenkernel/BKE_node.hh#L467-L475)）。versioning 里比对一个**已删除节点**的 idname 时必须直接写 `this->idname == query`，不能用 `is_type()`。

`[边界 9]` **重复注册**。测试里 `node_system_init()` 可能被多次调用；`node_free_type` 注释（L2909–L2912）明确说 `static_declaration` 置空是为了"跑测试时可能反复注册/反注册"。函数内 `static bNodeType ntype` 只初始化一次，所以二次注册时字段值还在，但 `add_new` 会因 idname 重复断言——正确退出必须走 `node_system_exit()`。

`[边界 10]` **`freefunc` 里不要碰 `node->id`**（声明处注释 L323–L327："called while freeing `Main`, the state of this ID is undefined"）。同理 `initfunc` 里给 `node->id` 赋值**不要** `id_us_plus`——调用方负责（L316–L318，实际在 L2638–L2640）。

---

## 对理解 Repeat 的帮助

- **正篇 [02-01 注册全解](../../重复区域-dsh/02-Repeat区域数据模型/01-Repeat节点注册与UI.md)**：那篇按 L149–L167 / L319–L339 逐行列了赋值。本篇补齐"每一行背后的字段语义"：`gather_link_search_ops = nullptr` 为什么必须显式写（默认值已被 `common_node_type_base` 设过）、`labelfunc` 为什么跨命名空间复用 Output 侧、`node_type_storage` 为什么两边用不同 free/copy、`register_operators` 为什么只在 Output。有了五组字段的心智模型，那 40 行注册代码就从"清单"变成"证明"。
- **正篇 [01-01 zone 配对](../../重复区域-dsh/01-Zone系统基础/01-NodeTreeZone区域表示与配对.md)**：本篇的 zone 协议专节正是它的前置——`get_corresponding_output_id` 返回**引用**意味着"id 住在 Input 的 storage 里"，配对是单向存储；`get_corresponding_input` 是基类的 O(n) 全扫，所以 `find_zone_nodes` 必须先建拓扑缓存，而静音会破坏这个契约，故 `no_muting`。`node_runtime.cc` 那个"手写扫循环绕开 `get_corresponding_input`"的例子（L296–L312）也解释了正篇里为什么有时看到重复的扫描代码。
- **正篇 02-02 DNA 存储**：`dna::shallow_copy` + `copy_array` 的两步式，与本篇"用法 B"是同一件事的两个视角。
- **05-DNA 章 / 06-版本迁移章**：`storagename` 反射 + `blend_write_storage_content` 追加、`no_muting` 与 versioning 硬编码 Set 的联动，都在本篇落好了坐标。

---

## 继续阅读

- [下一篇：05-拓扑缓存与更新传播](05-拓扑缓存与更新传播.md) —— 注册完成后，`node_by_id`、`nodes_by_type`、`ensure_topology_cache` 这套运行时索引怎么支撑本篇里所有的查找。
- [上一章：03-NodeDeclarationBuilder](03-NodeDeclarationBuilder.md) —— `declare` 字段指向的那个构建器。
- [02-bNodeSocket 与声明系统](02-bNodeSocket与声明系统.md) —— `static_declaration` 与实例 declaration 的共享规则。
- [本章导航](README.md) · [前置知识总入口](../README.md)

<details>
<summary>本篇涉及的实测行数速查（均可用 ReadAllLines(path).Count 复核）</summary>

| 文件 | 实测行数 | 本篇用到的位置 |
| --- | --- | --- |
| [`blenkernel/BKE_node.hh`](../../../source/blender/blenkernel/BKE_node.hh) | 1363 | `bNodeType` L265–L475；`NodeInsertLinkParams` L233–L239；`node_type_storage` 声明 L848–L853；`bNodeZoneType` L1309–L1332；`NODE_STORAGE_FUNCS` L1353–L1361 |
| [`nodes/geometry/nodes/node_geo_repeat.cc`](../../../source/blender/nodes/geometry/nodes/node_geo_repeat.cc) | 372 | Input 注册 L149–L167；Output 注册 L319–L339；`node_layout_ex` L34–L66 |
| [`blenkernel/intern/node.cc`](../../../source/blender/blenkernel/intern/node.cc) | 6308 | 注册表 L2779；`node_register_type` L2920–L2943；`node_init` L2590–L2643；`node_type_base` L5866–L5894；`node_type_storage` L6166–L6177；`node_system_init` L6178 |
| [`blenkernel/intern/node_tree_zones.cc`](../../../source/blender/blenkernel/intern/node_tree_zones.cc) | 653 | `find_zone_nodes` L34–L72；`bNodeZoneType` 实现 L492–L583 |
| [`nodes/intern/node_register.cc`](../../../source/blender/nodes/intern/node_register.cc) | 186 | `RepeatZoneType` L74–L90；`register_nodes` L161–L184 |
| [`nodes/NOD_register.hh`](../../../source/blender/nodes/NOD_register.hh) | 49 | 宏 L42–L47，说明注释 L29–L41 |
| [`nodes/intern/discover_nodes.py`](../../../source/blender/nodes/intern/discover_nodes.py) | 132 | 正则与命名空间栈 L68–L107 |
| [`nodes/intern/node_util.cc`](../../../source/blender/nodes/intern/node_util.cc) | 321 | standard free/copy L45–L62；`node_insert_link_default` L223 |
| [`nodes/shader/node_shader_util.cc`](../../../source/blender/nodes/shader/node_shader_util.cc) | 629 | `common_node_type_base` L88–L95 |
| [`nodes/geometry/node_geometry_util.cc`](../../../source/blender/nodes/geometry/node_geometry_util.cc) | 167 | `geo_node_type_base` L136–L144 |
| [`nodes/NOD_socket_items.hh`](../../../source/blender/nodes/NOD_socket_items.hh) | 419 | `destruct_array` L92；`copy_array` L119 |
| [`nodes/geometry/include/NOD_geo_repeat.hh`](../../../source/blender/nodes/geometry/include/NOD_geo_repeat.hh) | 89 | `RepeatItemsAccessor` L17–L60 |
| [`makesdna/DNA_node_types.h`](../../../source/blender/makesdna/DNA_node_types.h) | 4047 | `eNode_Flag` L205；`NodeRepeatItem` L3543；Input L3554；Output L3561 |
| [`makesdna/DNA_defs.h`](../../../source/blender/makesdna/DNA_defs.h) | 170 | `dna::shallow_copy` L146–L150 |
| [`blenkernel/BKE_node_legacy_types.hh`](../../../source/blender/blenkernel/BKE_node_legacy_types.hh) | 583 | `GEO_NODE_REPEAT_INPUT/OUTPUT` L479–L480 |
| [`blenkernel/BKE_node_tree_zones.hh`](../../../source/blender/blenkernel/BKE_node_tree_zones.hh) | 122 | `bNodeTreeZone` L23–L55 |
| [`blenloader/intern/versioning_500.cc`](../../../source/blender/blenloader/intern/versioning_500.cc) | 4523 | `no_muting_nodes` 清理 L4445–L4473 |
| [`nodes/intern/socket_search_link.cc`](../../../source/blender/nodes/intern/socket_search_link.cc) | 210 | `search_link_ops_for_basic_node` L181–L189 |
| [`blenkernel/intern/node_runtime.cc`](../../../source/blender/blenkernel/intern/node_runtime.cc) | 741 | `get_implicit_origin_nodes` L296–L312 |

</details>
