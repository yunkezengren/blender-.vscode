# 01 · Context 存储与 UserData

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:16px 0 20px;padding:10px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px">
<span style="font-size:11px;font-weight:700;letter-spacing:.1em;color:#64748B;margin-right:2px">导航</span>
<a href="../README.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0">前置知识总入口</a>
<a href="./README.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE">本章 02-参数转发与上下文</a>
<a href="./03-RemappedParams参数重映射.md" style="font-size:13px;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap;color:#7C3AED;background:#F5F3FF;border:1px solid #DDD6FE">03-RemappedParams参数重映射 ›</a>
</div>

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;margin:18px 0 22px;padding:14px 18px;background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:10px">

基准：Blender `5.4.0-alpha`，本地工作树。本篇讲惰性函数执行时携带的第二个参数：`Context`。主要源码：[`FN_lazy_function.hh`](../../../source/blender/functions/FN_lazy_function.hh) L80-L103（`Context` 定义）与 [`FN_user_data.hh`](../../../source/blender/functions/FN_user_data.hh)（34 行全文）。

</div>

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## 先回答一个具体问题

`fn.execute(params, context)` 里的 `params` 和 `context` 到底什么关系？

一句话：**`Params` 管"数据交换"，`Context` 管"环境身份"**。

`[讲解]` 两者分工：

| | `Params` | `Context` |
| --- | --- | --- |
| 装什么 | 输入输出值 | storage、user_data、local_user_data |
| 谁提供 | 执行器按接口生成 | 调用方传入并逐层传递 |
| 生命周期 | 一次 execute 调用 | 整个调用链 |
| Repeat 里的角色 | 见第 03 篇 | per-iteration 上下文注入（正篇 04-02） |

## Context 的三个字段

```cpp
struct Context {
  /**
   * If the lazy-function has some state (which only makes sense when it is executed more than once
   * to finish its job), the state is stored here. This points to memory returned from
   * #LazyFunction::init_storage.
   */
  void *storage;
  /**
   * Custom user data that can be used in the function.
   */
  UserData *user_data;
  /**
   * Custom user data that is local to the thread that executes the lazy-function.
   */
  LocalUserData *local_user_data;

  Context(void *storage, UserData *user_data, LocalUserData *local_user_data)
      : storage(storage), user_data(user_data), local_user_data(local_user_data)
  {
  }
};
```

`[讲解]` 逐个字段：

### `storage`

指向 `init_storage` 返回的内存。这是**本次调用的可变状态**。

注释强调 "which only makes sense when it is executed more than once"：如果函数只执行一次，它不需要 storage（可以返回 nullptr）。

**Repeat 的用法**：`RepeatEvalStorage` 就是这么来的。它装展开图、执行器、索引映射等，全部是"这次求值"的可变状态。

**关键区别**：storage 是 `void*`，具体类型由函数自己知道。`RepeatEvalStorage` 通过 `static_cast<RepeatEvalStorage *>(context.storage)` 取回。

### `user_data`

自定义数据，**跨线程共享**（同名数据被所有线程看到）。

`[讲解]` 为什么不用 `void*` 直接传？

看 `FN_user_data.hh` 的注释：

> "This mainly exists because it's more type safe than passing a `void *` with no type information attached."

所以 `UserData` 是一个空基类——它提供的是**类型标识**，不是数据。子类加自己的字段，接收方用 `static_cast<GeoNodesUserData *>(context.user_data)` 取回。

**Repeat 的用法**：`GeoNodesUserData` 里有 `compute_context` 指针、`call_data`、`verbose_log` 等。wrapper 修改的正是它（拷一份、换 `compute_context` 指针）。

### `local_user_data`

线程本地的 user data。

`[讲解]` 注释（FN_user_data.hh L15-L21）说得很好：

> "Extension of #UserData that is thread-local. This avoids accessing e.g. `EnumerableThreadSpecific.local()` in every nested lazy-function because the thread local data is passed in by the caller."

意思是：本来可以从 `user_data` 里查"当前线程的本地数据"，但那需要每次查一个线程局部容器。改成由调用方**直接传进来**，省掉这层查找。

