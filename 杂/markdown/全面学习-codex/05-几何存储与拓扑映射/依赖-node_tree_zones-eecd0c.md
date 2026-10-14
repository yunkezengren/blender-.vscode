# 实现依赖专题：source/blender/blenkernel/intern/node_tree_zones.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::bke::update_zone_depths"]:::abstraction
  F1["blender::bke::find_zone_nodes"]:::compute
  F2["blender::bke::get_direct_zone_relations"]:::compute
  F3["blender::bke::update_zone_per_node"]:::compute
  F4["blender::bke::update_zone_border_links"]:::compute
  F5["blender::bke::discover_tree_zones"]:::compute
  F6["blender::bke::get_tree_zones"]:::compute
  F7["blender::bke::bNodeTreeZone::contains_zone_recursively"]:::compute
  F0 -->|"显式调用"| F0
  F4 -->|"显式调用"| F7
  F5 -->|"显式调用"| F1
  F5 -->|"显式调用"| F2
  F5 -->|"显式调用"| F0
  F5 -->|"显式调用"| F3
  F5 -->|"显式调用"| F4
  F6 -->|"显式调用"| F5
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
  F["node_tree_zones.cc实现"]:::compute
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

<a id="f-b9a90f3e3e8f3d36"></a>

### `blender::bke::update_zone_depths`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L21—L32。

接口参数：

- `bNodeTreeZone &zone`

**教学注释版**

<!-- annotated:c680184b2c22ee -->

