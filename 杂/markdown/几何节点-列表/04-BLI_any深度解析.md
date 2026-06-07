# BLI_any.hh 深度解析

> 源文件：`source/blender/blenlib/BLI_any.hh`

## 一、它是什么？

`blender::Any` 是一个**类型擦除**容器，可以存储**任何可复制构造**的类型。它类似于 `std::any`，但增加了两个关键能力：

| 特性 | `std::any` | `blender::Any` |
|---|---|---|
| 内联缓冲区大小 | 实现定义，不可控 | **可配置** `InlineBufferCapacity` |
| 对齐要求 | 实现定义，不可控 | **可配置** `Alignment` |
| 附加类型信息 | 不支持 | **支持** `ExtraInfo` + `ExtraData` |

```mermaid
graph TB
    subgraph "std::any"
        A1["固定大小内联缓冲区<br/>（实现定义）"]
        A2["类型信息<br/>（仅 RTTI）"]
    end
    subgraph "blender::Any"
        B1["可配置内联缓冲区<br/>InlineBufferCapacity + Alignment"]
        B2["函数指针表<br/>copy/move/destruct/get"]
        B3["ExtraInfo<br/>编译期附加类型信息"]
        B4["ExtraData<br/>利用对齐填充存储运行时数据"]
    end
    style A1 fill:#555,color:#fff
    style A2 fill:#555,color:#fff
    style B1 fill:#4a9,color:#fff
    style B2 fill:#49a,color:#fff
    style B3 fill:#a49,color:#fff
    style B4 fill:#a94,color:#fff
```

---

## 二、模板参数

```cpp
template<
    typename ExtraInfo = void,       // 编译期附加类型信息
    size_t InlineBufferCapacity = 8, // 内联缓冲区字节数
    size_t Alignment = 8,            // 内联缓冲区对齐
    typename ExtraData = blenlib_detail::EmptyType  // 利用对齐填充的运行时数据
>
class Any;
```

```mermaid
graph LR
    subgraph "4 个模板参数"
        EI["ExtraInfo<br/>编译期类型信息<br/>如 AnyExtraData"]
        IBC["InlineBufferCapacity<br/>内联缓冲区大小<br/>默认 8 字节"]
        AL["Alignment<br/>内联缓冲区对齐<br/>默认 8 字节"]
        ED["ExtraData<br/>利用 padding 存储<br/>运行时附加数据"]
    end
    EI --> |"存于 AnyTypeInfo"| VTable["函数指针表<br/>+ extra_info"]
    IBC --> |"决定小对象<br/>是否内联"| Buffer["buffer_"]
    AL --> |"决定对齐要求<br/>和 padding 大小"| Buffer
    ED --> |"存于 padding"| Extra["extra 成员"]
```

### SocketValueVariant 中的使用

```cpp
// BKE_node_socket_value.hh
Any<void, 32, 16, AnyExtraData> value_;
//       ↑   ↑        ↑
//      32B  16B对齐   利用 padding 存 kind + socket_type
```

- `InlineBufferCapacity = 32`：足够内联存储 `int`、`float`、`float3`、`GField` 等
- `Alignment = 16`：满足 SIMD 类型的对齐需求
- `AnyExtraData`：利用对齐产生的 padding 空间存储 `kind` 和 `socket_type`

---

## 三、内存布局

### 3.1 三个核心数据成员

```cpp
class Any {
private:
    AlignedBuffer<RealInlineBufferCapacity, Alignment> buffer_{};  // 内联缓冲区
public:
    BLI_NO_UNIQUE_ADDRESS ExtraData extra = {};  // 利用 padding 的附加数据
private:
    const Info *info_ = nullptr;  // 指向静态函数指针表
};
```

```mermaid
graph TB
    subgraph "Any 对象的内存布局"
        direction TB
        BUF["buffer_<br/>AlignedBuffer<max(InlineBufferCapacity, sizeof(unique_ptr))><br/>─────────────────<br/>小对象：值直接存于此<br/>大对象：存 unique_ptr 指向堆"]
        PAD["extra<br/>BLI_NO_UNIQUE_ADDRESS<br/>─────────────────<br/>利用对齐 padding 存储<br/>如 kind + socket_type"]
        INFO["info_<br/>const Info*<br/>─────────────────<br/>指向静态 AnyTypeInfo 实例<br/>null = 空 Any"]
    end
    BUF --> |"8字节起"| PAD
    PAD --> |"可能 0 字节<br/>(no_unique_address)"| INFO
```

### 3.2 `BLI_NO_UNIQUE_ADDRESS` — 关键优化

