# GSpan、GMutableSpan、GPointer、GMutablePointer — 泛型数据视图

> 📖 系列文档：[目录](01-列表系统架构与核心数据结构.md) | [上一篇](13-CPPType运行时类型信息.md) | [下一篇](15-VArray与GVArray虚拟数组.md)
> 源码文件：[BLI_generic_span.hh](../../source/blender/blenlib/BLI_generic_span.hh)、[BLI_generic_pointer.hh](../../source/blender/blenlib/BLI_generic_pointer.hh)

---

## 目录

1. [类型擦除的 Span/Pointer 体系](#1-类型擦除的-spanpointer-体系)
2. [GSpan — 泛型只读跨度](#2-gspan--泛型只读跨度)
3. [GMutableSpan — 泛型可变跨度](#3-gmutablespan--泛型可变跨度)
4. [GPointer — 泛型只读指针](#4-gpointer--泛型只读指针)
5. [GMutablePointer — 泛型可变指针](#5-gmutablepointer--泛型可变指针)
6. [四者关系与转换规则](#6-四者关系与转换规则)
7. [在列表系统中的应用](#7-在列表系统中的应用)

---

## 1. 类型擦除的 Span/Pointer 体系

Blender 的泛型数据视图类遵循统一的命名模式：`G` 前缀表示泛型（Generic），对应编译期类型化的版本：

```mermaid
graph TB
    subgraph "编译期类型化"
        S["Span&lt;T&gt;<br/>只读数组视图"]
        MS["MutableSpan&lt;T&gt;<br/>可变数组视图"]
        P["const T*<br/>只读指针"]
        MP["T*<br/>可变指针"]
    end

    subgraph "运行时泛型"
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

### 元素访问

```cpp
const void *operator[](int64_t index) const
{
  BLI_assert(index < size_);
  return POINTER_OFFSET(data_, type_->size * index);
}
```

> **返回 `const void*` 而非 `const T&`**：因为类型在运行时才知道，无法返回类型化引用。调用者需要自己 `static_cast<const T*>(span[index])`。

> **`POINTER_OFFSET(ptr, offset)`**：Blender 宏，等价于 `(void*)((char*)(ptr) + (offset))`。比 `ptr + index` 更明确——因为 `void*` 不支持指针算术。

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
GPointer(const CPPType &type, const void *data);

// 从类型化指针（隐式转换）
GPointer(T *data);  // 自动获取 CPPType::get<T>()
```

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
