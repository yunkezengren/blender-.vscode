# VArray<T> / GVArray / GSpan - 类型擦除数组

> 在不知道具体类型的情况下操作数组，是字段系统和属性系统的核心

---

## 📖 源码注释翻译与解释

### 虚拟数组文件头注释 (BLI_virtual_array.hh:7~26)

> **原文注释：**
> ```cpp
> /** \file
>  * \ingroup bli
>  *
>  * A virtual array is a data structure that behaves similarly to an array, but its elements are
>  * accessed through virtual methods. This improves the decoupling of a function from its callers,
>  * because it does not have to know exactly how the data is laid out in memory, or if it is stored
>  * in memory at all. It could just as well be computed on the fly.
>  *
>  * Taking a virtual array as parameter instead of a more specific non-virtual type has some
>  * tradeoffs. Access to individual elements of the individual elements is slower due to function
>  * call overhead. On the other hand, potential callers don't have to convert the data into the
>  * specific format required for the function. This can be a costly conversion if only few of the
>  * elements are accessed in end.
>  *
>  * Functions taking a virtual array as input can still optimize for different data layouts. For
>  * example, they can check if the array references contiguous memory internally or if it is the
>  * same value for all indices. Whether it is worth optimizing for different data layouts in a
>  * function has to be decided on a case by case basis. One should always do some benchmarking to
>  * see if the increased compile time and binary size is worth it.
>  */
> ```

**中文翻译与详细解释：**

| 段落 | 翻译 | 关键要点 |
|------|------|----------|
| **核心定义** | 虚拟数组是一种行为类似于数组的数据结构，但其元素通过虚方法访问。 | 虚方法访问元素 |
| **解耦优势** | 这提高了函数与其调用者的解耦，因为它不必确切知道数据在内存中的布局方式，或者它是否完全存储在内存中。 | 不关心内存布局 |
| **惰性计算** | 数据可以即时计算。 | 支持函数生成 |
| **权衡** | 使用虚拟数组作为参数而不是更具体的非虚拟类型有一些权衡。由于函数调用开销，访问单个元素较慢。 | 性能 vs 灵活性 |
| **避免转换** | 另一方面，潜在调用者不必将数据转换为函数所需的特定格式。如果最终只访问少数元素，这种转换可能代价高昂。 | 避免不必要的数据转换 |
| **优化可能** | 接受虚拟数组作为输入的函数仍然可以为不同的数据布局进行优化。例如，可以检查数组内部是否引用连续内存，或者所有索引的值是否相同。 | 可以检查底层类型优化 |
| **基准测试** | 函数中是否值得为不同数据布局进行优化必须根据具体情况决定。应该始终进行一些基准测试，看看增加的编译时间和二进制大小是否值得。 | 需要权衡编译时间/二进制大小 |

### CommonVArrayInfo 结构注释 (BLI_virtual_array.hh:43~71)

> **原文：**
> ```cpp
> /**
>  * Used to quickly check if a varray is a span or a single value. This struct also allows
>  * retrieving multiple pieces of data with a single virtual method call.
>  */
> struct CommonVArrayInfo {
>   enum class Type : uint8_t {
>     /* Is not one of the common special types below. */
>     Any,
>     Span,
>     Single,
>   };
>
>   Type type = Type::Any;
>
>   /** True when the #data becomes a dangling pointer when the virtual array is destructed. */
>   bool may_have_ownership = true;
>
>   /**
>    * Points either to nothing, a single value, or an array of values, depending on #type.
>    * If this is a span of a mutable virtual array, it is safe to cast away const.
>    */
>   const void *data;
>   ...
> };
> ```

**翻译：** 用于快速检查 varray 是否是 span 或单值。这个结构体还允许通过单次虚方法调用检索多段数据。

**字段说明：**

| 字段 | 说明 |
|------|------|
| `type` | 类型：Any（通用）、Span（连续数组）、Single（单值广播） |
| `may_have_ownership` | 当虚拟数组被销毁时，#data 是否变成悬垂指针 |
| `data` | 根据 #type 指向空、单值或值数组 |

### VArrayImpl 类注释 (BLI_virtual_array.hh:73~76)

> **原文：**
> ```cpp
> /**
>  * Implements the specifics of how the elements of a virtual array are accessed. It contains a
>  * bunch of virtual methods that are wrapped by #VArray.
>  */
> template<typename T> class VArrayImpl {
> ```

**翻译：** 实现虚拟数组元素访问的具体方式。它包含一组被 #VArray 包装的虚方法。

### size_ 成员注释 (BLI_virtual_array.hh:78~83)

> **原文：**
> ```cpp
> /**
>  * Number of elements in the virtual array. All virtual arrays have a size, but in some cases it
>  * may make sense to set it to the max value.
>  */
> int64_t size_;
> ```

**翻译：** 虚拟数组中的元素数量。所有虚拟数组都有大小，但在某些情况下将其设置为最大值可能有意义。

### get 方法注释 (BLI_virtual_array.hh:98~100)

