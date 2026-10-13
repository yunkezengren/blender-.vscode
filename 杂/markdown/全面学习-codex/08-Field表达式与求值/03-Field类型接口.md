# 08-03 Field类型接口

[方向导航](README.md) · [总目录](../README.md) · [覆盖索引](../%E6%BA%90%E7%A0%81%E7%89%88%E6%9C%AC%E4%B8%8E%E8%A6%86%E7%9B%96%E7%B4%A2%E5%BC%95.md)

> 阅读顺序：问题与数据模型 → 语法与类型 → 源码逐行 → 调用线索 → 历史与取舍 → 推演和练习。

- 基准 HEAD：`cbda6b96c26c0dee3c3b5cbb93960c4ac06a6b30`。
- 记录日期：2026-10-14。
- 教学示例状态：正文中的推演不是本机性能实测；已运行练习见验收报告。

## 一、从问题到设计

Field<T>和GField怎样平衡类型安全与通用性？

静态类型包装便于编译期检查，动态形式支持统一容器；转换必须维护真实CPPType一致。

本篇把语法、数据语义和系统取舍连接起来。Field表达式、求值上下文、mask与结果存储各自有独立职责和生命周期。

### 本篇独立模型与设计推理

Field<T>在编译期表达结果类型，GField在运行期保存类型。

设计取舍：通用容器需要动态表示，算法内部常希望恢复静态类型。

最小反例：把数值转换和类型包装转换混为一谈。

推导与处理：先验证类型身份，真正数值转换生成相应运算。

```mermaid
flowchart TB
  M["Field＜T＞在编译期表达结果类型，GField在<br/>运行期保存类型。"]:::data
  T["通用容器需要动态表示，算法内部常希望恢复<br/>静态类型。"]:::abstraction
  X["把数值转换和类型包装转换混为一谈。"]:::error
  A["先验证类型身份，真正数值转换生成相应运算<br/>。"]:::result
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
| [source/blender/functions/FN_field.hh](../../../../../source/blender/functions/FN_field.hh) | L203—L290 | `4ce5d9b67e7b82f22293a3250ae787716e34c6a6b5f1afe561a000eeb6dfa112` |

同一主讲文件可能分多篇覆盖；超出本篇范围的符号通过覆盖索引定位。空行与纯注释保留在源码摘录中，逐行表解释有效语句与语法边界；许可证头统一保留。

前篇：[GField存储表示](02-GField%E5%AD%98%E5%82%A8%E8%A1%A8%E7%A4%BA.md).

后篇：[FieldInput输入节点](04-FieldInput%E8%BE%93%E5%85%A5%E8%8A%82%E7%82%B9.md).

## 二、类型、数据与阅读地图

```mermaid
flowchart TB
  Q["Field＜T＞和GField怎样平衡类型安全与通用<br/>性？"]:::input
  C0["表达式"]:::abstraction
  C1["上下文"]:::data
  C2["选择集合"]:::data
  C3["批量求值"]:::data
  R["Field类型接口"]:::result
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

### 模板 template

模板把类型或常量作为生成实现的参数。读声明时先列出类型参数、非类型参数和默认值，再看使用者实际实例化了什么。模板声明本身不意味着每种T都支持其全部成员。

具体检查：把T替换为int、string、只能移动的类型，分别检查每个被调用操作是否成立。

### 依赖名称 typename

typename既可引入类型模板参数，也可告诉编译器某个依赖名称是类型。它不创建运行时对象；解析期确认语法类别与实例化期检查具体类型是不同阶段。

具体检查：区分typename T::value_type和T::size()，前者标记类型，后者是表达式。

### 只读限定 const

const约束当前访问路径可做的修改。const指针、指向const的指针、const视图对象、const元素是不同位置的限定；其他别名可能仍可修改原对象。

具体检查：分别写T* const、const T*与const T* const，并画出不可修改的层次。

### 判别联合 variant

