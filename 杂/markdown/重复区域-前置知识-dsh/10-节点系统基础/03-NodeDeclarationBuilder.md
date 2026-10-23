# 03 · NodeDeclarationBuilder

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](02-bNodeSocket与声明系统.md) · [下一篇](04-bNodeType注册.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `NodeDeclarationBuilder`——节点声明 socket 的构建器接口。Repeat 的 `node_declare` 就靠它动态生成 socket。主要源码：[`NOD_node_declaration.hh`](../../../source/blender/nodes/NOD_node_declaration.hh)（实测 665 行）。

## 先回答一个具体问题

`node_declare` 的参数是 `NodeDeclarationBuilder &b`。这个 `b` 到底是什么？为什么能"动态"生成 socket？

`[讲解]` 一句话：**`b` 是一个"声明收集器"**。你往里加声明，它收集起来，最后由节点系统拿去和旧 socket 比对。

它不是"创建 socket 的对象"——socket 的创建在别处。

## 构建器的角色

`[讲解]` 看三者关系：

```text
node_declare(NodeDeclarationBuilder &b)
  ├── b.add_input(...)   → 往 b 里加一条声明
  └── b.add_output(...)  → 往 b 里加一条声明
         ↓
      NodeDeclaration（声明集合）
         ↓
      refresh_node_socket 拿它与旧 socket 比对
         ↓
      实际 bNodeSocket 列表
```

`[讲解]` 关键：**构建器只产"意图"，不碰"实例"**。

这解释了为什么 `node_declare` 可以反复调用而不破坏状态——它每次都在重新表达意图。

## 主要接口

`[讲解]` 从源码（`NOD_node_declaration.hh` L558-L571）提炼：

| 接口 | 用途 |
| --- | --- |
| `add_input<T>(name, identifier)` | 加一个类型已知的输入 |
| `add_output<T>(name, identifier)` | 加一个类型已知的输出 |
| `add_input(socket_type, name, identifier)` | 加一个运行时决定类型的输入 |
| `add_output(socket_type, name, identifier)` | 同上输出 |

`[讲解]` 两套接口的区别：

| | 模板版 | 非模板版 |
| --- | --- | --- |
| 类型 | 编译期（`decl::Float`） | 运行时（`eNodeSocketDatatype`） |
| 适用 | 固定 socket 的节点 | 动态 socket 的节点 |
| 例子 | Value 节点的 Value 输出 | **Repeat 的 item socket** |

`[讲解]` **Repeat 必须用非模板版**——因为 item 的类型是运行时数据（存在 `NodeRepeatItem::socket_type` 里）。

## 两个顺序开关

`[讲解]` 这是 Repeat 必用的功能。源码（L626）：

```cpp
bool use_custom_socket_order = false;
```

`[讲解]` 默认 `false` 意味着：**socket 顺序由"输入在前输出在后"的固定规则决定**。

打开后：

- 可以任意排列输入输出的顺序；
- 用 `align_with_previous()` 把某个输出与上一个输入对齐显示。

`[讲解]` Repeat 的实际用法（正篇 02-01）：

```cpp
static void node_declare(NodeDeclarationBuilder &b)
{
  b.use_custom_socket_order();
  b.allow_any_socket_order();

  b.add_output<decl::Int>("Iteration").description(...);
  b.add_input<decl::Int>("Iterations").min(0).default_value(1);

  /* 每个 item 生成一对 input+output，且输出紧跟输入 */
  for (const int i : IndexRange(output_storage.items_num)) {
    auto &input_decl = b.add_input(socket_type, name, identifier)...;
    b.add_output(socket_type, name, identifier)
        .align_with_previous()
        .propagate_all({input_decl.index()});
  }
}
```

`[讲解]` 三个关键点：

1. **`use_custom_socket_order()`** —— 允许 Iteration 输出出现在 Iterations 输入之前；
2. **`align_with_previous()`** —— 让每个 item 的 output 视觉上紧邻它的 input（形成"一对"）；
3. **`propagate_all({input_decl.index()})`** —— 声明输出与输入的引用传播关系。

`[讲解]` 如果没有 `use_custom_socket_order`，Blender 会强制把 Iteration 输出排到所有输入之后——UI 就乱了。

## builder 返回的 Builder 对象

`[讲解]` `b.add_input<T>(...)` 返回的不是声明本身，而是**该声明的 Builder**：

```cpp
typename DeclType::Builder &add_input(UString name, UString identifier);
```

`[讲解]` 为什么多一层？因为要用**链式调用**配置属性：

```cpp
b.add_input<decl::Int>("Iterations")
    .min(0)
    .default_value(1)
    .description("Number of iterations");
```

每个方法返回 `Builder&`，所以可以一路点下去。

`[讲解]` 常用配置项：

| 方法 | 作用 |
| --- | --- |
| `.description(str)` | 悬停提示 |
| `.min(v)` / `.max(v)` | 数值范围 |
| `.default_value(v)` | 默认值 |
| `.socket_name_ptr(...)` | 名字绑定到 RNA 属性 |
| `.structure_type(...)` | 结构类型（Single/Field/Dynamic） |
| `.inferred_structure_type(...)` | 从哪些输入推断结构类型 |
| `.propagate_all(...)` | 引用传播关系 |
| `.align_with_previous()` | UI 对齐 |
| `.hide_value()` | 隐藏值输入框 |

## 静态声明 vs 动态声明

`[讲解]` 两类节点的对比：

### 静态声明（大多数节点）

```cpp
static void node_declare(NodeDeclarationBuilder &b)
{
  b.add_input<decl::Geometry>("Geometry");
  b.add_input<decl::Float>("Radius").default_value(1.0f);
  b.add_output<decl::Geometry>("Geometry");
}
```

`[讲解]` 完全固定。每次调用产生相同的声明列表。

### 动态声明（Repeat）

```cpp
static void node_declare(NodeDeclarationBuilder &b)
{
  b.add_output<decl::Int>("Iteration");
  b.add_input<decl::Int>("Iterations");

  const bNode *node = b.node_or_null();
  const bNodeTree *tree = b.tree_or_null();
  if (node && tree) {
    const NodeGeometryRepeatInput &storage = node_storage(*node);
    if (const bNode *output_node = tree->node_by_id(storage.output_node_id)) {
      const auto &output_storage = *static_cast<const NodeGeometryRepeatOutput *>(
          output_node->storage);
      for (const int i : IndexRange(output_storage.items_num)) {
        /* 按 item 动态生成 socket 对 */
      }
    }
  }
}
```

`[讲解]` 四个要点：

1. **`b.node_or_null()` / `b.tree_or_null()`** —— 声明期可能没有节点上下文（比如预览），所以要判空；
2. **通过 `storage.output_node_id` 找配对节点** —— 这是 01 篇讲的配对机制；
3. **从 Output 的 items 读数据** —— 因为 item 只存 Output；
4. **循环生成** —— 每个 item 一对 socket。

`[讲解]` **注意 Input 节点自己不带 item 数据**。它只是"投影"Output 的 items。这是正篇讲的"单一数据源"设计。

## 一个隐蔽的坑：声明期的 node 可能为 null

`[讲解]` 看 `b.node_or_null()` 的命名——带 `_or_null` 后缀说明**可能返回空**。

什么情况会空？注释没有明说，但典型场景：

- 节点类型注册时做"预览声明"（不知道具体节点）；
- 某些 UI 预览路径。

`[讲解]` 如果直接 `b.node()`（不带 null 检查）会崩溃。所以 Repeat 的 `node_declare` 整个动态部分包在 `if (node && tree)` 里。

## 声明期不能做的事

`[讲解]` 这是实践中的重要约束。`node_declare` 会被**频繁重跑**（每次节点更新），所以：

| 不要做 | 原因 |
| --- | --- |
| 耗时计算 | 热路径 |
| 修改节点数据 | 声明应该是纯函数 |
| 分配内存 | 每次重跑都泄漏 |
| 依赖全局状态 | 结果应该可重现 |

`[讲解]` **Repeat 的做法是正确示范**：它只读 `output_storage.items`，不写、不分配。

## 用小数据走一遍

`[讲解]` Repeat Input 节点 `node_declare` 的执行过程，2 个 item（Geometry、Float）。

**上下文**：

```text
node = Repeat Input, identifier = 43
storage.output_node_id = 42
tree.node_by_id(42) → Repeat Output
  output_storage.items = [
    { name: "Geometry", socket_type: SOCK_GEOMETRY, identifier: 0 },
    { name: "Radius",   socket_type: SOCK_FLOAT,    identifier: 1 },
  ]
  output_storage.items_num = 2
```

**声明生成**：

| 步 | 调用 | 结果 |
| --- | --- | --- |
| 1 | `b.use_custom_socket_order()` | 允许任意顺序 |
| 2 | `b.allow_any_socket_order()` | 同上 |
| 3 | `b.add_output<decl::Int>("Iteration")` | 输出 socket 声明 |
| 4 | `b.add_input<decl::Int>("Iterations").min(0).default_value(1)` | 输入声明 |
| 5 | 循环 i=0：`b.add_input(SOCK_GEOMETRY, "Geometry", "Item_0")` | 输入声明 |
| 6 | 循环 i=0：`b.add_output(SOCK_GEOMETRY, "Geometry", "Item_0").align_with_previous()` | 输出声明 |
| 7 | 循环 i=1：`b.add_input(SOCK_FLOAT, "Radius", "Item_1")` | 输入声明 |
| 8 | 循环 i=1：`b.add_output(SOCK_FLOAT, "Radius", "Item_1").align_with_previous()` | 输出声明 |
| 9 | `b.add_input("", "__extend__")` | 扩展 socket |

**最终声明列表**（8 个声明）：

```text
[输出] Iteration         id="Iteration"
[输入] Iterations        id="Iterations"      min=0, default=1
[输入] Geometry          id="Item_0"
[输出] Geometry          id="Item_0"          align_with_previous
[输入] Radius            id="Item_1"
[输出] Radius            id="Item_1"          align_with_previous
[输入] (extend)          id="__extend__"
[输出] (extend)          id="__extend__"
```

**与旧 socket 比对**：

| 声明 id | 旧 socket | 动作 |
| --- | --- | --- |
| `Iteration` | 存在 | 复用 |
| `Iterations` | 存在 | 复用 |
| `Item_0` | 存在 | 复用 |
| `Item_1` | 存在 | 复用 |
| `__extend__` | 存在 | 复用 |

`[讲解]` 全部复用——**连线一条没断**。这就是 02 篇讲的机制在这里的具体体现。

## 反例与边界

### 反例 1：在 `node_declare` 里改 storage

```cpp
/* 错误 */
static void node_declare(NodeDeclarationBuilder &b)
{
  NodeGeometryRepeatOutput &storage = ...;
  storage.items_num++;   /* 每次重跑都 +1 → 无限增长 */
}
```

### 反例 2：不判 `node_or_null()`

```cpp
/* 危险 */
const NodeGeometryRepeatInput &storage = node_storage(*b.node());
```

预览场景会崩。

### 反例 3：以为 `add_input` 会创建 socket

它只加声明。实际 socket 由 `refresh_node_socket` 创建。

### 反例 4：忘了 `use_custom_socket_order`

Iteration 输出会被强制排到末尾，UI 错乱。

### 反例 5：`align_with_previous` 没有对应的前者

它要求前面有一个 socket 可对齐。如果第一个声明就用它，行为未定义或无效。

### 反例 6：动态生成时用了不稳定的 identifier

如果 identifier 用数组下标（`"Item_" + i`），删除中间 item 后匹配错位。

## 对理解 Repeat 的帮助

`[讲解]` 本篇把正篇 02-01 的 `node_declare` 彻底讲透：

| 正篇代码 | 本篇概念 |
| --- | --- |
| `b.use_custom_socket_order()` | 允许 Iteration 输出在前 |
| `b.add_output<decl::Int>("Iteration")` | 固定声明 |
| `b.add_input<decl::Int>("Iterations").min(0).default_value(1)` | Builder 链式配置 |
| `b.add_input(socket_type, name, identifier)` | 运行时类型版 |
| `.align_with_previous()` | UI 对齐 |
| `.propagate_all({input_decl.index()})` | 引用传播 |
| `b.add_input("", "__extend__").custom_draw(...)` | 扩展 socket |
| `b.node_or_null()` | 声明期判空 |

`[讲解]` **最关键的一条**：`node_declare` 是**纯函数式的意图表达**。它不创建、不修改、不分配——只是"描述我想要什么样的 socket"。这种设计让"重建"变得安全：随时可以重来一遍。

## 继续阅读

- [02-bNodeSocket与声明系统](02-bNodeSocket与声明系统.md) —— 声明与实例的匹配
- [04-bNodeType注册](04-bNodeType注册.md) —— `node_declare` 在哪注册
- [05-拓扑缓存与更新传播](05-拓扑缓存与更新传播.md) —— 什么时候触发重跑
