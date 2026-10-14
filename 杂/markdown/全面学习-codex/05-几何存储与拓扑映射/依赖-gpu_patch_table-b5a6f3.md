# 实现依赖专题：intern/opensubdiv/internal/evaluator/gpu_patch_table.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::opensubdiv::GPUPatchTable::Create"]:::abstraction
  F1["blender::opensubdiv::GPUPatchTable::allocate"]:::compute
  F0 -->|"显式调用"| F1
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
  F["gpu_patch_table.cc实现"]:::compute
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

<a id="f-7577968ff4e0de67"></a>

### `blender::opensubdiv::GPUPatchTable::Create`

实现位置：[intern/opensubdiv/internal/evaluator/gpu_patch_table.cc](../../../../../intern/opensubdiv/internal/evaluator/gpu_patch_table.cc) · L14—L22。

接口参数：

- `PatchTable const *far_patch_table`
- `void *`

**教学注释版**

<!-- annotated:ae84fc504b57ed -->

```cpp
GPUPatchTable *GPUPatchTable::Create(PatchTable const *far_patch_table, void * /*deviceContext*/)
{
  GPUPatchTable *instance = new GPUPatchTable();
  if (instance->allocate(far_patch_table)) {
    return instance;
  }
  delete instance;
  return nullptr;
}
```

<details>
<summary>核对原始源码：intern/opensubdiv/internal/evaluator/gpu_patch_table.cc · L14—L22</summary>

<!-- original:ae84fc504b57ed:intern/opensubdiv/internal/evaluator/gpu_patch_table.cc:14:22 -->

```cpp
GPUPatchTable *GPUPatchTable::Create(PatchTable const *far_patch_table, void * /*deviceContext*/)
{
  GPUPatchTable *instance = new GPUPatchTable();
  if (instance->allocate(far_patch_table)) {
    return instance;
  }
  delete instance;
  return nullptr;
}
```

</details>

**结果出口**

- `return instance;`
- `return nullptr;`

**继续追踪实现**

