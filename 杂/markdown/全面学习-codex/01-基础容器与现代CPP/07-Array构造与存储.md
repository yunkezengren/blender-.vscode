# 01-07 Array构造与存储

[方向导航](README.md) · [总目录](../README.md) · [覆盖索引](../%E6%BA%90%E7%A0%81%E7%89%88%E6%9C%AC%E4%B8%8E%E8%A6%86%E7%9B%96%E7%B4%A2%E5%BC%95.md)

> 阅读顺序：问题与数据模型 → 语法与类型 → 源码逐行 → 调用线索 → 历史与取舍 → 推演和练习。

- 基准 HEAD：`cbda6b96c26c0dee3c3b5cbb93960c4ac06a6b30`。
- 记录日期：2026-10-14。
- 教学示例状态：正文中的推演不是本机性能实测；已运行练习见验收报告。

## 一、从问题到设计

固定大小动态数组为什么还需要复杂构造逻辑？

元素数不作为类型参数，存储可能使用内嵌缓冲；初始化方式决定基本类型是否有可读取的值。

本篇把语法、数据语义和系统取舍连接起来。先证明对象存活，再讨论索引；先区分借用与拥有，再讨论复制移动。

### 本篇独立模型与设计推理

Array大小在实例运行时确定，Array<int>(n)与std::array<int,n>的类型机制不同。

设计取舍：固定大小动态存储简化增长语义，但内嵌缓冲和泛型构造仍需要类型性质判断。

最小反例：把所有默认构造的标量都当成零值读取。

推导与处理：根据具体构造器检查初始化路径，用明确值填充建立可读取基线。

```mermaid
flowchart TB
  M["Array大小在实例运行时确定，Array＜int＞(<br/>n)与std::array＜int,n＞的类型机制不同。"]:::data
  T["固定大小动态存储简化增长语义，但内嵌缓冲<br/>和泛型构造仍需要类型性质判断。"]:::abstraction
  X["把所有默认构造的标量都当成零值读取。"]:::error
  A["根据具体构造器检查初始化路径，用明确值填<br/>充建立可读取基线。"]:::result
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
| [source/blender/blenlib/BLI_array.hh](../../../../../source/blender/blenlib/BLI_array.hh) | L1—L245 | `a98265cac6cfcc1e86688b3cf11100dbb507c282c6b983c19572206997f63d5f` |

同一主讲文件可能分多篇覆盖；超出本篇范围的符号通过覆盖索引定位。空行与纯注释保留在源码摘录中，逐行表解释有效语句与语法边界；许可证头统一保留。

前篇：[MutableSpan可写视图](06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md).

后篇：[Array复制移动与销毁](08-Array%E5%A4%8D%E5%88%B6%E7%A7%BB%E5%8A%A8%E4%B8%8E%E9%94%80%E6%AF%81.md).

## 二、类型、数据与阅读地图

```mermaid
flowchart TB
  Q["固定大小动态数组为什么还需要复杂构造逻辑<br/>？"]:::input
  C0["拥有型容器"]:::abstraction
  C1["借用视图"]:::data
  C2["元素生命周期"]:::data
  C3["分配与失效"]:::data
  R["Array构造与存储"]:::result
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
  S["BLI_array.hh"]:::abstraction
  I0["BLI_allocator.hh"]:::data
  I1["BLI_index_range.hh"]:::data
  I2["BLI_memory_utils.hh"]:::data
  I3["BLI_span.hh"]:::data
  I4["BLI_utildefines.hh"]:::data
  S -->|"直接include"| I0
  S -->|"直接include"| I1
  S -->|"直接include"| I2
  S -->|"直接include"| I3
  S -->|"直接include"| I4
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

### 约束 requires

requires表达式或requires子句限制模板参与重载的条件。它提供编译期可用性检查，不是运行时if，不能指望输入到达程序后再被这一机制验证。

具体检查：构造满足和不满足约束的两个类型，观察候选被排除而不是在函数内返回错误。

### 只读限定 const

const约束当前访问路径可做的修改。const指针、指向const的指针、const视图对象、const元素是不同位置的限定；其他别名可能仍可修改原对象。

具体检查：分别写T* const、const T*与const T* const，并画出不可修改的层次。

### 移动转换 std::move

std::move把表达式转换为可供移动重载选择的值类别，实际资源转移发生在被选中的构造或赋值中。对const对象move可能仍调用复制，对视图move也不会获得底层数据所有权。

具体检查：记录移动构造调用次数，不用变量名或std::move的出现次数替代测量。

### 异常约定 noexcept

noexcept表达式可以依赖类型特征。违反不抛异常约定会终止程序；它不是自动捕获异常，也不是资源回滚代码。

具体检查：找出声明的条件与实际可能抛出的分配、构造操作是否一致。

### 对象表示 sizeof

sizeof给出对象表示大小，不是其引用的所有堆内存总量。sizeof视图很小并不说明底层数组很小。

具体检查：分别统计容器对象、容量字节和元素拥有的间接资源。

### 构造与new表达式

普通new可能分配并构造；placement new在给定地址构造，存储由其他机制提供。失败回滚应区分两类责任。

具体检查：追踪地址来自哪里、构造何时成功、由谁析构、由谁释放。

### 内部断言 assert

断言表达开发者预期成立的内部契约，发布构建可能关闭。它不能替代对不可信输入的完整错误处理，也不保证后续操作被运行时保护。

具体检查：对每条断言构造违反条件的输入，区分调用者错误与应向用户报告的错误。

### 类型别名 using

类型别名为已有类型建立名字，不创建运行期对象。它常把模板内部使用的类型统一暴露给泛型调用者。

