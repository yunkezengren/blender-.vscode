# 实现依赖专题：intern/cycles/kernel/svm/radial_tiling_shared.h

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["radial_tiling_shared.h"]:::abstraction
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
  F["radial_tiling_shared.h实现"]:::compute
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

<a id="m-b0b88656637a"></a>

## 宏 `atanf`

<!-- annotated:76926d894c238f -->

```cpp
#  define atanf math::atan
#  define atan2f math::atan2
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L17—L18</summary>

<!-- original:76926d894c238f:intern/cycles/kernel/svm/radial_tiling_shared.h:17:18 -->

```cpp
#  define atanf math::atan
#  define atan2f math::atan2
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-a77af3382db2"></a>

## 宏 `atan2f`

<!-- annotated:0e73675799dc50 -->

```cpp
#  define atan2f math::atan2
#  define ceilf math::ceil
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L18—L19</summary>

<!-- original:0e73675799dc50:intern/cycles/kernel/svm/radial_tiling_shared.h:18:19 -->

```cpp
#  define atan2f math::atan2
#  define ceilf math::ceil
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-30f54371dd32"></a>

## 宏 `ceilf`

<!-- annotated:eed1dfedade541 -->

```cpp
#  define ceilf math::ceil
#  define cosf math::cos
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L19—L20</summary>

<!-- original:eed1dfedade541:intern/cycles/kernel/svm/radial_tiling_shared.h:19:20 -->

```cpp
#  define ceilf math::ceil
#  define cosf math::cos
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-cee9ebf67d86"></a>

## 宏 `cosf`

<!-- annotated:e9bf0bc84f5c25 -->

```cpp
#  define cosf math::cos
#  define fabsf math::abs
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L20—L21</summary>

<!-- original:e9bf0bc84f5c25:intern/cycles/kernel/svm/radial_tiling_shared.h:20:21 -->

```cpp
#  define cosf math::cos
#  define fabsf math::abs
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-02cc4c69cfb3"></a>

## 宏 `fabsf`

<!-- annotated:f263de12688dbe -->

```cpp
#  define fabsf math::abs
#  define floorf math::floor
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L21—L22</summary>

<!-- original:f263de12688dbe:intern/cycles/kernel/svm/radial_tiling_shared.h:21:22 -->

```cpp
#  define fabsf math::abs
#  define floorf math::floor
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-fb64dda1b0f0"></a>

## 宏 `floorf`

<!-- annotated:1cfbb1f37d282d -->

```cpp
#  define floorf math::floor
#  define fmaxf math::max
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L22—L23</summary>

<!-- original:1cfbb1f37d282d:intern/cycles/kernel/svm/radial_tiling_shared.h:22:23 -->

```cpp
#  define floorf math::floor
#  define fmaxf math::max
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-61cc16a44918"></a>

## 宏 `fractf`

<!-- annotated:2e73aa0d678490 -->

```cpp
#  define fractf math::fract
#  define mix math::interpolate
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L25—L26</summary>

<!-- original:2e73aa0d678490:intern/cycles/kernel/svm/radial_tiling_shared.h:25:26 -->

```cpp
#  define fractf math::fract
#  define mix math::interpolate
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-40547e913688"></a>

## 宏 `sinf`

<!-- annotated:2e1c6aab1d94ce -->

```cpp
#  define sinf math::sin
#  define sqrtf math::sqrt
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L27—L28</summary>

<!-- original:2e1c6aab1d94ce:intern/cycles/kernel/svm/radial_tiling_shared.h:27:28 -->

```cpp
#  define sinf math::sin
#  define sqrtf math::sqrt
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-59a434b9184c"></a>

## 宏 `tanf`

<!-- annotated:5b86016623fdbb -->

```cpp
#  define tanf math::tan

```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L30—L31</summary>

<!-- original:5b86016623fdbb:intern/cycles/kernel/svm/radial_tiling_shared.h:30:31 -->

```cpp
#  define tanf math::tan

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-506bd97c52ec"></a>

## 宏 `atanf`

<!-- annotated:51e4fd17964af5 -->

```cpp
#    define atanf atan
#    define atan2f atan2
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L39—L40</summary>

<!-- original:51e4fd17964af5:intern/cycles/kernel/svm/radial_tiling_shared.h:39:40 -->

```cpp
#    define atanf atan
#    define atan2f atan2
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-cec47b2ce998"></a>

## 宏 `atan2f`

<!-- annotated:355b89b8e5b226 -->

```cpp
#    define atan2f atan2
#    define ceilf ceil
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L40—L41</summary>

<!-- original:355b89b8e5b226:intern/cycles/kernel/svm/radial_tiling_shared.h:40:41 -->

```cpp
#    define atan2f atan2
#    define ceilf ceil
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-227f233ea8b8"></a>

## 宏 `ceilf`

<!-- annotated:2bcde6ca9a943e -->

```cpp
#    define ceilf ceil
#    define cosf cos
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L41—L42</summary>

<!-- original:2bcde6ca9a943e:intern/cycles/kernel/svm/radial_tiling_shared.h:41:42 -->

```cpp
#    define ceilf ceil
#    define cosf cos
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-346533627567"></a>

## 宏 `cosf`

<!-- annotated:017364d7338a89 -->

```cpp
#    define cosf cos
#    define fabsf abs
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L42—L43</summary>

<!-- original:017364d7338a89:intern/cycles/kernel/svm/radial_tiling_shared.h:42:43 -->

```cpp
#    define cosf cos
#    define fabsf abs
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-04effe61803b"></a>

## 宏 `fabsf`

<!-- annotated:08292842efe1fc -->

```cpp
#    define fabsf abs
#    define floorf floor
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L43—L44</summary>