- `instance->allocate` → [blender::opensubdiv::GPUPatchTable::allocate · L50](%E4%BE%9D%E8%B5%96-gpu_patch_table-b5a6f3.md#f-9a8016c62fad9b09)。

<a id="f-9a8016c62fad9b09"></a>

### `blender::opensubdiv::GPUPatchTable::allocate`

实现位置：[intern/opensubdiv/internal/evaluator/gpu_patch_table.cc](../../../../../intern/opensubdiv/internal/evaluator/gpu_patch_table.cc) · L50—L111。

接口参数：

- `PatchTable const *far_patch_table`

**教学注释版**

<!-- annotated:e45975b9f14555 -->

```cpp
bool GPUPatchTable::allocate(PatchTable const *far_patch_table)
{
  CpuPatchTable patch_table(far_patch_table);

  /* Patch array */
  size_t num_patch_arrays = patch_table.GetNumPatchArrays();
  _patchArrays.assign(patch_table.GetPatchArrayBuffer(),
                      patch_table.GetPatchArrayBuffer() + num_patch_arrays);

  /* Patch index buffer */
  const size_t index_size = patch_table.GetPatchIndexSize();
  _patchIndexBuffer = GPU_storagebuf_create_ex(
      index_size * sizeof(int32_t),
      static_cast<const void *>(patch_table.GetPatchIndexBuffer()),
      GPU_USAGE_STATIC,
      "osd_patch_index");

  /* Patch param buffer */
  const size_t patch_param_size = patch_table.GetPatchParamSize();
  _patchParamBuffer = GPU_storagebuf_create_ex(patch_param_size * sizeof(PatchParam),
                                               patch_table.GetPatchParamBuffer(),
                                               GPU_USAGE_STATIC,
                                               "osd_patch_param");

  /* Varying patch array */
  _varyingPatchArrays.assign(patch_table.GetVaryingPatchArrayBuffer(),
                             patch_table.GetVaryingPatchArrayBuffer() + num_patch_arrays);

  /* Varying index buffer */
  _varyingIndexBuffer = GPU_storagebuf_create_ex(patch_table.GetVaryingPatchIndexSize() *
                                                     sizeof(uint32_t),
                                                 patch_table.GetVaryingPatchIndexBuffer(),
                                                 GPU_USAGE_STATIC,
                                                 "osd_varying_index");

  /* Face varying */
  const int num_face_varying_channels = patch_table.GetNumFVarChannels();
  _fvarPatchArrays.resize(num_face_varying_channels);
  _fvarIndexBuffers.resize(num_face_varying_channels);
  _fvarParamBuffers.resize(num_face_varying_channels);
  for (int index = 0; index < num_face_varying_channels; index++) {
    /* Face varying patch arrays */
    _fvarPatchArrays[index].assign(patch_table.GetFVarPatchArrayBuffer(),
                                   patch_table.GetFVarPatchArrayBuffer() + num_patch_arrays);

    /* Face varying patch index buffer */
    _fvarIndexBuffers[index] = GPU_storagebuf_create_ex(patch_table.GetFVarPatchIndexSize(index) *
                                                            sizeof(int32_t),
                                                        patch_table.GetFVarPatchIndexBuffer(index),
                                                        GPU_USAGE_STATIC,
                                                        "osd_face_varying_index");

    /* Face varying patch param buffer */
    _fvarParamBuffers[index] = GPU_storagebuf_create_ex(patch_table.GetFVarPatchParamSize(index) *
                                                            sizeof(PatchParam),
                                                        patch_table.GetFVarPatchParamBuffer(index),
                                                        GPU_USAGE_STATIC,
                                                        "osd_face_varying_params");
  }

  return true;
}
```

<details>
<summary>核对原始源码：intern/opensubdiv/internal/evaluator/gpu_patch_table.cc · L50—L111</summary>

<!-- original:e45975b9f14555:intern/opensubdiv/internal/evaluator/gpu_patch_table.cc:50:111 -->

```cpp
bool GPUPatchTable::allocate(PatchTable const *far_patch_table)
{
  CpuPatchTable patch_table(far_patch_table);

  /* Patch array */
  size_t num_patch_arrays = patch_table.GetNumPatchArrays();
  _patchArrays.assign(patch_table.GetPatchArrayBuffer(),
                      patch_table.GetPatchArrayBuffer() + num_patch_arrays);

  /* Patch index buffer */
  const size_t index_size = patch_table.GetPatchIndexSize();
  _patchIndexBuffer = GPU_storagebuf_create_ex(
      index_size * sizeof(int32_t),
      static_cast<const void *>(patch_table.GetPatchIndexBuffer()),
      GPU_USAGE_STATIC,
      "osd_patch_index");

  /* Patch param buffer */
  const size_t patch_param_size = patch_table.GetPatchParamSize();
  _patchParamBuffer = GPU_storagebuf_create_ex(patch_param_size * sizeof(PatchParam),
                                               patch_table.GetPatchParamBuffer(),
                                               GPU_USAGE_STATIC,
                                               "osd_patch_param");

  /* Varying patch array */
  _varyingPatchArrays.assign(patch_table.GetVaryingPatchArrayBuffer(),
                             patch_table.GetVaryingPatchArrayBuffer() + num_patch_arrays);

  /* Varying index buffer */
  _varyingIndexBuffer = GPU_storagebuf_create_ex(patch_table.GetVaryingPatchIndexSize() *
                                                     sizeof(uint32_t),
                                                 patch_table.GetVaryingPatchIndexBuffer(),
                                                 GPU_USAGE_STATIC,
                                                 "osd_varying_index");

  /* Face varying */
  const int num_face_varying_channels = patch_table.GetNumFVarChannels();
  _fvarPatchArrays.resize(num_face_varying_channels);
  _fvarIndexBuffers.resize(num_face_varying_channels);
  _fvarParamBuffers.resize(num_face_varying_channels);
  for (int index = 0; index < num_face_varying_channels; index++) {
    /* Face varying patch arrays */
    _fvarPatchArrays[index].assign(patch_table.GetFVarPatchArrayBuffer(),
                                   patch_table.GetFVarPatchArrayBuffer() + num_patch_arrays);

    /* Face varying patch index buffer */
    _fvarIndexBuffers[index] = GPU_storagebuf_create_ex(patch_table.GetFVarPatchIndexSize(index) *
                                                            sizeof(int32_t),
                                                        patch_table.GetFVarPatchIndexBuffer(index),
                                                        GPU_USAGE_STATIC,
                                                        "osd_face_varying_index");

    /* Face varying patch param buffer */
    _fvarParamBuffers[index] = GPU_storagebuf_create_ex(patch_table.GetFVarPatchParamSize(index) *
                                                            sizeof(PatchParam),
                                                        patch_table.GetFVarPatchParamBuffer(index),
                                                        GPU_USAGE_STATIC,
                                                        "osd_face_varying_params");
  }

  return true;
}
```

</details>

**沿实际写入检查状态**

- `_patchIndexBuffer = GPU_storagebuf_create_ex(`
- `_patchParamBuffer = GPU_storagebuf_create_ex(patch_param_size * sizeof(PatchParam),`
- `_varyingIndexBuffer = GPU_storagebuf_create_ex(patch_table.GetVaryingPatchIndexSize() *`
- `_fvarIndexBuffers[index] = GPU_storagebuf_create_ex(patch_table.GetFVarPatchIndexSize(index) *`
- `_fvarParamBuffers[index] = GPU_storagebuf_create_ex(patch_table.GetFVarPatchParamSize(index) *`

**结果出口**

- `return true;`

**继续追踪实现**

- `patch_table.GetNumPatchArrays` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L55。
- `_patchArrays.assign` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L56。
- `patch_table.GetPatchArrayBuffer` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L56。
- `patch_table.GetPatchIndexSize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L60。
- `GPU_storagebuf_create_ex` → [blender::GPU_storagebuf_create_ex · L59](%E4%BE%9D%E8%B5%96-gpu_storage_buffer-1706c5.md#f-4042921669abadf8)。
- `patch_table.GetPatchIndexBuffer` → [blender::opensubdiv::GPUPatchTable::GetPatchIndexBuffer · L34](%E4%BE%9D%E8%B5%96-gpu_patch_table-7ca9ff.md#f-bbe12493ea0baa29)。
- `patch_table.GetPatchParamSize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L68。
- `patch_table.GetPatchParamBuffer` → [blender::opensubdiv::GPUPatchTable::GetPatchParamBuffer · L40](%E4%BE%9D%E8%B5%96-gpu_patch_table-7ca9ff.md#f-2d98e130a8e57809)。
- `_varyingPatchArrays.assign` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L75。
- `patch_table.GetVaryingPatchArrayBuffer` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L75。
- `patch_table.GetVaryingPatchIndexSize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L79。
- `patch_table.GetVaryingPatchIndexBuffer` → [blender::opensubdiv::GPUPatchTable::GetVaryingPatchIndexBuffer · L52](%E4%BE%9D%E8%B5%96-gpu_patch_table-7ca9ff.md#f-f1af0b5a4da11abb)。
- `patch_table.GetNumFVarChannels` → [blender::opensubdiv::GPUPatchTable::GetNumFVarChannels · L58](%E4%BE%9D%E8%B5%96-gpu_patch_table-7ca9ff.md#f-be07aa1249e0dbff)。
- `_fvarPatchArrays.resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L87。
- `_fvarIndexBuffers.resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L88。
- `_fvarParamBuffers.resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L89。
- `_fvarPatchArrays[index].assign` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L92。
- `patch_table.GetFVarPatchArrayBuffer` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L92。
- `patch_table.GetFVarPatchIndexSize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L96。
- `patch_table.GetFVarPatchIndexBuffer` → [blender::opensubdiv::GPUPatchTable::GetFVarPatchIndexBuffer · L70](%E4%BE%9D%E8%B5%96-gpu_patch_table-7ca9ff.md#f-bd6cebd98a523da1)。
- `patch_table.GetFVarPatchParamSize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L103。
- `patch_table.GetFVarPatchParamBuffer` → [blender::opensubdiv::GPUPatchTable::GetFVarPatchParamBuffer · L76](%E4%BE%9D%E8%B5%96-gpu_patch_table-7ca9ff.md#f-8a35ebed3ac70aaf)。
