# CS-02 Task、POD 与"wait 会干活"

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:16px 0 20px;padding:10px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px">
<span style="font-size:11px;font-weight:700;letter-spacing:.1em;color:#64748B;margin-right:2px">导航</span>
<a href="../README.md" style="font-size:13px;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">总入口</a>
<a href="./README.md" style="font-size:13px;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">本章 07-调用栈与调试</a>
<a href="./01-主线程栈与depsgraph求值链路.md" style="font-size:13px;color:#7C3AED;background:#F5F3FF;border:1px solid #DDD6FE;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">‹ 主线程栈与depsgraph求值链路</a>
</div>

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;margin:18px 0 22px;padding:14px 18px;background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:10px">

**基准说明**：Blender **5.4.0-alpha** 本地工作树。
本文由一次断点栈出发，回答三个问题：

1. **POD 这个 C++ 术语到底指什么**，`Task` 算不算；
2. 这张栈为什么同时包含**"等待"和"构建"**两种语义；
3. `isolate` / `CacheMutex` / `FunctionRef` 各自在这条链上解决什么问题。

**前置阅读**：[07-01](01-主线程栈与depsgraph求值链路.md)（五层职责、构建期与执行期分界）。

</div>

## §0 这张栈最反直觉的一点

先看栈的**底部**（最老 → 最新）：

```
evaluate_graph_threaded_stage       deg_eval.cc:361
└─ BLI_task_pool_work_and_wait      task_pool.cc:457
   └─ TaskPool::work_and_wait       task_pool.cc:281
      └─ tbb_task_pool_work_and_wait    task_pool.cc:360
         └─ tbb_group->wait()       tbb/task_group.h:598
            └─ tbb::detail::d1::wait    tbb/detail/_task.h:243
               └─ tbb12_debug.dll
                  └─ function_task<Task>::execute   tbb/task_group.h:101
                     └─ task_ptr_or_nullptr         tbb/task_group.h:167
                        └─ Task::operator()         task_pool.cc:120
                           └─ deg_task_run_func     deg_eval.cc:118
                              └─ evaluate_node      deg_eval.cc:101
                                 └─ build_nodetree lambda   deg_builder_nodes.cc:2066
                                    └─ ... → build_repeat_zone_function   :2245
```

**注意这个转折**：线程调用 `wait()` 之后，栈上没有返回，
而是**往下钻进了 `function_task<Task>::execute`**。

含义只有一个：

> **调用 `work_and_wait()` 的那个线程，在等的同时自己接了一个任务在跑。**
> 它此刻既是"等待者"，也是"执行者"。

这正是 [07-01 §5](01-主线程栈与depsgraph求值链路.md) 引用过的那段注释的现场证据：

```cpp
// task_pool.cc · L355-L361
#ifdef WITH_TBB
  if (this->use_threads) {
    /* This is called wait(), but internally it can actually do work. This
     * matters because we don't want recursive usage of task pools to run
     * out of threads and get stuck. */
    this->tbb_group->wait();
  }
#endif
```

### 这张栈的独特价值：它不是"worker 栈"

对比 [07-01](01-主线程栈与depsgraph求值链路.md) 那种"主线程停在 wait、worker 在干活"的双栈结构，
这张栈是**单线程自证**：

| | 07-01 的双栈 | 本文这张栈 |
| --- | --- | --- |
| 谁在等 | 主线程（`wait` 帧在顶部） | 同一个线程（`wait` 在底部） |
| 谁在执行 | 另一个 worker | **同一个线程** |
| 栈形态 | 两条独立栈 | 一条栈里"等待"和"执行"共存 |
| 证明什么 | 调度者与执行者分离 | **`wait()` 会帮忙干活** |

如果只看"主线程停在 `wait`"就推断"主线程没在干活"，这张栈会立刻推翻这个结论。

### 为什么场景是"构建"而不是"求值"

栈顶是 `build_repeat_zone_function`，说明这个任务走的是：

```
build_nodetree → preprocess_geometry_node_tree_for_evaluation → ensure_graph → build()
```

也就是**构建期**（编译惰性函数图），而不是执行期的 `execute_impl`。
这两个阶段在 [07-01 §3](01-主线程栈与depsgraph求值链路.md) 里对应
`scene_graph_update_tagged` 相邻的两行：

