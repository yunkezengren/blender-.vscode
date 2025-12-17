# GLSL 基础语法与 Blender 扩展详解

## 目录
- [1. GLSL 基础语法](#1-glsl-基础语法)
  - [1.1. 数据类型](#11-数据类型)
  - [1.2. 变量与限定符](#12-变量与限定符)
  - [1.3. 运算符与表达式](#13-运算符与表达式)
- [2. 函数定义与调用](#2-函数定义与调用)
  - [2.1. 基本函数](#21-基本函数)
  - [2.2. 参数传递模式](#22-参数传递模式)
- [3. 着色器阶段](#3-着色器阶段)
  - [3.1. 顶点着色器](#31-顶点着色器)
  - [3.2. 片段着色器](#32-片段着色器)
  - [3.3. 几何着色器](#33-几何着色器)
- [4. Blender GLSL 特有语法](#4-blender-glsl-特有语法)
  - [4.1. 预处理宏系统](#41-预处理宏系统)
  - [4.2. Shader Create Info](#42-shader-create-info)
  - [4.3. 库文件包含系统](#43-库文件包含系统)
- [5. Blender 常用内建函数](#5-blender-常用内建函数)
  - [5.1. 视图变换函数](#51-视图变换函数)
  - [5.2. 坐标转换函数](#52-坐标转换函数)
  - [5.3. 颜色处理函数](#53-颜色处理函数)
- [6. 实战代码对比](#6-实战代码对比)
  - [6.1. 纯 GLSL vs Blender GLSL](#61-纯-glsl-vs-blender-glsl)
- [7. 常见陷阱与技巧](#7-常见陷阱与技巧)

---

## 1. GLSL 基础语法

### 1.1. 数据类型

#### **基本类型**

```glsl
// 1. 浮点数
float x = 1.5;          // 32位浮点，默认类型
float y = 2.0f;         // 显式指定浮点
float z = 2;            // 错误！整数不会自动转换
float w = float(2);     // 正确：显式转换

// 2. 整数
int a = 42;            // 有符号整数
uint b = 100u;         // 无符号整数（必须加 u 后缀）
int c = int(3.14);     // 类型转换

// 3. 布尔值
bool flag = true;
bool result = (x > 2.0);  // 比较得到

// 4. 向量（GLSL 核心）
vec2 v2 = vec2(1.0, 2.0);
vec3 v3 = vec3(1.0, 2.0, 3.0);
vec4 v4 = vec4(1.0, 2.0, 3.0, 4.0);

// 整数向量
ivec3 iv3 = ivec3(1, 2, 3);
uvec4 uv4 = uvec4(1u, 2u, 3u, 4u);

// 布尔向量
bvec2 bv2 = bvec2(true, false);

// 5. 矩阵（用于坐标变换）
mat2 m2 = mat2(1.0, 0.0, 0.0, 1.0);  // 2x2
mat3 m3 = mat3(1.0);                 // 3x3 单位阵
mat4 m4 = mat4(1.0);                 // 4x4 单位阵

// 按列初始化
mat4 transform = mat4(
    1.0, 0.0, 0.0, 0.0,   // 第一列
    0.0, 1.0, 0.0, 0.0,   // 第二列
    0.0, 0.0, 1.0, 0.0,   // 第三列
    0.0, 0.0, 0.0, 1.0    // 第四列
);

// 6. 采样器（纹理）
uniform sampler2D depth_tx;        // 2D 纹理
uniform samplerCube env_map;       // 立方体贴图
uniform sampler3D volume_tex;      // 3D 纹理

// 7. 结构体（自定义类型）
struct Light {
    vec3 position;
    vec3 color;
    float intensity;
};

Light sun = Light(vec3(0, 1, 0), vec3(1, 1, 0.8), 1.0);
```

#### **向量分量访问**

```glsl
vec4 color = vec4(1.0, 0.5, 0.3, 1.0);

// 位置分量（xyzw）
float r = color.x;      // 1.0
float g = color.y;      // 0.5
float b = color.z;      // 0.3
float a = color.w;      // 1.0

// 颜色分量（rgba）- 等价于 xyzw
float red = color.r;    // 1.0

// 纹理坐标（stpq）
float s = color.s;      // 1.0

// 重组
vec3 rgb = color.rgb;        // (1.0, 0.5, 0.3)
vec2 rg = color.rg;          // (1.0, 0.5)
vec4 bgra = color.bgra;      // (0.3, 0.5, 1.0, 1.0) - 重新排序

// 修改部分分量
color.rgb = vec3(0.0, 1.0, 0.0);  // 只修改 RGB，保持 Alpha
color.a = 0.5;                    // 只修改 Alpha

// 掩码操作
vec4 result = color;
result.aba = color.rgr;  // 按位置赋值：a=y, b=x, a=y
```

#### **矩阵访问与运算**

```glsl
mat4 m = mat4(
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 16
);

// 访问元素（列主序！）
float x = m[0][0];   // 第1列第1行 = 1
float y = m[1][0];   // 第2列第1行 = 5 (注意：不是 m[0][1]!)
float z = m[2][2];   // 第3列第3行 = 11

// 乘法
vec4 pos = vec4(1.0, 2.0, 3.0, 1.0);
vec4 transformed = m * pos;  // 矩阵×向量

mat4 a = mat4(1.0);
mat4 b = mat4(2.0);
mat4 c = a * b;  // 矩阵×矩阵（行×列）

// 矩阵×标量
mat4 scaled = m * 2.0;  // 每个元素×2
```

---

### 1.2. 变量与限定符

#### **存储限定符**

| 限定符 | 作用范围 | 用途 | 示例 |
|--------|---------|------|------|
| `const` | 函数内/全局 | 编译时常量 | `const float PI = 3.14159;` |
| `uniform` | 所有着色器 | CPU 传入，每帧统一 | `uniform mat4 MVP;` |
| `attribute` | 顶点着色器 | 每个顶点数据（旧版） | `attribute vec3 position;` |
| `varying` | 顶点→片段 | 插值传递（旧版） | `varying vec3 vNormal;` |
| `in` | 片段/几何着色器 | 输入（现代） | `in vec3 vNormal;` |
| `out` | 顶点/几何着色器 | 输出（现代） | `out vec3 vNormal;` |
| `buffer` | 所有 | SSBO（大数组） | `buffer PosBuf { float pos[]; };` |

**现代 GLSL 符号** (3.30+，Blender 使用此风格):

```glsl
// 顶点着色器
layout(location = 0) in vec3 position;   // 顶点属性
layout(location = 1) in vec3 normal;
out vec3 vNormal;                        // 传递到片段

void main() {
    vNormal = normal;
    gl_Position = vec4(position, 1.0);
}

// 片段着色器
in vec3 vNormal;                         // 从顶点接收
out vec4 fragColor;                      // 输出颜色

void main() {
    fragColor = vec4(vNormal, 1.0);
}
```

**Uniform 使用示例**:

```glsl
// CPU 每帧设置一次，对所有顶点/片段相同
uniform mat4 ModelMatrix;       // 模型矩阵
uniform mat4 ViewMatrix;        // 视图矩阵
uniform mat4 ProjectionMatrix;  // 投影矩阵
uniform vec3 LightPosition;     // 光源位置
uniform float Time;             // 时间

void main() {
    vec4 worldPos = ModelMatrix * vec4(position, 1.0);
    vec4 viewPos = ViewMatrix * worldPos;
    gl_Position = ProjectionMatrix * viewPos;

    float dist = distance(worldPos.xyz, LightPosition);
    // ...
}
```

**Buffer/SSBO** (大数组):

```glsl
// Shader Storage Buffer Object - 用于大数据
layout(std430, binding = 0) buffer PositionBuffer {
    vec4 positions[];  // 动态大小数组
};

layout(std430, binding = 1) buffer SelectionBuffer {
    uint select[];
};

void main() {
    uint id = gl_VertexID;
    vec3 pos = positions[id].xyz;  // 直接从 GPU 内存读取
    uint sel = select[id >> 5];    // 位操作选择标记
}
```

#### **精度限定符**

```glsl
// 精度影响性能和准确性
precision highp float;    // 默认：32位浮点（高精度）
precision mediump float;  // 默认：16-32位浮点（中等）

// 为特定变量指定精度
highp vec3 position;      // 顶点坐标（需要高精度）
mediump vec3 normal;      // 法线（中等精度即可）
lowp vec3 color;          // 颜色（低精度）

// 3 种精度级别
highp   ~32位浮点，精确，速度慢
mediump ~16-32位，中等精度和速度
lowp    ~8-16位，低精度但速度快，适合颜色

// 实际应用
uniform sampler2D diffuse_tex;
void main() {
    highp vec2 uv = texCoord;      // UV 坐标
    mediump vec4 col = texture(diffuse_tex, uv);
    lowp float alpha = col.a;      // Alpha 通道
    gl_FragColor = vec4(col.rgb, alpha);
}
```

#### **插值限定符**

```glsl
// 顶点着色器输出
smooth out vec3 vNormal;   // 平滑插值（默认）
flat out int materialID;   // 不插值（整数）
noperspective out float depth; // 透视校正（特殊场景）

// 使用
void main() {
    vNormal = normalize(normal);
    materialID = int(data.x);
    depth = gl_Position.z;

    // 平面着色：整个图元使用值
    flat materialID = 1;  // 整个三角形使用同一ID
}
```

---

### 1.3. 运算符与表达式

#### **算术运算符**

```glsl
// 基本运算
float a = 1.0 + 2.0;  // 3.0
float b = a * 3.0;    // 9.0
float c = b / 2.0;    // 4.5
int d = 9 % 4;        // 1

// 向量运算（分量级）
vec3 v1 = vec3(1.0, 2.0, 3.0);
vec3 v2 = vec3(4.0, 5.0, 6.0);

vec3 sum = v1 + v2;          // (5.0, 7.0, 9.0)
vec3 diff = v1 - v2;         // (-3.0, -3.0, -3.0)
vec3 product = v1 * v2;      // (4.0, 10.0, 18.0) - 分量相乘！
vec3 scaled = v1 * 2.0;      // (2.0, 4.0, 6.0) - 标量乘法

// 矩阵运算
mat4 m = mat4(1.0);
mat4 n = m * 2.0;            // 缩放矩阵
vec4 p = m * vec4(1,1,1,1);  // 变换向量

// 点积与叉积
float dot_product = dot(v1, v2);      // 1×4 + 2×5 + 3×6 = 32.0
vec3 cross_product = cross(v1, v2);   // (2×6-3×5, 3×4-1×6, 1×5-2×4) = (-3, 6, -3)
```

#### **比较运算符**

```glsl
// 逻辑比较
bool eq = (1.0 == 1.0);           // true
bool ne = (1.0 != 2.0);           // true
bool gt = (2.0 > 1.0);            // true
bool ge = (2.0 >= 1.0);           // true
bool lt = (1.0 < 2.0);            // true
bool le = (1.0 <= 2.0);           // true

// 向量比较（返回布尔向量）
bvec3 res = greaterThan(v1, v2);  // (false, false, false)

// 向量聚合比较
bool all_v = all(greaterThan(v1, v2));  // 所有分量都？
bool any_v = any(lessThan(v1, v2));     // 任一分量？

// 混合
float result = (condition) ? 1.0 : 0.0;
vec3 color = (useRed) ? vec3(1,0,0) : vec3(0,1,0);
```

#### **位运算与逻辑**

```glsl
// 位运算
uint flags = 0b1010u;                // 二进制
uint selection = 0b0100u;
uint combined = flags | selection;    // 0b1110u = 14
uint masked = flags & selection;      // 0b0000u
uint flipped = ~flags;                // 按位取反

// 位移（常用于打包数据）
uint data = 0x00FF00FFu;
uint byte0 = data & 0xFFu;           // 取最低字节
uint byte1 = (data >> 8) & 0xFFu;    // 取第2字节
uint packed = (value1 << 16) | value0;

// 逻辑运算
bool a = true, b = false;
bool AND = a && b;          // false
bool OR = a || b;           // true
bool NOT = !a;              // false

// 短路求值
if (someCondition && expensiveTest()) {
    // 如果 someCondition 为 false，不执行 expensiveTest
}
```

---

## 2. 函数定义与调用

### 2.1. 基本函数

```glsl
// 函数定义
返回类型 函数名(参数列表) {
    // 函数体
    return 返回值;
}

// 示例 1：简单计算
float distance2(vec3 a, vec3 b) {
    vec3 diff = a - b;
    return length(diff);  // sqrt(a²+b²+c²)
}

// 示例 2：返回多个值
void getMinMax(vec3 color, out float minVal, out float maxVal) {
    minVal = min(color.r, min(color.g, color.b));
    maxVal = max(color.r, max(color.g, color.b));
}

// 使用
float minC, maxC;
getMinMax(vec3(1, 2, 3), minC, maxC);  // minC=1, maxC=3

// 示例 3：复杂光照计算
vec3 calculateLighting(vec3 normal, vec3 lightDir, vec3 viewDir, vec3 baseColor) {
    // 漫反射
    float NdotL = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = baseColor * NdotL;

    // 高光（Blinn-Phong）
    vec3 halfDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfDir), 0.0), 32.0);
    vec3 specular = vec3(1.0) * spec;

    return diffuse + specular;
}
```

### 2.2. 参数传递模式

#### **值传递**（默认）

```glsl
void modifyValue(float x) {
    x = x * 2.0;  // 只修改副本，不影响原变量
}

void main() {
    float val = 5.0;
    modifyValue(val);  // val 仍是 5.0
}
```

#### **in 参数**（只读输入）

```glsl
void processInput(in vec3 position) {
    // 可以读取 position，但不能修改原值
    vec3 p = position * 2.0;  // 新变量
}

void main() {
    vec3 pos = vec3(1, 2, 3);
    processInput(pos);
    // pos 不变
}
```

#### **out 参数**（只写输出）

```glsl
void calculateResult(in vec3 input, out vec3 result) {
    result = input * 2.0;  // 直接修改原变量
}

void main() {
    vec3 v = vec3(1, 2, 3);
    vec3 output;
    calculateResult(v, output);  // output = (2,4,6)
}
```

#### **inout 参数**（输入输出）

```glsl
void modifyVector(inout vec3 v) {
    v.x += 1.0;      // 修改原变量
    v = normalize(v); // 也修改原变量
}

void main() {
    vec3 v = vec3(1, 0, 0);
    modifyVector(v);  // v = (1, 0, 0) -> (2, 0, 0) -> (1, 0, 0)
}
```

### 2.3. 函数重载

```glsl
// GLSL 支持函数重载
vec3 shade(vec3 baseColor) {
    return baseColor;
}

vec3 shade(vec3 baseColor, float intensity) {
    return baseColor * intensity;
}

vec3 shade(vec3 baseColor, vec3 lightColor, float intensity) {
    return baseColor * lightColor * intensity;
}

// 使用
void main() {
    vec3 c1 = shade(white);                    // 调用版本1
    vec3 c2 = shade(white, 0.5);               // 调用版本2
    vec3 c3 = shade(white, vec3(1,0.5,0), 1); // 调用版本3
}
```

---

## 3. 着色器阶段

### 3.1. 顶点着色器 (Vertex Shader)

**输入**：
```glsl
// 顶点属性（来自 CPU 的顶点缓冲）
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texCoord;
layout(location = 3) in vec4 color;

// 内置变量
int gl_VertexID;        // 顶点索引
int gl_InstanceID;      // 实例化索引
```

**输出**（传递给片段着色器）：
```glsl
out vec3 vNormal;
out vec2 vTexCoord;
out vec4 vColor;

// 或使用接口块
out VertexData {
    vec3 normal;
    vec2 uv;
} frag_out;
```

**内置输出**：
```glsl
void main() {
    gl_Position = vec4(position, 1.0);  // 必须设置：裁减空间坐标
    gl_PointSize = 5.0;                 // 可选：点绘制大小
}
```

**完整示例**：
```glsl
// 顶点着色器
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texCoord;

uniform mat4 MVP;
uniform mat3 NormalMatrix;

out vec3 vNormal;
out vec2 vTexCoord;
out vec3 vViewPos;

void main() {
    // 坐标变换
    vec4 worldPos = vec4(position, 1.0);
    vec4 viewPos = ModelViewMatrix * worldPos;
    gl_Position = ProjectionMatrix * viewPos;

    // 传递插值数据
    vNormal = normalize(NormalMatrix * normal);
    vTexCoord = texCoord;
    vViewPos = viewPos.xyz;

    // 点模式（可选）
    gl_PointSize = 10.0;
}
```

### 3.2. 片段着色器 (Fragment Shader)

**输入**（从顶点着色器插值而来）：
```glsl
// 现代 GLSL
in vec3 vNormal;
in vec2 vTexCoord;
in vec4 vColor;

// 旧版 GLSL
varying vec3 vNormal;
```

**内置输入**：
```glsl
vec4 gl_FragCoord;     // 屏幕坐标 (x, y, z, w)
bool gl_FrontFacing;   // 是否正面朝向
float gl_FragDepth;    // 可写深度（可选）
```

**输出**：
```glsl
// 现代 GLSL
out vec4 fragColor;    // 必须设置：输出颜色

// 旧版 GLSL
gl_FragColor = vec4(...);  // 已废弃但在 Blender 某些旧代码中使用

// 多输出（MRT - Multiple Render Targets）
layout(location = 0) out vec4 color;
layout(location = 1) out vec4 normal;
layout(location = 2) out float depth;
```

**完整示例**：
```glsl
// 片段着色器
in vec3 vNormal;
in vec2 vTexCoord;
in vec3 vViewPos;

uniform sampler2D diffuseTex;
uniform sampler2D normalTex;
uniform vec3 lightPos;
uniform vec3 viewPos;

out vec4 fragColor;

void main() {
    // 采样纹理
    vec4 base = texture(diffuseTex, vTexCoord);

    // 法线映射
    vec3 normal = texture(normalTex, vTexCoord).xyz;
    normal = normalize(normal * 2.0 - 1.0);

    // 光照计算
    vec3 lightDir = normalize(lightPos - vViewPos);
    float NdotL = max(dot(normal, lightDir), 0.0);

    // 高光
    vec3 viewDir = normalize(viewPos - vViewPos);
    vec3 halfDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfDir), 0.0), 32.0);

    // 最终颜色
    vec3 ambient = base.rgb * 0.2;
    vec3 diffuse = base.rgb * NdotL * 0.8;
    vec3 specular = vec3(1.0) * spec * 0.5;

    fragColor = vec4(ambient + diffuse + specular, base.a);

    // 简单的深度写入（可选）
    gl_FragDepth = gl_FragCoord.z;
}
```

### 3.3. 几何着色器 (Geometry Shader)

**输入**：
```glsl
layout(triangles) in;  // 输入图元类型
in vec3 vNormal[];     // 数组形式，每个顶点一个

// 内置
vec4 gl_in[];          // 输入顶点位置
int gl_PrimitiveIDIn;  // 图元ID
```

**输出**：
```glsl
layout(triangle_strip, max_vertices = 3) out;  // 输出配置
out vec3 gNormal;                               // 输出变量

// 内置
void EmitVertex();    // 发射一个顶点
void EndPrimitive();  // 结束当前图元
```

**完整示例（Blender 边缘着色器）**：
```glsl
// overlay_edit_mesh_edge_vert.glsl 几何着色器部分

layout(lines) in;  // 输入：线段
layout(triangle_strip, max_vertices = 4) out;  // 输出：四边形

in vec4 final_color[];  // 输入颜色（每顶点）

out vec4 geometry_out_final_color;
out float edge_coord;

void main() {
    // 获取原始线段的两个端点
    vec4 pos0 = gl_in[0].gl_Position;
    vec4 pos1 = gl_in[1].gl_Position;

    // 屏幕空间计算
    vec2 ss_pos0 = pos0.xy / pos0.w;
    vec2 ss_pos1 = pos1.xy / pos1.w;

    // 线段方向（像素空间）
    vec2 line = (ss_pos0 - ss_pos1) * viewport_size;
    vec2 perp = normalize(vec2(-line.y, line.x));

    // 边缘半宽（像素）
    float half_width = edge_width + (do_smooth_wire ? 0.5 : 0.0);
    vec2 offset = perp * half_width / viewport_size;

    // 发射 4 个顶点形成四边形
    // 顶点顺序：0-outer, 0-inner, 1-outer, 1-inner

    // 顶点 0（外侧）
    gl_Position = pos0;
    gl_Position.xy += offset * pos0.w;
    edge_coord = 1.0;  // 外侧
    geometry_out_final_color = final_color[0];
    EmitVertex();

    // 顶点 1（内侧）
    gl_Position = pos0;
    gl_Position.xy -= offset * pos0.w;
    edge_coord = -1.0;  // 内侧
    geometry_out_final_color = final_color[0];
    EmitVertex();

    // 顶点 2（外侧）
    gl_Position = pos1;
    gl_Position.xy += offset * pos1.w;
    edge_coord = 1.0;
    geometry_out_final_color = final_color[1];
    EmitVertex();

    // 顶点 3（内侧）
    gl_Position = pos1;
    gl_Position.xy -= offset * pos1.w;
    edge_coord = -1.0;
    geometry_out_final_color = final_color[1];
    EmitVertex();

    EndPrimitive();  // 结束四边形
}
```

---

## 4. Blender GLSL 特有语法

### 4.1. 预处理宏系统

Blender 独特的魔法在于**宏定义 + 条件编译**。

#### **条件编译核心**

```glsl
// overlay_edit_mesh_vert.glsl

// 包含创建信息（C++ 定义）
#include "infos/overlay_edit_mode_infos.hh"

// 这个宏由 C++ 的 .define("VERT") 生成
VERTEX_SHADER_CREATE_INFO(overlay_edit_mesh_vert)

#ifdef GLSL_CPP_STUBS
#  define VERT
#endif

// 包含库
#include "draw_model_lib.glsl"
#include "overlay_common_lib.glsl"

void main() {
    // 坐标变换
    vec3 world_pos = drw_point_object_to_world(pos);
    vec3 view_pos = drw_point_world_to_view(world_pos);
    gl_Position = drw_point_view_to_homogenous(view_pos);

    // === 关键：条件分支 ===
    #if defined(VERT)
        // 顶点显示模式
        final_color = EDIT_MESH_vertex_color(m_data.y, vertex_crease);
        gl_PointSize = theme.sizes.vert;
        if (data.x & VERT_ACTIVE) {
            gl_Position.z -= 5e-7f;  // 置顶
        }

    #elif defined(EDGE)
        // 边缘显示模式（由 EDGE 生成）
        final_color = EDIT_MESH_edge_vertex_color(m_data.y);

    #elif defined(EDGE)
        // 面显示模式
        final_color = EDIT_MESH_face_color(m_data.x);

    #elif defined(FACEDOT)
        // 面点模式
        final_color = EDIT_MESH_facedot_color(norAndFlag.w);
        gl_PointSize = theme.sizes.face_dot;
    #endif

    // 面向混合（所有模式共享）
    if (occluded) {
        final_color.a *= alpha;
    }
}
```

#### **C++ 控制宏**

```cpp
// overlay_edit_mode_infos.hh

// 定义顶点着色器（不带变体）
GPU_SHADER_CREATE_INFO(overlay_edit_mesh_vert)
    .define("VERT")  // ← 关键：在 GLSL 中生成 #define VERT
    .vertex_in(0, float3, pos)
    .vertex_in(1, uint4, data)
    .vertex_source("overlay_edit_mesh_vert.glsl")
    .fragment_source("overlay_point_varying_color_frag.glsl")
.end()

// 定义边缘着色器（复用同一文件，不同宏）
GPU_SHADER_CREATE_INFO(overlay_edit_mesh_edge)
    .define("EDGE")  // ← 使用 #elif defined(EDGE) 分支
    .vertex_in(0, float3, pos)
    .vertex_in(1, uint4, data)
    .vertex_source("overlay_edit_mesh_vert.glsl")  // 同一个文件！
    .geometry_source("overlay_edit_mesh_edge_vert.glsl")  // 几何着色器
    .fragment_source("overlay_edit_mesh_frag.glsl")
.end()

// 定义面着色器
GPU_SHADER_CREATE_INFO(overlay_edit_mesh_face)
    .define("FACE")  // ← 使用 #elif defined(FACE) 分支
    .vertex_source("overlay_edit_mesh_vert.glsl")  // 同一个文件！
    .fragment_source("overlay_varying_color.glsl")
.end()
```

**一个文件，多个用途**：
```
overlay_edit_mesh_vert.glsl
├── #ifdef VERT    → 顶点模式
├── #elif EDGE    → 边缘模式
├── #elif FACE    → 面模式
└── #elif FACEDOT → 面点模式
```

#### **调试宏**

```glsl
// 自定义调试宏
#ifdef DEBUG
#  define DEBUG_PRINT(x) print(x)
#  define DEBUG_COLOR(c) fragColor = c
#else
#  define DEBUG_PRINT(x)
#  define DEBUG_COLOR(c)
#endif

void main() {
    DEBUG_PRINT("Rendering pixel");
    DEBUG_COLOR(vec4(1,0,0,1));  // 调试时显示红色
}
```

### 4.2. Shader Create Info 语法

这是 Blender 独有的**配置即代码**系统。

```cpp
// C++ 配置代码

// ===== 定义着色器接口 =====
GPU_SHADER_INTERFACE_INFO(my_shader_iface)
    .smooth(vec3, world_normal)      // 平滑插值
    .flat(vec2, uv)                  // 平面插值
.end()

// ===== 定义通用配置库 =====
GPU_SHADER_CREATE_INFO(my_common_lib)
    .sampler(0, sampler2D, diffuseTex)
    .push_constant(float, time)
    .additional_info("draw_view")  // 继承库
.end()

// ===== 定义完整着色器 =====
GPU_SHADER_CREATE_INFO(my_surface_shader)
    .do_static_compilation(true)      // 预编译
    .vertex_in(0, float3, position)
    .vertex_in(1, vec3, normal)
    .vertex_out(my_shader_iface)      // 输出接口
    .vertex_source("my_vert.glsl")
    .fragment_source("my_frag.glsl")
    .additional_info("my_common_lib")
.end()

// ===== 创建变体 =====
CREATE_INFO_VARIANT(my_surface_shader_selectable,
                    my_surface_shader,
                    drw_selectable)   // + 选择ID

CREATE_INFO_VARIANT(my_surface_shader_clipped,
                    my_surface_shader,
                    drw_clipped)      // + 裁剪

// ===== 使用 =====
void Resources::init() {
    // ShaderModule 内部使用这些配置链接
    // 实际生成的着色器：
    // - my_surface_shader
    // - my_surface_shader_selectable
    // - my_surface_shader_clipped
    // - my_surface_shader_selectable_clipped
}
```

**产生的实际效果**：

| C++ 配置 | GLSL 生成结果 |
|---------|--------------|
| `.define("VERT")` | `#define VERT` |
| `.vertex_in(0, float3, pos)` | `layout(location=0) in vec3 pos;` |
| `.sampler(0, sampler2D, tex)` | `uniform sampler2D tex;` |
| `.push_constant(float, time)` | `uniform float time;` |
| `.additional_info("draw_view")` | `#include "draw_view_lib.glsl"` |

### 4.3. 库文件包含系统

#### **库文件结构**

```glsl
// ===== draw_view_lib.glsl =====
#pragma once  // 防止重复包含

#include "draw_view_infos.hh"  // 头文件定义

SHADER_LIBRARY_CREATE_INFO(draw_view)  // 声明为库

// 库函数定义
ViewMatrices drw_view() {
    return drw_view_buf[drw_view_id];
}

float3 drw_point_world_to_view(float3 P) {
    return (drw_view().viewmat * vec4(P, 1.0)).xyz;
}

// ===== overlay_common_lib.glsl =====
#pragma once

#include "draw_view_lib.glsl"  // 依赖其他库

SHADER_LIBRARY_CREATE_INFO(overlay_edit_mesh_common)

float4 EDIT_MESH_edge_color_outer(uint edge_flag, uint face_flag,
                                   float crease, float bweight) {
    float4 color = float4(0.0);
    if ((edge_flag & EDGE_FREESTYLE) != 0u) {
        color = theme.colors.edge_freestyle;
    }
    // ... 一系列颜色计算逻辑
    return color;
}

// ===== 使用库的着色器 =====
#include "infos/overlay_edit_mode_infos.hh"
VERTEX_SHADER_CREATE_INFO(overlay_edit_mesh_vert)

#include "draw_view_lib.glsl"
#include "overlay_common_lib.glsl"

void main() {
    // 可以使用库函数
    float3 view_pos = drw_point_world_to_view(world_pos);
    vec4 color = EDIT_MESH_edge_color_outer(data.x, data.y, 0.0, 0.0);
}
```

#### **库信息配置**

```cpp
// C++ 中的库配置

// ===== draw_view Infos =====
GPU_SHADER_LIBRARY_CREATE_INFO(draw_view)
    .uniform_block(0, "ViewMatrices", "drw_view_buf")
    .push_constant(int, "drw_view_id")
.end()

// ===== overlay_common Infos =====
GPU_SHADER_LIBRARY_CREATE_INFO(overlay_edit_mesh_common)
    .define("EDGE_FREESTYLE", "1")
    .define("EDGE_SHARP", "2")
    .uniform_buffer(0, "UniformData", "theme")
.end()
```

---

## 5. Blender 常用内建函数

### 5.1. 视图变换函数库

**文件**: `draw_view_lib.glsl`

```glsl
// ===== 核心视图函数 =====

// 获取当前视图矩阵
ViewMatrices drw_view();

// 检查是否透视投影
bool drw_view_is_perspective() {
    return drw_view().winmat[3][3] == 0.0f;
}

// 坐标变换（这是最常用的！）
float3 drw_point_object_to_world(float3 P) {
    return (drw_view().modelmat * vec4(P, 1.0)).xyz;
}

float3 drw_point_world_to_view(float3 P) {
    return (drw_view().viewmat * vec4(P, 1.0)).xyz;
}

float4 drw_point_view_to_homogenous(float3 P) {
    return drw_view().winmat * vec4(P, 1.0);
}

// 法线变换
float3 drw_normal_object_to_view(float3 N) {
    return normalize((drw_view().modelmat_inv_transpose * vec4(N, 0.0)).xyz);
}

// ===== 高级函数 =====

// 屏幕空间到 NDC
float3 drw_screen_to_ndc(float3 ss_P) {
    return ss_P * 2.0f - 1.0f;
}

// 视图深度
float drw_view_z_distance(float3 P) {
    return dot(P - drw_view_position(), -drw_view_forward());
}

// 近/远裁剪面
float drw_view_near();
float drw_view_far();
```

### 5.2. 模型矩阵库

**文件**: `draw_model_lib.glsl`

```glsl
// 对象到世界的变换矩阵
mat4 drw_modelmat();

// 变换点
float3 drw_point_model_to_world(float3 P) {
    return (drw_modelmat() * vec4(P, 1.0)).xyz;
}

// 实例化对象（多次渲染同一网格不同位置）
mat4 drw_instance_modelmat(int instance_id) {
    return drw_instance_matrix_buf[instance_id];
}
```

### 5.3. 颜色处理函数

**文件**: `overlay_common_lib.glsl`

```glsl
// ===== 颜色编码与解码（用于选择） =====

// 将 ID 编码为 RGB 颜色
vec4 encode_id_to_color(int id) {
    id++;  // 避免 ID=0 问题
    return vec4(
        float(id & 0xFF) / 255.0f,
        float((id >> 8) & 0xFF) / 255.0f,
        float((id >> 16) & 0xFF) / 255.0f,
        1.0f
    );
}

// 从颜色解码 ID
int decode_color_to_id(vec4 color) {
    int r = int(color.r * 255.0f);
    int g = int(color.g * 255.0f);
    int b = int(color.b * 255.0f);
    return (r | (g << 8) | (b << 16)) - 1;
}

// ===== 颜色空间转换 =====

// sRGB 到线性
vec3 srgb_to_linear(vec3 color) {
    return pow(color, vec3(2.2f));
}

// 线性到 sRGB
vec3 linear_to_srgb(vec3 color) {
    return pow(color, vec3(1.0f/2.2f));
}

// ===== 非线性混合（更好的视觉效果） =====

vec3 non_linear_blend_color(vec3 col1, vec3 col2, float fac) {
    col1 = pow(col1, vec3(1.0f/2.2f));
    col2 = pow(col2, vec3(1.0f/2.2f));
    vec3 col = mix(col1, col2, fac);
    return pow(col, vec3(2.2f));
}

// ===== 深度偏移计算 =====

float get_homogenous_z_offset(float4x4 winmat, float vs_z,
                              float hs_w, float vs_offset) {
    if (vs_offset == 0.0f) {
        return 0.0f;
    }
    else if (winmat[3][3] == 0.0f) {
        // 透视投影深度偏移
        vs_offset = min(vs_offset, vs_z * -0.5f);
        return winmat[3][2] * (vs_offset / (vs_z * (vs_z + vs_offset))) * hs_w;
    }
    else {
        // 正交投影深度偏移
        return winmat[2][2] * vs_offset * hs_w;
    }
}
```

---

## 6. 实战代码对比

### 6.1. 纯 GLSL vs Blender GLSL

#### **场景：渲染一个简单的变换立方体**

#### **纯 GLSL 写法**

```glsl
// ===== 顶点着色器 =====
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 ModelMatrix;
uniform mat4 ViewMatrix;
uniform mat4 ProjectionMatrix;
uniform mat3 NormalMatrix;

out vec3 vNormal;
out vec3 vWorldPos;

void main() {
    // 手动矩阵乘法
    vec4 worldPos = ModelMatrix * vec4(position, 1.0);
    vec4 viewPos = ViewMatrix * worldPos;
    gl_Position = ProjectionMatrix * viewPos;

    vNormal = normalize(NormalMatrix * normal);
    vWorldPos = worldPos.xyz;
}

// ===== 片段着色器 =====
#version 330 core

in vec3 vNormal;
in vec3 vWorldPos;

uniform vec3 lightPos;
uniform vec3 viewPos;

out vec4 fragColor;

void main() {
    vec3 N = normalize(vNormal);
    vec3 L = normalize(lightPos - vWorldPos);
    vec3 V = normalize(viewPos - vWorldPos);

    float diff = max(dot(N, L), 0.0);

    vec3 H = normalize(L + V);
    float spec = pow(max(dot(N, H), 0.0), 32.0);

    fragColor = vec4(vec3(0.8) * diff + vec3(1.0) * spec, 1.0);
}
```

#### **Blender GLSL 写法**

```glsl
// ===== 顶点着色器 =====
// 通常命名为 my_shader.glsl

// 1. 包含创建信息
#include "infos/my_shader_infos.hh"
VERTEX_SHADER_CREATE_INFO(my_shader)

// 2. 包含 Blender 库（一行代码搞定矩阵变换）
#include "draw_view_lib.glsl"
#include "draw_model_lib.glsl"

void main() {
    // 使用库函数 - 自动处理矩阵
    float3 worldPos = drw_point_object_to_world(position);
    float3 viewPos = drw_point_world_to_view(worldPos);
    gl_Position = drw_point_view_to_homogenous(viewPos);

    // 法线变换
    vNormal = drw_normal_object_to_view(normal);
}

// ===== 片段着色器 =====
#include "infos/my_shader_infos.hh"

void main() {
    // 直接使用库函数
    float3 lightPos = drw_view_position();  // 从视图获取
    float3 viewPos = drw_view_position();

    // 计算光照（与纯 GLSL 相同）
    float diff = max(dot(vNormal, normalize(lightPos - vWorldPos)), 0.0);
    // ...
}
```

#### **C++ 配置对比**

**纯 GLSL（没有 C++ 配置）**：
```cpp
// 只需要传统方式绑定
glUseProgram(shader_id);
glUniformMatrix4fv(model_loc, 1, GL_FALSE, &model[0][0]);
glUniformMatrix4fv(view_loc, 1, GL_FALSE, &view[0][0]);
```

**Blender 方式**：
```cpp
// overlay_my_shader_infos.hh
GPU_SHADER_CREATE_INFO(my_shader)
    .vertex_in(0, float3, position)
    .vertex_in(1, vec3, normal)
    .vertex_source("my_shader.vert")
    .fragment_source("my_shader.frag")
    .additional_info("draw_view")      // 自动注入 view 矩阵
    .additional_info("draw_modelmat")  // 自动注入 model 矩阵
.end()

// C++ 简化代码
pass.shader_set(shaders->my_shader.get());
pass.bind_ubo(WORLD_GLOBALS_SLOT, &res.globals_buf);
pass.draw(geom);
```

### 6.2. 复杂性分析

| 方面 | 纯 GLSL | Blender GLSL |
|------|---------|--------------|
| **矩阵变换** | 手写或自带数学库 | 通过库函数一行搞定 |
| **资源绑定** | 逐个 uniform 绑定 | 通过 info 自动注入 |
| **维护成本** | 分散在各处 | 集中管理 |
| **可读性** | 直观但冗长 | 简洁但需学习宏 |
| **变体管理** | 手写多个文件 | 自动生成 |
| **学习曲线** | 平缓 | 较陡（需理解宏系统）|

---

## 7. 常见陷阱与技巧

### 7.1. 精度陷阱

```glsl
// ❌ 错误：低精度导致 Z-fighting
lowp float depth;  // 精度不足
gl_FragDepth = depth;

// ✅ 正确：使用高精度
highp float depth;
gl_FragDepth = depth;

// ❌ 错误：中间计算精度不足
lowp vec3 normal;
normal = normalize(normal);  // 可能产生误差

// ✅ 正确：计算用高精度，存储用低精度
highp vec3 temp = normalize(normal_data);
lowp vec3 normal = temp;
```

### 7.2. 向量运算陷阱

```glsl
// ❌ 错误：点积 vs 分量乘法混淆
vec3 product = v1 * v2;  // 分量乘法 (x1*x2, y1*y2, z1*z2)
float dot = v1 * v2;     // 编译错误！不能直接乘

// ✅ 正确
float dot_result = dot(v1, v2);  // 点积结果
vec3 component_wise = v1 * v2;   // 分量乘法

// ❌ 错误：矩阵 vs 向量维度
vec4 result = mat4(1.0) * vec3(1.0);  // 维度不匹配

// ✅ 正确
vec4 result = mat4(1.0) * vec4(vec3(1.0), 1.0);  // 补齐 w 分量
```

### 7.3. 条件编译陷阱

```glsl
// ❌ 错误：宏未定义导致编译失败
void main() {
    #ifdef DEBUG
    degub_print("test");
    #endif
    // 如果 DEBUG 未定义，且 debug_print 被删除编译失败

    // ✅ 正确：定义空宏作为占位
    #ifndef DEBUG
    #  define debug_print(x)
    #endif
}

// ❌ 错误：分支预测不可预测
uniform bool useTexture;
void main() {
    if (useTexture) {
        // 如果 useTexture 在一个 draw call 内变化
        // GPU 会因为分支预测失败而性能下降
    }
}

// ✅ 正确：使用条件赋值而非分支
vec3 color = useTexture ?
             texture(tex, uv).rgb :
             default_color;
```

### 7.4. Blender 特有技巧

```glsl
// 技巧 1：一行获取视图位置
float3 camera_pos = drw_view_position();  // 替代 uniform 变量

// 技巧 2：深度测试 + 偏置
if (gl_FragCoord.z > texture(depth_tx, uv).r) {
    discard;  // 被遮挡
}

// 技巧 3：半透明排序（OIT - Order Independent Transparency）
vec4 final_color = compute_color();
gl_FragColor = vec4(final_color.rgb, final_color.a * project_order_factor);

// 技巧 4：使用 textureGather 进行快速邻域测试（效率高）
float4 depths = textureGather(depth_tx, uv);
bool all_deeper = all(greaterThan(vec4(gl_FragCoord.z), depths));
```

---

## 8. 语法速查表

### 数据类型

```glsl
// 基本
float x;        // 浮点数
int i;          // 整数
uint u;         // 无符号整数
bool b;         // 布尔

// 向量
vec2, vec3, vec4
ivec2, ivec3, ivec4
uvec2, uvec3, uvec4
bvec2, bvec3, bvec4

// 矩阵
mat2, mat3, mat4

// 采样器
sampler2D, sampler3D, samplerCube

// 结构体
struct MyStruct { vec3 pos; float val; };
```

### 限定符

```glsl
const       // 编译时常量
uniform     // CPU → GPU
in / out    // 着色器间传递
buffer      // SSBO（大数组）
location    // 属性绑定
binding     // UBO/SSBO 绑定
```

### Blender 库函数

```glsl
// 视图变换
drw_point_object_to_world(obj_pos)  // 对象→世界
drw_point_world_to_view(world_pos)  // 世界→视图
drw_point_view_to_homogenous(view_pos)  // 视图→齐次

// 视图信息
drw_view_position()      // 相机位置
drw_view_near()          // 近裁剪面
drw_view_far()           // 远裁剪面

// 颜色
encode_id_to_color(id)   // ID→颜色（选择）
non_linear_blend_color(c1, c2, f)  // 空间混合
```

---

**版本**: 1.0
**基于**: Blender 4.3 + GLSL 4.60
**创建时间**: 2025-12-17
