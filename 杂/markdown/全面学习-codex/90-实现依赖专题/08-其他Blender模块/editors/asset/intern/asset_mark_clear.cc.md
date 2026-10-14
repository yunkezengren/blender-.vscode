# 实现依赖专题：source/blender/editors/asset/intern/asset_mark_clear.cc

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::ed::asset::can_mark_single_from_context"]:::abstraction
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
  F["asset_mark_clear.cc实现"]:::compute
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

<a id="f-227b4f2ce477f9ba"></a>

### `blender::ed::asset::can_mark_single_from_context`

实现位置：[source/blender/editors/asset/intern/asset_mark_clear.cc](../../../../../../../../../source/blender/editors/asset/intern/asset_mark_clear.cc) · L111—L120。

接口参数：

- `const bContext *C`

**教学注释版**

<!-- annotated:3d5a9d29162f4c -->

```cpp
bool can_mark_single_from_context(const bContext *C)
{
  /* Context needs a "id" pointer to be set for #ASSET_OT_mark()/#ASSET_OT_mark_single() and
   * #ASSET_OT_clear()/#ASSET_OT_clear_single() to use. */
  const ID *id = static_cast<ID *>(CTX_data_pointer_get_type_silent(C, "id", RNA_ID).data);
  if (!id) {
    return false;
  }
  return id_type_is_supported(id);
}
```

<details>
<summary>核对原始源码：source/blender/editors/asset/intern/asset_mark_clear.cc · L111—L120</summary>

<!-- original:3d5a9d29162f4c:source/blender/editors/asset/intern/asset_mark_clear.cc:111:120 -->

```cpp
bool can_mark_single_from_context(const bContext *C)
{
  /* Context needs a "id" pointer to be set for #ASSET_OT_mark()/#ASSET_OT_mark_single() and
   * #ASSET_OT_clear()/#ASSET_OT_clear_single() to use. */
  const ID *id = static_cast<ID *>(CTX_data_pointer_get_type_silent(C, "id", RNA_ID).data);
  if (!id) {
    return false;
  }
  return id_type_is_supported(id);
}
```

</details>

**结果出口**

- `return false;`
- `return id_type_is_supported(id);`

**继续追踪实现**

- `CTX_data_pointer_get_type_silent` → [blender::CTX_data_pointer_get_type_silent · L680](../../../../02-BKE几何与数据/intern/context.cc.md#f-cbffa111260463df)。
- `id_type_is_supported` → [blender::ed::asset::id_type_is_supported · L26](asset_type.cc.md#f-d0e3b4d35746f0be)。
