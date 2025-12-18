# 典型 Shader 深度剖析

## 目录
- [1. 引言：为什么分析典型 Shader？](#1-引言为什么分析典型-shader)
- [2. 案例 1：网格编辑顶点着色器](#2-案例-1网格编辑顶点着色器)
  - [2.1. 完整代码](#21-完整代码)
  - [2.2. 处理流程解析](#23-处理流程解析)
  - [2.3. 关键技术点](#24-关键技术点)
- [3. 案例 2：边缘几何着色器](#3-案例-2边缘几何着色器)
  - [3.1. 顶点拉取模式](#31-顶点拉取模式)
  - [3.2. 几何扩展算法](#32-几何扩展算法)
  - [3.3. 抗锯齿原理](#33-抗锯齿原理)
- [4. 案例 3：骨骼球体渲染](#4-案例-3骨骼球体渲染)
  - [4.1. 实例渲染](#41-实例渲染)
  - [4.2. 视图对齐球体](#42-视图对齐球体)
  - [4.3. 深度计算](#43-深度计算)
- [5. 案例 4：权重分析着色器](#5-案例-4权重分析着色器)
  - [5.1. 颜色映射](#51-颜色映射)
- [6. 案例 5：UV 编辑边缘](#6-案例-5uv-编辑边缘)
- [7. Shader 变体对比表](#7-shader-变体对比表)

---

## 1. 引言：为什么分析典型 Shader？

通过分析真实代码，你可以学习：
1. **最佳实践**：Blender 团队的编码规范
2. **性能技巧**：在复杂场景下保持流畅
3. **设计模式**：如何构建可复用的系统
4. **调试技术**：浏览器工作原理

---

## 2. 案例 1：网格编辑顶点着色器

**文件**: `overlay_edit_mesh_vert.glsl`

### 2.1. 完整代码解析

```glsl
/* SPDX-FileCopyrightText: 2017-2023 Blender Authors
 * SPDX-License-Identifier: GPL-2.0-or-later */

// ===== 1. 头部与包含系统 =====
#include "infos/overlay_edit_mode_infos.hh"
VERTEX_SHADER_CREATE_INFO(overlay_edit_mesh_vert)

#ifdef GLSL_CPP_STUBS
#  define VERT
#endif

#include "draw_model_lib.glsl"
#include "draw_view_clipping_lib.glsl"
#include "draw_view_lib.glsl"
#include "overlay_common_lib.glsl"
#include "overlay_edit_mesh_common_lib.glsl"

// ===== 2. 定义与宏 =====
#ifdef EDGE
/* 将最终颜色从几何着色器输入传递 */
#  define final_color geometry_in.final_color_
#  define final_color_outer geometry_in.final_color_outer_
#  define selectOverride geometry_in.selectOverride_
#endif

// ===== 3. 辅助函数 =====
bool test_occlusion()
{
    // 屏幕空间坐标转换
    float3 ndc = (gl_Position.xyz / gl_Position.w) * 0.5f + 0.5f;

    // 纹理收集：一次读取 2x2 邻域的 4 个深度值
    float4 depths = textureGather(depth_tx, ndc.xy);

    // 如果当前片段深度比所有收集到的深度都大，说明被遮挡
    return all(greaterThan(float4(ndc.z), depths));
}

float3 non_linear_blend_color(float3 col1, float3 col2, float fac)
{
    // 伽马空间混合：在 2.2 伽马空间中混合
    col1 = pow(col1, float3(1.0f / 2.2f));
    col2 = pow(col2, float3(1.0f / 2.2f));
    float3 col = mix(col1, col2, fac);
    return pow(col, float3(2.2f));
}

// ===== 4. 主函数 =====
void main()
{
    // ---- Step 1: 坐标变换链 ----
    // 对象空间 → 世界空间 → 视图空间 → 齐次裁剪空间
    float3 world_pos = drw_point_object_to_world(pos);        // 库函数
    float3 view_pos = drw_point_world_to_view(world_pos);     // 库函数
    gl_Position = drw_point_view_to_homogenous(view_pos);     // 库函数

    // ---- Step 2: Retopology 深度偏移 ----
    gl_Position.z += get_homogenous_z_offset(
        drw_view().winmat,    // 当前投影矩阵
        view_pos.z,           // 视图空间深度
        gl_Position.w,        // 齐次 W 分量
        retopology_offset     // Push Constant：偏移量
    );

    // ---- Step 3: 数据解包 ----
    // data 是 uint4，data_mask 用于提取需要的位
    uint4 m_data = data & uint4(data_mask);

    // ---- Step 4: 条件编译分支 ----
    // 多个着色器共享同一文件，通过宏决定执行路径

    #if defined(VERT)  // =================== 顶点模式
        // 计算折痕值（从高4位）
        vertex_crease = float(m_data.z >> 4) / 15.0f;

        // 计算顶点颜色
        final_color = EDIT_MESH_vertex_color(m_data.y, vertex_crease);

        // 根据折痕大小调整点大小
        gl_PointSize = theme.sizes.vert *
                      ((vertex_crease > 0.0f) ? 3.0f : 2.0f);

        // 特殊处理：选中和活动顶点置顶
        if ((data.x & VERT_SELECTED) != 0u) {
            gl_Position.z -= 5e-7f * abs(gl_Position.w);
        }
        if ((data.x & VERT_ACTIVE) != 0u) {
            gl_Position.z -= 5e-7f * abs(gl_Position.w);
        }

        // 遮挡测试
        bool occluded = test_occlusion();

    #elif defined(EDGE)  // ================= 边缘模式（几何着色器）
        // 在顶点着色器中只处理颜色
        #  ifdef FLAT
            final_color = EDIT_MESH_edge_color_inner(m_data.y);
            selectOverride = 1u;
        #  else
            final_color = EDIT_MESH_edge_vertex_color(m_data.y);
            selectOverride = (m_data.y & EDGE_SELECTED);
        #  endif

        // 边缘外层颜色（标记如折痕、权重等）
        float edge_crease = float(m_data.z & 0xFu) / 15.0f;
        float bweight = float(m_data.w) / 255.0f;
        final_color_outer = EDIT_MESH_edge_color_outer(
            m_data.y, m_data.x, edge_crease, bweight
        );

        // 高亮边缘置顶
        if (final_color_outer.a > 0.0f) {
            gl_Position.z -= 5e-7f * abs(gl_Position.w);
        }

        // 边缘不使用顶点遮挡测试（在片段着色器中完成）
        bool occluded = false;

    #elif defined(FACE)  // ================= 面模式
        final_color = EDIT_MESH_face_color(m_data.x);
        bool occluded = true;  // 默认遮挡

        // Metal 平台的特殊处理
        #  ifdef GPU_METAL
        gl_Position.z -= 5e-5f;  // 防止 Z-fighting
        #  endif

    #elif defined(FACEDOT)  // ============== 面点模式
        final_color = EDIT_MESH_facedot_color(norAndFlag.w);

        // 面点 Z 偏移（不同投影类型不同）
        gl_Position.z -= (drw_view().winmat[3][3] == 0.0f) ?
                         0.00035f : 1e-6f;

        gl_PointSize = theme.sizes.face_dot;
        bool occluded = test_occlusion();

    #endif

    // ---- Step 5: Alpha 处理 ----
    final_color.a *= (occluded) ? alpha : 1.0f;

    // ---- Step 6: 面向混合（Fresnel 效果） ----
    #if !defined(FACE)  // 面不使用面向混合
        // 将法线转到视图空间
        float3 view_normal = normalize(
            drw_normal_object_to_view(vnor) + 1e-4f
        );

        // 选择视图向量（透视/正交）
        float3 view_vec = (drw_view().winmat[3][3] == 0.0f) ?
                          normalize(view_pos) :
                          vec3(0.0f, 0.0f, 1.0f);

        // 计算面向因子（1 - |cosθ| × 0.2）
        float facing = dot(view_vec, view_normal);
        facing = 1.0f - abs(facing) * 0.2f;

        // 非线性混合（伽马空间）
        final_color.rgb = mix(
            final_color.rgb,
            non_linear_blend_color(
                theme.colors.edit_mesh_middle.rgb,
                final_color.rgb,
                facing
            ),
            theme.fresnel_mix_edit  // 混合系数（来自 UBO）
        );
    #endif

    // ---- Step 7: 视图裁剪 ----
    gl_Position.z -= ndc_offset_factor * ndc_offset;
    view_clipping_distances(world_pos);
}
```

### 2.2. 关键技术点

#### **1. 单文件多模式设计**

```glsl
// 设计意图：避免代码重复
overlay_edit_mesh_vert.glsl
├── #if defined(VERT)   → 顶点显示（gl_PointSize）
├── #if defined(EDGE)   → 边缘（结合几何着色器）
├── #if defined(FACE)   → 面填充
└── #if defined(FACEDOT) → 面点

// C++ 通过 .define("VERT") 控制编译哪个分支
```

**好处**：
- 代码复用：核心的坐标变换、遮挡测试、面向混合只写一次
- 维护简单：修改算法只需改一个文件

#### **2. TextureGather 深度测试**

```glsl
// 传统方式：4 次纹理采样
float d00 = texture(depth_tx, uv + vec2(-1,-1)/size).r;
float d01 = texture(depth_tx, uv + vec2(-1, 1)/size).r;
float d10 = texture(depth_tx, uv + vec2( 1,-1)/size).r;
float d11 = texture(depth_tx, uv + vec2( 1, 1)/size).r;

// 优化方式：一次指令采集 4 个值
float4 depths = textureGather(depth_tx, uv);

// 性能提升：减少 75% 的纹理访问
```

**原理**：GPU 硬件支持一次读取 2x2 邻域，用于高效实现 MSAA 和深度测试。

#### **3. 非线性颜色混合**

```glsl
// 为什么要在伽马空间混合？
// 线性空间：mix(a, b, 0.5) = (a+b)/2
// 伽马空间：mix(a, b, 0.5) = (a^γ + b^γ)/2 ^ (1/γ)

// 视觉结果：线性混合变暗，伽马混合保持视觉亮度一致
```

#### **4. 精确深度偏移**

```glsl
// 常数偏移（错误）
gl_Position.z -= 0.001;  // 透视下深度非线性，效果不一致

// 函数偏移（正确）
gl_Position.z += get_homogenous_z_offset(...);  // 自动处理投影
```

---

## 3. 案例 2：边缘几何着色器

**文件**: `overlay_edit_mesh_edge_vert.glsl`

### 3.1. 顶点拉取模式 (Vertex Pulling)

```glsl
// 传统顶点属性
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

// ➔ 顶点拉取：从缓冲区读取，不使用顶点属性
layout(std430, binding = 0) buffer PosBuf {
    float pos[];
} pos_buf;

layout(std430, binding = 1) buffer DataBuf {
    uint data[];
} data_buf;

// 优势：
// 1. 更大的数据量（无 16 顶点属性限制）
// 2. 更灵活的数据布局
// 3. 可以直接读取压缩数据

VertIn input_assembly(uint in_vertex_id) {
    uint v_i = gpu_index_load(in_vertex_id);  // 加载索引
    VertIn vert_in;
    vert_in.lP = gpu_attr_load_float3(pos, gpu_attr_0, v_i);
    vert_in.e_data = gpu_attr_load_uchar4(data, gpu_attr_2, v_i);
    return vert_in;
}
```

### 3.2. 几何着色器扩展算法

完整的几何着色器工作流程：

```glsl
// ===== 顶点着色器（输入阶段）=====
void main() {
    // 处理线段的两个端点
    // 输出到几何着色器：VertOut[2]
}

// ===== 几何着色器（扩展阶段）=====
void geometry_main(VertOut geom_in[2],
                   uint out_vert_id,
                   uint out_prim_id,
                   uint out_invocation_id) {

    // 1. 获取原始线段
    vec4 pos0 = geom_in[0].gpu_position;
    vec4 pos1 = geom_in[1].gpu_position;

    // 2. 裁剪近平面（避免变形）
    float2 pz_ndc = float2(pos0.z / pos0.w, pos1.z / pos0.w);

    // 如果两个端点都在裁剪面后面，完全剔除
    bool2 clipped = lessThan(pz_ndc, float2(-1.0f));
    if (all(clipped)) return;

    // 3. 裁剪计算（防止近平面处的变形）
    float4 pos01 = pos0 - pos1;
    float ofs = abs((pz_ndc.y + 1.0f) / (pz_ndc.x - pz_ndc.y));

    if (clipped.y) {
        pos1 += pos01 * ofs;  // 推移端点 1
    }
    else if (clipped.x) {
        pos0 -= pos01 * (1.0f - ofs);  // 推移端点 0
    }

    // 4. 屏幕空间计算
    vec2 ss_pos0 = pos0.xy / pos0.w;
    vec2 ss_pos1 = pos1.xy / pos1.w;
    vec2 line_dir = ss_pos0 - ss_pos1;  // 屏幕空间线段

    // 5. 计算线宽（像素）
    float half_size = theme.sizes.edge;
    if (do_smooth_wire) half_size += 0.5f;  // AA 额外像素

    // 6. 计算偏移方向（垂直线段）
    vec2 perp = normalize(vec2(-line_dir.y, line_dir.x));
    vec2 offset = perp * half_size / uniform_buf.size_viewport;

    // 7. 构建四边形（4 个顶点）
    // 发射顺序：0-out, 0-in, 1-out, 1-in
    // 形成两个三角形带

    // 顶点 0（外侧）
    gl_Position = pos0;
    gl_Position.xy += offset * pos0.w;
    geometry_out.final_color = geom_in[0].final_color;
    geometry_noperspective_out.edge_coord = half_size;
    EmitVertex();

    // 顶点 1（内侧）
    gl_Position = pos0;
    gl_Position.xy -= offset * pos0.w;
    geometry_noperspective_out.edge_coord = -half_size;
    EmitVertex();

    // 顶点 2（外侧）
    gl_Position = pos1;
    gl_Position.xy += offset * pos1.w;
    geometry_noperspective_out.edge_coord = half_size;
    geometry_flat_out.final_color_outer = geom_in[0].final_color_outer;
    EmitVertex();

    // 顶点 3（内侧）
    gl_Position = pos1;
    gl_Position.xy -= offset * pos1.w;
    geometry_noperspective_out.edge_coord = -half_size;
    EmitVertex();

    EndPrimitive();  // 结束四边形
}
```

### 3.3. 抗锯齿原理

```glsl
// ===== 片段着色器 =====

// 从几何着色器接收
in vec4 final_color;
in vec4 final_color_outer;
in float edge_coord;  // [-size, +size] 范围
in noperspective float edge_coord;  // 透视校正

// 边缘的 fragmented shader 需要处理两种情况：
// 1. 内层线（edge_coord 会反向）
// 2. 外层标记（折痕、权重）

void main() {
    // 获取平滑因子（边缘抗锯齿）
    // 只计算距离边缘线的距离
    float width = abs(edge_coord);

    // 检查外层颜色
    if (final_color_outer.a > 0.0f) {
        // 在边缘外围绘制外层标记
        // 处理折痕、权重标记
        frag_color = final_color_outer;

        // 边缘位置检查
        if (edge_coord < 0.0f) {
            // 内部区域使用内层颜色
            frag_color = final_color;
        }
    }
    else {
        // 普通边缘
        frag_color = final_color;
    }

    // 使用混合或丢弃来创建平滑边缘
    // ...
}
```

---

## 4. 案例 3：骨骼球体渲染

**文件**: `overlay_armature_sphere_solid_vert.glsl`

### 4.1. 实例渲染

```glsl
// ===== 顶点着色器 =====

// 实例数据
uniform samplerBuffer data_buf;  // 存储了每个实例的矩阵和颜色

// 实例选择数据
uniform samplerBuffer in_select_buf;
uniform int select_id;

void main() {
    // 步骤 1: 设置选择 ID（如果支持）
    select_id_set(in_select_buf[gl_InstanceID]);

    // 步骤 2: 获取实例数据
    float4x4 inst_obmat = data_buf[gl_InstanceID];

    // 解包：一个矩阵中存储了变换 + 状态颜色 + 骨骼颜色
    float4 bone_color, state_color;
    float4x4 model_mat = extract_matrix_packed_data(
        inst_obmat, state_color, bone_color
    );

    // 步骤 3: 计算模型视图矩阵
    float4x4 model_view_matrix = drw_view().viewmat * model_mat;

    // 步骤 4: 为球体生成计算构建逆矩阵
    // 用于在片段着色器中进行光线求交
    const float4x4 sphere_matrix = inverse(model_view_matrix);
    sphere_matrix0 = sphere_matrix[0];
    sphere_matrix1 = sphere_matrix[1];
    sphere_matrix2 = sphere_matrix[2];
    sphere_matrix3 = sphere_matrix[3];

    // 步骤 5: 判断投影类型
    bool is_persp = (drw_view().winmat[3][3] == 0.0f);

    // 步骤 6: 计算相机射线（局部空间）
    // 透视：从球心到相机的射线
    // 正交：固定方向
    float3 cam_ray = (is_persp) ?
                     model_view_matrix[3].xyz :  // 透视模式：相机到球心
                     float3(0.0f, 0.0f, -1.0f);  // 正交模式：正向

    cam_ray = to_float3x3(sphere_matrix) * cam_ray;

    // 步骤 7: 计算球体与相机的距离
    float cam_dist = length(cam_ray);

    // 步骤 8: 构建视图对齐的正交基
    float3 z_axis = cam_ray / cam_dist;           // 球心→相机方向
    float3 x_axis = normalize(cross(sphere_matrix[1].xyz, z_axis));
    float3 y_axis = cross(z_axis, x_axis);        // 生成正交系

    // 步骤 9: 半径计算与透视补偿
    float z_ofs = -0.05f - 1e-8f;  // 球体半径

    if (is_persp) {
        // 透视投影：远处的球体看起来更小
        // 需要调整位置使其投射成正圆

        // 计算视线的夹角
        constexpr float half_pi = 3.1415926f * 0.5f;
        float a = half_pi - asin(0.05f / cam_dist);  // 0.05 是半径
        float cos_b = cos(a);
        float sin_b = sqrt(clamp(1.0f - cos_b * cos_b, 0.0f, 1.0f));

        // 选择最近的圆，而非最大的（利用保守深度）
        float minor = cam_dist - 0.05f;
        float major = cam_dist - cos_b * 0.05f;
        float fac = minor / major;
        sin_b *= fac;

        // 缩放顶点
        x_axis *= sin_b;
        y_axis *= sin_b;
    }

    // 步骤 10: 计算最终顶点位置
    // 顶点位置通过相机对齐，形成正面圆盘
    float3 cam_pos = x_axis * pos.x + y_axis * pos.y + z_axis * z_ofs;

    // 步骤 11: 变换到裁剪空间
    float4 pos_4d = float4(cam_pos, 1.0f);
    float4 V = model_view_matrix * pos_4d;
    gl_Position = drw_view().winmat * V;

    // 传递到片段着色器
    view_position = V.xyz;  // 视图空间位置
    final_state_color = state_color.xyz;
    final_bone_color = bone_color.xyz;

    // 步骤 12: 裁剪处理
    float4 world_pos = model_mat * pos_4d;
    view_clipping_distances(world_pos.xyz);
}
```

### 4.2. 片段着色器光线求交

```glsl
// ===== 片段着色器（创建球体 3D 效果）=====

void main() {
    // 1. 重建球体矩阵（从顶点着色器传递）
    float4x4 sphere_matrix;
    sphere_matrix[0] = sphere_matrix0;
    sphere_matrix[1] = sphere_matrix1;
    sphere_matrix[2] = sphere_matrix2;
    sphere_matrix[3] = sphere_matrix3;

    // 2. 判断投影并构建光线
    bool is_perp = (drw_view().winmat[3][3] == 0.0f);

    // 透视：光线从视图原点出发
    // 正交：光线沿 Z 轴负向
    float3 ray_ori_view = (is_perp) ? float3(0.0f) : view_position.xyz;
    float3 ray_dir_view = (is_perp) ? view_position : float3(0.0f, 0.0f, -1.0f);

    // 3. 通过单次矩阵乘法转换到球体空间
    float4 mul_vec = (is_perp) ?
                     float4(ray_dir_view, 0.0f) :  // 透视：方向
                     float4(ray_ori_view, 1.0f);   // 正交：原点

    float3 mul_res = (sphere_matrix * mul_vec).xyz;

    // 4. 在球体空间中的光线
    float3 ray_ori = (is_perp) ? sphere_matrix[3].xyz : mul_res;
    float3 ray_dir = (is_perp) ? mul_res : -sphere_matrix[2].xyz;

    float ray_len = length(ray_dir);
    ray_dir /= ray_len;  // 归一化

    // 5. 线段与球体相交求解
    // 方程：|ray_ori + t * ray_dir|² = radius²
    // 展开：dot(ray_dir,ray_dir)*t² + 2*dot(ray_ori,ray_dir)*t + dot(ray_ori,ray_ori)-r² = 0
    // 简化：t² + 2bt + c = 0

    constexpr float sphere_radius_sqr = 0.05f * 0.05f;
    float b = dot(ray_ori, ray_dir);               // -b/2a
    float c = dot(ray_ori, ray_ori) - sphere_radius_sqr;
    float h = b * b - c;                           // 判别式
    float t = -sqrt(max(0.0f, h)) - b;             // 取交点参数

    // 6. 计算交点和法线（用于光照）
    float3 p = ray_dir * t + ray_ori;  // 交点
    float3 n = normalize(p);           // 球体法线（球心→点）

    // 7. 光照方向（使用视图 Z 轴）
    float3 l = normalize(sphere_matrix[2].xyz);

    // 8. 简单光照
    constexpr float s = 0.2f;  // 环境光
    float fac = clamp((dot(n, l) * (1.0f - s)) + s, 0.0f, 1.0f);

    // 9. 颜色混合（根据面向角度）
    frag_color.rgb = mix(final_state_color, final_bone_color, fac * fac);

    // 10. 2x2 抖动（让边缘更平滑）
    float dither = (0.5f + dot(
        float2(int2(gl_FragCoord.xy) & int2(1)),
        float2(1.0f, 2.0f)
    )) * 0.25f;
    dither *= (1.0f / 255.0f);

    frag_color = float4(frag_color.rgb + dither, alpha);

    // 11. 自定义深度（精确）
    t /= ray_len;
    gl_FragDepth = drw_depth_view_to_screen(
        ray_dir_view.z * t + ray_ori_view.z
    );

    select_id_output(select_id);
}
```

### 4.3. 交互点总结

| 技术 | 在此 Shader 中的作用 |
|-----|------|
| **实例渲染** | 使用 `gl_InstanceID` 一次绘制几千个骨骼 |
| **逆矩阵重构** | 片段着色器需要球体空间的完整变换 |
| **光线求交** | 在 2D 屏幕上模拟 3D 球体 |
| **视图对齐** | 四边形始终面对相机，看起来像球体 |
| **可变深度** | 正确处理遮挡，使用自定义深度值 |

---

## 5. 案例 4：权重分析着色器

**文件**: `overlay_edit_mesh_analysis_vert.glsl`

### 5.1. 简洁但巧妙

```glsl
// 输入：每个顶点一个权重值
in float weight;  // 权重: [0..1]

// 纹理查找表：权重 → 颜色
uniform sampler1D weight_tx;

// 输出颜色（泛用）
out vec4 weight_color;

float3 weight_to_rgb(float t) {
    // 特殊值处理
    if (t < 0.0f) {
        return float3(0.25f);  // 负值：灰色
    }
    else if (t > 1.0f) {
        return vec3(1.0f, 0.0f, 1.0f);  // 过高：红色
    }
    else {
        return texture(weight_tx, t).rgb;  // 正常：LUT 查找
    }
}

void main() {
    // 1. 简化：只需一个变换
    float3 world_pos = drw_point_object_to_world(pos);
    gl_Position = drw_point_world_to_homogenous(world_pos);

    // 2. 采样颜色查找表
    weight_color = float4(weight_to_rgb(weight), 1.0f);

    // 3. 裁剪
    view_clipping_distances(world_pos);
}
```

### 5.2. 权重颜色范围映射

```
在 C++ 中生成纹理：
weight = 0.0  →  蓝色
weight = 0.5  →  绿色
weight = 1.0  →  红色

纹理大小: 1D, 宽度 = 256 像素
CPU: palette[256] = 渐变计算 → upload to GPU
GPU: color = texture(weight_tx, weight)
```

---

## 6. 案例 5：UV 编辑边缘（概要）

**特点**：
- 无投影：2D 空间直接映射
- 无深度测试
- 可能需要虚线模式

```glsl
// ===== 虚线模式 =====
uniform float dash_length;  // 虚线长度
in vec2 edge_uv;            // 边上的坐标

void main() {
    // 计算沿边的长度
    float len = length(edge_uv);

    // 取模实现虚线
    float in_dash = mod(len, dash_length * 2.0) < dash_length ? 1.0 : 0.0;

    if (in_dash < 0.5) {
        discard;  // 丢弃虚线间隙
    }

    // 或者改变透明度
    final_color.a *= in_dash;
}
```

---

## 7. Shader 变体对比表

| Shader | 变体 | 核心功能 | 复杂度 | 使用库 |
|--------|------|----------|--------|--------|
| **边缘编辑** | VERT/EDGE/FACE/FACEDOT | 多模式共享 | 高 | 5个库 |
| **骨骼球体** | Solid/Outline | 实例 + 球体生成 | 中 | 3个库 |
| **权重分析** | 无 | 颜色映射 | 低 | 3个库 |
| **简单顶点** | 常规 | 坐标变换 | 低 | 2个库 |
| **网格线框** | Selectable | 抗锯齿线 | 中 | 4个库 |

### 性能特征

| Shader | 主要瓶颈 | 优化点 |
|--------|----------|--------|
| 编辑网格 | 几何着色器扩展 | 简化模式 |
| 骨骼球体 | 片段深度计算 | 视锥剔除 |
| 权重分析 | 纹理查找 | 减少顶点 |
| UV 边缘 | 无 | 静态数据 |

---

## 8. 从简单到复杂的学习路径

### 阶段 1：基础理解
1. **权重分析** → 简单：变换 + 颜色
2. **简单顶点** → 包含条件编译

### 阶段 2：中等复杂度
3. **骨骼球体** → 球体生成、实例渲染、光线求交
4. **UV 编辑** → 2D 空间、虚线模式

### 阶段 3：高级技巧
5. **边缘编辑** → 几何着色器、顶点拉取、抗锯齿
6. **完整网格** → 变体系统、深度偏移、Fresnel

---

## 9. 常见实现模式总结

### 模式 1：条件编译
```glsl
#ifdef VERT
   // 顶点逻辑
#elif defined(EDGE)
   // 边缘逻辑
#endif
```

### 模式 2：顶点拉取
```glsl
uint v_i = gpu_attr_load_index(v_i, gpu_attr_1);
pos = gpu_attr_load_float3(pos_buf, gpu_attr_0, v_i);
```

### 模式 3：片段光线求交
```glsl
// 构建光线 + 二次方程求解
float h = b*b - c;
float t = -sqrt(max(0,h)) - b;
```

### 模式 4：视图对齐
```glsl
// 构建正交基，面对相机
z_axis = view_dir;
x_axis = normalize(cross(up, z_axis));
y_axis = cross(z_axis, x_axis);
```

### 模式 5：纹理收集（深度测试）
```glsl
float4 depths = textureGather(depth_tx, uv);
bool occluded = all(greaterThan(frag_z, depths));
```

---

**文档用途**: 学习真实代码，理解复杂 Shader

**练习建议**:
1. 从权重分析开始（最简单）
2. 添加条件编译到简单顶点
3. 理解骨骼球体的光线求交
4. 尝试修改边缘宽度

---
**版本**: 1.0
**基于**: Blender 4.3 源码
**创建时间**: 2025-12-17