```cpp
// BLI_utildefines.h
#if defined(_MSC_VER) && !defined(__clang__)
#  define BLI_NO_UNIQUE_ADDRESS [[msvc::no_unique_address]]
#else
#  define BLI_NO_UNIQUE_ADDRESS [[no_unique_address]]
#endif
```

`[[no_unique_address]]` 是 C++20 属性，允许空类型或具有特定对齐的类型**不占用独立字节**，而是利用前一个成员的 padding 空间。

**实际效果**：`AlignedBuffer<32, 16>` 本身可能有尾部 padding（因为 16 字节对齐），`ExtraData` 就可以"塞进"这些 padding 中，**不增加 `Any` 的总大小**。

```mermaid
graph LR
    subgraph "不用 no_unique_address"
        A1["buffer_: 32B"] --> A2["padding: 0-15B"] --> A3["extra: N B"] --> A4["info_: 8B"]
        A5["总大小可能 > 48B"]
    end
    subgraph "用 no_unique_address"
        B1["buffer_: 32B"] --> B2["extra 藏在 padding 中<br/>0 额外开销"] --> B3["info_: 8B"]
        B4["总大小 = 40B"]
    end
    style A5 fill:#c44,color:#fff
    style B4 fill:#4a9,color:#fff
```

### 3.3 `RealInlineBufferCapacity` 的保底策略

```cpp
static constexpr size_t RealInlineBufferCapacity =
    std::max(InlineBufferCapacity, sizeof(std::unique_ptr<int>));
```

即使你设 `InlineBufferCapacity = 0`，实际缓冲区也至少能容纳一个 `unique_ptr`（8 字节），因为大对象需要在缓冲区中存 `unique_ptr`。

---

## 四、类型擦除机制 — AnyTypeInfo

### 4.1 函数指针表

```cpp
template<typename ExtraInfo>
struct AnyTypeInfo {
    void (*copy_construct)(void *dst, const void *src);  // 复制构造
    void (*move_construct)(void *dst, void *src);        // 移动构造
    void (*destruct)(void *src);                          // 析构
    const void *(*get)(const void *src);                  // 获取值指针
    ExtraInfo extra_info;                                 // 编译期附加信息
};
```

```mermaid
graph TB
    subgraph "AnyTypeInfo — 静态函数指针表"
        CC["copy_construct<br/>复制构造函数指针"]
        MC["move_construct<br/>移动构造函数指针"]
        DT["destruct<br/>析构函数指针"]
        GT["get<br/>获取值指针"]
        EI["extra_info<br/>ExtraInfo::get&lt;T&gt;()"]
    end
    CC --> |"可为 nullptr<br/>= 平凡复制"| TRIVIAL["平凡操作<br/>直接 memcpy"]
    MC --> |"可为 nullptr<br/>= 平凡移动"| TRIVIAL
    DT --> |"可为 nullptr<br/>= 平凡析构"| TRIVIAL
    GT --> |"可为 nullptr<br/>= 内联存储<br/>直接返回 &buffer_"| INLINE["内联：值就在 buffer_ 中"]
    GT --> |"非 nullptr<br/>= 堆存储<br/>解引用 unique_ptr"| HEAP["堆上：buffer_ 存的是 unique_ptr"]
```

### 4.2 两种函数表实例

根据类型大小，`Any` 选择两种存储策略之一，对应两套函数表：

#### 内联存储 — `info_for_inline`

```cpp
template<typename ExtraInfo, typename T>
inline constexpr AnyTypeInfo<ExtraInfo> info_for_inline = {
    // copy_construct: 平凡类型 → nullptr，非平凡 → placement new 拷贝
    is_trivially_copy_constructible_extended_v<T> ?
        nullptr :
        +[](void *dst, const void *src) { new (dst) T(*static_cast<const T *>(src)); },
    // move_construct: 同理
    is_trivially_move_constructible_extended_v<T> ?
        nullptr :
        +[](void *dst, void *src) { new (dst) T(std::move(*static_cast<T *>(src))); },
    // destruct: 平凡析构 → nullptr
    is_trivially_destructible_extended_v<T> ?
        nullptr :
        +[](void *src) { std::destroy_at(static_cast<T *>(src)); },
    // get: 内联存储不需要额外间接，返回 nullptr
    nullptr,
    ExtraInfo::template get<T>()
};
```

#### 堆存储 — `info_for_unique_ptr`

