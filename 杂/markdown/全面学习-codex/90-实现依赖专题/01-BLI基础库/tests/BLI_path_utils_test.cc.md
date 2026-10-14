# 实现依赖专题：source/blender/blenlib/tests/BLI_path_utils_test.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["BLI_path_utils_test.cc"]:::abstraction
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
  F["BLI_path_utils_test.cc实现"]:::compute
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

<a id="m-e5db1d122630"></a>

## 宏 `if`

<!-- annotated:1ba18727893996 -->

```cpp
#define AT_INDEX(str_input, index_input, str_expect) \
  { \
    char path[] = str_input; \
    /* Test input assumes forward slash, support back-slash on WIN32. */ \
    if (SEP == '\\') { \
      BLI_string_replace_char(path, '/', '\\'); \
    } \
    const char *expect = str_expect; \
    int index_output, len_output; \
    const bool ret = BLI_path_name_at_index(path, index_input, &index_output, &len_output); \
    if (expect == nullptr) { \
      EXPECT_FALSE(ret); \
    } \
    else { \
      EXPECT_TRUE(ret); \
      EXPECT_EQ(len_output, strlen(expect)); \
      path[index_output + len_output] = '\0'; \
      EXPECT_STREQ(&path[index_output], expect); \
    } \
  } \
  ((void)0)

```

<details>
<summary>核对原始源码：source/blender/blenlib/tests/BLI_path_utils_test.cc · L262—L283</summary>

<!-- original:1ba18727893996:source/blender/blenlib/tests/BLI_path_utils_test.cc:262:283 -->

```cpp
#define AT_INDEX(str_input, index_input, str_expect) \
  { \
    char path[] = str_input; \
    /* Test input assumes forward slash, support back-slash on WIN32. */ \
    if (SEP == '\\') { \
      BLI_string_replace_char(path, '/', '\\'); \
    } \
    const char *expect = str_expect; \
    int index_output, len_output; \
    const bool ret = BLI_path_name_at_index(path, index_input, &index_output, &len_output); \
    if (expect == nullptr) { \
      EXPECT_FALSE(ret); \
    } \
    else { \
      EXPECT_TRUE(ret); \
      EXPECT_EQ(len_output, strlen(expect)); \
      path[index_output + len_output] = '\0'; \
      EXPECT_STREQ(&path[index_output], expect); \
    } \
  } \
  ((void)0)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
