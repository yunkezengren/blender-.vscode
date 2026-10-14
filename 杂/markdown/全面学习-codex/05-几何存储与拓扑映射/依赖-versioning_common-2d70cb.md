# 实现依赖专题：source/blender/blenloader/versioning_common.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::adjust_fcurve_key_frame_values"]:::abstraction
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
  F["versioning_common.hh实现"]:::compute
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

<a id="f-534a6e48783f59f7"></a>

### `blender::adjust_fcurve_key_frame_values`

实现位置：[source/blender/blenloader/versioning_common.hh](../../../../../source/blender/blenloader/versioning_common.hh) · L283—L319。

接口参数：

- `FCurve *fcurve`
- `const PropertyType property_type`
- `const Function &function`

**教学注释版**

<!-- annotated:e606af4ccdc2e4 -->

```cpp
template<typename Function>
static void adjust_fcurve_key_frame_values(FCurve *fcurve,
                                           const PropertyType property_type,
                                           const Function &function)
{
  /* Adjust key frames. */
  if (fcurve->bezt) {
    for (int i = 0; i < fcurve->totvert; i++) {
      fcurve->bezt[i].vec[0][1] = function(fcurve->bezt[i].vec[0][1]);
      fcurve->bezt[i].vec[1][1] = function(fcurve->bezt[i].vec[1][1]);
      fcurve->bezt[i].vec[2][1] = function(fcurve->bezt[i].vec[2][1]);
    }
  }

  /* Adjust baked key frames. */
  if (fcurve->fpt) {
    for (int i = 0; i < fcurve->totvert; i++) {
      fcurve->fpt[i].vec[1] = function(fcurve->fpt[i].vec[1]);
    }
  }

  /* Setup the flags based on the property type. */
  fcurve->flag &= ~(FCURVE_INT_VALUES | FCURVE_DISCRETE_VALUES);
  switch (property_type) {
    case PROP_FLOAT:
      break;
    case PROP_INT:
      fcurve->flag |= FCURVE_INT_VALUES;
      break;
    default:
      fcurve->flag |= (FCURVE_DISCRETE_VALUES | FCURVE_INT_VALUES);
      break;
  }

  /* Recalculate the automatic handles of the FCurve after adjustments. */
  BKE_fcurve_handles_recalc(*fcurve);
}
```

<details>
<summary>核对原始源码：source/blender/blenloader/versioning_common.hh · L283—L319</summary>

<!-- original:e606af4ccdc2e4:source/blender/blenloader/versioning_common.hh:283:319 -->

```cpp
template<typename Function>
static void adjust_fcurve_key_frame_values(FCurve *fcurve,
                                           const PropertyType property_type,
                                           const Function &function)
{
  /* Adjust key frames. */
  if (fcurve->bezt) {
    for (int i = 0; i < fcurve->totvert; i++) {
      fcurve->bezt[i].vec[0][1] = function(fcurve->bezt[i].vec[0][1]);
      fcurve->bezt[i].vec[1][1] = function(fcurve->bezt[i].vec[1][1]);
      fcurve->bezt[i].vec[2][1] = function(fcurve->bezt[i].vec[2][1]);
    }
  }

  /* Adjust baked key frames. */
  if (fcurve->fpt) {
    for (int i = 0; i < fcurve->totvert; i++) {
      fcurve->fpt[i].vec[1] = function(fcurve->fpt[i].vec[1]);
    }
  }

  /* Setup the flags based on the property type. */
  fcurve->flag &= ~(FCURVE_INT_VALUES | FCURVE_DISCRETE_VALUES);
  switch (property_type) {
    case PROP_FLOAT:
      break;
    case PROP_INT:
      fcurve->flag |= FCURVE_INT_VALUES;
      break;
    default:
      fcurve->flag |= (FCURVE_DISCRETE_VALUES | FCURVE_INT_VALUES);
      break;
  }

  /* Recalculate the automatic handles of the FCurve after adjustments. */
  BKE_fcurve_handles_recalc(*fcurve);
}
```

</details>

**沿实际写入检查状态**

- `fcurve->bezt[i].vec[0][1] = function(fcurve->bezt[i].vec[0][1]);`
- `fcurve->bezt[i].vec[1][1] = function(fcurve->bezt[i].vec[1][1]);`
- `fcurve->bezt[i].vec[2][1] = function(fcurve->bezt[i].vec[2][1]);`
- `fcurve->fpt[i].vec[1] = function(fcurve->fpt[i].vec[1]);`
- `fcurve->flag &= ~(FCURVE_INT_VALUES | FCURVE_DISCRETE_VALUES);`
- `fcurve->flag |= FCURVE_INT_VALUES;`
- `fcurve->flag |= (FCURVE_DISCRETE_VALUES | FCURVE_INT_VALUES);`

**继续追踪实现**

- `function` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L291。
- `BKE_fcurve_handles_recalc` → [blender::BKE_fcurve_handles_recalc · L1298](%E4%BE%9D%E8%B5%96-fcurve-593e2e.md#f-0673929c9eae7450)。