> **原文：**
> ```cpp
> /**
>  * Get the element at #index. This does not return a reference, because the value may be computed
>  * on the fly.
>  */
> ```

**翻译：** 获取 #index 处的元素。这不返回引用，因为值可能是即时计算的。

**重要：** 返回的是值而非引用，因为底层可能是函数生成的值，没有实际的内存位置。

---

## 🎯 核心概念

```mermaid
flowchart TB
    subgraph 类型擦除层次["类型擦除层次"]
        A["VArray<T><br/>编译期类型"] --> B["GVArray<br/>运行期类型"]
        B --> C["GSpan<br/>只读视图"]
        B --> D["GMutableSpan<br/>可写视图"]
    end
    
    subgraph 使用场景["使用场景"]
        E["字段求值"] --> E1["GVArray 存储结果"]
        F["属性系统"] --> F1["GSpan 读取属性"]
        G["多函数"] --> G1["类型擦除参数"]
    end
    
    类型擦除层次 --> 使用场景
    
    style B fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style C fill:#fff3e0,stroke:#e65100
```

---

## 📦 VArray<T> - 虚拟数组

### 核心特性

`VArray<T>` 是一个**只读**的虚拟数组接口，底层可以是：
- 实际数组（`Array<T>`、`Vector<T>`）
- 单值广播（所有元素相同）
- 函数生成（按需计算）

```cpp
#include "BLI_virtual_array.hh"

namespace blender::nodes {

void varray_examples() {
    // 1. 从 Vector 构造
    Vector<float> vec = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f};
    VArray<float> varray1 = VArray<float>::ForContainer(vec);
    
    // 2. 单值广播（所有元素都是 42）
    VArray<float> varray2 = VArray<float>::ForSingle(42.0f, 1000);
    
    // 3. 函数生成（按需计算）
    VArray<float> varray3 = VArray<float>::ForFunc(
        100,
        [](const int64_t i) { return float(i) * 0.5f; }
    );
    
    // 4. 访问元素
    float val = varray1[0];  // 1.0f
    
    // 5. 检查是否为单值
    if (varray1.is_single()) {
        float single_val = varray1.get_internal_single();
    }
}

} // namespace blender::nodes
```

### 常用操作

```cpp
void varray_operations() {
    VArray<float> varray = get_varray();
    
    // 大小
    int64_t size = varray.size();
    bool empty = varray.is_empty();
    
    // 索引访问
    float val = varray[10];
    
    // 尝试获取内部数组（如果是实际数组）
    const float *data = varray.try_get_internal_single();
    
    // 遍历
    for (int64_t i : varray.index_range()) {
        float value = varray[i];
    }
    
    // 转换为 Span（如果可能）
    std::optional<Span<float>> span = varray.try_get_internal_span();
}
```

---

## 🌐 GVArray - 类型擦除的 VArray

### 核心概念

`GVArray` 是 `VArray<T>` 的类型擦除版本，在**运行期**才知道元素类型。

```mermaid
flowchart LR
    subgraph 编译期["编译期已知类型"]
        A["VArray<float3>"] --> B["具体类型操作"]
    end
    
    subgraph 运行期["运行期确定类型"]
        C["GVArray"] --> D["通过 CPPType 操作"]
        D --> E["type() 获取类型"]
        D --> F["typed<T>() 转换"]
    end
    
    style C fill:#e1f5fe,stroke:#01579b,stroke-width:3px
```

### 使用示例

```cpp
#include "BLI_virtual_array.hh"
#include "BLI_cpp_type.hh"

namespace blender::nodes {

void gvarray_examples() {
    // 1. 从 VArray<float3> 构造
    VArray<float3> typed_varray = VArray<float3>::ForSingle(float3(1, 2, 3), 100);
    GVArray gvarray(typed_varray);
    
    // 2. 获取类型
    const CPPType &type = gvarray.type();
    std::cout << "Type: " << type.name << std::endl;
    
    // 3. 类型检查
    if (gvarray.type() == CPPType::get<float3>()) {
        // 安全地转换为具体类型
        VArray<float3> typed = gvarray.typed<float3>();
        float3 val = typed[0];
    }
    
    // 4. 通用访问（类型擦除）
    void *buffer = MEM_mallocN(type.size, __func__);
    gvarray.get_to_uninitialized(0, buffer);  // 获取第0个元素
    type.destruct(buffer);
    MEM_freeN(buffer);
}

} // namespace blender::nodes
```

---

## 📏 GSpan - 类型擦除的 Span

### 核心概念

`GSpan` 是 `Span<T>` 的类型擦除版本，用于**只读**访问类型未知的数组。

```cpp
#include "BLI_span.hh"

namespace blender::nodes {

void gspan_examples() {
    // 1. 从 Span<float3> 构造
    Array<float3> positions(100);
    Span<float3> span = positions;
    GSpan gspan(span);
    
    // 2. 获取类型
    const CPPType &type = gspan.type();
    
    // 3. 类型检查并转换
    if (gspan.type() == CPPType::get<float3>()) {
        Span<float3> typed = gspan.typed<float3>();
        // 使用 typed...
    }
    
    // 4. 大小
    int64_t size = gspan.size();
    
    // 5. 元素访问（类型擦除）
    const void *element = gspan[0];  // 返回 void*
}

} // namespace blender::nodes
```

