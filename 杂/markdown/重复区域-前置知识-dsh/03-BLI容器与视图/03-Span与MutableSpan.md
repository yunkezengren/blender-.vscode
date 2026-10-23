# 03 · Span 与 MutableSpan

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](02-Span只读视图.md) · [下一篇](04-Vector与Array.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `MutableSpan<T>`——`Span` 的可写版本，它就在同一个头文件里（`BLI_span.hh` L447 起，没有独立的 `BLI_mutable_span.hh`）。主要源码：[`BLI_span.hh`](../../../source/blender/blenlib/BLI_span.hh)（681 行）。

## 先回答一个具体问题

> 既然有 `Span`，为什么还要 `MutableSpan`？直接让 `Span` 可写不行吗？

不行，理由不是风格，而是**类型系统能给什么保证**。如果 `Span<T>` 本身可写（像 `std::span<T>`），那么 `void f(Span<Foo> x)` 就同时意味着"能读"和"能写"，于是：从签名看不出函数会不会改你的数组；`const Vector<Foo>` 也能塞进来，const 白丢了；只想遍历的函数写错下标就静默污染调用方数据，编译器不报警。

Blender 的选择是**把"可写性"提到最外层的类型名上**，而不是塞进 `T` 的 const 限定里。调用点因此一眼可辨：

```cpp
void analyze(Span<const Foo> in);        // 我只看
void fill_all(MutableSpan<Foo> r_out);   // 我会写，你准备地方
```

所以 `MutableSpan` 不是"功能更强的 Span"，而是**另一种权限**：它牺牲了 Span 的一部分能力（不能从临时 `initializer_list` 构造、不能从 const 容器构造），换来"写"必须显式声明。

一句话定义：**`MutableSpan<T>` 是"指向别人拥有的数组"的（非 const 指针, 长度）对，允许改元素，但不允许改数组的形状。**

## 一个类型，两种写权限

文件头在讲 `Span` 与 `std::span` 差异时顺手给出了全景对照表（[BLI_span.hh · L22-L31](../../../source/blender/blenlib/BLI_span.hh#L22)）：

| `std::span` 写法 | Blender 等价 | 说明 |
| --- | --- | --- |
| `std::span<int>` | `MutableSpan<int>` | 可写数组 |
| `std::span<const int>` | `Span<int>` | 只读数组 |
| `std::span<int *>` | `MutableSpan<int *>` | 数组里装指针，指针本身可写 |
| `std::span<const int *>` | `MutableSpan<const int *>` | 指针可写，它指向的内容只读 |
| `std::span<int * const>` | `Span<int *>` | 指针本身只读，指向的内容可写 |
| `std::span<const int * const>` | `Span<const int *>` | 全只读 |

这张表揭示了两套机制的正交性：**数组整体的可写性**由 `Span` / `MutableSpan` 类型名决定；**元素自身的 const** 由模板参数 `T` 决定。在 `std::span` 里 const 被复用了两次（`span<const int>` 是数组只读，`span<int * const>` 是元素只读），读起来要数星号；Blender 把前者抽成类型名，于是只剩一层需要解读。原文说得很直白（L23-L25）：

> "`Span` is const by default. This is to avoid making things mutable when they don't have to be. To get a non-const span, you need to use `MutableSpan`."

文件头还给 MutableSpan 一条使用建议（L43-L47）：

> "`MutableSpan<T>` can be used when a function is supposed to return an array, the size of which is known before the function is called. One advantage of this approach is that the caller is responsible for allocation and deallocation."

这是它存在的**核心理由**：把"分配"和"填充"拆给两个人。还有一条容易忽略的警告（L49-L51）：

> "NOTE: When a function has a `MutableSpan<T>` output parameter and T is not a trivial type, then the function has to specify whether the referenced array is expected to be initialized or not."

这是 `MutableSpan` 比 `Span` **更容易出 UB** 的地方：写之前那块内存是"已构造的对象"还是"原始字节"，签名里看不出来。Span 因为只读，永远没这个问题。

## 类定义逐段

### 类型别名与两个成员（L448-L459）

```cpp
using value_type = T;
using pointer = T *;
using const_pointer = const T *;
using reference = T &;
using const_reference = const T &;
using iterator = T *;              // 注意：不是 const T *
using size_type = int64_t;
protected:
  T *data_ = nullptr;
  int64_t size_ = 0;
```

七个别名与 `Span` 同名同序，只有实际类型变了：

| 别名 | `Span<T>` | `MutableSpan<T>` |
| --- | --- | --- |
| `pointer` | `const T *` | `T *` |
| `reference` | `const T &` | `T &` |
| `iterator` | `const T *` | `T *` |
| `const_pointer` / `const_reference` | `const T *` / `const T &` | 同左（不变） |

保留两个"只读镜像"有实意义：泛型代码常写 `typename C::const_reference`，两套视图都能提取出同一个只读类型，模板便可同时接受 Span 和 MutableSpan。`iterator` 是裸指针而非自定义迭代器类，与 `Span` 一致——`std::sort`、`std::copy`、range-for 零成本可用。

成员与 `Span` 唯一的差别是 `data_` 的类型：`T *` 而不是 `const T *`；它是 `T *` 而非 `const T * const`，因为视图对象本身可重新赋值（拷贝赋值、`= default` 构造），视图可替换、指向的数组才有所有权问题。对象 16 字节（64 位），文件头 L56 明确要求 "should be passed by value"，所以全库的 `MutableSpan` 参数都按值传。

### 构造函数（L461-L494）

```cpp
constexpr MutableSpan() = default;

constexpr MutableSpan(T *start, const int64_t size) : data_(start), size_(size) {}

constexpr MutableSpan(std::vector<T> &vector) : MutableSpan(vector.data(), vector.size()) {}

template<std::size_t N>
constexpr MutableSpan(std::array<T, N> &array) : MutableSpan(array.data(), N) {}

template<typename U>
constexpr MutableSpan(MutableSpan<U> span)
  requires(is_span_convertible_pointer_v<U, T>)
    : data_(static_cast<T *>(span.data())), size_(span.size()) {}
```

**默认构造**给 `nullptr, 0`，是合法的空视图，可当"没有输出"的占位值。**指针 + 长度**是全库用得最多的一条，注意一处真实的不对称——`Span` 的对应构造函数里有 `BLI_assert(size >= 0)`（L96），`MutableSpan` 的这个**没有**，长度非负要自己保证。

**从 `std::vector<T> &` / `std::array<T, N> &`**：参数都是**非 const 引用**，这是语义约束的自然表达——`const std::vector<T>` 拿不到 `T *`，构造不出来。两条都是隐式的（无 `explicit`），所以能直接写 `MutableSpan<float> span = data;`。C 数组不走这两条，退化成"指针 + 长度"。

**从 `MutableSpan<U>` 转换**：约束 `is_span_convertible_pointer_v<U, T>`，定义在 [`BLI_memory_utils.hh` L251-L262](../../../source/blender/blenlib/BLI_memory_utils.hh#L251)：

```cpp
template<typename From, typename To>
inline constexpr bool is_span_convertible_pointer_v =
    std::is_pointer_v<From> && std::is_pointer_v<To> &&
    (std::is_same_v<From, To> ||
     std::is_same_v<std::remove_pointer_t<From>, std::remove_const_t<std::remove_pointer_t<To>>> ||
     (!std::is_const_v<std::remove_pointer_t<From>> && std::is_same_v<To, void *>) ||
     std::is_same_v<To, const void *>);
```

注释说得很清楚（L245-L250）：**允许加 const，允许转 `void *`，禁止去 const，禁止类层次上下转换**。于是 `MutableSpan<int *> → MutableSpan<const int *>` 可以，反过来不行。

最后是转换运算符（L484-L494）：到 `Span<T>` 的非模板精确转换（优先选中），加一个到 `Span<U>` 的加 const 版本：

```cpp
constexpr operator Span<T>() const { return Span<T>(data_, size_); }

template<typename U>
constexpr operator Span<U>() const
  requires(is_span_convertible_pointer_v<T, U>)
{
  return Span<U>(static_cast<const U *>(data_), size_);
}
```

于是任何接受 `Span<T>` 的函数都能直接吃 `MutableSpan<T>`——**收窄权限永远不需要写转换代码**。

## MutableSpan 独有的方法

| 能力 | `Span<T>` | `MutableSpan<T>` | 备注 |
| --- | --- | --- | --- |
| `size` / `size_in_bytes` / `is_empty` | 有 | 有 | 完全相同 |
| `data()` / `begin()` / `end()` | 返回 `const T *` | 返回 `T *` | 唯一差别 |
| `operator[]`、`first()`、`last()` | 返回 `const T &` | 返回 `T &` | 唯一差别 |
| `slice` / `slice_safe` | 返回 `Span` | 返回 `MutableSpan` | 切片保留写权限 |
| `drop_front` / `drop_back` / `take_*` | 返回 `Span` | 返回 `MutableSpan` | 同上 |
| `index_range` / `count` / `contains` / `contains_ptr` | 有 | 有 | 只读查询两边都有 |
| `cast<NewT>()` | 返回 `Span<NewT>` | 返回 `MutableSpan<NewT>` | L751 |
| `fill(value)` | **无** | 有 | 批量写 |
| `fill_indices(indices, value)` | **无** | 有 | 按索引批量写 |
| `reverse()` | **无** | 有 | 原地反转 |
| `copy_from(Span<T>)` | **无** | 有 | 批量拷贝 |
| `as_span()` | **无** | 有 | 显式转只读 |
| `initializer_list` 构造 | 有 | **无** | 临时数组不可写 |
| `has_duplicates__` / `intersects__` / `first_index(_try)` / `hash` / `==` | 有 | **无** | 只是没加，不是不能加 |

表里"Span 独有的只读查询"并非设计上排除 MutableSpan，只是没写——手里有 `MutableSpan` 时 `.as_span()` 一下就能调。真正**语义上无法共享**的只有三样：`initializer_list` 构造（临时对象不能改），以及所有"写"操作（Span 手里是 `const T *`，物理上做不到）。

### `fill` 与 `fill_indices`（L520-L539）

```cpp
constexpr void fill(const T &value) const { initialized_fill_n(data_, size_, value); }

template<typename IndexT> constexpr void fill_indices(Span<IndexT> indices, const T &value) const
{
  static_assert(std::is_integral_v<IndexT>);
  for (IndexT i : indices) {
    BLI_assert(i < size_);
    data_[i] = value;
  }
}
```

`fill` 转到 [`BLI_memory_utils.hh` L86](../../../source/blender/blenlib/BLI_memory_utils.hh#L86) 的 `std::fill_n`，没有花招。**关键细节：方法带 `const` 限定但它改数据**——`const` 修饰视图对象本身（`data_`、`size_` 没变），不是指向的数组，所以 `void clear_all(const MutableSpan<int> span) { span.fill(0); }` 合法。这是有意设计：若 `fill` 非 const，"用 `const MutableSpan<int>` 做输出"这种极常见情形就没法写。**"`const MutableSpan` 仍然可写"是正确且必须的行为，不是 bug。** 名字叫 `initialized_fill_n` 而非 `uninitialized_`，意味着它**假定那块内存已有活着的对象**，走赋值 `operator=` 而非 placement new——对裸 `MEM_mallocN` 的字节直接 `fill` 是错的，正是 L49-L51 那条 NOTE 警告的坑。

`fill_indices` 的用途是"把选中的位置设成同一个值"，最常见搭档是 `IndexMask`（几何节点的选择集），只碰 `indices` 里出现的位置，比 `fill` 省。**边界**：断言只有 `i < size_` 一条上界检查，若传进负数则 `-1 < size_` 为真、断言通过、然后写 `data_[-1]`——这是源码里已有的真实缺口，用的时候自己保证非负。

### `reverse`（L653-L661）

```cpp
constexpr void reverse() const
{
  for (const int i : IndexRange(size_ / 2)) {
    std::swap(data_[size_ - 1 - i], data_[i]);
  }
}
```

只遍历前一半，`std::swap` 对称换。空视图和单元素视图都自然正确（`size_ / 2 == 0`，循环一次不进）。测试 [`BLI_span_test.cc` L373-L394](../../../source/blender/blenlib/tests/BLI_span_test.cc#L373) 把 0/1/2/5 四种长度都测了。

### `copy_from`（L740-L749）

```cpp
/** Copy all values from another span into this span. This invokes undefined behavior when the
 * destination contains uninitialized data and T is not trivially copy constructible.
 * The size of both spans is expected to be the same. */
constexpr void copy_from(Span<T> values) const
{
  BLI_assert(size_ == values.size());
  initialized_copy_n(values.data(), size_, data_);
}
```

三个要点：参数是 `Span<T>`（源必须是只读视图，但这不增加传参难度，任何容器都能隐式转 `Span`）；**长度必须相等**（debug 断言，release 不检查，不是 `append` 也不会只拷 `min` 个，想拷一部分先 `slice`）；**目标必须是已初始化对象**（注释点名的 UB 条件）。

典型用法到处都是，如 [`node_geo_distribute_points_in_grid.cc` L220](../../../source/blender/nodes/geometry/nodes/node_geo_distribute_points_in_grid.cc#L220) 的 `pointcloud->positions_for_write().copy_from(positions)`——`for_write()` 返回的就是 `MutableSpan<float3>`。最小例子见 [`BLI_span_test.cc` L347-L358](../../../source/blender/blenlib/tests/BLI_span_test.cc#L347)。

### `as_span` 与 `cast<NewT>`（L663-L670、L751-L760）

```cpp
constexpr Span<T> as_span() const { return Span<T>(data_, size_); }

template<typename NewT> constexpr MutableSpan<NewT> cast() const
{
  BLI_assert((size_ * sizeof(T)) % sizeof(NewT) == 0);
  int64_t new_size = size_ * sizeof(T) / sizeof(NewT);
  return MutableSpan<NewT>(reinterpret_cast<NewT *>(data_), new_size);
}
```

`as_span` 的注释解释了它为何存在（L663-L666）：因为 `operator Span<T>()` 已经存在，绝大多数场合不用写；唯一理由是**模板类型推导**——`f(span)` 里若 `f` 是模板，编译器不会为推导做用户定义转换。`cast` 与 `Span::cast` 完全同构，只是返回可写版本，用于 `MutableSpan<void *> → MutableSpan<T *>` 这类（[`BLI_linear_allocator.hh` L204](../../../source/blender/blenlib/BLI_linear_allocator.hh#L204) 有一例）。断言只保证字节数整除，**元素类型兼容性由调用方负责**。

## 关键：为什么需要它

三个真实场景，全部来自本仓库。

### 场景一：批量填充一块已经存在的数据

几何节点执行器在调 lazy function 之前，要把输出口用途全置 `Used`、输入口全置 `Unused`（[`geometry_nodes_execute.cc` L576-L579](../../../source/blender/nodes/intern/geometry_nodes_execute.cc#L576)）：

```cpp
Array<lf::ValueUsage> param_output_usages(num_outputs);

param_output_usages.as_mutable_span().slice(function.outputs.main).fill(lf::ValueUsage::Used);
param_output_usages.as_mutable_span()
    .slice(function.outputs.input_usages)
    .fill(lf::ValueUsage::Unused);
```

注意 `as_mutable_span()` + `slice()` + `fill()` 三连。`Array` 拥有内存（[`BLI_array.hh` L259](../../../source/blender/blenlib/BLI_array.hh#L259)），`MutableSpan` 只借出来写，写完立即丢弃，整条链没有一次分配。没有它，写法会退化成 `for (int i = ...) arr[i] = ...`——啰嗦，且在不知道容器是 `Array` 还是 `std::vector` 的泛型代码里根本写不出 `std::fill`。

同理 [`node_geo_curve_handle_type_selection.cc` L52-L74](../../../source/blender/nodes/geometry/nodes/node_geo_curve_handle_type_selection.cc#L52) 用一个 `MutableSpan<bool>` 同时干两件事：`r_selection.slice(points).fill(false)` 整段清零，再 `r_selection[i_point] = ...` 逐点覆写。`fill` 负责批量、`operator[]` 负责精确，同一块内存上配合，中间没有拷贝。

### 场景二：把结果写进调用方预先分配的缓冲区

这正是文件头 L43-L47 说的"caller is responsible for allocation"。[`BLI_virtual_array.hh` L662](../../../source/blender/blenlib/BLI_virtual_array.hh#L662) 的 `void materialize(MutableSpan<T> r_span) const;` 是"把虚拟数组展开成一堆实值，塞进你给我那块地方"，[`BLI_index_mask.hh` L500](../../../source/blender/blenlib/BLI_index_mask.hh#L500) 的 `template<typename T> void to_indices(MutableSpan<T> r_indices) const;` 是"把掩码里的索引写成真正的整数数组"。两者都**不返回容器**，因为返回容器意味着被调方要替调用方选分配器和容器类型。

命名约定也在这里体现：`r_` 前缀表示 return 参数（`r_span`、`r_indices`、`r_cos`、`r_selection`），是 Blender C++ 代码的硬约定之一。看到 `MutableSpan` + `r_`，基本可断定"函数会往里写，长度由我保证"。同类还有 [`BKE_mesh_runtime.hh` L51](../../../source/blender/blenkernel/BKE_mesh_runtime.hh#L51) 的 `void mesh_get_mapped_verts_coords(const Mesh *mesh_eval, MutableSpan<float3> r_cos);`——一句话讲清"读这个，写那个"。

### 场景三：函数"我给你一块地方，你来填"

反向视角：调用方有块空间，被调方负责填。`IndexMask` 那组最典型（[`BLI_index_mask.hh` L496-L513](../../../source/blender/blenlib/BLI_index_mask.hh#L496)）：

```cpp
/**
 * Fill the provided span with the indices in the mask. The span is expected to have the same
 * size as the mask.
 */
template<typename T> void to_indices(MutableSpan<T> r_indices) const;

/**
 * Set the bools at indices in the mask to true and all others to false.
 */
void to_bools(MutableSpan<bool> r_bools) const;
```

注释里"expected to have the same size as the mask"就是契约，`MutableSpan` 把它写进了签名——尺寸不匹配时函数第一行就能断言，换成裸 `bool *` 连自己有多长都不知道。

## 与 Span 的互相转换

### `MutableSpan<T>` → `Span<T>`：永远可以

```cpp
MutableSpan<int> m(values, 5);
Span<int> a = m;            // operator Span<T>()
Span<int> b = m.as_span();  // 显式，帮模板推导
```

配合模板版本的 `operator Span<U>()`，还能顺手加 const。测试 [`BLI_span_test.cc` L428-L435](../../../source/blender/blenlib/tests/BLI_span_test.cc#L428) 把这组关系全写成了 `static_assert`：

```cpp
BLI_STATIC_ASSERT((std::is_convertible_v<MutableSpan<int>, Span<int>>), "");
BLI_STATIC_ASSERT((std::is_convertible_v<MutableSpan<int *>, Span<const int *>>), "");
BLI_STATIC_ASSERT((std::is_convertible_v<MutableSpan<int *>, MutableSpan<const int *>>), "");
BLI_STATIC_ASSERT((!std::is_convertible_v<MutableSpan<const int *>, MutableSpan<int *>>), "");
BLI_STATIC_ASSERT((!std::is_convertible_v<Span<const int *>, Span<int *>>), "");
BLI_STATIC_ASSERT((!std::is_convertible_v<Span<int *>, MutableSpan<const int *>>), "");
```

### `Span<T>` → `MutableSpan<T>`：不存在

`MutableSpan` 没有任何接受 `Span` 的构造函数。最后一行 `static_assert` 正是在验证这一点：即便 `T` 只是 `int *`（元素本身没被 const 化），`Span<int *> → MutableSpan<const int *>` 也被禁止。**因为"Span 保证我不写"是调用方的信任基础，任何一条到 MutableSpan 的隐式路径都会让这份信任失效。**

实在需要写，唯一的路是回到原始所有者：

```cpp
Vector<int> v = ...;
Span<int> s = v;                          // 从容器拿只读视图
MutableSpan<int> m = v.as_mutable_span(); // 要写就从容器重新拿（v 非 const）
```

`Vector::as_mutable_span()` 在 [`BLI_vector.hh` L395](../../../source/blender/blenlib/BLI_vector.hh#L395)，`Array::as_mutable_span()` 在 [`BLI_array.hh` L259](../../../source/blender/blenlib/BLI_array.hh#L259)，都要求非 const 的容器对象。

```text
   Vector<T> / Array<T> / std::vector<T> / std::array<T,N>   (拥有内存)
        │ as_span()          │ as_mutable_span()
        ▼                    ▼
     Span<T>  ◄────────  MutableSpan<T>     （operator Span<T>()，隐式）

   Span<T> ──✗──► MutableSpan<T>   （无路径，去 const 不允许）
```

## 为什么 SocketItemsRef 不是 MutableSpan

这是 Repeat 正篇（[02-03 SocketItems通用条目框架](../../重复区域-dsh/02-Repeat区域数据模型/03-SocketItems通用条目框架.md)）最关键的一处论证。原文只有一句话，在 [`NOD_socket_items.hh` L48-L56](../../../source/blender/nodes/NOD_socket_items.hh#L48)：

```cpp
/**
 * References a "C-Array" that is stored elsewhere. This is different from a MutableSpan, because
 * one can even resize the array through this reference.
 */
template<typename T> struct SocketItemsRef {
  T **items;
  int *items_num;
  int *active_index;
};
```

拆开看这三个字段，就明白为什么它必须是**指向指针的指针**：

| 字段 | 类型 | 它指向什么 |
| --- | --- | --- |
| `items` | `T **` | storage 里那个 `ItemT *items` 变量本身 |
| `items_num` | `int *` | storage 里那个 `int items_num` 变量本身 |
| `active_index` | `int *` | storage 里那个 `int active_index` 变量本身 |

`MutableSpan<T>` 存的是 `T *data_`（**值的拷贝**），`SocketItemsRef` 存的是 `T **items`（**变量本身的地址**）。这个"多一层"就是全部区别。

一次扩容要三件事同时发生：分配新内存、把新地址**写回持有者的变量**、更新长度**写回持有者的变量**。`MutableSpan` 连分配都不该管，后两步**物理上做不到**——它手里只有 `data_` 和 `size_` 两个副本，改了只改自己的字段，拥有者一无所知。`SocketItemsRef` 三个字段全是变量地址，于是 [`detail::add_item_to_array`](../../../source/blender/nodes/NOD_socket_items.hh#L194)（L194-L215）能做完整套动作：

```cpp
ItemT *new_items = MEM_new_array<ItemT>(new_items_num, __func__);
std::copy_n(old_items, old_items_num, new_items);
MEM_SAFE_DELETE(old_items);
*array.items = new_items;         // ← MutableSpan 做不到
*array.items_num = new_items_num; // ← MutableSpan 做不到
```

| 动作 | `MutableSpan<T>` | `SocketItemsRef<T>` |
| --- | --- | --- |
| 读/写第 i 个元素 | 可以 | 可以（`(*items)[i]`） |
| 批量 fill / copy | 可以 | 无直接接口，要自己循环 |
| 知道当前长度 | 可以（**快照值**） | 可以（`*items_num`，**实时值**） |
| **增加/删除元素、改容量、换内存块** | **不可以** | 可以 |
| **改 `active_index`** | 不可以（不知道有此字段） | 可以 |
| 释放数组 | 不可以 | 可以（`destruct_array`） |

所以两者的关系不是"谁更强"，而是**"视图" vs "句柄"**：`MutableSpan` 是**内容视图**，快照式（指针, 长度），拍下来就固定；`SocketItemsRef` 是**结构句柄**，每次用都解引用 storage 里的当前值，永远看得到最新状态。

同一份框架里三种用法同时存在：读用 `Span`（[`NOD_socket_items_blend.hh` L23](../../../source/blender/nodes/NOD_socket_items_blend.hh#L23) 的 `for (const ItemT &item : Span(*items.items, *items.items_num))`）、写内容用 `MutableSpan`（同文件 L33）、改结构用 `SocketItemsRef`。口诀：**形状变了用句柄，只改内容用 MutableSpan，只读用 Span。** 注意 `Span(*items.items, *items.items_num)` 是**在调用瞬间**拍的快照——若循环体内部可能触发 `add_item`（进而 realloc），这张快照立刻失效，见反例 5。

## 用小数据走一遍

取 5 个 `int`，全程跟踪底层数组变化。

```cpp
int values[5] = {10, 20, 30, 40, 50};
MutableSpan<int> span(values, 5);
```

此时 `span.data() == &values[0]`（同一地址，不是拷贝），`span.size() == 5`，`span[0]`、`span.first()` 都是 `10`，`span[4]`、`span.last()` 都是 `50`，`size_in_bytes()` 是 `20`，`index_range()` 是 `IndexRange(5)`。

**步骤 1：`fill` 整块覆盖。** `span.fill(7)` 之后 `values` 变成 `{7, 7, 7, 7, 7}`。`values` 本身变了，中间没有"转换"或"提交"步骤——它一直是同一块内存的视图。

**步骤 2：`slice` 拿到子视图并通过它写回。** `span.slice(1, 3).fill(0)` 之后是 `{7, 0, 0, 0, 7}`。切片返回的**仍是 `MutableSpan`**，所以写权限跟着走，这是 MutableSpan 与 Span 在切片上的关键区别。

**步骤 3：`operator[]` 精确写。** `auto mid = span.slice(1, 3); mid[0] = 42; span[0] = 99;` 之后是 `{99, 42, 0, 0, 7}`。注意 `mid[0]` 和 `span[1]` 是同一个位置——两个视图、一块内存。这是 span 语义最容易出事故的地方，也是它最大的性能优势。

**步骤 4：`copy_from` 从另一块内存整块搬。** `span.slice(2, 3).copy_from(Span(src, 3))`（`src = {1,2,3}`）之后是 `{99, 42, 1, 2, 3}`。断言要求 `size_ == values.size()`，这里 3 == 3；若写成 `slice(2, 2)` 配 `Span(src, 3)`，debug 下断言失败。

**步骤 5：窗口调整全是新对象。** `drop_front(2)` 给 `{1,2,3}`（`data()` 指向 `values[2]`），`take_front(2)` 给 `{99,42}`，`take_back(2)` 给 `{2,3}`，`drop_back(1)` 给 `{99,42,1,2}`。原 `span` 一字未改——这些方法都不动内存，只改两个字段的副本，这就是"视图"的本义。

**步骤 6：`reverse` 原地反转。** `span.reverse()` 之后 `{99, 42, 1, 2, 3}` 变成 `{3, 2, 1, 42, 99}`。循环只走 `size_ / 2 == 2` 次，交换 `(0,4)` 与 `(1,3)`，中间的 `values[2]` 不用动。

**步骤 7：收窄成只读，验证仍是同一块。** `Span<int> readonly = span;` 隐式转换成功，`readonly[0] = 1` 编译错误（`operator[]` 返回 `const int &`），而 `readonly.data() == span.data()` 为真。

几句总结：**整个过程零分配、零拷贝（除了 `copy_from` 那有意复制的 3 个 int），所有操作都在 `values` 这块栈内存上完成。** 这就是 `MutableSpan` 的全部价值——用两个字段的开销，把任意连续容器接进同一套写接口。

## 反例与边界

### 反例 1：用 `MutableSpan` 试图扩容

`span.push_back(6)` 和 `span.resize(10)` 都是编译错误——它只有 `size()`、没有 `resize()`，这是刻意的。它不知道内存从哪来（栈？`MEM_mallocN`？`std::vector` 的内部缓冲？），因此**没有资格重新分配**。想要扩容语义就得换类型：`Vector`（自己管内存）或 `SocketItemsRef`（知道 storage 里变量在哪）。Repeat 正篇必须用后者，根子就在这一条。

### 反例 2：从 const 容器构造 `MutableSpan`

`MutableSpan<int> span(v)` 对 `const std::vector<int> v` 是编译错误（要的是 `std::vector<T> &`）；`Span<int> s = v;` 没问题；但 `MutableSpan<int> m = s;` 也是编译错误（没有接受 `Span` 的构造函数）。**编译器在这里挡住了"去 const"。** 如果哪天发现自己写 `const_cast` 来绕这一步，先停下来想想：是真要写，还是接口设计错了？

### 反例 3：`slice` 越界（debug 断言，release 静默）

`slice` 里有 `BLI_assert(start + size <= size_ || size == 0)`（L583）。debug 构建会炸，**release 不会**——`span.slice(3, 4)`（长度 5）拿到一个长度 4 的视图指向 `values + 3`，往后越界 2 个元素，读写都是纯 UB。对比 `slice_safe`（L596-L602）用 `std::max(0, std::min(size, size_ - start))` 把长度夹到合法范围，`span.slice_safe(3, 4)` 给长度 2 的视图。**边界情况用 `slice_safe`，确定合法时用 `slice`**——前者慢一点点（两次 `min/max`），后者零成本但要求自己保证。顺带一个真实的不对称：`Span::slice_safe` 写的是 `Span(data_ ? data_ + start : nullptr, new_size)`（L163），对空视图做了保护；`MutableSpan::slice_safe` 没有这层保护（L601）。空视图上做 `slice_safe` 会算出 `nullptr + start` 这样的悬空指针——长度是 0、不解引用就没事，但仍值得知道。

### 反例 4：把 `MutableSpan` 存起来跨函数用

`class Cache { MutableSpan<Foo> cached_; };` 是危险写法。文件头 L53-L55 直接点名："Since the arrays are only referenced, it is generally unsafe to store a Span. When you store one, you should know who owns the memory."

存 `MutableSpan` 比存 `Span` 更危险，因为它多了"写"的能力——不仅可能在别人释放后读到垃圾，还可能**往垃圾上写**。正确做法：存拥有者（`Vector<Foo>`），或存变量地址级别的句柄（像 `SocketItemsRef`，至少每次解引用都拿最新值），或者就在调用栈上当参数传。全 Blender 的 `MutableSpan` 成员都是短生命周期对象内部的字段（`SimpleMixer::buffer_`、`NearestNQuery::nearest_` 之类），构造后立刻用完。

### 反例 5：在持有视图期间让底层容器 realloc

```cpp
Vector<int> v = {1, 2, 3};
MutableSpan<int> span = v.as_mutable_span();
v.append(4);        // 可能触发 realloc，v.data() 变了
span[0] = 99;       // span.data() 还是旧地址 → 悬空写
```

这是 span 类视图**最经典的事故**。`MutableSpan` 里的 `data_` 是**快照值**，不是"跟着容器走的引用"。容器扩容、`reserve`、`MEM_reallocN` 之后旧视图立即失效。`SocketItemsRef` 免疫这一条，就是因为它存的是 `T **` 而不是 `T *`。

### 反例 6：以为 `const MutableSpan` 不能写

`void f(const MutableSpan<int> span) { span[0] = 1; }` 是合法的，编译通过。`operator[]`、`fill`、`copy_from`、`reverse` 全带 `const` 限定，但都返回 `T &` 或直接写 `data_`。`const` 保护视图对象（不能把 `span` 重新指向别处），不保护指向的数据。若写成非 const，"传一个 `const MutableSpan` 做输出"就没法写，也与 `Span` 的行为无法对齐（`Span` 的所有方法都是 const）。理解这点，才不会在 review 时误判"这里漏了 const"。

### 反例 7：对未初始化内存 `fill` / `copy_from`

```cpp
Foo *raw = static_cast<Foo *>(MEM_mallocN(10 * sizeof(Foo), __func__));
MutableSpan<Foo> span(raw, 10);
span.fill(Foo{});   // UB：目标没有活着的对象
```

`fill` 走 `initialized_fill_n` → `std::fill_n` → `operator=`，对未构造的 `Foo` 调 `operator=` 是 UB（`std::string` 这类会直接崩）。正确做法是 [`BLI_memory_utils.hh` L91](../../../source/blender/blenlib/BLI_memory_utils.hh#L91) 的 `uninitialized_fill_n`（用 placement new）。判断规则：目标是容器里已有的元素 → 用 `fill`/`copy_from`；目标是 `MEM_mallocN` 出来的裸字节 → 先 construct 再拿 span，或直接调 `uninitialized_*` 系列。

### 反例 8：`fill_indices` 传负索引

如前述，只断言 `i < size_`，负值能通过（`span.fill_indices(Span(idx, 2), 0)` 配 `idx = {-1, 2}` 会写 `data_[-1]`）。索引来自 `IndexMask` 时天然安全（掩码里索引非负），来自用户输入或算术前要先夹一遍。

### 反例 9：以为 `MutableSpan` 能改形状

`void f(MutableSpan<int> items) { items = MutableSpan<int>(new_buffer, new_size); }` 里的赋值**只影响形参副本**，因为 `MutableSpan` 按值传递（正是推荐做法），调用方的容器、指针、长度一概不变。想真"换一块内存"，必须像 `SocketItemsRef` 那样手里有变量地址。

## 对理解 Repeat 的帮助

`MutableSpan` 在 Repeat 相关代码里的三个落点，正好对应正篇的三处论证：
| 位置 | 代码 | 意义 |
| --- | --- | --- |
| 02-02 存储与条目 | `MutableSpan<NodeRepeatItem> NodeGeometryRepeatOutput::items_span();` | 非 const 重载，给执行器就地改条目 |
| 02-03 通用条目框架 | `SocketItemsRef` 的注释与三个指针字段 | 论证"能改形状"必须用句柄 |
| 02-03 持久化 | `MutableSpan(*items.items, *items.items_num)` | 读 .blend 时逐条目就地写回 |

### 落点一：`items_span()` 的双重载

[`node_geo_repeat.cc` L362-L370](../../../source/blender/nodes/geometry/nodes/node_geo_repeat.cc#L362)：

```cpp
Span<NodeRepeatItem> NodeGeometryRepeatOutput::items_span() const
{
  return Span<NodeRepeatItem>(items, items_num);
}

MutableSpan<NodeRepeatItem> NodeGeometryRepeatOutput::items_span()
{
  return MutableSpan<NodeRepeatItem>(items, items_num);
}
```

经典的 const 重载模式，但有三点值得注意。第一，**两个实现体完全对称**，区别只在返回类型——这正是"可写性提到类型名上"的直接体现；按 `std::span` 风格会写成 `Span<NodeRepeatItem>` 与 `Span<const NodeRepeatItem>`，读者要数 const。第二，**声明在 DNA 头里**（[`DNA_node_types.h` L3571-L3574](../../../source/blender/makesdna/DNA_node_types.h#L3571)），外面套着 `#ifdef __cplusplus`，意味着这是纯 C++ 便利方法、不参与 SDNA 布局计算——DNA 结构体里只允许 `items`、`items_num`、`active_index`、`next_identifier`、`inspection_index` 这些真实字段（L3561-L3569）。第三，**它不做任何形状检查**，就是把两个字段打包；`items_num` 若因损坏文件而离谱，这个 span 就是超长的，校验发生在别处（`BLO_read_array_and_validate_size`）。同一模式在另外四个节点上重复出现：[`node_geo_combine_list.cc` L281-L289](../../../source/blender/nodes/geometry/nodes/node_geo_combine_list.cc#L281)、[`node_geo_index_switch.cc` L563-L570](../../../source/blender/nodes/geometry/nodes/node_geo_index_switch.cc#L563)、[`node_geo_simulation.cc` L832-L839](../../../source/blender/nodes/geometry/nodes/node_geo_simulation.cc#L832)、[`node_geo_rasterize_points.cc` L385-L392](../../../source/blender/nodes/geometry/nodes/node_geo_rasterize_points.cc#L385)——这是 `socket_items` 框架的统一约定：**每个 ItemT 的 storage 都提供一对 `items_span()` 重载**。

### 落点二：为什么 `SocketItemsRef` 不能换成 `MutableSpan`

本篇第三节已把它钉死：`MutableSpan` 的成员是 `T *data_` + `int64_t size_` 两个**值**；扩容需要写回"持有者的变量"，而它手里没有那些变量的地址；所以 `add_item_to_array` 里 `*array.items = new_items; *array.items_num = new_items_num;`（[`NOD_socket_items.hh` L208-L209](../../../source/blender/nodes/NOD_socket_items.hh#L208)）这两行在 `MutableSpan` 上**根本无法表达**。那句注释因此不是在说"`SocketItemsRef` 功能更多"，而是在说两者是不同类型的抽象：`MutableSpan<T>` 是"我指向一块**内容**"，`SocketItemsRef<T>` 是"我指向三个**变量**"。Repeat 的条目数组必须能增删（用户点一次"添加条目"就 realloc 一次），所以整条链路用的都是后者。

### 落点三：`MutableSpan(*items.items, *items.items_num)`

[`NOD_socket_items_blend.hh` L28-L36](../../../source/blender/nodes/NOD_socket_items_blend.hh#L28)：

```cpp
template<typename Accessor> inline void blend_read_data(BlendDataReader *reader, bNode &node)
{
  using ItemT = typename Accessor::ItemT;
  const SocketItemsRef<ItemT> items = Accessor::get_items_from_node(node);
  BLO_read_array_and_validate_size(reader, items.items, items.items_num);
  for (ItemT &item : MutableSpan(*items.items, *items.items_num)) {
    Accessor::blend_read_data_item(reader, item);
  }
}
```

- `const SocketItemsRef<ItemT> items`——句柄本身 const（不会改它指向哪个变量），但 `items.items` 是 `ItemT **`，解引用仍能读写 storage；
- `BLO_read_array_and_validate_size(...)` 先让重载系统把数组恢复出来并校验 `items_num` 合法；
- `MutableSpan(*items.items, *items.items_num)` **在循环开始前拍快照**。这里安全，因为循环体只重建条目内部的堆资源（`RepeatItemsAccessor` 的实现是 `BLO_read_string(reader, &item.name)`），**绝不会 realloc 数组本身**；
- `for (ItemT &item : ...)` 的 `&` 是关键——它让 `item` 是可变引用，能传给 `ItemT &` 形参；`MutableSpan::begin()/end()` 返回 `T *`，range-for 因此推导出 `ItemT &`。

对照组是同文件 L23 的 `blend_write`，那里写的是 `for (const ItemT &item : Span(*items.items, *items.items_num))`。**写文件用 `Span` + `const ItemT &`，读文件用 `MutableSpan` + `ItemT &`。** 一对函数、一对视图、一对引用限定，语义分毫不差——这两行是本篇最值得记住的模板，用最少的字演示完了权限模型。

假设有人把 `blend_read_data` 那行顺手写成读者更容易写出的 `Span`（配 `const ItemT &`），`blend_read_data_item(BlendDataReader *, ItemT &)` 要非 const 引用，绑不上——**编译器立刻抓住**。这就是把可写性放进类型名的日常收益：错误在编译期暴露，而不是等到运行时发现数据没被读回来。

## 继续阅读

- 上一篇：[02-Span只读视图](02-Span只读视图.md) —— 同一文件的 L74-L445
- 下一篇：[04-Vector与Array](04-Vector与Array.md) —— `as_mutable_span()` 的两个主要来源
- 本章导航：[03-BLI容器与视图](README.md) · 前置总入口：[前置知识总入口](../README.md)
- 相关：[05-VectorSet稳定索引](05-VectorSet稳定索引.md) —— 另一种"稳定引用"的思路，可与 `SocketItemsRef` 对照
- 正篇：[02-03 SocketItems通用条目框架](../../重复区域-dsh/02-Repeat区域数据模型/03-SocketItems通用条目框架.md) —— 本篇末节的完整论证
- 正篇：[02-02 DNA存储与NodeRepeatItem](../../重复区域-dsh/02-Repeat区域数据模型/02-DNA存储与NodeRepeatItem.md) —— `items_span()` 的 DNA 侧声明
