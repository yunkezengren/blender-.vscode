# Blender Brick Texture Node - Comprehensive Technical Analysis

## 目录
- [1. 概述](#概述)
- [2. 核心数据结构分析](#核心数据结构分析)
  - [2.1. NodeTexBrick 结构体](#1-nodebrick-结构体)
  - [2.2. NodeTexBase 基础结构](#2-nodebase-基础结构)
- [3. 节点声明与UI界面](#节点声明与ui界面)
  - [3.1. 输入输出插座](#1-输入输出插座)
  - [3.2. 界面布局display](#2-界面布局display)
- [4. 核心算法实现](#核心算法实现)
  - [4.1. 砖块生成算法](#1-砖块生成算法)
  - [4.2. 噪声函数](#2-噪声函数)
  - [4.3. 边缘平滑处理](#3-边缘平滑处理)
- [5. 多后端实现对比](#多后端实现对比)
  - [5.1. CPU实现(C++)](#1-cpu实现c)
  - [5.2. GPU实现(GLSL)](#2-gpu实现glsl)
  - [5.3. Cycles OSL实现](#3-cycles-osl实现)
- [6. 关键函数深度解析](#关键函数深度解析)
  - [6.1. brick() 核心计算](#1-brick-核心计算)
  - [6.2. 顶点着色器集成](#2-顶点着色器集成)
- [7. 源代码位置汇总](#源代码位置汇总)

---

## <a id="概述"></a>1. 概述

<font color="#FFA500">**Brick Texture**</font> 是 Blender 中用于生成程序化砖墙纹理的着色器节点。它<font color="#7CFC00">**无需外部贴图**</font>，纯数学算法即可创建逼真的砖墙图案，支持多种参数控制砖块布局、颜色、灰缝等特征。

### 核心特性
- **程序化生成**: 基于数学公式实时计算
- **多平台支持**: CPU (C++), GPU (GLSL), Cycles (OSL)
- **高度可定制**: 支持偏移、挤压、灰缝、噪声等高级参数
- **实时预览**: 在视口中快速更新

---

## <a id="核心数据结构分析"></a>2. 核心数据结构分析

### <a id="1-nodebrick-结构体"></a>2.1. NodeTexBrick 结构体

**定义位置**: `E:\blender-git\blender\source\blender\makesdna\DNA_node_types.h:1497-1501`

```cpp
typedef struct NodeTexBrick {
  NodeTexBase base;           // 继承自基础纹理结构
  int offset_freq;            // 偏移频率 (每N行偏移一次)
  int squash_freq;            // 压缩频率 (每N行压缩一次)
  float offset;               // 偏移量 (0.0 - 1.0)
  float squash;               // 压缩量 (0.0 - 1.0)
} NodeTexBrick;
```

**字段说明**:
- **`base`**: 包含纹理映射(`TexMapping`)和颜色映射(`ColorMapping`)，这是所有程序化纹理节点的公共基础
- **`offset_freq`**: 控制交替行偏移的频率，值为2时每隔一行偏移一次，形成传统砖墙交错效果
- **`squash_freq`**: 控制压缩的频率，通常与偏移同步使用
- **`offset`**: 单行内砖块的水平偏移比例，0.5表示半块宽度的偏移
- **`squash`**: 砖块宽度的缩放系数，1.0为原始宽度，<1.0使砖变窄

---

### <a id="2-nodebase-基础结构"></a>2.2. NodeTexBase 基础结构

**定义位置**: `E:\blender-git\blender\source\blender\makesdna\DNA_node_types.h:1459-1462`

```cpp
typedef struct NodeTexBase {
  TexMapping tex_mapping;    // 纹理坐标变换（位置、旋转、缩放）
  ColorMapping color_mapping; // 颜色变换（饱和度、对比度等）
} NodeTexBase;
```

**作用**:
- **纹理映射**: 自动处理矢量输入的变换（<span style="background-color:#2E7D32;color:white">位置、旋转、缩放</span>）
- **颜色映射**: 支持后期颜色调整（<span style="background-color:#1565C0;color:white">饱和度、亮度、对比度</span>）

---

## <a id="节点声明与UI界面"></a>3. 节点声明与UI界面

### <a id="1-输入输出插座"></a>3.1. 输入输出插座

**定义位置**: `E:\blender-git\blender\source\blender\nodes\shader\nodes\node_shader_tex_brick.cc:22-77`

```cpp
static void sh_node_tex_brick_declare(NodeDeclarationBuilder &b)
{
  b.is_function_node();  // 声明为函数式节点

  // 输入插座
  b.add_input<decl::Vector>("Vector").min(-10000.0f).max(10000.0f)
    .implicit_field(NODE_DEFAULT_INPUT_POSITION_FIELD);  // 默认使用物体坐标
  b.add_input<decl::Color>("Color1").default_value({0.8f, 0.8f, 0.8f, 1.0f})
    .description("Color of the first reference brick");  // 主砖颜色
  b.add_input<decl::Color>("Color2").default_value({0.2f, 0.2f, 0.2f, 1.0f})
    .description("Color of the second reference brick"); // 次砖颜色
  b.add_input<decl::Color>("Mortar").default_value({0.0f, 0.0f, 0.0f, 1.0f})
    .no_muted_links().description("Color of the area between bricks"); // 灰缝颜色
  b.add_input<decl::Float>("Scale").default_value(5.0f).min(-1000.0f).max(1000.0f)
    .description("Scale of the texture"); // 整体缩放
  b.add_input<decl::Float>("Mortar Size").default_value(0.02f).min(0.0f).max(0.125f)
    .description("Size of the filling between the bricks"); // 灰缝大小
  b.add_input<decl::Float>("Mortar Smooth").default_value(0.1f).min(0.0f).max(1.0f)
    .description("Blurs/softens the edge between mortar and bricks"); // 灰缝边缘模糊
  b.add_input<decl::Float>("Bias").min(-1.0f).max(1.0f)
    .description("Color variation between Color1 and Color2"); // 颜色偏向
  b.add_input<decl::Float>("Brick Width").default_value(0.5f).min(0.01f).max(100.0f)
    .description("Ratio of brick's width relative to texture scale"); // 砖宽度比
  b.add_input<decl::Float>("Row Height").default_value(0.25f).min(0.01f).max(100.0f)
    .description("Ratio of brick's row height relative to texture scale"); // 行高度比

  // 输出插座
  b.add_output<decl::Color>("Color");  // 最终颜色
  b.add_output<decl::Float>("Factor", "Fac"); // 灰缝因子 (0=砖块, 1=灰缝)
}
```

**关键参数说明**:
| 参数 | 类型 | 默认值 | 范围 | 作用 |
|------|------|--------|------|------|
| **Scale** | Float | 5.0 | -1000~1000 | 整体纹理密度 |
| **Mortar Size** | Float | 0.02 | 0~0.125 | 灰缝宽度 |
| **Mortar Smooth** | Float | 0.1 | 0~1 | 灰缝边缘柔和度 |
| **Bias** | Float | 0.0 | -1~1 | Color1/Color2偏向 |
| **Brick Width** | Float | 0.5 | 0.01~100 | 砖块宽度比例 |
| **Row Height** | Float | 0.25 | 0.01~100 | 行高度比例 |

---

### <a id="2-界面布局display"></a>3.2. 界面布局 display

**定义位置**: `E:\blender-git\blender\source\blender\nodes\shader\nodes\node_shader_tex_brick.cc:79-95`

```cpp
static void node_shader_buts_tex_brick(ui::Layout &layout, bContext * /*C*/, PointerRNA *ptr)
{
  {
    ui::Layout &col = layout.column(true);  // 创建垂直布局
    col.prop(ptr, "offset", ui::ITEM_R_SPLIT_EMPTY_NAME | ui::ITEM_R_SLIDER,
             IFACE_("Offset"), ICON_NONE);
    col.prop(ptr, "offset_frequency", ui::ITEM_R_SPLIT_EMPTY_NAME,
             IFACE_("Frequency"), ICON_NONE);
  }
  {
    ui::Layout &col = layout.column(true);
    col.prop(ptr, "squash", ui::ITEM_R_SPLIT_EMPTY_NAME, IFACE_("Squash"), ICON_NONE);
    col.prop(ptr, "squash_frequency", ui::ITEM_R_SPLIT_EMPTY_NAME,
             IFACE_("Frequency"), ICON_NONE);
  }
}
```

**作用**: 在节点UI中显示额外的高级控制参数（<span style="background-color:#FF6B6B;color:white">offset</span> 和 <span style="background-color:#FF6B6B;color:white">squash</span>相关参数），这些不通过插座输入，而是节点内部属性。

---

## <a id="核心算法实现"></a>4. 核心算法实现

### <a id="1-砖块生成算法"></a>4.1. 砖块生成算法

<font color="#FFA500">**算法核心思路**</font>:
1. **坐标转换**: 将世界坐标映射到局部网格坐标系
2. **行计算**: 确定当前点所在的行号
3. **偏移/压缩**: 根据行号决定是否需要偏移或压缩
4. **列计算**: 确定当前点在行中的砖块编号
5. **局部坐标**: 计算在单块砖内的相对位置
6. **灰缝检测**: 计算到边缘的最小距离
7. **颜色混合**: 根据位置和噪声生成最终颜色

---

### <a id="2-噪声函数"></a>4.2. 噪声函数

**C++实现**:
```cpp
/* Fast integer noise */
static float brick_noise(uint n)
{
  n = (n + 1013) & 0x7fffffff;           // 添加常数并掩码
  n = (n >> 13) ^ n;                     // 位移和异或混合
  const uint nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff;
  return 0.5f * (float(nn) / 1073741824.0f);  // 归一化到[0, 0.5]
}
```

**GLSL实现** (`E:\blender-git\blender\source\blender\gpu\shaders\material\gpu_shader_material_tex_brick.glsl`):
```glsl
float tint = clamp((integer_noise((rownum << 16) + (bricknum & 0xFFFF)) + bias), 0.0f, 1.0f);
```

**OSL实现** (`E:\blender-git\blender\intern\cycles\kernel\osl\shaders\node_brick_texture.osl`):
```c
float brick_noise(int ns) {
  int nn;
  int n = (ns + 1013) & 2147483647;
  n = (n >> 13) ^ n;
  nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 2147483647;
  return 0.5 * ((float)nn / 1073741824.0);
}
```

**算法说明**:
- **输入**: 基于行号和砖块号组合的hash值
- **输出**: 0~0.5范围的伪随机数
- **作用**: 为每块砖生成独特的颜色偏移，增加真实感

---

### <a id="3-边缘平滑处理"></a>4.3. 边缘平滑处理

**C++实现** (`node_shader_tex_brick.cc:176-180`):
```cpp
static float smoothstepf(const float f)
{
  const float ff = f * f;
  return (3.0f * ff - 2.0f * ff * f);  // 经典smoothstep: 3t² - 2t³
}

// 灰缝计算 (line 209-221)
float min_dist = std::min({x, y, brick_width - x, row_height - y});
float mortar;
if (min_dist >= mortar_size) {
  mortar = 0.0f;                             // 不在灰缝内
}
else if (mortar_smooth == 0.0f) {
  mortar = 1.0f;                             // 锐利边缘
}
else {
  min_dist = 1.0f - min_dist / mortar_size;  // 距离映射到0-1
  mortar = (min_dist < mortar_smooth) ? smoothstepf(min_dist / mortar_smooth) : 1.0f;
}
```

**GLSL实现**:
```glsl
float min_dist = min(min(x, y), min(brick_width - x, row_height - y));
if (min_dist >= mortar_size) {
  return float2(tint, 0.0f);               // 砖块内部
}
else if (mortar_smooth == 0.0f) {
  return float2(tint, 1.0f);               // 纯灰缝
}
else {
  min_dist = 1.0f - min_dist / mortar_size;
  return float2(tint, smoothstep(0.0f, mortar_smooth, min_dist)); // 柔和过渡
}
```

**算法解释**:
1. **min_dist**: 计算当前点到最近砖块边缘的距离
2. **mortar_size**: 定义灰缝的物理宽度
3. **smoothstep**: 使用三次曲线创建平滑过渡（<span style="background-color:#8E24AA;color:white">避免线性过渡的生硬感</span>）
4. **结果**: 返回0~1范围的混合因子，用于颜色混合

---

## <a id="多后端实现对比"></a>5. 多后端实现对比

### <a id="1-cpu实现c"></a>5.1. CPU实现 (C++)

**完整流程**：
```cpp
// 定义位置: E:\blender-git\blender\source\blender\nodes\shader\nodes\node_shader_tex_brick.cc:226-282

void call(const IndexMask &mask, mf::Params params, mf::Context /*context*/) const override
{
  // 1. 读取输入参数
  const VArray<float3> &vector = params.readonly_single_input<float3>(0, "Vector");
  // ... 其他参数读取

  // 2. 批量处理（支持SIMD优化）
  mask.foreach_index([&](const int64_t i) {
    // 3. 核心计算
    const float2 f2 = brick(vector[i] * scale[i], ...);

    // 4. 颜色混合
    float4 color_data;
    if (f != 1.0f) {
      const float facm = 1.0f - tint;
      color_data = color1 * facm + color2 * tint;  // Color1/Color2混合
    }

    // 5. 灰缝混合
    if (store_color) {
      color_data = color_data * (1.0f - f) + mortar * f;  // 灰缝因子
      copy_v4_v4(r_color[i], color_data);
    }
  });
}
```

**特点**:
- **面向对象**: 使用`BrickFunction`类继承`mf::MultiFunction`
- **批量处理**: 支持多线程和SIMD优化
- **惰性计算**: 仅计算需要的输出（`store_fac`, `store_color`）

---

### <a id="2-gpu实现glsl"></a>5.2. GPU实现 (GLSL)

**着色器结构**:
```glsl
// 定义位置: E:\blender-git\blender\source\blender\gpu\shaders\material\gpu_shader_material_tex_brick.glsl

float2 calc_brick_texture(float3 p, ...) {
  // 1. 行号计算
  rownum = int(floor(p.y / row_height));

  // 2. 压缩处理
  if (offset_frequency != 0 && squash_frequency != 0) {
    brick_width *= (rownum % squash_frequency != 0) ? 1.0f : squash_amount;
    offset = (rownum % offset_frequency != 0) ? 0.0f : (brick_width * offset_amount);
  }

  // 3. 列号计算
  bricknum = int(floor((p.x + offset) / brick_width));

  // 4. 局部坐标
  x = (p.x + offset) - brick_width * bricknum;
  y = p.y - row_height * rownum;

  // 5. 噪声计算（使用GLSL内置hash）
  float tint = clamp((integer_noise((rownum << 16) + (bricknum & 0xFFFF)) + bias), 0.0f, 1.0f);

  // 6. 灰缝距离计算
  float min_dist = min(min(x, y), min(brick_width - x, row_height - y));
  if (min_dist >= mortar_size) {
    return float2(tint, 0.0f);
  }
  else if (mortar_smooth == 0.0f) {
    return float2(tint, 1.0f);
  }
  else {
    min_dist = 1.0f - min_dist / mortar_size;
    return float2(tint, smoothstep(0.0f, mortar_smooth, min_dist));
  }
}

void node_tex_brick(...) {
  float2 f2 = calc_brick_texture(co * scale, ...);
  float tint = f2.x;
  float f = f2.y;
  if (f != 1.0f) {
    float facm = 1.0f - tint;
    color1 = facm * color1 + tint * color2;
  }
  color = mix(color1, mortar, f);
  fac = f;
}
```

**GPU链接函数** (`node_shader_gpu_tex_brick`):
```cpp
// 定义位置: E:\blender-git\blender\source\blender\nodes\shader\nodes\node_shader_tex_brick.cc:111-131

static int node_shader_gpu_tex_brick(GPUMaterial *mat, bNode *node, ...) {
  node_shader_gpu_default_tex_coord(mat, node, &in[0].link);  // 纹理坐标处理
  node_shader_gpu_tex_mapping(mat, node, in, out);             // 坐标变换
  NodeTexBrick *tex = (NodeTexBrick *)node->storage;

  // 传递节点参数到GPU
  return GPU_stack_link(mat, node, "node_tex_brick", in, out,
                        GPU_uniform(&tex->offset),           // float
                        GPU_constant(&offset_freq),          // int
                        GPU_uniform(&tex->squash),           // float
                        GPU_constant(&squash_freq));         // int
}
```

**特点**:
- **函数式**: 完全使用GLSL函数，无状态
- **内置优化**: 使用`smoothstep`, `floor`等GPU优化函数
- **实时渲染**: 逐像素计算，支持动态光影

---

### <a id="3-cycles-osl实现"></a>5.3. Cycles OSL实现

**OSL着色器**:
```c
// 定义位置: E:\blender-git\blender\intern\cycles\kernel\osl\shaders\node_brick_texture.osl

shader node_brick_texture(
    int use_mapping = 0,
    matrix mapping = matrix(0),
    float offset = 0.5,
    int offset_frequency = 2,
    float squash = 1.0,
    int squash_frequency = 1,
    point Vector = P,           // OSL内置位置
    color Color1 = 0.2,
    color Color2 = 0.8,
    color Mortar = 0.0,
    float Scale = 5.0,
    float MortarSize = 0.02,
    float MortarSmooth = 0.0,
    float Bias = 0.0,
    float BrickWidth = 0.5,
    float RowHeight = 0.25,
    output float Fac = 0.0,
    output color Color = 0.2)
{
  point p = Vector;

  // 可选的变换矩阵应用
  if (use_mapping)
    p = transform(mapping, p);

  float tint = 0.0;
  color Col = Color1;

  // 调用核心计算函数
  Fac = brick(p * Scale, MortarSize, MortarSmooth, Bias,
              BrickWidth, RowHeight, offset, offset_frequency,
              squash, squash_frequency, tint);

  // 颜色混合
  if (Fac != 1.0) {
    float facm = 1.0 - tint;
    Col = facm * Color1 + tint * Color2;
  }

  Color = mix(Col, Mortar, Fac);
}
```

**特点**:
- **光线追踪兼容**: 使用OSL的光线空间坐标
- **矩阵变换**: 支持复杂的纹理坐标变换
- **高精度**: 浮点运算精度更高，适合离线渲染

---

## <a id="关键函数深度解析"></a>6. 关键函数深度解析

### <a id="1-brick-核心计算"></a>6.1. `brick()` - 核心计算函数

**C++版本** `static float2 brick(...)`：
```cpp
// 定义位置: E:\blender-git\blender\source\blender\nodes\shader\nodes\node_shader_tex_brick.cc:182-224

static float2 brick(float3 p,
                    float mortar_size,
                    float mortar_smooth,
                    float bias,
                    float brick_width,
                    float row_height,
                    float offset_amount,
                    int offset_frequency,
                    float squash_amount,
                    int squash_frequency)
{
  float offset = 0.0f;

  // ==================== 行号计算 ====================
  const int rownum = int(floorf(p.y / row_height));

  // ==================== 压缩与偏移 ====================
  if (offset_frequency && squash_frequency) {
    // 压缩: 按squash_frequency决定是否压缩砖块宽度
    brick_width *= (rownum % squash_frequency) ? 1.0f : squash_amount;

    // 偏移: 按offset_frequency决定是否水平偏移
    offset = (rownum % offset_frequency) ? 0.0f : (brick_width * offset_amount);
  }

  // ==================== 列号计算 ====================
  const int bricknum = int(floorf((p.x + offset) / brick_width));

  // ==================== 局部相对坐标 ====================
  const float x = (p.x + offset) - brick_width * bricknum;
  const float y = p.y - row_height * rownum;

  // ==================== 随机颜色偏移 ====================
  const float tint = clamp_f(
      brick_noise((rownum << 16) + (bricknum & 0xFFFF)) + bias, 0.0f, 1.0f);

  // ==================== 灰缝距离计算 ====================
  // x, y: 到左上边界的距离
  // brick_width - x, row_height - y: 到右下边界的距离
  float min_dist = std::min({x, y, brick_width - x, row_height - y});

  // ==================== 灰缝值计算 ====================
  float mortar;
  if (min_dist >= mortar_size) {
    mortar = 0.0f;                           // 在砖块内部
  }
  else if (mortar_smooth == 0.0f) {
    mortar = 1.0f;                           // 完全灰缝
  }
  else {
    // 归一化距离到[0, min_dist/max_dist]
    min_dist = 1.0f - min_dist / mortar_size;
    // 灰缝值: 0(砖块边缘) → 1(灰缝中心)
    mortar = (min_dist < mortar_smooth) ? smoothstepf(min_dist / mortar_smooth) : 1.0f;
  }

  return float2(tint, mortar);  // 返回: x=颜色偏移, y=灰缝因子
}
```

**算法分步图解**:
```
假设: brick_width = 0.5, row_height = 0.25, offset = 0.5

输入点 p = (0.7, 0.3)

1. 行号 = floor(0.3 / 0.25) = 1 (第2行)

2. 检查偏移: rownum % offset_frequency (1 % 2) = 1 ≠ 0
   → 不偏移，offset = 0

3. 列号 = floor((0.7 + 0) / 0.5) = 1 (第2块砖)

4. 局部坐标:
   x = (0.7 + 0) - 0.5 * 1 = 0.2  (砖内x=0.2)
   y = 0.3 - 0.25 * 1 = 0.05       (砖内y=0.05)

5. 到四边距离:
   left: x = 0.2
   top: y = 0.05
   right: 0.5 - 0.2 = 0.3
   bottom: 0.25 - 0.05 = 0.2
   min_dist = 0.05 (到顶部最近)

6. 若 mortar_size=0.02, 0.05 > 0.02 → mortar = 0 (砖块内部)
```

---

### <a id="2-顶点着色器集成"></a>6.2. 顶点着色器集成流程

**执行顺序**:
```
1. 用户创建节点 → 调用 register_node_type_sh_tex_brick()
   ↓
2. 节点初始化 → node_shader_init_tex_brick()
   - 分配 NodeTexBrick 内存
   - 设置默认值: offset=0.5, squash=1.0, freq=2

3. UI显示 → node_shader_buts_tex_brick()
   - 显示 offset/squash 参数控制面板

4. GPU材质编译 → node_shader_gpu_tex_brick()
   - 绑定GLSL函数 node_tex_brick
   - 传递参数 uniform/constant

5. 渲染时执行 (每像素):
   GLSL node_tex_brick → calc_brick_texture → 输出颜色
```

**数据流**:
```
节点输入
  ├─ Vector → [纹理坐标] ──┐
  ├─ Color1 ───────────────┤
  ├─ Color2 ───────────────┤
  ├─ Mortar ───────────────┤
  ├─ Scale ────────────────┤
  ├─ 以及其他参数 ────────────┤
  ↓                          ↓
[BrickFunction::call] 或 [node_tex_brick]
  ↓                          ↓
计算 tint 和 mortar
  ↓                          ↓
混合颜色 → 输出 Color/Factor
```

---

## <a id="源代码位置汇总"></a>7. 源代码位置汇总

### 核心数据结构
| 文件 | 行号 | 内容 |
|------|------|------|
| `DNA_node_types.h` | 1497-1501 | `NodeTexBrick` 结构体 |
| `DNA_node_types.h` | 1459-1462 | `NodeTexBase` 基础结构 |

### 声明与初始化
| 文件 | 行号 | 函数 | 说明 |
|------|------|------|------|
| `node_shader_tex_brick.cc` | 22-77 | `sh_node_tex_brick_declare` | 插座定义 |
| `node_shader_tex_brick.cc` | 79-95 | `node_shader_buts_tex_brick` | UI布局 |
| `node_shader_tex_brick.cc` | 97-109 | `node_shader_init_tex_brick` | 节点初始化 |
| `node_shader_tex_brick.cc` | 296-318 | `register_node_type_sh_tex_brick` | 节点注册 |

### CPU计算实现
| 文件 | 行号 | 函数 | 说明 |
|------|------|------|------|
| `node_shader_tex_brick.cc` | 133-283 | `class BrickFunction` | 多函数实现 |
| `node_shader_tex_brick.cc` | 168-174 | `brick_noise` | 噪声函数 |
| `node_shader_tex_brick.cc` | 176-180 | `smoothstepf` | 平滑函数 |
| `node_shader_tex_brick.cc` | 182-224 | `brick` | 核心计算 |
| `node_shader_tex_brick.cc` | 226-282 | `call` | 批量处理接口 |
| `node_shader_tex_brick.cc` | 285-292 | `sh_node_brick_build_multi_function` | 多函数构造 |

### GPU实现
| 文件 | 行号 | 函数 | 说明 |
|------|------|------|------|
| `gpu_shader_material_tex_brick.glsl` | 7-47 | `calc_brick_texture` | GLSL核心函数 |
| `gpu_shader_material_tex_brick.glsl` | 49-84 | `node_tex_brick` | GLSL入口函数 |
| `node_shader_tex_brick.cc` | 111-131 | `node_shader_gpu_tex_brick` | GPU绑定函数 |

### Cycles OSL实现
| 文件 | 行号 | 函数 | 说明 |
|------|------|------|------|
| `node_brick_texture.osl` | 9-16 | `brick_noise` | OSL噪声 |
| `node_brick_texture.osl` | 18-60 | `brick` | OSL核心 |
| `node_brick_texture.osl` | 62-107 | `shader node_brick_texture` | OSL着色器入口 |

---

## 附录

### 参数对照表

| UI名称 | 结构体字段 | GPU参数 | OSL参数 | 默认值 | 单位/范围 |
|--------|------------|---------|---------|--------|-----------|
| 偏移量 | `offset` | `offset_amount` | `offset` | 0.5 | 相对砖宽度比例 (0-1) |
| 偏移频率 | `offset_freq` | `offset_frequency` | `offset_frequency` | 2 | 每N行偏移一次 |
| 压缩量 | `squash` | `squash_amount` | `squash` | 1.0 | 砖宽度缩放系数 |
| 压缩频率 | `squash_freq` | `squash_frequency` | `squash_frequency` | 2 | 每N行压缩一次 |

### 常见问题

**Q: 为什么我的砖块是斜的？**
A: 检查纹理坐标连接，确保使用物体坐标或UV坐标而非窗口坐标。

**Q: 如何创建完全不规则的砖墙？**
A: 增加`Mortar Smooth`到0.5以上，设置`Bias`为随机值，调整`Brick Width`和`Row Height`的比值。

**Q: 为什么GPU渲染和CPU渲染有差异？**
A: 主要原因是`smoothstep`实现细节和浮点精度差异，但在视觉上应该非常接近。

---

**文档版本**: 1.0
**基于**: Blender 4.3+ (main分支 ee36a031fb8)
**最后更新**: 2025-12-18
