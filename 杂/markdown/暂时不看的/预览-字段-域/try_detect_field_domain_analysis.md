# `try_detect_field_domain` 函数详细分析与改进建议

## 建议的核心思想

### 1. "如果没有任何 field-inputs 有非 Instance 的 preferred_domain"

**含义：**
- 检查字段的所有输入节点
- 如果所有输入节点的 `preferred_domain` 都是 `Instance` 或 `nullopt`
- 那么可以安全地在实例域上评估字段

**示例：**

```cpp
// 场景 1：可以评估在实例域
GField instance_transform = field_input::instance_transform();
// 输入节点：InstanceTransformFieldInput
// preferred_domain: Instance
// ✅ 可以在实例域评估

// 场景 2：不能评估在实例域
GField position = field_input::position();
// 输入节点：PositionFieldInput
// preferred_domain: Point（在引用的几何体上）
// ❌ 不能在实例域评估

// 场景 3：混合字段，不能评估在实例域
GField mixed = instance_transform + position;
// 输入节点：
//   - InstanceTransformFieldInput (preferred_domain: Instance)
//   - PositionFieldInput (preferred_domain: Point)
// ❌ 有非 Instance 的 preferred_domain，不能在实例域评估
```

### 2. "并且有顶层实例"

**含义：**
- 实例组件必须非空
- 必须有实际的实例存在

**示例：**

```cpp
// 场景 1：有实例
InstancesComponent {
  instances_num = 100  // ✅ 可以在实例域评估
}

// 场景 2：空实例
InstancesComponent {
  instances_num = 0  // ❌ 不能在实例域评估
}
```

### 3. "如果字段在实例域上评估，不需要调用 modify_geometry_sets"

**含义：**
- `foreach_real_geometry` 会递归处理所有嵌套的几何体
- 但如果字段只在实例域上评估，只需要处理顶层实例
- 不需要递归到嵌套的几何体

**示例：**

```cpp
// 几何体结构
GeometrySet {
  InstancesComponent: [
    引用 Mesh A (100 个实例)
    引用 GeometrySet {
      InstancesComponent: [
        引用 Mesh B (50 个实例)
      ]
    }
  ]
}

// 场景 1：字段在实例域评估
GField instance_id = field_input::instance_id();
// 只需要评估 100 个顶层实例
// 不需要递归到嵌套的 GeometrySet
// ❌ 不需要调用 foreach_real_geometry

// 场景 2：字段在点域评估
GField position = field_input::position();
// 需要评估：
//   - Mesh A 的所有点
//   - Mesh B 的所有点（在嵌套的 GeometrySet 中）
// ✅ 需要调用 foreach_real_geometry
```

---

## 第一部分：域推断的妥协方案

### 当前实现的问题

```cpp
// geometry_fields.cc:1018-1020
if (component_type == GeometryComponent::Type::Instance) {
  return AttrDomain::Instance;  // ❌ 总是返回 Instance
}
```

**问题：**
- 没有分析字段的实际依赖
- 对于引用几何体的属性，返回 `Instance` 是错误的

### 改进的妥协方案

```cpp
if (component_type == GeometryComponent::Type::Instance) {
  const InstancesComponent &instances_component = static_cast<const InstancesComponent &>(component);
  const Instances *instances = instances_component.get();
  if (instances == nullptr || instances->instances_num() == 0) {
    return std::nullopt;  // 没有实例，无法推断
  }

  // 检查所有输入节点的 preferred_domain
  for (const fn::FieldInput &field_input : field_inputs->deduplicated_nodes) {
    if (const auto *geometry_field_input = dynamic_cast<const GeometryFieldInput *>(&field_input))
    {
      std::optional<AttrDomain> domain = geometry_field_input->preferred_domain(component);

      // 如果有任何输入的 preferred_domain 不是 Instance，返回 nullopt
      if (domain.has_value() && *domain != AttrDomain::Instance) {
        return std::nullopt;  // ❌ 有非 Instance 的域
      }

      if (!handle_domain(domain)) {
        return std::nullopt;
      }
    }
    else if (const auto *instances_field_input = dynamic_cast<const InstancesFieldInput *>(&field_input))
    {
      // InstancesFieldInput 的 preferred_domain 应该是 Instance
      if (!handle_domain(AttrDomain::Instance)) {
        return std::nullopt;
      }
    }
    else {
      return std::nullopt;  // 未知输入类型
    }
  }

  // 所有输入都是 Instance 或 nullopt，可以推断为 Instance
  return output_domain.value_or(AttrDomain::Instance);
}
```

