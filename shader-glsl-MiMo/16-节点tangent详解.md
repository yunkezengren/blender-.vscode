# 深度解析 Blender Tangent 节点

## 文档信息
- **编号**: 016
- **文件名**: 016-节点tangent详解.md
- **创建日期**: 2025-12-18
- **主题**: Tangent 节点的三个层面实现详解

---

## 1. 概述

Tangent（切线）节点是 Blender 着色器系统中用于生成切线方向的关键组件，主要用于各向异性 BSDF（Anisotropic BSDF）着色和法线贴图计算。本文档将从 C++ 接口层面、GPU 渲染层面和 Cycles 渲染器三个维度深入分析其实现机制。

### 1.1 核心功能
- **生成切线向量**：为表面提供切线空间的 T 轴
- **两种工作模式**：UV Map 模式和 Radial（径向）模式
- **坐标系支持**：Object Space, World Space, Tangent Space
- **输出能力**：Tangent 和 Bitangent（副切线）向量

---

## 2. 三种实现层面分析

### 2.1 C++ 接口层 (`node_shader_tangent.cc`)

#### 2.1.1 数据结构定义

```cpp
// E:\blender-git\blender\source\blender\makesdna\DNA_node_types.h:1679
typedef struct NodeShaderTangent {
  int direction_type;      // 方向类型：0=Radial, 1=UV Map
  int axis;                // 轴向：0=X, 1=Y, 2=Z
  char uv_map[64];        // UV 贴图名称
} NodeShaderTangent;
```

#### 2.1.2 枚举常量

```cpp
// E:\blender-git\blender\source\blender\makesdna\DNA_node_types.h:2815-2826
/* 方向类型 */
enum {
  SHD_TANGENT_RADIAL = 0,   // 径向模式
  SHD_TANGENT_UVMAP = 1,    // UV Map 模式
};

/* 轴向选择 */
enum {
  SHD_TANGENT_AXIS_X = 0,   // X 轴
  SHD_TANGENT_AXIS_Y = 1,   // Y 轴
  SHD_TANGENT_AXIS_Z = 2,   // Z 轴（默认）
};
```

#### 2.1.3 节点声明与 UI

```cpp
static void node_declare(NodeDeclarationBuilder &b)
{
  b.add_output<decl::Vector>("Tangent");  // 只有一个 Tangent 输出
}
```

UI 按钮逻辑：
```cpp
static void node_shader_buts_tangent(ui::Layout &layout, bContext *C, PointerRNA *ptr)
{
  // 显示方向类型选择：Radial 或 UV Map
  layout.prop(ptr, "direction_type", ...);

  if (RNA_enum_get(ptr, "direction_type") == SHD_TANGENT_UVMAP) {
    // UV Map 模式：显示 UV 层选择器
    layout.prop_search(ptr, "uv_map", &dataptr, "uv_layers", ...);
  }
  else {
    // Radial 模式：显示轴向选择
    layout.prop(ptr, "axis", ...);
  }
}
```

#### 2.1.4 GPU 材质链接

```cpp
static int node_shader_gpu_tangent(GPUMaterial *mat,
                                   bNode *node,
                                   bNodeExecData * /*execdata*/,
                                   GPUNodeStack *in,
                                   GPUNodeStack *out)
{
  NodeShaderTangent *attr = static_cast<NodeShaderTangent *>(node->storage);

  if (attr->direction_type == SHD_TANGENT_UVMAP) {
    // UV Map 模式：从 mesh 属性获取切线
    return GPU_stack_link(mat, node, "node_tangentmap", in, out,
                          GPU_attribute(mat, CD_TANGENT, attr->uv_map));
  }

  // Radial 模式：基于原始坐标计算
  GPUNodeLink *orco = GPU_attribute(mat, CD_ORCO, "");

  // 根据轴向选择不同的 orco 变换函数
  if (attr->axis == SHD_TANGENT_AXIS_X) {
    GPU_link(mat, "tangent_orco_x", orco, &orco);
  }
  else if (attr->axis == SHD_TANGENT_AXIS_Y) {
    GPU_link(mat, "tangent_orco_y", orco, &orco);
  }
  else {
    GPU_link(mat, "tangent_orco_z", orco, &orco);
  }

  return GPU_stack_link(mat, node, "node_tangent", in, out, orco);
}
```

---

### 2.2 GPU 渲染层 (`gpu_shader_material_tangent.glsl`)

#### 2.2.1 Radial 模式核心算法

**X 轴径向切线生成**：
```glsl
void tangent_orco_x(float3 orco_in, out float3 orco_out)
{
  // 坐标重映射：xzy 交换 + 偏移
  orco_out = orco_in.xzy * float3(0.0f, -0.5f, 0.5f) + float3(0.0f, 0.25f, -0.25f);
}
```

