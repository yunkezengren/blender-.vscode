# 实现依赖专题：source/blender/windowmanager/intern/wm_gesture.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::WM_gesture_end"]:::abstraction
  F1["blender::WM_gestures_remove"]:::compute
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
  F["wm_gesture.cc实现"]:::compute
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

<a id="f-f855c36ac68e4a44"></a>

### `blender::WM_gesture_end`

实现位置：[source/blender/windowmanager/intern/wm_gesture.cc](../../../../../source/blender/windowmanager/intern/wm_gesture.cc) · L101—L108。

接口参数：

- `wmWindow *win`
- `wmGesture *gesture`

**教学注释版**

<!-- annotated:a7281971d63643 -->

```cpp
void WM_gesture_end(wmWindow *win, wmGesture *gesture)
{
  BLI_remlink(&win->runtime->gesture, gesture);
  // [讲解] MEM_delete_void：以原始存储释放约定调用当前后端。
  MEM_delete_void(gesture->customdata);
  WM_generic_user_data_free(&gesture->user_data);
  MEM_delete(gesture->edge_pan_data);
  MEM_delete(gesture);
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_gesture.cc · L101—L108</summary>

<!-- original:a7281971d63643:source/blender/windowmanager/intern/wm_gesture.cc:101:108 -->

```cpp
void WM_gesture_end(wmWindow *win, wmGesture *gesture)
{
  BLI_remlink(&win->runtime->gesture, gesture);
  MEM_delete_void(gesture->customdata);
  WM_generic_user_data_free(&gesture->user_data);
  MEM_delete(gesture->edge_pan_data);
  MEM_delete(gesture);
}
```

</details>

**继续追踪实现**

- `BLI_remlink` → [blender::BLI_remlink · L138](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-listbase-2816d9.md#f-120d80f281ca4cb7)。
- `MEM_delete_void` → [MEM_delete_void · L647](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-642896c7c62ff8b9)；[MEM_delete_void · L109](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-mallocn-afdcd4.md#f-9a07b26421f2bee6)。同名重载需按实参类型选择。
- `WM_generic_user_data_free` → [blender::WM_generic_user_data_free · L47](%E4%BE%9D%E8%B5%96-wm_utils-2d6444.md#f-3eb55123c40b8f45)。
- `MEM_delete` → [MEM_delete · L400](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-9049ffdd1682887c)。

<a id="f-5030de55e4326345"></a>

### `blender::WM_gestures_remove`

实现位置：[source/blender/windowmanager/intern/wm_gesture.cc](../../../../../source/blender/windowmanager/intern/wm_gesture.cc) · L117—L122。

接口参数：

- `wmWindow *win`

**教学注释版**

<!-- annotated:0d6e0e3198a8fc -->

```cpp
void WM_gestures_remove(wmWindow *win)
{
  while (win->runtime->gesture.first()) {
    WM_gesture_end(win, win->runtime->gesture.first());
  }
}
```

<details>
<summary>核对原始源码：source/blender/windowmanager/intern/wm_gesture.cc · L117—L122</summary>

<!-- original:0d6e0e3198a8fc:source/blender/windowmanager/intern/wm_gesture.cc:117:122 -->

```cpp
void WM_gestures_remove(wmWindow *win)
{
  while (win->runtime->gesture.first()) {
    WM_gesture_end(win, win->runtime->gesture.first());
  }
}
```

</details>

**继续追踪实现**

- `win->runtime->gesture.first` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L119。
- `WM_gesture_end` → [blender::WM_gesture_end · L101](%E4%BE%9D%E8%B5%96-wm_gesture-528e91.md#f-f855c36ac68e4a44)。
