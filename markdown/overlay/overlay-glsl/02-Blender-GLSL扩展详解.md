# Blender GLSL扩展详解 

## 目录
- [1. 概述](#1-概述)
- [2. Blender GLSL架构](#2-blender-glsl架构)
  - [2.1. 着色器系统结构](#21-着色器系统结构)
  - [2.2. 多后端支持](#22-多后端支持)
  - [2.3. 代码生成机制](#23-代码生成机制)
- [3. 类型系统扩展](#3-类型系统扩展)
  - [3.1. 向量类型别名](#31-向量类型别名)
  - [3.2. 矩阵类型扩展](#32-矩阵类型扩展)
  - [3.3. 特殊类型定义](#33-特殊类型定义)
- [4. 扩展函数库](#4-扩展函数库)
  - [4.1. 数学函数库](#41-数学函数库)
  - [4.2. 几何处理函数](#42-几何处理函数)
  - [4.3. 纹理访问扩展](#43-纹理访问扩展)
- [5. 跨平台兼容性](#5-跨平台兼容性)
  - [5.1. OpenGL后端](#51-opengl后端)
  - [5.2. Vulkan后端](#52-vulkan后端)
  - [5.3. Metal后端](#53-metal后端)
- [6. 性能优化扩展](#6-性能优化扩展)
  - [6.1. 快速数学函数](#61-快速数学函数)
  - [6.2. 内存访问优化](#62-内存访问优化)
  - [6.3. 计算着色器优化](#63-计算着色器优化)
- [7. 代码对比分析](#7-代码对比分析)
  - [7.1. 标准GLSL vs Blender GLSL](#71-标准glsl-vs-blender-glsl)
  - [7.2. 向量操作对比](#72-向量操作对比)
  - [7.3. 矩阵操作对比](#73-矩阵操作对比)
- [8. 设计原理和动机](#8-设计原理和动机)
- [9. 最佳实践](#9-最佳实践)

## 1. 概述 

Blender GLSL是对标准GLSL的重大扩展，旨在提供跨图形API的兼容性、增强的性能和简化的开发体验。Blender的着色器系统通过抽象层和运行时代码生成，实现了单一源码支持OpenGL、Vulkan和Metal后端。

**核心特点**：
- 跨平台兼容性
- 类型别名系统
- 扩展数学库
- 性能优化函数
- 运行时代码生成

## 2. Blender GLSL架构 

### 2.1. 着色器系统结构 

Blender采用分层的着色器架构：

**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat.hh:11-18`
```cpp
#pragma once
#pragma runtime_generated
#include "gpu_shader_compat_cxx.hh"
// 运行时替换为特定后端实现
// #include "gpu_shader_compat_glsl.hh"
// #include "gpu_shader_compat_msl.hh"
```

这种设计允许在运行时选择合适的后端实现，而无需修改着色器源码。

### 2.2. 多后端支持 

**定义位置**: `source/blender/gpu/shaders/gpu_shader_glsl_extension.glsl:16-40`
```glsl
#if defined(GPU_OPENGL)
#  version 430
#  extension GL_ARB_shader_draw_parameters : enable
#  extension GL_ARB_shader_viewport_layer_array : enable
#elif defined(GPU_VULKAN)
#  version 450
#  extension GL_ARB_shader_draw_parameters : enable
#  extension GL_EXT_fragment_shader_barycentric : require
#endif
```

### 2.3. 代码生成机制 

Blender使用`#pragma runtime_generated`指令标记需要在运行时生成的文件，允许动态适配不同GPU架构。

## 3. 类型系统扩展 

### 3.1. 向量类型别名 

**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:43-51`
```glsl
#define float2 vec2
#define float3 vec3
#define float4 vec4
#define int2 ivec2
#define int3 ivec3
#define int4 ivec4
#define uint2 uvec2
#define uint3 uvec3
#define uint4 uvec4
```

这些别名提供了更直观的命名约定，与Blender C++代码保持一致。

**布尔向量类型**:
**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:38-41`
```glsl
#define bool2 bvec2
#define bool3 bvec3
#define bool4 bvec4
```

### 3.2. 矩阵类型扩展 

**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:63-71`
```glsl
#define float2x2 mat2x2
#define float3x3 mat3x3
#define float4x4 mat4x4
#define float2x3 mat2x3
#define float3x2 mat3x2
#define float2x4 mat2x4
#define float4x2 mat4x2
#define float3x4 mat3x4
#define float4x3 mat4x3
```

### 3.3. 特殊类型定义 

**小类型提升**:
**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:73-93`
```glsl
#define char int
#define short int
#define uchar uint
#define ushort uint
#define half float
```

**字符串类型**:
**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:194-208`
```glsl
struct string_t {
  uint hash;
};

uint as_uint(string_t str)
{
  return str.hash;
}
```

## 4. 扩展函数库 

### 4.1. 数学函数库 

**快速幂函数**:
**定义位置**: `source/blender/gpu/shaders/common/gpu_shader_math_base_lib.glsl:11-38`
```glsl
float pow2f(float x)
{
  return x * x;
}
float pow3f(float x)
{
  return x * x * x;
}
float pow4f(float x)
{
  return pow2f(pow2f(x));
}
float pow5f(float x)
{
  return pow4f(x) * x;
}
float pow6f(float x)
{
  return pow2f(pow3f(x));
}
float pow7f(float x)
{
  return pow6f(x) * x;
}
float pow8f(float x)
{
  return pow2f(pow4f(x));
}
```

这些函数避免了标准`pow()`函数的性能开销，对于整数幂次特别高效。

**通用数学工具**:
**定义位置**: `source/blender/gpu/shaders/common/gpu_shader_math_base_lib.glsl:40-124`
```glsl
float square(float v) { return v * v; }
float2 square(float2 v) { return v * v; }
float3 square(float3 v) { return v * v; }
float4 square(float4 v) { return v * v; }

float hypot(float x, float y)
{
  return sqrt(x * x + y * y);
}

int ceil_to_multiple(int a, int b)
{
  return ((a + b - 1) / b) * b;
}
```

### 4.2. 几何处理函数 

**矩阵重塑函数**:
**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:14-31`
```glsl
#define RESHAPE(name, mat_to, mat_from) \
  mat_to to_##name(mat_from m) \
  { \
    return mat_to(m); \
  }

RESHAPE(float2x2, mat2x2, mat3x3)
RESHAPE(float3x3, mat3x3, mat4x4)
RESHAPE(float4x4, mat4x4, mat2x2)
```

### 4.3. 纹理访问扩展 

**扩展纹理访问**:
**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:210-214`
```glsl
float4 texelFetchExtend(sampler2D samp, int2 texel, int lvl)
{
  texel = clamp(texel, int2(0), textureSize(samp, lvl).xy - 1);
  return texelFetch(samp, texel, lvl);
}
```

**阶段无关的内置函数**:
**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:219-229`
```glsl
#ifdef GPU_FRAGMENT_SHADER
#  define gpu_discard_fragment() discard
#  define gpu_dfdx(x) dFdx(x)
#  define gpu_dfdy(x) dFdy(x)
#  define gpu_fwidth(x) fwidth(x)
#else
#  define gpu_discard_fragment()
#  define gpu_dfdx(x) x
#  define gpu_dfdy(x) x
#  define gpu_fwidth(x) x
#endif
```

## 5. 跨平台兼容性 

### 5.1. OpenGL后端 

OpenGL 4.3是最低要求版本，支持以下扩展：
- `GL_ARB_shader_draw_parameters`: 绘制调用批处理
- `GL_ARB_shader_viewport_layer_array`: 分层渲染
- `GL_AMD_shader_explicit_vertex_parameter`: 重心坐标
- `GL_EXT_shader_framebuffer_fetch`: 子通道输入模拟
- `GL_ARB_shader_stencil_export`: 模板缓冲区导出

### 5.2. Vulkan后端 

Vulkan 1.0对应GLSL 450，包含：
- `GL_EXT_fragment_shader_barycentric`: 片段着色器重心坐标（必需）
- 相同的绘制参数和分层渲染支持

### 5.3. Metal后端 

通过MSL转换支持，包含Metal特定的构造函数宏：
**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:149-156`
```glsl
#define METAL_CONSTRUCTOR_1(class_name, t1, m1)
#define METAL_CONSTRUCTOR_2(class_name, t1, m1, t2, m2)
// ... 更多构造函数宏
```

## 6. 性能优化扩展 

### 6.1. 快速数学函数 

**自定义三角函数**:
**定义位置**: `source/blender/draw/engines/eevee/shaders/eevee_ambient_occlusion_lib.glsl:115-124`
```glsl
float sin_from_cos(float c)
{
  return sqrt(max(0.0f, 1.0f - square(c)));
}

float cos_from_sin(float s)
{
  return sqrt(max(0.0f, 1.0f - square(s)));
}
```

### 6.2. 内存访问优化 

**快速加载/存储**:
**定义位置**: `source/blender/gpu/shaders/gpu_shader_compat_glsl.glsl:99-102`
```glsl
#define imageStoreFast imageStore
#define imageLoadFast imageLoad
```

虽然目前在GLSL中等同于标准函数，但为其他后端提供了优化接口。

### 6.3. 计算着色器优化 

**计算着色器示例**:
**定义位置**: `source/blender/compositor/shaders/compositor_alpha_crop.glsl:11-19`
```glsl
void main()
{
  int2 texel = int2(gl_GlobalInvocationID.xy);
  bool is_inside = all(greaterThanEqual(texel, lower_bound)) && 
                   all(lessThan(texel, upper_bound));
  float4 color = is_inside ? texture_load(input_tx, texel) : float4(0.0f);
  imageStore(output_img, texel, color);
}
```

## 7. 代码对比分析 

### 7.1. 标准GLSL vs Blender GLSL 

| 特性 | 标准GLSL | Blender GLSL |
|------|----------|--------------|
| 向量类型 | `vec2, vec3, vec4` | `float2, float3, float4` |
| 整数向量 | `ivec2, ivec3, ivec4` | `int2, int3, int4` |
| 无符号向量 | `uvec2, uvec3, uvec4` | `uint2, uint3, uint4` |
| 矩阵类型 | `mat2, mat3, mat4` | `float2x2, float3x3, float4x4` |
| 字符串支持 | 无 | `string_t`（哈希） |
| 快速幂函数 | `pow(x, n)` | `pow2f(), pow3f(), ...` |

### 7.2. 向量操作对比 

**标准GLSL示例**:
```glsl
vec3 position = vec3(1.0, 2.0, 3.0);
vec3 velocity = normalize(position);
float length = length(velocity);
```

**Blender GLSL示例**:
```glsl
float3 position = float3(1.0f, 2.0f, 3.0f);
float3 velocity = normalize(position);
float length_sqr = length_square(position); // 扩展函数
float length = sqrt(length_sqr);
```

### 7.3. 矩阵操作对比 

**标准GLSL示例**:
```glsl
mat4 model = mat4(1.0);
mat3 normal = mat3(model);
```

**Blender GLSL示例**:
```glsl
float4x4 model = float4x4(1.0f);
float3x3 normal = to_float3x3(model); // 重塑函数
```

## 8. 设计原理和动机 

### 8.1. 跨平台需求

Blender需要支持多种图形API，主要原因：
1. **硬件兼容性**: 不同GPU对各个API的支持程度不同
2. **性能优化**: 某些操作在特定API上更高效
3. **未来准备**: 为新兴图形API做好准备

### 8.2. 开发效率考虑

**类型别名的优势**：
- 与C++代码风格一致
- 提高代码可读性
- 减少类型转换错误
- 简化跨语言接口

**扩展函数库的价值**：
- 避免重复实现常见数学运算
- 提供平台优化版本
- 统一数值精度处理

### 8.3. 性能优化策略

**快速数学函数**：
- 避免通用`pow()`函数的分支开销
- 利用乘法替代指数运算
- 针对常用幂次专门优化

**内存访问优化**：
- 提供无边界检查的快速访问接口
- 优化纹理采样模式
- 减少不必要的数据转换

## 9. 最佳实践 

### 9.1. 类型使用建议

```glsl
// 推荐的使用方式
float3 position;           // 位置向量
float4 color;              // 颜色（包含alpha）
float3x3 transform;        // 3x3变换矩阵
int2 tex_coord;            // 纹理坐标
bool4 mask;                // 布尔掩码
```

### 9.2. 性能优化技巧

```glsl
// 使用快速幂函数
float value_sqr = pow2f(value);    // 而不是 pow(value, 2.0)
float value_cube = pow3f(value);   // 而不是 pow(value, 3.0)

// 使用内置数学函数
float distance_sqr = length_square(vector);  // 避免sqrt直到需要
```

### 9.3. 跨平台兼容性

```glsl
// 使用阶段无关的函数
float gradient_x = gpu_dfdx(value);  // 在所有着色器阶段安全
float gradient_y = gpu_dfdy(value);

// 使用扩展纹理访问
float4 texel = texelFetchExtend(sampler, coord, lod);  // 自动边界检查
```

### 9.4. 资源管理

```glsl
// 使用Blender的资源访问器
sampler_get(create_info, texture_name)  // 统一的资源获取
image_get(create_info, image_name)       // 统一的图像获取
```

---

**总结**：Blender GLSL扩展系统通过精心设计的类型别名、扩展函数库和跨平台抽象层，为开发者提供了一个高效、一致且易于使用的着色器开发环境。这些扩展不仅提高了开发效率，还确保了Blender在各种硬件平台上的最佳性能表现。