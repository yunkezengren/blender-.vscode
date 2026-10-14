# 实现依赖专题：source/blender/nodes/intern/sync_sockets.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::nodes::node_can_sync_cache_clear"]:::abstraction
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
  F["sync_sockets.cc实现"]:::compute
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

<a id="f-eac6490a6eaec1f9"></a>

### `blender::nodes::node_can_sync_cache_clear`

实现位置：[source/blender/nodes/intern/sync_sockets.cc](../../../../../../../source/blender/nodes/intern/sync_sockets.cc) · L799—L814。

接口参数：

- `Main &bmain`

**教学注释版**

<!-- annotated:e2c14a48af9f88 -->

```cpp
void node_can_sync_cache_clear(Main &bmain)
{
  if (wmWindowManager *wm = bmain.wm.first()) {
    for (wmWindow &window : wm->windows) {
      bScreen *screen = BKE_workspace_active_screen_get(window.workspace_hook);
      for (ScrArea &area : screen->areabase) {
        SpaceLink *sl = area.spacedata.first_as<SpaceLink>();
        if (sl->spacetype == SPACE_NODE) {
          SpaceNode *snode = reinterpret_cast<SpaceNode *>(sl);
          Map<int, bool> &cache = ed::space_node::node_can_sync_cache_get(*snode);
          // [讲解] cache.clear：移除全部活项，并按接口决定是否归还存储。
          cache.clear();
        }
      }
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/nodes/intern/sync_sockets.cc · L799—L814</summary>

<!-- original:e2c14a48af9f88:source/blender/nodes/intern/sync_sockets.cc:799:814 -->

```cpp
void node_can_sync_cache_clear(Main &bmain)
{
  if (wmWindowManager *wm = bmain.wm.first()) {
    for (wmWindow &window : wm->windows) {
      bScreen *screen = BKE_workspace_active_screen_get(window.workspace_hook);
      for (ScrArea &area : screen->areabase) {
        SpaceLink *sl = area.spacedata.first_as<SpaceLink>();
        if (sl->spacetype == SPACE_NODE) {
          SpaceNode *snode = reinterpret_cast<SpaceNode *>(sl);
          Map<int, bool> &cache = ed::space_node::node_can_sync_cache_get(*snode);
          cache.clear();
        }
      }
    }
  }
}
```

</details>

**继续追踪实现**

- `bmain.wm.first` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L801。
- `BKE_workspace_active_screen_get` → [blender::BKE_workspace_active_screen_get · L684](../../02-BKE几何与数据/intern/workspace.cc.md#f-514f5bcbd6245e5d)。
- `area.spacedata.first_as<SpaceLink>` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L805。
- `ed::space_node::node_can_sync_cache_get` → [blender::ed::space_node::node_can_sync_cache_get · L116](../../08-其他Blender模块/editors/space_node/node_sync_sockets.cc.md#f-91fc0bf00977e5a7)。
- `cache.clear` → [blender::Map::clear · L1038](../../../02-哈希表与关联数据结构/06-删除墓碑与值销毁.md#f-c58ca43ed9dafe4a)。
