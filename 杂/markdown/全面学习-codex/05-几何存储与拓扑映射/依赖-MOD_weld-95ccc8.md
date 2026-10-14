# 实现依赖专题：source/blender/modifiers/intern/MOD_weld.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::get_vertex_group"]:::abstraction
  F1["blender::selected_indices_from_vertex_group"]:::compute
  F2["blender::selection_array_from_vertex_group"]:::compute
  F3["blender::calculate_weld"]:::compute
  F4["blender::modify_mesh"]:::compute
  F5["blender::required_data_mask"]:::compute
  F3 -->|"显式调用"| F0
  F3 -->|"显式调用"| F1
  F3 -->|"显式调用"| F2
  F4 -->|"显式调用"| F3
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
  F["MOD_weld.cc实现"]:::compute
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

<a id="f-042200c5a68d465c"></a>

### `blender::get_vertex_group`

实现位置：[source/blender/modifiers/intern/MOD_weld.cc](../../../../../source/blender/modifiers/intern/MOD_weld.cc) · L47—L53。

接口参数：

- `const Mesh &mesh`
- `const int defgrp_index`

**教学注释版**

<!-- annotated:92d87d0c898966 -->

```cpp
static Span<MDeformVert> get_vertex_group(const Mesh &mesh, const int defgrp_index)
{
  if (defgrp_index == -1) {
    return {};
  }
  return mesh.deform_verts();
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_weld.cc · L47—L53</summary>

<!-- original:92d87d0c898966:source/blender/modifiers/intern/MOD_weld.cc:47:53 -->

```cpp
static Span<MDeformVert> get_vertex_group(const Mesh &mesh, const int defgrp_index)
{
  if (defgrp_index == -1) {
    return {};
  }
  return mesh.deform_verts();
}
```

</details>

**结果出口**

- `return {};`
- `return mesh.deform_verts();`

**继续追踪实现**

- `mesh.deform_verts` → [Mesh::deform_verts · L1266](03-MPoly%E8%BF%81%E7%A7%BB%E4%B8%8E%E5%85%BC%E5%AE%B9.md#f-4c0433aad24aa301)。

<a id="f-deb6f267abfadd1c"></a>

### `blender::selected_indices_from_vertex_group`

实现位置：[source/blender/modifiers/intern/MOD_weld.cc](../../../../../source/blender/modifiers/intern/MOD_weld.cc) · L55—L63。

接口参数：

- `Span<MDeformVert> vertex_group`
- `const int index`
- `const bool invert`
- `IndexMaskMemory &memory`

**教学注释版**

<!-- annotated:421f4ac5851842 -->

```cpp
static IndexMask selected_indices_from_vertex_group(Span<MDeformVert> vertex_group,
                                                    const int index,
                                                    const bool invert,
                                                    IndexMaskMemory &memory)
{
  // [讲解] vertex_group.index_range：查询视图长度或生成对应有效索引区间。
  return IndexMask::from_predicate(vertex_group.index_range(), memory, [&](const int i) {
    return (BKE_defvert_find_weight(&vertex_group[i], index) > 0.0f) != invert;
  });
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_weld.cc · L55—L63</summary>

<!-- original:421f4ac5851842:source/blender/modifiers/intern/MOD_weld.cc:55:63 -->

```cpp
static IndexMask selected_indices_from_vertex_group(Span<MDeformVert> vertex_group,
                                                    const int index,
                                                    const bool invert,
                                                    IndexMaskMemory &memory)
{
  return IndexMask::from_predicate(vertex_group.index_range(), memory, [&](const int i) {
    return (BKE_defvert_find_weight(&vertex_group[i], index) > 0.0f) != invert;
  });
}
```

</details>

**结果出口**

- `return IndexMask::from_predicate(vertex_group.index_range(), memory, [&](const int i) {`
- `return (BKE_defvert_find_weight(&vertex_group[i], index) > 0.0f) != invert;`

**继续追踪实现**

- `IndexMask::from_predicate` → [blender::index_mask::IndexMask::from_predicate · L1073](../04-%E8%99%9A%E6%8B%9F%E6%95%B0%E7%BB%84%E4%B8%8E%E7%B4%A2%E5%BC%95%E9%80%89%E6%8B%A9/12-%E9%87%8D%E6%9E%84%E5%8E%86%E5%8F%B2%E4%B8%8E%E5%9F%BA%E5%87%86%E7%BB%83%E4%B9%A0.md#f-3864daa059098df8)。
- `vertex_group.index_range` → [blender::Span::index_range · L405](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-caaa9b06e13e53e0)。
- `BKE_defvert_find_weight` → [blender::BKE_defvert_find_weight · L779](%E4%BE%9D%E8%B5%96-deform-6949f4.md#f-c117fcd05c4fd453)。

<a id="f-967c9d5038c617be"></a>

### `blender::selection_array_from_vertex_group`

实现位置：[source/blender/modifiers/intern/MOD_weld.cc](../../../../../source/blender/modifiers/intern/MOD_weld.cc) · L65—L75。

接口参数：

- `Span<MDeformVert> vertex_group`
- `const int index`
- `const bool invert`

**教学注释版**

<!-- annotated:bec42e5f0b9513 -->

```cpp
static Array<bool> selection_array_from_vertex_group(Span<MDeformVert> vertex_group,
                                                     const int index,
                                                     const bool invert)
{
  // [讲解] vertex_group.size：查询视图长度或生成对应有效索引区间。
  Array<bool> selection(vertex_group.size());
  // [讲解] vertex_group.index_range：查询视图长度或生成对应有效索引区间。
  for (const int i : vertex_group.index_range()) {
    const bool found = BKE_defvert_find_weight(&vertex_group[i], index) > 0.0f;
    selection[i] = (found != invert);
  }
  return selection;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_weld.cc · L65—L75</summary>

<!-- original:bec42e5f0b9513:source/blender/modifiers/intern/MOD_weld.cc:65:75 -->

```cpp
static Array<bool> selection_array_from_vertex_group(Span<MDeformVert> vertex_group,
                                                     const int index,
                                                     const bool invert)
{
  Array<bool> selection(vertex_group.size());
  for (const int i : vertex_group.index_range()) {
    const bool found = BKE_defvert_find_weight(&vertex_group[i], index) > 0.0f;
    selection[i] = (found != invert);
  }
  return selection;
}
```

</details>

**沿实际写入检查状态**

- `selection[i] = (found != invert);`

**结果出口**

- `return selection;`

**继续追踪实现**

- `vertex_group.size` → [blender::Span::size · L256](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-5f80fa006089c998)。
- `vertex_group.index_range` → [blender::Span::index_range · L405](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-caaa9b06e13e53e0)。
- `BKE_defvert_find_weight` → [blender::BKE_defvert_find_weight · L779](%E4%BE%9D%E8%B5%96-deform-6949f4.md#f-c117fcd05c4fd453)。

<a id="f-998dd16ca154f94a"></a>

### `blender::calculate_weld`

实现位置：[source/blender/modifiers/intern/MOD_weld.cc](../../../../../source/blender/modifiers/intern/MOD_weld.cc) · L77—L108。

接口参数：

- `const Mesh &mesh`
- `const WeldModifierData &wmd`

**教学注释版**

<!-- annotated:f14237e212e1ff -->

```cpp
static std::optional<Mesh *> calculate_weld(const Mesh &mesh, const WeldModifierData &wmd)
{
  const int defgrp_index = BKE_id_defgroup_name_index(&mesh.id, wmd.defgrp_name);
  Span<MDeformVert> vertex_group = get_vertex_group(mesh, defgrp_index);
  const bool invert = (wmd.flag & MOD_WELD_INVERT_VGROUP) != 0;

  if (wmd.mode == MOD_WELD_MODE_ALL) {
    // [讲解] vertex_group.is_empty：查询视图长度或生成对应有效索引区间。
    if (!vertex_group.is_empty()) {
      IndexMaskMemory memory;
      const IndexMask selected_indices = selected_indices_from_vertex_group(
          vertex_group, defgrp_index, invert, memory);
      return geometry::mesh_merge_by_distance_all(
          mesh, IndexMask(selected_indices), wmd.merge_dist);
    }
    return geometry::mesh_merge_by_distance_all(mesh, IndexMask(mesh.verts_num), wmd.merge_dist);
  }
  if (wmd.mode == MOD_WELD_MODE_CONNECTED) {
    const bool only_loose_edges = (wmd.flag & MOD_WELD_LOOSE_EDGES) != 0;
    if (!vertex_group.is_empty()) {
      Array<bool> selection = selection_array_from_vertex_group(
          vertex_group, defgrp_index, invert);
      return geometry::mesh_merge_by_distance_connected(
          mesh, selection, wmd.merge_dist, only_loose_edges);
    }
    Array<bool> selection(mesh.verts_num, true);
    return geometry::mesh_merge_by_distance_connected(
        mesh, selection, wmd.merge_dist, only_loose_edges);
  }

  BLI_assert_unreachable();
  return nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_weld.cc · L77—L108</summary>

<!-- original:f14237e212e1ff:source/blender/modifiers/intern/MOD_weld.cc:77:108 -->

```cpp
static std::optional<Mesh *> calculate_weld(const Mesh &mesh, const WeldModifierData &wmd)
{
  const int defgrp_index = BKE_id_defgroup_name_index(&mesh.id, wmd.defgrp_name);
  Span<MDeformVert> vertex_group = get_vertex_group(mesh, defgrp_index);
  const bool invert = (wmd.flag & MOD_WELD_INVERT_VGROUP) != 0;

  if (wmd.mode == MOD_WELD_MODE_ALL) {
    if (!vertex_group.is_empty()) {
      IndexMaskMemory memory;
      const IndexMask selected_indices = selected_indices_from_vertex_group(
          vertex_group, defgrp_index, invert, memory);
      return geometry::mesh_merge_by_distance_all(
          mesh, IndexMask(selected_indices), wmd.merge_dist);
    }
    return geometry::mesh_merge_by_distance_all(mesh, IndexMask(mesh.verts_num), wmd.merge_dist);
  }
  if (wmd.mode == MOD_WELD_MODE_CONNECTED) {
    const bool only_loose_edges = (wmd.flag & MOD_WELD_LOOSE_EDGES) != 0;
    if (!vertex_group.is_empty()) {
      Array<bool> selection = selection_array_from_vertex_group(
          vertex_group, defgrp_index, invert);
      return geometry::mesh_merge_by_distance_connected(
          mesh, selection, wmd.merge_dist, only_loose_edges);
    }
    Array<bool> selection(mesh.verts_num, true);
    return geometry::mesh_merge_by_distance_connected(
        mesh, selection, wmd.merge_dist, only_loose_edges);
  }

  BLI_assert_unreachable();
  return nullptr;
}
```

</details>

**结果出口**

- `return geometry::mesh_merge_by_distance_all(`
- `return geometry::mesh_merge_by_distance_all(mesh, IndexMask(mesh.verts_num), wmd.merge_dist);`
- `return geometry::mesh_merge_by_distance_connected(`
- `return nullptr;`

**继续追踪实现**

- `BKE_id_defgroup_name_index` → [blender::BKE_id_defgroup_name_index · L557](%E4%BE%9D%E8%B5%96-deform-6949f4.md#f-886667bbd10fa710)。
- `get_vertex_group` → [blender::get_vertex_group · L47](%E4%BE%9D%E8%B5%96-MOD_weld-95ccc8.md#f-042200c5a68d465c)。
- `vertex_group.is_empty` → [blender::Span::is_empty · L264](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-8cc1d7ba8feb50e6)。
- `selected_indices_from_vertex_group` → [blender::selected_indices_from_vertex_group · L55](%E4%BE%9D%E8%B5%96-MOD_weld-95ccc8.md#f-deb6f267abfadd1c)。
- `geometry::mesh_merge_by_distance_all` → [blender::geometry::mesh_merge_by_distance_all · L1285](%E4%BE%9D%E8%B5%96-mesh_merge_verts-bfe93a.md#f-5072276c0024899f)。
- `IndexMask` → [blender::index_mask::IndexMask::IndexMask · L704](../04-%E8%99%9A%E6%8B%9F%E6%95%B0%E7%BB%84%E4%B8%8E%E7%B4%A2%E5%BC%95%E9%80%89%E6%8B%A9/09-%E5%88%86%E6%AE%B5%E5%AD%98%E5%82%A8%E4%B8%8E%E9%81%8D%E5%8E%86.md#f-8c95440e4c5fec78)；[blender::index_mask::IndexMask::IndexMask · L709](../04-%E8%99%9A%E6%8B%9F%E6%95%B0%E7%BB%84%E4%B8%8E%E7%B4%A2%E5%BC%95%E9%80%89%E6%8B%A9/09-%E5%88%86%E6%AE%B5%E5%AD%98%E5%82%A8%E4%B8%8E%E9%81%8D%E5%8E%86.md#f-fdd9dc18868bc0cd)；[blender::index_mask::IndexMask::IndexMask · L722](../04-%E8%99%9A%E6%8B%9F%E6%95%B0%E7%BB%84%E4%B8%8E%E7%B4%A2%E5%BC%95%E9%80%89%E6%8B%A9/09-%E5%88%86%E6%AE%B5%E5%AD%98%E5%82%A8%E4%B8%8E%E9%81%8D%E5%8E%86.md#f-4b32f3ba3de66d05)。同名重载需按实参类型选择。
- `selection_array_from_vertex_group` → [blender::selection_array_from_vertex_group · L65](%E4%BE%9D%E8%B5%96-MOD_weld-95ccc8.md#f-967c9d5038c617be)。
- `geometry::mesh_merge_by_distance_connected` → [blender::geometry::mesh_merge_by_distance_connected · L1315](%E4%BE%9D%E8%B5%96-mesh_merge_verts-bfe93a.md#f-83a605e6ac22f89c)。
- `BLI_assert_unreachable` → [BLI_assert_unreachable · L77](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-7a2d91a67d8e)。宏定义由构建条件选择。

<a id="f-42477853422458a5"></a>

### `blender::modify_mesh`

实现位置：[source/blender/modifiers/intern/MOD_weld.cc](../../../../../source/blender/modifiers/intern/MOD_weld.cc) · L110—L119。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *`
- `Mesh *mesh`

**教学注释版**

<!-- annotated:8b75dfd996b77b -->

```cpp
static Mesh *modify_mesh(ModifierData *md, const ModifierEvalContext * /*ctx*/, Mesh *mesh)
{
  const WeldModifierData &wmd = reinterpret_cast<WeldModifierData &>(*md);

  std::optional<Mesh *> result = calculate_weld(*mesh, wmd);
  if (!result) {
    return mesh;
  }
  return *result;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_weld.cc · L110—L119</summary>

<!-- original:8b75dfd996b77b:source/blender/modifiers/intern/MOD_weld.cc:110:119 -->

```cpp
static Mesh *modify_mesh(ModifierData *md, const ModifierEvalContext * /*ctx*/, Mesh *mesh)
{
  const WeldModifierData &wmd = reinterpret_cast<WeldModifierData &>(*md);

  std::optional<Mesh *> result = calculate_weld(*mesh, wmd);
  if (!result) {
    return mesh;
  }
  return *result;
}
```

</details>

**结果出口**

- `return mesh;`
- `return *result;`

**继续追踪实现**

- `calculate_weld` → [blender::calculate_weld · L77](%E4%BE%9D%E8%B5%96-MOD_weld-95ccc8.md#f-998dd16ca154f94a)。

<a id="f-d565a45eef6f667d"></a>

### `blender::required_data_mask`

实现位置：[source/blender/modifiers/intern/MOD_weld.cc](../../../../../source/blender/modifiers/intern/MOD_weld.cc) · L127—L135。

接口参数：

- `ModifierData *md`
- `CustomData_MeshMasks *r_cddata_masks`

**教学注释版**

<!-- annotated:277612b02c73b5 -->

```cpp
static void required_data_mask(ModifierData *md, CustomData_MeshMasks *r_cddata_masks)
{
  WeldModifierData *wmd = reinterpret_cast<WeldModifierData *>(md);

  /* Ask for vertex-groups if we need them. */
  if (wmd->defgrp_name[0] != '\0') {
    r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_weld.cc · L127—L135</summary>

<!-- original:277612b02c73b5:source/blender/modifiers/intern/MOD_weld.cc:127:135 -->

```cpp
static void required_data_mask(ModifierData *md, CustomData_MeshMasks *r_cddata_masks)
{
  WeldModifierData *wmd = reinterpret_cast<WeldModifierData *>(md);

  /* Ask for vertex-groups if we need them. */
  if (wmd->defgrp_name[0] != '\0') {
    r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;
  }
}
```

</details>

**沿实际写入检查状态**

- `r_cddata_masks->vmask |= CD_MASK_MDEFORMVERT;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
