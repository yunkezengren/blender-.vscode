# 08-04 FieldInput输入节点

[方向导航](README.md) · [总目录](../README.md) · [覆盖索引](../%E6%BA%90%E7%A0%81%E7%89%88%E6%9C%AC%E4%B8%8E%E8%A6%86%E7%9B%96%E7%B4%A2%E5%BC%95.md)

> 阅读顺序：问题与数据模型 → 语法与类型 → 源码逐行 → 调用线索 → 历史与取舍 → 推演和练习。

- 基准 HEAD：`cbda6b96c26c0dee3c3b5cbb93960c4ac06a6b30`。
- 记录日期：2026-10-14。
- 教学示例状态：正文中的推演不是本机性能实测；已运行练习见验收报告。

## 一、从问题到设计

输入如何从上下文读取不同几何数据？

输入节点表示需求，实际数据由上下文解析；同一个输入对象不固定绑定某一网格地址。

本篇把语法、数据语义和系统取舍连接起来。Field表达式、求值上下文、mask与结果存储各自有独立职责和生命周期。

### 本篇独立模型与设计推理

FieldInput表示某类输入需求，不等同于保存一个具体数组。

设计取舍：共享输入对象可减少分配，但其数据必须仍由本轮上下文提供。

最小反例：输入实现缓存上一次Context里的裸数组地址并用于下一次不同Context。

推导与处理：缓存必须按环境身份和变化管理，最小实现先不缓存。

```mermaid
flowchart TB
  M["FieldInput表示某类输入需求，不等同于保存<br/>一个具体数组。"]:::data
  T["共享输入对象可减少分配，但其数据必须仍由<br/>本轮上下文提供。"]:::abstraction
  X["输入实现缓存上一次Context里的裸数组地址<br/>并用于下一次不同Context。"]:::error
  A["缓存必须按环境身份和变化管理，最小实现先<br/>不缓存。"]:::result
  M -->|"建立约束"| T
  T -->|"构造反例"| X
  X -->|"恢复不变量"| A
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

### 源码范围与相邻篇章

| 文件 | 本篇逐行范围 | 基准SHA-256 |
|---|---|---|
| [source/blender/functions/FN_field.hh](../../../../../source/blender/functions/FN_field.hh) | L339—L386 | `4ce5d9b67e7b82f22293a3250ae787716e34c6a6b5f1afe561a000eeb6dfa112` |

同一主讲文件可能分多篇覆盖；超出本篇范围的符号通过覆盖索引定位。空行与纯注释保留在源码摘录中，逐行表解释有效语句与语法边界；许可证头统一保留。

前篇：[Field类型接口](03-Field%E7%B1%BB%E5%9E%8B%E6%8E%A5%E5%8F%A3.md).

后篇：[FieldOperation运算节点](05-FieldOperation%E8%BF%90%E7%AE%97%E8%8A%82%E7%82%B9.md).

## 二、类型、数据与阅读地图

```mermaid
flowchart TB
  Q["输入如何从上下文读取不同几何数据？"]:::input
  C0["表达式"]:::abstraction
  C1["上下文"]:::data
  C2["选择集合"]:::data
  C3["批量求值"]:::data
  R["FieldInput输入节点"]:::result
  Q -->|"建立模型"| C0
  C0 -->|"区分职责"| C1
  C1 -->|"区分职责"| C2
  C2 -->|"区分职责"| C3
  C3 -->|"回到源码"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

这是概念依赖图，边表示阅读关系，不声称是运行时调用顺序。

### 直接编译依赖