```cpp
static void update_zone_depths(bNodeTreeZone &zone)
{
  if (zone.depth >= 0) {
    return;
  }
  if (zone.parent_zone == nullptr) {
    zone.depth = 0;
    return;
  }
  update_zone_depths(*zone.parent_zone);
  zone.depth = zone.parent_zone->depth + 1;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L21—L32</summary>

<!-- original:c680184b2c22ee:source/blender/blenkernel/intern/node_tree_zones.cc:21:32 -->

```cpp
static void update_zone_depths(bNodeTreeZone &zone)
{
  if (zone.depth >= 0) {
    return;
  }
  if (zone.parent_zone == nullptr) {
    zone.depth = 0;
    return;
  }
  update_zone_depths(*zone.parent_zone);
  zone.depth = zone.parent_zone->depth + 1;
}
```

</details>

**沿实际写入检查状态**

- `zone.depth = 0;`
- `zone.depth = zone.parent_zone->depth + 1;`

**继续追踪实现**

- `update_zone_depths` → [blender::bke::update_zone_depths · L21](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-b9a90f3e3e8f3d36)。

<a id="f-99305529a0be15ee"></a>

### `blender::bke::find_zone_nodes`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L34—L72。

接口参数：

- `const bNodeTree &tree`
- `bNodeTreeZones &owner`
- `Map<const bNode *, bNodeTreeZone *> &r_zone_by_inout_node`

**教学注释版**

<!-- annotated:bca507342ba41a -->

```cpp
static Vector<std::unique_ptr<bNodeTreeZone>> find_zone_nodes(
    const bNodeTree &tree,
    bNodeTreeZones &owner,
    Map<const bNode *, bNodeTreeZone *> &r_zone_by_inout_node)
{
  const Span<const bNodeZoneType *> zone_types = all_zone_types();

  Vector<std::unique_ptr<bNodeTreeZone>> zones;
  Vector<const bNode *> zone_output_nodes;
  for (const bNodeZoneType *zone_type : zone_types) {
    // [讲解] zone_output_nodes.extend：将一段来源元素加入尾部。
    zone_output_nodes.extend(tree.nodes_by_type(zone_type->output_idname));
  }
  for (const bNode *node : zone_output_nodes) {
    // [讲解] std::make_unique<bNodeTreeZone>：创建独占拥有的对象，拥有关系可移动，get返回的借用指针不自动延长寿命。
    auto zone = std::make_unique<bNodeTreeZone>();
    zone->owner = &owner;
    // [讲解] zones.size：用end_减begin_得到活元素数量。
    zone->index = zones.size();
    zone->output_node_id = node->identifier;
    // [讲解] r_zone_by_inout_node.add：按哈希与相等关系加入键或键值。
    r_zone_by_inout_node.add(node, zone.get());
    // [讲解] zones.append：在尾部建立新元素，必要时先扩大存储。
    zones.append(std::move(zone));
  }
  for (const bNodeZoneType *zone_type : zone_types) {
    for (const bNode *input_node : tree.nodes_by_type(zone_type->input_idname)) {
      if (const bNode *output_node = zone_type->get_corresponding_output(tree, *input_node)) {
        // [讲解] r_zone_by_inout_node.lookup_default：按键查找对应项。
        if (bNodeTreeZone *zone = r_zone_by_inout_node.lookup_default(output_node, nullptr)) {
          zone->input_node_id = input_node->identifier;
          r_zone_by_inout_node.add(input_node, zone);
        }
      }
    }
  }
  /* Avoid incomplete zones, all zones must have a valid input and output node. */
  for (const std::unique_ptr<bNodeTreeZone> &zone : zones) {
    if (!zone->input_node_id || !zone->output_node_id) {
      // [讲解] r_zone_by_inout_node.clear：移除全部活项，并按接口决定是否归还存储。
      r_zone_by_inout_node.clear();
      return {};
    }
  }
  return zones;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L34—L72</summary>

<!-- original:bca507342ba41a:source/blender/blenkernel/intern/node_tree_zones.cc:34:72 -->

```cpp
static Vector<std::unique_ptr<bNodeTreeZone>> find_zone_nodes(
    const bNodeTree &tree,
    bNodeTreeZones &owner,
    Map<const bNode *, bNodeTreeZone *> &r_zone_by_inout_node)
{
  const Span<const bNodeZoneType *> zone_types = all_zone_types();

  Vector<std::unique_ptr<bNodeTreeZone>> zones;
  Vector<const bNode *> zone_output_nodes;
  for (const bNodeZoneType *zone_type : zone_types) {
    zone_output_nodes.extend(tree.nodes_by_type(zone_type->output_idname));
  }
  for (const bNode *node : zone_output_nodes) {
    auto zone = std::make_unique<bNodeTreeZone>();
    zone->owner = &owner;
    zone->index = zones.size();
    zone->output_node_id = node->identifier;
    r_zone_by_inout_node.add(node, zone.get());
    zones.append(std::move(zone));
  }
  for (const bNodeZoneType *zone_type : zone_types) {
    for (const bNode *input_node : tree.nodes_by_type(zone_type->input_idname)) {
      if (const bNode *output_node = zone_type->get_corresponding_output(tree, *input_node)) {
        if (bNodeTreeZone *zone = r_zone_by_inout_node.lookup_default(output_node, nullptr)) {
          zone->input_node_id = input_node->identifier;
          r_zone_by_inout_node.add(input_node, zone);
        }
      }
    }
  }
  /* Avoid incomplete zones, all zones must have a valid input and output node. */
  for (const std::unique_ptr<bNodeTreeZone> &zone : zones) {
    if (!zone->input_node_id || !zone->output_node_id) {
      r_zone_by_inout_node.clear();
      return {};
    }
  }
  return zones;
}
```

</details>

**沿实际写入检查状态**

- `zone->owner = &owner;`
- `zone->index = zones.size();`
- `zone->output_node_id = node->identifier;`
- `zone->input_node_id = input_node->identifier;`

**结果出口**

- `return {};`
- `return zones;`

**继续追踪实现**

- `all_zone_types` → [blender::bke::all_zone_types · L533](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-5d8e901f52f6d1b6)。
- `zone_output_nodes.extend` → [blender::Vector::extend · L595](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-fe6fcb7d09beded9)；[blender::Vector::extend · L599](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-40095c219019e2f9)；[blender::Vector::extend · L613](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-4d2e556cd7412fe4)；[blender::Vector::extend · L650](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-ae44ad8b3f05b082)。同名重载需按实参类型选择。
- `tree.nodes_by_type` → [blender::bNodeTree::nodes_by_type · L524](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-dbf5b02db7697f8c)；[blender::bNodeTree::nodes_by_type · L530](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-1316cfee8b291699)。同名重载需按实参类型选择。
- `std::make_unique<bNodeTreeZone>` → [外部契约](https://eel.is/c++draft/unique.ptr.create)：创建独占拥有的对象，拥有关系可移动，get返回的借用指针不自动延长寿命。
- `zones.size` → [blender::Vector::size · L780](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-714773731767349c)。
- `r_zone_by_inout_node.add` → [blender::Map::add · L295](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-8d38101abf162f88)；[blender::Map::add · L299](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-1f59510cdfbd9f87)；[blender::Map::add · L303](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-645e0522347aa018)；[blender::Map::add · L307](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-03405db0730cedc0)。同名重载需按实参类型选择。
- `zone.get` → [blender::bke::VolumeComponent::get · L68](%E4%BE%9D%E8%B5%96-geometry_component_volume-b14dd5.md#f-f542e2b53c8bf289)；[blender::bke::PointCloudComponent::get · L77](%E4%BE%9D%E8%B5%96-geometry_component_pointcloud-0caac6.md#f-fe39c478efa2050c)；[blender::bke::MeshComponent::get · L78](%E4%BE%9D%E8%B5%96-geometry_component_mesh-de716f.md#f-10a41ea54073cd9c)；[blender::bke::InstancesComponent::get · L74](%E4%BE%9D%E8%B5%96-geometry_component_instances-4b1341.md#f-4c08d16e1f4a620c)；[blender::bke::GreasePencilComponent::get · L72](%E4%BE%9D%E8%B5%96-geometry_component_grease_pencil-01c648.md#f-5a16e7ffc6574319)；[blender::bke::CurveComponent::get · L85](%E4%BE%9D%E8%B5%96-geometry_component_curves-b84d24.md#f-dcafa3852e73eb1e)；[blender::bke::AttributeIter::get · L408](%E4%BE%9D%E8%B5%96-attribute_access-bceef3.md#f-2c1e25e65fcbed9b)。同名重载需按实参类型选择。
- `zones.append` → [blender::Vector::append · L498](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-591e0b15e6308532)。同名重载需按实参类型选择。
- `std::move` → [外部契约](https://eel.is/c++draft/utility.forward)：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
- `zone_type->get_corresponding_output` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L56。
- `r_zone_by_inout_node.lookup_default` → [blender::Map::lookup_default · L570](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/05-Map%E6%8F%92%E5%85%A5%E4%B8%8E%E5%9B%9E%E8%B0%83.md#f-40294aaf345f6a8b)。
- `r_zone_by_inout_node.clear` → [blender::Map::clear · L1038](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/06-%E5%88%A0%E9%99%A4%E5%A2%93%E7%A2%91%E4%B8%8E%E5%80%BC%E9%94%80%E6%AF%81.md#f-c58ca43ed9dafe4a)。

<a id="f-a456d99c5fb99b19"></a>

### `blender::bke::get_direct_zone_relations`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L86—L142。

接口参数：

- `const Span<bNodeTreeZone *> all_zones`
- `const BitGroupVector<> &depend_on_input_flag_array`

**教学注释版**

<!-- annotated:c38f1754dbfd13 -->

```cpp
static std::optional<Vector<ZoneRelation>> get_direct_zone_relations(
    const Span<bNodeTreeZone *> all_zones, const BitGroupVector<> &depend_on_input_flag_array)
{
  VectorSet<ZoneRelation> all_zone_relations;

  /* Gather all relations, even the transitive once. */
  for (bNodeTreeZone *zone : all_zones) {
    const int zone_i = zone->index;
    for (const bNode *node : {zone->output_node()}) {
      if (node == nullptr) {
        continue;
      }
      const BoundedBitSpan depend_on_input_flags = depend_on_input_flag_array[node->index()];
      bits::foreach_1_index(depend_on_input_flags, [&](const int parent_zone_i) {
        if (parent_zone_i != zone_i) {
          // [讲解] all_zone_relations.add_new：按哈希与相等关系加入键或键值。
          all_zone_relations.add_new({all_zones[parent_zone_i], zone});
        }
      });
    }
  }

  for (const ZoneRelation &relation : all_zone_relations) {
    const ZoneRelation reverse_relation{relation.child, relation.parent};
    // [讲解] all_zone_relations.contains：查询活项数量或键是否存在。
    if (all_zone_relations.contains(reverse_relation)) {
      /* There is a cyclic zone dependency. */
      return std::nullopt;
    }
  }

  /* Remove transitive relations. This is a brute force algorithm currently. */
  Vector<int> transitive_relations;
  for (const int a : all_zone_relations.index_range()) {
    const ZoneRelation &relation_a = all_zone_relations[a];
    for (const int b : all_zone_relations.index_range()) {
      if (a == b) {
        continue;
      }
      const ZoneRelation &relation_b = all_zone_relations[b];
      if (relation_a.child != relation_b.parent) {
        continue;
      }
      const ZoneRelation transitive_relation{relation_a.parent, relation_b.child};
      const int transitive_relation_i = all_zone_relations.index_of_try(transitive_relation);
      if (transitive_relation_i != -1) {
        transitive_relations.append_non_duplicates(transitive_relation_i);
      }
    }
  }
  std::ranges::sort(transitive_relations, std::greater<>());

  Vector<ZoneRelation> zone_relations = all_zone_relations.as_span();
  for (const int i : transitive_relations) {
    // [讲解] zone_relations.remove_and_reorder：允许用末尾元素填补空洞，以减少后缀搬移。
    zone_relations.remove_and_reorder(i);
  }

  return zone_relations;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L86—L142</summary>

<!-- original:c38f1754dbfd13:source/blender/blenkernel/intern/node_tree_zones.cc:86:142 -->

```cpp
static std::optional<Vector<ZoneRelation>> get_direct_zone_relations(
    const Span<bNodeTreeZone *> all_zones, const BitGroupVector<> &depend_on_input_flag_array)
{
  VectorSet<ZoneRelation> all_zone_relations;

  /* Gather all relations, even the transitive once. */
  for (bNodeTreeZone *zone : all_zones) {
    const int zone_i = zone->index;
    for (const bNode *node : {zone->output_node()}) {
      if (node == nullptr) {
        continue;
      }
      const BoundedBitSpan depend_on_input_flags = depend_on_input_flag_array[node->index()];
      bits::foreach_1_index(depend_on_input_flags, [&](const int parent_zone_i) {
        if (parent_zone_i != zone_i) {
          all_zone_relations.add_new({all_zones[parent_zone_i], zone});
        }
      });
    }
  }

  for (const ZoneRelation &relation : all_zone_relations) {
    const ZoneRelation reverse_relation{relation.child, relation.parent};
    if (all_zone_relations.contains(reverse_relation)) {
      /* There is a cyclic zone dependency. */
      return std::nullopt;
    }
  }

  /* Remove transitive relations. This is a brute force algorithm currently. */
  Vector<int> transitive_relations;
  for (const int a : all_zone_relations.index_range()) {
    const ZoneRelation &relation_a = all_zone_relations[a];
    for (const int b : all_zone_relations.index_range()) {
      if (a == b) {
        continue;
      }
      const ZoneRelation &relation_b = all_zone_relations[b];
      if (relation_a.child != relation_b.parent) {
        continue;
      }
      const ZoneRelation transitive_relation{relation_a.parent, relation_b.child};
      const int transitive_relation_i = all_zone_relations.index_of_try(transitive_relation);
      if (transitive_relation_i != -1) {
        transitive_relations.append_non_duplicates(transitive_relation_i);
      }
    }
  }
  std::ranges::sort(transitive_relations, std::greater<>());

  Vector<ZoneRelation> zone_relations = all_zone_relations.as_span();
  for (const int i : transitive_relations) {
    zone_relations.remove_and_reorder(i);
  }

  return zone_relations;
}
```

</details>

**结果出口**

- `return std::nullopt;`
- `return zone_relations;`

**继续追踪实现**

- `zone->output_node` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L94。
- `node->index` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L98。
- `bits::foreach_1_index` → [blender::bits::foreach_1_index · L319](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_bit_span_ops-63a2e2.md#f-27c095604fcf6348)。
- `all_zone_relations.add_new` → [blender::VectorSet::add_new · L336](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/14-VectorSet%E7%A8%B3%E5%AE%9A%E7%B4%A2%E5%BC%95%E4%B8%8E%E5%8E%BB%E9%87%8D.md#f-03989f7359a8636d)；[blender::VectorSet::add_new · L340](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/14-VectorSet%E7%A8%B3%E5%AE%9A%E7%B4%A2%E5%BC%95%E4%B8%8E%E5%8E%BB%E9%87%8D.md#f-ef9174f041011a6b)。同名重载需按实参类型选择。
- `all_zone_relations.contains` → [blender::VectorSet::contains · L406](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/14-VectorSet%E7%A8%B3%E5%AE%9A%E7%B4%A2%E5%BC%95%E4%B8%8E%E5%8E%BB%E9%87%8D.md#f-c940dd79693ca442)。
- `all_zone_relations.index_range` → [blender::VectorSet::index_range · L589](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/14-VectorSet%E7%A8%B3%E5%AE%9A%E7%B4%A2%E5%BC%95%E4%B8%8E%E5%8E%BB%E9%87%8D.md#f-da5115bdc28bb390)。
- `all_zone_relations.index_of_try` → [blender::VectorSet::index_of_try · L492](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/14-VectorSet%E7%A8%B3%E5%AE%9A%E7%B4%A2%E5%BC%95%E4%B8%8E%E5%8E%BB%E9%87%8D.md#f-216c9238b6003f1a)。
- `transitive_relations.append_non_duplicates` → [blender::Vector::append_non_duplicates · L537](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-7741238254851c96)。
- `std::ranges::sort` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `std::greater<>` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `all_zone_relations.as_span` → [blender::VectorSet::as_span · L326](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/14-VectorSet%E7%A8%B3%E5%AE%9A%E7%B4%A2%E5%BC%95%E4%B8%8E%E5%8E%BB%E9%87%8D.md#f-76ed81b1cfbe99ad)。
- `zone_relations.remove_and_reorder` → [blender::Vector::remove_and_reorder · L829](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-d33bba972e915909)。

<a id="f-ee2be693cb4c98ee"></a>

### `blender::bke::update_zone_per_node`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L144—L197。

接口参数：

- `const Span<const bNode *> all_nodes`
- `const Span<bNodeTreeZone *> all_zones`
- `const BitGroupVector<> &depend_on_input_flag_array`
- `const Map<const bNode *, bNodeTreeZone *> &zone_by_inout_node`
- `Map<int, int> &r_zone_by_node_id`
- `Vector<int> &r_node_outside_zones`

**教学注释版**

<!-- annotated:93089f48b3acda -->

```cpp
static bool update_zone_per_node(const Span<const bNode *> all_nodes,
                                 const Span<bNodeTreeZone *> all_zones,
                                 const BitGroupVector<> &depend_on_input_flag_array,
                                 const Map<const bNode *, bNodeTreeZone *> &zone_by_inout_node,
                                 Map<int, int> &r_zone_by_node_id,
                                 Vector<int> &r_node_outside_zones)
{
  bool found_node_in_multiple_zones = false;
  // [讲解] all_nodes.index_range：查询视图长度或生成对应有效索引区间。
  for (const int node_i : all_nodes.index_range()) {
    const bNode &node = *all_nodes[node_i];
    const BoundedBitSpan depend_on_input_flags = depend_on_input_flag_array[node_i];
    bNodeTreeZone *parent_zone = nullptr;
    bits::foreach_1_index(depend_on_input_flags, [&](const int parent_zone_i) {
      bNodeTreeZone *zone = all_zones[parent_zone_i];
      if (ELEM(&node, zone->input_node(), zone->output_node())) {
        return;
      }
      if (parent_zone == nullptr) {
        parent_zone = zone;
        return;
      }
      for (bNodeTreeZone *iter_zone = zone->parent_zone; iter_zone;
           iter_zone = iter_zone->parent_zone)
      {
        if (iter_zone == parent_zone) {
          /* This zone is nested in the parent zone, so it becomes the new parent of the node. */
          parent_zone = zone;
          return;
        }
      }
      for (bNodeTreeZone *iter_zone = parent_zone->parent_zone; iter_zone;
           iter_zone = iter_zone->parent_zone)
      {
        if (iter_zone == zone) {
          /* This zone is a parent of the current parent of the node, do nothing. */
          return;
        }
      }
      found_node_in_multiple_zones = true;
    });
    if (parent_zone == nullptr) {
      // [讲解] zone_by_inout_node.contains：查询活项数量或键是否存在。
      if (!zone_by_inout_node.contains(&node)) {
        // [讲解] r_node_outside_zones.append：在尾部建立新元素，必要时先扩大存储。
        r_node_outside_zones.append(node.identifier);
      }
    }
    else {
      // [讲解] r_zone_by_node_id.add：按哈希与相等关系加入键或键值。
      r_zone_by_node_id.add(node.identifier, parent_zone->index);
    }
  }
  for (const MapItem<const bNode *, bNodeTreeZone *> item : zone_by_inout_node.items()) {
    r_zone_by_node_id.add_overwrite(item.key->identifier, item.value->index);
  }
  return found_node_in_multiple_zones;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L144—L197</summary>

<!-- original:93089f48b3acda:source/blender/blenkernel/intern/node_tree_zones.cc:144:197 -->

```cpp
static bool update_zone_per_node(const Span<const bNode *> all_nodes,
                                 const Span<bNodeTreeZone *> all_zones,
                                 const BitGroupVector<> &depend_on_input_flag_array,
                                 const Map<const bNode *, bNodeTreeZone *> &zone_by_inout_node,
                                 Map<int, int> &r_zone_by_node_id,
                                 Vector<int> &r_node_outside_zones)
{
  bool found_node_in_multiple_zones = false;
  for (const int node_i : all_nodes.index_range()) {
    const bNode &node = *all_nodes[node_i];
    const BoundedBitSpan depend_on_input_flags = depend_on_input_flag_array[node_i];
    bNodeTreeZone *parent_zone = nullptr;
    bits::foreach_1_index(depend_on_input_flags, [&](const int parent_zone_i) {
      bNodeTreeZone *zone = all_zones[parent_zone_i];
      if (ELEM(&node, zone->input_node(), zone->output_node())) {
        return;
      }
      if (parent_zone == nullptr) {
        parent_zone = zone;
        return;
      }
      for (bNodeTreeZone *iter_zone = zone->parent_zone; iter_zone;
           iter_zone = iter_zone->parent_zone)
      {
        if (iter_zone == parent_zone) {
          /* This zone is nested in the parent zone, so it becomes the new parent of the node. */
          parent_zone = zone;
          return;
        }
      }
      for (bNodeTreeZone *iter_zone = parent_zone->parent_zone; iter_zone;
           iter_zone = iter_zone->parent_zone)
      {
        if (iter_zone == zone) {
          /* This zone is a parent of the current parent of the node, do nothing. */
          return;
        }
      }
      found_node_in_multiple_zones = true;
    });
    if (parent_zone == nullptr) {
      if (!zone_by_inout_node.contains(&node)) {
        r_node_outside_zones.append(node.identifier);
      }
    }
    else {
      r_zone_by_node_id.add(node.identifier, parent_zone->index);
    }
  }
  for (const MapItem<const bNode *, bNodeTreeZone *> item : zone_by_inout_node.items()) {
    r_zone_by_node_id.add_overwrite(item.key->identifier, item.value->index);
  }
  return found_node_in_multiple_zones;
}
```

</details>

**沿实际写入检查状态**

- `parent_zone = zone;`
- `iter_zone = iter_zone->parent_zone)`
- `found_node_in_multiple_zones = true;`

**结果出口**

- `return found_node_in_multiple_zones;`

**继续追踪实现**

- `all_nodes.index_range` → [blender::Span::index_range · L405](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-caaa9b06e13e53e0)。
- `bits::foreach_1_index` → [blender::bits::foreach_1_index · L319](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_bit_span_ops-63a2e2.md#f-27c095604fcf6348)。
- `ELEM` → [ELEM · L88](%E4%BE%9D%E8%B5%96-GHOST_utildefines-34b996.md#m-d28724a15928)；[ELEM · L135](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_utildefines-293a0a.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `zone->input_node` → [blender::bke::bNodeTreeZone::input_node · L585](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-bbefd398fe5fd5b4)。
- `zone->output_node` → [blender::bke::bNodeTreeZone::output_node · L593](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-512b761599384e03)。
- `zone_by_inout_node.contains` → [blender::Map::contains · L353](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-70237c86261ee04d)。
- `r_node_outside_zones.append` → [blender::Vector::append · L498](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-591e0b15e6308532)。同名重载需按实参类型选择。
- `r_zone_by_node_id.add` → [blender::Map::add · L295](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-8d38101abf162f88)；[blender::Map::add · L299](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-1f59510cdfbd9f87)；[blender::Map::add · L303](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-645e0522347aa018)；[blender::Map::add · L307](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-03405db0730cedc0)。同名重载需按实参类型选择。
- `zone_by_inout_node.items` → [blender::Map::items · L902](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/06-%E5%88%A0%E9%99%A4%E5%A2%93%E7%A2%91%E4%B8%8E%E5%80%BC%E9%94%80%E6%AF%81.md#f-9ef4f6f70cba8f81)；[blender::Map::items · L913](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/06-%E5%88%A0%E9%99%A4%E5%A2%93%E7%A2%91%E4%B8%8E%E5%80%BC%E9%94%80%E6%AF%81.md#f-0a69f4e73db8973e)；[blender::Map::items · L926](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/06-%E5%88%A0%E9%99%A4%E5%A2%93%E7%A2%91%E4%B8%8E%E5%80%BC%E9%94%80%E6%AF%81.md#f-092add737130dcfb)；[blender::Map::items · L927](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/06-%E5%88%A0%E9%99%A4%E5%A2%93%E7%A2%91%E4%B8%8E%E5%80%BC%E9%94%80%E6%AF%81.md#f-4bfc999f60cdede4)。同名重载需按实参类型选择。
- `r_zone_by_node_id.add_overwrite` → [blender::Map::add_overwrite · L325](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-e340706c503570c8)；[blender::Map::add_overwrite · L329](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-33b468b72fd66944)；[blender::Map::add_overwrite · L333](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-d91cbf0ab4beeb7f)；[blender::Map::add_overwrite · L337](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/04-Map%E6%9F%A5%E6%89%BE%E4%B8%8E%E9%94%AE%E8%AE%BF%E9%97%AE.md#f-7e2b93551ab3f253)。同名重载需按实参类型选择。

<a id="f-eabaf03c405c9129"></a>

### `blender::bke::update_zone_border_links`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L199—L224。

接口参数：

- `const bNodeTree &tree`
- `bNodeTreeZones &tree_zones`

**教学注释版**

<!-- annotated:efdd3e9b2affd9 -->

```cpp
static void update_zone_border_links(const bNodeTree &tree, bNodeTreeZones &tree_zones)
{
  tree.ensure_topology_cache();
  for (const bNodeLink *link : tree.all_links()) {
    if (!link->is_available()) {
      continue;
    }
    if (link->is_muted()) {
      continue;
    }
    if (link->fromnode->is_dangling_reroute()) {
      continue;
    }
    bNodeTreeZone *from_zone = const_cast<bNodeTreeZone *>(
        tree_zones.get_zone_by_socket(*link->fromsock));
    bNodeTreeZone *to_zone = const_cast<bNodeTreeZone *>(
        tree_zones.get_zone_by_socket(*link->tosock));
    if (from_zone == to_zone) {
      continue;
    }
    BLI_assert(from_zone == nullptr || from_zone->contains_zone_recursively(*to_zone));
    for (bNodeTreeZone *zone = to_zone; zone != from_zone; zone = zone->parent_zone) {
      zone->border_links.append(link);
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L199—L224</summary>

<!-- original:efdd3e9b2affd9:source/blender/blenkernel/intern/node_tree_zones.cc:199:224 -->

```cpp
static void update_zone_border_links(const bNodeTree &tree, bNodeTreeZones &tree_zones)
{
  tree.ensure_topology_cache();
  for (const bNodeLink *link : tree.all_links()) {
    if (!link->is_available()) {
      continue;
    }
    if (link->is_muted()) {
      continue;
    }
    if (link->fromnode->is_dangling_reroute()) {
      continue;
    }
    bNodeTreeZone *from_zone = const_cast<bNodeTreeZone *>(
        tree_zones.get_zone_by_socket(*link->fromsock));
    bNodeTreeZone *to_zone = const_cast<bNodeTreeZone *>(
        tree_zones.get_zone_by_socket(*link->tosock));
    if (from_zone == to_zone) {
      continue;
    }
    BLI_assert(from_zone == nullptr || from_zone->contains_zone_recursively(*to_zone));
    for (bNodeTreeZone *zone = to_zone; zone != from_zone; zone = zone->parent_zone) {
      zone->border_links.append(link);
    }
  }
}
```

</details>

**继续追踪实现**

- `tree.ensure_topology_cache` → [blender::bNodeTree::ensure_topology_cache · L621](%E4%BE%9D%E8%B5%96-node_runtime-ee7c39.md#f-566e97bdf0367424)。
- `tree.all_links` → [blender::bNodeTree::all_links · L648](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-cfcf7bf984de76d5)；[blender::bNodeTree::all_links · L654](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-ef41559be796ba97)。同名重载需按实参类型选择。
- `link->is_available` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L203。
- `link->is_muted` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L206。
- `link->fromnode->is_dangling_reroute` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L209。
- `tree_zones.get_zone_by_socket` → [blender::bke::bNodeTreeZones::get_zone_by_socket · L417](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-e2e1838196101381)。
- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `from_zone->contains_zone_recursively` → [blender::bke::bNodeTreeZone::contains_zone_recursively · L407](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-21693947f7630897)。
- `zone->border_links.append` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L221。

<a id="f-9ea4d39a978a60ec"></a>

### `blender::bke::discover_tree_zones`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L226—L378。

接口参数：

- `const bNodeTree &tree`

**教学注释版**

<!-- annotated:b83865a3309f9d -->

```cpp
static std::unique_ptr<bNodeTreeZones> discover_tree_zones(const bNodeTree &tree)
{
  tree.ensure_topology_cache();
  if (tree.has_available_link_cycle()) {
    return {};
  }

  const Span<int> input_types = all_zone_input_node_types();
  const Span<int> output_types = all_zone_output_node_types();

  // [讲解] std::make_unique<bNodeTreeZones>：创建独占拥有的对象，拥有关系可移动，get返回的借用指针不自动延长寿命。
  std::unique_ptr<bNodeTreeZones> tree_zones = std::make_unique<bNodeTreeZones>();
  tree_zones->tree = &tree;

  const Span<const bNode *> all_nodes = tree.all_nodes();
  Map<const bNode *, bNodeTreeZone *> zone_by_inout_node;
  tree_zones->zones_ptrs = find_zone_nodes(tree, *tree_zones, zone_by_inout_node);
  for (const std::unique_ptr<bNodeTreeZone> &zone : tree_zones->zones_ptrs) {
    tree_zones->zones.append(zone.get());
  }

  const int zones_num = tree_zones->zones.size();
  // [讲解] all_nodes.size：查询视图长度或生成对应有效索引区间。
  const int nodes_num = all_nodes.size();
  /* A bit for every node-zone-combination. The bit is set when the node is in the zone. */
  BitGroupVector<> depend_on_input_flag_array(nodes_num, zones_num, false);
  /* The bit is set when the node depends on the output of the zone. */
  BitGroupVector<> depend_on_output_flag_array(nodes_num, zones_num, false);

  const Span<const bNode *> sorted_nodes = tree.toposort_left_to_right();
  for (const bNode *node : sorted_nodes) {
    const int node_i = node->index();
    MutableBoundedBitSpan depend_on_input_flags = depend_on_input_flag_array[node_i];
    MutableBoundedBitSpan depend_on_output_flags = depend_on_output_flag_array[node_i];

    /* Forward all bits from the nodes to the left. */
    for (const bNodeSocket *input_socket : node->input_sockets()) {
      if (!input_socket->is_available()) {
        continue;
      }
      for (const bNodeLink *link : input_socket->directly_linked_links()) {
        if (link->is_muted()) {
          continue;
        }
        const bNode &from_node = *link->fromnode;
        const int from_node_i = from_node.index();
        depend_on_input_flags |= depend_on_input_flag_array[from_node_i];
        depend_on_output_flags |= depend_on_output_flag_array[from_node_i];
      }
    }
    if (input_types.contains(node->type_legacy)) {
      // [讲解] zone_by_inout_node.lookup_default：按键查找对应项。
      if (const bNodeTreeZone *zone = zone_by_inout_node.lookup_default(node, nullptr)) {
        /* Now entering a zone, so set the corresponding bit. */
        depend_on_input_flags[zone->index].set();
      }
    }
    else if (output_types.contains(node->type_legacy)) {
      if (const bNodeTreeZone *zone = zone_by_inout_node.lookup_default(node, nullptr)) {
        /* The output is implicitly linked to the input, so also propagate the bits from there. */
        if (const bNode *zone_input_node = zone->input_node()) {
          const int input_node_i = zone_input_node->index();
          depend_on_input_flags |= depend_on_input_flag_array[input_node_i];
          depend_on_output_flags |= depend_on_output_flag_array[input_node_i];
        }
        /* Now exiting a zone, so change the bits accordingly. */
        depend_on_input_flags[zone->index].reset();
        depend_on_output_flags[zone->index].set();
      }
    }

    if (bits::has_common_set_bits(depend_on_input_flags, depend_on_output_flags)) {
      /* A node can not be inside and after a zone at the same time. */
      return {};
    }
  }

  const std::optional<Vector<ZoneRelation>> zone_relations = get_direct_zone_relations(
      tree_zones->zones, depend_on_input_flag_array);
  if (!zone_relations) {
    /* Found cyclic relations. */
    return {};
  }

  /* Set parent and child pointers in zones. */
  for (const ZoneRelation &relation : *zone_relations) {
    relation.parent->child_zones.append(relation.child);
    BLI_assert(relation.child->parent_zone == nullptr);
    relation.child->parent_zone = relation.parent;
  }

  Set<const bNodeTreeZone *> found_zones;
  for (bNodeTreeZone *main_zone : tree_zones->zones) {
    // [讲解] found_zones.clear：移除全部活项，并按接口决定是否归还存储。
    found_zones.clear();
    for (bNodeTreeZone *zone = main_zone; zone; zone = zone->parent_zone) {
      // [讲解] found_zones.add：按哈希与相等关系加入键或键值。
      if (!found_zones.add(zone)) {
        /* Found cyclic parent relationships between zones. */
        return {};
      }
    }
  }

  /* Update depths. */
  for (bNodeTreeZone *zone : tree_zones->zones) {
    update_zone_depths(*zone);
  }

  for (bNodeTreeZone *zone : tree_zones->zones) {
    if (zone->depth == 0) {
      tree_zones->root_zones.append(zone);
    }
  }

  const bool found_node_in_multiple_zones = update_zone_per_node(
      all_nodes,
      tree_zones->zones,
      depend_on_input_flag_array,
      zone_by_inout_node,
      tree_zones->zone_by_node_id,
      tree_zones->node_ids_outside_zones);
  if (found_node_in_multiple_zones) {
    return {};
  }

  for (const UString output_idname : {"NodeGroupOutput"_ustr,
                                      "ShaderNodeOutputMaterial"_ustr,
                                      "ShaderNodeOutputLight"_ustr,
                                      "ShaderNodeOutputWorld"_ustr,
                                      "ShaderNodeOutputAOV"_ustr})
  {
    for (const bNode *node : tree.nodes_by_type(output_idname)) {
      if (tree_zones->zone_by_node_id.contains(node->identifier)) {
        /* Output nodes must not be in a zone. */
        return {};
      }
    }
  }

  // [讲解] all_nodes.index_range：查询视图长度或生成对应有效索引区间。
  for (const int node_i : all_nodes.index_range()) {
    const bNode *node = all_nodes[node_i];
    const int zone_i = tree_zones->zone_by_node_id.lookup_default(node->identifier, -1);
    if (zone_i == -1) {
      continue;
    }
    bNodeTreeZone &zone = *tree_zones->zones[zone_i];
    if (ELEM(node->identifier, zone.input_node_id, zone.output_node_id)) {
      continue;
    }
    zone.child_node_ids.append(node->identifier);
  }

  update_zone_border_links(tree, *tree_zones);

  // std::cout << *tree_zones << std::endl;
  return tree_zones;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L226—L378</summary>

<!-- original:b83865a3309f9d:source/blender/blenkernel/intern/node_tree_zones.cc:226:378 -->

```cpp
static std::unique_ptr<bNodeTreeZones> discover_tree_zones(const bNodeTree &tree)
{
  tree.ensure_topology_cache();
  if (tree.has_available_link_cycle()) {
    return {};
  }

  const Span<int> input_types = all_zone_input_node_types();
  const Span<int> output_types = all_zone_output_node_types();

  std::unique_ptr<bNodeTreeZones> tree_zones = std::make_unique<bNodeTreeZones>();
  tree_zones->tree = &tree;

  const Span<const bNode *> all_nodes = tree.all_nodes();
  Map<const bNode *, bNodeTreeZone *> zone_by_inout_node;
  tree_zones->zones_ptrs = find_zone_nodes(tree, *tree_zones, zone_by_inout_node);
  for (const std::unique_ptr<bNodeTreeZone> &zone : tree_zones->zones_ptrs) {
    tree_zones->zones.append(zone.get());
  }

  const int zones_num = tree_zones->zones.size();
  const int nodes_num = all_nodes.size();
  /* A bit for every node-zone-combination. The bit is set when the node is in the zone. */
  BitGroupVector<> depend_on_input_flag_array(nodes_num, zones_num, false);
  /* The bit is set when the node depends on the output of the zone. */
  BitGroupVector<> depend_on_output_flag_array(nodes_num, zones_num, false);

  const Span<const bNode *> sorted_nodes = tree.toposort_left_to_right();
  for (const bNode *node : sorted_nodes) {
    const int node_i = node->index();
    MutableBoundedBitSpan depend_on_input_flags = depend_on_input_flag_array[node_i];
    MutableBoundedBitSpan depend_on_output_flags = depend_on_output_flag_array[node_i];

    /* Forward all bits from the nodes to the left. */
    for (const bNodeSocket *input_socket : node->input_sockets()) {
      if (!input_socket->is_available()) {
        continue;
      }
      for (const bNodeLink *link : input_socket->directly_linked_links()) {
        if (link->is_muted()) {
          continue;
        }
        const bNode &from_node = *link->fromnode;
        const int from_node_i = from_node.index();
        depend_on_input_flags |= depend_on_input_flag_array[from_node_i];
        depend_on_output_flags |= depend_on_output_flag_array[from_node_i];
      }
    }
    if (input_types.contains(node->type_legacy)) {
      if (const bNodeTreeZone *zone = zone_by_inout_node.lookup_default(node, nullptr)) {
        /* Now entering a zone, so set the corresponding bit. */
        depend_on_input_flags[zone->index].set();
      }
    }
    else if (output_types.contains(node->type_legacy)) {
      if (const bNodeTreeZone *zone = zone_by_inout_node.lookup_default(node, nullptr)) {
        /* The output is implicitly linked to the input, so also propagate the bits from there. */
        if (const bNode *zone_input_node = zone->input_node()) {
          const int input_node_i = zone_input_node->index();
          depend_on_input_flags |= depend_on_input_flag_array[input_node_i];
          depend_on_output_flags |= depend_on_output_flag_array[input_node_i];
        }
        /* Now exiting a zone, so change the bits accordingly. */
        depend_on_input_flags[zone->index].reset();
        depend_on_output_flags[zone->index].set();
      }
    }

    if (bits::has_common_set_bits(depend_on_input_flags, depend_on_output_flags)) {
      /* A node can not be inside and after a zone at the same time. */
      return {};
    }
  }

  const std::optional<Vector<ZoneRelation>> zone_relations = get_direct_zone_relations(
      tree_zones->zones, depend_on_input_flag_array);
  if (!zone_relations) {
    /* Found cyclic relations. */
    return {};
  }

  /* Set parent and child pointers in zones. */
  for (const ZoneRelation &relation : *zone_relations) {
    relation.parent->child_zones.append(relation.child);
    BLI_assert(relation.child->parent_zone == nullptr);
    relation.child->parent_zone = relation.parent;
  }

  Set<const bNodeTreeZone *> found_zones;
  for (bNodeTreeZone *main_zone : tree_zones->zones) {
    found_zones.clear();
    for (bNodeTreeZone *zone = main_zone; zone; zone = zone->parent_zone) {
      if (!found_zones.add(zone)) {
        /* Found cyclic parent relationships between zones. */
        return {};
      }
    }
  }

  /* Update depths. */
  for (bNodeTreeZone *zone : tree_zones->zones) {
    update_zone_depths(*zone);
  }

  for (bNodeTreeZone *zone : tree_zones->zones) {
    if (zone->depth == 0) {
      tree_zones->root_zones.append(zone);
    }
  }

  const bool found_node_in_multiple_zones = update_zone_per_node(
      all_nodes,
      tree_zones->zones,
      depend_on_input_flag_array,
      zone_by_inout_node,
      tree_zones->zone_by_node_id,
      tree_zones->node_ids_outside_zones);
  if (found_node_in_multiple_zones) {
    return {};
  }

  for (const UString output_idname : {"NodeGroupOutput"_ustr,
                                      "ShaderNodeOutputMaterial"_ustr,
                                      "ShaderNodeOutputLight"_ustr,
                                      "ShaderNodeOutputWorld"_ustr,
                                      "ShaderNodeOutputAOV"_ustr})
  {
    for (const bNode *node : tree.nodes_by_type(output_idname)) {
      if (tree_zones->zone_by_node_id.contains(node->identifier)) {
        /* Output nodes must not be in a zone. */
        return {};
      }
    }
  }

  for (const int node_i : all_nodes.index_range()) {
    const bNode *node = all_nodes[node_i];
    const int zone_i = tree_zones->zone_by_node_id.lookup_default(node->identifier, -1);
    if (zone_i == -1) {
      continue;
    }
    bNodeTreeZone &zone = *tree_zones->zones[zone_i];
    if (ELEM(node->identifier, zone.input_node_id, zone.output_node_id)) {
      continue;
    }
    zone.child_node_ids.append(node->identifier);
  }

  update_zone_border_links(tree, *tree_zones);

  // std::cout << *tree_zones << std::endl;
  return tree_zones;
}
```

</details>

**沿实际写入检查状态**

- `tree_zones->tree = &tree;`
- `tree_zones->zones_ptrs = find_zone_nodes(tree, *tree_zones, zone_by_inout_node);`
- `depend_on_input_flags |= depend_on_input_flag_array[from_node_i];`
- `depend_on_output_flags |= depend_on_output_flag_array[from_node_i];`
- `depend_on_input_flags |= depend_on_input_flag_array[input_node_i];`
- `depend_on_output_flags |= depend_on_output_flag_array[input_node_i];`
- `relation.child->parent_zone = relation.parent;`

**结果出口**

- `return {};`
- `return tree_zones;`

**继续追踪实现**

- `tree.ensure_topology_cache` → [blender::bNodeTree::ensure_topology_cache · L621](%E4%BE%9D%E8%B5%96-node_runtime-ee7c39.md#f-566e97bdf0367424)。
- `tree.has_available_link_cycle` → [blender::bNodeTree::has_available_link_cycle · L572](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-7bdcb85482e6bf35)。
- `all_zone_input_node_types` → [blender::bke::all_zone_input_node_types · L551](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-71714be31c5b4385)。
- `all_zone_output_node_types` → [blender::bke::all_zone_output_node_types · L563](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-414886f235d25392)。
- `std::make_unique<bNodeTreeZones>` → [外部契约](https://eel.is/c++draft/unique.ptr.create)：创建独占拥有的对象，拥有关系可移动，get返回的借用指针不自动延长寿命。
- `tree.all_nodes` → [blender::bNodeTree::all_nodes · L500](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-cda455cbcc6c7f36)；[blender::bNodeTree::all_nodes · L505](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-358b65e5678f8a32)。同名重载需按实参类型选择。
- `find_zone_nodes` → [blender::bke::find_zone_nodes · L34](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-99305529a0be15ee)。
- `tree_zones->zones.append` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L243。
- `zone.get` → [blender::bke::VolumeComponent::get · L68](%E4%BE%9D%E8%B5%96-geometry_component_volume-b14dd5.md#f-f542e2b53c8bf289)；[blender::bke::PointCloudComponent::get · L77](%E4%BE%9D%E8%B5%96-geometry_component_pointcloud-0caac6.md#f-fe39c478efa2050c)；[blender::bke::MeshComponent::get · L78](%E4%BE%9D%E8%B5%96-geometry_component_mesh-de716f.md#f-10a41ea54073cd9c)；[blender::bke::InstancesComponent::get · L74](%E4%BE%9D%E8%B5%96-geometry_component_instances-4b1341.md#f-4c08d16e1f4a620c)；[blender::bke::GreasePencilComponent::get · L72](%E4%BE%9D%E8%B5%96-geometry_component_grease_pencil-01c648.md#f-5a16e7ffc6574319)；[blender::bke::CurveComponent::get · L85](%E4%BE%9D%E8%B5%96-geometry_component_curves-b84d24.md#f-dcafa3852e73eb1e)；[blender::bke::AttributeIter::get · L408](%E4%BE%9D%E8%B5%96-attribute_access-bceef3.md#f-2c1e25e65fcbed9b)。同名重载需按实参类型选择。
- `tree_zones->zones.size` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L246。
- `all_nodes.size` → [blender::Span::size · L256](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-5f80fa006089c998)。
- `tree.toposort_left_to_right` → [blender::bNodeTree::toposort_left_to_right · L536](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-78989f1063f73ab2)；[blender::bNodeTree::toposort_left_to_right · L548](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-f08564985dc90c11)。同名重载需按实参类型选择。
- `node->index` → [blender::bNode::index · L745](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-0b206fb814a0e6da)。
- `node->input_sockets` → [blender::bNode::input_sockets · L754](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-82cd385c5c18b40d)；[blender::bNode::input_sockets · L766](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-65ad84a029887502)。同名重载需按实参类型选择。
- `input_socket->is_available` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L261。
- `input_socket->directly_linked_links` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L264。
- `link->is_muted` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L265。
- `from_node.index` → [blender::bNode::index · L745](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-0b206fb814a0e6da)。
- `input_types.contains` → [blender::Span::contains · L281](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-7caee498c984f2c0)。
- `zone_by_inout_node.lookup_default` → [blender::Map::lookup_default · L570](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/05-Map%E6%8F%92%E5%85%A5%E4%B8%8E%E5%9B%9E%E8%B0%83.md#f-40294aaf345f6a8b)。
- `depend_on_input_flags[zone->index].set` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L277。
- `output_types.contains` → [blender::Span::contains · L281](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-7caee498c984f2c0)。
- `zone->input_node` → [blender::bke::bNodeTreeZone::input_node · L585](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-bbefd398fe5fd5b4)。
- `zone_input_node->index` → [blender::bNode::index · L745](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-0b206fb814a0e6da)。
- `depend_on_input_flags[zone->index].reset` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L289。
- `depend_on_output_flags[zone->index].set` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L290。
- `bits::has_common_set_bits` → [blender::bits::has_common_set_bits · L299](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_bit_span_ops-63a2e2.md#f-6828962affbed504)。
- `get_direct_zone_relations` → [blender::bke::get_direct_zone_relations · L86](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-a456d99c5fb99b19)。
- `relation.parent->child_zones.append` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L309。
- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `found_zones.clear` → [blender::Set::clear · L570](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/08-Set%E4%B8%8E%E9%9B%86%E5%90%88%E8%AF%AD%E4%B9%89.md#f-ca1071f7960a58f0)。
- `found_zones.add` → [blender::Set::add · L248](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/08-Set%E4%B8%8E%E9%9B%86%E5%90%88%E8%AF%AD%E4%B9%89.md#f-c7498809c2327fba)；[blender::Set::add · L252](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/08-Set%E4%B8%8E%E9%9B%86%E5%90%88%E8%AF%AD%E4%B9%89.md#f-e3ac8d1c52c03c2b)。同名重载需按实参类型选择。
- `update_zone_depths` → [blender::bke::update_zone_depths · L21](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-b9a90f3e3e8f3d36)。
- `tree_zones->root_zones.append` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L332。
- `update_zone_per_node` → [blender::bke::update_zone_per_node · L144](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-ee2be693cb4c98ee)。
- `tree.nodes_by_type` → [blender::bNodeTree::nodes_by_type · L524](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-dbf5b02db7697f8c)；[blender::bNodeTree::nodes_by_type · L530](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-1316cfee8b291699)。同名重载需按实参类型选择。
- `tree_zones->zone_by_node_id.contains` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L354。
- `all_nodes.index_range` → [blender::Span::index_range · L405](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/05-Span%E5%8F%AA%E8%AF%BB%E8%BF%9E%E7%BB%AD%E8%A7%86%E5%9B%BE.md#f-caaa9b06e13e53e0)。
- `tree_zones->zone_by_node_id.lookup_default` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L363。
- `ELEM` → [ELEM · L88](%E4%BE%9D%E8%B5%96-GHOST_utildefines-34b996.md#m-d28724a15928)；[ELEM · L135](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_utildefines-293a0a.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `zone.child_node_ids.append` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L371。
- `update_zone_border_links` → [blender::bke::update_zone_border_links · L199](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-eabaf03c405c9129)。

<a id="f-d77c6f93b237a57d"></a>

### `blender::bke::get_tree_zones`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L380—L390。

接口参数：

- `const bNodeTree &tree`

**教学注释版**

<!-- annotated:e8572e822f832f -->

```cpp
const bNodeTreeZones *get_tree_zones(const bNodeTree &tree)
{
  tree.ensure_topology_cache();
  tree.runtime->tree_zones_cache_mutex.ensure([&]() {
    tree.runtime->tree_zones = discover_tree_zones(tree);
    if (tree.runtime->tree_zones) {
      tree.runtime->last_valid_zones = tree.runtime->tree_zones;
    }
  });
  return tree.runtime->tree_zones.get();
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L380—L390</summary>

<!-- original:e8572e822f832f:source/blender/blenkernel/intern/node_tree_zones.cc:380:390 -->

```cpp
const bNodeTreeZones *get_tree_zones(const bNodeTree &tree)
{
  tree.ensure_topology_cache();
  tree.runtime->tree_zones_cache_mutex.ensure([&]() {
    tree.runtime->tree_zones = discover_tree_zones(tree);
    if (tree.runtime->tree_zones) {
      tree.runtime->last_valid_zones = tree.runtime->tree_zones;
    }
  });
  return tree.runtime->tree_zones.get();
}
```

</details>

**沿实际写入检查状态**

- `tree.runtime->tree_zones = discover_tree_zones(tree);`
- `tree.runtime->last_valid_zones = tree.runtime->tree_zones;`

**结果出口**

- `return tree.runtime->tree_zones.get();`

**继续追踪实现**

- `tree.ensure_topology_cache` → [blender::bNodeTree::ensure_topology_cache · L621](%E4%BE%9D%E8%B5%96-node_runtime-ee7c39.md#f-566e97bdf0367424)。
- `tree.runtime->tree_zones_cache_mutex.ensure` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L383。
- `discover_tree_zones` → [blender::bke::discover_tree_zones · L226](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-9ea4d39a978a60ec)。
- `tree.runtime->tree_zones.get` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L389。

<a id="f-21693947f7630897"></a>

### `blender::bke::bNodeTreeZone::contains_zone_recursively`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L407—L415。

接口参数：

- `const bNodeTreeZone &other_zone`

**教学注释版**

<!-- annotated:98f8a9b74f50c9 -->

```cpp
bool bNodeTreeZone::contains_zone_recursively(const bNodeTreeZone &other_zone) const
{
  for (const bNodeTreeZone *zone = other_zone.parent_zone; zone; zone = zone->parent_zone) {
    if (zone == this) {
      return true;
    }
  }
  return false;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L407—L415</summary>

<!-- original:98f8a9b74f50c9:source/blender/blenkernel/intern/node_tree_zones.cc:407:415 -->

```cpp
bool bNodeTreeZone::contains_zone_recursively(const bNodeTreeZone &other_zone) const
{
  for (const bNodeTreeZone *zone = other_zone.parent_zone; zone; zone = zone->parent_zone) {
    if (zone == this) {
      return true;
    }
  }
  return false;
}
```

</details>

**结果出口**

- `return true;`
- `return false;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-e2e1838196101381"></a>

### `blender::bke::bNodeTreeZones::get_zone_by_socket`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L417—L435。

接口参数：

- `const bNodeSocket &socket`

**教学注释版**

<!-- annotated:5882db45af8f34 -->

```cpp
const bNodeTreeZone *bNodeTreeZones::get_zone_by_socket(const bNodeSocket &socket) const
{
  const bNode &node = socket.owner_node();
  const bNodeTreeZone *zone = this->get_zone_by_node(node.identifier);
  if (zone == nullptr) {
    return zone;
  }
  if (zone->input_node_id == node.identifier) {
    if (socket.is_input()) {
      return zone->parent_zone;
    }
  }
  if (zone->output_node_id == node.identifier) {
    if (socket.is_output()) {
      return zone->parent_zone;
    }
  }
  return zone;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L417—L435</summary>

<!-- original:5882db45af8f34:source/blender/blenkernel/intern/node_tree_zones.cc:417:435 -->

```cpp
const bNodeTreeZone *bNodeTreeZones::get_zone_by_socket(const bNodeSocket &socket) const
{
  const bNode &node = socket.owner_node();
  const bNodeTreeZone *zone = this->get_zone_by_node(node.identifier);
  if (zone == nullptr) {
    return zone;
  }
  if (zone->input_node_id == node.identifier) {
    if (socket.is_input()) {
      return zone->parent_zone;
    }
  }
  if (zone->output_node_id == node.identifier) {
    if (socket.is_output()) {
      return zone->parent_zone;
    }
  }
  return zone;
}
```

</details>

**结果出口**

- `return zone;`
- `return zone->parent_zone;`

**继续追踪实现**

- `socket.owner_node` → [blender::bNodeSocket::owner_node · L1069](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-e92f9934c26a08ec)；[blender::bNodeSocket::owner_node · L1159](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-88477f32cb5dce90)。同名重载需按实参类型选择。
- `this->get_zone_by_node` → [blender::bke::bNodeTreeZones::get_zone_by_node · L437](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-dcc4746d65b4807a)。
- `socket.is_input` → [blender::bNodeSocket::is_input · L1144](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-708c56203502bb29)。
- `socket.is_output` → [blender::bNodeSocket::is_output · L1149](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-50a6549b2d3958ca)。

<a id="f-dcc4746d65b4807a"></a>

### `blender::bke::bNodeTreeZones::get_zone_by_node`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L437—L444。

接口参数：

- `const int32_t node_id`

**教学注释版**

<!-- annotated:e4ef543e161aca -->

```cpp
const bNodeTreeZone *bNodeTreeZones::get_zone_by_node(const int32_t node_id) const
{
  const int zone_i = this->zone_by_node_id.lookup_default(node_id, -1);
  if (zone_i == -1) {
    return nullptr;
  }
  return this->zones[zone_i];
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L437—L444</summary>

<!-- original:e4ef543e161aca:source/blender/blenkernel/intern/node_tree_zones.cc:437:444 -->

```cpp
const bNodeTreeZone *bNodeTreeZones::get_zone_by_node(const int32_t node_id) const
{
  const int zone_i = this->zone_by_node_id.lookup_default(node_id, -1);
  if (zone_i == -1) {
    return nullptr;
  }
  return this->zones[zone_i];
}
```

</details>

**结果出口**

- `return nullptr;`
- `return this->zones[zone_i];`

**继续追踪实现**

- `this->zone_by_node_id.lookup_default` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L439。

<a id="f-f8f1a0c53a5f1acf"></a>

### `blender::bke::bNodeTreeZones::link_between_zones_is_allowed`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L446—L462。

接口参数：

- `const bNodeTreeZone *from_zone`
- `const bNodeTreeZone *to_zone`

**教学注释版**

<!-- annotated:1587018e72678a -->

```cpp
bool bNodeTreeZones::link_between_zones_is_allowed(const bNodeTreeZone *from_zone,
                                                   const bNodeTreeZone *to_zone) const
{
  if (from_zone == to_zone) {
    /* Links between zones in the same zone are always allowed. */
    return true;
  }
  if (!from_zone) {
    /* Links from the root tree can go to any zone. */
    return true;
  }
  if (!to_zone) {
    /* Links can not leave a zone and connect to a socket in the root tree. */
    return false;
  }
  return from_zone->contains_zone_recursively(*to_zone);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L446—L462</summary>

<!-- original:1587018e72678a:source/blender/blenkernel/intern/node_tree_zones.cc:446:462 -->

```cpp
bool bNodeTreeZones::link_between_zones_is_allowed(const bNodeTreeZone *from_zone,
                                                   const bNodeTreeZone *to_zone) const
{
  if (from_zone == to_zone) {
    /* Links between zones in the same zone are always allowed. */
    return true;
  }
  if (!from_zone) {
    /* Links from the root tree can go to any zone. */
    return true;
  }
  if (!to_zone) {
    /* Links can not leave a zone and connect to a socket in the root tree. */
    return false;
  }
  return from_zone->contains_zone_recursively(*to_zone);
}
```

</details>

**结果出口**

- `return true;`
- `return false;`
- `return from_zone->contains_zone_recursively(*to_zone);`

**继续追踪实现**

- `from_zone->contains_zone_recursively` → [blender::bke::bNodeTreeZone::contains_zone_recursively · L407](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-21693947f7630897)。

<a id="f-2cf7f249167abb9c"></a>

### `blender::bke::bNodeTreeZones::link_between_sockets_is_allowed`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L464—L472。

接口参数：

- `const bNodeSocket &from`
- `const bNodeSocket &to`

**教学注释版**

<!-- annotated:04b21588615279 -->

```cpp
bool bNodeTreeZones::link_between_sockets_is_allowed(const bNodeSocket &from,
                                                     const bNodeSocket &to) const
{
  BLI_assert(from.in_out == SOCK_OUT);
  BLI_assert(to.in_out == SOCK_IN);
  const bNodeTreeZone *from_zone = this->get_zone_by_socket(from);
  const bNodeTreeZone *to_zone = this->get_zone_by_socket(to);
  return this->link_between_zones_is_allowed(from_zone, to_zone);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L464—L472</summary>

<!-- original:04b21588615279:source/blender/blenkernel/intern/node_tree_zones.cc:464:472 -->

```cpp
bool bNodeTreeZones::link_between_sockets_is_allowed(const bNodeSocket &from,
                                                     const bNodeSocket &to) const
{
  BLI_assert(from.in_out == SOCK_OUT);
  BLI_assert(to.in_out == SOCK_IN);
  const bNodeTreeZone *from_zone = this->get_zone_by_socket(from);
  const bNodeTreeZone *to_zone = this->get_zone_by_socket(to);
  return this->link_between_zones_is_allowed(from_zone, to_zone);
}
```

</details>

**结果出口**

- `return this->link_between_zones_is_allowed(from_zone, to_zone);`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `this->get_zone_by_socket` → [blender::bke::bNodeTreeZones::get_zone_by_socket · L417](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-e2e1838196101381)。
- `this->link_between_zones_is_allowed` → [blender::bke::bNodeTreeZones::link_between_zones_is_allowed · L446](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-f8f1a0c53a5f1acf)。

<a id="f-b6ce06ad015298e1"></a>

### `blender::bke::bNodeTreeZones::get_zones_to_enter`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L474—L484。

接口参数：

- `const bNodeTreeZone *outer_zone`
- `const bNodeTreeZone *inner_zone`

**教学注释版**

<!-- annotated:a919ed2f37bdab -->

```cpp
Vector<const bNodeTreeZone *> bNodeTreeZones::get_zones_to_enter(
    const bNodeTreeZone *outer_zone, const bNodeTreeZone *inner_zone) const
{
  BLI_assert(this->link_between_zones_is_allowed(outer_zone, inner_zone));
  Vector<const bNodeTreeZone *> zones_to_enter;
  for (const bNodeTreeZone *zone = inner_zone; zone != outer_zone; zone = zone->parent_zone) {
    // [讲解] zones_to_enter.append：在尾部建立新元素，必要时先扩大存储。
    zones_to_enter.append(zone);
  }
  // [讲解] zones_to_enter.begin：提供当前存储或有效范围的地址。
  std::reverse(zones_to_enter.begin(), zones_to_enter.end());
  return zones_to_enter;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L474—L484</summary>

<!-- original:a919ed2f37bdab:source/blender/blenkernel/intern/node_tree_zones.cc:474:484 -->

```cpp
Vector<const bNodeTreeZone *> bNodeTreeZones::get_zones_to_enter(
    const bNodeTreeZone *outer_zone, const bNodeTreeZone *inner_zone) const
{
  BLI_assert(this->link_between_zones_is_allowed(outer_zone, inner_zone));
  Vector<const bNodeTreeZone *> zones_to_enter;
  for (const bNodeTreeZone *zone = inner_zone; zone != outer_zone; zone = zone->parent_zone) {
    zones_to_enter.append(zone);
  }
  std::reverse(zones_to_enter.begin(), zones_to_enter.end());
  return zones_to_enter;
}
```

</details>

**结果出口**

- `return zones_to_enter;`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `this->link_between_zones_is_allowed` → [blender::bke::bNodeTreeZones::link_between_zones_is_allowed · L446](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-f8f1a0c53a5f1acf)。
- `zones_to_enter.append` → [blender::Vector::append · L498](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-591e0b15e6308532)。同名重载需按实参类型选择。
- `std::reverse` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `zones_to_enter.begin` → [blender::Vector::begin · L967](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/12-Vector%E5%BC%82%E5%B8%B8%E5%AE%89%E5%85%A8%E4%B8%8E%E8%BE%B9%E7%95%8C.md#f-64fb75a6663b953c)；[blender::Vector::begin · L976](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/12-Vector%E5%BC%82%E5%B8%B8%E5%AE%89%E5%85%A8%E4%B8%8E%E8%BE%B9%E7%95%8C.md#f-7c6486a8b8e8f13f)。同名重载需按实参类型选择。
- `zones_to_enter.end` → [blender::Vector::end · L971](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/12-Vector%E5%BC%82%E5%B8%B8%E5%AE%89%E5%85%A8%E4%B8%8E%E8%BE%B9%E7%95%8C.md#f-8a6033745be8f712)；[blender::Vector::end · L980](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/12-Vector%E5%BC%82%E5%B8%B8%E5%AE%89%E5%85%A8%E4%B8%8E%E8%BE%B9%E7%95%8C.md#f-ebb3ada259887677)。同名重载需按实参类型选择。

<a id="f-cc9a16cd8896fd73"></a>

### `blender::bke::bNodeTreeZones::get_zones_to_enter_from_root`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L486—L490。

接口参数：

- `const bNodeTreeZone *zone`

**教学注释版**

<!-- annotated:b387fb25e82e7c -->

```cpp
Vector<const bNodeTreeZone *> bNodeTreeZones::get_zones_to_enter_from_root(
    const bNodeTreeZone *zone) const
{
  return this->get_zones_to_enter(nullptr, zone);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L486—L490</summary>

<!-- original:b387fb25e82e7c:source/blender/blenkernel/intern/node_tree_zones.cc:486:490 -->

```cpp
Vector<const bNodeTreeZone *> bNodeTreeZones::get_zones_to_enter_from_root(
    const bNodeTreeZone *zone) const
{
  return this->get_zones_to_enter(nullptr, zone);
}
```

</details>

**结果出口**

- `return this->get_zones_to_enter(nullptr, zone);`

**继续追踪实现**

- `this->get_zones_to_enter` → [blender::bke::bNodeTreeZones::get_zones_to_enter · L474](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-b6ce06ad015298e1)。

<a id="f-d7ac9d8e56bbc9bb"></a>

### `blender::bke::bNodeZoneType::get_corresponding_input`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L492—L502。

接口参数：

- `const bNodeTree &tree`
- `const bNode &output_bnode`

**教学注释版**

<!-- annotated:a215e211a736b0 -->

```cpp
const bNode *bNodeZoneType::get_corresponding_input(const bNodeTree &tree,
                                                    const bNode &output_bnode) const
{
  tree.ensure_topology_cache();
  for (const bNode *node : tree.nodes_by_type(this->input_idname)) {
    if (this->get_corresponding_output_id(*node) == output_bnode.identifier) {
      return node;
    }
  }
  return nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L492—L502</summary>

<!-- original:a215e211a736b0:source/blender/blenkernel/intern/node_tree_zones.cc:492:502 -->

```cpp
const bNode *bNodeZoneType::get_corresponding_input(const bNodeTree &tree,
                                                    const bNode &output_bnode) const
{
  tree.ensure_topology_cache();
  for (const bNode *node : tree.nodes_by_type(this->input_idname)) {
    if (this->get_corresponding_output_id(*node) == output_bnode.identifier) {
      return node;
    }
  }
  return nullptr;
}
```

</details>

**结果出口**

- `return node;`
- `return nullptr;`

**继续追踪实现**

- `tree.ensure_topology_cache` → [blender::bNodeTree::ensure_topology_cache · L621](%E4%BE%9D%E8%B5%96-node_runtime-ee7c39.md#f-566e97bdf0367424)。
- `tree.nodes_by_type` → [blender::bNodeTree::nodes_by_type · L524](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-dbf5b02db7697f8c)；[blender::bNodeTree::nodes_by_type · L530](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-1316cfee8b291699)。同名重载需按实参类型选择。
- `this->get_corresponding_output_id` → [bNodeZoneType::get_corresponding_output_id · L1321](%E4%BE%9D%E8%B5%96-BKE_node-4006d7.md#f-83fa308b827169d3)。

<a id="f-b4cf6a6324d9b816"></a>

### `blender::bke::bNodeZoneType::get_corresponding_output`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L504—L508。

接口参数：

- `const bNodeTree &tree`
- `const bNode &input_bnode`

**教学注释版**

<!-- annotated:8d3ab7937a044d -->

```cpp
const bNode *bNodeZoneType::get_corresponding_output(const bNodeTree &tree,
                                                     const bNode &input_bnode) const
{
  return tree.node_by_id(this->get_corresponding_output_id(input_bnode));
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L504—L508</summary>

<!-- original:8d3ab7937a044d:source/blender/blenkernel/intern/node_tree_zones.cc:504:508 -->

```cpp
const bNode *bNodeZoneType::get_corresponding_output(const bNodeTree &tree,
                                                     const bNode &input_bnode) const
{
  return tree.node_by_id(this->get_corresponding_output_id(input_bnode));
}
```

</details>

**结果出口**

- `return tree.node_by_id(this->get_corresponding_output_id(input_bnode));`

**继续追踪实现**

- `tree.node_by_id` → [blender::bNodeTree::node_by_id · L510](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-9ad10482fbea31d4)；[blender::bNodeTree::node_by_id · L517](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-d25cdfa86a7c2cb1)。同名重载需按实参类型选择。
- `this->get_corresponding_output_id` → [bNodeZoneType::get_corresponding_output_id · L1321](%E4%BE%9D%E8%B5%96-BKE_node-4006d7.md#f-83fa308b827169d3)。

<a id="f-b4b9326f710ef601"></a>

### `blender::bke::bNodeZoneType::get_corresponding_input`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L510—L514。

接口参数：

- `bNodeTree &tree`
- `const bNode &output_bnode`

**教学注释版**

<!-- annotated:20da66296be8ad -->

```cpp
bNode *bNodeZoneType::get_corresponding_input(bNodeTree &tree, const bNode &output_bnode) const
{
  return const_cast<bNode *>(
      this->get_corresponding_input(const_cast<const bNodeTree &>(tree), output_bnode));
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L510—L514</summary>

<!-- original:20da66296be8ad:source/blender/blenkernel/intern/node_tree_zones.cc:510:514 -->

```cpp
bNode *bNodeZoneType::get_corresponding_input(bNodeTree &tree, const bNode &output_bnode) const
{
  return const_cast<bNode *>(
      this->get_corresponding_input(const_cast<const bNodeTree &>(tree), output_bnode));
}
```

</details>

**结果出口**

- `return const_cast<bNode *>(`

**继续追踪实现**

- `this->get_corresponding_input` → [blender::bke::bNodeZoneType::get_corresponding_input · L492](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-d7ac9d8e56bbc9bb)；[blender::bke::bNodeZoneType::get_corresponding_input · L510](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-b4b9326f710ef601)。同名重载需按实参类型选择。

<a id="f-03562d1ac0958424"></a>

### `blender::bke::bNodeZoneType::get_corresponding_output`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L516—L520。

接口参数：

- `bNodeTree &tree`
- `const bNode &input_bnode`

**教学注释版**

<!-- annotated:f752fe610af185 -->

```cpp
bNode *bNodeZoneType::get_corresponding_output(bNodeTree &tree, const bNode &input_bnode) const
{
  return const_cast<bNode *>(
      this->get_corresponding_output(const_cast<const bNodeTree &>(tree), input_bnode));
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L516—L520</summary>

<!-- original:f752fe610af185:source/blender/blenkernel/intern/node_tree_zones.cc:516:520 -->

```cpp
bNode *bNodeZoneType::get_corresponding_output(bNodeTree &tree, const bNode &input_bnode) const
{
  return const_cast<bNode *>(
      this->get_corresponding_output(const_cast<const bNodeTree &>(tree), input_bnode));
}
```

</details>

**结果出口**

- `return const_cast<bNode *>(`

**继续追踪实现**

- `this->get_corresponding_output` → [blender::bke::bNodeZoneType::get_corresponding_output · L504](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-b4cf6a6324d9b816)；[blender::bke::bNodeZoneType::get_corresponding_output · L516](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-03562d1ac0958424)。同名重载需按实参类型选择。

<a id="f-bb78e1d32e6e7795"></a>

### `blender::bke::get_zone_types_vector`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L522—L526。

**教学注释版**

<!-- annotated:942f605b6da65b -->

```cpp
static Vector<const bNodeZoneType *> &get_zone_types_vector()
{
  static Vector<const bNodeZoneType *> zone_types;
  return zone_types;
};
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L522—L526</summary>

<!-- original:942f605b6da65b:source/blender/blenkernel/intern/node_tree_zones.cc:522:526 -->

```cpp
static Vector<const bNodeZoneType *> &get_zone_types_vector()
{
  static Vector<const bNodeZoneType *> zone_types;
  return zone_types;
};
```

</details>

**结果出口**

- `return zone_types;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-5d8e901f52f6d1b6"></a>

### `blender::bke::all_zone_types`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L533—L536。

**教学注释版**

<!-- annotated:108571b914c66a -->

```cpp
Span<const bNodeZoneType *> all_zone_types()
{
  return get_zone_types_vector();
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L533—L536</summary>

<!-- original:108571b914c66a:source/blender/blenkernel/intern/node_tree_zones.cc:533:536 -->

```cpp
Span<const bNodeZoneType *> all_zone_types()
{
  return get_zone_types_vector();
}
```

</details>

**结果出口**

- `return get_zone_types_vector();`

**继续追踪实现**

- `get_zone_types_vector` → [blender::bke::get_zone_types_vector · L522](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-bb78e1d32e6e7795)。

<a id="f-71714be31c5b4385"></a>

### `blender::bke::all_zone_input_node_types`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L551—L561。

**教学注释版**

<!-- annotated:5f44b4cdb5bc59 -->

```cpp
Span<int> all_zone_input_node_types()
{
  static const Vector<int> node_types = []() {
    Vector<int> node_types;
    for (const bNodeZoneType *zone_type : all_zone_types()) {
      // [讲解] node_types.append：在尾部建立新元素，必要时先扩大存储。
      node_types.append(zone_type->input_type);
    }
    return node_types;
  }();
  return node_types;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L551—L561</summary>

<!-- original:5f44b4cdb5bc59:source/blender/blenkernel/intern/node_tree_zones.cc:551:561 -->

```cpp
Span<int> all_zone_input_node_types()
{
  static const Vector<int> node_types = []() {
    Vector<int> node_types;
    for (const bNodeZoneType *zone_type : all_zone_types()) {
      node_types.append(zone_type->input_type);
    }
    return node_types;
  }();
  return node_types;
}
```

</details>

**结果出口**

- `return node_types;`

**继续追踪实现**

- `[]() { Vector<int> node_types; for (const bNodeZoneType *zone_type : all_zone_types()) { node_types.append(zone_type->input_type); } return node_types; }` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L553。
- `all_zone_types` → [blender::bke::all_zone_types · L533](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-5d8e901f52f6d1b6)。
- `node_types.append` → [blender::Vector::append · L498](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-591e0b15e6308532)。同名重载需按实参类型选择。

<a id="f-414886f235d25392"></a>

### `blender::bke::all_zone_output_node_types`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L563—L573。

**教学注释版**

<!-- annotated:e184d37ea94a15 -->

```cpp
Span<int> all_zone_output_node_types()
{
  static const Vector<int> node_types = []() {
    Vector<int> node_types;
    for (const bNodeZoneType *zone_type : all_zone_types()) {
      // [讲解] node_types.append：在尾部建立新元素，必要时先扩大存储。
      node_types.append(zone_type->output_type);
    }
    return node_types;
  }();
  return node_types;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L563—L573</summary>

<!-- original:e184d37ea94a15:source/blender/blenkernel/intern/node_tree_zones.cc:563:573 -->

```cpp
Span<int> all_zone_output_node_types()
{
  static const Vector<int> node_types = []() {
    Vector<int> node_types;
    for (const bNodeZoneType *zone_type : all_zone_types()) {
      node_types.append(zone_type->output_type);
    }
    return node_types;
  }();
  return node_types;
}
```

</details>

**结果出口**

- `return node_types;`

**继续追踪实现**

- `[]() { Vector<int> node_types; for (const bNodeZoneType *zone_type : all_zone_types()) { node_types.append(zone_type->output_type); } return node_types; }` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L565。
- `all_zone_types` → [blender::bke::all_zone_types · L533](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-5d8e901f52f6d1b6)。
- `node_types.append` → [blender::Vector::append · L498](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-591e0b15e6308532)。同名重载需按实参类型选择。

<a id="f-e15b3588965609cf"></a>

### `blender::bke::zone_type_by_node_type`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L575—L583。

接口参数：

- `const int node_type`

**教学注释版**

<!-- annotated:c7f7d4febaae31 -->

```cpp
const bNodeZoneType *zone_type_by_node_type(const int node_type)
{
  for (const bNodeZoneType *zone_type : all_zone_types()) {
    if (ELEM(node_type, zone_type->input_type, zone_type->output_type)) {
      return zone_type;
    }
  }
  return nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L575—L583</summary>

<!-- original:c7f7d4febaae31:source/blender/blenkernel/intern/node_tree_zones.cc:575:583 -->

```cpp
const bNodeZoneType *zone_type_by_node_type(const int node_type)
{
  for (const bNodeZoneType *zone_type : all_zone_types()) {
    if (ELEM(node_type, zone_type->input_type, zone_type->output_type)) {
      return zone_type;
    }
  }
  return nullptr;
}
```

</details>

**结果出口**

- `return zone_type;`
- `return nullptr;`

**继续追踪实现**

- `all_zone_types` → [blender::bke::all_zone_types · L533](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-5d8e901f52f6d1b6)。
- `ELEM` → [ELEM · L88](%E4%BE%9D%E8%B5%96-GHOST_utildefines-34b996.md#m-d28724a15928)；[ELEM · L135](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_utildefines-293a0a.md#m-d6572de7cae0)。宏定义由构建条件选择。

<a id="f-bbefd398fe5fd5b4"></a>

### `blender::bke::bNodeTreeZone::input_node`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L585—L591。

**教学注释版**

<!-- annotated:9c45f1fc74bbda -->

```cpp
const bNode *bNodeTreeZone::input_node() const
{
  if (!this->input_node_id) {
    return nullptr;
  }
  return this->owner->tree->node_by_id(*this->input_node_id);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L585—L591</summary>

<!-- original:9c45f1fc74bbda:source/blender/blenkernel/intern/node_tree_zones.cc:585:591 -->

```cpp
const bNode *bNodeTreeZone::input_node() const
{
  if (!this->input_node_id) {
    return nullptr;
  }
  return this->owner->tree->node_by_id(*this->input_node_id);
}
```

</details>

**结果出口**

- `return nullptr;`
- `return this->owner->tree->node_by_id(*this->input_node_id);`

**继续追踪实现**

- `this->owner->tree->node_by_id` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L590。

<a id="f-512b761599384e03"></a>

### `blender::bke::bNodeTreeZone::output_node`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L593—L599。

**教学注释版**

<!-- annotated:a9b4340793d2d6 -->

```cpp
const bNode *bNodeTreeZone::output_node() const
{
  if (!this->output_node_id) {
    return nullptr;
  }
  return this->owner->tree->node_by_id(*this->output_node_id);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L593—L599</summary>

<!-- original:a9b4340793d2d6:source/blender/blenkernel/intern/node_tree_zones.cc:593:599 -->

```cpp
const bNode *bNodeTreeZone::output_node() const
{
  if (!this->output_node_id) {
    return nullptr;
  }
  return this->owner->tree->node_by_id(*this->output_node_id);
}
```

</details>

**结果出口**

- `return nullptr;`
- `return this->owner->tree->node_by_id(*this->output_node_id);`

**继续追踪实现**

- `this->owner->tree->node_by_id` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L598。

<a id="f-3805f670cb2a3f01"></a>

### `blender::bke::node_ids_to_vector`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L601—L608。

接口参数：

- `const bNodeTree &tree`
- `const Vector<int> &node_ids`

**教学注释版**

<!-- annotated:3d8e747345e6c4 -->

```cpp
static Vector<const bNode *> node_ids_to_vector(const bNodeTree &tree, const Vector<int> &node_ids)
{
  // [讲解] node_ids.size：用end_减begin_得到活元素数量。
  Vector<const bNode *> nodes(node_ids.size());
  for (const int i : nodes.index_range()) {
    nodes[i] = tree.node_by_id(node_ids[i]);
  }
  return nodes;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L601—L608</summary>

<!-- original:3d8e747345e6c4:source/blender/blenkernel/intern/node_tree_zones.cc:601:608 -->

```cpp
static Vector<const bNode *> node_ids_to_vector(const bNodeTree &tree, const Vector<int> &node_ids)
{
  Vector<const bNode *> nodes(node_ids.size());
  for (const int i : nodes.index_range()) {
    nodes[i] = tree.node_by_id(node_ids[i]);
  }
  return nodes;
}
```

</details>

**沿实际写入检查状态**

- `nodes[i] = tree.node_by_id(node_ids[i]);`

**结果出口**

- `return nodes;`

**继续追踪实现**

- `node_ids.size` → [blender::Vector::size · L780](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/11-Vector%E6%8F%92%E5%85%A5%E5%88%A0%E9%99%A4%E4%B8%8E%E9%87%8D%E6%8E%92.md#f-714773731767349c)。
- `nodes.index_range` → [blender::Vector::index_range · L1026](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/12-Vector%E5%BC%82%E5%B8%B8%E5%AE%89%E5%85%A8%E4%B8%8E%E8%BE%B9%E7%95%8C.md#f-ac29cf36ef185ab9)。
- `tree.node_by_id` → [blender::bNodeTree::node_by_id · L510](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-9ad10482fbea31d4)；[blender::bNodeTree::node_by_id · L517](%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-d25cdfa86a7c2cb1)。同名重载需按实参类型选择。

<a id="f-9bc3a63f6c89cb1a"></a>

### `blender::bke::bNodeTreeZone::child_nodes`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L610—L613。

**教学注释版**

<!-- annotated:bb834c1063d789 -->

```cpp
Vector<const bNode *> bNodeTreeZone::child_nodes() const
{
  return node_ids_to_vector(*this->owner->tree, this->child_node_ids);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L610—L613</summary>

<!-- original:bb834c1063d789:source/blender/blenkernel/intern/node_tree_zones.cc:610:613 -->

```cpp
Vector<const bNode *> bNodeTreeZone::child_nodes() const
{
  return node_ids_to_vector(*this->owner->tree, this->child_node_ids);
}
```

</details>

**结果出口**

- `return node_ids_to_vector(*this->owner->tree, this->child_node_ids);`

**继续追踪实现**

- `node_ids_to_vector` → [blender::bke::node_ids_to_vector · L601](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-3805f670cb2a3f01)。

<a id="f-8068782029a2f908"></a>

### `blender::bke::bNodeTreeZones::nodes_outside_zones`

实现位置：[source/blender/blenkernel/intern/node_tree_zones.cc](../../../../../source/blender/blenkernel/intern/node_tree_zones.cc) · L615—L618。

**教学注释版**

<!-- annotated:72565e0f4b9271 -->

```cpp
Vector<const bNode *> bNodeTreeZones::nodes_outside_zones() const
{
  return node_ids_to_vector(*this->tree, this->node_ids_outside_zones);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/node_tree_zones.cc · L615—L618</summary>

<!-- original:72565e0f4b9271:source/blender/blenkernel/intern/node_tree_zones.cc:615:618 -->

```cpp
Vector<const bNode *> bNodeTreeZones::nodes_outside_zones() const
{
  return node_ids_to_vector(*this->tree, this->node_ids_outside_zones);
}
```

</details>

**结果出口**

- `return node_ids_to_vector(*this->tree, this->node_ids_outside_zones);`

**继续追踪实现**

- `node_ids_to_vector` → [blender::bke::node_ids_to_vector · L601](%E4%BE%9D%E8%B5%96-node_tree_zones-eecd0c.md#f-3805f670cb2a3f01)。
