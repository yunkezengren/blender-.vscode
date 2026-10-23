# 03-02 Span 只读视图

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:16px 0 20px;padding:10px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px">
<span style="font-size:11px;font-weight:700;letter-spacing:.1em;color:#64748B;margin-right:2px">导航</span>
<a href="../README.md" style="font-size:13px;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">总入口</a>
<a href="./README.md" style="font-size:13px;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">本章 03-BLI容器与视图</a>
</div>

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;margin:18px 0 22px;padding:14px 18px;background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:10px">

系列定位：本篇是《重复区域前置知识》系列 03 章第 2 篇。它讲 Span&lt;T&gt;：一个函数需要遍历"别人拥有的数组"时，参数应该怎么写。

</div>

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

基准：Blender `5.4.0-alpha`，本地工作树。本篇讲解 [`source/blender/blenlib/BLI_span.hh`](../../../source/blender/blenlib/BLI_span.hh) （实测 681 行）中的 `Span<T>`。

## 先回答一个具体问题

一个函数需要"遍历一段别人拥有的数组"，参数应该怎么写？

三种常见答案：

```cpp
void f(const std::vector<T> &v);   // 只能接 vector
void f(const T *data, int64_t n);  // 能接任何东西，但调用点丑且易错
void f(Span<T> span);              // 能接任何连续容器，且零开销
```

Blender 的答案几乎总是第三种。本系列正篇里 `Span` 出现在 provider 的成员（`Span<lf::FunctionNode *> lf_body_nodes_`）、函数参数（`insert_nodes_and_zones(const Span<const bNode *>)`）、返回值（`Input::inputs()`）等位置——它是 BLI 里**最常用的类型**。不理解它，读 Blender 源码会处处卡顿。

## 一句话定义

> **`Span<T>` 是"指向别人拥有的数组"的一对（指针, 长度），只读。**

它是 `const T*` + `int64_t` 的封装，不拥有内存、不负责释放、不保证被引用对象活着。

## 文件头注释揭示的设计意图

