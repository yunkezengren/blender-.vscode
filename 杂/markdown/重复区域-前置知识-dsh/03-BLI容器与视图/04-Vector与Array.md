# 04 · Vector 与 Array

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](03-Span与MutableSpan.md) · [下一篇](05-VectorSet稳定索引.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲两个拥有型序列容器：`Vector<T>`（动态扩容）与 `Array<T>`（固定大小）——它们是 `Span` 的数据来源。主要源码：[`BLI_vector.hh`](../../../source/blender/blenlib/BLI_vector.hh)（1057 行）、[`BLI_array.hh`](../../../source/blender/blenlib/BLI_array.hh)（430 行）。

> 行数口径：上文 1057 / 430 是**去空行**的统计（与本章 `README.md` 总表一致）。本篇所有 `#L` 锚点用**原始行号**，所以 `BLI_vector.hh` 的锚点最大到 L1167、`BLI_array.hh` 到 L487。两种口径都对，混用不算错。

## 先回答一个具体问题

写 Repeat Zone 的执行图时，有一组数据**事先就知道要几个**（迭代次数 `iterations`），还有一组**边算边确定**（每轮往映射表里塞一个新下标）。分别用哪个容器？正篇代码已经摆好了答案：

| 数据 | 声明 | 源码 |
| --- | --- | --- |
| 每轮的下标值 | `Array<SocketValueVariant> index_values` | [`geometry_nodes_repeat_zone.cc` · L106](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L106) |
| 输入参数重映射 | `Vector<int> input_index_map` | [同文件 · L109](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L109) |
| 输出参数重映射 | `Vector<int> output_index_map` | [同文件 · L110](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L110) |

**判断规则只有一条**：元素个数在"容器第一次成型的那一刻"就已完全确定 → `Array`；个数要在一串操作中逐步长出来 → `Vector`。

选错的代价是具体的：该用 `Array` 却用了 `Vector`，会多一份"容量可能大于大小"的冗余，更糟的是**读代码的人以为这个数组后面还会变**，去追一条不存在的数据流；该用 `Vector` 却用了 `Array`，你只能提前算个上界再 `reinitialize(上界)`，于是数组里躺着一堆逻辑上无效的元素，`size()` 也不再是真实个数——这类 bug 全在合理范围内，视觉上极难发现。

## Vector 的设计取向

`BLI_vector.hh` 的文件头（[L7-L25](../../../source/blender/blenlib/BLI_vector.hh#L7)）开门见山：它是 `std::vector` 的"更方便、更高效的替代品"，并明确要求 **`Vector` 应成为 Blender 里向量结构的默认选择**。注意那句提示——此处的 "vector" 与计算机图形学里的向量毫无关系。

| # | 维度 | `std::vector` | Blender `Vector` | 证据 |
| --- | --- | --- | --- | --- |
| 1 | 小对象优化 | 无，首次插入即分配 | inline buffer，容量内**完全不碰堆** | [L19-L22](../../../source/blender/blenlib/BLI_vector.hh#L19)、[L103](../../../source/blender/blenlib/BLI_vector.hh#L103) |
| 2 | 移动后的迭代器 | 移动后原迭代器仍指向数据 | 数据若在内联缓冲中，移动即**搬字节**，迭代器全失效 | [L21-L22](../../../source/blender/blenlib/BLI_vector.hh#L21) |
| 3 | 尾部插入 | `push_back` / `emplace_back` | `append` / `append_as` / `append_unchecked` / `append_and_get_index` | [L498-L563](../../../source/blender/blenlib/BLI_vector.hh#L498) |
| 4 | 批量追加 | `insert(end(), ...)` 模拟 | 一等公民 `extend(Span<T>)`：一次 reserve + 一次拷贝 | [L595-L603](../../../source/blender/blenlib/BLI_vector.hh#L595) |
| 5 | 无序删除 | `erase` 后整体前移 O(n) | `remove_and_reorder`：末尾元素填洞，O(1) | [L829-L841](../../../source/blender/blenlib/BLI_vector.hh#L829) |
| 6 | 扩容策略 | 实现定义，通常 1.5×~2× | 明写 `capacity() * 2`，且保证 `>= min_capacity` | [L1129-L1131](../../../source/blender/blenlib/BLI_vector.hh#L1129) |
| 7 | 分配器 | `std::allocator` | 默认 `GuardedAllocator`，即 `MEM_*` 受保护分配器 | [L75](../../../source/blender/blenlib/BLI_vector.hh#L75) |
| 8 | 大小表示 | 存 `size` + `capacity` 两个整数 | 存**三个指针** `begin_ / end_ / capacity_end_` | [L89-L97](../../../source/blender/blenlib/BLI_vector.hh#L89) |
| 9 | 异常 | 强异常保证是标准要求 | 实现里大量 `try/catch(...)` 回滚，测试有专门用例 | [L1136-L1146](../../../source/blender/blenlib/BLI_vector.hh#L1136) |

**第 8 条是理解全部取舍的钥匙**。`size()` 每次现算（[L780-L785](../../../source/blender/blenlib/BLI_vector.hh#L780)）：

```cpp
int64_t size() const
{
  const int64_t current_size = int64_t(end_ - begin_);
  BLI_assert(debug_size_ == current_size);
  return current_size;
}
```

指针相减比"读一个 int64 成员"少一次内存访问，`append` 因此更快。代价是调试体验差——所以 debug 构建额外塞了 `debug_size_`，只在 `BLI_assert` 里用，release 下被 `#ifndef NDEBUG` 整个裁掉（[L110-L115](../../../source/blender/blenlib/BLI_vector.hh#L110)）。看到 `UPDATE_VECTOR_SIZE(this)` 别慌，release 下它展开成 `((void)0)`。

## Vector 的核心接口

| 接口 | 签名要点 | 复杂度 | 行号 |
| --- | --- | --- | --- |
| `append` | `void append(const T &)` / `void append(T &&)` | 均摊 O(1)，满时 O(n) | [L498-L505](../../../source/blender/blenlib/BLI_vector.hh#L498) |
| `append_as` | 变参完美转发，原地构造 | 同上 | [L507-L511](../../../source/blender/blenlib/BLI_vector.hh#L507) |
| `append_and_get_index` | 返回新元素**下标** | 同上 | [L517-L530](../../../source/blender/blenlib/BLI_vector.hh#L517) |
| `extend` | `(Span<T>)` / `(const T*, int64_t)` / 移动版 | 一次 reserve + 线性拷贝 | [L595-L619](../../../source/blender/blenlib/BLI_vector.hh#L595) |
| `resize` | `(int64_t)` / `(int64_t, const T &)` | O(差值) | [L418-L452](../../../source/blender/blenlib/BLI_vector.hh#L418) |
| `reinitialize` | `clear()` + `resize()` | O(旧 + 新) | [L458-L462](../../../source/blender/blenlib/BLI_vector.hh#L458) |
| `reserve` | 只调容量，**不改 size** | O(n) 仅在真要扩容时 | [L405-L410](../../../source/blender/blenlib/BLI_vector.hh#L405) |
| `as_span` / `as_mutable_span` | 转视图 | O(1) | [L390-L398](../../../source/blender/blenlib/BLI_vector.hh#L390) |
| `remove_and_reorder` | 末尾元素填洞 | O(1) | [L829](../../../source/blender/blenlib/BLI_vector.hh#L829) |
| `remove` | 后续元素整体前移 | O(n) | [L860-L892](../../../source/blender/blenlib/BLI_vector.hh#L860) |
| `pop_last` / `remove_last` | 弹尾，前者**返回值** | O(1) | [L801-L823](../../../source/blender/blenlib/BLI_vector.hh#L801) |
| `last(n=0)` / `first()` | 带断言的引用 | O(1) | [L749-L775](../../../source/blender/blenlib/BLI_vector.hh#L749) |
| `operator[]` | 两条 `BLI_assert` + 裸索引 | O(1) | [L352-L364](../../../source/blender/blenlib/BLI_vector.hh#L352) |
| `capacity` / `is_at_capacity` | 观察扩容状态 | O(1) | [L1007-L1015](../../../source/blender/blenlib/BLI_vector.hh#L1007) |

### `append` 与 `append_as` 的真实区别

这里必须给一个**与直觉不符的实测结论**：不少二手资料会说 `append_as` 返回新元素的引用。本地工作树的实际签名是（[L506-L511](../../../source/blender/blenlib/BLI_vector.hh#L506)）：

```cpp
/* This is similar to `std::vector::emplace_back`. */
template<typename... ForwardValue> void append_as(ForwardValue &&...value)
{
  this->ensure_space_for_one();
  this->append_unchecked_as(std::forward<ForwardValue>(value)...);
}
```

返回类型是 **`void`**，不是 `T &`。我用 `git log -S "T &append_as"` 查遍整个历史也没找到任何一版返回引用；唯一相关提交是 `686452fb1bc BLI: add Vector.append_as method`，加进来就是 `void`。

所以二者**唯一**的区别是构造方式：`v.append(7)` 是先有一个 `int` 值 7 再拷/移进容器；而 `v2.append_as("hello", 2)` 直接把参数转发给 `StringRef` 的构造函数，对应 `std::vector::emplace_back`，省掉一次临时对象。单元测试 [`BLI_vector_test.cc` · L255-L262](../../../source/blender/blenlib/tests/BLI_vector_test.cc#L255) 正是这个用法。**需要拿到新元素**时，官方给的是 `append_and_get_index`（[L517-L530](../../../source/blender/blenlib/BLI_vector.hh#L517)）——返回下标而不是引用，这恰恰是"不要持有引用"的安全设计，见反例 2。

### `append` 的三层调用栈

`append` → `append_as` → `ensure_space_for_one` + `append_unchecked_as`，最内层是（[L557-L563](../../../source/blender/blenlib/BLI_vector.hh#L557)）：

```cpp
template<typename... ForwardT> void append_unchecked_as(ForwardT &&...value)
{
  BLI_assert(end_ < capacity_end_);
  new (end_) T(std::forward<ForwardT>(value)...);
  end_++;
  UPDATE_VECTOR_SIZE(this);
}
```

**一次定位构造 + 指针自增**，没有 size 字段回写，这就是 `append` 快的根本原因。外层 `ensure_space_for_one` 把"是否满了"压成一次比较并加 `[[unlikely]]` 提示分支预测（[L1114-L1119](../../../source/blender/blenlib/BLI_vector.hh#L1114)）——正常路径几乎永不命中。

### `extend` 为什么比循环 append 快

```cpp
void extend(Span<T> array) { this->extend(array.data(), array.size()); }
void extend(const T *start, int64_t amount)
{
  this->reserve(this->size() + amount);
  this->extend_unchecked(start, amount);
}
```

（[L595-L603](../../../source/blender/blenlib/BLI_vector.hh#L595)）关键在于 `reserve` **只调一次**：

```cpp
void extend(const T *start, int64_t amount)
{
  this->reserve(this->size() + amount);
  this->extend_unchecked(start, amount);
}
```

循环 `append` 可能在中间多次触发 `realloc_to_at_least`，每次都要搬已有元素；`extend` 一次把容量抬够，之后退化成一次 `uninitialized_copy_n`。正篇 L383-L385 就靠这个拼装输出列表：先用 `lf_outputs.as_span().take_front(iteration_usage_index)` 构造前半段，再 `extend(lf_outputs.as_span().drop_front(iteration_usage_index + 1))` 接上后半段，正好跳过中间那个 `iteration_usage_index` 位置。

### `resize` 与 `reinitialize` 的分工

`resize` 保留已有元素、只在尾部增删（[L418-L431](../../../source/blender/blenlib/BLI_vector.hh#L418)）；`reinitialize` 是"全清 + 重设大小"（[L458-L462](../../../source/blender/blenlib/BLI_vector.hh#L458)）：

```cpp
void reinitialize(const int64_t new_size)
{
  this->clear();
  this->resize(new_size);
}
```

注意 `clear()` 只析构元素、**不释放容量**（[L468-L473](../../../source/blender/blenlib/BLI_vector.hh#L468)），所以 `reinitialize(大数)` 之后仍可能扩容，除非先 `reserve`。想连内存一起还回去只有 `clear_and_shrink()`（[L479-L490](../../../source/blender/blenlib/BLI_vector.hh#L479)）。`resize` 增大部分调 `default_construct_n`，对 `int` 这类平凡类型什么都不做——**新元素是未初始化的**，见反例 3。

## 小对象优化

`Vector` 的三个指针可以指向堆，也可以指向**自己体内**一块预留缓冲。这就是 small buffer optimization（SBO）。

### 字段与容量常量

模板参数（[L57-L75](../../../source/blender/blenlib/BLI_vector.hh#L57)）里，默认容量由 [`BLI_memory_utils.hh` · L274-L277](../../../source/blender/blenlib/BLI_memory_utils.hh#L274) 决定：

```cpp
constexpr int64_t default_inline_buffer_capacity(size_t element_size)
{
  return (int64_t(element_size) < 100) ? 4 : 0;
}
```

**规则极朴素**：元素小于 100 字节 → 内联 4 个；否则内联 0 个。注释给了动机——"避免在栈上产生意料之外的大分配"。命名对照：本版本的常量名是 `InlineBufferCapacity` 与 `default_inline_buffer_capacity`，成员名 `inline_buffer_`；**源码里不存在 `MinInlineCapacity`**，别照抄别的资料去找这个名字。

### 内存布局

release 构建下的 `Vector<T, 4>`（[L95-L103](../../../source/blender/blenlib/BLI_vector.hh#L95)）：

| 偏移 | 字段 | 大小 |
| --- | --- | --- |
| 0 | `begin_` (`T *`) | 8 |
| 8 | `end_` (`T *`) | 8 |
| 16 | `capacity_end_` (`T *`) | 8 |
| 24 | `allocator_`（`BLI_NO_UNIQUE_ADDRESS`，空类） | 0 |
| 24 | `inline_buffer_`（`TypedBuffer<T, 4>`） | `4 * sizeof(T)` |
| — | `debug_size_`（**仅 debug 构建**） | 0 / 8 |

所以 `Vector<int>` 是 40 字节（debug 48）；`Vector<float3>`（12 字节）是 72；`Vector<std::string>`（32 字节）是 152；任何 `sizeof(T) >= 100` 的类型 `InlineBufferCapacity == 0`，`Vector` 只剩 24 字节——**SBO 被彻底关闭**，第一次 `append` 就分配。

`TypedBuffer`（[`BLI_memory_utils.hh` · L154-L178](../../../source/blender/blenlib/BLI_memory_utils.hh#L154)）是个只声明对齐和大小、**不构造任何对象**的裸缓冲，`Size == 0` 时用 `if constexpr` 连 `sizeof(T)` 和 `alignof(T)` 一并规避——这就是 `Vector<IncompleteType>` 在 Blender 里能编过的原因。

### 构造函数如何点亮 inline buffer

默认构造是 **`noexcept` 且零分配**的（[L140-L146](../../../source/blender/blenlib/BLI_vector.hh#L140)）：`begin_ = inline_buffer_; end_ = begin_; capacity_end_ = begin_ + InlineBufferCapacity;`——三个指针全指向自己体内，`capacity()` 立刻等于 `InlineBufferCapacity`。`is_inline()` 就是一句指针相等（[L1108-L1111](../../../source/blender/blenlib/BLI_vector.hh#L1108)）。

`release()` 的行为完全被这一点决定：内联缓冲的所有权**不可能转移**（它长在 `Vector` 体内），所以内联且非空时 `release()` 先**新分配一块、把元素搬过去**再交出指针（[L1060-L1097](../../../source/blender/blenlib/BLI_vector.hh#L1060)）。测试 [`BLI_vector_test.cc` · L991-L1005](../../../source/blender/blenlib/tests/BLI_vector_test.cc#L991) 验证的正是这一点：`Vector<int> vec = {1, 2};` 后 `vec.is_inline()` 为真，而 `release()` 返回的 `data.data` **不等于** 原来的 `vec.data()`——地址变了，因为内联缓冲交不出去。对照内联且为空的情形：直接返回空 `VectorData`，**连一次分配都不做**（[L1062-L1066](../../../source/blender/blenlib/BLI_vector.hh#L1062)，测试 L967-L972）。

### 关闭或放大 SBO

`InlineBufferCapacity` 是模板参数，可显式指定：`Vector<int, 0>` 关掉 SBO 全走堆；`Vector<int, 16>` 内联 16 个适合"几乎总是小"的热路径；`RawVector<int>` = `Vector<T, default, RawAllocator>`，绕开 `MEM_*` 守卫分配器（[L1160-L1161](../../../source/blender/blenlib/BLI_vector.hh#L1160)，注释给的场景是静态存储期全局对象）。

## Vector 扩容策略

扩容只发生在一处：`ensure_space_for_one` 发现 `end_ >= capacity_end_` 时调 `realloc_to_at_least(size() + 1)`。全部逻辑在 [L1121-L1151](../../../source/blender/blenlib/BLI_vector.hh#L1121)：

```cpp
BLI_NOINLINE void realloc_to_at_least(const int64_t min_capacity)
{
  if (this->capacity() >= min_capacity) { return; }

  /* At least double the size of the previous allocation. Otherwise consecutive calls to grow can
   * cause a reallocation every time even though min_capacity only increments. */
  const int64_t min_new_capacity = this->capacity() * 2;
  const int64_t new_capacity = std::max(min_capacity, min_new_capacity);
  const int64_t size = this->size();

  T *new_array = static_cast<T *>(
      allocator_.allocate(size_t(new_capacity) * sizeof(T), alignof(T), AT));
  try { uninitialized_relocate_n(begin_, size, new_array); }
  catch (...) { allocator_.deallocate(new_array); throw; }

  if (!this->is_inline()) { allocator_.deallocate(begin_); }

  begin_ = new_array;
  end_ = begin_ + size;
  capacity_end_ = begin_ + new_capacity;
}
```

五个要点：

1. **是 `max(min_capacity, capacity * 2)`，不是纯 ×2**。注释（L1127-L1128）解释了为何必须取 max：只按 `min_capacity` 增长的话，"每次只多要 1 个"的调用序列会导致每次 `append` 都重分配。
2. **均摊 O(1)**：n 次 `append` 的总拷贝量 `1 + 2 + 4 + ... + n < 2n`，均摊到每次是常数。
3. **`capacity() == 0` 时（SBO 关闭）第一跳是 1**：`max(1, 0*2) = 1`，之后才 1 → 2 → 4 → 8。知道要大就**在第一条 `append` 之前 `reserve`**。
4. **`is_inline()` 决定要不要 `deallocate`**：内联缓冲不属于分配器，误释放是灾难。这一句是 SBO 与扩容的交汇点。
5. **异常安全**：`uninitialized_relocate_n` 抛异常时只释放**新**数组再 `throw`，三个指针一个没动，`Vector` 保持扩容前状态。

`reserve` 是这层的门面（[L405-L410](../../../source/blender/blenlib/BLI_vector.hh#L405)），注释明确写"**min_capacity 很小时不一定会分配**"——`Vector<int> v; v.reserve(3);` 什么也不做，因为 `capacity()` 已是 4。测试 L974-L989 用 `reserve(100)` 证明只有超过 4 才真正分配，且释放后 `data.capacity == 100`。**`reserve` 的实际用途**不是"省一次分配"，而是：把 k 次摊薄的扩容合并成一次，避免**引用/指针在过程中批量失效**（反例 2）；让后续可安全使用 `append_unchecked`（[L549-L563](../../../source/blender/blenlib/BLI_vector.hh#L549)），它跳过容量检查；多线程写入前一次性备好容量。

## Array 的设计取向

`BLI_array.hh` 的文件头（[L7-L26](../../../source/blender/blenlib/BLI_array.hh#L7)）给了四条硬约束：

1. **大小运行期确定，但一旦确定就不再变**——"a container for a fixed size array the size of which is NOT known at compile time"。
2. 大小在**编译期**就已知的话，请用 `std::array<T, N>`。
3. **只要元素个数在构造时已知，就应当用 `Array` 而不是 `Vector`**。
4. 主要好处是**表达意图**：明确宣告"这个结构的大小不打算变"，并且"你可以更确定它没有过度分配"。

第 4 条是这个类存在的全部理由。`Array` 在能力上几乎是 `Vector` 的子集——没有 `append`、没有 `resize`、没有 `capacity`、没有 `reserve`、没有 `remove`。**它不是"简化版 Vector"，它是"另一种意图的声明"**。

### 字段与"没有容量这个概念"

```cpp
T *data_;            /** The beginning of the array. It might point into the inline buffer. */
int64_t size_;       /** Number of elements in the array. */
BLI_NO_UNIQUE_ADDRESS Allocator allocator_;
BLI_NO_UNIQUE_ADDRESS TypedBuffer<T, InlineBufferCapacity> inline_buffer_;
```

（[L61-L72](../../../source/blender/blenlib/BLI_array.hh#L61)）对比 `Vector` 的三指针，这里只有**一个指针 + 一个 size**。差别不是笔误：`Vector` 的大小与容量是两个独立的量，需要三个指针表达"用了多少 / 能用多少"；`Array` 的容量**恒等于** size，第二个指针纯属冗余。

省掉的不只是 8 字节，而是**一整类 bug**：任何"容量 > 大小"的状态在 `Array` 里根本不可能出现，围绕它的分支（`is_at_capacity`、`shrink_to_fit`、扩容后指针失效）也全部不存在。

### 构造即定型

| 构造 | 大小来源 | 元素初始化 | 行号 |
| --- | --- | --- | --- |
| `Array()` | 0 | 无 | [L78-L82](../../../source/blender/blenlib/BLI_array.hh#L78) |
| `Array(int64_t size)` | 参数 | **默认构造全部**（平凡类型不动内存） | [L123-L129](../../../source/blender/blenlib/BLI_array.hh#L123) |
| `Array(int64_t size, const T &value)` | 参数 | 全部拷贝构造自 `value` | [L135-L154](../../../source/blender/blenlib/BLI_array.hh#L135) |
| `Array(Span<U> values)` | span 长度 | 全部拷贝构造自源 | [L89-L98](../../../source/blender/blenlib/BLI_array.hh#L89) |
| `Array(int64_t size, NoInitialization)` | 参数 | **完全不构造**，调用者负责 | [L168-L174](../../../source/blender/blenlib/BLI_array.hh#L168) |

第二条要留意。头注释（[L15-L18](../../../source/blender/blenlib/BLI_array.hh#L15)）坦白这是 `Array` 相对 `Vector` 的**劣势**：`Array(n)` 会对所有元素做默认构造，平凡类型零开销，非平凡类型则是实打实的 n 次构造。

`Array(n, value)` 里还藏了个优化（[L139-L152](../../../source/blender/blenlib/BLI_array.hh#L139)）：若 `T` 平凡可拷贝**且** `value_is_zero_memory(value)` 成立，就直接向分配器要**清零**的内存（`allocate_zero`），省掉逐元素写。这条分支是为"零向量 / 零矩阵"这类高频场景准备的。

## Array 的核心接口

| 接口 | 作用 | 行号 |
| --- | --- | --- |
| `reinitialize(int64_t new_size)` | **唯一能改大小的入口**：析构旧的、按新大小重建 | [L430-L455](../../../source/blender/blenlib/BLI_array.hh#L430) |
| `as_span()` / `as_mutable_span()` | 转视图 | [L254-L262](../../../source/blender/blenlib/BLI_array.hh#L254) |
| `operator Span<T>()` / `operator MutableSpan<T>()` | 隐式转换 | [L230-L252](../../../source/blender/blenlib/BLI_array.hh#L230) |
| `fill(const T &value)` | 每个元素赋成 `value` | [L283-L286](../../../source/blender/blenlib/BLI_array.hh#L283) |
| `size()` / `is_empty()` / `index_range()` | 观察 | [L267-L270](../../../source/blender/blenlib/BLI_array.hh#L267)、[L371](../../../source/blender/blenlib/BLI_array.hh#L371) |
| `operator[]` / `first()` / `last(n)` | 访问，全带 `BLI_assert` | [L216-L228](../../../source/blender/blenlib/BLI_array.hh#L216)、[L292-L318](../../../source/blender/blenlib/BLI_array.hh#L292) |
| `data()` / `begin()` / `end()` / `rbegin()` / `rend()` | 迭代器与裸指针 | [L323-L366](../../../source/blender/blenlib/BLI_array.hh#L323) |
| `clear_without_destruct()` | **只把 size 置 0**，不析构 | [L400-L403](../../../source/blender/blenlib/BLI_array.hh#L400) |
| `inline_buffer_capacity()` | 静态查询模板参数 | [L421-L424](../../../source/blender/blenlib/BLI_array.hh#L421) |

> **必须纠正三处常见误记**。本版本 `BLI_array.hh` 里：**没有 `release()`**（`Vector` 有 `release()` 返回 `VectorData`，`Array` 完全没有对应物）；**没有 `resize()`**（改大小只有 `reinitialize()`，语义是旧元素全丢）；**没有 `copy()` 成员**（复制走拷贝构造 [L176](../../../source/blender/blenlib/BLI_array.hh#L176) 或 `Array(Span<U>)` [L89](../../../source/blender/blenlib/BLI_array.hh#L89)）。直接证据：在 `BLI_array.hh` 上搜 `release|resize|append|capacity|copy\(` 只命中两行（L44 的模板参数、L421 的 `inline_buffer_capacity`）。

### `reinitialize`：唯一的形状改变

```cpp
void reinitialize(const int64_t new_size)
{
  int64_t old_size = size_;
  destruct_n(data_, size_);          // 无条件析构全部旧元素
  size_ = 0;

  if (new_size <= old_size) {
    default_construct_n(data_, new_size);      // 原地复用旧缓冲
  }
  else {
    T *new_data = this->get_buffer_for_size(new_size, false);   // 精确大小
    try { default_construct_n(new_data, new_size); }
    catch (...) { this->deallocate_if_not_inline(new_data); throw; }
    this->deallocate_if_not_inline(data_);
    data_ = new_data;
  }
  size_ = new_size;
}
```

（[L430-L455](../../../source/blender/blenlib/BLI_array.hh#L430)）逐行读：

1. `destruct_n(data_, size_)` 无条件析构**全部**旧元素——包括那些"新大小仍覆盖得到"的位置。`reinitialize(3)` 之后 `[0..2]` 是**重新默认构造的**，不是旧的三个值。
2. `new_size <= old_size` → **原地复用同一块缓冲**，只在上面重新默认构造。这块缓冲可能来自内联缓冲，也可能来自一块**比 new_size 更大的堆分配**。
3. `new_size > old_size` → `get_buffer_for_size(new_size)` 拿**恰好 new_size** 个（[L458-L469](../../../source/blender/blenlib/BLI_array.hh#L458)）：`new_size <= InlineBufferCapacity` 就返回 `inline_buffer_`，否则**精确分配**——不预留、不翻倍。
4. 构造新元素时抛异常 → 只释放新缓冲，旧的 `data_ / size_` 尚未改动，`Array` 保持空而有效（`size_` 在 L436 已置 0）；成功后 `deallocate_if_not_inline(data_)` 释放旧块（[L479-L484](../../../source/blender/blenlib/BLI_array.hh#L479)），再更新 `data_`。

**这就是本章 `README.md` 说的"精确大小、一次分配"**：一旦决定 `new_size`，内存就是这个尺寸，没有 `reserve` 可以追加，也没有 `append` 可以长大。

### `release` 与所有权

`Array` 没有 `release`，但所有权仍可转移——通过**移动构造/赋值**（[L178-L198](../../../source/blender/blenlib/BLI_array.hh#L178)）：内联则 `uninitialized_relocate_n` 搬家，非内联则偷指针（`data_ = other.data_;`），两种分支都把源对象重置回空的内联状态（`other.data_ = other.inline_buffer_; other.size_ = 0;`）。

**这段和 `Vector` 的移动构造（[L245-L307](../../../source/blender/blenlib/BLI_vector.hh#L245)）是同构的**——SBO 带来的结构相似性，远超两个容器接口上的差异。值得对照的是 `Vector` 移动构造里那段额外优化（[L252-L271](../../../source/blender/blenlib/BLI_vector.hh#L252)）：当两个 `Vector` 类型完全相同时、`T` 平凡、内联缓冲 ≤ 32 字节，直接 `memcpy` **整个**内联缓冲（连未初始化的尾部一起），因为固定长度的 `memcpy` 比"按动态 size 拷贝"能生成更紧的代码。`Array` 里没有这一版——移动不是它的最热路径，不值得为此付复杂度。

## 二者的选择标准

| # | 场景 | 选择 | 理由 |
| --- | --- | --- | --- |
| 1 | 个数在构造时**完全已知**、之后不变 | `Array` | 头注释 L15："元素个数构造时已知时通常应优先 `Array`" |
| 2 | 个数**编译期已知**且很小 | `std::array<T, N>` | 头注释 L13 明确赶客 |
| 3 | 需要**逐个追加**、个数未知 | `Vector` | `Array` 没有 `append`，这件事它做不到 |
| 4 | 需要**删除中间元素** | `Vector` | `Array` 无 `remove*`；`Vector` 还有 O(1) 的 `remove_and_reorder` |
| 5 | 大小**周期性变化**（每帧重新分配） | `Array` + `reinitialize` | 一次精确分配、无过度分配；`Vector` 会保留历史最大容量 |
| 6 | 用作**函数参数、只读** | 都不是，用 `Span` | 见下一节 |
| 7 | 需要**转移所有权**给缓冲区 / C API | `Vector`（`release()` → `VectorData`） | `Array` 没有 `release` |
| 8 | 元素类型**大于 100 字节**的热路径 | `Vector` 需注意 SBO 关闭 | `default_inline_buffer_capacity` 返回 0 |
| 9 | 需要 `append_unchecked` 等**手动控容量**技巧 | `Vector` | `Array` 没有容量的概念 |

一句话版本：**`Vector` 表达"我正在长"，`Array` 表达"我已经定型"，`Span` 表达"我只是借来看"**。三者的分工是纯语义的，与性能基本无关——这是 Blender 容器设计里最值得学的一点：先选对意图，性能自然跟着来；选错意图的代码能跑，但读它的人会一直误解数据流。

## 与 Span 的关系

`Vector` 和 `Array` 都是 `Span` 的**生产者**，`Span` 是它们的**只读解码器**。三条转换路径：

```cpp
Vector<int> v = {1, 2, 3};
Span<int> s1 = v;              // 隐式 operator Span<T>();          BLI_vector.hh L366
Span<int> s2 = v.as_span();    // 显式，语义相同
MutableSpan<int> m = v;        // operator MutableSpan<T>();        L371
```

`Array` 版本完全对称（[L230-L262](../../../source/blender/blenlib/BLI_array.hh#L230)）。两者还都支持**模板化的元素类型转换**，只要指针可转换（[L376-L381](../../../source/blender/blenlib/BLI_vector.hh#L376)）——这让 `Vector<Derived *>` 能直接当 `Span<Base *>` 用。

`operator Span<T>()` 与 `as_span()` 实现完全相同，区别只是**调用点能否被隐式触发**。函数签名写 `Span<int>` 时传 `Vector<int>` 会自动转换；写 `as_span()` 的地方则在强调"我确实在处理视图"。正篇两种都写：`geometry_nodes_repeat_zone.cc` 里既有 L374 的 `lf_inputs.as_span()`，也有直接把 `Vector<int>` 传进 `RemappedParams`（L179-L180）。

### 为什么函数参数优先 `Span` 而不是 `const Vector &`

[`BLI_span.hh` · L37-L41](../../../source/blender/blenlib/BLI_span.hh#L37) 给了三条理由，几乎逐字可背：

> "`Span<T>` should be your default choice when you have to pass a read-only array into a function. It is better than passing a `const Vector &`, because e.g. then the function only works for vectors and not arrays. Using Span as function parameter makes it usable in more contexts, better expresses the intent and does not sacrifice performance."

拆开：**可用性**——`const Vector<T> &` 只能接 `Vector`，接不了 `Array`、`std::vector`、C 数组、`VectorSet`，而 `Span` 全都能接（[`BLI_span.hh` · L18-L20](../../../source/blender/blenlib/BLI_span.hh#L18) 明确列出这串来源）；**意图**——写 `Span` 等于宣告"我只读、不管所有权、不保存这个指针"；**性能**——`Span` 就是 `(指针, 长度)` 两个寄存器大小的值，零开销。

而 `Vector` / `Array` 自己的成员也普遍**用 `Span` 做输入**，这是同一条规则的内部化：`Vector::extend`（[L595](../../../source/blender/blenlib/BLI_vector.hh#L595)）、`insert`（[L669](../../../source/blender/blenlib/BLI_vector.hh#L669)）、`prepend`（[L736](../../../source/blender/blenlib/BLI_vector.hh#L736)）、`extend_non_duplicates`（[L626](../../../source/blender/blenlib/BLI_vector.hh#L626)）、`Array::Array`（[L90](../../../source/blender/blenlib/BLI_array.hh#L90)）——连"自己人"都只吃 `Span`，可见这条约定有多硬。

### Span 反过来喂给容器

```cpp
Span<int> range = some_vector.as_span().drop_front(1);
Vector<int> owned{range};    // Vector(Span<U>) 拷贝构造所有元素;  L173-L182
Array<int> owned2{range};    // Array(Span<U>) 同上;                L89-L98
```

两者都在构造时**一次性**把 size 定好（`Vector` 走 `reserve(size)` + `uninitialized_convert_n` + `increase_size_by_unchecked`，[L178-L182](../../../source/blender/blenlib/BLI_vector.hh#L178)）。这是从 `Span` 重建容器最省的方式，**比循环 `append` 好**，因为只碰一次容量逻辑。

## 用小数据走一遍

取最普通的 `int`，看两种容器面对"第 5 个元素"时的行为差异。

### Vector 侧

`Vector<int> v;` 之后，三个指针全指向 `inline_buffer_`、`capacity_end_ = inline_buffer_ + 4`，此刻 `size()==0`、`capacity()==4`、`is_inline()==true`、**堆分配 0 次**（[L140-L146](../../../source/blender/blenlib/BLI_vector.hh#L140)）。连续 `append` 四个值 10/20/30/40 后 `size=4` 且 `end_ == capacity_end_`，但还没触发扩容——此时 `is_at_capacity()` 为 `true`（[L1012-L1015](../../../source/blender/blenlib/BLI_vector.hh#L1012)），`is_inline()` 仍是 `true`，**依旧零堆分配**。追加第 5 个 `v.append(50);` 时，`ensure_space_for_one` 的 `4 >= 4` 成立，进入 `realloc_to_at_least(5)`：

| 步骤 | 计算 | 结果 |
| --- | --- | --- |
| 容量检查 | `capacity()=4 >= 5`？ | 否，继续 |
| 最小新容量 | `capacity() * 2 = 4 * 2` | 8 |
| 实际新容量 | `max(min_capacity=5, 8)` | **8** |
| 分配 | `8 * sizeof(int)` | 32 字节，堆 |
| 搬运 | `uninitialized_relocate_n(begin_, 4, new_array)` | 4 个 int 搬家 |
| 释放旧块 | `if (!this->is_inline())` → false | **不释放**（内联缓冲不属于堆） |
| 更新 | `begin_/end_/capacity_end_` 三者重设 | `is_inline()` 变 `false` |

搬运用 `uninitialized_relocate_n`（[`BLI_memory_utils.hh` · L80-L84](../../../source/blender/blenlib/BLI_memory_utils.hh#L80)），比"拷贝构造 + 析构"少一次构造，对非平凡类型尤其重要。

**结论**：第 5 个元素让 `Vector<int>` 经历 **0 → 1 次堆分配**，容量从 4 跳到 8，可用地址全部改变。容量序列继续是 8 → 16 → 32 → 64...

### Array 侧

同样的数据，`Array` 必须在**构造时**就决定要几个——`Array<int> a(4);` 精确 4 个，走 `inline_buffer_`（`4 <= InlineBufferCapacity`）。想加第 5 个，**没有 `append` 可调**，只剩两条路：

```cpp
// 路 A：重新定型（旧元素全丢，需要自己搬）
a.reinitialize(5);      // 4 → 5 超过 InlineBufferCapacity，触发一次精确分配：5 * 4 = 20 字节
a[0] = 10; a[1] = 20; a[2] = 30; a[3] = 40; a[4] = 50;   // [0..3] 得重填

// 路 B：一开始就按上界构造
Array<int> b(5);        // 5 > 4 → 一次精确分配 20 字节，b[4] = 50 直接可用
```

路 A 的代价：`reinitialize` 里 `destruct_n` 干掉了全部 4 个旧元素，然后精确分配 5 个新槽并默认构造（[L430-L455](../../../source/blender/blenlib/BLI_array.hh#L430)）。**你必须自己把 `[0..3]` 重填一遍**——这是语义差异最刺眼处：`Vector` 扩容会**带着数据**搬过去，`Array::reinitialize` 会**扔掉数据**。

### 并列对照

| 时刻 | `Vector<int>` | `Array<int>`（`Array<int>(4)`） |
| --- | --- | --- |
| 刚构造 | 0 元素 / 容量 4 / 内联 / 0 次分配 | 4 元素 / 容量=大小=4 / 内联 / 0 次分配 |
| 填 4 个 | 4 元素 / 满 / 内联 / 0 次分配 | 4 元素 / 满 / 内联 / 0 次分配 |
| 想加第 5 个 | `append` 即可 → 容量 8 + 1 次分配，**数据随迁** | 无接口。只能 `reinitialize(5)`，**数据全丢**、需重填；或另建 `Array<int>(5)` |
| 分配量 | 32 字节（8 个 int，**过度分配 3 个**） | 20 字节（5 个 int，**零过度分配**） |
| 之后还能不能加 | 能，一直到容量 8 | 不能，除非再次 `reinitialize` |

这张表就是决策规则在数据层面的展开：**"过度分配"和"能弹性增长"是同一枚硬币的两面**。

## 反例与边界

### 反例 1：以为 `Array` 有 `push_back`

```cpp
Array<int> arr(3);
arr.push_back(4);   // 编译错误：Array 没有这个成员
```

上一节的接口表里没有任何追加方法。这是**故意的设计限制**，不是遗漏：`Array` 的存在意义就是让"它会变大"在类型层面不可能发生。写出这一行，编译器其实在告诉你——**这个场景该用 `Vector`**。同理 `arr.resize(5)`、`arr.reserve(10)`、`arr.capacity()`、`arr.release()` 全部编译不过。

### 反例 2：`append` 之后继续用旧引用

```cpp
Vector<int> v = {1, 2, 3};
int &ref = v[2];
v.append(4);        // capacity=4，加上去正好满，不扩容
v.append(5);        // 这一步一定扩容到 8，旧内存被弃用
ref = 99;           // 悬空引用；UB，但通常"看起来正常"
```

扩容路径（[L1121-L1151](../../../source/blender/blenlib/BLI_vector.hh#L1121)）会分配新块、搬走元素、**放弃旧块**（堆上则 `deallocate`）。所有指向旧块的 `T *`、`T &`、迭代器立刻失效。这正是 `Vector` 用**下标**而非引用提供"新元素"入口的原因：`append_and_get_index` 返回 `int64_t`，下标在扩容后依然有效——这也是 `append_as` 本版本**故意不返回引用**的合理解释。规避办法：先 `reserve(n)` 再 `append`，或在循环里用下标重取。

### 反例 3：以为 `resize` 会把新元素清零

```cpp
Vector<int> v;
v.resize(10);
// v[0] .. v[9] 全部是未初始化的垃圾值
```

`resize` 增大部分调 `default_construct_n`（[L424](../../../source/blender/blenlib/BLI_vector.hh#L424)），展开成 `std::uninitialized_default_construct_n`（[`BLI_memory_utils.hh` · L43-L46](../../../source/blender/blenlib/BLI_memory_utils.hh#L43)）。对 `int` 这类平凡默认构造类型，标准说**不做任何初始化**；注释也明写了（[L415-L416](../../../source/blender/blenlib/BLI_vector.hh#L415)）。要零值请用 `v.resize(10, 0)` 或 `Vector<int> v(10, 0)`。

`Array` 完全一样：`Array<int> a(10)` 也不清零（[L116-L118](../../../source/blender/blenlib/BLI_array.hh#L116) 写着 "For trivial types like int, default construction does nothing"）。只有 `Array<int> a(10, 0)` 会走 `allocate_zero` 快捷路径（[L139-L141](../../../source/blender/blenlib/BLI_array.hh#L139)）。

### 反例 4：以为 `Array::reinitialize` 会保留旧数据

```cpp
Array<std::string> a = {"aa", "bb", "cc", "dd"};
a.reinitialize(2);
// a[0]、a[1] 是空字符串（重新默认构造），"aa" / "bb" 已不存在
```

`reinitialize` 第一件事就是 `destruct_n(data_, size_)` 把**全部**旧元素析构、`size_` 归零，再按新尺寸默认构造（[L430-L455](../../../source/blender/blenlib/BLI_array.hh#L430)）。名字里的 "reinitialize"（重新初始化）是字面意思，不是"调整大小"。

对平凡类型更隐蔽，因为**看不出差别**：`Array<int> a = {1,2,3,4}; a.reinitialize(2);` 之后 `a[0]`、`a[1]` 的字节仍是 1 和 2——`destruct_n` 对 `int` 是空操作，`default_construct_n` 对 `int` 也是空操作，谁都没动内存，于是代码"碰巧正确"。这不是可依赖的行为：`reinitialize` 从未承诺保留数据，换个元素类型或换次优化就可能翻车。**判断依据要看成写成的语义，而不是看成跑出来的结果。**

### 反例 5：用 `Vector` 或 `Array` 当只读参数

```cpp
void process(const Vector<int> &data);   // 差
void process(const Array<int> &data);    // 同样差，只是换了个容器
void process(Span<int> data);            // 好
```

前两个只能接受各自那一种容器，还暗示了一种它们并不需要的所有权关系。第三条能接受 Blender 里几乎所有连续数据源，且零开销。**推论**：签名写成 `const Vector<T> &` 时先自问有没有用到 `capacity()`、`release()`、`is_inline()` 这些 `Span` 没有的能力；没用就改 `Span`。

### 反例 6：把大元素类型塞进 `Vector` 而不检查 SBO

```cpp
struct Big { char data[200]; };
Vector<Big> v;              // InlineBufferCapacity == 0！
v.append(Big{});            // 第一次 append 就分配 1 个，然后 2、4、8...
```

`default_inline_buffer_capacity(200)` 返回 0（[`BLI_memory_utils.hh` · L274-L277](../../../source/blender/blenlib/BLI_memory_utils.hh#L274)），于是容量从 0 起步，第一跳是 `max(1, 0*2) = 1`——**只分配 1 个**。结论：**大元素类型 + 逐步 `append` = 前几次全浪费在搬运上**，应先 `reserve(expected_count)` 或用 `extend(Span)`。

### 反例 7：在 `reinitialize` 之后假设容量 = 大小

```cpp
Array<int> a(100);      // 堆上 100 个
a.reinitialize(10);     // size=10，但堆上那块仍是 100 个的空间
```

`new_size <= old_size` 分支**原地复用**旧缓冲（[L438-L440](../../../source/blender/blenlib/BLI_array.hh#L438)），**不缩容**。所以 `Array` 也可能持有比 `size()` 更大的内存——只是这个事实**从不通过接口暴露**（没有 `capacity()`）。真要收缩只能重建：`Array<int> compact(a.as_span());`（用 `Span` 构造，精确 size 个）。这说明"`Array` 从不浪费内存"只是个**近似说法**：它不在构造/扩容时过度分配，但 `reinitialize` 缩小时不归还内存。

### 边界：`operator[]` 的断言不是边界检查

```cpp
const T &operator[](int64_t index) const
{
  BLI_assert(index >= 0);
  BLI_assert(index < this->size());
  return begin_[index];
}
```

（[L352-L357](../../../source/blender/blenlib/BLI_vector.hh#L352)；`Array` 版本在 [L216-L221](../../../source/blender/blenlib/BLI_array.hh#L216)）两条 `BLI_assert` 在 release 构建里被整个编译掉。所以 `operator[]` 是**零成本、无检查**的裸访问——快，但越界即 UB。`first()` / `last()` 同理。需要运行时保护时不要指望容器，请自己判 `size()`。

## 对理解 Repeat 的帮助

现在回到正篇 `geometry_nodes_repeat_zone.cc`，它的 `RepeatEvalStorage`（[L98-L111](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L98)）把本篇两个容器都用上了，而且用在了**语义最贴合的位置**：

```cpp
struct RepeatEvalStorage {
  LinearAllocator<> allocator;
  VectorSet<lf::FunctionNode *> lf_body_nodes;
  lf::Graph graph;
  std::optional<LazyFunctionForLogicalOr> or_function;
  std::optional<RepeatZoneSideEffectProvider> side_effect_provider;
  std::optional<RepeatBodyNodeExecuteWrapper> body_execute_wrapper;
  std::optional<lf::GraphExecutor> graph_executor;
  Array<SocketValueVariant> index_values;   // 个数 = iterations，构造时定型
  void *graph_executor_storage = nullptr;
  bool multi_threading_enabled = false;
  Vector<int> input_index_map;              // 按段拼出来，需要 resize / 切片
  Vector<int> output_index_map;
};
```

### `index_values` 为什么是 `Array`

它的使用只有两段，都极短（[L263-L272](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L263)、[L278-L281](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L278)）：

```cpp
if (use_index_values) {
  eval_storage.index_values.reinitialize(iterations);
  threading::parallel_for(IndexRange(iterations), 1024, [&](const IndexRange range) {
    for (const int i : range) { eval_storage.index_values[i].emplace<int>(i); }
  });
}

/* 消费端：把元素地址交给惰性函数图当默认值 */
const SocketValueVariant *index_value = use_index_values ?
                                            &eval_storage.index_values[iter_i] :
                                            &static_unused_index;
lf_node.input(body_fn_.indices.inputs.main[0]).set_default_value(index_value);
```

四点串起来就解释了为什么必须是 `Array`：

1. **大小完全已知，就是 `iterations`**——最纯粹的"构造时定型"场景，正好命中 `Array` 的设计目标。
2. **`reinitialize(iterations)` 一次性精确分配**（[`BLI_array.hh` · L430](../../../source/blender/blenlib/BLI_array.hh#L430)）：没有 `capacity > size` 的浪费，没有二次扩容，也没有"先 append 再发现不够"的可能。这正是 `README.md` 说的"精确大小、一次分配"。
3. **多线程并行填充**（L267-L271）：`parallel_for` 划分区间、各线程写各的 `[i]`，前提是**每个 `i` 都有确定槽位且数组不会移动**。`Array` 天然满足——`reinitialize` 之后 `data_` 不再变，直到下一次 `reinitialize`。若换 `Vector` 边并行边 `append`，扩容会让所有线程的指针同时失效。
4. **只读共享元素地址**：`&eval_storage.index_values[iter_i]` 把元素**地址**交给惰性函数图当默认值（`set_default_value(const SocketValueVariant *)`）。该指针寿命取决于 `Array` 对象，只要不再 `reinitialize` 地址就稳定——`Array` 没有 `append`，**从类型上就保证了没人能偷偷改变它的形状**，这正是"每轮只读共享"需要的契约。

`index_values` 只在有连线时才 `reinitialize`（L263），否则保持空 `Array`。空 `Array` 是**零分配**的（[L78-L82](../../../source/blender/blenlib/BLI_array.hh#L78)：`data_ = inline_buffer_`），所以"没用到"这条路径不付任何代价。同一模式在 foreach-geometry-elements zone 里也出现了（[`geometry_nodes_foreach_geometry_element_zone.cc` · L504-L506](../../../source/blender/nodes/intern/geometry_nodes_foreach_geometry_element_zone.cc#L504)）：`reinitialize(mask.size())`，同样"大小已由掩码算出，一次精确分配"。

### `input_index_map` / `output_index_map` 为什么是 `Vector`

构造段是（[L370-L381](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L370)）：

```cpp
eval_storage.output_index_map.reinitialize(outputs_.size() - 1);
eval_storage.input_index_map.resize(inputs_.size() - 1);
array_utils::fill_index_range<int>(eval_storage.input_index_map, 1);

const int iteration_usage_index = zone_info_.indices.outputs.input_usages[0];
array_utils::fill_index_range<int>(
    eval_storage.output_index_map.as_mutable_span().take_front(iteration_usage_index));
array_utils::fill_index_range<int>(
    eval_storage.output_index_map.as_mutable_span().drop_front(iteration_usage_index),
    iteration_usage_index + 1);
```

五个要点：

**（1）两个 map 用了不同的重置方法，是有意的。** `output_index_map` 用 `reinitialize`（[L458](../../../source/blender/blenlib/BLI_vector.hh#L458)），`input_index_map` 用 `resize`（[L418](../../../source/blender/blenlib/BLI_vector.hh#L418)）。`reinitialize` 是 `clear()` + `resize()`，更清楚地表达"这份映射是全新的"；`resize` 则对应"只成型一次、后面紧接无条件填充"。

**（2）`fill_index_range` 吃的正是 `MutableSpan`。** 签名 `template<typename T> inline void fill_index_range(MutableSpan<T> span, const T start = 0)`，实现只有一行 `std::iota(span.begin(), span.end(), start)`（[`BLI_array_utils.hh` · L440-L443](../../../source/blender/blenlib/BLI_array_utils.hh#L440)）。`Vector<int>` 靠**隐式转换**变成 `MutableSpan<int>`（[`BLI_vector.hh` · L371-L374](../../../source/blender/blenlib/BLI_vector.hh#L371)），不需要写 `as_mutable_span()`；而 `output_index_map` 那两行**显式**写了，因为要在视图上继续链式调 `take_front()` / `drop_front()`。

**（3）为什么输出要分两段填。** 长度是 `outputs_.size() - 1`（第 0 个输出是 `iterations` 的使用标记，单独处理），但值要**跳过** `iteration_usage_index`：前半段填 `0,1,2,...`，后半段从 `iteration_usage_index + 1` 续编号。这就是 `drop_front` + 带 `start` 的 `fill_index_range` 两个重载配合的原因。

**（4）`Vector` 在这里的正当性来自"逐步拼出来"。** 输入映射要跳过第 0 个参数（`fill_index_range(..., 1)` 的起始值 1 就是"跳过"的痕迹），输出映射要在中间挖掉一个位置再续编号。这种"按段构造"的形状不适合 `Array`——`Array` 只有"一次定型"，而这里必须先定型再分段覆写，语义上 `Vector`（可 `resize` / `reinitialize` / 取可变切片）更贴。再加上 `Vector<int>` 的 `InlineBufferCapacity == 4`，而参数个数常常就是 2~4 个，**实际经常连堆分配都不发生**。

**（5）它们最终以 `Span<int>` 的身份被消费。** 两个 `Vector<int>` 被传进 `lf::RemappedParams`（[L177-L181](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L177)），而 `RemappedParams` 的成员声明（[`FN_lazy_function_execute.hh` · L53-L58](../../../source/blender/functions/FN_lazy_function_execute.hh#L53)）里是 `Params &base_params_;`、**`Span<int> input_map_;`**、**`Span<int> output_map_;`**、`bool &multi_threading_enabled_;`。

**`Span<int>`，不是 `const Vector<int> &`**。这就是"与 Span 的关系"那一节的实战版本：执行器只需读这张表，不需要知道它是不是 `Vector`、容量多大、将来会不会变。`RepeatEvalStorage` 保留 `Vector<int>` 的所有权（图创建后反复执行都要用同一张表），执行器只看一段只读区间。**拥有者用 `Vector`，消费者用 `Span`**——分工清晰到没有第三种可能。

### 一句话总括

| 容器 | 在 Repeat 里代表什么 | 为什么是它 |
| --- | --- | --- |
| `Array<SocketValueVariant>` | "第 i 轮的下标值" | 个数 = `iterations`，一次精确分配，地址稳定可共享 |
| `Vector<int>` | "参数重映射表" | 按段拼装，需要 `resize` / `reinitialize` / 可变切片 |
| `Span<int>`（消费端） | "只读地看那张表" | 零开销、不承诺所有权、不关心来源容器 |

理解这三行，`RepeatEvalStorage` 里每个成员的选型就不再是"作者随便挑的"了。

## 继续阅读

- [上一篇 · 03-Span与MutableSpan](03-Span与MutableSpan.md)：`MutableSpan` 为什么必须与 `Span` 分开，以及它和 `SocketItemsRef` 的关系——本篇所有 `as_mutable_span()` 调用点在那篇都有完整交代。
- [下一篇 · 05-VectorSet稳定索引](05-VectorSet稳定索引.md)：`VectorSet` 是 `Vector` 与开放寻址哈希表的合体，它的 `index_of_try` 正是 Repeat 身份机制的核心；读完本篇再看它的 `VectorT` 内部实现会顺很多。
- [本章导航](README.md) 与 [前置知识总入口](../README.md)：本章其余篇目、实测行数总表，以及容器与 Repeat 的对应关系表。
- 源码直读：[`BLI_vector.hh`](../../../source/blender/blenlib/BLI_vector.hh) 建议按本文接口表顺序读 L135-L231（构造）、L390-L530（容量与追加）、L745-L900（访问与删除）、L1050-L1151（release 与扩容）；[`BLI_array.hh`](../../../source/blender/blenlib/BLI_array.hh) 建议顺序读 L74-L174（构造）、L216-L286（访问与 fill）、L368-L455（reinitialize）。
- 可执行的规约：单元测试是最好的规格书。[`BLI_vector_test.cc`](../../../source/blender/blenlib/tests/BLI_vector_test.cc)（1025 行）里 `ReleaseEmptyInline`（L967）、`ReleaseNonEmptyInline`（L991）、`ExtendExceptions`（L853）三组直接对应本篇的 SBO、所有权与异常安全三段论述；[`BLI_array_test.cc`](../../../source/blender/blenlib/tests/BLI_array_test.cc) 的 `Reinitialize`（L271）与 `NoInitializationSizeConstructor`（L171）对应 `reinitialize` 一节。
