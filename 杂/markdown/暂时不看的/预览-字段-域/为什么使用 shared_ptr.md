## 问题 1：为什么使用 `std::shared_ptr`？

### 核心原因：共享所有权和避免复制

#### 1. `FieldNode::field_inputs_` 使用 `std::shared_ptr`

```cpp
class FieldNode {
protected:
  std::shared_ptr<const FieldInputs> field_inputs_;  // 第 74 行
};
```

**为什么使用 `shared_ptr`？**

从注释（第 69-72 行）可以看到：
```cpp
/**
 * Keeps track of inputs that this node depends on. This avoids recomputing it every time
 * data is required. It is a shared pointer, because very often multiple nodes depend on same
 * inputs.
 */
```

**关键点：**
- "very often multiple nodes depend on same inputs"
- **多个节点经常依赖相同的输入**

#### 2. 实际例子

```cpp
// 创建两个字段，都依赖位置输入
GField position_x = field_math::math_operation(
    field_input::position(),  // PositionFieldInput
    math_op::ADD,
    field_input::constant(0.0f)
);

GField position_y = field_math::math_operation(
    field_input::position(),  // 同一个 PositionFieldInput
    math_op::ADD,
    field_input::constant(1.0f)
);

// position_x 和 position_y 的 field_inputs_ 都包含：
// - PositionFieldInput (同一个对象)
```

**如果使用原始指针或引用：**
```cpp
// ❌ 问题：
FieldNode {
  FieldInputs* field_inputs_;  // 需要手动管理生命周期
}

FieldNode {
  FieldInputs& field_inputs_;  // 无法重新绑定，生命周期管理复杂
}
```

**使用 `shared_ptr` 的优势：**
```cpp
// ✅ 优势：
// 1. 自动管理生命周期
// 2. 多个节点共享同一个 FieldInputs
// 3. 当所有节点都销毁时，FieldInputs 自动销毁
// 4. 避免复制 FieldInputs（可能很大）
```

#### 3. `combine_field_inputs` 函数的优化

```cpp
static std::shared_ptr<const FieldInputs> combine_field_inputs(Span<GField> fields)
{
  // 尝试重用现有的 FieldInputs
  const std::shared_ptr<const FieldInputs> *field_inputs_candidate = nullptr;
  for (const GField &field : fields) {
    const std::shared_ptr<const FieldInputs> &field_inputs = field.node().field_inputs();
    if (field_inputs && !field_inputs->nodes.is_empty()) {
      if (field_inputs_candidate == nullptr) {
        field_inputs_candidate = &field_inputs;
      }
      else if ((*field_inputs_candidate)->nodes.size() < field_inputs->nodes.size()) {
        // 重用节点最多的 FieldInputs
        field_inputs_candidate = &field_inputs;
      }
    }
  }

  // 如果所有输入都在候选中，直接重用
  if (inputs_not_in_candidate.is_empty()) {
    return *field_inputs_candidate;  // ✅ 直接返回共享指针，不复制
  }

  // 创建新的 FieldInputs
  std::shared_ptr<FieldInputs> new_field_inputs = std::make_shared<FieldInputs>(
      **field_inputs_candidate);
  // ...
  return new_field_inputs;
}
```

**关键优化：**
- 尝试重用现有的 `FieldInputs`，避免复制
- 如果可能，直接返回共享指针
- 只有在必要时才创建新的 `FieldInputs`

#### 4. `FieldInput` 构造函数的初始化

```cpp
FieldInput::FieldInput(const CPPType &type, std::string debug_name)
    : FieldNode(FieldNodeType::Input), type_(&type), debug_name_(std::move(debug_name))
{
  std::shared_ptr<FieldInputs> field_inputs = std::make_shared<FieldInputs>();
  field_inputs->nodes.add_new(this);
  field_inputs->deduplicated_nodes.add_new(*this);
  field_inputs_ = std::move(field_inputs);  // 移动到成员变量
}
```

**每个 `FieldInput` 节点：**
- 创建自己的 `FieldInputs`
- 包含自己（`nodes.add_new(this)`）
- 其他节点可以共享这个 `FieldInputs`

#### 5. `GField` 使用 `shared_ptr`

```cpp
class GField : public GFieldBase<std::shared_ptr<FieldNode>> {
  // GField 持有 FieldNode 的 shared_ptr
};

// 创建常量字段
GField make_constant_field(const CPPType &type, const void *value)
{
  auto constant_node = std::make_shared<FieldConstant>(type, value);  // shared_ptr
  return GField{std::move(constant_node)};
}
```

**为什么 `GField` 也使用 `shared_ptr`？**

```cpp
// 场景：多个字段共享同一个节点
GField constant1 = fn::make_constant_field<int>(42);
GField constant2 = fn::make_constant_field<int>(42);

// 可能返回同一个 FieldConstant 节点（通过缓存）
// 使用 shared_ptr 可以安全共享

// 场景：字段被复制
GField position = field_input::position();
GField position_copy = position;  // 复制 shared_ptr，共享同一个节点

// 场景：字段作为函数参数传递
void process_field(GField field) {
  // field 持有 FieldNode 的 shared_ptr
  // 当函数返回时，field 销毁
  // 如果没有其他引用，FieldNode 自动销毁
}
```

#### 6. `FieldInputs` 的共享

```cpp
struct FieldInputs {
  VectorSet<const FieldInput *> nodes;
  VectorSet<std::reference_wrapper<const FieldInput>> deduplicated_nodes;
};

// 场景：多个操作节点依赖相同的输入
GField a = field_input::position();
GField b = field_input::normal();

GField c1 = field_math::math_operation(a, math_op::ADD, b);
GField c2 = field_math::math_operation(a, math_op::MUL, b);

// c1 和 c2 的 field_inputs_ 都包含：
// - PositionFieldInput
// - NormalFieldInput
// 使用 shared_ptr 可以共享同一个 FieldInputs
```

### 对比其他智能指针

| 指针类型   | 优点                 | 缺点                 | 适用场景     |
| ------------ | -------------------- | -------------------- | ------------ |
| `raw pointer` | 无开销               | 需要手动管理生命周期 | 不适用       |
| `unique_ptr`  | 独占所有权，无开销   | 无法共享             | 独占资源     |
| `shared_ptr`  | 共享所有权，自动管理 | 有引用计数开销       | **共享资源** ✅  |
| `weak_ptr`    | 打破循环引用         | 需要 lock()          | 解决循环引用 |

**为什么不用 `unique_ptr`？**
```cpp
class FieldNode {
  std::unique_ptr<const FieldInputs> field_inputs_;  // ❌ 无法共享
};

// 问题：
GField a = field_input::position();
GField b = field_input::position();  // 需要创建新的 FieldInputs
// 导致重复，无法优化
```

**为什么不用 `weak_ptr`？**
```cpp
class FieldNode {
  std::weak_ptr<const FieldInputs> field_inputs_;  // ❌ 需要 lock()
};

// 问题：
const FieldInputs* get_inputs() {
  auto locked = field_inputs_.lock();  // 需要 lock()
  if (locked) {
    return locked.get();
  }
  return nullptr;
}
// 每次访问都需要 lock()，开销大
```

---