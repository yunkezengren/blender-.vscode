# GLSL 语法详解 - 从基础到高级

## 目录
- [1. GLSL 概述](#1-glsl-概述)
- [2. 数据类型](#2-数据类型)
  - [2.1. 基本数据类型](#21-基本数据类型)
  - [2.2. 向量类型](#22-向量类型)
  - [2.3. 矩阵类型](#23-矩阵类型)
  - [2.4. 采样器类型](#24-采样器类型)
- [3. 变量与限定符](#3-变量与限定符)
  - [3.1. 存储限定符](#31-存储限定符)
  - [3.2. 插值限定符](#32-插值限定符)
  - [3.3. 精度限定符](#33-精度限定符)
- [4. 函数定义与调用](#4-函数定义与调用)
  - [4.1. 函数语法](#41-函数语法)
  - [4.2. 参数传递模式](#42-参数传递模式)
- [5. 着色器阶段与内置变量](#5-着色器阶段与内置变量)
  - [5.1. 顶点着色器](#51-顶点着色器)
  - [5.2. 片段着色器](#52-片段着色器)
  - [5.3. 几何着色器](#53-几何着色器)
- [6. 预处理指令](#6-预处理指令)
  - [6.1. 条件编译](#61-条件编译)
  - [6.2. 宏定义](#62-宏定义)
  - [6.3. 文件包含](#63-文件包含)
- [7. 常用内建函数](#7-常用内建函数)
  - [7.1. 数学函数](#71-数学函数)
  - [7.2. 向量操作函数](#72-向量操作函数)
  - [7.3. 纹理采样函数](#73-纹理采样函数)
- [8. GLSL 与 Blender 的差异](#8-glsl-与-blender-的差异)
  - [8.1. 语法扩展](#81-语法扩展)
  - [8.2. 预处理宏](#82-预处理宏)

---

## 1. GLSL 概述

**GLSL** (OpenGL Shading Language) 是 OpenGL 的着色器语言，用于在 GPU 上执行并行计算。Blender 使用 GLSL 进行实时渲染和可视化。

### 核心特点
- **C 语言风格语法**：类似 C/C++ 的语法结构
- **类型安全**：强类型系统，需要显式类型转换
- **并行执行**：每个顶点或片段的处理都是独立的
- **硬件加速**：直接在 GPU 上运行

---

## 2. 数据类型

### 2.1. 基本数据类型

| 类型 | 描述 | 示例 | 大小 |
|------|------|------|------|
| `float` | 32 位浮点数 | `float x = 1.5;` | 4 字节 |
| `int` | 32 位有符号整数 | `int y = 42;` | 4 字节 |
| `uint` | 32 位无符号整数 | `uint z = 100u;` | 4 字节 |
| `bool` | 布尔值 | `bool flag = true;` | 1 字节 |

**注意**:
- 数值字面量默认是 `float` 类型，如 `1.0`
- 整数字面量需要后缀，如 `42`, `100u`
- 布尔值用于条件判断

### 2.2. 向量类型

GLSL 提供 2/3/4 分量向量类型：

```glsl
// 声明
vec2 v2 = vec2(1.0, 2.0);      // 2D 向量
vec3 v3 = vec3(1.0, 2.0, 3.0); // 3D 向量
vec4 v4 = vec4(1.0, 2.0, 3.0, 4.0); // 4D 向量

// 对应的整数和布尔向量
ivec2 iv2 = ivec2(1, 2);
bvec3 bv3 = bvec3(true, false, true);

// 也可以从其他向量构造
vec4 v4_from_v3 = vec4(v3, 1.0);  // v3 作为 xyz, 1.0 作为 w
vec3 v3_from_v4 = v4.xyz;           // 提取 xyz 分量
```

**分量访问**：
- `xy`, `xyz`, `xyzw` - 位置分量
- `rgba` - 颜色分量
- `st`, `stpq` - 纹理坐标分量

**示例**:
```glsl
vec4 color = vec4(1.0, 0.0, 0.0, 1.0); // RGBA: 红色不透明
color.rgb = vec3(0.0, 1.0, 0.0);       // 修改 RGB 为绿色
color.a = 0.5;                         // 修改 Alpha 为半透明
```

### 2.3. 矩阵类型

用于坐标变换：

```glsl
// 声明
mat2 m2 = mat2(1.0, 0.0, 0.0, 1.0);     // 2x2 矩阵
mat3 m3 = mat3(1.0);                    // 3x3 单位矩阵
mat4 m4 = mat4(1.0);                    // 4x4 单位矩阵

// 按列初始化
mat4 transform = mat4(
    1.0, 0.0, 0.0, 0.0,   // 第一列
    0.0, 1.0, 0.0, 0.0,   // 第二列
    0.0, 0.0, 1.0, 0.0,   // 第三列
    0.0, 0.0, 0.0, 1.0    // 第四列
);

// 访问矩阵元素（列主序）
float m42 = transform[3][1]; // 第 4 列，第 2 行的值

// 矩阵向量乘法
vec4 pos = transform * vec4(1.0, 2.0, 3.0, 1.0);
```

### 2.4. 采样器类型

用于纹理采样：

```glsl
// 2D 纹理采样器
uniform sampler2D depth_tx;        // 深度纹理
uniform sampler2D diffuse_texture; // 漫反射纹理

// 其他采样器类型
samplerCube  // 立方体贴图
sampler3D    // 3D 纹理
sampler1D    // 1D 纹理
```

**使用示例**:
```glsl
uniform sampler2D myTexture;
varying vec2 texCoord;

void main() {
    vec4 color = texture2D(myTexture, texCoord);
    gl_FragColor = color;
}
```

---

## 3. 变量与限定符

### 3.1. 存储限定符

| 限定符 | 描述 | 使用场景 |
|--------|------|----------|
| `const` | 常量，不可修改 | `const float PI = 3.14159;` |
| `uniform` | CPU 传入的统一变量 | 顶点/片段间共享 |
| `attribute` | 顶点属性（旧版） | 每个顶点的数据 |
| `varying` | 顶点到片段的传递变量 | 插值后的数据 |
| `in` / `out` | 着色器输入输出（GLSL 3.30+） | 替代 attribute/varying |
| `buffer` | SSBO (Shader Storage Buffer) | 大数据块读写 |

**uniform 示例**:
```glsl
uniform mat4 ModelViewMatrix;    // 变换矩阵
uniform vec3 LightPosition;      // 光源位置
uniform float Time;              // 时间
```

**in/out 示例** (现代 GLSL):
```glsl
// 顶点着色器
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
out vec3 vNormal;  // 传递到片段着色器

void main() {
    vNormal = normal;
    gl_Position = vec4(position, 1.0);
}

// 片段着色器
in vec3 vNormal;  // 从顶点着色器接收
out vec4 FragColor;

void main() {
    FragColor = vec4(vNormal, 1.0);
}
```

### 3.2. 插值限定符

控制变量在光栅化时的插值方式：

```glsl
// 平滑插值（默认）
smoothout vec3 colorSmooth;

// 平面插值（不插值，使用图元的值）
flat out vec3 colorFlat;

// 透视校正插值
noperspective out vec3 colorNoPerspective;
```

### 3.3. 精度限定符

指定数值精度，影响性能和准确性：

```glsl
// 高精度（32 位浮点）
highp vec3 position;    // 用于顶点坐标
highp mat4 transform;   // 用于矩阵

// 中等精度（16-32位浮点）
mediump vec3 normal;    // 用于法线
mediump float factor;   // 用于系数

// 低精度（8-16位浮点）
lowp vec3 color;        // 用于颜色
lowp float alpha;       // 用于透明度
```

**全局默认设置**:
```glsl
precision highp float;    // 指定 float 默认高精度
precision mediump int;    // 指定 int 默认中精度
```

---

## 4. 函数定义与调用

### 4.1. 函数语法

```glsl
// 基本函数定义
返回类型 函数名(参数列表) {
    // 函数体
    return 返回值;
}

// 示例：计算光照
float calculateDiffuse(vec3 normal, vec3 lightDir) {
    float diff = max(dot(normal, lightDir), 0.0);
    return diff;
}

// 重载函数
vec3 shadeColor(vec3 baseColor, float intensity) {
    return baseColor * intensity;
}

vec3 shadeColor(vec3 baseColor, vec3 lightColor, float intensity) {
    return baseColor * lightColor * intensity;
}
```

### 4.2. 参数传递模式

```glsl
// 值传递（默认）- 不影响原变量
void multiplyByTwo(float x) {
    x = x * 2.0;  // 只修改副本
}

// in 传递 - 输入参数
void processInput(in vec3 position) {
    vec3 p = position;  // 只读
}

// out 传递 - 输出参数
void calculateResult(in vec3 input, out vec3 result) {
    result = input * 2.0;  // 修改原变量
}

// inout 传递 - 输入输出参数
void modifyVector(inout vec3 v) {
    v.x += 1.0;  // 修改原变量
}

// 使用示例
void main() {
    float value = 5.0;
    multiplyByTwo(value);      // value 仍是 5.0

    vec3 v = vec3(1.0, 2.0, 3.0);
    modifyVector(v);           // v 变为 (2.0, 2.0, 3.0)
}
```

### 4.3. 内存布局

**结构体与对齐**:
```glsl
struct Light {
    vec3 position;     // 12 字节
    vec3 color;        // 12 字节
    float intensity;   // 4 字节
                    // 总计: 28 字节（可能需要对齐到 32 字节）
};

// 均匀缓冲区对象 (UBO)
layout(std140, binding = 0) uniform Lights {
    Light lights[8];  // 固定大小数组
};
```

---

## 5. 着色器阶段与内置变量

### 5.1. 顶点着色器 (Vertex Shader)

**输入**:
- `attribute` 或 `layout(location = N) in 类型 变量名`

**输出**:
- `varying` 或 `out 类型 变量名`

**内置变量**:
```glsl
// 坐标输出
vec4 gl_Position;           // 必须设置：裁剪空间坐标
float gl_PointSize;         // 点绘制大小（可选）

// 坐标输入
vec3 gl_VertexID;           // 顶点 ID
vec3 gl_InstanceID;         // 实例 ID（几何实例化）

// 旧版（兼容）
attribute vec3 gl_Vertex;   // 顶点位置
attribute vec3 gl_Normal;   // 顶点法线
attribute vec4 gl_Color;    // 顶点颜色
```

**示例**:
```glsl
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
out vec3 vNormal;

uniform mat4 MVP;  // Model-View-Projection

void main() {
    vNormal = normal;
    gl_Position = MVP * vec4(position, 1.0);
    gl_PointSize = 5.0;  // 点绘制模式使用
}
```

### 5.2. 片段着色器 (Fragment Shader)

**输入**:
- `varying` 或 `in 类型 变量名`

**输出**:
- `out vec4 gl_FragColor` (旧版)
- `out 类型 变量名` (现代) `layout(location = 0) out vec4 FragColor;`

**内置变量**:
```glsl
// 输出颜色
vec4 gl_FragColor;               // 旧版输出

// 输入
vec4 gl_FragCoord;               // 片段屏幕坐标 (x, y, z, w)
bool gl_FrontFacing;             // 是否正面朝向
float gl_FragDepth;              // 深度值（可写）

// 采样器
sampler2D gl_Texture[8];         // 旧版纹理单元
```

**示例**:
```glsl
in vec3 vNormal;
in vec2 vTexCoord;
uniform sampler2D diffuseTex;
layout(location = 0) out vec4 FragColor;

void main() {
    vec4 texColor = texture(diffuseTex, vTexCoord);
    vec3 light = normalize(vec3(1.0, 1.0, 1.0));
    float diff = max(dot(vNormal, light), 0.0);
    FragColor = texColor * diff;
}
```

### 5.3. 几何着色器 (Geometry Shader)

在顶点和片段之间，可修改几何图元：

```glsl
// 输入
layout(triangles) in;  // 输入图元类型
in vec3 vNormal[];     // 数组形式

// 输出
layout(triangle_strip, max_vertices = 3) out;
out vec3 gNormal;

void main() {
    // 传递原始三角形
    for(int i = 0; i < 3; i++) {
        gl_Position = gl_in[i].gl_Position;
        gNormal = vNormal[i];
        EmitVertex();
    }
    EndPrimitive();
}
```

---

## 6. 预处理指令

### 6.1. 条件编译

```glsl
// 选择编译
#ifdef MACRO_NAME
    // 如果定义了 MACRO_NAME，编译这段代码
#elif defined(MACRO2)
    // 否则如果定义了 MACRO2
#else
    // 否则
#endif

// 示例
#ifdef VERT
    // 顶点着色器专用代码
    attribute vec3 position;
#endif

#ifdef EDGE
    // 边缘着色器专用代码
    // ...
#endif

// 如果未定义
#ifndef DEBUG
    // 调试代码，仅在定义 DEBUG 时生效
#endif

// 逻辑运算
#if defined(VERT) && !defined(FACE)
    // 同时定义 VERT 且未定义 FACE
#endif

#if defined(VERT) || defined(EDGE)
    // 定义 VERT 或 EDGE
#endif
```

### 6.2. 宏定义

```glsl
// 简单宏定义
#define MAX_LIGHTS 8
#define PI 3.14159265359

// 带参数宏
#define POW2(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

// 使用示例
float area = POW2(5.0);  // 结果: 25.0

// 多行宏（反斜杠续行）
#define COMPUTE_LIGHT(i, pos) \
    vec3 lightDir = normalize(lights[i].position - pos); \
    float diff = max(dot(normal, lightDir), 0.0); \
    result += diff * lights[i].color;

// 取消定义
#undef PI
```

**Blender 特有宏示例**:
```glsl
// Shader 创建信息（C++ 定义，在 GLSL 中可用）
#define GPU_SHADER_CREATE_INFO(name) ...

// 自定义宏
#define LINE_OUTPUT  // 启用线段输出
#define VERT         // 顶点模式
#define EDGE         // 边缘模式
#define FACE         // 面模式
```

### 6.3. 文件包含

```glsl
// 标准包含
#include "path/to/header.glsl"

// Blender 库包含
#include "draw_view_lib.glsl"        // 视图变换函数
#include "overlay_common_lib.glsl"   // 通用工具函数

// 系统包含（如果有）
#include <math.h>
```

**包含路径查找**：
- 相对路径：从 shader 文件所在目录开始
- Blender 预定义路径：`source/blender/draw/intern/shaders/`

---

## 7. 常用内建函数

### 7.1. 数学函数

```glsl
// 三角函数
sin(x), cos(x), tan(x)
asin(x), acos(x), atan(y, x)

// 指数函数
pow(x, y)  // x^y
exp(x)     // e^x
log(x)     // ln(x)
sqrt(x)    // 平方根
inversesqrt(x)  // 1/sqrt(x)

// 绝对值、取整
abs(x)
floor(x)   // 向下取整
ceil(x)    // 向上取整
round(x)   // 四舍五入
fract(x)   // 小数部分
mod(x, y)  // 取模

// 截断/限制
min(x, y)
max(x, y)
clamp(x, minVal, maxVal)  // 限制在 [minVal, maxVal] 范围内

// 混合
mix(x, y, a)          // 线性混合: x * (1-a) + y * a
step(edge, x)         // x < edge ? 0.0 : 1.0
smoothstep(e0, e1, x) // 平滑过渡

// 例子：距离衰减
float attenuation = clamp(1.0 - distance / maxDistance, 0.0, 1.0);
```

### 7.2. 向量操作函数

```glsl
// 长度相关
length(v)           // 向量长度
distance(a, b)      // 点间距离
dot(a, b)           // 点积
cross(a, b)         // 叉积（仅 vec3）

// 归一化
normalize(v)        // 单位向量

// 反射/折射
reflect(I, N)       // 反射向量
refract(I, N, eta)  // 折射向量

// 处理
clamp(v, minVal, maxVal)  // 向量分量限制
mix(a, b, t)              // 向量混合

// 例子：光照计算
vec3 N = normalize(normal);
vec3 L = normalize(lightDir);
float NdotL = max(dot(N, L), 0.0);  // 漫反射强度
vec3 reflectDir = reflect(-L, N);   // 反射方向
```

### 7.3. 纹理采样函数

```glsl
// 基本采样
vec4 texture(sampler2D sam, vec2 coord)  // 现代 GLSL
vec4 texture2D(sampler2D sam, vec2 coord) // 旧版

// 带 LOD 采样
vec4 textureLod(sampler2D sam, vec2 coord, float lod)

// 带偏移采样
vec4 textureOffset(sampler2D sam, vec2 coord, ivec2 offset)

// 投影采样
vec4 textureProj(sampler2D sam, vec3 coord)  // 齐次坐标

// 多重采样（MSAA）
vec4 texture(sampler2DMS sam, vec2 coord, int sampleIdx)

// 纹理大小查询
ivec2 textureSize(sampler2D sam, int lod)

// 示例：深度纹理采样
uniform sampler2D depth_tx;
vec4 depths = textureGather(depth_tx, ndc.xy);  // 采集 4 个深度值
```

**Blender 中的特殊用法**:
```glsl
float textureGather(sampler2D sam, vec2 coord) {
    // 采集纹理的 2x2 邻域
    // 常用于深度测试
}
```

---

## 8. GLSL 与 Blender 的差异

### 8.1. 语法扩展

**Blender 的 GLSL 实际上是预处理后的纯 GLSL**，但使用了大量自定义宏：

```glsl
// 纯 GLSL 写法
uniform mat4 ModelMatrix;
uniform mat4 ViewMatrix;
uniform mat4 ProjectionMatrix;
in vec3 position;
out vec3 worldPos;

void main() {
    worldPos = (ModelMatrix * vec4(position, 1.0)).xyz;
    gl_Position = ProjectionMatrix * ViewMatrix * vec4(worldPos, 1.0);
}

// Blender GLSL 写法（使用库函数）
#include "draw_view_lib.glsl"
in vec3 position;
out vec3 worldPos;

void main() {
    worldPos = drw_point_object_to_world(position);
    gl_Position = drw_point_view_to_homogenous(
        drw_point_world_to_view(worldPos)
    );
}
```

### 8.2. 预处理宏对比

| 功能 | 纯 GLSL | Blender GLSL |
|------|---------|--------------|
| 视图变换 | 手动矩阵乘法 | `drw_view_lib.glsl` |
| 坐标变换 | `MVP * position` | `drw_point_...()` 系列函数 |
| Shader 定义 | 手动编写 | `GPU_SHADER_CREATE_INFO` |
| 资源绑定 | `uniform` | `.push_constant()`, `.sampler()` |
| 变体管理 | 手动写多个文件 | `.define()`, `#ifdef` |

---

## 9. Blender GLSL 实战示例

### 9.1 编辑模式顶点着色器

**定义位置**: `source/blender/draw/engines/overlay/shaders/overlay_edit_mesh_vert.glsl`

```glsl
// 包含创建信息定义
#include "infos/overlay_edit_mode_infos.hh"
VERTEX_SHADER_CREATE_INFO(overlay_edit_mesh_vert)

// 包含库
#include "draw_model_lib.glsl"
#include "draw_view_lib.glsl"
#include "overlay_common_lib.glsl"

// 顶点输入（来自 C++ 代码）
in vec3 pos;        // 位置
in vec4 data;       // 选择/标记数据
in vec3 vnor;       // 法线

// Uniforms（来自 C++ 代码）
uniform sampler2D depth_tx;       // 深度纹理
uniform float alpha;              // 透明度
uniform int4 data_mask;           // 数据掩码
uniform float retopology_offset;  // Retopology 偏移

// 输出到片段着色器
out vec4 final_color;         // 颜色
out float vertex_crease;      // 顶点折痕

void main() {
    // 1. 坐标变换链
    vec3 world_pos = drw_point_object_to_world(pos);
    vec3 view_pos = drw_point_world_to_view(world_pos);
    gl_Position = drw_point_view_to_homogenous(view_pos);

    // 2. Retopology 深度偏移
    float offset = get_homogenous_z_offset(
        drw_view().winmat,
        view_pos.z,
        gl_Position.w,
        retopology_offset
    );
    gl_Position.z += offset;

    // 3. 数据掩码处理
    vec4 m_data = data & data_mask;

    // 4. 颜色计算（条件编译分支）
    #if defined(VERT)
        vertex_crease = float(m_data.z >> 4) / 15.0f;
        final_color = EDIT_MESH_vertex_color(m_data.y, vertex_crease);
        gl_PointSize = theme.sizes.vert * ((vertex_crease > 0.0f) ? 3.0f : 2.0f);

        // 深度微调（选中顶点置顶）
        if ((data.x & VERT_SELECTED) != 0u) {
            gl_Position.z -= 5e-7f * abs(gl_Position.w);
        }

        // 测试遮挡
        bool occluded = test_occlusion();
    #elif defined(EDGE)
        // 边缘着色逻辑...
    #elif defined(FACE)
        // 面着色逻辑...
    #endif

    // 5. Alpha 混合
    final_color.a *= (occluded) ? alpha : 1.0f;

    // 6. 面向混合（Fresnel 效果）
    vec3 view_normal = normalize(drw_normal_object_to_view(vnor) + 1e-4f);
    vec3 view_vec = (drw_view().winmat[3][3] == 0.0f) ?
                    normalize(view_pos) : vec3(0.0, 0.0, 1.0);
    float facing = dot(view_vec, view_normal);
    facing = 1.0f - abs(facing) * 0.2f;

    final_color.rgb = mix(
        final_color.rgb,
        non_linear_blend_color(
            theme.colors.edit_mesh_middle.rgb,
            final_color.rgb,
            facing
        ),
        theme.fresnel_mix_edit
    );

    // 7. 视图裁剪
    view_clipping_distances(world_pos);
}
```

### 9.2 扩展学习资源

要深入学习 Blender 的 GLSL，建议：
1. 阅读 `docs/02_overlay_glsl_overview.md`
2. 查看 `source/blender/draw/intern/shaders/` 目录
3. 分析 `overlay_edit_mesh_common_lib.glsl` 中的工具函数
4. 使用 Blender 的 Shader 编辑器调试

---

**最后更新**: 2025-12-17
**适用版本**: Blender 4.3+
**参考资料**: GLSL Spec 4.60, Blender Source Code
