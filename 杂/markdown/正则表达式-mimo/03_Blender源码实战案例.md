# Blender 源码正则表达式实战案例

## 目录
- [1. 空间节点编辑器分析](#空间节点编辑器分析)
- [2. 节点系统深度解析](#节点系统深度解析)
- [3. 重构与批量修改](#重构与批量修改)
- [4. 代码质量检查](#代码质量检查)
- [5. 文档生成辅助](#文档生成辅助)

---

## 空间节点编辑器分析

### 1.1. 查找所有节点绘制函数

<span style="background-color: #1e3a8a; color: white; padding: 2px 8px; border-radius: 4px;">源码位置</span>：`source/blender/editors/space_node/node_draw.cc`

```regex
# 搜索模式
^void\s+node_\w+\([^)]*\)\s*\{

# 实际匹配结果 (node_draw.cc:100-200)
void node_draw(bNode *node, bNodeTree *ntree, float x, float y)
void node_draw_sockets(bNode *node, float x, float y)
void node_draw_label(bNode *node, const char *label)
void node_draw_buttons(uiLayout *layout, bContext *C, bNode *node)
```

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">扩展搜索：查找所有节点相关函数</span>

```regex
# 包含静态函数
^\w+\s+node_\w+\([^)]*\)\s*\{

# 在 node_draw.cc 中查找
# 结果示例:
static void node_draw_shadow(bNode *node)
void node_draw(bNode *node, bNodeTree *ntree, float x, float y)
void node_verify_sockets(bNodeTree *ntree, bNode *node, bool do_id_user)
```

### 1.2. 查找节点编辑器操作

<span style="background-color: #f59e0b; color: black; padding: 2px 8px; border-radius: 4px;">源码位置</span>：`source/blender/editors/space_node/node_edit.cc`

```regex
# 查找所有节点编辑函数
^\w+\s+\w+\([^)]*\)\s*\{.*\n.*node_

# 查找节点树操作
ntree->\w+

# 查找节点类型操作
node->type
```

**实际应用**：

```regex
# 在 node_edit.cc:86-100 中查找
搜索: blender::ed::space_node::
匹配:
- blender::ed::space_node::CompoJob
- blender::ed::space_node::node_tree_update_tagged
```

### 1.3. 查找DNA结构体使用

```regex
# 查找DNA头文件包含
#include\s+"DNA_\w+_types\.h"

# 在 node_draw.cc:15-23 中查找
结果:
#include "DNA_light_types.h"
#include "DNA_linestyle_types.h"
#include "DNA_material_types.h"
#include "DNA_modifier_types.h"
#include "DNA_node_types.h"
#include "DNA_screen_types.h"
#include "DNA_space_types.h"
#include "DNA_text_types.h"
#include "DNA_world_types.h"
```

---

## 节点系统深度解析

### 2.1. Socket类型分析

<span style="background-color: #7c3aed; color: white; padding: 2px 8px; border-radius: 4px;">源码位置</span>：`source/blender/nodes/NOD_socket.hh`

```regex
# 查找所有socket相关函数
^\w+\s+node_socket_\w+\([^)]*\)\s*\;

# 实际匹配 (NOD_socket.hh:16-28)
void node_socket_init_default_value_data(eNodeSocketDatatype datatype, int subtype, void **data)
void node_socket_copy_default_value_data(eNodeSocketDatatype datatype, void *to, const void *from)
void node_socket_init_default_value(bNodeSocket *sock)
void node_socket_copy_default_value(bNodeSocket *to, const bNodeSocket *from)
```

### 2.2. 命名空间使用

```regex
# 查找blender::nodes命名空间
blender::nodes::\w+

# 在 NOD_socket.hh:29-36 中查找
结果:
blender::nodes::update_node_declaration_and_sockets
blender::nodes::socket_type_supports_fields
blender::nodes::socket_type_supports_grids
blender::nodes::socket_type_always_single
```

### 2.3. 节点声明更新

```regex
# 查找声明更新函数
update_node_declaration_and_sockets

# 搜索所有调用此函数的地方
\bupdate_node_declaration_and_sockets\b

# 在源码中查找调用
# 结果可能在:
# - node_edit.cc
# - node_group.cc
# - node_templates.cc
```

### 2.4. 函数指针和回调

```regex
# 查找函数指针调用
\(\*\w+\)\s*\(

# 在 Blender 源码中查找
# 示例:
(*node->type->draw)(node, ...)
(*callback)(data)
(*func_ptr)(param1, param2)
```

---

## 重构与批量修改

### 3.1. 函数重命名

<span style="background-color: #dc2626; color: white; padding: 2px 8px; border-radius: 4px;">场景</span>：将 `node_add_socket_from_template` 重命名为 `node_add_socket_from_template_v2`

```regex
# 步骤1: 查找所有调用
搜索: \bnode_add_socket_from_template\b
替换: node_add_socket_from_template_v2

# 步骤2: 查找函数定义
搜索: ^bNodeSocket\s+\*node_add_socket_from_template
替换: bNodeSocket *node_add_socket_from_template_v2
```

### 3.2. 添加参数

```regex
# 场景: 给函数添加调试参数

# 搜索函数定义
搜索: ^(void\s+node_\w+\([^)]*)(\)\s*\{)
替换: $1, bool debug$2

# 结果:
void node_draw(bNode *node, bNodeTree *ntree, float x, float y) {
# 变为:
void node_draw(bNode *node, bNodeTree *ntree, float x, float y, bool debug) {
```

### 3.3. 修改变量命名

```regex
# 场景: 将 node 改为 bnode (更明确的命名)

# 搜索指针声明
搜索: (\w+)\s*\*+\s*node\b
替换: $1 *bnode

# 搜索函数参数
搜索: \(\w+\s*\*+\s*node\b
替换: ($1 *bnode

# 搜索函数体中的使用
搜索: \bnode->
替换: bnode->
```

### 3.4. 批量添加日志

```regex
# 在函数开头添加调试信息

# 搜索函数定义
搜索: ^(void\s+\w+\([^)]*\)\s*\{)
替换: $1\n    printf("DEBUG: Entering %s\\n", "$2");

# 结果:
void node_draw(bNode *node) {
# 变为:
void node_draw(bNode *node) {
    printf("DEBUG: Entering node_draw\n");
```

---

## 代码质量检查

### 4.1. 命名规范检查

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">检查不符合规范的命名</span>：

```regex
# 查找小写开头的全局函数 (C++规范应为驼峰或snake_case)
^[a-z]\w+\s+\w+\(

# 查找缺少空格的运算符
[^+\-*/<>]=[^=]

# 查找行尾空格
\s+$

# 查找混合制表符和空格
^\t* +\t*
```

### 4.2. 内存管理检查

```regex
# 查找内存分配但没有释放
# 这需要结合上下文，但可以查找模式

# 查找MEM_分配
MEM_\w+alloc

# 查找对应的free
MEM_freeN
MEM_deleteN
```

### 4.3. 注释规范检查

```regex
# 查找单行注释缺少空格
//\S

# 查找多行注释格式
/\*\*\s*\n\s*\*.*\n\s*\*/

# 查找SPDX注释完整性
SPDX-FileCopyrightText.*\nSPDX-License-Identifier
```

### 4.4. 头文件包含检查

```regex
# 查找重复包含
#include\s+"BKE_node\.hh"

# 查找未使用的包含
# 需要结合编译器警告，但可以查找模式
#include\s+"[^"]+"\s*$

# 查找包含顺序问题
# 搜索: #include\s+"DNA.*\n#include\s+"BKE
# 这可能表示包含顺序不正确
```

---

## 文档生成辅助

### 5.1. 提取函数列表

```regex
# 从头文件提取所有函数声明
^\w+\s+\w+\([^)]*\)\s*;

# 在 NOD_socket.hh 中应用
结果:
bNodeSocket *node_add_socket_from_template(bNodeTree *ntree, bNode *node, blender::bke::bNodeSocketTemplate *stemp, eNodeSocketInOut in_out)
void node_verify_sockets(bNodeTree *ntree, bNode *node, bool do_id_user)
void node_socket_init_default_value_data(eNodeSocketDatatype datatype, int subtype, void **data)
void node_socket_copy_default_value_data(eNodeSocketDatatype datatype, void *to, const void *from)
void node_socket_init_default_value(bNodeSocket *sock)
void node_socket_copy_default_value(bNodeSocket *to, const bNodeSocket *from)
void register_standard_node_socket_types()
```

### 5.2. 提取结构体定义

```regex
# 查找结构体定义
struct\s+\w+\s*\{[^}]*\}

# 或者更详细
struct\s+(\w+)\s*\{([^}]*)\}

# 在 node_draw.cc:94-100 中查找
struct CompoJob {
  /* Input parameters. */
  Main *bmain;
  Scene *scene;
  ViewLayer *view_layer;
  bNodeTree *ntree;
  /* Evaluated state/ */
  ...
}
```

### 5.3. 生成函数调用图

```regex
# 查找函数调用
\w+\([^)]*\)\s*;

# 排除定义
^\w+\s+\w+\([^)]*\)\s*\{  # 排除函数定义

# 在特定函数中查找调用
# 例如: 在 node_draw 中查找所有调用
# 搜索: node_draw.*\{[\s\S]*?\}
# 然后提取内部的函数调用
```

### 5.4. 提取宏定义

```regex
# 查找所有宏定义
^#define\s+\w+

# 在 node_edit.cc:88 中查找
#define USE_ESC_COMPO

# 查找带参数的宏
^#define\s+\w+\([^)]*\)
```

---

## 高级技巧

### 6.1. 多条件搜索

```regex
# 查找同时包含特定模式的函数
# 例如: 包含 node 和 ntree 的函数
\bnode\b.*\bntree\b

# 查找特定命名模式的函数
^(void|int|bool|bNode\*)\s+node_\w+\([^)]*\)\s*\{
```

### 6.2. 排除模式

```regex
# 使用负向先行断言排除某些模式
# 查找不包含 "test" 的函数
^(?!.*test)\w+\s+\w+\([^)]*\)\s*\{

# 查找不以 _ 开头的变量
\b(?<!_)\w+\b
```

### 6.3. 范围限定

```regex
# 在特定文件范围内搜索
# 使用文件过滤: *.cc, *.hh

# 限定行数范围
# VSCode不支持直接的行范围，但可以使用上下文
```

### 6.4. 替换中的条件逻辑

```regex
# 使用捕获组进行条件替换

# 搜索: (\w+)(\(\w+\s*\*+\s*\w+\))
# 替换: $1_v2$2

# 结果:
node_draw(bNode *node) → node_draw_v2(bNode *node)
```

---

## 实战工作流程

### 完整案例：重构节点编辑器函数

<span style="background-color: #1e3a8a; color: white; padding: 2px 8px; border-radius: 4px;">任务</span>：将 `node_draw` 系列函数添加版本号

```regex
# 步骤1: 查找所有相关函数
搜索: ^void\s+node_\w+\([^)]*\)\s*\{
结果: 5个函数

# 步骤2: 重命名函数定义
搜索: ^(void\s+)node_(draw|draw_sockets|draw_label|draw_buttons|verify_sockets)
替换: $1node_v2_$2

# 步骤3: 重命名函数调用
搜索: \bnode_(draw|draw_sockets|draw_label|draw_buttons|verify_sockets)\b
替换: node_v2_$1

# 步骤4: 验证结果
搜索: node_v2_
计数: 应该是 10 (5定义 + 5调用)
```

### 快速检查清单

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">搜索前</span>：
- [ ] 确认正则模式已启用
- [ ] 在小样本上测试
- [ ] 确认捕获组正确

<span style="background-color: #f59e0b; color: black; padding: 2px 8px; border-radius: 4px;">替换前</span>：
- [ ] 预览替换结果
- [ ] 备份代码
- [ ] 确认范围正确

<span style="background-color: #dc2626; color: white; padding: 2px 8px; border-radius: 4px;">替换后</span>：
- [ ] 编译检查
- [ ] 运行测试
- [ ] 检查意外修改

---

## 性能优化建议

### 避免灾难性回溯

<span style="background-color: #dc2626; color: white; padding: 2px 8px; border-radius: 4px;">不好的模式</span>：
```regex
(a*)*          # 指数级回溯
(a+)*          # 同上
(a|a)*         # 同上
```

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">好的模式</span>：
```regex
a*             # 线性时间
a+             # 线性时间
a              # 线性时间
```

### 大文件优化

```regex
# 1. 使用具体字符类代替 .
# 不好: .*
# 好: [^}]*

# 2. 使用非贪婪模式
# 不好: \{.*\}
# 好: \{[^}]*\}

# 3. 限制重复次数
# 不好: \d*
# 好: \d{1,10}
```

---

## 总结

<span style="background-color: #1e3a8a; color: white; padding: 2px 8px; border-radius: 4px;">核心模式总结</span>：

| 用途 | 模式 | 示例文件 |
|------|------|----------|
| 函数定义 | `^\w+\s+\w+\([^)]*\)\s*\{` | node_draw.cc |
| 函数调用 | `\w+\([^)]*\)` | node_edit.cc |
| 结构体 | `struct\s+\w+\s*\{` | node_draw.cc |
| 头文件 | `#include\s+"[^"]+"` | node_draw.cc |
| 命名空间 | `blender::\w+::\w+` | NOD_socket.hh |
| DNA类型 | `DNA_\w+_types` | node_draw.cc |
| 内存分配 | `MEM_\w+alloc` | node_edit.cc |

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">Blender特定</span>：
- `bNode`, `bNodeTree`, `bNodeSocket`
- `ntree->`, `node->`, `sock->`
- `node_\w+`, `NOD_\w+`, `DNA_\w+`
- `BLI_\w+`, `BKE_\w+`

---

**相关文档**：
- [01_正则表达式完全指南.md](./01_正则表达式完全指南.md) - 完整语法
- [02_VSCode快速参考.md](./02_VSCode快速参考.md) - 快捷键和常用模式

**源码参考**：
- `source/blender/editors/space_node/`
- `source/blender/nodes/`