**逻辑：**
1. 检查是否有实例
2. 遍历所有输入节点
3. 如果有任何输入的 `preferred_domain` 是非 `Instance` 的值，返回 `nullopt`
4. 如果所有输入都是 `Instance` 或 `nullopt`，返回 `Instance`

---

## 第二部分：避免不必要的 `foreach_real_geometry` 调用

### 当前实现的问题

```cpp
// node_geo_viewer.cc:348-374
else {
  geometry::foreach_real_geometry(geometry, [&](GeometrySet &geometry) {
    // 处理所有真实几何体
  });
}
```

**问题：**
- 即使字段只在实例域上评估，也会调用 `foreach_real_geometry`
- `foreach_real_geometry` 会递归处理所有嵌套的几何体
- 这是不必要的开销

### 改进方案

```cpp
// 检查是否可以在实例域上评估
bool can_evaluate_on_instance = false;
if (geometry.has_instances()) {
  bke::GeometryComponent &component = geometry.get_component_for_write<bke::InstancesComponent>();

  // 尝试推断域
  if (const std::optional<AttrDomain> domain = bke::try_detect_field_domain(component, field)) {
    if (*domain == AttrDomain::Instance) {
      can_evaluate_on_instance = true;
    }
  }
}

if (can_evaluate_on_instance) {
  // 只在实例域上评估，不需要递归处理
  bke::GeometryComponent &component = geometry.get_component_for_write<bke::InstancesComponent>();
  AttrDomain used_domain = AttrDomain::Instance;
  bke::try_capture_field_on_geometry(component, viewer_attribute_name, used_domain, field);
}
else {
  // 需要在其他域上评估，递归处理所有几何体
  geometry::foreach_real_geometry(geometry, [&](GeometrySet &geometry) {
    // 处理所有真实几何体
  });
}
```

**逻辑：**
1. 检查是否可以在实例域上评估
2. 如果可以，直接在实例组件上捕获字段
3. 如果不可以，调用 `foreach_real_geometry` 递归处理

---

## 完整的实现方案

### 步骤 1：改进 `try_detect_field_domain`

```cpp
std::optional<AttrDomain> try_detect_field_domain(const GeometryComponent &component,
                                                  const fn::GField &field)
{
  const GeometryComponent::Type component_type = component.type();

  // 简单类型快速返回
  if (component_type == GeometryComponent::Type::PointCloud) {
    return AttrDomain::Point;
  }
  if (component_type == GeometryComponent::Type::GreasePencil) {
    return AttrDomain::Layer;
  }

  // 实例类型的特殊处理
  if (component_type == GeometryComponent::Type::Instance) {
    const InstancesComponent &instances_component = static_cast<const InstancesComponent &>(component);
    const Instances *instances = instances_component.get();

    // 没有实例，无法推断
    if (instances == nullptr || instances->instances_num() == 0) {
      return std::nullopt;
    }

    // 获取字段输入
    const std::shared_ptr<const fn::FieldInputs> &field_inputs = field.node().field_inputs();
    if (!field_inputs) {
      return std::nullopt;
    }

    std::optional<AttrDomain> output_domain;
    auto handle_domain = [&](const std::optional<AttrDomain> domain) {
      if (!domain.has_value()) {
        return false;
      }
      if (output_domain.has_value()) {
        if (*output_domain != *domain) {
          return false;  // 域冲突
        }
        return true;
      }
      output_domain = domain;
      return true;
    };

    // 遍历所有输入节点
    for (const fn::FieldInput &field_input : field_inputs->deduplicated_nodes) {
      if (const auto *geometry_field_input = dynamic_cast<const GeometryFieldInput *>(&field_input))
      {
        std::optional<AttrDomain> domain = geometry_field_input->preferred_domain(component);

        // 如果有非 Instance 的域，返回 nullopt
        if (domain.has_value() && *domain != AttrDomain::Instance) {
          return std::nullopt;
        }

        if (!handle_domain(domain)) {
          return std::nullopt;
        }
      }
      else if (const auto *instances_field_input = dynamic_cast<const InstancesFieldInput *>(&field_input))
      {
        // InstancesFieldInput 默认在实例域上
        if (!handle_domain(AttrDomain::Instance)) {
          return std::nullopt;
        }
      }
      else {
        return std::nullopt;  // 未知输入类型
      }
    }

    // 所有输入都是 Instance 或 nullopt
    return output_domain.value_or(AttrDomain::Instance);
  }

  // Mesh 和 Curve 的现有处理...
  // ...
}
```

