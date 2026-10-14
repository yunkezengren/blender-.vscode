# 05-Geometry几何算法

[实现依赖总导航](../README.md)

## 模块公共接口

- [GEO_mesh_copy_selection.hh](GEO_mesh_copy_selection.hh.md)
- [GEO_realize_instances.hh](GEO_realize_instances.hh.md)

## intern

- [extend_curves.cc](intern/extend_curves.cc.md)
- [foreach_geometry.cc](intern/foreach_geometry.cc.md)
- [join_geometries.cc](intern/join_geometries.cc.md)
- [mesh_boolean.cc](intern/mesh_boolean.cc.md)
- [mesh_boolean_manifold.cc](intern/mesh_boolean_manifold.cc.md)
- [mesh_merge_verts.cc](intern/mesh_merge_verts.cc.md)
- [mesh_to_volume.cc](intern/mesh_to_volume.cc.md)
- [randomize.cc](intern/randomize.cc.md)
- [realize_instances.cc](intern/realize_instances.cc.md)
- [reorder.cc](intern/reorder.cc.md)
- [resample_curves.cc](intern/resample_curves.cc.md)
- [simplify_curves.cc](intern/simplify_curves.cc.md)
- [smooth_curves.cc](intern/smooth_curves.cc.md)
- [subdivide_curves.cc](intern/subdivide_curves.cc.md)
- [trim_curves.cc](intern/trim_curves.cc.md)

```mermaid
flowchart TB
  E["05-Geometry几何算法"]:::input
  Q["按主题选择正文"]:::abstraction
  S["按需追踪实现依赖"]:::compute
  R["回到调用点核对行为"]:::result
  E -->|"进入"| Q
  Q -->|"查实现"| S
  S -->|"带着问题返回"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  M["主线学习"]:::input
  D["类与函数实现"]:::data
  H["历史提交与证据"]:::abstraction
  M -->|"深入"| D
  D -->|"核对演化"| H
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```
