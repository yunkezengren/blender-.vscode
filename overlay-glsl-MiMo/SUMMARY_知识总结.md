# Blender Overlay GLSL 系统 - 知识总结文档

> **创建时间**: 2025-12-17
> **适用版本**: Blender 4.3+
> **文档性质**: 快速复习/知识索引

---

## 📊 核心概览

### 1. 系统架构

```
C++ 层 (source/blender/draw/engines/overlay/)
├── overlay_private.hh         # ShaderModule 类
├── overlay_shader.cc          # 变体生成 + 编译
├── overlay_instance.cc        # 渲染实例
└── overlay_*_pass.cc        # 渲染流程

GLSL 层 (source/blender/draw/engines/overlay/shaders/)
├── shaders/infos/             # 配置定义 (.hh)
│   └── overlay_*_infos.hh
├── shaders/*.glsl             # 118+ 个着色器文件
│   ├── overlay_edit_mesh_*.glsl    # 编辑模式
│   ├── overlay_armature_*.glsl     # 骨骼
│   ├── overlay_curve_*.glsl        # 曲线
│   ├── overlay_lattice_*.glsl      # 晶格
│   ├── overlay_empty_*.glsl        # 空物体
│   ├── overlay_image_*.glsl        # 图像
│   └── overlay_*.glsl              # 其他
└── lib/                       # 通用库
    ├── overlay_common_lib.glsl
    ├── overlay_edit_mesh_common_lib.glsl
    └── ...

公共库 (source/blender/draw/intern/shaders/)
├── draw_view_lib.glsl         # 视图变换
├── draw_model_lib.glsl        # 模型矩阵
├── draw_math_geom_lib.glsl    # 几何数学
└── gpu_shader_math_*.glsl     # 向量运算
```

### 2. ShaderModule 工作原理

**核心类**: `class ShaderModule` (overlay_private.hh:428)

```cpp
// 变体维度：选择状态 + 裁剪状态
StaticCache static_cache[2][2];  // [Selection][Clipping]

// 获取变体
ShaderModule& module_get(SelectionType selection, bool clipping) {
    return cache[selection][clipping];
}

// 使用示例
auto& module = ShaderModule::module_get(SelectionType::ENABLED, true);
StaticShader shader = module.my_shader;  // 返回 "overlay_edit_mesh_vert_clipped"
```

**变体组合**:
- **4 种基础**: VERT / EDGE / FACE / FACEDOT
- **+ 裁剪**: 后缀 `_clipped`
- **+ 选择**: 后缀 `_selectable`
- **最长**: 8 种变体 (4 × 2 × 2)

---

## 🔧 关键技术点

### 1. 信息配置系统 (Shader Info)

**C++ 配置** → **GLSL 自动生成**:

```cpp
GPU_SHADER_CREATE_INFO(overlay_edit_mesh_vert)
    .define("VERT")                           // → #define VERT
    .vertex_in(0, float3, pos)                // → layout(location=0) in float3 pos;
    .vertex_in(1, uint4, data)                // → layout(location=1) in uint4 data;
    .vertex_source("overlay_edit_mesh_vert.glsl")
    .fragment_source("overlay_point_varying_color_frag.glsl")
    .additional_info("draw_view")             // 自动包含库
    .additional_info("overlay_edit_mesh_common")
.end()

CREATE_INFO_VARIANT(overlay_edit_mesh_vert_selectable,
                    overlay_edit_mesh_vert,
                    drw_selectable)
```

**GLSL 生成结果**:
```glsl
// （在编译前由系统自动组合）

#define VERT
#define VERTEX_SHADER_CREATE_INFO overlay_edit_mesh_vert

// draw_view 库自动注入的内容
layout(std140, binding = 0) uniform ViewMatrices {
    mat4 viewmat;
    mat4 winmat;
    // ...
} drw_view_buf;
uniform int drw_view_id;

// overlay_edit_mesh_common 库注入
#define VERT_ACTIVE 0x0001u
#define VERT_SELECTED 0x0002u
// ...

// 用户的 shader 代码
// source/blender/draw/engines/overlay/shaders/overlay_edit_mesh_vert.glsl
```

### 2. 库函数系统

**三层架构**:
1. **基础库** (`draw_view_lib.glsl`, `draw_model_lib.glsl`) - 核心变换
2. **工具库** (`overlay_common_lib.glsl`) - 常用函数
3. **应用库** (`overlay_edit_mesh_common_lib.glsl`) - 业务逻辑