### 步骤 2：改进 `node_geo_viewer.cc` 的域处理

```cpp
static void log_viewer_attribute(const bNode &node, geo_eval_log::ViewerNodeLog &r_log)
{
  const auto &storage = *static_cast<NodeGeometryViewer *>(node.storage);
  const StringRef viewer_attribute_name = ".viewer";
  std::optional<int> last_geometry_identifier;

  for (const int i : IndexRange(storage.items_num)) {
    // ... 获取几何体和字段 ...

    const AttrDomain domain_or_auto = AttrDomain(storage.domain);

    // 分支 1：显式选择 Instance 域
    if (domain_or_auto == AttrDomain::Instance) {
      if (geometry.has_instances()) {
        bke::GeometryComponent &component =
            geometry.get_component_for_write<bke::InstancesComponent>();
        bke::try_capture_field_on_geometry(
            component, viewer_attribute_name, AttrDomain::Instance, field);
      }
    }
    // 分支 2：Auto 或其他域
    else {
      // 检查是否可以在实例域上评估
      bool can_evaluate_on_instance = false;
      if (domain_or_auto == AttrDomain::Auto && geometry.has_instances()) {
        bke::GeometryComponent &component = geometry.get_component_for_write<bke::InstancesComponent>();
        if (const std::optional<AttrDomain> domain = bke::try_detect_field_domain(component, field)) {
          if (*domain == AttrDomain::Instance) {
            can_evaluate_on_instance = true;
          }
        }
      }

      if (can_evaluate_on_instance) {
        // 只在实例域上评估，不需要递归
        bke::GeometryComponent &component = geometry.get_component_for_write<bke::InstancesComponent>();
        bke::try_capture_field_on_geometry(
            component, viewer_attribute_name, AttrDomain::Instance, field);
      }
      else {
        // 需要在其他域上评估，递归处理
        geometry::foreach_real_geometry(geometry, [&](GeometrySet &geometry) {
          for (const bke::GeometryComponent::Type type :
               {bke::GeometryComponent::Type::Mesh,
                bke::GeometryComponent::Type::PointCloud,
                bke::GeometryComponent::Type::Curve,
                bke::GeometryComponent::Type::GreasePencil})
          {
            if (!geometry.has(type)) {
              continue;
            }
            bke::GeometryComponent &component = geometry.get_component_for_write(type);
            AttrDomain used_domain = domain_or_auto;
            if (domain_or_auto == AttrDomain::Auto) {
              if (const std::optional<AttrDomain> domain = bke::try_detect_field_domain(component, field)) {
                used_domain = *domain;
              }
              else {
                used_domain = AttrDomain::Point;
              }
            }
            bke::try_capture_field_on_geometry(component, viewer_attribute_name, used_domain, field);
          }
        });
      }
    }

    last_geometry_identifier.reset();
  }
}
```

---

## 示例场景分析

### 场景 1：实例的变换矩阵

```cpp
GField transform = field_input::instance_transform();

// try_detect_field_domain:
// component_type = Instance
// instances_num = 100
// field_inputs = [InstanceTransformFieldInput]
// InstanceTransformFieldInput::preferred_domain() → Instance
// ✅ 返回 AttrDomain::Instance

// node_geo_viewer.cc:
// can_evaluate_on_instance = true
// 直接在实例组件上捕获字段
// ❌ 不需要调用 foreach_real_geometry
```

