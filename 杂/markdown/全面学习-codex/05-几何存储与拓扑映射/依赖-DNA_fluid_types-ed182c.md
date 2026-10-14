# 实现依赖专题：source/blender/makesdna/DNA_fluid_types.h

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_fluid_types.h"]:::abstraction
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
  F["DNA_fluid_types.h实现"]:::compute
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

<a id="t-63a2576e2335"></a>

### `blender::eFluidDomain_Flags`

原始声明：[source/blender/makesdna/DNA_fluid_types.h](../../../../../source/blender/makesdna/DNA_fluid_types.h) · L26—L46。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:4d99b23316d72c -->

```cpp
enum eFluidDomain_Flags : int {
  FLUID_DOMAIN_USE_NOISE = (1 << 1),        /* Use noise. */
  FLUID_DOMAIN_USE_DISSOLVE = (1 << 2),     /* Let smoke dissolve. */
  FLUID_DOMAIN_USE_DISSOLVE_LOG = (1 << 3), /* Using 1/x for dissolve. */

#ifdef DNA_DEPRECATED_ALLOW
  FLUID_DOMAIN_USE_HIGH_SMOOTH = (1 << 5), /* -- Deprecated -- */
#endif
  FLUID_DOMAIN_FILE_LOAD = (1 << 6), /* Flag for file load. */
  FLUID_DOMAIN_USE_ADAPTIVE_DOMAIN = (1 << 7),
  FLUID_DOMAIN_USE_ADAPTIVE_TIME = (1 << 8),    /* Adaptive time stepping in domain. */
  FLUID_DOMAIN_USE_MESH = (1 << 9),             /* Use mesh. */
  FLUID_DOMAIN_USE_GUIDE = (1 << 10),           /* Use guiding. */
  FLUID_DOMAIN_USE_SPEED_VECTORS = (1 << 11),   /* Generate mesh speed vectors. */
  FLUID_DOMAIN_EXPORT_MANTA_SCRIPT = (1 << 12), /* Export mantaflow script during bake. */
  FLUID_DOMAIN_USE_FRACTIONS = (1 << 13),       /* Use second order obstacles. */
  FLUID_DOMAIN_DELETE_IN_OBSTACLE = (1 << 14),  /* Delete fluid inside obstacles. */
  FLUID_DOMAIN_USE_DIFFUSION = (1 << 15), /* Use diffusion (e.g. viscosity, surface tension). */
  FLUID_DOMAIN_USE_RESUMABLE_CACHE = (1 << 16), /* Determine if cache should be resumable. */
  FLUID_DOMAIN_USE_VISCOSITY = (1 << 17),       /* Use viscosity. */
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_fluid_types.h · L26—L46</summary>

<!-- original:4d99b23316d72c:source/blender/makesdna/DNA_fluid_types.h:26:46 -->

```cpp
enum eFluidDomain_Flags : int {
  FLUID_DOMAIN_USE_NOISE = (1 << 1),        /* Use noise. */
  FLUID_DOMAIN_USE_DISSOLVE = (1 << 2),     /* Let smoke dissolve. */
  FLUID_DOMAIN_USE_DISSOLVE_LOG = (1 << 3), /* Using 1/x for dissolve. */

#ifdef DNA_DEPRECATED_ALLOW
  FLUID_DOMAIN_USE_HIGH_SMOOTH = (1 << 5), /* -- Deprecated -- */
#endif
  FLUID_DOMAIN_FILE_LOAD = (1 << 6), /* Flag for file load. */
  FLUID_DOMAIN_USE_ADAPTIVE_DOMAIN = (1 << 7),
  FLUID_DOMAIN_USE_ADAPTIVE_TIME = (1 << 8),    /* Adaptive time stepping in domain. */
  FLUID_DOMAIN_USE_MESH = (1 << 9),             /* Use mesh. */
  FLUID_DOMAIN_USE_GUIDE = (1 << 10),           /* Use guiding. */
  FLUID_DOMAIN_USE_SPEED_VECTORS = (1 << 11),   /* Generate mesh speed vectors. */
  FLUID_DOMAIN_EXPORT_MANTA_SCRIPT = (1 << 12), /* Export mantaflow script during bake. */
  FLUID_DOMAIN_USE_FRACTIONS = (1 << 13),       /* Use second order obstacles. */
  FLUID_DOMAIN_DELETE_IN_OBSTACLE = (1 << 14),  /* Delete fluid inside obstacles. */
  FLUID_DOMAIN_USE_DIFFUSION = (1 << 15), /* Use diffusion (e.g. viscosity, surface tension). */
  FLUID_DOMAIN_USE_RESUMABLE_CACHE = (1 << 16), /* Determine if cache should be resumable. */
  FLUID_DOMAIN_USE_VISCOSITY = (1 << 17),       /* Use viscosity. */
};
```

</details>


## 完整成员与函数实现