```cpp
template<typename ExtraInfo, typename T>
inline constexpr AnyTypeInfo<ExtraInfo> info_for_unique_ptr = {
    // copy_construct: 深拷贝 — new T(**ptr)
    [](void *dst, const void *src) {
        new (dst) Ptr<T>(new T(**static_cast<const Ptr<T> *>(src)));
    },
    // move_construct: 移动构造新 unique_ptr（注意：这里也做了深拷贝而非移动！）
    [](void *dst, void *src) {
        new (dst) Ptr<T>(new T(std::move(**static_cast<Ptr<T> *>(src))));
    },
    // destruct: 销毁 unique_ptr，自动释放堆内存
    [](void *src) { std::destroy_at(static_cast<Ptr<T> *>(src)); },
    // get: 需要解引用 unique_ptr → 返回 &**ptr
    [](const void *src) -> const void * {
        return &**static_cast<const Ptr<T> *>(src);
    },
    ExtraInfo::template get<T>()
};
```

```mermaid
graph TB
    subgraph "存储策略选择"
        CHECK{"sizeof(T) ≤ InlineBufferCapacity<br/>且 alignof(T) ≤ Alignment<br/>且 is_nothrow_move_constructible?"}
        CHECK -->|"是"| INLINE["info_for_inline<br/>值直接在 buffer_ 中"]
        CHECK -->|"否"| HEAP["info_for_unique_ptr<br/>buffer_ 存 unique_ptr<br/>值在堆上"]
    end

    subgraph "内联存储（如 int, float3）"
        I_BUF["buffer_: [ int 值 ]"]
    end

    subgraph "堆存储（如 std::string, GField）"
        H_BUF["buffer_: [ unique_ptr ──→ ] 堆上的对象"]
    end

    INLINE --> I_BUF
    HEAP --> H_BUF

    style INLINE fill:#4a9,color:#fff
    style HEAP fill:#a94,color:#fff
```

### 4.3 `+[](...)` — Lambda 到函数指针的转换

```cpp
+[](void *dst, const void *src) { new (dst) T(*static_cast<const T *>(src)); }
```

前缀 `+` 是一元加法运算符。无捕获 lambda 可以隐式转换为函数指针，`+` 强制了这个转换。这是为了确保 `info_for_inline` 中的初始化器是**编译期常量**（`inline constexpr`），而不是留下一个未决的 lambda 类型。

### 4.4 `is_trivially_xxx_extended_v` — 扩展的平凡判断

```cpp
// BLI_memory_utils.hh
template<typename T>
inline constexpr bool is_trivially_copy_constructible_extended_v =
    is_trivial_extended_v<T> || std::is_trivially_copy_constructible_v<T>;
```

比标准库多检查了 `is_trivial_v<T>`。某些类型（如某些聚合体）可能不是 `is_trivially_copy_constructible` 但却是 `is_trivial` 的，这个扩展覆盖了更多情况，让函数指针可以为 `nullptr`（即用 `memcpy` 代替）。

---

## 五、类型判断 — `is<T>()` 的巧妙实现

```cpp
template<typename T> bool is() const
{
    return info_ == &this->template get_info<T>();
}
```

**不比较类型名称或 RTTI，而是比较指针地址！** 每个类型 `T` 对应的 `AnyTypeInfo` 是一个 `inline constexpr` 静态变量，地址全局唯一。`info_` 存的就是这个地址，所以直接比指针即可判断类型。

```mermaid
sequenceDiagram
    participant Code as 调用方
    participant Any as Any 对象
    participant VTable as 静态 AnyTypeInfo<int>

    Code->>Any: any.is<int>()
    Any->>Any: get_info<int>()<br/>返回 &info_for_inline<..., int>
    Any->>Any: info_ == &info_for_inline<..., int> ?
    alt 指针相等
        Any-->>Code: true
    else 指针不等
        Any-->>Code: false
    end
```

---

## 六、核心操作流程

### 6.1 构造/赋值 — `emplace_on_empty`

```mermaid
flowchart TD
    START["emplace_on_empty<T>(args...)"] --> ASSERT["BLI_assert(!has_value())"]
    ASSERT --> SET_INFO["info_ = &get_info<DecayT>()"]
    SET_INFO --> CHECK{"is_inline_v<DecayT>?"}
    CHECK -->|"是"| INLINE["new (&buffer_) DecayT(args...)<br/>直接在缓冲区构造"]
    CHECK -->|"否"| HEAP["new (&buffer_) unique_ptr<DecayT>(<br/>  new DecayT(args...))<br/>堆分配 + 缓冲区存指针"]
    INLINE --> RET["返回引用"]
    HEAP --> RET
```

### 6.2 复制构造

