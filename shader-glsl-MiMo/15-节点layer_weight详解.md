# 015-Layer Weight 节点深度详解

**编号**: 015
**创建日期**: 2025-12-18
**文档类型**: Shader节点技术分析
**Blender版本**: 4.x

---

## 一、节点概述

Layer Weight 节点是 Blender 着色器系统中用于**基于视角角度**生成混合因子的输入节点。它提供了两种物理上不同的权重计算模式：**Fresnel（菲涅尔）**和 **Facing（面向）**。

### 输出接口

| 输出接口 | 物理意义 | 取值范围 |
|---------|---------|---------|
| **Fresnel** | 基于菲涅尔反射定律的反射率 | 0.0 ~ 1.0 |
| **Facing** | 基于法线与视角夹角的简单权重 | 0.0 ~ 1.0 |

---

## 二、物理原理与数学推导

### 2.1 Fresnel 输出：物理精确的反射率计算

#### 物理背景

菲涅尔效应描述了光在不同介质界面反射时，**反射率随入射角变化**的现象。当光线垂直入射时反射最少，掠射时反射最强。

#### 数学公式推导

##### 1. 完整菲涅尔公式（偏振光）

对于非偏振光，反射率 `F` 为：

```
F(θ) = ½ [ (sin²(θ_i - θ_t) / sin²(θ_i + θ_t)) + (tan²(θ_i - θ_t) / tan²(θ_i + θ_t)) ]
```

其中：
- `θ_i`：入射角
- `θ_t`：折射角
- `η = n₂/n₁`：相对折射率

##### 2. 布鲁斯特公式（非偏振光，简化版）

通过斯涅尔定律和三角恒等式，可简化为：

```
cosi = N · V  (入射角余弦)

g = √(η² - 1 + cosi²)

反射率 F = ½ × [ (g - cosi)/(g + cosi) ]² × [ 1 + ( (cosi(g + cosi) - 1)/(cosi(g - cosi) + 1) )² ]
```

##### 3. 绝缘体的透射率与反射率关系

**关键物理原理**：
- 能量守恒：**反射率 + 透射率 = 1**
- Layer Weight 的 Fresnel 输出 = **透射率 T = 1 - F**

因此：
```
T = 1 - Fresnel_Dielectric(cosθ, η)
```

#### 混合因子（Blend）的含义

在 Blender 中，Blend 值被转换为折射率：
```python
η = max(1.0 - Blend, 0.00001)
```

- Blend = 0.0 → η = 1.0（与空气相同，无反射）
- Blend = 0.5 → η = 0.5（强反射）
- Blend = 1.0 → η = 0.00001（极限情况，接近完全反射）

> **注意**：当观察方向**从内部指向外部**（FrontFacing = true），需要使用倒数 `1/η` 来保证物理正确性。

---

### 2.2 Facing 输出：几何角度权重

#### 物理背景

Facing 模式**不是物理模拟**，而是基于**几何关系**的简单余弦衰减。用于快速层混合，不考虑折射。

#### 数学公式推导

##### 基础公式

```
cosθ = |N · V|  (视角与法线点积的绝对值)
```

- 当视角与法线平行（正面）：cosθ = 1.0
- 当视角与法线垂直（边缘）：cosθ = 0.0

##### 混合因子影响

原始面向权重：
```
facing_raw = |cosθ|
```

应用混合因子 `b`：
```
if (b == 0.5):
    facing = facing_raw
else:
    b = clamp(blend, 0.0, 0.99999)
    b = (b < 0.5) ? 2b : 0.5/(1 - b)
    facing = facing_raw^b
```

##### 最终输出

```
Facing = 1 - facing
```

**曲线变换说明**：
- `b < 0.5`：`facing = x^(2b)`，曲线在原点更陡峭
- `b > 0.5`：`facing = x^(0.5/(1-b))`，曲线在原点更平缓

---

## 三、三层实现对比分析

### 3.1 C++ 节点定义层

**文件**: `source/blender/nodes/shader/nodes/node_shader_layer_weight.cc`

