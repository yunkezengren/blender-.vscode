# 实现依赖专题：source/blender/blenkernel/intern/multires_subdiv.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::BKE_multires_subdiv_settings_init"]:::abstraction
  F1["blender::BKE_multires_subdiv_mesh_settings_init"]:::compute
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
  F["multires_subdiv.cc实现"]:::compute
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

<a id="f-a313efd66d1384ce"></a>

### `blender::BKE_multires_subdiv_settings_init`

实现位置：[source/blender/blenkernel/intern/multires_subdiv.cc](../../../../../source/blender/blenkernel/intern/multires_subdiv.cc) · L16—L27。

接口参数：

- `bke::subdiv::Settings *settings`
- `const MultiresModifierData *mmd`

**教学注释版**

<!-- annotated:5253970ad92fb6 -->

```cpp
void BKE_multires_subdiv_settings_init(bke::subdiv::Settings *settings,
                                       const MultiresModifierData *mmd)
{
  settings->is_simple = false;
  settings->is_adaptive = true;
  settings->level = settings->is_simple ? 1 : mmd->quality;
  settings->use_creases = (mmd->flags & eMultiresModifierFlag_UseCrease);
  settings->vtx_boundary_interpolation = bke::subdiv::vtx_boundary_interpolation_from_subsurf(
      mmd->boundary_smooth);
  settings->fvar_linear_interpolation = bke::subdiv::fvar_interpolation_from_uv_smooth(
      mmd->uv_smooth);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/multires_subdiv.cc · L16—L27</summary>

<!-- original:5253970ad92fb6:source/blender/blenkernel/intern/multires_subdiv.cc:16:27 -->

```cpp
void BKE_multires_subdiv_settings_init(bke::subdiv::Settings *settings,
                                       const MultiresModifierData *mmd)
{
  settings->is_simple = false;
  settings->is_adaptive = true;
  settings->level = settings->is_simple ? 1 : mmd->quality;
  settings->use_creases = (mmd->flags & eMultiresModifierFlag_UseCrease);
  settings->vtx_boundary_interpolation = bke::subdiv::vtx_boundary_interpolation_from_subsurf(
      mmd->boundary_smooth);
  settings->fvar_linear_interpolation = bke::subdiv::fvar_interpolation_from_uv_smooth(
      mmd->uv_smooth);
}
```

</details>

**沿实际写入检查状态**

- `settings->is_simple = false;`
- `settings->is_adaptive = true;`
- `settings->level = settings->is_simple ? 1 : mmd->quality;`
- `settings->use_creases = (mmd->flags & eMultiresModifierFlag_UseCrease);`
- `settings->vtx_boundary_interpolation = bke::subdiv::vtx_boundary_interpolation_from_subsurf(`
- `settings->fvar_linear_interpolation = bke::subdiv::fvar_interpolation_from_uv_smooth(`

**继续追踪实现**

- `bke::subdiv::vtx_boundary_interpolation_from_subsurf` → [blender::bke::subdiv::vtx_boundary_interpolation_from_subsurf · L69](%E4%BE%9D%E8%B5%96-subdiv-6aa500.md#f-933a39ad7057338e)。
- `bke::subdiv::fvar_interpolation_from_uv_smooth` → [blender::bke::subdiv::fvar_interpolation_from_uv_smooth · L49](%E4%BE%9D%E8%B5%96-subdiv-6aa500.md#f-767f64d27fdc130d)。

<a id="f-a2a91c018e742a96"></a>

### `blender::BKE_multires_subdiv_mesh_settings_init`

实现位置：[source/blender/blenkernel/intern/multires_subdiv.cc](../../../../../source/blender/blenkernel/intern/multires_subdiv.cc) · L29—L41。

接口参数：

- `bke::subdiv::ToMeshSettings *mesh_settings`
- `const Scene *scene`
- `const Object *object`
- `const MultiresModifierData *mmd`
- `const bool use_render_params`
- `const bool ignore_simplify`
- `const bool ignore_control_edges`

**教学注释版**

<!-- annotated:26e38fd6360ffd -->

```cpp
void BKE_multires_subdiv_mesh_settings_init(bke::subdiv::ToMeshSettings *mesh_settings,
                                            const Scene *scene,
                                            const Object *object,
                                            const MultiresModifierData *mmd,
                                            const bool use_render_params,
                                            const bool ignore_simplify,
                                            const bool ignore_control_edges)
{
  const int level = multires_get_level(scene, object, mmd, use_render_params, ignore_simplify);
  mesh_settings->resolution = (1 << level) + 1;
  mesh_settings->use_optimal_display = (mmd->flags & eMultiresModifierFlag_ControlEdges) &&
                                       !ignore_control_edges;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/multires_subdiv.cc · L29—L41</summary>

<!-- original:26e38fd6360ffd:source/blender/blenkernel/intern/multires_subdiv.cc:29:41 -->

```cpp
void BKE_multires_subdiv_mesh_settings_init(bke::subdiv::ToMeshSettings *mesh_settings,
                                            const Scene *scene,
                                            const Object *object,
                                            const MultiresModifierData *mmd,
                                            const bool use_render_params,
                                            const bool ignore_simplify,
                                            const bool ignore_control_edges)
{
  const int level = multires_get_level(scene, object, mmd, use_render_params, ignore_simplify);
  mesh_settings->resolution = (1 << level) + 1;
  mesh_settings->use_optimal_display = (mmd->flags & eMultiresModifierFlag_ControlEdges) &&
                                       !ignore_control_edges;
}
```

</details>

**沿实际写入检查状态**

- `mesh_settings->resolution = (1 << level) + 1;`
- `mesh_settings->use_optimal_display = (mmd->flags & eMultiresModifierFlag_ControlEdges) &&`

**继续追踪实现**

- `multires_get_level` → [blender::multires_get_level · L212](%E4%BE%9D%E8%B5%96-multires-7e6ba8.md#f-8f4d947b77878017)。
