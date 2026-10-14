# 实现依赖专题：intern/cycles/subd/patch.cpp

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["decasteljau_cubic"]:::abstraction
  F1["decasteljau_bicubic"]:::compute
  F2["LinearQuadPatch::eval"]:::compute
  F3["BicubicPatch::eval"]:::compute
  F1 -->|"显式调用"| F0
  F3 -->|"显式调用"| F1
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
  F["patch.cpp实现"]:::compute
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

## 完整成员与函数实现

<a id="f-236b6c11fb417d76"></a>

### `decasteljau_cubic`

实现位置：[intern/cycles/subd/patch.cpp](../../../../../intern/cycles/subd/patch.cpp) · L12—L29。

接口参数：

- `float3 *P`
- `float3 *dt`
- `const float t`
- `const float3 cp[4]`

**教学注释版**

<!-- annotated:f1c2aafe8daf93 -->

```cpp
CCL_NAMESPACE_BEGIN

/* De Casteljau Evaluation */

static void decasteljau_cubic(float3 *P, float3 *dt, const float t, const float3 cp[4])
{
  float3 d0 = cp[0] + t * (cp[1] - cp[0]);
  float3 d1 = cp[1] + t * (cp[2] - cp[1]);
  const float3 d2 = cp[2] + t * (cp[3] - cp[2]);

  d0 += t * (d1 - d0);
  d1 += t * (d2 - d1);

  *P = d0 + t * (d1 - d0);
  if (dt) {
    *dt = d1 - d0;
  }
}
```

<details>
<summary>核对原始源码：intern/cycles/subd/patch.cpp · L12—L29</summary>

<!-- original:f1c2aafe8daf93:intern/cycles/subd/patch.cpp:12:29 -->

```cpp
CCL_NAMESPACE_BEGIN

/* De Casteljau Evaluation */

static void decasteljau_cubic(float3 *P, float3 *dt, const float t, const float3 cp[4])
{
  float3 d0 = cp[0] + t * (cp[1] - cp[0]);
  float3 d1 = cp[1] + t * (cp[2] - cp[1]);
  const float3 d2 = cp[2] + t * (cp[3] - cp[2]);

  d0 += t * (d1 - d0);
  d1 += t * (d2 - d1);

  *P = d0 + t * (d1 - d0);
  if (dt) {
    *dt = d1 - d0;
  }
}
```

</details>

**沿实际写入检查状态**

- `d0 += t * (d1 - d0);`
- `d1 += t * (d2 - d1);`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-4f1ed62206d967ca"></a>

### `decasteljau_bicubic`

实现位置：[intern/cycles/subd/patch.cpp](../../../../../intern/cycles/subd/patch.cpp) · L31—L48。

接口参数：

- `float3 *P`
- `float3 *du`
- `float3 *dv`
- `const float3 cp[16]`
- `float u`
- `const float v`

**教学注释版**

<!-- annotated:84b59e78cecc21 -->

```cpp
static void decasteljau_bicubic(
    float3 *P, float3 *du, float3 *dv, const float3 cp[16], float u, const float v)
{
  float3 ucp[4];
  float3 utn[4];

  /* interpolate over u */
  decasteljau_cubic(ucp + 0, utn + 0, u, cp);
  decasteljau_cubic(ucp + 1, utn + 1, u, cp + 4);
  decasteljau_cubic(ucp + 2, utn + 2, u, cp + 8);
  decasteljau_cubic(ucp + 3, utn + 3, u, cp + 12);

  /* interpolate over v */
  decasteljau_cubic(P, dv, v, ucp);
  if (du) {
    decasteljau_cubic(du, nullptr, v, utn);
  }
}
```

<details>
<summary>核对原始源码：intern/cycles/subd/patch.cpp · L31—L48</summary>

<!-- original:84b59e78cecc21:intern/cycles/subd/patch.cpp:31:48 -->

```cpp
static void decasteljau_bicubic(
    float3 *P, float3 *du, float3 *dv, const float3 cp[16], float u, const float v)
{
  float3 ucp[4];
  float3 utn[4];

  /* interpolate over u */
  decasteljau_cubic(ucp + 0, utn + 0, u, cp);
  decasteljau_cubic(ucp + 1, utn + 1, u, cp + 4);
  decasteljau_cubic(ucp + 2, utn + 2, u, cp + 8);
  decasteljau_cubic(ucp + 3, utn + 3, u, cp + 12);

  /* interpolate over v */
  decasteljau_cubic(P, dv, v, ucp);
  if (du) {
    decasteljau_cubic(du, nullptr, v, utn);
  }
}
```

</details>

**继续追踪实现**

