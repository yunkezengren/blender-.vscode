# 实现依赖专题：source/blender/makesdna/DNA_particle_types.h

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_particle_types.h"]:::abstraction
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
  F["DNA_particle_types.h实现"]:::compute
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

<a id="t-5e33cefae34a"></a>

### `blender::VecBase`

原始声明：[source/blender/makesdna/DNA_particle_types.h](../../../../../source/blender/makesdna/DNA_particle_types.h) · L20—L20。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:544a533b7efc61 -->

```cpp
template<typename T, int Size> struct VecBase;
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_particle_types.h · L20—L20</summary>

<!-- original:544a533b7efc61:source/blender/makesdna/DNA_particle_types.h:20:20 -->

```cpp
template<typename T, int Size> struct VecBase;
```

</details>


<a id="t-7d74bd346171"></a>

### `blender::eParticleDrawFlag`

原始声明：[source/blender/makesdna/DNA_particle_types.h](../../../../../source/blender/makesdna/DNA_particle_types.h) · L47—L72。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:bf3156a2d33090 -->

```cpp
enum eParticleDrawFlag : int {
  PART_DRAW_VEL = (1 << 0),
  PART_DRAW_GLOBAL_OB = (1 << 1),
  PART_DRAW_SIZE = (1 << 2),
#ifdef DNA_DEPRECATED_ALLOW
  /** Render emitter as well. */
  PART_DRAW_EMITTER = (1 << 3), /* DEPRECATED */
#endif
  PART_DRAW_HEALTH = (1 << 4),
  PART_ABS_PATH_TIME = (1 << 5),
  PART_DRAW_COUNT_GR = (1 << 6),
  /* PART_DRAW_BB_LOCK = (1 << 7), */ /* DEPRECATED */
  /* used with billboards */          /* DEPRECATED */
  PART_DRAW_ROTATE_OB = (1 << 7),     /* used with instance object/collection */
  PART_DRAW_PARENT = (1 << 8),
  PART_DRAW_NUM = (1 << 9),
  PART_DRAW_RAND_GR = (1 << 10),
  PART_DRAW_REN_ADAPT = (1 << 11),
  PART_DRAW_VEL_LENGTH = (1 << 12),
  PART_DRAW_MAT_COL = (1 << 13), /* deprecated, but used in do_versions */
  PART_DRAW_WHOLE_GR = (1 << 14),
  PART_DRAW_REN_STRAND = (1 << 15),
  PART_DRAW_NO_SCALE_OB = (1 << 16), /* used with instance object/collection */
  PART_DRAW_GUIDE_HAIRS = (1 << 17),
  PART_DRAW_HAIR_GRID = (1 << 18),
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_particle_types.h · L47—L72</summary>

<!-- original:bf3156a2d33090:source/blender/makesdna/DNA_particle_types.h:47:72 -->

```cpp
enum eParticleDrawFlag : int {
  PART_DRAW_VEL = (1 << 0),
  PART_DRAW_GLOBAL_OB = (1 << 1),
  PART_DRAW_SIZE = (1 << 2),
#ifdef DNA_DEPRECATED_ALLOW
  /** Render emitter as well. */
  PART_DRAW_EMITTER = (1 << 3), /* DEPRECATED */
#endif
  PART_DRAW_HEALTH = (1 << 4),
  PART_ABS_PATH_TIME = (1 << 5),
  PART_DRAW_COUNT_GR = (1 << 6),
  /* PART_DRAW_BB_LOCK = (1 << 7), */ /* DEPRECATED */
  /* used with billboards */          /* DEPRECATED */
  PART_DRAW_ROTATE_OB = (1 << 7),     /* used with instance object/collection */
  PART_DRAW_PARENT = (1 << 8),
  PART_DRAW_NUM = (1 << 9),
  PART_DRAW_RAND_GR = (1 << 10),
  PART_DRAW_REN_ADAPT = (1 << 11),
  PART_DRAW_VEL_LENGTH = (1 << 12),
  PART_DRAW_MAT_COL = (1 << 13), /* deprecated, but used in do_versions */
  PART_DRAW_WHOLE_GR = (1 << 14),
  PART_DRAW_REN_STRAND = (1 << 15),
  PART_DRAW_NO_SCALE_OB = (1 << 16), /* used with instance object/collection */
  PART_DRAW_GUIDE_HAIRS = (1 << 17),
  PART_DRAW_HAIR_GRID = (1 << 18),
};
```

</details>


<a id="t-dbcd476846a8"></a>

### `blender::eParticleFrom`

原始声明：[source/blender/makesdna/DNA_particle_types.h](../../../../../source/blender/makesdna/DNA_particle_types.h) · L166—L172。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:78a1baeb218475 -->

```cpp
enum eParticleFrom : short {
  PART_FROM_VERT = 0,
  PART_FROM_FACE = 1,
  PART_FROM_VOLUME = 2,
  // PART_FROM_PARTICLE = 3, /* Deprecated. */
  PART_FROM_CHILD = 4,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_particle_types.h · L166—L172</summary>

<!-- original:78a1baeb218475:source/blender/makesdna/DNA_particle_types.h:166:172 -->

```cpp
enum eParticleFrom : short {
  PART_FROM_VERT = 0,
  PART_FROM_FACE = 1,
  PART_FROM_VOLUME = 2,
  // PART_FROM_PARTICLE = 3, /* Deprecated. */
  PART_FROM_CHILD = 4,
};
```

</details>


<a id="t-411f197933f3"></a>

### `blender::ParticleSettings::MTex`

原始声明：[source/blender/makesdna/DNA_particle_types.h](../../../../../source/blender/makesdna/DNA_particle_types.h) · L658—L658。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:c9f73292574d3c -->

```cpp
  struct MTex *mtex[/*MAX_MTEX*/ 18] = {};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_particle_types.h · L658—L658</summary>

<!-- original:c9f73292574d3c:source/blender/makesdna/DNA_particle_types.h:658:658 -->

```cpp
  struct MTex *mtex[/*MAX_MTEX*/ 18] = {};
```

</details>


## 完整成员与函数实现