**Y 轴径向切线生成**：
```glsl
void tangent_orco_y(float3 orco_in, out float3 orco_out)
{
  orco_out = orco_in.zyx * float3(-0.5f, 0.0f, 0.5f) + float3(0.25f, 0.0f, -0.25f);
}
```

**Z 轴径向切线生成**：
```glsl
void tangent_orco_z(float3 orco_in, out float3 orco_out)
{
  orco_out = orco_in.yxz * float3(-0.5f, 0.5f, 0.0f) + float3(0.25f, -0.25f, 0.0f);
}
```

#### 2.2.2 UV Map 模式处理

```glsl
void node_tangentmap(float4 attr_tangent, out float3 tangent)
{
  tangent = normalize(attr_tangent.xyz);  // 从属性获取并归一化
}
```

#### 2.2.3 最终切线计算与坐标变换

```glsl
void node_tangent(float3 orco, out float3 T)
{
  // 1. 坐标变换：Object Space → World Space
  direction_transform_object_to_world(orco, T);

  // 2. 核心算法：确保切线与法线正交
  // T = N × (T × N) 规范化后的结果
  T = cross(g_data.N, normalize(cross(T, g_data.N)));
}
```

#### 2.2.4 坐标变换工具

```glsl
// E:\blender-git\blender\source\blender\gpu\shaders\material\gpu_shader_material_transform_utils.glsl
void direction_transform_object_to_world(float3 vin, out float3 vout)
{
  vout = to_float3x3(drw_modelmat()) * vin;  // 3x3 矩阵变换（方向向量）
}
```

**GlobalData 结构**：
```glsl
// E:\blender-git\blender\source\blender\gpu\shaders\gpu_shader_codegen_lib.glsl
struct GlobalData {
  packed_float3 P;          // World position
  packed_float3 N;          // Surface Normal (normalized, bump affected)
  packed_float3 Ng;         // Geometric Normal
  // ... 其他成员
};
```

---

### 2.3 Cycles 渲染器层

#### 2.3.1 OSL 实现 (`node_tangent.osl`)

```cpp
shader node_tangent(string attr_name = "geom:tangent",
                    string direction_type = "radial",
                    string axis = "z",
                    output normal Tangent = normalize(dPdu))
{
  vector T = vector(0.0, 0.0, 0.0);

  // 1. UV Map 模式：从属性获取
  if (direction_type == "uv_map") {
    getattribute(attr_name, T);
  }
  // 2. Radial 模式：基于生成坐标计算
  else if (direction_type == "radial") {
    point generated;

    // 尝试获取生成坐标，失败则使用位置
    if (!getattribute("geom:generated", generated))
      generated = P;

    // 根据轴向计算切线
    if (axis == "x")
      T = vector(0.0, -(generated[2] - 0.5), (generated[1] - 0.5));
    else if (axis == "y")
      T = vector(-(generated[2] - 0.5), 0.0, (generated[0] - 0.5));
    else
      T = vector(-(generated[1] - 0.5), (generated[0] - 0.5), 0.0);
  }

  // 坐标系变换并确保正交
  T = transform("object", "world", T);
  Tangent = cross(N, normalize(cross(T, N)));
}
```

#### 2.3.2 SVM 实现 (`tex_coord.h`)

```cpp
ccl_device_noinline void svm_node_tangent(KernelGlobals kg,
                                          ccl_private ShaderData *sd,
                                          ccl_private float *stack,
                                          const uint4 node)
{
  uint tangent_offset, direction_type, axis;
  svm_unpack_node_uchar3(node.y, &tangent_offset, &direction_type, &axis);

  float3 tangent;
  float3 attribute_value;

  // 获取属性
  const AttributeDescriptor desc = find_attribute(kg, sd, node.z);

  if (direction_type == NODE_TANGENT_UVMAP) {
    tangent = attribute_value;  // 直接使用属性值
  }
  else {
    // Radial 模式计算
    float3 generated = (desc.offset == ATTR_STD_NOT_FOUND) ? sd->P : attribute_value;

    if (axis == NODE_TANGENT_AXIS_X) {
      tangent = make_float3(0.0f, -(generated.z - 0.5f), (generated.y - 0.5f));
    }
    else if (axis == NODE_TANGENT_AXIS_Y) {
      tangent = make_float3(-(generated.z - 0.5f), 0.0f, (generated.x - 0.5f));
    }
    else {
      tangent = make_float3(-(generated.y - 0.5f), (generated.x - 0.5f), 0.0f);
    }
  }

  // 变换到世界空间并确保与法线正交
  object_normal_transform(kg, sd, &tangent);
  tangent = cross(sd->N, normalize(cross(tangent, sd->N)));

  stack_store_float3(stack, tangent_offset, tangent);
}
```

