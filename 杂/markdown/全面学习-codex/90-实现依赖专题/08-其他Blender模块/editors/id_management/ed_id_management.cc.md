# 实现依赖专题：source/blender/editors/id_management/ed_id_management.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::ED_id_rename"]:::abstraction
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
  F["ed_id_management.cc实现"]:::compute
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

<a id="f-7603f92d63149572"></a>

### `blender::ED_id_rename`

实现位置：[source/blender/editors/id_management/ed_id_management.cc](../../../../../../../../source/blender/editors/id_management/ed_id_management.cc) · L26—L73。

接口参数：

- `Main &bmain`
- `ID &id`
- `StringRefNull name`

**教学注释版**

<!-- annotated:1d4d88051a05d0 -->

```cpp
bool ED_id_rename(Main &bmain, ID &id, StringRefNull name)
{
  BLI_assert(ID_IS_EDITABLE(&id));

  const IDNewNameResult result = BKE_id_rename(
      bmain, id, name, IDNewNameMode::RenameExistingSameRoot);

  switch (result.action) {
    case IDNewNameResult::Action::UNCHANGED:
      CLOG_DEBUG(&LOG, "ID '%s' not renamed, already using the requested name", id.name + 2);
      return false;
    case IDNewNameResult::Action::UNCHANGED_COLLISION:
      CLOG_DEBUG(&LOG,
                 "ID '%s' not renamed, requested new name '%s' would collide with an existing one",
                 id.name + 2,
                 name.c_str());
      return false;
    case IDNewNameResult::Action::RENAMED_NO_COLLISION:
      CLOG_DEBUG(&LOG, "ID '%s' renamed without any collision", id.name + 2);
      WM_main_add_notifier(NC_ID | NA_RENAME, &id);
      return true;
    case IDNewNameResult::Action::RENAMED_COLLISION_ADJUSTED:
      CLOG_DEBUG(&LOG,
                 "ID '%s' renamed with adjustment from requested name '%s', to avoid name "
                 "collision with another ID",
                 id.name + 2,
                 name.c_str());
      WM_global_reportf(RPT_INFO,
                        "Data-block renamed to '%s', try again to force renaming it to '%s'",
                        id.name + 2,
                        name.c_str());
      WM_main_add_notifier(NC_ID | NA_RENAME, &id);
      return true;
    case IDNewNameResult::Action::RENAMED_COLLISION_FORCED:
      CLOG_DEBUG(
          &LOG,
          "ID '%s' forcefully renamed, another ID had to also be renamed to avoid name collision",
          id.name + 2);
      WM_global_reportf(RPT_INFO,
                        "Name in use. The other data-block was renamed to '%s'",
                        result.other_id->name + 2);
      WM_main_add_notifier(NC_ID | NA_RENAME, &id);
      WM_main_add_notifier(NC_ID | NA_RENAME, result.other_id);
      return true;
  }

  return false;
}
```

<details>
<summary>核对原始源码：source/blender/editors/id_management/ed_id_management.cc · L26—L73</summary>

<!-- original:1d4d88051a05d0:source/blender/editors/id_management/ed_id_management.cc:26:73 -->

```cpp
bool ED_id_rename(Main &bmain, ID &id, StringRefNull name)
{
  BLI_assert(ID_IS_EDITABLE(&id));

  const IDNewNameResult result = BKE_id_rename(
      bmain, id, name, IDNewNameMode::RenameExistingSameRoot);

  switch (result.action) {
    case IDNewNameResult::Action::UNCHANGED:
      CLOG_DEBUG(&LOG, "ID '%s' not renamed, already using the requested name", id.name + 2);
      return false;
    case IDNewNameResult::Action::UNCHANGED_COLLISION:
      CLOG_DEBUG(&LOG,
                 "ID '%s' not renamed, requested new name '%s' would collide with an existing one",
                 id.name + 2,
                 name.c_str());
      return false;
    case IDNewNameResult::Action::RENAMED_NO_COLLISION:
      CLOG_DEBUG(&LOG, "ID '%s' renamed without any collision", id.name + 2);
      WM_main_add_notifier(NC_ID | NA_RENAME, &id);
      return true;
    case IDNewNameResult::Action::RENAMED_COLLISION_ADJUSTED:
      CLOG_DEBUG(&LOG,
                 "ID '%s' renamed with adjustment from requested name '%s', to avoid name "
                 "collision with another ID",
                 id.name + 2,
                 name.c_str());
      WM_global_reportf(RPT_INFO,
                        "Data-block renamed to '%s', try again to force renaming it to '%s'",
                        id.name + 2,
                        name.c_str());
      WM_main_add_notifier(NC_ID | NA_RENAME, &id);
      return true;
    case IDNewNameResult::Action::RENAMED_COLLISION_FORCED:
      CLOG_DEBUG(
          &LOG,
          "ID '%s' forcefully renamed, another ID had to also be renamed to avoid name collision",
          id.name + 2);
      WM_global_reportf(RPT_INFO,
                        "Name in use. The other data-block was renamed to '%s'",
                        result.other_id->name + 2);
      WM_main_add_notifier(NC_ID | NA_RENAME, &id);
      WM_main_add_notifier(NC_ID | NA_RENAME, result.other_id);
      return true;
  }

  return false;
}
```

</details>

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `ID_IS_EDITABLE` → [ID_IS_EDITABLE · L708](../../makesdna/DNA_ID.h.md#m-57579f93767f)。宏定义由构建条件选择。
- `BKE_id_rename` → [blender::BKE_id_rename · L2654](../../../02-BKE几何与数据/intern/lib_id.cc.md#f-366d3be77c856752)。
- `CLOG_DEBUG` → [CLOG_DEBUG · L191](../../../07-Intern运行时与平台/clog/CLG_log.h.md#m-e062f5f17675)。宏定义由构建条件选择。
- `name.c_str` → [blender::StringRefNull::c_str · L544](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-4a8bbfe1e6d00757)。
- `WM_main_add_notifier` → [blender::WM_main_add_notifier · L403](../../windowmanager/intern/wm_event_system.cc.md#f-29a090eae8ebe51c)。
- `WM_global_reportf` → [blender::WM_global_reportf · L1069](../../windowmanager/intern/wm_event_system.cc.md#f-bebcdbebb52fae1d)。
