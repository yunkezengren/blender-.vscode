# 实现依赖专题：source/blender/blenkernel/intern/geometry_set_instances.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::bke::add_final_mesh_as_geometry_component"]:::abstraction
  F1["blender::bke::object_get_evaluated_geometry_set"]:::compute
  F2["blender::bke::Instances::foreach_referenced_geometry"]:::compute
  F3["blender::bke::Instances::ensure_geometry_instances"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F1
  F3 -->|"显式调用"| F1
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
  F["geometry_set_instances.cc实现"]:::compute
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

<a id="f-e778de57ed285ddb"></a>

### `blender::bke::add_final_mesh_as_geometry_component`

实现位置：[source/blender/blenkernel/intern/geometry_set_instances.cc](../../../../../../../source/blender/blenkernel/intern/geometry_set_instances.cc) · L26—L44。

接口参数：

- `const Object &object`
- `GeometrySet &geometry_set`
- `const bool apply_subdiv`

**教学注释版**

<!-- annotated:ceb8837dfc3fa5 -->

```cpp
static void add_final_mesh_as_geometry_component(const Object &object,
                                                 GeometrySet &geometry_set,
                                                 const bool apply_subdiv)
{
  if (apply_subdiv) {
    Mesh *mesh = BKE_modifier_get_evaluated_mesh_from_evaluated_object(
        &const_cast<Object &>(object));

    if (mesh != nullptr) {
      BKE_mesh_wrapper_ensure_mdata(mesh);
      geometry_set.replace_mesh(mesh, GeometryOwnershipType::ReadOnly);
    }
    return;
  }
  Mesh *mesh = BKE_object_get_evaluated_mesh_no_subsurf(&object);
  if (mesh != nullptr) {
    geometry_set.replace_mesh(mesh, GeometryOwnershipType::ReadOnly);
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/geometry_set_instances.cc · L26—L44</summary>

<!-- original:ceb8837dfc3fa5:source/blender/blenkernel/intern/geometry_set_instances.cc:26:44 -->

```cpp
static void add_final_mesh_as_geometry_component(const Object &object,
                                                 GeometrySet &geometry_set,
                                                 const bool apply_subdiv)
{
  if (apply_subdiv) {
    Mesh *mesh = BKE_modifier_get_evaluated_mesh_from_evaluated_object(
        &const_cast<Object &>(object));

    if (mesh != nullptr) {
      BKE_mesh_wrapper_ensure_mdata(mesh);
      geometry_set.replace_mesh(mesh, GeometryOwnershipType::ReadOnly);
    }
    return;
  }
  Mesh *mesh = BKE_object_get_evaluated_mesh_no_subsurf(&object);
  if (mesh != nullptr) {
    geometry_set.replace_mesh(mesh, GeometryOwnershipType::ReadOnly);
  }
}
```

</details>

**继续追踪实现**

- `BKE_modifier_get_evaluated_mesh_from_evaluated_object` → [blender::BKE_modifier_get_evaluated_mesh_from_evaluated_object · L1041](modifier.cc.md#f-75729c35b147b115)。
- `BKE_mesh_wrapper_ensure_mdata` → [blender::BKE_mesh_wrapper_ensure_mdata · L79](mesh_wrapper.cc.md#f-391cdba59bba6a12)。
- `geometry_set.replace_mesh` → [blender::bke::GeometrySet::replace_mesh · L477](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-bf82c30bb38f2007)。
- `BKE_object_get_evaluated_mesh_no_subsurf` → [blender::BKE_object_get_evaluated_mesh_no_subsurf · L4419](object.cc.md#f-7f352b57780250ef)。

<a id="f-47e721147bb67b7f"></a>

### `blender::bke::object_get_evaluated_geometry_set`

实现位置：[source/blender/blenkernel/intern/geometry_set_instances.cc](../../../../../../../source/blender/blenkernel/intern/geometry_set_instances.cc) · L46—L77。

接口参数：

- `const Object &object`
- `const bool apply_subdiv`

**教学注释版**

<!-- annotated:baff5b570620e4 -->

```cpp
GeometrySet object_get_evaluated_geometry_set(const Object &object, const bool apply_subdiv)
{
  if (!DEG_object_geometry_is_evaluated(object)) {
    return {};
  }

  if (object.runtime->geometry_set_eval != nullptr) {
    GeometrySet geometry_set = *object.runtime->geometry_set_eval;
    /* Ensure that subdivision is performed on the CPU. */
    if (geometry_set.has_mesh()) {
      add_final_mesh_as_geometry_component(object, geometry_set, apply_subdiv);
    }
    return geometry_set;
  }

  /* Otherwise, construct a new geometry set with the component based on the object type. */
  if (object.type == OB_MESH) {
    GeometrySet geometry_set;
    add_final_mesh_as_geometry_component(object, geometry_set, apply_subdiv);
    return geometry_set;
  }
  if (object.type == OB_EMPTY && object.instance_collection != nullptr) {
    Collection &collection = *object.instance_collection;
    // [讲解] std::make_unique<Instances>：创建独占拥有的对象，拥有关系可移动，get返回的借用指针不自动延长寿命。
    auto instances = std::make_unique<Instances>(1);
    instances->reference_handles_for_write().first() = instances->add_reference(collection);
    instances->transforms_for_write().first() = float4x4::identity();
    // [讲解] std::move：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
    return GeometrySet::from_instances(std::move(instances));
  }

  /* Return by value since there is not always an existing geometry set owned elsewhere to use. */
  return {};
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/geometry_set_instances.cc · L46—L77</summary>

<!-- original:baff5b570620e4:source/blender/blenkernel/intern/geometry_set_instances.cc:46:77 -->

```cpp
GeometrySet object_get_evaluated_geometry_set(const Object &object, const bool apply_subdiv)
{
  if (!DEG_object_geometry_is_evaluated(object)) {
    return {};
  }

  if (object.runtime->geometry_set_eval != nullptr) {
    GeometrySet geometry_set = *object.runtime->geometry_set_eval;
    /* Ensure that subdivision is performed on the CPU. */
    if (geometry_set.has_mesh()) {
      add_final_mesh_as_geometry_component(object, geometry_set, apply_subdiv);
    }
    return geometry_set;
  }

  /* Otherwise, construct a new geometry set with the component based on the object type. */
  if (object.type == OB_MESH) {
    GeometrySet geometry_set;
    add_final_mesh_as_geometry_component(object, geometry_set, apply_subdiv);
    return geometry_set;
  }
  if (object.type == OB_EMPTY && object.instance_collection != nullptr) {
    Collection &collection = *object.instance_collection;
    auto instances = std::make_unique<Instances>(1);
    instances->reference_handles_for_write().first() = instances->add_reference(collection);
    instances->transforms_for_write().first() = float4x4::identity();
    return GeometrySet::from_instances(std::move(instances));
  }

  /* Return by value since there is not always an existing geometry set owned elsewhere to use. */
  return {};
}
```

</details>

**结果出口**

- `return {};`
- `return geometry_set;`
- `return GeometrySet::from_instances(std::move(instances));`

**继续追踪实现**

- `DEG_object_geometry_is_evaluated` → [blender::DEG_object_geometry_is_evaluated · L409](../../06-Depsgraph依赖图/intern/depsgraph_query.cc.md#f-a62f5fc620060b5d)。
- `geometry_set.has_mesh` → [blender::bke::GeometrySet::has_mesh · L321](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-8d9a6e8a3a3c9006)。
- `add_final_mesh_as_geometry_component` → [blender::bke::add_final_mesh_as_geometry_component · L26](geometry_set_instances.cc.md#f-e778de57ed285ddb)。
- `std::make_unique<Instances>` → [外部契约](https://eel.is/c++draft/unique.ptr.create)：创建独占拥有的对象，拥有关系可移动，get返回的借用指针不自动延长寿命。
- `instances->reference_handles_for_write().first` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L70。
- `instances->reference_handles_for_write` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L70。
- `instances->add_reference` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L70。
- `instances->transforms_for_write().first` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L71。
- `instances->transforms_for_write` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L71。
- `float4x4::identity` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L71。
- `GeometrySet::from_instances` → [blender::bke::GeometrySet::from_instances · L455](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-0c23a168248fb2cb)；[blender::bke::GeometrySet::from_instances · L462](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-447a100ea7cfda47)。同名重载需按实参类型选择。
- `std::move` → [外部契约](https://eel.is/c++draft/utility.forward)：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。

<a id="f-f22fd0d0114d3f20"></a>

### `blender::bke::Instances::foreach_referenced_geometry`

实现位置：[source/blender/blenkernel/intern/geometry_set_instances.cc](../../../../../../../source/blender/blenkernel/intern/geometry_set_instances.cc) · L79—L109。

接口参数：

- `FunctionRef<void(const GeometrySet &geometry_set)> callback`
- `const GeometrySet &geometry_set`

**教学注释版**

<!-- annotated:ed1a0ffa3b5bb2 -->

```cpp
void Instances::foreach_referenced_geometry(
    FunctionRef<void(const GeometrySet &geometry_set)> callback) const
{
  for (const InstanceReference &reference : references_) {
    switch (reference.type()) {
      case InstanceReference::Type::Object: {
        const Object &object = reference.object();
        const GeometrySet object_geometry_set = object_get_evaluated_geometry_set(object);
        callback(object_geometry_set);
        break;
      }
      case InstanceReference::Type::Collection: {
        Collection &collection = reference.collection();
        FOREACH_COLLECTION_OBJECT_RECURSIVE_BEGIN (&collection, object) {
          const GeometrySet object_geometry_set = object_get_evaluated_geometry_set(*object);
          callback(object_geometry_set);
        }
        FOREACH_COLLECTION_OBJECT_RECURSIVE_END;
        break;
      }
      case InstanceReference::Type::GeometrySet: {
        const GeometrySet &instance_geometry_set = reference.geometry_set();
        callback(instance_geometry_set);
        break;
      }
      case InstanceReference::Type::None: {
        break;
      }
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/geometry_set_instances.cc · L79—L109</summary>

<!-- original:ed1a0ffa3b5bb2:source/blender/blenkernel/intern/geometry_set_instances.cc:79:109 -->

```cpp
void Instances::foreach_referenced_geometry(
    FunctionRef<void(const GeometrySet &geometry_set)> callback) const
{
  for (const InstanceReference &reference : references_) {
    switch (reference.type()) {
      case InstanceReference::Type::Object: {
        const Object &object = reference.object();
        const GeometrySet object_geometry_set = object_get_evaluated_geometry_set(object);
        callback(object_geometry_set);
        break;
      }
      case InstanceReference::Type::Collection: {
        Collection &collection = reference.collection();
        FOREACH_COLLECTION_OBJECT_RECURSIVE_BEGIN (&collection, object) {
          const GeometrySet object_geometry_set = object_get_evaluated_geometry_set(*object);
          callback(object_geometry_set);
        }
        FOREACH_COLLECTION_OBJECT_RECURSIVE_END;
        break;
      }
      case InstanceReference::Type::GeometrySet: {
        const GeometrySet &instance_geometry_set = reference.geometry_set();
        callback(instance_geometry_set);
        break;
      }
      case InstanceReference::Type::None: {
        break;
      }
    }
  }
}
```

</details>

**继续追踪实现**

- `reference.type` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L83。
- `reference.object` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L85。
- `object_get_evaluated_geometry_set` → [blender::bke::object_get_evaluated_geometry_set · L46](geometry_set_instances.cc.md#f-47e721147bb67b7f)。
- `callback` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L87。
- `reference.collection` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L91。
- `FOREACH_COLLECTION_OBJECT_RECURSIVE_BEGIN` → [FOREACH_COLLECTION_OBJECT_RECURSIVE_BEGIN · L485](../BKE_collection.hh.md#m-056dd72ee5fb)。宏定义由构建条件选择。
- `reference.geometry_set` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L100。

<a id="f-c6c307192970c4f3"></a>

### `blender::bke::Instances::ensure_geometry_instances`

实现位置：[source/blender/blenkernel/intern/geometry_set_instances.cc](../../../../../../../source/blender/blenkernel/intern/geometry_set_instances.cc) · L111—L170。

**教学注释版**

<!-- annotated:dadfa3fdd29abd -->

```cpp
void Instances::ensure_geometry_instances()
{
  Vector<InstanceReference> new_references;
  // [讲解] new_references.reserve：确保可容纳至少min_capacity个元素；当前size和已有元素值不因容量请求本身而增加。
  new_references.reserve(references_.size());
  for (const InstanceReference &reference : references_) {
    switch (reference.type()) {
      case InstanceReference::Type::None: {
        // [讲解] new_references.append：在尾部建立新元素，必要时先扩大存储。
        new_references.append(InstanceReference(GeometrySet{}));
        break;
      }
      case InstanceReference::Type::GeometrySet: {
        /* Those references can stay as their were. */
        new_references.append(reference);
        break;
      }
      case InstanceReference::Type::Object: {
        /* Create a new reference that contains the geometry set of the object. We may want to
         * treat e.g. lamps and similar object types separately here. */
        Object &object = reference.object();
        if (ELEM(object.type, OB_LAMP, OB_CAMERA, OB_SPEAKER, OB_ARMATURE)) {
          new_references.append(InstanceReference(object));
          break;
        }
        GeometrySet object_geometry_set = object_get_evaluated_geometry_set(object);
        object_geometry_set.set_name(BKE_id_name(object.id));
        if (object_geometry_set.has_instances()) {
          object_geometry_set.get_instances_for_write()->ensure_geometry_instances();
        }
        // [讲解] std::move：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
        new_references.append(std::move(object_geometry_set));
        break;
      }
      case InstanceReference::Type::Collection: {
        /* Create a new reference that contains a geometry set that contains all objects from the
         * collection as instances. */
        Collection &collection = reference.collection();

        Vector<Object *, 8> objects;
        FOREACH_COLLECTION_OBJECT_RECURSIVE_BEGIN (&collection, object) {
          objects.append(object);
        }
        FOREACH_COLLECTION_OBJECT_RECURSIVE_END;

        // [讲解] std::make_unique<Instances>：创建独占拥有的对象，拥有关系可移动，get返回的借用指针不自动延长寿命。
        auto instances = std::make_unique<Instances>(objects.size());
        MutableSpan<int> handles = instances->reference_handles_for_write();
        MutableSpan<float4x4> transforms = instances->transforms_for_write();
        for (const int i : objects.index_range()) {
          handles[i] = instances->add_reference(*objects[i]);
          transforms[i] = objects[i]->object_to_world();
          transforms[i].location() -= collection.instance_offset;
        }
        instances->ensure_geometry_instances();
        GeometrySet geometry_set = GeometrySet::from_instances(std::move(instances));
        geometry_set.set_name(BKE_id_name(collection.id));
        new_references.append(std::move(geometry_set));
        break;
      }
    }
  }
  references_ = std::move(new_references);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/geometry_set_instances.cc · L111—L170</summary>

<!-- original:dadfa3fdd29abd:source/blender/blenkernel/intern/geometry_set_instances.cc:111:170 -->

```cpp
void Instances::ensure_geometry_instances()
{
  Vector<InstanceReference> new_references;
  new_references.reserve(references_.size());
  for (const InstanceReference &reference : references_) {
    switch (reference.type()) {
      case InstanceReference::Type::None: {
        new_references.append(InstanceReference(GeometrySet{}));
        break;
      }
      case InstanceReference::Type::GeometrySet: {
        /* Those references can stay as their were. */
        new_references.append(reference);
        break;
      }
      case InstanceReference::Type::Object: {
        /* Create a new reference that contains the geometry set of the object. We may want to
         * treat e.g. lamps and similar object types separately here. */
        Object &object = reference.object();
        if (ELEM(object.type, OB_LAMP, OB_CAMERA, OB_SPEAKER, OB_ARMATURE)) {
          new_references.append(InstanceReference(object));
          break;
        }
        GeometrySet object_geometry_set = object_get_evaluated_geometry_set(object);
        object_geometry_set.set_name(BKE_id_name(object.id));
        if (object_geometry_set.has_instances()) {
          object_geometry_set.get_instances_for_write()->ensure_geometry_instances();
        }
        new_references.append(std::move(object_geometry_set));
        break;
      }
      case InstanceReference::Type::Collection: {
        /* Create a new reference that contains a geometry set that contains all objects from the
         * collection as instances. */
        Collection &collection = reference.collection();

        Vector<Object *, 8> objects;
        FOREACH_COLLECTION_OBJECT_RECURSIVE_BEGIN (&collection, object) {
          objects.append(object);
        }
        FOREACH_COLLECTION_OBJECT_RECURSIVE_END;

        auto instances = std::make_unique<Instances>(objects.size());
        MutableSpan<int> handles = instances->reference_handles_for_write();
        MutableSpan<float4x4> transforms = instances->transforms_for_write();
        for (const int i : objects.index_range()) {
          handles[i] = instances->add_reference(*objects[i]);
          transforms[i] = objects[i]->object_to_world();
          transforms[i].location() -= collection.instance_offset;
        }
        instances->ensure_geometry_instances();
        GeometrySet geometry_set = GeometrySet::from_instances(std::move(instances));
        geometry_set.set_name(BKE_id_name(collection.id));
        new_references.append(std::move(geometry_set));
        break;
      }
    }
  }
  references_ = std::move(new_references);
}
```

</details>

**沿实际写入检查状态**

- `handles[i] = instances->add_reference(*objects[i]);`
- `transforms[i] = objects[i]->object_to_world();`
- `references_ = std::move(new_references);`

**继续追踪实现**

- `new_references.reserve` → [blender::Vector::reserve · L405](../../../01-基础容器与现代CPP/10-Vector扩容与增长.md#f-4cf9c0f00e01102e)。
- `references_.size` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L114。
- `reference.type` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L116。
- `new_references.append` → [blender::Vector::append · L498](../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-591e0b15e6308532)。同名重载需按实参类型选择。
- `InstanceReference` → [blender::bke::InstanceReference::InstanceReference · L25](instances.cc.md#f-087c9bd8d14e53b8)；[blender::bke::InstanceReference::InstanceReference · L31](instances.cc.md#f-3a1a225c151dca34)。同名重载需按实参类型选择。
- `reference.object` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L129。
- `ELEM` → [ELEM · L88](../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-d28724a15928)；[ELEM · L135](../../01-BLI基础库/BLI_utildefines.hh.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `object_get_evaluated_geometry_set` → [blender::bke::object_get_evaluated_geometry_set · L46](geometry_set_instances.cc.md#f-47e721147bb67b7f)。
- `object_geometry_set.set_name` → [blender::bke::GeometrySet::set_name · L805](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-8509f63d0760936e)。
- `BKE_id_name` → [blender::BKE_id_name · L1001](../BKE_lib_id.hh.md#f-b9397f1fe1fcc017)；[blender::BKE_id_name · L1005](../BKE_lib_id.hh.md#f-c026427d13979145)。同名重载需按实参类型选择。
- `object_geometry_set.has_instances` → [blender::bke::GeometrySet::has_instances · L381](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-96f474fc46f602f1)。
- `object_geometry_set.get_instances_for_write()->ensure_geometry_instances` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L137。
- `object_geometry_set.get_instances_for_write` → [blender::bke::GeometrySet::get_instances_for_write · L586](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-e2fefbfed77f753f)。
- `std::move` → [外部契约](https://eel.is/c++draft/utility.forward)：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
- `reference.collection` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L145。
- `FOREACH_COLLECTION_OBJECT_RECURSIVE_BEGIN` → [FOREACH_COLLECTION_OBJECT_RECURSIVE_BEGIN · L485](../BKE_collection.hh.md#m-056dd72ee5fb)。宏定义由构建条件选择。
- `objects.append` → [blender::Vector::append · L498](../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-591e0b15e6308532)。同名重载需按实参类型选择。
- `std::make_unique<Instances>` → [外部契约](https://eel.is/c++draft/unique.ptr.create)：创建独占拥有的对象，拥有关系可移动，get返回的借用指针不自动延长寿命。
- `objects.size` → [blender::Vector::size · L780](../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-714773731767349c)。
- `instances->reference_handles_for_write` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L154。
- `instances->transforms_for_write` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L155。
- `objects.index_range` → [blender::Vector::index_range · L1026](../../../01-基础容器与现代CPP/12-Vector异常安全与边界.md#f-ac29cf36ef185ab9)。
- `instances->add_reference` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L157。
- `objects[i]->object_to_world` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L158。
- `transforms[i].location` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L159。
- `instances->ensure_geometry_instances` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L161。
- `GeometrySet::from_instances` → [blender::bke::GeometrySet::from_instances · L455](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-0c23a168248fb2cb)；[blender::bke::GeometrySet::from_instances · L462](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-447a100ea7cfda47)。同名重载需按实参类型选择。
- `geometry_set.set_name` → [blender::bke::GeometrySet::set_name · L805](../../../06-隐式共享与缓存系统/05-GeometrySet读写与复制.md#f-8509f63d0760936e)。
