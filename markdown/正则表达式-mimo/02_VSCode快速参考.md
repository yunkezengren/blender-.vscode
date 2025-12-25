# VSCode 正则表达式快速参考指南

## 目录
- [1. 快捷键速查](#快捷键速查)
- [2. 常用搜索模式](#常用搜索模式)
- [3. Blender源码专用模式](#blender源码专用模式)
- [4. 替换技巧](#替换技巧)
- [5. 调试与验证](#调试与验证)

---

## 快捷键速查

<span style="background-color: #1e3a8a; color: white; padding: 2px 8px; border-radius: 4px;">Windows/Linux</span>：

| 功能 | 快捷键 | 说明 |
|------|--------|------|
| 全局搜索 | `Ctrl+Shift+F` | 在所有文件中搜索 |
| 当前文件搜索 | `Ctrl+F` | 在当前文件中搜索 |
| 切换正则模式 | `Alt+R` 或点击 `.*` 按钮 | 启用/禁用正则表达式 |
| 替换 | `Ctrl+H` | 打开替换面板 |
| 全部替换 | `Ctrl+Alt+Enter` | 替换所有匹配项 |

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">macOS</span>：

| 功能 | 快捷键 | 说明 |
|------|--------|------|
| 全局搜索 | `Cmd+Shift+F` | 在所有文件中搜索 |
| 当前文件搜索 | `Cmd+F` | 在当前文件中搜索 |
| 切换正则模式 | `Option+R` | 启用/禁用正则表达式 |
| 替换 | `Cmd+H` | 打开替换面板 |

---

## 常用搜索模式

### 基础模式

<span style="background-color: #f59e0b; color: black; padding: 2px 8px; border-radius: 4px;">函数相关</span>：

```regex
# 查找函数定义
^\w+\s+\w+\([^)]*\)\s*\{

# 查找函数调用
\w+\(\)

# 查找特定函数
\bprintf\b
\bnode_add_socket_from_template\b

# 查找带参数的函数调用
\w+\([^)]+\)
```

<span style="background-color: #7c3aed; color: white; padding: 2px 8px; border-radius: 4px;">变量相关</span>：

```regex
# 查找指针声明
\w+\s*\*+\s*\w+

# 查找变量赋值
\w+\s*=\s*[^;]+

# 查找特定变量名
\bnode\b
\bntree\b
```

<span style="background-color: #dc2626; color: white; padding: 2px 8px; border-radius: 4px;">注释与文档</span>：

```regex
# 单行注释
//.*$

# 多行注释
/\*[\s\S]*?\*/

# SPDX注释
SPDX-FileCopyrightText.*\nSPDX-License-Identifier

# 文件头注释
/\*\*\\file
```

### 高级模式

<span style="background-color: #0891b2; color: white; padding: 2px 8px; border-radius: 4px;">结构体与类</span>：

```regex
# 结构体定义
struct\s+\w+\s*\{

# 类定义
class\s+\w+\s*[:{]

# DNA结构体
DNA_\w+_types\.h

# 命名空间
namespace\s+\w+\s*\{
```

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">头文件包含</span>：

```regex
# 包含双引号
#include\s+"[^"]+"

# 包含尖括号
#include\s+<[^>]+>

# 特定头文件
#include\s+"BKE_node\.hh"
```

---

## Blender源码专用模式

### 空间节点编辑器 (space_node)

<span style="background-color: #1e3a8a; color: white; padding: 2px 8px; border-radius: 4px;">源码位置</span>：`source/blender/editors/space_node/`

```regex
# 查找所有节点绘制函数
^void\s+node_\w+\([^)]*\)\s*\{

# 查找节点编辑器相关函数
\bed::space_node::\w+\(

# 查找节点树操作
ntree->\w+

# 查找节点类型
node->type

# 查找socket操作
sock->\w+
```

**实际应用示例**：

```regex
# 在 node_draw.cc 中查找所有函数
搜索: ^void\s+node_\w+\(
结果:
- void node_draw(bNode *node)
- void node_verify_sockets(bNodeTree *ntree, bNode *node, bool do_id_user)
```

### 节点系统 (nodes)

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">源码位置</span>：`source/blender/nodes/`

```regex
# 查找NOD_开头的函数
\bNOD_\w+\(

# 查找blender::nodes命名空间
blender::nodes::\w+

# 查找socket类型
eNodeSocketDatatype

# 查找节点声明
update_node_declaration_and_sockets
```

**实际应用示例**：

```regex
# 在 NOD_socket.hh 中查找函数
搜索: void\s+\w+\([^)]*\);
结果:
- void node_add_socket_from_template(...)
- void node_verify_sockets(...)
- void node_socket_init_default_value(...)
```

### DNA和内存管理

```regex
# DNA结构体
DNA_\w+_types

# 内存分配
MEM_\w+alloc

# 字符串操作
BLI_\w+

# 数学函数
math_\w+
```

---

## 替换技巧

### 基础替换

<span style="background-color: #f59e0b; color: black; padding: 2px 8px; border-radius: 4px;">捕获组引用</span>：

```regex
# 搜索: (\w+)_v(\d+)
# 替换: $1_v$2
# 结果: func_v1 → func_v1 (不变)

# 搜索: (\w+)_v(\d+)
# 替换: $1_v$2_v2
# 结果: func_v1 → func_v1_v2
```

### 实用替换模式

<span style="background-color: #7c3aed; color: white; padding: 2px 8px; border-radius: 4px;">函数重命名</span>：

```regex
# 搜索: node_add_socket_from_template
# 替换: node_add_socket_from_template_v2
```

<span style="background-color: #dc2626; color: white; padding: 2px 8px; border-radius: 4px;">添加参数</span>：

```regex
# 搜索: (\w+)\(ntree, node
# 替换: $1(ntree, node, extra_param
# 结果: func(ntree, node → func(ntree, node, extra_param
```

<span style="background-color: #0891b2; color: white; padding: 2px 8px; border-radius: 4px;">修改类型</span>：

```regex
# 搜索: (\w+)\s+\*+\s*(\w+)
# 替换: const $1 *$2
# 结果: bNode *node → const bNode *node
```

### 批量注释

```regex
# 添加调试日志
搜索: ^(void\s+\w+\([^)]*\)\s*\{)
替换: $1\n    printf("DEBUG: Entering %s\\n", "$2");

# 修改注释格式
搜索: //\s*(.*)
替换: /* $1 */
```

---

## 调试与验证

### 测试策略

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">步骤1: 小样本测试</span>

```regex
# 先在单个文件中测试
# 例如: source/blender/nodes/NOD_socket.hh

# 测试模式
^\w+\s+\w+\([^)]*\)\s*;

# 预期匹配
bNodeSocket *node_add_socket_from_template(...)
void node_verify_sockets(...)
```

<span style="background-color: #1e3a8a; color: white; padding: 2px 8px; border-radius: 4px;">步骤2: 逐步扩展</span>

1. 确认基础模式正确
2. 添加边界条件
3. 测试特殊字符
4. 验证替换结果

### 常见问题排查

<span style="background-color: #dc2626; color: white; padding: 2px 8px; border-radius: 4px;">问题1: 无匹配结果</span>

**可能原因**：
- 正则模式太严格
- 忘记启用正则模式
- 大小写不匹配

**解决方案**：
```regex
# 使用更宽松的模式
# 原: ^void\s+node_\w+\(
# 改: void\s+node_\w+\(
```

<span style="background-color: #f59e0b; color: black; padding: 2px 8px; border-radius: 4px;">问题2: 匹配过多</span>

**可能原因**：
- 模式太宽泛
- 缺少边界限制

**解决方案**：
```regex
# 使用单词边界
# 原: node
# 改: \bnode\b
```

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">问题3: 替换错误</span>

**解决方案**：
- 使用捕获组 `()` 和 `$1`, `$2`
- 先预览替换结果
- 小范围测试后再全库替换

### 验证工具

<span style="background-color: #7c3aed; color: white; padding: 2px 8px; border-radius: 4px;">在线测试</span>：
- [regex101.com](https://regex101.com) - 实时测试和解释
- [regexr.com](https://regexr.com) - 可视化匹配

<span style="background-color: #0891b2; color: white; padding: 2px 8px; border-radius: 4px;">VSCode内置</span>：
- 搜索结果计数
- 高亮显示匹配
- 替换预览

---

## 实战案例

### 案例1: 查找所有节点类型定义

```regex
# 搜索
\bnode_type_\w+\b

# 在 source/blender/editors/space_node/
# 结果示例:
- node_type_draw
- node_type_edit
- node_type_select
```

### 案例2: 批量修改函数名

```regex
# 搜索旧函数名
\bnode_socket_init\b

# 替换为新函数名
node_socket_init_v2

# 在替换前先搜索确认匹配数
```

### 案例3: 查找未使用的变量

```regex
# 查找声明但未使用的变量
^\s*\w+\s*\*?\s*\w+\s*;\s*$

# 注意：这需要结合上下文判断
```

### 案例4: 验证代码规范

```regex
# 查找不符合命名规范的函数
^[a-z]\w+\s+\w+\(

# 查找缺少空格的运算符
[^+\-*/<>]=[^=]

# 查找行尾空格
\s+$
```

---

## 总结

<span style="background-color: #1e3a8a; color: white; padding: 2px 8px; border-radius: 4px;">核心要点</span>：

1. **快捷键**: `Ctrl+Shift+F` + `Alt+R` = 全局正则搜索
2. **基础模式**: `\w+`, `\d+`, `.*`, `^`, `$`
3. **Blender专用**: `node_\w+`, `ntree->`, `bNode`
4. **替换技巧**: 使用 `$1`, `$2` 引用捕获组
5. **调试方法**: 小样本测试 → 逐步扩展 → 全库应用

<span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">快速开始</span>：

```bash
# 1. 打开VSCode
# 2. Ctrl+Shift+F
# 3. Alt+R 启用正则
# 4. 输入模式
# 5. 查看结果
```

---

**参考文档**：
- [01_正则表达式完全指南.md](./01_正则表达式完全指南.md) - 详细语法说明
- Blender源码: `source/blender/editors/space_node/`
- Blender源码: `source/blender/nodes/`
