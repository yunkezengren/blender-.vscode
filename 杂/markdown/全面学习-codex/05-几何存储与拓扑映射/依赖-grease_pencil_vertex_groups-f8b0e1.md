# 实现依赖专题：source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::bke::greasepencil::validate_drawing_vertex_groups"]:::abstraction
  F1["blender::bke::greasepencil::ensure_vertex_group"]:::compute
  F2["blender::bke::greasepencil::clear_vertex_groups"]:::compute
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
  F["grease_pencil_vertex_groups.cc实现"]:::compute
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

<a id="f-eacafd3f78cf4dfa"></a>

### `blender::bke::greasepencil::validate_drawing_vertex_groups`

实现位置：[source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc](../../../../../source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc) · L26—L52。

接口参数：

- `GreasePencil &grease_pencil`

**教学注释版**

<!-- annotated:3bceb463b601d9 -->

```cpp
void validate_drawing_vertex_groups(GreasePencil &grease_pencil)
{
  Set<std::string> valid_names;
  for (const bDeformGroup &defgroup : grease_pencil.vertex_group_names) {
    // [讲解] valid_names.add_new：按哈希与相等关系加入键或键值。
    valid_names.add_new(defgroup.name);
  }

  for (GreasePencilDrawingBase *base : grease_pencil.drawings()) {
    if (base->type != GP_DRAWING) {
      continue;
    }
    Drawing &drawing = reinterpret_cast<GreasePencilDrawing *>(base)->wrap();

    /* Remove unknown vertex groups. */
    CurvesGeometry &curves = drawing.strokes_for_write();
    int defgroup_index = 0;
    for (bDeformGroup &defgroup : curves.vertex_group_names.items_mutable()) {
      // [讲解] valid_names.contains：查询活项数量或键是否存在。
      if (!valid_names.contains(defgroup.name)) {
        remove_defgroup_index(curves.deform_verts_for_write(), defgroup_index);

        BLI_freelinkN(&curves.vertex_group_names, &defgroup);
      }

      ++defgroup_index;
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc · L26—L52</summary>

<!-- original:3bceb463b601d9:source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc:26:52 -->

```cpp
void validate_drawing_vertex_groups(GreasePencil &grease_pencil)
{
  Set<std::string> valid_names;
  for (const bDeformGroup &defgroup : grease_pencil.vertex_group_names) {
    valid_names.add_new(defgroup.name);
  }

  for (GreasePencilDrawingBase *base : grease_pencil.drawings()) {
    if (base->type != GP_DRAWING) {
      continue;
    }
    Drawing &drawing = reinterpret_cast<GreasePencilDrawing *>(base)->wrap();

    /* Remove unknown vertex groups. */
    CurvesGeometry &curves = drawing.strokes_for_write();
    int defgroup_index = 0;
    for (bDeformGroup &defgroup : curves.vertex_group_names.items_mutable()) {
      if (!valid_names.contains(defgroup.name)) {
        remove_defgroup_index(curves.deform_verts_for_write(), defgroup_index);

        BLI_freelinkN(&curves.vertex_group_names, &defgroup);
      }

      ++defgroup_index;
    }
  }
}
```

</details>

**继续追踪实现**

- `valid_names.add_new` → [blender::Set::add_new · L233](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/08-Set%E4%B8%8E%E9%9B%86%E5%90%88%E8%AF%AD%E4%B9%89.md#f-12f4dd65a3abaaac)；[blender::Set::add_new · L237](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/08-Set%E4%B8%8E%E9%9B%86%E5%90%88%E8%AF%AD%E4%B9%89.md#f-9c46c167cdd9bb73)。同名重载需按实参类型选择。
- `grease_pencil.drawings` → [blender::GreasePencil::drawings · L3338](%E4%BE%9D%E8%B5%96-grease_pencil-f750d6.md#f-4a9381efc430533a)；[blender::GreasePencil::drawings · L3343](%E4%BE%9D%E8%B5%96-grease_pencil-f750d6.md#f-75a528a69126428b)。同名重载需按实参类型选择。
- `reinterpret_cast<GreasePencilDrawing *>(base)->wrap` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L37。
- `drawing.strokes_for_write` → [blender::bke::greasepencil::Drawing::strokes_for_write · L1012](%E4%BE%9D%E8%B5%96-grease_pencil-f750d6.md#f-0649333785d0aa95)。
- `curves.vertex_group_names.items_mutable` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L42。
- `valid_names.contains` → [blender::Set::contains · L310](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/08-Set%E4%B8%8E%E9%9B%86%E5%90%88%E8%AF%AD%E4%B9%89.md#f-af7099799494350e)。
- `remove_defgroup_index` → [blender::bke::remove_defgroup_index · L1758](%E4%BE%9D%E8%B5%96-deform-6949f4.md#f-42eb2479d5254ae6)。
- `curves.deform_verts_for_write` → [blender::bke::CurvesGeometry::deform_verts_for_write · L621](%E4%BE%9D%E8%B5%96-curves_geometry-ad7f9f.md#f-188eb89702a0a9e8)。
- `BLI_freelinkN` → [blender::BLI_freelinkN · L277](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-listbase-2816d9.md#f-c7719591852af7da)。

<a id="f-2d0283b48f7c4c8a"></a>

### `blender::bke::greasepencil::ensure_vertex_group`

实现位置：[source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc](../../../../../source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc) · L54—L65。

接口参数：

- `const StringRef name`
- `ListBaseT<bDeformGroup> &vertex_group_names`

**教学注释版**

<!-- annotated:518c638c8b9ed4 -->

```cpp
int ensure_vertex_group(const StringRef name, ListBaseT<bDeformGroup> &vertex_group_names)
{
  int def_nr = BKE_defgroup_name_index(&vertex_group_names, name);
  if (def_nr < 0) {
    bDeformGroup *defgroup = MEM_new<bDeformGroup>(__func__);
    name.copy_utf8_truncated(defgroup->name);
    BLI_addtail(&vertex_group_names, defgroup);
    def_nr = vertex_group_names.count() - 1;
    BLI_assert(def_nr >= 0);
  }
  return def_nr;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc · L54—L65</summary>

<!-- original:518c638c8b9ed4:source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc:54:65 -->

```cpp
int ensure_vertex_group(const StringRef name, ListBaseT<bDeformGroup> &vertex_group_names)
{
  int def_nr = BKE_defgroup_name_index(&vertex_group_names, name);
  if (def_nr < 0) {
    bDeformGroup *defgroup = MEM_new<bDeformGroup>(__func__);
    name.copy_utf8_truncated(defgroup->name);
    BLI_addtail(&vertex_group_names, defgroup);
    def_nr = vertex_group_names.count() - 1;
    BLI_assert(def_nr >= 0);
  }
  return def_nr;
}
```

</details>

**沿实际写入检查状态**

- `def_nr = vertex_group_names.count() - 1;`

**结果出口**

- `return def_nr;`

**继续追踪实现**

- `BKE_defgroup_name_index` → [blender::BKE_defgroup_name_index · L544](%E4%BE%9D%E8%B5%96-deform-6949f4.md#f-41ba0c2309b689c8)。
- `MEM_new<bDeformGroup>` → [MEM_new · L351](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-115f9b6784f89912)。
- `name.copy_utf8_truncated` → [blender::StringRefBase::copy_utf8_truncated · L28](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-string_ref-ed6905.md#f-5d01486bac37768d)；[blender::StringRefBase::copy_utf8_truncated · L256](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-b2a0157cbe286321)。同名重载需按实参类型选择。
- `BLI_addtail` → [blender::BLI_addtail · L118](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-listbase-2816d9.md#f-4fb027713fa3115b)。
- `vertex_group_names.count` → [blender::ListBaseT::count · L92](%E4%BE%9D%E8%B5%96-DNA_listBase-48dbc9.md#f-7d243d006ac4c693)。
- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。

<a id="f-630a526cbb7f2773"></a>

### `blender::bke::greasepencil::clear_vertex_groups`

实现位置：[source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc](../../../../../source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc) · L158—L171。

接口参数：

- `GreasePencil &grease_pencil`

**教学注释版**

<!-- annotated:b4eee82e60c8bb -->

```cpp
void clear_vertex_groups(GreasePencil &grease_pencil)
{
  for (GreasePencilDrawingBase *base : grease_pencil.drawings()) {
    if (base->type != GP_DRAWING) {
      continue;
    }
    Drawing &drawing = reinterpret_cast<GreasePencilDrawing *>(base)->wrap();
    bke::CurvesGeometry &curves = drawing.strokes_for_write();

    for (MDeformVert &dvert : curves.deform_verts_for_write()) {
      BKE_defvert_clear(&dvert);
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc · L158—L171</summary>

<!-- original:b4eee82e60c8bb:source/blender/blenkernel/intern/grease_pencil_vertex_groups.cc:158:171 -->

```cpp
void clear_vertex_groups(GreasePencil &grease_pencil)
{
  for (GreasePencilDrawingBase *base : grease_pencil.drawings()) {
    if (base->type != GP_DRAWING) {
      continue;
    }
    Drawing &drawing = reinterpret_cast<GreasePencilDrawing *>(base)->wrap();
    bke::CurvesGeometry &curves = drawing.strokes_for_write();

    for (MDeformVert &dvert : curves.deform_verts_for_write()) {
      BKE_defvert_clear(&dvert);
    }
  }
}
```

</details>

**继续追踪实现**

- `grease_pencil.drawings` → [blender::GreasePencil::drawings · L3338](%E4%BE%9D%E8%B5%96-grease_pencil-f750d6.md#f-4a9381efc430533a)；[blender::GreasePencil::drawings · L3343](%E4%BE%9D%E8%B5%96-grease_pencil-f750d6.md#f-75a528a69126428b)。同名重载需按实参类型选择。
- `reinterpret_cast<GreasePencilDrawing *>(base)->wrap` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L164。
- `drawing.strokes_for_write` → [blender::bke::greasepencil::Drawing::strokes_for_write · L1012](%E4%BE%9D%E8%B5%96-grease_pencil-f750d6.md#f-0649333785d0aa95)。
- `curves.deform_verts_for_write` → [blender::bke::CurvesGeometry::deform_verts_for_write · L621](%E4%BE%9D%E8%B5%96-curves_geometry-ad7f9f.md#f-188eb89702a0a9e8)。
- `BKE_defvert_clear` → [blender::BKE_defvert_clear · L918](%E4%BE%9D%E8%B5%96-deform-6949f4.md#f-b838f638844bd559)。