**Repeat 的用法**：`GeoNodesLocalUserData` 里有日志器、临时分配器等线程相关资源。

## 三个字段的"谁改谁读"

`[讲解]` 理解 `Context` 的关键是搞清"谁能改、谁只读"：

| 字段 | 谁设置 | 谁读取 | 能否在 execute 中改 |
| --- | --- | --- | --- |
| `storage` | 执行器（init_storage） | 函数自己 | 能（内容可变，指针不变） |
| `user_data` | 调用方 | 所有嵌套函数 | **不能改指针**（但内容可变） |
| `local_user_data` | 调用方 | 当前线程的函数 | 不能改指针 |

`[讲解]` 为什么 `user_data` 的指针不能改？

因为它跨线程共享。如果某个函数改了指针，其他线程看到的就变了——竞态。

**那 Repeat 的 wrapper 怎么"换" user_data？** 它没有改原来的，而是：

```cpp
GeoNodesUserData body_user_data = user_data;         // 拷贝一份
body_user_data.compute_context = &body_compute_context;  // 改副本的字段
lf::Context body_context{context.storage, &body_user_data, &body_local_user_data};
```

`[讲解]` 三步：

1. **拷贝一份**（在栈上）；
2. **改副本的字段**（不是改指针）；
3. **构造新的 Context** 用这份副本。

原来的 `user_data` 完全没动。这是"只在当前调用链生效"的正确做法。

## 为什么 storage 是 void*

`[讲解]` 因为 `LazyFunction` 是通用基类，它不知道子类需要什么状态。用 `void*` 让子类自己解释。

**代价**：失去类型安全，需要 `static_cast`。这是 C++ 里常见的"通用接口 + 类型擦除"取舍。

**替代方案**：让 `LazyFunction` 带模板参数（`LazyFunction<StorageT>`）。但那会让基类无法统一使用——执行器要按类型分派，代码爆炸。

Blender 选了 `void*` + 约定。

## UserData 的 get_local 机制

```cpp
class UserData {
 public:
  virtual ~UserData() = default;

  /**
   * Get thread local data for this user-data and the current thread.
   */
  virtual destruct_ptr<LocalUserData> get_local(LinearAllocator<> &allocator);
};
```

`[讲解]` 这个虚函数是"按需创建线程本地数据"的入口：

- 传入一个 `LinearAllocator`（数据生命周期跟随它）；
- 返回 `destruct_ptr<LocalUserData>`（只调析构不释放内存）；
- 具体类型由子类决定。

**为什么用 `destruct_ptr` 而不是 `unique_ptr`？** 因为内存来自 `LinearAllocator`，不由 `LocalUserData` 自己释放。`destruct_ptr` 正好是"只调析构、不管内存"的语义。

**Repeat 的实际路径**：内层执行器在第一次需要时调 `user_data->get_local(allocator)` 创建 `GeoNodesLocalUserData`，之后同一线程复用。

## 三个字段的生命周期

`[讲解]` 这是最容易出错的点。三个字段的生命周期**不同**：

| 字段 | 生命周期 | 谁负责释放 |
| --- | --- | --- |
| `storage` | 一次 execute 调用 | 执行器调 `destruct_storage` |
| `user_data` | 外层调用链 | 调用方 |
| `local_user_data` | 一次 execute 或更长 | 创建者（通常随 allocator） |

**关键推论**：函数不能把 `context.storage` 的指针存到别的地方跨调用使用。也不能把 `local_user_data` 存进 storage（因为它可能比 storage 短命）。

## 嵌套时的 Context 传递

`[讲解]` 正篇 04-01 的三行代码展示了完整传递：

```cpp
lf::Context eval_graph_context{
    eval_storage.graph_executor_storage,   // 新的 storage
    context.user_data,                     // 透传 user_data
    context.local_user_data};              // 透传 local_user_data
```

`[讲解]` 三个决定：

1. **storage 换新**：内层图有自己的状态，用 `graph_executor_storage`；
2. **user_data 透传**：上下文身份要延续（日志才能定位）；
3. **local_user_data 透传**：线程本地数据也要延续。

