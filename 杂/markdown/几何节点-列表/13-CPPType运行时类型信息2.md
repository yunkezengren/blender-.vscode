# 13. CPPType 运行时类型信息

> 源文件：`source/blender/blenlib/BLI_cpp_type.hh`（第 1~791 行）

---

## 一、文件头部注释（第 1~73 行）

```cpp
/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

#pragma once
```

- **SPDX 声明**：标准的 Blender 版权与许可证头。`GPL-2.0-or-later` 表示代码采用 GPL 2.0 或更新版本授权。
- **`#pragma once`**：确保头文件在单个编译单元中只被包含一次，是 `#ifndef` 守卫的现代替代写法。

```cpp
/** \file
 * \ingroup bli
 *
 * The `CPPType` class allows working with arbitrary C++ types in a generic way. An instance of
 * #CPPType wraps exactly one type like `int` or `std::string`.
 *
 * With #CPPType one can write generic data structures and algorithms. That is similar to what C++
 * templates allow. The difference is that when using templates, the types have to be known at
 * compile time and the code has to be instantiated multiple times. On the other hand, when using
 * #CPPType, the data type only has to be known at run-time, and the code only has to be compiled
 * once. Whether #CPPType or classic c++ templates should be used depends on the context:
 * - If the data type is not known at run-time, #CPPType should be used.
 * - If the data type is known to be one of a few, it depends on how performance sensitive the code
 *   is.
 *   - If it it's a small hot loop, a template can be used to optimize for every type (at the
 *     cost of longer compile time, a larger binary and the complexity that comes from using
 *     templates).
 *   - If the code is not performance sensitive, it usually makes sense to use #CPPType instead.
 * - Sometimes a combination can make sense. Optimized code can be generated at compile-time for
 *   some types, while there is a fallback code path using #CPPType for all other types.
 *   #CPPType::to_static_type allows dispatching between both versions based on the type.
 *
 * Under some circumstances, #CPPType serves a similar role as #std::type_info. However, #CPPType
 * has much more utility because it contains methods for actually working with instances of the
 * type.
 *
 * Every type has a size and an alignment. Every function dealing with C++ types in a generic way,
 * has to make sure that alignment rules are followed. The methods provided by a #CPPType instance
 * will check for correct alignment as well.
 *
 * Every type has a name that is for debugging purposes only. It should not be used as identifier.
 *
 * To check if two instances of #CPPType represent the same type, only their pointers have to be
 * compared. Any C++ type has at most one corresponding #CPPType instance.
 *
 * A #CPPType instance comes with many methods that allow dealing with types in a generic way. Most
 * methods come in three variants. Using the default-construct methods as an example:
 *  - `default_construct(void *ptr)`:
 *      Constructs a single instance of that type at the given pointer.
 *  - `default_construct_n(void *ptr, int64_t n)`:
 *      Constructs n instances of that type in an array that starts at the given pointer.
 *  - `default_construct_indices(void *ptr, const IndexMask &mask)`:
 *      Constructs multiple instances of that type in an array that starts at the given pointer.
 *      Only the indices referenced by `mask` will by constructed.
 *
 * In some cases default-construction does nothing (e.g. for trivial types like int). The
 * `default_value` method provides some default value anyway that can be copied instead. What the
 * default value is, depends on the type. Usually it is something like 0 or an empty string.
 *
 *
 * Implementation Considerations
 * -----------------------------
 *
 * Concepts like inheritance are currently not captured by this system. This is not because it is
 * not possible, but because it was not necessary to add this complexity yet.
 *
 * One could also implement CPPType itself using virtual methods and a child class for every
 * wrapped type. However, the approach used now with explicit function pointers to works better.
 * Here are some reasons:
 *  - If CPPType would be inherited once for every used C++ type, we would get a lot of classes
 *    that would only be instanced once each.
 *  - Methods like `default_construct` that operate on a single instance have to be fast. Even this
 *    one necessary indirection using function pointers adds a lot of overhead. If all methods were
 *    virtual, there vtable adds a second level of indirection that increases the overhead even more.
 *  - If it becomes necessary, we could pass the function指针 to C functions more easily than
 *    pointers to virtual member functions.
 */
```

### 逐段翻译与解读

#### 1. 核心设计目标

> The `CPPType` class allows working with arbitrary C++ types in a generic way. An instance of `#CPPType` wraps exactly one type like `int` or `std::string`.

**翻译**：`CPPType` 类允许以泛型方式处理任意 C++ 类型。一个 `CPPType` 实例精确地包装一个类型，比如 `int` 或 `std::string`。

> With `#CPPType` one can write generic data structures and algorithms. That is similar to what C++ templates allow. The difference is that when using templates, the types have to be known at compile time and the code has to be instantiated multiple times. On the other hand, when using `#CPPType`, the data type only has to be known at run-time, and the code only has to be compiled once.

**翻译**：借助 `CPPType`，可以编写通用的数据结构与算法。这与 C++ 模板的能力类似。区别在于：使用模板时，类型必须在**编译期**确定，代码会被多次实例化；而使用 `CPPType` 时，数据类型只需在**运行期**确定，代码只需编译一次。

#### 2. 何时使用 CPPType vs 模板

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| 运行期才能确定类型 | **CPPType** | 模板无法在运行期动态选择类型 |
| 类型已知且是少数几种，且是性能热点小循环 | **模板** | 为每种类型生成最优代码，但代价是编译时间更长、二进制更大、代码更复杂 |
| 类型已知但代码对性能不敏感 | **CPPType** | 代码更简洁，编译更快 |
| 混合方案 | **两者结合** | 对常见类型用模板生成优化版本，其余类型用 `CPPType` 兜底回退；`CPPType::to_static_type` 负责分发 |

#### 3. 与 `std::type_info` 的对比

> Under some circumstances, `#CPPType` serves a similar role as `#std::type_info`. However, `#CPPType` has much more utility because it contains methods for actually working with instances of the type.

