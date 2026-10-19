# AnyDerived 逐行详解

> 源文件: `source/blender/blenlib/BLI_any_derived.hh` (177 行)

---

## 一句话概览

**AnyDerived** 是一个带小缓冲区优化 (SBO) 的类型擦除容器，可以持有某个基类 `Base` 的**任意派生类**对象，并根据对象大小自动选择内联存储或堆分配（`shared_ptr`）。

---

## 整体架构

```mermaid
graph TB
    subgraph "AnyDerived<Base, InlineBufferCapacity=24>"
        impl_["impl_ : Base*<br/>指向当前实现对象的指针"]
        storage_["storage_ : Storage(Any)<br/>负责内存管理"]
    end

    subgraph "Storage 内部三种存储形态"
        S1["🔹 内联派生类<br/>ImplT 直接存在 buffer 中"]
        S2["🔸 裸指针 Base*<br/>非拥有指针"]
        S3["🔶 shared_ptr&lt;Base&gt;<br/>共享拥有指针"]
    end

    storage_ --> S1
    storage_ --> S2
    storage_ --> S3
    S1 -->|"buffer 地址经转换"| impl_
    S2 -->|"解引用"| impl_
    S3 -->|"->get()"| impl_

    style impl_ fill:#4a9eff,color:#fff
    style storage_ fill:#ff9f43,color:#fff
    style S1 fill:#2ecc71,color:#fff
    style S2 fill:#f39c12,color:#fff
    style S3 fill:#e74c3c,color:#fff
```

---

## 依赖关系

```mermaid
graph LR
    AnyDerived --> Any["Any&lt;ExtraInfo, Capacity, Alignment&gt;"]
    AnyDerived --> AnyDerivedExtraInfo["AnyDerivedExtraInfo&lt;Base&gt;"]
    AnyDerivedExtraInfo -->|"ExtraInfo 参数"| Any

    VArrayCommon -->|"AnyDerived&lt;const VArrayImpl&lt;T&gt;&gt;"| AnyDerived
    GVArrayCommon -->|"AnyDerived&lt;const GVArrayImpl, 40&gt;"| AnyDerived

    style AnyDerived fill:#4a9eff,color:#fff
    style Any fill:#2ecc71,color:#fff
    style AnyDerivedExtraInfo fill:#f39c12,color:#fff
    style VArrayCommon fill:#9b59b6,color:#fff
    style GVArrayCommon fill:#9b59b6,color:#fff
```

---

## 第 1–9 行：文件头与包含

```cpp
// SPDX-FileCopyrightText: 2026 Blender Authors
// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include "BLI_any.hh"
```

- `#pragma once` — 非标准但广泛支持的包含守卫，确保头文件只被编译一次。
- `BLI_any.hh` — 提供 `Any` 模板，是 AnyDerived 的底层存储引擎。

---

## 第 11–47 行：`detail::AnyDerivedExtraInfo<Base>`

```cpp
namespace blender {
namespace detail {

template<typename Base> struct AnyDerivedExtraInfo {
```

这是传给 `Any` 的 **ExtraInfo** 参数。`Any` 为每种存储类型保存一份 ExtraInfo，AnyDerived 利用它来存储一个函数指针 `get_impl`，用于从 `Any` 的不透明 buffer 中提取出 `Base*`。

### 第 15 行：核心函数指针

```cpp
Base *(*get_impl)(const void *buffer);
```

- **类型**: 指向函数的指针，接受 `const void*`（即 Any 内部 buffer 的地址），返回 `Base*`。
- **作用**: 因为 Any 内部 buffer 可能存放的是 `ImplT`（内联对象）、`Base*`（裸指针）或 `shared_ptr<Base>`，三种情况提取 `Base*` 的方式不同，所以用函数指针做分发。

```mermaid
flowchart LR
    buffer["const void* buffer"] --> get_impl
    get_impl -->|"情况1: 内联 ImplT"| P1["static_cast 得到 ImplT*<br/>再转为 Base*"]
    get_impl -->|"情况2: Base*"| P2["解引用裸指针<br/>得到 Base*"]
    get_impl -->|"情况3: shared_ptr"| P3["调用 ->get()<br/>得到 Base*"]

    style get_impl fill:#e74c3c,color:#fff
    style P1 fill:#2ecc71,color:#fff
    style P2 fill:#f39c12,color:#fff
    style P3 fill:#9b59b6,color:#fff
```

