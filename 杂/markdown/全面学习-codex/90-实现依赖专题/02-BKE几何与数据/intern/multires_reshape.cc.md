# 实现依赖专题：source/blender/blenkernel/intern/multires_reshape.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::multiresModifier_reshape_store_original_grids_for_smoothing"]:::abstraction
  F1["blender::multiresModifier_reshapeFromCCG"]:::compute
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
  F["multires_reshape.cc实现"]:::compute
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

<a id="f-4e51549447a8299b"></a>

### `blender::multiresModifier_reshape_store_original_grids_for_smoothing`

实现位置：[source/blender/blenkernel/intern/multires_reshape.cc](../../../../../../../source/blender/blenkernel/intern/multires_reshape.cc) · L31—L38。

接口参数：

- `MultiresReshapeContext *reshape_context`

**教学注释版**

<!-- annotated:4ddd052f798173 -->

```cpp
static void multiresModifier_reshape_store_original_grids_for_smoothing(
    MultiresReshapeContext *reshape_context)
{
  if (reshape_context->top.level == reshape_context->reshape.level) {
    return;
  }
  multires_reshape_store_original_grids(reshape_context);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/multires_reshape.cc · L31—L38</summary>

<!-- original:4ddd052f798173:source/blender/blenkernel/intern/multires_reshape.cc:31:38 -->

```cpp
static void multiresModifier_reshape_store_original_grids_for_smoothing(
    MultiresReshapeContext *reshape_context)
{
  if (reshape_context->top.level == reshape_context->reshape.level) {
    return;
  }
  multires_reshape_store_original_grids(reshape_context);
}
```

</details>

**继续追踪实现**

- `multires_reshape_store_original_grids` → [blender::multires_reshape_store_original_grids · L626](multires_reshape_util.cc.md#f-2dd543f3f5744e6a)。

<a id="f-9583ebfec42c6493"></a>

### `blender::multiresModifier_reshapeFromCCG`

实现位置：[source/blender/blenkernel/intern/multires_reshape.cc](../../../../../../../source/blender/blenkernel/intern/multires_reshape.cc) · L129—L150。

接口参数：

- `const int tot_level`
- `Mesh *coarse_mesh`
- `SubdivCCG *subdiv_ccg`

**教学注释版**

<!-- annotated:0169457375b72b -->

```cpp
bool multiresModifier_reshapeFromCCG(const int tot_level, Mesh *coarse_mesh, SubdivCCG *subdiv_ccg)
{
  MultiresReshapeContext reshape_context;
  if (!multires_reshape_context_create_from_ccg(
          &reshape_context, subdiv_ccg, coarse_mesh, tot_level))
  {
    return false;
  }

  multires_ensure_external_read(coarse_mesh, reshape_context.top.level);

  multiresModifier_reshape_store_original_grids_for_smoothing(&reshape_context);
  multires_reshape_ensure_grids(coarse_mesh, reshape_context.top.level);
  if (!multires_reshape_assign_final_coords_from_ccg(&reshape_context, subdiv_ccg)) {
    multires_reshape_context_free(&reshape_context);
    return false;
  }
  multires_reshape_smooth_object_grids_with_details(&reshape_context);
  multires_reshape_object_grids_to_tangent_displacement(&reshape_context);
  multires_reshape_context_free(&reshape_context);
  return true;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/multires_reshape.cc · L129—L150</summary>

<!-- original:0169457375b72b:source/blender/blenkernel/intern/multires_reshape.cc:129:150 -->

```cpp
bool multiresModifier_reshapeFromCCG(const int tot_level, Mesh *coarse_mesh, SubdivCCG *subdiv_ccg)
{
  MultiresReshapeContext reshape_context;
  if (!multires_reshape_context_create_from_ccg(
          &reshape_context, subdiv_ccg, coarse_mesh, tot_level))
  {
    return false;
  }

  multires_ensure_external_read(coarse_mesh, reshape_context.top.level);

  multiresModifier_reshape_store_original_grids_for_smoothing(&reshape_context);
  multires_reshape_ensure_grids(coarse_mesh, reshape_context.top.level);
  if (!multires_reshape_assign_final_coords_from_ccg(&reshape_context, subdiv_ccg)) {
    multires_reshape_context_free(&reshape_context);
    return false;
  }
  multires_reshape_smooth_object_grids_with_details(&reshape_context);
  multires_reshape_object_grids_to_tangent_displacement(&reshape_context);
  multires_reshape_context_free(&reshape_context);
  return true;
}
```

</details>

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `multires_reshape_context_create_from_ccg` → [blender::multires_reshape_context_create_from_ccg · L235](multires_reshape_util.cc.md#f-1fb787766b7b0c82)。
- `multires_ensure_external_read` → [blender::multires_ensure_external_read · L766](multires.cc.md#f-d727a1334b17c264)。
- `multiresModifier_reshape_store_original_grids_for_smoothing` → [blender::multiresModifier_reshape_store_original_grids_for_smoothing · L31](multires_reshape.cc.md#f-4e51549447a8299b)。
- `multires_reshape_ensure_grids` → [blender::multires_reshape_ensure_grids · L614](multires_reshape_util.cc.md#f-7e328656b61675cc)。
- `multires_reshape_assign_final_coords_from_ccg` → [blender::multires_reshape_assign_final_coords_from_ccg · L20](multires_reshape_ccg.cc.md#f-00c38e623f7ae299)。
- `multires_reshape_context_free` → [blender::multires_reshape_context_free · L347](multires_reshape_util.cc.md#f-1845e67e2c78f6b9)。
- `multires_reshape_smooth_object_grids_with_details` → [blender::multires_reshape_smooth_object_grids_with_details · L1216](multires_reshape_smooth.cc.md#f-359c9d63e65d630e)。
- `multires_reshape_object_grids_to_tangent_displacement` → [blender::multires_reshape_object_grids_to_tangent_displacement · L750](multires_reshape_util.cc.md#f-fd93b78ce31d0da9)。