这是理解 Span 最好的入口。逐条拆解 [BLI_span.hh · L7-L57](../../../source/blender/blenlib/BLI_span.hh#L7)：

### 要点 1：它不拥有内存

> "An `Span<T>` references an array that is owned by someone else. It is just a > pointer and a size. Since the memory is not owned, Span should not be used to > transfer ownership."

**推论**：Span 绝不能作为"我把数组交给你"的手段。要转移所有权用 `Vector`/`Array`。

### 要点 2：默认只读

> "The array cannot be modified through the Span. However, if T is a non-const > pointer, the pointed-to elements can be modified."

注意后半句的精妙：`Span<int*>` 里元素是指针，你可以改指针**指向的内容**，但不能改指针本身。这是 `const` 的正确传播。

### 要点 3：与 std::span 的五组对照

注释给出了极清晰的对照表（L26-L31），值得完整背诵：

| `std::span` | Blender 等价 |
| --- | --- |
| `std::span<int>` | `MutableSpan<int>` |
| `std::span<const int>` | `Span<int>` |
| `std::span<int *>` | `MutableSpan<int *>` |
| `std::span<const int *>` | `MutableSpan<const int *>` |
| `std::span<int * const>` | `Span<int *>` |
| `std::span<const int * const>` | `Span<const int *>` |

规律：**Blender 把"可写性"提到最外层类型上**（`Span` vs `MutableSpan`），而 `std::span` 用元素的 const 表达。Blender 的选择避免了"`Span<const int>` 到底是只读还是可写"的歧义。

### 要点 4：为什么不用 `const Vector&`

> "It is better than passing a `const Vector &`, because e.g. then the function > only works for vectors and not arrays. Using Span as function parameter makes > it usable in more contexts, better expresses the intent and does not sacrifice > performance."

这是"**接受最宽泛的输入，返回最具体的输出**"原则（Postel 定律的 C++ 版）。

### 要点 5：存储 Span 是危险的

> "Since the arrays are only referenced, it is generally unsafe to store a Span. > When you store one, you should know who owns the memory."

**这条对读 Repeat 正篇极其关键**：`RepeatZoneSideEffectProvider` 成员 `Span<lf::FunctionNode *> lf_body_nodes_` 是存的 Span！它安全的前提是——节点列表存在 storage 里、活得和 provider 一样久。正篇 03-03 L943 专门讨论过这一点（wrapper 存指针、provider 存 Span 拷贝）。

### 要点 6：按值传递

> "Instances of Span and MutableSpan are small and should be passed by value."

16 字节（指针 + 长度），比传引用还快。

## 类定义逐段读

### 成员与类型别名（L74-L87）

```cpp
template<typename T> class Span {
 public:
  using value_type = T;
  using pointer = T *;
  using const_pointer = const T *;
  using reference = T &;
  using const_reference = const T &;
  using iterator = const T *;
  using size_type = int64_t;

 protected:
  const T *data_ = nullptr;
  int64_t size_ = 0;
```

`[讲解]` 三个细节：

1. **`size_type = int64_t`** 而不是 `size_t`。Blender 用有符号 64 位，避免 `size() - 1` 在空 span 上回绕成巨大正数（`size_t` 的经典陷阱）。
2. **默认构造是 `nullptr + 0`**。空 Span 完全合法，所有成员函数都要能处理它。
3. **`data_` 是 `const T*`**。这是只读性的物理保证，不是靠约定。

### 构造：从各种容器隐式转换（L92-L136）

```cpp
constexpr Span() = default;

constexpr Span(const T *start, int64_t size) : data_(start), size_(size)
{
  BLI_assert(size >= 0);
}

template<typename U>
constexpr Span(const U *start, int64_t size)
  requires(is_span_convertible_pointer_v<U, T>)
  : data_(start), size_(size)
{
  BLI_assert(size >= 0);
}

constexpr Span(const std::initializer_list<T> &list) : Span(list.begin(), int64_t(list.size()))
constexpr Span(const std::vector<T> &vector) : Span(vector.data(), int64_t(vector.size())) {}
template<std::size_t N> constexpr Span(const std::array<T, N> &array) : Span(array.data(), N) {}
```

`[讲解]` 这组构造函数是 Span 好用的根源：

- `std::vector`、`std::array`、`initializer_list` 都有隐式转换；
- **Blender 自己的 `Vector`/`Array`/`VectorSet` 也有对应的转换运算符** （在第 04、05 篇讲），所以 `Span` 能接 Blender 全部序列容器；
- `constexpr` 意味着编译期可用；
- `BLI_assert(size >= 0)` 是唯一的防御——负长度在 Debug 崩、Release 未定义。

**为什么需要 `requires is_span_convertible_pointer_v`？** 让 `Span<Base>` 能接 `Derived*`（指针可转换），但不能接 `int* → float*` 这种非法转换。这是模板约束的正确用法。

### 切片家族：`slice` / `drop_*` / `take_*`（L141-L212）

这组方法是 Span 最常用的操作，也是**正篇 03-03 的核心工具**。

```cpp
constexpr Span slice(int64_t start, int64_t size) const
{
  BLI_assert(start >= 0);
  BLI_assert(size >= 0);
  BLI_assert(start + size <= size_ || size == 0);
  return Span(data_ + start, size);
}

constexpr Span slice_safe(const int64_t start, const int64_t size) const
{
  const int64_t new_size = std::max<int64_t>(0, std::min(size, size_ - start));
  return Span(data_ ? data_ + start : nullptr, new_size);
}

constexpr Span drop_front(int64_t n) const
{
  const int64_t new_size = std::max<int64_t>(0, size_ - n);
  return Span(data_ + n, new_size);
}

constexpr Span drop_back(int64_t n) const
{
  const int64_t new_size = std::max<int64_t>(0, size_ - n);
  return Span(data_, new_size);
}

constexpr Span take_front(int64_t n) const
{
  const int64_t new_size = std::min<int64_t>(size_, n);
  return Span(data_, new_size);
}

constexpr Span take_back(int64_t n) const
{
  const int64_t new_size = std::min<int64_t>(size_, n);
  return Span(data_ + size_ - new_size, new_size);
}
```

`[讲解]` 两组语义完全不同，必须分清：

| 方法 | 越界时的行为 | 用在哪 |
| --- | --- | --- |
| `slice` | **assert 崩溃**（Debug） | 已知合法时，性能优先 |
| `slice_safe` | **夹取到合法范围** | 输入不可信时 |
| `drop_front(n)` | **夹取**（超长则变空） | 宁可空不可崩 |
| `drop_back(n)` | **夹取** | 同上 |
| `take_front(n)` | **夹取**（超长则全取） | 同上 |
| `take_back(n)` | **夹取** | 同上 |

后四个是"**永不失败**"的，这就是它们在框架代码里高频出现的原因。

**正篇实证**：`geometry_nodes_repeat_zone.cc` 里两处典型用法——

```cpp
/* L299 起：成对串联，最后一轮没有"下一轮" */
for (const int iter_i : lf_body_nodes.index_range().drop_back(1)) {
```

```cpp
/* L374 起：索引映射，跳过 iterations 输入 */
Vector<const lf::GraphInputSocket *> lf_graph_inputs = lf_inputs.as_span().drop_front(1);
```

这两行都是"我知道边界，但要写得安全且自解释"的典范。`drop_back(1)` 比 `IndexRange(size - 1)` 好在：**空列表时也不崩溃**（size=0 时 `drop_back(1)` 得空范围，而 `size-1` 会得到 -1）。

### 访问器（L219-L283）

```cpp
constexpr const T *data() const
constexpr const T *begin() const
constexpr const T *end() const
constexpr const T &operator[](int64_t index) const
{
  BLI_assert(index >= 0);
  BLI_assert(index < size_);
  return data_[index];
}
constexpr int64_t size() const
constexpr bool is_empty() const
constexpr int64_t size_in_bytes() const { return sizeof(T) * size_; }
constexpr bool contains(const T &value) const
```

`[讲解]` 三个要点：

1. **`operator[]` 有 assert 但无边界检查**（Release 下裸访问）。这与 `std::vector::operator[]` 一致，是性能取舍。
2. **`begin()`/`end()` 让 Span 支持范围 for**，这是它能替代手写循环的关键。
3. **`contains()` 是线性查找**（L281-L283 的 for 循环），别在热路径用。

## Span 与 MutableSpan 的边界

因为 `MutableSpan` 就在同一个文件（L447 起），这里先给结论，第 03 篇详讲：

| | `Span<T>` | `MutableSpan<T>` |
| --- | --- | --- |
| 存储 | `const T *data_` | `T *data_` |
| 能否改元素 | 否 | 是 |
| 几何意义 | 只读窗口 | 可写窗口 |
| Repeat 中的例子 | provider 的 body 列表 | `items_span()` 可变版 |

## 用小数据走一遍

初始 `Span<int> s` 引用 `{10, 20, 30, 40, 50}`（size=5）：

| 表达式 | 结果 | 说明 |
| --- | --- | --- |
| `s.size()` | 5 | |
| `s[2]` | 30 | |
| `s.slice(1, 3)` | {20,30,40} | 精确切片，越界会崩 |
| `s.slice_safe(3, 10)` | {40,50} | 夹取到剩余长度 |
| `s.drop_front(2)` | {30,40,50} | 去掉前 2 个 |
| `s.drop_front(99)` | {} | **不崩**，得空 |
| `s.drop_back(2)` | {10,20,30} | 去掉后 2 个 |
| `s.take_front(2)` | {10,20} | 取前 2 个 |
| `s.take_front(99)` | 全部 5 个 | **不崩**，全取 |
| `s.take_back(2)` | {40,50} | 取后 2 个 |
| `s.slice(2, 0)` | {} | 空切片合法（assert 有 `size == 0` 例外） |
| `s.contains(30)` | true | 线性查找 |

**内存视角**：所有这些操作都**不复制任何元素**，只改 `data_` 与 `size_` 两个字段。`s.slice(1,3)` 的 `data_` 是原 `data_ + 1`。

## 反例与边界

### 反例 1：存储指向临时容器的 Span

```cpp
// 错误
Span<int> bad() {
  Vector<int> local = {1, 2, 3};
  return local.as_span();   // local 析构，Span 悬空
}
```

这正是注释 L53-L54 警告的场景。**Returning a Span is almost always a bug unless the owner outlives the caller.**

### 反例 2：把 Span 当所有权转移手段

```cpp
// 错误
void take(Span<Mesh> meshes) {
  my_meshes_ = meshes;   // 谁负责释放？没人
}
```

应该接受 `Vector<Mesh>` 或 `Span` + 明确的"调用方保证生命周期"契约，并在注释里写清。

### 反例 3：误以为 `slice` 会夹取

```cpp
Span<int> s = ...;  // size 5
auto x = s.slice(3, 10);  // Debug: assert 崩；Release: 越界读
```

要安全用 `slice_safe`。

### 反例 4：`Span<const T>` 与 `Span<T>` 的转换不对称

```cpp
Span<int> a = ...;
Span<const int> b = a;   // OK：加 const 是安全方向
Span<int> c = b;          // 编译错误：去 const 不允许
```

这是 C++ 类型系统的正常行为，但初学者常被 `MutableSpan` 的对应规则搞混。

### 反例 5：在 Span 上做插入/删除

```cpp
Span<T> 没有 push_back / erase / resize
```

因为它只是视图。需要改结构必须用 `Vector`。

### 反例 6：以为 `size_in_bytes()` 是元素个数

```cpp
s.size()          // 5
s.size_in_bytes() // 5 * sizeof(T)
```

拼写相近，用途完全不同。

## 对理解 Repeat 的帮助

`Span` 在 Repeat 正篇里出现的位置与作用：

| 位置 | 代码片段 | 意义 |
| --- | --- | --- |
| 04-03 副作用 provider | `Span<lf::FunctionNode *> lf_body_nodes_;` | 只读持有 body 列表，靠 storage 保活 |
| 03-02 body 构建 | `const Span<const bNode *> bnodes` | 接受任意来源的节点列表 |
| 03-03 成对串联 | `.drop_back(1)` | 安全地"除最后一轮" |
| 03-03 索引映射 | `.drop_front(1)` | 安全地"跳过 iterations" |
| 03-01 wrapper 接口 | `Span<lf::Input> inputs` | 遍历接口定义 |
| 05-01 合成器 | `Span<const bNodeLink *>` | border link 列表 |

**最关键的一条**：`Span` 的"不拥有"语义，正好匹配 LF 框架里 "某个东西由上层保活、我只看一眼"的模式。理解这一点，正篇 03-03 L943 那段"wrapper 存指针、provider 存 Span 拷贝"的讨论就不再困惑——两种选择都是在表达"我不拥有它，**而且**我知道谁拥有"。

## 继续阅读

- 下一篇：[03-Span与MutableSpan](03-Span与MutableSpan.md) —— 同文件 L447 起的可写版本
- 本章：[容器全景与选型](01-容器全景与选型.md)
- 相关：[04-Vector与Array](04-Vector与Array.md) —— Span 的来源容器
- 正篇：[03-03 执行图按迭代展开](../../重复区域-dsh/03-几何节点执行架构/03-执行图按迭代展开.md)
- 正篇：[04-03 副作用迭代与按需执行](../../重复区域-dsh/04-运行时机制/03-副作用迭代与按需执行.md)
