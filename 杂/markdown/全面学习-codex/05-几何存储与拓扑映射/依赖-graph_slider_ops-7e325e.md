# 实现依赖专题：source/blender/editors/space_graph/graph_slider_ops.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::update_depsgraph"]:::abstraction
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
  F["graph_slider_ops.cc实现"]:::compute
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

<a id="f-78fb90c2baa1fefe"></a>

### `blender::update_depsgraph`

实现位置：[source/blender/editors/space_graph/graph_slider_ops.cc](../../../../../source/blender/editors/space_graph/graph_slider_ops.cc) · L278—L290。

接口参数：

- `tGraphSliderOp *gso`

**教学注释版**

<!-- annotated:6642484b0a76be -->

```cpp
static void update_depsgraph(tGraphSliderOp *gso)
{
  ListBaseT<bAnimListElem> anim_data = {nullptr, nullptr};

  bAnimContext *ac = &gso->ac;
  ANIM_animdata_filter(
      ac, &anim_data, OPERATOR_DATA_FILTER, ac->data, eAnimCont_Types(ac->datatype));
  for (bAnimListElem &ale : anim_data) {
    DEG_id_tag_update(ale.fcurve_owner_id, ID_RECALC_ANIMATION);
  }

  ANIM_animdata_freelist(&anim_data);
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_graph/graph_slider_ops.cc · L278—L290</summary>

<!-- original:6642484b0a76be:source/blender/editors/space_graph/graph_slider_ops.cc:278:290 -->

```cpp
static void update_depsgraph(tGraphSliderOp *gso)
{
  ListBaseT<bAnimListElem> anim_data = {nullptr, nullptr};

  bAnimContext *ac = &gso->ac;
  ANIM_animdata_filter(
      ac, &anim_data, OPERATOR_DATA_FILTER, ac->data, eAnimCont_Types(ac->datatype));
  for (bAnimListElem &ale : anim_data) {
    DEG_id_tag_update(ale.fcurve_owner_id, ID_RECALC_ANIMATION);
  }

  ANIM_animdata_freelist(&anim_data);
}
```

</details>

**继续追踪实现**

- `ANIM_animdata_filter` → [blender::ANIM_animdata_filter · L3958](%E4%BE%9D%E8%B5%96-anim_filter-ad667b.md#f-90a333015e7ffee7)。
- `eAnimCont_Types` → [blender::eAnimCont_Types](%E4%BE%9D%E8%B5%96-ED_anim_api-28e639.md#t-0af283128251)。
- `DEG_id_tag_update` → [blender::DEG_id_tag_update · L844](../11-Depsgraph%E4%B8%8E%E5%B9%B6%E8%A1%8C%E4%BB%BB%E5%8A%A1%E7%B3%BB%E7%BB%9F/%E4%BE%9D%E8%B5%96-depsgraph_tag-d8b3c7.md#f-62d2949dd168bb81)。
- `ANIM_animdata_freelist` → [blender::ANIM_animdata_freelist · L472](%E4%BE%9D%E8%B5%96-anim_deps-ba7801.md#f-b53b43ffdc2da250)。
