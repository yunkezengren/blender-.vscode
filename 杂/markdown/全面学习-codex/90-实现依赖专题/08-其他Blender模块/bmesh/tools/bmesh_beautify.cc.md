# 实现依赖专题：source/blender/bmesh/tools/bmesh_beautify.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::bm_edge_calc_rotate_beauty__angle"]:::abstraction
  F1["blender::BM_verts_calc_rotate_beauty"]:::compute
  F1 -->|"显式调用"| F0
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
  F["bmesh_beautify.cc实现"]:::compute
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

<a id="f-1cfd7baf0d95fbef"></a>

### `blender::bm_edge_calc_rotate_beauty__angle`

实现位置：[source/blender/bmesh/tools/bmesh_beautify.cc](../../../../../../../../source/blender/bmesh/tools/bmesh_beautify.cc) · L143—L169。

接口参数：

- `const float v1[3]`
- `const float v2[3]`
- `const float v3[3]`
- `const float v4[3]`

**教学注释版**

<!-- annotated:f9c3b4897ad13d -->

```cpp
static float bm_edge_calc_rotate_beauty__angle(const float v1[3],
                                               const float v2[3],
                                               const float v3[3],
                                               const float v4[3])
{
  /* not a loop (only to be able to break out) */
  do {
    float no_a[3], no_b[3];
    float angle_24, angle_13;

    /* edge (2-4), current state */
    normal_tri_v3(no_a, v2, v3, v4);
    normal_tri_v3(no_b, v2, v4, v1);
    angle_24 = angle_normalized_v3v3(no_a, no_b);

    /* edge (1-3), new state */
    /* only check new state for degenerate outcome */
    if ((normal_tri_v3(no_a, v1, v2, v3) == 0.0f) || (normal_tri_v3(no_b, v1, v3, v4) == 0.0f)) {
      break;
    }
    angle_13 = angle_normalized_v3v3(no_a, no_b);

    return angle_13 - angle_24;
  } while (false);

  return FLT_MAX;
}
```

<details>
<summary>核对原始源码：source/blender/bmesh/tools/bmesh_beautify.cc · L143—L169</summary>

<!-- original:f9c3b4897ad13d:source/blender/bmesh/tools/bmesh_beautify.cc:143:169 -->

```cpp
static float bm_edge_calc_rotate_beauty__angle(const float v1[3],
                                               const float v2[3],
                                               const float v3[3],
                                               const float v4[3])
{
  /* not a loop (only to be able to break out) */
  do {
    float no_a[3], no_b[3];
    float angle_24, angle_13;

    /* edge (2-4), current state */
    normal_tri_v3(no_a, v2, v3, v4);
    normal_tri_v3(no_b, v2, v4, v1);
    angle_24 = angle_normalized_v3v3(no_a, no_b);

    /* edge (1-3), new state */
    /* only check new state for degenerate outcome */
    if ((normal_tri_v3(no_a, v1, v2, v3) == 0.0f) || (normal_tri_v3(no_b, v1, v3, v4) == 0.0f)) {
      break;
    }
    angle_13 = angle_normalized_v3v3(no_a, no_b);

    return angle_13 - angle_24;
  } while (false);

  return FLT_MAX;
}
```

</details>

**沿实际写入检查状态**

- `angle_24 = angle_normalized_v3v3(no_a, no_b);`
- `angle_13 = angle_normalized_v3v3(no_a, no_b);`

**结果出口**

- `return angle_13 - angle_24;`
- `return FLT_MAX;`

**继续追踪实现**

