# Blender Overlay GLSL 系统 - 完整学习指南

## 📚 文档清单

这个教程包含了 **7 个详细文档**，从基础到高级，系统讲解 Blender overlay 引擎的 GLSL 架构。

### 🎯 推荐学习路径

| 顺序 | 文档 | 预计时间 | 难度 |
|------|------|----------|------|
| **1** | [01_glsl_syntax_detailed.md](01_glsl_syntax_detailed.md) | 2小时 | ⭐⭐ |
| **2** | [02_overlay_glsl_overview.md](02_overlay_glsl_overview.md) | 1小时 | ⭐⭐ |
| **3** | [04_glsl_basics_and_blender_syntax.md](04_glsl_basics_and_blender_syntax.md) | 2小时 | ⭐⭐⭐ |
| **4** | [03_overlay_cpp_glsl_integration.md](03_overlay_cpp_glsl_integration.md) | 3小时 | ⭐⭐⭐⭐ |
| **5** | [05_overlay_core_libraries.md](05_overlay_core_libraries.md) | 2小时 | ⭐⭐⭐ |
| **6** | [06_overlay_shader_examples.md](06_overlay_shader_examples.md) | 3小时 | ⭐⭐⭐⭐ |
| **7** | [07_blender_glsl_vs_standard_glsl.md](07_blender_glsl_vs_standard_glsl.md) | 2小时 | ⭐⭐⭐ |

---

## 📖 每个文档的作用

### 文档 1: GLSL 语法基础 (01_glsl_syntax_detailed.md)

**目标**: 掌握 GLSL 基础语法

**内容**:
- 数据类型详解（vec/mat/sampler）
- 限定符系统（uniform/in/out）
- 函数定义与参数传递
- 预处理指令
- 内置函数库

**何时阅读**:
- 你有 Python 基础但 GLSL 是零基础
- 需要快速查阅 GLSL 语法

**核心知识点**:
```glsl
// 理解这种基本结构
vec4 color = texture(tex, uv);
gl_Position = MVP * vec4(position, 1.0);
```

---

### 文档 2: 系统架构概览 (02_overlay_glsl_overview.md)

**目标**: 理解大局，知道文件分布

**内容**:
- 118 个 GLSL 文件分类和功能
- ShaderModule 类设计
- 4 种变体系统
- C++ 与 GLSL 的分层架构

**何时阅读**:
- 开始前先读，建立整体认知
- 搞不清楚某个文件作用时查阅

**核心知识点**:
```
source/blender/draw/engines/overlay/
├── shaders/ (118 files)
│   ├── overlay_edit_mesh_*.glsl (编辑模式)
│   ├── overlay_armature_*.glsl (骨骼)
│   └── ...
├── overlay_private.hh (ShaderModule)
├── overlay_shader.cc (变体实现)
└── shaders/infos/ (配置)
```

---

### 文档 3: Blender GLSL 语法扩展 (04_glsl_basics_and_blender_syntax.md)

**目标**: 学会 Blender 独特的语法

**内容**:
- **宏系统**: `GPU_SHADER_CREATE_INFO`
- **库系统**: `#include "draw_view_lib"`
- **条件编译**: `#ifdef VERT`
- **C++ 配置**: ` .vertex_in() `.sampler()``

**何时阅读**:
- 已知 GLSL 基础，想看懂 Blender 代码
- 需要自己编写第一个 Blender shader

**核心知识点**:
```cpp
// 这是 Blender 的"魔法"配置
GPU_SHADER_CREATE_INFO(my_shader)
    .define("VERT")                          // 生成 #define VERT
    .vertex_in(0, float3, position)          // 生成 layout(location=0) in vec3 position
    .sampler(0, sampler2D, tex)              // 生成 uniform sampler2D tex
    .additional_info("draw_view")            // 自动包含库
.end()

// 实际上生成为复合后的纯 GLSL
```

---

### 文档 4: C++ 与 GLSL 调用机制 (03_overlay_cpp_glsl_integration.md)

**目标**: 理解数据如何从 C++ 流向 GPU

**内容**:
- ShaderModule 的变体生成
- Resources 的管理流程
- UBO/Texture/PushConstant 的绑定
- 渲染管线完整流程
- Shader Info 系统的工作原理

**何时阅读**:
- 想调试问题（需要知道数据流向）
- 需要扩展 C++ 侧功能
- 性能调优

