# 实现依赖专题：source/blender/blenlib/BLI_linklist_stack.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["BLI_linklist_stack.hh"]:::abstraction
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  C["调用者提供参数与有效对象"]:::input
  F["BLI_linklist_stack.hh实现"]:::compute
  R["结果与被修改状态"]:::result
  C -->|"进入"| F
  F -->|"返回或提交"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  T["具体类型与模板实参"]:::abstraction
  B["分支与构建条件"]:::data
  I["匹配的实现"]:::compute
  E["标准库或系统契约边界"]:::result
  T -->|"静态选择"| I
  B -->|"配置选择"| I
  I -->|"到达外部接口"| E
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  S["完整源码单元"]:::input
  A["教学注释与推导"]:::abstraction
  D["被调用实现专题"]:::compute
  V["原文与token一致性检查"]:::result
  S -->|"就近阅读"| A
  A -->|"继续深入"| D
  A -->|"核对"| V
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

<a id="m-b02508c85647"></a>

## 宏 `BLI_LINKSTACK_INIT`

<!-- annotated:74756488a61990 -->

```cpp
#define BLI_LINKSTACK_INIT(var) \
  { \
    var = NULL; \
    var##_pool_ = BLI_mempool_create(sizeof(LinkNode), 0, 64, BLI_MEMPOOL_NOP); \
  } \
  (void)0

```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L30—L36</summary>

<!-- original:74756488a61990:source/blender/blenlib/BLI_linklist_stack.hh:30:36 -->