```cpp
DEG_graph_relations_update(depsgraph);                    // L2823 ← 构建期发起
...
DEG_evaluate_on_refresh(depsgraph, DEG_EVALUATE_...);     // L2830 ← 执行期发起
```

但注意：这张栈里的 `build_nodetree` 任务本身是**被 depsgraph 求值调度器推入任务池的**
（`evaluate_graph_threaded_stage` → `work_and_wait`），所以它是
"**求值阶段里被调度的一个构建动作**"——两阶段并非完全隔离，
而是"求值调度器也会跑构建任务"。这正是它能出现在同一个任务池里的原因。

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §1 先回答：POD 是什么

**POD = Plain Old Data**——"**布局和行为都像 C 结构体**"的类型。

它的价值一句话：**这种类型可以安全地按字节搬运，而不需要调用任何代码。**

### 判据（C++11 之后）

C++98 的 `POD`（= 聚合 + trivial）在 C++11 被拆成更细的概念：

| 性质 | 含义 | 判据 |
| --- | --- | --- |
| **trivial** | 构造/析构/拷贝/移动都是编译器自动生成的平凡版本 | 没有用户提供的这四类特殊成员函数（`= default` 仍算 trivial） |
| **trivially copyable** | `memcpy` 到另一块内存后仍然有效 | trivial 拷贝/移动 + trivial 析构 |
| **standard layout** | 内存布局与 C 结构体一致 | 无虚函数、无虚基类、非静态成员同访问权限 |
| **aggregate** | 可花括号整体初始化 | 无用户声明构造、无私有成员、无基类 |

> 严格意义的 `POD`（C++98）= trivial **且** standard layout。
> C++20 已弃用 `std::is_pod`，建议分别用 `is_trivially_copyable` + `is_standard_layout`。

### 为什么 Blender 那么在意

| 场景 | 需求 | 只有 POD 能满足 |
| --- | --- | --- |
| DNA 序列化（.blend） | 内存块直接落盘/读回 | ✅ 布局固定、无指针、无 vtable |
| `MEM_mallocN` / `LinearAllocator` | 批量分配、不执行构造 | ✅ 无需构造 |
| `GPointer` / `GMutableSpan` | 只知道"类型 + 地址"，用 `copy_construct` 搬运 | ✅ trivial 拷贝 |
| `MultiFunction` 批量参数 | 一次准备、反复调用 | ✅ 无隐藏状态 |
| GPU 上传 / 顶点缓冲 | 连续布局 | ✅ standard layout |
| RNA / Python 桥接 | 布局可预测、偏移固定 | ✅ 固定偏移 |

### 反例：为什么很多 Blender 类型不是 POD

- `SocketValueVariant`：union + 类型标签，可能持有 `GListPtr`（引用计数），非平凡析构
- `GeometrySet`：持有多个 `GeometryComponent`，需要引用计数
- `Vector` / `Array` / `Map`：堆分配 + 析构

所以 Blender 用 `CPPType` 描述"多大、怎么拷、怎么析构、是否 trivial"。
`CPPType::is_trivial()` 这类查询在热路径上被用来选择
"**批量 memcpy**"还是"**逐个 copy_construct**"。

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §2 纠正：`Task` 不是 POD

我先前口头说过"`Task` 是一个轻量的 POD"，**这个说法不准确**。看源码：