具体检查：展开别名直到基础类型，区分类型别名和变量声明。

## 四、真实源码与逐行讲解

源码块保持原行内容，原始行号由小节标题及逐行表给出。表中的调用定位是静态阅读辅助；重载、模板实例化、宏展开和虚调用需结合完整声明，不能仅凭词法出现证明动态调用。

### BLI_array.hh：L1—L51

<!-- source:source/blender/blenlib/BLI_array.hh:1:51 -->

```cpp
/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

#pragma once

/** \file
 * \ingroup bli
 *
 * A `Array<T>` is a container for a fixed size array the size of which is NOT known at
 * compile time.
 *
 * If the size is known at compile time, `std::array<T, N>` should be used instead.
 *
 * Array should usually be used instead of Vector whenever the number of elements
 * is known at construction time. Note however, that Array will default construct all
 * elements when initialized with the size-constructor. For trivial types, this does nothing. In
 * all other cases, this adds overhead.
 *
 * A main benefit of using Array over Vector is that it expresses the intent of the developer
 * better. It indicates that the size of the data structure is not expected to change. Furthermore,
 * you can be more certain that an array does not over-allocate.
 *
 * Array supports small object optimization to improve performance when the size turns out
 * to be small at run-time.
 */

#include "BLI_allocator.hh"
#include "BLI_index_range.hh"
#include "BLI_memory_utils.hh"
#include "BLI_span.hh"
#include "BLI_utildefines.hh"

namespace blender {

template<
    /**
     * The type of the values stored in the array.
     */
    typename T,
    /**
     * The number of values that can be stored in the array, without doing a heap allocation.
     */
    int64_t InlineBufferCapacity = default_inline_buffer_capacity(sizeof(T)),
    /**
     * The allocator used by this array. Should rarely be changed, except when you don't want that
     * MEM_* functions are used internally.
     */
    typename Allocator = GuardedAllocator>
class Array {
 public:
```

| 原始行 | 语义、约束与检查 |
|---|---|
| L5 | 防止同一头文件在一个翻译单元中重复展开；不控制多个源文件之间的链接或对象寿命。 |
| L28 | 引入编译依赖 "BLI_allocator.hh"；这是声明可见性关系，不表示运行时一定调用该文件的所有接口。 |
| L29 | 引入编译依赖 "BLI_index_range.hh"；这是声明可见性关系，不表示运行时一定调用该文件的所有接口。 |
| L30 | 引入编译依赖 "BLI_memory_utils.hh"；这是声明可见性关系，不表示运行时一定调用该文件的所有接口。 |
| L31 | 引入编译依赖 "BLI_span.hh"；这是声明可见性关系，不表示运行时一定调用该文件的所有接口。 |
| L32 | 引入编译依赖 "BLI_utildefines.hh"；这是声明可见性关系，不表示运行时一定调用该文件的所有接口。 |
| L34 | 把后续声明放入 blender 命名空间，影响名称查找和符号归属，不创建运行时对象。 |
| L36 | 声明模板参数 `template<`。类型参数决定生成操作的类型，非类型参数可决定内嵌容量或编译期分支。 |
| L40 | 本行是连续声明或表达式的一部分：`typename T,`。与本段前后行合读；逗号、括号和限定符决定它属于参数、初始化列表还是实际计算。 |
| L44 | 显式采用编译器生成的特殊成员行为：`int64_t InlineBufferCapacity = default_inline_buffer_capacity(sizeof(T)),`。成员和基类的性质决定该操作是否可用、是否被删除及异常约定，不表示运行时给对象赋值为default。 |
| L49 | 把右侧 `GuardedAllocator>` 用于初始化或更新左侧 `typename Allocator`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L50 | 声明或定义类型 `class Array`。结合继承、访问权限和成员布局确认接口与拥有关系；前向声明本身没有完整对象布局。 |
| L51 | 切换成员访问权限为 public；它是编译期接口边界，不是线程同步或内存保护。 |

### BLI_array.hh：L52—L98

<!-- source:source/blender/blenlib/BLI_array.hh:52:98 -->

```cpp
  using value_type = T;
  using pointer = T *;
  using const_pointer = const T *;
  using reference = T &;
  using const_reference = const T &;
  using iterator = T *;
  using const_iterator = const T *;
  using size_type = int64_t;

 private:
  /** The beginning of the array. It might point into the inline buffer. */
  T *data_;

  /** Number of elements in the array. */
  int64_t size_;

  /** Used for allocations when the inline buffer is too small. */
  BLI_NO_UNIQUE_ADDRESS Allocator allocator_;

  /** A placeholder buffer that will remain uninitialized until it is used. */
  BLI_NO_UNIQUE_ADDRESS TypedBuffer<T, InlineBufferCapacity> inline_buffer_;

 public:
  /**
   * By default an empty array is created.
   */
  Array(Allocator allocator = {}) noexcept : allocator_(allocator)
  {
    data_ = inline_buffer_;
    size_ = 0;
  }

  Array(NoExceptConstructor, Allocator allocator = {}) noexcept : Array(allocator) {}

  /**
   * Create a new array that contains copies of all values.
   */
  template<typename U>
  Array(Span<U> values, Allocator allocator = {})
    requires(std::is_convertible_v<U, T>)
      : Array(NoExceptConstructor(), allocator)
  {
    const int64_t size = values.size();
    data_ = this->get_buffer_for_size(size);
    uninitialized_convert_n<U, T>(values.data(), size, data_);
    size_ = size;
  }
```

本段语义重点：

