# Array<T> - 固定大小数组

> `Array<T>` 是大小在构造时确定、之后不变的数组容器，比 `Vector` 更轻量

---

## 🎯 核心特性

```mermaid
flowchart TB
    subgraph Array特性["Array 核心特性"]
        A[固定大小] --> A1[构造后不可变]
        B[小对象优化] --> B1[小数据栈分配]
        C[RAII管理] --> C1[自动内存释放]
        D[默认初始化] --> D1[构造时初始化所有元素]
    end
    
    subgraph 对比Vector["对比 Vector"]
        E[Array] --> E1["大小固定\n更轻量"]
        F[Vector] --> F1["大小可变\n更灵活"]
    end
    
    Array特性 --> 对比Vector
    
    style A fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style E fill:#c8e6c9,stroke:#2e7d32
```

---

## 📦 内存布局

```mermaid
flowchart LR
    subgraph 小数组["小数组 (size <= InlineBufferCapacity)"]
        A[data_] --> B[内联缓冲区]
        C[size_] --> D[数组大小]
    end
    
    subgraph 大数组["大数组 (size > InlineBufferCapacity)"]
        E[data_] --> F[堆内存]
        G[size_] --> H[数组大小]
        I[inline_buffer_] --> J[未使用]
    end
    
    style B fill:#c8e6c9,stroke:#2e7d32
    style F fill:#fff3e0,stroke:#e65100
```

---

## 🚀 常用操作

### 构造

```cpp
#include "BLI_array.hh"

namespace blender::nodes {

void array_construct_examples() {
    // 1. 默认构造 - 空数组
    Array<int> arr1;
    BLI_assert(arr1.is_empty());
    
    // 2. 指定大小 - 默认初始化
    Array<float> arr2(100);  // 100个float，默认初始化为0
    
    // 3. 指定大小和初始值
    Array<int> arr3(10, 42);  // 10个42
    
    // 4. 从 Span 拷贝
    Vector<float> vec = {1.0f, 2.0f, 3.0f};
    Array<float> arr4(vec);  // 拷贝构造
    
    // 5. 初始化列表
    Array<int> arr5 = {1, 2, 3, 4, 5};
    
    // 6. 指定内联缓冲区大小
    Array<float3, 16> positions(10);  // 10个float3，内联缓冲区16个
}

} // namespace blender::nodes
```

### 访问元素

```cpp
void array_access_examples() {
    Array<int> arr = {10, 20, 30, 40, 50};
    
    // 1. 索引访问
    int val = arr[2];  // 30
    
    // 2. 首尾元素
    int first = arr.first();  // 10
    int last = arr.last();    // 50
    
    // 3. 指针访问
    const int *data = arr.data();
    
    // 4. 迭代
    for (int value : arr) {
        // 10, 20, 30, 40, 50
    }
    
    // 5. 索引范围
    for (int64_t i : arr.index_range()) {
        arr[i] *= 2;
    }
}
```

### 获取信息

```cpp
void array_info_examples() {
    Array<int> arr(100);
    
    // 大小
    int64_t size = arr.size();  // 100
    bool empty = arr.is_empty();  // false
    
    // 容量（Array中等于size）
    int64_t capacity = arr.capacity();  // 100
    
    // 是否在栈上
    bool is_inline = arr.is_inline();  // 取决于大小和InlineBufferCapacity
}
```

---

## 🔄 与 Span/Vector 互操作

```cpp
void array_interop_examples() {
    // Array → Span
    Array<float3> arr(100);
    Span<float3> span = arr;  // 隐式转换
    MutableSpan<float3> mspan = arr.as_mutable_span();
    
    // Array → Vector
    Vector<float3> vec(span);  // 拷贝构造
    
    // Span → Array
    Span<float3> some_span = get_data();
    Array<float3> arr2(some_span);  // 拷贝
}
```

---

## 🎯 节点开发中的典型用法

### 字段求值输出缓冲区

```cpp
static void node_geo_exec(GeoNodeExecParams params)
{
    GeometrySet geometry = params.extract_input<GeometrySet>("Geometry"_ustr);
    const Field<float> field = params.extract_input<Field<float>>("Value"_ustr);
    
    if (Mesh *mesh = geometry.get_mesh()) {
        const int64_t size = mesh->totvert;
        
        // 分配输出缓冲区
        Array<float> result(size);
        
        // 求值字段
        const bke::MeshFieldContext context(*mesh, bke::AttrDomain::Point);
        fn::FieldEvaluator evaluator(context, size);
        evaluator.add_with_destination(field, result.as_mutable_span());
        evaluator.evaluate();
        
        // 使用 result ...
    }
}
```

### 临时计算缓冲区

```cpp
static void process_with_temp_buffer(Span<float> input, MutableSpan<float> output)
{
    // 分配临时缓冲区
    Array<float> temp(input.size());
    
    // 第一阶段计算
    for (int64_t i : input.index_range()) {
        temp[i] = input[i] * 2.0f;
    }
    
    // 第二阶段计算
    for (int64_t i : input.index_range()) {
        output[i] = temp[i] + 1.0f;
    }
}
```

---

## ✅ 检查清单

- [ ] 理解 Array 大小固定
- [ ] 掌握构造方式
- [ ] 了解小对象优化
- [ ] 会用 as_mutable_span()
- [ ] 了解与 Vector 的区别

---

## 📁 相关文件

| 文件 | 路径 |
|-----|------|
| BLI_array.hh | `source/blender/blenlib/BLI_array.hh` |

---

## 🔗 相关文档

- [01_Vector.md](01_Vector.md) - 动态数组
- [02_Span.md](02_Span.md) - 非拥有视图