---

## 3. 数学原理深入分析

### 3.1 切线空间基础

在表面着色点处，我们定义一个三维正交坐标系：

```
Tangent Space:
   T (Tangent):     主切线方向，通常与 UV 的 U 方向对应
   B (Bitangent):   副切线方向，通常与 UV 的 V 方向对应
   N (Normal):      法线方向，垂直于表面
```

**正交约束**：
```
T · N = 0
B · N = 0
T · B = 0
|T| = |B| = |N| = 1
```

### 3.2 核心算法：`T = N × (T × N)`

这个算法确保了输出的切线严格与法线正交：

```glsl
T = cross(N, normalize(cross(T, N)));
```

**数学推导**：

1. **第一步**：`cross(T, N)`
   - 产生一个与 T 和 N 都垂直的向量
   - 这个向量位于切平面内，是 B 的方向

2. **第二步**：`normalize(cross(T, N))`
   - 归一化得到单位 B 向量（忽略符号）

3. **第三步**：`cross(N, B)`
   - 重新计算 T 向量（红箭头），确保持垂直

**几何解释**：
```
      N
      ↑
      |
      |----> T (原始)
     / \
    /   \
   B     T' (修正后)

T' = N × B
```

### 3.3 Radial 模式的几何意义

以 Z 轴为例，Radial 模式计算：

```glsl
T = vector(-(generated.y - 0.5), (generated.x - 0.5), 0.0);
```

**几何直观**：
- 假设物体中心在 (0.5, 0.5, 0.5)
- `generated.x - 0.5` 和 `generated.y - 0.5` 表示相对于中心的位置
- 在 XY 平面上，`(dy, -dx)` 正好是绕 Z 轴的切向方向

**可视化**：
```
         ↑ Y
         |
   Q2    |    Q1
         |
---------+--------> X
         |
   Q3    |    Q4
         |

对于点 P(x,y)，切线方向：(-(y-0.5), x-0.5, 0)
相当于围绕中心点的旋转切线
```

### 3.4 坐标系变换流程

#### 3.4.1 GPU 渲染管线

```
Object Space → [Radial Calc] → [Orthogonalize] → World Space
                    ↑
               或
                    ↑
          [UV Map Attribute] → [Normalize] → World Space
```

```
(blender-git) $ source\blender\gpu\shaders\material\gpu_shader_material_tangent.glsl

节点计算流程：
1. UV Map 模式：attr_tangent → normalize → codomain check
2. Radial 模式：orco → transform → direction_calc → orthogonality
3. 两者都通过：T = cross(N, normalize(cross(T_raw, N)))
4. 最终输出：World Space 切线向量
```

#### 3.4.2 渲染器对比

| 特性 | GPU (EEVEE) | OSL (Cycles) | SVM (Cycles) |
|------|-------------|--------------|--------------|
| **坐标变换** | `direction_transform_object_to_world` | `transform("object", "world")` | `object_normal_transform` |
| **输入源** | `g_data.N` | `N` | `sd->N` |
| **Radial 计算** | Shader 内置函数 | OSL 向量运算 | SIMD 浮点运算 |
| **正交化** | `cross(N, normalize(cross(T,N)))` | 相同 | 相同 |

---

## 4. Bitangent（副切线）与 Tangent 节点的关系

### 4.1 Bitangent 的重要性

虽然 Tangent 节点只输出 Tangent，但 Bitangent 在实际应用中同样重要：

```glsl
// E:\blender-git\blender\source\blender\gpu\shaders\material\gpu_shader_material_normal_map.glsl
void node_normal_map(float4 tangent, float strength, float3 texnormal, out float3 outnormal)
{
  float3 B = tangent.w * cross(g_data.Ni, tangent.xyz);
  // 法线贴图转换：T * nx + B * ny + N * nz
  outnormal = texnormal.x * tangent.xyz + texnormal.y * B + texnormal.z * g_data.Ni;
}
```

**Tangent 的 W 分量**：
- W 分量存储了 bitangent 的符号（手性）
- `B = sign * cross(N, T)` 其中 sign = tangent.w

### 4.2 如何获得 Bitangent

在 Blender 中，Bitangent 可以通过以下方式获得：

#### 方法 1：数学计算
```python
import bpy

# 在 Python 中计算
tangent = ... # Tangent 节点输出
normal = ...  # 法线

bitangent = mathutils.Vector(tangent).cross(normal)
# 根据需要乘以符号
```

#### 方法 2：使用 Geometry Workflow
在现代渲染管线中，通常由这四个向量构成切线空间：
- Position (P)
- Normal (N)
- Tangent (T)
- Bitangent (B = cross(N, T) * sign)

