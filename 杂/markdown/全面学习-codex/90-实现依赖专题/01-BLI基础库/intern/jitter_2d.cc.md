# 实现依赖专题：source/blender/blenlib/intern/jitter_2d.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::BLI_jitterate1"]:::abstraction
  F1["blender::BLI_jitterate2"]:::compute
  F2["blender::BLI_jitter_init"]:::compute
  F2 -->|"显式调用"| F0
  F2 -->|"显式调用"| F1
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
  F["jitter_2d.cc实现"]:::compute
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

<a id="f-448acb6346acbd67"></a>

### `blender::BLI_jitterate1`

实现位置：[source/blender/blenlib/intern/jitter_2d.cc](../../../../../../../source/blender/blenlib/intern/jitter_2d.cc) · L21—L77。

接口参数：

- `float (*jit1)[2]`
- `float (*jit2)[2]`
- `int num`
- `float radius1`

**教学注释版**

<!-- annotated:fe01e6578c42c7 -->

```cpp
void BLI_jitterate1(float (*jit1)[2], float (*jit2)[2], int num, float radius1)
{
  int i, j, k;
  float vecx, vecy, dvecx, dvecy, x, y, len;

  for (i = num - 1; i >= 0; i--) {
    dvecx = dvecy = 0.0;
    x = jit1[i][0];
    y = jit1[i][1];
    for (j = num - 1; j >= 0; j--) {
      if (i != j) {
        vecx = jit1[j][0] - x - 1.0f;
        vecy = jit1[j][1] - y - 1.0f;
        for (k = 3; k > 0; k--) {
          if (fabsf(vecx) < radius1 && fabsf(vecy) < radius1) {
            len = sqrtf(vecx * vecx + vecy * vecy);
            if (len > 0 && len < radius1) {
              len = len / radius1;
              dvecx += vecx / len;
              dvecy += vecy / len;
            }
          }
          vecx += 1.0f;

          if (fabsf(vecx) < radius1 && fabsf(vecy) < radius1) {
            len = sqrtf(vecx * vecx + vecy * vecy);
            if (len > 0 && len < radius1) {
              len = len / radius1;
              dvecx += vecx / len;
              dvecy += vecy / len;
            }
          }
          vecx += 1.0f;

          if (fabsf(vecx) < radius1 && fabsf(vecy) < radius1) {
            len = sqrtf(vecx * vecx + vecy * vecy);
            if (len > 0 && len < radius1) {
              len = len / radius1;
              dvecx += vecx / len;
              dvecy += vecy / len;
            }
          }
          vecx -= 2.0f;
          vecy += 1.0f;
        }
      }
    }

    x -= dvecx / 18.0f;
    y -= dvecy / 18.0f;
    x -= floorf(x);
    y -= floorf(y);
    jit2[i][0] = x;
    jit2[i][1] = y;
  }
  // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
  memcpy(jit1, jit2, 2 * uint(num) * sizeof(float));
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/jitter_2d.cc · L21—L77</summary>

<!-- original:fe01e6578c42c7:source/blender/blenlib/intern/jitter_2d.cc:21:77 -->

```cpp
void BLI_jitterate1(float (*jit1)[2], float (*jit2)[2], int num, float radius1)
{
  int i, j, k;
  float vecx, vecy, dvecx, dvecy, x, y, len;

  for (i = num - 1; i >= 0; i--) {
    dvecx = dvecy = 0.0;
    x = jit1[i][0];
    y = jit1[i][1];
    for (j = num - 1; j >= 0; j--) {
      if (i != j) {
        vecx = jit1[j][0] - x - 1.0f;
        vecy = jit1[j][1] - y - 1.0f;
        for (k = 3; k > 0; k--) {
          if (fabsf(vecx) < radius1 && fabsf(vecy) < radius1) {
            len = sqrtf(vecx * vecx + vecy * vecy);
            if (len > 0 && len < radius1) {
              len = len / radius1;
              dvecx += vecx / len;
              dvecy += vecy / len;
            }
          }
          vecx += 1.0f;

          if (fabsf(vecx) < radius1 && fabsf(vecy) < radius1) {
            len = sqrtf(vecx * vecx + vecy * vecy);
            if (len > 0 && len < radius1) {
              len = len / radius1;
              dvecx += vecx / len;
              dvecy += vecy / len;
            }
          }
          vecx += 1.0f;

          if (fabsf(vecx) < radius1 && fabsf(vecy) < radius1) {
            len = sqrtf(vecx * vecx + vecy * vecy);
            if (len > 0 && len < radius1) {
              len = len / radius1;
              dvecx += vecx / len;
              dvecy += vecy / len;
            }
          }
          vecx -= 2.0f;
          vecy += 1.0f;
        }
      }
    }

    x -= dvecx / 18.0f;
    y -= dvecy / 18.0f;
    x -= floorf(x);
    y -= floorf(y);
    jit2[i][0] = x;
    jit2[i][1] = y;
  }
  memcpy(jit1, jit2, 2 * uint(num) * sizeof(float));
}
```

</details>

**沿实际写入检查状态**

- `dvecx = dvecy = 0.0;`
- `x = jit1[i][0];`
- `y = jit1[i][1];`
- `vecx = jit1[j][0] - x - 1.0f;`
- `vecy = jit1[j][1] - y - 1.0f;`
- `len = sqrtf(vecx * vecx + vecy * vecy);`
- `len = len / radius1;`
- `dvecx += vecx / len;`
- `dvecy += vecy / len;`
- `vecx += 1.0f;`
- `vecx -= 2.0f;`
- `vecy += 1.0f;`
- `x -= dvecx / 18.0f;`
- `y -= dvecy / 18.0f;`
- `x -= floorf(x);`
- `y -= floorf(y);`
- `jit2[i][0] = x;`
- `jit2[i][1] = y;`

**继续追踪实现**

- `fabsf` → [fabsf · L21](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-02cc4c69cfb3)；[fabsf · L43](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-04effe61803b)；[fabsf · L74](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-927dd4eba7dc)；[fabsf · L25](radial_tiling_shared.hh.md#m-8348d6b3d08f)；[fabsf · L47](radial_tiling_shared.hh.md#m-13b7e0b6d84f)；[fabsf · L78](radial_tiling_shared.hh.md#m-326c83464a0d)；[fabsf · L21](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-7c3ee12fc119)；[fabsf · L43](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-9112db0e2dd1)；[fabsf · L74](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-ee4e61908a6f)；[fabsf · L167](../../07-Intern运行时与平台/cycles/kernel/device/oneapi/compat.h.md#m-b039ee6c1601)；[fabsf · L265](../../07-Intern运行时与平台/cycles/kernel/device/metal/compat.h.md#m-6b21869e9f3f)。宏定义由构建条件选择。
- `sqrtf` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `floorf` → [floorf · L22](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-fb64dda1b0f0)；[floorf · L44](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-25e4a157b53d)；[floorf · L75](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-e128f662cbe8)；[floorf · L26](radial_tiling_shared.hh.md#m-ebadf845d492)；[floorf · L48](radial_tiling_shared.hh.md#m-efe0b148573a)；[floorf · L79](radial_tiling_shared.hh.md#m-9df2f26758e8)；[floorf · L22](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-6b2e29ad4b19)；[floorf · L44](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-f90222d9b445)；[floorf · L75](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-938380992bb5)；[floorf · L172](../../07-Intern运行时与平台/cycles/kernel/device/oneapi/compat.h.md#m-176475a253a6)；[floorf · L270](../../07-Intern运行时与平台/cycles/kernel/device/metal/compat.h.md#m-fb37dbc77698)；[floorf · L49](../../08-其他Blender模块/gpu/GPU_shader_shared_utils.hh.md#m-e7115fdd7560)；[floorf · L70](../../08-其他Blender模块/gpu/GPU_shader_shared_utils.hh.md#m-aee5f6a438e4)。宏定义由构建条件选择。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。

<a id="f-ea1f41c34facd5aa"></a>

### `blender::BLI_jitterate2`

实现位置：[source/blender/blenlib/intern/jitter_2d.cc](../../../../../../../source/blender/blenlib/intern/jitter_2d.cc) · L79—L127。

接口参数：

- `float (*jit1)[2]`
- `float (*jit2)[2]`
- `int num`
- `float radius2`

**教学注释版**

<!-- annotated:d432ed787d9cc7 -->

```cpp
void BLI_jitterate2(float (*jit1)[2], float (*jit2)[2], int num, float radius2)
{
  int i, j;
  float vecx, vecy, dvecx, dvecy, x, y;

  for (i = num - 1; i >= 0; i--) {
    dvecx = dvecy = 0.0;
    x = jit1[i][0];
    y = jit1[i][1];
    for (j = num - 1; j >= 0; j--) {
      if (i != j) {
        vecx = jit1[j][0] - x - 1.0f;
        vecy = jit1[j][1] - y - 1.0f;

        if (fabsf(vecx) < radius2) {
          dvecx += vecx * radius2;
        }
        vecx += 1.0f;
        if (fabsf(vecx) < radius2) {
          dvecx += vecx * radius2;
        }
        vecx += 1.0f;
        if (fabsf(vecx) < radius2) {
          dvecx += vecx * radius2;
        }

        if (fabsf(vecy) < radius2) {
          dvecy += vecy * radius2;
        }
        vecy += 1.0f;
        if (fabsf(vecy) < radius2) {
          dvecy += vecy * radius2;
        }
        vecy += 1.0f;
        if (fabsf(vecy) < radius2) {
          dvecy += vecy * radius2;
        }
      }
    }

    x -= dvecx / 2.0f;
    y -= dvecy / 2.0f;
    x -= floorf(x);
    y -= floorf(y);
    jit2[i][0] = x;
    jit2[i][1] = y;
  }
  // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
  memcpy(jit1, jit2, uint(num) * sizeof(float[2]));
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/jitter_2d.cc · L79—L127</summary>

<!-- original:d432ed787d9cc7:source/blender/blenlib/intern/jitter_2d.cc:79:127 -->

```cpp
void BLI_jitterate2(float (*jit1)[2], float (*jit2)[2], int num, float radius2)
{
  int i, j;
  float vecx, vecy, dvecx, dvecy, x, y;

  for (i = num - 1; i >= 0; i--) {
    dvecx = dvecy = 0.0;
    x = jit1[i][0];
    y = jit1[i][1];
    for (j = num - 1; j >= 0; j--) {
      if (i != j) {
        vecx = jit1[j][0] - x - 1.0f;
        vecy = jit1[j][1] - y - 1.0f;

        if (fabsf(vecx) < radius2) {
          dvecx += vecx * radius2;
        }
        vecx += 1.0f;
        if (fabsf(vecx) < radius2) {
          dvecx += vecx * radius2;
        }
        vecx += 1.0f;
        if (fabsf(vecx) < radius2) {
          dvecx += vecx * radius2;
        }

        if (fabsf(vecy) < radius2) {
          dvecy += vecy * radius2;
        }
        vecy += 1.0f;
        if (fabsf(vecy) < radius2) {
          dvecy += vecy * radius2;
        }
        vecy += 1.0f;
        if (fabsf(vecy) < radius2) {
          dvecy += vecy * radius2;
        }
      }
    }

    x -= dvecx / 2.0f;
    y -= dvecy / 2.0f;
    x -= floorf(x);
    y -= floorf(y);
    jit2[i][0] = x;
    jit2[i][1] = y;
  }
  memcpy(jit1, jit2, uint(num) * sizeof(float[2]));
}
```

</details>

**沿实际写入检查状态**

- `dvecx = dvecy = 0.0;`
- `x = jit1[i][0];`
- `y = jit1[i][1];`
- `vecx = jit1[j][0] - x - 1.0f;`
- `vecy = jit1[j][1] - y - 1.0f;`
- `dvecx += vecx * radius2;`
- `vecx += 1.0f;`
- `dvecy += vecy * radius2;`
- `vecy += 1.0f;`
- `x -= dvecx / 2.0f;`
- `y -= dvecy / 2.0f;`
- `x -= floorf(x);`
- `y -= floorf(y);`
- `jit2[i][0] = x;`
- `jit2[i][1] = y;`

**继续追踪实现**

- `fabsf` → [fabsf · L21](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-02cc4c69cfb3)；[fabsf · L43](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-04effe61803b)；[fabsf · L74](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-927dd4eba7dc)；[fabsf · L25](radial_tiling_shared.hh.md#m-8348d6b3d08f)；[fabsf · L47](radial_tiling_shared.hh.md#m-13b7e0b6d84f)；[fabsf · L78](radial_tiling_shared.hh.md#m-326c83464a0d)；[fabsf · L21](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-7c3ee12fc119)；[fabsf · L43](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-9112db0e2dd1)；[fabsf · L74](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-ee4e61908a6f)；[fabsf · L167](../../07-Intern运行时与平台/cycles/kernel/device/oneapi/compat.h.md#m-b039ee6c1601)；[fabsf · L265](../../07-Intern运行时与平台/cycles/kernel/device/metal/compat.h.md#m-6b21869e9f3f)。宏定义由构建条件选择。
- `floorf` → [floorf · L22](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-fb64dda1b0f0)；[floorf · L44](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-25e4a157b53d)；[floorf · L75](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-e128f662cbe8)；[floorf · L26](radial_tiling_shared.hh.md#m-ebadf845d492)；[floorf · L48](radial_tiling_shared.hh.md#m-efe0b148573a)；[floorf · L79](radial_tiling_shared.hh.md#m-9df2f26758e8)；[floorf · L22](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-6b2e29ad4b19)；[floorf · L44](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-f90222d9b445)；[floorf · L75](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-938380992bb5)；[floorf · L172](../../07-Intern运行时与平台/cycles/kernel/device/oneapi/compat.h.md#m-176475a253a6)；[floorf · L270](../../07-Intern运行时与平台/cycles/kernel/device/metal/compat.h.md#m-fb37dbc77698)；[floorf · L49](../../08-其他Blender模块/gpu/GPU_shader_shared_utils.hh.md#m-e7115fdd7560)；[floorf · L70](../../08-其他Blender模块/gpu/GPU_shader_shared_utils.hh.md#m-aee5f6a438e4)。宏定义由构建条件选择。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。

<a id="f-4973891f06af9586"></a>

### `blender::BLI_jitter_init`

实现位置：[source/blender/blenlib/intern/jitter_2d.cc](../../../../../../../source/blender/blenlib/intern/jitter_2d.cc) · L129—L174。

接口参数：

- `float (*jitarr)[2]`
- `int num`

**教学注释版**

<!-- annotated:c4fab9ce60be4a -->

```cpp
void BLI_jitter_init(float (*jitarr)[2], int num)
{
  float (*jit2)[2];
  float number_fl, number_fl_sqrt;
  float x, rad1, rad2, rad3;
  RNG *rng;
  int i;

  if (num == 0) {
    return;
  }

  number_fl = float(num);
  number_fl_sqrt = sqrtf(number_fl);

  jit2 = MEM_new_array_uninitialized<float[2]>(2 + size_t(num), "initjit");
  rad1 = 1.0f / number_fl_sqrt;
  rad2 = 1.0f / number_fl;
  rad3 = number_fl_sqrt / number_fl;

  rng = BLI_rng_new(31415926 + uint(num));

  x = 0;
  for (i = 0; i < num; i++) {
    jitarr[i][0] = x + rad1 * float(0.5 - BLI_rng_get_double(rng));
    jitarr[i][1] = float(i) / number_fl + rad1 * float(0.5 - BLI_rng_get_double(rng));
    x += rad3;
    x -= floorf(x);
  }

  BLI_rng_free(rng);

  for (i = 0; i < 24; i++) {
    BLI_jitterate1(jitarr, jit2, num, rad1);
    BLI_jitterate1(jitarr, jit2, num, rad1);
    BLI_jitterate2(jitarr, jit2, num, rad2);
  }

  MEM_delete(jit2);

  /* Finally, move jitter to be centered around (0, 0). */
  for (i = 0; i < num; i++) {
    jitarr[i][0] -= 0.5f;
    jitarr[i][1] -= 0.5f;
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/jitter_2d.cc · L129—L174</summary>

<!-- original:c4fab9ce60be4a:source/blender/blenlib/intern/jitter_2d.cc:129:174 -->

```cpp
void BLI_jitter_init(float (*jitarr)[2], int num)
{
  float (*jit2)[2];
  float number_fl, number_fl_sqrt;
  float x, rad1, rad2, rad3;
  RNG *rng;
  int i;

  if (num == 0) {
    return;
  }

  number_fl = float(num);
  number_fl_sqrt = sqrtf(number_fl);

  jit2 = MEM_new_array_uninitialized<float[2]>(2 + size_t(num), "initjit");
  rad1 = 1.0f / number_fl_sqrt;
  rad2 = 1.0f / number_fl;
  rad3 = number_fl_sqrt / number_fl;

  rng = BLI_rng_new(31415926 + uint(num));

  x = 0;
  for (i = 0; i < num; i++) {
    jitarr[i][0] = x + rad1 * float(0.5 - BLI_rng_get_double(rng));
    jitarr[i][1] = float(i) / number_fl + rad1 * float(0.5 - BLI_rng_get_double(rng));
    x += rad3;
    x -= floorf(x);
  }

  BLI_rng_free(rng);

  for (i = 0; i < 24; i++) {
    BLI_jitterate1(jitarr, jit2, num, rad1);
    BLI_jitterate1(jitarr, jit2, num, rad1);
    BLI_jitterate2(jitarr, jit2, num, rad2);
  }

  MEM_delete(jit2);

  /* Finally, move jitter to be centered around (0, 0). */
  for (i = 0; i < num; i++) {
    jitarr[i][0] -= 0.5f;
    jitarr[i][1] -= 0.5f;
  }
}
```

</details>

**沿实际写入检查状态**

- `number_fl = float(num);`
- `number_fl_sqrt = sqrtf(number_fl);`
- `jit2 = MEM_new_array_uninitialized<float[2]>(2 + size_t(num), "initjit");`
- `rad1 = 1.0f / number_fl_sqrt;`
- `rad2 = 1.0f / number_fl;`
- `rad3 = number_fl_sqrt / number_fl;`
- `rng = BLI_rng_new(31415926 + uint(num));`
- `x = 0;`
- `jitarr[i][0] = x + rad1 * float(0.5 - BLI_rng_get_double(rng));`
- `jitarr[i][1] = float(i) / number_fl + rad1 * float(0.5 - BLI_rng_get_double(rng));`
- `x += rad3;`
- `x -= floorf(x);`
- `jitarr[i][0] -= 0.5f;`
- `jitarr[i][1] -= 0.5f;`

**继续追踪实现**

- `sqrtf` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `MEM_new_array_uninitialized<float[2]>` → [MEM_new_array_uninitialized · L608](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-b7103eae8eb57b05)；[MEM_new_array_uninitialized · L129](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-bf6ef4ddcfb6e5df)。同名重载需按实参类型选择。
- `BLI_rng_new` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L149。
- `BLI_rng_get_double` → [RNG::BLI_rng_get_double · L85](rand.cc.md#f-84f75c207b68570c)。
- `floorf` → [floorf · L22](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-fb64dda1b0f0)；[floorf · L44](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-25e4a157b53d)；[floorf · L75](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-e128f662cbe8)；[floorf · L26](radial_tiling_shared.hh.md#m-ebadf845d492)；[floorf · L48](radial_tiling_shared.hh.md#m-efe0b148573a)；[floorf · L79](radial_tiling_shared.hh.md#m-9df2f26758e8)；[floorf · L22](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-6b2e29ad4b19)；[floorf · L44](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-f90222d9b445)；[floorf · L75](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-938380992bb5)；[floorf · L172](../../07-Intern运行时与平台/cycles/kernel/device/oneapi/compat.h.md#m-176475a253a6)；[floorf · L270](../../07-Intern运行时与平台/cycles/kernel/device/metal/compat.h.md#m-fb37dbc77698)；[floorf · L49](../../08-其他Blender模块/gpu/GPU_shader_shared_utils.hh.md#m-e7115fdd7560)；[floorf · L70](../../08-其他Blender模块/gpu/GPU_shader_shared_utils.hh.md#m-aee5f6a438e4)。宏定义由构建条件选择。
- `BLI_rng_free` → [RNG::BLI_rng_free · L55](rand.cc.md#f-366aa1dd842611e9)。
- `BLI_jitterate1` → [blender::BLI_jitterate1 · L21](jitter_2d.cc.md#f-448acb6346acbd67)。
- `BLI_jitterate2` → [blender::BLI_jitterate2 · L79](jitter_2d.cc.md#f-ea1f41c34facd5aa)。
- `MEM_delete` → [MEM_delete · L400](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