- `normal_tri_v3` → [blender::normal_tri_v3 · L45](../../../01-BLI基础库/intern/math_geom.cc.md#f-f574cdfe156b33d2)。
- `angle_normalized_v3v3` → [blender::angle_normalized_v3v3 · L336](../../../01-BLI基础库/intern/math_vector.cc.md#f-46a4c8a9d1ed895e)。

<a id="f-aaadc1a9d9afe57c"></a>

### `blender::BM_verts_calc_rotate_beauty`

实现位置：[source/blender/bmesh/tools/bmesh_beautify.cc](../../../../../../../../source/blender/bmesh/tools/bmesh_beautify.cc) · L171—L202。

接口参数：

- `const BMVert *v1`
- `const BMVert *v2`
- `const BMVert *v3`
- `const BMVert *v4`
- `const short flag`
- `const short method`

**教学注释版**

<!-- annotated:b36bd4baec5064 -->

```cpp
float BM_verts_calc_rotate_beauty(const BMVert *v1,
                                  const BMVert *v2,
                                  const BMVert *v3,
                                  const BMVert *v4,
                                  const short flag,
                                  const short method)
{
  /* not a loop (only to be able to break out) */
  do {
    if (flag & VERT_RESTRICT_TAG) {
      const BMVert *v_a = v1, *v_b = v3;
      if (BM_elem_flag_test(v_a, BM_ELEM_TAG) == BM_elem_flag_test(v_b, BM_ELEM_TAG)) {
        break;
      }
    }

    if (v1 == v3) [[unlikely]] {
      // printf("This should never happen, but does sometimes!\n");
      break;
    }

    switch (method) {
      case 0:
        return BLI_polyfill_edge_calc_rotate_beauty__area(
            v1->co, v2->co, v3->co, v4->co, flag & EDGE_RESTRICT_DEGENERATE);
      default:
        return bm_edge_calc_rotate_beauty__angle(v1->co, v2->co, v3->co, v4->co);
    }
  } while (false);

  return FLT_MAX;
}
```

<details>
<summary>核对原始源码：source/blender/bmesh/tools/bmesh_beautify.cc · L171—L202</summary>

<!-- original:b36bd4baec5064:source/blender/bmesh/tools/bmesh_beautify.cc:171:202 -->

```cpp
float BM_verts_calc_rotate_beauty(const BMVert *v1,
                                  const BMVert *v2,
                                  const BMVert *v3,
                                  const BMVert *v4,
                                  const short flag,
                                  const short method)
{
  /* not a loop (only to be able to break out) */
  do {
    if (flag & VERT_RESTRICT_TAG) {
      const BMVert *v_a = v1, *v_b = v3;
      if (BM_elem_flag_test(v_a, BM_ELEM_TAG) == BM_elem_flag_test(v_b, BM_ELEM_TAG)) {
        break;
      }
    }

    if (v1 == v3) [[unlikely]] {
      // printf("This should never happen, but does sometimes!\n");
      break;
    }

    switch (method) {
      case 0:
        return BLI_polyfill_edge_calc_rotate_beauty__area(
            v1->co, v2->co, v3->co, v4->co, flag & EDGE_RESTRICT_DEGENERATE);
      default:
        return bm_edge_calc_rotate_beauty__angle(v1->co, v2->co, v3->co, v4->co);
    }
  } while (false);

  return FLT_MAX;
}
```

</details>

**结果出口**

- `return BLI_polyfill_edge_calc_rotate_beauty__area(`
- `return bm_edge_calc_rotate_beauty__angle(v1->co, v2->co, v3->co, v4->co);`
- `return FLT_MAX;`

**继续追踪实现**

- `BM_elem_flag_test` → [BM_elem_flag_test · L21](../intern/bmesh_inline.hh.md#m-2431d1179b41)。宏定义由构建条件选择。
- `BLI_polyfill_edge_calc_rotate_beauty__area` → [blender::BLI_polyfill_edge_calc_rotate_beauty__area · L182](../../../01-BLI基础库/intern/polyfill_2d_beautify.cc.md#f-4ca59348ff5a1727)。
- `bm_edge_calc_rotate_beauty__angle` → [blender::bm_edge_calc_rotate_beauty__angle · L143](bmesh_beautify.cc.md#f-1cfd7baf0d95fbef)。