**翻译**：在某些场景下，`CPPType` 扮演的角色类似于 `std::type_info`。但 `CPPType` 的实用性远超后者，因为它包含了**真正操作该类型实例**的方法（构造、析构、复制、移动、打印、哈希等）。

#### 4. 内存对齐与调试名

> Every type has a size and an alignment. Every function dealing with C++ types in a generic way, has to make sure that alignment rules are followed. The methods provided by a `#CPPType` instance will check for correct alignment as well.

**翻译**：每种类型都有大小（size）和对齐（alignment）。任何以泛型方式处理 C++ 类型的函数都必须确保遵守对齐规则。`CPPType` 提供的方法也会检查对齐是否正确。

> Every type has a name that is for debugging purposes only. It should not be used as identifier.

**翻译**：每种类型都有一个名称，但**仅用于调试**，不能作为标识符使用。

> To check if two instances of `#CPPType` represent the same type, only their pointers have to be compared. Any C++ type has at most one corresponding `#CPPType` instance.

**翻译**：判断两个 `CPPType` 实例是否代表同一类型，只需比较它们的**指针**即可。任何 C++ 类型最多只有一个对应的 `CPPType` 实例（单例模式）。

#### 5. 三种方法变体

> Most methods come in three variants. Using the default-construct methods as an example:
> - `default_construct(void *ptr)`: 在给定指针位置构造单个实例
> - `default_construct_n(void *ptr, int64_t n)`: 在给定指针开始的数组中构造 n 个实例
> - `default_construct_indices(void *ptr, const IndexMask &mask)`: 只构造被 `mask` 索引指定的那些位置

这是 Blender 几何节点中非常典型的模式：
- **单元素版**：处理单个值
- **批量版（_n）**：连续处理 n 个元素
- **索引掩码版（_indices）**：通过 `IndexMask` 只处理部分元素，避免遍历整个数组

#### 6. 默认值（default_value）

> In some cases default-construction does nothing (e.g. for trivial types like int). The `default_value` method provides some default value anyway that can be copied instead. What the default value is, depends on the type. Usually it is something like 0 or an empty string.

**翻译**：某些情况下默认构造什么都不做（比如 `int` 这类平凡类型）。`default_value` 方法仍然提供一个默认值供复制使用。具体是什么值取决于类型，通常是 `0` 或空字符串。

#### 7. 实现考量（Implementation Considerations）

> Concepts like inheritance are currently not captured by this system. This is not because it is not possible, but because it was not necessary to add this complexity yet.

**翻译**：继承等概念目前未被该系统捕获。这不是因为做不到，而是因为暂时没必要引入这种复杂性。

> One could also implement CPPType itself using virtual methods and a child class for every wrapped type. However, the approach used now with explicit function pointers works better.

**翻译**：也可以用虚方法和每个被包装类型的子类来实现 `CPPType`，但当前使用**显式函数指针**的方式效果更好。

**原因有三**：
1. **避免类爆炸**：如果每个 C++ 类型都继承出一个子类，会产生大量只会实例化一次的类。
2. **性能**：`default_construct` 等操作单个实例的方法必须快。即使函数指针已经引入了一层间接开销，如果再用虚函数，vtable 会引入第二层间接开销，性能更差。
3. **C 语言互操作**：如果需要，显式函数指针比虚成员函数指针更容易传给 C 函数。

---

## 二、头文件包含（第 75~85 行）

```cpp
#include <atomic>

#include "BLI_dynamic_stack_buffer.hh"  // IWYU pragma: keep
#include "BLI_enum_flags.hh"
#include "BLI_hash.hh"
#include "BLI_index_mask_fwd.hh"
#include "BLI_map.hh"
#include "BLI_parameter_pack_utils.hh"
#include "BLI_string_ref.hh"
#include "BLI_utility_mixins.hh"
```

| 头文件 | 用途 |
|--------|------|
| `<atomic>` | 原子操作，可能用于类型注册时的线程安全 |
| `BLI_dynamic_stack_buffer.hh` | 动态栈缓冲区，用于 `BUFFER_FOR_CPP_TYPE_VALUE` 宏 |
| `BLI_enum_flags.hh` | 枚举标志位操作宏，如 `ENUM_OPERATORS` |
| `BLI_hash.hh` | 哈希函数工具 |
| `BLI_index_mask_fwd.hh` | `IndexMask` 的前向声明，用于索引掩码操作 |
| `BLI_map.hh` | 映射容器 |
| `BLI_parameter_pack_utils.hh` | 参数包工具，用于模板元编程 |
| `BLI_string_ref.hh` | 字符串引用类型（非 owning 的轻量字符串视图） |
| `BLI_utility_mixins.hh` | 实用混入类，如 `NonCopyable`、`NonMovable` |

---

## 三、命名空间与前置声明（第 86~88 行）

```cpp
namespace blender {

struct UniqueHashBytes;
```

- **`blender` 命名空间**：Blender 核心代码的标准命名空间。
- **`UniqueHashBytes`**：前置声明，用于唯一哈希字节的结构体，后面在 `hash_unique` 方法中使用。

---

## 四、CPPTypeFlags 枚举（第 90~103 行）

```cpp
/**
 * Different types support different features. Features like copy constructability can be detected
 * automatically easily. For some features this is harder as of C++17. Those have flags in this
 * enum and need to be determined by the programmer.
 */
enum class CPPTypeFlags {
  None = 0,
  Hashable = 1 << 0,           // 可哈希
  Printable = 1 << 1,          // 可打印
  EqualityComparable = 1 << 2, // 可相等比较
  IdentityDefaultValue = 1 << 3,

  BasicType = Hashable | Printable | EqualityComparable,
};
ENUM_OPERATORS(CPPTypeFlags)
```

### 逐行解读

> Different types support different features. Features like copy constructability can be detected automatically easily. For some features this is harder as of C++17. Those have flags in this enum and need to be determined by the programmer.