**最常用的 5 个函数**:

| 函数 | 作用 | 使用频率 |
|------|------|----------|
| `drw_point_object_to_world(pos)` | 对象→世界坐标 | ⭐⭐⭐⭐⭐ |
| `drw_point_world_to_view(world)` | 世界→视图坐标 | ⭐⭐⭐⭐⭐ |
| `drw_point_view_to_homogenous(view)` | 视图→齐次裁剪 | ⭐⭐⭐⭐⭐ |
| `get_homogenous_z_offset(winmat, z, w, offset)` | 深度偏移 | ⭐⭐⭐ |
| `EDIT_MESH_vertex_color(flag, crease)` | 顶点颜色 | ⭐⭐⭐ |

### 3. 深度偏移机制

**问题**: 不同投影（透视/正交）需要不同偏移策略

**解决方案**:
```glsl
// overlay_common_lib.glsl:482
float get_homogenous_z_offset(float4x4 winmat, float vs_z, float hs_w, float vs_offset)
{
    if (vs_offset == 0.0f) return 0.0f;

    if (winmat[3][3] == 0.0f) {  // 透视投影
        // Eric Lengyel 公式
        return winmat[3][2] * (vs_offset / (vs_z * (vs_z + vs_offset))) * hs_w;
    }
    else {  // 正交投影
        return winmat[2][2] * vs_offset * hs_w;
    }
}

// 使用
gl_Position.z += get_homogenous_z_offset(
    drw_view().winmat,
    view_pos.z,
    gl_Position.w,
    retopology_offset
);
```

### 4. 数据打包技巧 (Matrix Packing)

**目的**: 节省 UBO 空间，将额外信息塞入矩阵第4列

```glsl
// C++ 端: 一个矩阵 = 64 bytes
// 传统: 需要单独的 UBO 存储颜色数据 (额外 16 bytes)
// 优化: 将颜色打包进矩阵第4列

// GLSL 解包
float4x4 extract_matrix_packed_data(float4x4 mat, out float4 dataA, out float4 dataB)
{
    constexpr float div = 1.0f / 255.0f;

    // 提取第4列的打包数据
    int a = int(mat[0][3]); int b = int(mat[1][3]);
    int c = int(mat[2][3]); int d = int(mat[3][3]);

    // 解包为 [0..1] 范围
    dataA = float4(a & 0xFF, a >> 8, b & 0xFF, b >> 8) * div;
    dataB = float4(c & 0xFF, c >> 8, d & 0xFF, d >> 8) * div;

    // 清理矩阵
    mat[0][3] = mat[1][3] = mat[2][3] = 0.0f;
    mat[3][3] = 1.0f;

    return mat;
}

// 使用 (骨骼球体示例)
mat4 model_mat = extract_matrix_packed_data(inst_obmat, bone_color, state_color);
```

---

## 🎯 典型 Shader 剖析

### 案例: `overlay_edit_mesh_vert.glsl`

**完整流程分析**:

```glsl
// ===== 头部与包含 =====
#include "infos/overlay_edit_mode_infos.hh"
VERTEX_SHADER_CREATE_INFO(overlay_edit_mesh_vert)

#ifdef GLSL_CPP_STUBS
#  define VERT  // 调试时的宏定义
#endif

// 包含所有库函数
#include "draw_model_lib.glsl"
#include "draw_view_clipping_lib.glsl"
#include "draw_view_lib.glsl"
#include "overlay_common_lib.glsl"
#include "overlay_edit_mesh_common_lib.glsl"

// ===== 输入 =====
in vec3 pos;          // 顶点位置 (location=0)
in uint4 data;        // 编辑数据 (location=1)
in vec3 vnor;         // 法线 (location=2)
// ... 更多输入根据需要

// ===== 主函数 =====
void main()
{
    // ---- Step 1: 坐标变换链 ----
    // 对象空间 → 世界空间 → 视图空间 → 齐次裁剪空间
    float3 world_pos = drw_point_object_to_world(pos);
    float3 view_pos = drw_point_world_to_view(world_pos);
    gl_Position = drw_point_view_to_homogenous(view_pos);

    // ---- Step 2: 深度偏移 (Retopology) ----
    gl_Position.z += get_homogenous_z_offset(
        drw_view().winmat, view_pos.z, gl_Position.w, retopology_offset
    );

    // ---- Step 3: 数据解包 ----
    // data 是 uint4，使用掩码提取
    uint4 m_data = data & data_mask;

    // ---- Step 4: 条件编译 ----
    // 模式分支（通过 .define("VERT") / .define("EDGE") 等控制）

    #if defined(VERT)  // 顶点显示模式
        // 计算折痕 (高4位)
        vertex_crease = float(m_data.z >> 4) / 15.0f;

        // 计算顶点颜色
        final_color = EDIT_MESH_vertex_color(m_data.y, vertex_crease);

        // 点大小
        gl_PointSize = theme.sizes.vert *
                      ((vertex_crease > 0.0f) ? 3.0f : 2.0f);

        // 选中顶点置顶
        if ((data.x & VERT_SELECTED) != 0u) {
            gl_Position.z -= 5e-7f * abs(gl_Position.w);
        }

    #elif defined(EDGE)  // 边缘模式（几何着色器）
        final_color = EDIT_MESH_edge_vertex_color(m_data.y);
        // 注意：实际边缘在几何着色器中扩展为四边形

    #elif defined(FACE)  // 面模式
        final_color = EDIT_MESH_face_color(m_data.x);

    #elif defined(FACEDOT)  // 面点模式
        final_color = EDIT_MESH_facedot_color(m_data.y);
        gl_PointSize = theme.sizes.face_dot;
    #endif

    // ---- Step 5: 遮挡测试 ----
    #if defined(VERT) || defined(EDGE) || defined(FACEDOT)
        // 屏幕空间坐标
        float3 ndc = (gl_Position.xyz / gl_Position.w) * 0.5f + 0.5f;

        // TextureGather: 一次读取 2x2 邻域的 4 个深度值
        float4 depths = textureGather(depth_tx, ndc.xy);

        // 如果比周围都深 = 被遮挡
        bool occluded = all(greaterThan(vec4(ndc.z), depths));

        final_color.a *= (occluded) ? alpha : 1.0f;
    #endif

    // ---- Step 6: 面向混合 (Fresnel) ----
    #if !defined(FACE)
        // 视图方向（透视/正交自适应）
        float3 view_vec = (drw_view().winmat[3][3] == 0.0f) ?
                          normalize(view_pos) :
                          vec3(0.0, 0.0, 1.0);

        // 法线（视图空间）
        float3 view_normal = normalize(
            drw_normal_object_to_view(vnor) + 1e-4f
        );

        // 面向因子
        float facing = dot(view_vec, view_normal);
        facing = 1.0f - abs(facing) * 0.2f;

        // 非线性混合（伽马空间）
        final_color.rgb = mix(
            final_color.rgb,
            non_linear_blend_color(
                theme.colors.edit_mesh_middle.rgb,
                final_color.rgb,
                facing
            ),
            theme.fresnel_mix_edit
        );
    #endif

    // ---- Step 7: 裁剪平面 ----
    // 仅对点和边缘应用裁剪（面不需要）
    #if !defined(FACE)
        view_clipping_distances(world_pos);
    #endif
}
```

---

## ⚡ 性能优化要点

### 1. 异步编译
```cpp
// overlay_private.hh:564
void ensure_compile_async() {
    if (!compiled_) {
        GPU_shader_create_async(...);  // 不阻塞主线程
    }
}
```

### 2. 静态编译
```cpp
GPU_SHADER_CREATE_INFO(overlay_edit_mesh_vert)
    .do_static_compilation(true)  // 预编译优化
.end()
```

### 3. 顶点拉取 (Vertex Pulling)
```glsl
// 替代传统顶点属性，从 SSBO 读取
layout(std430, binding = 0) buffer PosBuf {
    float pos[];
};

// 使用 gl_VertexID 索引
void main() {
    uint idx = gl_VertexID;
    vec3 p = vec3(pos[idx*3], pos[idx*3+1], pos[idx*3+2]);
}
```

### 4. 高效深度测试
```glsl
// 传统: 4 次纹理采样
float d00 = texture(depth_tx, uv + vec2(-1,-1)/size).r;
float d01 = texture(depth_tx, uv + vec2(-1, 1)/size).r;
float d10 = texture(depth_tx, uv + vec2( 1,-1)/size).r;
float d11 = texture(depth_tx, uv + vec2( 1, 1)/size).r;

// 优化: 一次 textureGather 指令
float4 depths = textureGather(depth_tx, uv);
// 性能提升: 减少 75% 的纹理访问
```

