# 02 · SocketValueVariant

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](01-CPPType运行时类型.md) · [下一篇](03-类型转换与访问接口.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `SocketValueVariant`——几何节点 socket 值的统一容器。它是 Repeat 展开图里所有通道的类型。主要源码：[`BKE_node_socket_value.hh`](../../../source/blender/blenkernel/BKE_node_socket_value.hh)（实测 434 行）、[`BLI_any.hh`](../../../source/blender/blenlib/BLI_any.hh)（366 行）。

## 先回答一个具体问题

一个整数 socket 可以传一个 int，也可以传一个 field。同一个容器怎么装这两种完全不同的东西？

答案是 `SocketValueVariant`。而且这个答案比想象的复杂——它不只是"union"，而是**类型擦除 + 运行时转换**。

## 官方定位（文件头注释逐句读）

`[讲解]` `BKE_node_socket_value.hh` 的类注释（L94-L110）是最高密度的说明，逐句拆：

### 第一句：用途

> "#SocketValueVariant is used to pass data between nodes, e.g. by geometry nodes in the lazy function evaluator. Specifically, it is the container type for the following socket types: bool, float, integer, vector, rotation, color and string."

`[讲解]` 关键信息：

- 它**不是**给用户的 API，是节点间的**传输格式**；
- 覆盖 7 种 socket 类型（bool / float / int / vector / rotation / color / string）。

**注意**：Geometry、Instances 等复合类型不在这 7 种里——它们由其他机制承载（GeometrySet 直接装进 variant，但 socket 类型层面是 `SOCK_GEOMETRY`）。

### 第二句：三种存储形态

> "The data passed through e.g. an integer socket can be a single value, a field or a grid (and in the lists and images). Each of those is stored differently, but this container can store them all."

`[讲解]` 这是核心洞察：**同一个 socket 类型有四种存储形态**。

看源码的枚举（L33-L38）：

```cpp
enum class SocketValueStorageKind : uint8_t {
  Single,
  Field,
  List,
  Grid,
};
```

| 形态 | 含义 | 例子 |
| --- | --- | --- |
| `Single` | 一个具体的值 | `int 42` |
| `Field` | 一个延迟求值的表达式 | `GField`（"每个点的位置"） |
| `List` | 一列值 | `GListPtr` |
| `Grid` | 体素网格 | `GVolumeGrid`（需 `WITH_OPENVDB`） |

`[讲解]` 为什么需要区分？因为一个"整数 socket"可能接：

- 用户输入的常量 `5` → Single；
- 一个 Position 节点的输出 → Field；
- 一个列表的某个元素 → List。

**这三种东西在内存里完全不同**，但用户看到的都是"整数 socket"。

### 第三句：为什么必须类型擦除

> "A key requirement for this container is that it is type-erased, i.e. not all code that uses it has to include all the headers required to process the other storage types. This is achieved by using the #Any type and by providing templated accessors that are implemented outside of a header."

`[讲解]` 这是工程上的关键约束：

如果不做类型擦除，每个用 `SocketValueVariant` 的地方都要 include：

- `FN_field.hh`（为了 Field）
- `BKE_list.hh`（为了 List）
- OpenVDB 头（为了 Grid，编译时间巨大）

而实际上**大部分代码只需要"传递"它，不需要"处理"它**。所以：

- 用 `Any` 做类型擦除（只存字节 + 类型信息）；
- **访问器（模板）定义在 .cc 里**，头文件只声明。

这是"编译防火墙"的经典应用。

### 第四句：隐式转换

> "This container is also able to do implicit conversions between the different types, with the #ensure_type() methods."

`[讲解]` `ensure_type<T>()` 能做类型转换。正篇 03-03 就有：

```cpp
params.get_input<SocketValueVariant>(zone_info_.indices.inputs.main[0])
    .ensure_type<int>()
```

`[讲解]` 这里 `.ensure_type<int>()` 把 variant 转成 int。如果里面装的是 float，会**转换**（不是失败）。这是"隐式转换"的含义。

## 内部结构

`[讲解]` 类定义的核心（L111-L122）：

```cpp
class SocketValueVariant {
 private:
  using Info = detail::SocketValueVariantTypeInfo;

  detail::SocketValueVariantAny value_;

  template<typename T> using to_storage_type = typename detail::storage_type<T>::type;
  ...
};
```

`[讲解]` 只有**一个成员** `value_`，类型是 `SocketValueVariantAny`。

看它的定义（L50）：

```cpp
using SocketValueVariantAny = Any<SocketValueVariantTypeInfo, 32, 16>;
```

`[讲解]` 三个模板参数：

| 参数 | 值 | 含义 |
| --- | --- | --- |
| `SocketValueVariantTypeInfo` | 类型 | 携带的运行时类型信息 |
| `32` | 字节 | **内联缓冲区大小** |
| `16` | 字节 | 对齐要求 |

`[讲解]` 32/16 的选择很关键：

- **32 字节够装大多数值**：`int`（4）、`float`（4）、`float3`（12）、`std::string`（32）都能内联；
- **超过 32 字节**（比如 `GeometrySet`）就**堆分配**。

这意味着小值**零堆分配**——这是性能关键。

## TypeInfo：三个函数指针

`[讲解]` `Any` 需要一个"类型信息"载体。`SocketValueVariantTypeInfo`（L52-L73）：

```cpp
struct SocketValueVariantTypeInfo {
  const CPPType &type;
  bool (*convert_to)(const CPPType &dst_type, SocketValueVariantAny &value);
  bool (*is_interpretable_as)(const CPPType &dst_type, const SocketValueVariantAny &value);
  SocketValueStorageKind storage_kind;
};
```

`[讲解]` 四个字段：

| 字段 | 用途 |
| --- | --- |
| `type` | 指向 `CPPType`（上一篇讲的运行时类型） |
| `convert_to` | 函数指针：能否转换到目标类型（并就地转换） |
| `is_interpretable_as` | 函数指针：能否按目标类型"解释"（不改数据） |
| `storage_kind` | 四种存储形态之一 |

`[讲解]` 两个函数指针的区别很微妙：

- **`convert_to`**：真的转换数据（float → int 要改数值）；
- **`is_interpretable_as`**：只是重新解释（`GField` 与 `Field<int>` 布局相同，可以直接当另一种看）。

**为什么需要后者？** 看 L117-L121 的注释：

> "Some types have a generic and compile-time version. For example, there is #GField and #Field<T>. Those are expected to have the same memory layout so that references can be cast between them. The #Any always stores the generic version if it exists."

`[讲解]` 关键：`Any` 里**总是存 generic 版本**（`GField`），而不是 typed 版本（`Field<int>`）。因为存储时不知道具体类型。

取用时如果用户要 `Field<int>`，就靠 `is_interpretable_as` 做零成本转换（`reinterpret_cast`，因为布局相同）。

## storage_type 的映射

`[讲解]` 上面那句"总是存 generic 版本"由这段实现（L75-L90）：

```cpp
template<typename T>
concept has_generic_type = requires { typename T::generic_type; };
template<typename T> struct storage_type {
  using type = T;
};
template<has_generic_type T> struct storage_type<T> {
  using type = typename T::generic_type;
};

inline const CPPType &to_storage_type(const CPPType &type)
{
  if (type.generic_type) {
    return *type.generic_type;
  }
  return type;
}
```

`[讲解]` 逻辑：

1. 如果类型有 `generic_type` 成员（如 `Field<int>` 有 `generic_type = GField`），就用它；
2. 否则用类型本身（如 `int`）。

**这是"类型擦除 + 泛型投影"的组合技巧**：存储层只用泛型类型，具体类型在访问时投影出来。

## SocketValueStorageKind 的编译期推导

`[讲解]` L40-L47：

```cpp
template<typename T>
inline constexpr SocketValueStorageKind socket_value_storage_kind =
    std::is_same_v<T, fn::GField> ? SocketValueStorageKind::Field :
    std::is_same_v<T, GListPtr>   ? SocketValueStorageKind::List :
#ifdef WITH_OPENVDB
    std::is_same_v<T, volume_grid::GVolumeGrid> ? SocketValueStorageKind::Grid :
#endif
                                                  SocketValueStorageKind::Single;
```

`[讲解]` 一个 `if constexpr` 风格的模板变量，**编译期**决定存储形态。

注意 `#ifdef WITH_OPENVDB`：没有 OpenVDB 时，Grid 形态不存在。这是**编译期裁剪**——不装 OpenVDB 就不会有任何 Grid 相关代码。

## 构造函数

`[讲解]` L128-L137：

```cpp
SocketValueVariant() = default;

template<typename T>
explicit SocketValueVariant(T &&value)
    requires(std::is_trivial_v<std::decay_t<T>> || is_same_any_v<std::decay_t<T>, std::string>);
```

`[讲解]` 两个要点：

1. **默认构造 = 空 variant**（L126-L127 注释："This is not valid for any socket type yet"）。
2. **模板构造受约束**：只接受 **trivial 类型**或 `std::string`。

`[讲解]` 为什么这么约束？看 L136 的注释："Required to avoid overriding the copy/move-constructors."

如果模板构造接受任何类型，它会和拷贝/移动构造冲突（比如 `SocketValueVariant(other_variant)` 会走模板而不是拷贝构造）。加约束能避免。

**复杂类型怎么办？** L131-L132 说："For more complex types, one can use the #from or #construct_in utilities."

## 在 Repeat 中的五处用法

`[讲解]` 正篇里 `SocketValueVariant` 出现在五个关键位置：

| 位置 | 代码 | 作用 |
| --- | --- | --- |
| 图接口类型 | `CPPType::get<SocketValueVariant>()` | 所有 main 通道的类型 |
| 读迭代数 | `params.get_input<SocketValueVariant>(...).ensure_type<int>()` | 提取 int |
| 预填充轮次值 | `Array<SocketValueVariant> index_values` | N 个常量 |
| 未使用哨兵 | `static const SocketValueVariant static_unused_index{-1}` | -1 占位 |
| 引用集通道 | `CPPType::get<GeometryNodesReferenceSet>()` | **不是** variant，是独立类型 |

`[讲解]` 最后一行值得强调：reference set **不走** `SocketValueVariant`，而是用独立类型 `GeometryNodesReferenceSet`。因为它不需要变体能力（永远就是那个类型）。

## 用小数据走一遍

`[讲解]` 三个场景，看 `Any` 的 32 字节缓冲怎么用：

**场景 A：`int 42`**

```text
SocketValueVariant{42}
  value_.type_info = &TypeInfo<int>
  value_.buffer   = [42][0][0]...[0]      （4 字节 + 28 字节未用）
  storage_kind    = Single
  堆分配：无
```

**场景 B：`float3{1,2,3}`**

```text
SocketValueVariant{float3{1,2,3}}
  value_.buffer = [1.0][2.0][3.0][0]...   （12 字节 + 20 字节未用）
  堆分配：无
```

**场景 C：`std::string("hello")`**

```text
std::string 是 32 字节（libstdc++ 的 SSO 结构）
  value_.buffer = [string 对象 32 字节]    （刚好装满）
  堆分配：无（但 string 内部的短字符串也在 SSO 缓冲里）
```

**场景 D：`GeometrySet`**

```text
GeometrySet 超过 32 字节
  value_.buffer = [指针][...]             （指向堆上的 GeometrySet）
  堆分配：有
```

`[讲解]` 四个场景说明：**32 字节覆盖了绝大多数 socket 值**。只有复合类型（GeometrySet、GListPtr 等）才堆分配。

## 反例与边界

### 反例 1：以为默认构造的 variant 可用

```cpp
SocketValueVariant v;       // 空
v.ensure_type<int>();       // 失败或崩溃
```

必须先赋值。

### 反例 2：以为 `ensure_type` 一定成功

它会尝试转换，但不保证。类型不兼容时返回失败（或断言）。

### 反例 3：存 Field 时要 `Field<int>` 

`Any` 只存 `GField`（generic）。要 typed 引用时靠 `is_interpretable_as` 投影——不能指望里面真的是 `Field<int>`。

### 反例 4：以为 32 字节缓冲是无限的

超过 32 字节会堆分配，性能敏感场景要注意。

### 反例 5：忘记 include 对应头文件

类型擦除的**好处**是头文件轻，**代价**是访问器的模板实现在 .cc 里——你需要 include 具体类型的头文件才能用 typed 访问。

### 反例 6：以为 variant 是 union

union 只存最大成员的大小且不能放非 POD。variant 是"类型擦除容器 + 运行时类型信息"，能力完全不同。

## 对理解 Repeat 的帮助

`[讲解]` 三处直接相关：

| 概念 | Repeat 中的体现 | 正篇位置 |
| --- | --- | --- |
| 统一接口类型 | 所有 main 通道都是 `SocketValueVariant` | 03-01、03-02、03-03 |
| `ensure_type<int>` | 读迭代数 | 03-03 L129-L135 |
| `emplace<int>(i)` | 预填充 `index_values` | 03-03 L263-L272 |

`[讲解]` 最后一行的意义：`Array<SocketValueVariant> index_values` 里存的是 N 个 `int`——但因为图接口要求 `SocketValueVariant`，所以不能直接用 `Array<int>`。

这解释了为什么正篇 03-03 要写 `emplace<int>(i)` 而不是 `index_values[i] = i`：**必须在 variant 里就地构造 int**。

## 继续阅读

- [03-类型转换与访问接口](03-类型转换与访问接口.md) —— `ensure_type`/`get`/`extract` 的完整语义
- [01-CPPType运行时类型](01-CPPType运行时类型.md) —— variant 依赖的类型信息
- [04-移动语义与内存布局](04-移动语义与内存布局.md) —— 为什么预分配能复用

---

## 深读篇：Any 容器的工作机制

`SocketValueVariant` 的成员只有一个 `Any`。理解 `Any` 才能理解它的性能与限制。

### Any 的三个模板参数

```cpp
using SocketValueVariantAny = Any<SocketValueVariantTypeInfo, 32, 16>;
```

`[讲解]` 逐个：

| 参数 | 值 | 语义 |
| --- | --- | --- |
| 类型信息 | `SocketValueVariantTypeInfo` | 携带 type / convert_to / is_interpretable_as / storage_kind |
| 内联容量 | 32 字节 | ≤32 字节的值直接存在对象内 |
| 对齐 | 16 字节 | 保证 SIMD 类型（float4）正确对齐 |

`[讲解]` **16 字节对齐很关键**。`float4` 是 16 字节、`double3` 需要 8 字节对齐。如果对齐不足，SIMD 指令会崩（或性能骤降）。

### 内联 vs 堆分配的分界

```text
值大小 ≤ 32 字节 → 内联（对象内 32 字节缓冲）
值大小 > 32 字节 → 堆分配（缓冲里存指针）
```

`[讲解]` 常见类型的大小：

| 类型 | 大小 | 内联？ |
| --- | --- | --- |
| `bool` | 1 | ✅ |
| `int` | 4 | ✅ |
| `float` | 4 | ✅ |
| `float3` | 12 | ✅ |
| `float4` / `Color` | 16 | ✅ |
| `std::string`（libstdc++） | 32 | ✅ 刚好 |
| `GField` | 取决于实现 | 通常 ✅ |
| `GeometrySet` | > 32 | ❌ 堆 |
| `GListPtr` | 24-32 | 临界 |

`[讲解]` 两个观察：

1. **绝大多数标量类型内联**——零堆分配；
2. **`std::string` 刚好 32 字节**——这是巧合还是设计？大概率是设计时挑的边界值。

### 移动语义如何工作

`[讲解]` `Any` 的移动构造只需：

1. 复制 32 字节缓冲（memcpy）；
2. 转移类型信息指针；
3. 如果原来是堆分配，把指针移过来（源置空）。

`[讲解]` **没有析构开销**——因为内联时不需要释放。这解释了正篇 06-02 讲的"移动很便宜"。

### 为什么 `Array<SocketValueVariant>` 能预分配复用

`[讲解]` 正篇 03-03 的做法：

```cpp
eval_storage.index_values.reinitialize(iterations);
threading::parallel_for(IndexRange(iterations), 1024, [&](const IndexRange range) {
  for (const int i : range) {
    eval_storage.index_values[i].emplace<int>(i);
  }
});
```

`[讲解]` 这里 `emplace<int>(i)` 对**已构造**的 variant 就地赋值。

**为什么能这样做？** 因为 `Array<T>::reinitialize` 会先默认构造每个元素（空的 variant），然后 `emplace` 覆盖。空 variant 没有堆分配，覆盖也没有释放——**零成本**。

如果换成 `Vector<int>` 就没这个问题，但图接口要求 `SocketValueVariant`——这是类型匹配的代价。

### 转换的两个层次

`[讲解]` `SocketValueVariantTypeInfo` 有两个函数指针，对应两种转换：

**层次 1：`is_interpretable_as`（零成本）**

```text
GField  → Field<int>     布局相同，reinterpret_cast
```

不改数据，只是"换个类型标签看"。

**层次 2：`convert_to`（有成本）**

```text
float 1.5  → int 1       要实际改数值
```

会分配新值、转换、替换。

`[讲解]` 判断顺序：先试 `is_interpretable_as`（便宜），失败再试 `convert_to`（贵）。这是典型的"快路径优先"。

## 与 CPPType 的分工再强调

`[讲解]` 两个类型容易混淆，用一张表定死：

| | `CPPType` | `SocketValueVariant` |
| --- | --- | --- |
| 是什么 | 类型的**描述**（元数据） | 值的**容器**（数据） |
| 有数据吗 | 没有 | 有（32 字节缓冲或堆） |
| 一处还是多处 | 每个类型一个全局实例 | 每个值一个实例 |
| 谁引用谁 | — | variant 持有 `const CPPType&` |

`[讲解]` 一句话：**CPPType 是"图纸"，SocketValueVariant 是"按图纸造出来的箱子"**。

## 三个真实使用模式

`[讲解]` 从正篇提炼三种用法：

### 模式 1：纯传递

```cpp
/* 从上游拿到，原样传给下游 */
const SocketValueVariant &value = params.get_input<SocketValueVariant>(index);
/* ... 不改，直接透传 ... */
```

`[讲解]` 这是最常见的——不需要知道里面是什么类型。类型擦除的全部价值在这里。

### 模式 2：提取已知类型

```cpp
const int iterations = params.get_input<SocketValueVariant>(index).ensure_type<int>();
```

`[讲解]` 当你知道接口约定（Iterations 一定是 int）时，直接提取。

**风险**：如果上游接错（比如接了 float），`ensure_type<int>()` 会尝试转换（1.5 → 1）而不是报错。这是宽松的。

### 模式 3：构造常量

```cpp
static const SocketValueVariant static_unused_index{-1};
```

`[讲解]` 静态常量 variant，一次构造、永久复用。正篇用 `-1` 表示"iteration 未使用"。

## 性能的三个数据点

`[讲解]` 从源码结构能推出的量级（非实测，是结构性估计）：

| 操作 | 成本 | 原因 |
| --- | --- | --- |
| 内联类型的构造 | ~memcpy(32) | 一次 32 字节拷贝 |
| 内联类型的移动 | ~memcpy(32) | 同上 |
| 堆类型的构造 | malloc + memcpy | 堆分配开销 |
| `ensure_type<int>`（同类型） | ~指针比较 | 无需转换 |
| `ensure_type`（跨类型） | 转换函数调用 | 有实际计算 |

`[讲解]` 关键结论：**同类型取出几乎免费**，所以正篇里大量 `get_input<SocketValueVariant>(...).ensure_type<int>()` 不是性能瓶颈。

## 反例补遗

### 反例 7：以为 `Any` 是 `std::any`

`std::any` 用堆分配小对象 + RTTI；Blender 的 `Any` 是内联缓冲 + 自定义类型信息，**不需要 RTTI**（Blender 编译时可能禁用 RTTI）。

### 反例 8：跨线程共享同一个 variant

variant 不是线程安全的。多个线程同时 `emplace` 同一个 variant 会竞态。

### 反例 9：把 `ensure_type` 当校验用

它做转换，不做校验。想校验要用 `is_type<T>()` 之类。

## 与 Repeat 的完整对应

`[讲解]` 把本篇与正篇对上：

| 正篇代码 | 本篇概念 |
| --- | --- |
| `CPPType::get<SocketValueVariant>()` | 图的接口类型用 variant 描述 |
| `Array<SocketValueVariant> index_values` | 用 Array 存 variant（预分配） |
| `.emplace<int>(i)` | 就地构造 int 进 variant |
| `static const SocketValueVariant static_unused_index{-1}` | 静态常量，永久复用 |
| `params.get_input<SocketValueVariant>(...).ensure_type<int>()` | 提取已知类型 |

## 本篇小结

`SocketValueVariant` 的设计可以总结成四条：

1. **一个容器装四种形态**（Single/Field/List/Grid）；
2. **32 字节内联**覆盖绝大多数值，零堆分配；
3. **类型擦除**让头文件保持轻量（访问器实现在 .cc）；
4. **双层转换**（解释 vs 转换）让常见情况走快路径。

理解了这四条，正篇里所有 `SocketValueVariant` 的用法都不再神秘。
