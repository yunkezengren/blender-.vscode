# 实现依赖专题：source/blender/python/mathutils/mathutils_Vector.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["Vector_CreatePyObject"]:::abstraction
  F1["Vector_CreatePyObject_cb"]:::compute
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
  F["mathutils_Vector.cc实现"]:::compute
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

<a id="f-0f21e86f7cf656e7"></a>

### `Vector_CreatePyObject`

实现位置：[source/blender/python/mathutils/mathutils_Vector.cc](../../../../../../../../source/blender/python/mathutils/mathutils_Vector.cc) · L3697—L3740。

接口参数：

- `const float *vec`
- `const int vec_num`
- `PyTypeObject *base_type`

**教学注释版**

<!-- annotated:0bd34438173857 -->

```cpp
PyObject *Vector_CreatePyObject(const float *vec, const int vec_num, PyTypeObject *base_type)
{
  VectorObject *self;
  float *vec_alloc;

  if (vec_num < 2) {
    PyErr_SetString(PyExc_RuntimeError, "Vector(): invalid size");
    return nullptr;
  }

  vec_alloc = static_cast<float *>(PyMem_Malloc(vec_num * sizeof(float)));
  if (vec_alloc == nullptr) [[unlikely]] {
    PyErr_SetString(PyExc_MemoryError,
                    "Vector(): "
                    "problem allocating data");
    return nullptr;
  }

  self = BASE_MATH_NEW(VectorObject, vector_Type, base_type);
  if (self) {
    self->vec = vec_alloc;
    self->vec_num = vec_num;

    /* Initialize callbacks as nullptr. */
    self->cb_user = nullptr;
    self->cb_type = self->cb_subtype = 0;

    if (vec) {
      // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
      memcpy(self->vec, vec, vec_num * sizeof(float));
    }
    else { /* new empty */
      std::fill_n(self->vec, vec_num, 0.0f);
      if (vec_num == 4) { /* do the homogeneous thing */
        self->vec[3] = 1.0f;
      }
    }
    self->flag = BASE_MATH_FLAG_DEFAULT;
  }
  else {
    PyMem_Free(vec_alloc);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

<details>
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Vector.cc · L3697—L3740</summary>

<!-- original:0bd34438173857:source/blender/python/mathutils/mathutils_Vector.cc:3697:3740 -->

```cpp
PyObject *Vector_CreatePyObject(const float *vec, const int vec_num, PyTypeObject *base_type)
{
  VectorObject *self;
  float *vec_alloc;

  if (vec_num < 2) {
    PyErr_SetString(PyExc_RuntimeError, "Vector(): invalid size");
    return nullptr;
  }

  vec_alloc = static_cast<float *>(PyMem_Malloc(vec_num * sizeof(float)));
  if (vec_alloc == nullptr) [[unlikely]] {
    PyErr_SetString(PyExc_MemoryError,
                    "Vector(): "
                    "problem allocating data");
    return nullptr;
  }

  self = BASE_MATH_NEW(VectorObject, vector_Type, base_type);
  if (self) {
    self->vec = vec_alloc;
    self->vec_num = vec_num;

    /* Initialize callbacks as nullptr. */
    self->cb_user = nullptr;
    self->cb_type = self->cb_subtype = 0;

    if (vec) {
      memcpy(self->vec, vec, vec_num * sizeof(float));
    }
    else { /* new empty */
      std::fill_n(self->vec, vec_num, 0.0f);
      if (vec_num == 4) { /* do the homogeneous thing */
        self->vec[3] = 1.0f;
      }
    }
    self->flag = BASE_MATH_FLAG_DEFAULT;
  }
  else {
    PyMem_Free(vec_alloc);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

</details>

**沿实际写入检查状态**

- `vec_alloc = static_cast<float *>(PyMem_Malloc(vec_num * sizeof(float)));`
- `self = BASE_MATH_NEW(VectorObject, vector_Type, base_type);`
- `self->vec = vec_alloc;`
- `self->vec_num = vec_num;`
- `self->cb_user = nullptr;`
- `self->cb_type = self->cb_subtype = 0;`
- `self->vec[3] = 1.0f;`
- `self->flag = BASE_MATH_FLAG_DEFAULT;`

**结果出口**

- `return nullptr;`
- `return reinterpret_cast<PyObject *>(self);`

**继续追踪实现**

- `PyErr_SetString` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L3703。
- `PyMem_Malloc` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L3707。
- `BASE_MATH_NEW` → [BASE_MATH_NEW · L29](mathutils.hh.md#m-c1b2025904e4)。宏定义由构建条件选择。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
- `std::fill_n` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `PyMem_Free` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L3736。

<a id="f-ea5832cdced57961"></a>

### `Vector_CreatePyObject_cb`

实现位置：[source/blender/python/mathutils/mathutils_Vector.cc](../../../../../../../../source/blender/python/mathutils/mathutils_Vector.cc) · L3765—L3778。

接口参数：

- `PyObject *cb_user`
- `int vec_num`
- `uchar cb_type`
- `uchar cb_subtype`

**教学注释版**

<!-- annotated:84f39ce8b2f756 -->

```cpp
PyObject *Vector_CreatePyObject_cb(PyObject *cb_user, int vec_num, uchar cb_type, uchar cb_subtype)
{
  VectorObject *self = reinterpret_cast<VectorObject *>(
      Vector_CreatePyObject(nullptr, vec_num, nullptr));
  if (self) {
    self->cb_user = Py_NewRef(cb_user);
    self->cb_type = cb_type;
    self->cb_subtype = cb_subtype;
    BLI_assert(!PyObject_GC_IsTracked((PyObject *)self));
    PyObject_GC_Track(self);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

<details>
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Vector.cc · L3765—L3778</summary>

<!-- original:84f39ce8b2f756:source/blender/python/mathutils/mathutils_Vector.cc:3765:3778 -->

```cpp
PyObject *Vector_CreatePyObject_cb(PyObject *cb_user, int vec_num, uchar cb_type, uchar cb_subtype)
{
  VectorObject *self = reinterpret_cast<VectorObject *>(
      Vector_CreatePyObject(nullptr, vec_num, nullptr));
  if (self) {
    self->cb_user = Py_NewRef(cb_user);
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

- `self->cb_user = Py_NewRef(cb_user);`
- `self->cb_type = cb_type;`
- `self->cb_subtype = cb_subtype;`

**结果出口**

- `return reinterpret_cast<PyObject *>(self);`

**继续追踪实现**

- `Vector_CreatePyObject` → [Vector_CreatePyObject · L3697](mathutils_Vector.cc.md#f-0f21e86f7cf656e7)。
- `Py_NewRef` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L3770。
- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `PyObject_GC_IsTracked` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L3773。
- `PyObject_GC_Track` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L3774。