```cpp
static void node_declare(NodeDeclarationBuilder &b)
{
  b.add_input<decl::Float>("Blend").default_value(0.5f).min(0.0f).max(1.0f);
  b.add_input<decl::Vector>("Normal").hide_value();
  b.add_output<decl::Float>("Fresnel");
  b.add_output<decl::Float>("Facing");
}

static int node_shader_gpu_layer_weight(...)
{
  if (!in[1].link) {
    GPU_link(mat, "world_normals_get", &in[1].link);
  }
  return GPU_stack_link(mat, node, "node_layer_weight", in, out);
}
```

**功能**：
- 声明节点接口
- 动态链接世界空间法线
- 调用 GPU shader 函数 `node_layer_weight`

---

### 3.2 GLSL GPU 实现层

**文件**: `source/blender/gpu/shaders/material/gpu_shader_material_layer_weight.glsl`

```glsl
void node_layer_weight(float blend, float3 N, out float fresnel, out float facing)
{
  N = normalize(N);

  /* Fresnel 计算 */
  float eta = max(1.0f - blend, 0.00001f);
  float3 V = coordinate_incoming(g_data.P);

  fresnel = fresnel_dielectric(V, N, (FrontFacing) ? 1.0f / eta : eta);

  /* Facing 计算 */
  facing = abs(dot(V, N));
  if (blend != 0.5f) {
    blend = clamp(blend, 0.0f, 0.99999f);
    blend = (blend < 0.5f) ? 2.0f * blend : 0.5f / (1.0f - blend);
    facing = pow(facing, blend);
  }
  facing = 1.0f - facing;
}
```

#### 关键依赖函数

```glsl
// gpu_shader_material_fresnel.glsl
float fresnel_dielectric_cos(float cosi, float eta) {
  float c = abs(cosi);
  float g = eta * eta - 1.0f + c * c;

  if (g > 0.0f) {
    g = sqrt(g);
    float A = (g - c) / (g + c);
    float B = (c * (g + c) - 1.0f) / (c * (g - c) + 1.0f);
    return 0.5f * A * A * (1.0f + B * B);
  }
  else {
    return 1.0f;  /* TIR - 全内反射 */
  }
}
```

---

### 3.3 OSL 渲染实现层

**文件**: `intern/cycles/kernel/osl/shaders/node_layer_weight.osl`

```osl
shader node_layer_weight(float Blend = 0.5,
                         normal Normal = N,
                         output float Fresnel = 0.0,
                         output float Facing = 0.0)
{
  float blend = Blend;
  float cosi = dot(I, Normal);

  /* Fresnel */
  float eta = max(1.0 - Blend, 1e-5);
  eta = backfacing() ? eta : 1.0 / eta;
  Fresnel = fresnel_dielectric_cos(cosi, eta);

  /* Facing */
  Facing = fabs(cosi);

  if (blend != 0.5) {
    blend = clamp(blend, 0.0, 1.0 - 1e-5);
    blend = (blend < 0.5) ? 2.0 * blend : 0.5 / (1.0 - blend);
    Facing = pow(Facing, blend);
  }

  Facing = 1.0 - Facing;
}
```

#### OSL 依赖函数

```osl
// node_fresnel.h
float fresnel_dielectric_cos(float cosi, float eta) {
  float c = fabs(cosi);
  float g = eta * eta - 1 + c * c;

  if (g > 0) {
    g = sqrt(g);
    float A = (g - c) / (g + c);
    float B = (c * (g + c) - 1) / (c * (g - c) + 1);
    return 0.5 * A * A * (1 + B * B);
  }
  else {
    return 1.0;  /* TIR */
  }
}
```

---

## 四、实现差异与技术细节

### 4.1 坐标系统差异

| 层面 | 视角向量获取 | 坐标系 |
|------|------------|--------|
| **GLSL** | `coordinate_incoming(g_data.P)` | 世界空间 |
| **OSL** | `I`（内置变量） | 眼睛空间 |
| **物理意义** | 都是从表面指向相机的向量 | - |

### 4.2 FrontFacing 处理

**GLSL**:
```glsl
fresnel = fresnel_dielectric(V, N, (FrontFacing) ? 1.0f / eta : eta);
```