### 第 17–44 行：`get<StorageT>()` 静态工厂

```cpp
template<typename StorageT> static constexpr AnyDerivedExtraInfo get()
```

这是一个 **静态成员函数模板**，根据 `StorageT` 的实际类型在编译期生成不同的 `get_impl` 函数。

#### 第 20–21 行：编译期约束

```cpp
static_assert(std::is_base_of_v<Base, StorageT> ||
              is_same_any_v<StorageT, Base *, std::shared_ptr<Base>>);
```

- `std::is_base_of_v<Base, StorageT>` — StorageT 是 Base 的派生类（内联存储场景）。
- `is_same_any_v<StorageT, Base*, std::shared_ptr<Base>>` — StorageT 是裸指针或 shared_ptr。
- `is_same_any_v` 是 Blender 自定义的工具：判断 `StorageT` 是否等于后面列表中的任一类型。
- `static_assert` 在编译期触发错误，不允许其他类型。

#### 第 25–28 行：情况 1 — 内联派生类

```cpp
if constexpr (std::is_base_of_v<Base, StorageT>) {
    return {[](const void *buffer) {
        return static_cast<Base *>(
            const_cast<StorageT *>(
                static_cast<const StorageT *>(buffer)));
    }};
}
```

**逐层拆解转换链**:

```
const void* buffer
  → static_cast<const StorageT*>(buffer)   // 1. 视为指向 StorageT 的 const 指针
  → const_cast<StorageT*>(...)              // 2. 去掉 const（因为我们要返回非 const Base*）
  → static_cast<Base*>(...)                 // 3. 派生类指针转基类指针（向上转型，隐式可行）
```

> **为什么需要 `const_cast`？** 因为 `buffer` 参数是 `const void*`，但返回类型是 `Base*`（非 const）。AnyDerived 的 `impl_` 是非 const 指针，所以必须去掉 const。

> **`if constexpr`** — C++17 特性，编译期分支。条件为 false 的分支**根本不会被编译**，所以即使里面有非法代码也不会报错。

#### 第 30–33 行：情况 2 — 裸指针 `Base*`

```cpp
else if constexpr (std::is_same_v<StorageT, Base *>) {
    return {[](const void *buffer) {
        return *const_cast<StorageT *>(static_cast<const StorageT *>(buffer));
    }};
}
```

buffer 里存的是一个 `Base*`（指针的指针），需要**解引用**才能得到 `Base*`：

```
const void* buffer
  → static_cast<const Base**>(buffer)  // 视为指向 Base* 的指针
  → const_cast<Base**>(...)            // 去 const
  → *(...)                             // 解引用，得到 Base*
```

#### 第 35–38 行：情况 3 — `shared_ptr<Base>`

```cpp
else if constexpr (std::is_same_v<StorageT, std::shared_ptr<Base>>) {
    return {[](const void *buffer) {
        return (const_cast<StorageT *>(static_cast<const StorageT *>(buffer)))->get();
    }};
}
```

buffer 里存的是 `shared_ptr<Base>` 对象，调用其 `.get()` 方法提取裸指针：

```
const void* buffer
  → static_cast<const shared_ptr<Base>*>(buffer)  // 视为指向 shared_ptr 的指针
  → const_cast<shared_ptr<Base>*>(...)             // 去 const
  → ->get()                                        // shared_ptr 的 get() 返回 Base*
```

#### 第 40–43 行：不可达分支

```cpp
else {
    BLI_assert_unreachable();
    return {};
}
```

`BLI_assert_unreachable()` — Blender 的断言宏，在 Debug 构建中触发中断。由于前面的 `static_assert` 已排除了其他类型，此分支理论上不会执行。

---

## 第 49–65 行：AnyDerived 类文档注释

```cpp
/**
 * This allows storing or passing around derived classes of a common base class.
 * Typically, this always requires allocating the value on the heap and passing it
 * around e.g. as unique_ptr.
 * #AnyDerived has small buffer optimization. So if the type is small, it can be
 * stored directly without an additional allocation.
 *
 * If all derived types are known where the type is used, it can be more efficient
 * to use std::variant<Derived1, Derived2, ...> instead. #AnyDerived uses type
 * erasure through the use of #Any and therefore works even when not all used
 * derived types are known.
 *
 * This is used extensively for virtual arrays. Each type of virtual array is
 * implemented as subclass of #VArrayImpl while #VArray actually stores a
 * specific implementation.
 *
 * Note: If the value is not stored inline, it's currently stored as a shared_ptr
 * which is shared when the AnyDerived is copied. This behavior is fine and
 * efficient for all current uses but it may need to be generalized if
 * #AnyDerived is supposed to be used in more places.
 */
```