**翻译**：不同类型支持不同的特性。像可复制构造这样的特性可以很容易自动检测。但截至 C++17，某些特性较难自动检测，因此在这个枚举中用标志位表示，需要由程序员显式指定。

| 标志位 | 值 | 含义 |
|--------|-----|------|
| `None` | `0` | 无任何特殊特性 |
| `Hashable` | `1 << 0` (1) | 该类型可以被哈希（用于哈希表键） |
| `Printable` | `1 << 1` (2) | 该类型可以被打印为字符串 |
| `EqualityComparable` | `1 << 2` (4) | 该类型支持 `==` 比较 |
| `IdentityDefaultValue` | `1 << 3` (8) | 默认值的特殊语义 |
| `BasicType` | `1 \| 2 \| 4` (7) | 组合标志：同时具备 Hashable、Printable、EqualityComparable |

- **`ENUM_OPERATORS(CPPTypeFlags)`**：宏展开后重载了 `|`、`&`、`^`、`~` 等位运算符，使枚举可以像标志位一样组合使用。

---

## 五、CPPType 类声明：公有数据成员（第 106~165 行）

```cpp
class CPPType : NonCopyable, NonMovable {
 public:
  /**
   * Required memory in bytes for an instance of this type.
   *
   * C++ equivalent:
   *   `sizeof(T);`
   */
  int64_t size = 0;

  /**
   * Required memory alignment for an instance of this type.
   *
   * C++ equivalent:
   *   `alignof(T);`
   */
  int64_t alignment = 0;

  /**
   * When true, the value is like a normal C type, it can be copied around with #memcpy and does
   * not have to be destructed.
   *
   * C++ equivalent:
   *   `std::is_trivial_v<T>;`
   */
  bool is_trivial = false;

  /**
   * When true, the destructor does not have to be called on this type. This can sometimes be used
   * for optimization purposes.
   *
   * C++ equivalent:
   *   `std::is_trivially_destructible_v<T>;`
   */
  bool is_trivially_destructible = false;

  /**
   * Returns true, when the type has the following functions:
   * - Default constructor.
   * - Copy constructor.
   * - Move constructor.
   * - Copy assignment operator.
   * - Move assignment operator.
   * - Destructor.
   */
  bool has_special_member_functions = false;

  bool is_default_constructible = false;
  bool is_copy_constructible = false;
  bool is_move_constructible = false;
  bool is_destructible = false;
  bool is_copy_assignable = false;
  bool is_move_assignable = false;

  /**
   * An index that is assigned when the type is registered. Each #CPPtype has a unique index.
   * While the pointer of a #CPPType is also unique, sometimes it's easier to work with an index
   * that is a relatively small number (generally <100).
   */
  int type_index = -1;
```

### 逐成员解读

| 成员 | 类型 | C++ 等价 | 说明 |
|------|------|----------|------|
| `size` | `int64_t` | `sizeof(T)` | 类型实例占用的字节数 |
| `alignment` | `int64_t` | `alignof(T)` | 类型实例需要的内存对齐边界 |
| `is_trivial` | `bool` | `std::is_trivial_v<T>` | 是否是平凡类型（可用 `memcpy` 复制，无需析构） |
| `is_trivially_destructible` | `bool` | `std::is_trivially_destructible_v<T>` | 是否无需调用析构函数 |
| `has_special_member_functions` | `bool` | — | 是否具备全套特殊成员函数（默认构造、拷贝/移动构造、拷贝/移动赋值、析构） |
| `is_default_constructible` | `bool` | `std::is_default_constructible_v<T>` | 是否可默认构造 |
| `is_copy_constructible` | `bool` | `std::is_copy_constructible_v<T>` | 是否可拷贝构造 |
| `is_move_constructible` | `bool` | `std::is_move_constructible_v<T>` | 是否可移动构造 |
| `is_destructible` | `bool` | `std::is_destructible_v<T>` | 是否可析构 |
| `is_copy_assignable` | `bool` | `std::is_copy_assignable_v<T>` | 是否可拷贝赋值 |
| `is_move_assignable` | `bool` | `std::is_move_assignable_v<T>` | 是否可移动赋值 |
| `type_index` | `int` | — | 类型注册时分配的唯一索引，通常是一个小于 100 的小整数，便于数组索引 |

**继承关系**：`CPPType` 继承自 `NonCopyable` 和 `NonMovable`，意味着 `CPPType` 实例本身不能被复制或移动，确保每个类型全局只有一个 `CPPType` 实例。

---

## 六、私有函数指针成员（第 167~220 行）

