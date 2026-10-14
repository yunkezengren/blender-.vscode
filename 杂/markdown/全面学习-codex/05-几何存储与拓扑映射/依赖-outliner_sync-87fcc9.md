# 实现依赖专题：source/blender/editors/space_outliner/outliner_sync.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::ED_outliner_select_sync_from_object_tag"]:::abstraction
  F1["blender::ED_outliner_select_sync_from_edit_bone_tag"]:::compute
  F2["blender::ED_outliner_select_sync_from_pose_bone_tag"]:::compute
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
  F["outliner_sync.cc实现"]:::compute
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

<a id="f-5825dbd6aa822a45"></a>

### `blender::ED_outliner_select_sync_from_object_tag`

实现位置：[source/blender/editors/space_outliner/outliner_sync.cc](../../../../../source/blender/editors/space_outliner/outliner_sync.cc) · L43—L47。

接口参数：

- `bContext *C`

**教学注释版**

<!-- annotated:84d3e47028a032 -->

```cpp
void ED_outliner_select_sync_from_object_tag(bContext *C)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_OBJECT;
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_outliner/outliner_sync.cc · L43—L47</summary>

<!-- original:84d3e47028a032:source/blender/editors/space_outliner/outliner_sync.cc:43:47 -->

```cpp
void ED_outliner_select_sync_from_object_tag(bContext *C)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_OBJECT;
}
```

</details>

**沿实际写入检查状态**

- `wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_OBJECT;`

**继续追踪实现**

- `CTX_wm_manager` → [blender::CTX_wm_manager · L928](%E4%BE%9D%E8%B5%96-context-a929d9.md#f-158f36db7379fbe8)。

<a id="f-e15b16f7f79d3b20"></a>

### `blender::ED_outliner_select_sync_from_edit_bone_tag`

实现位置：[source/blender/editors/space_outliner/outliner_sync.cc](../../../../../source/blender/editors/space_outliner/outliner_sync.cc) · L49—L53。

接口参数：

- `bContext *C`

**教学注释版**

<!-- annotated:b6b06dc27d16be -->

```cpp
void ED_outliner_select_sync_from_edit_bone_tag(bContext *C)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_EDIT_BONE;
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_outliner/outliner_sync.cc · L49—L53</summary>

<!-- original:b6b06dc27d16be:source/blender/editors/space_outliner/outliner_sync.cc:49:53 -->

```cpp
void ED_outliner_select_sync_from_edit_bone_tag(bContext *C)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_EDIT_BONE;
}
```

</details>

**沿实际写入检查状态**

- `wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_EDIT_BONE;`

**继续追踪实现**

- `CTX_wm_manager` → [blender::CTX_wm_manager · L928](%E4%BE%9D%E8%B5%96-context-a929d9.md#f-158f36db7379fbe8)。

<a id="f-1b9216da11a76328"></a>

### `blender::ED_outliner_select_sync_from_pose_bone_tag`

实现位置：[source/blender/editors/space_outliner/outliner_sync.cc](../../../../../source/blender/editors/space_outliner/outliner_sync.cc) · L55—L59。

接口参数：

- `bContext *C`

**教学注释版**

<!-- annotated:c692c0496df295 -->

```cpp
void ED_outliner_select_sync_from_pose_bone_tag(bContext *C)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_POSE_BONE;
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_outliner/outliner_sync.cc · L55—L59</summary>

<!-- original:c692c0496df295:source/blender/editors/space_outliner/outliner_sync.cc:55:59 -->

```cpp
void ED_outliner_select_sync_from_pose_bone_tag(bContext *C)
{
  wmWindowManager *wm = CTX_wm_manager(C);
  wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_POSE_BONE;
}
```

</details>

**沿实际写入检查状态**

- `wm->outliner_sync_select_dirty |= WM_OUTLINER_SYNC_SELECT_FROM_POSE_BONE;`

**继续追踪实现**

- `CTX_wm_manager` → [blender::CTX_wm_manager · L928](%E4%BE%9D%E8%B5%96-context-a929d9.md#f-158f36db7379fbe8)。
