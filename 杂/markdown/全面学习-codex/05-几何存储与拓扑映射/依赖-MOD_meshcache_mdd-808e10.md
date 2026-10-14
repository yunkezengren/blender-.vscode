# 实现依赖专题：source/blender/modifiers/intern/MOD_meshcache_mdd.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::meshcache_read_mdd_head"]:::abstraction
  F1["blender::meshcache_read_mdd_range"]:::compute
  F2["blender::meshcache_read_mdd_range_from_time"]:::compute
  F3["blender::MOD_meshcache_read_mdd_index"]:::compute
  F4["blender::MOD_meshcache_read_mdd_frame"]:::compute
  F5["blender::MOD_meshcache_read_mdd_times"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F0
  F3 -->|"显式调用"| F0
  F4 -->|"显式调用"| F1
  F4 -->|"显式调用"| F3
  F5 -->|"显式调用"| F2
  F5 -->|"显式调用"| F0
  F5 -->|"显式调用"| F4
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
  F["MOD_meshcache_mdd.cc实现"]:::compute
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

<a id="f-7e707d83d96e2e30"></a>

### `blender::meshcache_read_mdd_head`

实现位置：[source/blender/modifiers/intern/MOD_meshcache_mdd.cc](../../../../../source/blender/modifiers/intern/MOD_meshcache_mdd.cc) · L34—L60。

接口参数：

- `FILE *fp`
- `const int verts_tot`
- `MDDHead *mdd_head`
- `const char **r_err_str`

**教学注释版**

<!-- annotated:4681fd363fc9a7 -->

```cpp
static bool meshcache_read_mdd_head(FILE *fp,
                                    const int verts_tot,
                                    MDDHead *mdd_head,
                                    const char **r_err_str)
{
  if (!fread(mdd_head, sizeof(*mdd_head), 1, fp)) {
    *r_err_str = RPT_("Missing header");
    return false;
  }

  /* NOTE: this is endianness-sensitive. */
  /* MDD is big-endian, its values need to be switched on little-endian systems. */
  BLI_endian_switch_int32_array(reinterpret_cast<int *>(mdd_head), 2);

  if (mdd_head->verts_tot != verts_tot) {
    *r_err_str = RPT_("Vertex count mismatch");
    return false;
  }

  if (mdd_head->frame_tot <= 0) {
    *r_err_str = RPT_("Invalid frame total");
    return false;
  }
  /* Intentionally don't seek back. */

  return true;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_meshcache_mdd.cc · L34—L60</summary>

<!-- original:4681fd363fc9a7:source/blender/modifiers/intern/MOD_meshcache_mdd.cc:34:60 -->

```cpp
static bool meshcache_read_mdd_head(FILE *fp,
                                    const int verts_tot,
                                    MDDHead *mdd_head,
                                    const char **r_err_str)
{
  if (!fread(mdd_head, sizeof(*mdd_head), 1, fp)) {
    *r_err_str = RPT_("Missing header");
    return false;
  }

  /* NOTE: this is endianness-sensitive. */
  /* MDD is big-endian, its values need to be switched on little-endian systems. */
  BLI_endian_switch_int32_array(reinterpret_cast<int *>(mdd_head), 2);

  if (mdd_head->verts_tot != verts_tot) {
    *r_err_str = RPT_("Vertex count mismatch");
    return false;
  }

  if (mdd_head->frame_tot <= 0) {
    *r_err_str = RPT_("Invalid frame total");
    return false;
  }
  /* Intentionally don't seek back. */

  return true;
}
```

</details>

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `fread` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L39。
- `RPT_` → [RPT_ · L51](%E4%BE%9D%E8%B5%96-BLT_translation-c89e58.md#m-c13f94a1a934)。宏定义由构建条件选择。
- `BLI_endian_switch_int32_array` → [blender::BLI_endian_switch_int32_array · L34](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-endian_switch-d88f86.md#f-404cc7db68d701cd)。

<a id="f-0c9e9993c8374f71"></a>

### `blender::meshcache_read_mdd_range`

实现位置：[source/blender/modifiers/intern/MOD_meshcache_mdd.cc](../../../../../source/blender/modifiers/intern/MOD_meshcache_mdd.cc) · L65—L84。

接口参数：

- `FILE *fp`
- `const int verts_tot`
- `const float frame`
- `const char interp`
- `int r_index_range[2]`
- `float *r_factor`
- `const char **r_err_str`

**教学注释版**

<!-- annotated:23ed0d533a92fe -->

```cpp
static bool meshcache_read_mdd_range(FILE *fp,
                                     const int verts_tot,
                                     const float frame,
                                     const char interp,
                                     int r_index_range[2],
                                     float *r_factor,
                                     const char **r_err_str)
{
  MDDHead mdd_head;

  /* first check interpolation and get the vert locations */

  if (meshcache_read_mdd_head(fp, verts_tot, &mdd_head, r_err_str) == false) {
    return false;
  }

  MOD_meshcache_calc_range(frame, interp, mdd_head.frame_tot, r_index_range, r_factor);

  return true;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_meshcache_mdd.cc · L65—L84</summary>

<!-- original:23ed0d533a92fe:source/blender/modifiers/intern/MOD_meshcache_mdd.cc:65:84 -->

```cpp
static bool meshcache_read_mdd_range(FILE *fp,
                                     const int verts_tot,
                                     const float frame,
                                     const char interp,
                                     int r_index_range[2],
                                     float *r_factor,
                                     const char **r_err_str)
{
  MDDHead mdd_head;

  /* first check interpolation and get the vert locations */

  if (meshcache_read_mdd_head(fp, verts_tot, &mdd_head, r_err_str) == false) {
    return false;
  }

  MOD_meshcache_calc_range(frame, interp, mdd_head.frame_tot, r_index_range, r_factor);

  return true;
}
```

</details>

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `meshcache_read_mdd_head` → [blender::meshcache_read_mdd_head · L34](%E4%BE%9D%E8%B5%96-MOD_meshcache_mdd-808e10.md#f-7e707d83d96e2e30)。
- `MOD_meshcache_calc_range` → [blender::MOD_meshcache_calc_range · L17](%E4%BE%9D%E8%B5%96-MOD_meshcache_util-8b8276.md#f-293a4803d3c64fd4)。

<a id="f-d32a515800373b5c"></a>

### `blender::meshcache_read_mdd_range_from_time`

实现位置：[source/blender/modifiers/intern/MOD_meshcache_mdd.cc](../../../../../source/blender/modifiers/intern/MOD_meshcache_mdd.cc) · L86—L139。

接口参数：

- `FILE *fp`
- `const int verts_tot`
- `const float time`
- `const float`
- `float *r_frame`
- `const char **r_err_str`

**教学注释版**

<!-- annotated:b9faefd20d579b -->

```cpp
static bool meshcache_read_mdd_range_from_time(FILE *fp,
                                               const int verts_tot,
                                               const float time,
                                               const float /*fps*/,
                                               float *r_frame,
                                               const char **r_err_str)
{
  MDDHead mdd_head;
  int i;
  float f_time, f_time_prev = FLT_MAX;
  float frame;

  if (meshcache_read_mdd_head(fp, verts_tot, &mdd_head, r_err_str) == false) {
    return false;
  }

  size_t frames_num_read = 0;
  size_t frames_num_expect = mdd_head.frame_tot;
  errno = 0;
  for (i = 0; i < mdd_head.frame_tot; i++) {
    frames_num_read += fread(&f_time, sizeof(float), 1, fp);
    /* NOTE: this is endianness-sensitive. */
    /* MDD is big-endian, its values need to be switched on little-endian systems. */
    BLI_endian_switch_float(&f_time);

    if (f_time >= time) {
      frames_num_expect = i + 1;
      break;
    }
    f_time_prev = f_time;
  }

  if (frames_num_read != frames_num_expect) {
    *r_err_str = errno ? strerror(errno) : RPT_("Timestamp read failed");
    return false;
  }

  if (f_time_prev == FLT_MAX) [[unlikely]] {
    frame = 0.0f;
  }
  else {
    const float range = f_time - f_time_prev;

    if (range <= FRAME_SNAP_EPS) {
      frame = float(i);
    }
    else {
      frame = float(i - 1) + ((time - f_time_prev) / range);
    }
  }

  *r_frame = frame;
  return true;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_meshcache_mdd.cc · L86—L139</summary>

<!-- original:b9faefd20d579b:source/blender/modifiers/intern/MOD_meshcache_mdd.cc:86:139 -->

```cpp
static bool meshcache_read_mdd_range_from_time(FILE *fp,
                                               const int verts_tot,
                                               const float time,
                                               const float /*fps*/,
                                               float *r_frame,
                                               const char **r_err_str)
{
  MDDHead mdd_head;
  int i;
  float f_time, f_time_prev = FLT_MAX;
  float frame;

  if (meshcache_read_mdd_head(fp, verts_tot, &mdd_head, r_err_str) == false) {
    return false;
  }

  size_t frames_num_read = 0;
  size_t frames_num_expect = mdd_head.frame_tot;
  errno = 0;
  for (i = 0; i < mdd_head.frame_tot; i++) {
    frames_num_read += fread(&f_time, sizeof(float), 1, fp);
    /* NOTE: this is endianness-sensitive. */
    /* MDD is big-endian, its values need to be switched on little-endian systems. */
    BLI_endian_switch_float(&f_time);

    if (f_time >= time) {
      frames_num_expect = i + 1;
      break;
    }
    f_time_prev = f_time;
  }

  if (frames_num_read != frames_num_expect) {
    *r_err_str = errno ? strerror(errno) : RPT_("Timestamp read failed");
    return false;
  }

  if (f_time_prev == FLT_MAX) [[unlikely]] {
    frame = 0.0f;
  }
  else {
    const float range = f_time - f_time_prev;

    if (range <= FRAME_SNAP_EPS) {
      frame = float(i);
    }
    else {
      frame = float(i - 1) + ((time - f_time_prev) / range);
    }
  }

  *r_frame = frame;
  return true;
}
```

</details>

**沿实际写入检查状态**

- `errno = 0;`
- `frames_num_read += fread(&f_time, sizeof(float), 1, fp);`
- `frames_num_expect = i + 1;`
- `f_time_prev = f_time;`
- `frame = 0.0f;`
- `frame = float(i);`
- `frame = float(i - 1) + ((time - f_time_prev) / range);`

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `meshcache_read_mdd_head` → [blender::meshcache_read_mdd_head · L34](%E4%BE%9D%E8%B5%96-MOD_meshcache_mdd-808e10.md#f-7e707d83d96e2e30)。
- `fread` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L106。
- `BLI_endian_switch_float` → [blender::BLI_endian_switch_float · L55](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_endian_switch_inline-fbfa0a.md#f-188b4b205db6042e)。
- `strerror` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L119。
- `RPT_` → [RPT_ · L51](%E4%BE%9D%E8%B5%96-BLT_translation-c89e58.md#m-c13f94a1a934)。宏定义由构建条件选择。

<a id="f-c28445e045f2c294"></a>

### `blender::MOD_meshcache_read_mdd_index`

实现位置：[source/blender/modifiers/intern/MOD_meshcache_mdd.cc](../../../../../source/blender/modifiers/intern/MOD_meshcache_mdd.cc) · L141—L216。

接口参数：

- `FILE *fp`
- `float (*vertexCos)[3]`
- `const int verts_tot`
- `const int index`
- `const float factor`
- `const char **r_err_str`

**教学注释版**

<!-- annotated:f52afca234b8d5 -->

```cpp
bool MOD_meshcache_read_mdd_index(FILE *fp,
                                  float (*vertexCos)[3],
                                  const int verts_tot,
                                  const int index,
                                  const float factor,
                                  const char **r_err_str)
{
  MDDHead mdd_head;

  if (meshcache_read_mdd_head(fp, verts_tot, &mdd_head, r_err_str) == false) {
    return false;
  }

  if (BLI_fseek(fp, mdd_head.frame_tot * sizeof(int), SEEK_CUR) != 0) {
    *r_err_str = RPT_("Header seek failed");
    return false;
  }

  if (BLI_fseek(fp, sizeof(float[3]) * index * mdd_head.verts_tot, SEEK_CUR) != 0) {
    *r_err_str = RPT_("Failed to seek frame");
    return false;
  }

  size_t verts_read_num = 0;
  errno = 0;
  if (factor >= 1.0f) {
#if 1
    float *vco = *vertexCos;
    uint i;
    for (i = mdd_head.verts_tot; i != 0; i--, vco += 3) {
      verts_read_num += fread(vco, sizeof(float[3]), 1, fp);

      /* NOTE: this is endianness-sensitive. */
      /* MDD is big-endian, its values need to be switched on little-endian systems. */
      BLI_endian_switch_float(vco + 0);
      BLI_endian_switch_float(vco + 1);
      BLI_endian_switch_float(vco + 2);
    }
#else
    /* no blending */
    if (!fread(vertexCos, sizeof(float[3]), mdd_head.verts_tot, f)) {
      *r_err_str = errno ? strerror(errno) : RPT_("Failed to read frame");
      return false;
    }
    /* NOTE: this is endianness-sensitive. */
    /* MDD is big-endian, its values need to be switched on little-endian systems. */
    BLI_endian_switch_float_array(vertexCos[0], mdd_head.verts_tot * 3);
#endif
  }
  else {
    const float ifactor = 1.0f - factor;
    float *vco = *vertexCos;
    uint i;
    for (i = mdd_head.verts_tot; i != 0; i--, vco += 3) {
      float tvec[3];
      verts_read_num += fread(tvec, sizeof(float[3]), 1, fp);

      /* NOTE: this is endianness-sensitive. */
      /* MDD is big-endian, its values need to be switched on little-endian systems. */
      BLI_endian_switch_float(tvec + 0);
      BLI_endian_switch_float(tvec + 1);
      BLI_endian_switch_float(tvec + 2);

      vco[0] = (vco[0] * ifactor) + (tvec[0] * factor);
      vco[1] = (vco[1] * ifactor) + (tvec[1] * factor);
      vco[2] = (vco[2] * ifactor) + (tvec[2] * factor);
    }
  }

  if (verts_read_num != mdd_head.verts_tot) {
    *r_err_str = errno ? strerror(errno) : RPT_("Vertex coordinate read failed");
    return false;
  }

  return true;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_meshcache_mdd.cc · L141—L216</summary>

<!-- original:f52afca234b8d5:source/blender/modifiers/intern/MOD_meshcache_mdd.cc:141:216 -->

```cpp
bool MOD_meshcache_read_mdd_index(FILE *fp,
                                  float (*vertexCos)[3],
                                  const int verts_tot,
                                  const int index,
                                  const float factor,
                                  const char **r_err_str)
{
  MDDHead mdd_head;

  if (meshcache_read_mdd_head(fp, verts_tot, &mdd_head, r_err_str) == false) {
    return false;
  }

  if (BLI_fseek(fp, mdd_head.frame_tot * sizeof(int), SEEK_CUR) != 0) {
    *r_err_str = RPT_("Header seek failed");
    return false;
  }

  if (BLI_fseek(fp, sizeof(float[3]) * index * mdd_head.verts_tot, SEEK_CUR) != 0) {
    *r_err_str = RPT_("Failed to seek frame");
    return false;
  }

  size_t verts_read_num = 0;
  errno = 0;
  if (factor >= 1.0f) {
#if 1
    float *vco = *vertexCos;
    uint i;
    for (i = mdd_head.verts_tot; i != 0; i--, vco += 3) {
      verts_read_num += fread(vco, sizeof(float[3]), 1, fp);

      /* NOTE: this is endianness-sensitive. */
      /* MDD is big-endian, its values need to be switched on little-endian systems. */
      BLI_endian_switch_float(vco + 0);
      BLI_endian_switch_float(vco + 1);
      BLI_endian_switch_float(vco + 2);
    }
#else
    /* no blending */
    if (!fread(vertexCos, sizeof(float[3]), mdd_head.verts_tot, f)) {
      *r_err_str = errno ? strerror(errno) : RPT_("Failed to read frame");
      return false;
    }
    /* NOTE: this is endianness-sensitive. */
    /* MDD is big-endian, its values need to be switched on little-endian systems. */
    BLI_endian_switch_float_array(vertexCos[0], mdd_head.verts_tot * 3);
#endif
  }
  else {
    const float ifactor = 1.0f - factor;
    float *vco = *vertexCos;
    uint i;
    for (i = mdd_head.verts_tot; i != 0; i--, vco += 3) {
      float tvec[3];
      verts_read_num += fread(tvec, sizeof(float[3]), 1, fp);

      /* NOTE: this is endianness-sensitive. */
      /* MDD is big-endian, its values need to be switched on little-endian systems. */
      BLI_endian_switch_float(tvec + 0);
      BLI_endian_switch_float(tvec + 1);
      BLI_endian_switch_float(tvec + 2);

      vco[0] = (vco[0] * ifactor) + (tvec[0] * factor);
      vco[1] = (vco[1] * ifactor) + (tvec[1] * factor);
      vco[2] = (vco[2] * ifactor) + (tvec[2] * factor);
    }
  }

  if (verts_read_num != mdd_head.verts_tot) {
    *r_err_str = errno ? strerror(errno) : RPT_("Vertex coordinate read failed");
    return false;
  }

  return true;
}
```

</details>

**沿实际写入检查状态**

- `errno = 0;`
- `verts_read_num += fread(vco, sizeof(float[3]), 1, fp);`
- `verts_read_num += fread(tvec, sizeof(float[3]), 1, fp);`
- `vco[0] = (vco[0] * ifactor) + (tvec[0] * factor);`
- `vco[1] = (vco[1] * ifactor) + (tvec[1] * factor);`
- `vco[2] = (vco[2] * ifactor) + (tvec[2] * factor);`

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `meshcache_read_mdd_head` → [blender::meshcache_read_mdd_head · L34](%E4%BE%9D%E8%B5%96-MOD_meshcache_mdd-808e10.md#f-7e707d83d96e2e30)。
- `BLI_fseek` → [blender::BLI_fseek · L201](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-storage-bda15e.md#f-66c5f3581da90506)。
- `RPT_` → [RPT_ · L51](%E4%BE%9D%E8%B5%96-BLT_translation-c89e58.md#m-c13f94a1a934)。宏定义由构建条件选择。
- `fread` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L171。
- `BLI_endian_switch_float` → [blender::BLI_endian_switch_float · L55](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_endian_switch_inline-fbfa0a.md#f-188b4b205db6042e)。
- `strerror` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L182。
- `BLI_endian_switch_float_array` → [blender::BLI_endian_switch_float_array · L54](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-endian_switch-d88f86.md#f-e06703b685f019f8)。

<a id="f-605ea10c0bd789cc"></a>

### `blender::MOD_meshcache_read_mdd_frame`

实现位置：[source/blender/modifiers/intern/MOD_meshcache_mdd.cc](../../../../../source/blender/modifiers/intern/MOD_meshcache_mdd.cc) · L218—L260。

接口参数：

- `FILE *fp`
- `float (*vertexCos)[3]`
- `const int verts_tot`
- `const char interp`
- `const float frame`
- `const char **r_err_str`

**教学注释版**

<!-- annotated:35b39872fd3c04 -->

```cpp
bool MOD_meshcache_read_mdd_frame(FILE *fp,
                                  float (*vertexCos)[3],
                                  const int verts_tot,
                                  const char interp,
                                  const float frame,
                                  const char **r_err_str)
{
  int index_range[2];
  float factor;

  if (meshcache_read_mdd_range(fp,
                               verts_tot,
                               frame,
                               interp,
                               index_range,
                               &factor, /* read into these values */
                               r_err_str) == false)
  {
    return false;
  }

  if (index_range[0] == index_range[1]) {
    /* read single */
    if ((BLI_fseek(fp, 0, SEEK_SET) == 0) &&
        MOD_meshcache_read_mdd_index(fp, vertexCos, verts_tot, index_range[0], 1.0f, r_err_str))
    {
      return true;
    }

    return false;
  }

  /* read both and interpolate */
  if ((BLI_fseek(fp, 0, SEEK_SET) == 0) &&
      MOD_meshcache_read_mdd_index(fp, vertexCos, verts_tot, index_range[0], 1.0f, r_err_str) &&
      (BLI_fseek(fp, 0, SEEK_SET) == 0) &&
      MOD_meshcache_read_mdd_index(fp, vertexCos, verts_tot, index_range[1], factor, r_err_str))
  {
    return true;
  }

  return false;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_meshcache_mdd.cc · L218—L260</summary>

<!-- original:35b39872fd3c04:source/blender/modifiers/intern/MOD_meshcache_mdd.cc:218:260 -->

```cpp
bool MOD_meshcache_read_mdd_frame(FILE *fp,
                                  float (*vertexCos)[3],
                                  const int verts_tot,
                                  const char interp,
                                  const float frame,
                                  const char **r_err_str)
{
  int index_range[2];
  float factor;

  if (meshcache_read_mdd_range(fp,
                               verts_tot,
                               frame,
                               interp,
                               index_range,
                               &factor, /* read into these values */
                               r_err_str) == false)
  {
    return false;
  }

  if (index_range[0] == index_range[1]) {
    /* read single */
    if ((BLI_fseek(fp, 0, SEEK_SET) == 0) &&
        MOD_meshcache_read_mdd_index(fp, vertexCos, verts_tot, index_range[0], 1.0f, r_err_str))
    {
      return true;
    }

    return false;
  }

  /* read both and interpolate */
  if ((BLI_fseek(fp, 0, SEEK_SET) == 0) &&
      MOD_meshcache_read_mdd_index(fp, vertexCos, verts_tot, index_range[0], 1.0f, r_err_str) &&
      (BLI_fseek(fp, 0, SEEK_SET) == 0) &&
      MOD_meshcache_read_mdd_index(fp, vertexCos, verts_tot, index_range[1], factor, r_err_str))
  {
    return true;
  }

  return false;
}
```

</details>

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `meshcache_read_mdd_range` → [blender::meshcache_read_mdd_range · L65](%E4%BE%9D%E8%B5%96-MOD_meshcache_mdd-808e10.md#f-0c9e9993c8374f71)。
- `BLI_fseek` → [blender::BLI_fseek · L201](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-storage-bda15e.md#f-66c5f3581da90506)。
- `MOD_meshcache_read_mdd_index` → [blender::MOD_meshcache_read_mdd_index · L141](%E4%BE%9D%E8%B5%96-MOD_meshcache_mdd-808e10.md#f-c28445e045f2c294)。

<a id="f-09fbd6eae70b300d"></a>

### `blender::MOD_meshcache_read_mdd_times`

实现位置：[source/blender/modifiers/intern/MOD_meshcache_mdd.cc](../../../../../source/blender/modifiers/intern/MOD_meshcache_mdd.cc) · L262—L314。

接口参数：

- `const char *filepath`
- `float (*vertexCos)[3]`
- `const int verts_tot`
- `const char interp`
- `const float time`
- `const float fps`
- `const char time_mode`
- `const char **r_err_str`

**教学注释版**

<!-- annotated:c1e0ea10f924a7 -->

```cpp
bool MOD_meshcache_read_mdd_times(const char *filepath,
                                  float (*vertexCos)[3],
                                  const int verts_tot,
                                  const char interp,
                                  const float time,
                                  const float fps,
                                  const char time_mode,
                                  const char **r_err_str)
{
  float frame;

  FILE *fp = BLI_fopen(filepath, "rb");
  bool ok;

  if (fp == nullptr) {
    *r_err_str = errno ? strerror(errno) : RPT_("Unknown error opening file");
    return false;
  }

  switch (time_mode) {
    case MOD_MESHCACHE_TIME_FRAME: {
      frame = time;
      break;
    }
    case MOD_MESHCACHE_TIME_SECONDS: {
      /* we need to find the closest time */
      if (meshcache_read_mdd_range_from_time(fp, verts_tot, time, fps, &frame, r_err_str) == false)
      {
        fclose(fp);
        return false;
      }
      rewind(fp);
      break;
    }
    case MOD_MESHCACHE_TIME_FACTOR:
    default: {
      MDDHead mdd_head;
      if (meshcache_read_mdd_head(fp, verts_tot, &mdd_head, r_err_str) == false) {
        fclose(fp);
        return false;
      }

      frame = std::clamp(time, 0.0f, 1.0f) * float(mdd_head.frame_tot);
      rewind(fp);
      break;
    }
  }

  ok = MOD_meshcache_read_mdd_frame(fp, vertexCos, verts_tot, interp, frame, r_err_str);

  fclose(fp);
  return ok;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_meshcache_mdd.cc · L262—L314</summary>

<!-- original:c1e0ea10f924a7:source/blender/modifiers/intern/MOD_meshcache_mdd.cc:262:314 -->

```cpp
bool MOD_meshcache_read_mdd_times(const char *filepath,
                                  float (*vertexCos)[3],
                                  const int verts_tot,
                                  const char interp,
                                  const float time,
                                  const float fps,
                                  const char time_mode,
                                  const char **r_err_str)
{
  float frame;

  FILE *fp = BLI_fopen(filepath, "rb");
  bool ok;

  if (fp == nullptr) {
    *r_err_str = errno ? strerror(errno) : RPT_("Unknown error opening file");
    return false;
  }

  switch (time_mode) {
    case MOD_MESHCACHE_TIME_FRAME: {
      frame = time;
      break;
    }
    case MOD_MESHCACHE_TIME_SECONDS: {
      /* we need to find the closest time */
      if (meshcache_read_mdd_range_from_time(fp, verts_tot, time, fps, &frame, r_err_str) == false)
      {
        fclose(fp);
        return false;
      }
      rewind(fp);
      break;
    }
    case MOD_MESHCACHE_TIME_FACTOR:
    default: {
      MDDHead mdd_head;
      if (meshcache_read_mdd_head(fp, verts_tot, &mdd_head, r_err_str) == false) {
        fclose(fp);
        return false;
      }

      frame = std::clamp(time, 0.0f, 1.0f) * float(mdd_head.frame_tot);
      rewind(fp);
      break;
    }
  }

  ok = MOD_meshcache_read_mdd_frame(fp, vertexCos, verts_tot, interp, frame, r_err_str);

  fclose(fp);
  return ok;
}
```

</details>

**沿实际写入检查状态**

- `frame = time;`
- `frame = std::clamp(time, 0.0f, 1.0f) * float(mdd_head.frame_tot);`
- `ok = MOD_meshcache_read_mdd_frame(fp, vertexCos, verts_tot, interp, frame, r_err_str);`

**结果出口**

- `return false;`
- `return ok;`

**继续追踪实现**

- `BLI_fopen` → [blender::BLI_fopen · L558](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-fileops_c-add581.md#f-c6d3cebeeea3cab3)；[blender::BLI_fopen · L1185](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-fileops_c-add581.md#f-d834ce38c568c49a)。同名重载需按实参类型选择。
- `strerror` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L277。
- `RPT_` → [RPT_ · L51](%E4%BE%9D%E8%B5%96-BLT_translation-c89e58.md#m-c13f94a1a934)。宏定义由构建条件选择。
- `meshcache_read_mdd_range_from_time` → [blender::meshcache_read_mdd_range_from_time · L86](%E4%BE%9D%E8%B5%96-MOD_meshcache_mdd-808e10.md#f-d32a515800373b5c)。
- `fclose` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L290。
- `rewind` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L293。
- `meshcache_read_mdd_head` → [blender::meshcache_read_mdd_head · L34](%E4%BE%9D%E8%B5%96-MOD_meshcache_mdd-808e10.md#f-7e707d83d96e2e30)。
- `std::clamp` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `MOD_meshcache_read_mdd_frame` → [blender::MOD_meshcache_read_mdd_frame · L218](%E4%BE%9D%E8%B5%96-MOD_meshcache_mdd-808e10.md#f-605ea10c0bd789cc)。