**为什么 storage 必须换？** 因为内层 `GraphExecutor` 也是一个 `LazyFunction`，它也需要自己的 storage。两层的状态不能混。

## 与 ComputeContext 的区别

`[讲解]` 一个常见的混淆点：`lf::Context` 里的 "Context" 和 `ComputeContext` 不是一回事。

| | `lf::Context` | `ComputeContext` |
| --- | --- | --- |
| 层次 | 惰性函数框架 | 几何节点求值 |
| 作用 | 传递 storage 与 user data | 标识"在哪求值"（树/节点/轮次） |
| 位置 | `FN_lazy_function.hh` | `BLI_compute_context.hh` |
| Repeat 里的关系 | `user_data->compute_context` 指向它 | 被登录在 user_data 里 |

`[讲解]` 关系是：`ComputeContext` **装在** `GeoNodesUserData` 里，而 `GeoNodesUserData` 就是 `lf::Context::user_data`。

所以 wrapper 换上下文 = 换 `user_data` 里那个 `compute_context` 指针。

## 用小数据走一遍

一个 Repeat 区域 2 轮，体里有一个节点：

**第 0 轮**：

```text
外层 Context:
  storage        = RepeatEvalStorage*
  user_data      = GeoNodesUserData*（compute_context 指向修改器上下文）
  local_user_data= GeoNodesLocalUserData*

wrapper 拦截后构造：
  body_user_data = *user_data 的副本
  body_user_data.compute_context = &RepeatZoneComputeContext(iter=0)

内层 Context:
  storage        = graph_executor_storage（不变，仍是一次求值）
  user_data      = &body_user_data（栈上，带 iter=0）
  local_user_data= &body_local_user_data（栈上）
```

**第 1 轮**：同上，但 `iteration = 1`，`body_user_data` 是另一个栈对象。

`[讲解]` 关键观察：

- **storage 不变**：两轮共享同一个 `RepeatEvalStorage`（它属于整次 zone 求值）；
- **user_data 每轮新建**：因为要带不同的 iteration；
- **栈上对象**：`body_user_data` 与 `body_compute_context` 都在栈上，函数返回就失效。

第三点正是正篇反复警告的"栈借用"——如果异步化，这些指针会悬空。

## 反例与边界

### 反例 1：把 storage 指针存进 user_data

```cpp
// 危险
user_data->some_field = context.storage;
```

storage 在一次调用结束时被销毁，之后 `some_field` 悬空。

### 反例 2：在 execute 中改 user_data 指针

```cpp
// 危险
const_cast<Context &>(context).user_data = &my_own_data;
```

指针跨线程共享，改了会影响其他线程。

### 反例 3：把 local_user_data 存进 storage

local_user_data 可能比 storage 短命，或者相反——总之生命周期不对齐。

### 反例 4：以为 Context 可以跨 execute 复用

`Context` 是值传递的小结构体（三个指针）。每次 execute 传新的，不要缓存。

### 反例 5：混淆 lf::Context 与 ComputeContext

两者层次完全不同（见上表）。

## 对理解 Repeat 的帮助

| 本篇概念 | Repeat 中的落点 |
| --- | --- |
| `storage` | `RepeatEvalStorage`（正篇 04-01） |
| `user_data` | `GeoNodesUserData`，wrapper 拷贝后改 compute_context |
| `local_user_data` | `GeoNodesLocalUserData`，装日志器等 |
| 嵌套透传 | 内层 `lf::Context` 换 storage、透传另两个 |
| 栈借用 | wrapper 里的 `body_user_data` 只在同步调用内有效 |

**最关键的一条**：Repeat 的"per-iteration 上下文"就是通过**拷贝 user_data + 换 Context** 实现的，而**不是**通过改 storage。理解这个分工，才能理解为什么 wrapper 的设计是"轻量"的——它只多一个栈上结构体，不动 storage。

## 继续阅读

- [02-BasicParams与参数内存布局](02-BasicParams与参数内存布局.md)
- [03-RemappedParams参数重映射](03-RemappedParams参数重映射.md)
- 正篇：[04-02 ComputeContext 与迭代身份](../../重复区域-dsh/04-运行时机制/02-ComputeContext与迭代身份.md)

