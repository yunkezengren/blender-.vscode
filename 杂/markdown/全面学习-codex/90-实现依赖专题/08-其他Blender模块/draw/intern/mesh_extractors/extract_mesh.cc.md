# 实现依赖专题：source/blender/draw/intern/mesh_extractors/extract_mesh.cc

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::draw::mesh_render_data_face_flag"]:::abstraction
  F1["blender::draw::mesh_render_data_loop_flag"]:::compute
  F2["blender::draw::mesh_render_data_loop_edge_flag"]:::compute
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
  F["extract_mesh.cc实现"]:::compute
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

<a id="f-78bb4555cc3bf13e"></a>

### `blender::draw::mesh_render_data_face_flag`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.cc) · L25—L53。

接口参数：

- `const MeshRenderData &mr`
- `const BMFace *efa`
- `const BMUVOffsets &offsets`
- `EditLoopData &eattr`

**教学注释版**

<!-- annotated:c6540048c05353 -->

```cpp
void mesh_render_data_face_flag(const MeshRenderData &mr,
                                const BMFace *efa,
                                const BMUVOffsets &offsets,
                                EditLoopData &eattr)
{
  if (efa == mr.efa_act) {
    eattr.v_flag |= VFLAG_FACE_ACTIVE;
  }
  if (BM_elem_flag_test(efa, BM_ELEM_SELECT)) {
    eattr.v_flag |= VFLAG_FACE_SELECTED;
  }

  if (efa == mr.efa_act_uv) {
    eattr.v_flag |= VFLAG_FACE_UV_ACTIVE;
  }
  if ((offsets.uv != -1) && (!BM_elem_flag_test(efa, BM_ELEM_HIDDEN)) &&
      uvedit_face_select_test_ex(mr.toolsettings, mr.bm, efa))
  {
    eattr.v_flag |= VFLAG_FACE_UV_SELECT;
  }

#ifdef WITH_FREESTYLE
  if (mr.freestyle_face_ofs != -1) {
    if (BM_ELEM_CD_GET_BOOL(efa, mr.freestyle_face_ofs)) {
      eattr.v_flag |= VFLAG_FACE_FREESTYLE;
    }
  }
#endif
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.cc · L25—L53</summary>

<!-- original:c6540048c05353:source/blender/draw/intern/mesh_extractors/extract_mesh.cc:25:53 -->

```cpp
void mesh_render_data_face_flag(const MeshRenderData &mr,
                                const BMFace *efa,
                                const BMUVOffsets &offsets,
                                EditLoopData &eattr)
{
  if (efa == mr.efa_act) {
    eattr.v_flag |= VFLAG_FACE_ACTIVE;
  }
  if (BM_elem_flag_test(efa, BM_ELEM_SELECT)) {
    eattr.v_flag |= VFLAG_FACE_SELECTED;
  }

  if (efa == mr.efa_act_uv) {
    eattr.v_flag |= VFLAG_FACE_UV_ACTIVE;
  }
  if ((offsets.uv != -1) && (!BM_elem_flag_test(efa, BM_ELEM_HIDDEN)) &&
      uvedit_face_select_test_ex(mr.toolsettings, mr.bm, efa))
  {
    eattr.v_flag |= VFLAG_FACE_UV_SELECT;
  }

#ifdef WITH_FREESTYLE
  if (mr.freestyle_face_ofs != -1) {
    if (BM_ELEM_CD_GET_BOOL(efa, mr.freestyle_face_ofs)) {
      eattr.v_flag |= VFLAG_FACE_FREESTYLE;
    }
  }
#endif
}
```

</details>

**沿实际写入检查状态**

- `eattr.v_flag |= VFLAG_FACE_ACTIVE;`
- `eattr.v_flag |= VFLAG_FACE_SELECTED;`
- `eattr.v_flag |= VFLAG_FACE_UV_ACTIVE;`
- `eattr.v_flag |= VFLAG_FACE_UV_SELECT;`
- `eattr.v_flag |= VFLAG_FACE_FREESTYLE;`

**继续追踪实现**

- `BM_elem_flag_test` → [BM_elem_flag_test · L21](../../../bmesh/intern/bmesh_inline.hh.md#m-2431d1179b41)。宏定义由构建条件选择。
- `uvedit_face_select_test_ex` → [blender::uvedit_face_select_test_ex · L427](../../../editors/uvedit/uvedit_select.cc.md#f-de42c8e97b3369b1)。
- `BM_ELEM_CD_GET_BOOL` → [BM_ELEM_CD_GET_BOOL · L593](../../../bmesh/bmesh_class.hh.md#m-6cba9d53d692)。宏定义由构建条件选择。

<a id="f-a1fd01bc7b0f896a"></a>

### `blender::draw::mesh_render_data_loop_flag`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.cc) · L55—L69。

接口参数：

- `const MeshRenderData &mr`
- `const BMLoop *l`
- `const BMUVOffsets &offsets`
- `EditLoopData &eattr`

**教学注释版**

<!-- annotated:dad071f432fa00 -->

```cpp
void mesh_render_data_loop_flag(const MeshRenderData &mr,
                                const BMLoop *l,
                                const BMUVOffsets &offsets,
                                EditLoopData &eattr)
{
  if (offsets.uv == -1) {
    return;
  }
  if (BM_ELEM_CD_GET_BOOL(l, offsets.pin)) {
    eattr.v_flag |= VFLAG_VERT_UV_PINNED;
  }
  if (uvedit_uv_select_test_ex(mr.toolsettings, mr.bm, l, offsets)) {
    eattr.v_flag |= VFLAG_VERT_UV_SELECT;
  }
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.cc · L55—L69</summary>

<!-- original:dad071f432fa00:source/blender/draw/intern/mesh_extractors/extract_mesh.cc:55:69 -->

```cpp
void mesh_render_data_loop_flag(const MeshRenderData &mr,
                                const BMLoop *l,
                                const BMUVOffsets &offsets,
                                EditLoopData &eattr)
{
  if (offsets.uv == -1) {
    return;
  }
  if (BM_ELEM_CD_GET_BOOL(l, offsets.pin)) {
    eattr.v_flag |= VFLAG_VERT_UV_PINNED;
  }
  if (uvedit_uv_select_test_ex(mr.toolsettings, mr.bm, l, offsets)) {
    eattr.v_flag |= VFLAG_VERT_UV_SELECT;
  }
}
```

</details>

**沿实际写入检查状态**

- `eattr.v_flag |= VFLAG_VERT_UV_PINNED;`
- `eattr.v_flag |= VFLAG_VERT_UV_SELECT;`

**继续追踪实现**

- `BM_ELEM_CD_GET_BOOL` → [BM_ELEM_CD_GET_BOOL · L593](../../../bmesh/bmesh_class.hh.md#m-6cba9d53d692)。宏定义由构建条件选择。
- `uvedit_uv_select_test_ex` → [blender::uvedit_uv_select_test_ex · L892](../../../editors/uvedit/uvedit_select.cc.md#f-e6b14094fd82e971)。

<a id="f-5c08a17389b379d1"></a>

### `blender::draw::mesh_render_data_loop_edge_flag`

实现位置：[source/blender/draw/intern/mesh_extractors/extract_mesh.cc](../../../../../../../../../source/blender/draw/intern/mesh_extractors/extract_mesh.cc) · L71—L83。

接口参数：

- `const MeshRenderData &mr`
- `const BMLoop *l`
- `const BMUVOffsets &offsets`
- `EditLoopData &eattr`

**教学注释版**

<!-- annotated:37e1c9145eec7d -->

```cpp
void mesh_render_data_loop_edge_flag(const MeshRenderData &mr,
                                     const BMLoop *l,
                                     const BMUVOffsets &offsets,
                                     EditLoopData &eattr)
{
  if (offsets.uv == -1) {
    return;
  }
  if (uvedit_edge_select_test_ex(mr.toolsettings, mr.bm, l, offsets)) {
    eattr.v_flag |= VFLAG_EDGE_UV_SELECT;
    eattr.v_flag |= VFLAG_VERT_UV_SELECT;
  }
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/mesh_extractors/extract_mesh.cc · L71—L83</summary>

<!-- original:37e1c9145eec7d:source/blender/draw/intern/mesh_extractors/extract_mesh.cc:71:83 -->

```cpp
void mesh_render_data_loop_edge_flag(const MeshRenderData &mr,
                                     const BMLoop *l,
                                     const BMUVOffsets &offsets,
                                     EditLoopData &eattr)
{
  if (offsets.uv == -1) {
    return;
  }
  if (uvedit_edge_select_test_ex(mr.toolsettings, mr.bm, l, offsets)) {
    eattr.v_flag |= VFLAG_EDGE_UV_SELECT;
    eattr.v_flag |= VFLAG_VERT_UV_SELECT;
  }
}
```

</details>

**沿实际写入检查状态**

- `eattr.v_flag |= VFLAG_EDGE_UV_SELECT;`
- `eattr.v_flag |= VFLAG_VERT_UV_SELECT;`

**继续追踪实现**

- `uvedit_edge_select_test_ex` → [blender::uvedit_edge_select_test_ex · L616](../../../editors/uvedit/uvedit_select.cc.md#f-06e34e6cf42e735d)。
