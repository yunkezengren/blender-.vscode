# 实现依赖专题：source/blender/draw/intern/draw_view_c.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::DRW_draw_region_info"]:::abstraction
  F1["blender::DRW_draw_gizmo_3d"]:::compute
  F2["blender::DRW_draw_gizmo_2d"]:::compute
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
  F["draw_view_c.cc实现"]:::compute
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

<a id="f-62f02cf481a549c8"></a>

### `blender::DRW_draw_region_info`

实现位置：[source/blender/draw/intern/draw_view_c.cc](../../../../../../../../source/blender/draw/intern/draw_view_c.cc) · L37—L42。

接口参数：

- `const bContext *C`
- `ARegion *region`

**教学注释版**

<!-- annotated:21e4f7953ccfaa -->

```cpp
void DRW_draw_region_info(const bContext *C, ARegion *region)
{
  GPU_debug_group_begin("RegionInfo");
  view3d_draw_region_info(C, region);
  GPU_debug_group_end();
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_view_c.cc · L37—L42</summary>

<!-- original:21e4f7953ccfaa:source/blender/draw/intern/draw_view_c.cc:37:42 -->

```cpp
void DRW_draw_region_info(const bContext *C, ARegion *region)
{
  GPU_debug_group_begin("RegionInfo");
  view3d_draw_region_info(C, region);
  GPU_debug_group_end();
}
```

</details>

**继续追踪实现**

- `GPU_debug_group_begin` → [blender::GPU_debug_group_begin · L23](../../gpu/intern/gpu_debug.cc.md#f-c74a16ba40e0e7a7)。
- `view3d_draw_region_info` → [blender::view3d_draw_region_info · L1469](../../editors/space_view3d/view3d_draw.cc.md#f-8bbeab40e85c6af8)。
- `GPU_debug_group_end` → [blender::GPU_debug_group_end · L34](../../gpu/intern/gpu_debug.cc.md#f-6d1ac356d118d5ac)。

<a id="f-fe3962b30af0fc56"></a>

### `blender::DRW_draw_gizmo_3d`

实现位置：[source/blender/draw/intern/draw_view_c.cc](../../../../../../../../source/blender/draw/intern/draw_view_c.cc) · L46—L52。

接口参数：

- `const bContext *C`
- `ARegion *region`

**教学注释版**

<!-- annotated:8b46c8edf0cfb0 -->

```cpp
void DRW_draw_gizmo_3d(const bContext *C, ARegion *region)
{
  /* draw depth culled gizmos - gizmos need to be updated *after* view matrix was set up */
  /* TODO: depth culling gizmos is not yet supported, just drawing _3D here, should
   * later become _IN_SCENE (and draw _3D separate) */
  WM_gizmomap_draw(region->runtime->gizmo_map, C, WM_GIZMOMAP_DRAWSTEP_3D);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_view_c.cc · L46—L52</summary>

<!-- original:8b46c8edf0cfb0:source/blender/draw/intern/draw_view_c.cc:46:52 -->

```cpp
void DRW_draw_gizmo_3d(const bContext *C, ARegion *region)
{
  /* draw depth culled gizmos - gizmos need to be updated *after* view matrix was set up */
  /* TODO: depth culling gizmos is not yet supported, just drawing _3D here, should
   * later become _IN_SCENE (and draw _3D separate) */
  WM_gizmomap_draw(region->runtime->gizmo_map, C, WM_GIZMOMAP_DRAWSTEP_3D);
}
```

</details>

**继续追踪实现**

- `WM_gizmomap_draw` → [blender::WM_gizmomap_draw · L507](../../windowmanager/gizmo/intern/wm_gizmo_map.cc.md#f-25216a0ce94632c3)。

<a id="f-93c11567cdc3f38c"></a>

### `blender::DRW_draw_gizmo_2d`

实现位置：[source/blender/draw/intern/draw_view_c.cc](../../../../../../../../source/blender/draw/intern/draw_view_c.cc) · L54—L58。

接口参数：

- `const bContext *C`
- `ARegion *region`

**教学注释版**

<!-- annotated:30e448d8896f2e -->

```cpp
void DRW_draw_gizmo_2d(const bContext *C, ARegion *region)
{
  WM_gizmomap_draw(region->runtime->gizmo_map, C, WM_GIZMOMAP_DRAWSTEP_2D);
  GPU_depth_mask(true);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_view_c.cc · L54—L58</summary>

<!-- original:30e448d8896f2e:source/blender/draw/intern/draw_view_c.cc:54:58 -->

```cpp
void DRW_draw_gizmo_2d(const bContext *C, ARegion *region)
{
  WM_gizmomap_draw(region->runtime->gizmo_map, C, WM_GIZMOMAP_DRAWSTEP_2D);
  GPU_depth_mask(true);
}
```

</details>

**继续追踪实现**

- `WM_gizmomap_draw` → [blender::WM_gizmomap_draw · L507](../../windowmanager/gizmo/intern/wm_gizmo_map.cc.md#f-25216a0ce94632c3)。
- `GPU_depth_mask` → [blender::GPU_depth_mask · L107](../../gpu/intern/gpu_state.cc.md#f-960a0181687885c0)。
