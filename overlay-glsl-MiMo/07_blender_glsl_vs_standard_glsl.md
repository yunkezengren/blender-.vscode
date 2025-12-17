# Blender GLSL 与标准 GLSL 全面对比

## 目录
- [1. 概述：核心差异](#1-概述核心差异)
- [2. 着色器定义与配置](#2-着色器定义与配置)
  - [2.1. 纯 GLSL 定义方式](#21-纯-glsl-定义方式)
  - [2.2. Blender GLSL 定义方式](#22-blender-glsl-定义方式)
- [3. 资源绑定系统](#3-资源绑定系统)
  - [3.1. Uniform 管理](#31-uniform-管理)
  - [3.2. 纹理绑定](#32-纹理绑定)
  - [3.3. UBO 对比](#33-ubo-对比)
- [4. 库文件系统](#4-库文件系统)
  - [4.1. 标准 GLSL 库](#41-标准-glsl-库)
  - [4.2. Blender 库系统](#42-blender-库系统)
- [5. 高级特性对比](#5-高级特性对比)
  - [5.1. 变体与条件编译](#51-变体与条件编译)
  - [5.2. 顶点数据输入](#52-顶点数据输入)
  - [5.3. 深度处理](#53-深度处理)
- [6. 语法细节差异](#6-语法细节差异)
  - [6.1. 类型定义](#61-类型定义)
  - [6.2. 内置函数](#62-内置函数)
  - [6.3. 预处理指令](#63-预处理指令)
- [7. 工作流程对比](#7-工作流程对比)
  - [7.1. 开发流程](#71-开发流程)
  - [7.2. 调试流程](#72-调试流程)
  - [7.3. 性能调优](#73-性能调优)
- [8. 互操作性](#8-互操作性)
  - [8.1. Blender GLSL 改写为标准 GLSL](#81-blender-glsl-改写为标准-glsl)
  - [8.2. 标准 GLSL 改写为 Blender GLSL](#82-标准-glsl-改写为-blender-glsl)
- [9. 最佳实践与陷阱](#9-最佳实践与陷阱)

---

## 1. 概述：核心差异

### 核心理念对比

| 特性 | **标准 GLSL** | **Blender GLSL** |
|------|--------------|------------------|
| **设计目标** | 通用图形编程 | 特定于 Blender 渲染管线 |
| **配置方式** | 手写代码或简单脚本 | 程序化配置系统 |
| **资源绑定** | 手动绑定 | 自动生成 + 声明式 |
| **代码复用** | #include（文件级） | 库系统（语义级） |
| **变体管理** | 手写多个文件 | 自动 + 宏系统 |
| **维护难度** | 低（小项目） | 高（大项目可维护）|

### 基本结构差异

```glsl
// ===== 标准 GLSL =====
#version 460 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 ModelMatrix;
uniform mat4 ViewMatrix;
uniform mat4 ProjectionMatrix;
uniform vec3 LightPos;

out vec3 vNormal;

void main() {
    vec4 worldPos = ModelMatrix * vec4(position, 1.0);
    vec4 viewPos = ViewMatrix * worldPos;
    gl_Position = ProjectionMatrix * viewPos;
    vNormal = mat3(ModelMatrix) * normal;
}

// ===== Blender GLSL =====
#include "infos/my_shader_infos.hh"
VERTEX_SHADER_CREATE_INFO(my_shader)

#include "draw_view_lib.glsl"

void main() {
    // 自动获取 ModelMatrix 等变换
    vec3 worldPos = drw_point_object_to_world(position);
    vec3 viewPos = drw_point_world_to_view(worldPos);
    gl_Position = drw_point_view_to_homogenous(viewPos);

    vNormal = drw_normal_object_to_view(normal);
}
```

---

## 2. 着色器定义与配置

### 2.1. 纯 GLSL 定义方式

#### **编译与运行**

```cpp
// C++ 传统方式
const char* vertSource = R"(
    #version 460 core
    layout(location=0) in vec3 pos;
    uniform mat4 MVP;
    void main() { gl_Position = MVP * vec4(pos, 1.0); }
)";

const char* fragSource = R"(
    #version 460 core
    out vec4 color;
    void main() { color = vec4(1.0); }
)";

// 编译
GLuint program = glCreateProgram();
GLuint vs = glCreateShader(GL_VERTEX_SHADER);
glShaderSource(vs, 1, &vertSource, NULL);
glCompileShader(vs);
// 错误检查...
glAttachShader(program, vs);
glLinkProgram(program);

// 使用
glUseProgram(program);
glUniformMatrix4fv(mvpLoc, 1, GL_FALSE, mvp);
glDrawArrays(GL_TRIANGLES, 0, 3);
```

**问题**：
- 字符串硬编码
- 无类型检查
- 需要手动管理错误
- 无集中配置

#### **配置文件方式**

```glsl
// my_shader.glsl
uniform mat4 MVP;
uniform vec3 diffuseColor;

void main() {
    // ...
}

// C++ 读取文件
std::string source = readFile("my_shader.glsl");
```

### 2.2. Blender GLSL 定义方式

#### **三层系统**

```
C++ 配置 (.hh 文件)
    ↓ 生成
GLSL 源码 + 宏处理
    ↓ 编译
GPU 程序
```

#### **配置层（C++）**

```cpp
// my_shader_infos.hh

// 1. 接口定义（可选）
GPU_SHADER_INTERFACE_INFO(my_iface)
    .smooth(vec4, color)
.end()

// 2. 库定义（可选）
GPU_SHADER_LIBRARY_CREATE_INFO(my_lib)
    .sampler(0, sampler2D, tex)
    .push_constant(float, time)
.end()

// 3. 着色器定义
GPU_SHADER_CREATE_INFO(my_shader)
    .do_static_compilation(true)        // 预编译
    .vertex_in(0, float3, position)     // 输入布局
    .vertex_in(1, vec3, normal)
    .vertex_out(my_iface)               // 输出接口
    .vertex_source("my_vert.glsl")      // 源文件
    .fragment_source("my_frag.glsl")
    .additional_info("my_lib")          // 库继承
    .additional_info("draw_view")       // 标准库
.end()

// 4. 变体定义
CREATE_INFO_VARIANT(my_shader_selectable,
                    my_shader,
                    drw_selectable)
```

#### **GLSL 层**

```glsl
// my_vert.glsl
void main() {
    // 使用库函数
    vec3 worldPos = drw_point_object_to_world(position);

    // 预处理宏自动注入
    // .additional_info("draw_view") → 自动生成 drw_view()

    gl_Position = ...
}
```

#### **使用层（C++）**

```cpp
// ShaderModule 通过配置查找实际着色器
ShaderModule& module = ShaderModule::module_get(
    SelectionType::ENABLED,  // 自动生成 "my_shader_selectable"
    true
);

StaticShader shader = module.my_shader;  // 返回可选版本

// 绘制
pass.shader_set(shader.get());
pass.draw(geom);
```

---

## 3. 资源绑定系统对比

### 3.1. Uniform 管理

#### **标准 GLSL：手动绑定**

```glsl
// GLSL 声明
uniform mat4 ModelMatrix;
uniform mat4 ViewMatrix;
uniform mat4 ProjectionMatrix;
uniform vec3 LightPosition[8];
uniform float Time;
```

```cpp
// C++ 绑定（每帧）
glUseProgram(program);

// 每个 uniform 都要单独绑定
glUniformMatrix4fv(glGetUniformLocation(program, "ModelMatrix"),
                   1, GL_FALSE, &model[0][0]);
glUniformMatrix4fv(glGetUniformLocation(program, "ViewMatrix"),
                   1, GL_FALSE, &view[0][0]);
glUniformMatrix4fv(glGetUniformLocation(program, "ProjectionMatrix"),
                   1, GL_FALSE, &proj[0][0]);

// 数组绑定
for (int i = 0; i < 8; ++i) {
    std::string name = "LightPosition[" + std::to_string(i) + "]";
    int loc = glGetUniformLocation(program, name.c_str());
    glUniform3fv(loc, 1, &lights[i].pos[0]);
}

glUniform1f(glGetUniformLocation(program, "Time"), time);
```

**缺点**：
- 权重高：每个 bind 都需要字符串查找（慢）
- 易出错：拼写错误不易发现
- 冗长：大量重复代码

#### **Blender GLSL: UBO + 自动绑定**

```glsl
// 1. 定义 UBO 结构（.hh 文件）
GPU_SHADER_CREATE_INFO(my_info)
    .uniform_block(0, "MyUBO", "my_ubo")
.end()

// 2. GLSL 自动获得
layout(std140, binding = 0) uniform MyUBO {
    mat4 ModelMatrix;
    mat4 ViewMatrix;
    mat4 ProjectionMatrix;
    vec3 LightPosition[8];
    float Time;
} my_ubo;

// 3. 使用
void main() {
    vec3 pos = (my_ubo.ModelMatrix * vec4(position, 1.0)).xyz;
}
```

```cpp
// C++：只需一次绑定，一次上传
struct MyUBO {
    Matrix4 model, view, proj;
    Vector3 lights[8];
    float time;
};

draw::UniformBuffer<MyUBO> ubo;

void update() {
    ubo.cpu_data.model = current_model;
    ubo.cpu_data.view = current_view;
    ubo.cpu_data.lights = lights;

    ubo.push_update();  // 一次上传到 GPU
}

void render() {
    // 只需绑定 UBO 到槽位 0
    pass.bind_ubo(0, &ubo);
}
```

**优势**：
- 状态切换快：一次绑定
- 数据紧凑：GPU 可以批量读取
- 表达力强：结构体清晰

### 3.2. 纹理绑定

#### **标准 GLSL：手动单元格绑定**

```cpp
// 绑定纹理到采样器
glActiveTexture(GL_TEXTURE0);
glBindTexture(GL_TEXTURE_2D, texture1_id);
glUniform1i(glGetUniformLocation(program, "tex1"), 0);

glActiveTexture(GL_TEXTURE1);
glBindTexture(GL_TEXTURE_2D, texture2_id);
glUniform1i(glGetUniformLocation(program, "tex2"), 1);

// 同时还要绑定采样器对象
glBindSampler(0, sampler1_id);
glBindSampler(1, sampler2_id);
```

#### **Blender GLSL：声明式绑定**

```cpp
// C++ 配置
GPU_SHADER_CREATE_INFO(my_info)
    .sampler(0, sampler2D, diffuseTex)
    .sampler(1, sampler2D, normalTex)
    .sampler(2, sampler2D, shadowTex)
.end()

// C++ 使用
pass.bind_texture("diffuseTex", res.diffuse_tx);
pass.bind_texture("normalTex", res.normal_tx);
// pass 内部自动计算 slot 和绑定
```

```glsl
// GLSL 自动获得（无需手动声明 location）
uniform sampler2D diffuseTex;
uniform sampler2D normalTex;

void main() {
    vec4 diff = texture(diffuseTex, uv);
    vec3 norm = texture(normalTex, uv).xyz;
}
```

### 3.3. 推送常量 vs 统一变量

#### **标准 GLSL：弃用 uniform**

```glsl
uniform float alpha;
uniform int flags;
```

```cpp
glUniform1f(alpha_loc, alpha);
glUniform1i(flags_loc, flags);
// 每次都要查询 loc（或缓存）
```

#### **Blender GLSL：Push Constants**

```cpp
// .hh 配置
PUSH_CONSTANT(float, alpha)
PUSH_CONSTANT(int, flags)

// C++
pass.push_constant("alpha", 0.5f);
pass.push_constant("flags", 0b101);
```

**Push Constants 优点**：
- 快速更新：不需要缓冲区绑定
- 使用场景：每绘制调用不同的小数据
- 大小限制：通常 128 字节

---

## 4. 库文件系统对比

### 4.1. 标准 GLSL 库

#### **实现方式**

```glsl
// common_math.glsl
#pragma once

vec3 saturate(vec3 x) {
    return clamp(x, 0.0, 1.0);
}

float sq(float x) {
    return x * x;
}
```

```glsl
// my_shader.glsl
#version 460 core

#include "common_math.glsl"

void main() {
    vec3 clamped = saturate(color);
    float dist_sq = sq(length(pos));
}
```

**特点**：
- 简单直接
- 文件路径管理
- 无语义信息

#### **局限性**
- 没有配置上下文
- 无法根据平台优化
- 无法知道库的依赖关系
- 不能自动处理输入输出

### 4.2. Blender 库系统

#### **三层结构**

**第一层：基础库（系统级）**
```glsl
// draw_view_lib.glsl
#pragma once
#include "draw_view_infos.hh"
SHADER_LIBRARY_CREATE_INFO(draw_view)

// 检查配置
#if !defined(DRAW_VIEW_CREATE_INFO) && !defined(GLSL_CPP_STUBS)
#  error Missing draw_view additional create info
#endif

// 函数定义
ViewMatrices drw_view() {
    return drw_view_buf[drw_view_id];
}

float3 drw_point_object_to_world(float3 P) {
    return (drw_view().modelmat * vec4(P, 1.0)).xyz;
}
```

```cpp
// C++ 配置
GPU_SHADER_LIBRARY_CREATE_INFO(draw_view)
    .uniform_block(0, "ViewMatrices", "drw_view_buf")
    .push_constant(int, "drw_view_id")
.end()
```

**第二层：功能库（应用级）**
```glsl
// overlay_common_lib.glsl
#pragma once
#include "draw_view_lib.glsl"

SHADER_LIBRARY_CREATE_INFO(overlay_edit_mesh_common)

// 依赖 overlay_edit_mesh_common 中的 theme 变量
float4 EDIT_MESH_vertex_color(uint vertex_flag, float crease) {
    if ((vertex_flag & VERT_ACTIVE) != 0u) {
        return theme.colors.edit_mesh_active;
    }
    // ...
}
```

**第三层：应用**
```glsl
// overlay_edit_mesh_vert.glsl
#include "infos/overlay_edit_mode_infos.hh"
VERTEX_SHADER_CREATE_INFO(overlay_edit_mesh_vert)

#include "overlay_common_lib.glsl"
#include "draw_view_lib.glsl"

void main() {
    vec3 pos = drw_point_object_to_world(position);
    vec4 color = EDIT_MESH_vertex_color(data.x, crease);
}
```

#### **Blender 库的优势**

| 特点 | 价值 |
|-----|------|
| **显式依赖** | `.additional_info()` 明确声明依赖 |
| **配置注入** | 库可以要求特定的 UBO/Constant |
| **错误检测** | 缺少依赖时在编译时报错 |
| **语义组** | 不是简单的文件包含，是有意义的逻辑组 |

---

## 5. 高级特性对比

### 5.1. 变体与条件编译

#### **标准方式：手写多个文件**

```glsl
// shader_v.glsl - 顶点模式
void main() {
    gl_PointSize = 5.0;
}

// shader_e.glsl - 边缘模式
void main() {
    // 复杂的边缘逻辑
}

// shader_f.glsl - 面模式
void main() {
    // 面填充逻辑
}
```

**问题**：
- 大量重复代码（坐标变换等）
- 同步困难
- 版本混乱

#### **Blender 方式：宏 + 配置**

```glsl
// one_file_for_all.glsl
void main() {
    // 坐标变换（所有模式共享）
    vec3 worldPos = drw_point_object_to_world(pos);
    gl_Position = drw_point_view_to_homogenous(worldPos);

    // 模式分支
    #if defined(VERT)
        gl_PointSize = theme.sizes.vert;
        final_color = EDIT_MESH_vertex_color(...);
    #elif defined(EDGE)
        final_color = EDIT_MESH_edge_color(...);
    #elif defined(FACE)
        final_color = EDIT_MESH_face_color(...);
    #endif
}
```

```cpp
// C++ 控制变体
GPU_SHADER_CREATE_INFO(overlay_edit_mesh_vert)
    .define("VERT")
    .vertex_source("one_file_for_all.glsl")
.end()

GPU_SHADER_CREATE_INFO(overlay_edit_mesh_edge)
    .define("EDGE")
    .vertex_source("one_file_for_all.glsl")
    .geometry_source("edge_expand.glsl")  // 额外组件
.end()
```

**变体倍数**：
```
Base: VERT, EDGE, FACE, FACEDOT (4)
+ Clipping: 名称后缀 "_clipped" (+4)
+ Selection: 名称后缀 "_selectable" (+8)

最长可生成 8 种变体。
```

### 5.2. 顶点数据输入

#### **标准 GLSL：顶点属性**

```glsl
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 uv;
layout(location = 3) in vec4 color;
```

```cpp
// VAO 布局
glBindVertexArray(vao);
glEnableVertexAttribArray(0);
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, offset);
// ... 每个属性都要设置
```

**限制**：
- 最多 16 个顶点属性（OpenGL 限制）
- 数据必须打包到 VBO

#### **Blender：顶点拉取**

```glsl
// GLSL：直接从 SSBO 读取
layout(std430, binding = 0) buffer PosBuf {
    float pos[];
};

void main() {
    uint idx = gl_VertexID;
    vec3 p = vec3(
        pos[idx * 3 + 0],
        pos[idx * 3 + 1],
        pos[idx * 3 + 2]
    );
}
```

```cpp
// C++：任意格式数据
StorageVectorBuffer<float> pos_buf;
pos_buf.push_update();

pass.bind_ssbo("PosBuf", &pos_buf);
```

**优势**：
- 无限属性数量
- 数据格式自由
- 支持压缩存储

### 5.3. 深度处理

#### **标准 GLSL：基础深度**

```glsl
// 经典深度测试
void main() {
    // Z-fighting 手动处理
    gl_Position.z -= 0.001;
    // 或
    gl_FragDepth = custom_depth;
}
```

#### **Blender：深度库 + 精确计算**

```glsl
// 1. Homogenous 偏移（解决所有投影类型）
#include "overlay_common_lib.glsl"
gl_Position.z += get_homogenous_z_offset(
    drw_view().winmat,
    view_pos.z,
    gl_Position.w,
    retopology_offset
);

// 2. 透视除法控制深度
void main() {
    vec3 world = drw_point_object_to_world(pos);
    vec3 view = drw_point_world_to_view(world);

    // 深度测试
    if (test_occlusion()) {
        final_color.a *= 0.5;
    }
}

// 3. 高级深度信息获取
float near_plane = drw_view_near();
float far_plane = drw_view_far();
bool is_perspective = drw_view_is_perspective();
```

---

## 6. 语法细节差异

### 6.1. 类型定义

#### **额外的类型系统**

```glsl
// Blender 专用类型
// 从 C++ 的 float3, vec4 翻译
// 实际上就是 vec3, vec4

// 但在 C++ 配置中这样声明
vertex_in(0, float3, pos)      // 映射到 layout(location=0) in vec3 pos
vertex_in(1, uint4, data)      // 映射到 layout(location=1) in uvec4 data
```

#### **结构体差异**

```glsl
// 标准 GLSL
struct Light {
    vec3 position;
    vec3 color;
    int type;
};

uniform Light lights[8];

// Blender（C++ 定义 → GLSL 自动）
struct Light {
    vec3 position;
    vec3 color;
    int type;
}

// C++ 配置
GPU_SHADER_CREATE_INFO(my_info)
    .uniform_block(0, "Light", "lights[8]")
.end()
```

### 6.2. 内置函数差异

#### **Blender 扩展库**

| 标准函数 | Blender 对应 | 说明 |
|---------|-------------|------|
| `mat4 * vec4` | `drw_point_object_to_world()` | 语义命名 |
| `texture()` | `textureGather()` | 更高效的邻域采样 |
| 自定义 | `encode_id_to_color()` | 选择系统 |

#### **矩阵解包（Blender 特供）**

```glsl
// C++ 优化：将数据打包进矩阵闲置区域
float4x4 extract_matrix_packed_data(float4x4 mat, out float4 dataA, out float4 dataB);

// 使用
mat4 transform = inst_obmat;
float4 infoA, infoB;
transform = extract_matrix_packed_data(transform, infoA, infoB);

// infoA、infoB 现在包含额外信息（颜色、权重等）
```

这种技巧无法直接在标准 GLSL 中实现。

### 6.3. 预处理指令

#### **Blender 宏系统**

```glsl
// 1. 条件编译（标准也有，但 Blender 机会更多）
#if defined(VERT) || defined(EDGE)
    // 共享代码
#endif

// 2. 信息检查
#ifndef DRAW_VIEW_CREATE_INFO
#  error "必须包含 draw_view 库"
#endif

// 3. 创建信息工具
// 由 C++ 源代码生成，GLSL 只是用
VERTEX_SHADER_CREATE_INFO(my_shader)
// 翻译为：#define VERTEX_SHADER_CREATE_INFO ...
// 经过预处理器后转发到 C++
```

#### **标准 GLSL 只有基本宏**

```glsl
// 标准
#define MAX_LIGHTS 8
#ifdef DEBUG
#  include "debug.glsl"
#endif

// Blender 额外
// .define("VERT") 生成 #define VERT
// 这样在 #if defined(VERT) 就能起作用
```

---

## 7. 工作流程对比

### 7.1. 开发流程

#### **标准 GLSL 开发**

1. **编写源代码**（单独的 .glsl 文件）
2. **在 C++ 中读取**：
   ```cpp
   std::string src = readFile("shader.glsl");
   const char* csrc = src.c_str();
   ```
3. **手动编译链接**：
   ```cpp
   glShaderSource(vs, 1, &glsl_str, NULL);
   glCompileShader(vs);
   glAttachShader(program, vs);
   glLinkProgram(program);
   ```
4. **错误处理**：
   ```cpp
   glGetShaderiv(vs, GL_COMPILE_STATUS, &status);
   if (!status) {
       glGetShaderInfoLog(vs, 1024, NULL, log);
       std::cerr << log << std::endl;
   }
   ```
5. **获取 uniform 位置**：
   ```cpp
   GLint mvp_loc = glGetUniformLocation(program, "MVP");
   ```
6. **运行时绑定**：
   ```cpp
   glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, &mvp[0][0]);
   ```

**耗时**：每个 shader 都需要 ~20-50 行 C++ 代码

#### **Blender GLSL 开发**

1. **编写配置**（在 .hh 文件中）：
   ```cpp
   GPU_SHADER_CREATE_INFO(my_shader)
       .vertex_source("my_vert.glsl")
       .fragment_source("my_frag.glsl")
   .end()
   ```

2. **编写 GLSL 源代码**：
   ```glsl
   #include "infos/my_shader_infos.hh"
   #include "draw_view_lib.glsl"

   void main() {
       vec3 pos = drw_point_object_to_world(input_pos);
   }
   ```

3. **使用（自动编译）**：
   ```cpp
   // ShaderModule 自动处理编译
   pass.shader_set(shaders->my_shader.get());
   ```

4. **错误信息**：
   ```
   Shader compile error for 'my_shader':
   ERROR: 0:12: 'drw_point_object_to_world' : undeclared identifier
   ```
   如果忘记包含库，系统会提示需要 `.additional_info()`

**耗时**：配置 5 行，GLSL 复用标准库函数

### 7.2. 调试流程

#### **标准 GLSL 调试**

```glsl
// 无专用调试语法
void main() {
    // 临时修改颜色调试
    fragColor = vec4(1,0,0,1);  // 为什么这里是红的？

    // 或使用
    if (some_condition) {
        // 插入断点（如果驱动支持）
        debugPrintfEXT("value = %f", some_var);
    }
}
```

```cpp
// 捕获 OpenGL 错误
GLenum err = glGetError();
if (err != GL_NO_ERROR) {
    // 查错误码及其含义
}
```

**困难**：
- 无法单步调试
- 错误位置不准确
- 只能肉眼观察输出

#### **Blender GLSL 调试**

```glsl
void main() {
    // 1. 检查宏是否正确应用
    #if defined(DEBUG)
        fragColor = vec4(1,0,0,1);
    #endif

    // 2. 使用 push_constant 调试
    uniform float debug_factor;
    fragColor.rgb *= debug_factor;  // C++ 动态调整查看效果

    // 3. 检查库函数结果
    vec3 world = drw_point_object_to_world(pos);
    // 临时:
    fragColor = vec4(world, 1.0); // 查看坐标

    // 4. 检查变体（打印实际使用的 shader 名称）
}
```

```cpp
// 调试 API
ShaderModule& module = ShaderModule::module_get(...);
std::cout << "Using shader: " << module.my_shader.name() << std::endl;
// 输出: "my_shader_vert_clipped"

// 调试实际编译的源代码


// GPU_shader_create_info 提供 debug 模式
gpu::shader->debug_print_source();
```

**优势**：
- 可以打印生成的最终代码
- 有配置检查系统
- 通过变体名称确认执行路径

### 7.3. 性能调优

#### **标准 GLSL 优化**

```glsl
// 1. 精度优化
lowp vec4 color;  // 尝试低精度

// 2. 避免分支
// 不好
if (useLight) { ... }
// 好
float factor = useLight * compute_light();

// 3. 预计算
void main() {
    static const mat4 precomputed = compute_expensive();
    // ...
}
```

```cpp
// C++ 侧优化
// 1. 状态排序
qsort(draw_calls, count, compare_shader_state);

// 2. 批次合并
glMultiDrawElements(...);

// 3. 纹理压缩
glCompressedTexImage2D(...);
```

#### **Blender GLSL 优化**

```glsl
// 1. 库级优化（使用 JIT）
// draw_view_lib 会根据场景优化计算

// 2. 变体最小化
// 只编译实际使用的变体

// 3. 异步编译
void Resources::init() {
    shaders->xxx.ensure_compile_async();  // 不阻塞主线程
}

// 4. 静态编译
GPU_SHADER_CREATE_INFO(my_info)
    .do_static_compilation(true)  // 预编译优化
.end()
```

```cpp
// C++ 端优化
// 1. 通过 ShaderModule 缓存
static StaticShaderCache cache;  // 跨帧复用

// 2. 按照状态排序
Pass::sort_by_depth_and_blend_state();

// 3. 实例化批处理
pass.draw(geom, instance_count);  // 自动实例化
```

**Blender 特有优化**：
- **缓存管理**：静态缓存自动保留
- **变体缓存**：只编译所需的变体组合
- **资源预热**：异步编译

---

## 8. 互操作性

### 8.1. 如何将 Blender GLSL 转换为标准 GLSL

#### **步骤 1: 分离依赖**

```
Blender:
  #include "draw_view_lib.glsl"
  void main() {
      vec3 wpos = drw_point_object_to_world(pos);
  }

转换后:
  uniform mat4 ModelMatrix;
  void main() {
      vec3 wpos = (ModelMatrix * vec4(pos, 1.0)).xyz;
  }
```

#### **步骤 2: 展开配置**

```cpp
// Blender 配置
GPU_SHADER_CREATE_INFO(my_shader)
    .push_constant(float, alpha)
    .sampler(1, sampler2D, tex)
.end()

// 展开为
uniform float alpha;  // 无 location，默认
uniform sampler2D tex;
// 在 C++ 中需要手动绑定位置
```

#### **步骤 3: 替换宏**

```glsl
// Blender
#ifdef EDGE
    // ...
#endif

// 展开为独立文件
// 或者定义宏并编译
#define EDGE
// 包含原文件
```

**转换工具**（理论上）：
```python
# 伪代码
def convert_blender_to_standard(blender_glsl, config):
    # 1. 解析 config
    uniforms = extract_uniforms(config)
    # 2. 替换库函数
    for lib in config.libs:
        src = inline_lib_function(src, lib)
    # 3. 展开宏
    src = evaluate_conditionals(src, config.defines)
    # 4. 添加 version 号
    src = "#version 460 core\n" + src
```

### 8.2. 如何将标准 GLSL 转换为 Blender GLSL

#### **步骤 1: 识别可复用部分**

```
原代码：
  vec4 vertex_color = vec4(1,0,0,1);
  gl_Position = MVP * vec4(pos,1);

转换：
  #include "overlay_common_lib.glsl"
  vec4 vertex_color = theme.colors.vertex;  // 使用主题
  gl_Position = drw_point_world_to_homogenous(pos);  // 使用库
```

#### **步骤 2: 创建库函数**

```glsl
// 识别通用函数
void calculatePhong(vec3 N, vec3 L, vec3 V) {
    // ...
}

// 移动到库
// my_lighting_lib.glsl
#pragma once
#include "infos/my_lighting_info.hh"
SHADER_LIBRARY_CREATE_INFO(my_lighting)

float3 compute_lighting(...) {
    // ...
}
```

#### **步骤 3: 创建配置**

```cpp
// my_shader_infos.hh

GPU_SHADER_CREATE_INFO(my_material)
    .vertex_in(0, float3, position)
    .vertex_in(1, vec3, normal)
    .additional_info("draw_view")      // 标准变换
    .additional_info("draw_normal")    // 法线变换
    .additional_info("my_lighting")    // 自定义库
    .vertex_source("my_vert.glsl")
    .fragment_source("my_frag.glsl")
.end()
```

---

## 9. 最佳实践与陷阱

### 9.1. 标准 GLSL 的陷阱（在 Blender 中已解决）

| 陷阱 | Blender 解决方案 |
|------|-----------------|
| **忘记绑定 uniform** | Push Constant 或 UBO 自动绑定 |
| **字符串查找性能低** | 缓存已经绑定的 location |
| **精度错误** | 计算用高精度，存储用低精度 |
| **Z-fighting** | `get_homogenous_z_offset()` |
| **分支发散** | 静态分析 + 条件编译 |
| **顶点属性限制** | 顶点拉取（SSBO） |
| **库管理混乱** | 三层库系统 |

### 9.2. Blender GLSL 新手常见错误

```glsl
// ❌ 错误 1: 忘记包含库
void main() {
    vec3 pos = drw_point_object_to_world(input_pos);  // 编译错误！
}
// ✅ 正确
#include "draw_view_lib.glsl"

// ❌ 错误 2: Uniform 位置冲突
uniform float my_param;  // 可能与库冲突
// ✅ 正确
PUSH_CONSTANT(float, my_param)  // 或使用不同的 UBO 槽

// ❌ 错误 3: 不理解变体系统
// 在 C++ 中忘记调用 .define()
void main() {
    #ifdef DEBUG  // 不生效
// ✅ 正确：必须在配置中 .define("DEBUG")

// ❌ 错误 4: 宏拼写错误
#ifdef VRT  // 打错了
// ✅ 正确：在配置中检查生成的宏名

// ❌ 错误 5: 库版本不匹配
// shader 使用旧版库 API
// ✅ 正确：统一版本或在 .hh 中声明兼容层
```

### 9.3. 迁移指南

#### **从标准 GLSL 迁移到 Blender**

```diff
// 1. 输入定义
-layout(location = 0) in vec3 position;
+vertex_in(0, float3, position)

// 2. Uniform 管理
-uniform mat4 ModelMatrix;
-uniform mat4 ViewMatrix;
+// 使用库自动提供
+vec3 world = drw_point_object_to_world(pos);

// 3. 片段输出
-out vec4 fragColor;
+fragColor = ...  // 自动绑定

// 4. 库替换
-vec3 saturate(vec3 x) { return clamp(x, 0.0, 1.0); }
+// 使用 gpu_shader_math_vector_lib.glsl
+vec3 saturate(vec3 x) { return clamp(x, 0.0, 1.0); }
```

#### **从 Blender 迁移到标准**

```diff
// 1. 库展开
-#include "draw_view_lib.glsl"
-world = drw_point_object_to_world(pos);
+world = (ModelMatrix * vec4(pos, 1.0)).xyz;

// 2. 配置展开
-GPU_SHADER_CREATE_INFO(my_shader)
-    .push_constant(float, alpha)
+uniform float alpha;

// 3. 宏管理
-#if defined(DEBUG)
+#ifdef DEBUG
```

---

## 10. 总结：何时选择哪个？

### **标准 GLSL 适用场景**

✅ **小型项目**
- J 个 shader
- 不需要复杂的状态管理
- 直接控制 GPU

✅ **引擎开发**
- 构建自己的渲染管线
- 需要绝对灵活性
- 不受框架限制

✅ **学习目的**
- 学习 GLSL 基础
- 理解底层原理
- 无抽象层

### **Blender GLSL 适用场景**

✅ **复杂渲染系统**
- 100+ 个 shader
- 大量变体
- 状态自动管理

✅ **需要快速迭代**
- 库复用减少代码量
- 类型安全
- 错误提示友好

✅ **团队协作**
- 配置即文档
- 依赖明确
- 维护成本低

### **混合模式**

```cpp
// 在 Blender 中嵌入标准 GLSL()
GPU_SHADER_CREATE_INFO(embedded)
    .vertex_source_from_string(R"(
        // 标准 GLSL
        #version 460 core
        layout(location=0) in vec3 pos;
        void main() {
            gl_Position = vec4(pos, 1.0);
        }
    )")
.end()

// 在标准 GLSL 中模拟 Blender 库
// 实现自己的 drw_view() 函数
```

---

**最终建议**：

| 使用者 | 建议 |
|--------|------|
| **初学者** | 先学标准 GLSL，理解后再学 Blender 扩展 |
| **插件开发者** | 直接学 Blender GLSL，使用库函数 |
| **引擎开发者** | 理解 Blender 设计，借鉴其思想 |
| **Shader 美术师** | Blender GLSL 更友好，有文档支持 |

---

**文档版本**: 1.0
**基于**: Blender 4.3 + GLSL 4.60
**创建时间**: 2025-12-17
**分类**: 高级对比分析

---
**附录：快速参考表**

| 功能 | 标准 GLSL | Blender GLSL |
|------|----------|--------------|
| 版本声明 | `#version 460` | `#include "infos/...hh"` |
| Uniform | 手动绑定 | UBO/Auto |
| 库 | `#include` | 库系统 + 配置 |
| 变体 | 多文件 | 宏 + 配置 |
| 顶点数据 | 属性 | SSBO/拉取 |
| 深度偏移 | 常数值 | 函数计算 |
| 错误检查 | 手动 | 自动配置检查 |
| 调试 | 有限 | 完整支持 |
| 性能优化 | 手动 | 自动缓存 |
| 大型项目 | 困难 | 容易 |
