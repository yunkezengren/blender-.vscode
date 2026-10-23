# 02 · BasicParams 与参数内存布局

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](01-Context存储与UserData.md) · [下一篇](03-RemappedParams参数重映射.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `BasicParams`——`Params` 接口最基础的实现，以及惰性函数的参数在内存里到底怎么排。主要源码：[`FN_lazy_function_execute.hh`](../../../source/blender/functions/FN_lazy_function_execute.hh)（158 行）、[`intern/lazy_function_execute.cc`](../../../source/blender/functions/intern/lazy_function_execute.cc)（144 行）。

## 先回答一个具体问题

惰性函数的输入输出值在内存里究竟放在哪、由谁分配、谁释放？

答案分三层。第一，**`BasicParams` 不存值，只存"指向值的指针表"**：它手里是五个 `Span`，每个都指向调用方准备好的一个数组，真正的值内存（`SocketValueVariant`、`GeometrySet`、`int`）在别处。第二，**分配由调用方做**：整个 [`lazy_function_execute.cc`](../../../source/blender/functions/intern/lazy_function_execute.cc) 的 `BasicParams` 段落（L17-L74，58 行）里没出现过一次 `new`、`malloc`、`allocator`。第三，**释放也由调用方做，但依据是 `set_outputs_`**：`BasicParams` 只在 `output_set` 时把 `set_outputs_[index]` 置 `true`，调用方事后遍历这个 bool 数组，对 `true` 的位置调 `GMutablePointer::destruct()`，真实例子见 [`geometry_nodes_execute.cc`](../../../source/blender/nodes/intern/geometry_nodes_execute.cc) L655-L660。

一句话：**`BasicParams` 是"记账本"，不是"仓库"**。它记的是"第 i 个输入现在在哪、第 i 个输出写完了没有、第 i 个输入还要不要"，至于那块内存归谁、多大、什么类型，它一概不管。

## BasicParams 的定位

类定义在 [`FN_lazy_function_execute.hh`](../../../source/blender/functions/FN_lazy_function_execute.hh) L19-L47。开头的注释原文是：

```cpp
/**
 * Most basic implementation of #Params. It does not actually implement any logic for how to
 * retrieve inputs or set outputs. Instead, code using #BasicParams has to implement that.
 */
```

翻译：**`Params` 最基础的实现。它并没有真正实现"如何取输入、如何设输出"的逻辑；相反，使用 `BasicParams` 的代码必须自己实现这些。**

最后一句容易被误读。这里"implement"不是指"再写一个子类重写虚函数"——八个虚函数它全实现了——而是指**调用方必须在外面把内存准备好、把五张表填好、执行完再自己收尾**。`BasicParams` 把这些准备工作抽象成了"给我五个数组"。

把三处实现放在一起对比，定位就清楚了：

| 类 | 文件 | 数据从哪来 | 谁分配值内存 |
| --- | --- | --- | --- |
| `BasicParams` | `FN_lazy_function_execute.hh` L23 | 调用方传进来的五个数组 | 调用方 |
| `RemappedParams` | 同文件 L53 | 另一个 `Params`（`base_params_`）+ 索引映射 | 底座那个实现 |
| `GraphExecutorLFParams` | `lazy_function_graph_executor_generic.hh` L1349 | 图执行器的 `NodeState` | 图执行器（用 `LinearAllocator`） |

`GraphExecutorLFParams` 不在本篇两个主文件里，但它是同族里最"重"的实现：`get_output_data_ptr_impl` 真的调 `allocator.allocate(type)`（L1409-L1411），`output_set_impl` 把值转发给下游节点后把指针置空（L1416-L1428）。跟它一比，`BasicParams` 的"什么都不做"就特别明显。

所以 `BasicParams` 只适合两种场合：**外层边界**（几何节点顶层求值、闭包急切求值），那里本来就是"调用方拥有所有内存"；**测试与工具函数**（`execute_lazy_function_eagerly`）。中间层的节点执行不该用它，那里需要真正的惰性调度。

## 五个成员字段逐个讲

```cpp
class BasicParams : public Params {
 private:
  const Span<GMutablePointer> inputs_;
  const Span<GMutablePointer> outputs_;
  MutableSpan<std::optional<ValueUsage>> input_usages_;
  Span<ValueUsage> output_usages_;
  MutableSpan<bool> set_outputs_;
```

| 字段 | 类型 | 每槽大小（x86-64） | 谁可写 | 语义 |
| --- | --- | --- | --- | --- |
| `inputs_` | `const Span<GMutablePointer>` | 16 字节 | 无人（仅 span 绑定不可改） | 第 i 个输入值在哪，`nullptr` = 未就绪 |
| `outputs_` | `const Span<GMutablePointer>` | 16 字节 | 无人（同上） | 第 i 个输出写哪块内存 |
| `input_usages_` | `MutableSpan<std::optional<ValueUsage>>` | 2 字节 | 惰性函数（经 `Params`） | 第 i 个输入"被要了 / 不要了 / 还不知道" |
| `output_usages_` | `Span<ValueUsage>` | 1 字节 | 只读 | 第 i 个输出"要不要算"，调用方定 |
| `set_outputs_` | `MutableSpan<bool>` | 1 字节 | 惰性函数（经 `Params`） | 第 i 个输出写完没 |

三处命名细节：

1. 前两个是 `const Span<...>`，const 加在 span 对象上，意思是"地址与长度不可改"——不能 `inputs_ = 别的数组`。但槽里的 `data_` 可以被外部改（调用方在两轮执行之间塞新指针）。所以是"绑定不可变，被指内容可变"。
2. `input_usages_` 是 `MutableSpan`，`output_usages_` 是 `Span`。这个不对称是设计意图：**函数可以报告"这个输入我不要了"，但绝不能改"输出要不要算"——那是调用方的决定**。
3. `outputs_` 与 `set_outputs_` 是一对：前者答"写哪"，后者答"写完没"。同一个 index，两张不同的表。

### `GMutablePointer` 到底是什么

定义在 [`BLI_generic_pointer.hh`](../../../source/blender/blenlib/BLI_generic_pointer.hh) L15-L82：

```cpp
/**
 * A generic non-const pointer whose type is only known at runtime.
 */
class GMutablePointer {
 private:
  const CPPType *type_ = nullptr;
  void *data_ = nullptr;

 public:
  GMutablePointer() = default;

  GMutablePointer(const CPPType *type, void *data = nullptr) : type_(type), data_(data)
  {
    /* If there is data, there has to be a type. */
    BLI_assert(data_ == nullptr || type_ != nullptr);
  }
```

两个成员、16 字节、类型擦除的可变指针。`type_` 指向运行期类型描述符 `CPPType`，里面有 `size`、`alignment`、`is_trivial` 以及一组函数指针（`destruct_`、`relocate_assign_` 等，见 [`BLI_cpp_type.hh`](../../../source/blender/blenlib/BLI_cpp_type.hh) L204-L206、L572、L663）；`data_` 是裸地址，那上面是否真的躺着一个已构造对象，它不知道。

构造函数里的断言 "If there is data, there has to be a type" 反过来说明：**允许 `type != nullptr && data == nullptr`**。这个组合就是本篇最重要的状态——"槽有类型，但值还没就绪"。`BasicParams` 判断输入是否就绪用的正是它：`return inputs_[index].get();`（`lazy_function_execute.cc` L32-L35）。返回 `nullptr` 是"未就绪"的唯一信号，没有哨兵值、没有额外的 ready 标志位。

为什么用类型擦除指针而不是 typed 指针？三个理由。

- **接口统一**。`Params` 是基类，`fn.inputs()` 里每个 `Input` 自带 `const CPPType *type`（`FN_lazy_function.hh` L211），运行期才知道第 i 个输入是 `int` 还是 `SocketValueVariant`。基类若存 typed 指针，就得对每种类型生成一套子类，组合爆炸。
- **转发无需知道类型**。`RemappedParams` 把 `void*` 原样往上传（`lazy_function_execute.cc` L95-L103），全程不关心类型。
- **`LinearAllocator` 只给裸内存**。`allocator.allocate(type)` 返回 `void*`（[`BLI_linear_allocator.hh`](../../../source/blender/blenlib/BLI_linear_allocator.hh) L105-L108）。`GMutablePointer` 正好装下"地址 + 该地址的类型"，是二者的最小载体。

代价是**任何解引用都必须先确认类型**：

```cpp
template<typename T> T *get() const
{
  BLI_assert(this->is_type<T>());
  return static_cast<T *>(data_);
}
```

`is_type<T>()` 在 debug 下比对类型索引。release 下断言消失，转错类型就是无声的内存解释错误——这是类型擦除的老账，Blender 用断言兜底。

### 为什么 `input_usages_` 是 `std::optional<ValueUsage>`

`ValueUsage` 本身是三值枚举（`FN_lazy_function.hh` L61-L76）：

```cpp
enum class ValueUsage : uint8_t {
  Used,     /* 确定要用，必须算 */
  Maybe,    /* 不确定，算了也可能丢 */
  Unused,   /* 确定不要 */
};
```

三值已经能表达"三态"了，为什么还要套 `optional`？因为这里需要的是**四态**：三值 + "还不知道"。

| 取值 | 含义 | 谁写 |
| --- | --- | --- |
| `nullopt` | 本轮还没发生任何事 | 构造时的默认值 |
| `Used` | 被请求过 | `try_get_input_data_ptr_or_request_impl` |
| `Unused` | 被明确放弃 | `set_input_unused_impl` |
| `Maybe` | 理论上可写，但本仓库无人写 | 语义主要属于 `Input::usage` 与图执行器的输出状态 |

`nullopt` 与 `Maybe` **不能互换**：前者是"从没被碰过"，后者是"已判定不确定，允许算也允许丢"。简化成 `Maybe` 后，调用方就分不清"可以安全延迟"和"函数已经探过底了"。

还有个容易忽略的事实：**目前 `input_usages_` 只被写、没人读**。`BasicParams` 里写它的三处（L26 构造、L41 写 `Used`、L68 写 `Unused`）之外，两个生产调用方——`geometry_nodes_execute.cc` L571/L642 和 `geometry_nodes_closure_zone.cc` L776/L851——传进去之后都没再读。这不是死代码，而是"报告通道已铺好、消费方还没接上"。读代码时别以为它在驱动什么逻辑。

## 构造函数

```cpp
BasicParams::BasicParams(const LazyFunction &fn,
                         const Span<GMutablePointer> inputs,
                         const Span<GMutablePointer> outputs,
                         MutableSpan<std::optional<ValueUsage>> input_usages,
                         Span<ValueUsage> output_usages,
                         MutableSpan<bool> set_outputs)
    : Params(fn, true),
      inputs_(inputs),
      outputs_(outputs),
      input_usages_(input_usages),
      output_usages_(output_usages),
      set_outputs_(set_outputs)
{
}
```

**六个参数（`fn` + 五张表），全函数体只有初始化列表，一个语句都没有。** 这是"纯记账"最直白的证据。容易数成七个，是因为基类实参 `Params(fn, true)` 里又出现了一次 `fn`，那是给基类的，不是本类的第六张表。

| 参数 | 实参从哪来 | 注意 |
| --- | --- | --- |
| `fn` | 要执行的那个 `LazyFunction` | 只用于基类：`fn_`、`main_thread_id_`、`allow_multi_threading_` |
| `inputs` | 长度 ≥ `fn.inputs().size()` 的 `GMutablePointer` 数组 | 未就绪的槽留默认构造 `{nullptr, nullptr}` 或 `{type, nullptr}` |
| `outputs` | 长度 ≥ 输出数的同类型数组 | 每槽必须指向一块**未初始化**内存 |
| `input_usages` | 长度 ≥ 输入数的 `optional<ValueUsage>` 数组 | 初始全 `nullopt` |
| `output_usages` | 长度 ≥ 输出数的 `ValueUsage` 数组 | 调用方必须填满，函数只读 |
| `set_outputs` | 长度 ≥ 输出数的 `bool` 数组 | 初始必须全 `false`，否则 `output_was_set` 撒谎 |

`Params(fn, true)` 里的第二个参数是 `allow_multi_threading_initially`。硬编码 `true`，和 `try_enable_multi_threading_impl` 无条件 `return true`（L71-L74）一致。资源权限的问题留给第 04 篇。

### 用例一：`execute_lazy_function_eagerly`

这是 `detail` 命名空间存在的唯一理由（头文件 L79-L129 是模板实现，L140-L156 是对外包装）。核心几行：

```cpp
std::array<GMutablePointer, InputsNum> input_pointers;
std::array<GMutablePointer, OutputsNum> output_pointers;
std::array<std::optional<ValueUsage>, InputsNum> input_usages;
std::array<ValueUsage, OutputsNum> output_usages;
std::array<bool, OutputsNum> set_outputs;
```

五个 `std::array`，**全部在栈上**，长度由 `sizeof...(Inputs)` 在编译期算出。填槽：

```cpp
input_pointers[I] = {type, &std::get<I>(inputs)};
```

输入指针指向按值传入的 `std::tuple<Inputs...> inputs` 的元素，输出指针指向 `std::tuple<Outputs *...> outputs` 里的裸指针，也就是**调用方传进来的结果缓冲区**。然后：

```cpp
output_usages.fill(ValueUsage::Used);
set_outputs.fill(false);
LinearAllocator<> allocator;
Context context(fn.init_storage(allocator), user_data, local_user_data);
BasicParams params{
    fn, input_pointers, output_pointers, input_usages, output_usages, set_outputs};
fn.execute(params, context);
fn.destruct_storage(context.storage);

/* Make sure all outputs have been computed. */
BLI_assert(!Span<bool>(set_outputs).contains(false));
```

三个要点：`output_usages` 全填 `Used`，因为"所有输入都给了，就必须算出所有输出"，这是 L132-L139 明说的契约；`set_outputs` 全 `false` 且执行完断言"没有一个是 false"，这就是"急切执行"的定义；`std::array` 能直接当 `Span`/`MutableSpan` 传，因为 `MutableSpan` 有从 `std::array<T, N>&` 构造的构造函数（[`BLI_span.hh`](../../../source/blender/blenlib/BLI_span.hh) L469）——所以五个数组不必同容器，`Array`、`Vector` 都行。`LinearAllocator allocator` 是局部变量，析构时一次性回收。

### 用例二：生产路径（几何节点顶层）

真实的重头在 [`geometry_nodes_execute.cc`](../../../source/blender/nodes/intern/geometry_nodes_execute.cc) L569-L660：

```cpp
Array<GMutablePointer> param_inputs(num_inputs);
Array<GMutablePointer> param_outputs(num_outputs);
Array<std::optional<lf::ValueUsage>> param_input_usages(num_inputs);
Array<lf::ValueUsage> param_output_usages(num_outputs);
Array<bool> param_set_outputs(num_outputs, false);
```

`Array` 构造会默认构造所有元素（[`BLI_array.hh`](../../../source/blender/blenlib/BLI_array.hh) L116-L123），所以 `param_inputs` 一开始每槽都是 `{nullptr, nullptr}`，即"全部未就绪"。填输入时直接塞指针：

```cpp
param_inputs[function.inputs.main[0]] = &value;
```

这能编译是因为 `GMutablePointer` 有 `template<typename T> GMutablePointer(T *data)`（`BLI_generic_pointer.hh` L34-L39），会自动补 `CPPType::get<T>()`。输出侧走另一条路，因为要手工分配：

```cpp
void *buffer = allocator.allocate(type);
param_outputs[i] = {type, buffer};
```

`allocator.allocate(type)` 用 `CPPType` 的 `size` 与 `alignment`，这块内存**未初始化**，符合 `get_output_data_ptr` 的契约（`FN_lazy_function.hh` L136-L139）。收尾：

```cpp
for (const int i : IndexRange(num_outputs)) {
  if (param_set_outputs[i]) {
    GMutablePointer &ptr = param_outputs[i];
    ptr.destruct();
  }
}
```

这就是 `set_outputs_` 存在的真正理由：**告诉调用方哪些槽里真有活对象需要析构**。没被 `output_set` 的槽是未初始化内存，析构它必崩。

## 八个 impl 的实现套路

`Params` 有八个虚函数（`FN_lazy_function.hh` L189-L196），七个纯虚加一个带默认实现（`try_enable_multi_threading_impl`，默认返回 `false`，见 `lazy_function.cc` L66-L69）。`BasicParams` 全部重写，`lazy_function_execute.cc` L32-L74 一共 43 行。

### 1. `try_get_input_data_ptr_impl`

```cpp
void *BasicParams::try_get_input_data_ptr_impl(const int index) const
{
  return inputs_[index].get();
}
```

取槽、取指针、返回，`nullptr` 就是"没有"。注意它是 const 的，而包装层 `Params::try_get_input_data_ptr`（L366-L370）**没有**调 `assert_valid_thread()`；对比 `_or_request`（L372-L377）调了。这个不对称是刻意的：只读探查被认为可以从任意线程做，请求/写入则必须在合法线程上。

### 2. `try_get_input_data_ptr_or_request_impl`

```cpp
void *BasicParams::try_get_input_data_ptr_or_request_impl(const int index)
{
  void *value = inputs_[index].get();
  if (value == nullptr) {
    input_usages_[index] = ValueUsage::Used;
  }
  return value;
}
```

**这是本篇最反直觉的一段**。它名义上叫 `_or_request`（"取不到就请求"），实际行为是：取不到就返回 `nullptr`，顺手把 `input_usages_[index]` 记成 `Used`，**不请求任何东西**。所以在返回值上它和 `try_get_input_data_ptr_impl` 完全等价，唯一差别是那次记账。

为什么可以这样？因为 **`BasicParams` 没有上游**。它的输入内存可能是栈变量，也可能是 allocator 里的一块，这里没有"谁负责算这个输入"的概念，自然无从请求。于是"请求"退化成"声明我要它"——把意图写进 `input_usages_`，交给调用方下次看。

对照真正的请求实现 `GraphExecutorLFParams::try_get_input_data_ptr_or_request_impl`（`lazy_function_graph_executor_generic.hh` L1394-L1402）：

```cpp
return executor_.set_input_required_during_execution(
    node_, node_state_, index, current_task_, this->get_local_data());
```

那里才真的去通知执行器"这个输入现在需要了"，执行器记到 `InputState::usage` 并挂进 `delayed_required_outputs`（L1139-L1145），下一轮调度去算它。两者的差距，就是"记账"与"调度"的差距。

一个副作用要注意：因为记账发生在**取失败**时，调用方读 `input_usages_` 得到的其实是"函数曾经想要但当时没有"，不是"函数最终要不要"。给 `input_usages_` 接消费方时必须处理这个语义差别。

### 3. `get_output_data_ptr_impl`

```cpp
void *BasicParams::get_output_data_ptr_impl(const int index)
{
  return outputs_[index].get();
}
```

返回调用方预分配的未初始化内存。它**不检查这块内存是否已被写过**——重复调两次返回同一地址，第二次会覆盖第一次。防御性检查由重实现提供：`GraphExecutorLFParams` 版会断 `!output_state.has_been_computed`，并在 `value == nullptr` 时才懒分配（L1404-L1414）。

### 4. `output_set_impl`

```cpp
void BasicParams::output_set_impl(const int index)
{
  set_outputs_[index] = true;
}
```

一行赋值，也是唯一会写 `set_outputs_` 的地方。但它承载的语义很重。`Params::set_output`（`FN_lazy_function.hh` L440-L447）是这么调它的：

```cpp
using DecayT = std::decay_t<T>;
this->assert_valid_thread();
void *data = this->get_output_data_ptr(index);
new (data) DecayT(std::forward<T>(value));
this->output_set(index);
```

拿地址、placement new 构造、标记完成。`BasicParams` 只参与第一步和第三步。注释（L143-L146）很硬："Call this after the output value is initialized. After this is called, the value must not be touched anymore. It may be moved or destructed immediately." 翻译：**设完之后不许再碰这个值，它可能立刻被搬走或析构。** 对 `BasicParams` 这种"内存不归我管"的实现，这条尤其要命——调用方完全可能在轮次结束后就清掉 allocator。

为什么这个 bool 数组不干脆在别处维护？因为它是**跨层唯一的最小共享状态**：函数写、调用方读，中间经过 `RemappedParams` 转发（L110-L113 → `base_params_.output_set(output_map_[index])`）时也不需要任何类型信息。

### 5. `output_was_set_impl`

```cpp
bool BasicParams::output_was_set_impl(const int index) const
{
  return set_outputs_[index];
}
```

读同一个数组。语义对应 L149-L153："Allows the #LazyFunction to check whether an output was computed already without keeping track of it itself." 这对"会被执行多次"的函数是刚需。最典型的是 Repeat，`execute_impl` 一进来就查：

```cpp
if (!params.output_was_set(iterations_usage_index)) {
  params.set_output(iterations_usage_index, true);
}
```

（[`geometry_nodes_repeat_zone.cc`](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc) L164-L168）。靠它就能"只设一次"，不用在 storage 里再存标志。测试里的 `PartialEvaluationTestFunction`（`FN_lazy_function_test.cc` L136-L148）也用它判断"这个输出上轮已算过、不用重算"。

### 6. `get_output_usage_impl`

```cpp
ValueUsage BasicParams::get_output_usage_impl(const int index) const
{
  return output_usages_[index];
}
```

纯读。它决定函数要不要费劲算某个输出：`Unused` 就别算，`Used` 必须算，`Maybe` 算了也可能白算。调用方怎么填？`geometry_nodes_execute.cc` L576-L579：

```cpp
param_output_usages.as_mutable_span().slice(function.outputs.main).fill(lf::ValueUsage::Used);
param_output_usages.as_mutable_span()
    .slice(function.outputs.input_usages)
    .fill(lf::ValueUsage::Unused);
```

主输出填 `Used`（用户要几何），"输入使用情况"那组填 `Unused`（这次不关心）。**这是在 execute 之前就定死的**，函数不能改——这就是它为什么是 `Span`。

有个坑：`Array<lf::ValueUsage> param_output_usages(num_outputs);` 对 `enum class : uint8_t` 不做初始化（`BLI_array.hh` L116-L123 说 trivial 类型默认构造"does nothing"）。所以那两个 `fill` 必须覆盖全部下标，漏一段就是读未定义值。上面代码正好按 `main` 与 `input_usages` 两个切片覆盖全量。

### 7. `set_input_unused_impl`

```cpp
void BasicParams::set_input_unused_impl(const int index)
{
  input_usages_[index] = ValueUsage::Unused;
}
```

语义见 L160-L164："Tell the caller ... that a specific input will definitely not be used. Only an input that was not #ValueUsage::Used can become unused."

这条"只能从非 `Used` 变 `Unused`"的规则，**`BasicParams` 没有断言**——它无条件赋值，会覆盖掉之前的 `Used`。断言在图层：`set_input_unused`（`lazy_function_graph_executor_generic.hh` L1086-L1096）里有 `BLI_assert(input_state.usage != ValueUsage::Used);`。为什么图执行器要断？因为那里要维护需求传播的一致性：先请求了上游（`Used`，上游可能已开算）又说不要，算力白花且 `missing_required_inputs` 会对不上。`BasicParams` 没这套账本，就只是记个心情。

使用示例（`node_geo_switch.cc` L188）：`params.set_input_unused(input_to_ignore);` Switch 节点知道自己只用一支，就把另一支标为不要，让上游跳过整棵子树。这是惰性求值省算力的主要手段。

### 8. `try_enable_multi_threading_impl`

```cpp
bool BasicParams::try_enable_multi_threading_impl()
{
  return true;
}
```

无条件成功。因为五个数组本来就是调用方完全掌控的裸内存，没有内部锁、没有 `NodeState`，天然可多线程访问——前提是调用方保证不同 index 不打架。debug 下它还有第二层作用：`Params::try_enable_multi_threading`（L449-L459）成功后会置 `allow_multi_threading_`，之后 `assert_valid_thread` 不再检查线程 id。所以这函数实质上是"解除线程断言"的开关。

## 参数内存布局

假设一个函数有 2 输入 1 输出，用生产路径那种写法：

```text
调用方栈上 / allocator：

  param_inputs      Array<GMutablePointer>，每槽 16 字节
    [0] type_->SocketVariant  data_->0x7f..a100 ──▶ SocketValueVariant 对象
    [1] type_->bool           data_->0x7f..a140 ──▶ bool（外层 Array<bool>）

  param_outputs     Array<GMutablePointer>
    [0] type_->SocketVariant  data_->0x7f..a200 ──▶ 未初始化内存
                                                   （LinearAllocator 按
                                                    CPPType 的 size/alignment 分配）

  param_input_usages  Array<optional<ValueUsage>>，每槽 2 字节
    [0] nullopt   [1] Used          ← 取失败写 Used，放弃写 Unused

  param_output_usages Array<ValueUsage>，每槽 1 字节
    [0] Used                        ← execute 前定死，函数只读

  param_set_outputs   Array<bool>，每槽 1 字节
    [0] false                       ← output_set 后变 true，调用方据此决定是否 destruct

BasicParams 内部（5 个 span = 5×(指针+长度) ≈ 80 字节）：

  inputs_ / outputs_ / input_usages_ / output_usages_ / set_outputs_
      └── 各自指向上面对应数组的起始地址与长度，仅此而已
```

要点：**值不在数组里**——五张表加起来只装"指针 + 小标记"，一个 `GeometrySet` 在输入槽里只占 16 字节；**五块内存彼此独立**，甚至可以是不同容器类型（`Array`、`std::array`、`Vector`），只要各自能转成 `Span`/`MutableSpan`；**`BasicParams` 不拥有任何一块**，它只是一组视图，所以可以随用随建、栈上构造；**`set_outputs_` 是唯一跨轮存活的状态**，只要调用方复用同一个数组，`input_usages_` 与 `set_outputs_` 都会累积，而 `inputs_`/`outputs_` 里的指针由调用方自己改；**对齐由 `CPPType::alignment` 保证**，槽里存着 `type_`，所以任何一处拿到指针都能验证对齐（`BLI_cpp_type.hh` L532-L536），这也是"为什么不直接用 `void*` 数组"的另一个答案。

## 与 RemappedParams 的关系

两句话：**`BasicParams` 是链尾，`RemappedParams` 是链中的转发器。** 前者直接读内存、不查任何"别人"，是终止条件；后者自己不存任何值，只存 `Params &base_params_` 加两张索引表，把每个 `index` 换成 `input_map_[index]` 之后转给底座（L95-L128）。

| 维度 | `BasicParams` | `RemappedParams` |
| --- | --- | --- |
| 存值吗 | 存指针表 | 只存 base 引用与映射 |
| 取输入 | `inputs_[index].get()` | `base_params_.try_get_input_data_ptr(input_map_[index])` |
| 索引含义 | 本函数的接口编号 | 映射后的外层编号 |
| 谁分配 | 构造它的调用方 | 底座那一层 |
| 线程许可 | 无条件 `true` | 缓存在 `bool&`，往上协商 |
| 能否独立工作 | 能 | 不能 |

实际运行时一层 `Params` 是另一层的底座，形成**转发链**。以 Repeat 为例（`geometry_nodes_repeat_zone.cc` L177-L181）：

```cpp
lf::RemappedParams eval_graph_params{*eval_storage.graph_executor,
                                     params,
                                     eval_storage.input_index_map,
                                     eval_storage.output_index_map,
                                     eval_storage.multi_threading_enabled};
```

这里的 `params` 是 Repeat Zone 这个 `LazyFunction` 收到的参数。它自己通常也是图执行器给的 `GraphExecutorLFParams`（Repeat Zone 是更大图里的一个节点），只有顶层调用时才是 `BasicParams`。所以完整链条常是：

```text
BasicParams（最外，几何节点顶层）
   ▲ 转发
GraphExecutorLFParams（外层图里某节点）
   ▲ 转发（RemappedParams，带 index_map）
GraphExecutorLFParams（Repeat 展开图里某节点）
   ▲ ...
```

内层节点说"我要第 3 个输入"，这次调用会一层一层往上爬，最后落到 `BasicParams::try_get_input_data_ptr_impl` 读 `inputs_[映射后的编号].get()`。这就是"参数转发"的字面意思。每层只是替换一次索引或直接读，开销 O(层数)，实践中层数很浅（2-4 层），所以没有缓存。

## 用小数据走一遍

用 `FN_lazy_function_test.cc` L19-L35 的 `AddLazyFunction`：2 输入（`int a`、`int b`）、1 输出（`int`）。测试 L76-L83：

```cpp
TEST_F(LazyFunctionTest, SimpleAdd)
{
  const AddLazyFunction add_fn;
  int result = 0;
  execute_lazy_function_eagerly(
      add_fn, nullptr, nullptr, std::make_tuple(30, 5), std::make_tuple(&result));
  EXPECT_EQ(result, 35);
}
```

**第 0 步：准备。** `inputs = (30, 5)`（栈上 tuple），`outputs = (&result)`，`result = 0`。

**第 1 步：模板展开填指针。**

```cpp
input_pointers[0] = {CPPType::get<int>(), &std::get<0>(inputs)};   // 指向 30
input_pointers[1] = {CPPType::get<int>(), &std::get<1>(inputs)};   // 指向 5
output_pointers[0] = {CPPType::get<int>(), std::get<0>(outputs)};  // 指向 result
```

**第 2 步：初始化标记。** `output_usages.fill(Used); set_outputs.fill(false);` 此时 `input_usages_` 是默认构造的 `[nullopt, nullopt]`，其余两表已是 `[Used]` 与 `[false]`。

**第 3 步：建 Context 与 BasicParams。** `AddLazyFunction` 没重写 `init_storage`，基类返回 `nullptr`（`lazy_function.cc` L28-L31），所以 `context.storage == nullptr`。`BasicParams` 构造后五个字段各自指向那五个 `std::array`。

**第 4 步：`fn.execute(params, context)`。** `assert_valid_thread` 通过（当前线程就是构造 `Params` 时的线程）。`always_used_inputs_available`（`lazy_function.cc` L50-L64）检查：两个 `Input::usage` 都是默认的 `Used`（`FN_lazy_function.hh` L223），所以要求两个输入非空——通过。

**第 5 步：函数体执行。** `params.get_input<int>(0)` 走到 `Params::get_input<int>`（L421-L426），它调非模板 `try_get_input_data_ptr(0)`，断长度后调虚函数，落到 `BasicParams` 的 `inputs_[0].get()`，返回指向 `30` 的地址，`static_cast<int *>` 解引用得 `30`。全程 `input_usages_` 未动——`get_input` 只调 `try_get_input_data_ptr`，不走 `_or_request`。同理得 `b = 5`。接着 `params.set_output(0, a + b)` 三步走：`get_output_data_ptr(0)` 断长度、断线程后 `outputs_[0].get()` 得 `&result`；`new (data) int(35)` 写入 `result`；`output_set(0)` 令 `set_outputs_[0] = true`。

最终状态：`inputs_` 仍是 `[{int*,→30}, {int*,→5}]`；`outputs_` 仍是 `[{int*,→result}]`；`input_usages_` 仍是 `[nullopt, nullopt]`，全程没变，因为走的是只读路径；`output_usages_` 仍是 `[Used]`；`set_outputs_` 变成 `[true]`，这是 `output_set` 唯一写过的地方。

**第 6 步：收尾。** `destruct_storage(nullptr)`（基类断言 storage == nullptr）；`BLI_assert(!Span<bool>(set_outputs).contains(false))` 通过；`EXPECT_EQ(result, 35)` 通过。

三个"什么都没发生"的地方，正是 `BasicParams` 的性格：`input_usages_` 全程 `nullopt`（用的是 `get_input`，只读路径）；没有任何分配（输入是 tuple 元素，输出是调用方的 `&result`）；没有析构（`int` 是 trivial 且 `execute_lazy_function_eagerly` 压根不做析构，它把 `result` 当调用方的东西）。

## 反例与边界

### 反例 1：以为 `BasicParams` 会自动请求上游

```cpp
int *v = params.try_get_input_data_ptr_or_request<int>(0);
/* v 仍是 nullptr；下一轮 execute 时输入还是空的 */
```

`BasicParams` 没有上游，无从请求，只把 `input_usages_[0]` 记成 `Used` 就返回 `nullptr`（L37-L44）。需要真正的请求能力，必须用图执行器那套，或者自己在调用方实现"看到 `Used` 就补数据、再 execute 一次"的循环。

### 反例 2：以为 `_or_request` 和 `try_get_input_data_ptr` 一样

返回值一样，副作用不一样：`_or_request` 会把 `input_usages_[index]` 从 `nullopt` 改成 `Used`。更麻烦的是它会**把 `Unused` 覆盖成 `Used`**——先 `set_input_unused(i)` 再 `_or_request(i)`，标记就变回 `Used`，`BasicParams` 不拦，违反 L162-L163 那条"Only an input that was not #ValueUsage::Used can become unused"的精神。

### 反例 3：以为 `set_outputs_` 是位数组

类型是 `MutableSpan<bool>`，每元素 1 字节，**不是** `std::vector<bool>` 的位压缩；`std::array<bool, N>` 也一样 1 字节/元素。所以不能对它做位运算，也别指望它省内存。输出数量在几何节点里也就几十个，1 字节不是问题。

### 反例 4：以为 `GMutablePointer` 会自动析构

```cpp
{
  GMutablePointer ptr = {CPPType::get<std::string>(), allocator.allocate(CPPType::get<std::string>())};
  new (ptr.get()) std::string("hello");
}  /* ptr 是平凡类型，没有析构函数。字符串泄漏 */
```

`GMutablePointer` 整个类里**没有析构函数**（`BLI_generic_pointer.hh` L18-L82）。它不会 `delete`、不会调 `CPPType::destruct`，必须显式 `ptr.destruct()`（L77-L81，内部调 `type_->destruct(data_)`）。而且要小心：`destruct()` 里有 `BLI_assert(data_ != nullptr)`，空指针调它直接断言失败，所以生产代码总是先查 `set_outputs_` 再析构。

### 反例 5：以为输入指针返回非空就能一直用

指针有效期由底层内存决定，`BasicParams` 不延长它。`GraphExecutorLFParams` 那边更激进：`output_set_impl` 一调完就把 `output_state.value = nullptr`（L1426-L1427），值已转发走、可能已被搬移。规则是：**非 const `Params` 方法调用之间，之前拿到的指针都可能失效**；要长期持有就 move 出来（`params.extract_input<T>(i)`，L412-L419）。

### 反例 6：以为数组长度会被检查

包装层断言的是 `index < fn_.inputs().size()`（L368），检查的是 **`fn` 声明的接口大小**，不是 `inputs_` span 的实际长度：

```cpp
std::array<GMutablePointer, 1> only_one;   /* 但这个函数有 3 个输入 */
BasicParams params{fn_with_3_inputs, only_one, /*...*/};
params.get_input<int>(2);                  /* 断言通过，数组越界读 */
```

`BasicParams` 构造时也不校验长度。这是零开销抽象的代价，写自定义用法时务必用 `fn.inputs().size()` 而不是硬编码数字。另外别以为 `fn` 参数是摆设：`BasicParams` 自己不读 `fn_`，但基类的 `assert_valid_thread` 要用构造时记下的 `main_thread_id_`，长度断言要用 `fn_.inputs().size()`。传一个和数组对不上的 `fn` 会同时破坏长度断言和线程断言。

### 反例 7：以为 `output_usages_` 能中途改

它是 `Span<ValueUsage>` 不是 `MutableSpan`，`get_output_usage_impl` 是 const 方法。想在 `execute_impl` 里"算着算着发现不需要某个输出"然后往回写？做不到，也不该做——输出需求是调用方的决策，半途改变会让调用方无从适从。

### 反例 8：把 `nullopt` 当成 `Maybe`

`std::optional<ValueUsage>{}` 是"还没有信息"，`ValueUsage::Maybe` 是"已知不确定"。前者可以合法升级成任何一个三值，后者已经是结论。混用会让需求传播的日志全是噪声。

## 对理解 Repeat 的帮助

Repeat Zone 的 `execute_impl`（[`geometry_nodes_repeat_zone.cc`](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc) L153-L185）里，每个 `params.xxx` 都对应本篇某个 `_impl`：

| Repeat 代码 | 经过的包装层 | 最终落到 |
| --- | --- | --- |
| `params.output_was_set(iterations_usage_index)` (L165) | `Params::output_was_set` | `output_was_set_impl` → 读 `set_outputs_[i]` |
| `params.set_output(iterations_usage_index, true)` (L167) | `Params::set_output`（取地址 + placement new + `output_set`） | `get_output_data_ptr_impl` + `output_set_impl` → 读 `outputs_[i].get()`、写 `set_outputs_[i] = true` |
| `params.get_input<SocketValueVariant>(zone_info_.indices.inputs.main[0])` (L207) | `Params::get_input<T>` → `try_get_input_data_ptr` | `try_get_input_data_ptr_impl` → `inputs_[i].get()` |
| 构造 `lf::RemappedParams`，把本层 `params` 当 `base_params_` (L177) | —— | 之后内层所有调用都先做索引映射再向上转发 |

三条推论。

**第一，`get_input` 不会写 `input_usages_`**。它走 `try_get_input_data_ptr`，不是 `_or_request`。所以 Repeat 从 iterations 输入取迭代次数时，**不会**在 `input_usages_` 上留下 `Used` 的痕迹——但那次计算早就发生了，留不留下无所谓。

**第二，`set_output(..., true)` 的 `true` 落在哪块 bool 上，取决于 `params` 的实际类型。** 顶层调用是 `BasicParams` 时落在调用方传的 `param_set_outputs`；是图里节点时落在 `NodeState::outputs[i].has_been_computed`。同一个 `set_output`，两种记账本。

**第三，`output_was_set` 是 Repeat 单次执行正确性的支点。** `execute` 可能被调多次（展开图执行需要多轮），而"iterations 已标为 Used"这件事只需做一次，`set_outputs_` / `has_been_computed` 就是那个"只做一次"的判据。

再看最关键的三行（L177-L184）：

```cpp
lf::RemappedParams eval_graph_params{*eval_storage.graph_executor,
                                     params,
                                     eval_storage.input_index_map,
                                     eval_storage.output_index_map,
                                     eval_storage.multi_threading_enabled};
lf::Context eval_graph_context{
    eval_storage.graph_executor_storage, context.user_data, context.local_user_data};
eval_storage.graph_executor->execute(eval_graph_params, eval_graph_context);
```

第一行把上层 `params` 整包塞进 `RemappedParams`，从此内层所有 `try_get_input_data_ptr_impl` 都会**往上转发，最后撞到某个 `BasicParams` 或 `GraphExecutorLFParams`**。这解释了为什么"参数内存布局"在 Repeat 里体现不出来——Repeat 的 `execute_impl` 里根本没有数组，只有转发。

索引映射的具体内容（L370-L381）：`input_index_map` 是 `fill_index_range<int>(..., 1)`，即内层第 i 个输入映射到外层第 i+1 个（外层第 0 个是 iterations，不进展开图）；`output_index_map` 则是跳过 `iteration_usage_index` 的分段填法。那是下一篇的主题，这里只需记住：**映射表里每个值就是一次往上的 `index` 替换**。

最后是三条实用推论。想知道某个值在哪块内存？沿 `Params` 链往上问这层是 `BasicParams` 还是 `GraphExecutorLFParams`，答案决定它是"调用方栈/allocator"还是"执行器的 `LinearAllocator`"。看到输出没算出来？先查 `set_outputs_` / `has_been_computed`；看到输入为空？先分清是"没填槽"还是"没转发"。想判断这轮要不要算某个输出，用 `get_output_usage(i)`，别自己猜。

## 继续阅读

- 上一篇：[01-Context存储与UserData](01-Context存储与UserData.md)
- 下一篇：[03-RemappedParams参数重映射](03-RemappedParams参数重映射.md)
- 本章导航：[02-参数转发与上下文](README.md)
- 相关源码：[`FN_lazy_function_execute.hh`](../../../source/blender/functions/FN_lazy_function_execute.hh) L19-L47 · [`intern/lazy_function_execute.cc`](../../../source/blender/functions/intern/lazy_function_execute.cc) L17-L74 · [`FN_lazy_function.hh`](../../../source/blender/functions/FN_lazy_function.hh) L105-L197
- 类型擦除背景：[08-类型擦除](../08-类型擦除/README.md) 中 `CPPType` 与 `GMutablePointer` 相关篇目
- 分配器背景：[04-生命周期与分配](../04-生命周期与分配/README.md) 中 `LinearAllocator` 篇目