```cpp
 private:
  uintptr_t alignment_mask_ = 0;

  void (*default_construct_)(void *ptr) = nullptr;
  void (*default_construct_n_)(void *ptr, int64_t n) = nullptr;
  void (*default_construct_indices_)(void *ptr, const IndexMask &mask) = nullptr;

  void (*value_initialize_)(void *ptr) = nullptr;
  void (*value_initialize_n_)(void *ptr, int64_t n) = nullptr;
  void (*value_initialize_indices_)(void *ptr, const IndexMask &mask) = nullptr;

  void (*destruct_)(void *ptr) = nullptr;
  void (*destruct_n_)(void *ptr, int64_t n) = nullptr;
  void (*destruct_indices_)(void *ptr, const IndexMask &mask) = nullptr;

  void (*copy_assign_)(const void *src, void *dst) = nullptr;
  void (*copy_assign_n_)(const void *src, void *dst, int64_t n) = nullptr;
  void (*copy_assign_indices_)(const void *src, void *dst, const IndexMask &mask) = nullptr;
  void (*copy_assign_compressed_)(const void *src, void *dst, const IndexMask &mask) = nullptr;

  void (*copy_construct_)(const void *src, void *dst) = nullptr;
  void (*copy_construct_n_)(const void *src, void *dst, int64_t n) = nullptr;
  void (*copy_construct_indices_)(const void *src, void *dst, const IndexMask &mask) = nullptr;
  void (*copy_construct_compressed_)(const void *src, void *dst, const IndexMask &mask) = nullptr;

  void (*move_assign_)(void *src, void *dst) = nullptr;
  void (*move_assign_n_)(void *src, void *dst, int64_t n) = nullptr;
  void (*move_assign_indices_)(void *src, void *dst, const IndexMask &mask) = nullptr;

  void (*move_construct_)(void *src, void *dst) = nullptr;
  void (*move_construct_n_)(void *src, void *dst, int64_t n) = nullptr;
  void (*move_construct_indices_)(void *src, void *dst, const IndexMask &mask) = nullptr;

  void (*relocate_assign_)(void *src, void *dst) = nullptr;
  void (*relocate_assign_n_)(void *src, void *dst, int64_t n) = nullptr;
  void (*relocate_assign_indices_)(void *src, void *dst, const IndexMask &mask) = nullptr;

  void (*relocate_construct_)(void *src, void *dst) = nullptr;
  void (*relocate_construct_n_)(void *src, void *dst, int64_t n) = nullptr;
  void (*relocate_construct_indices_)(void *src, void *dst, const IndexMask &mask) = nullptr;

  void (*fill_assign_n_)(const void *value, void *dst, int64_t n) = nullptr;
  void (*fill_assign_indices_)(const void *value, void *dst, const IndexMask &mask) = nullptr;

  void (*fill_construct_n_)(const void *value, void *dst, int64_t n) = nullptr;
  void (*fill_construct_indices_)(const void *value, void *dst, const IndexMask &mask) = nullptr;

  void (*print_)(const void *value, std::stringstream &ss) = nullptr;
  bool (*is_equal_)(const void *a, const void *b) = nullptr;
  uint64_t (*hash_)(const void *value) = nullptr;
  void (*hash_unique_)(const void *value, UniqueHashBytes &hash) = nullptr;

  const void *default_value_ = nullptr;
  std::string debug_name_;
```

### 解读

这是 `CPPType` 的核心实现机制——**显式函数指针表**。

#### 1. `alignment_mask_`

用于快速检查指针是否满足对齐要求。计算方式通常是 `alignment - 1`，然后检查 `(ptr & mask) == 0`。

#### 2. 函数指针分类

| 类别 | 单元素 | 批量 `_n` | 索引掩码 `_indices` | 压缩 `_compressed` |
|------|--------|-----------|---------------------|-------------------|
| **默认构造** | `default_construct_` | `default_construct_n_` | `default_construct_indices_` | — |
| **值初始化** | `value_initialize_` | `value_initialize_n_` | `value_initialize_indices_` | — |
| **析构** | `destruct_` | `destruct_n_` | `destruct_indices_` | — |
| **拷贝赋值** | `copy_assign_` | `copy_assign_n_` | `copy_assign_indices_` | `copy_assign_compressed_` |
| **拷贝构造** | `copy_construct_` | `copy_construct_n_` | `copy_construct_indices_` | `copy_construct_compressed_` |
| **移动赋值** | `move_assign_` | `move_assign_n_` | `move_assign_indices_` | — |
| **移动构造** | `move_construct_` | `move_construct_n_` | `move_construct_indices_` | — |
| **重定位赋值** | `relocate_assign_` | `relocate_assign_n_` | `relocate_assign_indices_` | — |
| **重定位构造** | `relocate_construct_` | `relocate_construct_n_` | `relocate_construct_indices_` | — |
| **填充赋值** | — | `fill_assign_n_` | `fill_assign_indices_` | — |
| **填充构造** | — | `fill_construct_n_` | `fill_construct_indices_` | — |

#### 3. 其他函数指针

| 函数指针 | 签名 | 说明 |
|----------|------|------|
| `print_` | `(const void*, std::stringstream&)` | 将值打印到字符串流 |
| `is_equal_` | `(const void*, const void*) -> bool` | 比较两个值是否相等 |
| `hash_` | `(const void*) -> uint64_t` | 计算值的哈希码 |
| `hash_unique_` | `(const void*, UniqueHashBytes&)` | 计算唯一哈希（用于更严格的哈希场景） |

#### 4. 数据成员

| 成员 | 类型 | 说明 |
|------|------|------|
| `default_value_` | `const void*` | 指向一个常量默认值的指针，供复制使用 |
| `debug_name_` | `std::string` | 调试用的类型名称 |

---

## 七、公有构造函数与静态方法（第 222~242 行）

```cpp
 public:
  template<typename T, CPPTypeFlags Flags>
  CPPType(TypeTag<T> /*type*/, TypeForValue<CPPTypeFlags, Flags> /*flags*/, StringRef debug_name);
  virtual ~CPPType() = default;

  /**
   * Get the `CPPType` that corresponds to a specific static type.
   * This only works for types that actually implement the template specialization using
   * `BLI_CPP_TYPE_REGISTER`.
   */
  template<typename T> static const CPPType &get();

  /**
   * Returns the name of the type for debugging purposes. This name should not be used as
   * identifier.
   */
  StringRefNull name() const;

  bool is_printable() const;
  bool is_equality_comparable() const;
  bool is_hashable() const;
```

### 解读

#### 1. 构造函数

```cpp
template<typename T, CPPTypeFlags Flags>
CPPType(TypeTag<T> /*type*/, TypeForValue<CPPTypeFlags, Flags> /*flags*/, StringRef debug_name);
```

- **模板参数 `T`**：被包装的具体 C++ 类型。
- **模板参数 `Flags`**：`CPPTypeFlags` 标志位组合。
- **`TypeTag<T>`**：标签类型，用于在模板推导中传递类型信息而不需要实际参数（空结构体）。
- **`TypeForValue<CPPTypeFlags, Flags>`**：将枚举值转换为类型的辅助模板，同样用于标签派发。
- **`StringRef debug_name`**：调试名称。

