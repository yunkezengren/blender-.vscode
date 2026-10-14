# 实现依赖专题：source/blender/depsgraph/intern/builder/deg_builder_relations_scene.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::deg::DepsgraphRelationBuilder::build_scene_parameters"]:::abstraction
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
  F["deg_builder_relations_scene.cc实现"]:::compute
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

<a id="f-bcacd2e907f5c723"></a>

### `blender::deg::DepsgraphRelationBuilder::build_scene_parameters`

实现位置：[source/blender/depsgraph/intern/builder/deg_builder_relations_scene.cc](../../../../../source/blender/depsgraph/intern/builder/deg_builder_relations_scene.cc) · L50—L69。

接口参数：

- `Scene *scene`

**教学注释版**

<!-- annotated:f298f15da477e9 -->

```cpp
void DepsgraphRelationBuilder::build_scene_parameters(Scene *scene)
{
  if (built_map_.check_is_built_and_tag(scene, BuilderMap::TAG_PARAMETERS)) {
    return;
  }

  /* TODO(sergey): Trace as a scene parameters. */

  build_idproperties(scene->id.properties);
  build_idproperties(scene->id.system_properties);
  build_parameters(&scene->id);
  OperationKey parameters_eval_key(
      &scene->id, NodeType::PARAMETERS, OperationCode::PARAMETERS_EXIT);
  ComponentKey scene_eval_key(&scene->id, NodeType::SCENE);
  add_relation(parameters_eval_key, scene_eval_key, "Parameters -> Scene Eval");

  for (TimeMarker &marker : scene->markers) {
    build_idproperties(marker.prop);
  }
}
```

<details>
<summary>核对原始源码：source/blender/depsgraph/intern/builder/deg_builder_relations_scene.cc · L50—L69</summary>

<!-- original:f298f15da477e9:source/blender/depsgraph/intern/builder/deg_builder_relations_scene.cc:50:69 -->

```cpp
void DepsgraphRelationBuilder::build_scene_parameters(Scene *scene)
{
  if (built_map_.check_is_built_and_tag(scene, BuilderMap::TAG_PARAMETERS)) {
    return;
  }

  /* TODO(sergey): Trace as a scene parameters. */

  build_idproperties(scene->id.properties);
  build_idproperties(scene->id.system_properties);
  build_parameters(&scene->id);
  OperationKey parameters_eval_key(
      &scene->id, NodeType::PARAMETERS, OperationCode::PARAMETERS_EXIT);
  ComponentKey scene_eval_key(&scene->id, NodeType::SCENE);
  add_relation(parameters_eval_key, scene_eval_key, "Parameters -> Scene Eval");

  for (TimeMarker &marker : scene->markers) {
    build_idproperties(marker.prop);
  }
}
```

</details>

**继续追踪实现**

- `built_map_.check_is_built_and_tag` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L52。
- `build_idproperties` → [blender::deg::DepsgraphRelationBuilder::build_idproperties · L635](04-%E5%85%B3%E7%B3%BB%E6%9E%84%E5%BB%BA%E5%99%A8.md#f-098c28c24f9a599e)；[blender::deg::DepsgraphNodeBuilder::build_idproperties · L685](03-%E8%8A%82%E7%82%B9%E6%9E%84%E5%BB%BA%E5%99%A8.md#f-cff75bdb39624564)。同名重载需按实参类型选择。
- `build_parameters` → [blender::deg::DepsgraphRelationBuilder::build_parameters · L2238](04-%E5%85%B3%E7%B3%BB%E6%9E%84%E5%BB%BA%E5%99%A8.md#f-a095a33b2fc26d07)；[blender::deg::DepsgraphNodeBuilder::build_parameters · L1468](03-%E8%8A%82%E7%82%B9%E6%9E%84%E5%BB%BA%E5%99%A8.md#f-c3ba3affce030f5d)。同名重载需按实参类型选择。
- `add_relation` → [blender::deg::DepsgraphRelationBuilder::add_relation · L29](%E4%BE%9D%E8%B5%96-deg_builder_relations_impl-5ae258.md#f-9c9f4ea4be1f8780)；[blender::deg::DepsgraphRelationBuilder::add_relation · L66](%E4%BE%9D%E8%B5%96-deg_builder_relations_impl-5ae258.md#f-5b2ef1e631a55534)。同名重载需按实参类型选择。
