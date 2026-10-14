# 实现依赖专题：source/blender/blenkernel/BKE_effect.h

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["BKE_effect.h"]:::abstraction
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
  F["BKE_effect.h实现"]:::compute
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

<a id="m-29f834e20bcb"></a>

## 宏 `BKE_sim_debug_data_add_dot`

<!-- annotated:ae198689f805cc -->

```cpp
#define BKE_sim_debug_data_add_dot(p, r, g, b, category, ...) \
  { \
    const float v2[3] = {0.0f, 0.0f, 0.0f}; \
    BKE_sim_debug_data_add_element( \
        SIM_DEBUG_ELEM_DOT, p, v2, NULL, r, g, b, category, SIM_DEBUG_HASH(__VA_ARGS__)); \
  }

```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_effect.h · L244—L250</summary>

<!-- original:ae198689f805cc:source/blender/blenkernel/BKE_effect.h:244:250 -->

```cpp
#define BKE_sim_debug_data_add_dot(p, r, g, b, category, ...) \
  { \
    const float v2[3] = {0.0f, 0.0f, 0.0f}; \
    BKE_sim_debug_data_add_element( \
        SIM_DEBUG_ELEM_DOT, p, v2, NULL, r, g, b, category, SIM_DEBUG_HASH(__VA_ARGS__)); \
  }

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-1adc53101d3d"></a>

## 宏 `BKE_sim_debug_data_add_circle`

<!-- annotated:5eeabe97a23afb -->

```cpp
#define BKE_sim_debug_data_add_circle(p, radius, r, g, b, category, ...) \
  { \
    const float v2[3] = {radius, 0.0f, 0.0f}; \
    BKE_sim_debug_data_add_element( \
        SIM_DEBUG_ELEM_CIRCLE, p, v2, NULL, r, g, b, category, SIM_DEBUG_HASH(__VA_ARGS__)); \
  }

```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_effect.h · L251—L257</summary>

<!-- original:5eeabe97a23afb:source/blender/blenkernel/BKE_effect.h:251:257 -->

```cpp
#define BKE_sim_debug_data_add_circle(p, radius, r, g, b, category, ...) \
  { \
    const float v2[3] = {radius, 0.0f, 0.0f}; \
    BKE_sim_debug_data_add_element( \
        SIM_DEBUG_ELEM_CIRCLE, p, v2, NULL, r, g, b, category, SIM_DEBUG_HASH(__VA_ARGS__)); \
  }

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-55515c00e176"></a>

## 宏 `BKE_sim_debug_data_add_line`

<!-- annotated:38cfbe7886d5ce -->

```cpp
#define BKE_sim_debug_data_add_line(p1, p2, r, g, b, category, ...) \
  { \
    BKE_sim_debug_data_add_element( \
        SIM_DEBUG_ELEM_LINE, p1, p2, NULL, r, g, b, category, SIM_DEBUG_HASH(__VA_ARGS__)); \
  }

```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_effect.h · L258—L263</summary>

<!-- original:38cfbe7886d5ce:source/blender/blenkernel/BKE_effect.h:258:263 -->

```cpp
#define BKE_sim_debug_data_add_line(p1, p2, r, g, b, category, ...) \
  { \
    BKE_sim_debug_data_add_element( \
        SIM_DEBUG_ELEM_LINE, p1, p2, NULL, r, g, b, category, SIM_DEBUG_HASH(__VA_ARGS__)); \
  }

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-d2afd0808e91"></a>

## 宏 `BKE_sim_debug_data_add_vector`

<!-- annotated:225e5c16f5e1da -->

```cpp
#define BKE_sim_debug_data_add_vector(p, d, r, g, b, category, ...) \
  { \
    BKE_sim_debug_data_add_element( \
        SIM_DEBUG_ELEM_VECTOR, p, d, NULL, r, g, b, category, SIM_DEBUG_HASH(__VA_ARGS__)); \
  }

```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_effect.h · L264—L269</summary>

<!-- original:225e5c16f5e1da:source/blender/blenkernel/BKE_effect.h:264:269 -->

```cpp
#define BKE_sim_debug_data_add_vector(p, d, r, g, b, category, ...) \
  { \
    BKE_sim_debug_data_add_element( \
        SIM_DEBUG_ELEM_VECTOR, p, d, NULL, r, g, b, category, SIM_DEBUG_HASH(__VA_ARGS__)); \
  }

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
