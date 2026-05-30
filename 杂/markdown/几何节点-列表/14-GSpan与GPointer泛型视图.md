# GSpan、GMutableSpan、GPointer、GMutablePointer — 泛型数据视图

> 📖 系列文档：[目录](01-列表系统架构与核心数据结构.md) | [上一篇](13-CPPType运行时类型信息.md) | [下一篇](15-VArray与GVArray虚拟数组.md)
> 源码文件：[BLI_generic_span.hh](../../source/blender/blenlib/BLI_generic_span.hh)、[BLI_generic_pointer.hh](../../source/blender/blenlib/BLI_generic_pointer.hh)

---

## 目录

1. [设计思想：为什么需要这几个类](#1-设计思想为什么需要这几个类)
2. [类型擦除的 Span/Pointer 体系](#2-类型擦除的-spanpointer-体系)
3. [GSpan — 泛型只读跨度](#3-gspan--泛型只读跨度)
4. [GMutableSpan — 泛型可变跨度](#4-gmutablespan--泛型可变跨度)
5. [GPointer — 泛型只读指针](#5-gpointer--泛型只读指针)
6. [GMutablePointer — 泛型可变指针](#6-gmutablepointer--泛型可变指针)
7. [四者关系与转换规则](#7-四者关系与转换规则)
8. [在列表系统中的应用](#8-在列表系统中的应用)

---

## 1. 设计思想：为什么需要这几个类

### 核心问题：编译期类型 vs 运行时类型

C++ 的模板系统在编译期提供了强大的类型安全，但几何节点系统面临一个根本矛盾：**Socket 的类型在运行时才确定**。

```mermaid
graph LR
    User["用户拖拽线"] --> |"运行时决定"| Socket["Socket 类型<br/>float? int? geometry?"]
    Socket --> |"编译期不知道"| Problem["如何写一个函数<br/>处理任意类型的数据?"]
```

如果只有 `Span<T>`，你无法写这样的函数：

```cpp
// ❌ 不可能：T 是什么？编译期不知道
void process_socket(Span<T> data);

// ❌ 也不行：每种类型写一个重载？几十种类型呢？
void process_socket(Span<float> data);
void process_socket(Span<int> data);
void process_socket(Span<float3> data);
// ... 无穷无尽
```

### 解决方案：类型擦除 + 运行时类型信息

Blender 的方案是**类型擦除**——把编译期的 `T` "擦掉"，换成运行时的 `CPPType`：

```mermaid
flowchart LR
    subgraph "编译期（类型化）"
        TF["Span&lt;float&gt;<br/>知道 T=float<br/>直接访问 float&"]
    end

    subgraph "运行时（类型擦除）"
        TG["GSpan<br/>不知道 T<br/>通过 CPPType 操作 void*"]
    end

    TF --> |"擦除 T"| TG
    TG --> |"typed&lt;float&gt;()"| TF
```

```cpp
// ✅ 一个函数处理所有类型
void process_socket(GSpan data) {
  const CPPType &type = data.type();
  if (type.is<float>()) {
    Span<float> values = data.typed<float>();
    // 处理 float
  } else if (type.is<int>()) {
    Span<int> values = data.typed<int>();
    // 处理 int
  }
  // ...
}
```

### 为什么需要四个类？

四个类解决两个正交维度的问题：

```mermaid
quadrantChart
    title 四个类的定位
    x-axis "单个值" --> "连续数组"
    y-axis "只读" --> "可变"
    quadrant-1 "GMutableSpan"
    quadrant-2 "GMutablePointer"
    quadrant-3 "GPointer"
    quadrant-4 "GSpan"
    GPointer: [0.1, 0.2]
    GMutablePointer: [0.1, 0.8]
    GSpan: [0.9, 0.2]
    GMutableSpan: [0.9, 0.8]
```

| 维度 | 只读 | 可变 |
|------|------|------|
| **单个值** | `GPointer`（`const void*`） | `GMutablePointer`（`void*`） |
| **连续数组** | `GSpan`（`const void*` + size） | `GMutableSpan`（`void*` + size） |

> **为什么区分只读和可变？** 隐式共享（Copy-on-Write）。只读视图可以安全地共享数据（多个拥有者读同一块内存），可变视图需要先检查是否独占（否则深拷贝）。区分两者让编译器帮你保证正确性——你不能意外修改只读数据。

> **为什么区分单个值和数组？** 它们的操作不同：数组支持索引访问、切片、批量操作；单个值支持**取出**（`relocate_out<T>()`，把值从指针中拿走，原位置析构）和**重定位**（`relocate_construct`，移动构造到新位置 + 析构旧位置，一步完成，比拷贝+析构更高效）。混在一起会让接口混乱。

### 能学到什么设计思想？

#### 1. 类型擦除模式（Type Erasure）

这是 C++ 中非常重要的设计模式。核心思想：**把类型信息从编译期移到运行时，同时保持值语义**。

```mermaid
graph TB
    subgraph "C++ 多态方式对比"
        A["虚函数继承<br/>类型信息在 vtable 中<br/>需要基类指针"]
        B["模板<br/>类型信息在编译期<br/>每种类型生成一份代码"]
        C["类型擦除<br/>类型信息在 CPPType 中<br/>不需要继承关系"]
    end

    style C fill:#9b59b6,color:#fff
```

类型擦除的优势：
- **不需要公共基类**：`float`、`GeometrySet`、`std::string` 没有共同基类，但都可以被 `GSpan` 管理
- **值语义**：`GSpan` 可以拷贝、赋值、作为函数参数传递，不像虚函数必须用指针
- **延迟绑定**：类型在运行时才确定，支持动态配置

#### 2. 只读/可变分离（Const Correctness）

```cpp
GMutableSpan → GSpan    // ✅ 可变隐式转为只读（安全）
GSpan → GMutableSpan    // ❌ 只读不能转为可变（不安全）
```

这个模式在 C++ 标准库中也常见：`std::string::c_str()` 返回 `const char*`，`std::vector::data()` 有 const 和非 const 两个重载。Blender 把这个模式系统化了——每种泛型视图都有只读和可变两个版本。

#### 3. 零开销互转（Zero-cost Abstraction）

```cpp
Span<T> → GSpan       // 隐式转换，零开销（只存指针和 size）
GSpan → Span<T>       // typed<T>()，零开销（只检查类型，不拷贝数据）
GMutableSpan → GSpan  // 隐式转换，零开销（丢弃可变性）
```

类型化版本和泛型版本之间可以零开销互转，这意味着你可以在性能关键路径使用类型化版本，在泛型接口使用泛型版本，两者之间没有性能损失。

#### 4. 渐进式类型安全

```mermaid
flowchart LR
    A["void* + int<br/>(C 风格，无类型信息)"]
    B["GSpan<br/>(有 CPPType，运行时检查)"]
    C["Span&lt;T&gt;<br/>(编译期类型检查)"]

    A --> |"加类型信息"| B
    B --> |"typed&lt;T&gt;()"| C

    style A fill:#e74c3c,color:#fff
    style B fill:#e67e22,color:#fff
    style C fill:#2ecc71,color:#fff
```

- **C 风格**：`void*` + 手动管理大小，零类型安全，容易出错
- **泛型版本**：`GSpan` 有 `CPPType`，运行时检查类型，比 C 风格安全
- **类型化版本**：`Span<T>` 编译期检查类型，最安全

Blender 的设计允许你在安全性和灵活性之间选择：泛型接口灵活但需要运行时检查，类型化接口安全但不够灵活。

---

## 2. 类型擦除的 Span/Pointer 体系

Blender 的泛型数据视图类遵循统一的命名模式：`G` 前缀表示泛型（Generic），对应编译期类型化的版本：

> **"Generic" 叫做泛型吗？** 是的。在 C++ 语境中，"Generic Programming"（泛型编程）通常指模板，但 Blender 的 `G` 前缀类更准确地说是**类型擦除**（Type Erasure）——编译期类型信息被"擦除"，改为运行时通过 `CPPType` 保存。这与 Java/C# 的泛型（Generics）不同——后者的类型参数在编译期擦除为 `Object`，而 Blender 的类型擦除保留完整的类型操作能力（构造/析构/拷贝等）。

> **为什么需要类型擦除版本？** 核心原因是**运行时多态**。几何节点系统中，Socket 的类型在运行时才能确定（用户可以动态添加/删除输出项）。如果只有 `Span<T>`，就无法将不同类型的 Span 存入同一个容器或传递给同一个函数。类型擦除版本通过 `CPPType` 在运行时描述类型，使得泛型代码可以处理任意类型的数据。

```mermaid
graph TB
    subgraph "编译期类型化"
        S["Span&lt;T&gt;<br/>只读数组视图"]
        MS["MutableSpan&lt;T&gt;<br/>可变数组视图"]
        P["const T*<br/>只读指针"]
        MP["T*<br/>可变指针"]
    end

    subgraph "运行时泛型（类型擦除）"
        GS["GSpan<br/>泛型只读跨度"]
        GMS["GMutableSpan<br/>泛型可变跨度"]
        GP["GPointer<br/>泛型只读指针"]
        GMP["GMutablePointer<br/>泛型可变指针"]
    end

    S --> |"类型擦除"| GS
    MS --> |"类型擦除"| GMS
    P --> |"类型擦除"| GP
    MP --> |"类型擦除"| GMP

    style GS fill:#3498db,color:#fff
    style GMS fill:#e67e22,color:#fff
    style GP fill:#2ecc71,color:#fff
    style GMP fill:#e74c3c,color:#fff
```

**核心区别**：类型化版本通过模板参数 `T` 在编译期知道元素类型，泛型版本通过 `const CPPType*` 在运行时知道元素类型。

> **为什么 GSpan/GPointer 等与 CPPType 紧密耦合？** 因为 `CPPType` 是类型擦除后的**唯一类型信息来源**。类型化版本 `Span<T>` 不需要 `CPPType`——编译器已经知道 `T` 的大小、对齐、构造/析构方法。但类型擦除后，所有类型信息都丢失了，只剩 `void*`。`CPPType` 填补了这个空缺——它存储了 `size`（用于计算元素偏移）、`alignment`（用于检查指针有效性）、`copy_construct`/`destruct` 等函数指针（用于操作 `void*` 数据）。没有 `CPPType`，`GSpan` 就无法知道每个元素多大、如何拷贝、如何析构——它只是一个盲目的 `void*` 指针。

---

## 2. GSpan — 泛型只读跨度

`GSpan` 是 `Span<T>` 的泛型版本，表示一段连续内存的只读视图。

### 数据成员

```cpp
class GSpan {
 protected:
  const CPPType *type_ = nullptr;
  const void *data_ = nullptr;
  int64_t size_ = 0;
};
```

| 成员 | 类型 | 说明 |
|------|------|------|
| `type_` | `const CPPType*` | 元素的运行时类型。可为 `nullptr`（空 GSpan） |
| `data_` | `const void*` | 指向首元素的指针。`const` 表示只读（隐式共享） |
| `size_` | `int64_t` | 元素数量（不是字节数） |

> **`data_` 为什么是 `const void*`？** 因为 `GSpan` 是只读视图。数据可能被多个拥有者共享（隐式共享），不允许修改。如果需要修改，使用 `GMutableSpan`。

> **为什么变量名叫 `type_` 而非 `type_ptr_`？** 这是 Blender 的命名惯例——指针成员不加 `_ptr` 后缀。原因有二：① `type_` 更简洁，读起来更自然（`type().size()` vs `type_ptr()->size()`）；② 访问方法 `type()` 返回 `const CPPType&`（解引用后的引用），而非指针，所以从使用者角度看，`type_` 是"类型"而非"类型指针"。Blender 代码库中所有指向 `CPPType` 的成员都叫 `type_`，保持一致性。

### 构造方式

```cpp
// 从 CPPType + 原始指针
GSpan(const CPPType &type, const void *buffer, int64_t size);

// 从类型化 Span（隐式转换）
GSpan(Span<T> array);  // 自动获取 CPPType::get<T>()

// 从类型化 MutableSpan（隐式转换，丢弃可变性）
GSpan(MutableSpan<T> array);
```

> **`Span<T>` → `GSpan` 的隐式转换**：这是安全的，因为 `Span<T>` 是 `GSpan` 的子集（只读 + 类型已知）。转换时自动获取 `CPPType::get<T>()`。

> **`CPPType::get<T>()` 是干什么的？** 它是获取类型 `T` 对应的 `CPPType` 单例的模板函数。对于每个已注册的类型 `T`，`CPPType::get<T>()` 返回同一个静态全局对象的引用。例如 `CPPType::get<float>()` 返回 `float` 类型的 `CPPType` 实例（包含 `size=4`, `alignment=4`, `is_trivial=true` 等），`CPPType::get<int>()` 返回 `int` 类型的实例。在 `GSpan(Span<T> array)` 构造函数中，`CPPType::get<T>()` 自动从编译期类型 `T` 获取运行时类型信息，完成类型化到泛型的桥接。

> **类型在哪里注册的？** 注册分两层，都在程序启动时执行：
>
> 1. **基础类型**（[blenlib/intern/cpp_types.cc](../../source/blender/blenlib/intern/cpp_types.cc)）：`register_cpp_types()` 函数中注册 `bool`、`float`、`float3`、`int32_t`、`std::string` 等基础类型。
>
> 2. **BKE 类型**（[blenkernel/intern/cpp_types.cc](../../source/blender/blenkernel/intern/cpp_types.cc)）：`BKE_cpp_types_init()` 先调用 `register_cpp_types()`，再注册 `GeometrySet`、`Object*`、`ClosurePtr`、**`GListPtr`** 等业务类型。
>
> 注册宏 `BLI_CPP_TYPE_REGISTER(TYPE_NAME, FLAGS)` 展开后调用 `detail::register_cpp_type<T, FLAGS>(name)`，在静态内存上 placement new 构造 `CPPType` 对象，并注册到全局查找表中。之后 `CPPType::get<T>()` 就能找到它——内部实现是 `detail::cpp_type_impl<std::decay_t<T>>.ref()`，返回之前构造的静态对象引用。如果类型未注册就调用 `CPPType::get<T>()`，会触发断言 `BLI_assert(type.size > 0)` 失败。
>
> ```mermaid
> sequenceDiagram
>     participant Startup as Blender 启动
>     participant BKE as BKE_cpp_types_init()
>     participant BLI as register_cpp_types()
>     participant Macro as BLI_CPP_TYPE_REGISTER
>     participant Static as 静态内存
>     participant User as 用户代码
>
>     Startup->>BKE: 调用
>     BKE->>BLI: register_cpp_types()
>     BLI->>Macro: BLI_CPP_TYPE_REGISTER(float, BasicType)
>     Macro->>Static: placement new CPPType(TypeTag<float>{}, ...)
>     Note over Static: cpp_type_impl<float> 现在有值了
>     BLI->>Macro: BLI_CPP_TYPE_REGISTER(int32_t, BasicType)
>     Macro->>Static: placement new CPPType(TypeTag<int32_t>{}, ...)
>     BKE->>Macro: BLI_CPP_TYPE_REGISTER(GListPtr, ...)
>     Macro->>Static: placement new CPPType(TypeTag<GListPtr>{}, ...)
>
>     User->>Static: CPPType::get<float>()
>     Static-->>User: 返回 float 的 CPPType 引用
> ```

### 元素访问

```cpp
const void *operator[](int64_t index) const
{
  BLI_assert(index < size_);
  return POINTER_OFFSET(data_, type_->size * index);
}
```

> **返回 `const void*` 而非 `const T&`**：因为类型在运行时才知道，无法返回类型化引用。调用者需要自己 `static_cast<const T*>(span[index])`。

> **`POINTER_OFFSET(ptr, offset)` 宏详解**：
> ```cpp
> #define POINTER_OFFSET(v, ofs) \
>   (reinterpret_cast<std::remove_reference_t<decltype(v)>>((char *)(v) + (ofs)))
> ```
> 
> 这个宏将指针 `v` 偏移 `ofs` 字节后返回同类型的指针。逐步拆解：
> 
> 1. **`(char *)(v) + (ofs)`**：将指针转为 `char*` 后加偏移。为什么用 `char*`？因为 C++ 中 `char` 的大小定义为 1 字节，`char*` 的指针算术以字节为单位。`void*` 不支持指针算术（C++ 标准禁止），`int*` 的 `+1` 会偏移 4 字节而非 1 字节。只有 `char*` 的 `+ofs` 精确偏移 `ofs` 字节。
> 
> 2. **`decltype(v)`**：C++11 关键字，获取表达式 `v` 的**声明类型**。如果 `v` 是 `const void*`，`decltype(v)` 就是 `const void*`；如果 `v` 是 `void*`，`decltype(v)` 就是 `void*`。
> 
> 3. **`std::remove_reference_t<decltype(v)>`**：移除引用类型。如果 `v` 是引用（如 `const void*&`），`remove_reference_t` 去掉 `&` 得到 `const void*`。这是防御性编程——确保 `reinterpret_cast` 的目标类型不是引用。
> 
> 4. **`reinterpret_cast<...>(...)`**：将偏移后的 `char*` 转回原始指针类型。如果输入是 `const void*`，输出也是 `const void*`；如果输入是 `void*`，输出也是 `void*`。这保持了 const 正确性。
> 
> **在 GSpan 中的使用**：`POINTER_OFFSET(data_, type_->size * index)` 计算 `data_` 偏移 `index` 个元素后的地址。`type_->size` 是每个元素的字节数（如 `float` 是 4），乘以 `index` 得到字节偏移量。

### typed\<T\>() — 转回类型化 Span

```cpp
template<typename T> Span<T> typed() const
{
  BLI_assert(size_ == 0 || type_ != nullptr);
  BLI_assert(type_ == nullptr || type_->is<T>());
  return Span<T>(static_cast<const T *>(data_), size_);
}
```

> **`type_->is<T>()`**：运行时类型检查。如果 `GSpan` 实际存储的不是 `T` 类型，会触发断言失败。这是安全的"向下转型"。

### 切片操作

```cpp
GSpan slice(int64_t start, int64_t size) const;
GSpan drop_front(int64_t n) const;
GSpan drop_back(int64_t n) const;
GSpan take_front(int64_t n) const;
GSpan take_back(int64_t n) const;
```

> **零拷贝**：切片操作只调整 `data_` 指针和 `size_`，不复制数据。

---

## 3. GMutableSpan — 泛型可变跨度

`GMutableSpan` 是 `MutableSpan<T>` 的泛型版本，表示一段连续内存的可变视图。

### 与 GSpan 的区别

| 特性 | GSpan | GMutableSpan |
|------|-------|-------------|
| `data_` 类型 | `const void*` | `void*` |
| 元素访问返回 | `const void*` | `void*` |
| `typed<T>()` 返回 | `Span<T>` | `MutableSpan<T>` |
| 可修改数据 | ❌ | ✅ |
| 隐式转换为 GSpan | — | ✅ |

### 隐式转换运算符

```cpp
operator GSpan() const
{
  return GSpan(type_, data_, size_);
}
```

> **`GMutableSpan` → `GSpan` 隐式转换**：丢弃可变性，从 `void*` 变为 `const void*`。这是安全的——可变视图可以当作只读视图使用，反之不行。

### copy_from — 批量赋值

```cpp
void copy_from(GSpan values)
{
  BLI_assert(type_ == &values.type());
  BLI_assert(size_ == values.size());
  type_->copy_assign_n(values.data(), data_, size_);
}
```

> **`copy_assign_n` 而非 `copy_construct_n`**：因为目标内存已经初始化（`GMutableSpan` 指向已有数据），需要赋值而非构造。

---

## 4. GPointer — 泛型只读指针

`GPointer` 是类型擦除的 `const T*`，指向单个值。

### 数据成员

```cpp
class GPointer {
 private:
  const CPPType *type_ = nullptr;
  const void *data_ = nullptr;
};
```

> **与 `GSpan` 的区别**：`GPointer` 指向单个值，没有 `size_`。`GSpan` 指向连续数组，有 `size_`。

### 构造方式

```cpp
// 从 GMutablePointer（隐式转换）
GPointer(GMutablePointer ptr);

// 从 CPPType + 原始指针
GPointer(const CPPType &type, const void *data = nullptr) : type_(&type), data_(data) {}

// 从类型化指针（隐式转换）
template<typename T>
GPointer(T *data)
  requires(!std::is_void_v<T>)
    : GPointer(&CPPType::get<T>(), data)
{}
```

> **`std::is_void_v<T>` 是什么？** C++17 类型特征，判断 `T` 是否为 `void` 类型。它的定义是：
> ```cpp
> template<class _Ty>
> constexpr bool is_void_v = is_same_v<remove_cv_t<_Ty>, void>;
> ```
> 逐步拆解：
> 1. **`_Ty`**：微软 MSVC 标准库的命名惯例，**Type** 的缩写（`T` + `y` 后缀），就是"类型"的意思，等价于更常见的 `T`。以下划线加大写字母开头的名称在 C++ 中被保留给标准库实现。
> 2. **`remove_cv_t<_Ty>`**：移除 const/volatile 限定符。`const void` → `void`，`volatile void` → `void`。
> 3. **`is_same_v<..., void>`**：判断去除 cv 后的类型是否为 `void`。
> 4. **`constexpr bool`**：编译期常量，`true` 或 `false`。
>
> 所以 `is_void_v<void>` = `true`，`is_void_v<const void>` = `true`，`is_void_v<int>` = `false`。

> **`requires(!std::is_void_v<T>)` 是什么？** C++20 Concepts 约束子句。把它想象成**门卫**——`requires(条件)` 里的条件为 `true` → 放行（函数存在）；为 `false` → 拒绝（函数不存在）。
>
> **没有门卫会怎样？** 编译器遇到 `GPointer(void *data)` 时，会老老实实地展开模板：
> ```cpp
> // T = void 时，编译器展开模板：
> GPointer(void *data)
>   : GPointer(&CPPType::get<void>(), data)  // ← get<void>() 不存在！编译错误！
> {}
> ```
> 就像你填了一张表，表上要求写"身份证号"，但你没有身份证——填到这一步就卡住了。
>
> **有了门卫后：** 编译器先检查门卫条件：
> - `T = void` → `requires(!true)` → `requires(false)` → 门卫说"你不符合条件，走开" → 编译器**根本不展开**这个模板 → 不会碰到 `get<void>()` → 不会出错
> - `T = float` → `requires(!false)` → `requires(true)` → 门卫说"通过" → 编译器展开模板 → 正常工作
>
> 简单理解：**`requires(条件)` 就是"只有条件满足时，这个函数才存在"。条件不满足时，编译器当这个函数不存在，不会尝试编译它。**
>
> **函数不存在时，调用会怎样？** 会报错——但报的是更清晰的错误。没有 `requires` 时，`GPointer(void*)` 会深入模板实例化后报 `CPPType::get<void>()` 不存在（错误信息又长又难懂）。有 `requires` 时，`GPointer(void*)` 直接报"no matching constructor"（错误信息简短清晰）。两种情况都报错，但 `requires` 让错误发生在更早的阶段，信息更易懂。如果确实需要传 `void*`，用显式构造函数 `GPointer(CPPType::get<float>(), (const void*)ptr)` 手动提供类型信息。

> **`&CPPType::get<T>()` 为什么取地址？** `GPointer` 有两个接受类型信息的构造函数：
> 1. `GPointer(const CPPType *type, const void *data)` — 接受**指针**
> 2. `GPointer(const CPPType &type, const void *data)` — 接受**引用**
>
> `CPPType::get<T>()` 返回 `const CPPType&`（引用），`&` 取其地址得到 `const CPPType*`（指针），匹配第1个构造函数。委托构造 `GPointer(&CPPType::get<T>(), data)` 最终调用指针版本，将指针存入 `type_` 成员。
>
> 取地址是安全的，因为 `CPPType::get<T>()` 返回的是静态全局对象的引用，地址在整个程序生命周期内有效。
>
> **为什么不直接用引用版本？** `GPointer(&CPPType::get<T>(), data)` 也可以写成 `GPointer(CPPType::get<T>(), data)`（调用引用版本），两者效果相同。使用 `&` 取地址再传指针只是代码风格选择——明确表示 `type_` 存储的是指针而非引用。

### operator bool() — 上下文转换为布尔值

```cpp
operator bool() const
{
  return data_ != nullptr;
}
```

> **`operator bool()` 是什么？** 用户定义的**隐式转换运算符**，允许 `GPointer` 对象在布尔上下文中使用。
>
> **没有 `operator bool()` 不能当 bool 用吗？** 是的，不能。C++ 不会自动把类对象转为 `bool`：
> ```cpp
> // 没有 operator bool() 时：
> GPointer ptr;
> if (ptr) { ... }    // ❌ 编译错误！编译器不知道怎么把 GPointer 转为 bool
> bool b = ptr;       // ❌ 编译错误！
> ```
> C++ 只支持内置类型的隐式转换（如 `int` → `double`、指针 → `bool`），用户自定义类型必须显式提供转换运算符。
>
> 有了 `operator bool()` 后：
> ```cpp
> GPointer ptr = some_function();
> if (ptr) {          // ✅ 调用 operator bool()，等价于 ptr.data_ != nullptr
>   // ptr 有值
> }
> if (!ptr) {         // ✅ 先调用 operator bool()，再取反
>   // ptr 为空
> }
> ```
> C++ 标准库的智能指针（`std::unique_ptr`、`std::shared_ptr`）也使用同样的模式。

> **`GMutablePointer` → `GPointer` 隐式转换**：与 `GMutableSpan` → `GSpan` 类似，丢弃可变性。

### is_type\<T\>() — 类型检查

```cpp
template<typename T> bool is_type() const
{
  return type_ != nullptr && type_->is<T>();
}
```

### get\<T\>() — 获取类型化指针

```cpp
template<typename T> const T *get() const
{
  BLI_assert(this->is_type<T>());
  return static_cast<const T *>(data_);
}
```

---

## 5. GMutablePointer — 泛型可变指针

`GMutablePointer` 是类型擦除的 `T*`，指向单个可变值。

### 与 GPointer 的区别

| 特性 | GPointer | GMutablePointer |
|------|----------|----------------|
| `data_` 类型 | `const void*` | `void*` |
| `get()` 返回 | `const void*` | `void*` |
| `get<T>()` 返回 | `const T*` | `T*` |
| 可修改数据 | ❌ | ✅ |
| `relocate_out<T>()` | ❌ | ✅ |
| `destruct()` | ❌ | ✅ |

### relocate_out\<T\>() — 重定位取出

```cpp
template<typename T> T relocate_out()
{
  BLI_assert(this->is_type<T>());
  T value;
  type_->relocate_assign(data_, &value);  // 移动构造到 value + 析构源
  data_ = nullptr;
  type_ = nullptr;
  return value;
}
```

> **`relocate_assign`**：移动构造 + 析构源。比"拷贝 + 析构源"更高效。调用后 `GMutablePointer` 变为空（`data_ = nullptr`），因为值已经被取走。

> **使用场景**：从 `LazyFunction` 的输出中取出值。输出值存储在 `void*` 内存中，通过 `relocate_out<T>()` 取出后，原始位置不再持有有效值。

### destruct() — 析构值

```cpp
void destruct()
{
  BLI_assert(data_ != nullptr);
  type_->destruct(data_);
}
```

> **何时使用？** 当值不再需要时，必须调用 `destruct()` 释放资源（如 `std::string` 的堆内存）。对于平凡类型（`float`、`int`），`destruct` 是空操作。

---

## 6. 四者关系与转换规则

```mermaid
flowchart LR
    GMS["GMutableSpan<br/>void* + size"]
    GS["GSpan<br/>const void* + size"]
    GMP["GMutablePointer<br/>void*"]
    GP["GPointer<br/>const void*"]

    GMS --> |"operator GSpan()"| GS
    GMP --> |"operator GPointer()"| GP

    GS -.-> |"typed&lt;T&gt;()"| S["Span&lt;T&gt;"]
    GMS -.-> |"typed&lt;T&gt;()"| MS["MutableSpan&lt;T&gt;"]
    GP -.-> |"get&lt;T&gt;()"| CP["const T*"]
    GMP -.-> |"get&lt;T&gt;()"| MP["T*"]

    S --> |"隐式转换"| GS
    MS --> |"隐式转换"| GMS
    CP --> |"隐式转换"| GP
    MP --> |"隐式转换"| GMP

    style GMS fill:#e67e22,color:#fff
    style GS fill:#3498db,color:#fff
    style GMP fill:#e74c3c,color:#fff
    style GP fill:#2ecc71,color:#fff
```

**转换规则总结**：

| 从 | 到 | 方式 | 安全性 |
|----|-----|------|--------|
| `Span<T>` | `GSpan` | 隐式转换 | ✅ 安全 |
| `MutableSpan<T>` | `GMutableSpan` | 隐式转换 | ✅ 安全 |
| `MutableSpan<T>` | `GSpan` | 隐式转换（经 GMutableSpan） | ✅ 安全（丢弃可变性） |
| `GMutableSpan` | `GSpan` | 隐式转换 | ✅ 安全（丢弃可变性） |
| `GMutablePointer` | `GPointer` | 隐式转换 | ✅ 安全（丢弃可变性） |
| `GSpan` | `Span<T>` | `typed<T>()` | ⚠️ 需类型匹配 |
| `GMutableSpan` | `MutableSpan<T>` | `typed<T>()` | ⚠️ 需类型匹配 |
| `GSpan` | `GMutableSpan` | 无 | ❌ 不允许（需 const_cast） |
| `GPointer` | `GMutablePointer` | 无 | ❌ 不允许 |

---

## 7. 在列表系统中的应用

### GList::ArrayData 使用 GSpan/GMutableSpan

```cpp
struct ArrayData {
  const void *data;
  ImplicitSharingPtr<> sharing_info;

  GSpan span(const CPPType &type, int64_t size) const {
    return GSpan(type, data, size);
  }

  GMutableSpan span_for_write(const CPPType &type, int64_t size) {
    // 写时复制...
    return GMutableSpan(type, const_cast<void *>(data), size);
  }
};
```

### GList::SingleData 使用 GPointer

```cpp
struct SingleData {
  const void *value;
  ImplicitSharingPtr<> sharing_info;

  GPointer pointer(const CPPType &type) const {
    return GPointer(type, value);
  }
};
```

### List\<T\>::values() 使用 GSpan 和 GPointer

```cpp
template<typename T> std::variant<Span<T>, const T *> List<T>::values() const
{
  const std::variant<GSpan, GPointer> values = list_.values();
  if (const auto *span_values = std::get_if<GSpan>(&values)) {
    return span_values->typed<T>();    // GSpan → Span<T>
  }
  if (const auto *single_value = std::get_if<GPointer>(&values)) {
    return single_value->get<T>();     // GPointer → const T*
  }
}
```

```mermaid
flowchart TD
    GList["GList<br/>DataVariant data_"]
    AD["ArrayData<br/>const void* data"]
    SD["SingleData<br/>const void* value"]

    GList --> AD
    GList --> SD

    AD --> |"span()"| GS["GSpan(type, data, size)"]
    SD --> |"pointer()"| GP["GPointer(type, value)"]

    GS --> |"typed&lt;T&gt;()"| S["Span&lt;T&gt;"]
    GP --> |"get&lt;T&gt;()"| CP["const T*"]

    style GS fill:#3498db,color:#fff
    style GP fill:#2ecc71,color:#fff
```