---

## 🔍 常见问题排查

### 问题 1: Shader 不工作

**检查清单**:
1. ✅ 是否包含信息文件: `#include "infos/...hh"`
2. ✅ 库是否添加到 `.additional_info()`
3. ✅ 变体宏是否正确定义 (`.define("VERT")`)
4. ✅ Uniform 是否在 C++ 中绑定

**调试代码**:
```cpp
// 1. 打印实际使用的 shader 名称
std::cout << "Using: " << module.my_shader.name() << std::endl;
// 输出: "overlay_edit_mesh_vert_clipped"

// 2. 查看编译错误
if (!shader.compile_ok()) {
    std::cerr << shader.get_error_log() << std::endl;
}
```

### 问题 2: 深度冲突 (Z-fighting)

**原因**: 常数偏移在透视投影下不一致

**解决方案**:
```glsl
// ❌ 错误
gl_Position.z -= 0.001;

// ✅ 正确
gl_Position.z += get_homogenous_z_offset(...);
```

### 问题 3: 变体不生效

**原因**: 宏定义顺序问题

**排查**:
```glsl
// 在 shader 中添加调试
#ifdef VERT
#  error "VERT is defined"
#endif
```

---

## 📚 学习路径图

### 阶段 1: 基础语法 (1-2 天)
- **阅读**: 文档 1 (GLSL 语法)
- **实践**: 理解 `vec3`, `mat4`, `uniform`
- **目标**: 能看懂基本 shader 结构

### 阶段 2: 架构理解 (1 天)
- **阅读**: 文档 2 (架构概览)
- **实践**: 浏览 118 个文件，建立分类认知
- **目标**: 知道文件作用和位置

### 阶段 3: Blender 特性 (2 天)
- **阅读**: 文档 4 (Blender 语法扩展)
- **实践**: 读懂 `GPU_SHADER_CREATE_INFO` 配置
- **目标**: 理解宏系统和库包含

### 阶段 4: 数据流向 (2-3 天)
- **阅读**: 文档 3 (C++ 调用机制)
- **实践**: 调试 `overlay_instance.cc` 的流程
- **目标**: 理解 C++ → GLSL 的完整数据链

### 阶段 5: 库函数掌握 (2 天)
- **阅读**: 文档 5 (核心库)
- **查阅**: 遇到不懂的函数就查表
- **目标**: 掌握 20+ 常用库函数

### 阶段 6: 实战分析 (3 天)
- **阅读**: 文档 6 (Shader 案例)
- **实践**: 逐行分析 `overlay_edit_mesh_vert.glsl`
- **目标**: 能读懂并修改复杂 shader

### 阶段 7: 对比优化 (1-2 天)
- **阅读**: 文档 7 (对比标准 GLSL)
- **思考**: 为什么要这样设计
- **目标**: 理解设计权衡

---

## 🎓 关键概念记忆点

### Shader 变体系统

```
base shader: overlay_edit_mesh_vert
==========================================
define("VERT")   → overlay_edit_mesh_vert
define("EDGE")   → overlay_edit_mesh_edge
define("FACE")   → overlay_edit_mesh_face
define("FACEDOT")→ overlay_edit_mesh_facedot

变体扩展（自动）:
- _clipped      : 添加裁剪支持
- _selectable   : 添加选择ID
- _combined     : 同时启用多个
```

### 坐标变换链

```
局部空间 (pos)
    ↓ drw_point_object_to_world()
世界空间 (world_pos)
    ↓ drw_point_world_to_view()
视图空间 (view_pos)
    ↓ drw_point_view_to_homogenous()
齐次裁剪空间 (gl_Position)
    ↓ 透视除法
NDC 空间 [-1,1]
    ↓ 映射
屏幕空间 [0,1]
```

### 内存布局

```
UBO ViewMatrices (128 bytes alignment)
├── viewmat (64 bytes)    // World → View
├── winmat (64 bytes)     // View → Clip
├── viewinv (64 bytes)    // View → World (逆)
├── wininv (64 bytes)     // Clip → View (逆)
├── modelmat (64 bytes)   // Local → World
├── modelinv (64 bytes)   // World → Local
├── normal_mat (64 bytes) // 法线变换
├── clipplanes[6] (96 bytes)
└── count (4 bytes)
```