### 场景 2：位置字段

```cpp
GField position = field_input::position();

// try_detect_field_domain:
// component_type = Instance
// instances_num = 100
// field_inputs = [PositionFieldInput]
// PositionFieldInput::preferred_domain() → Point
// ❌ 有非 Instance 的域，返回 nullopt

// node_geo_viewer.cc:
// can_evaluate_on_instance = false
// 调用 foreach_real_geometry
// ✅ 递归处理所有几何体
```

### 场景 3：混合字段

```cpp
GField mixed = instance_transform + position;

// try_detect_field_domain:
// component_type = Instance
// instances_num = 100
// field_inputs = [InstanceTransformFieldInput, PositionFieldInput]
// InstanceTransformFieldInput::preferred_domain() → Instance
// PositionFieldInput::preferred_domain() → Point
// ❌ 域冲突，返回 nullopt

// node_geo_viewer.cc:
// can_evaluate_on_instance = false
// 调用 foreach_real_geometry
// ✅ 递归处理所有几何体
```

### 场景 4：实例的自定义属性

```cpp
GField scale = field_input::attribute("scale");

// try_detect_field_domain:
// component_type = Instance
// instances_num = 100
// field_inputs = [AttributeFieldInput]
// AttributeFieldInput::preferred_domain() → nullopt（不知道域）
// ✅ 返回 AttrDomain::Instance（默认）

// node_geo_viewer.cc:
// can_evaluate_on_instance = true
// 直接在实例组件上捕获字段
// ❌ 不需要调用 foreach_real_geometry
```

---

## 优势

### 1. 更准确的域推断
- 分析字段的实际依赖
- 避免错误的域推断

### 2. 性能优化
- 对于实例域的字段，避免递归处理
- 减少不必要的计算

### 3. 一致性
- 与 Mesh/Curve 的处理保持一致
- 使用相同的域推断逻辑

### 4. 灵活性
- 支持混合字段（域冲突时回退到递归处理）
- 支持实例的自定义属性

---

## 需要的额外工作

### 1. 添加 `InstancesFieldInput::preferred_domain`

```cpp
class InstancesFieldInput : public fn::FieldInput {
public:
  // ... 现有代码 ...

  virtual std::optional<AttrDomain> preferred_domain(const Instances &instances) const {
    return std::nullopt;  // 默认返回 nullopt
  }
};
```

### 2. 为具体的实例字段输入实现 `preferred_domain`

```cpp
class InstanceTransformFieldInput : public InstancesFieldInput {
public:
  std::optional<AttrDomain> preferred_domain(const Instances &instances) const override {
    return AttrDomain::Instance;  // 变换只在实例域上有意义
  }
};

class InstanceIDFieldInput : public InstancesFieldInput {
public:
  std::optional<AttrDomain> preferred_domain(const Instances &instances) const override {
    return AttrDomain::Instance;  // ID 只在实例域上有意义
  }
};
```

### 3. 添加 `GeometryFieldContext` 的 `instances()` 方法

```cpp
class GeometryFieldContext : public fn::FieldContext {
public:
  // ... 现有代码 ...

  const Instances *instances() const {
    if (type_ == GeometryComponent::Type::Instance) {
      return static_cast<const Instances *>(geometry_);
    }
    return nullptr;
  }
};
```

---

## 总结

### 建议的核心：

1. **妥协的域推断**
   - 如果所有输入节点的 `preferred_domain` 都是 `Instance` 或 `nullopt`
   - 且有顶层实例
   - 则推断为 `Instance` 域

2. **避免不必要的递归**
   - 如果字段只在实例域上评估
   - 不需要调用 `foreach_real_geometry`
   - 直接在实例组件上捕获字段

### 实现步骤：

1. 改进 `try_detect_field_domain` 对实例的处理
2. 添加 `InstancesFieldInput::preferred_domain` 方法
3. 改进 `node_geo_viewer.cc` 的域处理逻辑
4. 为具体的实例字段输入实现 `preferred_domain`

### 优势：

- 更准确的域推断
- 性能优化（避免不必要的递归）
- 与 Mesh/Curve 的处理保持一致
- 支持更复杂的字段组合