构造函数是模板化的，意味着每个具体类型 `T` 都会实例化一个特定的构造函数，该构造函数内部会根据 `T` 的特性设置所有函数指针和标志位。

#### 2. `CPPType::get<T>()`

```cpp
template<typename T> static const CPPType &get();
```

- 获取与静态类型 `T` 对应的 `CPPType` 实例。
- 只有用 `BLI_CPP_TYPE_REGISTER` 宏注册过的类型才有特化版本。
- 返回的是全局单例的引用。

#### 3. 能力查询

| 方法 | 说明 |
|------|------|
| `name()` | 返回调试名称（`StringRefNull` 是可能为空的字符串引用） |
| `is_printable()` | 是否可打印（`print_ != nullptr`） |
| `is_equality_comparable()` | 是否可相等比较（`is_equal_ != nullptr`） |
| `is_hashable()` | 是否可哈希（`hash_ != nullptr`） |

---

## 八、指针对齐检查（第 244~248 行）

```cpp
  /**
   * Returns true, when the given pointer fulfills the alignment requirement of this type.
   */
  bool pointer_has_valid_alignment(const void *ptr) const;
  bool pointer_can_point_to_instance(const void *ptr) const;
```

### 实现（第 500~508 行）

```cpp
inline bool CPPType::pointer_has_valid_alignment(const void *ptr) const
{
  return (uintptr_t(ptr) & alignment_mask_) == 0;
}

inline bool CPPType::pointer_can_point_to_instance(const void *ptr) const
{
  return ptr != nullptr && pointer_has_valid_alignment(ptr);
}
```

- **`pointer_has_valid_alignment`**：检查指针是否满足该类型的对齐要求。通过与 `alignment_mask_`（即 `alignment - 1`）进行位与运算来判断。
- **`pointer_can_point_to_instance`**：指针不仅需要对齐，还不能是 `nullptr`。

---

## 九、默认构造（第 250~260 行）

```cpp
  /**
   * Call the default constructor at the given memory location.
   * The memory should be uninitialized before this method is called.
   * For some trivial types (like int), this method does nothing.
   *
   * C++ equivalent:
   *   `new (ptr) T;`
   */
  void default_construct(void *ptr) const;
  void default_construct_n(void *ptr, int64_t n) const;
  void default_construct_indices(void *ptr, const IndexMask &mask) const;
```

### 实现（第 510~523 行）

```cpp
inline void CPPType::default_construct(void *ptr) const
{
  default_construct_(ptr);
}

inline void CPPType::default_construct_n(void *ptr, int64_t n) const
{
  default_construct_n_(ptr, n);
}

inline void CPPType::default_construct_indices(void *ptr, const IndexMask &mask) const
{
  default_construct_indices_(ptr, mask);
}
```

- **`default_construct`**：在已分配但未初始化的内存上调用默认构造。等价于 placement new：`new (ptr) T;`
- **`default_construct_n`**：连续构造数组中的 n 个元素。
- **`default_construct_indices`**：只构造被 `IndexMask` 指定的索引位置。

---

## 十、值初始化（第 262~270 行）

```cpp
  /**
   * Same as #default_construct, but does zero initialization for trivial types.
   *
   * C++ equivalent:
   *   `new (ptr) T();`
   */
  void value_initialize(void *ptr) const;
  void value_initialize_n(void *ptr, int64_t n) const;
  void value_initialize_indices(void *ptr, const IndexMask &mask) const;
```

### 解读

- **`value_initialize`** 与 `default_construct` 的区别在于：对于平凡类型（如 `int`），`default_construct` 可能什么都不做（值不确定），而 `value_initialize` 会零初始化。
- C++ 等价语法：`new (ptr) T();`（注意括号）vs `new (ptr) T;`（无括号）。

---

## 十一、析构（第 272~282 行）

```cpp
  /**
   * Call the destructor on the given instance of this type. The pointer must not be nullptr.
   *
   * For some trivial types, this does nothing.
   *
   * C++ equivalent:
   *   `ptr->~T();`
   */
  void destruct(void *ptr) const;
  void destruct_n(void *ptr, int64_t n) const;
  void destruct_indices(void *ptr, const IndexMask &mask) const;
```

### 解读

- **`destruct`**：显式调用析构函数。等价于 `ptr->~T();`
- 对于平凡类型（如 `int`），析构函数什么都不做，可以直接跳过。
- 三种变体分别处理：单个元素、连续数组、索引掩码指定的部分元素。

---

## 十二、拷贝赋值（第 284~297 行）

```cpp
  /**
   * Copy an instance of this type from src to dst.
   *
   * C++ equivalent:
   *   `dst = src;`
   */
  void copy_assign(const void *src, void *dst) const;
  void copy_assign_n(const void *src, void *dst, int64_t n) const;
  void copy_assign_indices(const void *src, void *dst, const IndexMask &mask) const;

  /**
   * Similar to #copy_assign_indices, but does not leave gaps in the #dst array.
   */
  void copy_assign_compressed(const void *src, void *dst, const IndexMask &mask) const;
```

### 解读

- **`copy_assign`**：`dst` 指向已初始化的内存，执行拷贝赋值操作。
- **`copy_assign_compressed`**：与 `copy_assign_indices` 类似，但会把元素紧凑地排列到 `dst` 中，不留空隙。这在过滤/压缩数组时非常有用。

---

## 十三、拷贝构造（第 299~314 行）

```cpp
  /**
   * Copy an instance of this type from src to dst.
   *
   * The memory pointed to by dst should be uninitialized.
   *
   * C++ equivalent:
   *   `new (dst) T(src);`
   */
  void copy_construct(const void *src, void *dst) const;
  void copy_construct_n(const void *src, void *dst, int64_t n) const;
  void copy_construct_indices(const void *src, void *dst, const IndexMask &mask) const;

  /**
   * Similar to #copy_construct_indices, but does not leave gaps in the #dst array.
   */
  void copy_construct_compressed(const void *src, void *dst, const IndexMask &mask) const;
```

