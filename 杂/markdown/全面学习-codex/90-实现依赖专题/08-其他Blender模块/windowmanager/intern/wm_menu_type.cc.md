# 实现依赖专题：source/blender/windowmanager/intern/wm_menu_type.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::get_menu_type_map"]:::abstraction
  F1["blender::WM_menutype_find"]:::compute
  F2["blender::WM_menutype_poll"]:::compute
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
  F["wm_menu_type.cc实现"]:::compute
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

<a id="f-0904ba93b7caca0b"></a>

### `blender::get_menu_type_map`

实现位置：[source/blender/windowmanager/intern/wm_menu_type.cc](../../../../../../../../source/blender/windowmanager/intern/wm_menu_type.cc) · L29—L39。

**教学注释版**

<!-- annotated:2003d7f98562b3 -->

```cpp
static auto &get_menu_type_map()
{
  struct IDNameGetter {
    StringRef operator()(const MenuType *value) const
    {
      return StringRef(value->idname);
    }
  };
  static CustomIDVectorSet<MenuType *, IDNameGetter> map;
  return map;
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_menu_type.cc · L29—L39</summary>

<!-- original:2003d7f98562b3:source/blender/windowmanager/intern/wm_menu_type.cc:29:39 -->

```cpp
static auto &get_menu_type_map()
{
  struct IDNameGetter {
    StringRef operator()(const MenuType *value) const
    {
      return StringRef(value->idname);
    }
  };
  static CustomIDVectorSet<MenuType *, IDNameGetter> map;
  return map;
}
```

</details>

**结果出口**

- `return StringRef(value->idname);`
- `return map;`

**继续追踪实现**

- `StringRef` → [blender::StringRef::StringRef · L555](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-f6aca324a36faa7e)；[blender::StringRef::StringRef · L560](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-ab9714781ca51bac)；[blender::StringRef::StringRef · L565](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-95f0b483bbdd7739)；[blender::StringRef::StringRef · L570](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-808d05699cb33334)；[blender::StringRef::StringRef · L631](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-37788e5f3fa3b736)；[blender::StringRef::StringRef · L641](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-11abd0510fb6b926)；[blender::StringRef::StringRef · L646](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-8437dbd8a582eefd)；[blender::StringRef::StringRef · L651](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-70bcb338de0db978)。同名重载需按实参类型选择。

<a id="f-f6b7065ddb0df160"></a>

### `blender::WM_menutype_find`

实现位置：[source/blender/windowmanager/intern/wm_menu_type.cc](../../../../../../../../source/blender/windowmanager/intern/wm_menu_type.cc) · L41—L54。

接口参数：

- `const StringRef idname`
- `bool quiet`

**教学注释版**

<!-- annotated:bdb72248d929d8 -->

```cpp
MenuType *WM_menutype_find(const StringRef idname, bool quiet)
{
  if (!idname.is_empty()) {
    if (MenuType *const *mt = get_menu_type_map().lookup_key_ptr_as(idname)) {
      return *mt;
    }
  }

  if (!quiet) {
    printf("search for unknown menutype %s\n", std::string(idname).c_str());
  }

  return nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_menu_type.cc · L41—L54</summary>

<!-- original:bdb72248d929d8:source/blender/windowmanager/intern/wm_menu_type.cc:41:54 -->

```cpp
MenuType *WM_menutype_find(const StringRef idname, bool quiet)
{
  if (!idname.is_empty()) {
    if (MenuType *const *mt = get_menu_type_map().lookup_key_ptr_as(idname)) {
      return *mt;
    }
  }

  if (!quiet) {
    printf("search for unknown menutype %s\n", std::string(idname).c_str());
  }

  return nullptr;
}
```

</details>

**结果出口**

- `return *mt;`
- `return nullptr;`

**继续追踪实现**

- `idname.is_empty` → [blender::Bounds<T>::is_empty · L533](../../../../12-空间数据结构与几何算法/07-Bounds与BVH对比.md#f-55ac376b3d0a0944)；[blender::GVArrayCommon::is_empty · L767](../../../../04-虚拟数组与索引选择/05-GVArray运行时类型.md#f-c1da602ffc5555f9)；[blender::StringRefBase::is_empty · L201](../../../../01-基础容器与现代CPP/15-StringRef字符串视图.md#f-9f6c3d2da1cb1796)；[blender::KDTreeNew<T>::is_empty · L498](../../../../12-空间数据结构与几何算法/05-K近邻与范围查询.md#f-67f0ff91cf00b00b)。同名重载需按实参类型选择。
- `get_menu_type_map().lookup_key_ptr_as` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L44。
- `get_menu_type_map` → [blender::get_menu_type_map · L29](wm_menu_type.cc.md#f-0904ba93b7caca0b)。
- `printf` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `std::string(idname).c_str` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `std::string` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。

<a id="f-7dbb17ec9d5b037f"></a>

### `blender::WM_menutype_poll`

实现位置：[source/blender/windowmanager/intern/wm_menu_type.cc](../../../../../../../../source/blender/windowmanager/intern/wm_menu_type.cc) · L94—L108。

接口参数：

- `bContext *C`
- `MenuType *mt`

**教学注释版**

<!-- annotated:d846f1d54c431d -->

```cpp
bool WM_menutype_poll(bContext *C, MenuType *mt)
{
  /* If we're tagged, only use compatible. */
  if (mt->owner_id[0] != '\0') {
    const WorkSpace *workspace = CTX_wm_workspace(C);
    if (BKE_workspace_owner_id_check(workspace, mt->owner_id) == false) {
      return false;
    }
  }

  if (mt->poll != nullptr) {
    return mt->poll(C, mt);
  }
  return true;
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_menu_type.cc · L94—L108</summary>

<!-- original:d846f1d54c431d:source/blender/windowmanager/intern/wm_menu_type.cc:94:108 -->

```cpp
bool WM_menutype_poll(bContext *C, MenuType *mt)
{
  /* If we're tagged, only use compatible. */
  if (mt->owner_id[0] != '\0') {
    const WorkSpace *workspace = CTX_wm_workspace(C);
    if (BKE_workspace_owner_id_check(workspace, mt->owner_id) == false) {
      return false;
    }
  }

  if (mt->poll != nullptr) {
    return mt->poll(C, mt);
  }
  return true;
}
```

</details>

**结果出口**

- `return false;`
- `return mt->poll(C, mt);`
- `return true;`

**继续追踪实现**

- `CTX_wm_workspace` → [blender::CTX_wm_workspace · L943](../../../02-BKE几何与数据/intern/context.cc.md#f-b74037d7a9d4ee39)。
- `BKE_workspace_owner_id_check` → [blender::BKE_workspace_owner_id_check · L607](../../../02-BKE几何与数据/intern/workspace.cc.md#f-c029513fe561a031)。
- `mt->poll` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：由接收对象具体类型或运行时策略提供实现。调用位置L105。
