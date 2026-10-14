# 实现依赖专题：source/blender/blenkernel/BKE_rigidbody.h

[实现依赖导航](../README.md) · [符号索引](../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["BKE_rigidbody.h"]:::abstraction
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
  F["BKE_rigidbody.h实现"]:::compute
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

<a id="m-ce170f8eade9"></a>

## 宏 `RBO_GET_MASS`

<!-- annotated:38bbc45d69a8bc -->

```cpp
#define RBO_GET_MASS(rbo) \
  (((rbo) && (((rbo)->type == RBO_TYPE_PASSIVE) || ((rbo)->flag & RBO_FLAG_KINEMATIC) || \
              ((rbo)->flag & RBO_FLAG_DISABLED))) ? \
       (0.0f) : \
       ((rbo)->mass))
/**
```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_rigidbody.h · L182—L187</summary>

<!-- original:38bbc45d69a8bc:source/blender/blenkernel/BKE_rigidbody.h:182:187 -->

```cpp
#define RBO_GET_MASS(rbo) \
  (((rbo) && (((rbo)->type == RBO_TYPE_PASSIVE) || ((rbo)->flag & RBO_FLAG_KINEMATIC) || \
              ((rbo)->flag & RBO_FLAG_DISABLED))) ? \
       (0.0f) : \
       ((rbo)->mass))
/**
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-7bfcef0746cd"></a>

## 宏 `RBO_GET_MARGIN`

<!-- annotated:39183211ef0b3e -->

```cpp
#define RBO_GET_MARGIN(rbo) \
  (((rbo)->flag & RBO_FLAG_USE_MARGIN || (rbo)->shape == RB_SHAPE_CONVEXH || \
    (rbo)->shape == RB_SHAPE_TRIMESH || (rbo)->shape == RB_SHAPE_CONE) ? \
       ((rbo)->margin) : \
       (0.04f))

```

<details>
<summary>核对原始源码：source/blender/blenkernel/BKE_rigidbody.h · L191—L196</summary>

<!-- original:39183211ef0b3e:source/blender/blenkernel/BKE_rigidbody.h:191:196 -->

```cpp
#define RBO_GET_MARGIN(rbo) \
  (((rbo)->flag & RBO_FLAG_USE_MARGIN || (rbo)->shape == RB_SHAPE_CONVEXH || \
    (rbo)->shape == RB_SHAPE_TRIMESH || (rbo)->shape == RB_SHAPE_CONE) ? \
       ((rbo)->margin) : \
       (0.04f))

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