<!-- original:08292842efe1fc:intern/cycles/kernel/svm/radial_tiling_shared.h:43:44 -->

```cpp
#    define fabsf abs
#    define floorf floor
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-25e4a157b53d"></a>

## 宏 `floorf`

<!-- annotated:fabc6ffdcbc17c -->

```cpp
#    define floorf floor
#    define fmaxf max
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L44—L45</summary>

<!-- original:fabc6ffdcbc17c:intern/cycles/kernel/svm/radial_tiling_shared.h:44:45 -->

```cpp
#    define floorf floor
#    define fmaxf max
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-d0a4b7752bc6"></a>

## 宏 `fractf`

<!-- annotated:cc0129ec581887 -->

```cpp
#    define fractf fract
#    define mix mix
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L47—L48</summary>

<!-- original:cc0129ec581887:intern/cycles/kernel/svm/radial_tiling_shared.h:47:48 -->

```cpp
#    define fractf fract
#    define mix mix
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-8908e5f49833"></a>

## 宏 `sinf`

<!-- annotated:03877e13744b05 -->

```cpp
#    define sinf sin
#    define sqrtf sqrt
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L49—L50</summary>

<!-- original:03877e13744b05:intern/cycles/kernel/svm/radial_tiling_shared.h:49:50 -->

```cpp
#    define sinf sin
#    define sqrtf sqrt
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-96d07165eab2"></a>

## 宏 `tanf`

<!-- annotated:8a188985cfe033 -->

```cpp
#    define tanf tan

```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L52—L53</summary>

<!-- original:8a188985cfe033:intern/cycles/kernel/svm/radial_tiling_shared.h:52:53 -->

```cpp
#    define tanf tan

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-f0908e385c5b"></a>

## 宏 `float4`

<!-- annotated:c04532fa290cc3 -->

```cpp
#    define float4 vector4
#    define make_float2 vector2
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L56—L57</summary>

<!-- original:c04532fa290cc3:intern/cycles/kernel/svm/radial_tiling_shared.h:56:57 -->

```cpp
#    define float4 vector4
#    define make_float2 vector2
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-f423567b08e4"></a>

## 宏 `atanf`

<!-- annotated:7556371546f250 -->

```cpp
#      define atanf atan
#      define atan2f atan2
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L70—L71</summary>

<!-- original:7556371546f250:intern/cycles/kernel/svm/radial_tiling_shared.h:70:71 -->

```cpp
#      define atanf atan
#      define atan2f atan2
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-bd31b1779092"></a>

## 宏 `atan2f`

<!-- annotated:2ce9d4ca46f940 -->

```cpp
#      define atan2f atan2
#      define ceilf ceil
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L71—L72</summary>

<!-- original:2ce9d4ca46f940:intern/cycles/kernel/svm/radial_tiling_shared.h:71:72 -->

```cpp
#      define atan2f atan2
#      define ceilf ceil
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-093dc1c96d76"></a>

## 宏 `ceilf`

<!-- annotated:bb4b92542669cd -->

```cpp
#      define ceilf ceil
#      define cosf cos
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L72—L73</summary>

<!-- original:bb4b92542669cd:intern/cycles/kernel/svm/radial_tiling_shared.h:72:73 -->

```cpp
#      define ceilf ceil
#      define cosf cos
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-e01b94a43b72"></a>

## 宏 `cosf`

<!-- annotated:f5e6e12a8cd7cb -->

```cpp
#      define cosf cos
#      define fabsf abs
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L73—L74</summary>

<!-- original:f5e6e12a8cd7cb:intern/cycles/kernel/svm/radial_tiling_shared.h:73:74 -->

```cpp
#      define cosf cos
#      define fabsf abs
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-927dd4eba7dc"></a>

## 宏 `fabsf`

<!-- annotated:8de6e7612992c8 -->

```cpp
#      define fabsf abs
#      define floorf floor
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L74—L75</summary>

<!-- original:8de6e7612992c8:intern/cycles/kernel/svm/radial_tiling_shared.h:74:75 -->

```cpp
#      define fabsf abs
#      define floorf floor
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-e128f662cbe8"></a>

## 宏 `floorf`

<!-- annotated:bc51d233277f27 -->

```cpp
#      define floorf floor
#      define fmaxf max
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L75—L76</summary>

<!-- original:bc51d233277f27:intern/cycles/kernel/svm/radial_tiling_shared.h:75:76 -->

```cpp
#      define floorf floor
#      define fmaxf max
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-e5a05aae8fbc"></a>

## 宏 `fractf`

<!-- annotated:26203e07107fd5 -->

```cpp
#      define fractf fract
#      define mix mix
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L78—L79</summary>

<!-- original:26203e07107fd5:intern/cycles/kernel/svm/radial_tiling_shared.h:78:79 -->

```cpp
#      define fractf fract
#      define mix mix
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-71130f6adcc4"></a>

## 宏 `sinf`

<!-- annotated:7cf304a9c153c6 -->

```cpp
#      define sinf sin
#      define sqrtf sqrt
```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L80—L81</summary>

<!-- original:7cf304a9c153c6:intern/cycles/kernel/svm/radial_tiling_shared.h:80:81 -->

```cpp
#      define sinf sin
#      define sqrtf sqrt
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-7663637581d9"></a>

## 宏 `tanf`

<!-- annotated:0a4a2db5f497da -->

```cpp
#      define tanf tan

```

<details>
<summary>核对原始源码：intern/cycles/kernel/svm/radial_tiling_shared.h · L83—L84</summary>

<!-- original:0a4a2db5f497da:intern/cycles/kernel/svm/radial_tiling_shared.h:83:84 -->

```cpp
#      define tanf tan

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
