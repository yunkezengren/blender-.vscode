# 实现依赖专题：source/blender/windowmanager/intern/wm.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::WM_operator_free"]:::abstraction
  F1["blender::WM_operator_free_all_after"]:::compute
  F2["blender::wm_operator_register"]:::compute
  F0 -->|"显式调用"| F0
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F0
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
  F["wm.cc实现"]:::compute
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

<a id="f-58bc17403b28c17b"></a>

### `blender::WM_operator_free`

实现位置：[source/blender/windowmanager/intern/wm.cc](../../../../../source/blender/windowmanager/intern/wm.cc) · L275—L308。

接口参数：

- `wmOperator *op`

**教学注释版**

<!-- annotated:9639c412eefe6c -->

```cpp
void WM_operator_free(wmOperator *op)
{

#ifdef WITH_PYTHON
  if (op->py_instance) {
    /* Do this first in case there are any __del__ functions or similar that use properties. */
    BPY_DECREF_RNA_INVALIDATE(op->py_instance);
  }
#endif

  if (op->ptr) {
    op->properties = static_cast<IDProperty *>(op->ptr->data);
    MEM_delete(op->ptr);
  }

  if (op->properties) {
    IDP_FreeProperty(op->properties);
  }

  if (op->reports && (op->reports->flag & RPT_FREE)) {
    BKE_reports_free(op->reports);
    MEM_delete(op->reports);
  }

  if (op->macro.first()) {
    wmOperator *opm, *opmnext;
    for (opm = op->macro.first(); opm; opm = opmnext) {
      opmnext = opm->next;
      WM_operator_free(opm);
    }
  }

  MEM_delete(op);
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm.cc · L275—L308</summary>

<!-- original:9639c412eefe6c:source/blender/windowmanager/intern/wm.cc:275:308 -->

```cpp
void WM_operator_free(wmOperator *op)
{

#ifdef WITH_PYTHON
  if (op->py_instance) {
    /* Do this first in case there are any __del__ functions or similar that use properties. */
    BPY_DECREF_RNA_INVALIDATE(op->py_instance);
  }
#endif

  if (op->ptr) {
    op->properties = static_cast<IDProperty *>(op->ptr->data);
    MEM_delete(op->ptr);
  }

  if (op->properties) {
    IDP_FreeProperty(op->properties);
  }

  if (op->reports && (op->reports->flag & RPT_FREE)) {
    BKE_reports_free(op->reports);
    MEM_delete(op->reports);
  }

  if (op->macro.first()) {
    wmOperator *opm, *opmnext;
    for (opm = op->macro.first(); opm; opm = opmnext) {
      opmnext = opm->next;
      WM_operator_free(opm);
    }
  }

  MEM_delete(op);
}
```

</details>

**沿实际写入检查状态**

- `op->properties = static_cast<IDProperty *>(op->ptr->data);`
- `opmnext = opm->next;`

**继续追踪实现**

- `BPY_DECREF_RNA_INVALIDATE` → [blender::BPY_DECREF_RNA_INVALIDATE · L800](%E4%BE%9D%E8%B5%96-bpy_interface-b3b9e6.md#f-91a708534db859b3)。
- `MEM_delete` → [MEM_delete · L400](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-9049ffdd1682887c)。
- `IDP_FreeProperty` → [blender::IDP_FreeProperty · L1403](%E4%BE%9D%E8%B5%96-idprop-006c65.md#f-389134a630df1bed)。
- `BKE_reports_free` → [blender::BKE_reports_free · L106](%E4%BE%9D%E8%B5%96-report-f916fd.md#f-14b48393664f8c21)。
- `op->macro.first` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L299。
- `WM_operator_free` → [blender::WM_operator_free · L275](%E4%BE%9D%E8%B5%96-wm-ef447a.md#f-58bc17403b28c17b)。

<a id="f-7073e7762d0ea5c1"></a>

### `blender::WM_operator_free_all_after`

实现位置：[source/blender/windowmanager/intern/wm.cc](../../../../../source/blender/windowmanager/intern/wm.cc) · L310—L319。

接口参数：

- `wmWindowManager *wm`
- `wmOperator *op`

**教学注释版**

<!-- annotated:246d4d057afbd3 -->

```cpp
void WM_operator_free_all_after(wmWindowManager *wm, wmOperator *op)
{
  op = op->next;
  while (op != nullptr) {
    wmOperator *op_next = op->next;
    BLI_remlink(&wm->runtime->operators, op);
    WM_operator_free(op);
    op = op_next;
  }
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm.cc · L310—L319</summary>

<!-- original:246d4d057afbd3:source/blender/windowmanager/intern/wm.cc:310:319 -->

```cpp
void WM_operator_free_all_after(wmWindowManager *wm, wmOperator *op)
{
  op = op->next;
  while (op != nullptr) {
    wmOperator *op_next = op->next;
    BLI_remlink(&wm->runtime->operators, op);
    WM_operator_free(op);
    op = op_next;
  }
}
```

</details>

**沿实际写入检查状态**

- `op = op->next;`
- `op = op_next;`

**继续追踪实现**

- `BLI_remlink` → [blender::BLI_remlink · L138](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-listbase-2816d9.md#f-120d80f281ca4cb7)。
- `WM_operator_free` → [blender::WM_operator_free · L275](%E4%BE%9D%E8%B5%96-wm-ef447a.md#f-58bc17403b28c17b)。

<a id="f-76e8a84c267fa6ae"></a>

### `blender::wm_operator_register`

实现位置：[source/blender/windowmanager/intern/wm.cc](../../../../../source/blender/windowmanager/intern/wm.cc) · L348—L371。

接口参数：

- `bContext *C`
- `wmOperator *op`

**教学注释版**

<!-- annotated:74fa17986720e6 -->

```cpp
void wm_operator_register(bContext *C, wmOperator *op)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  int tot = 0;

  BLI_addtail(&wm->runtime->operators, op);

  /* Only count registered operators. */
  while (op) {
    wmOperator *op_prev = op->prev;
    if (op->type->flag & OPTYPE_REGISTER) {
      tot += 1;
    }
    if (tot > MAX_OP_REGISTERED) {
      BLI_remlink(&wm->runtime->operators, op);
      WM_operator_free(op);
    }
    op = op_prev;
  }

  /* So the console is redrawn. */
  WM_event_add_notifier(C, NC_SPACE | ND_SPACE_INFO_REPORT, nullptr);
  WM_event_add_notifier(C, NC_WM | ND_HISTORY, nullptr);
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm.cc · L348—L371</summary>

<!-- original:74fa17986720e6:source/blender/windowmanager/intern/wm.cc:348:371 -->

```cpp
void wm_operator_register(bContext *C, wmOperator *op)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  int tot = 0;

  BLI_addtail(&wm->runtime->operators, op);

  /* Only count registered operators. */
  while (op) {
    wmOperator *op_prev = op->prev;
    if (op->type->flag & OPTYPE_REGISTER) {
      tot += 1;
    }
    if (tot > MAX_OP_REGISTERED) {
      BLI_remlink(&wm->runtime->operators, op);
      WM_operator_free(op);
    }
    op = op_prev;
  }

  /* So the console is redrawn. */
  WM_event_add_notifier(C, NC_SPACE | ND_SPACE_INFO_REPORT, nullptr);
  WM_event_add_notifier(C, NC_WM | ND_HISTORY, nullptr);
}
```

</details>

**沿实际写入检查状态**

- `tot += 1;`
- `op = op_prev;`

**继续追踪实现**

- `CTX_wm_manager` → [blender::CTX_wm_manager · L928](%E4%BE%9D%E8%B5%96-context-a929d9.md#f-158f36db7379fbe8)。
- `BLI_addtail` → [blender::BLI_addtail · L118](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-listbase-2816d9.md#f-4fb027713fa3115b)。
- `BLI_remlink` → [blender::BLI_remlink · L138](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-listbase-2816d9.md#f-120d80f281ca4cb7)。
- `WM_operator_free` → [blender::WM_operator_free · L275](%E4%BE%9D%E8%B5%96-wm-ef447a.md#f-58bc17403b28c17b)。
- `WM_event_add_notifier` → [blender::WM_event_add_notifier · L396](%E4%BE%9D%E8%B5%96-wm_event_system-a0fa4f.md#f-a1b32e7f4a69b28f)。
