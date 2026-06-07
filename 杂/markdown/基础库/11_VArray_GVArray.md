# VArray / GVArray 完全指南

> 从 `curves.cyclic()` 的一行代码出发，彻底理解 Blender 的虚拟数组系统。
>
> 核心源码：[BLI_virtual_array.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_virtual_array.hh)、[BLI_generic_virtual_array.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_generic_virtual_array.hh)、[BLI_generic_array.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_generic_array.hh)

---

## 目录

1. [从一个问题出发](#1-从一个问题出发)
2. [VArray 解决什么痛点](#2-varray-解决什么痛点)
3. [VArray\<T\> — 类型化虚拟数组](#3-varrayt--类型化虚拟数组)
4. [VArray vs Span vs Array](#4-varray-vs-span-vs-array)
5. [源码中的真实用例](#5-源码中的真实用例)
6. [GVArray — 类型擦除版](#6-gvarray--类型擦除版)
7. [VArray 与 GVArray 的互转](#7-varray-与-gvarray-的互转)
8. [可写版本与辅助类](#8-可写版本与辅助类)
9. [去虚拟化优化](#9-去虚拟化优化)
10. [GArray 与 GVArray 的协作](#10-garray-与-gvarray-的协作)
11. [在列表系统中的应用](#11-在列表系统中的应用)
12. [总结速查表](#12-总结速查表)

---

## 1. 从一个问题出发

### 1.1 这行代码在干什么？

```cpp
// source/blender/geometry/intern/curves_remove_and_split.cc:20
const VArray<bool> src_cyclic = curves.cyclic();
```

**直觉问题**：
- 为什么返回 `VArray<bool>`？直接返回 `Array<bool>` 或 `Span<bool>` 不行吗？
- `VArray` 和 `Array` 有什么区别？
- 这行代码背后隐藏了什么设计思想？

### 1.2 先看一下 `CurvesGeometry::cyclic()` 可能返回什么

在 Blender 中，每条曲线有一个 `cyclic` 标志（是否首尾相连形成闭环）。这个数据的存储方式**不是固定的**：

| 场景 | 底层存储 | 示例 |
|------|----------|------|
| **所有曲线都是非循环的** | 单个 `false` 值 | 1000 条曲线，只需要 1 个 bool |
| **所有曲线都是循环的** | 单个 `true` 值 | 1000 条曲线，只需要 1 个 bool |
| **混合情况** | `Array<bool>`，每条曲线一个值 | 曲线 0 循环，曲线 1 不循环... |

**关键洞察**：如果强制返回 `Array<bool>`，前两种场景会浪费 999 个 bool 的内存。如果返回 `Span<bool>`，前两种场景根本无法表示（没有数组可引用）。

**VArray 的解决方案**：统一接口，底层可以是"单值"、"数组"、甚至"函数"，调用者完全不用关心。

```mermaid
flowchart TB
    subgraph 调用者["调用者视角"]
        CALL["src_cyclic[i]<br/>获取第 i 条曲线的循环标志"]
    end

    subgraph VArray内部["VArray 内部（透明）"]
        direction TB
        SINGLE["场景 A：单值<br/>返回同一个 bool"]
        SPAN["场景 B：数组<br/>从 Array&lt;bool&gt; 取"]
        FUNC["场景 C：函数<br/>按需计算"]
    end

    CALL --> SINGLE
    CALL --> SPAN
    CALL --> FUNC

    style CALL fill:#e3f2fd,stroke:#1976d2,stroke-width:3px,color:#0d47a1
    style SINGLE fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20
    style SPAN fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100
    style FUNC fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#880e4f
```

---

## 2. VArray 解决什么痛点

### 2.1 文件头注释详解

源码文件 [BLI_virtual_array.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_virtual_array.hh) 开头的注释翻译：

> **"A virtual array is a data structure that behaves similarly to an array, but its elements are accessed through virtual methods."**
>
> 虚拟数组是一种行为类似数组的数据结构，但它的元素通过虚方法访问。

> **"Its purpose is to allow code that uses arrays to also work with data that is not actually stored as an array. For example, a virtual array can represent a single value that is used for every index, or it can represent a function that computes a value for each index."**
>
> 它的目的是让使用数组的代码也能处理**实际上不是以数组形式存储的数据**。例如，虚拟数组可以表示"每个索引都返回同一个值"，或者"每个索引通过函数计算值"。

> **"The disadvantage of using a virtual array is that calling a virtual method for every element access has some overhead compared to accessing elements in a plain array. However, in many cases, the overhead is negligible or is offset by the benefits of not having to convert data into an array format first."**
>
> 缺点是：每次元素访问都要调用虚方法，比直接访问数组有额外开销。但在很多场景下，这个开销可以忽略，或者被"不需要先把数据转成数组格式"的优势所抵消。

> **"In some cases, the overhead of virtual method calls can be avoided by "devirtualizing" the virtual array. This means that the code that uses the virtual array is compiled multiple times for different storage types. This is useful when the overhead of virtual method calls is significant."**
>
> 某些情况下，可以通过"去虚拟化"避免虚方法调用开销——即为不同的存储类型编译多份代码。当虚方法开销显著时很有用。

```mermaid
flowchart TD
    PROBLEM["痛点：数据不总是数组"]

    P1["所有值相同<br/>（如全部非循环）<br/>存 1 个值 vs 1000 个值"]
    P2["值需要计算<br/>（如 position.x）<br/>没有预存数据"]
    P3["数据在容器中<br/>（如 Vector&lt;T&gt;）<br/>需要统一接口"]

    SOL["VArray 解决方案"]
    S1["VArrayImpl_For_Single<br/>单值广播"]
    S2["VArrayImpl_For_Func<br/>函数生成"]
    S3["VArrayImpl_For_Span<br/>包装数组"]

    PROBLEM --> P1 --> S1 --> SOL
    PROBLEM --> P2 --> S2 --> SOL
    PROBLEM --> P3 --> S3 --> SOL

    style PROBLEM fill:#e74c3c,color:#fff
    style SOL fill:#2ecc71,color:#fff
```

### 2.2 痛点一：调用者不想做数据转换

```cpp
// ❌ 方案 A：接受 Span<float>（太严格）
void process(Span<float> values) {
    for (float v : values) { /* ... */ }
}

// 调用者必须先把数据转成连续数组
Vector<float> vec = {1.0f, 2.0f, 3.0f};
process(vec);  // ✅ 可以

// 但如果是单值广播呢？
process(Span<float>(/* 只有一个 float，没法构造 Span */));  // ❌ 不行！
```

```cpp
// ✅ 方案 B：接受 VArray<float>（灵活）
void process(VArray<float> values) {
    for (int64_t i : values.index_range()) {
        float v = values[i];  // 不管底层是什么，都能访问
    }
}

// 从数组构造
Array<float> arr = {1.0f, 2.0f, 3.0f};
process(VArray<float>::from_span(arr));  // ✅

// 从单值构造（1000 个元素都是 42.0f）
process(VArray<float>::from_single(42.0f, 1000));  // ✅

// 从函数构造
process(VArray<float>::from_func(100, [](int64_t i) { return float(i) * 0.5f; }));  // ✅
```

### 2.3 痛点二：有些数据根本不存在于内存中

字段系统（Field System）的核心特性是**延迟计算**。比如用户输入了一个 `"position"` 字段，它的值不是预先存好的，而是在求值时根据几何体实时计算出来的。

```cpp
// 字段求值结果就是一个 VArray
// 底层根本没有 Array<float3>，只有一个计算函数
VArray<float3> positions = evaluator.get_evaluated<float3>(0);

// 访问 positions[10] 时，才会调用底层函数计算第 10 个点的位置
float3 pos = positions[10];
```

### 2.4 痛点三：性能与灵活性的权衡

```mermaid
flowchart LR
    subgraph 传统方式["传统方式：先转换再处理"]
        A["原始数据<br/>（任意格式）"] --> B["强制转换为<br/>Array&lt;T&gt;"]
        B --> C["处理"]
    end

    subgraph VArray方式["VArray 方式：直接处理"]
        D["原始数据<br/>（任意格式）"] --> E["包装为 VArray&lt;T&gt;"]
        E --> F["处理<br/>按需访问"]
    end

    style B fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#b71c1c
    style E fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20
```

---

## 3. VArray\<T\> — 类型化虚拟数组

### 3.1 类层次结构

```mermaid
flowchart TB
    subgraph 接口层["接口层"]
        VA["VArray&lt;T&gt;<br/>用户直接使用的包装类"]
    end

    subgraph 实现层["实现层"]
        IMPL["VArrayImpl&lt;T&gt;<br/>抽象基类<br/>virtual T get(int64_t) = 0"]
        MIMPL["VMutableArrayImpl&lt;T&gt;<br/>增加 virtual void set()"]

        SPAN["VArrayImpl_For_Span<br/>包装连续数组"]
        SINGLE["VArrayImpl_For_Single<br/>单值广播"]
        FUNC["VArrayImpl_For_Func<br/>函数生成"]
        DERIVED["VArrayImpl_For_DerivedSpan<br/>派生 Span（转换视图）"]
        CONT["VArrayImpl_For_ArrayContainer<br/>拥有容器"]
    end

    VA -->|持有| IMPL
    IMPL -->|派生| SPAN
    IMPL -->|派生| SINGLE
    IMPL -->|派生| FUNC
    IMPL -->|派生| DERIVED
    IMPL -->|派生| CONT
    MIMPL -->|派生| SPAN

    style VA fill:#e3f2fd,stroke:#1976d2,stroke-width:3px,color:#0d47a1
    style IMPL fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100
    style SPAN fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20
    style SINGLE fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20
    style FUNC fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20
    style DERIVED fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20
```

### 3.2 VArrayImpl — 抽象基类注释详解

```cpp
// BLI_virtual_array.hh:88~99
template<typename T> class VArrayImpl {
 public:
  virtual ~VArrayImpl() = default;

  /* Get the element at the given index. */
  virtual T get(const int64_t index) const = 0;

  /* Return info about the virtual array implementation that allows for
   * optimizations. For example, it may tell whether the virtual array is
   * stored as a span or as a single value. */
  virtual CommonVArrayInfo common_info() const
  {
    return CommonVArrayInfo{};
  }
};
```

> **`get(index)` 注释**："Get the element at the given index."——获取给定索引处的元素。这是所有虚拟数组实现的核心方法——每个子类都必须实现它。
>
> **`common_info()` 注释**："Return info about the virtual array implementation that allows for optimizations. For example, it may tell whether the virtual array is stored as a span or as a single value."——返回虚拟数组实现的信息，用于优化。例如，可以告诉调用者底层是 Span 还是 Single。
>
> **为什么 `common_info()` 有默认实现？** 因为不是所有实现都需要特殊优化。`VArrayImpl_For_Func`（函数生成）就用默认实现（返回 `Type::Any`），因为函数没有可优化的内部结构。而 `VArrayImpl_For_Span` 和 `VArrayImpl_For_Single` 重写了此方法，返回 `Type::Span` 和 `Type::Single`，让调用者可以走快速路径。

### 3.3 实现一：VArrayImpl_For_Span（包装数组）

```cpp
// BLI_virtual_array.hh:204~264
template<typename T> class VArrayImpl_For_Span : public VMutableArrayImpl<T> {
 protected:
  T *data_ = nullptr;

 public:
  VArrayImpl_For_Span(const MutableSpan<T> data)
      : VMutableArrayImpl<T>(data.size()), data_(data.data()) {}

  T get(const int64_t index) const final {
    return data_[index];  // 直接数组访问
  }

  void set(const int64_t index, T value) final {
    data_[index] = value;  // 直接数组写入
  }

  CommonVArrayInfo common_info() const override {
    return CommonVArrayInfo(CommonVArrayInfo::Type::Span, true, data_);
  }
};
```

**特点**：
- 底层就是一块连续内存
- `get()` 直接 `data_[index]`，最快
- `common_info()` 返回 `Type::Span`，让外部知道可以优化

### 3.4 实现二：VArrayImpl_For_Single（单值广播）

```cpp
// BLI_virtual_array.hh:314~366
template<typename T> class VArrayImpl_For_Single final : public VArrayImpl<T> {
 private:
  T value_;

 public:
  VArrayImpl_For_Single(T value, const int64_t size)
      : VArrayImpl<T>(size), value_(std::move(value)) {}

  T get(const int64_t /*index*/) const override {
    return value_;  // 不管 index 是什么，返回同一个值
  }

  CommonVArrayInfo common_info() const override {
    return CommonVArrayInfo(CommonVArrayInfo::Type::Single, true, &value_);
  }
};
```

**特点**：
- 所有索引返回同一个值
- 内存占用极小（只有一个 `T`）
- `materialize` 优化：用 `fill` 而不是逐个 `get`

**用例**：`curves.cyclic()` 在所有曲线都是非循环时，底层就是这个实现。

### 3.5 实现三：VArrayImpl_For_Func（函数生成）

```cpp
// BLI_virtual_array.hh:375~423
template<typename T, typename GetFunc> class VArrayImpl_For_Func final : public VArrayImpl<T> {
 private:
  GetFunc get_func_;

 public:
  VArrayImpl_For_Func(const int64_t size, GetFunc get_func)
      : VArrayImpl<T>(size), get_func_(std::move(get_func)) {}

  T get(const int64_t index) const override {
    return get_func_(index);  // 调用函数生成值
  }
};
```

> **类注释**："This class makes it easy to create a virtual array for an existing function or lambda. The `GetFunc` should take a single `index` argument and return the value at that index."——这个类让为已有函数或 lambda 创建虚拟数组变得容易。`GetFunc` 应该接受一个 `index` 参数并返回该索引处的值。
>
> **为什么用模板参数 `GetFunc` 而非 `std::function<T(int64_t)>`？** 性能！`GetFunc` 是模板参数，编译器可以内联 lambda 的调用。`std::function` 有类型擦除开销（虚函数调用 + 堆分配）。源码也提供了 `from_std_func` 作为慢速替代——注释说："Same as #from_func, but uses a std::function instead of a template. This is slower, but requires less code generation. Therefore this should be used in non-performance critical code."（和 from_func 相同，但用 std::function 代替模板。更慢，但需要更少的代码生成。因此应该用在非性能关键代码中。）

### 3.6 实现四：VArrayImpl_For_DerivedSpan（派生 Span — 转换视图）

```cpp
// BLI_virtual_array.hh:428~495
template<typename StructT,
         typename ElemT,
         ElemT (*GetFunc)(const StructT &),
         void (*SetFunc)(StructT &, ElemT) = nullptr>
class VArrayImpl_For_DerivedSpan final : public VMutableArrayImpl<ElemT> {
```

> **类注释**："This is `final` so that #may_have_ownership can be implemented reliably."——标记为 `final` 以便 `may_have_ownership` 能可靠实现。`final` 阻止进一步继承，确保 `common_info()` 的 `may_have_ownership` 逻辑不会被错误覆盖。
>
> **这是什么？** 一个"转换视图"——底层存储的是 `StructT` 数组，但对外暴露为 `ElemT` 数组。每次 `get(index)` 调用 `GetFunc(data_[index])` 把 `StructT` 转为 `ElemT`。
>
> **模板参数**：
> - `StructT`：底层存储的结构类型（如 `float4`）
> - `ElemT`：对外暴露的元素类型（如 `float3`）
> - `GetFunc`：从 `StructT` 提取 `ElemT` 的函数指针
> - `SetFunc`：将 `ElemT` 写回 `StructT` 的函数指针（可选，`nullptr` 表示只读）
>
> **用例**：Blender 的自定义属性存储为 `float4`（4 字节对齐），但用户访问的是 `float3`（3 字节）。`VArrayImpl_For_DerivedSpan` 提供了一个零拷贝的"视图"——不需要把 `float4[]` 转成 `float3[]`，每次访问时调用转换函数。

### 3.7 CommonVArrayInfo：快速类型探测

```cpp
// BLI_virtual_array.hh:47~71
struct CommonVArrayInfo {
  enum class Type : uint8_t {
    Any,    // 通用类型（如 Func）
    Span,   // 底层是连续数组
    Single, // 底层是单值广播
  };

  Type type = Type::Any;
  bool may_have_ownership = true;
  const void *data;  // 指向底层数据
};
```

> **`may_have_ownership` 注释**："Whether the virtual array implementation may own the memory. This is useful to determine whether the data can be accessed safely even after the original data source has been modified or freed."——虚拟数组实现是否可能拥有内存。用于判断即使原始数据源被修改或释放后，数据是否仍然安全访问。
>
> - `Span` 模式：`may_have_ownership = true`（可能拥有，取决于是否通过 `from_container` 创建）
> - `Single` 模式：`may_have_ownership = true`（拥有单值的拷贝）
> - `Func` 模式：`may_have_ownership = true`（函数可能持有捕获变量的所有权）
> - `DerivedSpan` 模式：`may_have_ownership = false`（只是一个视图，不拥有底层数据）

```mermaid
graph TB
    subgraph "Span 模式"
        SP["data 指向连续内存<br/>arr[0]=1.0, arr[1]=2.0, arr[2]=3.0<br/>访问: O(1), 无函数调用"]
    end

    subgraph "Single 模式"
        SI["data 指向单个值<br/>arr[i] = 42.0 (对所有 i)<br/>访问: O(1), 无函数调用"]
    end

    subgraph "Any 模式"
        AN["通过虚函数 get(index) 访问<br/>可能是计算函数、字段求值等<br/>访问: O(1) 但有虚函数调用开销"]
    end

    style SP fill:#2ecc71,color:#fff
    style SI fill:#e67e22,color:#fff
    style AN fill:#9b59b6,color:#fff
```

**作用**：通过一次虚函数调用 `common_info()`，外部就能知道底层是什么类型，从而选择优化路径：

```cpp
VArray<float> varray = get_some_varray();

if (varray.is_single()) {
    float val = varray.get_internal_single();
    // 所有值相同，可以用 fill 优化
}
else if (varray.is_span()) {
    Span<float> span = varray.get_internal_span();
    // 底层是连续数组，可以直接拿指针
}
```

### 3.8 工厂方法

```cpp
// 从连续内存创建
static VArray<T> from_span(Span<T> span);

// 从单个值创建（所有索引返回同一个值）
static VArray<T> from_single(T value, int64_t size);

// 从计算函数创建
template<typename GetFn> static VArray<T> from_func(GetFn fn, int64_t size);

// 空 VArray
static VArray<T> empty();
```

---

## 4. VArray vs Span vs Array

| 特性 | `Span<T>` | `VArray<T>` | `Array<T>` |
|------|-----------|-------------|------------|
| **只读/可写** | 只读视图 | 只读（`VMutableArray` 可写） | 可写 |
| **底层形态** | 必须是连续数组 | Span / Single / Func 都可以 | 连续数组 |
| **内存拥有** | 不拥有 | 可选（取决于实现） | 拥有 |
| **访问开销** | O(1)，直接指针 | O(1) + 虚函数开销 | O(1)，直接指针 |
| **单值广播** | ❌ 不支持 | ✅ 支持 | ❌ 不支持（浪费内存） |
| **函数生成** | ❌ 不支持 | ✅ 支持 | ❌ 不支持 |
| **适用场景** | 已知底层是数组 | 不知道底层形态 | 需要拥有并修改数据 |

### 选择指南

```mermaid
flowchart TB
    START{"你需要什么？"}

    START -->|已知底层是连续数组<br/>追求极致性能| SPAN["Span&lt;T&gt;"]
    START -->|不知道底层怎么存的<br/>可能是单值/数组/函数| VARRAY["VArray&lt;T&gt;"]
    START -->|需要拥有数据并修改<br/>且数据量不大| ARRAY["Array&lt;T&gt;"]

    SPAN -->|但调用者只有 VArray| VS["VArraySpan&lt;T&gt;<br/>（必要时拷贝）"]
    VARRAY -->|发现底层是 Span<br/>想直接操作| DEV["devirtualize_varray<br/>（去虚拟化）"]

    style SPAN fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20
    style VARRAY fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#0d47a1
    style ARRAY fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100
```

---

## 5. 源码中的真实用例

### 5.1 用例一：curves.cyclic()（属性读取）

```cpp
// source/blender/geometry/intern/curves_remove_and_split.cc:20
const VArray<bool> src_cyclic = curves.cyclic();

// 后续使用：像普通数组一样索引访问
const bool curve_cyclic = src_cyclic[curve_i];
```

**为什么用 VArray？**
- `cyclic` 属性可能以单值存储（所有曲线相同）
- 也可能以数组存储（每条曲线不同）
- 调用者不需要关心，统一用 `operator[]` 访问

### 5.2 用例二：字段求值结果

```cpp
// node_geo_curve_split.cc:183~187
fn::FieldEvaluator evaluator{field_context, src_curves.points_num()};
evaluator.add(selection_field);
evaluator.evaluate();

const IndexMask selection = evaluator.get_evaluated_as_mask(0);
```

**内部实现**：`FieldEvaluator` 的求值结果底层是 `GVArray`（`VArray` 的类型擦除版），可能来自：
- 直接从几何体属性读取（Span）
- 常量字段（Single）
- 复杂表达式计算（Func）

### 5.3 用例三：函数参数解耦

```cpp
void process_curves(const CurvesGeometry &curves,
                    const VArray<bool> &cyclic_flags)  // 可以是 Single 或 Span
{
    for (const int i : curves.curves_range()) {
        if (cyclic_flags[i]) {
            // 处理循环曲线...
        }
    }
}

// 调用方式 1：从 CurvesGeometry 获取（可能是 Single）
process_curves(curves, curves.cyclic());

// 调用方式 2：手动构造 Single（测试用）
process_curves(curves, VArray<bool>::from_single(false, curves.curves_num()));
```

---

## 6. GVArray — 类型擦除版

### 6.1 为什么需要 GVArray？

`VArray<T>` 的 `T` 在**编译期**确定。但属性系统的场景是：运行期才知道属性是什么类型（`float`、`float3`、`int`...）。

```cpp
// 属性查找返回 GVArray（类型在运行期确定）
std::optional<GVArray> attribute = attributes.lookup("position");

// 检查类型
if (attribute->type() == CPPType::get<float3>()) {
    // 安全地转回具体类型
    VArray<float3> typed = attribute->typed<float3>();
    float3 pos = typed[0];
}
```

### 6.2 类层次结构

```mermaid
classDiagram
    class GVArrayImpl {
        #type_ : const CPPType*
        #size_ : int64_t
        +type() const CPPType&
        +size() int64_t
        +get(index, void* r_value)*
        +get_to_uninitialized(index, void* r_value)*
        +common_info() CommonVArrayInfo
        +materialize(mask, dst)*
    }

    class GVArrayCommon {
        #impl_ : AnyDerived
        +type() const CPPType&
        +size() int64_t
        +is_span() bool
        +is_single() bool
        +get(index, void* r_value)
        +common_info() CommonVArrayInfo
    }

    class GVArray {
        +typed~T~() VArray~T~
        +from_span(span)$ GVArray
        +from_single(type, size, value)$ GVArray
        +from_garray(array)$ GVArray
    }

    class GVMutableArray {
        +set_by_copy(index, value)
        +set_by_move(index, value)
        +typed~T~() VMutableArray~T~
    }

    GVArrayImpl <|-- GVArrayCommon : 持有
    GVArrayCommon <|-- GVArray
    GVArrayCommon <|-- GVMutableArray
```

### 6.3 与 VArray\<T\> 的关键区别

| 特性 | `VArray<T>` | `GVArray` |
|------|------------|-----------|
| 元素类型 | 编译期 `T` | 运行时 `CPPType` |
| `get(index)` 返回 | `T`（值） | `void`（写入 `r_value` 指针） |
| `operator[]` 返回 | `T`（值） | 无（需用 `get`） |
| `typed<T>()` | — | 转为 `VArray<T>` |
| 内部存储 | `AnyDerived<VArrayImpl<T>>` | `AnyDerived<GVArrayImpl>` |

### 6.4 get() 方法 — 泛型值获取

```cpp
void get(int64_t index, void *r_value) const
{
  impl_->get(index, r_value);  // 虚函数调用，将值写入 r_value
}

template<typename T> T get(int64_t index) const
{
  BLI_assert(this->type().is<T>());
  T value{};
  impl_->get(index, &value);
  return value;
}
```

> **`get(index, void*)` vs `get<T>(index)`**：前者是泛型接口（写入指定内存），后者是类型化便捷方法（返回值）。前者用于泛型代码，后者用于已知类型的代码。

### 6.5 工厂方法

```cpp
// 从 GSpan 创建
static GVArray from_span(GSpan span);

// 从单个值创建
static GVArray from_single(const CPPType &type, int64_t size, const void *value);

// 从 GArray 创建（共享所有权）
static GVArray from_garray(GArray<> array);

// 从计算函数创建
template<typename GetToUninitFn>
static GVArray from_func(const CPPType &type, int64_t size, GetToUninitFn &&fn);

// 空 GVArray
static GVArray from_empty(const CPPType &type);
```

> **`from_garray` vs `from_span`**：`from_span` 不拥有数据（数据可能被其他代码释放），`from_garray` 拥有数据（`GArray` 的生命周期由 `GVArray` 管理）。

### 6.6 GVArray 与 VArray 的关系

```mermaid
flowchart TB
    subgraph 编译期类型["编译期确定类型"]
        VA_F["VArray&lt;float&gt;"]
        VA_I["VArray&lt;int&gt;"]
        VA_3["VArray&lt;float3&gt;"]
    end

    subgraph 运行期类型["运行期确定类型"]
        GVA["GVArray<br/>持有 CPPType*<br/>+ VArrayImpl&lt;void&gt;*"]
    end

    VA_F -->|擦除类型| GVA
    VA_I -->|擦除类型| GVA
    VA_3 -->|擦除类型| GVA

    GVA -->|typed&lt;float&gt;()| VA_F
    GVA -->|typed&lt;int&gt;()| VA_I

    style GVA fill:#fce4ec,stroke:#c2185b,stroke-width:3px,color:#880e4f
```

---

## 7. VArray 与 GVArray 的互转

`VArray<T>` 和 `GVArray` 可以互相转换，但转换不是零开销的——需要创建适配器。

```mermaid
sequenceDiagram
    participant VA as VArray&lt;float&gt;
    participant GVA as GVArray
    participant VA2 as VArray&lt;float&gt;

    Note over VA: 编译期类型 float
    VA->>GVA: 隐式转换<br/>检查 common_info<br/>Span/Single → 零开销<br/>其他 → 包装为 GVArrayImpl_For_VArray
    Note over GVA: 运行时类型 CPPType::get&lt;float&gt;()
    GVA->>VA2: typed&lt;float&gt;()<br/>检查 common_info<br/>Span/Single → 零开销<br/>其他 → 包装为 VArrayImpl_For_GVArray
```

### 7.1 VArray → GVArray（隐式转换）

```cpp
template<typename T> GVArray::GVArray(VArray<T> &&varray)
{
  const CommonVArrayInfo info = varray.common_info();
  if (info.type == CommonVArrayInfo::Type::Single) {
    // 单值模式：直接创建 GVArray（零开销）
    *this = GVArray::from_single(CPPType::get<T>(), varray.size(), info.data);
    return;
  }
  if (info.type == CommonVArrayInfo::Type::Span && !info.may_have_ownership) {
    // 连续内存 + 无所有权：直接创建 GVArray（零开销）
    *this = GVArray::from_span(GSpan(CPPType::get<T>(), info.data, varray.size()));
    return;
  }
  // 其他情况：需要适配器（有开销）
  *this = GVArray::from<GVArrayImpl_For_VArray<T>>(std::move(varray));
}
```

### 7.2 GVArray → VArray（typed\<T\>()）

```cpp
template<typename T> VArray<T> GVArray::typed() const
{
  const CommonVArrayInfo info = this->common_info();
  if (info.type == CommonVArrayInfo::Type::Single) {
    return VArray<T>::from_single(*static_cast<const T *>(info.data), this->size());
  }
  if (info.type == CommonVArrayInfo::Type::Span && !info.may_have_ownership) {
    return VArray<T>::from_span(Span<T>(static_cast<const T *>(info.data), this->size()));
  }
  // 其他情况：需要适配器
  return VArray<T>::template from<VArrayImpl_For_GVArray<T>>(*this);
}
```

> **零开销转换条件**：当 `VArray` 内部是 Span 或 Single 模式时，可以零开销转换——只需提取 `data` 指针和 `size`，不需要适配器。其他情况需要创建适配器对象，有额外开销。

```mermaid
flowchart LR
    subgraph "零开销转换"
        Z1["VArray(Span) → GVArray(Span)"]
        Z2["VArray(Single) → GVArray(Single)"]
        Z3["GVArray(Span) → VArray(Span)"]
        Z4["GVArray(Single) → VArray(Single)"]
    end

    subgraph "需要适配器"
        A1["VArray(Func) → GVArray<br/>GVArrayImpl_For_VArray"]
        A2["GVArray(Any) → VArray<br/>VArrayImpl_For_GVArray"]
    end

    style Z1 fill:#2ecc71,color:#fff
    style Z2 fill:#2ecc71,color:#fff
    style Z3 fill:#2ecc71,color:#fff
    style Z4 fill:#2ecc71,color:#fff
    style A1 fill:#e67e22,color:#fff
    style A2 fill:#e67e22,color:#fff
```

---

## 8. 可写版本与辅助类

### 8.1 VArrayCommon 注释详解

```cpp
// BLI_virtual_array.hh:504~511
/**
 * Utility class to reduce code duplication for methods available on #VArray and #VMutableArray.
 * Deriving #VMutableArray from #VArray would have some issues:
 * - Static methods on #VArray would also be available on #VMutableArray.
 * - It would allow assigning a #VArray to a #VMutableArray under some circumstances which is not
 *   allowed and could result in hard to find bugs.
 */
template<typename T> class VArrayCommon {
```

> **为什么用 `VArrayCommon` 而非让 `VMutableArray` 继承 `VArray`？** 注释解释了两个问题：
>
> 1. **静态方法泄漏**：如果 `VMutableArray` 继承 `VArray`，`VArray` 的静态方法（如 `VArray::from_single`）也会出现在 `VMutableArray` 上——但 `from_single` 创建的是只读虚拟数组，不应该出现在可写类型上
> 2. **隐式转换风险**：继承会允许在某些情况下把 `VArray` 赋值给 `VMutableArray`——这是不允许的，因为只读数组不能当可写数组用，可能导致难以发现的 bug
>
> 所以 `VArrayCommon` 是**组合**而非继承——`VArray` 和 `VMutableArray` 都继承 `VArrayCommon`，共享通用方法，但各自有独立的接口。

### 8.2 VArray 类注释详解

```cpp
// BLI_virtual_array.hh:720~724
/**
 * A #VArray wraps a virtual array implementation and provides easy access to its elements. It can
 * be copied and moved. While it is relatively small, it should still be passed by reference if
 * possible (other than e.g. #Span).
 */
template<typename T> class VArray : public VArrayCommon<T> {
```

> **"It can be copied and moved"**——VArray 可以拷贝和移动。拷贝 VArray 是浅拷贝——只复制 `impl_`（`AnyDerived`），不复制底层数据。底层通过 `shared_ptr` 共享。
>
> **"While it is relatively small, it should still be passed by reference if possible (other than e.g. #Span)"**——虽然 VArray 相对较小（约 32-48 字节），但仍然应该尽量按引用传递。注意 `Span` 不同——`Span` 只有 16 字节（指针+大小），按值传递和按引用传递性能差不多，所以 `Span` 通常按值传递。但 `VArray` 包含 `AnyDerived`，拷贝需要增加引用计数，开销更大。

### 8.3 `operator[]` 注释详解

```cpp
// BLI_virtual_array.hh:543~549
/**
 * Get the element at a specific index.
 * \note This can't return a reference because the value may be computed on the fly. This also
 * implies that one can not use this method for assignments.
 */
T operator[](const int64_t index) const
{
  BLI_assert(*this);
  BLI_assert(index >= 0);
  BLI_assert(index < this->size());
  return impl_->get(index);
}
```

> **"This can't return a reference because the value may be computed on the fly"**——不能返回引用，因为值可能是即时计算的。`VArrayImpl_For_Func` 每次调用 `get()` 都计算一个新值，这个值存在临时变量中，函数返回后就没了——无法返回引用。
>
> **"This also implies that one can not use this method for assignments"**——这也意味着不能用 `[]` 赋值。`varray[i] = value` 需要返回引用，但 `operator[]` 返回值（`T`），不是引用（`T&`）。可写版本用 `VMutableArray::set(index, value)` 代替。

### 8.4 varray_tag 注释详解

```cpp
// BLI_virtual_array.hh:707~718
/**
 * Various tags to disambiguate constructors of virtual arrays.
 * Generally it is easier to use `VArray::from_*` functions to construct virtual arrays, but
 * sometimes being able to use the constructor can result in better performance. For example, when
 * constructing the virtual array directly in a vector. Without the constructor one would have to
 * construct the virtual array first and then move it into the vector.
 */
namespace varray_tag {
struct span {};
struct single_ref {};
struct single {};
}  // namespace varray_tag
```

> **"Various tags to disambiguate constructors"**——各种标签，用于消除构造函数的歧义。因为 `VArray` 的构造函数可能接受多种参数类型，标签帮助编译器区分。
>
> **"Sometimes being able to use the constructor can result in better performance"**——有时用构造函数比 `from_*` 静态方法性能更好。例如直接在 vector 中构造虚拟数组——用构造函数可以原地构造（`vector.emplace_back(varray_tag::span{}, my_span)`），用 `from_*` 则需要先构造再移动。

| 标签 | 对应 | 等价静态方法 |
|------|------|------------|
| `varray_tag::span` | 从 Span 构造 | `VArray::from_span()` |
| `varray_tag::single` | 从单值构造（拷贝） | `VArray::from_single()` |
| `varray_tag::single_ref` | 从单值引用构造 | 无直接等价 |

### 8.5 VMutableArray\<T\>

```cpp
template<typename T> class VMutableArray : public VArrayCommon<T> {
 public:
    void set(int64_t index, T value);  // 写入
    void set_all(Span<T> src);         // 批量写入
    operator VArray<T>() const;        // 隐式转只读
};
```

### 8.6 VArraySpan：VArray → Span 的桥梁

```cpp
// BLI_virtual_array.hh:948~1003
template<typename T> class VArraySpan final : public Span<T> {
 private:
  VArray<T> varray_;
  Array<T> owned_data_;  // 如果底层不是 Span，需要拷贝到这里

 public:
  VArraySpan(VArray<T> &&varray) : varray_(std::move(varray)) {
    const CommonVArrayInfo info = varray_.common_info();
    if (info.type == CommonVArrayInfo::Type::Span) {
      // 底层就是 Span，直接引用，零拷贝！
      this->data_ = static_cast<const T *>(info.data);
    }
    else {
      // 底层是 Single 或 Func，必须拷贝到数组
      owned_data_.~Array();
      new (&owned_data_) Array<T>(varray_.size(), NoInitialization{});
      varray_.materialize_to_uninitialized(owned_data_);
      this->data_ = owned_data_.data();
    }
  }
};
```

**使用场景**：某个 API 只接受 `Span<T>`，但你的数据是 `VArray<T>`。

```cpp
void api_only_accepts_span(Span<float> data);  // 第三方 API

VArray<float> varray = get_varray();
VArraySpan<float> varray_span(varray);  // 如果底层是 Span，零拷贝；否则拷贝
api_only_accepts_span(varray_span);      // ✅
```

### 8.7 MutableVArraySpan：可写版 + save() 机制

```cpp
// BLI_virtual_array.hh:1016~1114
template<typename T> class MutableVArraySpan final : public MutableSpan<T> {
 private:
  VMutableArray<T> varray_;
  Array<T> owned_data_;
  bool save_has_been_called_ = false;

 public:
  MutableVArraySpan(VMutableArray<T> varray) : varray_(std::move(varray)) {
    const CommonVArrayInfo info = varray_.common_info();
    if (info.type == CommonVArrayInfo::Type::Span) {
      this->data_ = const_cast<T *>(static_cast<const T *>(info.data));
    }
    else {
      // 分配临时数组，修改这里
      owned_data_.reinitialize(varray_.size());
      this->data_ = owned_data_.data();
    }
  }

  // 关键：将修改写回底层虚拟数组
  void save() {
    save_has_been_called_ = true;
    if (this->data_ != owned_data_.data()) {
      return;  // 底层就是 Span，修改已直接生效
    }
    varray_.set_all(owned_data_);  // 将临时数组写回
  }

  ~MutableVArraySpan() {
    if (!save_has_been_called_) {
      print_mutable_varray_span_warning();  // 忘记 save 会警告！
    }
  }
};
```

**关键设计**：
- 如果底层是 Span，直接操作底层内存，`save()` 什么都不做
- 如果底层是 Single/Func，修改的是临时数组，必须调用 `save()` 写回
- 析构时检查是否调用了 `save()`，防止忘记写回

```mermaid
flowchart TB
    subgraph 修改前["构造 MutableVArraySpan"]
        A["VMutableArray&lt;float&gt;"]
    end

    subgraph 分支["底层类型判断"]
        B{"底层是 Span?"}
    end

    subgraph Span路径["Span 路径 ✅"]
        C["直接引用底层内存"]
        C --> D["修改直接生效"]
        D --> E["save() 无操作"]
    end

    subgraph 非Span路径["Single/Func 路径 ⚠️"]
        F["分配 owned_data_ 临时数组"]
        F --> G["修改临时数组"]
        G --> H["必须调用 save()"]
        H --> I["set_all 写回底层"]
    end

    A --> B
    B -->|是| C
    B -->|否| F

    style Span路径 fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20
    style 非Span路径 fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100
```

---

## 9. 去虚拟化优化

### 9.1 问题：虚函数调用有开销

```cpp
VArray<float> varray = get_varray();
for (int64_t i = 0; i < varray.size(); i++) {
    float v = varray[i];  // 每次都有虚函数调用！
}
```

如果循环 100 万次，虚函数调用的累积开销可能很显著。

### 9.2 解决方案：编译期生成多版本

```cpp
// BLI_virtual_array.hh:1183~1194
template<typename T, typename Func>
inline void devirtualize_varray(const VArray<T> &varray, const Func &func, bool enable = true) {
  if (enable) {
    if (call_with_devirtualized_parameters(
            std::make_tuple(VArrayDevirtualizer<T, true, true>{varray}), func)) {
      return;  // 成功去虚拟化，直接返回
    }
  }
  func(VArrayRef<T>(varray));  // 回退：普通虚函数调用
}
```

**原理**：
1. 检查 `varray.common_info()` 的底层类型
2. 如果是 `Span`，调用 `func(Span<T>())`
3. 如果是 `Single`，调用 `func(SingleAsSpan<T>())`
4. 如果是 `Any`，回退到 `func(VArrayRef<T>())`

```cpp
// 使用示例
devirtualize_varray(varray, [&](auto &&span) {
    // 这里的 span 可能是 Span<T>、SingleAsSpan<T> 或 VArrayRef<T>
    // 编译器会为每种情况生成一份代码
    for (int64_t i = 0; i < span.size(); i++) {
        float v = span[i];  // 如果是 Span，直接内联；如果是 Single，直接返回单值
    }
});
```

### 9.3 注意事项

```cpp
// 文件注释警告（BLI_virtual_array.hh:1176~1182）
/*
 * One has to be careful with nesting multiple devirtualizations,
 * because that results in an exponential number of function instantiations.
 *
 * 嵌套多个去虚拟化会导致指数级代码膨胀！
 * 2 个 varray × 3 种类型 = 9 个版本
 * 3 个 varray × 3 种类型 = 27 个版本
 */
```

```mermaid
flowchart LR
    subgraph "去虚拟化原理"
        A["VArray&lt;float&gt;"] --> CHECK["检查 common_info()"]
        CHECK -->|"Type::Span"| S["编译版本 1<br/>Span&lt;float&gt; 直接访问"]
        CHECK -->|"Type::Single"| SG["编译版本 2<br/>单值广播"]
        CHECK -->|"Type::Any"| F["编译版本 3<br/>虚函数回退"]
    end

    subgraph "代码膨胀警告"
        W1["1 个 varray → 3 版本"]
        W2["2 个 varray → 9 版本"]
        W3["3 个 varray → 27 版本 ⚠️"]
    end

    style S fill:#2ecc71,color:#fff
    style SG fill:#e67e22,color:#fff
    style F fill:#9b59b6,color:#fff
    style W3 fill:#e74c3c,color:#fff
```

---

## 10. GArray 与 GVArray 的协作

`GArray<>` 是 `Array<T>` 的泛型版本，拥有数据的所有权。它与 `GVArray` 的协作是几何节点中最常见的数据流转模式。

### 10.1 所有权语义对比

| 特性 | `GSpan` | `GArray<>` | `GVArray` |
|------|---------|-----------|-----------|
| 所有权 | 不拥有数据（视图） | 拥有数据（分配/释放） | 可选（取决于实现） |
| 可复制 | 浅拷贝（共享数据） | 深拷贝（复制数据） | 浅拷贝（共享 impl） |
| 大小可变 | 不可变 | 可变（`reinitialize`） | 不可变 |
| 析构行为 | 无 | `destruct_n` + 释放内存 | 释放 impl |
| 隐式转换为 GSpan | ✅ | ✅ | ✅（`is_span()` 时） |

### 10.2 GArray → GVArray：from_garray

```cpp
static GVArray from_garray(GArray<> array);
```

> **`from_garray` 的特殊之处**：`GArray<>` 拥有数据所有权，`GVArray` 需要保持数据存活。内部会创建一个适配器，持有 `GArray<>` 的共享指针，确保数据在 `GVArray` 存活期间不被释放。

### 10.3 典型数据流：GArray 作为字段求值缓冲区

这是几何节点中最常见的模式——将 `GArray` 作为 `FieldEvaluator` 的输出目标，求值后转为 `GVArray` 返回：

```mermaid
sequenceDiagram
    participant Node as 几何节点
    participant FE as FieldEvaluator
    participant GA as GArray
    participant GVA as GVArray

    Node->>GA: GArray<>(cpp_type, domain_size)
    Node->>FE: add_with_destination(field, array.as_mutable_span())
    Node->>FE: evaluate()
    FE->>GA: 字段求值结果写入
    Node->>GVA: GVArray::from_garray(std::move(array))
    Note over GVA: 所有权转移，零拷贝
```

**真实代码**（模糊属性节点）：

```cpp
const int64_t domain_size = context.attributes()->domain_size(context.domain());

GArray<> buffer_a(*type_, domain_size);  // ① 分配缓冲区

FieldEvaluator evaluator(context, domain_size);
evaluator.add_with_destination(value_field_, buffer_a.as_mutable_span());  // ② 求值目标
evaluator.evaluate();  // ③ 求值，结果写入 buffer_a

return GVArray::from_garray(std::move(buffer_a));  // ④ 零拷贝转为 GVArray
```

### 10.4 域转换中的 GArray

```cpp
// Corner → Point 域转换
static GVArray adapt_mesh_domain_corner_to_point(const Mesh &mesh, const GVArray &varray)
{
    GArray<> values(varray.type(), mesh.verts_num);  // ① 用目标域大小分配
    attribute_math::to_static_type(varray.type(), [&]<typename T>() {
        if constexpr (!std::is_void_v<attribute_math::DefaultMixer<T>>) {
            adapt_mesh_domain_corner_to_point_impl<T>(
                mesh, varray.typed<T>(),
                values.as_mutable_span().typed<T>());  // ② 类型化后填充
        }
    });
    return GVArray::from_garray(std::move(values));  // ③ 转为 GVArray
}
```

---

## 11. 在列表系统中的应用

### 11.1 GList 使用 GVArray

`GList` 的 `varray()` 方法返回 `GVArray`，将列表数据作为虚拟数组暴露：

```cpp
GVArray GList::varray() const
{
  return std::visit(
      [&](auto &&data) -> GVArray {
        using T = std::decay_t<decltype(data)>;
        if constexpr (std::is_same_v<T, ArrayData>) {
          if (data.sharing_info && data.sharing_info->is_mutable()) {
            return GVArray::from_span(GSpan(cpp_type_, data.data, size_));
          }
          return GVArray::from_span(GSpan(cpp_type_, data.data, size_));
        }
        if constexpr (std::is_same_v<T, SingleData>) {
          return GVArray::from_single_ref(cpp_type_, size_, data.value);
        }
      }, data_);
}
```

```mermaid
flowchart TD
    GList["GList"]
    AD["ArrayData<br/>const void* data"]
    SD["SingleData<br/>const void* value"]

    GList --> AD
    GList --> SD

    AD --> |"GVArray::from_span"| GVA1["GVArray (Span 模式)<br/>直接读取内存"]
    SD --> |"GVArray::from_single_ref"| GVA2["GVArray (Single 模式)<br/>所有索引返回同一个值"]

    GVA1 --> |"typed&lt;float&gt;()"| VA1["VArray&lt;float&gt;"]
    GVA2 --> |"typed&lt;float&gt;()"| VA2["VArray&lt;float&gt;"]

    style GVA1 fill:#3498db,color:#fff
    style GVA2 fill:#e67e22,color:#fff
```

### 11.2 List\<T\> 使用 VArray\<T\>

```cpp
template<typename T> VArray<T> List<T>::varray() const
{
  return list_.varray().template typed<T>();  // GVArray → VArray<T>
}
```

### 11.3 GList::from_garray 使用 GArray

```cpp
GListPtr GList::from_garray(GArray<> array)
{
  auto *sharable_data = new ImplicitSharedValue<GArray<>>(std::move(array));
  ArrayData array_data;
  array_data.data = sharable_data->data.data();
  array_data.sharing_info = ImplicitSharingPtr<>(sharable_data);
  return GList::create(array.data().type(), std::move(array_data), array.data().size());
}
```

### 11.4 Closure to List 使用 GArray

```cpp
// 快速路径：所有闭包结果都是单值
GArray<> array(type, count, NoInitialization());
threading::parallel_for(IndexRange(count), 128, [&](const IndexRange range) {
  for (const int list_i : range) {
    void *closure_result = const_cast<void *>(values[list_i].get_single_ptr_raw());
    type.move_construct(closure_result, array[list_i]);
  }
});
params.set_output(identifier, GList::from_garray(std::move(array)));
```

---

## 12. 总结速查表

### 概念速查

| 概念 | 一句话解释 |
|------|-----------|
| **VArray\<T\>** | "像数组一样用，但底层可能是数组/单值/函数" |
| **VArrayImpl_For_Span** | 底层包装连续数组，最快 |
| **VArrayImpl_For_Single** | 底层只有一个值，所有索引返回同一个 |
| **VArrayImpl_For_Func** | 底层是函数，按需计算 |
| **VArrayImpl_For_DerivedSpan** | 转换视图，底层 StructT[] 对外暴露为 ElemT[] |
| **CommonVArrayInfo** | 快速探测底层类型，用于优化分支 |
| **GVArray** | VArray 的类型擦除版，运行期才知道 `T` |
| **GVMutableArray** | GVArray 的可写版本 |
| **VArraySpan** | VArray → Span 的适配器，必要时拷贝 |
| **MutableVArraySpan** | 可写适配器，`save()` 写回机制 |
| **devirtualize_varray** | 编译期生成多版本，消除虚函数开销 |
| **GArray\<\>** | 泛型动态数组，拥有数据所有权，常与 GVArray 协作 |

### 场景选择

| 场景 | 推荐类型 |
|------|----------|
| 属性读取（如 `curves.cyclic()`） | `VArray<T>` |
| 字段求值结果 | `GVArray` → `typed<T>()` |
| 已知底层是数组，追求性能 | `Span<T>` |
| API 只接受 Span，但数据是 VArray | `VArraySpan<T>` |
| 需要修改 VArray 的数据 | `MutableVArraySpan<T>` + `save()` |
| 处理大量数据，虚函数开销显著 | `devirtualize_varray` |
| 运行期才知道类型的数据缓冲区 | `GArray<>` → `GVArray::from_garray()` |
| 列表数据作为虚拟数组 | `GList::varray()` → `GVArray` |

### 类关系总览

```mermaid
graph TB
    subgraph "编译期类型化"
        S["Span&lt;T&gt;"]
        MS["MutableSpan&lt;T&gt;"]
        VA["VArray&lt;T&gt;"]
        VMA["VMutableArray&lt;T&gt;"]
        A["Array&lt;T&gt;"]
    end

    subgraph "运行时泛型"
        GS["GSpan"]
        GMS["GMutableSpan"]
        GVA["GVArray"]
        GVMA["GVMutableArray"]
        GA["GArray&lt;&gt;"]
    end

    subgraph "类型信息"
        CT["CPPType"]
    end

    S --> GS
    MS --> GMS
    VA --> GVA
    VMA --> GVMA
    A --> GA

    GS --> CT
    GMS --> CT
    GVA --> CT
    GVMA --> CT
    GA --> CT

    GMS --> |"隐式转换"| GS
    GVMA --> |"隐式转换"| GVA
    GA --> |"隐式转换"| GS
    GA --> |"隐式转换"| GMS
    GA --> |"from_garray()"| GVA

    style GS fill:#3498db,color:#fff
    style GMS fill:#e67e22,color:#fff
    style GVA fill:#9b59b6,color:#fff
    style GA fill:#2ecc71,color:#fff
    style CT fill:#e74c3c,color:#fff
```

---

## 相关文件

| 文件 | 路径 |
|------|------|
| [BLI_virtual_array.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_virtual_array.hh) | `source/blender/blenlib/` |
| [BLI_generic_virtual_array.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_generic_virtual_array.hh) | `source/blender/blenlib/` |
| [BLI_generic_array.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_generic_array.hh) | `source/blender/blenlib/` |
| [BLI_generic_span.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_generic_span.hh) | `source/blender/blenlib/` |
| [BLI_cpp_type.hh](file:///e:/blender-git/blender/source/blender/blenlib/BLI_cpp_type.hh) | `source/blender/blenlib/` |