variant在若干候选类型中保存一个活动值，通过判别信息选择操作。它能把不同表示集中在值类型中，但各分支的复制移动成本不同。

具体检查：列出活动分支及每种分支实际拥有或借用的数据。

### 受控访问 friend

friend授予指定函数或类访问非公开成员的权限，并不意味着继承，也不自动扩展到友元的派生类。

具体检查：解释执行器为何需要访问包装器的内部映射，同时检查边界是否仍清楚。

### 类型别名 using

类型别名为已有类型建立名字，不创建运行期对象。它常把模板内部使用的类型统一暴露给泛型调用者。

具体检查：展开别名直到基础类型，区分类型别名和变量声明。

## 四、真实源码与逐行讲解

源码块保持原行内容，原始行号由小节标题及逐行表给出。表中的调用定位是静态阅读辅助；重载、模板实例化、宏展开和虚调用需结合完整声明，不能仅凭词法出现证明动态调用。

### FN_field.hh：L203—L250

<!-- source:source/blender/functions/FN_field.hh:203:250 -->

```cpp
template<typename T> class Field {
 public:
  using base_type = T;
  using generic_type = GField;

 private:
  /**
   * #Field<T> just stores a #GField. This makes converting between the two types easy.
   */
  GField field_;

  friend GField;

 public:
  /**
   * Unlike #GField, default construction is allowed here, because the type is known without extra
   * arguments.
   */
  Field();

  /** Same as corresponding #GField constructors. */
  explicit Field(FieldInputPtr node);
  explicit Field(FieldOperationPtr node, int output_i = 0);

  /** Construct a field that just outputs the given value. */
  explicit Field(T value);

  /** This is implicitly cast to #GField which is always valid. */
  operator const GField &() const;

  /** These are the same as the corresponding #GField methods. */
  bool depends_on_input() const;
  template<typename InputT, typename... Args> static Field from_input(Args &&...args);
  template<typename InputT> const InputT *get_input_if() const;
  uint64_t hash() const;
  static Field from_non_owning_ref(const Field &field);
};

/**
 * A version of #GField that only references data from other fields but does not own any data
 * itself. This allows it to be smaller and trivially copyable making it more efficient in some
 * contexts. This is mainly used during field evaluation.
 */
class GFieldRef {
 public:
  struct Value {
    const CPPType *type = nullptr;
    const void *value = nullptr;
```

| 原始行 | 语义、约束与检查 |
|---|---|
| L203 | 声明模板参数 `template<typename T> class Field {`。类型参数决定生成操作的类型，非类型参数可决定内嵌容量或编译期分支。 |
| L204 | 切换成员访问权限为 public；它是编译期接口边界，不是线程同步或内存保护。 |
| L205 | 定义类型别名 `using base_type = T`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L206 | 定义类型别名 `using generic_type = GField`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L208 | 切换成员访问权限为 private；它是编译期接口边界，不是线程同步或内存保护。 |
| L212 | 声明成员、局部对象或完成语句 `GField field_`。若为指针或引用，它本身不说明拥有；若为值对象，其构造析构由所在作用域或外层对象管理。 |
| L214 | 声明成员、局部对象或完成语句 `friend GField`。若为指针或引用，它本身不说明拥有；若为值对象，其构造析构由所在作用域或外层对象管理。 |
| L216 | 切换成员访问权限为 public；它是编译期接口边界，不是线程同步或内存保护。 |
| L221 | 出现调用或函数声明 `Field`，对应表达式为 `Field();`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L224 | 声明接口 `explicit Field(FieldInputPtr node)`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L225 | 把右侧 `0)` 用于初始化或更新左侧 `explicit Field(FieldOperationPtr node, int output_i`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L228 | 声明接口 `explicit Field(T value)`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L231 | 运算符重载声明、定义或显式调用：`operator const GField &() const;`。结合参数和返回类型判断是赋值、索引、比较还是转换；operator=声明中的等号不是在给名为operator的变量赋值。 |
| L234 | 声明接口 `bool depends_on_input() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L235 | 声明模板参数 `template<typename InputT, typename... Args> static Field from_input(Args &&...args);`。类型参数决定生成操作的类型，非类型参数可决定内嵌容量或编译期分支。 |
| L236 | 声明模板参数 `template<typename InputT> const InputT *get_input_if() const;`。类型参数决定生成操作的类型，非类型参数可决定内嵌容量或编译期分支。 |
| L237 | 声明接口 `uint64_t hash() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L238 | 声明接口 `static Field from_non_owning_ref(const Field &field)`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L239 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L246 | 声明或定义类型 `class GFieldRef`。结合继承、访问权限和成员布局确认接口与拥有关系；前向声明本身没有完整对象布局。 |
| L247 | 切换成员访问权限为 public；它是编译期接口边界，不是线程同步或内存保护。 |
| L248 | 声明或定义类型 `struct Value`。结合继承、访问权限和成员布局确认接口与拥有关系；前向声明本身没有完整对象布局。 |
| L249 | 把右侧 `nullptr` 用于初始化或更新左侧 `const CPPType *type`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L250 | 把右侧 `nullptr` 用于初始化或更新左侧 `const void *value`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |

### FN_field.hh：L251—L290

<!-- source:source/blender/functions/FN_field.hh:251:290 -->

```cpp
  };
  struct Input {
    const FieldInput *node = nullptr;
  };
  struct MultiFn {
    const FieldOperation *node = nullptr;
    int output_i = 0;
  };

  using Variant = std::variant<Value, Input, MultiFn>;

 private:
  Variant variant_;

 public:
  /**
   * Create a reference to the given fields. The caller is responsible for making sure that the
   * referenced data stays valid.
   */
  GFieldRef(const GField &field);
  template<typename T> GFieldRef(const Field<T> &field);
  explicit GFieldRef(const FieldInput &field_input);
  explicit GFieldRef(const FieldOperation &field_multi_fn, int output_i = 0);
  explicit GFieldRef(Variant variant);

  /** Get access to the underlying #Variant. */
  const Variant &variant() const;

  /** These are the same as the corresponding #GField methods. */
  const CPPType &cpp_type() const;
  const FieldInputsPtr &field_inputs() const;
  uint64_t hash() const;

  static GFieldRef from_constant(const CPPType &type, const void *value);
};

/**
 * A field is always evaluated in some context. This context determines the value of the field
 * inputs.
 */
```

| 原始行 | 语义、约束与检查 |
|---|---|
| L251 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L252 | 声明或定义类型 `struct Input`。结合继承、访问权限和成员布局确认接口与拥有关系；前向声明本身没有完整对象布局。 |
| L253 | 把右侧 `nullptr` 用于初始化或更新左侧 `const FieldInput *node`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L254 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L255 | 声明或定义类型 `struct MultiFn`。结合继承、访问权限和成员布局确认接口与拥有关系；前向声明本身没有完整对象布局。 |
| L256 | 把右侧 `nullptr` 用于初始化或更新左侧 `const FieldOperation *node`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L257 | 把右侧 `0` 用于初始化或更新左侧 `int output_i`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L258 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L260 | 定义类型别名 `using Variant = std::variant<Value, Input, MultiFn>`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L262 | 切换成员访问权限为 private；它是编译期接口边界，不是线程同步或内存保护。 |
| L263 | 声明成员、局部对象或完成语句 `Variant variant_`。若为指针或引用，它本身不说明拥有；若为值对象，其构造析构由所在作用域或外层对象管理。 |
| L265 | 切换成员访问权限为 public；它是编译期接口边界，不是线程同步或内存保护。 |
| L270 | 出现调用或函数声明 `GFieldRef`，对应表达式为 `GFieldRef(const GField &field);`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L271 | 声明模板参数 `template<typename T> GFieldRef(const Field<T> &field);`。类型参数决定生成操作的类型，非类型参数可决定内嵌容量或编译期分支。 |
| L272 | 声明接口 `explicit GFieldRef(const FieldInput &field_input)`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L273 | 把右侧 `0)` 用于初始化或更新左侧 `explicit GFieldRef(const FieldOperation &field_multi_fn, int output_i`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L274 | 声明接口 `explicit GFieldRef(Variant variant)`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L277 | 声明接口 `const Variant &variant() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L280 | 声明接口 `const CPPType &cpp_type() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L281 | 声明接口 `const FieldInputsPtr &field_inputs() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L282 | 声明接口 `uint64_t hash() const`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L284 | 声明接口 `static GFieldRef from_constant(const CPPType &type, const void *value)`，本行没有对应函数体；返回类型、参数限定和const/noexcept共同组成调用契约，实际行为需继续定位实现。 |
| L285 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |

## 五、接口定位、调用线索与生命周期

### 本篇声明与实现入口

| 源码位置 | 实际声明片段 |
|---|---|
| [FN_field.hh:L203](../../../../../source/blender/functions/FN_field.hh#L203) | `template<typename T> class Field` |
| [FN_field.hh:L221](../../../../../source/blender/functions/FN_field.hh#L221) | `Field();` |
| [FN_field.hh:L224](../../../../../source/blender/functions/FN_field.hh#L224) | `explicit Field(FieldInputPtr node);` |
| [FN_field.hh:L225](../../../../../source/blender/functions/FN_field.hh#L225) | `explicit Field(FieldOperationPtr node, int output_i = 0);` |
| [FN_field.hh:L228](../../../../../source/blender/functions/FN_field.hh#L228) | `explicit Field(T value);` |
| [FN_field.hh:L234](../../../../../source/blender/functions/FN_field.hh#L234) | `bool depends_on_input() const;` |
| [FN_field.hh:L236](../../../../../source/blender/functions/FN_field.hh#L236) | `template<typename InputT> const InputT *get_input_if() const;` |
| [FN_field.hh:L237](../../../../../source/blender/functions/FN_field.hh#L237) | `uint64_t hash() const;` |
| [FN_field.hh:L238](../../../../../source/blender/functions/FN_field.hh#L238) | `static Field from_non_owning_ref(const Field &field);` |
| [FN_field.hh:L246](../../../../../source/blender/functions/FN_field.hh#L246) | `class GFieldRef` |
| [FN_field.hh:L248](../../../../../source/blender/functions/FN_field.hh#L248) | `struct Value` |
| [FN_field.hh:L252](../../../../../source/blender/functions/FN_field.hh#L252) | `struct Input` |
| [FN_field.hh:L255](../../../../../source/blender/functions/FN_field.hh#L255) | `struct MultiFn` |
| [FN_field.hh:L270](../../../../../source/blender/functions/FN_field.hh#L270) | `GFieldRef(const GField &field);` |
| [FN_field.hh:L271](../../../../../source/blender/functions/FN_field.hh#L271) | `template<typename T> GFieldRef(const Field<T> &field);` |
| [FN_field.hh:L272](../../../../../source/blender/functions/FN_field.hh#L272) | `explicit GFieldRef(const FieldInput &field_input);` |
| [FN_field.hh:L273](../../../../../source/blender/functions/FN_field.hh#L273) | `explicit GFieldRef(const FieldOperation &field_multi_fn, int output_i = 0);` |
| [FN_field.hh:L274](../../../../../source/blender/functions/FN_field.hh#L274) | `explicit GFieldRef(Variant variant);` |
| [FN_field.hh:L277](../../../../../source/blender/functions/FN_field.hh#L277) | `const Variant &variant() const;` |
| [FN_field.hh:L280](../../../../../source/blender/functions/FN_field.hh#L280) | `const CPPType &cpp_type() const;` |
| [FN_field.hh:L281](../../../../../source/blender/functions/FN_field.hh#L281) | `const FieldInputsPtr &field_inputs() const;` |
| [FN_field.hh:L282](../../../../../source/blender/functions/FN_field.hh#L282) | `uint64_t hash() const;` |
| [FN_field.hh:L284](../../../../../source/blender/functions/FN_field.hh#L284) | `static GFieldRef from_constant(const CPPType &type, const void *value);` |

### 同名符号出现位置

以下表提供跨文件阅读入口，包含声明、调用或测试使用；没有经过完整C++名称解析，不把它命名为已证明的运行时调用图。

| 符号 | 位置 | 文本证据 |
|---|---|---|
| `depends_on_input` | [geometry_fields.cc:L1019](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L1019) | `const bool selection_is_full = !selection.depends_on_input() &&` |
| `depends_on_input` | [geometry_fields.cc:L1077](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L1077) | `if (field.depends_on_input() &#124;&#124; !selection_is_full) {` |
| `depends_on_input` | [field_evaluation.cc:L509](../../../../../source/blender/functions/intern/field_evaluation.cc#L509) | `if (field.depends_on_input()) {` |
| `hash` | [BKE_geometry_set.hh:L470](../../../../../source/blender/blenkernel/BKE_geometry_set.hh#L470) | `uint64_t hash() const` |
| `hash` | [BLI_array.hh:L376](../../../../../source/blender/blenlib/BLI_array.hh#L376) | `uint64_t hash() const` |
| `hash` | [BLI_array.hh:L378](../../../../../source/blender/blenlib/BLI_array.hh#L378) | `return this->as_span().hash();` |
| `from_non_owning_ref` | [BKE_geometry_fields.hh:L358](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L358) | `static const auto field_ref = fn::Field<T>::from_non_owning_ref(field);` |
| `from_non_owning_ref` | [geometry_fields.cc:L577](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L577) | `static const fn::Field<int> field_ref = fn::Field<int>::from_non_owning_ref(field);` |
| `from_non_owning_ref` | [geometry_fields.cc:L903](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L903) | `static const fn::Field<float3> field_ref = fn::Field<float3>::from_non_owning_ref(field);` |
| `GFieldRef` | [field.cc:L373](../../../../../source/blender/functions/intern/field.cc#L373) | `GFieldRef::GFieldRef(const GField &field)` |
| `variant` | [BKE_geometry_fields.hh:L247](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L247) | `NativeFieldDomain(const None & ) : variant(None{}) {}` |
| `variant` | [BKE_geometry_fields.hh:L248](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L248) | `NativeFieldDomain(const Domain &domain) : variant(domain) {}` |
| `variant` | [BKE_geometry_fields.hh:L249](../../../../../source/blender/blenkernel/BKE_geometry_fields.hh#L249) | `NativeFieldDomain(const Constant & ) : variant(Constant{}) {}` |
| `cpp_type` | [geometry_fields.cc:L630](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L630) | `: bke::GeometryFieldInput(value_field.cpp_type(), "Evaluate at Index"),` |
| `cpp_type` | [geometry_fields.cc:L716](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L716) | `builder.single_output("Value", src_field_.cpp_type());` |
| `cpp_type` | [geometry_fields.cc:L767](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L767) | `: bke::GeometryFieldInput(field.cpp_type(), "Evaluate on Domain"),` |
| `field_inputs` | [geometry_fields.cc:L1205](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L1205) | `const fn::FieldInputsPtr &field_inputs = field.field_inputs();` |
| `field_inputs` | [geometry_fields.cc:L1255](../../../../../source/blender/blenkernel/intern/geometry_fields.cc#L1255) | `const fn::FieldInputsPtr &field_inputs = field.field_inputs();` |
| `field_inputs` | [field.cc:L175](../../../../../source/blender/functions/intern/field.cc#L175) | `const FieldInputsPtr &FieldInput::field_inputs() const` |
| `from_constant` | [field.cc:L24](../../../../../source/blender/functions/intern/field.cc#L24) | `GField GField::from_constant(const CPPType &type, const void *value)` |
| `from_constant` | [field_evaluation.cc:L530](../../../../../source/blender/functions/intern/field_evaluation.cc#L530) | `GField new_field = GField::from_constant(type, buffer);` |
| `from_constant` | [field_evaluation.cc:L605](../../../../../source/blender/functions/intern/field_evaluation.cc#L605) | `fields.append(GFieldRef::from_constant(CPPType::get<bool>(), &true_value));` |

### 生命周期推理图

```mermaid
flowchart LR
  O["调用者或源数据拥有者"]:::input
  V["Field类型接口的接口与状态"]:::abstraction
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

本方向的共同数值模型如下。本篇的专门检查是：比较明确类型转换和错误强转的契约。

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

比较明确类型转换和错误强转的契约。

参考思路：静态类型包装便于编译期检查，动态形式支持统一容器；转换必须维护真实CPPType一致。

将输入、预期结果和资源责任分成三张清单。先用最直接的实现给出可核对的答案，再替换成对应源码使用的表示；比较结果不变的条件，而不是只比较接口名字。

验收依据：结果与直接计算一致；多个输出共享子表达式时不改变语义；深链构造、执行、销毁三个阶段分别检查。

## 七、复杂度、设计取舍与其他基础库

与表达式模板、AST和闭包比较：Field可在运行时组合并对不同上下文批量求值；不要把Field对象误当作固定几何的结果数组。

本篇的具体取舍：静态类型包装便于编译期检查，动态形式支持统一容器；转换必须维护真实CPPType一致。

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

阅读任务：先根据说明复述旧问题，提出一个自己的修复方案，再对照diff。结合本篇重点“Field<T>和GField怎样平衡类型安全与通用性？”判断方案改变的是表示、接口、生命周期还是调度。

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

阅读任务：先根据说明复述旧问题，提出一个自己的修复方案，再对照diff。结合本篇重点“Field<T>和GField怎样平衡类型安全与通用性？”判断方案改变的是表示、接口、生命周期还是调度。

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

阅读任务：先根据说明复述旧问题，提出一个自己的修复方案，再对照diff。结合本篇重点“Field<T>和GField怎样平衡类型安全与通用性？”判断方案改变的是表示、接口、生命周期还是调度。

## 九、反例、测试入口与掌握标准

仓库测试入口：

- [FN_field_test.cc](../../../../../source/blender/functions/tests/FN_field_test.cc)：阅读输入、断言与覆盖边界；本篇不把“存在测试”写成“本轮已运行”。

需要实际构造的反例：

- 空输入或没有结果需求：确认接口允许的空状态与不允许访问的操作。
- 边界位置和退化结构：把长度为1、末尾位置、重复值或深链代入真实分支。
- 生命周期结束或修改之后：检查保存的指针、引用、结果视图是否仍有效。
- 与本篇核心不变量相冲突的输入：比较明确类型转换和错误强转的契约。

### 可运行的教学参考程序

[reference_exercises.cc](../_tools/reference_exercises.cc)包含独立于Blender的C++20参考检查：视图、简化SmallVector、异常回滚、哈希碰撞与删除、偏移数组、拓扑映射、共享缓存、表达式、惰性分支、闭包和暴力最近邻。

参考程序有意省略生产实现的完整能力。例如SmallVector禁止复制移动容器，不支持只能移动的元素，并禁止append参数别名到自身元素；TinyMap固定8槽，不提供增长。程序通过不能替代Blender实现测试。实际运行结果、编译器与命令见验收报告。

掌握标准：离开源码解释“Field<T>和GField怎样平衡类型安全与通用性？”；独立完成上述练习；能指出一个会破坏表达式相关约束的最小反例，并用具体代码行说明检查或修复应放在哪里。