### 解读

- **`copy_construct`**：`dst` 指向**未初始化**的内存，执行拷贝构造（placement new + 拷贝构造）。
- 与 `copy_assign` 的关键区别：`copy_construct` 在裸内存上构造新对象；`copy_assign` 要求目标对象已存在。

---

## 十四、移动赋值与移动构造（第 316~338 行）

```cpp
  /**
   * Move an instance of this type from src to dst.
   *
   * The memory pointed to by dst should be initialized.
   *
   * C++ equivalent:
   *   `dst = std::move(src);`
   */
  void move_assign(void *src, void *dst) const;
  void move_assign_n(void *src, void *dst, int64_t n) const;
  void move_assign_indices(void *src, void *dst, const IndexMask &mask) const;

  /**
   * Move an instance of this type from src to dst.
   *
   * The memory pointed to by dst should be uninitialized.
   *
   * C++ equivalent:
   *   `new (dst) T(std::move(src));`
   */
  void move_construct(void *src, void *dst) const;
  void move_construct_n(void *src, void *dst, int64_t n) const;
  void move_construct_indices(void *src, void *dst, const IndexMask &mask) const;
```

### 解读

- **`move_assign`**：`dst` 已初始化，执行移动赋值。等价于 `dst = std::move(src);`
- **`move_construct`**：`dst` 未初始化，执行移动构造。等价于 `new (dst) T(std::move(src));`
- 移动语义允许资源转移（如字符串、向量的内部指针转移），避免不必要的深拷贝。

---

## 十五、重定位（Relocate）（第 340~362 行）

```cpp
  /**
   * Relocates an instance of this type from src to dst. src will point to uninitialized memory
   * afterwards.
   *
   * C++ equivalent:
   *   `dst = std::move(src);`
   *   `src->~T();`
   */
  void relocate_assign(void *src, void *dst) const;
  void relocate_assign_n(void *src, void *dst, int64_t n) const;
  void relocate_assign_indices(void *src, void *dst, const IndexMask &mask) const;

  /**
   * Relocates an instance of this type from src to dst. src will point to uninitialized memory
   * afterwards.
   *
   * C++ equivalent:
   *   `new (dst) T(std::move(src))`
   *   `src->~T();`
   */
  void relocate_construct(void *src, void *dst) const;
  void relocate_construct_n(void *src, void *dst, int64_t n) const;
  void relocate_construct_indices(void *src, void *dst, const IndexMask &mask) const;
```

### 解读

**重定位（Relocate）** 是 C++ 中一个高级概念，可以理解为"移动 + 析构源对象"的组合操作：

- **`relocate_assign`**：先把 `src` 移动到 `dst`（`dst` 已初始化），然后析构 `src`。之后 `src` 指向的内存变为未初始化状态。
- **`relocate_construct`**：先把 `src` 移动构造到 `dst`（`dst` 未初始化），然后析构 `src`。

**使用场景**：在重新分配数组容量时，需要把旧数组的元素"转移"到新数组，然后销毁旧数组的元素。重定位操作一次性完成这两步。

---

## 十六、填充（Fill）（第 364~378 行）

```cpp
  /**
   * Copy the given value to the first n elements in an array starting at dst.
   *
   * Other instances of the same type should live in the array before this method is called.
   */
  void fill_assign_n(const void *value, void *dst, int64_t n) const;
  void fill_assign_indices(const void *value, void *dst, const IndexMask &mask) const;

  /**
   * Copy the given value to the first n elements in an array starting at dst.
   *
   * The array should be uninitialized before this method is called.
   */
  void fill_construct_n(const void *value, void *dst, int64_t n) const;
  void fill_construct_indices(const void *value, void *dst, const IndexMask &mask) const;
```

### 解读

- **`fill_assign_n`**：把同一个值复制到数组的前 n 个位置。要求数组元素**已初始化**（使用赋值）。
- **`fill_construct_n`**：把同一个值复制到数组的前 n 个位置。要求数组**未初始化**（使用构造）。
- 类似于 `std::fill` 和 `std::uninitialized_fill` 的区别。

---

## 十七、缓冲区兼容性与打印/比较/哈希（第 380~398 行）

```cpp
  bool can_exist_in_buffer(const int64_t buffer_size, const int64_t buffer_alignment) const;

  void print(const void *value, std::stringstream &ss) const;
  std::string to_string(const void *value) const;
  void print_or_default(const void *value, std::stringstream &ss, StringRef default_value) const;

  bool is_equal(const void *a, const void *b) const;
  bool is_equal_or_false(const void *a, const void *b) const;

  uint64_t hash(const void *value) const;
  uint64_t hash_or_fallback(const void *value, uint64_t fallback_hash) const;
  void hash_unique(const void *value, UniqueHashBytes &hash) const;

  /**
   * Get a pointer to a constant value of this type. The specific value depends on the type.
   * It is usually a zero-initialized or default constructed value.
   */
  const void *default_value() const;

  uint64_t hash() const;
```

### 解读

| 方法 | 说明 |
|------|------|
| `can_exist_in_buffer` | 检查该类型是否能放入给定大小和对齐的缓冲区中 |
| `print` | 将值打印到 `std::stringstream` |
| `to_string` | 将值转换为 `std::string` |
| `print_or_default` | 如果类型不可打印，则输出默认值 |
| `is_equal` | 比较两个值是否相等 |
| `is_equal_or_false` | 如果类型不可比较，返回 `false` 而不是报错 |
| `hash` | 计算值的哈希码 |
| `hash_or_fallback` | 如果类型不可哈希，返回备用哈希值 |
| `hash_unique` | 计算唯一哈希（更严格的哈希） |
| `default_value` | 返回指向默认值的指针 |
| `hash`（无参） | 对 `CPPType` 对象本身计算哈希（基于指针） |

