# 014-节点fresnel详解

> **文档编号**: 014
> **创建日期**: 2025-12-18
> **主题**: Fresnel 节点的三个层面实现深度解析
> **Blender版本**: 4.3+

---

## 目录
1. [物理原理与菲涅尔方程](#物理原理)
2. [核心算法：fresnel_dielectric_cos()](#核心算法)
3. [C++ 层面：node_shader_fresnel.cc](#cpp层面)
4. [GLSL 层面：gpu_shader_material_fresnel.glsl](#glsl层面)
5. [OSL 层面：node_fresnel.osl & node_fresnel.h](#osl层面)
6. [IOR（折射率）参数详解](#ior详解)
7. [常见材质折射率表](#材质折射率表)

---

<a name="物理原理"></a>
## 1. 物理原理与菲涅尔方程

### 1.1 什么是菲涅尔效应？

**菲涅尔效应（Fresnel Effect）** 描述了光线在不同介质交界面反射强度的物理现象：

- **垂直入射**（视线与法线平行）时，反射较弱
- **掠射角**（视线与法线接近90°）时，反射接近100%

这解释了为什么水面在远处看起来是镜面，而在脚下则是透明的。

### 1.2 菲涅尔方程（Fresnel Equations）

对于**电介质**（非金属）材质，菲涅尔反射系数 `F` 由以下公式给出：

```
菲涅尔反射系数 F = (Rs + Rp) / 2
```

其中：
- **Rs**：垂直偏振光反射率
- **Rp**：平行偏振光反射率

#### 完整公式推导

令：
- `ηi` = 入射介质折射率
- `ηt` = 透射介质折射率
- `cosθi` = 入射角余弦值（`θi` 为入射角）
- `η = ηt / ηi` = 相对折射率

首先计算折射角余弦值：
```
cosθt = √(1 - (1 - cos²θi) / η²)
```

当 `η > 1` 且 `cosθi` 较小时，可能发生**全内反射（TIR）**。

垂直偏振光反射率：
```
Rs = (ηi·cosθi - ηt·cosθt)² / (ηi·cosθi + ηt·cosθt)²
```

平行偏振光反射率：
```
Rp = (ηi·cosθt - ηt·cosθi)² / (ηi·cosθt + ηt·cosθi)²
```

最终反射系数：
```
F = (Rs + Rp) / 2
```

### 1.3 简化版本（常用渲染公式）

在计算机图形学中，常用以下简化版本：

```
cosθ = dot(I, N)  // 视线与法线点积
η = ηt / ηi       // 相对折射率

if (η > 1):
    // 需要检查全内反射
    sin²θt = (1 - cos²θ) / η²
    if (sin²θt > 1):
        return 1.0  // 全反射
    cosθt = √(1 - sin²θt)
else:
    cosθt = √(1 - (1 - cos²θ) / η²)

// 使用 Schlick 近似或精确公式
F = 0.5 × [(g-c)/(g+c)]² × [1 + ((c(g+c)-1)/(c(g-c)+1))²]
其中 g = √(η² - 1 + c²), c = |cosθ|
```

---

<a name="核心算法"></a>
## 2. 核心算法：fresnel_dielectric_cos()

Blender 使用一个优化的算法，避免计算折射方向。

### 2.1 算法原理

```glsl
/* source/blender/gpu/shaders/material/gpu_shader_material_fresnel.glsl */
float fresnel_dielectric_cos(float cosi, float eta)
{
  /* compute fresnel reflectance without explicitly computing
   * the refracted direction */
  float c = abs(cosi);
  float g = eta * eta - 1.0f + c * c;
  float result;

  if (g > 0.0f) {
    g = sqrt(g);
    float A = (g - c) / (g + c);
    float B = (c * (g + c) - 1.0f) / (c * (g - c) + 1.0f);
    result = 0.5f * A * A * (1.0f + B * B);
  }
  else {
    result = 1.0f; /* TIR (no refracted component) */
  }

  return result;
}
```

### 2.2 逐行解析

| 行号 | 代码 | 解释 |
|------|------|------|
| 9 | `float c = abs(cosi);` | 获取入射角余弦的绝对值，确保 `c ∈ [0, 1]` |
| 10 | `float g = eta * eta - 1.0f + c * c;` | 计算中间变量 `g`，用于判断TIR和后续计算 |
| 13-14 | `if (g > 0.0f) { g = sqrt(g); }` | 如果 `g > 0`，说明未发生TIR，计算 `√g` |
| 15 | `float A = (g - c) / (g + c);` | 计算 Fresnel 公式中的分量 A |
| 16 | `float B = (c * (g + c) - 1.0f) / (c * (g - c) + 1.0f);` | 计算 Fresnel 公式中的分量 B |
| 17 | `result = 0.5f * A * A * (1.0f + B * B);` | 组合 A 和 B，得到最终反射系数 |
| 19-20 | `else { result = 1.0f; }` | 如果 `g ≤ 0`，发生全内反射，反射率为 1.0 |

### 2.3 物理意义

这个公式是基于**精确菲涅尔方程**的代数变换，避免了以下计算：
- 不需要计算折射方向
- 不需要处理偏振分离（Rs, Rp）
- 直接输出非偏振光的平均反射率

---

<a name="cpp层面"></a>
## 3. C++ 层面：node_shader_fresnel.cc

### 3.1 节点声明

```cpp
/* source/blender/nodes/shader/nodes/node_shader_fresnel.cc */
static void node_declare(NodeDeclarationBuilder &b)
{
  b.add_input<decl::Float>("IOR").default_value(1.5f).min(0.0f).max(1000.0f);
  b.add_input<decl::Vector>("Normal").hide_value();
  b.add_output<decl::Float>("Factor", "Fac");
}
```

**输入参数：**
- **IOR**: 折射率，默认值 1.5（玻璃/塑料典型值），范围 0.0-1000.0
- **Normal**: 表面法向量，隐藏默认值（自动使用世界法线）

**输出参数：**
- **Fac**: 反射强度因子，范围 0.0-1.0

### 3.2 GPU 链接函数

```cpp
static int node_shader_gpu_fresnel(GPUMaterial *mat,
                                   bNode *node,
                                   bNodeExecData * /*execdata*/,
                                   GPUNodeStack *in,
                                   GPUNodeStack *out)
{
  if (!in[1].link) {
    /* 如果法线输入未连接，自动使用世界法线 */
    GPU_link(mat, "world_normals_get", &in[1].link);
  }

  /* 链接到 GLSL 函数 node_fresnel */
  return GPU_stack_link(mat, node, "node_fresnel", in, out);
}
```

**流程：**
1. 检查法线输入是否连接
2. 如果未连接，链接 `world_normals_get` 函数获取世界法线
3. 调用 GPU shader 函数 `node_fresnel`

### 3.3 MaterialX 支持

```cpp
NODE_SHADER_MATERIALX_BEGIN
#ifdef WITH_MATERIALX
{
  /* TODO: 待实现 */
  return get_input_value("IOR", NodeItem::Type::Float);
}
#endif
NODE_SHADER_SHADERX_END
```

### 3.4 节点注册

```cpp
void register_node_type_sh_fresnel()
{
  static blender::bke::bNodeType ntype;

  sh_node_type_base(&ntype, "ShaderNodeFresnel", SH_NODE_FRESNEL);
  ntype.ui_name = "Fresnel";
  ntype.ui_description = "Produce a blending factor depending on the angle "
                         "between the surface normal and the view direction "
                         "using Fresnel equations.\n"
                         "Typically used for mixing reflections at grazing angles";
  ntype.enum_name_legacy = "FRESNEL";
  ntype.nclass = NODE_CLASS_INPUT;
  ntype.declare = file_ns::node_declare;
  ntype.gpu_fn = file_ns::node_shader_gpu_fresnel;
  ntype.materialx_fn = file_ns::node_shader_materialx;

  blender::bke::node_register_type(ntype);
}
```

---

<a name="glsl层面"></a>
## 4. GLSL 层面：gpu_shader_material_fresnel.glsl

### 4.1 完整代码

```glsl
/* source/blender/gpu/shaders/material/gpu_shader_material_fresnel.glsl */

float fresnel_dielectric_cos(float cosi, float eta)
{
  /* compute fresnel reflectance without explicitly computing
   * the refracted direction */
  float c = abs(cosi);
  float g = eta * eta - 1.0f + c * c;
  float result;

  if (g > 0.0f) {
    g = sqrt(g);
    float A = (g - c) / (g + c);
    float B = (c * (g + c) - 1.0f) / (c * (g - c) + 1.0f);
    result = 0.5f * A * A * (1.0f + B * B);
  }
  else {
    result = 1.0f; /* TIR (no refracted component) */
  }

  return result;
}

float fresnel_dielectric(float3 Incoming, float3 Normal, float eta)
{
  /* compute fresnel reflectance without explicitly computing
   * the refracted direction */
  return fresnel_dielectric_cos(dot(Incoming, Normal), eta);
}

void node_fresnel(float ior, float3 N, out float result)
{
  N = normalize(N);
  float3 V = coordinate_incoming(g_data.P);

  float eta = max(ior, 0.00001f);
  result = fresnel_dielectric(V, N, (FrontFacing) ? eta : 1.0f / eta);
}
```

### 4.2 逐函数解析

#### 4.2.1 `fresnel_dielectric_cos(cosi, eta)`

这是核心计算函数，已在[第2章](#核心算法)详细解释。

#### 4.2.2 `fresnel_dielectric(Incoming, Normal, eta)`

```glsl
float fresnel_dielectric(float3 Incoming, float3 Normal, float eta)
{
  return fresnel_dielectric_cos(dot(Incoming, Normal), eta);
}
```

- **Incoming**: 视线方向向量（从表面指向相机）
- **Normal**: 表面法线向量
- **eta**: 相对折射率
- **功能**: 计算视线与法线的点积，调用核心函数

#### 4.2.3 `node_fresnel(ior, N, result)`

```glsl
void node_fresnel(float ior, float3 N, out float result)
{
  /* 1. 归一化法线 */
  N = normalize(N);

  /* 2. 计算视线方向 */
  float3 V = coordinate_incoming(g_data.P);

  /* 3. 处理折射率，避免除零 */
  float eta = max(ior, 0.00001f);

  /* 4. 考虑背面处理和法线计算 */
  result = fresnel_dielectric(V, N, (FrontFacing) ? eta : 1.0f / eta);
}
```

### 4.3 关键点解释

#### 4.3.1 `coordinate_incoming(g_data.P)`

这个函数计算从表面点到相机（或光源）的视线向量。

在 Blender 的 GPU shader 系统中：
- `g_data.P`: 当前片元的世界坐标
- `coordinate_incoming()`: 根据相机位置计算入射方向

**数学定义**：
```
V = normalize(camera_position - surface_point)
```

#### 4.3.2 `FrontFacing` 宏

```glsl
/* source/blender/gpu/shaders/gpu_shader_codegen_lib.glsl */
#ifdef GPU_FRAGMENT_SHADER
#  define FrontFacing gl_FrontFacing
#else
#  define FrontFacing true
#endif
```

- **gl_FrontFacing**: OpenGL 内置变量，`true` 表示正面，`false` 表示背面
- **用途**: 处理双面材质时的法线方向

#### 4.3.3 背面处理

```glsl
(FrontFacing) ? eta : 1.0f / eta
```

**为什么需要反转折射率？**

当渲染**背面**时：
- 光线从内部（折射率 η）射向外部（折射率 1.0）
- 相对折射率变为 `1.0 / η`

物理意义：从玻璃内部往外看 vs 从外部往里看。

#### 4.3.4 数值稳定性

```glsl
float eta = max(ior, 0.00001f);
```

- 防止 IOR 为 0 导致除零错误
- 实际物理中 IOR 不会为 0，但防止异常输入

---

<a name="osl层面"></a>
## 5. OSL 层面：node_fresnel.osl & node_fresnel.h

### 5.1 node_fresnel.osl

```osl
/* intern/cycles/kernel/osl/shaders/node_fresnel.osl */

#include "node_fresnel.h"
#include "stdcycles.h"

shader node_fresnel(float IOR = 1.45, normal Normal = N, output float Fac = 0.0)
{
  float f = max(IOR, 1e-5);
  float eta = backfacing() ? 1.0 / f : f;
  float cosi = dot(I, Normal);
  Fac = fresnel_dielectric_cos(cosi, eta);
}
```

#### 5.1.1 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| IOR | float | 1.45 | 折射率 |
| Normal | normal | N | 表面法线（N 是 OSL 内置） |
| Fac | float | 0.0 | 输出（反射强度） |

#### 5.1.2 与 GLSL 的区别

| 对比项 | GLSL | OSL |
|--------|------|-----|
| 法线输入 | 显式传递 `N` | 使用内置 `N` |
| 视线向量 | `coordinate_incoming(g_data.P)` | 内置 `I` |
| 背面判断 | `FrontFacing` 宏 | `backfacing()` 函数 |

**OSL 内置变量：**
- `I`: 入射光线方向（从表面指向相机）
- `N`: 表面法线
- `P`: 表面位置
- `backfacing()`: 返回是否为背面

### 5.2 node_fresnel.h

```c
/* intern/cycles/kernel/osl/shaders/node_fresnel.h */

float fresnel_dielectric_cos(float cosi, float eta)
{
  /* compute fresnel reflectance without explicitly computing
   * the refracted direction */
  float c = fabs(cosi);
  float g = eta * eta - 1 + c * c;
  float result;

  if (g > 0) {
    g = sqrt(g);
    float A = (g - c) / (g + c);
    float B = (c * (g + c) - 1) / (c * (g - c) + 1);
    result = 0.5 * A * A * (1 + B * B);
  }
  else {
    result = 1.0; /* TIR (no refracted component) */
  }

  return result;
}

color fresnel_conductor(float cosi, color eta, color k)
{
  color cosi2 = color(cosi * cosi);
  color one = color(1, 1, 1);
  color tmp_f = eta * eta + k * k;
  color tmp = tmp_f * cosi2;
  color Rparl2 = (tmp - (2.0 * eta * cosi) + one) / (tmp + (2.0 * eta * cosi) + one);
  color Rperp2 = (tmp_f - (2.0 * eta * cosi) + cosi2) / (tmp_f + (2.0 * eta * cosi) + cosi2);
  return (Rparl2 + Rperp2) * 0.5;
}

float F0_from_ior(float eta)
{
  float f0 = (eta - 1.0) / (eta + 1.0);
  return f0 * f0;
}

float ior_from_F0(float f0)
{
  float sqrt_f0 = sqrt(clamp(f0, 0.0, 0.99));
  return (1.0 + sqrt_f0) / (1.0 - sqrt_f0);
}
```

#### 5.2.1 额外函数解析

##### `fresnel_conductor(cosi, eta, k)`

这是用于**金属（导体）**的菲涅尔函数：

- **eta**: 复折射率的实部（折射率）
- **k**: 复折射率的虚部（吸收系数）
- **返回**: 金属的反射率（彩色）

与电介质不同，金属的折射率是复数：`η̂ = η + i·k`

##### `F0_from_ior(eta)`

计算**垂直入射**时的菲涅尔反射率：

```
F0 = ((η - 1) / (η + 1))²
```

**用途**：PBR 工作流中常用的近似公式，用于金属度（Metallic）工作流。

**示例**：
- 玻璃 (η=1.5): F0 = ((1.5-1)/(1.5+1))² = 0.04
- 钻石 (η=2.42): F0 = ((2.42-1)/(2.42+1))² = 0.17

##### `ior_from_F0(f0)`

`F0_from_ior` 的逆函数，从 F0 反推 IOR。

---

<a name="ior详解"></a>
## 6. IOR（折射率）参数详解

### 6.1 什么是 IOR？

**IOR (Index of Refraction)** 折射率，定义为：

```
IOR = c / v = n
```

其中：
- `c`: 真空中光速
- `v`: 介质中光速
- `n`: 折射率数值

### 6.2 物理意义

| IOR 值范围 | 物理意义 | 光的行为 |
|-----------|---------|---------|
| **= 1.0** | 真空/空气 | 无折射，全透射 |
| **> 1.0** | 常见介质 | 光速减慢，发生折射 |
| **< 1.0** | 非物理 | 理论上不存在（除特殊材料） |

### 6.3 在菲涅尔公式中的作用

IOR 影响两个方面：

1. **垂直入射反射率**：
   ```
   F0 = ((IOR - 1) / (IOR + 1))²
   ```
   - IOR 越大，F0 越大
   - 1.0 → 0.00
   - 1.5 → 0.04
   - 2.4 → 0.17

2. **掠射角行为**：
   - 所有非金属在掠射角都趋向 100% 反射
   - IOR 只影响过渡曲线的形状

### 6.4 数值范围限制

Blender 中 IOR 的限制：
- **最小值**: 0.00001（防止除零）
- **最大值**: 1000.0
- **推荐范围**: 1.0 - 3.0（绝大多数常见材质）

---

<a name="材质折射率表"></a>
## 7. 常见材质折射率表

### 7.1 非金属（电介质）

| 材质 | IOR | F0 (approx) | 说明 |
|------|-----|-------------|------|
| **真空** | 1.000 | 0.000 | 定义标准 |
| **空气** | 1.0003 | 0.000 | 近似为1.0 |
| **水** | 1.333 | 0.020 | 海水约1.34 |
| **冰** | 1.310 | 0.019 | - |
| **酒精** | 1.329 | 0.020 | 乙醇 |
| **甘油** | 1.473 | 0.032 | - |
| **玻璃** | 1.50-1.60 | 0.04 | 标准玻璃 |
| **水晶** | 1.544 | 0.041 | 石英 |
| **钻石** | 2.417 | 0.172 | 高折射率 |
| **红宝石** | 1.76-1.77 | 0.075 | 宝石 |
| **蓝宝石** | 1.76-1.77 | 0.075 | - |

### 7.2 金属（导体）

金属使用复折射率 `η + i·k`，常用 IOR 值：

| 金属 | IOR (η) | k (吸收) | 反射率 (垂直) | 反射率 (掠射) |
|------|---------|----------|---------------|---------------|
| **铝** | 1.39 | 7.61 | 0.91 | 0.98 |
| **铜** | 0.27 | 3.09 | 0.93 | 0.99 |
| **金** | 0.18 | 3.09 | 0.95 | 0.99 |
| **铁** | 2.94 | 3.05 | 0.65 | 0.98 |
| **银** | 0.15 | 3.93 | 0.96 | 0.99 |
| **钛** | 2.16 | 3.28 | 0.54 | 0.97 |

**注意**：金属在 Blender 的 Fresnel 节点中通常需要配合其他节点使用，因为 `fresnel_dielectric_cos()` 只处理电介质。

### 7.3 塑料和合成材料

| 材质 | IOR | F0 | 说明 |
|------|-----|-----|------|
| **聚苯乙烯** | 1.59 | 0.051 | 常见塑料 |
| **聚碳酸酯** | 1.58 | 0.050 | 防弹玻璃 |
| **聚乙烯** | 1.49 | 0.035 | 食品包装 |
| **丙烯酸** | 1.49 | 0.035 | 亚克力 |
| **橡胶** | 1.52 | 0.040 | - |

### 7.4 其他材料

| 材质 | IOR | F0 | 说明 |
|------|-----|-----|------|
| **皮肤** | 1.37-1.40 | 0.023 | SSS专用 |
| **脂肪** | 1.45 | 0.032 | - |
| **头发** | 1.55 | 0.044 | - |
| **油漆** | 1.50 | 0.040 | 油基漆 |
| **纸张** | 1.45-1.55 | 0.03-0.04 | - |

---

## 8. 实际应用示例

### 8.1 基本使用（混合反射）

```
材质节点设置：
Fresnel (IOR=1.5) → Mix Shader (Fac)
                    ↓
Diffuse BSDF       Glossy BSDF
                    ↓
Output
```

结果：
- 正面（法线视角）：主要显示 Diffuse
- 侧面（掠射角）：主要显示 Glossy 反射

### 8.2 配合玻璃材质

```
Principled BSDF:
- Transmission = 1.0
- IOR = 1.5
- Roughness = 0.0
```

Fresnel 自动应用，产生真实玻璃外观。

### 8.3 自定义 Fresnel 曲线

```
Layer Weight (Fresnel) → ColorRamp → Math(Multiply) → Mix Shader
                                                      ↓
                                              Diffuse/Emission
```

通过 ColorRamp 调整过渡曲线，实现艺术化控制。

---

## 9. 跨层面对比总结

| 层面 | 文件 | IOR上限 | 法线处理 | 视线计算 | 背面处理 |
|------|------|---------|----------|----------|----------|
| **C++** | node_shader_fresnel.cc | 1000.0 | GPU链接 | GPU链接 | GPU链接 |
| **GLSL** | gpu_shader_material_fresnel.glsl | 0.00001 | normalize | coordinate_incoming | FrontFacing |
| **OSL** | node_fresnel.osl | 1e-5 | 内置N | 内置I | backfacing() |

核心函数统一：
```
fresnel_dielectric_cos(cosi, eta)
├─ C++: 使用GPU链接调用GLSL
├─ GLSL: 直接实现，GPU执行
└─ OSL: 直接实现，CPU渲染
```

---

## 10. 性能优化与数值稳定性

### 10.1 优化技巧

1. **避免重复计算**：
   - 法线归一化只做一次
   - 点积计算在调用前完成

2. **分支预测**：
   - TIR 仅在 `eta > 1.0` 且 `cosi` 较小时发生
   - 现代 GPU 能很好处理此分支

3. **使用内置函数**：
   - `sqrt()` 硬件加速
   - `abs()` 单周期指令

### 10.2 数值边界处理

| 情况 | 处理方法 | 原因 |
|------|----------|------|
| IOR = 0 | `max(ior, 0.00001)` | 防止除零 |
| cosi = 0 | `abs(cosi)` | 避免负值 |
| IOR < 1.0 | 正常计算 | 物理上可能（但少见） |
| g ≤ 0 | `result = 1.0` | 全反射 |

---

## 参考文献

1. **物理原理**：
   - Fresnel Equations: https://en.wikipedia.org/wiki/Fresnel_equations
   - Schlick's Approximation: Schlick, Christophe (1994)

2. **Blender 源码**：
   - `source/blender/nodes/shader/nodes/node_shader_fresnel.cc`
   - `source/blender/gpu/shaders/material/gpu_shader_material_fresnel.glsl`
   - `intern/cycles/kernel/osl/shaders/node_fresnel.osl`
   - `intern/cycles/kernel/osl/shaders/node_fresnel.h`

3. **渲染理论**：
   - Physically Based Rendering (PBR) 文档
   - Real-Time Rendering, 4th Edition

---

**文档结束**
*本文档解析了 Blender Fresnel 节点在三个层面的完整实现，包括物理原理、核心算法和实际应用。*
