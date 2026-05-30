# CPPType — 运行时类型信息系统

> 📖 系列文档：[目录](01-列表系统架构与核心数据结构.md) | [上一篇](12-列表节点对比与设计总结.md) | [下一篇](14-GSpan与GPointer泛型视图.md)
> 源码文件：[BLI_cpp_type.hh](../../source/blender/blenlib/BLI_cpp_type.hh)、[BLI_cpp_type_make.hh](../../source/blender/blenlib/BLI_cpp_type_make.hh)

---

## 目录

1. [为什么需要 CPPType](#1-为什么需要-cpptype)
2. [核心设计思想](#2-核心设计思想)
3. [类结构与成员详解](#3-类结构与成员详解)
4. [类型注册机制](#4-类型注册机制)
5. [常用操作详解](#5-常用操作详解)
6. [在列表系统中的应用](#6-在列表系统中的应用)
7. [与 C++ RTTI 的对比](#7-与-c++-rtti-的对比)

---

## 1. 为什么需要 CPPType

C++ 的模板系统在编译期提供了强大的类型安全，但在某些场景下类型必须在运行时才能确定：

```mermaid
graph TB
    subgraph "编译期已知类型"
        T1["Span&lt;float&gt;<br/>元素类型 = float"]
        T2["Vector&lt;int&gt;<br/>元素类型 = int"]
    end

    subgraph "运行时才知类型"
        G1["GSpan<br/>元素类型 = ???"]
        G2["GList<br/>元素类型 = ???"]
        G3["GVArray<br/>元素类型 = ???"]
    end

    T1 --> |"类型擦除"| G1
    T2 --> |"类型擦除"| G1

    style G1 fill:#e67e22,color:#fff
    style G2 fill:#e67e22,color:#fff
    style G3 fill:#e67e22,color:#fff
```

**问题**：当你有一个 `void*` 指针和运行时类型信息时，如何正确地构造、析构、拷贝、移动、比较元素？

**答案**：`CPPType` 将 C++ 类型的所有操作存储为函数指针，使得在类型擦除后仍能正确操作数据。

---

## 2. 核心设计思想

`CPPType` 的核心思想是**将类型的操作从编译期绑定变为运行时查找**：

```mermaid
graph LR
    subgraph "编译期（模板）"
        CT["Span&lt;T&gt;<br/>T::copy_construct()<br/>T::~T()"]
    end

    subgraph "运行时（CPPType）"
        RT["GSpan<br/>type_.copy_construct_fn()<br/>type_.destruct_fn()"]
    end

    CT --> |"类型擦除"| RT

    style RT fill:#9b59b6,color:#fff
```

每个 `CPPType` 实例是一个**单例**——对于同一个 C++ 类型，全局只有一个 `CPPType` 对象：

```cpp
const CPPType &float_type = CPPType::get<float>();
const CPPType &float_type2 = CPPType::get<float>();
// &float_type == &float_type2  （同一个对象）
```

> **单例设计**：`CPPType::get<T>()` 返回的是静态全局对象的引用。这使得比较类型只需比较指针——`&type1 == &type2` 就能判断两个类型是否相同，比字符串比较快得多。

---

## 3. 类结构与成员详解

```mermaid
classDiagram
    class CPPType {
        +size : int64_t
        +alignment : int64_t
        +is_trivial : bool
        +is_trivially_destructible : bool
        +has_special_member_functions : bool
        +is_default_constructible : bool
        +is_copy_constructible : bool
        +is_move_constructible : bool
        +is_destructible : bool
        +is_copy_assignable : bool
        +is_move_assignable : bool
        +type_index : int
        -default_construct_ : function
        -destruct_ : function
        -copy_construct_ : function
        -move_construct_ : function
        -copy_assign_ : function
        -move_assign_ : function
        -relocate_construct_ : function
        -fill_assign_n_ : function
        -print_ : function
        -is_equal_ : function
        -hash_ : function
        -default_value_ : const void*
        -debug_name_ : string
        +get~T~()$ const CPPType&
        +default_construct(void*)
        +destruct(void*)
        +copy_construct(const void*, void*)
        +move_construct(void*, void*)
        +copy_assign(const void*, void*)
        +move_assign(void*, void*)
        +relocate_construct(void*, void*)
        +is~T~() bool
        +default_value() const void*
        +print(const void*, stringstream&)
        +hash(const void*) uint64_t
    }
```

### 公共成员

| 成员 | 类型 | 对应 C++ | 说明 |
|------|------|---------|------|
| `size` | `int64_t` | `sizeof(T)` | 单个元素占用的字节数 |
| `alignment` | `int64_t` | `alignof(T)` | 内存对齐要求 |
| `is_trivial` | `bool` | `std::is_trivial_v<T>` | 是否可以用 `memcpy` 拷贝 |
| `is_trivially_destructible` | `bool` | `std::is_trivially_destructible_v<T>` | 析构是否是空操作 |
| `has_special_member_functions` | `bool` | — | 是否有完整的特殊成员函数 |
| `type_index` | `int` | — | 唯一索引，用于快速比较 |

### 函数指针成员

每个函数指针对应一个 C++ 操作：

| 函数指针 | 签名 | 对应操作 |
|---------|------|---------|
| `default_construct_` | `void(void*)` | 在未初始化内存上默认构造 |
| `destruct_` | `void(void*)` | 析构（不释放内存） |
| `copy_construct_` | `void(const void*, void*)` | 拷贝构造（src → 未初始化 dst） |
| `move_construct_` | `void(void*, void*)` | 移动构造（src → 未初始化 dst） |
| `copy_assign_` | `void(const void*, void*)` | 拷贝赋值（src → 已初始化 dst） |
| `move_assign_` | `void(void*, void*)` | 移动赋值（src → 已初始化 dst） |
| `relocate_construct_` | `void(void*, void*)` | 重定位（移动构造 + 析构源） |
| `is_equal_` | `bool(const void*, const void*)` | 比较两个值是否相等 |
| `hash_` | `uint64_t(const void*)` | 计算哈希值 |

> **`copy_construct` vs `copy_assign`**：`copy_construct` 在**未初始化**的内存上构造（placement new），`copy_assign` 在**已初始化**的内存上赋值（先析构旧值再构造新值，或直接 `operator=`）。

> **`relocate_construct`**：等价于移动构造 + 析构源。对于平凡类型，就是 `memcpy`。对于非平凡类型，先移动构造到目标，再析构源。这比"拷贝构造 + 析构源"更高效。

### 批量操作

每个单元素操作都有对应的批量版本：

```cpp
void default_construct_n(void *ptr, int64_t n);
void destruct_n(void *ptr, int64_t n);
void copy_construct_n(const void *src, void *dst, int64_t n);
void move_construct_n(void *src, void *dst, int64_t n);
void copy_assign_n(const void *src, void *dst, int64_t n);
void move_assign_n(void *src, void *dst, int64_t n);
void fill_assign_n(const void *value, void *dst, int64_t n);
void fill_construct_n(const void *value, void *dst, int64_t n);
```

> **批量操作的优化**：对于平凡类型（如 `float`、`int`），批量操作直接使用 `memcpy` 或 `memset`，比逐个操作快得多。对于非平凡类型（如 `std::string`），则逐个调用对应的操作。

### IndexMask 版本

还有接受 `IndexMask` 的版本，只对掩码指定的索引操作：

```cpp
void default_construct_indices(void *ptr, const IndexMask &mask);
void destruct_indices(void *ptr, const IndexMask &mask);
void copy_construct_indices(const void *src, void *dst, const IndexMask &mask);
// ...
```

> **IndexMask 的用途**：在几何节点中，经常只需要对部分元素操作（如被选中的顶点）。`IndexMask` 高效地表示这些索引，避免操作整个数组。

---

## 4. 类型注册机制

`CPPType` 使用宏注册类型，在程序启动时自动创建单例：

```cpp
// 在 .cc 文件中注册类型
BLI_CPP_TYPE_IMPLEMENT(float);
BLI_CPP_TYPE_IMPLEMENT(int);
BLI_CPP_TYPE_IMPLEMENT(blender::float3);
BLI_CPP_TYPE_IMPLEMENT(std::string);
```

### BLI_CPP_TYPE_MAKE 宏

```cpp
// 在 .hh 文件中声明类型
BLI_CPP_TYPE_MAKE(float, CPPTypeFlags::BasicType)
```

展开后大致等价于：

```cpp
template<> const CPPType &CPPType::get<float>()
{
  static CPPType instance{TypeTag<float>{}, TypeForValue<CPPTypeFlags, Flags>{}, "float"};
  return instance;
}
```

> **`TypeTag<T>`**：空结构体，用于在构造函数中传递类型信息。`CPPType` 的构造函数是模板函数，通过 `TypeTag<T>` 推断类型 `T`，然后为每个函数指针成员绑定对应的 `T` 操作。

### CPPTypeFlags

```cpp
enum class CPPTypeFlags {
  None = 0,
  Hashable = 1 << 0,
  Printable = 1 << 1,
  EqualityComparable = 1 << 2,
  IdentityDefaultValue = 1 << 3,
  BasicType = Hashable | Printable | EqualityComparable,
};
```

| 标志 | 含义 |
|------|------|
| `Hashable` | 支持 `hash_` 函数 |
| `Printable` | 支持 `print_` 函数 |
| `EqualityComparable` | 支持 `is_equal_` 函数 |
| `IdentityDefaultValue` | 默认值是全零（如 `int(0)`, `float(0.0f)`） |
| `BasicType` | 同时具备 Hashable + Printable + EqualityComparable |

---

## 5. 常用操作详解

### is\<T\>() — 类型检查

```cpp
template<typename T> bool is() const
{
  return this == &CPPType::get<T>();
}
```

> **比较指针而非名称**：因为 `CPPType::get<T>()` 返回单例，所以只需比较指针就能判断类型是否相同。这比字符串比较（`name == "float"`）快得多，且不会出错。

### default_value() — 获取默认值

```cpp
const void *default_value() const
{
  return default_value_;
}
```

返回指向类型默认值的指针。对于 `float`，指向 `0.0f`；对于 `int`，指向 `0`；对于 `std::string`，指向空字符串。

### pointer_has_valid_alignment() — 对齐检查

```cpp
bool pointer_has_valid_alignment(const void *ptr) const
{
  return (uintptr_t(ptr) & alignment_mask_) == 0;
}
```

> **`alignment_mask_`**：预计算的掩码，`alignment - 1`。如果指针地址与掩码按位与为零，则对齐正确。这比取模运算快。

---

## 6. 在列表系统中的应用

`CPPType` 是列表系统类型擦除的基础：

```mermaid
flowchart TD
    subgraph "类型化层"
        LT["List&lt;float&gt;<br/>元素类型编译期已知"]
        LS["Span&lt;float&gt;<br/>直接访问 T&"]
    end

    subgraph "类型擦除层"
        GL["GList<br/>const CPPType& cpp_type_"]
        GS["GSpan<br/>const CPPType* type_"]
    end

    subgraph "CPPType 操作"
        OP1["type.copy_construct_n()"]
        OP2["type.destruct_n()"]
        OP3["type.size"]
        OP4["type.is&lt;T&gt;()"]
    end

    LT --> |"reinterpret_cast"| GL
    LS --> |"隐式转换"| GS
    GL --> OP1
    GL --> OP2
    GL --> OP3
    GS --> OP4

    style GL fill:#9b59b6,color:#fff
    style GS fill:#e67e22,color:#fff
```

### GList 中的使用

```cpp
// GList::ArrayData::span_for_write — 深拷贝时使用 CPPType
void *new_data = MEM_new_array_uninitialized_aligned(size, type.size, type.alignment, __func__);
type.copy_construct_n(this->data, new_data, size);  // 通过 CPPType 逐个拷贝构造
```

```cpp
// GList::ArrayData::ForDefaultValue — 创建默认值数组
ArrayData ArrayData::ForDefaultValue(const CPPType &type, int64_t size)
{
  void *data = MEM_new_array_uninitialized_aligned(size, type.size, type.alignment, __func__);
  type.default_construct_n(data, size);  // 通过 CPPType 逐个默认构造
  // ...
}
```

### GSpan 中的使用

```cpp
// GSpan::operator[] — 通过 CPPType 计算偏移
const void *operator[](int64_t index) const
{
  return POINTER_OFFSET(data_, type_->size * index);  // type_->size = sizeof(T)
}
```

### GVArray 中的使用

```cpp
// GVArray::typed<T>() — 类型检查
BLI_assert(impl_->type().is<T>());  // 运行时类型检查
```

---

## 7. 与 C++ RTTI 的对比

| 特性 | C++ RTTI (`typeid`) | CPPType |
|------|-------------------|---------|
| 类型名称 | ✅ `typeid(T).name()` | ✅ `debug_name_` |
| 类型比较 | ✅ `typeid(a) == typeid(b)` | ✅ `&type1 == &type2`（指针比较） |
| 构造/析构 | ❌ | ✅ 函数指针 |
| 拷贝/移动 | ❌ | ✅ 函数指针 |
| 哈希 | ❌ | ✅ `hash_` |
| 打印 | ❌ | ✅ `print_` |
| 默认值 | ❌ | ✅ `default_value_` |
| 对齐信息 | ❌ | ✅ `alignment` |
| 批量操作 | ❌ | ✅ `*_n` / `*_indices` |
| 性能开销 | 有（需启用 RTTI） | 无（编译期生成） |
| 跨编译单元 | 可能不一致 | 一致（单例） |

> **为什么不用 C++ RTTI？** Blender 编译时禁用了 RTTI（`-fno-rtti`），因为 RTTI 增加二进制大小且有性能开销。`CPPType` 提供了更丰富的功能，且通过宏在编译期生成，零运行时开销。

---

## 附录：前向声明头文件的作用

[NOD_geometry_nodes_list_fwd.hh](../../source/blender/nodes/NOD_geometry_nodes_list_fwd.hh) 只包含前向声明：

```cpp
namespace blender::nodes {
class GList;
class GListPtr;
template<typename T> class List;
template<typename T> class ListPtr;
}
```

**为什么需要单独的前向声明头文件？** 当两个头文件互相引用对方的类时，会产生循环依赖。前向声明打破循环——只需要知道类名（不需要知道类的大小和成员），就可以声明指针或引用。

```mermaid
graph LR
    FWD["list_fwd.hh<br/>前向声明"]
    MAIN["list.hh<br/>完整定义"]
    OTHER["其他头文件<br/>只需指针/引用"]

    FWD --> MAIN
    OTHER --> FWD

    style FWD fill:#2ecc71,color:#fff
    style MAIN fill:#e74c3c,color:#fff
```

**具体场景**：`NOD_geometry_nodes_list.hh` 包含了 `BLI_generic_virtual_array.hh`（因为 `GList` 使用 `GVArray`），而 `BLI_generic_virtual_array.hh` 可能间接依赖某些前向声明。`list_fwd.hh` 使得其他文件只需 `#include "NOD_geometry_nodes_list_fwd.hh"` 就能使用 `GList*` 或 `ListPtr<T>` 的引用，而不需要拉入整个 `list.hh` 的重量级依赖链。
