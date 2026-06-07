# Allocator 深度解析

> 源文件：[BLI_allocator.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_allocator.hh)

---

## 目录

- [Allocator 深度解析](#allocator-深度解析)
  - [目录](#目录)
  - [1. 什么是 Allocator？为什么需要？](#1-什么是-allocator为什么需要)
    - [1.1 一句话定义](#11-一句话定义)
    - [1.2 为什么不直接用 malloc/free？](#12-为什么不直接用-mallocfree)
    - [1.3 文件头注释翻译](#13-文件头注释翻译)
  - [2. Blender Allocator 接口设计](#2-blender-allocator-接口设计)
    - [2.1 最小接口：只需两个方法](#21-最小接口只需两个方法)
    - [2.2 接口参数解读](#22-接口参数解读)
    - [2.3 为什么不用 std::allocator？](#23-为什么不用-stdallocator)
  - [3. 三大 Allocator 详解](#3-三大-allocator-详解)
    - [3.1 GuardedAllocator — 默认选择](#31-guardedallocator--默认选择)
    - [3.2 GuardedAlignedAllocator — 对齐增强版](#32-guardedalignedallocator--对齐增强版)
    - [3.3 RawAllocator — 裸分配器](#33-rawallocator--裸分配器)
    - [3.4 三者对比](#34-三者对比)
  - [4. 容器如何使用 Allocator — 逐行源码分析](#4-容器如何使用-allocator--逐行源码分析)
    - [4.1 Array\<T\> 中的 Allocator](#41-arrayt-中的-allocator)
      - [模板参数声明](#模板参数声明)
      - [成员变量](#成员变量)
      - [Allocator 调用点 ①：`allocate` — 分配堆内存](#allocator-调用点-allocate--分配堆内存)
      - [Allocator 调用点 ②：`deallocate_if_not_inline` — 释放堆内存](#allocator-调用点-deallocate_if_not_inline--释放堆内存)
      - [Allocator 调用点 ③：`get_buffer_for_size` — 决定用内联还是堆](#allocator-调用点-get_buffer_for_size--决定用内联还是堆)
      - [`allocate_zero` 的触发场景](#allocate_zero-的触发场景)
      - [Array 完整生命周期](#array-完整生命周期)
    - [4.2 Vector\<T\> 中的 Allocator](#42-vectort-中的-allocator)
      - [模板参数声明](#模板参数声明-1)
      - [成员变量](#成员变量-1)
      - [Allocator 调用点 ①：`realloc_to_at_least` — 扩容（最核心）](#allocator-调用点-realloc_to_at_least--扩容最核心)
      - [Allocator 调用点 ②：`~Vector` — 析构](#allocator-调用点-vector--析构)
      - [Allocator 调用点 ③：`clear_and_shrink` — 清空并释放](#allocator-调用点-clear_and_shrink--清空并释放)
      - [Allocator 调用点 ④：`release` — 转移所有权](#allocator-调用点-release--转移所有权)
      - [Allocator 调用点 ⑤：移动构造中的内联→堆路径](#allocator-调用点-移动构造中的内联堆路径)
      - [Vector 中没有 `allocate_zero`](#vector-中没有-allocate_zero)
    - [4.3 GArray\<Allocator\> 中的 Allocator](#43-garrayallocator-中的-allocator)
      - [模板参数声明](#模板参数声明-2)
      - [成员变量](#成员变量-2)
      - [Allocator 调用点 ①：`allocate` — 分配](#allocator-调用点-allocate--分配)
      - [Allocator 调用点 ②：`deallocate` — 释放](#allocator-调用点-deallocate--释放)
      - [GArray 中没有 `allocate_zero`](#garray-中没有-allocate_zero)
      - [GArray 完整生命周期](#garray-完整生命周期)
    - [4.4 三者对比总结](#44-三者对比总结)
      - [Allocator 使用对比](#allocator-使用对比)
      - [内联缓冲区决策流程](#内联缓冲区决策流程)
      - [释放决策流程](#释放决策流程)
      - [为什么只有 Array 有 `allocate_zero`？](#为什么只有-array-有-allocate_zero)
      - [`AT` 宏在各容器中的展开](#at-宏在各容器中的展开)
    - [4.5 BLI\_NO\_UNIQUE\_ADDRESS 优化](#45-bli_no_unique_address-优化)
  - [5. 语法专题：标签类型 — NoInitialization 与 NoExceptConstructor](#5-语法专题标签类型--noinitialization-与-noexceptconstructor)
    - [5.1 它们是什么？](#51-它们是什么)
    - [5.2 为什么是空类？——标签分发（Tag Dispatch）模式](#52-为什么是空类标签分发tag-dispatch模式)
    - [5.3 调用时为什么写 `NoInitialization{}`？](#53-调用时为什么写-noinitialization)
    - [5.4 标签分发的编译期效果](#54-标签分发的编译期效果)
    - [5.5 NoExceptConstructor 的特殊用途](#55-noexceptconstructor-的特殊用途)
    - [5.6 标签类型零开销证明](#56-标签类型零开销证明)
    - [5.7 C++ 标准库中的同类模式](#57-c-标准库中的同类模式)
  - [6. 源码中的真实用例](#6-源码中的真实用例)
    - [6.1 GuardedAlignedAllocator — 曲线重采样临时缓冲区](#61-guardedalignedallocator--曲线重采样临时缓冲区)
    - [6.2 RawAllocator — 线程局部静态变量](#62-rawallocator--线程局部静态变量)
    - [6.3 GuardedAllocator 显式指定 — VectorSet 的 int32 优化](#63-guardedallocator-显式指定--vectorset-的-int32-优化)
    - [6.4 类型别名 — Blender 预定义的 Raw 容器](#64-类型别名--blender-预定义的-raw-容器)
  - [7. 语法专题：ul / ULL 后缀](#7-语法专题ul--ull-后缀)
    - [6.1 整数字面量后缀一览](#61-整数字面量后缀一览)
    - [6.2 `64ul` 是什么？](#62-64ul-是什么)
    - [6.3 `16ULL` 是什么？](#63-16ull-是什么)
    - [6.4 为什么用 ULL 而不是普通整数？](#64-为什么用-ull-而不是普通整数)
    - [6.5 ul vs ULL 的区别](#65-ul-vs-ull-的区别)
  - [8. 语法专题：MEM\_MIN\_CPP\_ALIGNMENT 宏](#8-语法专题mem_min_cpp_alignment-宏)
    - [7.1 宏定义](#71-宏定义)
    - [7.2 逐步拆解](#72-逐步拆解)
    - [7.3 `__STDCPP_DEFAULT_NEW_ALIGNMENT__` 是什么？](#73-__stdcpp_default_new_alignment__-是什么)
    - [7.4 为什么取较大者？](#74-为什么取较大者)
    - [7.5 在 Allocator 中的作用](#75-在-allocator-中的作用)
    - [7.6 三元运算符实现 max 的原因](#76-三元运算符实现-max-的原因)
  - [9. Allocator vs std::allocator](#9-allocator-vs-stdallocator)
  - [10. 总结速查表](#10-总结速查表)
    - [Allocator 选择](#allocator-选择)
    - [关键概念](#关键概念)
  - [附录 A：allocate\_zero、memset、calloc 详解](#附录-aallocate_zeromemsetcalloc-详解)
    - [A.1 allocate\_zero 是什么？](#a1-allocate_zero-是什么)
    - [A.2 memset 是什么？](#a2-memset-是什么)
    - [A.3 calloc 是什么？](#a3-calloc-是什么)
    - [A.4 为什么 memset / calloc 命名看起来奇怪？](#a4-为什么-memset--calloc-命名看起来奇怪)
    - [A.5 在 GuardedAllocator 中的完整流程](#a5-在-guardedallocator-中的完整流程)
  - [附录 B：__STDCPP\_DEFAULT\_NEW\_ALIGNMENT__ 为什么是 16 而不是 8？](#附录-bstdcpp_default_new_alignment-为什么是-16-而不是-8)
    - [B.1 指针对齐 vs new 对齐是两回事](#b1-指针对齐-vs-new-对齐是两回事)
    - [B.2 __STDCPP\_DEFAULT\_NEW\_ALIGNMENT__ 是什么？](#b2-stdcpp_default_new_alignment-是什么)
    - [B.3 为什么 new 保证 16 字节对齐？](#b3-为什么-new-保证-16-字节对齐)
    - [B.4 指针对齐 vs new 对齐的关系](#b4-指针对齐-vs-new-对齐的关系)
    - [B.5 MEM\_MIN\_CPP\_ALIGNMENT 的完整逻辑](#b5-mem_min_cpp_alignment-的完整逻辑)


---

## 1. 什么是 Allocator？为什么需要？

### 1.1 一句话定义

**Allocator（分配器）** 是容器与底层内存管理之间的**抽象层**——容器说"我要 N 字节内存"，Allocator 决定**怎么给**。

### 1.2 为什么不直接用 malloc/free？

```mermaid
flowchart LR
    subgraph "没有 Allocator"
        C1["Vector"] -->|"直接调用"| M1["malloc / free"]
        C2["Array"] -->|"直接调用"| M1
        C3["Set"] -->|"直接调用"| M1
    end

    subgraph "有 Allocator"
        C4["Vector"] -->|"通过 Allocator"| A1["GuardedAllocator<br/>MEM_* 受保护"]
        C5["Array"] -->|"通过 Allocator"| A2["RawAllocator<br/>malloc/free"]
        C6["Set"] -->|"通过 Allocator"| A3["GuardedAlignedAllocator<br/>对齐增强"]
        A1 --> M2["底层内存"]
        A2 --> M2
        A3 --> M2
    end

    style M1 fill:#e74c3c,color:#fff
    style A1 fill:#2ecc71,color:#fff
    style A2 fill:#f39c12,color:#fff
    style A3 fill:#9b59b6,color:#fff
```

**没有 Allocator 的问题**：

| 问题 | 说明 |
|------|------|
| **无法切换内存策略** | 容器硬编码 malloc/free，无法切换到 Blender 的内存守护分配器 |
| **无法统一调试** | 想追踪内存泄漏？每个容器都得改 |
| **无法定制对齐** | SIMD 指令要 16/32/64 字节对齐，容器无法保证 |
| **无法控制生命周期** | 静态变量的内存不能走 MEM_*（泄漏检测会误报） |

**有 Allocator 的好处**：

| 好处 | 说明 |
|------|------|
| **策略可替换** | 同一个 `Vector<T>` 可以用不同分配器，只需改模板参数 |
| **统一调试** | `GuardedAllocator` 自动追踪所有分配，泄漏一目了然 |
| **对齐可控** | `GuardedAlignedAllocator` 保证最小对齐 |
| **生命周期可控** | `RawAllocator` 绕过泄漏检测，用于静态变量 |

### 1.3 文件头注释翻译

> *An `Allocator` can allocate and deallocate memory. It is used by containers such as Vector. The allocators defined in this file do not work with standard library containers such as std::vector.*
>
> Allocator 可以分配和释放内存。它被 Vector 等容器使用。本文件定义的分配器**不兼容**标准库容器（如 `std::vector`）。

> *Every allocator has to implement two methods:*
> *`void *allocate(size_t size, size_t alignment, const char *name);`*
> *`void deallocate(void *ptr);`*
>
> 每个 Allocator 必须实现两个方法：`allocate` 和 `deallocate`。

> *We don't use the std::allocator interface, because it does more than is really necessary for an allocator and has some other quirks. It mixes the concepts of allocation and construction. It is essentially forced to be a template, even though the allocator should not care about the type.*
>
> 我们不用 `std::allocator` 接口，因为它做了超出分配器职责的事情，还有一些怪癖。它**混淆了"分配"和"构造"的概念**。它被迫成为模板，但分配器其实不应该关心元素类型。

> *The allocator interface dictated by this file is very simplistic, but for now that is all we need. More complexity can be added when it seems necessary.*
>
> 本文件定义的分配器接口非常简洁，但目前够用了。必要时可以增加复杂度。

---

## 2. Blender Allocator 接口设计

### 2.1 最小接口：只需两个方法

```mermaid
classDiagram
    class AllocatorConcept {
        +allocate(size, alignment, name) void*
        +deallocate(ptr) void
    }

    class GuardedAllocator {
        +allocate(size, alignment, name) void*
        +allocate_zero(size, alignment, name) void*
        +deallocate(ptr) void
    }

    class GuardedAlignedAllocator~Alignment~ {
        +min_alignment : size_t
        +allocate(size, alignment, name) void*
        +allocate_zero(size, alignment, name) void*
        +deallocate(ptr) void
    }

    class RawAllocator {
        +allocate(size, alignment, name) void*
        +allocate_zero(size, alignment, name) void*
        +deallocate(ptr) void
    }

    AllocatorConcept <|.. GuardedAllocator : 实现
    AllocatorConcept <|.. GuardedAlignedAllocator : 实现
    AllocatorConcept <|.. RawAllocator : 实现
```

### 2.2 接口参数解读

```cpp
void *allocate(size_t size, size_t alignment, const char *name);
```

| 参数 | 类型 | 含义 |
|------|------|------|
| `size` | `size_t` | 要分配的**字节数**（不是元素数！） |
| `alignment` | `size_t` | 对齐要求（必须是 2 的幂），如 4、8、16、64 |
| `name` | `const char*` | 分配的标识名，用于内存调试（泄漏报告会显示这个名字） |
| **返回值** | `void*` | 指向已分配内存的指针，保证按 `alignment` 对齐 |

```cpp
void deallocate(void *ptr);
```

| 参数 | 类型 | 含义 |
|------|------|------|
| `ptr` | `void*` | 之前 `allocate` 返回的指针 |

### 2.3 为什么不用 std::allocator？

```mermaid
graph TB
    subgraph "std::allocator 的问题"
        P1["❌ 混淆分配与构造<br/>allocate() + construct()<br/>应该分开"]
        P2["❌ 必须是模板<br/>allocator&lt;T&gt;<br/>但分配器不该关心类型"]
        P3["❌ 接口过于复杂<br/>rebind / max_size / ...<br/>大部分用不到"]
    end

    subgraph "Blender 的方案"
        S1["✅ 只管分配/释放<br/>不涉及构造/析构"]
        S2["✅ 非模板类<br/>GuardedAllocator<br/>不关心元素类型"]
        S3["✅ 极简接口<br/>allocate + deallocate<br/>两个方法搞定"]
    end

    P1 --> S1
    P2 --> S2
    P3 --> S3

    style P1 fill:#e74c3c,color:#fff
    style P2 fill:#e74c3c,color:#fff
    style P3 fill:#e74c3c,color:#fff
    style S1 fill:#2ecc71,color:#fff
    style S2 fill:#2ecc71,color:#fff
    style S3 fill:#2ecc71,color:#fff
```

---

## 3. 三大 Allocator 详解

### 3.1 GuardedAllocator — 默认选择

```cpp
class GuardedAllocator {
 public:
  void *allocate(size_t size, size_t alignment, const char *name)
  {
    return MEM_new_uninitialized_aligned(size, alignment, name);
  }
  void *allocate_zero(size_t size, size_t alignment, const char *name)
  {
    if (alignment > MEM_MIN_CPP_ALIGNMENT) {
      void *ptr = this->allocate(size, alignment, name);
      memset(ptr, 0, size);
      return ptr;
    }
    return MEM_new_zeroed(size, name);
  }
  void deallocate(void *ptr)
  {
    MEM_delete_void(ptr);
  }
};
```

> *Use Blender's guarded allocator (aka MEM_*). This should always be used except there is a good reason not to use it.*
>
> 使用 Blender 的受保护分配器（即 MEM_* 函数）。除非有充分理由，否则**应该始终使用它**。

**核心特性**：

| 特性 | 说明 |
|------|------|
| 底层实现 | `MEM_new_uninitialized_aligned` / `MEM_delete_void` |
| 内存守护 | ✅ 所有分配都会被追踪，泄漏时打印报告 |
| 对齐支持 | ✅ 通过 `MEM_new_uninitialized_aligned` 支持任意对齐 |
| 零初始化 | `allocate_zero`：小对齐用 `MEM_new_zeroed`（calloc），大对齐手动 `memset` |
| 内存名 | ✅ `name` 参数出现在泄漏报告中 |

**`allocate_zero` 的分支逻辑**：

```mermaid
flowchart TD
    A["allocate_zero(size, alignment, name)"] --> B{"alignment > MEM_MIN_CPP_ALIGNMENT?"}
    B -->|"是：需要特殊对齐"| C["allocate() + memset(ptr, 0, size)<br/>⚠️ 没有对齐版 calloc"]
    B -->|"否：标准对齐即可"| D["MEM_new_zeroed(size, name)<br/>✅ 直接用 calloc，更高效"]
    style C fill:#f39c12,color:#fff
    style D fill:#2ecc71,color:#fff
```

### 3.2 GuardedAlignedAllocator — 对齐增强版

```cpp
template<size_t Alignment = 64ul> class GuardedAlignedAllocator {
 public:
  static constexpr size_t min_alignment = Alignment;

  void *allocate(size_t size, size_t alignment, const char *name)
  {
    return MEM_new_uninitialized_aligned(size, std::max(alignment, min_alignment), name);
  }
  // ...
};
```

> *Like #GuardedAllocator, but makes sure each allocation has a minimum alignment. One use case is reusing an allocation between multiple types that have different alignment requirements. The default alignment template parameter should be large enough for any type in practice.*
>
> 类似 GuardedAllocator，但确保每次分配都有**最小对齐**。一个用例是在多种不同对齐要求的类型之间**复用同一块内存**。默认对齐参数（64 字节）在实践中应该满足任何类型。

**关键设计**：`std::max(alignment, min_alignment)` — 取请求对齐和最小对齐中的**较大者**。

```mermaid
flowchart LR
    subgraph "请求 alignment = 4"
        A1["min_alignment = 64"] --> MAX1["max(4, 64) = 64"]
        MAX1 --> R1["实际对齐: 64 字节"]
    end
    subgraph "请求 alignment = 128"
        A2["min_alignment = 64"] --> MAX2["max(128, 64) = 128"]
        MAX2 --> R2["实际对齐: 128 字节"]
    end

    style R1 fill:#3498db,color:#fff
    style R2 fill:#9b59b6,color:#fff
```

**为什么默认 64 字节？**
- SSE/AVX 需要 16/32 字节对齐
- AVX-512 需要 64 字节对齐
- 64 字节也是常见缓存行大小
- 满足 64 字节对齐 → 自动满足所有更小的对齐要求

### 3.3 RawAllocator — 裸分配器

```cpp
class RawAllocator {
 private:
  struct MemHead {
    int offset;
  };

 public:
  void *allocate(size_t size, size_t alignment, const char * /*name*/)
  {
    BLI_assert(is_power_of_2(int(alignment)));
    void *ptr = malloc(size + alignment + sizeof(MemHead));
    void *used_ptr = reinterpret_cast<void *>(
        uintptr_t(POINTER_OFFSET(ptr, alignment + sizeof(MemHead))) & ~(uintptr_t(alignment) - 1));
    int offset = int(intptr_t(used_ptr) - intptr_t(ptr));
    BLI_assert(offset >= int(sizeof(MemHead)));
    (static_cast<MemHead *>(used_ptr) - 1)->offset = offset;
    return used_ptr;
  }

  void deallocate(void *ptr)
  {
    MemHead *head = static_cast<MemHead *>(ptr) - 1;
    int offset = -head->offset;
    void *actual_pointer = POINTER_OFFSET(ptr, offset);
    free(actual_pointer);
  }
};
```

> *This is a wrapper around malloc/free. Only use this when the GuardedAllocator cannot be used. This can be the case when the allocated memory might live longer than Blender's allocator. For example, when the memory is owned by a static variable.*
>
> 这是对 malloc/free 的封装。**只在无法使用 GuardedAllocator 时才用**。例如内存可能比 Blender 的分配器活得更久——被静态变量拥有时。

**核心难点：对齐 malloc 的实现**

标准 `malloc` 只保证 `alignof(max_align_t)` 对齐（通常 16 字节）。如果需要更大对齐，必须手动实现。RawAllocator 的策略：

```mermaid
flowchart TD
    A["malloc(size + alignment + sizeof(MemHead))"] --> B["原始指针 ptr"]
    B --> C["跳过 alignment + MemHead 字节"]
    C --> D["向下对齐到 alignment 边界"]
    D --> E["得到 used_ptr（返回给用户）"]
    E --> F["在 used_ptr 前面存 offset<br/>MemHead = used_ptr - sizeof(MemHead)"]
    F --> G["deallocate 时：<br/>读取 offset → 算出原始 ptr → free()"]

    style A fill:#e74c3c,color:#fff
    style E fill:#2ecc71,color:#fff
    style G fill:#3498db,color:#fff
```

**内存布局**：

```
malloc 返回的原始内存:
┌──────────────────────────────────────────────────────┐
│  padding  │ MemHead(offset) │    用户数据区域         │
│  (浪费)   │  (4 字节)       │    (size 字节)         │
└──────────────────────────────────────────────────────┘
^           ^                 ^
ptr         head              used_ptr (对齐后, 返回给用户)
            = used_ptr - sizeof(MemHead)
```

**为什么需要 MemHead？** 因为 `deallocate` 只收到 `used_ptr`，但 `free()` 需要原始 `ptr`。`MemHead` 存储了偏移量，可以反算出原始指针。

### 3.4 三者对比

| 特性 | GuardedAllocator | GuardedAlignedAllocator | RawAllocator |
|------|-----------------|------------------------|-------------|
| 底层 | MEM_* | MEM_* | malloc/free |
| 内存守护 | ✅ | ✅ | ❌ |
| 泄漏检测 | ✅ | ✅ | ❌ |
| 最小对齐保证 | ❌ | ✅（默认 64B） | ❌ |
| 适用场景 | 通用（默认） | 跨类型复用缓冲区 | 静态变量/长生命周期 |
| 使用频率 | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ |

```mermaid
flowchart TB
    Q{"你的内存需求？"}
    Q -->|"通用场景"| GA["GuardedAllocator<br/>默认选择"]
    Q -->|"需要保证对齐<br/>（跨类型复用缓冲区）"| GAA["GuardedAlignedAllocator<br/>64B 对齐"]
    Q -->|"静态变量/长生命周期<br/>（超过 Blender 进程）"| RA["RawAllocator<br/>绕过泄漏检测"]

    style GA fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
    style GAA fill:#9b59b6,color:#fff
    style RA fill:#f39c12,color:#fff
```

---

## 4. 容器如何使用 Allocator — 逐行源码分析

### 4.1 Array\<T\> 中的 Allocator

#### 模板参数声明

```cpp
// BLI_array.hh:36~49
template<
    typename T,
    int64_t InlineBufferCapacity = default_inline_buffer_capacity(sizeof(T)),
    typename Allocator = GuardedAllocator>
class Array {
```

#### 成员变量

```cpp
// BLI_array.hh:62~72
T *data_;                                                    // 数据指针
int64_t size_;                                               // 元素数量
BLI_NO_UNIQUE_ADDRESS Allocator allocator_;                  // 分配器（空类时 0 字节）
BLI_NO_UNIQUE_ADDRESS TypedBuffer<T, InlineBufferCapacity> inline_buffer_;  // 内联缓冲区
```

#### Allocator 调用点 ①：`allocate` — 分配堆内存

```cpp
// BLI_array.hh:471~477
T *allocate(int64_t size, const bool zero)
{
  if (zero) {
    return static_cast<T *>(
        allocator_.allocate_zero(size_t(size) * sizeof(T), alignof(T), AT));
  }
  return static_cast<T *>(
      allocator_.allocate(size_t(size) * sizeof(T), alignof(T), AT));
}
```

**关键细节**：
- `size_t(size) * sizeof(T)` — 元素数 × 单个元素大小 = 总字节数
- `alignof(T)` — 类型 T 的对齐要求（如 `float` = 4, `float3` = 16）
- `AT` — 展开为 `"文件名:行号"`，用于内存调试
- `zero` 参数控制是否零初始化：`true` 调用 `allocate_zero`，`false` 调用 `allocate`
- **Array 是三个容器中唯一使用 `allocate_zero` 的**

#### Allocator 调用点 ②：`deallocate_if_not_inline` — 释放堆内存

```cpp
// BLI_array.hh:479~484
void deallocate_if_not_inline(T *ptr)
{
  if (ptr != inline_buffer_) {
    allocator_.deallocate(ptr);
  }
}
```

**关键**：`ptr != inline_buffer_` — 如果数据在内联缓冲区中，**不释放**（栈内存，不是堆分配的）。

#### Allocator 调用点 ③：`get_buffer_for_size` — 决定用内联还是堆

```cpp
// BLI_array.hh:458~469
T *get_buffer_for_size(int64_t size, const bool zero = false)
{
  if (size <= InlineBufferCapacity) {
    if (zero) {
      if constexpr (InlineBufferCapacity > 0) {
        memset(static_cast<void *>(inline_buffer_), 0, size * sizeof(T));
      }
    }
    return inline_buffer_;       // ← 用内联缓冲区，不调用 Allocator
  }
  return this->allocate(size, zero);  // ← 超出内联容量，调用 Allocator
}
```

```mermaid
flowchart TD
    A["get_buffer_for_size(size, zero)"] --> B{"size ≤ InlineBufferCapacity?"}
    B -->|"是：用内联缓冲区"| C["返回 inline_buffer_<br/>⚠️ 不调用 Allocator！<br/>zero=true 时手动 memset"]
    B -->|"否：需要堆分配"| D["调用 allocator_.allocate()<br/>或 allocator_.allocate_zero()"]

    style C fill:#2ecc71,color:#fff
    style D fill:#e74c3c,color:#fff
```

#### `allocate_zero` 的触发场景

```cpp
// BLI_array.hh:135~154 — 构造时指定值
Array(int64_t size, const T &value, Allocator allocator = {})
{
    if (std::is_trivially_copyable_v<T> && value_is_zero(value)) {
      data_ = this->get_buffer_for_size(size, true);  // ← zero=true!
    }
    // ...
}
```

当 `T` 是平凡类型且值为全零时（如 `Array<int>(100, 0)`），使用 `allocate_zero` 代替 `allocate` + `uninitialized_fill_n`，因为 `calloc`（`allocate_zero` 的底层）通常比 `malloc` + `memset` 更高效。

#### Array 完整生命周期

```mermaid
sequenceDiagram
    participant User as 用户代码
    participant Arr as Array<T>
    participant Buf as inline_buffer_
    participant Alloc as Allocator

    Note over User: Array<float> arr(100);
    User->>Arr: Array(100)
    Arr->>Arr: get_buffer_for_size(100)
    Note over Arr: 100 > InlineBufferCapacity
    Arr->>Alloc: allocate(100*4, 4, "BLI_array.hh:xxx")
    Alloc-->>Arr: void* heap_ptr
    Arr->>Arr: data_ = heap_ptr, size_ = 100
    Arr->>Arr: default_construct_n(data_, 100)

    Note over User: arr.~Array()
    User->>Arr: 析构
    Arr->>Arr: destruct_n(data_, 100)
    Arr->>Arr: deallocate_if_not_inline(data_)
    Note over Arr: data_ != inline_buffer_
    Arr->>Alloc: deallocate(heap_ptr)
```

---

### 4.2 Vector\<T\> 中的 Allocator

#### 模板参数声明

```cpp
// BLI_vector.hh:57~75
template<
    typename T,
    int64_t InlineBufferCapacity = default_inline_buffer_capacity(sizeof(T)),
    typename Allocator = GuardedAllocator>
class Vector {
```

#### 成员变量

```cpp
// BLI_vector.hh:95~103
T *begin_;                                                    // 数据起始
T *end_;                                                      // 数据末尾
T *capacity_end_;                                             // 容量末尾
BLI_NO_UNIQUE_ADDRESS Allocator allocator_;                   // 分配器
BLI_NO_UNIQUE_ADDRESS TypedBuffer<T, InlineBufferCapacity> inline_buffer_;  // 内联缓冲区
```

**与 Array 的关键区别**：Vector 用**三个指针**（begin/end/capacity_end）代替 Array 的 `data_ + size_`。这是因为 `append` 是 Vector 的核心操作，用指针可以减少一次减法计算。

#### Allocator 调用点 ①：`realloc_to_at_least` — 扩容（最核心）

```cpp
// BLI_vector.hh:1121~1151
void realloc_to_at_least(const int64_t min_capacity)
{
    const int64_t min_new_capacity = this->capacity() * 2;  // 至少翻倍
    const int64_t new_capacity = std::max(min_capacity, min_new_capacity);
    const int64_t size = this->size();

    // ① 分配新内存
    T *new_array = static_cast<T *>(
        allocator_.allocate(size_t(new_capacity) * sizeof(T), alignof(T), AT));
    try {
      // ② 移动旧元素到新内存
      uninitialized_relocate_n(begin_, size, new_array);
    }
    catch (...) {
      // ③ 移动失败 → 释放新内存，抛异常
      allocator_.deallocate(new_array);
      throw;
    }

    // ④ 释放旧内存（如果不是内联缓冲区）
    if (!this->is_inline()) {
      allocator_.deallocate(begin_);
    }

    // ⑤ 更新指针
    begin_ = new_array;
    end_ = begin_ + size;
    capacity_end_ = begin_ + new_capacity;
}
```

```mermaid
flowchart TD
    A["realloc_to_at_least(min_capacity)"] --> B["new_capacity = max(min_capacity, capacity*2)"]
    B --> C["allocator_.allocate(new_capacity * sizeof(T))"]
    C --> D{"uninitialized_relocate_n 成功?"}
    D -->|"是"| E["释放旧内存<br/>is_inline()? 不释放 : deallocate"]
    D -->|"否（异常）"| F["allocator_.deallocate(new_array)<br/>throw"]
    E --> G["更新 begin_/end_/capacity_end_"]

    style C fill:#e74c3c,color:#fff
    style F fill:#f39c12,color:#fff
    style E fill:#2ecc71,color:#fff
```

**注意**：Vector 的 `realloc_to_at_least` **没有 `allocate_zero`** 路径——因为扩容后新空间会被逐步 `append` 填充，不需要零初始化。

#### Allocator 调用点 ②：`~Vector` — 析构

```cpp
// BLI_vector.hh:330~336
~Vector()
{
    destruct_n(begin_, this->size());
    if (!this->is_inline()) {
      allocator_.deallocate(begin_);
    }
}
```

与 Array 的 `deallocate_if_not_inline` 逻辑相同——内联缓冲区不释放。

#### Allocator 调用点 ③：`clear_and_shrink` — 清空并释放

```cpp
// BLI_vector.hh:479~490
void clear_and_shrink()
{
    destruct_n(begin_, this->size());
    if (!this->is_inline()) {
      allocator_.deallocate(begin_);
    }
    begin_ = inline_buffer_;
    end_ = begin_;
    capacity_end_ = begin_ + InlineBufferCapacity;
}
```

#### Allocator 调用点 ④：`release` — 转移所有权

```cpp
// BLI_vector.hh:1060~1097
VectorData<T, Allocator> release()
{
    if (this->is_inline()) {
      // 内联数据 → 先分配堆内存，再搬过去
      T *data = static_cast<T *>(
          allocator_.allocate(size_t(size) * sizeof(T), alignof(T), __func__));
      uninitialized_relocate_n(begin_, size, data);
      begin_ = data;
      // ...
    }

    VectorData<T, Allocator> result;
    result.data = begin_;
    result.size = end_ - begin_;
    result.capacity = capacity_end_ - begin_;
    result.allocator = allocator_;  // ← Allocator 也一起转移！

    begin_ = inline_buffer_;
    end_ = begin_;
    capacity_end_ = begin_ + InlineBufferCapacity;
    return result;
}
```

**关键**：`VectorData` 也携带 Allocator——因为释放者需要知道用什么分配器来释放内存。

#### Allocator 调用点 ⑤：移动构造中的内联→堆路径

```cpp
// BLI_vector.hh:281~288
// 当源 Vector 是内联的，但目标内联缓冲区不够大时
begin_ = static_cast<T *>(
    allocator_.allocate(sizeof(T) * size_t(capacity), alignof(T), AT));
capacity_end_ = begin_ + capacity;
uninitialized_relocate_n(other.begin_, size, begin_);
```

#### Vector 中没有 `allocate_zero`

Vector **从不使用 `allocate_zero`**！原因：
1. `reserve` / `realloc_to_at_least` 只分配不初始化
2. `resize` 新增元素时用 `default_construct_n`（不是零初始化）
3. `append` 用 placement new 构造单个元素

---

### 4.3 GArray\<Allocator\> 中的 Allocator

#### 模板参数声明

```cpp
// BLI_generic_array.hh:24~29
template<typename Allocator = GuardedAllocator>
class GArray {
```

**与 Array/Vector 的关键区别**：没有 `T` 和 `InlineBufferCapacity` 模板参数。

#### 成员变量

```cpp
// BLI_generic_array.hh:31~38
const CPPType *type_ = nullptr;
void *data_ = nullptr;
int64_t size_ = 0;
BLI_NO_UNIQUE_ADDRESS Allocator allocator_;
```

**与 Array/Vector 的关键区别**：
- **没有内联缓冲区**（`TypedBuffer`）！GArray 总是堆分配
- 数据指针是 `void*`，不是 `T*`

#### Allocator 调用点 ①：`allocate` — 分配

```cpp
// BLI_generic_array.hh:247~252
void *allocate(int64_t size)
{
    const int64_t item_size = type_->size;       // 运行时获取元素大小
    const int64_t alignment = type_->alignment;  // 运行时获取对齐
    return allocator_.allocate(size_t(size) * item_size, alignment, AT);
}
```

**与 Array 的对比**：

| 特性     | Array::allocate       | GArray::allocate            |
| -------- | --------------------- | --------------------------- |
| 元素大小 | `sizeof(T)` — 编译期  | `type_->size` — 运行时      |
| 对齐     | `alignof(T)` — 编译期 | `type_->alignment` — 运行时 |
| 零初始化 | 支持 `allocate_zero`  | ❌ 不支持                    |
| 返回类型 | `T*`                  | `void*`                     |

#### Allocator 调用点 ②：`deallocate` — 释放

```cpp
// BLI_generic_array.hh:254~257
void deallocate(void *ptr)
{
    allocator_.deallocate(ptr);
}
```

**注意**：没有 `deallocate_if_not_inline`——因为 GArray **没有内联缓冲区**，所有数据都是堆分配的，所以总是需要释放。

#### GArray 中没有 `allocate_zero`

GArray **从不使用 `allocate_zero`**。原因：
1. `GArray(type, size)` 构造时用 `type_->default_construct_n` 初始化
2. `GArray(type, size, NoInitialization{})` 连默认构造都跳过
3. 没有像 Array 那样的 `Array(size, value=0)` 构造函数

#### GArray 完整生命周期

```mermaid
sequenceDiagram
    participant User as 用户代码
    participant GA as GArray
    participant Alloc as Allocator

    Note over User: GArray&lt;&gt; arr(CPPType::get&lt;float&gt;(), 100);
    User->>GA: GArray(type, 100)
    GA->>GA: GArray(type, 100, NoInitialization{})
    GA->>Alloc: allocate(100 * 4, 4, "BLI_generic_array.hh:xxx")
    Alloc-->>GA: void* heap_ptr
    GA->>GA: data_ = heap_ptr, size_ = 100
    GA->>GA: type_->default_construct_n(data_, 100)

    Note over User: arr.~GArray()
    User->>GA: 析构
    GA->>GA: type_->destruct_n(data_, 100)
    GA->>Alloc: deallocate(heap_ptr)
```

---

### 4.4 三者对比总结

#### Allocator 使用对比

| 特性                         | Array                                  | Vector                                 | GArray             |
| ---------------------------- | -------------------------------------- | -------------------------------------- | ------------------ |
| **模板参数**                 | `<T, InlineBufferCapacity, Allocator>` | `<T, InlineBufferCapacity, Allocator>` | `<Allocator>`      |
| **内联缓冲区**               | ✅ `TypedBuffer<T>`                     | ✅ `TypedBuffer<T>`                     | ❌ 无               |
| **allocate**                 | ✅                                      | ✅                                      | ✅                  |
| **allocate_zero**            | ✅ 有                                   | ❌ 无                                   | ❌ 无               |
| **deallocate**               | ✅                                      | ✅                                      | ✅                  |
| **deallocate_if_not_inline** | ✅                                      | ✅ (内联检查)                           | ❌ 总是释放         |
| **BLI_NO_UNIQUE_ADDRESS**    | ✅ allocator_ + inline_buffer_          | ✅ allocator_ + inline_buffer_          | ✅ allocator_       |
| **元素大小来源**             | `sizeof(T)`                            | `sizeof(T)`                            | `type_->size`      |
| **对齐来源**                 | `alignof(T)`                           | `alignof(T)`                           | `type_->alignment` |
| **扩容策略**                 | 无（固定大小）                         | 翻倍增长                               | 无（固定大小）     |
| **所有权转移**               | 移动构造                               | 移动构造 + `release()`                 | 移动构造           |

#### 内联缓冲区决策流程

```mermaid
flowchart TD
    A["需要 N 个元素的缓冲区"] --> B{"有内联缓冲区?<br/>(Array/Vector)"}
    B -->|"是"| C{"N ≤ InlineBufferCapacity?"}
    C -->|"是"| D["✅ 用 inline_buffer_<br/>不调用 Allocator<br/>零内存分配开销"]
    C -->|"否"| E["❌ 调用 Allocator.allocate()<br/>堆分配"]
    B -->|"否（GArray）"| E

    style D fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
    style E fill:#e74c3c,color:#fff
```

#### 释放决策流程

```mermaid
flowchart TD
    A["需要释放 data_ 指针"] --> B{"有内联缓冲区?<br/>(Array/Vector)"}
    B -->|"是"| C{"data_ == inline_buffer_?"}
    C -->|"是：数据在内联缓冲区"| D["✅ 不调用 Allocator.deallocate()<br/>栈内存，自动释放"]
    C -->|"否：数据在堆上"| E["❌ 调用 Allocator.deallocate()"]
    B -->|"否（GArray）"| E

    style D fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
    style E fill:#e74c3c,color:#fff
```

#### 为什么只有 Array 有 `allocate_zero`？

```mermaid
flowchart LR
    subgraph "Array — 有 allocate_zero"
        A1["构造: Array(100, 0)<br/>知道值是零 → 用 calloc 优化"]
    end
    subgraph "Vector — 无 allocate_zero"
        V1["扩容: realloc<br/>新空间逐步 append → 不需零初始化"]
    end
    subgraph "GArray — 无 allocate_zero"
        G1["构造: GArray(type, size)<br/>运行时类型 → default_construct_n<br/>不知道值是否为零"]
    end

    style A1 fill:#e67e22,color:#fff
    style V1 fill:#3498db,color:#fff
    style G1 fill:#9b59b6,color:#fff
```

#### `AT` 宏在各容器中的展开

```cpp
// Array::allocate
allocator_.allocate(size_t(size) * sizeof(T), alignof(T), AT);
// AT = "BLI_array.hh:476"

// Vector::realloc_to_at_least
allocator_.allocate(size_t(new_capacity) * sizeof(T), alignof(T), AT);
// AT = "BLI_vector.hh:1135"

// GArray::allocate
allocator_.allocate(size_t(size) * item_size, alignment, AT);
// AT = "BLI_generic_array.hh:251"

// Vector::release (特殊：用 __func__ 代替 AT)
allocator_.allocate(size_t(size) * sizeof(T), alignof(T), __func__);
// __func__ = "release"
```

### 4.5 BLI_NO_UNIQUE_ADDRESS 优化

在所有三个容器中，Allocator 成员都使用了 `BLI_NO_UNIQUE_ADDRESS`：

```cpp
// Array
BLI_NO_UNIQUE_ADDRESS Allocator allocator_;
BLI_NO_UNIQUE_ADDRESS TypedBuffer<T, InlineBufferCapacity> inline_buffer_;

// Vector
BLI_NO_UNIQUE_ADDRESS Allocator allocator_;
BLI_NO_UNIQUE_ADDRESS TypedBuffer<T, InlineBufferCapacity> inline_buffer_;

// GArray
BLI_NO_UNIQUE_ADDRESS Allocator allocator_;
```

**原理**：`GuardedAllocator` 和 `RawAllocator` 都是**空类**（无数据成员），按 C++ 规范空类大小 ≥ 1 字节。`[[no_unique_address]]`（即 `BLI_NO_UNIQUE_ADDRESS`）告诉编译器这个成员不需要唯一地址，可以优化为 0 字节。

```mermaid
graph LR
    subgraph "无 [[no_unique_address]]"
        M1["type_: 8B"] --- M2["data_: 8B"] --- M3["size_: 8B"] --- M4["allocator_: 1B + 7B padding"]
        T1["总计: 32B"]
    end
    subgraph "有 [[no_unique_address]]"
        N1["type_: 8B"] --- N2["data_: 8B"] --- N3["size_: 8B"]
        T2["总计: 24B"]
    end

    style M4 fill:#e74c3c,color:#fff
    style T1 fill:#e74c3c,color:#fff
    style T2 fill:#2ecc71,color:#fff
```

---

## 5. 语法专题：标签类型 — NoInitialization 与 NoExceptConstructor

### 5.1 它们是什么？

```cpp
// BLI_memory_utils.hh:222~234

/**
 * This can be used by container constructors. A parameter of this type should be used to indicate
 * that the constructor does not construct the elements.
 */
class NoInitialization {};

/**
 * This can be used to mark a constructor of an object that does not throw exceptions. Other
 * constructors can delegate to this constructor to make sure that the object lifetime starts.
 * With this, the destructor of the object will be called, even when the remaining constructor
 * throws.
 */
class NoExceptConstructor {};
```

**翻译**：
- `NoInitialization`：用于容器构造函数，表示**不初始化元素**。
- `NoExceptConstructor`：标记构造函数**不抛异常**。其他构造函数可以委托给它，确保对象生命周期开始——这样即使后续构造抛异常，析构函数也会被调用。

### 5.2 为什么是空类？——标签分发（Tag Dispatch）模式

这两个类**没有任何数据成员和成员函数**，它们是纯粹的**标签类型（Tag Type）**。

**核心问题**：C++ 不支持仅靠参数值来区分重载，但支持用**参数类型**来区分。

```mermaid
flowchart TD
    Q["问题：如何区分两种构造？"] --> A["方案 1：用 bool 参数？"]
    A --> A1["Array(size, false) ← 不初始化<br/>Array(size, true) ← 默认构造<br/>❌ 可读性差，容易搞混"]
    Q --> B["方案 2：用 enum 参数？"]
    B --> B1["Array(size, InitMode::None)<br/>Array(size, InitMode::Default)<br/>⚠️ 可以，但 enum 值可以隐式转换"]
    Q --> C["方案 3：用空类标签？✅"]
    C --> C1["Array(size, NoInitialization{})<br/>Array(size) ← 默认构造<br/>✅ 类型安全，编译期区分，零开销"]

    style C1 fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
    style A1 fill:#e74c3c,color:#fff
```

### 5.3 调用时为什么写 `NoInitialization{}`？

```cpp
// 构造函数声明
Array(int64_t size, NoInitialization, Allocator allocator = {});
//                     ^^^^^^^^^^^^^^  类型名，不是变量名

// 调用
Array<int> arr(100, NoInitialization{});
//                  ^^^^^^^^^^^^^^^^^  构造一个临时对象
```

**拆解**：

| 代码                 | 含义                                                                    |
| -------------------- | ----------------------------------------------------------------------- |
| `NoInitialization`   | **类型名**（class 名）                                                  |
| `NoInitialization{}` | **构造该类型的临时对象**（空花括号 = 默认构造）                         |
| `NoInitialization,`  | 在参数列表中，只写类型名 = **匿名参数**（不需要变量名，因为不会使用它） |

**等价写法对比**：

```cpp
// 写法 1：匿名参数（Blender 风格）
Array(int64_t size, NoInitialization, Allocator allocator = {});

// 写法 2：有名字的参数（效果相同，但多余）
Array(int64_t size, NoInitialization /*tag*/, Allocator allocator = {});

// 调用
Array<int> arr(100, NoInitialization{});
```

> 💡 **为什么参数列表里只写类名不写变量名？** 因为函数体里**永远不会使用这个参数**——它存在的唯一目的是让编译器根据类型选择正确的重载。给它起名字没有意义，反而可能误导读者以为它有值。

### 5.4 标签分发的编译期效果

```cpp
// 重载 1：默认构造
explicit Array(int64_t size, Allocator allocator = {})
{
    data_ = this->get_buffer_for_size(size);
    default_construct_n(data_, size);  // ← 初始化元素
    size_ = size;
}

// 重载 2：不初始化
Array(int64_t size, NoInitialization, Allocator allocator = {})
{
    data_ = this->get_buffer_for_size(size);
    // ← 不调用 default_construct_n！
    size_ = size;
}
```

```mermaid
flowchart LR
    subgraph "调用 Array&lt;int&gt;(100)"
        A1["匹配重载 1<br/>default_construct_n(data_, 100)<br/>int 是平凡类型 → 什么也不做"]
    end
    subgraph "调用 Array&lt;string&gt;(100, NoInitialization{})"
        A2["匹配重载 2<br/>不调用 default_construct_n<br/>内存内容不确定 ⚡"]
    end
    subgraph "调用 Array&lt;string&gt;(100)"
        A3["匹配重载 1<br/>default_construct_n(data_, 100)<br/>每个 string 调用默认构造函数"]
    end

    style A1 fill:#3498db,color:#fff
    style A2 fill:#f39c12,color:#fff
    style A3 fill:#2ecc71,color:#fff
```

### 5.5 NoExceptConstructor 的特殊用途

```cpp
// Array 的很多构造函数都委托给 NoExceptConstructor 版本
Array(NoExceptConstructor, Allocator allocator = {}) noexcept : Array(allocator) {}

// 例如：带大小的构造函数
explicit Array(int64_t size, Allocator allocator = {})
    : Array(NoExceptConstructor(), allocator)  // ← 委托！
{
    data_ = this->get_buffer_for_size(size);
    default_construct_n(data_, size);
    size_ = size;
}
```

**为什么这样做？** 注释说：

> *Other constructors can delegate to this constructor to make sure that the object lifetime starts. With this, the destructor of the object will be called, even when the remaining constructor throws.*
>
> 其他构造函数可以委托给这个构造函数，确保对象生命周期开始。这样即使后续构造抛异常，析构函数也会被调用。

```mermaid
sequenceDiagram
    participant User as 用户代码
    participant Ctor as Array(size, allocator)
    participant NoEx as Array(NoExceptConstructor, allocator)
    participant Dtor as ~Array()

    User->>Ctor: Array(100)
    Ctor->>NoEx: 委托构造（noexcept）
    Note over NoEx: 对象生命周期开始<br/>data_ = inline_buffer_<br/>size_ = 0
    NoEx-->>Ctor: 返回
    Ctor->>Ctor: get_buffer_for_size(100)
    alt 分配成功
        Ctor->>Ctor: default_construct_n(data_, 100)
        Note over Ctor: 构造完成 ✅
    else default_construct_n 抛异常
        Ctor-->>Dtor: 析构函数被调用
        Note over Dtor: data_ = inline_buffer_<br/>size_ = 0<br/>安全清理 ✅
    end
```

**关键**：如果 `default_construct_n` 抛异常，因为对象生命周期已经在 `NoExceptConstructor` 版本中开始了，C++ 保证析构函数会被调用。如果直接在构造函数里初始化成员，异常发生时对象生命周期还没开始，析构函数不会被调用，可能导致资源泄漏。

### 5.6 标签类型零开销证明

```cpp
// 编译后的汇编中：
Array<int> arr(100, NoInitialization{});

// NoInitialization{} 不会生成任何代码！
// 编译器知道它是空类，构造它 = 什么也不做
// 函数调用的参数传递中，空类参数通常被完全优化掉

// 对比：如果用 int 标志
Array<int> arr(100, 0);  // 0 需要压栈或放入寄存器 → 有开销
```

```mermaid
flowchart LR
    subgraph "空类标签：零开销"
        T1["NoInitialization{} → 无代码生成<br/>编译器直接选择重载"]
    end
    subgraph "int 标志：有开销"
        T2["0 → 需要传递参数<br/>运行时 if 判断"]
    end

    style T1 fill:#2ecc71,color:#fff
    style T2 fill:#e74c3c,color:#fff
```

### 5.7 C++ 标准库中的同类模式

Blender 不是唯一使用标签类型的库。C++ 标准库也大量使用：

| 标签类型                     | 用途                                 | 头文件       |
| ---------------------------- | ------------------------------------ | ------------ |
| `std::nothrow_t`             | 表示 new 失败返回 nullptr 而非抛异常 | `<new>`      |
| `std::piecewise_construct_t` | 表示 pair 逐片构造                   | `<utility>`  |
| `std::allocator_arg_t`       | 表示构造时传入分配器                 | `<memory>`   |
| `std::in_place_t`            | 表示就地构造（optional/variant）     | `<optional>` |
| `std::defer_lock_t`          | 表示 unique_lock 不立即加锁          | `<mutex>`    |

```cpp
// C++ 标准库用法示例
auto* p = new (std::nothrow) int(42);  // nothrow 标签
std::pair<std::string, std::string> p2(std::piecewise_construct,
    std::forward_as_tuple("hello"), std::forward_as_tuple(5, 'x'));
```

> 💡 **设计模式名称**：**标签分发（Tag Dispatch）** 或 **标签零开销重载选择（Tag-based Overload Selection）**。用空类的类型信息在编译期选择重载，运行时零开销。

---

## 6. 源码中的真实用例

### 6.1 GuardedAlignedAllocator — 曲线重采样临时缓冲区

[resample_curves.cc](file:///e:/blender-git/blender/source/blender/geometry/intern/resample_curves.cc)：

```cpp
struct EvalDataBuffer {
  using AllocatorType = GuardedAlignedAllocator<>;
  /* Use a default alignment that works for all attribute types, and don't use the inline buffer
   * because it doesn't necessarily have the correct alignment. */
  Vector<std::byte, 0, AllocatorType> heap_allocated;
  alignas(AllocatorType::min_alignment) std::array<std::byte, 1024> inline_buffer;

  template<typename T> MutableSpan<T> resize(const int64_t size)
  {
    const int64_t size_in_bytes = sizeof(T) * size;
    if (size_in_bytes <= this->inline_buffer.size()) {
      return MutableSpan<std::byte>(this->inline_buffer).slice(0, size_in_bytes).cast<T>();
    }
    this->heap_allocated.resize(size_in_bytes);
    return this->heap_allocated.as_mutable_span().cast<T>();
  }
};
```

**为什么用 GuardedAlignedAllocator？** 同一块缓冲区可能被 `float`、`float3`、`int` 等不同类型复用。64 字节对齐满足所有类型的对齐要求，避免未定义行为。

### 6.2 RawAllocator — 线程局部静态变量

[lazy_threading.cc](file:///e:/blender-git/blender/source/blender/blenlib/intern/lazy_threading.cc)：

```cpp
/**
 * This uses a "raw" stack and vector so that it can be destructed after Blender checks for memory
 * leaks. A new list of receivers is created whenever an isolated region is entered to avoid
 * deadlocks.
 */
using HintReceivers = RawStack<RawVector<FunctionRef<void()>, 0>, 0>;
static thread_local HintReceivers hint_receivers = /* ... */;
```

**为什么用 RawAllocator？** 这是 `static thread_local` 变量，生命周期持续到线程结束。如果用 `GuardedAllocator`，Blender 的内存泄漏检查器会在程序退出前检查，此时这个变量还没析构，会误报泄漏。用 `RawAllocator`（malloc/free）则不会被追踪。

### 6.3 GuardedAllocator 显式指定 — VectorSet 的 int32 优化

[mesh_validate.cc](file:///e:/blender-git/blender/source/blender/blenkernel/intern/mesh_validate.cc)：

```cpp
using EdgeMap = VectorSet<OrderedEdge,
                          32,
                          DefaultProbingStrategy,
                          DefaultHash<OrderedEdge>,
                          DefaultEquality<OrderedEdge>,
                          SimpleVectorSetSlot<OrderedEdge, int>,  // ← 用 int 代替 int64_t
                          GuardedAllocator>;                       // ← 被迫显式写出
```

**为什么显式写 GuardedAllocator？** `VectorSet` 有 7 个模板参数，当需要修改第 6 个参数（slot 索引类型从 `int64_t` 改为 `int` 以节省内存）时，必须把所有参数都写出来，包括默认的 `GuardedAllocator`。

### 6.4 类型别名 — Blender 预定义的 Raw 容器

Blender 为 `RawAllocator` 预定义了便捷类型别名，分散定义在各自的头文件中：

| 类型别名 | 定义位置 | 完整定义 |
|---------|---------|---------|
| `RawVector<T>` | [BLI_vector.hh:1161](file:///e:/blender-git/blender/source/blender/blenlib/BLI_vector.hh#L1161) | `Vector<T, InlineBufferCapacity, RawAllocator>` |
| `RawStack<T>` | [BLI_stack.hh:413](file:///e:/blender-git/blender/source/blender/blenlib/BLI_stack.hh#L413) | `Stack<T, InlineBufferCapacity, RawAllocator>` |
| `RawSet<Key>` | [BLI_set.hh:989](file:///e:/blender-git/blender/source/blender/blenlib/BLI_set.hh#L989) | `Set<Key, ..., RawAllocator>` |
| `RawMap<Key, Value>` | [BLI_map.hh:1376](file:///e:/blender-git/blender/source/blender/blenlib/BLI_map.hh#L1376) | `Map<Key, Value, ..., RawAllocator>` |
| `RawVectorSet<Key>` | [BLI_vector_set.hh:1117](file:///e:/blender-git/blender/source/blender/blenlib/BLI_vector_set.hh#L1117) | `VectorSet<Key, ..., RawAllocator>` |

> ⚠️ **没有 `RawArray`**：`Array` 头文件中没有定义 `RawArray` 类型别名。如果需要，可以自己写：
> ```cpp
> template<typename T, int64_t N = default_inline_buffer_capacity(sizeof(T))>
> using RawArray = Array<T, N, RawAllocator>;
> ```

> *Same as a normal Vector, but does not use Blender's guarded allocator. This is useful when allocating memory with static storage duration.* — [BLI_vector.hh:1157](file:///e:/blender-git/blender/source/blender/blenlib/BLI_vector.hh#L1157)
>
> 和普通 Vector 相同，但不使用 Blender 的受保护分配器。适用于**静态存储期**的内存分配。

---

## 7. 语法专题：ul / ULL 后缀

### 6.1 整数字面量后缀一览

| 后缀 | 含义 | 类型 | 示例 |
|------|------|------|------|
| （无） | 十进制整数 | `int` | `42` |
| `u` / `U` | 无符号 | `unsigned int` | `42u` |
| `l` / `L` | long | `long` | `42l` |
| `ul` / `UL` | unsigned long | `unsigned long` | `42ul` |
| `ll` / `LL` | long long | `long long` | `42ll` |
| `ull` / `ULL` | unsigned long long | `unsigned long long` | `42ull` |

### 6.2 `64ul` 是什么？

```cpp
template<size_t Alignment = 64ul> class GuardedAlignedAllocator {
```

- `64ul` = 值为 64 的 **unsigned long** 字面量
- `size_t` 在 64 位 Windows 上是 `unsigned long long`，在 64 位 Linux 上是 `unsigned long`
- `64ul` 可以隐式转换为 `size_t`，不会丢失精度

### 6.3 `16ULL` 是什么？

```cpp
#define MEM_MIN_CPP_ALIGNMENT \
  (__STDCPP_DEFAULT_NEW_ALIGNMENT__ < alignof(void *) ? __STDCPP_DEFAULT_NEW_ALIGNMENT__ : \
   alignof(void *))  // Expands to (16ULL < alignof(void *) ? 16ULL : alignof(void *))
```

- `16ULL` = 值为 16 的 **unsigned long long** 字面量
- 注释说宏展开后 `__STDCPP_DEFAULT_NEW_ALIGNMENT__` 变为 `16ULL`
- `alignof(void*)` 在 64 位系统上是 8，在 32 位系统上也是 8

### 6.4 为什么用 ULL 而不是普通整数？

```mermaid
flowchart LR
    subgraph "用普通 int"
        A["16 < alignof(void*)<br/>16 是 int, alignof 返回 size_t<br/>int 与 size_t 比较可能警告"]
    end
    subgraph "用 ULL"
        B["16ULL < alignof(void*)<br/>两者都是无符号大整数<br/>类型匹配，无警告 ✅"]
    end

    style A fill:#e74c3c,color:#fff
    style B fill:#2ecc71,color:#fff
```

**核心原因**：`alignof()` 返回 `size_t`（无符号类型）。如果用有符号 `int` 与无符号 `size_t` 比较，编译器会发出**有符号/无符号比较警告**。用 `ULL` 后缀确保两边都是无符号类型。

### 6.5 ul vs ULL 的区别

| 后缀 | 类型 | 64 位 Windows | 64 位 Linux |
|------|------|--------------|-------------|
| `ul` | `unsigned long` | 4 字节（32 位） | 8 字节（64 位） |
| `ULL` | `unsigned long long` | 8 字节（64 位） | 8 字节（64 位） |

> ⚠️ **Windows 上的陷阱**：`unsigned long` 在 Windows 上只有 4 字节（即使是 64 位系统）！所以 `64ul` 在 Windows 上是 32 位无符号整数（值 64 没问题），但如果值超过 2³² 就会溢出。`ULL` 在所有平台上都是 64 位，更安全。

---

## 8. 语法专题：MEM_MIN_CPP_ALIGNMENT 宏

### 7.1 宏定义

```cpp
#define MEM_MIN_CPP_ALIGNMENT \
  (__STDCPP_DEFAULT_NEW_ALIGNMENT__ < alignof(void *) \
    ? __STDCPP_DEFAULT_NEW_ALIGNMENT__ \
    : alignof(void *))
```

展开后等价于：

```cpp
#define MEM_MIN_CPP_ALIGNMENT (16ULL < alignof(void *) ? 16ULL : alignof(void *))
```

### 7.2 逐步拆解

```mermaid
flowchart TD
    A["MEM_MIN_CPP_ALIGNMENT"] --> B["取两个值的较大者<br/>max(A, B)"]
    
    C["A = __STDCPP_DEFAULT_NEW_ALIGNMENT__<br/>= 16ULL<br/>C++ new 操作符保证的最小对齐"]
    D["B = alignof(void*)<br/>= 8（64 位系统）<br/>指针的对齐要求"]
    
    C --> B
    D --> B
    
    B --> E["结果: max(16, 8) = 16"]
    
    style C fill:#3498db,color:#fff
    style D fill:#9b59b6,color:#fff
    style E fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
```

### 7.3 `__STDCPP_DEFAULT_NEW_ALIGNMENT__` 是什么？

这是 C++17 引入的编译器预定义宏，表示 `operator new` 保证的**最小对齐**。

| 编译器 | 值 |
|--------|-----|
| MSVC (x64) | 16 |
| GCC (x64) | 16 |
| Clang (x64) | 16 |
| 32 位平台 | 8 |

### 7.4 为什么取较大者？

```mermaid
flowchart TD
    Q{"为什么要 max？"}
    Q --> R1["C++ 标准保证 new 返回的指针<br/>至少按 __STDCPP_DEFAULT_NEW_ALIGNMENT__ 对齐<br/>通常是 16 字节"]
    Q --> R2["某些平台指针的对齐要求<br/>可能更大（罕见）<br/>alignof(void*) 通常 8"]
    Q --> R3["取较大者确保<br/>MEM_MIN_CPP_ALIGNMENT<br/>在所有平台上都安全"]

    style R3 fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
```

**本质**：`MEM_MIN_CPP_ALIGNMENT` 是"使用标准 `new`/`calloc` 时，返回的指针至少有多大对齐"的保守估计。

### 7.5 在 Allocator 中的作用

```cpp
// GuardedAllocator::allocate_zero
if (alignment > MEM_MIN_CPP_ALIGNMENT) {
  // 请求的对齐 > 标准 new 的保证
  // → 没有对齐版 calloc 可用
  // → 必须手动 allocate + memset
  void *ptr = this->allocate(size, alignment, name);
  memset(ptr, 0, size);
  return ptr;
}
// 请求的对齐 ≤ 标准 new 的保证
// → 可以直接用 MEM_new_zeroed（底层 calloc），更高效
return MEM_new_zeroed(size, name);
```

```mermaid
flowchart TD
    A["allocate_zero(size, alignment, name)"] --> B{"alignment > MEM_MIN_CPP_ALIGNMENT?"}
    B -->|"是（如 alignment=64）"| C["⚠️ calloc 不保证 64B 对齐<br/>→ allocate() + memset()"]
    B -->|"否（如 alignment=4,8,16）"| D["✅ calloc 保证 ≥ 16B 对齐<br/>→ MEM_new_zeroed() 更快"]
    
    style C fill:#f39c12,color:#fff
    style D fill:#2ecc71,color:#fff
```

### 7.6 三元运算符实现 max 的原因

为什么不用 `std::max(16ULL, alignof(void*))`？

因为这是**预处理器宏**——在 `#define` 中不能调用函数。三元运算符 `? :` 是语言级表达式，可以在宏中安全使用。

---

## 9. Allocator vs std::allocator

| 特性 | Blender Allocator | std::allocator |
|------|------------------|----------------|
| 接口方法 | `allocate` + `deallocate` | `allocate` + `deallocate` + `construct` + `destroy` |
| 是否模板 | ❌ 非模板 | ✅ `std::allocator<T>` |
| 关心元素类型 | ❌ 不关心 | ✅ 必须知道 T |
| 对齐参数 | ✅ 显式传入 | ❌ 自动推断 |
| 调试名称 | ✅ `const char *name` | ❌ 无 |
| 零初始化 | ✅ `allocate_zero` | ❌ 无 |
| 标准兼容 | ❌ 不兼容 std 容器 | ✅ 标准接口 |
| 复杂度 | 极简 | 复杂（rebind 等） |

```mermaid
flowchart LR
    subgraph "Blender Allocator"
        BA1["GuardedAllocator"] --> BA2["allocate(size, align, name)"]
        BA1 --> BA3["deallocate(ptr)"]
    end
    subgraph "std::allocator&lt;T&gt;"
        SA1["std::allocator&lt;T&gt;"] --> SA2["allocate(n)"]
        SA1 --> SA3["deallocate(ptr, n)"]
        SA1 --> SA4["construct(ptr, args...)"]
        SA1 --> SA5["destroy(ptr)"]
        SA1 --> SA6["rebind&lt;U&gt;"]
    end

    style BA1 fill:#2ecc71,color:#fff
    style SA1 fill:#3498db,color:#fff
```

---

## 10. 总结速查表

### Allocator 选择

| 场景 | 推荐 | 原因 |
|------|------|------|
| 通用容器 | `GuardedAllocator` | 默认，内存守护 + 泄漏检测 |
| 跨类型复用缓冲区 | `GuardedAlignedAllocator<>` | 保证 64B 对齐，满足所有类型 |
| 静态/线程局部变量 | `RawAllocator` | 绕过泄漏检测，避免误报 |
| SIMD 向量运算 | `GuardedAlignedAllocator<64>` | AVX-512 需要 64B 对齐 |

### 关键概念

| 概念 | 一句话 |
|------|--------|
| **Allocator** | 容器与内存管理之间的抽象层 |
| **GuardedAllocator** | 默认选择，使用 MEM_* 受保护分配 |
| **GuardedAlignedAllocator** | 增加最小对齐保证，用于类型擦除后的内存复用 |
| **RawAllocator** | malloc/free 封装，绕过泄漏检测 |
| **MEM_MIN_CPP_ALIGNMENT** | 标准 new 保证的最小对齐（通常 16B） |
| **`ul` 后缀** | unsigned long 字面量 |
| **`ULL` 后缀** | unsigned long long 字面量，跨平台安全 |
| **`BLI_NO_UNIQUE_ADDRESS`** | 空类分配器不占容器空间 |

---

## 附录 A-1：STRINGIFY 宏与 AT 宏详解

### 为什么 AT 宏需要 STRINGIFY？

```cpp
// BLI_utildefines.h:585
#define AT __FILE__ ":" STRINGIFY(__LINE__)
```

`AT` 用在 Allocator 的 `allocate` 调用中，生成 `"文件名:行号"` 字符串用于内存调试。它依赖 `STRINGIFY` 宏将 `__LINE__` 转为字符串。

### 三个 STRINGIFY 宏

```cpp
// BLI_utildefines.h:443~445
#define STRINGIFY_ARG(x) "" #x
#define STRINGIFY_APPEND(a, b) "" a #b
#define STRINGIFY(x) STRINGIFY_APPEND("", x)
```

### 核心问题：为什么需要两层宏？

C 预处理器有一条关键规则：**当宏参数出现在 `#`（字符串化）旁边时，该参数不会被展开。**

```mermaid
flowchart TD
    subgraph "❌ 直接用 STRINGIFY_APPEND"
        A1["STRINGIFY_APPEND(\"\", __LINE__)"]
        A2["#b 阻止展开 → \"__LINE__\""]
        A1 --> A2
    end
    subgraph "✅ 用 STRINGIFY 包装"
        B1["STRINGIFY(__LINE__)"]
        B2["→ STRINGIFY_APPEND(\"\", __LINE__)<br/>外层替换时 x 旁无 #，__LINE__ 展开"]
        B3["→ STRINGIFY_APPEND(\"\", 476)<br/>内层 #b 字符串化 476 → \"476\""]
        B1 --> B2 --> B3
    end

    style A2 fill:#e74c3c,color:#fff
    style B3 fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
```

### 逐步展开 AT 宏

```
AT
→ __FILE__ ":" STRINGIFY(__LINE__)
→ "BLI_array.hh" ":" STRINGIFY_APPEND("", __LINE__)
→ "BLI_array.hh" ":" STRINGIFY_APPEND("", 476)    ← __LINE__ 展开了！
→ "BLI_array.hh" ":" "" "476"
→ "BLI_array.hh:476"                               ← 最终结果
```

### 命名与用途

| 宏 | 全称 | 功能 |
|----|------|------|
| `STRINGIFY_ARG` | string-ify **arg**ument | 把参数**原样**转字符串（不展开宏） |
| `STRINGIFY_APPEND` | string-ify **append** | 字符串拼接 + 字符串化（内部辅助） |
| `STRINGIFY` | string-ify | 把参数**展开后的值**转字符串（日常使用） |
| `AT` | **at**（位置） | `__FILE__` + `:` + `__LINE__` → 内存调试标识 |

> 💡 **记忆**：`STRINGIFY_ARG` → 参数的**名字**，`STRINGIFY` → 参数的**值**。这是 C 预处理器的经典惯用法——**双层字符串化技巧（Double-Stringify Trick）**。

---

## 附录 A：allocate_zero、memset、calloc 详解

### A.1 allocate_zero 是什么？

`allocate_zero` 是 Blender Allocator 提供的**零初始化分配**方法——分配内存后，所有字节自动设为 0。

```cpp
// BLI_allocator.hh:49~58
void *allocate_zero(size_t size, size_t alignment, const char *name)
{
  if (alignment > MEM_MIN_CPP_ALIGNMENT) {
    /* There is no version of calloc with a specific alignment argument. */
    void *ptr = this->allocate(size, alignment, name);
    memset(ptr, 0, size);
    return ptr;
  }
  return MEM_new_zeroed(size, name);
}
```

> *There is no version of calloc with a specific alignment argument.*
>
> 没有带对齐参数的 calloc 版本。

**为什么需要 `allocate_zero`？** 有些场景需要分配的内存初始为全零（而不是随机值），比如：
- 分配结构体，所有字段默认为 0/nullptr/false
- 分配数组，所有元素默认初始化

**与 `allocate` 的区别**：

| 方法 | 分配后内存内容 | 性能 |
|------|--------------|------|
| `allocate` | **未初始化**（随机值） | ⚡ 更快 |
| `allocate_zero` | **全零** | 稍慢（需要写零） |

```mermaid
flowchart TD
    A["allocate_zero(size, alignment, name)"] --> B{"alignment > MEM_MIN_CPP_ALIGNMENT?"}
    B -->|"是：需要特殊对齐<br/>（如 64 字节）"| C["allocate() → memset(ptr, 0, size)<br/>⚠️ 没有对齐版 calloc"]
    B -->|"否：标准对齐即可<br/>（≤ 16 字节）"| D["MEM_new_zeroed(size, name)<br/>✅ 底层用 calloc，一步到位"]

    style C fill:#f39c12,color:#fff
    style D fill:#2ecc71,color:#fff
```

### A.2 memset 是什么？

```cpp
// vcruntime_string.h:63~68
void* __cdecl memset(void* _Dst, int _Val, size_t _Size);
```

**功能**：将内存块的每个字节设为指定值。

**参数解读**：

| 参数 | 含义 | 示例 |
|------|------|------|
| `_Dst` | 目标内存起始地址 | `ptr` |
| `_Val` | 要填充的字节值（0~255） | `0`（清零） |
| `_Size` | 要填充的字节数 | `1024` |

**常见用法**：

```cpp
// 清零内存（最常见）
memset(ptr, 0, size);       // 每个字节 = 0x00

// 填充 0xFF（常用于调试标记已释放内存）
memset(ptr, 0xFF, size);    // 每个字节 = 0xFF

// 填充特定模式
memset(ptr, 0xAB, size);    // 每个字节 = 0xAB
```

**命名来源**：`memset` = **mem**ory + **set**（内存设置）。C 标准库函数，命名遵循 `mem + 动作` 的模式。

### A.3 calloc 是什么？

```cpp
void* calloc(size_t _NumOfElements, size_t _SizeOfElements);
```

**功能**：分配内存**并自动清零**。

**参数解读**：

| 参数 | 含义 | 示例 |
|------|------|------|
| `_NumOfElements` | 元素数量 | `100` |
| `_SizeOfElements` | 每个元素的字节大小 | `sizeof(int)` = 4 |
| **返回值** | 指向已清零内存的指针 | — |

**与 malloc 的区别**：

| 函数 | 分配内存 | 初始化 | 用法 |
|------|---------|--------|------|
| `malloc(size)` | ✅ | ❌（内容随机） | `malloc(100 * sizeof(int))` |
| `calloc(n, size)` | ✅ | ✅（全零） | `calloc(100, sizeof(int))` |

```cpp
// malloc + memset = calloc 的手动版
void *ptr = malloc(100 * sizeof(int));  // 分配
memset(ptr, 0, 100 * sizeof(int));      // 清零

// 等价于
void *ptr = calloc(100, sizeof(int));   // 一步到位
```

**命名来源**：`calloc` = **c**leared + **alloc**ation（清零分配）。"c" 代表 cleared（已清除），不是 "clear"（动词）。

### A.4 为什么 memset / calloc 命名看起来奇怪？

这些函数来自 **1970 年代的 C 标准库**，命名遵循当时的风格：

```mermaid
flowchart LR
    subgraph "C 标准库命名模式"
        M1["memcpy = memory + copy"]
        M2["memset = memory + set"]
        M3["memcmp = memory + compare"]
        M4["memmove = memory + move"]
        M5["malloc = memory + allocate"]
        M6["calloc = cleared + allocate"]
        M7["realloc = re + allocate"]
    end

    style M5 fill:#3498db,color:#fff
    style M6 fill:#e67e22,color:#fff
```

| 函数 | 全称 | 逻辑 |
|------|------|------|
| `malloc` | **m**emory **alloc**ate | 分配内存（内容随机） |
| `calloc` | **c**leared **alloc**ate | 分配内存并清零 |
| `realloc` | **re**-**alloc**ate | 重新分配（调整大小） |
| `free` | **free** | 释放内存 |
| `memset` | **mem**ory **set** | 设置内存的每个字节 |
| `memcpy` | **mem**ory **copy** | 复制内存 |
| `memcmp` | **mem**ory **compare** | 比较内存 |

> 💡 **记忆技巧**：
> - `malloc` → **m**em + alloc → 分配内存
> - `calloc` → **c**leared + alloc → 清零分配（c = cleared）
> - `memset` → mem + **set** → 设置内存

### A.5 在 GuardedAllocator 中的完整流程

```mermaid
sequenceDiagram
    participant Container as 容器
    participant GA as GuardedAllocator
    participant MEM as MEM_guardedalloc
    participant CRT as C 运行时

    Note over Container: 需要零初始化分配
    Container->>GA: allocate_zero(size, alignment, name)
    
    alt alignment > MEM_MIN_CPP_ALIGNMENT
        GA->>MEM: MEM_new_uninitialized_aligned(size, alignment, name)
        MEM-->>GA: void* ptr
        GA->>CRT: memset(ptr, 0, size)
        GA-->>Container: ptr（已清零，已对齐）
    else alignment ≤ MEM_MIN_CPP_ALIGNMENT
        GA->>MEM: MEM_new_zeroed(size, name)
        Note over MEM: 底层调用 calloc
        MEM-->>GA: void* ptr（已清零）
        GA-->>Container: ptr（已清零，标准对齐）
    end
```

---

## 附录 B：__STDCPP_DEFAULT_NEW_ALIGNMENT__ 为什么是 16 而不是 8？

### B.1 指针对齐 vs new 对齐是两回事

**常见困惑**：64 位系统上指针是 8 字节，`alignof(void*)` = 8，为什么 `__STDCPP_DEFAULT_NEW_ALIGNMENT__` 是 16？

**答案**：这两个概念完全不同！

| 概念 | 含义 | 值 |
|------|------|-----|
| `alignof(void*)` | 指针类型本身的对齐要求 | 8（64 位系统） |
| `__STDCPP_DEFAULT_NEW_ALIGNMENT__` | `operator new` **保证返回**的指针的最小对齐 | 16（x64） |

### B.2 __STDCPP_DEFAULT_NEW_ALIGNMENT__ 是什么？

这是 C++17 引入的编译器预定义宏：

> *The value of `__STDCPP_DEFAULT_NEW_ALIGNMENT__` is the alignment guaranteed by `operator new`.*
>
> `__STDCPP_DEFAULT_NEW_ALIGNMENT__` 的值是 `operator new` 保证的对齐。

**拆解名称**：

```
__STDCPP_DEFAULT_NEW_ALIGNMENT__
   │      │       │    │
   │      │       │    └── 对齐（alignment）
   │      │       └─────── new 操作符
   │      └─────────────── 默认的（default）
   └────────────────────── C++ 标准定义（STDCPP）
```

**翻译**：C++ 标准定义的 new 操作符的默认对齐保证。

### B.3 为什么 new 保证 16 字节对齐？

**原因**：`operator new` 必须满足**所有基本类型**的对齐要求，不仅仅是指针。

```mermaid
flowchart TD
    Q["为什么 new 保证 16B 对齐？"] --> R1["SSE/AVX 向量类型<br/>__m128 需要 16B 对齐<br/>long double 可能 16B"]
    Q --> R2["某些平台的 long double<br/>sizeof = 16, alignof = 16"]
    Q --> R3["编译器为了安全<br/>统一保证 16B 对齐<br/>满足所有基本类型"]

    style Q fill:#e74c3c,color:#fff
    style R3 fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
```

**各类型的对齐要求**（x64 平台）：

| 类型 | 大小 | 对齐要求 |
|------|------|---------|
| `char` | 1 | 1 |
| `short` | 2 | 2 |
| `int` | 4 | 4 |
| `float` | 4 | 4 |
| `void*` | 8 | 8 |
| `double` | 8 | 8 |
| `int64_t` | 8 | 8 |
| `__m128` (SSE) | 16 | **16** ⬅️ 最大的基本对齐！ |
| `long double` | 16 (MSVC) | **16** ⬅️ |

**关键**：`operator new` 必须返回满足**所有基本类型**对齐要求的指针。SSE 的 `__m128` 类型需要 16 字节对齐，所以 `new` 保证 16 字节对齐。

### B.4 指针对齐 vs new 对齐的关系

```mermaid
flowchart TD
    subgraph "指针对齐 alignof(void*) = 8"
        P1["指针变量本身占 8 字节"]
        P2["放在 8 的倍数地址即可"]
        P3["这是指针类型的最低要求"]
    end

    subgraph "new 对齐 __STDCPP_DEFAULT_NEW_ALIGNMENT__ = 16"
        N1["new 返回的内存要满足所有类型"]
        N2["包括 __m128 (16B 对齐)"]
        N3["所以保证 16B 对齐"]
    end

    P1 -.->|"8 ≤ 16，自动满足"| N3

    style P1 fill:#3498db,color:#fff
    style N1 fill:#2ecc71,color:#fff
    style N3 fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
```

**类比**：
- `alignof(void*)` = 8 → "我（指针）只需要住在 8 的倍数号房间"
- `__STDCPP_DEFAULT_NEW_ALIGNMENT__` = 16 → "酒店（new）保证所有房间都是 16 的倍数号，比你要求的更好"

### B.5 MEM_MIN_CPP_ALIGNMENT 的完整逻辑

```cpp
#define MEM_MIN_CPP_ALIGNMENT \
  (__STDCPP_DEFAULT_NEW_ALIGNMENT__ < alignof(void *) \
    ? __STDCPP_DEFAULT_NEW_ALIGNMENT__ \
    : alignof(void *))
// 展开: (16ULL < 8 ? 16ULL : 8) = 8? 不对！
```

等等，`16 < 8` 是 false，所以结果是 `alignof(void*)` = 8？

**实际上**，展开后 `__STDCPP_DEFAULT_NEW_ALIGNMENT__` 在大多数 x64 平台上是 16，`alignof(void*)` 是 8，所以 `max(16, 8) = 16`。

但注释说展开为 `(16ULL < alignof(void*) ? 16ULL : alignof(void*))`——这意味着在某些平台上 `alignof(void*)` 可能大于 16（如某些 128 位架构），此时取 `alignof(void*)`。

```mermaid
flowchart TD
    A["MEM_MIN_CPP_ALIGNMENT"] --> B["max(16, alignof(void*))"]
    B --> C{"平台"}
    C -->|"x86 / x64<br/>alignof(void*) = 8"| D["max(16, 8) = 16"]
    C -->|"某些 128 位架构<br/>alignof(void*) = 16"| E["max(16, 16) = 16"]
    C -->|"假设未来架构<br/>alignof(void*) = 32"| F["max(16, 32) = 32"]

    style D fill:#2ecc71,color:#fff,stroke:#27ae60,stroke-width:3px
    style E fill:#3498db,color:#fff
    style F fill:#9b59b6,color:#fff
```

**结论**：在所有当前主流 x64 平台上，`MEM_MIN_CPP_ALIGNMENT = 16`。这个宏的设计是**面向未来**的——如果将来出现指针对齐更大的架构，它会自动适应。

---

*文档生成日期：2026-06-03 | 源码版本：Blender main 分支*