```cpp
#define BLI_LINKSTACK_INIT(var) \
  { \
    var = NULL; \
    var##_pool_ = BLI_mempool_create(sizeof(LinkNode), 0, 64, BLI_MEMPOOL_NOP); \
  } \
  (void)0

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-9a309cb83e46"></a>

## 宏 `BLI_LINKSTACK_PUSH`

<!-- annotated:52f85f47a521f5 -->

```cpp
#define BLI_LINKSTACK_PUSH(var, ptr) \
  (CHECK_TYPE_INLINE_NONCONST(ptr, decltype(var##_type_)), \
   BLI_linklist_prepend_pool(&(var), ptr, var##_pool_))
#define BLI_LINKSTACK_POP(var) \
```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L40—L43</summary>

<!-- original:52f85f47a521f5:source/blender/blenlib/BLI_linklist_stack.hh:40:43 -->

```cpp
#define BLI_LINKSTACK_PUSH(var, ptr) \
  (CHECK_TYPE_INLINE_NONCONST(ptr, decltype(var##_type_)), \
   BLI_linklist_prepend_pool(&(var), ptr, var##_pool_))
#define BLI_LINKSTACK_POP(var) \
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-87d1552fe96d"></a>

## 宏 `BLI_LINKSTACK_POP`

<!-- annotated:4ba22991855f2b -->

```cpp
#define BLI_LINKSTACK_POP(var) \
  (decltype(var##_type_))(var ? BLI_linklist_pop_pool(&(var), var##_pool_) : NULL)
#define BLI_LINKSTACK_POP_DEFAULT(var, r) \
```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L43—L45</summary>

<!-- original:4ba22991855f2b:source/blender/blenlib/BLI_linklist_stack.hh:43:45 -->

```cpp
#define BLI_LINKSTACK_POP(var) \
  (decltype(var##_type_))(var ? BLI_linklist_pop_pool(&(var), var##_pool_) : NULL)
#define BLI_LINKSTACK_POP_DEFAULT(var, r) \
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-1e4884061ace"></a>

## 宏 `BLI_LINKSTACK_FREE`

<!-- annotated:f403f823adcfbf -->

```cpp
#define BLI_LINKSTACK_FREE(var) \
  { \
    BLI_mempool_destroy(var##_pool_); \
    var##_pool_ = NULL; \
    (void)var##_pool_; \
    var = NULL; \
    (void)var; \
    (void)&(var##_type_); \
  } \
  (void)0

```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L56—L66</summary>

<!-- original:f403f823adcfbf:source/blender/blenlib/BLI_linklist_stack.hh:56:66 -->

```cpp
#define BLI_LINKSTACK_FREE(var) \
  { \
    BLI_mempool_destroy(var##_pool_); \
    var##_pool_ = NULL; \
    (void)var##_pool_; \
    var = NULL; \
    (void)var; \
    (void)&(var##_type_); \
  } \
  (void)0

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-f6feea21b839"></a>

## 宏 `BLI_SMALLSTACK_PUSH`

<!-- annotated:7652e43ab1ed39 -->

```cpp
#define BLI_SMALLSTACK_PUSH(var, data) \
  { \
    CHECK_TYPE_PAIR(data, _##var##_type); \
    if (_##var##_free) { \
      _##var##_temp = _##var##_free; \
      _##var##_free = _##var##_free->next; \
    } \
    else { \
      _##var##_temp = (LinkNode *)alloca(sizeof(LinkNode)); \
    } \
    _##var##_temp->next = _##var##_stack; \
    _##var##_temp->link = data; \
    _##var##_stack = _##var##_temp; \
    _BLI_SMALLSTACK_FAKEUSER(var); \
  } \
  (void)0

```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L93—L109</summary>

<!-- original:7652e43ab1ed39:source/blender/blenlib/BLI_linklist_stack.hh:93:109 -->

```cpp
#define BLI_SMALLSTACK_PUSH(var, data) \
  { \
    CHECK_TYPE_PAIR(data, _##var##_type); \
    if (_##var##_free) { \
      _##var##_temp = _##var##_free; \
      _##var##_free = _##var##_free->next; \
    } \
    else { \
      _##var##_temp = (LinkNode *)alloca(sizeof(LinkNode)); \
    } \
    _##var##_temp->next = _##var##_stack; \
    _##var##_temp->link = data; \
    _##var##_stack = _##var##_temp; \
    _BLI_SMALLSTACK_FAKEUSER(var); \
  } \
  (void)0

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-de9dbbe51aef"></a>

## 宏 `BLI_SMALLSTACK_POP`

<!-- annotated:6f4d59660bd05e -->

```cpp
#define BLI_SMALLSTACK_POP(var) \
  (_BLI_SMALLSTACK_CAST(var)( \
      (_##var##_stack) ? (_BLI_SMALLSTACK_DEL(var), (_##var##_free->link)) : NULL))

```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L122—L125</summary>

<!-- original:6f4d59660bd05e:source/blender/blenlib/BLI_linklist_stack.hh:122:125 -->

```cpp
#define BLI_SMALLSTACK_POP(var) \
  (_BLI_SMALLSTACK_CAST(var)( \
      (_##var##_stack) ? (_BLI_SMALLSTACK_DEL(var), (_##var##_free->link)) : NULL))

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-884d63d7718b"></a>

## 宏 `BLI_SMALLSTACK_POP_EX`

<!-- annotated:744f4f22f501a7 -->

```cpp
#define BLI_SMALLSTACK_POP_EX(var_src, var_dst) \
  (_BLI_SMALLSTACK_CAST(var_src)( \
      (_##var_src##_stack) ? \
          (_BLI_SMALLSTACK_DEL_EX(var_src, var_dst), (_##var_dst##_free->link)) : \
          NULL))

```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L127—L132</summary>

<!-- original:744f4f22f501a7:source/blender/blenlib/BLI_linklist_stack.hh:127:132 -->

```cpp
#define BLI_SMALLSTACK_POP_EX(var_src, var_dst) \
  (_BLI_SMALLSTACK_CAST(var_src)( \
      (_##var_src##_stack) ? \
          (_BLI_SMALLSTACK_DEL_EX(var_src, var_dst), (_##var_dst##_free->link)) : \
          NULL))

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-35bfee506840"></a>

## 宏 `BLI_SMALLSTACK_IS_EMPTY`

<!-- annotated:24d829e3d5ffbb -->

```cpp
#define BLI_SMALLSTACK_IS_EMPTY(var) ((_BLI_SMALLSTACK_CAST(var) _##var##_stack) == NULL)

```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L136—L137</summary>

<!-- original:24d829e3d5ffbb:source/blender/blenlib/BLI_linklist_stack.hh:136:137 -->

```cpp
#define BLI_SMALLSTACK_IS_EMPTY(var) ((_BLI_SMALLSTACK_CAST(var) _##var##_stack) == NULL)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-618917001ef5"></a>

## 宏 `BLI_SMALLSTACK_AS_TABLE`

<!-- annotated:63f0a76f33926e -->

```cpp
#define BLI_SMALLSTACK_AS_TABLE(var, data) \
  { \
    LinkNode *_##var##_iter; \
    unsigned int i; \
    for (_##var##_iter = _##var##_stack, i = 0; _##var##_iter; \
         _##var##_iter = _##var##_iter->next, i++) \
    { \
      *(void **)&(data)[i] = _##var##_iter->link; \
    } \
  } \
  ((void)0)

```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L139—L150</summary>

<!-- original:63f0a76f33926e:source/blender/blenlib/BLI_linklist_stack.hh:139:150 -->

```cpp
#define BLI_SMALLSTACK_AS_TABLE(var, data) \
  { \
    LinkNode *_##var##_iter; \
    unsigned int i; \
    for (_##var##_iter = _##var##_stack, i = 0; _##var##_iter; \
         _##var##_iter = _##var##_iter->next, i++) \
    { \
      *(void **)&(data)[i] = _##var##_iter->link; \
    } \
  } \
  ((void)0)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-5062ab6dd6a0"></a>

## 宏 `BLI_SMALLSTACK_SWAP`

<!-- annotated:3c9f8c14a74d9b -->

```cpp
#define BLI_SMALLSTACK_SWAP(var_a, var_b) \
  { \
    CHECK_TYPE_PAIR(_##var_a##_type, _##var_b##_type); \
    SWAP(LinkNode *, _##var_a##_stack, _##var_b##_stack); \
    SWAP(LinkNode *, _##var_a##_free, _##var_b##_free); \
  } \
  (void)0

```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_linklist_stack.hh · L163—L170</summary>

<!-- original:3c9f8c14a74d9b:source/blender/blenlib/BLI_linklist_stack.hh:163:170 -->

```cpp
#define BLI_SMALLSTACK_SWAP(var_a, var_b) \
  { \
    CHECK_TYPE_PAIR(_##var_a##_type, _##var_b##_type); \
    SWAP(LinkNode *, _##var_a##_stack, _##var_b##_stack); \
    SWAP(LinkNode *, _##var_a##_free, _##var_b##_free); \
  } \
  (void)0

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
