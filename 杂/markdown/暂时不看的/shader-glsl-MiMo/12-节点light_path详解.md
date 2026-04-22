# Light Path 节点深度解析（编号：012）

> **文档信息**
> - 创建日期：2025-12-18
> - Blender 版本：4.3+ (基于当前开发分支)
> - 涉及文件：
>   - `source/blender/nodes/shader/nodes/node_shader_light_path.cc`
>   - `source/blender/gpu/shaders/material/gpu_shader_material_light_path.glsl`
>   - `intern/cycles/kernel/osl/shaders/node_light_path.osl`
>   - `intern/cycles/kernel/svm/light_path.h`

---

## 目录
1. [概述与功能定位](#概述与功能定位)
2. [输出接口详解](#输出接口详解)
3. [三层实现架构对比](#三层实现架构对比)
4. [光线类型输出](#光线类型输出)
5. [深度输出](#深度输出)
6. [物理含义与渲染路径](#物理含义与渲染路径)
7. [实际应用场景](#实际应用场景)
8. [技术对比总结](#技术对比总结)

---

## 概述与功能定位

Light Path（光线路径）节点是 Blender 着色器系统中的**核心输入节点**，用于在着色器执行时获取当前光线的上下文信息。它允许艺术家根据光线的类型、深度等属性来控制材质表现，是实现非物理渲染技巧和高级材质效果的重要工具。

### 核心能力
- **8 种光线类型判断**：识别当前执行的光线类别
- **6 种深度追踪**：记录不同光线类型的反弹次数
- **1 个距离信息**：光线长度

---

## 输出接口详解

### 1. 光线类型判断（8 个 Boolean 输出）

| 输出名称 | 物理含义 | 使用场景 |
|---------|---------|---------|
| **Is Camera Ray** | 是否为主视图/相机发出的光线 | 区分直接观察 vs 反射/折射 |
| **Is Shadow Ray** | 是否为阴影计算光线 | 实现假阴影、卡通阴影 |
| **Is Diffuse Ray** | 是否为漫反射光线 | 控制间接光照细节 |
| **Is Glossy Ray** | 是否为光泽反射光线 | 镜面反射控制 |
| **Is Singular Ray** | 是否为奇异光线 | 特殊光源（太阳、HDRI） |
| **Is Reflection Ray** | 是否为反射光线 | 金属材质特殊处理 |
| **Is Transmission Ray** | 是否为透射光线 | 玻璃、SSS 材质优化 |
| **Is Volume Scatter Ray** | 是否为体积散射光线 | 体积雾效控制 |

### 2. 深度追踪（6 个数值输出）

| 输出名称 | 物理含义 | 取值范围 |
|---------|---------|---------|
| **Ray Length** | 光线从起点到当前点的物理距离 | 0 ~ ∞ |
| **Ray Depth** | 总反弹次数（所有类型累计） | 0 ~ Max Bounces |
| **Diffuse Depth** | 漫反射反弹次数 | 0 ~ Max Diffuse |
| **Glossy Depth** | 光泽反射反弹次数 | 0 ~ Max Glossy |
| **Transparent Depth** | 透明反弹次数 | 0 ~ Max Transparent |
| **Transmission Depth** | 透射反弹次数 | 0 ~ Max Transmission |
| **Portal Depth** | 光域网/门户反弹次数 | 0 ~ Max Portal |

---

## 三层实现架构对比

### 架构概览图

```
┌─────────────────────────────────────────────────────────────────┐
│                      Blender 节点编辑器                           │
│                    (node_shader_light_path.cc)                   │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                ┌─────────────────┴─────────────────┐
                │                                   │
        ┌───────▼───────┐                ┌────────▼────────┐
        │  EEVEE / GPU  │                │    Cycles SVM   │
        │  (GLSL)       │                │   (C++)         │
        └───────────────┘                └─────────────────┘
                │                                   │
                ▼                                   ▼
    ┌───────────────────────┐        ┌────────────────────────┐
    │ GPU材质管线            │        │  Cycles 渲染内核        │
    │ g_data 结构体          │        │  path_flag 位掩码       │
    └───────────────────────┘        └────────────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────────┐
                                    │  OSL (可选)          │
                                    │  raytype() / getattribute() │
                                    └──────────────────────┘
```

---

## 光线类型输出详解

### SVM (Cycles) 实现机制

**文件位置**：`intern/cycles/kernel/svm/light_path.h`

```cpp
template<uint node_feature_mask, typename ConstIntegratorGenericState>
ccl_device_noinline void svm_node_light_path(
    KernelGlobals kg,
    ConstIntegratorGenericState state,
    const ccl_private ShaderData *sd,
    ccl_private float *stack,
    const uint type,
    const uint out_offset,
    const uint32_t path_flag)
{
    // 通过路径标志位判断光线类型
    switch ((NodeLightPath)type) {
        case NODE_LP_camera:
            info = (path_flag & PATH_RAY_CAMERA) ? 1.0f : 0.0f;
            break;
        case NODE_LP_shadow:
            info = (path_flag & PATH_RAY_SHADOW) ? 1.0f : 0.0f;
            break;
        // ... 其他类型
    }
}
```

**关键数据结构**：
- `path_flag`：32 位掩码，存储当前光线属性
- `PATH_RAY_CAMERA` = (1 << 0)
- `PATH_RAY_SHADOW` = (1 << 9)  // 单独的阴影标志
- `PATH_RAY_DIFFUSE` = (1 << 3)
- `PATH_RAY_GLOSSY` = (1 << 4)

### GLSL (EEVEE) 实现机制

**文件位置**：`source/blender/gpu/shaders/material/gpu_shader_material_light_path.glsl`

```glsl
void node_light_path(
    out float is_camera_ray,
    out float is_shadow_ray,
    /* ... 其他输出 */)
{
    /* 通过 g_data.ray_type 比较 */
    is_camera_ray = float(g_data.ray_type == RAY_TYPE_CAMERA);
    is_shadow_ray = float(g_data.ray_type == RAY_TYPE_SHADOW);
    is_diffuse_ray = float(g_data.ray_type == RAY_TYPE_DIFFUSE);
    is_glossy_ray = float(g_data.ray_type == RAY_TYPE_GLOSSY);

    /* 部分复用 */
    is_singular_ray = is_glossy_ray;
    is_reflection_ray = is_glossy_ray;
    is_transmission_ray = is_glossy_ray;
}
```

**g_data 结构定义**（来自 eevee_surf_lib.glsl）：
```glsl
#ifdef MAT_SHADOW
    g_data.ray_type = RAY_TYPE_SHADOW;
#elif defined(MAT_CAPTURE)
    g_data.ray_type = RAY_TYPE_DIFFUSE;
#else
    g_data.ray_type = uniform_buf.pipeline.ray_type;
#endif
```

**限制**：
- `is_volume_scatter_ray`：不支持（始终返回 0）
- `transparent_depth`：不支持（始终返回 0）
- `portal_depth`：不支持（始终返回 0）

### OSL (Cycles OSL) 实现机制

**文件位置**：`intern/cycles/kernel/osl/shaders/node_light_path.osl`

```osl
shader node_light_path(
    output float IsCameraRay = 0.0,
    output float IsShadowRay = 0.0,
    /* ... 其他输出 */)
{
    IsCameraRay = raytype("camera");
    IsShadowRay = raytype("shadow");
    IsDiffuseRay = raytype("diffuse");
    IsGlossyRay = raytype("glossy");
    IsSingularRay = raytype("singular");
    IsReflectionRay = raytype("reflection");
    IsTransmissionRay = raytype("refraction");  // 注意：参数为 "refraction"
    IsVolumeScatterRay = raytype("volume_scatter");

    getattribute("path:ray_length", RayLength);
    getattribute("path:ray_depth", RayDepth);
    getattribute("path:diffuse_depth", DiffuseDepth);
    // ...
}
```

**OSL 内置函数**：
- `raytype(string name)`：返回 1.0 如果当前光线匹配类型
- `getattribute(string name, output type)`：获取光线路径属性

---

## 深度输出详解

### SVM 深度计算

**文件位置**：`intern/cycles/kernel/svm/light_path.h` 第 55-101 行

```cpp
case NODE_LP_ray_depth: {
    /* 从 integrator state 获取反弹计数 */
    IF_KERNEL_NODES_FEATURE(LIGHT_PATH) {
        info = (float)integrator_state_bounce(state, path_flag);
    }

    /* 阴影和发射光额外 +1 */
    if (path_flag & (PATH_RAY_SHADOW | PATH_RAY_EMISSION)) {
        info += 1.0f;
    }
    break;
}

case NODE_LP_ray_diffuse:
    info = (float)integrator_state_diffuse_bounce(state, path_flag);
    break;

case NODE_LP_ray_glossy:
    info = (float)integrator_state_glossy_bounce(state, path_flag);
    break;

case NODE_LP_ray_transparent:
    info = (float)integrator_state_transparent_bounce(state, path_flag);
    break;

case NODE_LP_ray_transmission:
    info = (float)integrator_state_transmission_bounce(state, path_flag);
    break;

case NODE_LP_ray_portal:
    info = (float)integrator_state_portal_bounce(kg, state, path_flag);
    break;
```

### GLSL 深度计算

**文件位置**：`source/blender/gpu/shaders/material/gpu_shader_material_light_path.glsl` 第 30-33 行

```glsl
ray_depth = g_data.ray_depth;
diffuse_depth = (is_diffuse_ray == 1.0f) ? g_data.ray_depth : 0.0f;
glossy_depth = (is_glossy_ray == 1.0f) ? g_data.ray_depth : 0.0f;
transmission_depth = (is_transmission_ray == 1.0f) ? glossy_depth : 0.0f;
```

**关键区别**：
- EEVEE 的深度计算是**条件性**的
- Diffuse Depth 仅在当前为漫反射光线时才有值
- Transmission Depth = Glossy Depth（不区分）

### OSL 深度获取

```osl
int ray_depth = 0;
getattribute("path:ray_length", RayLength);
getattribute("path:ray_depth", ray_depth);
RayDepth = (float)ray_depth;
```

OSL 通过 `getattribute` 从渲染器内部获取预计算的深度值。

---

## 物理含义与渲染路径

### 典型渲染路径示例

考虑一个光线路径：**相机 → 金属球 → 漫反射墙面 → 光源**

```
路径阶段        | Ray Type      | Depth | Diffuse | Glossy
----------------|---------------|-------|---------|--------
相机发射        | Camera        | 0     | 0       | 0
击中金属球      | Glossy        | 1     | 0       | 1
反射到墙面      | Diffuse       | 2     | 1       | 0
最终采样光源    | Emission      | 2     | 1       | 0
```

### 透明反弹路径（玻璃）

```
路径阶段        | Type      | Ray | Transp | Transm
----------------|-----------|-----|--------|--------
相机            | Camera    | 0   | 0      | 0
进入玻璃        | Transm    | 1   | 0      | 1
穿过玻璃        | Transm    | 1   | 1      | 1
离开玻璃        | Camera    | 1   | 2      | 1
```

### 体积散射路径

```
路径阶段        | Type          | Ray Vol
----------------|---------------|--------
相机            | Camera        | 0
进入雾          | Volume Scatter| 1
散射            | Volume Scatter| 2
最终            | Diffuse       | 2
```

---

## 实际应用场景

### 1. 限制光泽反射次数（防止噪点）

```python
# 节点连接
Light Path → Glossy Depth → Math(Greater Than, 3) → Mix Shader
                        ↓
              Glossy BSDF      Transparent BSDF
```

**效果**：超过 3 次光泽反射后变为透明，节省渲染时间。

### 2. 镜子只在第一跳显示

```python
# 节点连接
Light Path → Ray Depth → Math(Equal, 0) → Mix Shader
                      ↓
            Glossy BSDF     Emission (黑色)
```

**效果**：镜子只在直接观察时显示反射，间接光照中变黑。

### 3. 区分相机路径和间接路径的发光

```python
# 节点连接
Light Path → Is Camera Ray → Mix Shader
                        ↓
              Emission      Holdout
```

**效果**：直接可见的材质发光，间接光照完全透明。

### 4. 菲涅尔效应增强

```python
# 节点连接
Light Path → Is Glossy Ray → Mix Shader (结合 Layer Weight)
                         ↓
                   高光层     无高光层
```

**效果**：仅在光泽反射光线下显示高光，其他情况下保持无光泽外观。

### 5. 体积雾的距离衰减

```python
# 节点连接
Light Path → Ray Length → Math(Multiply) → Volume Scatter Density
```

**效果**：光线穿行距离越长，体积散射密度越小。

### 6. 阴影遮罩技巧

```python
# 节点连接
Light Path → Is Shadow Ray → Mix Shader
                        ↓
                  Diffuse BSDF   Transparent
```

**效果**：物体对阴影光线不可见，但对其他光线可见。

### 7. 优化 SSS 次表面散射

```python
# 节点连接
Light Path → Transmission Depth → Math(Greater Than, 1) → Mix Shader
                             ↓
                       SSS BSDF   Diffuse BSDF
```

**效果**：限制次表面散射深度，防止过暗的内部散射。

---

## 技术对比总结

| 特性 | SVM (Cycles) | GLSL (EEVEE) | OSL (Cycles OSL) |
|------|--------------|--------------|------------------|
| **实现方式** | 指令 + 位掩码 | 结构体比较 | 内置函数 |
| **光线类型完整度** | ✅ 8/8 | ⚠️ 5/8 (部分复用) | ✅ 8/8 |
| **深度追踪完整度** | ✅ 6/6 | ⚠️ 4/6 (部分限制) | ✅ 6/6 |
| **Ray Length** | ✅ | ✅ | ✅ |
| **Transparent Depth** | ✅ | ❌ (硬编码 0) | ✅ |
| **Portal Depth** | ✅ | ❌ (硬编码 0) | ✅ |
| **Volume Scatter** | ✅ | ❌ (硬编码 0) | ✅ |
| **性能开销** | 低（位运算） | 低（比较） | 中（函数调用） |
| **可用性** | ✅ 生产环境 | ⚠️ 部分支持 | ✅ 生产环境 |

### 编译器优化提示

#### SVM
```c
// 高效的位掩码检查
if (path_flag & PATH_RAY_DIFFUSE) { /* ... */ }
```

#### GLSL
```glsl
// GPU 分支预测友好
float is_diffuse = float(g_data.ray_type == RAY_TYPE_DIFFUSE);
```

#### OSL
```osl
// 解释执行，开销较大
IsDiffuseRay = raytype("diffuse");
```

---

## 总结

Light Path 节点是连接**渲染器内部状态**与**艺术家控制**的桥梁。三层实现反映了不同渲染引擎的设计哲学：

1. **SVM (Cycles)**：高效、完整，基于位掩码的系统级实现
2. **GLSL (EEVEE)**：受限但实时，基于状态结构体的 GPU 实现
3. **OSL (Cycles)**：灵活、通用，基于函数查询的脚本实现

掌握这些差异对于创作**跨渲染器兼容**的材质和**性能优化**至关重要。建议在生产中：
- 使用高阶输出（如 Ray Depth）而非枚举类型判断
- 注意 EEVEE 的功能限制
- 通过烘焙测试验证材质行为

---

## 参考资料

- Blender 源码：`source/blender/nodes/shader/nodes/node_shader_light_path.cc`
- GPU 着色器：`source/blender/gpu/shaders/material/gpu_shader_material_light_path.glsl`
- Cycles OSL：`intern/cycles/kernel/osl/shaders/node_light_path.osl`
- SVM 内核：`intern/cycles/kernel/svm/light_path.h`
- 测试文件：`tests/files/render/integrator/light_path_*.blend`

---

**文档版本**：v1.0
**更新日期**：2025-12-18