---

## ✏️ GMutableSpan - 类型擦除的可写 Span

```cpp
#include "BLI_span.hh"

namespace blender::nodes {

void gmutable_span_examples() {
    // 1. 构造
    Array<float> data(100);
    GMutableSpan gspan(CPPType::get<float>(), data.data(), data.size());
    
    // 2. 设置值
    float value = 42.0f;
    gspan.set(0, &value);  // 设置第0个元素
    
    // 3. 批量填充
    gspan.fill(&value);
    
    // 4. 从 GSpan 构造（拷贝）
    GSpan src = get_source_data();
    Array<uint8_t> buffer(src.type().size * src.size());
    GMutableSpan dst(src.type(), buffer.data(), src.size());
    dst.copy_from(src);
}

} // namespace blender::nodes
```

---

## 🎯 节点开发中的典型用法

### 模式 1：字段求值结果

```cpp
static void node_geo_exec(GeoNodeExecParams params)
{
    GeometrySet geometry = params.extract_input<GeometrySet>("Geometry"_ustr);
    const Field<float> field = params.extract_input<Field<float>>("Value"_ustr);
    
    if (Mesh *mesh = geometry.get_mesh()) {
        const bke::MeshFieldContext context(*mesh, bke::AttrDomain::Point);
        fn::FieldEvaluator evaluator(context, mesh->totvert);
        
        // 分配输出缓冲区
        Array<float> result(mesh->totvert);
        evaluator.add_with_destination(field, result.as_mutable_span());
        evaluator.evaluate();
        
        // result 现在包含字段求值结果
    }
}
```

### 模式 2：通用属性读取

```cpp
static void process_generic_attribute(const bke::AttributeAccessor &attributes,
                                      StringRef name)
{
    // 查找属性（返回 GVArray）
    std::optional<GVArray> attribute = attributes.lookup(name);
    if (!attribute) {
        return;
    }
    
    const CPPType &type = attribute->type();
    int64_t size = attribute->size();
    
    // 根据类型处理
    if (type == CPPType::get<float>()) {
        VArray<float> typed = attribute->typed<float>();
        for (int64_t i : typed.index_range()) {
            float value = typed[i];
            // 处理...
        }
    }
    else if (type == CPPType::get<float3>()) {
        VArray<float3> typed = attribute->typed<float3>();
        // 处理...
    }
}
```

### 模式 3：属性写入

```cpp
static void write_generic_attribute(bke::MutableAttributeAccessor &attributes,
                                    StringRef name,
                                    const CPPType &type,
                                    int64_t size)
{
    // 添加属性
    bke::GSpanAttributeWriter writer = attributes.lookup_or_add_for_write(
        name, bke::AttrDomain::Point, type);
    
    if (!writer) {
        return;
    }
    
    // 写入数据
    GMutableSpan span = writer.span;
    for (int64_t i : span.index_range()) {
        // 构造值并写入
        void *value = MEM_mallocN(type.size, __func__);
        type.default_construct(value);
        span.set(i, value);
        type.destruct(value);
        MEM_freeN(value);
    }
    
    writer.finish();
}
```

---

## 🔄 类型转换关系

```mermaid
flowchart TB
    subgraph 具体类型["编译期具体类型"]
        A["Span<float3>"] --> B["VArray<float3>"]
        C["MutableSpan<float3>"] --> D["VMutableArray<float3>"]
    end
    
    subgraph 类型擦除["运行期类型擦除"]
        E["GSpan"] --> F["GVArray"]
        G["GMutableSpan"] --> H["GVMutableArray"]
    end
    
    subgraph 转换["转换"]
        A --> E
        B --> F
        C --> G
        D --> H
        E -.->|typed<float3>| A
        F -.->|typed<float3>| B
    end
    
    style E fill:#e1f5fe,stroke:#01579b
    style F fill:#fff3e0,stroke:#e65100
```

---

## ✅ 检查清单

- [ ] 理解 VArray 的虚拟数组概念
- [ ] 掌握 GVArray 的类型擦除机制
- [ ] 会用 typed<T>() 进行类型转换
- [ ] 了解 GSpan 和 GMutableSpan 的区别
- [ ] 掌握字段求值中的缓冲区使用

---

## 📁 相关文件

| 文件 | 路径 |
|-----|------|
| BLI_virtual_array.hh | `source/blender/blenlib/BLI_virtual_array.hh` |
| BLI_span.hh | `source/blender/blenlib/BLI_span.hh` |
| BLI_cpp_type.hh | `source/blender/blenlib/BLI_cpp_type.hh` |

---

## 🔗 相关文档

- [09_CPPType.md](09_CPPType.md) - 类型擦除系统
- [10_Field.md](10_Field.md) - 字段系统