- `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。
- `size_`：该对象记录的元素数或长度，不能直接当作容量。
- `allocator_`：提供存储的分配策略对象，释放必须与分配策略匹配。
- `inline_buffer_`：容器对象内部的缓冲区，不能像堆缓冲那样直接交给另一个对象。

| 原始行 | 语义、约束与检查 |
|---|---|
| L52 | 定义类型别名 `using value_type = T`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L53 | 定义类型别名 `using pointer = T *`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L54 | 定义类型别名 `using const_pointer = const T *`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L55 | 定义类型别名 `using reference = T &`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L56 | 定义类型别名 `using const_reference = const T &`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L57 | 定义类型别名 `using iterator = T *`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L58 | 定义类型别名 `using const_iterator = const T *`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L59 | 定义类型别名 `using size_type = int64_t`，为模板接口或内部实现统一命名；本行不分配该类型对象。 |
| L61 | 切换成员访问权限为 private；它是编译期接口边界，不是线程同步或内存保护。 |
| L63 | 本行涉及 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。按此语义解读 `T *data_`，不要把地址、数量或状态混用。 |
| L66 | 本行涉及 `size_`：该对象记录的元素数或长度，不能直接当作容量。按此语义解读 `int64_t size_`，不要把地址、数量或状态混用。 |
| L69 | 本行涉及 `allocator_`：提供存储的分配策略对象，释放必须与分配策略匹配。按此语义解读 `BLI_NO_UNIQUE_ADDRESS Allocator allocator_`，不要把地址、数量或状态混用。 |
| L72 | 本行涉及 `inline_buffer_`：容器对象内部的缓冲区，不能像堆缓冲那样直接交给另一个对象。按此语义解读 `BLI_NO_UNIQUE_ADDRESS TypedBuffer<T, InlineBufferCapacity> inline_buffer_`，不要把地址、数量或状态混用。 |
| L74 | 切换成员访问权限为 public；它是编译期接口边界，不是线程同步或内存保护。 |
| L78 | 建立或更新 `allocator_`：提供存储的分配策略对象，释放必须与分配策略匹配。本行的具体值关系为 `Array(Allocator allocator = {}) noexcept : allocator_(allocator)`；对照更新前后相应范围或状态是否一致。 |
| L79 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L80 | 建立或更新 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。本行的具体值关系为 `data_ = inline_buffer_`；对照更新前后相应范围或状态是否一致。 |
| L81 | 建立或更新 `size_`：该对象记录的元素数或长度，不能直接当作容量。本行的具体值关系为 `size_ = 0`；对照更新前后相应范围或状态是否一致。 |
| L82 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L84 | 把右侧 `{}) noexcept : Array(allocator) {}` 用于初始化或更新左侧 `Array(NoExceptConstructor, Allocator allocator`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L89 | 声明模板参数 `template<typename U>`。类型参数决定生成操作的类型，非类型参数可决定内嵌容量或编译期分支。 |
| L90 | 把右侧 `{})` 用于初始化或更新左侧 `Array(Span<U> values, Allocator allocator`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L91 | 约束模板可用性：`requires(std::is_convertible_v<U, T>)`。条件在编译期检查，不替代运行期的地址、长度和类型一致性验证。 |
| L92 | 出现调用或函数声明 `Array`，对应表达式为 `: Array(NoExceptConstructor(), allocator)`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L93 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L94 | 把右侧 `values.size()` 用于初始化或更新左侧 `const int64_t size`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L95 | 建立或更新 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。本行的具体值关系为 `data_ = this->get_buffer_for_size(size)`；对照更新前后相应范围或状态是否一致。 |
| L96 | 本行涉及 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。按此语义解读 `uninitialized_convert_n<U, T>(values.data(), size, data_)`，不要把地址、数量或状态混用。 |
| L97 | 建立或更新 `size_`：该对象记录的元素数或长度，不能直接当作容量。本行的具体值关系为 `size_ = size`；对照更新前后相应范围或状态是否一致。 |
| L98 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |

### BLI_array.hh：L99—L154

<!-- source:source/blender/blenlib/BLI_array.hh:99:154 -->

```cpp

  /**
   * Create a new array that contains copies of all values.
   */
  template<typename U>
  Array(const std::initializer_list<U> &values, Allocator allocator = {})
    requires(std::is_convertible_v<U, T>)
      : Array(Span<U>(values), allocator)
  {
  }

  Array(const std::initializer_list<T> &values, Allocator allocator = {})
      : Array(Span<T>(values), allocator)
  {
  }

  /**
   * Create a new array with the given size. All values will be default constructed. For trivial
   * types like int, default construction does nothing.
   *
   * We might want another version of this in the future, that does not do default construction
   * even for non-trivial types. This should not be the default though, because one can easily mess
   * up when dealing with uninitialized memory.
   */
  explicit Array(int64_t size, Allocator allocator = {}) : Array(NoExceptConstructor(), allocator)
  {
    BLI_assert(size >= 0);
    data_ = this->get_buffer_for_size(size);
    default_construct_n(data_, size);
    size_ = size;
  }

  /**
   * Create a new array with the given size. All values will be initialized by copying the given
   * default.
   */
  Array(int64_t size, const T &value, Allocator allocator = {})
      : Array(NoExceptConstructor(), allocator)
  {
    BLI_assert(size >= 0);
    if (std::is_trivially_copyable_v<T> && value_is_zero_memory(value)) {
      data_ = this->get_buffer_for_size(size, true);
    }
    else {
      data_ = this->get_buffer_for_size(size);
#if defined(__GNUC__) && !defined(__clang__)
#  pragma GCC diagnostic push
#  pragma GCC diagnostic ignored "-Warray-bounds"
#endif
      uninitialized_fill_n(data_, size, value);
#if defined(__GNUC__) && !defined(__clang__)
#  pragma GCC diagnostic pop
#endif
    }
    size_ = size;
  }
```

本段语义重点：

- `default_construct_n`：为目标区间建立默认构造对象；基本类型默认初始化未必给出可读取的零。
- `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。
- `size_`：该对象记录的元素数或长度，不能直接当作容量。

| 原始行 | 语义、约束与检查 |
|---|---|
| L103 | 声明模板参数 `template<typename U>`。类型参数决定生成操作的类型，非类型参数可决定内嵌容量或编译期分支。 |
| L104 | 把右侧 `{})` 用于初始化或更新左侧 `Array(const std::initializer_list<U> &values, Allocator allocator`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L105 | 约束模板可用性：`requires(std::is_convertible_v<U, T>)`。条件在编译期检查，不替代运行期的地址、长度和类型一致性验证。 |
| L106 | 出现调用或函数声明 `Array`，对应表达式为 `: Array(Span<U>(values), allocator)`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L107 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L108 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L110 | 把右侧 `{})` 用于初始化或更新左侧 `Array(const std::initializer_list<T> &values, Allocator allocator`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L111 | 出现调用或函数声明 `Array`，对应表达式为 `: Array(Span<T>(values), allocator)`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L112 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L113 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L123 | 把右侧 `{}) : Array(NoExceptConstructor(), allocator)` 用于初始化或更新左侧 `explicit Array(int64_t size, Allocator allocator`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L124 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L125 | 断言约束 `BLI_assert(size >= 0);`。条件是后续访问的内部前置条件；发布构建可能不执行，不能把断言当作输入修复。 |
| L126 | 建立或更新 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。本行的具体值关系为 `data_ = this->get_buffer_for_size(size)`；对照更新前后相应范围或状态是否一致。 |
| L127 | 本行使用 `default_construct_n`：为目标区间建立默认构造对象；基本类型默认初始化未必给出可读取的零。 |
| L128 | 建立或更新 `size_`：该对象记录的元素数或长度，不能直接当作容量。本行的具体值关系为 `size_ = size`；对照更新前后相应范围或状态是否一致。 |
| L129 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L135 | 把右侧 `{})` 用于初始化或更新左侧 `Array(int64_t size, const T &value, Allocator allocator`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L136 | 出现调用或函数声明 `Array`，对应表达式为 `: Array(NoExceptConstructor(), allocator)`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L137 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L138 | 断言约束 `BLI_assert(size >= 0);`。条件是后续访问的内部前置条件；发布构建可能不执行，不能把断言当作输入修复。 |
| L139 | 判断 `std::is_trivially_copyable_v<T> && value_is_zero_memory(value)`，成立时进入本分支，否则继续后续路径。 |
| L140 | 建立或更新 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。本行的具体值关系为 `data_ = this->get_buffer_for_size(size, true)`；对照更新前后相应范围或状态是否一致。 |
| L141 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L142 | 处理前一条件不成立的互补路径。比较两条路径最后是否恢复同一不变量，以及是否产生不同的资源责任。 |
| L143 | 建立或更新 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。本行的具体值关系为 `data_ = this->get_buffer_for_size(size)`；对照更新前后相应范围或状态是否一致。 |
| L144 | 预处理阶段处理 #if defined(__GNUC__) && !defined(__clang__)。它决定哪些代码进入编译，不是运行时分支；阅读行为时必须结合实际构建宏。 |
| L145 | 本行是连续声明或表达式的一部分：`#  pragma GCC diagnostic push`。与本段前后行合读；逗号、括号和限定符决定它属于参数、初始化列表还是实际计算。 |
| L146 | 本行是连续声明或表达式的一部分：`#  pragma GCC diagnostic ignored "-Warray-bounds"`。与本段前后行合读；逗号、括号和限定符决定它属于参数、初始化列表还是实际计算。 |
| L147 | 预处理阶段处理 #endif。它决定哪些代码进入编译，不是运行时分支；阅读行为时必须结合实际构建宏。 |
| L148 | 本行涉及 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。按此语义解读 `uninitialized_fill_n(data_, size, value)`，不要把地址、数量或状态混用。 |
| L149 | 预处理阶段处理 #if defined(__GNUC__) && !defined(__clang__)。它决定哪些代码进入编译，不是运行时分支；阅读行为时必须结合实际构建宏。 |
| L150 | 本行是连续声明或表达式的一部分：`#  pragma GCC diagnostic pop`。与本段前后行合读；逗号、括号和限定符决定它属于参数、初始化列表还是实际计算。 |
| L151 | 预处理阶段处理 #endif。它决定哪些代码进入编译，不是运行时分支；阅读行为时必须结合实际构建宏。 |
| L152 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L153 | 建立或更新 `size_`：该对象记录的元素数或长度，不能直接当作容量。本行的具体值关系为 `size_ = size`；对照更新前后相应范围或状态是否一致。 |
| L154 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |

### BLI_array.hh：L155—L204

<!-- source:source/blender/blenlib/BLI_array.hh:155:204 -->

```cpp

  /**
   * Create a new array with uninitialized elements. The caller is responsible for constructing the
   * elements. Moving, copying or destructing an Array with uninitialized elements invokes
   * undefined behavior.
   *
   * This should be used very rarely. Note, that the normal size-constructor also does not
   * initialize the elements when T is trivially constructible. Therefore, it only makes sense to
   * use this with non trivially constructible types.
   *
   * Usage:
   *  Array<std::string> my_strings(10, NoInitialization());
   */
  Array(int64_t size, NoInitialization, Allocator allocator = {})
      : Array(NoExceptConstructor(), allocator)
  {
    BLI_assert(size >= 0);
    data_ = this->get_buffer_for_size(size);
    size_ = size;
  }

  Array(const Array &other) : Array(other.as_span(), other.allocator_) {}

  Array(Array &&other) noexcept(std::is_nothrow_move_constructible_v<T>)
      : Array(NoExceptConstructor(), other.allocator_)
  {
    if (other.data_ == other.inline_buffer_) {
#if defined(__GNUC__) && !defined(__clang__)
#  pragma GCC diagnostic push
#  pragma GCC diagnostic ignored "-Warray-bounds"
#endif
      uninitialized_relocate_n(other.data_, other.size_, data_);
#if defined(__GNUC__) && !defined(__clang__)
#  pragma GCC diagnostic pop
#endif
    }
    else {
      data_ = other.data_;
    }
    size_ = other.size_;

    other.data_ = other.inline_buffer_;
    other.size_ = 0;
  }

  ~Array()
  {
    destruct_n(data_, size_);
    this->deallocate_if_not_inline(data_);
  }
```

本段语义重点：

- `uninitialized_relocate_n`：在目标原始存储建立n个对象，并结束源对象寿命；与仅移动构造不同，后续不能再次把源当作存活元素销毁。
- `destruct_n`：对已构造的元素区间执行析构；计数必须对应真实存活对象，释放原始内存是另一操作。
- `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。
- `size_`：该对象记录的元素数或长度，不能直接当作容量。
- `allocator_`：提供存储的分配策略对象，释放必须与分配策略匹配。

| 原始行 | 语义、约束与检查 |
|---|---|
| L168 | 把右侧 `{})` 用于初始化或更新左侧 `Array(int64_t size, NoInitialization, Allocator allocator`。声明初始化与已有对象赋值应按上下文区分；有资源的类型会调用相应特殊成员。 |
| L169 | 出现调用或函数声明 `Array`，对应表达式为 `: Array(NoExceptConstructor(), allocator)`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L170 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L171 | 断言约束 `BLI_assert(size >= 0);`。条件是后续访问的内部前置条件；发布构建可能不执行，不能把断言当作输入修复。 |
| L172 | 建立或更新 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。本行的具体值关系为 `data_ = this->get_buffer_for_size(size)`；对照更新前后相应范围或状态是否一致。 |
| L173 | 建立或更新 `size_`：该对象记录的元素数或长度，不能直接当作容量。本行的具体值关系为 `size_ = size`；对照更新前后相应范围或状态是否一致。 |
| L174 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L176 | 本行涉及 `allocator_`：提供存储的分配策略对象，释放必须与分配策略匹配。按此语义解读 `Array(const Array &other) : Array(other.as_span(), other.allocator_) {}`，不要把地址、数量或状态混用。 |
| L178 | 出现调用或函数声明 `Array`，对应表达式为 `Array(Array &&other) noexcept(std::is_nothrow_move_constructible_v<T>)`。参数求值、返回类型与重载需结合前后完整语句；静态文本引用不能证明动态目标。 |
| L179 | 本行涉及 `allocator_`：提供存储的分配策略对象，释放必须与分配策略匹配。按此语义解读 `: Array(NoExceptConstructor(), other.allocator_)`，不要把地址、数量或状态混用。 |
| L180 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L181 | 判断 `other.data_ == other.inline_buffer_`，成立时进入本分支，否则继续后续路径。 |
| L182 | 预处理阶段处理 #if defined(__GNUC__) && !defined(__clang__)。它决定哪些代码进入编译，不是运行时分支；阅读行为时必须结合实际构建宏。 |
| L183 | 本行是连续声明或表达式的一部分：`#  pragma GCC diagnostic push`。与本段前后行合读；逗号、括号和限定符决定它属于参数、初始化列表还是实际计算。 |
| L184 | 本行是连续声明或表达式的一部分：`#  pragma GCC diagnostic ignored "-Warray-bounds"`。与本段前后行合读；逗号、括号和限定符决定它属于参数、初始化列表还是实际计算。 |
| L185 | 预处理阶段处理 #endif。它决定哪些代码进入编译，不是运行时分支；阅读行为时必须结合实际构建宏。 |
| L186 | 本行使用 `uninitialized_relocate_n`：在目标原始存储建立n个对象，并结束源对象寿命；与仅移动构造不同，后续不能再次把源当作存活元素销毁。 |
| L187 | 预处理阶段处理 #if defined(__GNUC__) && !defined(__clang__)。它决定哪些代码进入编译，不是运行时分支；阅读行为时必须结合实际构建宏。 |
| L188 | 本行是连续声明或表达式的一部分：`#  pragma GCC diagnostic pop`。与本段前后行合读；逗号、括号和限定符决定它属于参数、初始化列表还是实际计算。 |
| L189 | 预处理阶段处理 #endif。它决定哪些代码进入编译，不是运行时分支；阅读行为时必须结合实际构建宏。 |
| L190 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L191 | 处理前一条件不成立的互补路径。比较两条路径最后是否恢复同一不变量，以及是否产生不同的资源责任。 |
| L192 | 建立或更新 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。本行的具体值关系为 `data_ = other.data_`；对照更新前后相应范围或状态是否一致。 |
| L193 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L194 | 建立或更新 `size_`：该对象记录的元素数或长度，不能直接当作容量。本行的具体值关系为 `size_ = other.size_`；对照更新前后相应范围或状态是否一致。 |
| L196 | 建立或更新 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。本行的具体值关系为 `other.data_ = other.inline_buffer_`；对照更新前后相应范围或状态是否一致。 |
| L197 | 建立或更新 `size_`：该对象记录的元素数或长度，不能直接当作容量。本行的具体值关系为 `other.size_ = 0`；对照更新前后相应范围或状态是否一致。 |
| L198 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L200 | 涉及析构接口或显式析构：`~Array()`。检查目标对象已成功构造，且资源不会在另一条清理路径再次销毁。 |
| L201 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L202 | 本行使用 `destruct_n`：对已构造的元素区间执行析构；计数必须对应真实存活对象，释放原始内存是另一操作。 |
| L203 | 本行涉及 `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。按此语义解读 `this->deallocate_if_not_inline(data_)`，不要把地址、数量或状态混用。 |
| L204 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |

### BLI_array.hh：L205—L245

<!-- source:source/blender/blenlib/BLI_array.hh:205:245 -->

```cpp

  Array &operator=(const Array &other)
  {
    return copy_assign_container(*this, other);
  }

  Array &operator=(Array &&other) noexcept(std::is_nothrow_move_constructible_v<T>)
  {
    return move_assign_container(*this, std::move(other));
  }

  T &operator[](int64_t index)
  {
    BLI_assert(index >= 0);
    BLI_assert(index < size_);
    return data_[index];
  }

  const T &operator[](int64_t index) const
  {
    BLI_assert(index >= 0);
    BLI_assert(index < size_);
    return data_[index];
  }

  operator Span<T>() const
  {
    return Span<T>(data_, size_);
  }

  operator MutableSpan<T>()
  {
    return MutableSpan<T>(data_, size_);
  }

  template<typename U>
  operator Span<U>() const
    requires(is_span_convertible_pointer_v<T, U>)
  {
    return Span<U>(data_, size_);
  }
```

本段语义重点：

- `data_`：数据或实现的存储入口；是否拥有应按该类声明和析构判定。
- `size_`：该对象记录的元素数或长度，不能直接当作容量。

| 原始行 | 语义、约束与检查 |
|---|---|
| L206 | 运算符重载声明、定义或显式调用：`Array &operator=(const Array &other)`。结合参数和返回类型判断是赋值、索引、比较还是转换；operator=声明中的等号不是在给名为operator的变量赋值。 |
| L207 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L208 | 返回表达式 `copy_assign_container(*this, other)`。 |
| L209 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L211 | 运算符重载声明、定义或显式调用：`Array &operator=(Array &&other) noexcept(std::is_nothrow_move_constructible_v<T>)`。结合参数和返回类型判断是赋值、索引、比较还是转换；operator=声明中的等号不是在给名为operator的变量赋值。 |
| L212 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L213 | 返回表达式 `move_assign_container(*this, std::move(other))`。 |
| L214 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L216 | 运算符重载声明、定义或显式调用：`T &operator[](int64_t index)`。结合参数和返回类型判断是赋值、索引、比较还是转换；operator=声明中的等号不是在给名为operator的变量赋值。 |
| L217 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L218 | 断言约束 `BLI_assert(index >= 0);`。条件是后续访问的内部前置条件；发布构建可能不执行，不能把断言当作输入修复。 |
| L219 | 断言约束 `BLI_assert(index < size_);`。条件是后续访问的内部前置条件；发布构建可能不执行，不能把断言当作输入修复。 |
| L220 | 返回表达式 `data_[index]`。 |
| L221 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L223 | 运算符重载声明、定义或显式调用：`const T &operator[](int64_t index) const`。结合参数和返回类型判断是赋值、索引、比较还是转换；operator=声明中的等号不是在给名为operator的变量赋值。 |
| L224 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L225 | 断言约束 `BLI_assert(index >= 0);`。条件是后续访问的内部前置条件；发布构建可能不执行，不能把断言当作输入修复。 |
| L226 | 断言约束 `BLI_assert(index < size_);`。条件是后续访问的内部前置条件；发布构建可能不执行，不能把断言当作输入修复。 |
| L227 | 返回表达式 `data_[index]`。 |
| L228 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L230 | 运算符重载声明、定义或显式调用：`operator Span<T>() const`。结合参数和返回类型判断是赋值、索引、比较还是转换；operator=声明中的等号不是在给名为operator的变量赋值。 |
| L231 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L232 | 返回表达式 `Span<T>(data_, size_)`。 |
| L233 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L235 | 运算符重载声明、定义或显式调用：`operator MutableSpan<T>()`。结合参数和返回类型判断是赋值、索引、比较还是转换；operator=声明中的等号不是在给名为operator的变量赋值。 |
| L236 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L237 | 返回表达式 `MutableSpan<T>(data_, size_)`。 |
| L238 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |
| L240 | 声明模板参数 `template<typename U>`。类型参数决定生成操作的类型，非类型参数可决定内嵌容量或编译期分支。 |
| L241 | 运算符重载声明、定义或显式调用：`operator Span<U>() const`。结合参数和返回类型判断是赋值、索引、比较还是转换；operator=声明中的等号不是在给名为operator的变量赋值。 |
| L242 | 约束模板可用性：`requires(is_span_convertible_pointer_v<T, U>)`。条件在编译期检查，不替代运行期的地址、长度和类型一致性验证。 |
| L243 | 连接上一行的声明或控制结构与其语句块；后续行在这个作用域中执行或声明。 |
| L244 | 返回表达式 `Span<U>(data_, size_)`。 |
| L245 | 结束当前语法单元。局部自动对象在离开其作用域时按规则销毁；这不等于所有被引用的外部数据也被释放。 |

## 五、接口定位、调用线索与生命周期

### 本篇声明与实现入口

| 源码位置 | 实际声明片段 |
|---|---|
| [BLI_array.hh:L50](../../../../../source/blender/blenlib/BLI_array.hh#L50) | `class Array` |
| [BLI_array.hh:L78](../../../../../source/blender/blenlib/BLI_array.hh#L78) | `Array(Allocator allocator = {}) noexcept : allocator_(allocator)` |
| [BLI_array.hh:L84](../../../../../source/blender/blenlib/BLI_array.hh#L84) | `Array(NoExceptConstructor, Allocator allocator = {}) noexcept : Array(allocator) {}` |
| [BLI_array.hh:L90](../../../../../source/blender/blenlib/BLI_array.hh#L90) | `Array(Span<U> values, Allocator allocator = {})` |
| [BLI_array.hh:L92](../../../../../source/blender/blenlib/BLI_array.hh#L92) | `: Array(NoExceptConstructor(), allocator)` |
| [BLI_array.hh:L104](../../../../../source/blender/blenlib/BLI_array.hh#L104) | `Array(const std::initializer_list<U> &values, Allocator allocator = {})` |
| [BLI_array.hh:L106](../../../../../source/blender/blenlib/BLI_array.hh#L106) | `: Array(Span<U>(values), allocator)` |
| [BLI_array.hh:L110](../../../../../source/blender/blenlib/BLI_array.hh#L110) | `Array(const std::initializer_list<T> &values, Allocator allocator = {})` |
| [BLI_array.hh:L111](../../../../../source/blender/blenlib/BLI_array.hh#L111) | `: Array(Span<T>(values), allocator)` |
| [BLI_array.hh:L123](../../../../../source/blender/blenlib/BLI_array.hh#L123) | `explicit Array(int64_t size, Allocator allocator = {}) : Array(NoExceptConstructor(), allocator)` |
| [BLI_array.hh:L135](../../../../../source/blender/blenlib/BLI_array.hh#L135) | `Array(int64_t size, const T &value, Allocator allocator = {})` |
| [BLI_array.hh:L136](../../../../../source/blender/blenlib/BLI_array.hh#L136) | `: Array(NoExceptConstructor(), allocator)` |
| [BLI_array.hh:L168](../../../../../source/blender/blenlib/BLI_array.hh#L168) | `Array(int64_t size, NoInitialization, Allocator allocator = {})` |
| [BLI_array.hh:L169](../../../../../source/blender/blenlib/BLI_array.hh#L169) | `: Array(NoExceptConstructor(), allocator)` |
| [BLI_array.hh:L176](../../../../../source/blender/blenlib/BLI_array.hh#L176) | `Array(const Array &other) : Array(other.as_span(), other.allocator_) {}` |
| [BLI_array.hh:L178](../../../../../source/blender/blenlib/BLI_array.hh#L178) | `Array(Array &&other) noexcept(std::is_nothrow_move_constructible_v<T>)` |
| [BLI_array.hh:L179](../../../../../source/blender/blenlib/BLI_array.hh#L179) | `: Array(NoExceptConstructor(), other.allocator_)` |

### 同名符号出现位置

以下表提供跨文件阅读入口，包含声明、调用或测试使用；没有经过完整C++名称解析，不把它命名为已证明的运行时调用图。

| 符号 | 位置 | 文本证据 |
|---|---|---|
| `Array` | [BLI_virtual_array.hh:L969](../../../../../source/blender/blenlib/BLI_virtual_array.hh#L969) | `owned_data_.~Array();` |
| `Array` | [BLI_virtual_array.hh:L1042](../../../../../source/blender/blenlib/BLI_virtual_array.hh#L1042) | `owned_data_.~Array();` |

### 生命周期推理图

```mermaid
flowchart LR
  O["调用者或源数据拥有者"]:::input
  V["Array构造与存储的接口与状态"]:::abstraction
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

本方向的共同数值模型如下。本篇的专门检查是：对int和string分别检查默认构造、值填充和从Span复制，避免读取未初始化标量。

| 步骤 | 数据或状态 | 为什么需要这一步 |
|---|---|---|
| 初始 | size=0, capacity=4 | 只有存储，没有可读取的T元素 |
| 追加A | size=1, capacity=4 | 在第0个位置构造A |
| 追加到满 | size=4, capacity=4 | 四个位置均已构造 |
| 请求第五个 | 需扩大存储 | 旧地址仍需被正确管理 |
| 迁移成功 | 新缓冲含原4元素 | 提交新指针并释放旧存储 |
| 追加E | size=5 | 只在成功构造后扩大有效区间 |

```mermaid
flowchart TB
  T0["size=0, capacity=4"]:::input
  T1["size=1, capacity=4"]:::compute
  T2["size=4, capacity=4"]:::compute
  T3["需扩大存储"]:::compute
  T4["新缓冲含原4元素"]:::compute
  T5["size=5"]:::result
  T0 -->|"追加A"| T1
  T1 -->|"追加到满"| T2
  T2 -->|"请求第五个"| T3
  T3 -->|"迁移成功"| T4
  T4 -->|"追加E"| T5
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

图是教学推演模型；精确分支与状态更新以本篇摘录及调用契约为准。

### 本篇独立练习与参考思路

对int和string分别检查默认构造、值填充和从Span复制，避免读取未初始化标量。

参考思路：元素数不作为类型参数，存储可能使用内嵌缓冲；初始化方式决定基本类型是否有可读取的值。

将输入、预期结果和资源责任分成三张清单。先用最直接的实现给出可核对的答案，再替换成对应源码使用的表示；比较结果不变的条件，而不是只比较接口名字。

验收依据：构造成功次数减析构次数应等于当前存活对象数；异常之后资源计数应回到合法状态。

## 七、复杂度、设计取舍与其他基础库

对比std::vector、std::array、std::span与LLVM SmallVector、ArrayRef时，分别比较拥有关系、内嵌存储、大小是否属于类型和失效条件。不要根据同名方法推断完全相同契约。

本篇的具体取舍：元素数不作为类型参数，存储可能使用内嵌缓冲；初始化方式决定基本类型是否有可读取的值。

| 观察维度 | 从源码取得证据的方法 | 本篇要避免的误判 |
|---|---|---|
| 时间 | 对循环次数、分派次数和重建频率分别计数 | 看到单次常数操作就断定整个操作序列是常数成本 |
| 内存 | 区分对象本体、容量存储、间接资源和共享控制块 | 用sizeof代替总内存 |
| 安全 | 沿构造、失败回滚、销毁与失效逐路径检查 | 把断言或非空指针当作完整安全证明 |
| 并发 | 逐字段确认锁、发布顺序和借用寿命 | 把引用计数线程安全等同数据读写线程安全 |

相关一手资料：

- [C++公开工作草案](https://eel.is/c++draft/)：持续更新的工作草案；语言与标准库语义以相应章节为准。
- [LLVM Programmer’s Manual](https://llvm.org/docs/ProgrammersManual.html)：在线版，2026-10-14查阅；仅比较设计思路，不保证与本地LLVM版本一致。

资料用于核对契约和进一步阅读；这里没有声称外部库与Blender实现相同，也没有把上游性能数字当作本机实测。

## 八、历史提交与设计演化

### 2020-08-19 · Jacques Lucke

[BLI: improve exception safety of Vector, Array and Stack](https://projects.blender.org/blender/blender/commit/2aff45146f1464ba8899368ad004522cb6a1a98c)

完整哈希：`2aff45146f1464ba8899368ad004522cb6a1a98c`。提交标题与作者日期来自本地Git对象。

提交说明原文（历史证据，不能直接作为当前API说明）：

```text
BLI: improve exception safety of Vector, Array and Stack

Using C++ exceptions in Blender is difficult, due to the large
number of C functions in the call stack. However, C++ data
structures in blenlib should at least try to be exception safe,
so that they can be used if someone wants to use exceptions
in some isolated area.

This patch improves the exception safety of the Vector, Array
and Stack data structure. This is mainly achieved by reordering
some lines and doing some explicit exception handling.
I don't expect performance of common operations to be affected
by this change.

The three containers are supposed to provide at least the
basic exception guarantee for most methods (except for e.g.
`*_unchecked` methods). So, resources should not leak when
the contained type throws an exception.

I also added new unit tests that test the exception handling
in various cases.
```

阅读任务：先根据说明复述旧问题，提出一个自己的修复方案，再对照diff。结合本篇重点“固定大小动态数组为什么还需要复杂构造逻辑？”判断方案改变的是表示、接口、生命周期还是调度。

### 2020-06-09 · Jacques Lucke

[BLI: rename ArrayRef to Span](https://projects.blender.org/blender/blender/commit/f7c0f1b8b83ac475755b633abf59cf9f447b2d49)

完整哈希：`f7c0f1b8b83ac475755b633abf59cf9f447b2d49`。提交标题与作者日期来自本地Git对象。

提交说明原文（历史证据，不能直接作为当前API说明）：

```text
BLI: rename ArrayRef to Span

This also renames `MutableArrayRef` to `MutableSpan`.
The name "Span" works better, because `std::span` will provide
similar functionality in C++20. Furthermore, a shorter, more
concise name for a common data structure is nice.
```

阅读任务：先根据说明复述旧问题，提出一个自己的修复方案，再对照diff。结合本篇重点“固定大小动态数组为什么还需要复杂构造逻辑？”判断方案改变的是表示、接口、生命周期还是调度。

## 九、反例、测试入口与掌握标准

仓库测试入口：

- [BLI_array_test.cc](../../../../../source/blender/blenlib/tests/BLI_array_test.cc)：阅读输入、断言与覆盖边界；本篇不把“存在测试”写成“本轮已运行”。

需要实际构造的反例：

- 空输入或没有结果需求：确认接口允许的空状态与不允许访问的操作。
- 边界位置和退化结构：把长度为1、末尾位置、重复值或深链代入真实分支。
- 生命周期结束或修改之后：检查保存的指针、引用、结果视图是否仍有效。
- 与本篇核心不变量相冲突的输入：对int和string分别检查默认构造、值填充和从Span复制，避免读取未初始化标量。

### 可运行的教学参考程序

[reference_exercises.cc](../_tools/reference_exercises.cc)包含独立于Blender的C++20参考检查：视图、简化SmallVector、异常回滚、哈希碰撞与删除、偏移数组、拓扑映射、共享缓存、表达式、惰性分支、闭包和暴力最近邻。

参考程序有意省略生产实现的完整能力。例如SmallVector禁止复制移动容器，不支持只能移动的元素，并禁止append参数别名到自身元素；TinyMap固定8槽，不提供增长。程序通过不能替代Blender实现测试。实际运行结果、编译器与命令见验收报告。

掌握标准：离开源码解释“固定大小动态数组为什么还需要复杂构造逻辑？”；独立完成上述练习；能指出一个会破坏拥有型容器相关约束的最小反例，并用具体代码行说明检查或修复应放在哪里。
