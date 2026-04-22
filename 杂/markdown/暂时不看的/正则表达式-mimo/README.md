# 正则表达式文档集 - Blender开发指南

<span style="background-color: #1e3a8a; color: white; padding: 4px 12px; border-radius: 6px; font-size: 16px; font-weight: bold;">📚 文档导航</span>

## 快速开始

如果你是：
- <span style="background-color: #059669; color: white; padding: 2px 6px; border-radius: 3px;">初学者</span> → 从 [01_正则表达式完全指南](./01_正则表达式完全指南.md) 开始
- <span style="background-color: #f59e0b; color: black; padding: 2px 6px; border-radius: 3px;">快速查询</span> → 查看 [02_VSCode快速参考](./02_VSCode快速参考.md)
- <span style="background-color: #7c3aed; color: white; padding: 2px 6px; border-radius: 3px;">实战应用</span> → 阅读 [03_Blender源码实战案例](./03_Blender源码实战案例.md)

---

## 📁 文档结构

```
.vscode/正则表达式-mimo/
├── 01_正则表达式完全指南.md      # 完整语法和理论基础
├── 02_VSCode快速参考.md         # 快捷键和常用模式速查
├── 03_Blender源码实战案例.md     # 实际应用和案例分析
└── README.md                     # 本文档
```

---

## 🎯 文档特点

### 1. 丰富的视觉元素
- <span style="background-color: #1e3a8a; color: white; padding: 2px 8px; border-radius: 4px;">彩色HTML标签</span> 用于强调关键信息
- <span style="background-color: #059669; color: white; padding: 2px 8px; border-radius: 4px;">绿色高亮</span> 表示最佳实践
- <span style="background-color: #f59e0b; color: black; padding: 2px 8px; border-radius: 4px;">橙色高亮</span> 表示警告或注意
- <span style="background-color: #dc2626; color: white; padding: 2px 8px; border-radius: 4px;">红色高亮</span> 表示错误或问题

### 2. Mermaid图表
包含多种图表类型：
- **流程图** - 正则表达式使用流程
- **状态图** - 搜索优化过程
- **关系图** - 复杂度对比

### 3. LaTeX数学公式
用于解释理论概念：
- 量词语义的数学表示
- 时间复杂度分析
- 正则表达式的形式化定义

### 4. Blender源码实战
所有示例都基于真实的Blender源码：
- `source/blender/editors/space_node/`
- `source/blender/nodes/`

---

## 📖 各文档详细说明

### 01_正则表达式完全指南.md

**内容概览**：
- 正则表达式核心语法详解
- VSCode搜索功能深度解析
- 大型代码库高效使用场景
- 实用技巧与最佳实践

**特色**：
- 完整的语法表格
- Blender C++/Python代码示例
- 性能优化建议
- Mermaid流程图和LaTeX公式

**适合**：系统学习正则表达式

---

### 02_VSCode快速参考.md

**内容概览**：
- 快捷键速查表
- 常用搜索模式集合
- Blender专用模式
- 替换技巧和调试方法

**特色**：
- 快速查找表格
- 实用案例
- 问题排查指南
- 实战工作流程

**适合**：日常开发快速查询

---

### 03_Blender源码实战案例.md

**内容概览**：
- 空间节点编辑器分析
- 节点系统深度解析
- 重构与批量修改案例
- 代码质量检查方法
- 文档生成辅助

**特色**：
- 完整的重构案例
- 代码质量检查清单
- 文档生成技巧
- 性能优化建议

**适合**：Blender源码开发和重构

---

## 🚀 快速使用指南

### 搜索模式

```regex
# 在VSCode中启用正则搜索
Ctrl+Shift+F → Alt+R → 输入模式

# 常用Blender搜索
\bnode_\w+\b                    # 节点相关函数
ntree->\w+                      # 节点树操作
bNode\s*\*                      # bNode指针
#include\s+"BKE_node\.hh"       # 头文件包含
```

### 替换模式

```regex
# 使用捕获组
搜索: (\w+)_v(\d+)
替换: $1_v$2_v2

# 函数重命名
搜索: \bnode_add_socket_from_template\b
替换: node_add_socket_from_template_v2
```

---

## 🎓 学习路径建议

### 第1天：基础入门
1. 阅读 01_文档的第1-2章
2. 在VSCode中尝试基础搜索
3. 练习 `\d+`, `\w+`, `.*` 等简单模式

### 第2-3天：进阶应用
1. 学习捕获组和替换
2. 阅读 02_快速参考
3. 在Blender源码中实践

### 第4-5天：实战精通
1. 阅读 03_实战案例
2. 尝试重构任务
3. 优化搜索性能

---

## 🔧 Blender开发专用技巧

### 节点编辑器相关

```regex
# 查找节点绘制函数
^void\s+node_\w+\([^)]*\)\s*\{

# 查找socket操作
sock->\w+

# 查找节点树操作
ntree->\w+
```

### DNA结构体相关

```regex
# 查找DNA包含
#include\s+"DNA_\w+_types\.h"

# 查找DNA类型使用
DNA_\w+_types
```

### 内存管理相关

```regex
# 查找内存分配
MEM_\w+alloc

# 查找内存释放
MEM_freeN
MEM_deleteN
```

---

## 💡 实用提示

### 性能优化
- 避免使用 `.*` 匹配整个文件
- 使用具体字符类 `[^\}]` 代替 `.*`
- 限制重复次数 `\d{1,10}` 而不是 `\d*`

### 调试技巧
1. 先在小文件中测试
2. 逐步增加复杂度
3. 使用在线工具验证
4. 检查匹配计数

### 安全操作
1. 搜索后先预览
2. 小范围替换测试
3. 使用版本控制
4. 编译验证

---

## 📚 相关资源

### 在线工具
- [regex101.com](https://regex101.com) - 实时测试
- [regexr.com](https://regexr.com) - 可视化

### Blender源码
- `source/blender/editors/space_node/`
- `source/blender/nodes/`
- `source/blender/makesdna/`

### 文档模板
- 参考 `.vscode\Markdown文档模板.md`

---

## 🔄 更新日志

**2025-12-24** - 初始版本
- 创建完整指南文档
- 添加快速参考手册
- 编写Blender实战案例
- 包含Mermaid图表和LaTeX公式

---

## 📝 使用反馈

如果在使用过程中发现：
- 模式不准确
- 示例需要更新
- 有新的使用场景

请根据实际需求修改文档，保持与Blender源码的同步更新。

---

<span style="background-color: #1e3a8a; color: white; padding: 4px 12px; border-radius: 6px;">🎯 开始你的正则表达式之旅吧！</span>
