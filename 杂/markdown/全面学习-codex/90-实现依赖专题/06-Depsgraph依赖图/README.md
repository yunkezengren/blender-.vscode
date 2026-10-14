# 06-Depsgraph依赖图

[实现依赖总导航](../README.md)

## 模块公共接口

- [DEG_depsgraph.hh](DEG_depsgraph.hh.md)
- [DEG_depsgraph_query.hh](DEG_depsgraph_query.hh.md)

## intern

- [depsgraph.cc](intern/depsgraph.cc.md)
- [depsgraph_build.cc](intern/depsgraph_build.cc.md)
- [depsgraph_debug.cc](intern/depsgraph_debug.cc.md)
- [depsgraph_eval.cc](intern/depsgraph_eval.cc.md)
- [depsgraph_light_linking.cc](intern/depsgraph_light_linking.cc.md)
- [depsgraph_physics.cc](intern/depsgraph_physics.cc.md)
- [depsgraph_query.cc](intern/depsgraph_query.cc.md)
- [depsgraph_query_foreach.cc](intern/depsgraph_query_foreach.cc.md)
- [depsgraph_query_iter.cc](intern/depsgraph_query_iter.cc.md)
- [depsgraph_registry.cc](intern/depsgraph_registry.cc.md)
- [depsgraph_relation.cc](intern/depsgraph_relation.cc.md)
- [depsgraph_tag.cc](intern/depsgraph_tag.cc.md)
- [depsgraph_type.cc](intern/depsgraph_type.cc.md)
- [depsgraph_type.hh](intern/depsgraph_type.hh.md)
- [depsgraph_update.cc](intern/depsgraph_update.cc.md)
- [depsgraph_writeback_sync.cc](intern/depsgraph_writeback_sync.cc.md)

## intern/builder

- [deg_builder.cc](intern/builder/deg_builder.cc.md)
- [deg_builder_cache.cc](intern/builder/deg_builder_cache.cc.md)
- [deg_builder_key.cc](intern/builder/deg_builder_key.cc.md)
- [deg_builder_key.h](intern/builder/deg_builder_key.h.md)
- [deg_builder_nodes.h](intern/builder/deg_builder_nodes.h.md)
- [deg_builder_nodes_rig.cc](intern/builder/deg_builder_nodes_rig.cc.md)
- [deg_builder_nodes_scene.cc](intern/builder/deg_builder_nodes_scene.cc.md)
- [deg_builder_pchanmap.cc](intern/builder/deg_builder_pchanmap.cc.md)
- [deg_builder_relations.h](intern/builder/deg_builder_relations.h.md)
- [deg_builder_relations_drivers.cc](intern/builder/deg_builder_relations_drivers.cc.md)
- [deg_builder_relations_impl.h](intern/builder/deg_builder_relations_impl.h.md)
- [deg_builder_relations_rig.cc](intern/builder/deg_builder_relations_rig.cc.md)
- [deg_builder_relations_scene.cc](intern/builder/deg_builder_relations_scene.cc.md)
- [deg_builder_rna.cc](intern/builder/deg_builder_rna.cc.md)

## intern/debug

- [deg_debug.cc](intern/debug/deg_debug.cc.md)
- [deg_debug.h](intern/debug/deg_debug.h.md)

## intern/eval

- [deg_eval_copy_on_write.cc](intern/eval/deg_eval_copy_on_write.cc.md)
- [deg_eval_copy_on_write.h](intern/eval/deg_eval_copy_on_write.h.md)
- [deg_eval_runtime_backup.cc](intern/eval/deg_eval_runtime_backup.cc.md)
- [deg_eval_stats.cc](intern/eval/deg_eval_stats.cc.md)

## intern/node

- [deg_node.cc](intern/node/deg_node.cc.md)
- [deg_node.hh](intern/node/deg_node.hh.md)
- [deg_node_component.cc](intern/node/deg_node_component.cc.md)
- [deg_node_factory.cc](intern/node/deg_node_factory.cc.md)
- [deg_node_factory_impl.hh](intern/node/deg_node_factory_impl.hh.md)
- [deg_node_id.cc](intern/node/deg_node_id.cc.md)
- [deg_node_operation.cc](intern/node/deg_node_operation.cc.md)

```mermaid
flowchart TB
  E["06-Depsgraph依赖图"]:::input
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
