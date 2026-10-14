# 实现依赖专题：source/blender/bmesh/intern/bmesh_iterators.hh

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["bmesh_iterators.hh"]:::abstraction
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
  F["bmesh_iterators.hh实现"]:::compute
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

<a id="t-5887f9d5a0b1"></a>

### `blender::BMIterType`

原始声明：[source/blender/bmesh/intern/bmesh_iterators.hh](../../../../../../../../source/blender/bmesh/intern/bmesh_iterators.hh) · L37—L59。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:7cacf8272ce993 -->

```cpp
enum BMIterType {
  BM_VERTS_OF_MESH = 1,
  BM_EDGES_OF_MESH = 2,
  BM_FACES_OF_MESH = 3,
  /* these are topological iterators. */
  BM_EDGES_OF_VERT = 4,
  BM_FACES_OF_VERT = 5,
  BM_LOOPS_OF_VERT = 6,
  BM_VERTS_OF_EDGE = 7, /* just v1, v2: added so py can use generalized sequencer wrapper */
  BM_FACES_OF_EDGE = 8,
  BM_VERTS_OF_FACE = 9,
  BM_EDGES_OF_FACE = 10,
  BM_LOOPS_OF_FACE = 11,
  /* returns elements from all boundaries, and returns
   * the first element at the end to flag that we're entering
   * a different face hole boundary. */
  // BM_ALL_LOOPS_OF_FACE = 12,
  /* iterate through loops around this loop, which are fetched
   * from the other faces in the radial cycle surrounding the
   * input loop's edge. */
  BM_LOOPS_OF_LOOP = 12,
  BM_LOOPS_OF_EDGE = 13,
};
```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_iterators.hh · L37—L59</summary>

<!-- original:7cacf8272ce993:source/blender/bmesh/intern/bmesh_iterators.hh:37:59 -->

```cpp
enum BMIterType {
  BM_VERTS_OF_MESH = 1,
  BM_EDGES_OF_MESH = 2,
  BM_FACES_OF_MESH = 3,
  /* these are topological iterators. */
  BM_EDGES_OF_VERT = 4,
  BM_FACES_OF_VERT = 5,
  BM_LOOPS_OF_VERT = 6,
  BM_VERTS_OF_EDGE = 7, /* just v1, v2: added so py can use generalized sequencer wrapper */
  BM_FACES_OF_EDGE = 8,
  BM_VERTS_OF_FACE = 9,
  BM_EDGES_OF_FACE = 10,
  BM_LOOPS_OF_FACE = 11,
  /* returns elements from all boundaries, and returns
   * the first element at the end to flag that we're entering
   * a different face hole boundary. */
  // BM_ALL_LOOPS_OF_FACE = 12,
  /* iterate through loops around this loop, which are fetched
   * from the other faces in the radial cycle surrounding the
   * input loop's edge. */
  BM_LOOPS_OF_LOOP = 12,
  BM_LOOPS_OF_EDGE = 13,
};
```

</details>


<a id="m-cfc837c73218"></a>

## 宏 `BM_ITER_MESH`

<!-- annotated:36a7e2a91092f1 -->

```cpp
#define BM_ITER_MESH(ele, iter, bm, itype) \
  for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, bm, itype, NULL); ele; \
       BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_step(iter))

```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_iterators.hh · L72—L75</summary>

<!-- original:36a7e2a91092f1:source/blender/bmesh/intern/bmesh_iterators.hh:72:75 -->

```cpp
#define BM_ITER_MESH(ele, iter, bm, itype) \
  for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, bm, itype, NULL); ele; \
       BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_step(iter))

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-6a0cac4538f9"></a>

## 宏 `BM_ITER_MESH_INDEX`

<!-- annotated:e543279ef69df2 -->

```cpp
#define BM_ITER_MESH_INDEX(ele, iter, bm, itype, indexvar) \
  for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, bm, itype, NULL), indexvar = 0; ele; \
       BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_step(iter), (indexvar)++)

