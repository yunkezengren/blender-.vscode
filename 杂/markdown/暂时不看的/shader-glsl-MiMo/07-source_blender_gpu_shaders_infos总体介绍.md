# 006-source_blender_gpu_shaders_infos 总体介绍

**文档编号：** 006
**文件名：** `006-source_blender_gpu_shaders_infos总体介绍.md`
**存放路径：** `.vscode/shader-glsl-MiMo/`
**最后更新：** 2025-12-18

---

## 目录

1. [infos 目录的作用和重要性](#1-infos-目录的作用和重要性)
2. [信息文件的格式规范](#2-信息文件的格式规范)
3. [所有 .info (.hh) 文件的解析](#3-所有-info-hh-文件的解析)
4. [每个文件的具体作用](#4-每个文件的具体作用)
5. [系统如何使用这些文件](#5-系统如何使用这些文件)
6. [配置文件的代码示例](#6-配置文件的代码示例)

---

## 1. infos 目录的作用和重要性

### 1.1 位置和结构

```plaintext
blender/source/blender/gpu/shaders/infos/
├── gpu_interface_infos.hh           # 接口定义（平滑/平面/透视差值）
├── gpu_shader_create_info.hh        # 核心宏定义和数据结构
├── gpu_clip_planes_infos.hh         # 裁剪平面共享信息
├── gpu_srgb_to_framebuffer_space_infos.hh  # 颜色空间转换
├── gpu_shader_2D_image_infos.hh     # 2D 图像着色器
├── gpu_shader_3D_flat_color_infos.hh # 3D 平面颜色着色器
├── gpu_shader_fullscreen_infos.hh   # 全屏着色器
├── gpu_shader_test_infos.hh         # 测试着色器（包含 compute 示例）
└── ... (其他 40+ 个信息文件)
```

### 1.2 核心作用

**infos 目录是 Blender GPU 着色器系统的"配置中心"**，它实现了以下关键功能：

1. **声明式着色器定义**：通过宏定义而不是手动编写 GLSL 代码来描述着色器
2. **类型安全**：在编译期检查资源绑定和接口匹配
3. **跨平台统一**：同一套定义可生成 OpenGL、Vulkan、Metal 等后端的着色器代码
4. **资源管理**：统一管理纹理、缓冲区、统一变量等 GPU 资源
5. **模块化组合**：通过 `ADDITIONAL_INFO` 实现着色器片段的复用

### 1.3 重要性

**为什么需要这套系统？**

| 传统方式 | Info 文件方式 |
|---------|--------------|
| 手动编写多种后端 GLSL | 一套定义，多后端生成 |
| 手动管理资源绑定 | 自动资源位置分配 |
| 硬编码 uniform 变量 | 声明式 push constant/uniform buffer |
| 难以复用代码 | 模块化组合 |
| 运行时错误 | 编译期检查 |

---

## 2. 信息文件的格式规范

### 2.1 文件头结构

每个 `.hh` 文件都遵循严格的模板：

```cpp
/* SPDX-FileCopyrightText: 2022 Blender Authors
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup gpu
 */

#ifdef GPU_SHADER
#  pragma once
#  include "gpu_shader_compat.hh"
#  include "GPU_shader_shared.hh"  // 共享类型定义
#endif

#include "gpu_interface_infos.hh"  // 接口定义
#include "gpu_shader_create_info.hh" // 核心宏
```

### 2.2 核心宏定义

#### 2.2.1 着色器创建信息

```cpp
GPU_SHADER_CREATE_INFO(shader_name)
```

**完整生命周期：**
```cpp
GPU_SHADER_CREATE_INFO(gpu_shader_3D_flat_color)
  /* 1. 输入定义 */
  VERTEX_IN(0, float3, pos)
  VERTEX_IN(1, float4, color)

  /* 2. 输出接口 */
  VERTEX_OUT(flat_color_iface)
  FRAGMENT_OUT(0, float4, fragColor)

  /* 3. 资源绑定 */
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  PUSH_CONSTANT(float, size)

  /* 4. 源文件引用 */
  VERTEX_SOURCE("gpu_shader_3D_flat_color_vert.glsl")
  FRAGMENT_SOURCE("gpu_shader_flat_color_frag.glsl")

  /* 5. 额外信息（模块化） */
  ADDITIONAL_INFO(gpu_srgb_to_framebuffer_space)

  /* 6. 编译选项 */
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()
```

#### 2.2.2 接口定义（阶段间通信）

```cpp
/* 定义平滑插值接口 */
GPU_SHADER_INTERFACE_INFO(smooth_color_iface)
  SMOOTH(float4, finalColor)
GPU_SHADER_INTERFACE_END()

/* 定义平面插值接口（不进行插值） */
GPU_SHADER_INTERFACE_INFO(flat_color_iface)
  FLAT(float4, finalColor)
GPU_SHADER_INTERFACE_END()

/* 定义透视校正插值 */
GPU_SHADER_INTERFACE_INFO(no_perspective_color_iface)
  NO_PERSPECTIVE(float4, finalColor)
GPU_SHADER_INTERFACE_END()
```

**插值类型说明：**
- `SMOOTH`：标准线性插值（默认）
- `FLAT`：平面插值，不进行插值（使用块中第一个顶点的值）
- `NO_PERSPECTIVE`：禁用透视校正的插值

### 2.3 资源绑定宏

#### 2.3.1 Push Constants（推送常量）

推送常量是最高效的每帧更新方式（适合少量、频繁变化的数据）：

```cpp
/* 单个值 */
PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
PUSH_CONSTANT(float, lineWidth)
PUSH_CONSTANT(bool, enableSmoothing)

/* 数组 */
PUSH_CONSTANT_ARRAY(float4, parameters, 12)
PUSH_CONSTANT_ARRAY(float4, parameters, MAX_PARAM)  // 使用宏定义大小
```

**使用限制：**
- 总大小通常受限（OpenGL 约 128-256 字节，Vulkan 更大）
- 适合每对象/每绘制调用的数据

#### 2.3.2 Uniform Buffers（统一缓冲区）

适合较大数据量，频率较低：

```cpp
/* 普通 Uniform Buffer */
UNIFORM_BUF(0, GPencilStrokeData, gpencil_stroke_data)

/* 带更新频率声明 */
UNIFORM_BUF_FREQ(1, GPUClipPlanes, clipPlanes, PASS)
```

**更新频率（Frequency）：**
- `PASS`：每渲染 pass 更新一次
- `GEOMETRY`：每个几何体更新一次
- `FRAME`：每帧更新一次

#### 2.3.3 Storage Buffers（存储缓冲区）

读写缓冲区，适合大规模数据：

```cpp
/* 只读 */
STORAGE_BUF(0, read, float, pos[])

/* 只写 */
STORAGE_BUF(0, write, uint, out_indices[])

/* 读写 */
STORAGE_BUF(0, read_write, SeqScopeRasterData, raster_buf[])

/* 带频率声明 */
STORAGE_BUF_FREQ(GPU_SSBO_POLYLINE_POS_BUF_SLOT,
                 read, float, pos[], GEOMETRY)
```

#### 2.3.4 采样器（Samplers）

纹理采样器绑定：

```cpp
SAMPLER(0, sampler2D, image)
SAMPLER(1, sampler2D, normalMap)

/* 带频率 */
SAMPLER_FREQ(0, sampler2D, albedo, PASS)
```

#### 2.3.5 图像（Image Load/Store）

GPU Image 对象（用于计算着色器）：

```cpp
IMAGE(1, SFLOAT_32_32_32_32, write, image1D, img_output)
IMAGE(1, UINT_32, read_write, uimage2DAtomic, img_atomic_2D)
```

**参数说明：**
- Slot: 绑定槽位
- Format: 纹理格式（如 SFLOAT_32_32_32_32 表示 4 通道 32 位浮点）
- Qualifiers: read / write / read_write
- Type: 图像类型（image1D, image2D, uimage2DAtomic 等）

### 2.4 计算着色器专用

```cpp
/* 工作组大小定义 */
LOCAL_GROUP_SIZE(16, 16, 1)

/* 计算源文件 */
COMPUTE_SOURCE("gpu_shader_sequencer_scope_comp.glsl")

/* 群组共享内存 */
GROUP_SHARED(float, sharedCache[256])
```

### 2.5 预处理器定义

```cpp
/* 简单定义 */
DEFINE("USE_special_feature")

/* 带值的定义 */
DEFINE_VALUE("MAX_PARAM", "12")
DEFINE_VALUE("widgetID", "gl_InstanceID")

/* 条件编译 */
#ifdef GLSL_CPP_STUBS
#  define USE_WORLD_CLIP_PLANES
#endif
```

### 2.6 特殊功能

#### 2.6.1 专用常量（Specialization Constants）

运行时可动态编译优化的常量（Vulkan/Metal）：

```cpp
SPECIALIZATION_CONSTANT(float, float_in, 2)
SPECIALIZATION_CONSTANT(uint, uint_in, 3)
SPECIALIZATION_CONSTANT(int, int_in, 4)
SPECIALIZATION_CONSTANT(bool, bool_in, true)
```

#### 2.6.2 编译期常量（Compilation Constants）

编译时确定的值：

```cpp
COMPILATION_CONSTANT(float, my_value, 3.14)
```

#### 2.6.3 内置功能启用

```cpp
BUILTINS(BuiltinBits::INSTANCE_ID)
BUILTINS(BuiltinBits::CLIP_DISTANCES)
```

**常用内置：**
- `INSTANCE_ID`：gl_InstanceID
- `CLIP_DISTANCES`：gl_ClipDistance
- `POINT_SIZE`：gl_PointSize
- `TEXTURE_ATOMIC`：纹理原子操作

### 2.7 继承和组合

```cpp
/* 基础定义 */
GPU_SHADER_CREATE_INFO(gpu_shader_3D_polyline)
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  STORAGE_BUF_FREQ(GPU_SSBO_POLYLINE_POS_BUF_SLOT, read, float, pos[], GEOMETRY)
  /* ... */
GPU_SHADER_CREATE_END()

/* 继承并添加功能 */
GPU_SHADER_CREATE_INFO(gpu_shader_3D_polyline_uniform_color)
  DO_STATIC_COMPILATION()
  DEFINE("UNIFORM")
  PUSH_CONSTANT(float4, color)
  ADDITIONAL_INFO(gpu_shader_3D_polyline)  /* 继承所有配置 */
GPU_SHADER_CREATE_END()

/* 继承多重信息 */
GPU_SHADER_CREATE_INFO(gpu_shader_3D_flat_color_clipped)
  ADDITIONAL_INFO(gpu_shader_3D_flat_color)
  ADDITIONAL_INFO(gpu_clip_planes)
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()
```

---

## 3. 所有 .info (.hh) 文件的解析

### 3.1 基础接口和共享信息

| 文件名 | 作用 |
|--------|------|
| `gpu_interface_infos.hh` | 定义所有预设的接口（平滑/平面/透视差值） |
| `gpu_shader_create_info.hh` | 核心宏定义系统 |
| `gpu_clip_planes_infos.hh` | 裁剪平面共享配置 |
| `gpu_srgb_to_framebuffer_space_infos.hh` | 颜色空间转换 |

### 3.2 2D UI 着色器

| 文件名 | 渲染内容 | 关键特性 |
|--------|---------|---------|
| `gpu_shader_2D_image_infos.hh` | 2D 图像 | 支持颜色空间转换 |
| `gpu_shader_2D_area_borders_infos.hh` | UI 边框 | 带抗锯齿 |
| `gpu_shader_2D_checker_infos.hh` | 棋盘格背景 | 透明度显示 |
| `gpu_shader_2D_diag_stripes_infos.hh` | 对角条纹 | 透明模式 |
| `gpu_shader_2D_widget_infos.hh` | UI 控件 | 复杂参数（边框/圆角/颜色） |
| `gpu_shader_2D_node_socket_infos.hh` | 节点连接点 | 动态颜色 |

### 3.3 3D 渲染着色器

| 文件名 | 用途 | 资源类型 |
|--------|------|---------|
| `gpu_shader_3D_flat_color_infos.hh` | 简单实体渲染 | Push Constant |
| `gpu_shader_3D_smooth_color_infos.hh` | 平滑着色 | Push Constant + 继承 |
| `gpu_shader_3D_depth_only_infos.hh` | 深度渲染 | 无颜色输出 |
| `gpu_shader_3D_uniform_color_infos.hh` | 统一颜色 | 4D 投影矩阵 |
| `gpu_shader_3D_point_infos.hh` | 3D 点 | 点大小 |
| `gpu_shader_3D_polyline_infos.hh` | 3D 折线 | 存储缓冲区 |

### 3.4 计算着色器

| 文件名 | 用途 | 关键特性 |
|--------|------|---------|
| `gpu_shader_test_infos.hh` | 测试用例 | 完整的 compute 示例 |
| `gpu_shader_index_infos.hh` | 索引生成 | 2D 阵列点/线/面 |
| `gpu_shader_sequencer_infos.hh` | 序列器 | 复杂的计算 + 存储缓冲区 |
| `gpu_clip_planes_infos.hh` | 裁剪计算 | Uniform Buffer |

### 3.5 特殊用途

| 文件名 | 用途 |
|--------|------|
| `gpu_shader_fullscreen_infos.hh` | 全屏处理 |
| `gpu_shader_gpencil_stroke_infos.hh` | Grease Pencil 笔画 |
| `gpu_shader_text_infos.hh` | 文本渲染 |
| `gpu_shader_icon_infos.hh` | 图标 |
| `gpu_shader_keyframe_shape_infos.hh` | 关键帧标记 |
| `gpu_shader_line_dashed_uniform_color_infos.hh` | 虚线 |
| `gpu_shader_print_infos.hh` | 打印调试 |
| `gpu_shader_simple_lighting_infos.hh` | 简单光照 |

---

## 4. 每个文件的具体作用

### 4.1 gpu_interface_infos.hh

**作用：** 预定义所有阶段间通信的接口

```cpp
/* 在所有着色器中使用的平滑插值接口 */
GPU_SHADER_INTERFACE_INFO(smooth_tex_coord_interp_iface)
  SMOOTH(float2, texCoord_interp)
GPU_SHADER_INTERFACE_END()

/* 图标渲染的多字段接口 */
GPU_SHADER_INTERFACE_INFO(icon_interp_iface)
  FLAT(float4, final_color)
  SMOOTH(float2, texCoord_interp)
  SMOOTH(float2, mask_coord_interp)
GPU_SHADER_INTERFACE_END()
```

### 4.2 gpu_shader_3D_flat_color_infos.hh

**作用：** 最简单的 3D 实体渲染着色器，用于场景中的基础几何体

```cpp
GPU_SHADER_CREATE_INFO(gpu_shader_3D_flat_color)
  VERTEX_IN(0, float3, pos)
  VERTEX_IN(1, float4, color)
  VERTEX_OUT(flat_color_iface)
  FRAGMENT_OUT(0, float4, fragColor)
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  PUSH_CONSTANT(float, size)
  VERTEX_SOURCE("gpu_shader_3D_flat_color_vert.glsl")
  FRAGMENT_SOURCE("gpu_shader_flat_color_frag.glsl")
  ADDITIONAL_INFO(gpu_srgb_to_framebuffer_space)
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()

/* 变体：带裁剪 */
GPU_SHADER_CREATE_INFO(gpu_shader_3D_flat_color_clipped)
  ADDITIONAL_INFO(gpu_shader_3D_flat_color)
  ADDITIONAL_INFO(gpu_clip_planes)
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()
```

### 4.3 gpu_shader_2D_image_infos.hh

**作用：** 2D 图像显示（UI 预览、图像编辑器等）

```cpp
GPU_SHADER_CREATE_INFO(gpu_shader_2D_image_common)
  VERTEX_IN(0, float2, pos)
  VERTEX_IN(1, float2, texCoord)
  VERTEX_OUT(smooth_tex_coord_interp_iface)
  FRAGMENT_OUT(0, float4, fragColor)
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  SAMPLER(0, sampler2D, image)
  VERTEX_SOURCE("gpu_shader_2D_image_vert.glsl")
  ADDITIONAL_INFO(gpu_srgb_to_framebuffer_space)
GPU_SHADER_CREATE_END()
```

### 4.4 gpu_shader_fullscreen_infos.hh

**作用：** 全屏后处理（需要单独定义接口）

```cpp
/* 定义全屏接口 */
GPU_SHADER_INTERFACE_INFO(gpu_fullscreen_iface)
  SMOOTH(float2, screen_uv)
GPU_SHADER_INTERFACE_END()

/* 全屏着色器（仅顶点，空的 fragment 可被后续添加） */
GPU_SHADER_CREATE_INFO(gpu_fullscreen)
  VERTEX_OUT(gpu_fullscreen_iface)
  VERTEX_SOURCE("gpu_shader_fullscreen_vert.glsl")
GPU_SHADER_CREATE_END()
```

### 4.5 gpu_shader_test_infos.hh

**作用：** 完整的测试套件，包含所有类型的 compute shader 示例

**亮点：**
```cpp
/* 1. 基本 Compute */
GPU_SHADER_CREATE_INFO(gpu_compute_2d_test)
  LOCAL_GROUP_SIZE(1, 1)
  IMAGE(1, SFLOAT_32_32_32_32, write, image2D, img_output)
  COMPUTE_SOURCE("gpu_compute_2d_test.glsl")
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()

/* 2. 原子操作 */
GPU_SHADER_CREATE_INFO(gpu_texture_atomic_test)
  LOCAL_GROUP_SIZE(32)
  BUILTINS(BuiltinBits::TEXTURE_ATOMIC)
  IMAGE(1, UINT_32, read_write, uimage2DAtomic, img_atomic_2D)
  PUSH_CONSTANT(bool, write_phase)
  COMPUTE_SOURCE("gpu_texture_atomic_test.glsl")
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()

/* 3. Push Constant 大小测试 */
GPU_SHADER_CREATE_INFO(gpu_push_constants_8192bytes_test)
  ADDITIONAL_INFO(gpu_push_constants_512bytes_test)
  PUSH_CONSTANT_ARRAY(float, filler4, 1920)  /* ≈ 8KB */
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()
```

### 4.6 gpu_shader_sequencer_infos.hh

**作用：** 视序列编辑器的 Scope 显示（波形图、示波器、直方图）

```cpp
/* Compute Shader 用于光栅化 */
GPU_SHADER_CREATE_INFO(gpu_shader_sequencer_scope_raster)
  LOCAL_GROUP_SIZE(16, 16)
  /* 2D 顶点数据通过屏幕坐标传入 */
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  PUSH_CONSTANT(float3, luma_coeffs)  /* 用于波形计算 */
  PUSH_CONSTANT(int, scope_mode)      /* 2=波形, 3=RGB Parade, 4=直方图 */
  /* ... */
  SAMPLER(0, sampler2D, image)        /* 输入图像 */
  STORAGE_BUF(0, read_write, SeqScopeRasterData, raster_buf[]) /* 输出缓冲区 */
  TYPEDEF_SOURCE("GPU_shader_shared.hh") /* 共享结构体定义 */
  COMPUTE_SOURCE("gpu_shader_sequencer_scope_comp.glsl")
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()

/* Fragment Shader 用于解析显示 */
GPU_SHADER_CREATE_INFO(gpu_shader_sequencer_scope_resolve)
  FRAGMENT_OUT(0, float4, fragColor)
  /* ... */
  ST OG storage_buf(0, read, SeqScopeRasterData, raster_buf[]) /* 只读 */
  FRAGMENT_SOURCE("gpu_shader_sequencer_scope_frag.glsl")
  ADDITIONAL_INFO(gpu_fullscreen) /* 使用全屏接口 */
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()
```

### 4.7 gpu_shader_3D_polyline_infos.hh

**作用：** 3D 折线渲染（支持复杂几何数据输入）

```cpp
GPU_SHADER_CREATE_INFO(gpu_shader_3D_polyline)
  DEFINE_VALUE("SMOOTH_WIDTH", "1.0f")
  /* 投影参数 */
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  PUSH_CONSTANT(float2, viewportSize)
  PUSH_CONSTANT(float, lineWidth)
  PUSH_CONSTANT(bool, lineSmooth)
  /* 顶点数据通过存储缓冲区 */
  STORAGE_BUF_FREQ(GPU_SSBO_POLYLINE_POS_BUF_SLOT, read, float, pos[], GEOMETRY)
  /* 顶点属性元数据 */
  PUSH_CONSTANT(int2, gpu_attr_0)           /* 属性偏移/步长 */
  PUSH_CONSTANT(int3, gpu_vert_stride_count_offset)
  PUSH_CONSTANT(int, gpu_attr_0_len)
  PUSH_CONSTANT(bool, gpu_attr_0_fetch_int)
  PUSH_CONSTANT(bool, gpu_attr_1_fetch_unorm8)
  /* ... */
  ADITIONAL_INFO(gpu_index_buffer_load) /* 继承索引加载 */
GPU_SHADER_CREATE_END()
```

---

## 5. 系统如何使用这些文件

### 5.1 工作流程概览

```plaintext
1. Info 文件定义
   ↓
2. 宏展开 + 预处理 (C++ 预处理器)
   ↓
3. Shader 创建信息对象构建 (ShaderCreateInfo)
   ↓
4. 资源位置自动分配
   ↓
5. 后端代码生成 (GLSL / HLSL / MSL)
   ↓
6. 运行时编译或预编译
```

### 5.2 代码生成示例

**输入（Info 文件）：**
```cpp
GPU_SHADER_CREATE_INFO(gpu_shader_3D_flat_color)
  VERTEX_IN(0, float3, pos)
  VERTEX_IN(1, float4, color)
  VERTEX_OUT(flat_color_iface)
  FRAGMENT_OUT(0, float4, fragColor)
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  VERTEX_SOURCE("gpu_shader_3D_flat_color_vert.glsl")
  FRAGMENT_SOURCE("gpu_shader_flat_color_frag.glsl")
  ADDITIONAL_INFO(gpu_srgb_to_framebuffer_space)
GPU_SHADER_CREATE_END()
```

**自动生成的 GLSL（OpenGL/Vulkan）：**
```glsl
#version 450

// Push Constant 成为 uniform
layout(location = 0) uniform mat4 ModelViewProjectionMatrix;

// VERTEX_IN 成为输入
layout(location = 0) in vec3 pos;
layout(location = 1) in vec4 color;

// VERTEX_OUT 接口
out flat_color_iface {
  flat vec4 finalColor;  // FLAT 限定符
} interp;

// FRAGMENT_OUT
layout(location = 0) out vec4 fragColor;

// 资源注入
#include "gpu_shader_3D_flat_color_vert.glsl"
```

**Shader 源文件使用：**
```glsl
/* gpu_shader_3D_flat_color_vert.glsl */
#include "infos/gpu_shader_3D_flat_color_infos.hh"

VERTEX_SHADER_CREATE_INFO(gpu_shader_3D_flat_color)

void main()
{
  float4 pos_4d = float4(pos, 1.0f);
  /* 直接使用 info 文件中定义的变量名 */
  gl_Position = ModelViewProjectionMatrix * pos_4d;
  finalColor = color;  /* 自动映射到接口变量 */
}
```

### 5.3 资源分配逻辑

| 宏 | 生成的绑定类型 | 示例 |
|----|--------------|------|
| `PUSH_CONSTANT` | Push Constants / Uniform | `layout(push_constant) uniform PC { mat4 MVP; }` |
| `UNIFORM_BUF` | Uniform Buffer | `layout(binding = 0) uniform UBO { ... }` |
| `STORAGE_BUF` | Shader Storage Buffer | `layout(binding = 0, std430) buffer SSBO { ... }` |
| `SAMPLER` | 纹理采样器 | `layout(binding = 0) uniform sampler2D image;` |
| `IMAGE` | 图像加载/存储 | `layout(binding = 1, rgba32f) writeonly uniform image2D img_output;` |

### 5.4 跨平台处理

**OpenGL / Vulkan / Metal：**
- 自动调整绑定槽位编号
- 语法差异适配
- 资源布局优化

**Metal 特化：**
```cpp
MTL_MAX_TOTAL_THREADS_PER_THREADGROUP(256)  /* Compute shader 并行度 */
```

### 5.5 运行时接口

**从 C++ 创建着色器：**
```cpp
using namespace blender::gpu;

/* 方式1：直接创建（静态编译） */
GPUShader *shader = GPU_shader_create_from_info_name("gpu_shader_3D_flat_color");

/* 方式2：动态组合 */
ShaderCreateInfo info("custom_shader");
info.vertex_in(0, Type::float3, "pos");
info.vertex_in(1, Type::float4, "color");
info.vertex_source("custom_vert.glsl");
info.fragment_source("custom_frag.glsl");
info.do_static_compilation(true);
GPUShader *shader = GPU_shader_create_from_info(info);
```

---

## 6. 配置文件的代码示例

### 6.1 简单顶点+片元着色器

```cpp
/* my_overlay_infos.hh */

#ifdef GPU_SHADER
#  pragma once
#  include "gpu_shader_compat.hh"
#endif

#include "gpu_shader_create_info.hh"

/* 1. 定义顶点输出接口 */
GPU_SHADER_INTERFACE_INFO(my_overlay_iface)
  SMOOTH(float4, vertexColor)
  SMOOTH(float2, uvCoord)
GPU_SHADER_INTERFACE_END()

/* 2. 定义着色器 */
GPU_SHADER_CREATE_INFO(my_overlay_shader)
  /* 输入 */
  VERTEX_IN(0, float3, pos)
  VERTEX_IN(1, float4, color)
  VERTEX_IN(2, float2, uv)

  /* 输出 */
  VERTEX_OUT(my_overlay_iface)
  FRAGMENT_OUT(0, float4, fragColor)

  /* 常量 */
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  PUSH_CONSTANT(float, overlayAlpha)

  /* 纹理 */
  SAMPLER(0, sampler2D, overlayTexture)

  /* 源文件 */
  VERTEX_SOURCE("my_overlay_vert.glsl")
  FRAGMENT_SOURCE("my_overlay_frag.glsl")

  /* 编译选项 */
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()
```

**对应的 GLSL 源文件：**

```glsl
/* my_overlay_vert.glsl */
#include "infos/my_overlay_infos.hh"

VERTEX_SHADER_CREATE_INFO(my_overlay_shader)

void main()
{
  gl_Position = ModelViewProjectionMatrix * float4(pos, 1.0);
  vertexColor = color;
  uvCoord = uv;
}
```

```glsl
/* my_overlay_frag.glsl */
#include "infos/my_overlay_infos.hh"

FRAGMENT_SHADER_CREATE_INFO(my_overlay_shader)

void main()
{
  vec4 texColor = texture(overlayTexture, uvCoord);
  vec4 finalColor = vertexColor * texColor * overlayAlpha;
  fragColor = finalColor;
}
```

### 6.2 复杂计算着色器

```cpp
/* my_particle_compute_infos.hh */

#ifdef GPU_SHADER
#  pragma once
#  include "gpu_shader_compat.hh"
#endif

#include "gpu_shader_create_info.hh"

/* 共享结构体（需要在 C++ 和 GLSL 中都可见） */
#define PARTICLE_STRUCT "my_particle_shared.hh"

GPU_SHADER_CREATE_INFO(my_particle_update)
  /* 工作组大小：16x16x1 */
  LOCAL_GROUP_SIZE(16, 16, 1)

  /* 读写存储缓冲区 */
  STORAGE_BUF_FREQ(0, read_write, ParticleData, particles[], GEOMETRY)

  /* 只读索引缓冲区 */
  STORAGE_BUF(1, read, uint, particle_indices[])

  /* 常量参数 */
  PUSH_CONSTANT(float, deltaTime)
  PUSH_CONSTANT(float3, gravity)
  PUSH_CONSTANT(int, particleCount)

  /* 图像输出（可选） */
  IMAGE(0, RGBA32F, write, image2D, debugOutput)

  /* 共享类型定义 */
  TYPEDEF_SOURCE(PARTICLE_STRUCT)

  /* 群组共享内存 */
  GROUP_SHARED(float, sharedGravity[16])

  /* 计算源 */
  COMPUTE_SOURCE("my_particle_update_comp.glsl")

  /* 优化选项 */
  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()
```

**计算着色器源文件：**

```glsl
/* my_particle_update_comp.glsl */
#include "infos/my_particle_compute_infos.hh"
#include "my_particle_shared.hh"

COMPUTE_SHADER_CREATE_INFO(my_particle_update)

shared float sharedGravity[16];

void main()
{
  uint idx = gl_GlobalInvocationID.x;
  if (idx >= particleCount) return;

  /* 读取粒子数据 */
  ParticleData p = particles[idx];

  /* 计算新速度 */
  p.velocity += gravity * deltaTime;
  p.position += p.velocity * deltaTime;

  /* 写回 */
  particles[idx] = p;

  /* 可选：调试输出 */
  if (gl_LocalInvocationID.x == 0) {
    imageStore(debugOutput, ivec2(gl_WorkGroupID.xy), vec4(p.position, 1.0));
  }
}
```

### 6.3 模块化组合

```cpp
/* my_ui_base_infos.hh - 基础 UI 功能 */
GPU_SHADER_CREATE_INFO(my_ui_base)
  VERTEX_IN(0, float2, pos)
  VERTEX_IN(1, float2, uv)
  PUSH_CONSTANT(float4x4, ModelViewProjectionMatrix)
  SAMPLER(0, sampler2D, uiTexture)
  DEFINE("UI_SCISSOR_ENABLE")
GPU_SHADER_CREATE_END()

/* my_ui_button_infos.hh - 按钮特定 */
#include "my_ui_base_infos.hh"

GPU_SHADER_CREATE_INFO(my_ui_button)
  ADDITIONAL_INFO(my_ui_base)  /* 继承基础 */

  VERTEX_OUT(my_button_iface)  /* 额外接口 */
  FRAGMENT_OUT(0, float4, fragColor)

  /* 按钮特定参数 */
  PUSH_CONSTANT(float4, buttonColor)
  PUSH_CONSTANT(float4, hoverColor)
  PUSH_CONSTANT(bool, isHovered)

  VERTEX_SOURCE("my_ui_button_vert.glsl")
  FRAGMENT_SOURCE("my_ui_button_frag.glsl")

  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()

/* my_ui_slider_infos.hh - 滑块特定 */
GPU_SHADER_CREATE_INFO(my_ui_slider)
  ADDITIONAL_INFO(my_ui_base)

  VERTEX_OUT(my_slider_iface)
  FRAGMENT_OUT(0, float4, fragColor)

  PUSH_CONSTANT(float, sliderValue)
  PUSH_CONSTANT(float, sliderMin)
  PUSH_CONSTANT(float, sliderMax)

  VERTEX_SOURCE("my_ui_slider_vert.glsl")
  FRAGMENT_SOURCE("my_ui_slider_frag.glsl")

  DO_STATIC_COMPILATION()
GPU_SHADER_CREATE_END()
```

---

## 7. 总结与最佳实践

### 7.1 何时使用哪种资源绑定

| 需求类型 | 推荐方式 | 示例 |
|---------|---------|------|
| 每帧变化的少量矩阵/数值 | `PUSH_CONSTANT` | MVP 矩阵 |
| 每对象变化的中等数据 | `UNIFORM_BUF` | 材质参数 |
| 大规模读写数据 | `STORAGE_BUF` | 粒子系统 |
| 图像处理/采样 | `SAMPLER` | 贴图 |
| 图像计算/存储 | `IMAGE` | Compute Shader 输出 |

### 7.2 性能优化建议

1. **使用正确的 Frequency**
   ```cpp
   /* 正确：每帧变化 */
   UNIFORM_BUF_FREQ(0, FrameData, frame, FRAME)

   /* 正确：每 Pass 变化 */
   UNIFORM_BUF_FREQ(0, PassData, pass, PASS)
   ```

2. **尽可能使用 PUSH_CONSTANT**
   - 开销最小
   - 适合 < 128 字节的数据

3. **静态编译**
   ```cpp
   DO_STATIC_COMPILATION()  // 启动时编译，运行时无编译开销
   ```

4. **模块化设计**
   ```cpp
   /* 复用常用配置 */
   ADDITIONAL_INFO(gpu_srgb_to_framebuffer_space)
   ```

### 7.3 调试技巧

1. **检查自动生成的代码**
   - 使用 `blender --debug-gpu` 查看生成的 GLSL

2. **验证资源绑定**
   - 通过 `ShaderCreateInfo` 的调试输出查看槽位分配

3. **宏展开检查**
   - 在 C++ 中编译 info 文件确保语法正确

---

## 附录 A: 宏定义速查表

```cpp
/* 着色器定义 */
GPU_SHADER_CREATE_INFO(name)
GPU_SHADER_INTERFACE_INFO(name)
GPU_SHADER_CREATE_END()
GPU_SHADER_INTERFACE_END()

/* 输入输出 */
VERTEX_IN(slot, type, name)
VERTEX_OUT(interface)
FRAGMENT_OUT(slot, type, name)

/* 资源绑定 */
PUSH_CONSTANT(type, name)
PUSH_CONSTANT_ARRAY(type, name, size)
UNIFORM_BUF(slot, type, name)
UNIFORM_BUF_FREQ(slot, type, name, freq)
STORAGE_BUF(slot, qualifier, type, name)
STORAGE_BUF_FREQ(slot, qualifier, type, name, freq)
SAMPLER(slot, type, name)
IMAGE(slot, format, qualifier, type, name)

/* 工作组定义 */
LOCAL_GROUP_SIZE(x, y, z)
GROUP_SHARED(type, name)

/* 源文件 */
VERTEX_SOURCE(filename)
FRAGMENT_SOURCE(filename)
COMPUTE_SOURCE(filename)

/* 条件与定义 */
DEFINE(name)
DEFINE_VALUE(name, value)
BUILTINS(bits)
SPECIALIZATION_CONSTANT(type, name, default)
COMPILATION_CONSTANT(type, name, value)

/* 继承与组合 */
ADDITIONAL_INFO(info_name)
TYPEDEF_SOURCE(filename)

/* 编译控制 */
DO_STATIC_COMPILATION()
AUTO_RESOURCE_LOCATION()
```

---

**文档结束**

*本文档基于 Blender 源代码分析生成，适用于 Blender 4.0+ 版本*
