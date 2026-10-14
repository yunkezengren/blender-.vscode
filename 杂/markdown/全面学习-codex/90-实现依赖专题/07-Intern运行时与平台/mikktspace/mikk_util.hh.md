# 实现依赖专题：intern/mikktspace/mikk_util.hh

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["mikk::not_zero"]:::abstraction
  F1["mikk::pack_index"]:::compute
  F2["mikk::unpack_index"]:::compute
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
  F["mikk_util.hh实现"]:::compute
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

<a id="f-d6d85f27cf5a09d9"></a>

### `mikk::not_zero`

实现位置：[intern/mikktspace/mikk_util.hh](../../../../../../../intern/mikktspace/mikk_util.hh) · L22—L25。

接口参数：

- `const float fX`

**教学注释版**

<!-- annotated:2e123f8afc1548 -->

```cpp
inline bool not_zero(const float fX)
{
  return fabsf(fX) > FLT_MIN;
}
```

<details>
<summary>核对原始源码：intern/mikktspace/mikk_util.hh · L22—L25</summary>

<!-- original:2e123f8afc1548:intern/mikktspace/mikk_util.hh:22:25 -->

```cpp
inline bool not_zero(const float fX)
{
  return fabsf(fX) > FLT_MIN;
}
```

</details>

**结果出口**

- `return fabsf(fX) > FLT_MIN;`

**继续追踪实现**

- `fabsf` → [fabsf · L21](../cycles/kernel/svm/radial_tiling_shared.h.md#m-02cc4c69cfb3)；[fabsf · L43](../cycles/kernel/svm/radial_tiling_shared.h.md#m-04effe61803b)；[fabsf · L74](../cycles/kernel/svm/radial_tiling_shared.h.md#m-927dd4eba7dc)；[fabsf · L25](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-8348d6b3d08f)；[fabsf · L47](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-13b7e0b6d84f)；[fabsf · L78](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-326c83464a0d)；[fabsf · L21](../cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-7c3ee12fc119)；[fabsf · L43](../cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-9112db0e2dd1)；[fabsf · L74](../cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-ee4e61908a6f)；[fabsf · L167](../cycles/kernel/device/oneapi/compat.h.md#m-b039ee6c1601)；[fabsf · L265](../cycles/kernel/device/metal/compat.h.md#m-6b21869e9f3f)。宏定义由构建条件选择。

<a id="f-3a15ac87c0be7fa2"></a>

### `mikk::pack_index`

实现位置：[intern/mikktspace/mikk_util.hh](../../../../../../../intern/mikktspace/mikk_util.hh) · L28—L32。

接口参数：

- `const uint face`
- `const uint vert`

**教学注释版**

<!-- annotated:bde6c7867bfbe6 -->

```cpp
static uint pack_index(const uint face, const uint vert)
{
  // [讲解] assert：检查开发者预期条件，配置可能关闭；不承担完整输入处理或自动修复。
  assert((vert & 0x3) == vert);
  return (face << 2) | (vert & 0x3);
}
```

<details>
<summary>核对原始源码：intern/mikktspace/mikk_util.hh · L28—L32</summary>

<!-- original:bde6c7867bfbe6:intern/mikktspace/mikk_util.hh:28:32 -->

```cpp
static uint pack_index(const uint face, const uint vert)
{
  assert((vert & 0x3) == vert);
  return (face << 2) | (vert & 0x3);
}
```

</details>

**结果出口**

- `return (face << 2) | (vert & 0x3);`

**继续追踪实现**

- `assert` → [外部契约](https://eel.is/c++draft/assertions)：检查开发者预期条件，配置可能关闭；不承担完整输入处理或自动修复。

<a id="f-5f4558ff149fd484"></a>

### `mikk::unpack_index`

实现位置：[intern/mikktspace/mikk_util.hh](../../../../../../../intern/mikktspace/mikk_util.hh) · L34—L38。

接口参数：

- `uint &face`
- `uint &vert`
- `const uint indexIn`

**教学注释版**

<!-- annotated:f12f19da875509 -->

```cpp
static void unpack_index(uint &face, uint &vert, const uint indexIn)
{
  vert = indexIn & 0x3;
  face = indexIn >> 2;
}
```

<details>
<summary>核对原始源码：intern/mikktspace/mikk_util.hh · L34—L38</summary>

<!-- original:f12f19da875509:intern/mikktspace/mikk_util.hh:34:38 -->

```cpp
static void unpack_index(uint &face, uint &vert, const uint indexIn)
{
  vert = indexIn & 0x3;
  face = indexIn >> 2;
}
```

</details>

**沿实际写入检查状态**

- `vert = indexIn & 0x3;`
- `face = indexIn >> 2;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
