# 实现依赖专题：source/blender/editors/space_outliner/outliner_collections.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::ED_outliner_selected_objects_get"]:::abstraction
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
  F["outliner_collections.cc实现"]:::compute
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

<a id="f-49463d1f29e92c6b"></a>

### `blender::ED_outliner_selected_objects_get`

实现位置：[source/blender/editors/space_outliner/outliner_collections.cc](../../../../../../../../source/blender/editors/space_outliner/outliner_collections.cc) · L153—L171。

接口参数：

- `const bContext *C`
- `ListBaseT<LinkData> *objects`

**教学注释版**

<!-- annotated:74b284398e6dfa -->

```cpp
void ED_outliner_selected_objects_get(const bContext *C, ListBaseT<LinkData> *objects)
{
  using namespace blender::ed::outliner;

  SpaceOutliner *space_outliner = CTX_wm_space_outliner(C);
  IDsSelectedData data = {{nullptr}};
  outliner_tree_traverse(space_outliner,
                         &space_outliner->runtime->tree,
                         0,
                         TSE_SELECTED,
                         outliner_collect_selected_objects,
                         &data);
  for (LinkData &link : data.selected_array) {
    TreeElement *ten_selected = static_cast<TreeElement *>(link.data);
    Object *ob = id_cast<Object *>(TREESTORE(ten_selected)->id);
    BLI_addtail(objects, BLI_genericNodeN(ob));
  }
  data.selected_array.free_no_destruct();
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_outliner/outliner_collections.cc · L153—L171</summary>

<!-- original:74b284398e6dfa:source/blender/editors/space_outliner/outliner_collections.cc:153:171 -->

```cpp
void ED_outliner_selected_objects_get(const bContext *C, ListBaseT<LinkData> *objects)
{
  using namespace blender::ed::outliner;

  SpaceOutliner *space_outliner = CTX_wm_space_outliner(C);
  IDsSelectedData data = {{nullptr}};
  outliner_tree_traverse(space_outliner,
                         &space_outliner->runtime->tree,
                         0,
                         TSE_SELECTED,
                         outliner_collect_selected_objects,
                         &data);
  for (LinkData &link : data.selected_array) {
    TreeElement *ten_selected = static_cast<TreeElement *>(link.data);
    Object *ob = id_cast<Object *>(TREESTORE(ten_selected)->id);
    BLI_addtail(objects, BLI_genericNodeN(ob));
  }
  data.selected_array.free_no_destruct();
}
```

</details>

**继续追踪实现**

- `CTX_wm_space_outliner` → [blender::CTX_wm_space_outliner · L1076](../../../02-BKE几何与数据/intern/context.cc.md#f-f8d504d7f208fe51)。
- `outliner_tree_traverse` → [blender::ed::outliner::outliner_tree_traverse · L306](outliner_utils.cc.md#f-b61df82f59e25d78)。
- `id_cast<Object *>` → [blender::id_cast · L1417](../../makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `TREESTORE` → [TREESTORE · L197](outliner_intern.hh.md#m-e90e76fc5e4d)。宏定义由构建条件选择。
- `BLI_addtail` → [blender::BLI_addtail · L118](../../../01-BLI基础库/intern/listbase.cc.md#f-4fb027713fa3115b)。
- `BLI_genericNodeN` → [blender::BLI_genericNodeN · L936](../../../01-BLI基础库/intern/listbase.cc.md#f-a3f8fad9ff74a185)。
- `data.selected_array.free_no_destruct` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L170。