**OSL**:
```glsl
eta = backfacing() ? eta : 1.0 / eta;
```

两者等价，方向处理一致。

### 4.3 数据精度

| 层面 | 最小值限制 | 说明 |
|------|-----------|------|
| GLSL | `0.00001f` | float 精度 |
| OSL | `1e-5` | 双精度浮点 |

---

## 五、实际应用场景

### 5.1 Fresnel 输出用途

**物理现象模拟**：
- ✅ **水面边缘增强**：水体在边缘处反射更强
- ✅ **玻璃材质边界**：玻璃边缘的明亮反射
- ✅ **复杂光照混合**：金属与非金属的平滑过渡
- ✅ **次表面散射过渡**：皮肤、蜡质材质的边缘发光

**工作流程**：
```glsl
// 清漆层混合
vec3 base = texture(diffuse, uv).rgb;
vec3 coat = texture(clearcoat, uv).rgb;
float fresnel = node_layer_weight_blend(0.5);

vec3 final = mix(base, coat, fresnel);
```

### 5.2 Facing 输出用途

**几何级混合**：
- ✅ **地形纹理过渡**：山顶岩石到山谷草地的混合
- ✅ **卡通风格着色**：基于角度的明暗分界
- ✅ **快速原型**：不依赖物理的快速混合
- ✅ **艺术控制**：创作者想要的任意角度混合

**工作流程**：
```glsl
// 地形混合
float facing = node_layer_weight_blend(0.3);
float slope = pow(facing, 2.0);  // 陡坡为1，平地为0
vec3 final = mix(valley, mountain, slope);
```

### 5.3 参数调优指南

#### Blend = 0.5（默认）

**Fresnel**：
- 反射率 ≈ 0.04（空气-介质标准）
- 适用于：水、玻璃、塑料

**Facing**：
- 线性变化，无指数加强
- 适用于：通用混合

#### Blend < 0.5（偏向下层）

**Fresnel**：
- 整体反射率降低（η 增大）
- 适用于：弱反射材质

**Facing**：
- 在垂直角度变化更敏感
- 适用于：强调边缘

#### Blend > 0.5（偏向上层）

**Fresnel**：
- 整体反射率增高（η 减小）
- 适用于：强反射材质

**Facing**：
- 在正面区域变化平缓
- 适用于：平滑过渡

---

## 六、性能与精度优化

### 6.1 计算复杂度

- **Fresnel**：O(1) - 单次平方根 + 多次乘法
- **Facing**：O(1) - 单次点积 + 条件分支

### 6.2 优化建议

1. **预计算**：Blend 固定时可预计算指数
2. **分支优化**：GLSL 中 `blend != 0.5` 分支很少触发，GPU 分支预测高效
3. **近似计算**：快速预览可用近似公式
   ```
   fresnel ≈ F0 + (1 - F0) * (1 - cosθ)^5  // Schlick近似
   ```

---

## 七、总结对比表

| 特性 | Fresnel | Facing |
|------|---------|--------|
| **物理基础** | 电磁波理论 | 几何角度 |
| **精度** | 高（完整BRDF） | 低（纯几何） |
| **计算开销** | 中（需要平方根） | 低（仅点积） |
| **Blend 参数** | 转化为折射率 | 转化为指数幂 |
| **用途** | 真实材质混合 | 艺术控制混合 |
| **边缘效果** | 物理准确 | 人为可控 |
| **常用值** | 0.3 ~ 0.7 | 0.0 ~ 1.0 |

---

## 参考资料

1. **物理公式**：基于 Schlick 近似和完整菲涅尔公式
2. **实现源码**：
   - `source/blender/nodes/shader/nodes/node_shader_layer_weight.cc`
   - `source/blender/gpu/shaders/material/gpu_shader_material_layer_weight.glsl`
   - `intern/cycles/kernel/osl/shaders/node_layer_weight.osl`
3. **相关理论**：Jones' 向量矩阵、斯涅尔定律、能量守恒

---

**文档版本**: 1.0
**维护状态**: 活跃
