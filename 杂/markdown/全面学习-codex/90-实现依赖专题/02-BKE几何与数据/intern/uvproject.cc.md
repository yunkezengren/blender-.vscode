# 实现依赖专题：source/blender/blenkernel/intern/uvproject.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::BKE_uvproject_from_camera"]:::abstraction
  F1["blender::BKE_uvproject_camera_info"]:::compute
  F2["blender::BKE_uvproject_camera_info_scale"]:::compute
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
  F["uvproject.cc实现"]:::compute
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

<a id="f-ae58e1a57e4d2ee0"></a>

### `blender::BKE_uvproject_from_camera`

实现位置：[source/blender/blenkernel/intern/uvproject.cc](../../../../../../../source/blender/blenkernel/intern/uvproject.cc) · L34—L84。

接口参数：

- `float target[2]`
- `const float source[3]`
- `const ProjCameraInfo *uci`

**教学注释版**

<!-- annotated:caea5758394cdb -->

```cpp
void BKE_uvproject_from_camera(float target[2], const float source[3], const ProjCameraInfo *uci)
{
  float pv4[4];

  copy_v3_v3(pv4, source);
  pv4[3] = 1.0;

  /* rotmat is the object matrix in this case */
  if (uci->do_rotmat) {
    mul_m4_v4(uci->rotmat, pv4);
  }

  /* caminv is the inverse camera matrix */
  mul_m4_v4(uci->caminv, pv4);

  if (uci->do_pano) {
    float angle = atan2f(pv4[0], -pv4[2]) / (float(M_PI) * 2.0f); /* angle around the camera */
    if (uci->do_persp == false) {
      target[0] = angle; /* No correct method here, just map to 0-1. */
      target[1] = pv4[1] / uci->camsize;
    }
    else {
      float vec2d[2]; /* 2D position from the camera */
      vec2d[0] = pv4[0];
      vec2d[1] = pv4[2];
      target[0] = angle * (float(M_PI) / uci->camangle);
      target[1] = pv4[1] / (len_v2(vec2d) * (uci->camsize * 2.0f));
    }
  }
  else {
    if (pv4[2] == 0.0f) {
      pv4[2] = 0.00001f; /* don't allow div by 0 */
    }

    if (uci->do_persp == false) {
      target[0] = (pv4[0] / uci->camsize);
      target[1] = (pv4[1] / uci->camsize);
    }
    else {
      target[0] = (-pv4[0] * ((1.0f / uci->camsize) / pv4[2])) / 2.0f;
      target[1] = (-pv4[1] * ((1.0f / uci->camsize) / pv4[2])) / 2.0f;
    }
  }

  target[0] *= uci->xasp;
  target[1] *= uci->yasp;

  /* adds camera shift + 0.5 */
  target[0] += uci->shiftx;
  target[1] += uci->shifty;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/uvproject.cc · L34—L84</summary>

<!-- original:caea5758394cdb:source/blender/blenkernel/intern/uvproject.cc:34:84 -->

```cpp
void BKE_uvproject_from_camera(float target[2], const float source[3], const ProjCameraInfo *uci)
{
  float pv4[4];

  copy_v3_v3(pv4, source);
  pv4[3] = 1.0;

  /* rotmat is the object matrix in this case */
  if (uci->do_rotmat) {
    mul_m4_v4(uci->rotmat, pv4);
  }

  /* caminv is the inverse camera matrix */
  mul_m4_v4(uci->caminv, pv4);

  if (uci->do_pano) {
    float angle = atan2f(pv4[0], -pv4[2]) / (float(M_PI) * 2.0f); /* angle around the camera */
    if (uci->do_persp == false) {
      target[0] = angle; /* No correct method here, just map to 0-1. */
      target[1] = pv4[1] / uci->camsize;
    }
    else {
      float vec2d[2]; /* 2D position from the camera */
      vec2d[0] = pv4[0];
      vec2d[1] = pv4[2];
      target[0] = angle * (float(M_PI) / uci->camangle);
      target[1] = pv4[1] / (len_v2(vec2d) * (uci->camsize * 2.0f));
    }
  }
  else {
    if (pv4[2] == 0.0f) {
      pv4[2] = 0.00001f; /* don't allow div by 0 */
    }

    if (uci->do_persp == false) {
      target[0] = (pv4[0] / uci->camsize);
      target[1] = (pv4[1] / uci->camsize);
    }
    else {
      target[0] = (-pv4[0] * ((1.0f / uci->camsize) / pv4[2])) / 2.0f;
      target[1] = (-pv4[1] * ((1.0f / uci->camsize) / pv4[2])) / 2.0f;
    }
  }

  target[0] *= uci->xasp;
  target[1] *= uci->yasp;

  /* adds camera shift + 0.5 */
  target[0] += uci->shiftx;
  target[1] += uci->shifty;
}
```

</details>

**沿实际写入检查状态**

- `pv4[3] = 1.0;`
- `target[0] = angle; /* No correct method here, just map to 0-1. */`
- `target[1] = pv4[1] / uci->camsize;`
- `vec2d[0] = pv4[0];`
- `vec2d[1] = pv4[2];`
- `target[0] = angle * (float(M_PI) / uci->camangle);`
- `target[1] = pv4[1] / (len_v2(vec2d) * (uci->camsize * 2.0f));`
- `pv4[2] = 0.00001f; /* don't allow div by 0 */`
- `target[0] = (pv4[0] / uci->camsize);`
- `target[1] = (pv4[1] / uci->camsize);`
- `target[0] = (-pv4[0] * ((1.0f / uci->camsize) / pv4[2])) / 2.0f;`
- `target[1] = (-pv4[1] * ((1.0f / uci->camsize) / pv4[2])) / 2.0f;`
- `target[0] *= uci->xasp;`
- `target[1] *= uci->yasp;`
- `target[0] += uci->shiftx;`
- `target[1] += uci->shifty;`

**继续追踪实现**

- `copy_v3_v3` → [blender::copy_v3_v3 · L47](../../01-BLI基础库/intern/math_vector_inline.cc.md#f-037a0d5fa5060bd6)。
- `mul_m4_v4` → [blender::mul_m4_v4 · L810](../../01-BLI基础库/intern/math_matrix_c.cc.md#f-aaa7c69c4ac12b2b)。
- `atan2f` → [atan2f · L18](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-a77af3382db2)；[atan2f · L40](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-cec47b2ce998)；[atan2f · L71](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-bd31b1779092)；[atan2f · L22](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-9b9c2a707484)；[atan2f · L44](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-63f49b7d81dc)；[atan2f · L75](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-4201e8b4c423)；[atan2f · L18](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-ec4f8238af32)；[atan2f · L40](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-980162d675e3)；[atan2f · L71](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-bcd4c102a83d)；[atan2f · L179](../../07-Intern运行时与平台/cycles/kernel/device/oneapi/compat.h.md#m-5be26d38bfa7)；[atan2f · L274](../../07-Intern运行时与平台/cycles/kernel/device/metal/compat.h.md#m-1b9636d3b02f)。宏定义由构建条件选择。
- `len_v2` → [blender::len_v2 · L744](../../01-BLI基础库/intern/math_vector_inline.cc.md#f-5cbb0955da676dd1)。

<a id="f-da1f42d3225f5fa7"></a>

### `blender::BKE_uvproject_camera_info`

实现位置：[source/blender/blenkernel/intern/uvproject.cc](../../../../../../../source/blender/blenkernel/intern/uvproject.cc) · L127—L177。

接口参数：

- `const Object *ob`
- `const float rotmat[4][4]`
- `float winx`
- `float winy`

**教学注释版**

<!-- annotated:421e663163de1c -->

```cpp
ProjCameraInfo *BKE_uvproject_camera_info(const Object *ob,
                                          const float rotmat[4][4],
                                          float winx,
                                          float winy)
{
  ProjCameraInfo uci;
  const Camera *camera = id_cast<Camera *>(ob->data);

  uci.do_pano = (camera->type == CAM_PANO);
  uci.do_persp = ELEM(camera->type, CAM_PERSP, CAM_CUSTOM);

  uci.camangle = focallength_to_fov(camera->lens, camera->sensor_x) / 2.0f;
  uci.camsize = uci.do_persp ? tanf(uci.camangle) : camera->ortho_scale;

  /* account for scaled cameras */
  copy_m4_m4(uci.caminv, ob->object_to_world().ptr());
  normalize_m4(uci.caminv);

  if (invert_m4(uci.caminv)) {
    ProjCameraInfo *uci_pt;

    /* normal projection */
    if (rotmat) {
      copy_m4_m4(uci.rotmat, rotmat);
      uci.do_rotmat = true;
    }
    else {
      uci.do_rotmat = false;
    }

    /* also make aspect ratio adjustment factors */
    if (winx > winy) {
      uci.xasp = 1.0f;
      uci.yasp = winx / winy;
    }
    else {
      uci.xasp = winy / winx;
      uci.yasp = 1.0f;
    }

    /* include 0.5f here to move the UVs into the center */
    uci.shiftx = 0.5f - (camera->shiftx * uci.xasp);
    uci.shifty = 0.5f - (camera->shifty * uci.yasp);

    uci_pt = MEM_new_uninitialized<ProjCameraInfo>(__func__);
    *uci_pt = uci;
    return uci_pt;
  }

  return nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/uvproject.cc · L127—L177</summary>

<!-- original:421e663163de1c:source/blender/blenkernel/intern/uvproject.cc:127:177 -->

```cpp
ProjCameraInfo *BKE_uvproject_camera_info(const Object *ob,
                                          const float rotmat[4][4],
                                          float winx,
                                          float winy)
{
  ProjCameraInfo uci;
  const Camera *camera = id_cast<Camera *>(ob->data);

  uci.do_pano = (camera->type == CAM_PANO);
  uci.do_persp = ELEM(camera->type, CAM_PERSP, CAM_CUSTOM);

  uci.camangle = focallength_to_fov(camera->lens, camera->sensor_x) / 2.0f;
  uci.camsize = uci.do_persp ? tanf(uci.camangle) : camera->ortho_scale;

  /* account for scaled cameras */
  copy_m4_m4(uci.caminv, ob->object_to_world().ptr());
  normalize_m4(uci.caminv);

  if (invert_m4(uci.caminv)) {
    ProjCameraInfo *uci_pt;

    /* normal projection */
    if (rotmat) {
      copy_m4_m4(uci.rotmat, rotmat);
      uci.do_rotmat = true;
    }
    else {
      uci.do_rotmat = false;
    }

    /* also make aspect ratio adjustment factors */
    if (winx > winy) {
      uci.xasp = 1.0f;
      uci.yasp = winx / winy;
    }
    else {
      uci.xasp = winy / winx;
      uci.yasp = 1.0f;
    }

    /* include 0.5f here to move the UVs into the center */
    uci.shiftx = 0.5f - (camera->shiftx * uci.xasp);
    uci.shifty = 0.5f - (camera->shifty * uci.yasp);

    uci_pt = MEM_new_uninitialized<ProjCameraInfo>(__func__);
    *uci_pt = uci;
    return uci_pt;
  }

  return nullptr;
}
```

</details>

**沿实际写入检查状态**

- `uci.do_pano = (camera->type == CAM_PANO);`
- `uci.do_persp = ELEM(camera->type, CAM_PERSP, CAM_CUSTOM);`
- `uci.camangle = focallength_to_fov(camera->lens, camera->sensor_x) / 2.0f;`
- `uci.camsize = uci.do_persp ? tanf(uci.camangle) : camera->ortho_scale;`
- `uci.do_rotmat = true;`
- `uci.do_rotmat = false;`
- `uci.xasp = 1.0f;`
- `uci.yasp = winx / winy;`
- `uci.xasp = winy / winx;`
- `uci.yasp = 1.0f;`
- `uci.shiftx = 0.5f - (camera->shiftx * uci.xasp);`
- `uci.shifty = 0.5f - (camera->shifty * uci.yasp);`
- `uci_pt = MEM_new_uninitialized<ProjCameraInfo>(__func__);`

**结果出口**

- `return uci_pt;`
- `return nullptr;`

**继续追踪实现**

- `id_cast<Camera *>` → [blender::id_cast · L1417](../../08-其他Blender模块/makesdna/DNA_ID.h.md#f-6c8ac6412850ac5a)。
- `ELEM` → [ELEM · L88](../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-d28724a15928)；[ELEM · L135](../../01-BLI基础库/BLI_utildefines.hh.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `focallength_to_fov` → [blender::focallength_to_fov · L2336](../../01-BLI基础库/intern/math_rotation_c.cc.md#f-e8999e0a3cdf4071)。
- `tanf` → [tanf · L30](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-59a434b9184c)；[tanf · L52](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-96d07165eab2)；[tanf · L83](../../07-Intern运行时与平台/cycles/kernel/svm/radial_tiling_shared.h.md#m-7663637581d9)；[tanf · L34](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-8b35fd329650)；[tanf · L56](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-9e153fc2f61f)；[tanf · L87](../../01-BLI基础库/intern/radial_tiling_shared.hh.md#m-8eb7d6521f7a)；[tanf · L30](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-d7bdd765eeff)；[tanf · L52](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-2b90b7f17f04)；[tanf · L83](../../07-Intern运行时与平台/cycles/kernel/osl/shaders/node_radial_tiling_shared.h.md#m-39bfd36efdd8)；[tanf · L189](../../07-Intern运行时与平台/cycles/kernel/device/oneapi/compat.h.md#m-2c0993e4c930)；[tanf · L289](../../07-Intern运行时与平台/cycles/kernel/device/metal/compat.h.md#m-377fea82ecaa)；[tanf · L96](../../07-Intern运行时与平台/cycles/kernel/device/hip/compat.h.md#m-bf249a5884aa)；[tanf · L94](../../07-Intern运行时与平台/cycles/kernel/device/cuda/compat.h.md#m-789daa70cab8)；[tanf · L45](../../08-其他Blender模块/gpu/GPU_shader_shared_utils.hh.md#m-47237e652f9a)；[tanf · L66](../../08-其他Blender模块/gpu/GPU_shader_shared_utils.hh.md#m-ec729c327d58)。宏定义由构建条件选择。
- `copy_m4_m4` → [blender::copy_m4_m4 · L84](../../01-BLI基础库/intern/math_matrix_c.cc.md#f-b4390cf8c94710f5)。
- `ob->object_to_world().ptr` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L142。
- `ob->object_to_world` → [blender::Object::object_to_world · L5761](object.cc.md#f-12fc20026327d50c)。
- `normalize_m4` → [blender::normalize_m4 · L1779](../../01-BLI基础库/intern/math_matrix_c.cc.md#f-55c35f5c5d7d4719)。
- `invert_m4` → [blender::invert_m4 · L1069](../../01-BLI基础库/intern/math_matrix_c.cc.md#f-db172dd1e3ce5867)。
- `MEM_new_uninitialized<ProjCameraInfo>` → [MEM_new_uninitialized · L590](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-c773b2e5b8fe70e4)；[MEM_new_uninitialized · L124](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-28a7e00a1e67f699)。同名重载需按实参类型选择。

<a id="f-deab22a6871fad54"></a>

### `blender::BKE_uvproject_camera_info_scale`

实现位置：[source/blender/blenkernel/intern/uvproject.cc](../../../../../../../source/blender/blenkernel/intern/uvproject.cc) · L197—L201。

接口参数：

- `ProjCameraInfo *uci`
- `float scale_x`
- `float scale_y`

**教学注释版**

<!-- annotated:77330ee240a84c -->

```cpp
void BKE_uvproject_camera_info_scale(ProjCameraInfo *uci, float scale_x, float scale_y)
{
  uci->xasp *= scale_x;
  uci->yasp *= scale_y;
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/uvproject.cc · L197—L201</summary>

<!-- original:77330ee240a84c:source/blender/blenkernel/intern/uvproject.cc:197:201 -->

```cpp
void BKE_uvproject_camera_info_scale(ProjCameraInfo *uci, float scale_x, float scale_y)
{
  uci->xasp *= scale_x;
  uci->yasp *= scale_y;
}
```

</details>

**沿实际写入检查状态**

- `uci->xasp *= scale_x;`
- `uci->yasp *= scale_y;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