**核心知识点**:
```mermaid
C++ (Resources::init)
    ↓ (变体)
"overlay_edit_mesh_vert_clipped"
    ↓ (编译)
GPU Program
    ↓ (绑定)
glDrawArrays → 执行
```

---

### 文档 5: 核心库深度解析 (05_overlay_core_libraries.md)

**目标**: 掌握可用的库函数

**内容**:
- **视图库**: `drw_view()`, `drw_point_world_to_view()`
- **数学库**: `get_homogenous_z_offset()`, `plane_from_tri()`
- **编辑库**: `EDIT_MESH_vertex_color()`
- **工具库**: `pack_line_data()`, `extract_matrix_packed_data()`

**何时阅读**:
- 编写 shader 时查阅函数
- 不知道某个函数如何工作

**核心函数索引**:

| 函数 | 作用 | 使用频率 |
|------|------|----------|
| `drw_point_object_to_world()` | 坐标变换 | ⭐⭐⭐⭐⭐ |
| `drw_view()` | 获取视图矩阵 | ⭐⭐⭐⭐⭐ |
| `get_homogenous_z_offset()` | 深度偏移 | ⭐⭐⭐ |
| `EDIT_MESH_vertex_color()` | 顶点颜色 | ⭐⭐⭐ |
| `textureGather()` | 深度测试 | ⭐⭐⭐ |
| `pack_line_data()` | 线段打包 | ⭐⭐ |

---

### 文档 6: 典型 Shader 深度剖析 (06_overlay_shader_examples.md)

**目标**: 通过真实代码理解设计

**内容**:
- **案例 1**: `overlay_edit_mesh_vert.glsl`（完整分析）
- **案例 2**: `overlay_edit_mesh_edge_vert.glsl`（几何着色器）
- **案例 3**: `overlay_armature_sphere_solid.Vert.glsl`（实例 + 光线求交）
- **案例 4**: `overlay_edit_mesh_analysis_vert.glsl`（简单且典型）
- **案例 5**: UV 着色器（虚线模式）

**何时阅读**:
- 需要编写复杂的 shader
- 学习最佳实践
- 理解高级技巧

**关键案例学习点**:

| 案例 | 学习要点 |
|------|---------|
| 网格编辑 | 单文件多模式、纹理收集、Fresnel |
| 边缘扩展 | 几何着色器、顶点拉取、抗锯齿 |
| 骨骼球体 | 实例渲染、逆矩阵、光线求交 |
| 权重分析 | 简单映射、LUT 使用 |

---

### 文档 7: 标准 vs Blender 全面对比 (07_blender_glsl_vs_standard_glsl.md)

**目标**: 理解差异，避免混淆

**内容**:
- 定义方式对比
- 资源绑定对比
- 库系统对比
- 高级特性对比
- 迁移指南

**何时阅读**:
- 有标准 GLSL 背景想知道 Blender 的不同
- 需要将代码移植
- 做技术选型

**核心结论**:

| 场景 | 推荐 |
|------|------|
| 小型项目 (<5 shaders) | 标准 GLSL |
| 大型项目 (>20 shaders) | Blender GLSL |
| 需要快速开发 | Blender GLSL |
| 需要绝对控制 | 标准 GLSL |
| 团队协作 | Blender GLSL |

---

## 🔍 按需求快速查找

### ❓ "我想写个简单的 overlay shader"

**阅读**: 文档 1 → 文档 3 → 文档 2 → 文档 5

### ❓ "C++ 代码和 GLSL 交互有问题"

**阅读**: 文档 4 → 文档 5（库函数）

### ❓ "我想理解某个复杂 shader"

**阅读**: 文档 6 → 文档 3（语法）→ 文档 5（库查表）

### ❓ "为什么我的 shader 不工作？"

**阅读**: 文档 7（对比排查）→ 文档 4（流程检查）
常见问题：
1. 忘记 `#include "infos/...hh"`
2. 库未添加到 `.additional_info()`
3. 变体宏拼写错误
4. Uniform 未绑定

### ❓ "性能优化"

**阅读**: 文档 4 → 文档 6 → 文档 3
优化点：
- 使用 `textureGather`
- 减少分支
- 静态编译
- 异步加载
- 顶点拉取代替属性

---

## 🎓 预期学习成果

完成全部 7 个文档后，你应该能够：

### ✅ 基础能力
- [ ] 写出标准的 GLSL 顶点/片段着色器
- [ ] 理解 Blender 特有的宏和配置系统
- [ ] 使用核心库函数进行坐标变换

