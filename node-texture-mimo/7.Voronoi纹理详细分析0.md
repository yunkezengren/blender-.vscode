# Blender Voronoi 纹理节点详细技术文档

## 目录
1. [概述](#概述)
2. [沃罗诺伊图数学原理](#沃罗诺伊图数学原理)
3. [距离度量](#距离度量)
4. [特征输出](#特征输出)
5. [参数详解](#参数详解)
6. [高维实现策略](#高维实现策略)
7. [实现细节](#实现细节)
8. [实际应用](#实际应用)
9. [参考文献](#参考文献)

## 概述

Voronoi 纹理节点在 Blender 中用于生成基于 Worley 噪声的程序化纹理。它通过将空间划分为单元格并计算到最近特征点的距离来创建各种图案。

**源代码位置:**
- C++ 实现: `source/blender/nodes/shader/nodes/node_shader_tex_voronoi.cc`
- GPU GLSL: `source/blender/gpu/shaders/material/gpu_shader_material_voronoi.glsl`
- OSL 实现: `intern/cycles/kernel/osl/shaders/node_voronoi_texture.osl`
- SVM 实现: `intern/cycles/kernel/svm/voronoi.h`

**节点输出:**
- **Distance**: 到最近点的距离
- **Color**: 单元格的颜色（基于哈希）
- **Position**: 特征点的位置
- **W**: 4D 坐标的第四个分量（1D 或 4D 维度时）
- **Radius**: N-球体半径（仅用于 N Sphere Radius 特征）

## 沃罗诺伊图数学原理

### 基本定义

沃罗诺伊图（Voronoi Diagram）是将空间划分为若干区域（单元格）的几何结构。对于一组离散点（称为生成点或细胞核），每个单元格包含所有距离该生成点比距离其他生成点更近的点。

数学上，对于点集 **P** = {**p**₁, **p**₂, ..., **p**ₙ}，第 i 个单元格定义为:
```
V(i) = { **x** ∈ ℝᵈ | ||**x** - **p**ᵢ|| ≤ ||**x** - **p**ⱼ||, ∀j ≠ i }
```

### Worley 噪声

Blender 实现的是 Worley 噪声（也称为细胞噪声），它是沃罗诺伊图的扩展：

1. **空间离散化**: 将连续空间划分为整数网格单元
2. **随机点生成**: 在每个网格单元中，通过哈希函数生成一个随机位置的点
3. **距离计算**: 对于任意采样点，计算到附近所有网格单元中点的距离
4. **特征提取**: 返回最近（F1）或次近（F2）距离等特征

### 1D 沃罗诺伊实现

```
cellPosition = floor(coord)
localPosition = coord - cellPosition

// 遍历相邻单元格：-1, 0, 1
for i in [-1, 0, 1]:
    cellOffset = i
    pointPosition = cellOffset + hash(cellPosition + cellOffset) * randomness
    distanceToPoint = |pointPosition - localPosition|
```

### 2D/3D/4D 沃罗诺伊实现

在更高维度中，需要遍历相邻的超立方体：

**2D**: 遍历 3×3 = 9 个相邻单元格
**3D**: 遍历 3×3×3 = 27 个相邻单元格
**4D**: 遍历 3×3×3×3 = 81 个相邻单元格

实现策略:
```cpp
// 伪代码
minDistance = ∞
targetOffset = (0, 0, ...)
targetPosition = (0, 0, ...)

for each neighborOffset in [-1, 0, 1]^dimensions:
    pointPosition = neighborOffset +
                    hash(cellPosition + neighborOffset) * randomness
    distance = voronoi_distance(pointPosition, localPosition, params)
    if distance < minDistance:
        minDistance = distance
        targetOffset = neighborOffset
        targetPosition = pointPosition
```

## 距离度量

Blender 支持四种距离度量方式，定义在:
- **C++**: `source/blender/nodes/shader/nodes/node_shader_tex_voronoi.cc`
- **字典**: `intern/cycles/kernel/svm/voronoi.h` (lines 56-72)
- **GLSL**: `source/blender/gpu/shaders/material/gpu_shader_material_voronoi.glsl` (lines 56-121)

### 1. 欧几里得距离 (Euclidean) - 默认

**枚举值**: `SHD_VORONOI_EUCLIDEAN` / `NODE_VORONOI_EUCLIDEAN` (0)

**数学公式**:
- **1D**: `d = |b - a|`
- **2D**: `d = √((x₂-x₁)² + (y₂-y₁)²)`
- **3D**: `d = √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²)`
- **4D**: `d = √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)² + (w₂-w₁)²)`

**GLSL 实现**:
```glsl
float voronoi_distance(float a, float b) {
    return abs(a - b);
}

float voronoi_distance(float2 a, float2 b, VoronoiParams params) {
    if (params.metric == SHD_VORONOI_EUCLIDEAN) {
        return distance(a, b);  // 内置函数
    }
    // ...
}
```

**特点**:
- 最自然的圆形距离
- 计算最复杂（需要平方根）
- 产生平滑的圆形图案

### 2. 曼哈顿距离 (Manhattan)

**枚举值**: `SHD_VORONOI_MANHATTAN` / `NODE_VORONOI_MANHATTAN` (1)

**数学公式**:
- **1D**: `d = |b - a|`
- **2D**: `d = |x₂-x₁| + |y₂-y₁|`
- **3D**: `d = |x₂-x₁| + |y₂-y₁| + |z₂-z₁|`
- **4D**: `d = |x₂-x₁| + |y₂-y₁| + |z₂-z₁| + |w₂-w₁|`

**GLSL 实现**:
```glsl
float voronoi_distance(float2 a, float2 b, VoronoiParams params) {
    if (params.metric == SHD_VORONOI_MANHATTAN) {
        return abs(a.x - b.x) + abs(a.y - b.y);
    }
    // ...
}
```

**特点**:
- 类似城市街区距离
- 产生菱形/多边形图案
- 计算快速（无需平方根）
- 常用于网格结构

### 3. 切比雪夫距离 (Chebychev) - 切块距离

**枚举值**: `SHD_VORONOI_CHEBYCHEV` / `NODE_VORONOI_CHEBYCHEV` (2)

**数学公式**:
- **1D**: `d = |b - a|`
- **2D**: `d = max(|x₂-x₁|, |y₂-y₁|)`
- **3D**: `d = max(|x₂-x₁|, |y₂-y₁|, |z₂-z₁|)`
- **4D**: `d = max(|x₂-x₁|, |y₂-y₁|, |z₂-z₁|, |w₂-w₁|)`

**GLSL 实现**:
```glsl
float voronoi_distance(float2 a, float2 b, VoronoiParams params) {
    if (params.metric == SHD_VORONOI_CHEBYCHEV) {
        return max(abs(a.x - b.x), abs(a.y - b.y));
    }
    // ...
}
```

**特点**:
- 八边形/正方形图案
- 棋盘距离
- 产生方形的单元格

### 4. 闵可夫斯基距离 (Minkowski) - 广义距离

**枚举值**: `SHD_VORONOI_MINKOWSKI` / `NODE_VORONOI_MINKOWSKI` (3)

**数学公式**:
- **通用**: `d = (∑|Δxᵢ|^p)^(1/p)`

**2D 示例**:
```
d = (|x₂-x₁|^p + |y₂-y₁|^p)^(1/p)
```

**GLSL 实现**:
```glsl
float voronoi_distance(float2 a, float2 b, VoronoiParams params) {
    if (params.metric == SHD_VORONOI_MINKOWSKI) {
        return pow(pow(abs(a.x - b.x), params.exponent) +
                   pow(abs(a.y - b.y), params.exponent),
                   1.0 / params.exponent);
    }
    // ...
}
```

**极值情况**:
- `p → 0`: 扇形图案
- `p = 1`: 等价于曼哈顿距离
- `p = 2`: 等价于欧几里得距离
- `p → ∞`: 等价于切比雪夫距离

**Exponent 参数**:
- 范围: 0.0 - 32.0
- 控制距离计算的"弯曲"程度
- 低值: 接近曼哈顿距离
- 高值: 接近切比雪夫距离

## 特征输出

特征定义在:
- `source/blender/makesdna/DNA_node_types.h` (lines 2721-2727)
- `intern/cycles/kernel/svm/types.h` (lines 337-343)

### 1. F1 (第一最近距离)

**枚举值**: `SHD_VORONOI_F1` / `NODE_VORONOI_F1` (0)

**计算过程**:
```cpp
minDistance = FLT_MAX
targetOffset = 0
targetPosition = 0

for each neighborCell in [3×3×... neighborhood]:
    point = cellOffset + hash(cell) * randomness
    distance = voronoi_distance(point, localPosition, params)

    if distance < minDistance:
        minDistance = distance
        targetOffset = cellOffset
        targetPosition = point

// 颜色基于目标单元格哈希
color = hash(cellPosition + targetOffset)

// 位置 = 目标点位置 + 单元格位置
position = targetPosition + cellPosition
```

**输出**:
- `Distance`: 到最近点的距离
- `Color`: 最近点所在单元格的随机颜色
- `Position`: 最近点的实际坐标

**特点**: 产生"坑洞"效果，中心暗边缘亮

### 2. F2 (第二最近距离)

**枚举值**: `SHD_VORONOI_F2` / `NODE_VORONOI_F2` (1)

**计算过程**:
```cpp
distanceF1 = FLT_MAX
distanceF2 = FLT_MAX
offsetF1 = 0, offsetF2 = 0
positionF1 = 0, positionF2 = 0

for each neighborCell:
    point = cellOffset + hash(cell) * randomness
    distance = voronoi_distance(point, localPosition, params)

    if distance < distanceF1:
        distanceF2 = distanceF1
        distanceF1 = distance
        offsetF2 = offsetF1
        offsetF1 = cellOffset
        positionF2 = positionF1
        positionF1 = point
    else if distance < distanceF2:
        distanceF2 = distance
        offsetF2 = cellOffset
        positionF2 = point

// F2 输出
distance = distanceF2  // 注意：返回的是 F2 距离
color = hash(cellPosition + offsetF2)  // F2 单元格颜色
position = positionF2 + cellPosition
```

**输出**:
- `Distance`: 第二近点的距离
- `Color`: 第二近点所在单元格的颜色
- `Position`: 第二近点的坐标

**特点**: 产生蜂窝状图案，中心亮边缘暗

### 3. Smooth F1 (平滑第一最近距离)

**枚举值**: `SHD_VORONOI_SMOOTH_F1` / `NODE_VORONOI_SMOOTH_F1` (2)

**算法**: 基于 Inigo Quilez 的平滑函数

```cpp
smoothDistance = 0
smoothColor = (0, 0, 0)
smoothPosition = 0
h = -1  // 权重系数

// 扩展范围：-2 到 2（比 F1 的 -1 到 1 更大）
for each neighborCell in [-2, 2]^dimensions:
    point = cellOffset + hash(cell) * randomness
    distance = voronoi_distance(point, localPosition, params)

    // Smoothstep 计算
    if h == -1:
        h = 1.0
    else:
        h = smoothstep(0, 1, 0.5 + 0.5 * (smoothDistance - distance) / smoothness)

    correction = smoothness * h * (1 - h)

    // 平滑混合
    smoothDistance = mix(smoothDistance, distance, h) - correction
    smoothColor = mix(smoothColor, hash(cell), h) - correction * (1 + 3*smoothness)^(-1)
    smoothPosition = mix(smoothPosition, point, h) - correction * (1 + 3*smoothness)^(-1)
```

**核心公式**:
```
h = smoothstep(0, 1, 0.5 + 0.5 * (prevDist - curDist) / smoothness)
correction = smoothness * h * (1 - h)
smooth = mix(prev, cur, h) - correction
```

**输出**:
- `Distance`: 平滑距离
- `Color`: 混合颜色
- `Position`: 混合位置

**特点**: 产生渐变过渡，类似水波或云层

### 4. Distance to Edge (到边缘距离)

**枚举值**: `SHD_VORONOI_DISTANCE_TO_EDGE` / `NODE_VORONOI_DISTANCE_TO_EDGE` (3)

**1D 实现**:
```cpp
// 已经在每个单元格中心和边界都有点
// 计算到这些边界中点的距离

midPoint = hash(cellPosition) * randomness
leftPoint = -1 + hash(cellPosition - 1) * randomness
rightPoint = 1 + hash(cellPosition + 1) * randomness

// 两个边界中点
midLeft = (midPoint + leftPoint) / 2
midRight = (midPoint + rightPoint) / 2

distanceLeft = |midLeft - localPosition|
distanceRight = |midRight - localPosition|

return min(distanceLeft, distanceRight)
```

**2D/3D/4D 实现**:
```cpp
// 第一遍：找到最近的点
vectorToClosest = 0
minDistance = FLT_MAX

for each neighborCell:
    vectorToPoint = cellOffset + hash(cell) * randomness - localPosition
    distanceSq = dot(vectorToPoint, vectorToPoint)  // 平方距离

    if distanceSq < minDistance:
        minDistance = distanceSq
        vectorToClosest = vectorToPoint

// 第二遍：计算到边缘距离
minEdgeDistance = FLT_MAX

for each neighborCell:
    vectorToPoint = cellOffset + hash(cell) * randomness - localPosition
    perpendicular = vectorToPoint - vectorToClosest

    if length(perpendicular) > 0.0001:
        // 边缘中点
        edgeMidPoint = (vectorToClosest + vectorToPoint) / 2
        // 到边缘距离 = 到中点在垂直方向上的距离
        distanceToEdge = dot(edgeMidPoint, normalize(perpendicular))
        minEdgeDistance = min(minEdgeDistance, distanceToEdge)

return minEdgeDistance
```

**几何意义**:
```
      . (point)
     / \
    /   \
   /     \
  .-------. (closest point, edge midpoint)

distanceToEdge = 从 point 到边的垂直距离
```

**特点**: 产生线框效果，类似细胞膜或电路板

### 5. N-Sphere Radius (N-球体半径)

**枚举值**: `SHD_VORONOI_N_SPHERE_RADIUS` / `NODE_VORONOI_N_SPHERE_RADIUS` (4)

**算法**: 计算以最近点为中心，经过次近点的球体半径

```cpp
// 步骤 1: 找到最近点
closestPoint = 0
closestPointOffset = 0
minDistanceSq = INF

for each neighborCell:
    point = cellOffset + hash(cell) * randomness
    distSq = lengthSquared(point - localPosition)

    if distSq < minDistanceSq:
        minDistanceSq = distSq
        closestPoint = point
        closestPointOffset = cellOffset

// 步骤 2: 找到最近点的最近邻
closestNeighbor = 0
minNeighborSq = INF

for each neighborCell (skip origin):
    if neighborCell == closestPointOffset:
        continue

    cellOffset = neighborCell
    point = cellOffset + hash(cell) * randomness
    distSq = lengthSquared(closestPoint - point)

    if distSq < minNeighborSq:
        minNeighborSq = distSq
        closestNeighbor = point

// 步骤 3: 计算半径
// 半径 = 两点距离的一半
radius = distance(closestNeighbor, closestPoint) / 2.0
```

**几何意义**:
- 找到最近点 C
- 找到 C 的最近邻 N
- 以 (C + N)/2 为圆心，|C - N|/2 为半径的球体刚好相切

**特点**: 产生孔洞或气泡效果，所有孔大小相同

## 参数详解

### Scale (缩放)

**来源**:
- `NodeTexVoronoi` 结构体中的 `NodeTexBase base` 包含 `tex_mapping`
- 输入: `Scale`

**作用**:
```cpp
coord *= Scale;  // 所有维度
w *= Scale;      // 1D 和 4D 额外的 W 分量
```

**数学效果**:
- 将输入坐标空间缩放
- `Scale = 5.0`: 空间缩小 5 倍 → 图案放大 5 倍
- `Scale = 0.1`: 空间放大 10 倍 → 图案缩小 10 倍
- 负值: 镜像 + 缩放

**UI 行为**:
- 范围: -1000.0 到 1000.0
- 默认: 5.0
- 空间变换后才会应用其他参数

### Randomness (随机性)

**来源**: `NodeTexVoronoi` 结构体

**作用**: 控制每个单元格内特征点的偏移程度

```cpp
pointPosition = cellOffset + hash(cellPosition + cellOffset) * randomness;
```

**数学解释**:
- `randomness = 0.0`: 点固定在单元格原点 (0, 0, ...)
- `randomness = 1.0`: 点在单元格内均匀随机分布
- `randomness = 0.5`: 点在半径为 0.5 的范围内随机

**UI 行为**:
- 范围: 0.0 - 1.0
- 默认: 1.0
- 类型: Factor (滑块)
- 影响 `max_distance` 计算

### Jitter (抖动) - Randomness 的另一名称

在文档和实现中，Randomness 有时被称为 Jitter，两者相同。

### Detail (细节等级)

**来源**: `NodeTexVoronoi` 通过 `fractal_voronoi_x_fx` 函数

**作用**: 控制分形噪声的叠加层数（类似于 fBM）

```cpp
float amplitude = 1.0;
float max_amplitude = 0.0;
float scale = 1.0;

for (int i = 0; i <= ceil(detail); i++) {
    // 生成当前层级的 Voronoi
    VoronoiOutput octave = ... // 使用 scale 进行缩放

    if (detail == 0 || roughness == 0) {
        // 无分形，直接返回
        return octave;
    }

    // 分形叠加
    max_amplitude += amplitude;
    output.distance += octave.distance * amplitude;
    output.color += octave.color * amplitude;
    output.position += octave.position * amplitude / scale;

    // 下一层级
    scale *= lacunarity;
    amplitude *= roughness;
}

// 剩余层级（如果 detail 不是整数）
if (detail != floor(detail)) {
    remainder = detail - floor(detail);
    // 线性插值
}
```

**层级缩放**:
- 第 0 层: scale = 1
- 第 1 层: scale = lacunarity
- 第 2 层: scale = lacunarity²
- ...

**UI 行为**:
- 范围: 0.0 - 15.0
- 默认: 0.0 (无分形)
- 整数: 精确层级数
- 小数: 最后层级部分混合

### Lacunarity (空隙度)

**来源**: VoronoiParams

**作用**: 控制每层之间的缩放倍数

```cpp
scale *= lacunarity;  // 在每个分形迭代后
```

**数学解释**:
- `lacunarity = 2.0`: 每层缩小到 1/2
- `lacunarity = 4.0`: 每层缩小到 1/4
- 较高值: 层级间跨度大，细节减少
- 较低值: 层级间跨度小，细节丰富

**UI 行为**:
- 范围: 0.0 - 1000.0
- 默认: 2.0

### Roughness (粗糙度)

**来源**: VoronoiParams

**作用**: 控制每层的振幅衰减

```cpp
amplitude *= roughness;  // 在每个分形迭代后
```

**数学解释**:
- `roughness = 1.0`: 所有层级振幅相同 (1, 1, 1, ...)
- `roughness = 0.5`: 振幅指数衰减 (1, 0.5, 0.25, ...)
- `roughness = 0.0`: 仅第一层有效

**UI 行为**:
- 范围: 0.0 - 1.0
- 默认: 0.5
- 类型: Factor

### Smoothness (平滑度)

**来源**: VoronoiParams (用于 Smooth F1)

**作用**: 控制平滑混合的程度

```cpp
params.smoothness = clamp(Smoothness / 2.0, 0.0, 0.5f);
```

**混合公式**:
```glsl
h = smoothstep(0, 1, 0.5 + 0.5 * (smoothDistance - distanceToPoint) / params.smoothness)
correctionFactor = params.smoothness * h * (1.0 - h)
smoothDistance = mix(smoothDistance, distanceToPoint, h) - correctionFactor
```

**参数转换**:
- UI 输入: 0.0 - 1.0
- 内部: Smoothness / 2.0
- 实际范围: 0.0 - 0.5

**效果**:
- 值越大: 曲线更平滑，过渡更柔和
- 值越小: 接近标准 F1，锐利边缘

### Exponent (指数)

**来源**: VoronoiParams (用于 Minkowski 距离)

**作用**: 控制闵可夫斯基距离的指数

```cpp
distance = pow(
    pow(abs(a.x - b.x), params.exponent) +
    pow(abs(a.y - b.y), params.exponent),
    1.0 / params.exponent
)
```

**UI 行为**:
- 范围: 0.0 - 32.0
- 默认: 0.5
- 仅在 Metric = Minkowski 且维度 ≠ 1 时可用

**特殊值**:
- `exponent = 1.0`: 曼哈顿距离
- `exponent = 2.0`: 欧几里得距离
- `exponent = 10.0+`: 切比雪夫距离

### Normalize (标准化)

**来源**: VoronoiParams

**作用**: 将输出值归一化到 [0, 1] 范围

```cpp
if (params.normalize) {
    output.distance /= max_amplitude * params.max_distance;
    output.color /= max_amplitude;
}
```

**max_distance 计算**:
```cpp
// For 2D/3D/4D
params.max_distance = voronoi_distance(
    origin,
    vector3(0.5 + 0.5 * randomness, ...),
    params
) * ((feature == F2) ? 2.0 : 1.0);

// For 1D
params.max_distance = (0.5 + 0.5 * randomness) * ((feature == F2) ? 2.0 : 1.0);
```

**UI 行为**:
- 开关: 勾选/取消
- 默认: 未勾选
- 用于纹理贴图时建议开启

## 高维实现策略

### 坐标系统

Blender 支持 1D, 2D, 3D, 4D Voronoi：

**1D**: 使用 W 输入
```
W -> Scale -> Voronoi 1D
```

**2D**: 使用 Vector (x, y)
```
Vector.xy -> Scale -> Voronoi 2D
```

**3D**: 使用 Vector (x, y, z)
```
Vector.xyz -> Scale -> Voronoi 3D
```

**4D**: 使用 Vector (x, y, z) + W
```
Vector.xyz + W -> Scale -> Voronoi 4D
```

### 高维扫描策略

为了维持性能，避免 N^d 复杂度，采用以下优化：

**实际扫描窗口**:
- **1D**: 检查 -1, 0, 1 (3 个单元格)
- **2D**: 检查 3×3 = 9 个单元格
- **3D**: 检查 3×3×3 = 27 个单元格
- **4D**: 检查 3×4×4×4 = 27→81 个单元格

**为什么是 -1 到 1**:
理论最远距离发生在:
```
P = (0.5, 0.5, ...)
Q = (-0.5, -0.5, ...)

距离 = √(1² + 1² + ... ) ≤ 3 (for 3D)
```
所以只需要检查相邻单元格。

**扩展窗口 (Smooth F1)**:
```cpp
// Smooth F1 使用 -2 到 2
for j in -2..2:
    for i in -2..2:
        // 更多邻居，更好的平滑
```

### 内存优化: 边界检查

```cpp
// SVM (Shader Virtual Machine) 实现
template<typename T>
ccl_device float voronoi_distance_bound(
    const T a,
    const T b,
    const ccl_private VoronoiParams ¶ms
) {
    if (params.metric == NODE_VORONOI_EUCLIDEAN) {
        return len_squared(a - b);  // 使用平方距离，避免 sqrt
    }
    // 其他度量直接使用距离
}
```

**优化原理**:
- 比较距离时，`d1 < d2` ⇔ `d1² < d2²`
- 避免 sqrt 计算
- 最终输出时才计算实际距离

### 哈希函数

```cpp
// 1D
hash_float_to_float(cellPosition)  // 返回 [0, 1)

// 2D
hash_int2_to_float2(cellPosition)  // 返回 float2([0, 1), [0, 1))

// 3D
hash_int3_to_float3(cellPosition)  // 返回 float3([0, 1), [0, 1), [0, 1))

// 4D
hash_int4_to_float4(cellPosition)  // 返回 float4([0, 1), ..., [0, 1))
```

基于高速哈希算法，保证:
- 相同输入 → 相同输出（确定性）
- 不同输入 → 统计上均匀分布
- 快速计算

### 位置编码

```cpp
// 1D
float4 voronoi_position(float coord) {
    return float4(0, 0, 0, coord);
}

// 2D
float4 voronoi_position(float2 coord) {
    return float4(coord.x, coord.y, 0, 0);
}

// 3D
float4 voronoi_position(float3 coord) {
    return float4(coord.x, coord.y, coord.z, 0);
}

// 4D
float4 voronoi_position(float4 coord) {
    return coord;
}
```

## 实现细节

### C++ 实现 (node_shader_tex_voronoi.cc)

**节点注册**:
```cpp
void register_node_type_sh_tex_voronoi() {
    static bNodeType ntype;
    common_node_type_base(&ntype, "ShaderNodeTexVoronoi", SH_NODE_TEX_VORONOI);

    ntype.ui_name = "Voronoi Texture";
    ntype.ui_description = "Generate Worley noise based on the distance to random points...";

    ntype.declare = sh_node_tex_voronoi_declare;
    ntype.draw_buttons = node_shader_buts_tex_voronoi;
    ntype.initfunc = node_shader_init_tex_voronoi;
    ntype.gpu_fn = node_shader_gpu_tex_voronoi;
    ntype.build_multi_function = sh_node_voronoi_build_multi_function;
}
```

**GPU 链接**:
```cpp
static int node_shader_gpu_tex_voronoi(GPUMaterial *mat, ...) {
    NodeTexVoronoi *tex = (NodeTexVoronoi *)node->storage;
    const char *name = gpu_shader_get_name(tex->feature, tex->dimensions);

    return GPU_stack_link(mat, node, name, in, out,
                         GPU_constant(&tex->distance),
                         GPU_constant(&tex->normalize));
}
```

**Shader 名称映射**:
```cpp
static const char *gpu_shader_get_name(int feature, int dimensions) {
    switch (feature) {
        case SHD_VORONOI_F1:
            return {"node_tex_voronoi_f1_1d", "node_tex_voronoi_f1_2d", ...}[dimensions-1];
        case SHD_VORONOI_F2:
            return {"node_tex_voronoi_f2_1d", ...}[dimensions-1];
        // ...
    }
}
```

### GPU GLSL 实现

**文件**: `gpu_shader_material_voronoi.glsl`

**结构**:
```glsl
struct VoronoiParams {
    float scale;
    float detail;
    float roughness;
    float lacunarity;
    float smoothness;
    float exponent;
    float randomness;
    float max_distance;
    bool normalize;
    int feature;
    int metric;
};

struct VoronoiOutput {
    float Distance;
    float3 Color;
    float4 Position;
};
```

**1D F1 完整示例**:
```glsl
VoronoiOutput voronoi_f1(VoronoiParams params, float coord) {
    float cellPosition = floor(coord);
    float localPosition = coord - cellPosition;

    float minDistance = 1e38;  // FLT_MAX
    float targetOffset = 0.0;
    float targetPosition = 0.0;

    for (int i = -1; i <= 1; i++) {
        float cellOffset = float(i);
        float pointPosition = cellOffset +
                              hash_float_to_float(cellPosition + cellOffset) *
                              params.randomness;
        float distanceToPoint = voronoi_distance(pointPosition, localPosition);

        if (distanceToPoint < minDistance) {
            targetOffset = cellOffset;
            minDistance = distanceToPoint;
            targetPosition = pointPosition;
        }
    }

    VoronoiOutput octave;
    octave.Distance = minDistance;
    octave.Color = hash_float_to_vec3(cellPosition + targetOffset);
    octave.Position = voronoi_position(targetPosition + cellPosition);

    return octave;
}
```

### SVM (Cycles) 实现

**文件**: `intern/cycles/kernel/svm/voronoi.h`

**入口函数**:
```cpp
template<uint node_feature_mask>
ccl_device_noinline int svm_node_tex_voronoi(
    KernelGlobals kg,
    ccl_private float *stack,
    const uint dimensions,
    const uint feature,
    const uint metric,
    int offset
) {
    // 读取栈数据
    const uint4 stack_offsets = read_node(kg, &offset);
    const uint4 defaults1 = read_node(kg, &offset);
    const uint4 defaults2 = read_node(kg, &offset);

    // 解压参数
    uint coord_stack_offset, w_stack_offset, scale_stack_offset, ...;
    svm_unpack_node_uchar4(stack_offsets.x, &coord_stack_offset, ...);

    // 从栈读取
    float3 coord = stack_load_float3(stack, coord_stack_offset);
    float w = stack_load_float_default(stack, w_stack_offset, defaults1.x);

    // 构建参数
    VoronoiParams params;
    params.feature = (NodeVoronoiFeature)feature;
    params.metric = (NodeVoronoiDistanceMetric)metric;
    params.scale = stack_load_float_default(stack, scale_stack_offset, defaults1.y);
    // ... 其他参数

    // 根据特征分支
    switch (params.feature) {
        case NODE_VORONOI_DISTANCE_TO_EDGE:
            distance = fractal_voronoi_distance_to_edge(params, ...);
            break;
        case NODE_VORONOI_N_SPHERE_RADIUS:
            radius = voronoi_n_sphere_radius(params, ...);
            break;
        default:
            output = fractal_voronoi_x_fx(params, ...);
            break;
    }

    // 输出到栈
    svm_voronoi_output(stack_offsets, stack, ...);

    return offset;
}
```

**分形迭代**:
```cpp
template<typename T>
ccl_device VoronoiOutput fractal_voronoi_x_fx(
    const ccl_private VoronoiParams ¶ms,
    const T coord
) {
    float amplitude = 1.0f;
    float max_amplitude = 0.0f;
    float scale = 1.0f;

    VoronoiOutput output;
    bool zero_input = params.detail == 0.0f || params.roughness == 0.0f;

    for (int i = 0; i <= ceilf(params.detail); ++i) {
        T scaled_coord = coord * scale;

        // 根据 feature 选择 F1, F2, Smooth
        VoronoiOutput octave;
        if (params.feature == NODE_VORONOI_F2) {
            octave = voronoi_f2(params, scaled_coord);
        }
        else if (params.feature == NODE_VORONOI_SMOOTH_F1 &&
                 params.smoothness != 0.0f) {
            octave = voronoi_smooth_f1(params, scaled_coord);
        }
        else {
            octave = voronoi_f1(params, scaled_coord);
        }

        if (zero_input) {
            output = octave;
            max_amplitude = 1.0f;
            break;
        }

        if (i <= params.detail) {
            max_amplitude += amplitude;
            output.distance += octave.distance * amplitude;
            output.color += octave.color * amplitude;
            output.position += octave.position * amplitude / scale;
            scale *= params.lacunarity;
            amplitude *= params.roughness;
        }
    }

    if (params.normalize) {
        output.distance /= max_amplitude * params.max_distance;
        output.color /= max_amplitude;
    }

    output.position = safe_divide(output.position, params.scale);

    return output;
}
```

### OSL 实现 (Cycles)

**文件**: `intern/cycles/kernel/osl/shaders/node_voronoi_texture.osl`

**调用外部库**:
```cpp
#include "node_fractal_voronoi.h"

shader node_voronoi_texture(
    int use_mapping = 0,
    matrix mapping = matrix(0),
    string dimensions = "3D",
    string feature = "f1",
    string metric = "euclidean",
    int use_normalize = 0,
    vector3 Vector = P,
    float WIn = 0.0,
    float Scale = 5.0,
    float Detail = 0.0,
    float Roughness = 0.5,
    float Lacunarity = 2.0,
    float Smoothness = 5.0,
    float Exponent = 1.0,
    float Randomness = 1.0,
    output float Distance = 0.0,
    output color Color = 0.0,
    output vector3 Position = P,
    output float WOut = 0.0,
    output float Radius = 0.0
) {
    // 参数转换和调用 C++ 函数
    VoronoiParams params;
    params.feature = feature;
    params.metric = metric;
    params.scale = Scale;
    // ...

    // 类似实现...
}
```

### 多函数优化 (Geometry Nodes)

在 Blender 3.x+ 中，使用 `mf::MultiFunction` 进行向量化计算：

```cpp
class VoronoiMetricFunction : public mf::MultiFunction {
    void call(const IndexMask &mask, mf::Params mf_params, mf::Context) const override {
        mask.foreach_index([&](const int64_t i) {
            // 批量计算每个点
            params.scale = scale[i];
            params.detail = detail[i];
            // ...

            output = fractal_voronoi_x_fx(params, coord[i]);

            if (calc_distance) r_distance[i] = output.distance;
            if (calc_color) r_color[i] = output.color;
        });
    }
};
```

## 实际应用

### 1. 细胞纹理 (Cellular Textures)

**特征**: F1, Euclidean 距离

**参数设置**:
```
Scale: 20-50
Randomness: 0.5-1.0
Feature: F1
```

**用途**:
- 生物细胞显微图像
- 蜂窝结构
- 马赛克瓷砖

**技巧**:
- 使用 Distance 输出作为高度图
- Color 输出作为基础颜色
- 添加 bump 节点增强立体感

### 2. 龟裂地形 (Cracked Ground)

**特征**: Distance to Edge

**参数设置**:
```
Scale: 30-100
Randomness: 0.8-1.0
Feature: Distance to Edge
Metric: Euclidean
```

**节点组合**:
```
Voronoi (Dist to Edge)
    |
    v
ColorRamp (Sharp edges)
    |
    v
Normal Map 或 Bump (3D 裂纹)
```

**应用**:
- 干旱土地
- 瓷器裂纹
- 老旧墙面

### 3. 霓虹/电路板 (Circuits)

**特征**: Distance to Edge，高 Contrast

**参数设置**:
```
Scale: 50-200
Randomness: 0.3-0.6（更规则）
Feature: Distance to Edge
Metric: Chebychev 或 Minkowski
```

**技巧**:
- 使用 `ColorRamp` 的 Constant 模式提取线框
- Combine with `Noise Texture` 制造随机瑕疵
- Emission 材质用于发光效果

### 4. 生物鳞片 (Organic Scales)

**特征**: Smooth F1, F2 混合

**参数设置**:
```
Scale: 15-30
Randomness: 0.8
Feature: F2
Detail: 3-5
Lacunarity: 2.0
Roughness: 0.4-0.6
Smoothness: 0.6
Metric: Euclidean
```

**节点网络**:
```
Voronoi (F2)     Noise (扰动)
    |                 |
    v                 v
Mix (0.3-0.7) -> ColorRamp -> Diffuse/Specular
```

### 5. 岩石开口 (Cave/Openings)

**特征**: N-Sphere Radius

**参数设置**:
```
Scale: 10-20
Randomness: 0.7-1.0
Feature: N Sphere Radius
```

**用途**:
- 溶洞系统
- 岩石孔隙
- 海绵结构

### 6. 分形景观 (Fractal Landscapes)

**特征**: 添加 Detail 和 Roughness

**参数设置**:
```
Scale: 5-10
Detail: 5-8
Roughness: 0.5-0.7
Lacunarity: 2.0-2.5
Feature: F1 或 F2
```

**组合使用**:
```
Voronoi F2 (大尺度)
    +
Voronoi F1 (小尺度)
    +
Noise (极小扰动)
```

### 颜色映射技巧

**多层着色**:
```python
# 分层表示
distance = Voronoi输出

# 亮区（F2）
if distance > 0.6:
    color = 红色

# 中间区
elif distance > 0.3:
    color = 黄色

# 暗区（F1）
else:
    color = 蓝色
```

**使用 ColorRamp**:
- Constant: 硬边分色
- Linear: 平滑过渡
- B-Spline: 曲线控制

### 与纹理混合

**考虑 UV 扰动**:
```
原始坐标 -> Perturbed (Noise) -> Voronoi
```

**与 Pattern 混合**:
```
Voronoi (F1) + Voronoi (F2) -> Subtract -> Square -> 棋盘图案
```

## 性能考虑

### 计算复杂度

| 维度 | 邻居数 | 计算次数 |
|------|--------|----------|
| 1D | 3 | 3 |
| 2D | 9 | 9 |
| 3D | 27 | 27 |
| 4D | 81 | 81 |

**分形迭代**:
```
总计算 = base × detail
```

**优化策略**:
1. **Early Exit**: 如果 detail=0，直接返回
2. **Bound Check**: 使用平方距离比较
3. **Vectorization**: 使用 SIMD/GPU 并行

### 降低计算量的方法

**1. 减少 Detail**:
```
Detail 5: 81 × 5 = 405 次距离计算
Detail 0: 81 × 1 = 81 次距离计算
```

**2. 使用较低维度**:
- 如果 2D 足够，不要用 3D
- 减少邻居遍历数

**3. 缩放空间**:
```
Scale = 0.1 (10 倍放大)
→ 更少的单元格被采样
→ 性能提升
```

## 参考文献

### 核心论文

1. **Worley, Steve (1996)**. "Cellular Texturing". *SIGGRAPH 96 Course Notes*
   - 奠基性论文，提出了细胞噪声

2. **Quilez, Inigo (2013)**. "Voronoi Patterns". *www.iquilezles.org*
   - 现代实现指南，包括光滑变体
   - https://www.iquilezles.org/www/articles/voronoilines/voronoilines.htm

3. **Lagae, Ares & Dutré, Philip (2008)**. "A Comparison of Voronoi and 3D Grid based Noise". *Eurographics*

### Blender 文档

1. **Blender 向量节点文档**: https://docs.blender.org/manual/en/latest/render/shader_nodes/vector/voronoi.html

2. **GPU Shader 着色器**: `source/blender/gpu/shaders/material/gpu_shader_material_voronoi.glsl`

3. **Cycles SVM**: `intern/cycles/kernel/svm/voronoi.h`

### Shadertoy 参考

1. **Distance to Edge**: https://www.shadertoy.com/view/ldl3W8
2. **优化技巧**: https://www.shadertoy.com/view/llG3zy

---

*文档版本: 1.0*
*基于 Blender Git 提交: 当前版本（2025）*
