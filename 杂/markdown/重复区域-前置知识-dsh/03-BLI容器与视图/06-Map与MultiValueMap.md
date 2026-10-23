# 06 · Map 与 MultiValueMap

[前置知识总入口](../README.md) · [本章导航](README.md) · [上一篇](05-VectorSet稳定索引.md) · [下一篇](07-IndexRange与OffsetIndices.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `Map` 与 `MultiValueMap`——后者的"一键多值"语义是 Repeat 副作用表的关键。主要源码：[`BLI_map.hh`](../../../source/blender/blenlib/BLI_map.hh)（1383 行）、[`BLI_multi_value_map.hh`](../../../source/blender/blenlib/BLI_multi_value_map.hh)（167 行）。

`[讲解]` 一处行数校正：本地工作树里 `BLI_multi_value_map.hh` 实测 **189 行**，本章总表记的 167 是更早的旧值。下文行号一律按 189 行引用；`BLI_map.hh` 的 1383 行与表格一致。以文件为准，不以表格为准。

## 先回答一个具体问题

如果我要记录"同一个上下文哈希下有哪些节点有副作用"，普通 `Map` 为什么不够？

`[讲解]` 因为副作用节点与上下文之间**不是一对一**，而是一对多。看 `BLI_map.hh` 对 `add` 的承诺（L288-L294）：

> "Add a key-value-pair to the map. If the map contains the key already, nothing is changed. If you want to replace the currently stored value, use `add_overwrite`. Returns true when the key has been newly added."

`[讲解]` 这句话有两层杀伤力。第一，键已存在时 `add` 什么都不做，你的第二次写入被**静默丢弃**；第二，它只用一个 `bool` 告诉你"是否新增"，不会报错、不会警告、也不会覆盖。于是下面这段代码看起来完全正常：

```cpp
Map<std::pair<ComputeContextHash, int32_t>, int> iterations;
iterations.add({ctx_hash, output_node_id}, 0);   // 第 0 轮有副作用
iterations.add({ctx_hash, output_node_id}, 1);   // 第 1 轮有副作用 —— 被丢弃，返回 false
```

`[讲解]` 结果 `iterations` 里只剩 `0`。如果有两个 Viewer 分别看第 0 轮和第 1 轮，系统就只知道第 0 轮要算，第 1 轮的 Viewer 拿到的数据是空的。这就是 `MultiValueMap` 存在的全部理由：**键仍然唯一，但每个键挂一条值列表**。

`[讲解]` 真实结构白纸黑字写在 [`NOD_geometry_nodes_lazy_function.hh`](../../../source/blender/nodes/NOD_geometry_nodes_lazy_function.hh) L149-L156：

```cpp
struct GeoNodesSideEffectNodes {
  MultiValueMap<ComputeContextHash, const lf::FunctionNode *> nodes_by_context;
  /**
   * The repeat/foreach zone is identified by the compute context of the parent and the identifier
   * of the repeat output node.
   */
  MultiValueMap<std::pair<ComputeContextHash, int32_t>, int> iterations_by_iteration_zone;
};
```

`[讲解]` 两张表都是 `MultiValueMap`，但用法不同：`nodes_by_context` 的"多值"是为了合并多个 Viewer 路径（同一个上下文可能收集到好几种节点），`iterations_by_iteration_zone` 的多值则是**语义必需**——同一次 Repeat 的每一轮都可能带副作用，必须全部记住。

## Map 的设计取向

`[讲解]` `BLI_map.hh` 的开头注释（L10-L53）是理解这个容器最快的入口。它第一句就定调（L10-L15）：

> "A `Map<Key, Value>` is an unordered associative container that stores key-value pairs. The keys have to be unique. It is designed to be a more convenient and efficient replacement for `std::unordered_map`."

> "Your default choice for a hash map in Blender should be `Map`."

`[讲解]` 然后是实现取向（L17-L19）：

> "Map is implemented using open addressing in a slot array with a power-of-two size. Every slot is in one of three states: empty, occupied or removed."

`[讲解]` 与 `std::unordered_map` 的差异，逐条摊开看：

| 维度 | `std::unordered_map` | `blender::Map` |
| --- | --- | --- |
| 冲突解决 | 标准不规定，主流实现是链地址/分桶 | **开放寻址**，槽数组大小强制为 2 的幂（L17-L19） |
| 槽位状态 | 隐含在桶的链表结构里 | **显式三态**：empty / occupied / removed（L18-L19） |
| 负载因子 | 实现自定义（常见接近 1.0） | **固定 1/2 = 50%**，超出即扩容（L161-L163） |
| 迭代方式 | range-for、迭代器对 | **不能 range-for**，只能用 `keys()` / `values()` / `items()`（L41-L43） |
| 命名风格 | `find` / `insert` / `erase` / `count` | `lookup_ptr` / `add_new` / `remove_contained` / `contains`（L51-L52） |
| 异构查找 | C++26 之前基本没有 | 所有接口都有 `_as` 后缀版本，按另一类型直接查、不做转换（L44-L46） |
| 小对象优化 | 无 | `InlineBufferCapacity` 模板参数；默认构造廉价，槽数组懒初始化（L37、L47-L48） |
| 指针稳定性 | 迭代器/rehash 后失效 | 注释直接写明"修改或移动 map 会令键值指针失效"（L33） |
| 定制点数量 | Hash / KeyEqual / Allocator | Hash / IsEqual / ProbingStrategy / Slot / Allocator / InlineBufferCapacity 共六个（L87-L128） |
| 内存来源 | `operator new` | `GuardedAllocator`；另有 `RawMap` 别名走 `RawAllocator`，供静态存储期使用（L1368-L1381） |
| 调试手段 | 无 | `print_stats()` 打印键分布与内存占用（L964-L971） |
| 相等比较 | 按内容 | 按内容（L1071-L1096） |

`[讲解]` 其中三条值得单独强调，因为它们直接影响**你写代码的方式**。

`[讲解]` 第一条是**不能 range-for**（L41-L43）：

> "You cannot use a range-for loop on the map directly. Instead use the keys(), values() and items() iterators. If your map is non-const, you can also change the values through those iterators (but not the keys)."

`[讲解]` 源码还加了一层防呆（L918-L927）：`keys() const &&`、`items() &&` 等右值限定重载被显式 `= delete`。注释解释了原因：

> "Avoid common bug when trying to do something like this: `for (auto key : get_map().keys())`. This does not work, because the compiler does not extend the lifetime of the map for the duration of the loop."

`[讲解]` `get_map()` 返回临时 `Map`，而迭代器里只存 `slots_` 的裸指针和总槽数，临时对象一销毁就成了野指针。编译器本可以让你写出来，源码主动封掉了这个口子。

`[讲解]` 第二条是**键不可变**。`MapItem` / `MutableMapItem`（L66-L85）里 `key` 永远是 `const Key &`——改键会改变哈希值，槽位就再也找不回来；所以 `items()` 的非 const 版本 `MutableMapItem` 只把 `value` 放开成 `Value &`，`key` 仍是 `const Key &`。

`[讲解]` 第三条是**定制点是"六个而不是三个"**。`ProbingStrategy` 与 `Slot` 在标准库里根本不存在，因为标准没规定冲突解决方式和槽位布局。默认策略是 [`BLI_probing_strategies.hh`](../../../source/blender/blenlib/BLI_probing_strategies.hh) L198 的 `PythonProbingStrategy<>`（CPython 2020 年的方案），不是朴素线性探测；再配合 [`BLI_hash.hh`](../../../source/blender/blenlib/BLI_hash.hh) L135-L148 里"整型默认用恒等哈希"——哈希质量靠探测策略兜底，这是"默认就快"的原因。

## Map 的核心接口

`[讲解]` 1383 行里方法很多，但按"缺失键时怎么办"归类就清楚了：

| 方法 | 行为 | 键不存在时 | 键已存在时 |
| --- | --- | --- | --- |
| `add(key, value)` | 插入 | 插入，返回 `true` | **不改动**，返回 `false` |
| `add_new(key, value)` | 断言后插入 | 插入 | `BLI_assert` 失败（UB） |
| `add_overwrite(key, value)` | 插入或覆盖 | 插入，返回 `true` | **覆盖**，返回 `false` |
| `lookup(key)` | 取引用 | `BLI_assert` 失败（UB） | 返回 `Value &` |
| `lookup_ptr(key)` | 取指针 | 返回 `nullptr` | 返回 `Value *` |
| `lookup_try(key)` | 取值副本 | 返回 `std::nullopt` | 返回 `std::optional<Value>` |
| `lookup_default(key, def)` | 取值或默认 | 返回 `def` 的副本 | 返回值的副本 |
| `contains(key)` | 判定存在 | `false` | `true` |
| `lookup_or_add(key, value)` | 取或插 | 插入后返回引用 | 返回已有引用 |
| `lookup_or_add_default(key)` | 取或插默认值 | 值默认构造后插入 | 返回已有引用 |
| `lookup_or_add_cb(key, cb)` | 取或惰性构造 | **调用 cb** 构造后插入 | 返回已有引用，**不调用 cb** |
| `remove(key)` | 删除 | 返回 `false` | 返回 `true` |
| `remove_contained(key)` | 断言后删除 | `BLI_assert` 失败 | 删除 |
| `pop` / `pop_try` / `pop_default` | 取出并删 | 分别 UB / `nullopt` / 默认值 | 返回被移出的值 |

`[讲解]` 上面每个方法又都有四个转发重载（`const&`/`&&` 的键 × `const&`/`&&` 的值），再加一个 `_as` 模板版本。所以文件里"方法"的实际数量是表里的五倍左右——这也是它 1383 行的主要原因。

### `add` 三兄弟的选择

`[讲解]` 头注释 L38-L39 有一条使用建议：

> "The methods `add_new` and `remove_contained` should be used instead of `add` and `remove` whenever appropriate. Assumptions and intention are described better this way."

`[讲解]` 意思是：当你**确信**键不在里面时，用 `add_new`——它会先 `BLI_assert(!this->contains_as(key))`（L1174），把你的意图写成断言，逻辑错了立刻炸在出错的地方，而不是等到别处表现异常。同理，确信存在就用 `remove_contained`，不确定才用 `remove`。

### `lookup_or_add_cb` 的惰性构造

`[讲解]` 这是全文件最值得细看的一个接口，声明在 L611-L633，实现是 `lookup_or_add_cb__impl`（L1251-L1269）。注释说（L611-L618）：

> "Returns a reference to the value that corresponds to the given key. If the key is not yet in the map, it will be newly added."

> "The create_value callback is only called when the key did not exist yet. It is expected to take no parameters and return the value to be inserted. The callback is called before the key is copied/moved into the map."

`[讲解]` 实现只有二十行：

```cpp
template<typename ForwardKey, typename CreateValueF>
Value &lookup_or_add_cb__impl(ForwardKey &&key, const CreateValueF &create_value, uint64_t hash)
{
  this->ensure_can_add();

  MAP_SLOT_PROBING_BEGIN (hash, slot) {
    if (slot.is_empty()) {
      slot.occupy(std::forward<ForwardKey>(key), hash, create_value());
      occupied_and_removed_slots_++;
      return *slot.value();
    }
    if (slot.contains(key, is_equal_, hash)) {
      return *slot.value();
    }
  }
  MAP_SLOT_PROBING_END();
}
```

`[讲解]` 四个语义要点：

- **一次探查，查与插合并**。整段只有一层探测循环，`ensure_can_add()` 先把容量备好，然后边走槽位边判断。如果拆成 `contains` + `add`，同一个键要喂两次哈希、走两遍探测链。
- **惰性**。`create_value()` 出现在 `slot.is_empty()` 分支内部，是"独占分支"，所以键已存在时**根本不会执行**——不是靠 if 判断，而是靠控制流位置。反过来，`lookup_or_add(key, value)` 的 `value` 是实参，**调用前就构造好了**，命中与否都要付一次构造代价。这是两者的本质差别。
- **回调在键落槽之前调用**。`slot.occupy(key, hash, create_value())` 里两边都在 `occupy` 之内求值，回调执行时键还没进槽位。所以回调**不能**从 map 里反查这个键（还不存在），也**不能**重入修改同一个 map（会破坏正在进行的探测）。
- **回调无参、返回 `Value`**。它拿不到键。`cb` 就是 callback 的缩写——Blender 风格里缩写优先。

`[讲解]` `lookup_or_add_default` 就是它的特例（L647-L650）：`return this->lookup_or_add_cb_as(std::forward<ForwardKey>(key), []() { return Value(); });` —— 传一个返回 `Value()` 的空 lambda。MultiValueMap 的 `add` 就架在它上面。

`[讲解]` 还有一个"既要造又要改"的 `add_or_modify`（L460-L500），回调签名改成 `Value *`：`create_value` 拿到未初始化内存自行 placement-new，`modify_value` 拿到已初始化值原地改，两者返回类型必须一致。注释给的例子是 `[](int *v){ *v = 5; }` 配 `[](int *v){ (*v)++; }`，效果"首次置 5，之后每次 +1"。`add_overwrite` 就是用 `add_or_modify` 实现的（L1291-L1304）：`create_func` 里 placement-new 返回 `true`，`modify_func` 里赋值返回 `false`，返回值恰好表达"是否新增"。

### 迭代器家族

`[讲解]` 所有迭代器共用 `BaseIterator`（L700-L755），只存三个字段：`slots_`、`total_slots_`、`current_slot_`。`operator++` 就是向后扫槽位、跳过非 occupied 的（`while (++current_slot_ < total_slots_) { if (occupied) break; }`）。

`[讲解]` 直接推论：**遍历顺序 = 槽位顺序**。槽位下标是哈希值按 `slot_mask_` 掩出来的，所以遍历顺序取决于键的哈希值，与插入顺序毫无关系。这一条在"反例与边界"里还会出现。

`[讲解]` 四个迭代器用 CRTP 挂在 `BaseIteratorRange` 上（L761-L782），`begin()` 从 0 找第一个 occupied，`end()` 直接把 `current_slot_` 设成 `total_slots_`。注释统一加了一句：**"The iterator is invalidated, when the map is changed."**（L872-L873 等）

`[讲解]` 另有"边遍历边删"的接口：`remove(iterator)`（L929-L940）允许删除当前迭代位置，删完不能再访问该元素；`remove_if(predicate)`（L942-L962）返回删除个数，对齐 `std::erase_if`。

## MultiValueMap 的语义

`[讲解]` 打开 [`BLI_multi_value_map.hh`](../../../source/blender/blenlib/BLI_multi_value_map.hh)，头注释（L10-L20）四句话讲完了全部设计：

> "A `MultiValueMap<Key, Value>` is an unordered associative container that stores key-value pairs. It is different from `Map` in that it can store multiple values for the same key. The list of values that corresponds to a specific key can contain duplicates and their order is maintained."

> "This data structure is different from a `std::multi_map`, because multi_map can store the same key more than once and MultiValueMap can't."

> "Currently, this class exists mainly for convenience. There are no performance benefits over using Map<Key, Vector<Value>>. In the future, a better implementation for this data structure can be developed."

`[讲解]` 逐句翻译成工程含义：

- **值列表可以有重复，且保持顺序**。同一个键下 `add(k, 1)` 两次，列表就是 `[1, 1]`，不去重，也不是 `std::multimap` 那种按键排序。
- **键不能重复**。这是它与 `std::multimap` 的分水岭：`multimap` 里 `k` 可以出现多次，整个容器没有"键唯一"约束；`MultiValueMap` 里 `k` 只出现一次，多出来的是它名下的值。
- **没有性能优势，只是便利封装**。这句话极其诚实，也极其重要：任何时候你都可以把它换手写成 `Map<Key, Vector<Value>>`，行为完全一致。

`[讲解]` 后一条在源码里是字面落实的。类定义（L28-L34）：

```cpp
template<typename Key, typename Value> class MultiValueMap {
 public:
  using size_type = int64_t;

 private:
  using MapType = Map<Key, Vector<Value>>;
  MapType map_;
```

`[讲解]` 全文只有 **一个成员** `map_`（`using MapType = Map<Key, Vector<Value>>;` + `MapType map_;`），没有索引、没有额外缓存、没有第二层结构。

`[讲解]` 于是"它与 `Map<Key, Vector<Value>>` 的关系与差异"可以一句话回答：**关系是完全等价，差异只在语法糖**。

| 方面 | 手写 `Map<Key, Vector<Value>>` | `MultiValueMap` |
| --- | --- | --- |
| 追加一个值 | `map.lookup_or_add_default(k).append(v)` | `map.add(k, v)` |
| 追加一批 | `map.lookup_or_add_default(k).extend(span)` | `map.add_multiple(k, span)` |
| 取值 | `map.lookup(k)` 得到 `Vector<Value>&` | `map.lookup(k)` 得到 `Span<Value>` |
| 缺失键取值 | 先 `lookup_ptr` 判空，再决定 | 直接得到空 `Span`，无需判空 |
| 去重追加 | `vec.append_non_duplicates(v)` | `map.add_non_duplicates(k, v)` |
| 遍历 | `item.value` 是 `Vector` | 同左，`item.value` 可直接当 `Span` 用 |

`[讲解]` `add_as` 的实现（L57-L62）就是第一种写法的机械展开：`Vector<Value> &vector = map_.lookup_or_add_default_as(...); vector.append(...);`。三次哈希变一次：`lookup_or_add_default_as` 内部走 `lookup_or_add_cb`，一条探测链同时完成"找桶"和"若缺失则插入空 Vector"，之后 `append` 是纯 Vector 操作。手写 `if (!map.contains(k)) map.add(k, {}); map.lookup(k).append(v);` 至少两次哈希。

`[讲解]` 注意 `add_as` 返回 `void`——不像 `Map::add` 返回 `bool`。对 MultiValueMap 来说"是否新建了键"通常不是使用方关心的信息。这个签名也暗示了它的定位：**它是一张"多值登记表"，不是一张"插入成功性判定表"**。

## MultiValueMap 接口逐个

`[讲解]` 189 行里公开接口一共十一个（`add` / `add_non_duplicates` / `add_multiple` / `lookup` / `size` / `is_empty` / `items` / `keys` / `values` / `clear` / `clear_and_shrink`），全部是转发或两行代码。

### `add`

`[讲解]` 四个重载（L41-L56）覆盖 `const&`/`&&` 的键值组合，最终都落到 `add_as`。L37-L40 的注释：

> "Add a new value for the given key. If the map contains the key already, the value will be appended to the list of corresponding values."

`[讲解]` 关键词是 **appended**（追加），不是 replaced（替换）、也不是 ignored（忽略）。这一词之差就是它与 `Map::add` 的全部区别。

### `add_non_duplicates`

`[讲解]` L64-L68，头注释里**没有**它，是从 `Vector::append_non_duplicates` 直接搬来的能力：`Vector<Value> &vector = map_.lookup_or_add_default_as(key); vector.append_non_duplicates(value);`。

`[讲解]` 注意 `append_non_duplicates` 是**线性查重**，所以这个接口在值很多时是 O(N)。Repeat 场景里每个 zone 的迭代数通常几十到几百，代价可忽略；但如果你拿它当"集合"用在上千个值上，就该换 `VectorSet` 了。

### `add_multiple`

`[讲解]` L70-L85，注释只有一句：

> "Add all given values to the key."

`[讲解]` 实现是 `Vector<Value> &vector = map_.lookup_or_add_default_as(...); vector.extend(values);`。参数是 `Span<Value>`，所以既能接 `Vector`（隐式转换，[`BLI_vector.hh`](../../../source/blender/blenlib/BLI_vector.hh) L366 的 `operator Span<T>()`），也能接花括号初始化列表（测试 `BLI_multi_value_map_test.cc` L58 的 `map.add_multiple(2, {4, 5, 6})` 就是这么用的）。`extend` 一次扩容，比逐个 `add` 少若干次 realloc 判断。

`[讲解]` 这个接口在实际代码里最重要的用途是**合并两张表**。[`MOD_nodes.cc`](../../../source/blender/modifiers/intern/MOD_nodes.cc) L650-L655 用两组对称的循环，把 `local_side_effect_nodes` 里两张表的每个 `(item.key, item.value)` 原样 `add_multiple` 进 `r_side_effect_nodes`。

`[讲解]` `item.value` 在这里是 `const Vector<Value> &`，直接喂给 `add_multiple` 的 `Span` 参数。多条 Viewer 路径各自往 `local_side_effect_nodes` 里登记，最后一次性并进结果表——**不同 Viewer 路径撞到同一个键时，值会累加而不是互相覆盖**。要是换成 `Map`，第二次合并就把第一次的整条列表吞掉了。

### `lookup`

`[讲解]` 两个版本（L87-L117），const 返回 `Span<Value>`，非 const 返回 `MutableSpan<Value>`。const 版的全文就是：`const Vector<Value> *vector = map_.lookup_ptr_as(key);` 若为空 `return {};`，否则 `return vector->as_span();`。

`[讲解]` 三件事在这一小段里全发生了：用 `lookup_ptr_as` 而不是 `lookup_as`（后者会断言）；空指针分支返回 `return {}`，即默认构造的 `Span`（[`BLI_span.hh`](../../../source/blender/blenlib/BLI_span.hh) L85-L92，`data_ = nullptr, size_ = 0`）；命中分支 `vector->as_span()`，零拷贝。

### 关于 `lookup_default`：它不存在

`[讲解]` 任务清单里提到了 `lookup_default`，但读完 189 行会发现 **MultiValueMap 没有这个成员**。这不是遗漏，而是被空 `Span` 取代了：`Map` 需要 `lookup_default(key, default_value)` 是因为它的 `lookup` 会在缺失时断言、`lookup_ptr` 会返回空指针——使用方要么判空、要么给默认值兜底。而 `MultiValueMap::lookup` 缺失时返回的是**尺寸为 0 的 Span**，本身就是一个合法、可遍历、可调 `size()` 的"空集合"，`for` 循环自然一次都不进。

`[讲解]` 换句话说：**返回视图而不是返回元素，把"默认值"这个问题在类型层面消解掉了**。这是下一节的主题。

### `items` / `keys` / `values`

`[讲解]` 全部直接转发给 `map_`（L136-L174），而且三个都带同一句注释：

> "NOTE: This signature will change when the implementation changes."

`[讲解]` 这句话是给你写代码时的警告：**不要把 `item.value` 的具体类型写进你自己的公共接口**。现在它是 `const Vector<Value> &`，未来实现换成"分段存储"或"扁平化数组"就会变。安全用法是像测试 L112-L114 那样立刻收敛成 `Span`：`for (auto &&item : map.items()) { Span<int> values = item.value; }`——赋值即退化成视图，不依赖底层容器类型。

`[讲解]` `values()` 迭代出来的就是一堆 `Span`，测试 L99-L105 里写的是 `Vector<Span<int>>`——每个键贡献一个 span。

### `size` 与 `is_empty`

`[讲解]` L119-L134。`size()` 的实现就是 `return map_.size();`，注释则针对 `is_empty()`：

> "Returns true if there are no keys in the map. NOTE: There may be keys without values. In this case the map is not empty."

`[讲解]` **`size()` 数的是键，不是值**。一张表里 `size() == 2` 也可能装着 300 个值。那句"可能存在有键无值的条目"是防御性说明：公开 API 走不到那个状态（`add` 一定会 append 至少一个值），但如果内部实现换成"先占位后填值"，这个状态就可能出现，于是提前把语义钉死。读源码时这类"看起来用不上的注释"往往最有信息量。

## lookup 为什么返回 Span

`[讲解]` 把两个 `lookup` 摆在一起对比，差异就清楚了：

| 容器 | `lookup` 返回 | 缺失键时 | 能否 range-for | 拷贝代价 |
| --- | --- | --- | --- | --- |
| `Map<K, V>` | `Value &` | `BLI_assert` 崩溃 | 不适用（单个值） | 无 |
| `Map<K, V>` | `Value *`（`lookup_ptr`） | `nullptr` | 不适用 | 无 |
| `MultiValueMap<K, V>` | `Span<Value>` | 空 `Span`（`size() == 0`） | **可以** | 无（16 字节的指针+长度） |

`[讲解]` 四个理由，从浅到深：

- **值的个数本身是变量**。"这个键对应几个值"在编译期未知，在运行期也随时可能变，所以接口不可能返回"对某个元素的引用"，只能返回"一片元素"。`Span` 恰好是"一片元素"的最小表示。
- **`Span` 自带长度，消除了判空分支**。返回 `Value*` 的写法，调用方必须 `if (ptr)`；返回 `Span` 的写法，`for (const int i : span)` 在空 span 上自然零次迭代。代码从"两分支"塌成"一分支"。
- **零拷贝、零分配**。`Vector` 的元素本来就连续存储，`as_span()` 只是把 `begin_ + size` 打包（[`BLI_vector.hh`](../../../source/blender/blenlib/BLI_vector.hh) L390-L398），不复制一个元素、不做一次堆分配。对比 `std::multimap::equal_range` 返回一对迭代器——语义相近但用起来笨重，且调用方要自己去 `distance`。
- **下游消费方式决定接口形状**。看 [`geometry_nodes_repeat_zone.cc`](../../../source/blender/nodes/intern/geometry_nodes_repeat_zone.cc) L84-L93：`const Span<int> iterations_with_side_effects = ...->iterations_by_iteration_zone.lookup({context_hash, repeat_output_bnode_->identifier});` 之后直接 `for (const int i : iterations_with_side_effects) { if (i >= 0 && i < lf_body_nodes_.size()) lf_nodes.append(lf_body_nodes_[i]); }`。

`[讲解]` provider 拿到 span 就直接 range-for，一个 `if (ptr != nullptr)` 都不需要。假如接口返回 `Vector<int>*` 或 `const Vector<int>*`，这段代码就要多一层解引用和一层判空，而且会把"值存在 `Vector` 里"这个实现细节泄露给调用方——与头注释那句 `NOTE: This signature will change` 的意图正好相反。

`[讲解]` 顺带一个容易被忽略的点：`Span` 是**只读**视图，而 `MultiValueMap::lookup` 的非 const 重载返回 `MutableSpan`。这个 const 重载决议由一个 `this` 的常量性决定，和 `Vector::as_span()` / `as_mutable_span()` 完全同构。所以问题"能不能改"的答案，取决于"你手上这个 map 是不是 const"，而不是取决于你调哪个名字的接口。

## 为什么副作用表需要它

`[讲解]` 回到正篇 04-03。`GeoNodesSideEffectNodes` 的第二个成员就是 `MultiValueMap<std::pair<ComputeContextHash, int32_t>, int> iterations_by_iteration_zone;`（L155）。

`[讲解]` 拆开看这个键值对：

- 键是 `std::pair<ComputeContextHash, int32_t>`。第一个分量是**父上下文的哈希**——这层 zone 是嵌在哪里的；第二个分量是 `int32_t`，也就是 zone 输出节点（Repeat Output / Foreach 的输出）的 `identifier`。注释 L151-L154 写明：

> "The repeat/foreach zone is identified by the compute context of the parent and the identifier of the repeat output node."

`[讲解]` 为什么不用"子上下文哈希"做键？因为子上下文一个迭代一个，那就变成一对一了，多值就没意义了。用**父上下文 + 输出节点 id** 才是"定位到某一个 loop zone"的正确粒度——一个 zone 只有一份身份，它下面挂着 N 轮。

- 值是 `int`，表示**迭代号**（Repeat 里是第几轮，Foreach 里是第几个元素）。注意它是"序号"而不是"节点指针"，因为节点指针已经能通过 `lf_body_nodes_[i]` 拿到（上一篇讲 `VectorSet` 时说过：第 i 次 `add_new` 的节点，下标天然是 i）。

`[讲解]` 写入点在 [`MOD_nodes.cc`](../../../source/blender/modifiers/intern/MOD_nodes.cc) L525-L528：`nodes_by_context.add(parent_compute_context_hash, lf_zone_node);` 之后紧跟 `iterations_by_iteration_zone.add({parent_compute_context_hash, compute_context->output_node_id()}, compute_context->iteration());`。

`[讲解]` 这段代码位于一个**沿 Viewer 路径逐层下钻**的循环里。每个 Viewer 节点都会走一遍，每走一层就把该层的 zone 登记进去。关键点在于：**两个 Viewer 如果都位于同一个 Repeat zone 之内，但分别看第 0 轮和第 1 轮，它们产生的键完全相同**（父上下文哈希相同、输出节点 id 相同），只有值是 0 和 1。

`[讲解]` 此时：

| 容器选择 | 第 0 轮 | 第 1 轮 | 结果 |
| --- | --- | --- | --- |
| `Map<K, int>` | `add(k, 0)` → true | `add(k, 1)` → **false，被丢弃** | 表里只有 0，第 1 轮 Viewer 拿到空数据 |
| `Map<K, int>` + `add_overwrite` | `add_overwrite(k, 0)` | `add_overwrite(k, 1)` → 覆盖 | 表里只有 1，第 0 轮同理丢 |
| **`MultiValueMap<K, int>`** | `add(k, 0)` | `add(k, 1)` → 追加 | 表里是 `[0, 1]`，两轮都算 |

`[讲解]` 中间两行是关键：`Map` 的两条路**都错**，而且错得不一样。`add` 丢后来的，`add_overwrite` 丢先来的。这不是"哪个更好"的取舍问题，而是"这个数据结构根本承载不了一对多"的表达力问题。

`[讲解]` 读取侧则完全对应，`geometry_nodes_repeat_zone.cc` L83-L86 用同一个键 `lookup`，拿回 `Span<int>` 后逐轮取 body 节点。同一个 zone 的多轮副作用就在这一次 `lookup` 里全部回来。

`[讲解]` 再看 `nodes_by_context`。它是 `MultiValueMap<ComputeContextHash, const lf::FunctionNode *>`，**也是多值**，但它的多值性质不同：一个上下文下可能挂多个不同类型的副作用节点（Viewer、Gizmo、Simulation Output、Repeat Zone 节点本身，见 L501/L504、L525、L548、L575、L618、L647），同一个节点也可能被不同 Viewer 路径重复登记（多条路径合并时不去重）。读取侧只关心"某个节点在不在里面"，所以用的是 `lookup(...)` 拿回 `Span` 后一次 `contains`（[`geometry_nodes_lazy_function.cc`](../../../source/blender/nodes/intern/geometry_nodes_lazy_function.cc) L912-L916）：`nodes_with_side_effects.contains(&lf_viewer_node_)`。

`[讲解]` 于是两张表的分工可以用一句话概括：**`nodes_by_context` 是"这个上下文里有哪些节点要算"（集合语义，靠 `Span::contains` 消费），`iterations_by_iteration_zone` 是"这个 loop zone 的哪几轮要算"（编号列表语义，靠 range-for 消费）**。同为 MultiValueMap，前者多值是为了并集合并，后者多值是为了不丢轮次。

## 与 Set 的关系

`[讲解]` 一个自然的疑问：`Map<Key, Value>` 是"键 → 值"，`Set<Key>` 是"只有键"，那 `Set` 是不是 `Map<Key, void>` 的特化？答案是**不是**，两者是**平行实现**。

`[讲解]` 读过 [`BLI_set.hh`](../../../source/blender/blenlib/BLI_set.hh) 就清楚了：它不 include `BLI_map.hh`，也不引用 `Map` 任何符号；`Slot` 来自 `BLI_set_slots.hh` 而不是 `BLI_map_slots.hh`；`InlineBufferCapacity` 的默认值按 `sizeof(Key)` 算，而不是 `sizeof(Key) + sizeof(Value)`。两者甚至私有宏都各写一套（`SET_SLOT_PROBING_BEGIN` vs `MAP_SLOT_PROBING_BEGIN`）。

`[讲解]` 但它们**共享骨架**，逐字段对照几乎一模一样（左 `Map` / 右 `Set`）：`removed_slots_` L140/L122、`occupied_and_removed_slots_` L141/L123、`usable_slots_` L147/L129、`slot_mask_` L153/L135、`hash_` L156/L138、`is_equal_` L159/L141、`max_load_factor_` L163/L145（都是 `LoadFactor(1, 2)`）、`slots_` L172/L154。共享的还有三份公共设施：`BLI_hash_tables.hh`（`LoadFactor`、容量换算这类两边都要用的算术）、`BLI_probing_strategies.hh`（`PythonProbingStrategy` 默认策略）、`BLI_hash.hh`（[`BLI_hash.hh`](../../../source/blender/blenlib/BLI_hash.hh) L236-L257 用五个质数因子混合多个参数）。

`[讲解]` 为什么不做成一份 `Map<Key, void>` 特化？因为那需要一大堆 `if constexpr` 分叉（有没有 value 这块内存、`lookup` 返回什么、`items()` 遍历出什么），把 1383 行变成 2000 多行难读代码；而两份平行实现的重复部分都是十几行的探测循环。这是"复制比抽象便宜"的典型判断，和 `VectorSet` 没有复用 `Map` 是同一个取向。

`[讲解]` 另外注意 `MultiValueMap` 并不依赖 `Set`——"键唯一"由内层 `Map` 天然保证。如果你需要一个"可重复值但键唯一、且值要快速查重"的结构，那才需要 `Map<Key, VectorSet<Value>>` 这种组合，Repeat 里并没有用到。

## 用小数据走一遍

`[讲解]` 向 `MultiValueMap<int, int>` 依次插入 `(key1, 1)`、`(key1, 2)`、`(key2, 5)`，`key1`、`key2` 为任意两个不相等的键。

| 步 | 操作 | 走哪条分支 | `map_` 状态 |
| --- | --- | --- | --- |
| 1 | `add(key1, 1)` | 空槽：回调造空 `Vector<int>`，连键落槽后 `append(1)` | `{ key1 → [1] }` |
| 2 | `add(key1, 2)` | 命中：`return *slot.value()`，**不调回调、不建 Vector**，再 `append(2)` | `{ key1 → [1, 2] }` |
| 3 | `add(key2, 5)` | 空槽：新建空 Vector 后 `append(5)` | `{ key1 → [1, 2], key2 → [5] }` |

**查询结果**：

| 表达式 | 结果 | 说明 |
| --- | --- | --- |
| `lookup(key1).size()` | `2` | 两个值 |
| `lookup(key1)[0]` | `1` | 插入顺序，先来的在前 |
| `lookup(key1)[1]` | `2` | 后追加的在后 |
| `lookup(key2).size()` | `1` | |
| `lookup(key3).size()` | `0` | 不存在 → 默认构造的空 Span，**不崩溃** |
| `lookup(key3).data()` | `nullptr` | 空 Span 的 `data_` 默认值 |
| `size()` | `2` | **键数**，不是值数（值有 3 个） |
| `is_empty()` | `false` | |

`[讲解]` `lookup(key3)` 那一行有官方测试背书（`BLI_multi_value_map_test.cc` L11-L17 的 `LookupNotExistant`）：空表 `lookup(5).size() == 0`，插入 `add(2, 5)` 之后 `lookup(5).size()` 仍然是 `0` —— 缺失键不崩溃、不插入、不制造占位。

`[讲解]` `lookup(key3).data()` 是 `nullptr`：空 Span 的 `data_` 就是默认值，这也解释了为什么 `lookup_as` 里那个 `return {};` 那么干净。

`[讲解]` **`items()` 的遍历顺序**：顺序由两个键在槽数组里的落槽位置决定。`Map` 的槽数组初始只有 1 个槽（[`BLI_map.hh`](../../../source/blender/blenlib/BLI_map.hh) L186-L195 构造函数把 `slot_mask_` 设为 0），第一次插入才真正扩容。所以谁在前取决于哈希值和槽数，**与"先插 key1"无关**。

`[讲解]` 可靠的部分只有一条：**同一键内部的值顺序 = 插入顺序**，`[1, 2]` 永远是 `1` 在前。测试 L19-L32 明确验证了这一点（`lookup(2)[0] == 4`、`lookup(2)[1] == 5`）。跨键顺序不可依赖——这正是"unordered"的应有之义。

`[讲解]` 测试 `LookupMutable`（L34-L53）还演示了**改完值之后必须重新 lookup**：先用 `MutableSpan` 把 `[0]`、`[1]` 改成 10、20，接着 `map.add(4, 5)` 又往同一个键追加（可能触发 Vector 扩容），然后**重新**调一次 `lookup(4)` 才断言结果。注释没写"为什么要重新取"，但代码结构本身就是答案：`add` 可能让 `Vector` 扩容搬迁，旧 `span` 就悬空了。测试作者宁可多写一行 `lookup`，也不去赌 `append` 会不会扩容。

## 反例与边界

### 反例 1：以为 Map 的遍历顺序稳定

`[讲解]` `Map` 的遍历顺序 = 槽数组下标顺序 = 哈希值掩码后的顺序。插入三个键，遍历顺序可能完全不同于插入顺序；而且**加一个新键触发扩容时，所有键的相对顺序都可能改变**（`realloc_and_reinsert` 会重新逐个落槽，L1129-L1148）。需要顺序就用 `Vector` / `VectorSet`（上一篇的主角），或者把键排一次序再遍历。

### 反例 2：以为 `MultiValueMap::lookup` 不存在的键会崩

`[讲解]` 不会，它返回空 `Span`。**但 `Map::lookup` 会**——`BLI_map.hh` L553-L564 里有 `BLI_assert(ptr != nullptr)`。这两个同名接口行为完全不同：

```cpp
Map<int, int> m;
int v = m.lookup(5);              // BLI_assert 失败（Debug 构建直接中断）
int w = m.lookup_default(5, 0);   // 安全，返回 0
int *p = m.lookup_ptr(5);         // 安全，返回 nullptr，但要自己判空

MultiValueMap<int, int> mv;
Span<int> s = mv.lookup(5);       // 安全，s.size() == 0
```

`[讲解]` 记忆口诀：**`Map::lookup` 是"我确信有"，`MultiValueMap::lookup` 是"有就给你，没有给你空"**。

### 反例 3：以为 MultiValueMap 会自动去重

`[讲解]` 头注释第一段就写了"can contain duplicates"，但实际写代码时很容易忘：`mv.add(k, 7)` 调两次，`lookup(k)` 得到的是 `[7, 7]`，不是 `[7]`。要去重得显式用 `add_non_duplicates`（L64-L68），代价是线性查重。反过来，如果业务上**需要**重复（比如"这个值出现了几次"这种计数语义），那么 `add` 保留重复正是特性，用 `add_non_duplicates` 反而错。

### 反例 4：在遍历时插入

`[讲解]` 所有迭代器都有"changes invalidate"的注释（L872-L873、L881-L882、L889-L890、L899-L900、L907-L908）。在 `for (const auto item : map.items())` 循环体里 `add` 一个新键，可能触发扩容、槽数组搬家，正在使用的 `slots_` 指针立即悬空。

`[讲解]` 允许的只有两种改动：一是通过非 const 的 `items()` 改 **value**（键不行）；二是用 `remove(iterator)` 删除**当前**元素（L929-L940 明确说"valid to call this method while iterating"）。其余一律要先把键收集起来再批处理——`MOD_nodes.cc` L650-L655 那段合并代码就是"先完整收集进 `local_`，再整体搬到 `r_`"的两段式写法，规避了同表内遍历时插入。

### 反例 5：把 `size()` 当成值的个数

`[讲解]` `MultiValueMap::size()` 返回 `map_.size()`，即**键的数量**。想要值总数，只能自己遍历 `values()` 把每个 `Span` 的 `size()` 累加起来，没有捷径。

`[讲解]` 而 `is_empty()` 也不完全等价于"没有值"——注释 L127-L130 明说"there may be keys without values"，虽然公开 API 造不出这个状态。

### 反例 6：以为 `lookup` 的 Span 能一直拿着

`[讲解]` Span 就是 `const T *data_ + int64_t size_` 两个字段（`BLI_span.hh` L84-L87），它不持有任何东西。**任何让底层 `Vector` 扩容的操作都会让它悬空**，包括往同一个键 `add`，也包括 `map_` 本身扩容导致整条 `Vector` 对象搬家。写法上就是：`Span<int> s = mv.lookup(k);` 之后 `mv.add(k, 99);` 再读 `s[0]` —— 未定义行为。正确姿势是测试 `LookupMutable` 那样：用完就丢，需要时重新 `lookup`。

### 反例 7：试图对 Map 用 range-for 或 `[]`

`[讲解]` `Map` 没有 `begin()`/`end()`，也没有 `operator[]`——`for (const auto &item : map)` 和 `map[key]` 都是编译错误。前者是设计选择（避免上文那类临时对象生命周期坑），后者是不给"缺失就默认构造"的隐式行为。要用就明确写 `map.items()` / `map.lookup_or_add_default(key)`。

### 反例 8：以为 `lookup_or_add_cb` 的回调随时会跑

`[讲解]` 回调只在**键缺失**时调用，而且是在**键落槽之前**调用（注释 L616-L617）。两个推论：

- 回调里不能 `map.lookup(key)` 反查这个键——那一刻 map 里还没有它；
- 回调里不能修改同一个 map——`lookup_or_add_cb__impl` 正在探测循环当中，插入会改变 `slots_` 布局，属于未定义行为。

`[讲解]` 另一个容易踩的坑是：`lookup_or_add_cb` 的惰性会被误当成"回调只会执行一次"。语义上确实如此（键存在后永远走命中分支），但如果两个线程同时对同一个空 map 调它，回调会被各调一次，而最终只有一个值存活。**`Map` 不是线程安全的**，头注释 L33 只承诺了指针失效规则，没有任何并发承诺。Repeat 里这些表都在建图/收集阶段单线程写入、执行阶段只读，所以安全。

## 对理解 Repeat 的帮助

`[讲解]` 正篇 04-03 那两张表，本篇已经能逐字段解释了。整理成对照：

| 维度 | `nodes_by_context` | `iterations_by_iteration_zone` |
| --- | --- | --- |
| 声明 | L150 | L155 |
| 类型 | `MultiValueMap<ComputeContextHash, const lf::FunctionNode *>` | `MultiValueMap<std::pair<ComputeContextHash, int32_t>, int>` |
| 键的语义 | 单个上下文的哈希 | (父上下文哈希, zone 输出节点 id) |
| 值的语义 | 该上下文下需要求值的 LF 节点 | 需要求值的迭代号 / 元素序号 |
| 多值为何必要 | 一个上下文下有多种副作用节点；多路径合并时要并集 | **同一 zone 的多轮都可能带副作用，一轮都不能丢** |
| 写入点 | `MOD_nodes.cc` L501/L504/L525/L548/L575/L618/L647 | `MOD_nodes.cc` L526-L528（Repeat）、L549-L551（Foreach） |
| 写入方式 | `add(...)` 单条；合并时 `add_multiple(...)` | `add(...)` 单条；合并时 `add_multiple(...)` |
| 读取点 | `geometry_nodes_lazy_function.cc` L913、L927-L928、L1060、L1963 | `geometry_nodes_repeat_zone.cc` L84-L86、`geometry_nodes_foreach_geometry_element_zone.cc` L193-L195 |
| 读取方式 | `Span::contains(node)` 做集合判定 | range-for 逐个迭代号取 `lf_body_nodes_[i]` |

`[讲解]` 为什么"后者必须多值"这件事，用两个 Viewer 的例子讲最透：

- Viewer A 挂在 Repeat zone 内部，迭代 0 时可求值 → 触发 `add({hash, out_id}, 0)`；
- Viewer B 也挂在同一 zone 内部，但需要迭代 1 的数据 → 触发 `add({hash, out_id}, 1)`；
- 两次 `add` 的**键完全一样**（同一个父上下文、同一个输出节点），只有值不同。

`[讲解]` 如果是普通 `Map`，第二次 `add` 返回 `false` 且什么都不改——表里只有 `0`。执行期 `RepeatZoneSideEffectProvider::get_nodes_with_side_effects` 拿到 `[0]`，只把迭代 0 的 body 节点标成"有副作用、必须执行"。迭代 1 的 body 节点被判定为"无副作用"，于是惰性求值直接跳过它——**Viewer B 永远不会收到数据**，界面上表现为"切到某个迭代就空白"。

`[讲解]` 而 `MultiValueMap` 里存的是 `[0, 1]`，provider 的 range-for 跑两遍，两个 body 节点都被标成副作用节点，两轮都会真执行并记录值。**这一个容器类型的选择，直接决定了"多个 Viewer 看不同轮"能不能工作**。

`[讲解]` 还有一层值得体会：`nodes_by_context`（单条 `add` 也够用）和 `iterations_by_iteration_zone`（非多值不可）**用了同一个容器类型**。设计者没有为前者精挑一个 `Map`，而是让两张表统一为 `MultiValueMap`。代价是前者每个值多一层 `Vector` 间接；收益是两张表的合并代码、遍历代码、`add_multiple` 用法完全一致（`MOD_nodes.cc` L650-L655 那两组循环是复制粘贴级的对称）。这是"统一结构优于逐个优化"的取舍——对几十条记录的规模，多一层 `Vector` 的间接寻址完全不值得优化。

`[讲解]` 最后回到本系列的主题：Repeat 的身份机制靠 `VectorSet`（第 i 个插入 = 第 i 轮），Repeat 的副作用登记靠 `MultiValueMap`（第 i 轮不能丢）。前者解决"**我是第几轮**"，后者解决"**第几轮需要算**"。两者都以"插入顺序/多值累积"这种极简机制承载了语义，而不是引入新的自定义类型。

## 继续阅读

- [05-VectorSet稳定索引](05-VectorSet稳定索引.md) —— `lf_body_nodes_[i]` 那个下标的来源，与本篇的"迭代号"配套阅读
- [07-IndexRange与OffsetIndices](07-IndexRange与OffsetIndices.md) —— 下一篇，另一种"连续区间"的零成本视图
- [02-Span只读视图](02-Span只读视图.md) —— 本篇 `lookup` 返回值的类型基础
- [03-Span与MutableSpan](03-Span与MutableSpan.md) —— `lookup` 的 const / 非 const 双重载靠什么区分
- 正篇：[04-03 副作用表与观察者](../../重复区域-dsh/04-运行时机制/03-副作用迭代与按需执行.md) —— `GeoNodesSideEffectNodes` 的完整用法
- 正篇：[03-03 执行图按迭代展开](../../重复区域-dsh/03-几何节点执行架构/03-执行图按迭代展开.md) —— `VectorSet` 建图、`MultiValueMap` 登记两件事同时出现
- 源码：[`BLI_set.hh`](../../../source/blender/blenlib/BLI_set.hh) —— 与 `Map` 同骨架的 Key-only 兄弟，可对照读
- 源码：[`BLI_hash.hh`](../../../source/blender/blenlib/BLI_hash.hh) —— `DefaultHash` 与 `get_default_hash`，理解键为何能直接当 `pair` 用
- 测试：[`BLI_multi_value_map_test.cc`](../../../source/blender/blenlib/tests/BLI_multi_value_map_test.cc) —— 145 行，把本篇所有边界都验了一遍
- 测试：[`BLI_map_test.cc`](../../../source/blender/blenlib/tests/BLI_map_test.cc) —— 头注释提到的基准数据就在这里
