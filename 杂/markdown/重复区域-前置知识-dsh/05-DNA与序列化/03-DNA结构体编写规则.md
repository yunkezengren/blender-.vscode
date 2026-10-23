# 03 · DNA 结构体编写规则

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](02-SDNA表与类型编码.md) · [下一篇](04-DNA_DEFINE_CXX_METHODS与浅拷贝.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲怎么写出一个合法的 DNA 结构体——规则不多，但违反任何一条都会导致文件读写崩溃或跨版本不兼容。主要源码：[`DNA_documentation.h`](../../../source/blender/makesdna/DNA_documentation.h)、[`DNA_defs.h`](../../../source/blender/makesdna/DNA_defs.h)（146 行）、[`DNA_node_types.h`](../../../source/blender/makesdna/DNA_node_types.h)（4047 行，实例来源）。

## 先回答一个具体问题

我要给某个节点加一个字段（比如给 Repeat Output 加一个 `inspection_index`）。写进 DNA 头文件就行了吗？

不行。DNA 结构体有一套硬规则，**违反任何一条的后果不是编译错误，而是运行时崩溃或静默的数据损坏**。本篇把这些规则列全。

## 规则一：只能写 C 语言能表达的东西

`[讲解]` DNA 头文件被 `makesdna` 程序扫描，而它**不是 C++ 编译器**。所以：

| 禁止 | 原因 |
| --- | --- |
| `class` / `private` / `public` | 不是 C 语法 |
| 虚函数 | 有 vtable 指针，不可序列化 |
| 模板 | makesdna 无法实例化 |
| 引用成员 `T&` | 不是对象，无地址 |
| 构造函数/析构函数 | 不是数据（除非包在 `#ifdef __cplusplus` 里） |
| 命名空间 | 不是 C |

`[讲解]` 允许的"类 C++"扩展只有一个：

```c
struct NodeGeometryRepeatOutput {
  NodeRepeatItem *items = nullptr;   // 默认成员初始化器
  int items_num = 0;
  int active_index = 0;
  int next_identifier = 0;
  int inspection_index = 0;

#ifdef __cplusplus
  Span<NodeRepeatItem> items_span() const;
  MutableSpan<NodeRepeatItem> items_span();
#endif
};
```

`[讲解]` 三种 C++ 扩展的合法形式：

1. **默认成员初始化器**（`= nullptr`）——makesdna 会忽略它，编译器用它；
2. **`#ifdef __cplusplus` 包住的方法声明**——C 侧看不到，C++ 侧能调；
3. **`DNA_DEFINE_CXX_METHODS(...)` 宏**（下一节讲）。

**关键**：第 1 条不只是方便，而是**必需**——读取旧文件时新增字段没有对应字节，必须靠默认初始化器给出初值（见 02 篇）。

## 规则二：指针只能指向其他 DNA 结构或 void

`[讲解]` 指针在文件里存的是"地址编号"，读取时重定位。所以指向的目标必须也是 DNA 结构（有 SDNA 定义）。

合法的指针：

```c
NodeRepeatItem *items;        // 指向 DNA 数组
struct bNodeTree *nodetree;   // 指向 DNA 结构
void *runtime_data;           // 运行时数据，不参与序列化
```

`[讲解]` 三种情况的处理不同：

| 指针类型 | 写入 | 读取 |
| --- | --- | --- |
| 指向 DNA 结构 | 写目标结构的 SDNA 定义 + 数据 | 分配 + 重定位 |
| `void *` | **只写 nullptr**（运行时数据不存） | 置 nullptr |
| 函数指针 | 特殊处理（历史遗留） | 特殊处理 |

`[讲解]` 第三行是 `DNA_documentation.h` 里提到的 "Known issues"：

> "Because of historical reasons, some function pointers were untyped. The parser/DNA generator has been modified to explicitly handle these special cases."

意思是：有些老结构体里有函数指针（比如 `SpaceFile::returnfunc`），makesdna 必须特殊处理。**新代码不要加函数指针**。

## 规则三：`_pad` 必须手工填充

`[讲解]` 这是最容易被忽视的规则。看 `NodeRepeatItem`：

```c
struct NodeRepeatItem {
  char *name = nullptr;
  eNodeSocketDatatype socket_type = {};
  char _pad[2] = {};
  int identifier = 0;
};
```

`[讲解]` 为什么需要 `_pad[2]`？

字段大小：`char*`（8）+ `eNodeSocketDatatype`（枚举，4）+ `int`（4）= 16 字节。看起来没问题？

问题在**枚举类型的大小不是标准的**。C 标准允许编译器选择 `enum` 的底层类型。如果某个编译器选了 8 字节，结构体就变成 20 字节——**跨编译器不一致**。

`[讲解]` 更根本的原因：**DNA 结构体必须让 makesdna 看到的布局与编译器实际布局一致**。

makesdna 是个独立程序，它用自己的方式解析 C 声明。如果编译器插入了隐式 padding（为了对齐），makesdna 可能算错偏移。手工写 `_pad` 让布局显式化。

`[讲解]` 对比 `NodeForeachGeometryElementInputItem`（同文件，几乎一样的结构）：

```c
struct NodeForeachGeometryElementInputItem {
  char *name = nullptr;
  eNodeSocketDatatype socket_type = {};
  char _pad[2] = {};
  int identifier = 0;
};
```

一模一样的 `_pad[2]`。这说明它不是随手写的，而是"这个布局模板"的固定成分。

`[讲解]` **实用判据**：DNA 结构体的 `sizeof` 必须是 4 或 8 的倍数。如果不是，就缺 padding。可以在编译期用 `static_assert` 验证。

## 规则四：不能有隐式 padding

`[讲解]` 上一条的推论。C 编译器会为对齐插入 padding，而 padding 的字节值是**未定义的**——这会破坏两件事：

1. **序列化**：未定义字节被写进文件，读回来可能不同；
2. **哈希/比较**：memcmp 两个逻辑相等的结构体可能不等。

`[讲解]` 所以 DNA 结构体的字段顺序要**精心排列**，让每个字段自然对齐、无间隙。这也是为什么字段顺序不能随便改——不是"重排会破坏兼容"，而是"重排后 padding 位置变了，makesdna 的偏移计算会错"。

## 规则五：动态数组必须靠回调处理

`[讲解]` SDNA 只能读"定长部分"。像 `items` 这种"指针 + 数量"的动态数组，SDNA 不知道有多少元素。

看 `NodeGeometryRepeatOutput`：

```c
struct NodeGeometryRepeatOutput {
  NodeRepeatItem *items = nullptr;
  int items_num = 0;
  ...
};
```

`[讲解]` 读写时必须提供两个回调：

```cpp
static void node_blend_write(const bNodeTree &tree, const bNode &node, BlendWriter &writer)
{
  socket_items::blend_write<RepeatItemsAccessor>(&writer, node);
}

static void node_blend_read(bNodeTree &tree, bNode &node, BlendDataReader &reader)
{
  socket_items::blend_read_data<RepeatItemsAccessor>(&reader, node);
}
```

`[讲解]` 回调做两件事：

1. 写 `items_num`（数量）；
2. 逐个写 `items[0..n-1]`。

**SDNA 完全不知道这些**——它只处理 `items` 指针字段本身（存为一个待重定位的地址）和 `items_num` 整数。

`[讲解]` 所以规则是：**任何"数量由另一个字段决定"的数组，都必须有自定义 blend 回调**。

## 规则六：结构体必须可 trivial 拷贝

`[讲解]` DNA 结构体在内存里会被 `memcpy`（因为 `dna::shallow_copy` 就是这么实现的）。所以：

| 要求 | 原因 |
| --- | --- |
| 无虚函数 | vtable 指针不能 memcpy |
| 无自引用 | 拷贝后指针仍指向原对象 |
| 无 RAII 成员 | 拷贝会双重释放 |

`[讲解]` 反过来：**如果结构体里含堆指针，memcpy 只拷贝指针值，不拷贝内容**——这就是 `dna::shallow_copy` 的语义（下一节详讲），也是为什么 Repeat 的 `node_copy_storage` 必须"先浅后深"：

```cpp
static void node_copy_storage(bNodeTree &dst_tree, bNode *dst_node, const bNode *src_node)
{
  const NodeGeometryRepeatOutput &src_storage = node_storage(*src_node);
  auto *dst_storage = MEM_new<NodeGeometryRepeatOutput>(__func__, dna::shallow_copy(src_storage));
  dst_node->storage = dst_storage;

  /* 上面只浅拷贝了 items 指针（现在指向源节点的数组） */
  /* 这一步做深拷贝 */
  socket_items::copy_array<RepeatItemsAccessor>(*src_node, *dst_node);
}
```

`[讲解]` 注释很关键：`dna::shallow_copy` 之后，`dst_storage->items` 仍指向**源节点的数组**。如果就此结束，两个节点共享同一块内存——删一个会导致另一个悬空。

所以 `copy_array` 必须逐项深拷贝（对 `char *name` 做 `BLI_strdup_null`）。

## 规则七：枚举值只能末尾追加

`[讲解]` 枚举在文件里存的是**整数值**。所以：

| 操作 | 后果 |
| --- | --- |
| 末尾追加 | ✅ 安全（老文件不会有新值） |
| 中间插入 | ❌ 后面所有值都要重编号，老文件读错 |
| 重排 | ❌ 同上 |
| 删除 | ❌ 老文件里的值变成非法 |

`[讲解]` Repeat 的实际例子：`GEO_NODE_REPEAT_INPUT` 与 `GEO_NODE_REPEAT_OUTPUT` 是 DNA 层的稳定标识（正篇 00-03 L822 提过）。它们在 `eNodeType` 枚举里的位置**不可重排**。

## 规则八：`#` `#` 忽略不需要序列化的结构

`[讲解]` `DNA_documentation.h` L28-L44 讲了语法：

```c
#
#
struct MyStruct {
    int value;
};
```

`[讲解]` 两个 `#` 让 makesdna **跳过**这个结构体。用途有三个：

1. **只读辅助结构**（不需要存盘）；
2. **编码/解码中间结构**（比如 `SDNA_Struct` 自身）；
3. **C++ 运行时的辅助类型**。

`[讲解]` 注意限制（注释 L42-L44）：

> "Ignored structs can only be referred to from non-ignored structs when referred to as a pointer"

即：被忽略的结构体只能以**指针**形式出现在非忽略结构体里。因为指针在文件里只是个地址编号，不需要知道结构体内部布局。

`[讲解]` `DNA_sdna_types.h` 里的三个结构（`SDNA_StructMember`、`SDNA_Struct`、`SDNA`）都带 `#` `#`——它们是 SDNA 表自身的定义，不需要被 SDNA 序列化（自举问题）。

## 规则九：不要改字段名

`[讲解]` SDNA 按**名字**匹配字段。改名意味着旧文件里的字段找不到目标。

`[讲解]` 如果非改不可，必须加别名（02 篇讲的 `alias` 机制）。Blender 的做法是把旧名注册进别名表，读取时先转换。

**实操建议**：除非有充分理由，不要改 DNA 字段名。改名带来的兼容成本远高于收益。

## 规则十：字段顺序尽量不动

`[讲解]` 虽然 SDNA 按名字匹配，理论上顺序无关，但实际有约束：

1. **padding 位置**由顺序决定（见规则四）；
2. **`makesdna` 的偏移计算**依赖顺序；
3. **某些工具**（如 Python 的 `foreach_get`）依赖字段顺序。

`[讲解]` 所以"末尾追加"是最安全的操作，"中间插入"需要格外小心。

## 完整示例：给 Repeat Output 加一个字段

`[讲解]` 把十条规则用一遍。假设要给 `NodeGeometryRepeatOutput` 加一个 `int filter_index`：

**第一步**：写到末尾（规则六）

```c
struct NodeGeometryRepeatOutput {
  NodeRepeatItem *items = nullptr;
  int items_num = 0;
  int active_index = 0;
  int next_identifier = 0;
  int inspection_index = 0;
  int filter_index = 0;        /* ← 追加在末尾 */
};
```

**第二步**：给默认值（规则二推论）

必须有 `= 0`。否则旧文件读出来是垃圾。

**第三步**：检查 padding（规则三、四）

五个 `int` + 一个指针 = 8 + 5×4 = 28。不是 8 的倍数，**缺 4 字节 padding**。

```c
  int filter_index = 0;
  char _pad[4] = {};           /* ← 补齐到 32 字节 */
```

`[讲解]` **这是最容易漏的一步**。加完字段后 `sizeof` 变了，必须重新检查对齐。

**第四步**：不需要改 blend 回调（规则五）

`filter_index` 是定长整数，SDNA 自动处理。只有动态数组才需要回调。

**第五步**：考虑版本迁移（第 06 章）

如果旧文件的 `filter_index` 应该有个非零的"合理默认值"（比如 -1 表示"无过滤"），需要写 versioning 代码。默认的 0 可能语义不对。

## 用小数据走一遍

`[讲解]` 验证一个 DNA 结构体是否合法，用这个清单：

| 检查 | 方法 |
| --- | --- |
| 大小是 4/8 的倍数 | `static_assert(sizeof(T) % 8 == 0)` |
| 无隐式 padding | 按字段顺序手算偏移，与 `offsetof` 对比 |
| 所有字段有默认值 | 逐个看有没有 `=` |
| 无禁止的 C++ 特性 | grep `virtual`、`template` |
| 动态数组有回调 | grep `blend_write` |

`[讲解]` 以 `NodeRepeatItem` 为例手算。字段依次是 `char *name`、`eNodeSocketDatatype socket_type`、`char _pad[2]`、`int identifier`。

**情形 A：假设枚举占 4 字节**（当前主流编译器对 `eNodeSocketDatatype` 的处理，其最大值 23 完全放得进 4 字节）：

```text
偏移 0 :  char *name           (8 字节)
偏移 8 :  eNodeSocketDatatype  (4 字节)
偏移 12:  char _pad[2]         (2 字节)
偏移 14:  —                    (2 字节隐式 padding，int 需 4 对齐)
偏移 16:  int identifier       (4 字节)
总大小 :  20 → 对齐到 8 的倍数 → 24 字节
```

**情形 B：假设枚举占 2 字节**：

```text
偏移 0 :  char *name           (8 字节)
偏移 8 :  eNodeSocketDatatype  (2 字节)
偏移 10:  char _pad[2]         (2 字节)
偏移 12:  int identifier       (4 字节，恰好 4 对齐)
总大小 :  16 字节，无任何隐式 padding
```

`[讲解]` 这个对比揭示了两件事，都值得记住：

第一，**情形 B 是 `_pad` 的设计意图**——它把"枚举实际占 2 字节"这个假设下的布局补成完美的 16 字节、零隐式 padding。

第二，**情形 A 下 `_pad` 反而使结构体多出 2 字节隐式 padding**（14-15）。这说明 `_pad` 不是为了"消除 padding"，而是为了**让布局在枚举大小变化时仍然可控且自洽**：无论枚举是 2 还是 4 字节，总大小都是 8 的倍数，`identifier` 都能正确对齐。

`[讲解]` 更重要的是第三条推论：**同一个 DNA 结构体在不同编译器下 `sizeof` 可能不同**（16 vs 24）。这听起来很危险，但 SDNA 机制正好化解了它——SDNA 表里记录的是**写出该文件的那台机器**的类型大小，读取时按表解释，所以不同大小的结构体之间仍能互通。

**实用判据**：DNA 结构体的 `sizeof` 必须是 4 或 8 的倍数。写成 `static_assert(sizeof(T) % 8 == 0)` 可以在编译期抓住漏 padding 的情况。

## 反例与边界

### 反例 1：用 `bool` 而不是 `char`

`[讲解]` C 的 `bool` 大小不确定（可能是 1 字节，也可能被当成 `int`）。DNA 里要用 `char` 或显式宽度的整数类型。

### 反例 2：用 `size_t` 存数量

`[讲解]` 32/64 位下 `size_t` 大小不同。应该用 `int` 或 `int64_t`。

### 反例 3：忘记给新增字段默认值

`[讲解]` 编译能过，但读旧文件时字段是垃圾。这是最隐蔽的 bug。

### 反例 4：在结构体里加 `std::string`

`[讲解]` 不是 C 类型，且有堆内存。应该用 `char *` + 手动回调。

### 反例 5：改了字段顺序却没重新检查 padding

`[讲解]` 顺序变了，padding 位置全变，makesdna 算错偏移。

### 反例 6：以为 `#` `#` 是注释

`[讲解]` 是 makesdna 的指令，不是注释。它让结构体**不参与序列化**，但 C 代码里仍然可见。

## 对理解 Repeat 的帮助

`[讲解]` Repeat 的三个 DNA 结构，逐条对照本规则：

| 结构 | 遵守的规则 | 特例 |
| --- | --- | --- |
| `NodeRepeatItem` | 规则一（纯 C）、三（`_pad`）、四（布局控制） | 有 `char *name` 需要深拷贝；**没有** `DNA_DEFINE_CXX_METHODS` |
| `NodeGeometryRepeatInput` | 规则一（只有一个 `int32_t`） | 有 `DNA_DEFINE_CXX_METHODS`；无指针、无动态数组，SDNA 全自动 |
| `NodeGeometryRepeatOutput` | 规则一、三、五（动态数组） | 有 `DNA_DEFINE_CXX_METHODS`；**需要 blend 回调** |

`[讲解]` 一个容易漏看的差异：**只有 Input 与 Output 声明了 `DNA_DEFINE_CXX_METHODS`，`NodeRepeatItem` 没有。**

原因：前两者是"节点存储"（`node->storage` 指向它们），会被 `dna::shallow_copy` 复制——所以需要那套专门处理浅拷贝的宏（下一篇详讲）。而 `NodeRepeatItem` 是**数组元素**，由 `socket_items` 框架用 `copy_item` 逐项深拷贝，不走 `shallow_copy`。

这个差异是很实用的判据：**看到 `DNA_DEFINE_CXX_METHODS` 就说明这个结构体会被整块浅拷贝**。

`[讲解]` 关键对比：Input 节点**不需要**自定义 blend 回调（因为它是纯 POD），而 Output 节点**必须**有（因为 `items` 是动态数组）。

这个差异正是正篇 02-01 强调的："Input 节点**没有**这两个钩子：它注册用的是标准存储读写，一个 int32 由 DNA 机制自动处理。"

## 继续阅读

- [04-DNA_DEFINE_CXX_METHODS与浅拷贝](04-DNA_DEFINE_CXX_METHODS与浅拷贝.md) —— `dna::shallow_copy` 的完整机制
- [05-blend读写与指针重定位](05-blend读写与指针重定位.md) —— 动态数组的实际处理
- [02-SDNA表与类型编码](02-SDNA表与类型编码.md) —— SDNA 的表结构