**翻译要点**:

| 原文 | 翻译 |
|------|------|
| small buffer optimization (SBO) | 小缓冲区优化——小对象直接存在栈上，无需堆分配 |
| type erasure | 类型擦除——隐藏具体类型，只暴露基类接口 |
| `std::variant` 替代方案 | 如果所有派生类型已知，用 `variant` 更高效（无虚函数开销） |
| shared when copied | 拷贝时共享 `shared_ptr`，即**浅拷贝**语义 |

```mermaid
graph TD
    subgraph "传统方式: unique_ptr"
        A1["堆分配"] --> A2["只能移动，不能拷贝"]
    end

    subgraph "AnyDerived 方式"
        B1{"对象 ≤ 24 字节<br/>且可拷贝？"}
        B1 -->|"是"| B2["内联存储<br/>零堆分配"]
        B1 -->|"否"| B3["shared_ptr 堆分配<br/>拷贝时共享"]
    end

    style B2 fill:#2ecc71,color:#fff
    style B3 fill:#e74c3c,color:#fff
    style A1 fill:#f39c12,color:#fff
```

---

## 第 66 行：类模板声明

```cpp
template<typename Base, int64_t InlineBufferCapacity = 24> struct AnyDerived {
```

| 参数 | 含义 | 默认值 |
|------|------|--------|
| `Base` | 基类类型，如 `const VArrayImpl<T>` | （必须指定） |
| `InlineBufferCapacity` | 内联缓冲区大小（字节） | 24 |

> **为什么默认 24？** 24 字节足以容纳大多数小型 VArray 实现（如 `VArrayImpl_For_Span`），同时不会让 `AnyDerived` 对象过大。`GVArrayCommon` 使用 40 字节因为其实现通常更大。

> **`struct` 而非 `class`** — Blender 风格：默认 public 访问。C++ 中 struct 和 class 唯一区别就是默认访问权限。

---

## 第 67–79 行：私有成员

```cpp
private:
    using Storage = Any<detail::AnyDerivedExtraInfo<Base>, InlineBufferCapacity, alignof(Base)>;
```

- **`Any<ExtraInfo, Capacity, Alignment>`** — 底层存储引擎。
  - `ExtraInfo` = `AnyDerivedExtraInfo<Base>`，提供 `get_impl` 函数指针。
  - `Capacity` = `InlineBufferCapacity`，内联缓冲区大小。
  - `Alignment` = `alignof(Base)`，对齐要求与基类一致。

```cpp
Base *impl_ = nullptr;
```

- 指向当前实现对象的**裸指针**。可能为 `nullptr`（空状态）。
- 这是访问实际对象的**快速路径**——不需要每次都通过 `storage_.extra_info().get_impl()` 提取。

```cpp
Storage storage_;
```

- 负责内存管理的存储对象。内部可能是以下三种之一：

```mermaid
graph LR
    storage_ --> I["内联 ImplT<br/>（对象直接在 buffer 中）"]
    storage_ --> P["Base*<br/>（非拥有裸指针）"]
    storage_ --> S["shared_ptr&lt;Base&gt;<br/>（共享拥有）"]

    style I fill:#2ecc71,color:#fff
    style P fill:#f39c12,color:#fff
    style S fill:#e74c3c,color:#fff
```

---

## 第 82 行：默认构造

```cpp
AnyDerived() = default;
```

- `= default` — 显式要求编译器生成默认构造函数。
- 效果：`impl_` 初始化为 `nullptr`，`storage_` 默认构造（空状态）。
- 结果：`operator bool()` 返回 `false`。

---

## 第 84–87 行：拷贝构造

```cpp
AnyDerived(const AnyDerived &other) : storage_(other.storage_)
{
    impl_ = this->impl_from_storage();
}
```

1. **`storage_(other.storage_)`** — 拷贝 Any 对象。Any 的拷贝行为：
   - 内联对象：调用拷贝构造函数（深拷贝）。
   - `shared_ptr`：引用计数 +1（浅拷贝/共享）。
   - 裸指针：直接复制指针值（非拥有，安全）。
