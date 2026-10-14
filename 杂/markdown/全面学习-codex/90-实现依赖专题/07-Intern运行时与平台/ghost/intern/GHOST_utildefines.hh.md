# 实现依赖专题：intern/ghost/intern/GHOST_utildefines.hh

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["ARRAY_SIZE"]:::abstraction
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
  F["GHOST_utildefines.hh实现"]:::compute
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

<a id="m-00ad768fe1c1"></a>

## 宏 `UNPACK2`

<!-- annotated:3d260ec43de40b -->

```cpp
#define UNPACK2(a) ((a)[0]), ((a)[1])
#define UNPACK3(a) UNPACK2(a), ((a)[2])
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L22—L23</summary>

<!-- original:3d260ec43de40b:intern/ghost/intern/GHOST_utildefines.hh:22:23 -->

```cpp
#define UNPACK2(a) ((a)[0]), ((a)[1])
#define UNPACK3(a) UNPACK2(a), ((a)[2])
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-f882324eb80a"></a>

## 宏 `UNPACK3`

<!-- annotated:203beed511bf15 -->

```cpp
#define UNPACK3(a) UNPACK2(a), ((a)[2])
#define UNPACK4(a) UNPACK3(a), ((a)[3])
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L23—L24</summary>

<!-- original:203beed511bf15:intern/ghost/intern/GHOST_utildefines.hh:23:24 -->

```cpp
#define UNPACK3(a) UNPACK2(a), ((a)[2])
#define UNPACK4(a) UNPACK3(a), ((a)[3])
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-b619f32aee40"></a>

## 宏 `UNPACK4`

<!-- annotated:d38f7e72543f97 -->

```cpp
#define UNPACK4(a) UNPACK3(a), ((a)[3])
/* pre may be '&', '*' or func, post may be '->member' */
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L24—L25</summary>

<!-- original:d38f7e72543f97:intern/ghost/intern/GHOST_utildefines.hh:24:25 -->

```cpp
#define UNPACK4(a) UNPACK3(a), ((a)[3])
/* pre may be '&', '*' or func, post may be '->member' */
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-dc91e463eff3"></a>

## 宏 `UNPACK3_EX`

<!-- annotated:4bf66c4f22aadb -->

```cpp
#define UNPACK3_EX(pre, a, post) UNPACK2_EX(pre, a, post), (pre((a)[2]) post)
#define UNPACK4_EX(pre, a, post) UNPACK3_EX(pre, a, post), (pre((a)[3]) post)
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L27—L28</summary>

<!-- original:4bf66c4f22aadb:intern/ghost/intern/GHOST_utildefines.hh:27:28 -->

```cpp
#define UNPACK3_EX(pre, a, post) UNPACK2_EX(pre, a, post), (pre((a)[2]) post)
#define UNPACK4_EX(pre, a, post) UNPACK3_EX(pre, a, post), (pre((a)[3]) post)
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-c7ddd34a8d19"></a>

## 宏 `UNPACK4_EX`

<!-- annotated:bb8cdd16511ac3 -->

```cpp
#define UNPACK4_EX(pre, a, post) UNPACK3_EX(pre, a, post), (pre((a)[3]) post)

```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L28—L29</summary>

<!-- original:bb8cdd16511ac3:intern/ghost/intern/GHOST_utildefines.hh:28:29 -->

```cpp
#define UNPACK4_EX(pre, a, post) UNPACK3_EX(pre, a, post), (pre((a)[3]) post)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-d28724a15928"></a>

## 宏 `ELEM`

<!-- annotated:2c498e007086d8 -->

```cpp
#define ELEM(...) VA_NARGS_CALL_OVERLOAD(_VA_ELEM, __VA_ARGS__)

```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L88—L89</summary>

<!-- original:2c498e007086d8:intern/ghost/intern/GHOST_utildefines.hh:88:89 -->

```cpp
#define ELEM(...) VA_NARGS_CALL_OVERLOAD(_VA_ELEM, __VA_ARGS__)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-9549fb6aafd2"></a>

## 宏 `STREQ`

<!-- annotated:7dca058a654bf2 -->

```cpp
#define STREQ(a, b) (strcmp(a, b) == 0)
#define STRCASEEQ(a, b) (strcasecmp(a, b) == 0)
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L112—L113</summary>

<!-- original:7dca058a654bf2:intern/ghost/intern/GHOST_utildefines.hh:112:113 -->

```cpp
#define STREQ(a, b) (strcmp(a, b) == 0)
#define STRCASEEQ(a, b) (strcasecmp(a, b) == 0)
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-4c9fb75cc1d1"></a>

## 宏 `STREQLEN`

<!-- annotated:06240f436c5a09 -->

```cpp
#define STREQLEN(a, b, n) (strncmp(a, b, n) == 0)
#define STRCASEEQLEN(a, b, n) (strncasecmp(a, b, n) == 0)
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L114—L115</summary>

<!-- original:06240f436c5a09:intern/ghost/intern/GHOST_utildefines.hh:114:115 -->

```cpp
#define STREQLEN(a, b, n) (strncmp(a, b, n) == 0)
#define STRCASEEQLEN(a, b, n) (strncasecmp(a, b, n) == 0)
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-f15302dd736a"></a>

## 宏 `STRPREFIX`

<!-- annotated:d68b2adc75e00b -->

```cpp
#define STRPREFIX(a, b) (strncmp((a), (b), strlen(b)) == 0)

```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L117—L118</summary>

<!-- original:d68b2adc75e00b:intern/ghost/intern/GHOST_utildefines.hh:117:118 -->

```cpp
#define STRPREFIX(a, b) (strncmp((a), (b), strlen(b)) == 0)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现

<a id="f-60392d045ee4c602"></a>

### `ARRAY_SIZE`

实现位置：[intern/ghost/intern/GHOST_utildefines.hh](../../../../../../../../intern/ghost/intern/GHOST_utildefines.hh) · L37—L41。

接口参数：

- `const T (&arg)[N]`

**教学注释版**

<!-- annotated:9c1b91423bc1bf -->

```cpp
template<class T, size_t N> constexpr size_t ARRAY_SIZE(const T (&arg)[N]) noexcept
{
  (void)arg;
  return N;
}
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_utildefines.hh · L37—L41</summary>

<!-- original:9c1b91423bc1bf:intern/ghost/intern/GHOST_utildefines.hh:37:41 -->

```cpp
template<class T, size_t N> constexpr size_t ARRAY_SIZE(const T (&arg)[N]) noexcept
{
  (void)arg;
  return N;
}
```

</details>

**结果出口**

- `return N;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
