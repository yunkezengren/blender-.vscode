# 实现依赖专题：source/blender/python/mathutils/mathutils_Matrix.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::matrix_identity_internal"]:::abstraction
  F1["blender::Matrix_CreatePyObject"]:::compute
  F2["blender::Matrix_CreatePyObject_cb"]:::compute
  F1 -->|"显式调用"| F0
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
  F["mathutils_Matrix.cc实现"]:::compute
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

<a id="f-8beb02289a7c17b1"></a>

### `blender::matrix_identity_internal`

实现位置：[source/blender/python/mathutils/mathutils_Matrix.cc](../../../../../source/blender/python/mathutils/mathutils_Matrix.cc) · L2300—L2313。

接口参数：

- `MatrixObject *self`

**教学注释版**

<!-- annotated:2e9dd516070ad8 -->

```cpp
static void matrix_identity_internal(MatrixObject *self)
{
  BLI_assert((self->col_num == self->row_num) && (self->row_num <= 4));

  if (self->col_num == 2) {
    unit_m2(reinterpret_cast<float (*)[2]>(self->matrix));
  }
  else if (self->col_num == 3) {
    unit_m3(reinterpret_cast<float (*)[3]>(self->matrix));
  }
  else {
    unit_m4(reinterpret_cast<float (*)[4]>(self->matrix));
  }
}
```

<details>
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Matrix.cc · L2300—L2313</summary>

<!-- original:2e9dd516070ad8:source/blender/python/mathutils/mathutils_Matrix.cc:2300:2313 -->

```cpp
static void matrix_identity_internal(MatrixObject *self)
{
  BLI_assert((self->col_num == self->row_num) && (self->row_num <= 4));

  if (self->col_num == 2) {
    unit_m2(reinterpret_cast<float (*)[2]>(self->matrix));
  }
  else if (self->col_num == 3) {
    unit_m3(reinterpret_cast<float (*)[3]>(self->matrix));
  }
  else {
    unit_m4(reinterpret_cast<float (*)[4]>(self->matrix));
  }
}
```

