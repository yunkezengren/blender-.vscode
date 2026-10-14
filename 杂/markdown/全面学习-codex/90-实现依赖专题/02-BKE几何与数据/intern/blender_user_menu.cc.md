# 实现依赖专题：source/blender/blenkernel/intern/blender_user_menu.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::BKE_blender_user_menu_find"]:::abstraction
  F1["blender::BKE_blender_user_menu_ensure"]:::compute
  F2["blender::BKE_blender_user_menu_item_add"]:::compute
  F3["blender::BKE_blender_user_menu_item_free"]:::compute
  F1 -->|"显式调用"| F0
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
  F["blender_user_menu.cc实现"]:::compute
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

<a id="f-f171528b1ea94f0e"></a>

### `blender::BKE_blender_user_menu_find`

实现位置：[source/blender/blenkernel/intern/blender_user_menu.cc](../../../../../../../source/blender/blenkernel/intern/blender_user_menu.cc) · L29—L39。

接口参数：

- `ListBaseT<bUserMenu> *lb`
- `char space_type`
- `const char *context`

**教学注释版**

<!-- annotated:cf7adbb093f8b1 -->

```cpp
bUserMenu *BKE_blender_user_menu_find(ListBaseT<bUserMenu> *lb,
                                      char space_type,
                                      const char *context)
{
  for (bUserMenu &um : *lb) {
    if ((space_type == um.space_type) && STREQ(context, um.context)) {
      return &um;
    }
  }
  return nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/blender_user_menu.cc · L29—L39</summary>

<!-- original:cf7adbb093f8b1:source/blender/blenkernel/intern/blender_user_menu.cc:29:39 -->

```cpp
bUserMenu *BKE_blender_user_menu_find(ListBaseT<bUserMenu> *lb,
                                      char space_type,
                                      const char *context)
{
  for (bUserMenu &um : *lb) {
    if ((space_type == um.space_type) && STREQ(context, um.context)) {
      return &um;
    }
  }
  return nullptr;
}
```

</details>

**结果出口**

- `return &um;`
- `return nullptr;`

**继续追踪实现**

- `STREQ` → [STREQ · L112](../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-9549fb6aafd2)；[STREQ · L451](../../01-BLI基础库/BLI_utildefines.hh.md#m-c7b745bcfad2)；[STREQ · L55](../../07-Intern运行时与平台/clog/clog.cc.md#m-96e78f386894)。宏定义由构建条件选择。

<a id="f-7a070c7cc5971cf4"></a>

### `blender::BKE_blender_user_menu_ensure`

实现位置：[source/blender/blenkernel/intern/blender_user_menu.cc](../../../../../../../source/blender/blenkernel/intern/blender_user_menu.cc) · L41—L53。

接口参数：

- `ListBaseT<bUserMenu> *lb`
- `char space_type`
- `const char *context`

**教学注释版**

<!-- annotated:067ea58515df1a -->

```cpp
bUserMenu *BKE_blender_user_menu_ensure(ListBaseT<bUserMenu> *lb,
                                        char space_type,
                                        const char *context)
{
  bUserMenu *um = BKE_blender_user_menu_find(lb, space_type, context);
  if (um == nullptr) {
    um = MEM_new<bUserMenu>(__func__);
    um->space_type = space_type;
    STRNCPY(um->context, context);
    BLI_addhead(lb, um);
  }
  return um;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/blender_user_menu.cc · L41—L53</summary>

<!-- original:067ea58515df1a:source/blender/blenkernel/intern/blender_user_menu.cc:41:53 -->

```cpp
bUserMenu *BKE_blender_user_menu_ensure(ListBaseT<bUserMenu> *lb,
                                        char space_type,
                                        const char *context)
{
  bUserMenu *um = BKE_blender_user_menu_find(lb, space_type, context);
  if (um == nullptr) {
    um = MEM_new<bUserMenu>(__func__);
    um->space_type = space_type;
    STRNCPY(um->context, context);
    BLI_addhead(lb, um);
  }
  return um;
}
```

</details>

**沿实际写入检查状态**

- `um = MEM_new<bUserMenu>(__func__);`
- `um->space_type = space_type;`

**结果出口**

- `return um;`

**继续追踪实现**

- `BKE_blender_user_menu_find` → [blender::BKE_blender_user_menu_find · L29](blender_user_menu.cc.md#f-f171528b1ea94f0e)。
- `MEM_new<bUserMenu>` → [MEM_new · L351](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-115f9b6784f89912)。
- `STRNCPY` → [blender::STRNCPY · L690](../../01-BLI基础库/BLI_string.hh.md#f-6b2d861724026be6)。
- `BLI_addhead` → [blender::BLI_addhead · L98](../../01-BLI基础库/intern/listbase.cc.md#f-fed3ad483fcdfeb9)。

<a id="f-1ac7bc59f9edc1ac"></a>

### `blender::BKE_blender_user_menu_item_add`

实现位置：[source/blender/blenkernel/intern/blender_user_menu.cc](../../../../../../../source/blender/blenkernel/intern/blender_user_menu.cc) · L61—L85。

接口参数：

- `ListBaseT<bUserMenuItem> *lb`
- `eUserMenu_Type type`

**教学注释版**

<!-- annotated:4d7d5ace82da04 -->

```cpp
bUserMenuItem *BKE_blender_user_menu_item_add(ListBaseT<bUserMenuItem> *lb, eUserMenu_Type type)
{
  bUserMenuItem *umi;

  if (type == USER_MENU_TYPE_SEP) {
    umi = MEM_new<bUserMenuItem>(__func__);
  }
  else if (type == USER_MENU_TYPE_OPERATOR) {
    umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Op>(__func__));
  }
  else if (type == USER_MENU_TYPE_MENU) {
    umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Menu>(__func__));
  }
  else if (type == USER_MENU_TYPE_PROP) {
    umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Prop>(__func__));
  }
  else {
    umi = MEM_new<bUserMenuItem>(__func__);
    BLI_assert(0);
  }

  umi->type = type;
  BLI_addtail(lb, umi);
  return umi;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/blender_user_menu.cc · L61—L85</summary>

<!-- original:4d7d5ace82da04:source/blender/blenkernel/intern/blender_user_menu.cc:61:85 -->

```cpp
bUserMenuItem *BKE_blender_user_menu_item_add(ListBaseT<bUserMenuItem> *lb, eUserMenu_Type type)
{
  bUserMenuItem *umi;

  if (type == USER_MENU_TYPE_SEP) {
    umi = MEM_new<bUserMenuItem>(__func__);
  }
  else if (type == USER_MENU_TYPE_OPERATOR) {
    umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Op>(__func__));
  }
  else if (type == USER_MENU_TYPE_MENU) {
    umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Menu>(__func__));
  }
  else if (type == USER_MENU_TYPE_PROP) {
    umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Prop>(__func__));
  }
  else {
    umi = MEM_new<bUserMenuItem>(__func__);
    BLI_assert(0);
  }

  umi->type = type;
  BLI_addtail(lb, umi);
  return umi;
}
```

</details>

**沿实际写入检查状态**

- `umi = MEM_new<bUserMenuItem>(__func__);`
- `umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Op>(__func__));`
- `umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Menu>(__func__));`
- `umi = reinterpret_cast<bUserMenuItem *>(MEM_new<bUserMenuItem_Prop>(__func__));`
- `umi->type = type;`

**结果出口**

- `return umi;`

**继续追踪实现**

- `MEM_new<bUserMenuItem>` → [MEM_new · L351](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-115f9b6784f89912)。
- `MEM_new<bUserMenuItem_Op>` → [MEM_new · L351](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-115f9b6784f89912)。
- `MEM_new<bUserMenuItem_Menu>` → [MEM_new · L351](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-115f9b6784f89912)。
- `MEM_new<bUserMenuItem_Prop>` → [MEM_new · L351](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-115f9b6784f89912)。
- `BLI_assert` → [BLI_assert · L48](../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `BLI_addtail` → [blender::BLI_addtail · L118](../../01-BLI基础库/intern/listbase.cc.md#f-4fb027713fa3115b)。

<a id="f-31a0329012ed9401"></a>

### `blender::BKE_blender_user_menu_item_free`

实现位置：[source/blender/blenkernel/intern/blender_user_menu.cc](../../../../../../../source/blender/blenkernel/intern/blender_user_menu.cc) · L87—L96。

接口参数：

- `bUserMenuItem *umi`

**教学注释版**

<!-- annotated:5742798dcb010c -->

```cpp
void BKE_blender_user_menu_item_free(bUserMenuItem *umi)
{
  if (umi->type == USER_MENU_TYPE_OPERATOR) {
    bUserMenuItem_Op *umi_op = reinterpret_cast<bUserMenuItem_Op *>(umi);
    if (umi_op->prop) {
      IDP_FreeProperty(umi_op->prop);
    }
  }
  MEM_delete(umi);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/blender_user_menu.cc · L87—L96</summary>

<!-- original:5742798dcb010c:source/blender/blenkernel/intern/blender_user_menu.cc:87:96 -->

```cpp
void BKE_blender_user_menu_item_free(bUserMenuItem *umi)
{
  if (umi->type == USER_MENU_TYPE_OPERATOR) {
    bUserMenuItem_Op *umi_op = reinterpret_cast<bUserMenuItem_Op *>(umi);
    if (umi_op->prop) {
      IDP_FreeProperty(umi_op->prop);
    }
  }
  MEM_delete(umi);
}
```

</details>

**继续追踪实现**

- `IDP_FreeProperty` → [blender::IDP_FreeProperty · L1403](idprop.cc.md#f-389134a630df1bed)。
- `MEM_delete` → [MEM_delete · L400](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