2. **`impl_ = this->impl_from_storage()`** — 从新拷贝的 storage 中重新提取 `impl_` 指针。**不能**直接用 `other.impl_`，因为内联对象被深拷贝后地址已变。

```mermaid
sequenceDiagram
    participant O as other (源)
    participant N as this (目标)

    Note over O,N: 拷贝构造
    O->>N: storage_ 拷贝
    alt 内联对象
        N->>N: 新 buffer 地址 ≠ 旧地址
        N->>N: impl_from_storage() 重新计算 impl_
    else shared_ptr
        N->>N: 引用计数 +1
        N->>N: impl_ 指向同一对象
    else 裸指针
        N->>N: impl_ 指向同一对象
    end
```

---

## 第 89–94 行：移动构造

```cpp
AnyDerived(AnyDerived &&other) noexcept : storage_(std::move(other.storage_))
{
    impl_ = this->impl_from_storage();
    other.storage_.reset();
    other.impl_ = nullptr;
}
```

1. **`std::move(other.storage_)`** — 移动 Any，源对象进入"有效但未指定"状态。
2. **`impl_from_storage()`** — 重新提取指针（移动后 buffer 内容可能已变）。
3. **`other.storage_.reset()`** — 清空源 storage，使其变为空状态。
4. **`other.impl_ = nullptr`** — 源的 impl 指针置空。

> **`noexcept`** — 声明此函数不抛异常。这使得 `AnyDerived` 可以被放入某些要求 noexcept 移动的容器中（如 `std::vector` 在 realloc 时会优先使用移动）。

---

## 第 96–99 行：裸指针构造

```cpp
explicit AnyDerived(Base *impl) : impl_(impl)
{
    storage_ = impl_;
}
```

- **`explicit`** — 防止隐式转换，必须显式写 `AnyDerived<Base>(ptr)`。
- **`storage_ = impl_`** — 将裸指针存入 Any。Any 会将其存为 `Base*` 类型（非拥有）。
- **注意**：调用者必须确保指针在 AnyDerived 存活期间有效。

---

## 第 101–106 行：shared_ptr 构造

```cpp
explicit AnyDerived(std::shared_ptr<Base> impl) : impl_(impl.get())
{
    if (impl_) {
        storage_ = std::move(impl);
    }
}
```

1. **`impl_(impl.get())`** — 从 shared_ptr 提取裸指针给 `impl_`。
2. **`if (impl_)`** — 如果指针非空，才将 shared_ptr 移入 storage。如果为空，storage 保持默认（空状态）。
3. **`std::move(impl)`** — 移动 shared_ptr 到 storage，避免引用计数增减。

---

## 第 108–128 行：赋值运算符

### 拷贝赋值

```cpp
AnyDerived &operator=(const AnyDerived &other)
{
    if (this == &other) { return *this; }  // 自赋值检查
    storage_ = other.storage_;
    impl_ = this->impl_from_storage();
    return *this;
}
```

逻辑与拷贝构造一致，只是多了自赋值检查。

### 移动赋值

```cpp
AnyDerived &operator=(AnyDerived &&other) noexcept
{
    if (this == &other) { return *this; }
    storage_ = std::move(other.storage_);
    impl_ = this->impl_from_storage();
    other.storage_.reset();
    other.impl_ = nullptr;
    return *this;
}
```

逻辑与移动构造一致。

---

## 第 130–146 行：`emplace<ImplT>(args...)` — 核心方法

```cpp
template<typename ImplT, typename... Args>
    requires std::is_base_of_v<Base, ImplT>
void emplace(Args &&...args)
```

- **`requires std::is_base_of_v<Base, ImplT>`** — C++20 概念约束，确保 `ImplT` 必须是 `Base` 的派生类。
- **`Args&&...`** — 完美转发的参数包。

### 第 134–138 行：内联路径

```cpp
if constexpr (std::is_copy_constructible_v<ImplT> && Storage::template is_inline_v<ImplT>) {
    impl_ = &storage_.template emplace<ImplT>(std::forward<Args>(args)...);
}
```

**条件**：`ImplT` 可拷贝 **且** 大小 ≤ `InlineBufferCapacity` 且对齐满足要求。

- **`Storage::template is_inline_v<ImplT>`** — Any 的静态常量，判断类型是否能内联存储。
- **`storage_.template emplace<ImplT>(...)`** — 在 Any 的 buffer 中原地构造 `ImplT`，返回引用。`&` 取地址赋给 `impl_`。
- **`template` 关键字** — 在依赖模板参数的成员模板调用中，必须加 `template` 告诉编译器 `emplace` 是模板而非 `<` 比较。