```mermaid
flowchart LR
  S["FN_field.hh"]:::abstraction
  I0["BLI_cache_mutex.hh"]:::data
  I1["BLI_implicit_sharing_ptr.hh"]:::data
  I2["BLI_vector_set.hh"]:::data
  I3["FN_multi_function.hh"]:::data
  S -->|"直接include"| I0
  S -->|"直接include"| I1
  S -->|"直接include"| I2
  S -->|"直接include"| I3
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

箭头只表示头文件包含关系；完整调用线索见后面的符号定位表。

## 三、关键词、语法与类型角色

### 只读限定 const

const约束当前访问路径可做的修改。const指针、指向const的指针、const视图对象、const元素是不同位置的限定；其他别名可能仍可修改原对象。

具体检查：分别写T* const、const T*与const T* const，并画出不可修改的层次。

### 运行时多态 virtual

虚调用根据实际动态类型选择实现；经基类指针销毁对象时通常需要相应虚析构契约。每元素虚调用和循环外一次分派有不同开销。

具体检查：找出虚接口的实现类和调用频率，再讨论是否值得去虚拟化。

### 覆写检查 override

override要求函数确实覆盖基类虚函数，可捕获参数类型和const限定不匹配。它不改变基类规定的生命周期或线程约束。

具体检查：故意改变一个参数或const，观察编译器如何拒绝误写的新函数。

## 四、真实源码与逐行讲解

源码块保持原行内容，原始行号由小节标题及逐行表给出。表中的调用定位是静态阅读辅助；重载、模板实例化、宏展开和虚调用需结合完整声明，不能仅凭词法出现证明动态调用。

### FN_field.hh：L339—L386

<!-- source:source/blender/functions/FN_field.hh:339:386 -->

```cpp
class FieldInput : public ImplicitSharingMixin {
 protected:
  const CPPType *type_;
  std::string debug_name_;

  /**
   * Field inputs are initialized lazily because it can't be done in the constructor because the
   * derived class constructor has not run yet.
   */
  mutable CacheMutex field_inputs_mutex_;
  mutable FieldInputsPtr field_inputs_;

 public:
  FieldInput(const CPPType &type, std::string debug_name = "");
  ~FieldInput() override;

  StringRefNull debug_name() const;
  virtual std::string socket_inspection_name() const;

  const CPPType &cpp_type() const;

  const FieldInputsPtr &field_inputs() const;

  uint64_t hash() const;
  virtual void hash_unique(UniqueHashBytes &hash, FieldHashDeep &deep_hash_cache) const;

  /**
   * If this #FieldInput depends on other fields, this function should be overridden.
   */
  virtual void foreach_recursive_field(FunctionRef<void(const GField &)> fn) const;

  /**
   * Output a virtual array for the given index mask in the given context.
   */
  virtual GVArray get_varray_for_context(const FieldContext &context,
                                         const IndexMask &mask,
                                         ResourceScope &scope) const = 0;

  void delete_self() override;
};

/**
 * This is an intermediate node in a field tree which executes a #MultiFunction on each value. The
 * #MultiFunction can either be owned or just referenced.
 *
 * It also stores a #GField for every input of the multi-function. Other fields may reference
 * individual outputs.
 */