```mermaid
flowchart TD
    START["Any(const Any& other)"] --> COPY_EXTRA["复制 extra"]
    COPY_EXTRA --> COPY_INFO["info_ = other.info_"]
    COPY_INFO --> CHECK{"info_ != nullptr?"}
    CHECK -->|"否（空 Any）"| DONE["完成"]
    CHECK -->|"是"| CHECK2{"info_->copy_construct<br/>!= nullptr?"}
    CHECK2 -->|"是（非平凡）"| CALL["info_->copy_construct(&buffer_,<br/>&other.buffer_)"]
    CHECK2 -->|"否（平凡）"| MEMCPY["std::copy_n<br/>memcpy 缓冲区"]
    CALL --> DONE
    MEMCPY --> DONE
```

### 6.3 获取值 — `get<T>()`

```cpp
template<typename T> const T &get() const
{
    BLI_assert(this->is<T>());
    const void *buffer;
    if constexpr (is_inline_v<T>) {
        buffer = &buffer_;           // 内联：直接取缓冲区地址
    } else {
        BLI_assert(info_->get != nullptr);
        buffer = info_->get(&buffer_); // 堆上：解引用 unique_ptr
    }
    return *static_cast<const T *>(buffer);
}
```

注意 `if constexpr` 分支在编译期就确定了，**零运行时开销**。

### 6.4 析构

```mermaid
flowchart TD
    START["~Any()"] --> CHECK{"info_ != nullptr?"}
    CHECK -->|"否"| DONE["完成"]
    CHECK -->|"是"| CHECK2{"info_->destruct<br/>!= nullptr?"}
    CHECK2 -->|"是（非平凡析构）"| CALL["info_->destruct(&buffer_)"]
    CHECK2 -->|"否（平凡析构）"| DONE
    CALL --> DONE
```

---

## 七、`allocate` — 延迟构造

```cpp
template<typename T> void *allocate_on_empty()
{
    BLI_assert(!this->has_value());
    info_ = &this->template get_info<T>();
    if constexpr (is_inline_v<T>) {
        return buffer_.ptr();  // 返回缓冲区原始指针
    } else {
        T *value = static_cast<T *>(::operator new(sizeof(T)));  // 原始堆分配
        new (&buffer_) std::unique_ptr<T>(value);
        return value;
    }
}
```

与 `emplace_on_empty` 不同，`allocate` **只分配内存，不调用构造函数**。调用者负责在返回的指针上 placement new 构造对象。这在性能敏感路径上很有用——可以先分配空间，稍后再构造。

---

## 八、ExtraInfo 机制

### 8.1 设计目的

`ExtraInfo` 允许为每个存储的类型附加编译期信息，嵌入在 `AnyTypeInfo` 中。

### 8.2 接口要求

```cpp
struct MyExtraInfo {
    template<typename T> static constexpr MyExtraInfo get() { return {...}; }
};
```

必须提供静态模板方法 `get<T>()`，返回基于类型 `T` 的附加信息。

### 8.3 SocketValueVariant 的使用

```cpp
struct AnyExtraData {
    Kind kind = Kind::None;                    // Single/Field/Grid/List
    eNodeSocketDatatype socket_type;           // SOCK_INT, SOCK_FLOAT, ...
};
```

这不是 `ExtraInfo`，而是 `ExtraData`（第四个模板参数）。`ExtraInfo` 在这里是 `void`（即 `NoExtraInfo`），而 `ExtraData` 利用 `[[no_unique_address]]` 藏在 padding 中。

```mermaid
graph TB
    subgraph "SocketValueVariant 的 Any"
        BUF["buffer_ (32B, 16B对齐)"]
        ED["extra: AnyExtraData<br/>kind + socket_type<br/>藏在 padding 中，0 额外开销"]
        INFO["info_: 指向 AnyTypeInfo"]
    end
    subgraph "AnyTypeInfo (静态)"
        CC["copy_construct"]
        MC["move_construct"]
        DT["destruct"]
        GT["get"]
        EI["extra_info: NoExtraInfo<br/>(void → 无附加)"]
    end
    INFO --> VTABLE["AnyTypeInfo"]
    ED -.->|"运行时读取"| KIND["kind: Single/Field/Grid/List"]
    ED -.->|"运行时读取"| STYPE["socket_type: SOCK_INT/..."]

    style ED fill:#a94,color:#fff
    style EI fill:#555,color:#fff
```

### 8.4 ExtraInfo vs ExtraData 的区别