---

## 十八、析构函数指针与类型判断（第 400~405 行）

```cpp
  void (*destruct_fn() const)(void *);

  template<typename T> bool is() const;

  template<typename... T> bool is_any() const;
```

### 实现（第 736~749 行）

```cpp
inline void (*CPPType::destruct_fn() const)(void *)
{
  return destruct_;
}

template<typename T> inline bool CPPType::is() const
{
  return this == &CPPType::get<std::decay_t<T>>();
}

template<typename... T> inline bool CPPType::is_any() const
{
  return (this->is<T>() || ...);
}
```

### 解读

- **`destruct_fn`**：返回析构函数指针，供外部需要直接获取函数指针的场景使用。
- **`is<T>()`**：判断当前 `CPPType` 是否代表类型 `T`。通过比较指针实现（`std::decay_t` 去除引用和 cv 限定符）。
- **`is_any<T1, T2, ...>()`**：判断当前类型是否是给定类型列表中的任意一种。使用 C++17 折叠表达式 `(this->is<T>() || ...)`。

---

## 十九、运行时到编译期的类型分发：`to_static_type`（第 407~433 行）

```cpp
  /**
   * Convert a #CPPType that is only known at run-time, to a static type that is known at
   * compile-time. This allows the compiler to optimize a function for specific types, while all
   * other types can still use a generic fallback function.
   *
   * \tparam Types: The types that code should be generated for.
   * \param fn: The function对象 to call. This is expected to have a templated `operator()` and
   * a non-templated `operator()`. The templated version will be called if the current #CPPType
   *   matches any of the given types.
   * \return True if the function was called.
   */
  template<typename... Types, typename Fn> bool to_static_type_try(Fn &&fn) const;

  /** Same as #to_static_type_try, but asserts if the type is valid. */
  template<typename... Types, typename Fn> void to_static_type(Fn &&fn) const;

 private:
  /**
   * Helper used in #to_static_type_try as a typed function pointer for each type in the list.
   * A named static function is used instead of a lambda to avoid a known MSVC bug where a
   * non-capturing lambda inside a comma fold expression that references the pack parameter
   * causes MSVC to generate zero iterations, leaving the map empty.
   */
  template<typename T, typename Fn> static void call_with_type_impl_(const Fn &fn)
  {
    fn.template operator()<T>();
  }
```

### 解读

这是 `CPPType` 最强大的特性之一——**运行时到编译期的桥接**。

#### 设计动机

- `CPPType` 提供运行期泛型，但有函数指针间接开销。
- 模板提供编译期优化，但类型必须在编译期确定。
- `to_static_type` 结合两者：对常见类型走模板优化路径，对不常见类型走 `CPPType` 泛型回退路径。

#### 使用方法

```cpp
// 假设 current_type 是一个 const CPPType&
current_type.to_static_type_try<int, float, double>([&](auto type_tag) {
    // 如果 current_type 是 int、float 或 double 之一，
    // 这里会被实例化为具体类型的 lambda
    using T = decltype(type_tag);
    // 编译期已知的优化代码...
});
```

#### 实现细节（第 759~789 行）

```cpp
template<typename... Types, typename Fn> inline bool CPPType::to_static_type_try(Fn &&fn) const
{
  /* Strip any reference from Fn to normalize the type used for the static map, ensuring the
   * same static is used regardless of whether fn is an lvalue or rvalue. */
  using Fn_ = std::remove_reference_t<Fn>;
  using Callback = void (*)(const Fn_ &);

  /* Use an array indexed by #CPPType::type_index instead of a #Map for faster lookup and less
   * generated code. The array can be quite a bit larger at run-time than the number of types but
   * the total number of types is fairly limited, so that should be fine. */
  static Array<Callback, 0> callback_array = [&]() {
    /* This way to compute the max generates less code than using std::max with an initializer
     * list. */
    int max_type_index = 0;
    ((max_type_index = std::max(max_type_index, CPPType::get<Types>().type_index)), ...);
    Array<Callback, 0> callback_array(max_type_index + 1, nullptr);
    /* Using call_with_type_impl_ instead of a lambda due to an MSVC bug.  */
    ((callback_array[CPPType::get<Types>().type_index] = call_with_type_impl_<Types, Fn_>), ...);
    return callback_array;
  }();

  if (this->type_index >= callback_array.size()) {
    return false;
  }
  const Callback callback = callback_array[this->type_index];
  if (!callback) {
    return false;
  }
  callback(fn);
  return true;
}
```

**关键实现点**：
1. **数组索引而非 Map**：用 `type_index` 作为数组下标，O(1) 查找，比 `Map` 更快且生成代码更少。
2. **MSVC Bug 规避**：不用 lambda 而用命名静态函数 `call_with_type_impl_`，因为 MSVC 在逗号折叠表达式中对非捕获 lambda 有 bug。
3. **惰性初始化**：`callback_array` 是 `static` 局部变量，首次调用时初始化。
4. **回退机制**：如果类型不匹配，返回 `false`，调用方可以用 `CPPType` 的泛型方法作为回退。

---

## 二十、全局类型注册（第 436~446 行）

```cpp
namespace detail {
/**
 * Global static variable that contains the #CPPType for a given type after it has been registered
 * with #BLI_CPP_TYPE_REGISTER. This should generally be accessed through #CPPType::get<T>. */
template<typename T> inline TypedBuffer<CPPType> cpp_type_impl{};
}  // namespace detail

/**
 * Initialize and register basic cpp types.
 */
void register_cpp_types();
```

### 解读

- **`cpp_type_impl<T>`**：全局静态变量，存储每个已注册类型 `T` 对应的 `CPPType` 实例。`TypedBuffer` 可能提供线程安全的初始化或对齐存储。
- **`register_cpp_types()`**：在程序启动时调用，注册所有基础类型（`int`、`float`、`bool`、`std::string` 等）的 `CPPType` 信息。

