# 实现依赖专题：source/blender/depsgraph/intern/eval/deg_eval_stats.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::deg::deg_eval_stats_aggregate"]:::abstraction
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
  F["deg_eval_stats.cc实现"]:::compute
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

<a id="f-bda18eeb58d4a24a"></a>

### `blender::deg::deg_eval_stats_aggregate`

实现位置：[source/blender/depsgraph/intern/eval/deg_eval_stats.cc](../../../../../../../../source/blender/depsgraph/intern/eval/deg_eval_stats.cc) · L20—L38。

接口参数：

- `Depsgraph *graph`

**教学注释版**

<!-- annotated:62c2cb91887dee -->

```cpp
void deg_eval_stats_aggregate(Depsgraph *graph)
{
  /* Reset current evaluation stats for ID and component nodes.
   * Those are not filled in by the evaluation engine. */
  for (Node *node : graph->id_nodes) {
    IDNode *id_node = static_cast<IDNode *>(node);
    for (ComponentNode *comp_node : id_node->components.values()) {
      comp_node->stats.reset_current();
    }
    id_node->stats.reset_current();
  }
  /* Now accumulate operation timings to components and IDs. */
  for (OperationNode *op_node : graph->operations) {
    ComponentNode *comp_node = op_node->owner;
    IDNode *id_node = comp_node->owner;
    id_node->stats.current_time += op_node->stats.current_time;
    comp_node->stats.current_time += op_node->stats.current_time;
  }
}
```

<details>
<summary>核对原始源码：source/blender/depsgraph/intern/eval/deg_eval_stats.cc · L20—L38</summary>

<!-- original:62c2cb91887dee:source/blender/depsgraph/intern/eval/deg_eval_stats.cc:20:38 -->

```cpp
void deg_eval_stats_aggregate(Depsgraph *graph)
{
  /* Reset current evaluation stats for ID and component nodes.
   * Those are not filled in by the evaluation engine. */
  for (Node *node : graph->id_nodes) {
    IDNode *id_node = static_cast<IDNode *>(node);
    for (ComponentNode *comp_node : id_node->components.values()) {
      comp_node->stats.reset_current();
    }
    id_node->stats.reset_current();
  }
  /* Now accumulate operation timings to components and IDs. */
  for (OperationNode *op_node : graph->operations) {
    ComponentNode *comp_node = op_node->owner;
    IDNode *id_node = comp_node->owner;
    id_node->stats.current_time += op_node->stats.current_time;
    comp_node->stats.current_time += op_node->stats.current_time;
  }
}
```

</details>

**沿实际写入检查状态**

- `id_node->stats.current_time += op_node->stats.current_time;`
- `comp_node->stats.current_time += op_node->stats.current_time;`

**继续追踪实现**

- `id_node->components.values` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L26。
- `comp_node->stats.reset_current` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L27。
- `id_node->stats.reset_current` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L29。
