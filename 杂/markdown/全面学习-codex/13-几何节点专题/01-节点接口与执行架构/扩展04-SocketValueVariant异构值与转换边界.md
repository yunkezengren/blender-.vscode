# GN-04 SocketValueVariant异构值与转换边界

[几何节点学习地图](../README.md) · [专题分组导航](README.md) · [全局实现索引](../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

基准：`cbda6b96c26c0dee3c3b5cbb93960c4ac06a6b30`；文件哈希及连续摘录区间记录在[新增专题证据](../../_evidence/geometry-extension.json)。本篇围绕所选函数解释核心机制，辅助依赖明确列出已定位实现与尚需类型确认的边界，不宣称相关整个文件已全文复核。

## 先回答一个具体问题

同一个浮点插槽为什么有时装一个float，有时装一个Field？类型擦除怎样和模板接口连接？

## 相关类与数据的职责

- **`SocketValueVariant`**：封装可在几何节点插槽上传递的实际值。 定义入口：[source/blender/blenkernel/BKE_node_socket_value.hh · L83](../../../../../../source/blender/blenkernel/BKE_node_socket_value.hh)。
- **`detail::SocketValueVariantAny`**：底层异构存储，定义实际可容纳的存储类型。 定义入口：[source/blender/blenkernel/BKE_node_socket_value.hh · L24](../../../../../../source/blender/blenkernel/BKE_node_socket_value.hh)。
- **`CPPType`**：提供运行时尺寸、对齐及类型操作。 定义入口：[source/blender/blenlib/BLI_cpp_type.hh · L106](../../../../../../source/blender/blenlib/BLI_cpp_type.hh)。
- **`GField`**：类型擦除后的延迟表达式。 定义入口：[source/blender/functions/FN_field.hh · L55](../../../../../../source/blender/functions/FN_field.hh)。
- **`to_storage_type<T>`**：将接口类型映射到Variant实际存储类型。

```mermaid
flowchart TB
  T0["SocketValueVariant"]:::abstraction
  T1["detail::SocketValueVariantAny"]:::data
  T2["CPPType"]:::abstraction
  T3["GField"]:::data
  T4["to_storage_type＜T＞"]:::data
  T0 -->|"使用底层存储"| T1
  T0 -->|"运行时接口需要类型操作"| T2
  T0 -->|"可装Field载荷"| T3
  T4 -->|"确定模板存储类型"| T1
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

上图箭头文字区分拥有、借用、调用和数据依赖。连线不表示这些类型存在同名继承关系；只有源码明确声明的继承才按继承理解。

## 设计推导与扩展知识

### 推导1

编辑器插槽的显示类型、SocketValueVariant本身的C++类型、内部载荷的运行时类型必须分开。例如显示为Float的连接可以携带依赖Position的Field，而不是单个浮点数。

### 推导2

from建立新包装值，emplace使用to_storage_type映射T，并通过底层Any构造实际载荷。源码中的sizeof断言说明接口类型与存储类型之间有明确布局假设，不能推广为任意两个同尺寸类型都可互换。

### 推导3

try_convert与ensure_type失败契约不同：前者可以返回空指针，后者必要时创建目标类型的默认值。使用ensure_type会改变载荷，因此不能把它当作无副作用的类型检查。

### 推导4

is_context_dependent_field比is_field更接近“能否在没有几何上下文时当单值处理”的问题。常量Field与依赖属性的Field都属于表达式包装，但执行选择可以不同。

### 推导5

设计异构系统时，要把允许的转换表、默认值策略与拥有关系作为一组协议。只写一个variant或void*容器并不能自动得到这些行为。

## 实际处理阶段

```mermaid
flowchart TB
  P0["调用SocketValueVariant::from"]:::input
  P1["emplace映射StorageT"]:::compute
  P2["根据实际内容查询is_field等"]:::compute
  P3["try_convert尝试转换"]:::compute
  P4["ensure_type在必要时提供默认值"]:::result
  P0 -->|"下一阶段"| P1
  P1 -->|"下一阶段"| P2
  P2 -->|"下一阶段"| P3
  P3 -->|"下一阶段"| P4
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

这张图概括本篇所讨论的主路径；等待输入、构建失败与不同策略的分支以下方完整代码为准，不能把概括图当作每次都会执行的无条件顺序。

## 教学注释代码与分段机制

<a id="f-fa3c16e83ef6de45"></a>

### `blender::bke::from` · L220—L225

创建包装后emplace，返回值可移动。T的推导与decay决定引用是否会成为实际存储类型。

实现位置：[source/blender/blenkernel/BKE_node_socket_value.hh](../../../../../../source/blender/blenkernel/BKE_node_socket_value.hh)。

**教学注释版**

<!-- annotated:f361bbaed26179 -->

```cpp
template<typename T> inline SocketValueVariant SocketValueVariant::from(T &&value)
{
  SocketValueVariant value_variant;
  value_variant.emplace<std::decay_t<T>>(std::forward<T>(value));
  return value_variant;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_node_socket_value.hh · L220—L225</summary>

<!-- original:f361bbaed26179:source/blender/blenkernel/BKE_node_socket_value.hh:220:225 -->

```cpp
template<typename T> inline SocketValueVariant SocketValueVariant::from(T &&value)
{
  SocketValueVariant value_variant;
  value_variant.emplace<std::decay_t<T>>(std::forward<T>(value));
  return value_variant;
}
```

</details>

<details>
<summary>实现依赖入口与尚需类型确认的调用</summary>

- `value_variant.emplace<std::decay_t<T>>` → [blender::bke::emplace · L227](扩展04-SocketValueVariant异构值与转换边界.md#f-b1c23f5500ae1b73)。
- `std::forward<T>`：在转发引用中恢复调用者传入的值类别；依赖推导类型，不能与无条件move互换。 [接口资料](https://eel.is/c++draft/utility.forward)。

</details>

<a id="f-b1c23f5500ae1b73"></a>

### `blender::bke::emplace` · L227—L233

关注StorageT、构造过程与sizeof断言，不把底层转换写成通用类型双关技巧。

实现位置：[source/blender/blenkernel/BKE_node_socket_value.hh](../../../../../../source/blender/blenkernel/BKE_node_socket_value.hh)。

**教学注释版**

<!-- annotated:cb5a0223302275 -->

```cpp
template<typename T, typename... Args> inline T &SocketValueVariant::emplace(Args &&...args)
{
  // [讲解] 接口类型与底层Any存储类型通过显式映射连接。
  using StorageT = to_storage_type<T>;
  StorageT &value = value_.emplace<StorageT>(T(std::forward<Args>(args)...));
  static_assert(sizeof(T) == sizeof(StorageT));
  return reinterpret_cast<T &>(value);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_node_socket_value.hh · L227—L233</summary>

<!-- original:cb5a0223302275:source/blender/blenkernel/BKE_node_socket_value.hh:227:233 -->

```cpp
template<typename T, typename... Args> inline T &SocketValueVariant::emplace(Args &&...args)
{
  using StorageT = to_storage_type<T>;
  StorageT &value = value_.emplace<StorageT>(T(std::forward<Args>(args)...));
  static_assert(sizeof(T) == sizeof(StorageT));
  return reinterpret_cast<T &>(value);
}
```

</details>

<details>
<summary>实现依赖入口与尚需类型确认的调用</summary>

- `value_.emplace<StorageT>` → [blender::bke::emplace · L227](扩展04-SocketValueVariant异构值与转换边界.md#f-b1c23f5500ae1b73)。
- `T` → [T · L96](../../90-实现依赖专题/07-Intern运行时与平台/cycles/subd/split.cpp.md#f-d5d0885c790cc4e4)。
- `std::forward<Args>`：在转发引用中恢复调用者传入的值类别；依赖推导类型，不能与无条件move互换。 [接口资料](https://eel.is/c++draft/utility.forward)。

</details>

<a id="f-dc6b18e59a681c72"></a>

### `blender::bke::try_convert` · L235—L254

先检查是否有值，再检查是否可按目标类型解释；必要时通过Info转换。失败返回空指针，不与ensure_type的默认值策略混用。

实现位置：[source/blender/blenkernel/BKE_node_socket_value.hh](../../../../../../source/blender/blenkernel/BKE_node_socket_value.hh)。

**教学注释版**

<!-- annotated:864d480b36f790 -->

```cpp
template<typename T> T *SocketValueVariant::try_convert()
{
  // [讲解] 接口类型与底层Any存储类型通过显式映射连接。
  using StorageT = to_storage_type<T>;
  if (!value_.has_value()) {
    return nullptr;
  }
  const Info &info = value_.extra_info();
  const CPPType &requested_type = CPPType::get<T>();
  if (info.type == requested_type) {
    return &reinterpret_cast<T &>(value_.get<StorageT>());
  }
  if (info.is_interpretable_as(requested_type, value_)) {
    return &reinterpret_cast<T &>(value_.get<StorageT>());
  }
  if (!info.convert_to(requested_type, value_)) {
    return nullptr;
  }
  BLI_assert(value_.extra_info().is_interpretable_as(requested_type, value_));
  return &reinterpret_cast<T &>(value_.get<StorageT>());
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_node_socket_value.hh · L235—L254</summary>

<!-- original:864d480b36f790:source/blender/blenkernel/BKE_node_socket_value.hh:235:254 -->

```cpp
template<typename T> T *SocketValueVariant::try_convert()
{
  using StorageT = to_storage_type<T>;
  if (!value_.has_value()) {
    return nullptr;
  }
  const Info &info = value_.extra_info();
  const CPPType &requested_type = CPPType::get<T>();
  if (info.type == requested_type) {
    return &reinterpret_cast<T &>(value_.get<StorageT>());
  }
  if (info.is_interpretable_as(requested_type, value_)) {
    return &reinterpret_cast<T &>(value_.get<StorageT>());
  }
  if (!info.convert_to(requested_type, value_)) {
    return nullptr;
  }
  BLI_assert(value_.extra_info().is_interpretable_as(requested_type, value_));
  return &reinterpret_cast<T &>(value_.get<StorageT>());
}
```

</details>

<details>
<summary>实现依赖入口与尚需类型确认的调用</summary>

- `value_.has_value`：L238的类型或分派协议；由接收对象具体类型或运行时策略提供实现。
- `value_.extra_info` → [blender::Any::extra_info · L390](../../01-基础容器与现代CPP/17-Any类型擦除存储.md#f-7a560ad93b9c62eb)。
- `CPPType::get<T>` → [blender::bke::get · L340](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-44fd803c51c13447)；[blender::bke::get · L349](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-c63e6331bfae49c4)。多候选需按实参和重载规则确认。
- `value_.get<StorageT>` → [blender::bke::get · L340](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-44fd803c51c13447)；[blender::bke::get · L349](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-c63e6331bfae49c4)。多候选需按实参和重载规则确认。
- `info.is_interpretable_as`：L246的类型或分派协议；由接收对象具体类型或运行时策略提供实现。
- `info.convert_to`：L249的类型或分派协议；由接收对象具体类型或运行时策略提供实现。
- `BLI_assert`：宏定义见[source/blender/blenlib/BLI_assert.hh](../../../../../../source/blender/blenlib/BLI_assert.hh), L48；按当前编译条件选择。
- `BLI_assert`：宏定义见[source/blender/blenlib/BLI_assert.hh](../../../../../../source/blender/blenlib/BLI_assert.hh), L63；按当前编译条件选择。
- `value_.extra_info().is_interpretable_as`：L252的类型或分派协议；接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。

</details>

<a id="f-8b47ae436faf6028"></a>

### `blender::bke::try_convert` · L256—L269

先检查是否有值，再检查是否可按目标类型解释；必要时通过Info转换。失败返回空指针，不与ensure_type的默认值策略混用。

实现位置：[source/blender/blenkernel/BKE_node_socket_value.hh](../../../../../../source/blender/blenkernel/BKE_node_socket_value.hh)。

**教学注释版**

<!-- annotated:81205230eb3d27 -->

```cpp
inline void *SocketValueVariant::try_convert(const CPPType &type)
{
  if (!value_.has_value()) {
    return nullptr;
  }
  const Info &info = value_.extra_info();
  if (info.type == type) {
    return value_.get();
  }
  if (!info.convert_to(type, value_)) {
    return nullptr;
  }
  return value_.get();
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_node_socket_value.hh · L256—L269</summary>

<!-- original:81205230eb3d27:source/blender/blenkernel/BKE_node_socket_value.hh:256:269 -->

```cpp
inline void *SocketValueVariant::try_convert(const CPPType &type)
{
  if (!value_.has_value()) {
    return nullptr;
  }
  const Info &info = value_.extra_info();
  if (info.type == type) {
    return value_.get();
  }
  if (!info.convert_to(type, value_)) {
    return nullptr;
  }
  return value_.get();
}
```

</details>

<details>
<summary>实现依赖入口与尚需类型确认的调用</summary>

- `value_.has_value`：L258的类型或分派协议；由接收对象具体类型或运行时策略提供实现。
- `value_.extra_info` → [blender::Any::extra_info · L390](../../01-基础容器与现代CPP/17-Any类型擦除存储.md#f-7a560ad93b9c62eb)。
- `value_.get` → [blender::bke::get · L340](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-44fd803c51c13447)；[blender::bke::get · L349](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-c63e6331bfae49c4)。多候选需按实参和重载规则确认。
- `info.convert_to`：L265的类型或分派协议；由接收对象具体类型或运行时策略提供实现。

</details>

<a id="f-36be485d1fc40c00"></a>

### `blender::bke::ensure_type` · L271—L277

尝试转换失败后init_default；这是有状态的接口。

实现位置：[source/blender/blenkernel/BKE_node_socket_value.hh](../../../../../../source/blender/blenkernel/BKE_node_socket_value.hh)。

**教学注释版**

<!-- annotated:672ffb5807ccd0 -->

```cpp
template<typename T> inline T &SocketValueVariant::ensure_type()
{
  if (!this->try_convert<T>()) {
    // [讲解] 转换失败后建立目标类型默认值；ensure_type不是只读检查。
    return this->init_default<T>();
  }
  return *this->get_if<T>();
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_node_socket_value.hh · L271—L277</summary>

<!-- original:672ffb5807ccd0:source/blender/blenkernel/BKE_node_socket_value.hh:271:277 -->

```cpp
template<typename T> inline T &SocketValueVariant::ensure_type()
{
  if (!this->try_convert<T>()) {
    return this->init_default<T>();
  }
  return *this->get_if<T>();
}
```

</details>

<details>
<summary>实现依赖入口与尚需类型确认的调用</summary>

- `this->try_convert<T>` → [blender::bke::try_convert · L235](扩展04-SocketValueVariant异构值与转换边界.md#f-dc6b18e59a681c72)；[blender::bke::try_convert · L256](扩展04-SocketValueVariant异构值与转换边界.md#f-8b47ae436faf6028)。多候选需按实参和重载规则确认。
- `this->init_default<T>` → [blender::bke::init_default · L358](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-fbb5e4b001990c29)；[blender::bke::init_default · L363](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-b23d972a3955fa05)。多候选需按实参和重载规则确认。
- `this->get_if<T>` → [blender::bke::get_if · L293](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-5744f0088e078efb)；[blender::bke::get_if · L315](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-0ee4db24be0746a2)；[blender::bke::get_if · L320](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-1e9674022bd220af)；[blender::bke::get_if · L335](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-95510bddaf248ec5)。多候选需按实参和重载规则确认。

</details>

<a id="f-417f182997393297"></a>

### `blender::bke::ensure_type` · L279—L285

尝试转换失败后init_default；这是有状态的接口。

实现位置：[source/blender/blenkernel/BKE_node_socket_value.hh](../../../../../../source/blender/blenkernel/BKE_node_socket_value.hh)。

**教学注释版**

<!-- annotated:3f5ed7f2d3acb3 -->

```cpp
inline void *SocketValueVariant::ensure_type(const CPPType &type)
{
  if (!this->try_convert(type)) {
    // [讲解] 运行时类型重载同样有默认值回退语义。
    return this->init_default(type);
  }
  return value_.get();
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_node_socket_value.hh · L279—L285</summary>

<!-- original:3f5ed7f2d3acb3:source/blender/blenkernel/BKE_node_socket_value.hh:279:285 -->

```cpp
inline void *SocketValueVariant::ensure_type(const CPPType &type)
{
  if (!this->try_convert(type)) {
    return this->init_default(type);
  }
  return value_.get();
}
```

</details>

<details>
<summary>实现依赖入口与尚需类型确认的调用</summary>

- `this->try_convert` → [blender::bke::try_convert · L235](扩展04-SocketValueVariant异构值与转换边界.md#f-dc6b18e59a681c72)；[blender::bke::try_convert · L256](扩展04-SocketValueVariant异构值与转换边界.md#f-8b47ae436faf6028)。多候选需按实参和重载规则确认。
- `this->init_default` → [blender::bke::init_default · L358](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-fbb5e4b001990c29)；[blender::bke::init_default · L363](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-b23d972a3955fa05)。多候选需按实参和重载规则确认。
- `value_.get` → [blender::bke::get · L340](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-44fd803c51c13447)；[blender::bke::get · L349](../../90-实现依赖专题/02-BKE几何与数据/BKE_node_socket_value.hh.md#f-c63e6331bfae49c4)。多候选需按实参和重载规则确认。

</details>

## 用小数据走一遍

1. Float插槽收到常量2。
2. 可按单值路径计算。
3. Float插槽收到Position.x。
4. 必须保留Field等待几何上下文。

```mermaid
flowchart LR
  S0["Float插槽收到常量2"]:::input
  S1["可按单值路径计算"]:::data
  S2["Float插槽收到Position.x"]:::data
  S3["必须保留Field等待几何上下文"]:::result
  S0 -->|"推演"| S1
  S1 -->|"推演"| S2
  S2 -->|"推演"| S3
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

这是明确输入条件下的教学推演，不是本地性能实测。对源码的验证应同时检查数值、对象寿命、输出需求和数据是否存在。

## 反例与边界

- 目标类型与载荷不同。
- try_convert可能返回nullptr。
- ensure_type可能改为默认值。
- 调用者应选择需要的失败契约。

```mermaid
flowchart TB
  R0["目标类型与载荷不同"]:::error
  R1["try_convert可能返回nullptr"]:::error
  R2["ensure_type可能改为默认值"]:::compute
  R3["调用者应选择需要的失败契约"]:::result
  R0 -->|"检查后果与修正"| R1
  R1 -->|"检查后果与修正"| R2
  R2 -->|"检查后果与修正"| R3
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

## 历史提交阅读

本地历史阅读样本：**Jacques Lucke**，2026-09-03T22:24:57+02:00。

`f05d3fbf34f7052f9abba1be5169a12f44ac1371`

提交标题：Refactor: Geometry Nodes: generalize SocketValueVariant

[所选文件的真实diff](../../_evidence/geometry-history/GN-04.patch)。这是本地历史中匹配作者的近期样本，不冒称该系统的最初引入提交。阅读时先找变更前后的不变量，再检查新增分支与测试；本篇当前源码说明不混用历史签名。

## 独立实现与验收

给一个小型节点系统设计Value包装，分别写出查询、尝试转换与保证目标类型三个接口。

<details>
<summary>参考思路</summary>

查询不改变载荷；try_convert显式失败；ensure_type明确默认值或错误策略。测试三者不会悄悄共用同一个失败行为。

</details>

验收时保留一个能击穿错误设计的反例，再对照实际符号重走调用链。教学练习未在完整Blender中运行；本轮独立运行的模型验证另见新增专题验收报告。

## 继续阅读

- [GN-01 几何节点从编辑树到执行结果的全景](扩展01-几何节点从编辑树到执行结果的全景.md)
- [GN-02 节点注册声明与引用关系契约](扩展02-节点注册声明与引用关系契约.md)
- [GN-03 GeoNodeExecParams参数适配与移动语义](扩展03-GeoNodeExecParams参数适配与移动语义.md)
- [GN-05 执行图构建缓存与树副本所有权](扩展05-执行图构建缓存与树副本所有权.md)
- [GN-06 按需执行匿名输出与Switch需求传播](扩展06-按需执行匿名输出与Switch需求传播.md)
- [GN-22 ComputeContext日志映射与副作用根](扩展07-ComputeContext日志映射与副作用根.md)
- [GN-24 Jacques与Hans提交中的架构演化](扩展08-Jacques与Hans提交中的架构演化.md)
