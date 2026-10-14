# 实现依赖专题：source/blender/blenkernel/intern/mesh_sample.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::bke::mesh_surface_sample::compute_bary_coord_in_triangle"]:::abstraction
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  C["调用者提供参数与有效对象"]:::input
  F["mesh_sample.cc实现"]:::compute
  R["结果与被修改状态"]:::result
  C -->|"进入"| F
  F -->|"返回或提交"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  T["具体类型与模板实参"]:::abstraction
  B["分支与构建条件"]:::data
  I["匹配的实现"]:::compute
  E["标准库或系统契约边界"]:::result
  T -->|"静态选择"| I
  B -->|"配置选择"| I
  I -->|"到达外部接口"| E
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  S["完整源码单元"]:::input
  A["教学注释与推导"]:::abstraction
  D["被调用实现专题"]:::compute
  V["原文与token一致性检查"]:::result
  S -->|"就近阅读"| A
  A -->|"继续深入"| D
  A -->|"核对"| V
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

## 完整成员与函数实现

<a id="f-1fd0d60fb57c63d1"></a>

### `blender::bke::mesh_surface_sample::compute_bary_coord_in_triangle`

实现位置：[source/blender/blenkernel/intern/mesh_sample.cc](../../../../../source/blender/blenkernel/intern/mesh_sample.cc) · L340—L351。

接口参数：

- `const Span<float3> vert_positions`
- `const Span<int> corner_verts`
- `const int3 &tri`
- `const float3 &position`

**教学注释版**

<!-- annotated:d7586c60bdaba4 -->

```cpp
float3 compute_bary_coord_in_triangle(const Span<float3> vert_positions,
                                      const Span<int> corner_verts,
                                      const int3 &tri,
                                      const float3 &position)
{
  const float3 &v0 = vert_positions[corner_verts[tri[0]]];
  const float3 &v1 = vert_positions[corner_verts[tri[1]]];
  const float3 &v2 = vert_positions[corner_verts[tri[2]]];
  float3 bary_coords;
  interp_weights_tri_v3(bary_coords, v0, v1, v2, position);
  return bary_coords;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/mesh_sample.cc · L340—L351</summary>

<!-- original:d7586c60bdaba4:source/blender/blenkernel/intern/mesh_sample.cc:340:351 -->

```cpp
float3 compute_bary_coord_in_triangle(const Span<float3> vert_positions,
                                      const Span<int> corner_verts,
                                      const int3 &tri,
                                      const float3 &position)
{
  const float3 &v0 = vert_positions[corner_verts[tri[0]]];
  const float3 &v1 = vert_positions[corner_verts[tri[1]]];
  const float3 &v2 = vert_positions[corner_verts[tri[2]]];
  float3 bary_coords;
  interp_weights_tri_v3(bary_coords, v0, v1, v2, position);
  return bary_coords;
}
```

</details>

**结果出口**

- `return bary_coords;`

**继续追踪实现**

- `interp_weights_tri_v3` → [blender::interp_weights_tri_v3 · L3782](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_geom-8d91a3.md#f-f1812aa46b84ce2c)。