---

## 5. 实际应用案例

### 5.1 法线贴图（Normal Mapping）

```
Shader Graph:

[Texture: Normal Map]
         ↓
[Normal Map Node]
         ↓
[Tangent Node] --┐
                 ↓
             [Mix/Combine]
                 ↓
           [Surface BSDF]
```

**配置要点**：
```glsl
// 1. 获取 Tangent
tangent = node_tangent(orco)  // 或从 UV Map

// 2. 法线贴图转换
float3 normal_map = texture(normal_tex, uv).xyz * 2.0 - 1.0;
float3 world_normal = tangent.x * T + tangent.y * B + tangent.z * N;

// 3. 应用于 BSDF
bsdf.N = world_normal;
```

### 5.2 各向异性反射（Anisotropic Reflections）

各向异性 BSDF 需要 Tangent 来控制反射的拉伸方向：

```
[Texture: Anisotropic Direction] → [Tangent] → [Anisotropic BSDF]
```

**参数设置**：
- `Tangent`：控制各向异性方向（0°, 90°, 180° 等）
- `Roughness U/V`：U 和 V 方向的不同粗糙度

### 5.3 圆柱/球体贴图（Radial Mode）

对于圆柱或球体物体，使用 Radial 模式能获得自然的切线方向：

**适用场景**：
- 瓶子标签环绕
- 汽车车身反光
- 圆柱形包装盒

**配置**：
- 选择轴向（X/Y/Z）匹配物体的对称轴
- 系统自动计算每个点的切向方向

---

## 6. 总结与最佳实践

### 6.1 模式选择指南

| 应用场景 | 推荐模式 | 轴向选择 | 备注 |
|---------|---------|---------|------|
| **标准网格** | UV Map | N/A | 需要正确 UV 展开 |
| **圆柱体** | Radial | Z (或 Y) | 匹配物体对称轴 |
| **球体** | Radial | X/Y/Z | 任一轴均可，效果一致 |
| **程序化几何** | Radial | 根据需要 | 不需要 UV |

### 6.2 调试技巧

1. **可视化 Tangent**：
   - 连接到 Emission 节点观察方向
   - 红色 = X (+/-), 绿色 = Y (+/-), 蓝色 = Z (+/-)

2. **检查正交性**：
   ```glsl
   float dot_product = dot(tangent, normal);
   assert(abs(dot_product) < 0.001);  // 应该接近 0
   ```

3. **UV Map 检查**：
   - 确保 UV 层名正确
   - 验证 UV 展开无重叠

### 6.3 性能考量

- **UV Map 模式**：查询属性，适合静态场景
- **Radial 模式**：实时计算，适合程序化/变形对象
- **Radial 计算量**：轻量，近似 O(1)

---

## 7. 参考实现文件

| 层面 | 文件路径 | 功能 |
|------|---------|------|
| **C++ 接口** | `E:\blender-git\blender\source\blender\gas\nodes\shader\nodes\node_shader_tangent.cc` | 节点定义、UI、GPU 链接 |
| **GPU 实现** | `E:\blender-git\blender\source\blender\gpu\shaders\material\gpu_shader_material_tangent.glsl` | GPU 着色器核心逻辑 |
| **Cycles OSL** | `E:\blender-git\blender\intern\cycles\kernel\osl\shaders\node_tangent.osl` | OSL 渲染器实现 |
| **Cycles SVM** | `E:\blender-git\blender\intern\cycles\kernel\svm\tex_coord.h` | SVM 渲染器实现 |
| **坐标变换** | `E:\blender-git\blender\source\blender\gpu\shaders\material\gpu_shader_material_transform_utils.glsl` | 坐标系转换工具 |
| **数据结构** | `E:\blender-git\blender\source\blender\makesdna\DNA_node_types.h` | 节点数据定义 |
| **RNA 定义** | `E:\blender-git\blender\source\blender\makesrna\intern\\rna_nodetree.cc` | 接口属性定义 |

---

## 8. 附录：关键公式汇总

### 8.1 正交切线计算
```
T_final = N × normalize(T_input × N)
B_final = sign × (N × T_final)
```

### 8.2 Radial 模式公式
```
X 轴：T = (0, -(z-0.5), (y-0.5))
Y 轴：T = (-(z-0.5), 0, (x-0.5))
Z 轴：T = (-(y-0.5), (x-0.5), 0)
```

### 8.3 法线贴图变换
```
world_normal = T × T_normal + B × B_normal + N × N_normal
```

### 8.4 符号手性（Handness）
```
bitangent = tangent.w × cross(normal, tangent.xyz)
```

---

**文档结束**
*Generated by analyzing Blender source code across three implementation layers*