> **为什么要求可拷贝？** 因为 `Any` 在拷贝时需要能拷贝其内容。不可拷贝的类型无法内联存储到 Any 中。

### 第 139–145 行：堆分配路径

```cpp
else {
    std::shared_ptr<Base> ptr = std::make_shared<ImplT>(std::forward<Args>(args)...);
    impl_ = &*ptr;
    storage_ = std::move(ptr);
}
```

- **`std::make_shared<ImplT>(...)`** — 在堆上构造 `ImplT`，创建 `shared_ptr<Base>`。
- **`&*ptr`** — `*ptr` 解引用得到 `ImplT&`，`&` 取地址得到 `ImplT*`，隐式转为 `Base*`。
- **`std::move(ptr)`** — 移动 shared_ptr 到 storage。

```mermaid
flowchart TD
    emplace["emplace&lt;ImplT&gt;(args...)"] --> check{"ImplT 可拷贝<br/>且能内联？"}
    check -->|"是"| inline["storage_.emplace&lt;ImplT&gt;(args...)<br/>在 buffer 中原地构造"]
    check -->|"否"| heap["make_shared&lt;ImplT&gt;(args...)<br/>堆上构造，存 shared_ptr"]

    inline --> impl_set1["impl_ = &buffer中的对象"]
    heap --> impl_set2["impl_ = &*shared_ptr"]

    style inline fill:#2ecc71,color:#fff
    style heap fill:#e74c3c,color:#fff
    style check fill:#f39c12,color:#fff
```

---

## 第 148–166 行：访问器

```cpp
operator bool() const { return impl_ != nullptr; }
```
- 隐式转换为 bool：`if (any_derived)` 检查是否持有值。

```cpp
Base &operator*() const { return *impl_; }
Base *operator->() const { return impl_; }
Base *get() const { return impl_; }
```
- `operator*` — 解引用，返回 `Base&`。
- `operator->` — 箭头运算符，返回 `Base*`，支持 `a->method()` 语法。
- `get()` — 显式获取裸指针。

> 这三个方法让 AnyDerived 用起来就像一个智能指针。

---

## 第 168–176 行：`impl_from_storage()` — 从 storage 恢复 impl_

```cpp
protected:
Base *impl_from_storage() const
{
    if (!storage_.has_value()) {
        return nullptr;
    }
    return storage_.extra_info().get_impl(storage_.get());
}
```

1. **`storage_.has_value()`** — 检查 Any 是否持有值。
2. **`storage_.extra_info()`** — 获取 `AnyDerivedExtraInfo<Base>`，其中包含 `get_impl` 函数指针。
3. **`storage_.get()`** — 获取 Any 内部 buffer 的 `void*` 地址。
4. **`get_impl(buffer)`** — 调用对应的提取函数，返回 `Base*`。

```mermaid
sequenceDiagram
    participant C as AnyDerived
    participant S as Storage (Any)
    participant E as ExtraInfo
    participant F as get_impl 函数

    C->>S: has_value()?
    alt 空
        S-->>C: false → return nullptr
    else 有值
        S->>E: extra_info()
        E-->>C: get_impl 函数指针
        C->>S: get() → void* buffer
        C->>F: get_impl(buffer)
        F-->>C: Base*
    end
```

---

## 实际使用场景

### VArray（虚拟数组）

```cpp
// BLI_virtual_array.hh:513
AnyDerived<const VArrayImpl<T>> impl_;
```

```mermaid
graph TD
    VArray["VArray&lt;T&gt;"] -->|"impl_"| AD["AnyDerived&lt;const VArrayImpl&lt;T&gt;&gt;"]
    AD -->|"可能内联"| Span["VArrayImpl_For_Span&lt;T&gt;<br/>（小对象，内联存储）"]
    AD -->|"可能堆分配"| Func["VArrayImpl_For_Func&lt;T&gt;<br/>（较大，shared_ptr）"]
    AD -->|"裸指针"| Ext["外部 VArrayImpl<br/>（非拥有）"]

    style VArray fill:#4a9eff,color:#fff
    style AD fill:#ff9f43,color:#fff
    style Span fill:#2ecc71,color:#fff
    style Func fill:#e74c3c,color:#fff
    style Ext fill:#f39c12,color:#fff
```