</details>

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `unit_m2` → [blender::unit_m2 · L40](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_matrix_c-004123.md#f-bfe83504111fa231)。
- `unit_m3` → [blender::unit_m3 · L47](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_matrix_c-004123.md#f-85e0073adca4ccff)。
- `unit_m4` → [blender::unit_m4 · L55](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_matrix_c-004123.md#f-e6cd812aae119176)。

<a id="f-d244d74d8638a2ba"></a>

### `blender::Matrix_CreatePyObject`

实现位置：[source/blender/python/mathutils/mathutils_Matrix.cc](../../../../../source/blender/python/mathutils/mathutils_Matrix.cc) · L3788—L3840。

接口参数：

- `const float *mat`
- `const ushort col_num`
- `const ushort row_num`
- `PyTypeObject *base_type`

**教学注释版**

<!-- annotated:59c823a9c07f84 -->

```cpp
PyObject *Matrix_CreatePyObject(const float *mat,
                                const ushort col_num,
                                const ushort row_num,
                                PyTypeObject *base_type)
{
  MatrixObject *self;
  float *mat_alloc;

  /* matrix objects can be any 2-4row x 2-4col matrix */
  if (col_num < 2 || col_num > 4 || row_num < 2 || row_num > 4) {
    PyErr_SetString(PyExc_RuntimeError,
                    "Matrix(): "
                    "row and column sizes must be between 2 and 4");
    return nullptr;
  }

  mat_alloc = static_cast<float *>(PyMem_Malloc(col_num * row_num * sizeof(float)));
  if (mat_alloc == nullptr) [[unlikely]] {
    PyErr_SetString(PyExc_MemoryError,
                    "Matrix(): "
                    "problem allocating data");
    return nullptr;
  }

  self = BASE_MATH_NEW(MatrixObject, matrix_Type, base_type);
  if (self) {
    self->matrix = mat_alloc;
    self->col_num = col_num;
    self->row_num = row_num;

    /* init callbacks as nullptr */
    self->cb_user = nullptr;
    self->cb_type = self->cb_subtype = 0;

    if (mat) { /* If a float array passed. */
      // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
      memcpy(self->matrix, mat, col_num * row_num * sizeof(float));
    }
    else if (col_num == row_num) {
      /* or if no arguments are passed return identity matrix for square matrices */
      matrix_identity_internal(self);
    }
    else {
      /* otherwise zero everything */
      // [讲解] memset：填充字节，不调用T构造函数，也不保证任意类型的全零表示是合法或期望值。
      memset(self->matrix, 0, col_num * row_num * sizeof(float));
    }
    self->flag = BASE_MATH_FLAG_DEFAULT;
  }
  else {
    PyMem_Free(mat_alloc);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

<details>
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Matrix.cc · L3788—L3840</summary>

<!-- original:59c823a9c07f84:source/blender/python/mathutils/mathutils_Matrix.cc:3788:3840 -->

```cpp
PyObject *Matrix_CreatePyObject(const float *mat,
                                const ushort col_num,
                                const ushort row_num,
                                PyTypeObject *base_type)
{
  MatrixObject *self;
  float *mat_alloc;

  /* matrix objects can be any 2-4row x 2-4col matrix */
  if (col_num < 2 || col_num > 4 || row_num < 2 || row_num > 4) {
    PyErr_SetString(PyExc_RuntimeError,
                    "Matrix(): "
                    "row and column sizes must be between 2 and 4");
    return nullptr;
  }

  mat_alloc = static_cast<float *>(PyMem_Malloc(col_num * row_num * sizeof(float)));
  if (mat_alloc == nullptr) [[unlikely]] {
    PyErr_SetString(PyExc_MemoryError,
                    "Matrix(): "
                    "problem allocating data");
    return nullptr;
  }

  self = BASE_MATH_NEW(MatrixObject, matrix_Type, base_type);
  if (self) {
    self->matrix = mat_alloc;
    self->col_num = col_num;
    self->row_num = row_num;

    /* init callbacks as nullptr */
    self->cb_user = nullptr;
    self->cb_type = self->cb_subtype = 0;

    if (mat) { /* If a float array passed. */
      memcpy(self->matrix, mat, col_num * row_num * sizeof(float));
    }
    else if (col_num == row_num) {
      /* or if no arguments are passed return identity matrix for square matrices */
      matrix_identity_internal(self);
    }
    else {
      /* otherwise zero everything */
      memset(self->matrix, 0, col_num * row_num * sizeof(float));
    }
    self->flag = BASE_MATH_FLAG_DEFAULT;
  }
  else {
    PyMem_Free(mat_alloc);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

</details>

**沿实际写入检查状态**

- `mat_alloc = static_cast<float *>(PyMem_Malloc(col_num * row_num * sizeof(float)));`
- `self = BASE_MATH_NEW(MatrixObject, matrix_Type, base_type);`
- `self->matrix = mat_alloc;`
- `self->col_num = col_num;`
- `self->row_num = row_num;`
- `self->cb_user = nullptr;`
- `self->cb_type = self->cb_subtype = 0;`
- `self->flag = BASE_MATH_FLAG_DEFAULT;`

**结果出口**

- `return nullptr;`
- `return reinterpret_cast<PyObject *>(self);`

**继续追踪实现**

- `PyErr_SetString` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：配置相关检测或外部运行时接口。调用位置L3798。
- `PyMem_Malloc` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：配置相关检测或外部运行时接口。调用位置L3804。
- `BASE_MATH_NEW` → [BASE_MATH_NEW · L29](%E4%BE%9D%E8%B5%96-mathutils-0ede3f.md#m-c1b2025904e4)。宏定义由构建条件选择。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
- `matrix_identity_internal` → [blender::matrix_identity_internal · L2300](%E4%BE%9D%E8%B5%96-mathutils_Matrix-3cdd44.md#f-8beb02289a7c17b1)。
- `memset` → [外部契约](https://eel.is/c++draft/cstring.syn)：填充字节，不调用T构造函数，也不保证任意类型的全零表示是合法或期望值。
- `PyMem_Free` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：配置相关检测或外部运行时接口。调用位置L3836。

<a id="f-599ed79684b1cb88"></a>

### `blender::Matrix_CreatePyObject_cb`

实现位置：[source/blender/python/mathutils/mathutils_Matrix.cc](../../../../../source/blender/python/mathutils/mathutils_Matrix.cc) · L3872—L3886。

接口参数：

- `PyObject *cb_user`
- `const ushort col_num`
- `const ushort row_num`
- `uchar cb_type`
- `uchar cb_subtype`

**教学注释版**

<!-- annotated:ee3b8353399274 -->

```cpp
PyObject *Matrix_CreatePyObject_cb(
    PyObject *cb_user, const ushort col_num, const ushort row_num, uchar cb_type, uchar cb_subtype)
{
  MatrixObject *self = reinterpret_cast<MatrixObject *>(
      Matrix_CreatePyObject(nullptr, col_num, row_num, nullptr));
  if (self) {
    Py_INCREF(cb_user);
    self->cb_user = cb_user;
    self->cb_type = cb_type;
    self->cb_subtype = cb_subtype;
    BLI_assert(!PyObject_GC_IsTracked((PyObject *)self));
    PyObject_GC_Track(self);
  }
  return reinterpret_cast<PyObject *>(self);
}
```

<details>
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Matrix.cc · L3872—L3886</summary>

<!-- original:ee3b8353399274:source/blender/python/mathutils/mathutils_Matrix.cc:3872:3886 -->

```cpp
PyObject *Matrix_CreatePyObject_cb(
    PyObject *cb_user, const ushort col_num, const ushort row_num, uchar cb_type, uchar cb_subtype)
{
  MatrixObject *self = reinterpret_cast<MatrixObject *>(
      Matrix_CreatePyObject(nullptr, col_num, row_num, nullptr));
  if (self) {
    Py_INCREF(cb_user);
    self->cb_user = cb_user;
    self->cb_type = cb_type;
    self->cb_subtype = cb_subtype;
    BLI_assert(!PyObject_GC_IsTracked((PyObject *)self));
    PyObject_GC_Track(self);
  }
  return reinterpret_cast<PyObject *>(self);
}
```

</details>

**沿实际写入检查状态**

- `self->cb_user = cb_user;`
- `self->cb_type = cb_type;`
- `self->cb_subtype = cb_subtype;`

**结果出口**

- `return reinterpret_cast<PyObject *>(self);`

**继续追踪实现**

- `Matrix_CreatePyObject` → [blender::Matrix_CreatePyObject · L3788](%E4%BE%9D%E8%B5%96-mathutils_Matrix-3cdd44.md#f-d244d74d8638a2ba)。
- `Py_INCREF` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：配置相关检测或外部运行时接口。调用位置L3878。
- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `PyObject_GC_IsTracked` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：配置相关检测或外部运行时接口。调用位置L3882。
- `PyObject_GC_Track` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：配置相关检测或外部运行时接口。调用位置L3883。
