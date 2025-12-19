# Cycles 渲染器 SVM（Shader Virtual Machine）架构详解

## 目录
1. [SVM 设计哲学和核心概念](#1-svm-设计哲学和核心概念)
2. [指令集架构（ISA）](#2-指令集架构isa)
3. [栈式计算系统](#3-栈式计算系统)
4. [内存管理和数据打包](#4-内存管理和数据打包)
5. [节点执行流程](#5-节点执行流程)
6. [性能优化机制](#6-性能优化机制)
7. [纹理节点实现详解](#7-纹理节点实现详解)
8. [编译流程](#8-编译流程)
9. [运行时执行流程](#9-运行时执行流程)
10. [与 GLSL/OSL 的配合方式](#10-与-glslosl-的配合方式)

---

## 1. SVM 设计哲学和核心概念

### 1.1 为什么需要虚拟机

Cycles 渲染器使用 SVM（Shader Virtual Machine）的主要原因包括：

**跨平台兼容性需求：**
- **GPU + CPU 统一架构**：SVM 提供了一个统一的着色器执行框架，能够在 CUDA、OptiX、Metal、OpenCL 和 CPU 上运行
- **避免代码重复**：不需要为每个平台编写单独的着色器代码
- **硬件抽象**：虚拟机封装了底层硬件差异

**内存效率：**
- **紧凑的字节码**：节点图被编译成紧凑的 uint4 指令序列
- **GPU 共享内存**：着色器程序可以在 GPU 上高效存储和执行
- **减少寄存器压力**：栈式计算避免了复杂函数的寄存器爆炸

**动态性：**
- **运行时编译**：着色器在渲染时根据场景动态编译
- **分支支持**：支持条件跳转和循环控制

### 1.2 核心设计原则

根据 `svm.h` 的注释，SVM 的核心设计原则：

```cpp
/* Shader Virtual Machine
 *
 * A shader is a list of nodes to be executed. These are simply read one after
 * the other and executed, using an node counter. Each node and its associated
 * data is encoded as one or more uint4's in a 1D texture. If the data is larger
 * than an uint4, the node can increase the node counter to compensate for this.
 * Floats are encoded as int and then converted to float again.
 *
 * Nodes write their output into a stack. All stack data in the stack is
 * floats, since it's all factors, colors and vectors. The stack will be stored
 * in local memory on the GPU, as it would take too many register and indexes in
 * ways not known at compile time. This seems the only solution even though it
 * may be slow, with two positive factors. If the same shader is being executed,
 * memory access will be coalesced and cached.
 */
```

---

## 2. 指令集架构（ISA）

### 2.1 指令格式

所有 SVM 指令都是 128 位（4个32位整数），称为 `uint4`：

```cpp
struct uint4 {
    uint x;  // 操作码 + 参数
    uint y;  // 参数1 + 参数2
    uint z;  // 参数3 + 参数4
    uint w;  // 参数5 + 参数6 + 参数7 + 参数8
};
```

### 2.2 操作码分类

在 `node_types_template.h` 中定义了所有操作码：

**基础操作：**
- `NODE_END` - 程序结束
- `NODE_SHADER_JUMP` - 着色器类型跳转（表面/体积/位移）
- `NODE_JUMP_IF_ZERO` - 条件跳转
- `NODE_JUMP_IF_ONE` - 条件跳转

**数据操作：**
- `NODE_CONVERT` - 类型转换
- `NODE_VALUE_F` - 设置浮点值
- `NODE_VALUE_V` - 设置向量值

**几何数据：**
- `NODE_GEOMETRY` - 几何信息
- `NODE_TEX_COORD` - 纹理坐标
- `NODE_ATTR` - 属性读取
- `NODE_VERTEX_COLOR` - 顶点颜色

**数学运算：**
- `NODE_MATH` - 标量数学
- `NODE_VECTOR_MATH` - 向量数学
- `NODE_MAPPING` - 坐标变换
- `NODE_MAP_RANGE` - 范围映射

**纹理节点：**
- `NODE_TEX_IMAGE` - 图像纹理
- `NODE_TEX_CHECKER` - 棋盘格
- `NODE_TEX_BRICK` - 砖墙
- `NODE_TEX_NOISE` - 噪声
- `NODE_TEX_VORONOI` - 沃罗诺伊
- `NODE_TEX_WAVE` - 波浪
- `NODE_TEX_MAGIC` - 魔术纹理

**色彩操作：**
- `NODE_GAMMA` - 伽马校正
- `NODE_BRIGHTCONTRAST` - 亮度对比度
- `NODE_HSV` - HSV 转换
- `NODE_RGB_RAMP` - RGB 渐变

**闭包（材质）：**
- `NODE_CLOSURE_BSDF` - BSDF 闭包
- `NODE_CLOSURE_EMISSION` - 发射闭包
- `NODE_CLOSURE_WEIGHT` - 闭包权重
- `NODE_MIX_CLOSURE` - 混合闭包

### 2.3 操作码编码策略

**Byte Packing（字节打包）：**

SVM 使用 `svm_unpack_node_uchar*` 函数来从一个 32 位整数中解包出多个 8 位参数：

```cpp
ccl_device_forceinline void svm_unpack_node_uchar4(const uint i,
                                                   ccl_private uint *x,
                                                   ccl_private uint *y,
                                                   ccl_private uint *z,
                                                   ccl_private uint *w)
{
  *x = (i & 0xFF);
  *y = ((i >> 8) & 0xFF);
  *z = ((i >> 16) & 0xFF);
  *w = ((i >> 24) & 0xFF);
}
```

**示例：Math 节点编码**
```cpp
// 节点结构：uint4 node = {操作码, 输入偏移打包, 输入偏移打包, 结果偏移}
// 操作码: NODE_MATH = 12
// 输入: a_offset, b_offset, c_offset 打包到一个字节
// 结果: result_offset

ccl_device_noinline void svm_node_math(ccl_private float *stack,
                                       const uint type,
                                       const uint inputs_stack_offsets,
                                       const uint result_stack_offset)
{
  uint a_stack_offset;
  uint b_stack_offset;
  uint c_stack_offset;
  svm_unpack_node_uchar3(inputs_stack_offsets, &a_stack_offset, &b_stack_offset, &c_stack_offset);

  const float a = stack_load_float(stack, a_stack_offset);
  const float b = stack_load_float(stack, b_stack_offset);
  const float c = stack_load_float(stack, c_stack_offset);
  const float result = svm_math((NodeMathType)type, a, b, c);

  stack_store_float(stack, result_stack_offset, result);
}
```

---

## 3. 栈式计算系统

### 3.1 栈结构

在 `types.h` 中定义：
```cpp
#define SVM_STACK_SIZE 255
#define SVM_STACK_INVALID 255
```

栈是一个固定大小的浮点数组，所有节点操作都在栈上进行。

### 3.2 栈操作原语

在 `util.h` 中定义的核心栈操作：

**浮点数栈操作：**
```cpp
ccl_device_inline float stack_load_float(const ccl_private float *stack, const uint a)
{
  kernel_assert(a < SVM_STACK_SIZE);
  return stack[a];
}

ccl_device_inline void stack_store_float(ccl_private float *stack, const uint a, const float f)
{
  kernel_assert(a < SVM_STACK_SIZE);
  stack[a] = f;
}
```

**向量栈操作（3个连续浮点数）：**
```cpp
ccl_device_inline float3 stack_load_float3(const ccl_private float *stack, const uint a)
{
  kernel_assert(a + 2 < SVM_STACK_SIZE);
  const ccl_private float *stack_a = stack + a;
  return make_float3(stack_a[0], stack_a[1], stack_a[2]);
}

ccl_device_inline void stack_store_float3(ccl_private float *stack, const uint a, const float3 f)
{
  kernel_assert(a + 2 < SVM_STACK_SIZE);
  copy_v3_v3(stack + a, f);
}
```

**带默认值的加载：**
```cpp
ccl_device_inline float stack_load_float_default(const ccl_private float *stack,
                                                 const uint a,
                                                 const float value)
{
  return (a == (uint)SVM_STACK_INVALID) ? value : stack_load_float(stack, a);
}
```

### 3.3 栈分配策略

**静态栈帧：**
每个着色器执行分配固定大小的栈：
```cpp
template<uint node_feature_mask, ShaderType type, typename ConstIntegratorGenericState>
ccl_device void svm_eval_nodes(KernelGlobals kg,
                               ConstIntegratorGenericState state,
                               ccl_private ShaderData *sd,
                               ccl_global float *render_buffer,
                               const uint32_t path_flag)
{
  float stack[SVM_STACK_SIZE];  // 栈分配
  Spectrum closure_weight = zero_spectrum();
  int offset = sd->shader & SHADER_MASK;

  while (true) {
    uint4 node = read_node(kg, &offset);  // 读取指令
    // ... 执行指令
  }
}
```

**栈偏移计算：**
编译器在编译时为每个节点的输入/输出分配固定的栈偏移。例如：
- 输入1 → 偏移 0-2 (float3)
- 输入2 → 偏移 3 (float)
- 输出 → 偏移 4

### 3.4 计算流程示例

以下是一个简单的节点图执行流程：

```
节点图：
TextureCoordinate → Noise → Math → BSDF

编译后的栈状态：
[0-2]︰ texture_coord (float3)
[3-5]︰ noise_output (float3)
[6-8]︰ math_output (float3)
[9]  ： bsdf_weight (float)

指令序列：
1. NODE_TEX_COORD [输出偏移: 0]
2. NODE_TEX_NOISE [输入偏移: 0, 输出偏移: 3]
3. NODE_MATH [输入偏移: 3, 输出偏移: 6]
4. NODE_CLOSURE_BSDF [颜色偏移: 6, 权重偏移: 9]
```

---

## 4. 内存管理和数据打包

### 4.1 指令存储格式

SVM 指令存储在 `kernel_data.svm_nodes` 中，这是一个 1D 纹理/数组：

```cpp
ccl_device_inline uint4 read_node(KernelGlobals kg, ccl_private int *const offset)
{
  uint4 node = kernel_data_fetch(svm_nodes, *offset);
  (*offset)++;
  return node;
}
```

**内存布局：**
```
[0]︰ [操作码, 参数打包, 参数打包, 参数打包]
[1]︰ [额外数据1, 额外数据2, 额外数据3, 额外数据4]
[2]︰ [额外数据5, 额外数据6, 额外数据7, 额外数据8]
...
```

### 4.2 数据类型转换

由于 GPU 内存限制，很多数据需要编码：

**Float → Int 编码：**
```cpp
// 存储时
uint float_as_uint = __float_as_uint(f);

// 读取时
float f = __uint_as_float(node.x);
```

**向量打包：**
小型向量可以在单个 `uint4` 中编码：
```cpp
// 4个浮点数打包到 uint4
uint4 packed = make_uint4(
  __float_as_uint(f1),
  __float_as_uint(f2),
  __float_as_uint(f3),
  __float_as_uint(f4)
);
```

### 4.3 节点数据扩展

复杂节点可能需要多个 `uint4`：

**砖墙纹理节点示例：**
```cpp
ccl_device_noinline int svm_node_tex_brick(KernelGlobals kg,
                                           ccl_private float *stack,
                                           const uint4 node,
                                           int offset)
{
  // 第一个 uint4 包含基本参数
  const uint4 node2 = read_node(kg, &offset);  // 额外参数1
  const uint4 node3 = read_node(kg, &offset);  // 额外参数2
  const uint4 node4 = read_node(kg, &offset);  // 额外参数3

  // 解包栈偏移
  uint co_offset;
  uint color1_offset;
  // ... 更多解包
  svm_unpack_node_uchar4(node.y, &co_offset, &color1_offset, ...);

  // 从栈读取输入
  float3 co = stack_load_float3(stack, co_offset);
  float3 color1 = stack_load_float3(stack, color1_offset);

  // 计算输出
  float2 result = svm_brick(co, mortar_size, mortgage_smooth, ...);

  // 写入输出到栈
  stack_store_float3(stack, color_offset, tint_color);
  stack_store_float(stack, fac_offset, result.x);

  return offset;  // 返回新的指令指针
}
```

---

## 5. 节点执行流程

### 5.1 主解释器循环

在 `svm.h` 中的核心执行循环：

```cpp
template<uint node_feature_mask, ShaderType type, typename ConstIntegratorGenericState>
ccl_device void svm_eval_nodes(KernelGlobals kg,
                               ConstIntegratorGenericState state,
                               ccl_private ShaderData *sd,
                               ccl_global float *render_buffer,
                               const uint32_t path_flag)
{
  float stack[SVM_STACK_SIZE];
  Spectrum closure_weight = zero_spectrum();
  int offset = sd->shader & SHADER_MASK;  // 着色器在内存中的偏移

  while (true) {
    uint4 node = read_node(kg, &offset);  // 读取当前指令

    switch (node.x) {  // node.x 包含操作码
      SVM_CASE(NODE_END)
        return;  // 结束执行

      SVM_CASE(NODE_SHADER_JUMP)
        // 根据着色器类型跳转到不同代码段
        if (type == SHADER_TYPE_SURFACE) {
          offset = node.y;
        }
        else if (type == SHADER_TYPE_VOLUME) {
          offset = node.z;
        }
        else if (type == SHADER_TYPE_DISPLACEMENT) {
          offset = node.w;
        }
        break;

      SVM_CASE(NODE_MATH)
        svm_node_math(stack, node.y, node.z, node.w);
        break;

      SVM_CASE(NODE_TEX_NOISE)
        offset = svm_node_tex_noise(kg, stack, node.y, node.z, node.w, offset);
        break;

      // ... 更多节点类型

      default:
        kernel_assert(!"Unknown node type");
        return;
    }
  }
}
```

### 5.2 纹理节点执行示例

**棋盘格纹理 (\`checker.h\`):**
```cpp
ccl_device_noinline void svm_node_tex_checker(ccl_private float *stack, const uint4 node)
{
  uint co_offset;
  uint color1_offset;
  uint color2_offset;
  uint scale_offset;
  uint color_offset;
  uint fac_offset;

  svm_unpack_node_uchar4(node.y, &co_offset, &color1_offset, &color2_offset, &scale_offset);
  svm_unpack_node_uchar2(node.z, &color_offset, &fac_offset);

  // 从栈读取输入
  const float3 co = stack_load_float3(stack, co_offset);
  const float3 color1 = stack_load_float3(stack, color1_offset);
  const float3 color2 = stack_load_float3(stack, color2_offset);
  const float scale = stack_load_float_default(stack, scale_offset, node.w);

  // 计算棋盘格
  const float f = svm_checker(co * scale);

  // 写入输出
  if (stack_valid(color_offset)) {
    stack_store_float3(stack, color_offset, (f == 1.0f) ? color1 : color2);
  }
  if (stack_valid(fac_offset)) {
    stack_store_float(stack, fac_offset, f);
  }
}

ccl_device float svm_checker(float3 p)
{
  p.x = (p.x + 0.000001f) * 0.999999f;
  p.y = (p.y + 0.000001f) * 0.999999f;
  p.z = (p.z + 0.000001f) * 0.999999f;

  const int xi = abs(float_to_int(floorf(p.x)));
  const int yi = abs(float_to_int(floorf(p.y)));
  const int zi = abs(float_to_int(floorf(p.z)));

  return ((xi % 2 == yi % 2) == (zi % 2)) ? 1.0f : 0.0f;
}
```

**噪声纹理 (\`noisetex.h\`):**
```cpp
ccl_device_noinline int svm_node_tex_noise(KernelGlobals kg,
                                           ccl_private float *stack,
                                           const uint type,
                                           const uint inputs_pack,
                                           const uint outputs_pack,
                                           int offset)
{
  uint co_offset;
  uint scale_offset;
  uint detail_offset;
  uint roughness_offset;
  svm_unpack_node_uchar4(inputs_pack, &co_offset, &scale_offset, &detail_offset, &roughness_offset);

  uint color_offset;
  uint fac_offset;
  svm_unpack_node_uchar2(outputs_pack, &color_offset, &fac_offset);

  float p = stack_load_float3(stack, co_offset).x;
  float scale = stack_load_float_default(stack, scale_offset, 1.0f);
  float detail = stack_load_float_default(stack, detail_offset, 2.0f);

  // 调用噪声计算函数
  float result = noise_fbm(p * scale, detail, 0.5f, 2.0f, true);

  if (stack_valid(fac_offset)) stack_store_float(stack, fac_offset, result);
  return offset;
}
```

**沃罗诺伊纹理 (\`voronoi.h\`):**
```cpp
ccl_device_noinline int svm_node_tex_voronoi(KernelGlobals kg,
                                             ccl_private float *stack,
                                             const uint type,
                                             const uint feat_pack,
                                             const uint params_pack,
                                             int offset)
{
  VoronoiParams params;
  // 解包参数并调用沃罗诺伊计算
  VoronoiOutput output = voronoi_f1(params, coord);

  if (stack_valid(color_offset))
    stack_store_float3(stack, color_offset, hash_float_to_float3(cell_offset));
  if (stack_valid(dist_offset))
    stack_store_float(stack, dist_offset, output.distance);

  return offset;
}
```

**砖墙纹理 (\`brick.h\`):**
```cpp
ccl_device_noinline int svm_node_tex_brick(KernelGlobals kg,
                                           ccl_private float *stack,
                                           const uint4 node,
                                           int offset)
{
  // 读取4个 uint4 来存储所有参数
  const uint4 node2 = read_node(kg, &offset);
  const uint4 node3 = read_node(kg, &offset);
  const uint4 node4 = read_node(kg, &offset);

  // 解包堆叠偏移
  uint co_offset, color1_offset, color2_offset, mortar_offset;
  svm_unpack_node_uchar4(node.y, &co_offset, &color1_offset, &color2_offset, &mortar_offset);

  uint scale_offset, mortar_size_offset, bias_offset, brick_width_offset;
  svm_unpack_node_uchar4(node.z, &scale_offset, &mortar_size_offset, &bias_offset, &brick_width_offset);

  uint row_height_offset, color_offset, fac_offset, mortar_smooth_offset;
  svm_unpack_node_uchar4(node.w, &row_height_offset, &color_offset, &fac_offset, &mortar_smooth_offset);

  // 计算砖墙
  float2 result = svm_brick(
    stack_load_float3(stack, co_offset),
    stack_load_float_default(stack, mortar_size_offset, node2.x),
    stack_load_float_default(stack, mortar_smooth_offset, node4.w),
    stack_load_float_default(stack, bias_offset, node2.z),
    stack_load_float_default(stack, brick_width_offset, node2.w),
    stack_load_float_default(stack, row_height_offset, node3.x),
    offset_frequency, squash_frequency  // 从 node4 解码
  );

  // 写入输出
  if (stack_valid(color_offset)) {
    float3 tint = make_float3(result.x, result.x, result.x);  // 灰度值
    stack_store_float3(stack, color_offset, tint);
  }
  if (stack_valid(fac_offset)) stack_store_float(stack, fac_offset, result.y);  // mortar factor

  return offset;
}
```

**brick_noise** 是一个快速的整数噪声函数：
```cpp
ccl_device_inline float brick_noise(uint n)
{
  uint nn;
  n = (n + 1013) & 0x7fffffff;
  n = (n >> 13) ^ n;
  nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff;
  return 0.5f * ((float)nn / 1073741824.0f);
}
```

---

## 6. 性能优化机制

### 6.1 编译器宏定义

**设备特定宏定义 (`cuda/compat.h`, `optix/compat.h`, `oneapi/compat.h`):**

**CUDA:**
```cpp
#define ccl_device __device__ __inline__
#define ccl_device_inline __device__ __inline__
#define ccl_device_forceinline __device__ __forceinline__
#define ccl_device_noinline __device__ __noinline__
#define ccl_private
```

**OneAPI:**
```cpp
#define ccl_device inline
#define ccl_device_inline __attribute__((always_inline))
#define ccl_device_forceinline __attribute__((always_inline))
#define ccl_device_noinline __attribute__((noinline))
```

**OpenCL/通用CPU:**
```cpp
#define ccl_device static inline
#define ccl_device_noinline static
```

### 6.2 内联策略

**强制内联 (`ccl_device_forceinline`)：**
用于频繁调用的小函数，如栈操作和数据访问：
```cpp
ccl_device_forceinline void svm_unpack_node_uchar4(const uint i,
                                                   ccl_private uint *x,
                                                   ccl_private uint *y,
                                                   ccl_private uint *z,
                                                   ccl_private uint *w)
{
  *x = (i & 0xFF);
  *y = ((i >> 8) & 0xFF);
  *z = ((i >> 16) & 0xFF);
  *w = ((i >> 24) & 0xFF);
}
```

**不内联 (`ccl_device_noinline`)：**
用于复杂函数以避免代码膨胀：
```cpp
ccl_device_noinline void svm_node_math(ccl_private float *stack, ...)
{
  // 复杂的数学运算
  // 使用 switch 处理多种数学类型
}
```

**选择性内联：**
模板函数利用编译器决定：
```cpp
template<uint node_feature_mask, ShaderType type>
ccl_device_noinline int svm_node_closure_bsdf(...)
{
  // 只在需要时编译特定特征
  IF_KERNEL_NODES_FEATURE(BSDF)
  {
    // BSDF 计算核心代码
  }
}
```

### 6.3 特征掩码优化

使用编译时特征掩码避免未使用功能的代码生成：

```cpp
#ifdef __KERNEL_USE_DATA_CONSTANTS__
#define SVM_CASE(node) \
  case node: \
    if (!kernel_data_svm_usage_##node) \
      break;
#else
#define SVM_CASE(node) case node:
#endif
```

在编译时分析着色器使用哪些节点类型，只为实际使用的节点生成代码。

### 6.4 GPU 内存优化

**齐次访问模式：**
```cpp
ccl_device_inline uint4 read_node(KernelGlobals kg, ccl_private int *const offset)
{
  uint4 node = kernel_data_fetch(svm_nodes, *offset);
  (*offset)++;
  return node;
}
```
GPU 上的 `kernel_data_fetch` 会合并内存访问。

**寄存器分配：**
- 栈使用局部内存（GPU shared memory 或 CPU 栈）
- 中间变量尽可能保持在寄存器中
- 使用 `ccl_private` 明确内存类别

### 6.5 特殊优化

**向量化：**
```cpp
ccl_device_inline float3 dPdx(const ccl_private ShaderData *sd)
{
  return sd->dPdu * sd->du.dx + sd->dPdv * sd->dv.dx;
}
```

**分支预测：**
```cpp
if (shader_type != SHADER_TYPE_SURFACE) {
  return svm_node_closure_bsdf_skip(kg, offset, type);
}
```

**常量传播：**
```cpp
const float a = stack_load_float(stack, a_stack_offset);
const float b = stack_load_float(stack, b_stack_offset);
// 编译器可以优化这些重复读取
```

---

## 7. 纹理节点实现详解

### 7.1 棋盘格纹理 (`checker.h`)

**实现算法：**
```cpp
ccl_device float svm_checker(float3 p)
{
  p.x = (p.x + 0.000001f) * 0.999999f;  // 避免精度问题
  p.y = (p.y + 0.000001f) * 0.999999f;
  p.z = (p.z + 0.000001f) * 0.999999f;

  const int xi = abs(float_to_int(floorf(p.x)));
  const int yi = abs(float_to_int(floorf(p.y)));
  const int zi = abs(float_to_int(floorf(p.z)));

  // 奇偶性检查逻辑
  return ((xi % 2 == yi % 2) == (zi % 2)) ? 1.0f : 0.0f;
}
```

**SVM 节点结构：**
- 输入：坐标、颜色1、颜色2、缩放
- 输出：颜色、因子
- 大小：1 个 uint4

### 7.2 砖墙纹理 (`brick.h`)

**核心算法：**
```cpp
ccl_device_noinline float2 svm_brick(...)
{
  // 计算砖块行号
  int rownum = floor_to_int(p.y / row_height);

  // 处理偏移和挤压
  if (offset_frequency && squash_frequency) {
    brick_width *= (rownum % squash_frequency) ? 1.0f : squash_amount;
    offset = (rownum % offset_frequency) ? 0.0f : (brick_width * offset_amount);
  }

  int bricknum = floor_to_int((p.x + offset) / brick_width);
  float x = (p.x + offset) - brick_width * bricknum;
  float y = p.y - row_height * rownum;

  // 随机色调
  const float tint = saturatef((brick_noise((rownum << 16) + (bricknum & 0xFFFF)) + bias));

  // 灰浆距离
  float min_dist = min(min(x, y), min(brick_width - x, row_height - y));

  float mortar;
  if (min_dist >= mortar_size) {
    mortar = 0.0f;
  }
  else if (mortar_smooth == 0.0f) {
    mortar = 1.0f;
  }
  else {
    min_dist = 1.0f - min_dist / mortar_size;
    mortar = smoothstepf(min_dist / mortar_smooth);
  }

  return make_float2(tint, mortar);
}
```

**SVM 节点结构：**
- 输入：7个参数（坐标、颜色、比例、灰浆大小等）
- 输出：颜色、因子
- 大小：4 个 uint4（包含所有参数的复杂节点）

### 7.3 噪声纹理 (`noisetex.h` + `fractal_noise.h`)

**分形噪声算法：**
```cpp
template<typename T>
ccl_device float noise_select(T p,
                              const float detail,
                              const float roughness,
                              const float lacunarity,
                              const float offset,
                              const float gain,
                              const int type,
                              bool normalize)
{
  switch ((NodeNoiseType)type) {
    case NODE_NOISE_MULTIFRACTAL:
      return noise_multi_fractal(p, detail, roughness, lacunarity);

    case NODE_NOISE_FBM:
      return noise_fbm(p, detail, roughness, lacunarity, normalize);

    case NODE_NOISE_HYBRID_MULTIFRACTAL:
      return noise_hybrid_multi_fractal(p, detail, roughness, lacunarity, offset, gain);

    case NODE_NOISE_RIDGED_MULTIFRACTAL:
      return noise_ridged_multi_fractal(p, detail, roughness, lacunarity, offset, gain);

    case NODE_NOISE_HETERO_TERRAIN:
      return noise_hetero_terrain(p, detail, roughness, lacunarity, offset);
  }
}
```

**FBM 噪声实现：**
```cpp
template<typename T>
ccl_device float noise_fbm(T p, float detail, float roughness, float lacunarity, bool normalize)
{
  float fscale = 1.0f;
  float weight = 1.0f;
  float sum = 0.0f;
  float max_weight = 0.0f;

  for (int i = 0; i < (int)detail; i++) {
    float n = perlin(p * fscale);
    sum += n * weight;
    max_weight += weight;
    weight *= roughness;
    fscale *= lacunarity;
  }

  return normalize ? sum / max_weight : sum;
}
```

**积雪噪声：**
```cpp
template<typename T>
ccl_device float noise_ridged_multi_fractal(...)
{
  float n = perlin(p * fscale);
  n = 1.0f - fabsf(n);
  n = n * n;  // 更清晰的边缘
  return n;
}
```

**SVM 节点结构：**
- 输入：坐标、缩放、细节、粗糙度、失真等
- 输出：值、颜色（可选6个独立噪声）
- 大小：包含参数的多节点结构

### 7.4 沃罗诺伊纹理 (`voronoi.h`)

**距离计算：**
```cpp
template<typename T>
ccl_device float voronoi_distance(const T a, const T b, const ccl_private VoronoiParams ¶ms)
{
  switch (params.metric) {
    case NODE_VORONOI_EUCLIDEAN:
      return distance(a, b);
    case NODE_VORONOI_MANHATTAN:
      return reduce_add(fabs(a - b));
    case NODE_VORONOI_CHEBYCHEV:
      return reduce_max(fabs(a - b));
    case NODE_VORONOI_MINKOWSKI:
      return powf(reduce_add(power(fabs(a - b), params.exponent)), 1.0f / params.exponent);
  }
}
```

**F1 特征：**
```cpp
ccl_device VoronoiOutput voronoi_f1(const ccl_private VoronoiParams ¶ms, const float coord)
{
  const float cellPosition = floorf(coord);
  const float localPosition = coord - cellPosition;

  float minDistance = FLT_MAX;
  float targetOffset = 0.0f;
  float targetPosition = 0.0f;

  for (int i = -1; i <= 1; i++) {
    const float cellOffset = i;
    const float pointPosition = cellOffset + hash_float_to_float(cellPosition + cellOffset) * params.randomness;
    const float distanceToPoint = voronoi_distance(pointPosition, localPosition);

    if (distanceToPoint < minDistance) {
      targetOffset = cellOffset;
      minDistance = distanceToPoint;
      targetPosition = pointPosition;
    }
  }

  VoronoiOutput octave;
  octave.distance = minDistance;
  octave.color = hash_float_to_float3(cellPosition + targetOffset);
  octave.position = voronoi_position(targetPosition + cellPosition);
  return octave;
}
```

**光滑 F1：**
```cpp
ccl_device VoronoiOutput voronoi_smooth_f1(...)
{
  float smoothDistance = 0.0f;
  float h = -1.0f;

  for (int i = -2; i <= 2; i++) {
    // 使用 smoothstep 进行加权平均
    float distanceToPoint = voronoi_distance(pointPosition, localPosition);
    h = h == -1.0f ? 1.0f : smoothstep(0.0f, 1.0f, 0.5f + 0.5f * (smoothDistance - distanceToPoint) / params.smoothness);
    float correctionFactor = params.smoothness * h * (1.0f - h);
    smoothDistance = mix(smoothDistance, distanceToPoint, h) - correctionFactor;
  }

  return result;
}
```

**距离到边缘：**
```cpp
ccl_device VoronoiOutput voronoi_distance_to_edge(VoronoiParams ¶ms, float coord)
{
  // 计算到 Voronoi 单元边界的最近距离
  float minDistance = FLT_MAX;
  for (int i = -1; i <= 1; i++) {
    float cellPosition = floorf(coord) + i;
    float cellHash = hash_float_to_float(cellPosition);
    float cellCenter = cellHash * params.randomness;

    // 计算与当前单元和相邻单元的边界距离
    // ... 复杂的距离计算
  }
}
```

**SVM 节点结构：**
- 输入：坐标、缩放、细节、粗糙度、平滑度、随机性等
- 输出：距离、颜色、位置（根据特征类型）
- 需要多 uint4 来存储复杂参数

---

## 8. 编译流程

### 8.1 节点图编译

**阶段1：节点图优化**
- 消除未使用的节点
- 合并简单的数学运算
- 常量折叠

**阶段2：栈分配**
- 分析节点依赖关系
- 为每个节点的输入输出分配栈位置
- 确定栈大小（不超过 255）

**阶段3：指令生成**
```cpp
class SVMCompiler {
  void compile_node(Node* node) {
    switch (node->type) {
      case NODE_MATH:
        push_instruction(NODE_MATH, {
          stack_offset(node->input_a),
          stack_offset(node->input_b),
          stack_offset(node->output)
        });
        break;

      case NODE_TEXTURE:
        push_instruction(NODE_TEX_..., {
          stack_offset(node->coords),
          pack_flags(node->flags)
        });
        break;
    }
  }
};
```

### 8.2 内存布局生成

**最终 SVM 字节码：**
```cpp
struct SVMBytecode {
  uint4* instructions;        // 指令数组
  size_t instruction_count;   // 指令数量
  size_t stack_size;          // 所需栈大小

  // 导出到 kernel_data
  void export_to_kernel(KernelData* data) {
    data->svm_nodes = instructions;
    data->svm_node_count = instruction_count;
    data->svm_stack_size = stack_size;
  }
};
```

### 8.3 特征检测和优化

在编译时检测使用了哪些节点类型，并通过编译时标志优化：

```cpp
// 在编译时设置使用标志
for each instruction in bytecode:
  if instruction.type == NODE_TEX_NOISE:
    kernel_data.svm_usage_TEX_NOISE = true;
```

然后在运行时：
```cpp
SVM_CASE(NODE_TEX_NOISE)  // 如果未使用，会被宏清除
  if (!kernel_data_svm_usage_TEX_NOISE)
    break;
```

---

## 9. 运行时执行流程

### 9.1 创建着色器执行上下文

**每个像素/采样点：**
```cpp
// 在光线追踪的着色阶段
ccl_device void shader_eval(KernelGlobals kg,
                           ShaderData* sd,
                           PathRadiance* L,
                           uint32_t path_flag)
{
  // 获取着色器 ID 和类型
  int shader = sd->shader & SHADER_MASK;

  // 调用 SVM 执行
  svm_eval_nodes<NODE_FEATURE_MASK, SHADER_TYPE_SURFACE>(
    kg,
    state,  // 积分器状态
    sd,     // 几何数据
    render_buffer,
    path_flag
  );
}
```

### 9.2 每个采样点的生命周期

**初始化阶段：**
```
1. 分配栈内存 (255浮点数)
2. 初始化闭包权重 = 0
3. 设置指令指针 = 着色器偏移

执行阶段：
4. 读取主着色器跳转指令
5. 根据着色器类型跳转到表面/体积/位移代码
6. 按顺序执行所有节点：
   - 读取指令
   - 解包参数
   - 从栈读取输入
   - 计算结果
   - 写入输出到栈
```

**砖墙纹理计算完整流程：**
```
1. 坐标冲压: 写入栈[0-2]
2. 砖墙参数: 写入栈[3-10] (包含颜色、比例等)
3. 砖墙执行:
   - 读取栈[0-2] 坐标
   - 读取栈[3-10] 参数
   - 计算 svm_brick()
   - 结果写入栈[11-13] 颜色, [14] 因子
4. BSDF 使用栈[11-14]
5. 继续下一个节点...
```

### 9.3 每帧统计和清理

**性能监控：**
```cpp
// 每帧结束时
update_shader_memory_usage();
reset_stack_allocation_stats();
```

---

## 10. 与 GLSL/OSL 的配合方式

### 10.1 GLSL 后端

**混合渲染模式：**
```cpp
#ifdef COMPILE_WITH_GLSL
  // 简单的节点使用 GLSL 硬件烘焙
  if (shader_is_simple_enough_for_glsl()) {
    return generate_glsl_shader(node_graph);
  }
  // 复杂节点回退到 SVM
  else {
    return generate_svm_bytecode(node_graph);
  }
#endif
```

**GLSL 生成模板：**
```glsl
// 简单的纹理坐标 + 噪声
vec3 tex_coord = texture_coordinate();
float noise = fractal_noise(tex_coord * scale, detail);
vec3 color = mix(color1, color2, noise);
```

### 10.2 OSL 集成

**OSL 用于CPU，SVM 用于GPU：**
```cpp
// CPU 渲染时
#ifdef SUPPORTS_OSL
  OSLCompiler compiler;
  shader = compiler.compile_to_llvm(node_graph);
  execute_osl_shader(shader,萧数据,表面点);
#endif

// GPU 渲染时
#ifdef SUPPORTS_SVM
  SVMCompiler compiler;
  shader = compiler.compile_to_bytecode(node_graph);
  svm_eval_nodes(kernel_data.svm_nodes,  /* ... */);
#endif
```

### 10.3 选择策略

**条件编译：**
```cpp
bool should_use_svm(ShaderGraph* graph) {
  // 如果包含 GPU 不支持的操作
  if (graph->contains_emissive_only()) {
    return true;  // SVM 可以更高效处理
  }

  // 如果包含复杂函数调用
  if (graph->complexity() > GPU_SHADER_COMPLEXITY_THRESHOLD) {
    return false;  // 使用 GLSL
  }

  // 系统统一选择
  return device_type == GPU;
}
```

### 10.4 统一的数据交换

**通用着色器数据结构：**
```cpp
struct ShaderData {
  // SVM 和 OSL 共享
  float3 P;           // 位置
  float3 N;           // 法线
  float3 T;           // 切线
  float2 uv;          // UV坐标
  // ... 更多几何数据

  // SVM 专用
  int shader_offset;  // SVM 字节码偏移

  // OSL 专用
  OSLShader* osl_shader;  // OSL 字节码
};
```

---

## 总结

SVM 作为 Cycles 的核心着色器执行后端，通过以下设计实现了高性能与跨平台兼容性的平衡：

1. **统一架构**：为所有平台提供相同的执行模型
2. **紧凑编码**：通过字节打包和栈式计算优化内存使用
3. **编译时优化**：特征掩码和内联策略减少代码膨胀
4. **高效的GPU访问**：齐次内存访问模式和寄存器优化
5. **模块化节点设计**：每个纹理节点都有清晰的职责分离

通过这种设计，Cycles 能够通过相同的着色器描述生成适用于 CPU、CUDA、OptiX、Metal 和 OpenCL 的高效执行代码，为复杂的材质系统提供统一的计算基础。