---

## 💡 实用技巧速查

### 快速测试 Shader 修改

1. **修改 GLSL 文件**
   ```bash
   # 编辑:
   source/blender/draw/engines/overlay/shaders/overlay_edit_mesh_vert.glsl
   ```

2. **重新编译 Blender**
   ```bash
   make -j8
   ```

3. **在 Blender 中测试**
   - 打开编辑模式
   - 选择/取消选择顶点
   - 观察颜色/大小变化

### 调试技巧

**打印生成的最终代码**:
```cpp
// 在 overlay_shader.cc 中添加
GPU_shader_print_source(shader);
```

**启用 OpenGL 调试**:
```cpp
glEnable(GL_DEBUG_OUTPUT);
glDebugMessageCallback(...);
```

**使用 RenderDoc**:
- 捕获帧
- 查看 OpenGL 调用
- 检查 shader 状态

---

## 📦 附录：关键文件清单

### C++ 核心文件
```
source/blender/draw/engines/overlay/
├── overlay_private.hh          # ShaderModule 定义
├── overlay_shader.cc           # 编译 + 变体
├── overlay_instance.cc         # 渲染实例
├── overlay_resource.cc         # 资源管理
├── overlay_pass.cc             # 渲染流程
└── overlay_*_pass.cc         # 具体 pass
```

### GLSL 配置文件
```
source/blender/draw/engines/overlay/shaders/infos/
├── overlay_edit_mode_infos.hh    # 编辑模式配置
├── overlay_armature_infos.hh     # 骨骼配置
├── overlay_curve_infos.hh        # 曲线配置
├── overlay_lattice_infos.hh      # 晶格配置
└── overlay_*_infos.hh          # 其他配置
```

### 最重要的 GLSL 文件
```
source/blender/draw/engines/overlay/shaders/
├── overlay_edit_mesh_vert.glsl          # 必读！最典型
├── overlay_edit_mesh_edge_vert.glsl     # 几何着色器
├── overlay_armature_sphere_solid_vert.glsl  # 实例+光线求交
├── overlay_common_lib.glsl              # 通用工具
├── overlay_edit_mesh_common_lib.glsl    # 网格编辑专用
└── overlay_*_lib.glsl                 # 其他库

source/blender/draw/intern/shaders/
├── draw_view_lib.glsl             # 视图变换（最常用）
├── draw_model_lib.glsl            # 模型矩阵
├── draw_math_geom_lib.glsl        # 几何数学
└── gpu_shader_math_vector_lib.glsl  # 向量运算
```

---

## 🎯 7天学习计划

### Day 1: 文档 1 + 2 (2-3小时)
- ✅ GLSL 基础语法
- ✅ 浏览 118 个文件目录
- ✅ 找到 10 个关键文件位置

### Day 2: 文档 4 (2小时)
- ✅ `GPU_SHADER_CREATE_INFO` 语法
- ✅ 库包含系统
- ✅ 条件编译宏
- **练习**: 读懂 5 个 shader 配置

### Day 3: 文档 3 (3小时)
- ✅ ShaderModule 类结构
- ✅ 变体生成逻辑
- ✅ C++ → GLSL 数据流
- **实践**: 调试查看一个 shader 完整名称

### Day 4: 文档 5 (2小时)
- ✅ 核心库函数速查
- ✅ 练习 10 个常用函数
- **实践**: 理解 `drw_view()` 返回值结构

### Day 5-6: 文档 6 (4小时)
- ✅ 剖析 `overlay_edit_mesh_vert.glsl`
- ✅ 理解边缘几何着色器
- ✅ 骨骼球体光线求交
- **实践**: 在 shader 中添加调试颜色

### Day 7: 文档 7 + 实践 (2小时)
- ✅ 标准 vs Blender 对比
- ✅ 完成一个小修改（改颜色/大小）
- **目标**: 看到修改效果

---

## 🚀 扩展方向

### 1. 添加新 Shader
```cpp
// 1. 创建配置
GPU_SHADER_CREATE_INFO(my_custom_shader)
    .vertex_in(0, float3, pos)
    .vertex_source("my_vert.glsl")
    .fragment_source("my_frag.glsl")
    .additional_info("draw_view")
.end()

// 2. 在 C++ 中使用
ShaderModule& module = ShaderModule::module_get(...);
StaticShader shader = module.my_custom_shader;
```

