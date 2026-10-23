# 02 · ResourceScope 资源作用域

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](01-LinearAllocator线性分配.md) · [下一篇](03-destruct_ptr与所有权.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `ResourceScope`——"按登记顺序、反向析构"的资源容器。Repeat 的 `LazyFunctionForRepeatZone` 就由它持有。主要源码：[`BLI_resource_scope.hh`](../../../source/blender/blenlib/BLI_resource_scope.hh)（243 行）。

## 先回答一个具体问题

我有一堆不同类型的对象，它们要在同一时刻销毁，而且析构顺序有讲究（后建的依赖先建的）。用普通容器怎么管？

难点在三处：

1. **类型不同**：`Vector<T>` 只能装一种；`unique_ptr<Base>` 要求有共同基类。
2. **顺序有讲究**：必须逆序析构，像 C++ 的栈帧。
3. **可选所有权**：有些对象归我管，有些不归——用 `optional<unique_ptr>` 会很啰嗦。

`ResourceScope` 同时解决这三个问题。

## 文件头注释揭示的设计意图

注释（L17-L36）值得逐句读：

> "A `ResourceScope` takes ownership of arbitrary data/resources. Those resources will be destructed and/or freed when the `ResourceScope` is destructed. **Destruction happens in reverse order.** That allows resources to depend on other resources that have been added before."

`[讲解]` 核心承诺有两个：

1. **任意类型**：不要求共同基类，靠 `void* + 函数指针` 做类型擦除。
2. **反向序析构**：后加的可以先死，依赖关系自然成立。

### 类比：运行期的花括号

> "A `ResourceScope` can also be thought of as a dynamic/runtime version of normal scopes in C++ that are surrounded by braces."

`[讲解]` 这个类比极妙。C++ 的栈对象：

```cpp
{
  Foo a;
  Bar b;   // b 依赖 a
}          // b 先析构，a 后析构
```

`ResourceScope` 让你在**运行期**动态地"打开一个花括号"，往里塞对象，然后统一关闭。这对于"构建期产物数量取决于运行时输入"的场景（比如 Repeat 展开几个 body 节点）至关重要。

### 核心用途：向调用方的作用域注入数据

> "The main purpose of a `ResourceScope` is to allow functions to inject data into the scope of the caller. Traditionally, that can only be done by returning a value that owns everything it needs. This is fine until one has to deal with optional ownership."

`[讲解]` 这是最有洞察力的一段。对比两种 API 风格：

| 风格 | 签名 | 问题 |
| --- | --- | --- |
| 返回值拥有 | `Result build(...)` | 可选所有权难表达（`optional<unique_ptr>`） |
| 注入作用域 | `Result& build(ResourceScope&, ...)` | 想要就 add，不想要就不 add |

**Repeat 正篇的例子**：`build_repeat_zone_lazy_function(ResourceScope &scope, ...)` 返回 `LazyFunction&`。函数内部把所有中间对象（图、索引、wrapper）都 `scope.construct(...)`，调用方只需要知道"这些东西活得和 scope 一样久"。

如果改成返回值拥有，就得造一个巨型结构体装所有中间产物，且部分可选的情况很难处理。

### 生命周期的一个微妙之处

> "When a function takes a `ResourceScope` as parameter, it usually means that its return value will live at least as long as the passed in resources scope. However, it might also live longer."

`[讲解]` "might also live longer" —— 返回值可能比 scope 活得久（比如返回静态数据或条件性动态数据）。所以**不能假设"scope 死了返回值就死了"**，只能反过来假设"返回值至少活到 scope 死"。

## 内部结构

```cpp
class ResourceScope : NonMovable {
 private:
  struct ResourceData {
    void *data;
    void (*free)(void *data);
  };
  using ResourceDataList = linear_allocator::ChunkedList<ResourceData, 4>;

  /** This stores all resources. They are later freed in the reverse order of construction. */
  ResourceDataList resources_;
  LinearAllocator<> &allocator_;
  ...
};
```

`[讲解]` 三个要点：

### 1. 类型擦除的三元组

`ResourceData` 只有两个字段：数据指针 + 释放函数指针。这就是**全部**的类型信息。

对比：如果是 `vtables` 方案，每个对象多一个虚表指针；这里每个对象多一点 16 字节的 `ResourceData`。对于"对象数不多、但类型杂"的场景，这个方案更省。

### 2. `ChunkedList<ResourceData, 4>`

注意模板参数 `4`：每个 chunk 装 4 个 `ResourceData`（64 字节）。

`[讲解]` 为什么用 `ChunkedList` 而不是 `Vector`？

- `Vector` 扩容时会**移动**已有元素。虽然 `ResourceData` 是 trivial 的（移动安全），但 `ChunkedList` 保证**地址稳定**——对于某些需要稳定地址的场景更安全。
- 更重要的是：`ChunkedList` 的节点从 `allocator_` 分配，与资源本身用同一个分配器，符合"整块回收"的语义。

### 3. `NonMovable`

`[讲解]` `ResourceScope` 不可移动。为什么？

因为它内部的 `resources_` 存的是"指向自己的分配器的指针"（`add(ptr, free)` 时把 `ResourceData` 追加到 `resources_`，而 `resources_` 的 chunk 来自 `allocator_`）。移动会导致自引用失效。

底部的 `static_assert(sizeof(ResourceScope) == 16)`（L144）也说明它刻意保持极小：`ResourceDataList`（8 字节指针？）+ `LinearAllocator&`（8 字节）= 16 字节。

## 构造函数家族

`[讲解]` 五种构造，对应不同的内存来源：

| 构造 | 内存来源 | 用途 |
| --- | --- | --- |
| `ResourceScope(initial_size = 32)` | 自建 allocator | 独立使用 |
| `ResourceScope(AlignedBuffer<Size, Alignment>&)` | 调用方的栈缓冲区 | 避免堆分配 |
| `ResourceScope(void *buffer, int64_t size)` | 调用方的裸缓冲区 | 同上 |
| `ResourceScope(LinearAllocator&)` | **调用方的 allocator** | 共享分配器 |

**Repeat 用的是第四种吗？** 不是——`build_repeat_zone_lazy_function` 收到的 `scope` 是上层（`GeometryNodesLazyFunctionGraphBuilder`）创建的，用于承载**整棵 lf 图**的所有构建期对象。Repeat 只是往里加东西。

## 五个 add 重载

`[讲解]` 这是 `ResourceScope` 最实用的部分。逐个看：

### `add(std::unique_ptr<T>)`

```cpp
template<typename T> inline T *ResourceScope::add(std::unique_ptr<T> resource)
{
  T *ptr = resource.release();
  if (ptr == nullptr) {
    return nullptr;
  }
  this->add(ptr, [](void *data) {
    T *typed_data = reinterpret_cast<T *>(data);
    delete typed_data;
  });
  return ptr;
}
```

`[讲解]` 三步：

1. `release()` 放弃所有权，拿到裸指针；
2. 登记一个 `delete` 回调；
3. 返回裸指针给调用方（**不转移**所有权，只是借用）。

注意返回值是 `T*` 而不是 `T&`，且允许 nullptr（当传入的 unique_ptr 为空时）。

### `add(std::shared_ptr<T>)`

```cpp
template<typename T> inline T *ResourceScope::add(std::shared_ptr<T> resource)
{
  ...
  this->add_destruct_call([resource = std::move(resource)]() mutable { resource.reset(); });
  return ptr;
}
```

`[讲解]` 这个更巧妙：把 `shared_ptr` **捕获进一个 lambda**，然后登记"调用 lambda"。

`resource.reset()` 减少引用计数——如果归零就析构。**为什么不用 unique_ptr 的方式？** 因为 `shared_ptr` 的删除器可能不是 `delete`（比如自定义删除器），必须走 `reset()` 才能正确调用。

### `add(destruct_ptr<T>)`

```cpp
template<typename T> inline T *ResourceScope::add(destruct_ptr<T> resource)
{
  T *ptr = resource.release();
  if (ptr == nullptr) {
    return nullptr;
  }
  /* There is no need to keep track of such types. */
  if constexpr (std::is_trivially_destructible_v<T>) {
    return ptr;
  }

  this->add(ptr, [](void *data) {
    T *typed_data = reinterpret_cast<T *>(data);
    typed_data->~T();
  });
  return ptr;
}
```

`[讲解]` 两个关键点：

1. **trivial 类型直接返回**：`if constexpr (std::is_trivially_destructible_v<T>)` 时**不登记**——因为析构什么都不做，登记纯属浪费。
2. **非 trivial 只调析构**：`typed_data->~T()`，**不释放内存**（内存归 allocator）。

这正是 `destruct_ptr` 的语义（下一篇详讲）。

### `add(void *userdata, void (*free)(void *))`

最底层的重载，其他三个都转发到它。

### `add_value(T &&value)`

```cpp
template<typename T> inline T &ResourceScope::add_value(T &&value)
{
  return this->construct<T>(std::forward<T>(value));
}
```

`[讲解]` 把**已有值**复制进 scope。用途：想延长一个局部变量的寿命。

## 两个"延迟调用"工具

### `add_destruct_call(Func)`

```cpp
template<typename Func> inline void ResourceScope::add_destruct_call(Func func)
{
  void *buffer = allocator_.allocate(sizeof(Func), alignof(Func));
  new (buffer) Func(std::move(func));
  this->add(buffer, [](void *data) { (*static_cast<Func *>(data))(); });
}
```

`[讲解]` 把任意可调用对象放进 scope，销毁时调用它。这是 `add(shared_ptr)` 的实现基础。

### `construct<T>(Args...)`

```cpp
template<typename T, typename... Args> inline T &ResourceScope::construct(Args &&...args)
{
  destruct_ptr<T> value_ptr = allocator_.construct<T>(std::forward<Args>(args)...);
  T &value_ref = *value_ptr;
  this->add(std::move(value_ptr));
  return value_ref;
}
```

`[讲解]` 这是**最常用的接口**。三步：

1. 用 `allocator_.construct<T>` 分配并构造（返回 `destruct_ptr`）；
2. 解引用拿引用；
3. 把 `destruct_ptr` 移进 scope（登记析构）。

返回值是 `T&`（不是指针）——所以调用方可以像用普通对象一样用它。

**Repeat 的用法**：

```cpp
return scope.construct<LazyFunctionForRepeatZone>(btree, zone, zone_info, body_fn);
```

一行：在 scope 上构造 `LazyFunctionForRepeatZone`，返回 `LazyFunction&`（向上转型）。这个函数对象将在 scope 销毁时被析构——而 scope 活得和整棵 lf 图一样久。

## 析构：反向序

`[讲解]` 注释明确说 "Destruction happens in reverse order"。实现上，析构函数大概做的是：

```cpp
ResourceScope::~ResourceScope()
{
  /* 逆序遍历 resources_，逐个调用 free */
  for (int64_t i = resources_.size() - 1; i >= 0; i--) {
    const ResourceData &data = resources_[i];
    data.free(data.data);
  }
}
```

`[讲解]` 为什么必须反向？

因为"后加的资源可能依赖先加的"。例如：

```cpp
Foo &a = scope.construct<Foo>();     // 先建
Bar &b = scope.construct<Bar>(a);    // 后建，持有 &a
```

析构时必须**先 b 后 a**，否则 `b` 的析构函数访问了已销毁的 `a`。

这正是 C++ 栈帧的语义：局部变量按声明逆序销毁。

## `allocate_owned`：给 CPPType 用

```cpp
inline void *ResourceScope::allocate_owned(const CPPType &type)
{
  void *buffer = allocator_.allocate(type);
  if (!type.is_trivially_destructible) {
    this->add_destruct_call([&type, buffer]() { type.destruct(buffer); });
  }
  return buffer;
}
```

`[讲解]` 当类型信息是**运行时**的（`CPPType`）而不是编译期的（模板参数）时用这个。

注意 lambda 捕获 `&type` —— 这是危险的（如果 `type` 比 scope 短命就悬空），但实际中 `CPPType` 都是静态单例，所以安全。

## 与 LinearAllocator 的分工

`[讲解]` 一张表说清：

| | LinearAllocator | ResourceScope |
| --- | --- | --- |
| 管什么 | 内存 | 对象析构 |
| 释放方式 | 整块 chunk 回收 | 逐个调 free 回调 |
| 知道类型吗 | 不知道 | 不知道（靠函数指针擦除） |
| 顺序 | 无 | 反向 |
| 能做可选所有权吗 | 不能 | 能 |

**关键**：`ResourceScope` 内部**用**一个 `LinearAllocator`。两者搭配使用：allocator 管"内存从哪来"，scope 管"对象何时析构"。

## 在 Repeat 中的位置

`[讲解]` Repeat 有两个生命周期层次，`ResourceScope` 管其中一层：

| 层 | 容器 | 生命周期 | 装什么 |
| --- | --- | --- | --- |
| 构建期 | `ResourceScope` | 整棵 lf 图（跨多次求值） | `LazyFunctionForRepeatZone`、`lf::Graph`、`ZoneBodyFunction` |
| 执行期 | `RepeatEvalStorage` + `LinearAllocator` | 一次调用 | 展开图、executor、索引映射 |

正篇 00-03 有一句准确的话："`ResourceScope` 保证所有构建期对象（图、函数、索引）的生命周期覆盖整个惰性函数图的使用期，统一析构。"

而 04-01 讲的是另一层：`RepeatEvalStorage` 每次求值新建。

**两层不能混**：如果把 `LazyFunctionForRepeatZone` 放进 storage，每次求值都会重新构造一个（浪费），而且它持有的树引用可能失效。

## 用小数据走一遍

```cpp
ResourceScope scope;
Foo &a = scope.construct<Foo>();        // a 依赖无
Bar &b = scope.construct<Bar>(a);       // b 依赖 a
Baz &c = scope.construct<Baz>(b);       // c 依赖 b
// scope 销毁
```

析构顺序：

| 步 | 调用 | 说明 |
| --- | --- | --- |
| 1 | `Baz::~Baz()` | 最后构造，最先析构 |
| 2 | `Bar::~Bar()` | 此时 Foo 还活着 |
| 3 | `Foo::~Foo()` | 最后析构 |

如果顺序反了（Foo 先死），`Bar::~Bar()` 就访问已销毁对象——未定义行为。

## 反例与边界

### 反例 1：以为 ResourceScope 会自动调整顺序

它**只保证反向序**，不分析依赖关系。如果你以错误顺序 add（先 add 依赖方，后 add 被依赖方），析构就会出错。

### 反例 2：在 scope 销毁后使用其中的对象

```cpp
Foo *p;
{
  ResourceScope scope;
  p = &scope.construct<Foo>();
}
p->doSomething();   // 悬空！
```

### 反例 3：把栈对象 add 进去

`add(destruct_ptr<T>)` 要求指针来自 allocator。如果传入栈地址，析构时会调 `~T()` 但内存仍在栈上——如果栈已经回退，就是非法析构。

### 反例 4：以为 add 会拷贝

```cpp
std::unique_ptr<Foo> p = ...;
Foo *q = scope.add(std::move(p));   // p 变空
```

`add` **接管**所有权，不是拷贝。想看拷贝用 `add_value`。

### 反例 5：以为回归值一定会活到 scope 结束

注释说 "However, it might also live longer" —— 但反过来**不成立**：返回值可能比 scope 短命（如果它是另一个对象的成员）。

### 反例 6：移动 ResourceScope

它继承 `NonMovable`，编译期就挡住了。

## 对理解 Repeat 的帮助

| 本篇概念 | Repeat 中的落点 |
| --- | --- |
| `scope.construct<T>` | 构造 `LazyFunctionForRepeatZone` |
| 反向序析构 | 图先于函数析构？还是函数先于图？（后者，因为图在函数之后构造） |
| 类型擦除 | 往一个 scope 里混装 `lf::Graph`、`ZoneBodyFunction`、各类 `LazyFunction` |
| 可选所有权 | zone 有无 reference set 就 add 不 add 对应对象 |
| NonMovable | 整个 lf 图 builder 持有它，不能被搬走 |

**最关键的一条**：理解了 `ResourceScope`，就能理解为什么正篇 03-03 里 `initialize_execution_graph` 里的图（`eval_storage.graph`）放在 **storage** 里，而 `LazyFunctionForRepeatZone` 放在 **scope** 里。前者每次求值重建（因为大小依赖迭代数），后者跨求值复用（因为它的接口是静态的）。

## 继续阅读

- [03-destruct_ptr与所有权](03-destruct_ptr与所有权.md)
- [01-LinearAllocator线性分配](01-LinearAllocator线性分配.md)
- [04-storage生命周期对照](04-storage生命周期对照.md)
- 正篇：[03-03 执行图按迭代展开](../../重复区域-dsh/03-几何节点执行架构/03-执行图按迭代展开.md)