### GVArray（泛型虚拟数组）

```cpp
// BLI_generic_virtual_array.hh:93
AnyDerived<const GVArrayImpl, 40> impl_;
```

- `InlineBufferCapacity = 40` — 泛型实现通常更大，需要更大的内联缓冲区。

---

## 内存布局对比

```mermaid
graph LR
    subgraph "AnyDerived&lt;Base, 24&gt; 大约 48 字节"
        direction TB
        A1["impl_: 8 字节 (指针)"]
        A2["storage_: ~40 字节"]
        A2a["  buffer_: 24 字节"]
        A2b["  info_: 8 字节"]
        A2c["  extra padding"]
    end

    subgraph "unique_ptr&lt;Base&gt; = 8 字节"
        direction TB
        B1["裸指针: 8 字节"]
    end

    style A1 fill:#4a9eff,color:#fff
    style A2 fill:#ff9f43,color:#fff
    style B1 fill:#2ecc71,color:#fff
```

> AnyDerived 牺牲了栈空间（约 48 字节 vs unique_ptr 的 8 字节），换来：
> 1. 小对象零堆分配
> 2. 可拷贝（shared_ptr 共享语义）
> 3. 支持非拥有引用（裸指针）

---

## 关键语法速查

| 语法 | 含义 |
|------|------|
| `if constexpr` | C++17 编译期分支，false 分支不编译 |
| `requires std::is_base_of_v<Base, ImplT>` | C++20 概念约束，限制模板参数 |
| `storage_.template emplace<ImplT>(...)` | 依赖模板参数的成员模板调用，`template` 消歧 |
| `std::forward<Args>(args)...` | 完美转发，保持参数的值类别 |
| `const_cast<StorageT*>(...)` | 去除 const，用于从 `const void*` 提取非 const 指针 |
| `static_cast<const StorageT*>(buffer)` | 向下转型（void→具体类型），编译期检查安全性 |
| `noexcept` | 声明不抛异常，允许容器优化 |
| `explicit` | 禁止隐式构造转换 |
| `= default` | 显式使用编译器生成的默认实现 |
| `BLI_assert_unreachable()` | Blender 断言宏，Debug 模式下触发中断 |

---

## 拷贝语义总结

```mermaid
graph TD
    copy["AnyDerived 拷贝"] --> S1{"存储形态"}
    S1 -->|"内联 ImplT"| D1["深拷贝：构造新对象<br/>impl_ 指向新地址"]
    S1 -->|"shared_ptr"| D2["浅拷贝：引用计数+1<br/>impl_ 指向同一对象"]
    S1 -->|"裸指针 Base*"| D3["浅拷贝：复制指针值<br/>impl_ 指向同一对象<br/>（非拥有，需注意生命周期）"]

    style D1 fill:#2ecc71,color:#fff
    style D2 fill:#f39c12,color:#fff
    style D3 fill:#e74c3c,color:#fff
```

---

## 完整数据流

```mermaid
flowchart TB
    subgraph "构造阶段"
        E["emplace&lt;ImplT&gt;(args)"] --> C{"可拷贝 && 可内联?"}
        C -->|是| I["buffer 中原地构造 ImplT"]
        C -->|否| H["堆上 make_shared&lt;ImplT&gt;"]
        I --> P1["impl_ = &buffer中的对象"]
        H --> P2["impl_ = shared_ptr.get()"]
    end

    subgraph "使用阶段"
        U["a->method()"] --> IMPL["通过 impl_ 直接调用<br/>虚函数分发到 ImplT"]
    end

    subgraph "拷贝阶段"
        CP["拷贝 AnyDerived"] --> CP2["storage_ 拷贝"]
        CP2 --> CP3["impl_from_storage()<br/>重新提取 impl_"]
    end

    subgraph "销毁阶段"
        D["AnyDerived 析构"] --> D2["storage_ 析构"]
        D2 --> D3{"存储形态"}
        D3 -->|"内联"| D4["调用 ImplT 析构"]
        D3 -->|"shared_ptr<br/>引用计数=0"| D5["删除堆上对象"]
        D3 -->|"裸指针"| D6["什么都不做（非拥有）"]
    end

    style E fill:#4a9eff,color:#fff
    style U fill:#2ecc71,color:#fff
    style CP fill:#f39c12,color:#fff
    style D fill:#e74c3c,color:#fff
```