### ✅ 进阶能力
- [ ] 为 Blender 设计新的 shader 配置
- [ ] 调试 shader 编译错误
- [ ] 在 C++ 中正确绑定 shader 参数
- [ ] 理解几何着色器的工作流程

### ✅ 高级能力
- [ ] 阅读并理解任何 overlay shader
- [ ] 扩展库系统添加自定义函数
- [ ] 优化 shader 性能
- [ ] 将标准 GLSL 转换为 Blender GLSL

---

## 🛠️ 实践建议

### 学习阶段

**阶段 1: 熟悉环境**
```
1. 找到 overlay_shaders 目录
2. 打开 01_glsl_syntax_detailed.md
3. 在 Blender 中看实际的 shader 文件
4. 对照文档理解一行代码
```

**阶段 2: 简单修改**
```
1. 修改 overlay_common_lib.glsl
2. 添加一个简单的调试颜色函数
3. 在编辑网格 shader 中调用它
4. 编译运行，看效果
```

**阶段 3: 理解流程**
```
1. 调试 overlay_instance.cc
2. 跟踪一个 draw call 的完整流程
3. 查看 ShaderModule 的缓存机制
```

**阶段 4: 完整创作**
```
1. 新建一个 shader_infos
2. 写一个新 shader
3. 在 C++ 中添加到 ShaderModule
4. 集成到渲染流程
```

### 调试技巧

```cpp
// 1. 打印实际使用的 shader
printf("Shader: %s\n", module.my_shader.name());

// 2. 查看编译错误
if (!shader.compile_ok()) {
    printf("Error: %s\n", shader.get_error_log());
}

// 3. 检查 UBO 绑定
glGetIntegeri_v(GL_UNIFORM_BUFFER_BINDING, 0, &ubo_id);

// 4. 查看 OpenGL 调用
glEnable(GL_DEBUG_OUTPUT);
// 或使用 RenderDoc
```

---

## 🔗 附加资源

### 官方文档
- [Blender 源码](https://projects.blender.org/blender/blender)
- [OpenGL 规范](https://www.khronos.org/registry/OpenGL/specs/gl/)
- [GLSL 规范](https://www.khronos.org/registry/OpenGL/specs/gl/GLSLangSpec.4.60.pdf)

### 工具
- **RenderDoc**: 图形调试器
- **glslangValidator**: GLSL 编译器
- **Blender**: 使用 Debug 模式启用 OpenGL 调试

### 关键目录
```
source/blender/draw/engines/overlay/
├── shaders/                      # GLSL 源码
│   ├── *.glsl                    # 118 个文件
│   └── infos/                    # 配置定义
├── overlay_private.hh            # ShaderModule
├── overlay_shader.cc             # 变体实现
└── overlay_*.hh/.cc              # 渲染逻辑

source/blender/draw/intern/shaders/
└── draw_*.glsl                   # 通用库
```

---

## 💡 最后的建议

### ✅ Do's
1. **从文档 1 开始**, 不要跳过基础
2. **对照源码阅读**，打开实际文件
3. **小步修改**，一次只改一点
4. **及时测试**，修改后立即验证
5. **做笔记**，记录不理解的模式

### ❌ Don'ts
1. **不要死记硬背**，理解设计原理
2. **不要跳过文档 4**，这是理解的关键
3. **不要忽略错误信息**，编译器会告诉你问题
4. **不要复制粘贴**，手动敲一遍加深理解
5. **不要一次性全部学完**，分阶段进行

### 时间安排建议

**紧张时间表（1 周）**:
- Day 1: 文档 1 + 2
- Day 2: 文档 3
- Day 3: 文档 4
- Day 4: 文档 5（查阅式）
- Day 5-6: 文档 6
- Day 7: 文档 7 + 实践

**完整时间表（1 个月）**:
- Week 1: 文档 1-3 + 简单实践
- Week 2: 文档 4 + 源码跟踪
- Week 3: 文档 5 + 练习库函数
- Week 4: 文档 6 + 7 + 完整项目

---

## 🎉 开始学习！

**第一步**: 打开 `01_glsl_syntax_detailed.md`

**第二步**: 在 Blender 源码中找到对应文件

**第三步**: 准备好你的编辑器和调试工具

**第四步**: 开始你的 GLSL 之旅！

---

**文档维护**: 2025-12-17
**适用版本**: Blender 4.3+
**文档状态**: 完整版 v1.0

如需更新或补充，请参考 Blender 官方源码仓库。
