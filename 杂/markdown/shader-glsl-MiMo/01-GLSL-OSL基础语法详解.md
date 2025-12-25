# GLSL 和 OSL 基础语法详解 - Blender 中的应用

## 目录

- [1. 概述](#概述)
- [2. GLSL 基础语法](#glsl-基础语法)
  - [2.1. 数据类型](#21-数据类型)
  - [2.2. 变量声明与作用域](#22-变量声明与作用域)
  - [2.3. 函数定义](#23-函数定义)
  - [2.4. 常用内置函数](#24-常用内置函数)
- [3. OSL 基础语法](#osl-基础语法)
  - [3.1. 数据类型](#31-数据类型)
  - [3.2. Shader 定义](#32-shader-定义)
  - [3.3. 参数与闭包](#33-参数与闭包)
  - [3.4. 标准库函数](#34-标准库函数)
- [4. Blender 特殊语法与扩展](#blender-特殊语法与扩展)
  - [4.1. Blender GPU Shader 系统](#41-blender-gpu-shader-系统)
  - [4.2. Blender OSL 扩展](#42-blender-osl-扩展)
- [5. 常见缩写详解](#5-常见缩写详解)
  - [5.1. 向量类型缩写](#51-向量类型缩写)
  - [5.2. 矩阵类型缩写](#52-矩阵类型缩写)
  - [5.3. 常用函数缩写](#53-常用函数缩写)
- [6. 代码示例](#6-代码示例)
  - [6.1. GLSL 实用函数示例](#61-glsl-实用函数示例)
  - [6.2. OSL 节点示例](#62-osl-节点示例)
- [7. 常见错误与最佳实践](#7-常见错误与最佳实践)
  - [7.1. 常见错误](#71-常见错误)
  - [7.2. 最佳实践](#72-最佳实践)

---

## 概述

本教程旨在帮助 Python 开发人员理解 GLSL（OpenGL Shading Language）和 OSL（Open Shading Language）的基础语法，特别针对 Blender 中的应用。尽管您可能熟悉 Python 和 C++ 基础，但 Shader 语言有其独特的范式和思维方式。

### GLSL vs OSL：核心区别

**GLSL (OpenGL Shading Language)**
- 用于实时渲染（GPU 加速）
- 应用于 Blender 的 EEVEE、视口渲染等
- 直接在图形管线中执行
- 没有光线追踪概念（主要用于光栅化）

**OSL (Open Shading Language)**
- 用于离线渲染（CPU/GPU 路径追踪）
- 应用于 Blender 的 Cycles 渲染器
- 基于物理的渲染（PBR）工作流
- 支持闭包（Closures）和光线追踪

> **关键理解**：就像 Python 有不同库（NumPy 用于数值计算，Pandas 用于数据处理）一样，GLSL 和 OSL 是针对不同渲染场景的"专用语言"。

---

## GLSL 基础语法

### 2.1. 数据类型

GLSL 是**强类型**语言，所有变量必须声明类型。这与 Python 的动态类型形成对比。

#### 标量 (Scalar Types)

```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_math_base_lib.glsl:11-38

// float: 单精度浮点数 (Python 中的 float)
float a = 0.5f;  // 注意末尾的 'f'，在 GLSL 中常用但可选

// int: 32位整数
int count = 10;

// bool: 布尔值
bool isActive = true;

// uint: 无符号整数 (常用于位运算)
uint flags = 0xFFu;
```

**Python 对比**：
```python
# Python
a = 0.5      # 动态类型
b = 10       # 自动推断为 int

# GLSL
float a = 0.5;  # 显式声明类型
int b = 10;       # 必须显式声明
```

#### 向量类型 (Vector Types)

向量是 GLSL 的核心概念，用于表示颜色、位置、法线等。

```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_common_math_utils.glsl:9-20

// 2D 向量 (常用于 UV 坐标)
float2 uv = float2(0.5, 0.5);
vec2 uv_alt = vec2(0.5, 0.5);  // vec2 是 float2 的别名

// 3D 向量 (常用于颜色、位置、法线)
float3 color = float3(1.0, 0.0, 0.0);  // 红色
float3 position = float3(0.0, 0.0, 0.0);
float3 normal = float3(0.0, 1.0, 0.0);  // 向上的法线

// 4D 向量 (常用于 RGBA 颜色 + Alpha)
float4 rgba = float4(1.0, 0.0, 0.0, 1.0);  // 不透明的红色
vec4 color_alt = vec4(1.0, 0.0, 0.0, 1.0);  // vec4 是 float4 的别名

// 向量组件访问（类似 Python 的元组解包）
float3 v = float3(1.0, 2.0, 3.0);
float x = v.x;  // 1.0
float y = v.y;  // 2.0
float z = v.z;  // 3.0

// 也可以使用 rgb 或 stpq 作为别名
float r = v.r;  // 1.0 (颜色语义)
float s = v.s;  // 1.0 (纹理坐标语义)

// 打包构造（Swizzling）
float4 rgba = float4(v, 1.0);  // float4(1.0, 2.0, 3.0, 1.0)
float2 xy = v.xy;  // float2(1.0, 2.0)
float3 yxz = v.yxz;  // float3(2.0, 1.0, 3.0) - 可以重新排列
```

#### 矩阵类型 (Matrix Types)

矩阵用于变换和图形计算。

```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_math_matrix_construct_lib.glsl

// 4x4 矩阵 (常用于 3D 变换)
mat4 transform = mat4(
    1.0, 0.0, 0.0, 0.0,  // 第一列
    0.0, 1.0, 0.0, 0.0,  // 第二列
    0.0, 0.0, 1.0, 0.0,  // 第三列
    0.0, 0.0, 0.0, 1.0   // 第四列
);

// 3x3 矩阵 (常用于法线变换)
mat3 rotation = mat3(
    1.0, 0.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 0.0, 1.0
);

// float3x3 是 Blender GPU 库中的类型别名
float3x3 identity = float3x3(1.0);
```

#### 数组类型

```glsl
// 固定大小数组
float points[4] = float[4](0.0, 1.0, 2.0, 3.0);

// 访问数组元素
float first = points[0];  // 0.0

// 纹理采样器数组 (常用于多纹理)
uniform sampler2D textures[8];
```

---

### 2.2. 变量声明与作用域

#### 变量命名规范

GLSL 使用 **snake_case** 命名法，这与 Python 一致：

```glsl
// 定位位置: source/blender/gpu/shaders/material/gpu_shader_material_base.glsl:12-20

// 变量定义（通常使用小写加下划线）
float math_value = 0.5f;
float3 input_color = float3(1.0, 0.0, 0.0);

// 函数参数（out 参数用于返回多个值）
void math_add(float a, float b, float c, out float result) {
    result = a + b;
}
// 使用: math_add(1.0, 2.0, 0.0, my_result);
```

#### 常见变量前缀

在 Blender 的 GPU shader 中，有命名约定：

```glsl
// uniform: 从 CPU 传递来的常量 (Python → GLSL)
uniform float time;           // 当前时间
uniform sampler2D texColor;   // 颜色纹理

// varying: 顶点着色器 → 片段着色器
varying float2 uvCoord;       // UV 坐标
varying float3 normal;        // 法线

// 形参和本地变量
void my_function(float input_param) {
    float local_var = input_param * 2.0;

    // 避免与关键字冲突的常见后缀
    float3 out_color;  // out 是关键字，所以用 out_color
}
```

#### 精度限定符

```glsl
// 高精度 (浮点运算推荐)
highp float precise_value;

// 中精度 (默认)
mediump float medium_value;

// 低精度 (颜色等不敏感数据)
lowp float color_value = 1.0;  // 对于 [0,1] 的颜色值足够
```

---

### 2.3. 函数定义

GLSL 函数定义与 C++ 类似，但有特殊的 `out` 参数机制。

#### 基本语法

```glsl
// 定位位置: source/blender/gpu/shaders/material/gpu_shader_material_base.glsl:12-30

// 返回单个值
float multiply(float a, float b) {
    return a * b;
}

// 使用 out 参数返回多个值 (Blender GPU 系统常用模式)
void math_multiply(float a, float b, float c, out float result) {
    result = a * b;  // 结果存储在 result 中
}

// 无返回值函数
void do_something(float3 color) {
    // 处理颜色
    color = color * 2.0;
}

// 函数重载（同一个函数名，不同参数类型）
float max(float a, float b) {
    return (a > b) ? a : b;
}

float3 max(float3 a, float3 b) {
    return float3(max(a.x, b.x), max(a.y, b.y), max(a.z, b.z));
}
```

#### 函数调用

```glsl
// 方式1: 传统 C 风格
float result;
math_multiply(2.0, 3.0, 0.0, result);  // result 现在是 6.0

// 方式2: 使用内置函数 (更常见)
float result = 2.0 * 3.0;

// 向量运算 (Python 风格的便利性)
float3 a = float3(1.0, 2.0, 3.0);
float3 b = float3(4.0, 5.0, 6.0);
float3 c = a + b;  // float3(5.0, 7.0, 9.0)
float3 d = a * b;  // float3(4.0, 10.0, 18.0) - 分量乘法

// 比较运算（返回的是 float，不是 bool，这是 GLSL 特性）
float result = step(0.5, 0.3);  // 0.0 (0.3 < 0.5)
```

---

### 2.4. 常用内置函数

GLSL 提供了丰富的数学函数库。以下是 Blender 中最常用的：

#### 向量运算函数

```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_math_utils.glsl:9-20

// 点积 (Dot Product) - 投影和夹角计算
float3 a = float3(1.0, 0.0, 0.0);
float3 b = float3(0.0, 1.0, 0.0);
float dot_result = dot(a, b);  // 0.0 (垂直)

// 叉积 (Cross Product) - 计算垂直向量
float3 normal = cross(a, b);  // float3(0.0, 0.0, 1.0)

// 长度 (Length) - 计算向量大小
float len = length(a);  // 1.0

// 标准化 (Normalize) - 使向量长度为 1
float3 normalized = normalize(a);  // float3(1.0, 0.0, 0.0)

// 定位位置: source/blender/gpu/shaders/common/gpu_shader_common_math_utils.glsl:15-20

// 距离 (Distance) - 两点间距离
float3 p1 = float3(0.0, 0.0, 0.0);
float3 p2 = float3(3.0, 4.0, 0.0);
float dist = distance(p1, p2);  // 5.0 (勾股定理)

// 反射 (Reflect) - 光线反射
float3 view = float3(0.0, 0.0, -1.0);
float3 normal = float3(0.0, 1.0, 0.0);
float3 reflected = reflect(view, normal);

// 折射 (Refract) - 光线折射
float3 refracted = refract(view, normal, 1.5);  // 1.5 = IOR
```

#### 三角函数

```glsl
// 定位位置: source/blender/gpu/shaders/material/gpu_shader_material_base.glsl:149-162

float angle = 3.14159 / 2.0;  // 90度

float sine = sin(angle);      // 1.0
float cosine = cos(angle);    // 0.0
float tangent = tan(angle);   // 大数值

// 反三角函数
float arcsine = asin(1.0);    // 1.5708 (π/2)
float arccosine = acos(0.0);  // 1.5708 (π/2)
float arctangent = atan(1.0); // 0.7854 (π/4)

// atan2(x, y) - 考虑象限的双参数反正切
float angle2 = atan2(y, x);   // 比 atan(y/x) 更安全
```

#### 数值操作函数

```glsl
// 定位位置: source/blender/gpu/shaders/material/gpu_shader_material_base.glsl:27-46

// 幂运算 (Power)
float p1 = pow(2.0, 3.0);     // 8.0

// 安全除法 (避免除零)
float safe_div = (b != 0.0) ? a / b : 0.0;

// 平方根
float sqrt_val = sqrt(4.0);   // 2.0
float inv_sqrt = inversesqrt(4.0);  // 0.5 (更快！)

// 混合/插值 (Mix)
float result = mix(0.0, 10.0, 0.5);  // 5.0
float3 color1 = float3(1.0, 0.0, 0.0);
float3 color2 = float3(0.0, 0.0, 1.0);
float3 blended = mix(color1, color2, 0.5);  // 紫色 (0.5, 0.0, 0.5)

// 限制范围 (Clamp)
float clamped = clamp(x, 0.0, 1.0);  // 确保 0 <= x <= 1

// 最大最小值
float max_val = max(a, b);
float min_val = min(a, b);
```

#### 面向 Python 开发者的快速对照表

| Python | GLSL | 说明 |
|--------|------|------|
| `math.sqrt(x)` | `sqrt(x)` | 平方根 |
| `math.pow(x, y)` | `pow(x, y)` | 幂运算 |
| `abs(x)` | `abs(x)` | 绝对值 |
| `max(a, b)` | `max(a, b)` | 最大值 |
| `min(a, b)` | `min(a, b)` | 最小值 |
| `math.sin(x)` | `sin(x)` | 正弦 |
| `math.cos(x)` | `cos(x)` | 余弦 |
| `np.dot(a, b)` | `dot(a, b)` | 点积 |
| `np.cross(a, b)` | `cross(a, b)` | 叉积 |
| `np.linalg.norm(v)` | `length(v)` | 向量长度 |
| `v / norm(v)` | `normalize(v)` | 标准化 |
| `np.clip(x, 0, 1)` | `clamp(x, 0.0, 1.0)` | 范围限制 |

---

## OSL 基础语法

### 3.1. 数据类型

OSL 的类型系统与 GLSL 相似，但增加了**闭包（Closure）**类型和更多图像处理相关的类型。

#### 基础类型

```osl
# 定位位置: intern/cycles/kernel/osl/shaders/node_principled_bsdf.osl:8-40

// 标量
float value = 0.5;  // OSL 默认就是 float，不需要 f 后缀
int count = 10;
string name = "material";

// 颜色 (Color spaces aware)
color black = color(0.0, 0.0, 0.0);
color white = color(1.0);  // 等同于 color(1.0, 1.0, 1.0)

// 向量 (3D 空间中的向量)
vector up = vector(0.0, 1.0, 0.0);

// 点 (3D 空间中的位置)
point origin = point(0.0, 0.0, 0.0);

// 法线 (表面法线)
normal n = normal(0.0, 1.0, 0.0);

// 矩阵
matrix identity = matrix(1.0);

// 闭包 (Closure) - OSL 独有的用于光线追踪的特殊类型
closure color BSDF = 0;  // 可以是 diffuse, glossy 等
```

**与 GLSL 的关键区别**：
- `float` 类型不需要 `f` 后缀
- 有明确的 `color`, `vector`, `point`, `normal` 类型（而 GLSL 都是 `float3`）
- `closure color` 是 OSL 特有的，用于构建材质

---

### 3.2. Shader 定义

#### 基本 Shader 结构

```osl
# 定位位置: intern/cycles/kernel/osl/shaders/node_math.osl:9-99

shader node_math(
    // 输入参数
    string math_type = "add",
    float Value1 = 0.5,
    float Value2 = 0.5,
    float Value3 = 0.5,

    // 输出参数
    output float Value = 0.0
)
{
    // Shader 主体
    if (math_type == "add")
        Value = Value1 + Value2;
    else if (math_type == "subtract")
        Value = Value1 - Value2;
    else if (math_type == "multiply")
        Value = Value1 * Value2;
    // ... 更多分支
}
```

#### Shader 参数类型

```osl
# 定位位置: intern/cycles/kernel/osl/shaders/node_principled_bsdf.osl:8-40

// 输入参数（可以在 Blender 的节点编辑器中连接）
shader principled_bsdf(
    // 标量参数
    float Roughness = 0.5,
    float Metallic = 0.0,

    // 颜色参数
    color BaseColor = color(0.8),

    // 向量参数
    vector SubsurfaceRadius = vector(1.0, 1.0, 1.0),

    // 字符串参数（枚举类型）
    string distribution = "multi_ggx",
    string subsurface_method = "random_walk",

    // 法线参数
    normal Normal = N,  // N 是内置变量，表面几何法线
    normal Tangent = normalize(dPdu),  // dPdu 是纹理切线

    // 输出参数
    output closure color BSDF = 0
)
{
    // Shader 实现...
}
```

**Blinn-Phong 简单示例**：

```osl
shader my_blinn_phong(
    color diffuse_color = color(0.8),
    color specular_color = color(1.0),
    float shininess = 20.0,
    normal Normal = N,
    output closure color BSDF = 0
)
{
    // Diffuse 部分
    closure color diffuse_term = diffuse_color * diffuse(Normal);

    // Specular 部分（简化）
    // 这里使用了 OSL 的闭包构建
    BSDF = diffuse_term;
}
```

---

### 3.3. 参数与闭包

#### 理解闭包 (Closure)

闭包是 OSL 中最难但最重要的概念。可以理解为：

> **闭包 = 材质行为的描述**（不是最终的颜色，而是"如何计算颜色"的规则）

```osl
# 定位位置: intern/cycles/kernel/osl/shaders/node_glossy_bsdf.osl

// 这个 Shader 输出一个 glossy（光泽）闭包
node_glossy_bsdf(
    color Color = color(1.0),
    float Roughness = 0.5,
    normal Normal = N,
    output closure color BSDF = 0
)
{
    // 闭包构建（不是直接计算颜色）
    BSDF = Color * microfacet_ggx(Normal, Roughness);
    // 等价于：material = base_color * glossy_distribution
}
```

闭包的组合：

```osl
// 定位位置: intern/cycles/kernel/osl/shaders/node_principled_bsdf.osl

// 混合多个闭包
BSDF = mix(BSDF, SubsurfBSDF, subsurface_weight);  // 混合

// 层叠（Layer）闭包
BSDF = layer(coat_weight * CoatBSDF, BSDF);  // 上层 + 下层

// 相加（Add）闭包
BSDF += EmissionStrength * EmissionColor * emission();  // 添加发光
```

#### 默认参数值

```osl
shader example(
    float value = 0.5,           // 默认值 0.5
    color col = color(1.0, 0.0, 0.0),  // 默认红色
    vector dir = vector(0, 1, 0),      // 默认向上
    string mode = "multiply",    // 默认字符串
    output float result = 0.0    // 输出默认为 0
)
{
    // 实现...
}
```

---

### 3.4. 标准库函数

OSL 提供了丰富的标准库，分为几个类别：

#### 数学函数

```osl
// 定位位置: intern/cycles/kernel/osl/shaders/node_math.osl

// 三角函数
float s = sin(angle);
float c = cos(angle);
float t = tan(angle);

// 向量运算
float d = dot(vector1, vector2);      // 点积
vector cross_vec = cross(v1, v2);      // 叉积
vector normalized = normalize(v);      // 标准化
float len = length(v);                 // 长度

// 安全运算（避免除零等问题）
float safe_div = safe_divide(a, b);    // a/b (b=0 时返回 0)
float safe_sqrt = safe_sqrt(x);        // sqrt(max(x,0))
float safe_log = safe_log(a, b);       // log(a)/log(b) (安全)

// 颜色相关
float lum = luminance(color);          // 亮度
color clamped = clamp(color, 0.0, 1.0); // 限制范围
```

#### 几何与变换

```osl
# 定位位置: intern/cycles/kernel/osl/shaders/node_vector_rotate.osl

// 旋转向量
vector rotated = rotate(vector, angle, point, axis);

// 欧拉角转矩阵
matrix rot = euler_to_mat(rotation_angle);

// 坐标变换
vector world_pos = transform("object", "world", point);

// 光线追踪相关
float fresnel = fresnel_dielectric_cos(cos_i, eta);  // 菲涅尔方程
bool backface = backfacing();  // 是否是背面
```

#### 文本与数据

```osl
// 字符串操作
string result = concat("Hello", " ", "World");  // 拼接
int length = strlen(result);                      // 字符串长度

// 纹理采样
color tex_color = texture("image.png", u, v);
color tex_obj = texture("image.png", u, v, "fill", fill_color);

// 文件 I/O
float data = getattribute("vertex_color");  // 获取顶点属性
```

---

## Blender 特殊语法与扩展

### 4.1. Blender GPU Shader 系统

Blender 为 GLSL 引入了特有的宏和函数简化 API。

#### 自动包含系统

```glsl
// 定位位置: source/blender/gpu/shaders/material/gpu_shader_material_base.glsl:1-10

// #pragma once 确保不被重复包含
#pragma once

// 包含 Blender 的兼容层
#include "gpu_shader_compat.hh"

// 包含数学库
#include "gpu_shader_math_base_lib.glsl"
#include "gpu_shader_math_safe_lib.glsl"
```

Blender 会自动在标准路径中寻找这些头文件：
- `source/blender/gpu/shaders/common/`
- `source/blender/gpu/shaders/`

#### Blender 特有的函数前缀

```glsl
// 定位位置: source/blender/gpu/shaders/material/gpu_shader_material_base.glsl:132-141

// float 类型的安全包裹（兼容 Python 的 wrap）
float wrap(float value, float max_val, float min_val) {
    float range = max_val - min_val;
    if (range == 0.0) return min_val;
    return value - range * floor((value - min_val) / range);
}

// "compatible_" 前缀：与 Cycles/OSL 行为一致
float compatible_pow(float a, float b) {
    // 处理负数和零的特殊情况
    return pow(max(a, 0.0), max(b, 0.0));
}
```

#### 常见 Blender GPU 库函数

```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_math_base_lib.glsl

// 优化的快速运算
float pow2f(float x) { return x * x; }  // 比 pow(x, 2.0) 快
float pow3f(float x) { return x * x * x; }
float pow4f(float x) { return pow2f(pow2f(x)); }

// 向量插值
float3 interpolate(float3 a, float3 b, float t) {
    return mix(a, b, t);
}

// 安全长度计算
template<typename VecT>
VecT normalize_and_get_length(VecT vector, out float out_length) {
    out_length = length_squared(vector);
    if (out_length > 1e-35f) {
        out_length = sqrt(out_length);
        return vector / out_length;
    }
    return VecT(0.0f);
}
```

#### Blender GPU 的混合模式函数

```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_common_mix_rgb.glsl:11-15

// Blender 特有的混合算法
void mix_blend(float fac, float4 col1, float4 col2, out float4 outcol) {
    outcol = mix(col1, col2, fac);
    outcol.a = col1.a;  // 保留原始 alpha
}

// 添加混合
void mix_add(float fac, float4 col1, float4 col2, out float4 outcol) {
    outcol = mix(col1, col1 + col2, fac);
    outcol.a = col1.a;
}

// 乘法混合
void mix_mult(float fac, float4 col1, float4 col2, out float4 outcol) {
    outcol = mix(col1, col1 * col2, fac);
    outcol.a = col1.a;
}
```

---

### 4.2. Blender OSL 扩展

#### Cycles 节点模板

Blender 的 Cycles OSL 节点通常遵循特定模式：

```osl
# 定位位置: intern/cycles/kernel/osl/shaders/node_math.osl:1-99

// 1. 包含标准库头文件
#include "node_math.h"      // 节点特定头文件
#include "stdcycles.h"      // Cycles 标准库

// 2. 同名 shader 定义（与节点名称匹配）
shader node_math(
    string math_type = "add",  // 枚举类型参数
    float Value1 = 0.5,
    float Value2 = 0.5,
    float Value3 = 0.5,
    output float Value = 0.0
)
{
    // 3. 使用大量 if-else 分支处理不同的操作类型
    if (math_type == "add")
        Value = Value1 + Value2;
    else if (math_type == "subtract")
        Value = Value1 - Value2;
    // ... 等等

    // 4. 确保处理无效参数
    else {
        warning("%s", "Unknown math operator!");
    }
}
```

#### 属性获取与内置变量

```osl
# 定位位置: intern/cycles/kernel/osl/shaders/node_geometry.osl

shader node_geometry(
    output float Position = 0.0,
    output float Normal = 0.0,
    // ...
)
{
    // 内置变量（类似 GLSL 的 varying）
    point P = transform("object", P);  // 对象空间位置
    vector N = normalize(N);           // 几何法线
    vector Ng = normalize(Ng);         // 面法线

    // 输入（来自 Blender）
    vector Tangent = normalize(dPdu);   // 切线
    vector Bitangent = normalize(dPdv); // 副切线

    // 纹理坐标
    float u = u;    // UV u 坐标
    float v = v;    // UV v 坐标

    // 属性查询
    float custom_attr = 0.0;
    getattribute("vertex_color", custom_attr);
}
```

#### 多通道输出

```osl
shader node_vector_math(
    vector Vector1 = vector(0.0),
    vector Vector2 = vector(0.0),
    output float Value = 0.0,      // 标量输出
    output vector Vector = vector(0.0)  // 向量输出
)
{
    // 可以同时输出多个值
    Value = length(Vector1);      // 输出标量
    Vector = normalize(Vector1);  // 输出向量
}
```

#### 纹理采样与颜色空间

```osl
# 定位位置: intern/cycles/kernel/osl/shaders/node_image_texture.osl

shader node_image_texture(
    string filename = "",
    float u = 0.0,
    float v = 0.0,
    output color Color = 0.0,
    output float Alpha = 1.0
)
{
    // 支持多种过滤和颜色空间选项
    Color = texture(filename, u, v,
                    "linear", true,      // 线性插值
                    "alpha", Alpha);     // 获取 alpha

    // 伽马校正
    Color = srgb_to_linear(Color);
}
```
---

## 5. 常见缩写详解

### 5.1. 向量类型缩写

| 缩写 | 全称 | 含义 | Python 等价 |
|------|------|------|-------------|
| **vec2 / float2** | Vector 2 | 2D 向量 (x,y) | `tuple[float, float]` 或 `numpy.array([x,y])` |
| **vec3 / float3** | Vector 3 | 3D 向量 (x,y,z) | `tuple[float, float, float]` |
| **vec4 / float4** | Vector 4 | 4D 向量 (x,y,z,w) | `tuple[float, float, float, float]` |

**使用示例**：
```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_common_math.glsl:15

// 常见场景
float3 position = position;   // 3D 坐标
float3 normal = normal;       // 法线 (单位向量)
float4 color = color;         // RGBA 颜色 (0-1)
float2 uv = uv_coord;         // 纹理坐标 (0-1)
```

---

### 5.2. 矩阵类型缩写

| 缩写 | 全称 | 含义 | 常用场景 |
|------|------|------|----------|
| **mat2 / float2x2** | 2x2 Matrix | 2x2 变换矩阵 | 2D 变换 |
| **mat3 / float3x3** | 3x3 Matrix | 3x3 变换矩阵 | 3D 旋转、缩放、法线变换 |
| **mat4 / float4x4** | 4x4 Matrix | 4x4 变换矩阵 | 3D 完整变换 (位置+旋转+缩放) |

**使用示例**：
```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_math_matrix_lib.glsl

// 单位矩阵（不进行任何变换）
mat4 identity = mat4(1.0);

// 3D 旋转矩阵（3x3 用于法线变换）
mat3 rotation = mat3(1.0, 0.0, 0.0,
                     0.0, 1.0, 0.0,
                     0.0, 0.0, 1.0);

// 矩阵乘法（变换应用）
float4 world_pos = transform_matrix * float4(obj_pos, 1.0);
```

---

### 5.3. 常用函数缩写

#### 数学函数简写

| 缩写 | 全称 | 功能详解 | 代码示例 |
|------|------|----------|----------|
| **dot** | Dot Product | 向量点积 (投影、夹角计算) | `float d = dot(a, b);` |
| **cross** | Cross Product | 向量叉积 (垂直向量、表面法线) | `float3 n = cross(a, b);` |
| **norm / normalize** | Normalization | 向量归一化 (长度 = 1) | `float3 v = normalize(v);` |
| **len / length** | Length | 向量长度 | `float l = length(v);` |
| **refl / reflect** | Reflection | 反射向量 (光反射) | `float3 r = reflect(incident, normal);` |
| **refr / refract** | Refraction | 折射向量 (光折射) | `float3 t = refract(incident, normal, ior);` |
| **mix / lerp** | Mix/Linear Interpolate | 线性插值 | `float3 c = mix(a, b, t);` |
| **step** | Step Function | 阶梯函数 (0 或 1) | `float v = step(edge, x);` |
| **abs** | Absolute | 绝对值 | `float v = abs(x);` |
| **clamp** | Clamp | 范围限制 | `float v = clamp(x, min, max);` |
| **min** | Minimum | 最小值 | `float v = min(a, b);` |
| **max** | Maximum | 最大值 | `float v = max(a, b);` |
| **pow** | Power | 幂运算 | `float v = pow(x, 2.0);` |
| **sqrt** | Square Root | 平方根 | `float v = sqrt(x);` |
| **inversesqrt** | Inverse Square Root | 平方根倒数 (优化) | `float v = inversesqrt(x);` |

**点积和叉积详解**：

```glsl
// 定位位置: source/blender/gpu/shaders/common/gpu_shader_math_utils.glsl:15-20

// === 点积 (dot) ===
// 计算两个向量的投影关系，返回标量
float3 light_dir = normalize(float3(1.0, 1.0, 1.0));
float3 normal = normalize(float3(0.0, 1.0, 0.0));

float intensity = dot(light_dir, normal);  // 0.577... (约 57.7% 光照)

// 用途1: 光照计算 (Lambertian)
float3 diffuse = base_color * max(0.0, dot(normal, light_dir));

// 用途2: 判断角度 (垂直时为 0，相同方向为 1)
float cos_theta = dot(normal, float3(0.0, 1.0, 0.0));
// cos_theta = 1.0 → 完全朝上
// cos_theta = 0.0 → 垂直
// cos_theta < 0.0 → 背面（在背面）

// 叉积 (cross) ===
// 计算垂直于两个向量的向量，返回向量
float3 tangent = float3(1.0, 0.0, 0.0);  // X 轴切线
float3 bitangent = float3(0.0, 0.0, 1.0); // Z 轴副切线

float3 normal = cross(tangent, bitangent);  // float3(0.0, -1.0, 0.0)

// 用途: 构建正交坐标系（TBN）
float3 T = normalize(tangent);
float3 B = normalize(bitangent);
float3 N = cross(T, B);  // 构建垂直于切平面的法线
```

#### 贝塞尔曲线/插值缩写

| 缩写 | 全称 | 功能 | 代码示例 |
|------|------|------|----------|
| **lerp** | Linear Interpolate | 线性插值 | `float v = lerp(a, b, t);` |
| **smoothstep** | Smooth Step | 平滑过渡 (Hermite 插值) | `float v = smoothstep(0.0, 1.0, x);` |

---

### 5.4. Blender 特有缩写

| 缩写 | 全称 | 含义 | Blender GPU 库位置 |
|------|------|------|-------------------|
| **float3x3** | 3x3 浮点矩阵 | 同 mat3 | gpu_shader_math_matrix_lib.glsl |
| **float4x4** | 4x4 浮点矩阵 | 同 mat4 | gpu_shader_math_matrix_transform_lib.glsl |
| **math_*** | Math functions | Blender 数学节点函数 | gpu_shader_material_base.glsl |
| **mix_* / col_*** | Color mixing | 颜色混合相关函数 | gpu_shader_common_mix_rgb.glsl |
| **rgb_to_hsv / hsv_to_rgb** | 颜色空间转换 | RGB ↔ HSV 转换 | gpu_shader_common_color_utils.glsl |

---

## 6. 代码示例

### 6.1. GLSL 实用函数示例

#### 示例 1: 简单的 Lambert 光照计算

**文件位置**: `E:\blender-git\blender\source\blender\gpu\shaders\common\gpu_shader_common_math.glsl`

```glsl
#version 330 core

// 计算漫反射光照强度
// 输入: 法线、光线方向
// 输出: 光照强度 (0.0 - 1.0)
float calculate_lambert_lighting(float3 normal, float3 light_dir) {
    // 标准化（确保是单位向量）
    float3 N = normalize(normal);
    float3 L = normalize(light_dir);

    // 点积计算夹角余弦，clamp 确保不会为负
    float intensity = max(0.0, dot(N, L));

    return intensity;
}

// 使用示例:
void main() {
    float3 surface_normal = float3(0.0, 1.0, 0.0);
    float3 light_direction = normalize(float3(1.0, 1.0, 0.0));

    float light = calculate_lambert_lighting(surface_normal, light_direction);
    // light = 0.707... (约 70.7%)
}
```

#### 示例 2: 颜色混合与 Gamma 校正

**文件位置**: `E:\blender-git\blender\source\blender\gpu\shaders\common\gpu_shader_common_color_utils.glsl`

```glsl
// 混合两个颜色并进行 Gamma 校正
float3 blend_with_gamma_correction(
    float3 color_a,
    float3 color_b,
    float factor
) {
    // 线性混合
    float3 linear_result = mix(color_a, color_b, factor);

    // Gamma 校正: linear → sRGB
    // 公式: x^(1/2.2) for x < 0.0031308
    float3 srgb_result;
    for (int i = 0; i < 3; i++) {
        float c = linear_result[i];
        if (c < 0.0031308) {
            srgb_result[i] = (c < 0.0f) ? 0.0f : c * 12.92f;
        } else {
            srgb_result[i] = 1.055f * pow(c, 1.0f / 2.4f) - 0.055f;
        }
    }

    return srgb_result;
}
```

#### 示例 3: 基于距离的衰减计算

**文件位置**: `E:\blender-git\blender\source\blender\gpu\shaders\common\gpu_shader_math_vector_lib.glsl`

```glsl
// 计算点光源距离衰减
float calculate_attenuation(float3 pixel_pos, float3 light_pos, float light_range) {
    float distance = length(pixel_pos - light_pos);

    // 避免除零
    if (distance > light_range) {
        return 0.0;
    }

    // 平滑衰减
    float t = distance / light_range;
    return 1.0 - t * t;  // 二次衰减
}

// 用途: 实时渲染中的点光源
```

#### 示例 4: 变换顶点位置

**文件位置**: `E:\blender-git\blender\source\blender\gpu\shaders\common\gpu_shader_math_matrix_transform_lib.glsl`

```glsl
// 应用 4x4 变换矩阵
float4 transform_vertex(float3 position, mat4 transform_matrix) {
    // 将 3D 点转换为齐次坐标 (x, y, z, w=1)
    float4 pos = float4(position, 1.0);

    // 矩阵乘法
    return transform_matrix * pos;
}

// 平移顶点
float3 translate_vertex(float3 position, float3 translation) {
    return position + translation;
}

// 旋转顶点（使用 3x3 矩阵，保持 w=1 不变）
float3 rotate_vertex(float3 position, mat3 rotation_mat) {
    return rotation_mat * position;
}
```

---

### 6.2. OSL 节点示例

#### 示例 1: 自定义混合节点

**文件位置**: `E:\blender-git\blender\intern\cycles\kernel\osl\shaders\node_mix_color.osl`

```osl
#include "node_mix.h"
#include "stdcycles.h"

// 简单的混合节点，支持不同混合模式
shader my_custom_mix(
    color Color1 = color(0.8, 0.8, 0.8),
    color Color2 = color(0.2, 0.2, 0.2),
    float Factor = 0.5,
    string MixMode = "mix",  // "mix", "add", "multiply"
    output color Result = 0.0
)
{
    // 将 factor 裁剪到 0-1 范围
    float fac = clamp(Factor, 0.0, 1.0);

    if (MixMode == "mix") {
        // 标准线性混合
        Result = mix(Color1, Color2, fac);
    }
    else if (MixMode == "add") {
        // 相加混合
        Result = Color1 + fac * Color2;
    }
    else if (MixMode == "multiply") {
        // 相乘混合
        Result = Color1 * (1.0 - fac + fac * Color2);
    }
    else {
        warning("Unknown mix mode: %s", MixMode);
        Result = Color1;
    }
}
```

#### 示例 2: 简单的菲涅尔发光节点

**文件位置**: `E:\blender-git\blender\intern\cycles\kernel\osl\shaders\node_fresnel.osl`

```osl
#include "node_fresnel.h"
#include "stdcycles.h"

shader simple_fresnel_glow(
    float IOR = 1.45,                    // 折射率
    color GlowColor = color(1.0, 0.5, 0.0),  // 发光颜色
    float Power = 2.0,                   // 强度
    normal Normal = N,                   // 表面法线
    output closure color BSDF = 0        // 输出闭包
)
{
    // 计算法线与视角的点积
    float cosi = dot(I, Normal);

    // 计算菲涅尔项
    float eta = backfacing() ? 1.0 / IOR : IOR;
    float fresnel = fresnel_dielectric_cos(cosi, eta);

    // 菲涅尔增强效果：边缘发光
    // F * (1.0 - cos) 更强烈的边缘效果
    float edge_glow = pow(fresnel, Power);

    // 组合材质：基础颜色 + 发光
    // 闭包构建：diffuse + emission
    closure color base = color(0.2) * diffuse(Normal);
    closure color glow = edge_glow * GlowColor * emission();

    BSDF = base + glow;
}
```

#### 示例 3: 法线贴图处理器

**文件位置**: `E:\blender-git\blender\intern\cycles\kernel\osl\shaders\node_normal_map.osl`

```osl
#include "stdcycles.h"

shader my_normal_map_processor(
    color Color = color(0.5, 0.5, 1.0),  // RGB 法线贴图
    float Strength = 1.0,                // 强度
    normal Normal = N,                   // 原始法线
    vector Tangent = normalize(dPdu),    // 切线
    output normal OutNormal = N          // 输出变换后的法线
)
{
    // 从 [0,1] 映射到 [-1,1]
    vector normal_map = 2.0 * (Color - 0.5);

    // 计算副切线（Bitangent）
    vector bitangent = cross(Tangent, Normal);

    // 构建 TBN 矩阵 (Tangent-Bitangent-Normal)
    // 将切线空间法线转换到世界空间
    vector new_normal =
        normal_map.x * Tangent +
        normal_map.y * bitangent +
        normal_map.z * Normal;

    // 应用强度和归一化
    OutNormal = normalize(mix(Normal, new_normal, Strength));
}
```

#### 示例 4: 程序化噪波纹理

**文件位置**: `E:\blender-git\blender\intern\cycles\kernel\osl\shaders\node_noise_texture.osl`

```osl
#include "stdcycles.h"

shader procedural_noise(
    point Position = P,           // 位置（通常是对象坐标）
    float Scale = 1.0,            // 缩放
    float Detail = 2.0,           // 细节级别
    float Roughness = 0.5,        // 粗糙度
    output color Color = 0.0,     // 输出颜色
    output float Fac = 0.0        // 输出数值
)
{
    // 基于 Perlin 噪波
    // 实际实现使用 Cycles 内置函数

    // 简单示例：手动实现的噪波（示意）
    point p = Position * Scale;

    // 获取噪波值
    float noise_val = noise("perlin", p);

    // 增加细节层次（分形噪声）
    float total = noise_val;
    float amplitude = 1.0;
    float frequency = 1.0;

    for (int i = 0; i < 5; i++) {
        if (Detail <= 0.0) break;

        frequency *= 2.0;
        amplitude *= Roughness;

        total += noise("perlin", p * frequency) * amplitude;
        Detail -= 1.0;
    }

    // 输出结果
    Fac = clamp(total, 0.0, 1.0);
    Color = color(Fac);
}
```

---

## 7. 常见错误与最佳实践

### 7.1. 常见错误

#### 错误 1: 忘记初始化变量

```glsl
// ❌ 错误代码
void calculate(float x, out float result) {
    result = process(x);  // 可能忘记赋值
}

// 如果分支没有覆盖所有情况
void math_mix(float a, float b, string mode, out float result) {
    if (mode == "add") {
        result = a + b;
    }
    // ❌ 错误：mode 为 "multiply" 时，result 未被初始化！
}
```

**正确写法**：
```glsl
// ✅ 正确
void math_mix(float a, float b, string mode, out float result) {
    result = 0.0;  // 先初始化默认值

    if (mode == "add") {
        result = a + b;
    } else if (mode == "multiply") {
        result = a * b;
    } else {
        // 处理未知情况
        result = 0.0;
    }
}

// 或使用 Blender GPU 风格（一次性赋值）
void math_add(float a, float b, float c, out float result) {
    result = a + b;  // 明确的单路径
}
```

---

#### 错误 2: 除零错误

```glsl
// ❌ 危险代码
float x = 0.0;
float y = 1.0 / x;  // GPU 会崩溃或返回 NaN
```

**正确写法**：
```glsl
// ✅ Blender GPU 安全除法（gpu_shader_math_safe_lib.glsl）
float safe_divide(float a, float b) {
    return (b != 0.0) ? a / b : 0.0;
}

// ✅ 或者用 step 函数优化（GPU 更高效）
float result = a / (b + 1e-10);  // 添加微小偏移
```

---

#### 错误 3: 负数的分数次幂

```glsl
// ❌ 问题代码
float x = -2.0;
float y = 0.5;
float result = pow(x, y);  // NaN (负数开方)
```

**正确写法**：
```glsl
// ✅ Blender 兼容的幂运算
float compatible_pow(float a, float b) {
    if (a >= 0.0) {
        return pow(a, b);
    } else {
        // 只处理整数次幂或特殊情况
        float fraction = mod(abs(b), 1.0);
        if (fraction > 0.999f || fraction < 0.001f) {
            return pow(a, floor(b + 0.5f));
        } else {
            return 0.0;
        }
    }
}
```

---

#### 错误 4: 浮点精度问题（尤其是法线）

```glsl
// ❌ 浮点漂移
float3 normal = float3(0.001, 0.999, 0.000);
// 长度可能不再是 1.0，导致光照计算错误

float len = length(normal);  // 0.9990005，不是 1.0
```

**正确写法**：
```glsl
// ✅ 始终归一化
float3 safe_normalize(float3 v) {
    float len = dot(v, v);  // 长度平方，更高效
    if (len > 1e-35) {
        return v * inversesqrt(len);  // 1/sqrt(len) 更快
    }
    return float3(0.0);  // 零向量处理
}

// 使用
float3 normal = safe_normalize(raw_normal);
```

---

#### 错误 5: 访问向量越界

```glsl
// ❌ 越界访问
float3 color = float3(1.0, 0.0, 0.0);
float alpha = color.a;  // float3 没有 .a，只能访问 .x/.y/.z
```

**正确写法**：
```glsl
// ✅ 类型匹配
float4 rgba = float4(1.0, 0.0, 0.0, 1.0);
float alpha = rgba.a;   // ✅ 正确

float3 rgb = float3(1.0, 0.0, 0.0);
float r = rgb.r;        // ✅ float3 可以用 .r/.g/.b
```

---

#### OSL 专属错误

##### 错误 6: 闭包类型错误

```osl
// ❌ 错误：不能直接返回 float
shader example(output closure color BSDF = 0) {
    float value = 0.5;
    BSDF = value;  // 错误！不能将 float 赋值给 closure
}

// ✅ 正确：构建闭包
shader example(output closure color BSDF = 0) {
    float value = 0.5;
    BSDF = value * diffuse(N);  // value * diffuce = closure
}
```

##### 错误 7: 字符串比较遗漏括号

```osl
// ❌ 错误
shader test(string mode = "add", output float res = 0.0) {
    if (mode == "add") res = 1.0;  // 某些 OSL 版本需要括号
}

// ✅ 保险写法
shader test(string mode = "add", output float res = 0.0) {
    if (mode == "add") {
        res = 1.0;
    }
}
```

---

### 7.2. 最佳实践

#### 1. 使用 Blender 的安全数学库

**始终包含安全库**：
```glsl
// ✅ 优先包含 Blender 提供的 safe 库
#include "gpu_shader_math_safe_lib.glsl"

// 避免手动写除零、负数平方根等检查
float sum = safe_divide(num, den);
float root = safe_sqrt(val);
```

**对比**：
- ❌ 手动检查：`if (b != 0.0) { return a/b; } else { return 0.0; }`
- ✅ 简洁调用：`safe_divide(a, b)`

---

#### 2. Leveraging 向量化操作

```glsl
// ❌ 展开循环（慢）
float3 result;
result.x = a.x * b.x;
result.y = a.y * b.y;
result.z = a.z * b.z;

// ✅ 向量化（快，且代码简洁）
float3 result = a * b;  // GPU 会并行计算

// Python 对比，GLSL 类似 numpy 的广播
// Python: a * b  (numpy array)
// GLSL:   a * b  (float3 operation)
```

---

#### 3. 函数命名保持语义一致

**Blender GPU 风格**：
```glsl
// ✅ 清晰的函数命名
void rgb_to_hsv(float4 rgb, out float4 outcol);  // 明确的输入输出关系
void vector_normalize(float3 normal, out float3 outnormal);

// ✅ 使用 type_ 前缀表示操作对象
void math_add(float a, float b, float c, out float result);
void vector_add(float3 a, float3 b, out float3 result);  // 如果有专门的向量函数
```

---

#### 4. OSL 最佳实践

**保持 shader 纯函数特性**：
```osl
// ✅ 纯函数：给定相同输入，总是相同输出
shader my_node(float input, output float result) {
    result = input * 2.0;  // 纯操作
}

// ❌ 好的做法（避免）
shader my_node(float input, output float result) {
    static float cache = 0.0;  // 避免状态（除非有特殊需求）
    cache += input;  // 可能导致不可预期的副作用
    result = cache;
}
```

**处理边缘情况**：
```osl
shader safe_mix(color a, color b, float factor, output color result) {
    // 限制输入范围
    factor = clamp(factor, 0.0, 1.0);

    // 确保颜色不为负
    color safe_a = max(a, color(0.0));
    color safe_b = max(b, color(0.0));

    result = mix(safe_a, safe_b, factor);
}
```

---

#### 5. GPU 性能优化技巧

**减少分支（Branch Divergence）**：
```glsl
// ❌ GPU 可能不友好（所有线程同步执行分支）
float result;
if (mode == 0) { result = a + b; }
else if (mode == 1) { result = a - b; }
else if (mode == 2) { result = a * b; }

// ✅ 使用混合函数（更适合 GPU）
float result = mix(a + b, a * b, step(0.5, mode));  // 简化示例

// ✅ 或者在 GLSL 中使用三元运算符
float result = (mode == 0) ? a + b :
               (mode == 1) ? a - b : a * b;
```

**减少纹理采样**：
```glsl
// ✅ 合并采样
// 一次采样获取多个值（如果可能）
float4 combined = texture(sampler, uv);
float red   = combined.r;
float alpha = combined.a;

// ❌ 避免重复采样同一个纹理
float red = texture(sampler, uv).r;
float alpha = texture(sampler, uv).a;  // 第二次采样 = 性能浪费
```

---

#### 6. 调试与注释习惯

```glsl
// ✅ 使用 Blender 调试库
#include "gpu_shader_print_lib.glsl"

void debug_color(float3 color) {
    // 在调试模式下打印颜色值
    print("Color: %f %f %f", color.r, color.g, color.b);
}

// ✅ 清晰的文档注释
/**
 * 计算 Lambert 漫反射光照
 * @param normal 表面法线 (必须归一化)
 * @param light_dir 光照方向 (会被归一化)
 * @return 光照强度 [0.0, 1.0]
 */
float lambert(float3 normal, float3 light_dir) {
    return max(0.0, dot(normalize(normal), normalize(light_dir)));
}
```

---

#### 7. BLI 库函数的使用

**总是使用 Blender 的 math 库**：
```glsl
✔️ 使用：len = length_squared(v);  // 避免 sqrt
❌ 避免：len = sqrt(v.x*v.x + v.y*v.y + v.z*v.z);  // 重复造轮子

✔️ 使用：float l = length(v);  // 可读性好
❌ 避免：float l = sqrt(dot(v, v));  // 缺少意图表达
```

**Blender GPU 头文件优先级**：
1. `gpu_shader_compat.hh` - 所有 shader 的基础
2. `gpu_shader_math_base_lib.glsl` - 数学运算
3. `gpu_shader_math_safe_lib.glsl` - 安全数学
4. `gpu_shader_common_*.glsl` - 特定工具集

---

## 总结

### 核心要点回顾

1. **类型严格性**：GLSL/OSL 是强类型语言，所有变量必须显式声明类型
2. **向量思维**：理解 `float3`, `mat4` 等类型的操作是并行的（SIMD）
3. **安全第一**：始终使用安全除法，处理边界条件
4. **命名约定**：使用 snake_case，函数名清晰表达意图

### Python 开发者的思维转换

| Python 习惯 | GLSL/OSL 适配 |
|-------------|---------------|
| 动态类型 `x = 1.0` | 强制类型 `float x = 1.0;` |
| 列表操作 `[x, y, z]` | 向量运算 `float3 v = (x, y, z);` |
| List Comprehension | 向量化操作 `result = a * b + c;` |
| Handles None | 显式检查 `if (b != 0.0)` |
| Exceptions | 限制值 `clamp(value, 0.0, 1.0)` |

### Blender 开发者的速查表

**GLSL 常用**：
- 变换：`transform(matrix, vector)`
- 光照：`dot(normal, light_dir)` + `clamp()`
- 颜色：`mix(color_a, color_b, factor)`
- 安全：`safe_divide()`, `inversesqrt()`

**OSL 常用**：
- 闭包：`closure = color * bsdf(N, roughness)`
- 混合：`BSDF = mix(BSDF, new_clojure, weight)`
- 层叠：`BSDF = layer(front, BSDF)`
- 查询：`getattribute("name", result)`

---

## 附录：快速参考

### GLSL 内置变量（Blender 重要）

| 变量名 | 类型 | 含义 | 用途 |
|--------|------|------|------|
| `gl_FragCoord` | vec4 | 片段坐标 | 屏幕空间计算 |
| `gl_Position` | vec4 | 顶点位置 | 顶点着色器输出 |
| `uv` | vec2 | 纹理坐标 | UV 映射 |
| `position` | vec3 | 顶点位置 | 3D 坐标 |
| `normal` | vec3 | 法线 | 光照计算 |
| `color` | vec4 | 顶点颜色 | 着色 |

### OSL 内置变量

| 变量名 | 类型 | 含义 | 用途 |
|--------|------|------|------|
| `P` | point | 位置 | 几何查询 |
| `I` | vector | 视角方向 | 菲涅尔计算 |
| `N` | normal | 几何法线 | 基础光照 |
| `dPdu`, `dPdv` | vector | 切线 | 切线空间 |
| `u`, `v` | float | UV 坐标 | 纹理采样 |

---

**文档版本**：Blender 4.2+
**参考来源**：`source/blender/gpu/shaders/material/gpu_shader_material_base.glsl`、`intern/cycles/kernel/osl/shaders/` 等核心文件

---

*Tutorial compiled for Python developers transitioning to rendering shader languages. Green text indicates Python parallels. Orange text indicates C++ style but with `float` types.*