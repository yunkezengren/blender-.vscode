# 01 · LinearAllocator 线性分配

[前置知识总入口](../README.md) · [本章导航](README.md) · [下一篇](02-ResourceScope资源作用域.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `LinearAllocator`——"只前进不回收"的分配器，Repeat 的两层 storage 都用它。主要源码：[`BLI_linear_allocator.hh`](../../../source/blender/blenlib/BLI_linear_allocator.hh)（279 行）。

## 先回答一个具体问题

为什么 Blender 要在标准 `malloc` / `free` 之外再造一个分配器？

因为 Repeat Zone 的一次求值里，会动态创建几十上百个**小而短命、同生共死**的对象：`RepeatEvalStorage` 本体、内层 `GenericExecutor`、图里每个节点的 storage、每个未连接输入的值缓冲、每个中间结果的值缓冲。它们是"一次求值"这个动态作用域里的临时产物——同时出生，同时死亡。

对这批对象用 `malloc` / `free` 有两个不可忽视的开销：每次分配都要进一次通用分配器（带 header、查空闲链表、可能加锁），每次释放还要按任意顺序归还。而这个场景的关键特征是：**根本不需要单独释放任何一个对象**。

真正要的不是"更快的分配器"，而是"**把 N 次释放压缩成 1 次**"的能力。这就是 `LinearAllocator` 的出发点。源码头注释写得非常直白（[L24-L28](../../../source/blender/blenlib/BLI_linear_allocator.hh#L24)）：

> "A linear allocator is the simplest form of an allocator. It never reuses any memory, and therefore does not need a deallocation method. It simply hands out consecutive buffers of memory. When the current buffer is full, it allocates a new larger buffer and continues."

注意 "does not need a deallocation method" 这句——不是"没实现"，而是**语义上不存在**。整个类里你找不到 `deallocate`、`free`、`reset` 这类接口（唯一带 "free" 字样的 `free_end_of_previous_allocation` 是特例，见后文）。

## 线性分配的语义

一句话：**只前进、不回收、整块释放**。

- **只前进**：内部只有一个"当前写指针"（bump pointer），每次返回内存后指针往后推，从不回退。
- **不回收**：没有办法单独释放某个对象。哪怕那个对象已经用完，那块内存也继续被占着。
- **整块释放**：所有从系统拿的 chunk 都记录在案，`LinearAllocator` 析构时一次性全部归还。

后两条是一体两面：因为不能单独释放，所以只能整块释放；因为整块释放，所以不需要记住每块内存的边界。代价是**内存占用只增不减**，收益是分配路径极短。

```text
                       LinearAllocator 的内存形态
                       ─────────────────────────

  owned_buffers_  ┌──────────┐   ┌──────────┐   ┌──────────┐
  （只记指针，  │  chunk#0 │   │  chunk#1 │   │  chunk#2 │
    不记大小）  └────┬─────┘   └────┬─────┘   └────┬─────┘
                     │              │              │
                     v              v              v
  内存              ┌──────────┐   ┌──────────────┐  ┌──────────────────┐
                    │ 已满     │   │ 当前正在用    │  │ 已满             │
                    │ 64 B     │   │ 128 B        │  │ 4096 B           │
                    └──────────┘   └──────────────┘  └──────────────────┘
                                   ↑        ↑
                              begin_      end_
                                │          │
                                └─ 剩余 ───┘
                                  （还没切的字节）

  分配请求 ──> 对齐 begin_ ──> 够？ ──> 是 ──> 返回，begin_ 后移
                                   └──> 否 ──> 新建更大的 chunk，重试
```

图里三个关键点：

1. **chunk 之间不连续**。每次不够就向系统再要一块，块与块之间没有物理连续性要求，靠 `owned_buffers_` 这个指针数组串起来。
2. **只有一个活跃 chunk**。`current_begin_` / `current_end_` 描述的永远是最后拿到的那块（或 `allocate_new_buffer` 新要的那块）。之前的所有 chunk 只剩"被记着，等着最后一起还"的作用。
3. **末尾有浪费**。当前 chunk 剩余字节如果塞不下一个请求，那点尾巴就永久浪费了（图中 `begin_` 到 `end_` 之间那截）。这是线性分配的固有碎片，靠"新 chunk 比需求大"来摊薄。

## 为什么快

至少六个原因，前四个是结构性的，后两个是 Blender 特有的实现选择。

**1. 没有空闲链表，也没有每次分配的元数据。** 通用 `malloc` 的每次分配通常带一个 header 记录块大小与状态，`free` 时还要把块插回对应大小的空闲链表、必要时与邻居合并。`LinearAllocator::allocate` 的全部工作就是三次算术：一次对齐、一次加法、一次比较（[L72-L83](../../../source/blender/blenlib/BLI_linear_allocator.hh#L72)）。没有指针追逐，没有分支预测失败。

**2. 没有锁。** `LinearAllocator` 内部没有任何原子操作或互斥量。它是**单线程独占**的：谁说它线程安全，谁就是在埋雷（见反例部分）。Blender 的处理方式是"每个线程一个分配器"，而不是"一个分配器加锁"——在 [`lazy_function_graph_executor_generic.hh` · L322-L329](../../../source/blender/functions/intern/lazy_function_graph_executor_generic.hh#L322) 里能看到 `ThreadLocalStorage { LinearAllocator<> allocator; ... }` 和那句注释 "A separate linear allocator for every thread"。两个线程各推各的指针，天然无竞争。

**3. cache 友好。** 连续切分意味着连续分配出来的对象在内存里**挨着**。遍历一批由同一分配器产出的对象时，访问模式是线性的，对预取器和 TLB 都友好；而一堆零散 `malloc` 出来的对象散落在堆各处，遍历就是随机访问。

**4. 批量释放。** 这是性能收益最大的一条。N 次分配对应的是 M 次真正的系统释放，其中 M 是 chunk 数量，通常是个位数。`RepeatEvalStorage` 一次求值里可能有上千次 `allocate`，析构时只循环 `owned_buffers_` 那么几轮（[L53-L58](../../../source/blender/blenlib/BLI_linear_allocator.hh#L53)）。分配与释放的成本都被摊薄到几乎为零。

**5. chunk 大小是渐进增长的。** `allocate_new_buffer` 里的 [L290](../../../source/blender/blenlib/BLI_linear_allocator.hh#L290)：

```cpp
const int grow_size = 1 << std::min<int>(owned_buffers_.size() + 6, 20);
```

第一块 64 字节（`1<<6`），随后 128、256、512……一路翻倍到 `1<<20`（1 MB）封顶，再与 `large_buffer_threshold`（4096）取小。这意味着**小块对象只需极少数几次系统分配**就能容纳大量对象，把"每次分配一次系统调用"降成"每个 chunk 一次"。

**6. 模板参数可以换成不带调试开销的底层分配器。** `template<typename Allocator = GuardedAllocator>` 的默认值是 Blender 自己的 `GuardedAllocator`（[`BLI_allocator.hh` · L41](../../../source/blender/blenlib/BLI_allocator.hh#L41)），它最终走 `MEM_new_uninitialized_aligned`。也就是说：**调试期的内存统计只作用在 chunk 级别，不会作用在对象级别**——既保留了可观测性，又不给每个小对象付统计代价。

## 内部结构

这个类小得出奇。完整的私有状态只有四项（[L30-L39](../../../source/blender/blenlib/BLI_linear_allocator.hh#L30)）：

```cpp
BLI_NO_UNIQUE_ADDRESS Allocator allocator_;
Vector<void *, 2> owned_buffers_;

uintptr_t current_begin_;
uintptr_t current_end_;

constexpr static int64_t large_buffer_threshold = 4096;
```

逐项说明：

| 字段 | 类型 | 作用 |
| --- | --- | --- |
| `allocator_` | `Allocator`（默认 `GuardedAllocator`） | 真正向系统要内存的人。`BLI_NO_UNIQUE_ADDRESS` 表示它是空类时不占空间——`GuardedAllocator` 无状态，所以整个字段零字节 |
| `owned_buffers_` | `Vector<void *, 2>` | 所有"我拥有的" chunk 的裸指针列表。**只存指针，不存每块的大小**——因为最后一次性 `deallocate` 不需要知道大小 |
| `current_begin_` | `uintptr_t` | 当前 chunk 里下一个可切分的字节位置。这就是 bump pointer |
| `current_end_` | `uintptr_t` | 当前 chunk 的末尾。`current_end_ - current_begin_` 是剩余字节 |
| `large_buffer_threshold` | `constexpr static int64_t` | 4096。超过它的请求不塞进当前 chunk，直接单独分配，避免为一个大对象浪费一整块小 chunk |

三个设计细节值得单独点出：

**用 `uintptr_t` 而不是裸指针。** `current_begin_` / `current_end_` 是整数类型，对齐运算可以直接用位运算完成，不用在指针与整数之间来回 `reinterpret_cast`。初始值是 `0`（[L47-L51](../../../source/blender/blenlib/BLI_linear_allocator.hh#L47)），于是**空分配器的第一次分配必然走"新建 chunk"路径**：`potential_allocation_end = 0 + size`，与 `current_end_ = 0` 比较必然失败。这是个干净的初始状态，不需要额外标志位。

**`Vector<void *, 2>` 的内联容量是 2。** 前两个 chunk 的指针存在 `Vector` 自身的栈内缓冲里，连记账数组都不需要堆分配。这对"只分配几块就结束"的短命分配器是个免费的优化。

**没有 freelist，也没有 chunk 头。** 对比典型的内存池实现会为每块加一个 `{size, next}` 头，这里完全不需要——chunk 大小只在 `allocate_new_buffer` 里用一次，之后再也不查。

关键常量 `large_buffer_threshold = 4096` 的作用在 [L84-L91](../../../source/blender/blenlib/BLI_linear_allocator.hh#L84)：

```cpp
if (size <= large_buffer_threshold) {
  this->allocate_new_buffer(size + alignment, alignment);
  return this->allocate(size, alignment);
}
return this->allocator_large_buffer(size, alignment);
```

小请求走"新开 chunk 再重试"，大请求走"单独 `allocated_owned`"。两条路径都会把指针 `append` 进 `owned_buffers_`，所以**大 buffer 同样会被析构时释放**，不会被漏掉。区别只在内存布局：大 buffer 独占一块，不与小块混居——这正是注释里 "to avoid wasting memory" 的意思。

## 核心接口

| 接口 | 返回 | 是否构造对象 | 用途 |
| --- | --- | --- | --- |
| `allocate(size, alignment)` | `void *` | 否 | 最底层，切一块原始内存 |
| `allocate<T>()` / `allocate(const CPPType &)` | `T *` / `void *` | 否 | 按类型取 size 与 alignof |
| `allocate_array<T>(n)` | `MutableSpan<T>` | 否 | 切一段数组，元素**未构造** |
| `allocate_array(const CPPType &, n)` | `void *` | 否 | 运行时类型的数组 |
| `construct<T>(args...)` | `destruct_ptr<T>` | 是 | 分配 + placement new |
| `construct_array<T>(n, args...)` | `MutableSpan<T>` | 是 | 分配 + 逐元素构造 |
| `construct_array_copy<T>(Span<T>)` | `MutableSpan<T>` | 是 | 分配 + 拷贝构造 |
| `copy_string(StringRef)` | `StringRefNull` | 是 | 分配 + 拷贝字符串（带 `\0`） |
| `provide_buffer(buf, size)` | — | — | 用外部缓冲当第一块 chunk，不接管所有权 |
| `transfer_ownership_from(other)` | — | — | 把另一个分配器的 chunk 全接管过来 |

### allocate：整个分配器的核心只有十几行

```cpp
const uintptr_t alignment_mask = alignment - 1;
const uintptr_t potential_allocation_begin = (current_begin_ + alignment_mask) & ~alignment_mask;
const uintptr_t potential_allocation_end = potential_allocation_begin + size;

if (potential_allocation_end <= current_end_) {
  current_begin_ = potential_allocation_end;
  return reinterpret_cast<void *>(potential_allocation_begin);
}
```

三段式语义：**先对齐、再判断、最后推进**。

- 对齐：`(begin + mask) & ~mask` 是标准的向上取整到 2 的幂。前置断言要求 `alignment` 是 2 的幂且 ≥ 1（[L68-L70](../../../source/blender/blenlib/BLI_linear_allocator.hh#L68)）。
- 判断：只比 `<=`，注意比较的是**对齐后的结束地址**，所以对齐产生的空隙被正确计入消耗。
- 推进：`current_begin_` 直接跳到 `potential_allocation_end`，而不是 `+size`——这样对齐填充不会被重复计算。

一个常被忽略的细节：源码头注释明确写了 "The alignment has to be a power of 2"（[L64](../../../source/blender/blenlib/BLI_linear_allocator.hh#L64)）。它不是建议，是**前置条件**：传 3 会得到未定义行为而不是断言（断言只在 debug 版生效）。

### allocate_array：只是乘一下

```cpp
template<typename T> MutableSpan<T> allocate_array(int64_t size)
{
  T *array = static_cast<T *>(this->allocate(sizeof(T) * size, alignof(T)));
  return MutableSpan<T>(array, size);
}
```

注意 `alignof(T)` 而不是 `alignof(T) * n`：数组元素天然按 `sizeof(T)` 递增，只要首地址对齐到 `alignof(T)`，全部元素就都对齐。同时注释反复强调 "This method only allocates memory and does not construct the instance"——它返回的 `MutableSpan<T>` 里的元素**处于未构造状态**，直接读是 UB。

### construct：返回 destruct_ptr 才是重点

```cpp
template<typename T, typename... Args> destruct_ptr<T> construct(Args &&...args)
{
  void *buffer = this->allocate(sizeof(T), alignof(T));
  T *value = new (buffer) T(std::forward<Args>(args)...);
  return destruct_ptr<T>(value);
}
```

两行动作：切内存、placement new。第三行才是设计决策——**返回值不是 `T *`，而是 `destruct_ptr<T>`**。注释 [L132-L133](../../../source/blender/blenlib/BLI_linear_allocator.hh#L132) 说得清楚：

> "You must not call `delete` on the returned value. Instead, only the destructor has to be called."

`destruct_ptr` 的析构只调 `T::~T()`，不去碰内存——因为内存不归它管，归分配器管。Repeat 里那一行 `allocator.construct<RepeatEvalStorage>().release()` 的 `.release()` 就是主动放弃这份"我只负责析构"的托管，把责任交给 `destruct_storage`，因为框架只认 `void *`。

### construct_array：构造但不返回 RAII 句柄

```cpp
template<typename T, typename... Args>
MutableSpan<T> construct_array(int64_t size, Args &&...args)
```

它返回 `MutableSpan<T>`，不是 `destruct_ptr` 的数组。注释 [L144-L145](../../../source/blender/blenlib/BLI_linear_allocator.hh#L144) 明确："The caller is responsible for calling the destructor (and not `delete`) on the constructed elements." 也就是说这里**没有 RAII 兜底**——漏调析构就是漏调，编译器不会提醒。对应的补救工具是 `BLI_memory_utils.hh` 里的 `destruct_n(ptr, n)`（[L34](../../../source/blender/blenlib/BLI_memory_utils.hh#L34)），它对 trivially destructible 类型是空操作。

### 三个不那么常用的接口

`provide_buffer(void *buffer, int64_t size)`（[L217-L222](../../../source/blender/blenlib/BLI_linear_allocator.hh#L217)）把一块**外部已有的内存**当作当前 chunk 用，断言 `owned_buffers_.is_empty()`——也就是只能在使用前调用一次。它**不接管所有权**，析构时不会释放这块外部内存。这是"调用方已有栈上或大块缓冲，别再去系统要"的优化入口，`ResourceScope` 就是这样把自身缓冲交给内部 `LinearAllocator` 的（[`resource_scope.cc` · L38-L43](../../../source/blender/blenlib/intern/resource_scope.cc#L38)）。

`free_end_of_previous_allocation(original_size, free_after)`（[L241-L260](../../../source/blender/blenlib/BLI_linear_allocator.hh#L241)）是"绝不回收"的唯一例外：**只能回退最后一次分配的尾部**。注释 [L237-L239](../../../source/blender/blenlib/BLI_linear_allocator.hh#L237) 解释了为什么值得为此开口子——某些算法先按上界超量分配、算完后把用不完的尾巴还回去。而且如果原分配大于阈值（单独成块），这个操作直接什么都不做，因为那块内存不在当前 chunk 里。

`transfer_ownership_from(LinearAllocator<> &other)`（[L269-L279](../../../source/blender/blenlib/BLI_linear_allocator.hh#L269)）把 `other` 的 chunk 数组整体搬过来，然后 `other` 被原地重建为一个空分配器。它的语义是"**把一堆小分配器的产物汇总到主分配器**"——多线程并行任务各自用局部线性分配器，结束后把所有权交给主分配器，主分配器活得比它们久。`BLI_kdtree.cc` 与 `index_mask.cc` 都是这个用法。

## destruct_ptr 是什么

它在 [`BLI_memory_utils.hh` · L107-L111](../../../source/blender/blenlib/BLI_memory_utils.hh#L107)，一共五行：

```cpp
/**
 * A destruct_ptr is like unique_ptr, but it will only call the destructor and will not free the
 * memory. This is useful when using custom allocators.
 */
template<typename T> using destruct_ptr = std::unique_ptr<T, DestructValueAtAddress<T>>;
```

关键全在 deleter 上（[L96-L105](../../../source/blender/blenlib/BLI_memory_utils.hh#L96)）：

```cpp
template<typename T> struct DestructValueAtAddress {
  DestructValueAtAddress() = default;
  template<typename U> DestructValueAtAddress(const U &) {}
  void operator()(T *ptr) { ptr->~T(); }
};
```

`operator()` 里只有 `ptr->~T()`。没有 `operator delete`，没有 `free`，没有 `MEM_delete_void`。所以 `destruct_ptr<T>` 的全套语义是：

| 行为 | `unique_ptr<T>` | `destruct_ptr<T>` |
| --- | --- | --- |
| 离开作用域 | 调析构 + `delete` 内存 | **只调析构** |
| 独占所有权 | 是 | 是（不可拷贝，可移动） |
| `reset()` | 析构并释放 | 只析构 |
| `release()` | 放弃托管，返回裸指针 | 同左 |
| 能配合 `new` 用吗 | 能 | **不能**——内存不会被还，必漏 |
| 必须配合分配器 | 否 | 是 |

注意那个模板化构造函数 `template<typename U> DestructValueAtAddress(const U &) {}`：它的存在是为了让 `unique_ptr` 在构造 deleter 时"接受任何参数"，本质是个空壳适配器（`unique_ptr` 要求 deleter 可从 `std::default_delete` 之类的东西构造）。它不存任何状态，所以 `destruct_ptr<T>` 与裸指针同大小——零开销。

这份分工是整章的核心：**分配器管内存的来去，对象管构造与析构**。`destruct_ptr` 就是把"对象的析构义务"从"内存的释放义务"里剥出来、单独打包成一个 RAII 句柄。`ResourceScope::add(destruct_ptr<T>)`（[`BLI_resource_scope.hh` · L96](../../../source/blender/blenlib/BLI_resource_scope.hh#L96)）正是接收这份"只管析构"的托管契约。

## 析构时的责任

这是本篇**最容易踩的坑**，务必读两遍。`LinearAllocator` 的析构函数全文只有这些（[L53-L58](../../../source/blender/blenlib/BLI_linear_allocator.hh#L53)）：

```cpp
~LinearAllocator()
{
  for (void *ptr : owned_buffers_) {
    allocator_.deallocate(ptr);
  }
}
```

它遍历 chunk 指针，把每块内存还给 `allocator_`。**它不知道 chunk 里构造过什么对象，也不会调用任何一个析构函数。** 分配器全程只处理 `void *`，它从来没有记录过"这块内存里放过一个 `std::string`"这类信息。

所以使用 `LinearAllocator` 时，你只有两种合法选择：

**选择 A：对象是 trivially destructible 的。** POD、`int`、`float`、`float3`、裸指针、`Span`、没有自定义析构的聚合体。这类对象的析构函数是空操作，不调也没关系。这也是为什么 Blender 的线性分配器场景里大量出现 `allocate<T>()` + `type.copy_construct()` 的组合——用 `CPPType` 手工管理构造与析构，而 `destruct_n` 对 trivial 类型直接 return（[`BLI_memory_utils.hh` · L34-L41](../../../source/blender/blenlib/BLI_memory_utils.hh#L34)）。

**选择 B：调用方在分配器析构前，对每个非平凡对象手动调析构。** 用 `destruct_ptr`（它替你做）、或 `destruct_n`、或 `std::destroy_at`。顺序有硬约束：**先析构对象，后销毁分配器**。反过来的话，析构函数里任何一次对自身成员的访问都读到了已归还的内存——use-after-free。

正确顺序长这样，`RepeatEvalStorage` 就是这个模式的标本：

```cpp
void destruct_storage(void *storage) const override
{
  RepeatEvalStorage *s = static_cast<RepeatEvalStorage *>(storage);
  if (s->graph_executor_storage) {
    s->graph_executor->destruct_storage(s->graph_executor_storage);  // 1. 先析构内层对象
  }
  std::destroy_at(s);                                                // 2. 再析构本层对象
}
// 3. 框架随后销毁外层 LinearAllocator —— 这时才真正还内存
```

三步的顺序不能动：内层 storage 的销毁需要**还活着的**内层 executor 来执行（它知道 storage 的真实类型），而 `std::destroy_at(s)` 会析构 `s` 里的 `allocator` 字段——那一刻内层 storage 占的内存就被还了。所以 2 必须在 1 之后。

## 在 Repeat 中的双套结构

Repeat 的两层 storage 都用 `LinearAllocator`，形成与函数调用嵌套一致的**生命周期嵌套**。

外层在 [`geometry_nodes_repeat_zone.cc` · L139-L142](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L139)：

```cpp
void *init_storage(LinearAllocator<> &allocator) const override
{
  return allocator.construct<RepeatEvalStorage>().release();
}
```

这里的 `allocator` 参数**不是** `RepeatEvalStorage` 自己的字段，而是**外层调用链的分配器**——由 `LazyFunction::init_storage` 的签名决定（[`FN_lazy_function.hh` · L273](../../../source/blender/functions/FN_lazy_function.hh#L273)）：

```cpp
virtual void *init_storage(LinearAllocator<> &allocator) const;
```

这个签名是整个框架的约定：**storage 不由函数对象持有，而是从调用方的分配器上切**。谁发起这次调用，谁管这块内存的生死。对 Repeat 来说，发起者是外层 `GenericExecutor` 的 `main_allocator_`（[`lazy_function_graph_executor_generic.hh` · L331](../../../source/blender/functions/intern/lazy_function_graph_executor_generic.hh#L331)），调用点在 L937 的 `node_state.storage = fn.init_storage(allocator);`。

而 `RepeatEvalStorage` 内部还有**自己的**一个分配器字段（[L99](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L99)）：

```cpp
struct RepeatEvalStorage {
  LinearAllocator<> allocator;
  ...
};
```

它服务的是内层（[L400-L401](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L400)）：

```cpp
eval_storage.graph_executor_storage = eval_storage.graph_executor->init_storage(
    eval_storage.allocator);
```

为什么必须嵌套两层？

**理由 1：内层执行器的 object 必须活到内层 storage 析构为止，而它的构造时机更晚。** `graph_executor` 是 `std::optional`，直到第一次 `execute_impl` 才 `emplace`（[L394-L399](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L394)）。外层分配器在 `init_storage` 时就已经存在了，但那时还什么都不该分配——因为 `iterations` 还没拿到，图的大小未知。所以外层只分配 `RepeatEvalStorage` 这个固定大小的壳，把"内层的动态部分"留给内层分配器，**在内层对象就位后再统一从内层分配**。

**理由 2：两层析构顺序被结构强制。** 内层 `allocator` 是 `RepeatEvalStorage` 的成员，它的析构自然发生在 `std::destroy_at(s)` 时，也就是在 `destruct_storage` 里内层对象已经被析构之后。这个顺序不需要手写代码维护，是**结构本身**保证的。

**理由 3：内存归属清晰，便于整体转移。** 外层分配器属于调用方；内层分配器属于这次求值的 `RepeatEvalStorage`。如果哪天需要把整个 Repeat 求值的产物交给上游，`transfer_ownership_from(eval_storage.allocator)` 一句话就能办到——前提是它们在不同的分配器上。

**理由 4：内层执行器还有第三层分配器。** `GenericExecutor` 自己有 `main_allocator_` 与每线程一个 `ThreadLocalStorage::allocator`（[L322-L331](../../../source/blender/functions/intern/lazy_function_graph_executor_generic.hh#L322)）。所以实际至少有四层：外层图分配器 → Repeat 的 allocator → 内层 executor 的 `main_allocator_` → 每线程分配器。每一层都严格包含在上一层里，析构顺序天然是逆序的。

## 与 ResourceScope 的分工

两个机制经常被混着谈，但解决的问题完全不同：

| 维度 | `LinearAllocator` | `ResourceScope` |
| --- | --- | --- |
| 管什么 | **内存从哪来** | **对象何时析构** |
| 认识对象类型吗 | 不认识（只处理 `void *`） | 认识（登记了 free 函数指针） |
| 析构顺序 | 无序（只是把块还回去） | **严格逆序**，晚加的早析构 |
| 能否单独释放一个 | 不能（整块） | 能，逐个回调 |
| 分配本身 | 自己就是分配器 | **内部含一个 `LinearAllocator<>`** |
| 典型场景 | 一次求值内的临时对象 | 构建期产物、跨求值存活 |

`ResourceScope` 不是一个替代方案，它是**建在 `LinearAllocator` 之上**的一层：`ResourceScope` 内部持有 `LinearAllocator<> &allocator_`（[`BLI_resource_scope.hh` · L52](../../../source/blender/blenlib/BLI_resource_scope.hh#L52)），既可以自己 `create_own_allocator`，也可以由调用方传入一个（[L76](../../../source/blender/blenlib/BLI_resource_scope.hh#L76)）。它在上面挂一个 `ChunkedList<ResourceData>` 记录 `{data, free}` 对，析构时逆序调用。

两者的职责边界在 Repeat 里划得非常清楚：

- `LazyFunctionForRepeatZone` 对象本身用 `ResourceScope` 构造（[L423-L430](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc#L423)）：`scope.construct<LazyFunctionForRepeatZone>(...)`。它跨多次求值存活，且不同类型混在一起。
- 一次求值的 `RepeatEvalStorage` 与 `graph_executor_storage` 用 `LinearAllocator`：同生共死、全是一次性产物、不需要单独释放任何一个。

`destruct_ptr` 是两者的接缝：`LinearAllocator::construct<T>()` 产出 `destruct_ptr<T>`，`ResourceScope::add(destruct_ptr<T>)` 接收它。前者提供内存，后者接管析构义务。

## 用小数据走一遍

假设 `sizeof(std::string) == 32`、`alignof(std::string) == 8`（libstdc++ 与 MSVC 都是这个值，具体数值并非标准保证）。代码：

```cpp
blender::LinearAllocator<> alloc;
int *i0 = alloc.allocate<int>();          // 4 字节，对齐 4
int *i1 = alloc.allocate<int>();
int *i2 = alloc.allocate<int>();
destruct_ptr<std::string> s0 = alloc.construct<std::string>("hello");
destruct_ptr<std::string> s1 = alloc.construct<std::string>("world, longer text");
```

逐步跟踪。**初始状态**：`current_begin_ = 0`、`current_end_ = 0`、`owned_buffers_` 为空。

**1. 分配 i0。** 对齐后 `potential_begin = 0`，`end = 4`；`4 <= 0` 不成立 → 走 `allocate_new_buffer(4 + 4, 4)`。`owned_buffers_.size()` 为 0，`grow_size = 1 << 6 = 64`，`size_in_bytes = max(8, 64) = 64`（未超 4096，不截断）。chunk #0 = 64 字节。递归重试：`begin=0`、`end=4`，成立 → `i0 = chunk0+0`，`current_begin_ = 4`。

**2. 分配 i1。** `potential_begin = align(4,4) = 4`，`end = 8 <= 64` → 成立。`i1 = chunk0+4`，`current_begin_ = 8`。

**3. 分配 i2。** 同理 `i2 = chunk0+8`，`current_begin_ = 12`。到这里 chunk #0 用了 12 字节，剩 52。

**4. 构造 s0。** `align(12, 8) = 16`（`(12+7) & ~7 = 19 & ~7 = 16`），`end = 16 + 32 = 48 <= 64` → **塞进当前 chunk**。`s0` 在 `chunk0+16`，占 16..47，`current_begin_ = 48`。注意 12→16 之间那 4 字节是**对齐填充**，永久浪费。调用 `new (chunk0+16) std::string("hello")`。

**5. 构造 s1。** `align(48, 8) = 48`，`end = 48 + 32 = 80 > 64` → **塞不下**。走 `allocate_new_buffer(32 + 8, 8)`：`owned_buffers_.size()` 现在是 1，`grow_size = 1 << 7 = 128`，`size_in_bytes = max(40, 128) = 128`。chunk #1 = 128 字节。递归重试：`s1` 在 `chunk1+0`，占 0..31，`current_begin_ = 32`，`current_end_ = 128`。

最终状态：

```text
chunk #0  (64 B)                     chunk #1  (128 B)
┌────┬────┬────┬────┬──────────┬─────┐ ┌──────────┬───────────────────────────┐
│ i0 │ i1 │ i2 │pad │   s0     │ 废  │ │    s1    │        剩余 96 B          │
│ 0  │ 4  │ 8  │12-16│ 16..47  │48-64│ │  0..31   │  32 .. 127                │
└────┴────┴────┴────┴──────────┴─────┘ └──────────┴───────────────────────────┘
                                    ↑                                    ↑
                              begin_ 曾到 48                        begin_ = 32
owned_buffers_ = [chunk0, chunk1]   ← 2 个指针，向量内联容量正好装下
```

总计：3 个 int + 2 个 string 共 5 次 `allocate` 调用，只触发了 **2 次**系统分配。若用 `malloc` / `free`，是 5 次分配 + 5 次释放，外加 5 个 header。

现在看析构时的分界线。按上面的代码，`s0` 与 `s1` 是 `destruct_ptr`，**离开作用域时自动调 `~string()`**——这会释放它们各自内部的堆缓冲，字符串内容被正确回收。然后是 `alloc.~LinearAllocator()`：循环两次 `deallocate`，把 chunk #0 与 chunk #1 还给 `MEM_delete_void`。

**被调用的析构函数**：`~basic_string()` × 2（由 `destruct_ptr` 触发）。**没被调用的析构函数**：如果代码改成裸 `std::string *s0 = ...`，且忘了手动 `std::destroy_at`，那么两个 `~basic_string()` **一次都不会执行**——字符串内部的堆缓冲全部泄漏，而 chunk 内存却干干净净地还掉了。这种"部分泄漏"极难排查：分配器显示一切正常，只有进程 RSS 在涨。

## 反例与边界

**1. 以为 allocator 析构会自动调对象析构。** 最常见也最致命。析构函数就那三行循环（[L53-L58](../../../source/blender/blenlib/BLI_linear_allocator.hh#L53)），完全不含任何对象信息。记住：**它只还块，不管对象**。含 `std::string` / `Vector` / 任何持有堆资源的成员的结构体，都必须显式析构。

**2. 在 allocator 销毁后继续用其中的对象。** chunk 已归还给 `MEM_*`，指针立刻悬空。典型写法是让 `init_storage` 返回的指针越过 `destruct_storage` 存活，或把 `RepeatEvalStorage` 里的 `Span` 缓存到跨调用的地方。`destruct_ptr` 一旦随 allocator 一起消失，任何残留副本都是 use-after-free。

**3. 跨 allocator 释放指针。** `LinearAllocator` 没有 `deallocate(void *)`，所以你不可能"还错"——但你可能把 A 分配器切出来的指针交给 B 的 `transfer_ownership_from` 之外的手段去管理。如果 A 先于 B 析构，指针提前失效。多线程场景更要小心：`transfer_ownership_from` 必须在源分配器析构**之前**调用，否则 chunk 列表已经被清空，接管到的是空集。

**4. 以为是线程安全的。** 没有任何锁、没有任何原子量。`allocate` 里的 `current_begin_` 是普通成员（[L34](../../../source/blender/blenlib/BLI_linear_allocator.hh#L34)），两个线程同时分配就是数据竞争，会切出重叠的两块内存——比崩溃更糟，是静默的数据损坏。Blender 的解法是每线程一个分配器（[`lazy_function_graph_executor_generic.hh` · L322-L329](../../../source/blender/functions/intern/lazy_function_graph_executor_generic.hh#L322)），或者根本不开多线程（`multi_threading_enabled` 为 false 时用 `main_allocator_`）。

**5. 以为对齐参数可以随便传。** `is_power_of_2(alignment)` 只是 `BLI_assert`，Release 构建下**不会检查**。传 `alignment = 3` 会得到 `mask = 2`、`(begin+2) & ~2` 这种荒谬结果，返回一个未对齐的指针。同样 `size < 0` 也不会被拦住。这些是"调试期断言、发布期 UB"的典型边界。

**6. 对超过 4096 字节的请求期待"打包"。** 大块走 `allocator_large_buffer` → 单独 `allocated_owned`，完全无视当前 chunk 的剩余空间。所以在大对象之间混入小对象，剩余空间不会被利用——这不是 bug，是避免 "为一个大对象浪费整块 chunk" 的取舍。推论：`allocate_array` 请求的字节数决定走哪条路，不是元素个数。

**7. 期望 `free_end_of_previous_allocation` 能释放任意对象。** 它只能回退**最后一次分配**的尾巴，且如果那次分配大于阈值就完全无效（[L244-L246](../../../source/blender/blenlib/BLI_linear_allocator.hh#L244)）。中间的对象永远收不回。它的用途是"超量分配后还尾"，不是通用释放。

**8. 用 `provide_buffer` 之后忘了外部缓冲的生命周期。** `provide_buffer` 不接管所有权，析构时不会释放它。如果那块内存来自一个更早结束的作用域，分配器会在上面继续切分——切到别人的栈或已归还的堆上。相关的是 `transfer_ownership_from` 的注释（[L262-L268](../../../source/blender/blenlib/BLI_linear_allocator.hh#L262)）：调用方要保证 `provide_buffer` 传进去的缓冲活得比接收方久。

**9. 把 `destruct_ptr` 和 `new` 一起用。** `destruct_ptr<T> p(new T(...))` 编译通过（`unique_ptr` 接口需要），但析构时只调 `~T()`，`new` 出来的内存永远不还。这是唯一能"配错对象"的地方，务必用 `allocator.construct<T>()`。

**10. 在 `construct` 之后对返回值做多余的事。** `allocator.construct<T>()` 返回的 `destruct_ptr` 一旦离开作用域就析构对象，但内存仍在 chunk 里。如果继续把它当有效对象用（比如存了个裸指针到别处），行为是"读已析构对象"——对 `std::string` 就是读已释放的堆缓冲。`.release()` 之后更是把责任彻底交给调用方，编译器不再兜底。

## 对理解 Repeat 的帮助

把上面的机制映射回正篇 04-01 的三处代码，一切就都不再是魔法。

**`RepeatEvalStorage` 的 `allocator` 字段**（L99）不是装饰，它是内层 `graph_executor_storage` 的唯一内存来源。这个字段的析构时点决定了内层 storage 的内存何时真正归还：`std::destroy_at(s)` 在 `destruct_storage` 里发生时，内层对象已经析构完毕，所以内层分配器可以安全地整块释放。

**`init_storage` 的两层分配**（L139-L142 与 L400-L401）解释了为什么 Repeat 需要两层：外层只切出一个固定大小的 `RepeatEvalStorage` 壳（连 `allocator` 在内），`std::optional` 字段全部空着；等 `iterations` 输入到手、图能定型了，才由内层分配器承担动态部分的分配。这正是"`init_storage` 里不构建图"这条结论的内存侧理由——**未知规模的东西不该从固定大小的壳里预分配**。

**`graph_executor_storage` 的分配位置**（L400-L401）还给出一条可验证的推论：它在 `initialize_execution_graph` 里，也就是 `!eval_storage.graph_executor` 的首次分支里。因为 `graph_executor_storage` 是内层 executor 的 storage，而内层 executor 是刚 `emplace` 出来的（L394-L399），所以 `init_storage` 必须在它之后、且在同一次调用内完成。`destruct_storage` 里的 `if (s->graph_executor_storage)` 判断也是必要的——若图从未构建过（例如输出从未被请求），这两个字段都是默认值，内层分配器里一个对象都没构造过。

最后把整条生命周期串起来，就是"一次求值"的全部内存故事：

```text
外层 GenericExecutor 的 main_allocator_
   │
   ├─ init_storage(外层 allocator)  ──> RepeatEvalStorage 壳（含内层 allocator 字段）
   │                                         │
   │                                         ├─ 首次 execute_impl：graph_executor.emplace()
   │                                         └─ init_storage(内层 allocator)
   │                                                └─> GenericExecutor 对象（含 main_allocator_ 与每线程分配器）
   │
   ├─ execute_impl × 1：内层 executor 跑完全部迭代
   │
   ├─ destruct_storage：先内层 destruct_storage，再 std::destroy_at(RepeatEvalStorage)
   │                     ↑ 内层 allocator 在此整块释放
   │
   └─ 外层 allocator 最终析构：RepeatEvalStorage 那几十字节也归还原处
```

注意最后两步的顺序：**内层先，外层后**。每一层都严格遵守"先析构对象、后销毁分配器"的规则，而"层与层之间"的顺序由调用链天然决定。这就是线性分配最舒适的用法——当所有对象的生死严格嵌套时，你不需要任何引用计数、任何图算法，只需要保证析构顺序与构造顺序相反。

## 继续阅读

- [下一篇：02-ResourceScope资源作用域](02-ResourceScope资源作用域.md)——`LinearAllocator` 的搭档，回答"对象何时析构"。
- [03-destruct_ptr与所有权](03-destruct_ptr与所有权.md)——把本篇里那个"只调析构不 free"的句柄讲透。
- [本章导航](README.md)——三套机制的对照总表。
- 源码：[`BLI_linear_allocator.hh`](../../../source/blender/blenlib/BLI_linear_allocator.hh)、[`BLI_memory_utils.hh`](../../../source/blender/blenlib/BLI_memory_utils.hh)、[`BLI_allocator.hh`](../../../source/blender/blenlib/BLI_allocator.hh)、[`BLI_resource_scope.hh`](../../../source/blender/blenlib/BLI_resource_scope.hh)。
- 单元测试：[`BLI_linear_allocator_test.cc`](../../../source/blender/blenlib/tests/BLI_linear_allocator_test.cc)——`PackedAllocation` 那个用例（L37-L57）用精确的偏移量验证了本篇"用小数据走一遍"里的对齐与打包行为，值得对照着读。
- 真实的三层调用链：[`lazy_function_graph_executor_generic.hh` · L322-L348](../../../source/blender/functions/intern/lazy_function_graph_executor_generic.hh#L322)（`ThreadLocalStorage` / `main_allocator_` / `LocalData`）。