- `decasteljau_cubic` → [decasteljau_cubic · L12](%E4%BE%9D%E8%B5%96-patch-26f041.md#f-236b6c11fb417d76)。

<a id="f-79ab1e763912b04a"></a>

### `LinearQuadPatch::eval`

实现位置：[intern/cycles/subd/patch.cpp](../../../../../intern/cycles/subd/patch.cpp) · L52—L73。

接口参数：

- `float3 *P`
- `float3 *dPdu`
- `float3 *dPdv`
- `float3 *N`
- `const float u`
- `float v`

**教学注释版**

<!-- annotated:cb89fa17925167 -->

```cpp
void LinearQuadPatch::eval(
    float3 *P, float3 *dPdu, float3 *dPdv, float3 *N, const float u, float v) const
{
  const float3 d0 = interp(hull[0], hull[1], u);
  const float3 d1 = interp(hull[2], hull[3], u);

  *P = interp(d0, d1, v);

  if (N || (dPdu && dPdv)) {
    const float3 dPdu_ = interp(hull[1] - hull[0], hull[3] - hull[2], v);
    const float3 dPdv_ = interp(hull[2] - hull[0], hull[3] - hull[1], u);

    if (dPdu && dPdv) {
      *dPdu = dPdu_;
      *dPdv = dPdv_;
    }

    if (N) {
      *N = normalize(cross(dPdu_, dPdv_));
    }
  }
}
```

<details>
<summary>核对原始源码：intern/cycles/subd/patch.cpp · L52—L73</summary>

<!-- original:cb89fa17925167:intern/cycles/subd/patch.cpp:52:73 -->

```cpp
void LinearQuadPatch::eval(
    float3 *P, float3 *dPdu, float3 *dPdv, float3 *N, const float u, float v) const
{
  const float3 d0 = interp(hull[0], hull[1], u);
  const float3 d1 = interp(hull[2], hull[3], u);

  *P = interp(d0, d1, v);

  if (N || (dPdu && dPdv)) {
    const float3 dPdu_ = interp(hull[1] - hull[0], hull[3] - hull[2], v);
    const float3 dPdv_ = interp(hull[2] - hull[0], hull[3] - hull[1], u);

    if (dPdu && dPdv) {
      *dPdu = dPdu_;
      *dPdv = dPdv_;
    }

    if (N) {
      *N = normalize(cross(dPdu_, dPdv_));
    }
  }
}
```

</details>

**继续追踪实现**

- `interp` → [interp · L638](%E4%BE%9D%E8%B5%96-math_float4-2d91ea.md#f-8f39108ecb93668d)；[interp · L557](%E4%BE%9D%E8%B5%96-math_float3-eb3e6f.md#f-819a62b72e3bc6a1)；[interp · L246](%E4%BE%9D%E8%B5%96-math_float2-be3c03.md#f-4b938685df05b6fa)；[interp · L549](%E4%BE%9D%E8%B5%96-math_base-b01ba9.md#f-c4d2373616f78322)。同名重载需按实参类型选择。
- `normalize` → [normalize · L109](%E4%BE%9D%E8%B5%96-IK_Math-614efe.md#f-1a1c851a5bd44fba)；[normalize · L77](%E4%BE%9D%E8%B5%96-Projections-91a559.md#f-15577af6ac05b036)；[normalize · L460](%E4%BE%9D%E8%B5%96-math_float4-2d91ea.md#f-25d06efa592ab5f5)；[normalize · L332](%E4%BE%9D%E8%B5%96-math_float3-eb3e6f.md#f-baa4b4b062d3b43f)；[normalize · L205](%E4%BE%9D%E8%B5%96-math_float2-be3c03.md#f-2a4866a4240a6727)；[normalize · L308](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-e2039e1856df8255)；[normalize · L16](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-c7ae20a29ab4da76)；[normalize · L20](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-058e4a05bbb6b503)；[normalize · L24](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-14dbdba2c67d0e8b)；[normalize · L34](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-625d4bad43dffd9c)；[normalize · L41](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-d55b4ac328dde4cb)；[normalize · L48](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-8a8b0bd437b339c5)；[normalize · L55](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-64d092bea6e62c87)；[normalize · L64](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-5e2d66321c5b1c64)；[normalize · L73](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-678c05ab6e94ffc2)；[normalize · L81](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-693795be99ff0d63)；[normalize · L90](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-e7110cf1e4527133)；[normalize · L100](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-c074535e46937142)。同名重载需按实参类型选择。
- `cross` → [cross · L436](%E4%BE%9D%E8%B5%96-math_float4-2d91ea.md#f-47c1848f44fe4b56)；[cross · L319](%E4%BE%9D%E8%B5%96-math_float3-eb3e6f.md#f-a89959ab21db0804)；[cross · L200](%E4%BE%9D%E8%B5%96-math_float2-be3c03.md#f-d4cf827d2d4b9025)；[cross · L284](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-8c812fdff783548f)；[cross · L291](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-fb4619a5864c3edc)；[cross · L296](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-d9964e9b2e1f70ab)。同名重载需按实参类型选择。

<a id="f-66a2b15808c8c4d1"></a>

### `BicubicPatch::eval`

实现位置：[intern/cycles/subd/patch.cpp](../../../../../intern/cycles/subd/patch.cpp) · L88—L106。

接口参数：

- `float3 *P`
- `float3 *dPdu`
- `float3 *dPdv`
- `float3 *N`
- `const float u`
- `const float v`

**教学注释版**

<!-- annotated:33ea2c38ea3b42 -->

```cpp
void BicubicPatch::eval(
    float3 *P, float3 *dPdu, float3 *dPdv, float3 *N, const float u, const float v) const
{
  if (N) {
    float3 dPdu_;
    float3 dPdv_;
    decasteljau_bicubic(P, &dPdu_, &dPdv_, hull, u, v);

    if (dPdu && dPdv) {
      *dPdu = dPdu_;
      *dPdv = dPdv_;
    }

    *N = normalize(cross(dPdu_, dPdv_));
  }
  else {
    decasteljau_bicubic(P, dPdu, dPdv, hull, u, v);
  }
}
```

<details>
<summary>核对原始源码：intern/cycles/subd/patch.cpp · L88—L106</summary>

<!-- original:33ea2c38ea3b42:intern/cycles/subd/patch.cpp:88:106 -->

```cpp
void BicubicPatch::eval(
    float3 *P, float3 *dPdu, float3 *dPdv, float3 *N, const float u, const float v) const
{
  if (N) {
    float3 dPdu_;
    float3 dPdv_;
    decasteljau_bicubic(P, &dPdu_, &dPdv_, hull, u, v);

    if (dPdu && dPdv) {
      *dPdu = dPdu_;
      *dPdv = dPdv_;
    }

    *N = normalize(cross(dPdu_, dPdv_));
  }
  else {
    decasteljau_bicubic(P, dPdu, dPdv, hull, u, v);
  }
}
```

</details>

**继续追踪实现**

- `decasteljau_bicubic` → [decasteljau_bicubic · L31](%E4%BE%9D%E8%B5%96-patch-26f041.md#f-4f1ed62206d967ca)。
- `normalize` → [normalize · L109](%E4%BE%9D%E8%B5%96-IK_Math-614efe.md#f-1a1c851a5bd44fba)；[normalize · L77](%E4%BE%9D%E8%B5%96-Projections-91a559.md#f-15577af6ac05b036)；[normalize · L460](%E4%BE%9D%E8%B5%96-math_float4-2d91ea.md#f-25d06efa592ab5f5)；[normalize · L332](%E4%BE%9D%E8%B5%96-math_float3-eb3e6f.md#f-baa4b4b062d3b43f)；[normalize · L205](%E4%BE%9D%E8%B5%96-math_float2-be3c03.md#f-2a4866a4240a6727)；[normalize · L308](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-e2039e1856df8255)；[normalize · L16](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-c7ae20a29ab4da76)；[normalize · L20](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-058e4a05bbb6b503)；[normalize · L24](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-14dbdba2c67d0e8b)；[normalize · L34](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-625d4bad43dffd9c)；[normalize · L41](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-d55b4ac328dde4cb)；[normalize · L48](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-8a8b0bd437b339c5)；[normalize · L55](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-64d092bea6e62c87)；[normalize · L64](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-5e2d66321c5b1c64)；[normalize · L73](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-678c05ab6e94ffc2)；[normalize · L81](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-693795be99ff0d63)；[normalize · L90](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-e7110cf1e4527133)；[normalize · L100](%E4%BE%9D%E8%B5%96-gpu_shader_math_matrix_normalize.bsl-299c5b.md#f-c074535e46937142)。同名重载需按实参类型选择。
- `cross` → [cross · L436](%E4%BE%9D%E8%B5%96-math_float4-2d91ea.md#f-47c1848f44fe4b56)；[cross · L319](%E4%BE%9D%E8%B5%96-math_float3-eb3e6f.md#f-a89959ab21db0804)；[cross · L200](%E4%BE%9D%E8%B5%96-math_float2-be3c03.md#f-d4cf827d2d4b9025)；[cross · L284](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-8c812fdff783548f)；[cross · L291](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-fb4619a5864c3edc)；[cross · L296](%E4%BE%9D%E8%B5%96-math_dual-a0f3ee.md#f-d9964e9b2e1f70ab)。同名重载需按实参类型选择。