```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_iterators.hh · L76—L79</summary>

<!-- original:e543279ef69df2:source/blender/bmesh/intern/bmesh_iterators.hh:76:79 -->

```cpp
#define BM_ITER_MESH_INDEX(ele, iter, bm, itype, indexvar) \
  for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, bm, itype, NULL), indexvar = 0; ele; \
       BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_step(iter), (indexvar)++)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-2887500f7f76"></a>

## 宏 `BM_ITER_MESH_MUTABLE`

<!-- annotated:6e797d9e12ae50 -->

```cpp
#  define BM_ITER_MESH_MUTABLE(ele, ele_next, iter, bm, itype) \
    for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, bm, itype, NULL); \
         ele ? ((void)((iter)->count = BM_iter_mesh_count(itype, bm)), \
                (void)(BM_CHECK_TYPE_ELEM_ASSIGN(ele_next) = BM_iter_step(iter)), \
                1) : \
               0; \
         BM_CHECK_TYPE_ELEM_ASSIGN(ele) = ele_next)
#else
```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_iterators.hh · L83—L90</summary>

<!-- original:6e797d9e12ae50:source/blender/bmesh/intern/bmesh_iterators.hh:83:90 -->

```cpp
#  define BM_ITER_MESH_MUTABLE(ele, ele_next, iter, bm, itype) \
    for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, bm, itype, NULL); \
         ele ? ((void)((iter)->count = BM_iter_mesh_count(itype, bm)), \
                (void)(BM_CHECK_TYPE_ELEM_ASSIGN(ele_next) = BM_iter_step(iter)), \
                1) : \
               0; \
         BM_CHECK_TYPE_ELEM_ASSIGN(ele) = ele_next)
#else
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-de2c06ab3bfc"></a>

## 宏 `BM_ITER_MESH_MUTABLE`

<!-- annotated:0cb32c6dc521f6 -->

```cpp
#  define BM_ITER_MESH_MUTABLE(ele, ele_next, iter, bm, itype) \
    for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, bm, itype, NULL); \
         ele ? ((BM_CHECK_TYPE_ELEM_ASSIGN(ele_next) = BM_iter_step(iter)), 1) : 0; \
         ele = ele_next)
#endif
```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_iterators.hh · L91—L95</summary>

<!-- original:0cb32c6dc521f6:source/blender/bmesh/intern/bmesh_iterators.hh:91:95 -->

```cpp
#  define BM_ITER_MESH_MUTABLE(ele, ele_next, iter, bm, itype) \
    for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, bm, itype, NULL); \
         ele ? ((BM_CHECK_TYPE_ELEM_ASSIGN(ele_next) = BM_iter_step(iter)), 1) : 0; \
         ele = ele_next)
#endif
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-751d15be7ee4"></a>

## 宏 `BM_ITER_ELEM`

<!-- annotated:45e8e3aa49ba04 -->

```cpp
#define BM_ITER_ELEM(ele, iter, data, itype) \
  for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, NULL, itype, data); ele; \
       BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_step(iter))

```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_iterators.hh · L97—L100</summary>

<!-- original:45e8e3aa49ba04:source/blender/bmesh/intern/bmesh_iterators.hh:97:100 -->

```cpp
#define BM_ITER_ELEM(ele, iter, data, itype) \
  for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, NULL, itype, data); ele; \
       BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_step(iter))

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-b74163463a01"></a>

## 宏 `BM_ITER_ELEM_INDEX`

<!-- annotated:1f977779f61e1e -->

```cpp
#define BM_ITER_ELEM_INDEX(ele, iter, data, itype, indexvar) \
  for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, NULL, itype, data), indexvar = 0; ele; \
       BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_step(iter), (indexvar)++)

```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_iterators.hh · L101—L104</summary>

<!-- original:1f977779f61e1e:source/blender/bmesh/intern/bmesh_iterators.hh:101:104 -->

```cpp
#define BM_ITER_ELEM_INDEX(ele, iter, data, itype, indexvar) \
  for (BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_new(iter, NULL, itype, data), indexvar = 0; ele; \
       BM_CHECK_TYPE_ELEM_ASSIGN(ele) = BM_iter_step(iter), (indexvar)++)

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