---

## 二十一、辅助宏与运算符重载（第 448~468 行）

```cpp
/* Utility for allocating an uninitialized buffer for a single value of the given #CPPType. */
#define BUFFER_FOR_CPP_TYPE_VALUE(type, variable_name) \
  DynamicStackBuffer<64, 64> stack_buffer_for_##variable_name((type).size, (type).alignment); \
  void *variable_name = stack_buffer_for_##variable_name.buffer();

/* Give a compile error instead of a link error when type information is missing. */
template<> const CPPType &CPPType::get<void>() = delete;

/**
 * Two types only compare equal when their pointer is equal. No two instances of CPPType for the
 * same C++ type should be created.
 */
inline bool operator==(const CPPType &a, const CPPType &b)
{
  return &a == &b;
}

inline bool operator!=(const CPPType &a, const CPPType &b)
{
  return !(&a == &b);
}
```

### 解读

| 代码 | 说明 |
|------|------|
| `BUFFER_FOR_CPP_TYPE_VALUE` | 宏，在栈上分配一个满足 `CPPType` 大小和对齐要求的未初始化缓冲区。`DynamicStackBuffer<64,64>` 表示最大 64 字节、64 字节对齐。 |
| `CPPType::get<void>() = delete` | 显式删除 `void` 类型的特化，如果代码错误地请求 `void` 的类型信息，会得到编译错误而非链接错误。 |
| `operator==` | 比较两个 `CPPType` 是否相同。由于每个类型全局只有一个实例，直接比较指针即可。 |
| `operator!=` | 基于 `operator==` 实现。 |

---

## 二十二、`CPPType::get<T>()` 实现（第 470~478 行）

```cpp
template<typename T> inline const CPPType &CPPType::get()
{
  const CPPType &type = detail::cpp_type_impl<std::decay_t<T>>.ref();
  /* Should have been initialized by #BLI_CPP_TYPE_REGISTER.
   * If this is hit in test code, make sure the test calls `register_cpp_types` (for blenlib
   * tests) or `BKE_cpp_types_init` (for general tests). */
  BLI_assert(type.size > 0);
  return type;
}
```

### 解读

- **`std::decay_t<T>`**：去除 `T` 的引用和 cv 限定符（`const`、`volatile`），确保 `const int&` 和 `int` 得到同一个 `CPPType`。
- **`BLI_assert(type.size > 0)`**：断言检查类型是否已注册。如果触发，说明忘记调用 `register_cpp_types()` 或 `BKE_cpp_types_init()`。
- 返回全局单例的引用。

---

## 二十三、内联访问器实现（第 480~739 行）

这部分是大量简单的内联函数，直接调用对应的私有函数指针。前面已经按功能分组解读过声明，此处不再重复。所有实现都遵循同一模式：

```cpp
inline ReturnType CPPType::method_name(Args...) const
{
  method_name_(Args...);
}
```

**这种设计的优势**：
1. **内联展开**：编译器可以将这些调用内联，消除函数调用开销。
2. **统一接口**：公有方法提供类型安全的包装，私有函数指针存储实际实现。
3. **运行期多态**：通过不同的函数指针，同一个 `CPPType` 接口可以操作完全不同的类型。

---

## 二十四、`to_static_type` 实现（第 751~789 行）

前面已详细解读，此处总结：

```cpp
template<typename... Types, typename Fn> inline void CPPType::to_static_type(Fn &&fn) const
{
  if (this->to_static_type_try<Types...>(fn)) {
    return;
  }
  BLI_assert_unreachable();
}
```

- **`to_static_type`**：断言版本，如果类型不匹配则触发不可达断言（调试用）。
- **`to_static_type_try`**：安全版本，返回 `bool` 表示是否匹配成功。

---

## 二十五、总结

### CPPType 的设计哲学

| 方面 | 说明 |
|------|------|
| **运行期类型擦除** | 用函数指针表替代虚函数，避免 vtable 开销 |
| **单例模式** | 每个 C++ 类型全局只有一个 `CPPType` 实例，指针比较即可判断类型相等 |
| **三变体方法** | 单元素、批量 `_n`、索引掩码 `_indices`，适应几何节点的稀疏数据处理需求 |
| **压缩变体** | `_compressed` 方法用于紧凑排列过滤后的数据 |
| **桥接模板** | `to_static_type` 允许在运行期类型上获得编译期优化 |
| **类型安全** | 所有方法都通过 `void*` 操作，但由 `CPPType` 确保正确的构造/析构/对齐 |

### 在几何节点中的作用

`CPPType` 是 Blender 几何节点系统的**基石**：
- **属性存储**：几何体上的属性（顶点色、UV、自定义属性）需要在运行期确定类型，`CPPType` 提供了统一的类型操作接口。
- **节点图执行**：节点之间的数据流类型在编译期未知，`CPPType` 使节点可以处理任意类型的数据。
- **性能优化**：通过 `to_static_type`，对常见类型（`float`、`int`、`float3` 等）可以走优化的模板路径，其他类型走泛型路径。

### 与 C++ 标准库的对比

| 特性 | `CPPType` | `std::type_info` | `std::any` |
|------|-----------|------------------|------------|
| 运行期类型信息 | ✅ | ✅ | ✅ |
| 构造/析构对象 | ✅ | ❌ | ✅（通过 any_cast） |
| 批量操作数组 | ✅ | ❌ | ❌ |
| 索引掩码操作 | ✅ | ❌ | ❌ |
| 编译期优化桥接 | ✅ | ❌ | ❌ |
| 零开销抽象 | ❌（函数指针间接） | ✅ | ❌ |

`CPPType` 本质上是一个**更重量级的、面向数组处理的、支持编译期桥接的运行期类型系统**，专门为 Blender 几何节点的高性能数据处理需求而设计。