```

| 原始行 | 语义、约束与检查 |
|---|---|
| L339 | 声明或定义类型 `class FieldInput : public ImplicitSharingMixin`。结合继承、访问权限和成员布局确认接口与拥有关系；前向声明本身没有完整对象布局。 |
| L340 | 切换成员访问权限为 protected；它是编译期接口边界，不是线程同步或内存保护。 |
| L341 | 声明成员、局部对象或完成语句 `const CPPType *type_`。若为指针或引用，它本身不说明拥有；若为值对象，其构造析构由所在作用域或外层对象管理。 |
| L342 | 声明成员、局部对象或完成语句 `std::string debug_name_`。若为指针或引用，它本身不说明拥有；若为值对象，其构造析构由所在作用域或外层对象管理。 |
| L348 | 声明成员、局部对象或完成语句 `mutable CacheMutex field_inputs_mutex_`。若为指针或引用，它本身不说明拥有；若为值对象，其构造析构由所在作用域或外层对象管理。 |
| L349 | 声明成员、局部对象或完成语句 `mutable FieldInputsPtr field_inputs_`。若为指针或引用，它本身不说明拥有；若为值对象，其构造析构由所在作用域或外层对象管理。 |
| L351 | 切换成员访问权限为 public；它是编译期接口边界，不是线程同步或内存保护。 |
| L352 | 把右侧 `"")` 用于初始化或更新左侧 `FieldInput(const CPPType &type, std::string debug_name`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L353 | 涉及析构接口或显式析构：`~FieldInput() override;`。检查目标对象已成功构造，且资源不会在另一条清理路径再次销毁。 |
| L355 | 声明接口 `StringRefNull debug_name() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L356 | 声明接口 `virtual std::string socket_inspection_name() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L358 | 声明接口 `const CPPType &cpp_type() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L360 | 声明接口 `const FieldInputsPtr &field_inputs() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L362 | 声明接口 `uint64_t hash() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L363 | 声明接口 `virtual void hash_unique(UniqueHashBytes &hash, FieldHashDeep &deep_hash_cache) const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L368 | 声明接口 `virtual void foreach_recursive_field(FunctionRef<void(const GField &)> fn) const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L373 | 出现调用或函数声明 `get_varray_for_context`，对应表达式为 `virtual GVArray get_varray_for_context(const FieldContext &context,`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L374 | 本行是连续声明或表达式的一部分：`const IndexMask &mask,`。与本段前后行合读；逗号、括号和限定符决定它属于参数、初始化列表还是实际计算。 |
| L375 | 把右侧 `0` 用于初始化或更新左侧 `ResourceScope &scope) const`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L377 | 声明接口 `void delete_self() override`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L378 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |

## 五、接口定位、调用线索与生命周期

### 本篇声明与实现入口

| 源码位置 | 实际声明片段 |
|---|---|
| [FN_field.hh:L339](../../../../../source/blender/functions/FN_field.hh#L339) | `class FieldInput : public ImplicitSharingMixin` |
| [FN_field.hh:L352](../../../../../source/blender/functions/FN_field.hh#L352) | `FieldInput(const CPPType &type, std::string debug_name = "");` |
| [FN_field.hh:L355](../../../../../source/blender/functions/FN_field.hh#L355) | `StringRefNull debug_name() const;` |
| [FN_field.hh:L356](../../../../../source/blender/functions/FN_field.hh#L356) | `virtual std::string socket_inspection_name() const;` |
| [FN_field.hh:L358](../../../../../source/blender/functions/FN_field.hh#L358) | `const CPPType &cpp_type() const;` |
| [FN_field.hh:L360](../../../../../source/blender/functions/FN_field.hh#L360) | `const FieldInputsPtr &field_inputs() const;` |
| [FN_field.hh:L362](../../../../../source/blender/functions/FN_field.hh#L362) | `uint64_t hash() const;` |
| [FN_field.hh:L363](../../../../../source/blender/functions/FN_field.hh#L363) | `virtual void hash_unique(UniqueHashBytes &hash, FieldHashDeep &deep_hash_cache) const;` |
| [FN_field.hh:L368](../../../../../source/blender/functions/FN_field.hh#L368) | `virtual void foreach_recursive_field(FunctionRef<void(const GField &)> fn) const;` |
| [FN_field.hh:L373](../../../../../source/blender/functions/FN_field.hh#L373) | `virtual GVArray get_varray_for_context(const FieldContext &context,` |
| [FN_field.hh:L377](../../../../../source/blender/functions/FN_field.hh#L377) | `void delete_self() override;` |

### 同名符号出现位置

以下表提供跨文件阅读入口，包含声明、调用或测试使用；没有经过完整C++名称解析，不把它命名为已证明的运行时调用图。

| 符号 | 位置 | 文本证据 |
|---|---|---|
| `FieldInput` | [field.cc:L19](../../../../../source/blender/functions/intern/field.cc#L19) | `FieldInput::FieldInput(const CPPType &type, std::string debug_name)` |
| `FieldInput` | [field.cc:L193](../../../../../source/blender/functions/intern/field.cc#L193) | `FieldInput::~FieldInput() = default;` |
| `FieldInput` | [field.cc:L534](../../../../../source/blender/functions/intern/field.cc#L534) | `IndexFieldInput::IndexFieldInput() : FieldInput(CPPType::get<int>(), "Index") {}` |
| `debug_name` | [FN_lazy_function.hh:L224](../../../../../source/blender/functions/FN_lazy_function.hh#L224) | `: debug_name(debug_name), type(&type), usage(usage)` |
| `debug_name` | [FN_lazy_function.hh:L240](../../../../../source/blender/functions/FN_lazy_function.hh#L240) | `Output(const char *debug_name, const CPPType &type) : debug_name(debug_name), type(&type) {}` |
| `debug_name` | [FN_multi_function.hh:L87](../../../../../source/blender/functions/FN_multi_function.hh#L87) | `virtual std::string debug_name() const;` |
| `socket_inspection_name` | [BKE_geometry_fields.hh:L347](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L347) | `std::string socket_inspection_name() const override;` |
| `socket_inspection_name` | [BKE_geometry_fields.hh:L409](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L409) | `std::string socket_inspection_name() const override;` |
| `socket_inspection_name` | [BKE_geometry_fields.hh:L440](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L440) | `std::string socket_inspection_name() const override;` |
| `cpp_type` | [geometry_fields.cc:L630](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L630) | `: bke::GeometryFieldInput(value_field.cpp_type(), "Evaluate at Index"),` |
| `cpp_type` | [geometry_fields.cc:L716](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L716) | `builder.single_output("Value", src_field_.cpp_type());` |
| `cpp_type` | [geometry_fields.cc:L767](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L767) | `: bke::GeometryFieldInput(field.cpp_type(), "Evaluate on Domain"),` |
| `field_inputs` | [geometry_fields.cc:L1205](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L1205) | `const fn::FieldInputsPtr &field_inputs = field.field_inputs();` |
| `field_inputs` | [geometry_fields.cc:L1255](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L1255) | `const fn::FieldInputsPtr &field_inputs = field.field_inputs();` |
| `field_inputs` | [field.cc:L175](../../../../../source/blender/functions/intern/field.cc#L175) | `const FieldInputsPtr &FieldInput::field_inputs() const` |
| `hash` | [BKE_geometry_set.hh:L470](../../../../../source/blender/blenkernel/BKE_geometry_set.hh#L470) | `uint64_t hash() const` |
| `hash` | [BLI_array.hh:L376](../../../../../source/blender/blenlib/BLI_array.hh#L376) | `uint64_t hash() const` |
| `hash` | [BLI_array.hh:L378](../../../../../source/blender/blenlib/BLI_array.hh#L378) | `return this->as_span().hash();` |
| `hash_unique` | [BKE_geometry_fields.hh:L349](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L349) | `void hash_unique(UniqueHashBytes &hash, fn::FieldHashDeep &deep_hash_cache) const override;` |
| `hash_unique` | [BKE_geometry_fields.hh:L381](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L381) | `void hash_unique(UniqueHashBytes &hash, fn::FieldHashDeep &deep_hash_cache) const override;` |
| `hash_unique` | [BKE_geometry_fields.hh:L398](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L398) | `void hash_unique(UniqueHashBytes &hash, fn::FieldHashDeep &deep_hash_cache) const override;` |
| `foreach_recursive_field` | [BKE_geometry_fields.hh:L513](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L513) | `void foreach_recursive_field(FunctionRef<void(const fn::GField &)> fn) const override;` |
| `foreach_recursive_field` | [geometry_fields.cc:L824](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L824) | `void EvaluateOnDomainInput::foreach_recursive_field(FunctionRef<void(const fn::GField &)> fn) const` |
| `foreach_recursive_field` | [field.cc:L195](../../../../../source/blender/functions/intern/field.cc#L195) | `void FieldInput::foreach_recursive_field(FunctionRef<void(const GField &)> ) const {}` |
| `get_varray_for_context` | [BKE_geometry_fields.hh:L255](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L255) | `GVArray get_varray_for_context(const fn::FieldContext &context,` |
| `get_varray_for_context` | [BKE_geometry_fields.hh:L258](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L258) | `virtual GVArray get_varray_for_context(const GeometryFieldContext &context,` |
| `get_varray_for_context` | [BKE_geometry_fields.hh:L267](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L267) | `GVArray get_varray_for_context(const fn::FieldContext &context,` |
| `delete_self` | [BKE_geometry_set.hh:L125](../../../../../source/blender/blenkernel/BKE_geometry_set.hh#L125) | `void delete_self() override;` |
| `delete_self` | [geometry_set.cc:L96](../../../../../source/blender/blenkernel/intern/geometry_set.cc#L96) | `void GeometryComponent::delete_self()` |
| `delete_self` | [BLI_implicit_sharing.hh:L203](../../../../../source/blender/blenlib/BLI_implicit_sharing.hh#L203) | `this->delete_self();` |

### 生命周期推理图

```mermaid
flowchart LR
  O["调用者或源数据拥有者"]:::input
  V["FieldInput输入节点的接口与状态"]:::abstraction
  B["借用地址、引用或视图"]:::data
  W["实际计算或修改"]:::compute
  R["结果与清理责任"]:::result
  O -->|"创建与配置"| V
  O -->|"保障寿命"| B
  B -->|"访问前验证"| W
  V -->|"规定操作"| W
  W -->|"交付或销毁"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

这是审查生命周期的通用模型。具体类是否拥有数据由本篇成员、构造、析构和调用者一起证明；任何箭头都不自动代表shared_ptr。

## 六、把代码放进具体数据中推演

本方向的共同数值模型如下。本篇的专门检查是：实现读取索引的输入，并在不同mask下验证编号。

| 步骤 | 数据或状态 | 为什么需要这一步 |
|---|---|---|
| 表达式 | Position*2+1 | 尚未绑定具体数组 |
| 上下文A | Position=[0,3,5] | 输入有3个元素 |
| 选择 | {0,2} | 只要求元素0和2 |
| 结果A | 1与11 | 元素1不属于本轮要求 |
| 上下文B | Position=[4,7,9] | 复用表达式而改变环境 |
| 结果B | 9与19 | 结果由表达式和上下文共同决定 |

```mermaid
flowchart TB
  T0["Position*2+1"]:::input
  T1["Position=[0,3,5]"]:::compute
  T2["{0,2}"]:::compute
  T3["1与11"]:::compute
  T4["Position=[4,7,9]"]:::compute
  T5["9与19"]:::result
  T0 -->|"上下文A"| T1
  T1 -->|"选择"| T2
  T2 -->|"结果A"| T3
  T3 -->|"上下文B"| T4
  T4 -->|"结果B"| T5
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

图是教学推演模型；精确分支与状态更新以本篇摘录及调用契约为准。

### 本篇独立练习与参考思路

实现读取索引的输入，并在不同mask下验证编号。

参考思路：输入节点表示需求，实际数据由上下文解析；同一个输入对象不固定绑定某一网格地址。

将输入、预期结果和资源责任分成三张清单。先用最直接的实现给出可核对的答案，再替换成对应源码使用的表示；比较结果不变的条件，而不是只比较接口名字。

验收依据：结果与直接计算一致；多个输出共享子表达式时不改变语义；深链构造、执行、销毁三个阶段分别检查。

## 七、复杂度、设计取舍与其他基础库

与表达式模板、AST和闭包比较：Field可在运行时组合并对不同上下文批量求值；不要把Field对象误当作固定几何的结果数组。

本篇的具体取舍：输入节点表示需求，实际数据由上下文解析；同一个输入对象不固定绑定某一网格地址。

| 观察维度 | 从源码取得证据的方法 | 本篇要避免的误判 |
|---|---|---|
| 时间 | 对循环次数、分派次数和重建频率分别计数 | 看到单次常数操作就断定整个操作序列是常数成本 |
| 内存 | 区分对象本体、容量存储、间接资源和共享控制块 | 用sizeof代替总内存 |
| 安全 | 沿构造、失败回滚、销毁与失效逐路径检查 | 把断言或非空指针当作完整安全证明 |
| 并发 | 逐字段确认锁、发布顺序和借用寿命 | 把引用计数线程安全等同数据读写线程安全 |

相关一手资料：

- [C++公开工作草案](https://eel.is/c++draft/)：持续更新的工作草案；语言与标准库语义以相应章节为准。
- [Blender依赖图设计](https://developer.blender.org/docs/features/core/depsgraph/)：包含历史设计背景，当前行为以本地源码为准。

资料用于核对契约和进一步阅读；这里没有声称外部库与Blender实现相同，也没有把上游性能数字当作本机实测。

## 八、历史提交与设计演化

### 2021-09-09 · Jacques Lucke

[Geometry Nodes: fields and anonymous attributes](https://projects.blender.org/blender/blender/commit/bf47fb40fd6f0ee9386e9936cf213a1049c55b61)

完整哈希：`bf47fb40fd6f0ee9386e9936cf213a1049c55b61`。提交标题与作者日期来自本地Git对象。

提交说明原文（历史证据，不能直接作为当前API说明）：

```text
Geometry Nodes: fields and anonymous attributes

This implements the initial core framework for fields and anonymous
attributes (also see T91274).

The new functionality is hidden behind the "Geometry Nodes Fields"
feature flag. When enabled in the user preferences, the following
new nodes become available: `Position`, `Index`, `Normal`,
`Set Position` and `Attribute Capture`.

Socket inspection has not been updated to work with fields yet.

Besides these changes at the user level, this patch contains the
ground work for:
* building and evaluating fields at run-time (`FN_fields.hh`) and
* creating and accessing anonymous attributes on geometry
  (`BKE_anonymous_attribute.h`).

For evaluating fields we use a new so called multi-function procedure
(`FN_multi_function_procedure.hh`). It allows composing multi-functions
in arbitrary ways and supports efficient evaluation as is required by
fields. See `FN_multi_function_procedure.hh` for more details on how
this evaluation mechanism can be used.

A new `AttributeIDRef` has been added which allows handling named
and anonymous attributes in the same way in many places.

Hans and I worked on this patch together.

Differential Revision: https://developer.blender.org/D12414
```

阅读任务：先根据说明复述旧问题，提出一个自己的修复方案，再对照diff。结合本篇重点“输入如何从上下文读取不同几何数据？”判断方案改变的是表示、接口、生命周期还是调度。

### 2026-04-02 · Jacques Lucke

[Refactor: Functions: update field storage and API](https://projects.blender.org/blender/blender/commit/66bee9561ba6b7ce89f0f95f4ed0420360c69924)

完整哈希：`66bee9561ba6b7ce89f0f95f4ed0420360c69924`。提交标题与作者日期来自本地Git对象。

提交说明原文（历史证据，不能直接作为当前API说明）：

```text
Refactor: Functions: update field storage and API

This reimplements the entire field API. Large parts of the API surface is the
same, but how a field is stored has change significantly.

The main motivating goals for this refactor were:
* Support storing single value fields without doing an allocation.
* Support referencing common fields without doing reference counting (e.g. the
  position field).

On top of these goals, a few other improvements were done:
* Field types are not nullable anymore. So one needs to use `std::optional` in
  such cases. This also implies that `GField` can't be default-constructed
  anymore because then it wouldn't have a type.
* Field comparisons are shallow now. Previously one could easily do a deep
  comparison of nested field inputs.
* `GField` now stores a `std::variant` to support different internal storage
  types, making it more easily extensible.

In my test file that is adapted from #156308 I get a speedup from 60ms to 54ms
of the modifier evaluation time.

Pull Request: https://projects.blender.org/blender/blender/pulls/156723
```

阅读任务：先根据说明复述旧问题，提出一个自己的修复方案，再对照diff。结合本篇重点“输入如何从上下文读取不同几何数据？”判断方案改变的是表示、接口、生命周期还是调度。

### 2026-06-01 · Jacques Lucke

[Fix #157485: avoid deep recursion when freeing field trees](https://projects.blender.org/blender/blender/commit/32f550c35ab3ffd89a8e8a602e4045e4091e044c)

完整哈希：`32f550c35ab3ffd89a8e8a602e4045e4091e044c`。提交标题与作者日期来自本地Git对象。

提交说明原文（历史证据，不能直接作为当前API说明）：

```text
Fix #157485: avoid deep recursion when freeing field trees

Destructing large fields could result in deep call stacks because of
long ownership chains. This could result in stack overflows leading
to crashes. The fix is to customize the destruction code a bit so that
it becomes more iterative instead of recursive.

Pull Request: https://projects.blender.org/blender/blender/pulls/159375
```

阅读任务：先根据说明复述旧问题，提出一个自己的修复方案，再对照diff。结合本篇重点“输入如何从上下文读取不同几何数据？”判断方案改变的是表示、接口、生命周期还是调度。

## 九、反例、测试入口与掌握标准

仓库测试入口：

- [FN_field_test.cc](../../../../../source/blender/functions/tests/FN_field_test.cc)：阅读输入、断言与覆盖边界；本篇不把“存在测试”写成“本轮已运行”。

需要实际构造的反例：

- 空输入或没有结果需求：确认接口允许的空状态与不允许访问的操作。
- 边界位置和退化结构：把长度为1、末尾位置、重复值或深链代入真实分支。
- 生命周期结束或修改之后：检查保存的指针、引用、结果视图是否仍有效。
- 与本篇核心不变量相冲突的输入：实现读取索引的输入，并在不同mask下验证编号。

### 可运行的教学参考程序

[reference_exercises.cc](../_tools/reference_exercises.cc)包含独立于Blender的C++20参考检查：视图、简化SmallVector、异常回滚、哈希碰撞与删除、偏移数组、拓扑映射、共享缓存、表达式、惰性分支、闭包和暴力最近邻。

参考程序有意省略生产实现的完整能力。例如SmallVector禁止复制移动容器，不支持只能移动的元素，并禁止append参数别名到自身元素；TinyMap固定8槽，不提供增长。程序通过不能替代Blender实现测试。实际运行结果、编译器与命令见验收报告。

掌握标准：离开源码解释“输入如何从上下文读取不同几何数据？”；独立完成上述练习；能指出一个会破坏表达式相关约束的最小反例，并用具体代码行说明检查或修复应放在哪里。
