# 实现依赖专题：source/blender/makesdna/DNA_anim_enums.h

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_anim_enums.h"]:::abstraction
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
  F["DNA_anim_enums.h实现"]:::compute
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

## 相关类型布局与成员入口

<a id="t-86ae0c63cf3b"></a>

### `blender::eFCurve_Flags`

原始声明：[source/blender/makesdna/DNA_anim_enums.h](../../../../../../../source/blender/makesdna/DNA_anim_enums.h) · L303—L331。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:8216291dd72c9e -->

```cpp
enum eFCurve_Flags : short {
  /** Curve/keyframes are visible in editor */
  FCURVE_VISIBLE = (1 << 0),
  /** Curve is selected for editing. */
  FCURVE_SELECTED = (1 << 1),
  /** Curve is active one. */
  FCURVE_ACTIVE = (1 << 2),
  /** Keyframes (beztriples) cannot be edited. */
  FCURVE_PROTECTED = (1 << 3),
  /** FCurve will not be evaluated for the next round. */
  FCURVE_MUTED = (1 << 4),

#ifdef DNA_DEPRECATED_ALLOW
  /** fcurve uses 'auto-handles', which stay horizontal... */
  FCURVE_AUTO_HANDLES = (1 << 5), /* Dirty. */
#endif
  FCURVE_MOD_OFF = (1 << 6),
  /** skip evaluation, as RNA-path cannot be resolved
   * (similar to muting, but cannot be set by user) */
  FCURVE_DISABLED = (1 << 10),
  /** curve can only have whole-number values (integer types) */
  FCURVE_INT_VALUES = (1 << 11),
  /** curve can only have certain discrete-number values
   * (no interpolation at all, for enums/booleans) */
  FCURVE_DISCRETE_VALUES = (1 << 12),

  /** temporary tag for editing */
  FCURVE_TAGGED = static_cast<short>(1 << 15),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_anim_enums.h · L303—L331</summary>

<!-- original:8216291dd72c9e:source/blender/makesdna/DNA_anim_enums.h:303:331 -->

```cpp
enum eFCurve_Flags : short {
  /** Curve/keyframes are visible in editor */
  FCURVE_VISIBLE = (1 << 0),
  /** Curve is selected for editing. */
  FCURVE_SELECTED = (1 << 1),
  /** Curve is active one. */
  FCURVE_ACTIVE = (1 << 2),
  /** Keyframes (beztriples) cannot be edited. */
  FCURVE_PROTECTED = (1 << 3),
  /** FCurve will not be evaluated for the next round. */
  FCURVE_MUTED = (1 << 4),

#ifdef DNA_DEPRECATED_ALLOW
  /** fcurve uses 'auto-handles', which stay horizontal... */
  FCURVE_AUTO_HANDLES = (1 << 5), /* Dirty. */
#endif
  FCURVE_MOD_OFF = (1 << 6),
  /** skip evaluation, as RNA-path cannot be resolved
   * (similar to muting, but cannot be set by user) */
  FCURVE_DISABLED = (1 << 10),
  /** curve can only have whole-number values (integer types) */
  FCURVE_INT_VALUES = (1 << 11),
  /** curve can only have certain discrete-number values
   * (no interpolation at all, for enums/booleans) */
  FCURVE_DISCRETE_VALUES = (1 << 12),

  /** temporary tag for editing */
  FCURVE_TAGGED = static_cast<short>(1 << 15),
};
```

</details>


<a id="t-1f2167ad3a7d"></a>

### `blender::eInsertKeyFlags`

原始声明：[source/blender/makesdna/DNA_anim_enums.h](../../../../../../../source/blender/makesdna/DNA_anim_enums.h) · L500—L524。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:9de9761a8619ec -->

```cpp
enum eInsertKeyFlags : short {
  INSERTKEY_NOFLAGS = 0,
  /** Only insert keyframes where they're needed. */
  INSERTKEY_NEEDED = (1 << 0),
  /** Insert "visual" keyframes where possible/needed. */
  INSERTKEY_MATRIX = (1 << 1),
  /** Don't recalculate handles,etc. after adding key. */
  INSERTKEY_FAST = (1 << 2),
  /** Don't re-allocate memory (or increase count, as array has already been set out). */
  /* INSERTKEY_FASTR = (1 << 3), */ /* UNUSED */
  /** Only replace an existing keyframe (this overrides #INSERTKEY_NEEDED). */
  INSERTKEY_REPLACE = (1 << 4),
  /** Ignore user-preferences (needed for predictable API use). */
  INSERTKEY_NO_USERPREF = (1 << 6),
  /**
   * Allow to make a full copy of new key into existing one, if any,
   * instead of 'reusing' existing handles.
   * Used by copy/paste code.
   */
  INSERTKEY_OVERWRITE_FULL = (1 << 7),
  /** For cyclic FCurves, adjust key timing to preserve the cycle period and flow. */
  INSERTKEY_CYCLE_AWARE = (1 << 9),
  /** Don't create new F-Curves (implied by #INSERTKEY_REPLACE). */
  INSERTKEY_AVAILABLE = (1 << 10),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_anim_enums.h · L500—L524</summary>

<!-- original:9de9761a8619ec:source/blender/makesdna/DNA_anim_enums.h:500:524 -->

```cpp
enum eInsertKeyFlags : short {
  INSERTKEY_NOFLAGS = 0,
  /** Only insert keyframes where they're needed. */
  INSERTKEY_NEEDED = (1 << 0),
  /** Insert "visual" keyframes where possible/needed. */
  INSERTKEY_MATRIX = (1 << 1),
  /** Don't recalculate handles,etc. after adding key. */
  INSERTKEY_FAST = (1 << 2),
  /** Don't re-allocate memory (or increase count, as array has already been set out). */
  /* INSERTKEY_FASTR = (1 << 3), */ /* UNUSED */
  /** Only replace an existing keyframe (this overrides #INSERTKEY_NEEDED). */
  INSERTKEY_REPLACE = (1 << 4),
  /** Ignore user-preferences (needed for predictable API use). */
  INSERTKEY_NO_USERPREF = (1 << 6),
  /**
   * Allow to make a full copy of new key into existing one, if any,
   * instead of 'reusing' existing handles.
   * Used by copy/paste code.
   */
  INSERTKEY_OVERWRITE_FULL = (1 << 7),
  /** For cyclic FCurves, adjust key timing to preserve the cycle period and flow. */
  INSERTKEY_CYCLE_AWARE = (1 << 9),
  /** Don't create new F-Curves (implied by #INSERTKEY_REPLACE). */
  INSERTKEY_AVAILABLE = (1 << 10),
};
```

</details>


## 完整成员与函数实现