| | ExtraInfo | ExtraData |
|---|---|---|
| 模板参数位置 | 第 1 个 | 第 4 个 |
| 存储位置 | 嵌入 `AnyTypeInfo`（静态区） | 嵌入 `Any` 对象本身（栈/堆） |
| 初始化方式 | `ExtraInfo::get<T>()` 编译期 | 运行时赋值 |
| 生命周期 | 永久（静态变量） | 随 `Any` 对象 |
| 访问方式 | `extra_info()` | `extra` 成员 |
| 典型用途 | 类型的编译期属性 | 类型的运行时标签 |

---

## 九、与 `std::any` 的关键差异总结

```mermaid
graph TB
    subgraph "std::any"
        SA1["type_info / RTTI 识别类型"]
        SA2["any_cast<T> 访问<br/>类型不匹配抛 bad_any_cast"]
        SA3["固定内联缓冲区"]
        SA4["无附加信息"]
    end
    subgraph "blender::Any"
        BA1["指针地址比较识别类型<br/>无 RTTI 开销"]
        BA2["is<T>() + get<T>() 访问<br/>类型不匹配 = UB（debug assert）"]
        BA3["可配置内联缓冲区<br/>+ 自动降级为堆分配"]
        BA4["ExtraInfo + ExtraData<br/>零开销附加信息"]
    end
    SA1 -.->|对比| BA1
    SA2 -.->|对比| BA2
    SA3 -.->|对比| BA3
    SA4 -.->|对比| BA4

    style SA1 fill:#555,color:#fff
    style SA2 fill:#555,color:#fff
    style SA3 fill:#555,color:#fff
    style SA4 fill:#555,color:#fff
    style BA1 fill:#4a9,color:#fff
    style BA2 fill:#49a,color:#fff
    style BA3 fill:#a49,color:#fff
    style BA4 fill:#a94,color:#fff
```

---

## 十、赋值运算符的"重建"模式

```cpp
Any &operator=(const Any &other)
{
    if (this == &other) return *this;
    this->~Any();          // 先析构当前值
    new (this) Any(other); // placement new 复制构造
    return *this;
}
```

赋值不是"先析构再构造新值"，而是**先调用析构函数，再在原地址 placement new**。这种模式避免了实现 `assign` 逻辑，复用了拷贝构造函数。所有赋值运算符都采用这种"destroy + reconstruct"模式。

---

## 十一、完整生命周期示例

```cpp
// 1. 构造空 Any
Any<void, 32, 16> a;          // info_ = nullptr, buffer_ 未初始化

// 2. 赋值 int（内联存储）
a = 42;
// → info_ = &info_for_inline<NoExtraInfo, int>
// → buffer_ 中直接存 int(42)

// 3. 赋值 std::string（堆存储）
a = std::string("hello");
// → info_ = &info_for_unique_ptr<NoExtraInfo, std::string>
// → buffer_ 中存 unique_ptr<string> → 堆上的 "hello"

// 4. 类型检查
a.is<int>();           // false
a.is<std::string>();   // true

// 5. 获取值
const std::string &s = a.get<std::string>();  // "hello"

// 6. 析构
// ~Any() → info_->destruct(&buffer_) → destroy_at(unique_ptr) → 释放堆内存
```

```mermaid
sequenceDiagram
    participant User
    participant AnyObj as Any 对象
    participant Buffer as buffer_
    participant Heap as 堆内存
    participant VTable as AnyTypeInfo

    User->>AnyObj: Any a 空对象
    Note over AnyObj: info_ = nullptr

    User->>AnyObj: a = 42
    AnyObj->>VTable: get_info<int>() → &info_for_inline
    AnyObj->>Buffer: new (&buffer_) int(42)
    Note over AnyObj: info_ = &info_for_inline<..., int>

    User->>AnyObj: a = string("hello")
    AnyObj->>AnyObj: ~Any() → 析构 int（平凡，无操作）
    AnyObj->>VTable: get_info<string>() → &info_for_unique_ptr
    AnyObj->>Heap: new string("hello")
    AnyObj->>Buffer: new (&buffer_) unique_ptr(heap_ptr)
    Note over AnyObj: info_ = &info_for_unique_ptr<..., string>

    User->>AnyObj: a.get<string>()
    AnyObj->>Buffer: info_->get(&buffer_) → 解引用 unique_ptr
    Buffer-->>AnyObj: 堆上 string 的地址
    AnyObj-->>User: const string& → "hello"

    User->>AnyObj: ~Any()
    AnyObj->>Buffer: info_->destruct → destroy_at(unique_ptr)
    Buffer->>Heap: unique_ptr 析构 → delete string
```