[task_pool.cc · L36-L115](../../../source/blender/blenlib/intern/task_pool.cc#L36)

```cpp
/**
 * Task
 *
 * Unit of work to execute. This is a C++ class to work with TBB.
 */
class Task {
 public:
  TaskPool *pool;
  TaskRunFunction run;
  void *taskdata;
  bool free_taskdata;
  TaskFreeFunction freedata;

  Task(TaskPool *pool, TaskRunFunction run, void *taskdata,
       bool free_taskdata, TaskFreeFunction freedata);   // ① 用户提供的构造

  ~Task()                                                 // ② 用户提供的析构（所有权逻辑）
  {
    if (free_taskdata) {
      if (freedata) { freedata(pool, taskdata); }
      else { MEM_delete_void(taskdata); }
    }
  }

  Task(Task &&other);                                     // ③ 用户提供的移动构造
  Task(const Task &other) = delete;                       // ④ 拷贝被删除
  Task &operator=(const Task &other) = delete;
  Task &operator=(Task &&other) = delete;

  void operator()() const;                                // ⑤ 可调用对象
};
```

对照 §1 判据：

| 判据 | `Task` | 结论 |
| --- | --- | --- |
| 无用户提供的析构 | ❌ 有 `~Task()` 且含副作用 | 不 trivial |
| 无用户提供的拷贝/移动 | ❌ 有移动构造，拷贝 delete | 不 trivial |
| trivially copyable | ❌ | 不能 `memcpy` |
| standard layout | ⚠️ 勉强满足 | 布局类似，但仍有所有权语义 |
| **POD** | ❌ | — |

### 准确的说法

> `Task` 是一个**小尺寸、可移动、不可拷贝的 move-only 值类型**，
> 本质上是"**智能指针 + 调用器**"的组合。

它"轻量"体现在：

| 特征 | 说明 |
| --- | --- |
| 只有 5 个成员 | 64 位上 40 字节（5 个机器字） |
| 无虚函数 | 无 vtable 指针、无虚调用 |
| 无堆分配 | `Task` 本身在栈上或被 move 进 TBB；它**管理**别人分配的内存，但不为自己分配 |
| 裸函数指针 | `run` 是 `void(*)(TaskPool*, void*)`，不是 `std::function` |

```cpp
// BLI_task_c.hh · L65-L66
typedef void (*TaskRunFunction)(TaskPool *__restrict pool, void *taskdata);
typedef void (*TaskFreeFunction)(TaskPool *__restrict pool, void *taskdata);
```

**用裸函数指针而非 `std::function` 是刻意的性能取舍**：
`std::function` 有类型擦除 + 可能堆分配 + 间接调用；
这里"任务类型"信息全部编码在 `run` 指针里，`taskdata` 退化为 `void *`，零额外成本。

> 与 `FunctionRef` 的思路一致：**Blender 在热路径上普遍拒绝 `std::function`**，
> 改用"函数指针 + void* 上下文"或"双指针的 `FunctionRef`"。

### 为什么拷贝必须 `= delete`

因为 `Task` 有**唯一所有权**——析构会释放 `taskdata`：

```cpp
~Task() {
  if (free_taskdata) { ... }   // 析构时释放
}
```

允许拷贝 → 两个副本各析构一次 → **双重释放**。
这与 `std::unique_ptr` 语义完全一致。

### 移动构造里"手工清空"而非"置标志位"

```cpp
Task(Task &&other)
    : pool(other.pool), run(other.run), taskdata(other.taskdata),
      free_taskdata(other.free_taskdata), freedata(other.freedata)
{
  other.pool = nullptr;
  other.run = nullptr;
  other.taskdata = nullptr;
  other.free_taskdata = false;     // ← 关键
  other.freedata = nullptr;
}
```

为什么不加一个 `moved` 布尔？

因为把 `free_taskdata` 直接置 `false`，被移动对象析构时就**走不进释放分支**，
天然安全。少一个字段、少一次分支判断。

**这是 move 语义的标准惯用法**：让被移动对象进入"可安全析构的空状态"，
而不是"记录自己已被移动"。

### 历史包袱：`#if` 里的拷贝构造

```cpp
/* TBB has a check in `tbb/include/task_group.h` where `__TBB_CPP11_RVALUE_REF_PRESENT` should
 * evaluate to true as with the other MSVC build. However, because of the clang compiler
 * it does not and we attempt to call a deleted constructor in the tbb_task_pool_run function.
 * This check fixes this issue and keeps our Task constructor valid. */
#if (defined(WITH_TBB) && TBB_INTERFACE_VERSION_MAJOR < 10) || \
    (defined(_MSC_VER) && defined(__clang__) && TBB_INTERFACE_VERSION_MAJOR < 12)
  Task(const Task &other) : ... { /* 手动模拟 move */ }
#else
  Task(const Task &other) = delete;
#endif
```

**编译环境兼容补丁**：某些 `clang-cl + 旧 TBB` 组合下，TBB 头文件误判
"不支持右值引用"，转而去调拷贝构造——而那时拷贝已被 `delete`，编译报错。
补丁让拷贝构造在特定组合下"看起来是拷贝、实际是 move"（内部清空源对象）。

**值得记住的模式**：当第三方库的能力检测出错，与其改库，
不如"让被误用的接口表现出正确行为"，并加注释说明触发条件。

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §3 `Task::operator()`：栈里那一行的分量

[task_pool.cc · L117-L121](../../../source/blender/blenlib/intern/task_pool.cc#L117)

```cpp
/* Execute task. */
void Task::operator()() const
{
  run(pool, taskdata);
}
```

就一行，但解释了两件事：

1. **为什么 `task_pool.cc:120` 紧接着 `deg_eval.cc:118`**
   —— 中间没有任何逻辑，`run` 就是 `deg_task_run_func` 的函数指针。
2. **为什么是 `const`**
   —— 执行任务不改变 `Task` 自身（它只是"绑定好的调用描述符"），
   真正的可变状态在 `taskdata` 指向的外部对象里。

这叫 **"分离描述符与状态"**：
`Task` 是**不可变的描述**（做什么、用什么数据），
`taskdata` 是**可变的执行状态**（depsgraph 节点等）。

## §4 从 `TaskPool` 到 TBB

### `tbb_task_pool_run`：三个分支

[task_pool.cc · L309-L339](../../../source/blender/blenlib/intern/task_pool.cc#L309)

```cpp
void TaskPool::tbb_task_pool_run(Task &&task)
{
  BLI_assert(ELEM(this->type, TASK_POOL_TBB, TASK_POOL_TBB_SUSPENDED, TASK_POOL_NO_THREADS));
  if (this->is_suspended) {
    /* Suspended task that will be executed in work_and_wait(). */
    this->suspended_tasks.append(std::move(task));      // ① 攒着
    ...
  }
#ifdef WITH_TBB
  else if (this->use_threads) {
    /* Execute in TBB task group. */
    this->tbb_group->run(std::move(task));              // ② 交给 TBB
  }
#endif
  else {
    /* Execute immediately. */
    task();                                             // ③ 当场调用
  }
}
```

| 分支 | 条件 | 行为 |
| --- | --- | --- |
| ① 攒着 | `is_suspended` | 放进 `suspended_tasks`，等 `work_and_wait()` 一次性放行 |
| ② 交给 TBB | `use_threads` | `tbb_group->run(std::move(task))`，**所有权转移给 TBB** |
| ③ 直接执行 | 否则（如 `-t 1`） | 当场 `task()`，走 `operator()` 一行调用 |

**分支 ③ 是排查多线程问题的关键**：`-t 1` 时 `use_threads == false`
（判据见 `task_pool.cc:183`：`BLI_task_scheduler_num_threads() > 1`），
所有任务在**当前线程同步执行**。若 `-t 1` 下问题消失，几乎可确定是数据竞争。

分支 ② 用 `std::move` 转交所有权，意味着 **`~Task()` 可能在任意线程上执行**——
所以 `freedata` 回调必须线程安全。

### 跨库调用链

```dml-ignore
TaskPool::task_push                     task_pool.cc:254
  └─ tbb_task_pool_run                  task_pool.cc:309
       └─ tbb_group->run(std::move)      task_pool.cc:332
            └─ function_task<Task>::execute   tbb/task_group.h:101
                 └─ Task::operator()           task_pool.cc:120   ← 跨回 Blender
                      └─ deg_task_run_func      deg_eval.cc:118
```

**注意方向**：Blender 调 TBB，TBB 在任意线程上调回 Blender。
这就是栈里 `tbb12_debug.dll` 裸地址帧夹在中间的原因——那里是 TBB 调度器，没有 PDB 符号。

### 本文这张栈里的"自调用"

普通情况下，`tbb_group->run` 之后由**别的线程**来执行。
但本文这张栈不同：

```
tbb_group->wait()  →  tbb::detail::d1::wait  →  tbb12_debug  →  function_task<Task>::execute
```

**`wait()` 自己在执行任务。** TBB 的 `wait` 实现是
"**循环检查 `wait_context` 引用计数，同时从 arena 里取任务执行**"。
计数归零才返回。所以等待者永远在推进工作，避免"所有线程都在等、队列里还有活"的死锁。

这就完整解释了栈里那个看似矛盾的组合：

```dml-ignore
线程 X:
  work_and_wait()          ← 我要等所有任务完成
    wait()                 ← 等，但同时接活
      [执行任务 A]          ← X 自己变成了 worker
        build_nodetree     ← 任务 A 的内容就是"构建节点树"
          ensure_graph     ← 构建几何节点惰性函数图
            build()        ← 编译所有区域
```

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §5 栈的中段：`CacheMutex` 与 `isolate`

栈中段（`preprocess` → `ensure_graph` → `CacheMutex` → `isolate` → `lambda_1`）
是几何节点图的**缓存加锁构建**：

```
preprocess_geometry_node_tree_for_evaluation   node_runtime.cc:32
└─ ensure_geometry_nodes_lazy_function_graph    geometry_nodes_lazy_function.cc:4337
   └─ CacheMutex::ensure                        BLI_cache_mutex.hh:91
      └─ CacheMutex::ensure_impl                cache_mutex.cc:28
         └─ threading::isolate_task             BLI_task.hh:228
            └─ tbb::detail::d1::isolate         task_arena.h:595
               └─ isolate_impl                  task_arena.h:258
                  └─ task_arena_function::operator()   task_arena.h:72
                     └─ tbb12_debug.dll
                        └─ FunctionRef::operator()        BLI_function_ref.hh:150
                           └─ FunctionRef::callback_fn    BLI_function_ref.hh:94
                              └─ lambda_1::operator()     :4338
                                 └─ ensure_..._impl       :4331
```

### `CacheMutex::ensure`：双检锁

[cache_mutex.cc · L14](../../../source/blender/blenlib/intern/cache_mutex.cc#L14)

```cpp
void CacheMutex::ensure_impl(const FunctionRef<void()> compute_cache)
{
  if (cache_valid_.load(std::memory_order_acquire)) {
    return;                                        // ① 无锁快路径
  }
  std::scoped_lock lock{mutex_};                   // ② 慢路径加锁
  /* Double checked lock. */
  if (cache_valid_.load(std::memory_order_relaxed)) {
    return;                                        // ③ 二次检查
  }
  /* Use task isolation because a mutex is locked and the cache computation might use
   * multi-threading. */
  threading::isolate_task(compute_cache);          // ④ ★ 隔离执行
  cache_valid_.store(true, std::memory_order_release);
}
```

| 步 | 用途 | 内存序理由 |
| --- | --- | --- |
| ① | 绝大多数调用走这里，无锁 | `acquire`：读到 `true` 时能看见之前写的缓存数据 |
| ② | 竞争时串行化 | — |
| ③ | 等锁期间别人可能已建好 | `relaxed`：mutex 自身的 acquire/release 已保证顺序 |
| ④ | 持锁期间执行可能多线程的代码 | 见下 |

### 为什么持锁时必须 `isolate`

注释一句话点破：*"because a mutex is locked and the cache computation might use multi-threading."*

问题就在于 §4 结论：**`wait()` 会帮忙干活**。若当前线程已持锁，
又被调度去执行**另一个也在等这把锁**的任务：

```dml-ignore
线程 A: 持有 mutex_ → 构建缓存 → TBB/调度器让它去执行任务 X
线程 B: 正在任务 X 的前置里等 mutex_
结果:   A 等 B 放锁，B 等 A 干活 → 死锁
```

**`isolate` 就是禁止当前线程"帮忙"**：

```cpp
// BLI_task.hh · L223-L232
template<typename Function> inline auto isolate_task(const Function &function)
{
#ifdef WITH_TBB
  lazy_threading::ReceiverIsolation isolation;
  return tbb::this_task_arena::isolate(function);
#else
  return function();
#endif
}
```

**两个动作缺一不可。** 栈里 `isolate_impl` → `task_arena_function::operator()` → 回调，
就是 `tbb::this_task_arena::isolate` 的执行路径。

### `ReceiverIsolation`：为什么光有 TBB 的 isolate 不够

`lazy_threading` 是 Blender 自己的一层"按需开线程"机制，
设计目标写在 [BLI_lazy_threading.hh · L8-L58](../../../source/blender/blenlib/BLI_lazy_threading.hh#L8)。
核心一段：

> *"By default, all work stays on a single thread. If an individual task notices that it is about
> to start a computation that will take a while, it notifies the task scheduler further up on the
> stack. The scheduler then allows other threads to take over other tasks that were originally
> meant for the current thread."*

三句话概括：

| 步骤 | 机制 |
| --- | --- |
| 默认 | 所有工作单线程跑，**零线程通信开销**，缓存友好 |
| 长任务出现 | 该任务调用 `lazy_threading::send_hint()` 主动上报 |
| 调度器响应 | `HintReceiver` 收到通知，把"本该当前线程做的其他任务"挪走 |

**为什么需要它**：`parallel_for` 用 grain size 控制并行度，但那只在**任务均匀**时有效。
几何节点/重复区域的任务量完全不可预测（一次 repeat 可能 1 轮也可能 10 万轮），
单一 grain size 无法判断。所以改成**由任务自己上报**。

这就是 [04-01](../04-运行时机制/01-RepeatEvalStorage与一次求值.md) 里那段代码的来由：

```cpp
// geometry_nodes_repeat_zone.cc · L210
if (iterations >= 10) {
  /* Constructing and running the repeat zone has some overhead so that it's probably worth
   * trying to do something else in the meantime already. */
  lazy_threading::send_hint();
}
```

**重复区域在 N ≥ 10 时主动上报**——这是它与 lazy_threading 的接口点。

接收端在 `GraphExecutor`：

```cpp
// lazy_function_graph_executor_generic.hh · L1480-L1490
auto blocking_hint_fn = [&]() {
  if (!current_task.has_scheduled_nodes.load()) { return; }
  if (!this->try_enable_multi_threading()) { return; }
  this->push_all_scheduled_nodes_to_task_pool(current_task);
};

lazy_threading::HintReceiver blocking_hint_receiver{blocking_hint_fn};
```

`send_hint()` 在**当前线程**上向上查找 `HintReceiver`，找到就回调。

**`ReceiverIsolation` 的作用**：阻止 hint 穿透隔离区。
否则隔离区外的执行器会以为"当前线程很闲、可以接活"，
又回到 §5 开头那个死锁场景。注释（L85-89）：

> *"Used to make sure that lazy-threading hints don't propagate through task isolation. This is
> necessary to avoid deadlocks when isolated regions are used together with e.g. task pools."*

所以 `isolate_task` 是**两件事的组合**：

| 组件 | 阻止什么 |
| --- | --- |
| `tbb::this_task_arena::isolate` | 阻止 TBB **主动**把任务塞给当前线程 |
| `lazy_threading::ReceiverIsolation` | 阻止 hint 穿透，从而阻止当前线程**主动请求**接活 |

只做前者，仍可能因 hint 而被动接活。

### `FunctionRef`：栈里那两层

```
FunctionRef::operator()             BLI_function_ref.hh:150
└─ FunctionRef::callback_fn<lambda_1>   BLI_function_ref.hh:94
```

`FunctionRef<void()>` 是**非拥有、无分配的可调用引用**：

| 特性 | `std::function` | `FunctionRef` |
| --- | --- | --- |
| 所有权 | 拥有可调用对象 | **不拥有**，仅调用期间有效 |
| 内存分配 | 超过 SBO 会堆分配 | **零分配** |
| 大小 | 通常 32 字节 | 两个指针 |
| 生命周期 | 自包含 | **被引用对象必须活得比它久** |

实现是"**对象指针 + 函数指针**"，`callback_fn` 负责把 `void *` 转回 lambda 再调用。
栈里这两层的存在，就是类型擦除的代价——**只有两次间接调用，没有分配**。

**约定**：不能捕获临时对象、不能长期持有。
`HintReceiver` 的注释专门强调过：

> *"The function has to stay alive after the call to the constructor. So one must not pass a lambda
> directly into this constructor but store it in a separate variable on the stack first."*

这就是 `blocking_hint_fn` 先声明为具名变量、再传给 `HintReceiver` 的原因。

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §6 全链路对照表

| # | 帧 | 文件:行 | 这一层解决什么 | 阶段 |
| --- | --- | --- | --- | --- |
| 1 | `BLI_task_pool_work_and_wait` | task_pool.cc:457 | C 接口 → C++ 方法 | 调度 |
| 2 | `work_and_wait` | task_pool.cc:281 | 按池类型分发 | 调度 |
| 3 | `tbb_task_pool_work_and_wait` | task_pool.cc:360 | **wait 时也干活** | 调度 |
| 4 | `tbb::wait` | tbb/_task.h:243 | 检查计数 + 取任务执行 | TBB |
| 5 | `function_task<Task>::execute` | tbb/task_group.h:101 | TBB 可调用对象适配 | TBB |
| 6 | `task_ptr_or_nullptr` | tbb/task_group.h:167 | 取可执行指针 | TBB |
| 7 | `Task::operator()` | task_pool.cc:120 | 一次函数指针调用 | 桥接 |
| 8 | `deg_task_run_func` | deg_eval.cc:118 | 求值一个 depsgraph 节点 | 执行 |
| 9 | `evaluate_node` | deg_eval.cc:101 | 按 `OperationNode` 类型分发 | 执行 |
| 10 | `build_nodetree` lambda | deg_builder_nodes.cc:2066 | 构建节点树运行时数据 | 执行 |
| 11 | `preprocess_..._for_evaluation` | node_runtime.cc:32 | 标脏旧图 + 强制重建 | 构建 |
| 12 | `ensure_..._graph` | geometry_nodes_lazy_function.cc:4337 | 幂等缓存入口 | 构建 |
| 13 | `CacheMutex::ensure` | BLI_cache_mutex.hh:91 | 双检锁 | 构建 |
| 14 | `ensure_impl` | cache_mutex.cc:28 | 隔离执行构建 | 构建 |
| 15 | `isolate_task` | BLI_task.hh:228 | 隔离 + 屏蔽 hint | 构建 |
| 16 | `tbb::isolate` / `isolate_impl` | task_arena.h:595/258 | 禁止线程帮忙 | TBB |
| 17 | `task_arena_function::operator()` | task_arena.h:72 | 隔离区适配 | TBB |
| 18 | `ReceiverIsolation`（构造/析构） | BLI_lazy_threading.hh:90 | 阻止 hint 穿透 | 构建 |
| 19 | `FunctionRef::operator()` / `callback_fn` | BLI_function_ref.hh:150/94 | 零分配调用回调 | 桥接 |
| 20 | `lambda_1::operator()` | geometry_nodes_lazy_function.cc:4338 | 调用 impl | 构建 |
| 21 | `ensure_..._impl` | geometry_nodes_lazy_function.cc:4331 | 拷贝树、建 builder | 构建 |
| 22 | `build()` | geometry_nodes_lazy_function.cc:2045 | 初始化映射数组 | 构建 |
| 23 | `build_zone_functions()` | geometry_nodes_lazy_function.cc:2079 | 按 depth 遍历区域 | 构建 |
| 24 | `build_repeat_zone_function()` | geometry_nodes_lazy_function.cc:2245 | 编译这个重复区域 | 构建 |

**栈里出现了两次"跨越"**：

1. `Task::operator()`（#7）：TBB → Blender
2. `FunctionRef::callback_fn`（#19）：类型擦除 → 具体 lambda

两次跨越都只用"函数指针 + void*"，这正是 Blender 热路径的通用手法。

## §7 涉及的类速览

| 类 / 类型 | 位置 | 是不是 POD | 职责 |
| --- | --- | --- | --- |
| `Task` | task_pool.cc:41 | ❌ move-only 值类型 | 5 字段任务描述符 + 所有权 |
| `TaskPool` | task_pool.cc:161 | ❌ | 五种池类型、TBB group、后台线程 |
| `TBBTaskGroup` | task_pool.cc:128 | ❌ | `tbb::task_group` 子类，仅为设优先级 |
| `FunctionRef` | BLI_function_ref.hh | ❌（2 指针视图） | 非拥有、零分配可调用引用 |
| `ReceiverIsolation` | BLI_lazy_threading.hh:90 | ❌（RAII 守卫） | 屏蔽 hint 穿透隔离区 |
| `HintReceiver` | BLI_lazy_threading.hh:74 | ❌（RAII 守卫） | 接收 hint 并回调调度器 |
| `CacheMutex` | BLI_cache_mutex.hh | ❌ | 双检锁 + 隔离构建 |
| `TaskRunFunction` | BLI_task_c.hh:65 | ✅ 函数指针 | `void(*)(TaskPool*, void*)` |
| `float3` / `int2` | BLI math | ✅ POD | 向量数学 |
| `CustomData_MeshMasks` | DNA | ✅ 位掩码 POD | 网格属性层需求 |

## §8 关键设计点汇总

1. **`wait()` 会干活不是实现细节，是防死锁的结构性保证**。本文这张栈是它的现场证据：
   等待线程自己钻进了 `function_task<Task>::execute` 开始执行任务。
   任何"主线程在 wait 所以没在干活"的推断都是错的。
2. **POD 的价值是"可按字节搬运"**。`Task` 不是 POD——它有非平凡析构（所有权语义）。
   准确说法是"小尺寸 move-only 值类型"。
3. **`Task` 用裸函数指针而非 `std::function`**：省掉类型擦除与可能的堆分配。
   任务类型编码在 `run` 里，`taskdata` 退化为 `void*`。
4. **move 构造手工清空字段，而不是加 `moved` 标志**：让源对象直接进入可安全析构状态。
5. **`CacheMutex` 三层结构**：无锁快路径 → 加锁 → 二次检查，再包一层 `isolate`。
   内存序 `acquire` / `relaxed` / `release` 各有依据。
6. **`isolate` 必须是两组件组合**：TBB 层阻止被动接活，`ReceiverIsolation` 阻止主动请求。
   只做一半仍会死锁。
7. **`lazy_threading` 的核心思想**："默认单线程，长任务自己上报"。
   它解决了任务量不可预测时 grain size 无法确定的问题——
   重复区域的 `iterations >= 10` 提示就是这条链的入口。
8. **`FunctionRef` 是"零分配但有生命周期约束"的取舍**：换来热路径无堆分配，
   代价是必须保证被引用对象活得更久。

## 附录：源码索引

| 符号 | 文件 | 行 |
| --- | --- | --- |
| `Task` 类定义 | blenlib/intern/task_pool.cc | 41 |
| `~Task` 所有权释放 | blenlib/intern/task_pool.cc | 58 |
| 移动构造 | blenlib/intern/task_pool.cc | 74 |
| clang-cl 兼容拷贝构造 | blenlib/intern/task_pool.cc | 92 |
| `Task::operator()` | blenlib/intern/task_pool.cc | 118 |
| `tbb_task_pool_run` 三分支 | blenlib/intern/task_pool.cc | 309 |
| "wait 也会干活" 注释 | blenlib/intern/task_pool.cc | 355-361 |
| `TaskRunFunction` typedef | blenlib/BLI_task_c.hh | 65 |
| `isolate_task` | blenlib/BLI_task.hh | 224 |
| `CacheMutex::ensure_impl` | blenlib/intern/cache_mutex.cc | 14 |
| `CacheMutex::ensure` | blenlib/BLI_cache_mutex.hh | 91 |
| `lazy_threading` 设计注释 | blenlib/BLI_lazy_threading.hh | 8-58 |
| `send_hint` | blenlib/BLI_lazy_threading.hh | 68 |
| `HintReceiver` | blenlib/BLI_lazy_threading.hh | 74 |
| `ReceiverIsolation` | blenlib/BLI_lazy_threading.hh | 90 |
| 重复区域线程提示 | nodes/intern/geometry_nodes_repeat_zone.cc | 210 |
| `HintReceiver` 使用点 | functions/intern/lazy_function_graph_executor_generic.hh | 1490 |
| `FunctionRef` 调用 | blenlib/BLI_function_ref.hh | 94 / 150 |
| 构建期 / 执行期分界 | blenkernel/intern/scene.cc | 2823 / 2830 |

## 附录二：三分钟自测

1. 本文这张栈为什么能同时"在等"和"在干活"？是哪一层让它成立的？
2. `Task` 为什么不是 POD？至少说出两条判据不满足。
3. `Task` 的拷贝构造为什么必须 `= delete`？如果允许拷贝会发生什么？
4. 移动构造里把 `free_taskdata` 置 `false`（而非加 `moved` 标志）的好处是什么？
5. `Task` 的析构可能在哪条线程上执行？由此对 `freedata` 有何要求？
6. 为什么 `CacheMutex::ensure_impl` 在持锁时必须调用 `isolate_task`？
7. 只调 `tbb::this_task_arena::isolate`、不加 `ReceiverIsolation`，会出什么问题？
8. `FunctionRef` 相比 `std::function` 省掉了什么？代价是什么？
9. 重复区域为什么要主动 `send_hint()`，而不是靠 `parallel_for` 的 grain size？
10. `POD` 在 C++11 之后被拆成哪几个概念？为什么 `std::is_pod` 被弃用？

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;margin:38px 0 4px;padding:13px 16px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;display:flex;flex-wrap:wrap;align-items:center;gap:8px">
<span style="font-size:11px;font-weight:700;letter-spacing:.1em;color:#64748B;margin-right:2px">继续阅读</span>
<a href="../README.md" style="font-size:13px;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">总入口</a>
<a href="./01-主线程栈与depsgraph求值链路.md" style="font-size:13px;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">‹ 主线程栈与depsgraph求值链路</a>
<span style="font-size:13px;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">回到顶部</span>
</div>
