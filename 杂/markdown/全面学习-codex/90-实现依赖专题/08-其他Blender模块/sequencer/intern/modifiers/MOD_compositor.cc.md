# 实现依赖专题：source/blender/sequencer/intern/modifiers/MOD_compositor.cc

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::seq::compositor_modifier_nodes_update_interface"]:::abstraction
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
  F["MOD_compositor.cc实现"]:::compute
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

<a id="f-59b61ebcfe34ecc0"></a>

### `blender::seq::compositor_modifier_nodes_update_interface`

实现位置：[source/blender/sequencer/intern/modifiers/MOD_compositor.cc](../../../../../../../../../source/blender/sequencer/intern/modifiers/MOD_compositor.cc) · L55—L75。

接口参数：

- `Main &bmain`
- `Scene &sequencer_scene`
- `SequencerCompositorModifierData &cmd`

**教学注释版**

<!-- annotated:492464ba73ecc7 -->

```cpp
void compositor_modifier_nodes_update_interface(Main &bmain,
                                                Scene &sequencer_scene,
                                                SequencerCompositorModifierData &cmd)
{
  if (!cmd.modifier.system_properties) {
    cmd.modifier.system_properties =
        bke::idprop::create_group("SequencerCompositorModifierProperties").release();
  }

  /* In case the node group is missing, do not update the properties to avoid the values reverting
   * to their default value if the node group later becomes available. */
  if (!cmd.node_group || ID_MISSING(cmd.node_group)) {
    return;
  }

  PointerRNA properties_ptr = RNA_pointer_create_discrete(
      &sequencer_scene.id, RNA_SequencerCompositorModifierProperties, &cmd);
  RNA_ensure_and_sync_system_properties(bmain, properties_ptr, *cmd.modifier.system_properties);

  DEG_id_tag_update(&sequencer_scene.id, ID_RECALC_SEQUENCER_STRIPS);
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/modifiers/MOD_compositor.cc · L55—L75</summary>

<!-- original:492464ba73ecc7:source/blender/sequencer/intern/modifiers/MOD_compositor.cc:55:75 -->

```cpp
void compositor_modifier_nodes_update_interface(Main &bmain,
                                                Scene &sequencer_scene,
                                                SequencerCompositorModifierData &cmd)
{
  if (!cmd.modifier.system_properties) {
    cmd.modifier.system_properties =
        bke::idprop::create_group("SequencerCompositorModifierProperties").release();
  }

  /* In case the node group is missing, do not update the properties to avoid the values reverting
   * to their default value if the node group later becomes available. */
  if (!cmd.node_group || ID_MISSING(cmd.node_group)) {
    return;
  }

  PointerRNA properties_ptr = RNA_pointer_create_discrete(
      &sequencer_scene.id, RNA_SequencerCompositorModifierProperties, &cmd);
  RNA_ensure_and_sync_system_properties(bmain, properties_ptr, *cmd.modifier.system_properties);

  DEG_id_tag_update(&sequencer_scene.id, ID_RECALC_SEQUENCER_STRIPS);
}
```

</details>

**沿实际写入检查状态**

- `cmd.modifier.system_properties =`

**继续追踪实现**

- `bke::idprop::create_group("SequencerCompositorModifierProperties").release` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L61。
- `bke::idprop::create_group` → [blender::bke::idprop::create_group · L155](../../../../02-BKE几何与数据/intern/idprop_create.cc.md#f-b1e2d8bfd5654bc2)。
- `ID_MISSING` → [ID_MISSING · L695](../../../makesdna/DNA_ID.h.md#m-ab9a2a270fb3)。宏定义由构建条件选择。
- `RNA_pointer_create_discrete` → [blender::RNA_pointer_create_discrete · L181](../../../makesrna/intern/rna_access.cc.md#f-592a276e869c6d94)。
- `RNA_ensure_and_sync_system_properties` → [blender::RNA_ensure_and_sync_system_properties · L6568](../../../makesrna/intern/rna_access.cc.md#f-3787705e085177e6)。
- `DEG_id_tag_update` → [blender::DEG_id_tag_update · L844](../../../../06-Depsgraph依赖图/intern/depsgraph_tag.cc.md#f-62d2949dd168bb81)。