### 2. 扩展库函数
```glsl
// 在 overlay_common_lib.glsl 添加
SHADER_LIBRARY_CREATE_INFO(my_lib)

float3 my_custom_function(float3 p) {
    return p * 2.0;
}
```

### 3. 性能调优
- 减少条件分支
- 使用 `textureGather`
- 静态编译预热
- 异步加载

---

## 📖 快速参考表

| 概念 | 关键文件 | 核心函数/宏 |
|------|----------|-------------|
| **变体系统** | `overlay_shader.cc` | `CREATE_INFO_VARIANT()` |
| **装配系统** | `*_infos.hh` | `GPU_SHADER_CREATE_INFO()` |
| **坐标变换** | `draw_view_lib.glsl` | `drw_point_object_to_world()` |
| **深度偏移** | `overlay_common_lib.glsl` | `get_homogenous_z_offset()` |
| **颜色计算** | `overlay_edit_mesh_common_lib.glsl` | `EDIT_MESH_vertex_color()` |
| **遮挡测试** | `overlay_edit_mesh_vert.glsl` | `textureGather()` |
| **实例渲染** | `overlay_armature_*.glsl` | `gl_InstanceID` |
| **顶点拉取** | `overlay_edit_mesh_edge_vert.glsl` | `layout(std430, binding=0)` |
| **几何着色器** | `_edge_vert.glsl` | `EmitVertex()` |
| **光线求交** | `_sphere_solid_vert.glsl` | `line_unit_sphere_intersect_dist()` |

---

## ✅ 完成标准

完成全部学习后，你应该能够：

### 🟢 基础能力
- [ ] 独立编写简单的 GLSL 顶点/片段着色器
- [ ] 看懂 `GPU_SHADER_CREATE_INFO` 配置的每个字段
- [ ] 查阅并使用 5 个以上库函数

### 🟡 进阶能力
- [ ] 理解 `gl_Position = ...;` 完整计算链
- [ ] 在现有 shader 中添加自定义逻辑
- [ ] 调试并修复 shader 编译错误
- [ ] 解释 `overlay_edit_mesh_vert.glsl` 的每个步骤

### 🔴 高级能力
- [ ] 为 Blender 添加新的 overlay 着色器
- [ ] 扩展库函数并集成到系统
- [ ] 分析并优化 shader 性能瓶颈
- [ ] 解释为什么 Blender 使用这种架构

---

## 📝 重要提示

### 学习建议
1. **不要死记硬背**：理解设计原理比记忆重要
2. **对照源码**：边看文档边打开实际文件
3. **小步修改**：每次只改一点，测试效果
4. **善用调试**：Print、RenderDoc、断点都是好朋友

### 关键文件地址

**源码位置**:
```
E:\blender-git\blender\source\blender\draw\engines\overlay\
```

**文档位置**:
```
E:\blender-git\blender\docs\
├── 01_glsl_syntax_detailed.md
├── 02_overlay_glsl_overview.md
├── 03_overlay_cpp_glsl_integration.md
├── 04_glsl_basics_and_blender_syntax.md
├── 05_overlay_core_libraries.md
├── 06_overlay_shader_examples.md
├── 07_blender_glsl_vs_standard_glsl.md
└── README_GLSL学习指南.md
```

---

## 🎉 总结

Blender Overlay GLSL 系统是一个**高度工程化**的渲染架构：

**核心思想**:
- **配置即代码**：C++ 配置自动生成 GLSL
- **分层设计**：库系统避免重复
- **变体管理**：单文件多用途
- **数据极致优化**：矩阵打包、顶点拉取

**学习曲线**:
- **前 20%**：理解了核心概念，能看懂 80% 代码
- **中 60%**：掌握库函数和 pattern，能做修改
- **后 20%**：精通优化和扩展，能创造新功能

**建议投入**：
- **总时长**：7-14 天系统学习
- **每日**：2-3 小时 + 实践
- **难点**：文档 3 (C++ 集成) 和 6 (实战案例)

---

**祝你学习顺利！** 🚀

> 参考文档：
> - 完整详细版请阅读上述 7 个详细文档
> - 快速查阅使用本总结 + 函数索引表
> - 实践遇到问题时返回文档 4 和 7

---
**文档生成时间**: 2025-12-17
**Blender 版本**: 4.3+
**文档状态**: v1.0
