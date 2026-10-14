# 实现依赖专题：source/blender/python/mathutils/mathutils_Euler.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::Euler_CreatePyObject"]:::abstraction
  F1["blender::Euler_CreatePyObject_cb"]:::compute
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
  F["mathutils_Euler.cc实现"]:::compute
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

<a id="f-7a12eeb2beadb2ae"></a>

### `blender::Euler_CreatePyObject`

实现位置：[source/blender/python/mathutils/mathutils_Euler.cc](../../../../../../../../source/blender/python/mathutils/mathutils_Euler.cc) · L999—L1035。

接口参数：

- `const float eul[3]`
- `const short order`
- `PyTypeObject *base_type`

**教学注释版**

<!-- annotated:466706ce777d88 -->

```cpp
PyObject *Euler_CreatePyObject(const float eul[3], const short order, PyTypeObject *base_type)
{
  EulerObject *self;
  float *eul_alloc;

  eul_alloc = static_cast<float *>(PyMem_Malloc(EULER_SIZE * sizeof(float)));
  if (eul_alloc == nullptr) [[unlikely]] {
    PyErr_SetString(PyExc_MemoryError,
                    "Euler(): "
                    "problem allocating data");
    return nullptr;
  }

  self = BASE_MATH_NEW(EulerObject, euler_Type, base_type);
  if (self) {
    self->eul = eul_alloc;

    /* init callbacks as nullptr */
    self->cb_user = nullptr;
    self->cb_type = self->cb_subtype = 0;

    if (eul) {
      copy_v3_v3(self->eul, eul);
    }
    else {
      zero_v3(self->eul);
    }

    self->flag = BASE_MATH_FLAG_DEFAULT;
    self->order = order;
  }
  else {
    PyMem_Free(eul_alloc);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

<details>
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Euler.cc · L999—L1035</summary>

<!-- original:466706ce777d88:source/blender/python/mathutils/mathutils_Euler.cc:999:1035 -->

```cpp
PyObject *Euler_CreatePyObject(const float eul[3], const short order, PyTypeObject *base_type)
{
  EulerObject *self;
  float *eul_alloc;

  eul_alloc = static_cast<float *>(PyMem_Malloc(EULER_SIZE * sizeof(float)));
  if (eul_alloc == nullptr) [[unlikely]] {
    PyErr_SetString(PyExc_MemoryError,
                    "Euler(): "
                    "problem allocating data");
    return nullptr;
  }

  self = BASE_MATH_NEW(EulerObject, euler_Type, base_type);
  if (self) {
    self->eul = eul_alloc;

    /* init callbacks as nullptr */
    self->cb_user = nullptr;
    self->cb_type = self->cb_subtype = 0;

    if (eul) {
      copy_v3_v3(self->eul, eul);
    }
    else {
      zero_v3(self->eul);
    }

    self->flag = BASE_MATH_FLAG_DEFAULT;
    self->order = order;
  }
  else {
    PyMem_Free(eul_alloc);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

</details>

**沿实际写入检查状态**

- `eul_alloc = static_cast<float *>(PyMem_Malloc(EULER_SIZE * sizeof(float)));`
- `self = BASE_MATH_NEW(EulerObject, euler_Type, base_type);`
- `self->eul = eul_alloc;`
- `self->cb_user = nullptr;`
- `self->cb_type = self->cb_subtype = 0;`
- `self->flag = BASE_MATH_FLAG_DEFAULT;`
- `self->order = order;`

**结果出口**

- `return nullptr;`
- `return reinterpret_cast<PyObject *>(self);`

**继续追踪实现**

- `PyMem_Malloc` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1004。
- `PyErr_SetString` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1006。
- `BASE_MATH_NEW` → [BASE_MATH_NEW · L29](mathutils.hh.md#m-c1b2025904e4)。宏定义由构建条件选择。
- `copy_v3_v3` → [blender::copy_v3_v3 · L47](../../../01-BLI基础库/intern/math_vector_inline.cc.md#f-037a0d5fa5060bd6)。
- `zero_v3` → [blender::zero_v3 · L26](../../../01-BLI基础库/intern/math_vector_inline.cc.md#f-13235b08fdecb098)。
- `PyMem_Free` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1031。

<a id="f-8ed7c9d5299baf8c"></a>

### `blender::Euler_CreatePyObject_cb`

实现位置：[source/blender/python/mathutils/mathutils_Euler.cc](../../../../../../../../source/blender/python/mathutils/mathutils_Euler.cc) · L1056—L1073。

接口参数：

- `PyObject *cb_user`
- `const short order`
- `uchar cb_type`
- `uchar cb_subtype`

**教学注释版**

<!-- annotated:25d64c7aade5cb -->

```cpp
PyObject *Euler_CreatePyObject_cb(PyObject *cb_user,
                                  const short order,
                                  uchar cb_type,
                                  uchar cb_subtype)
{
  EulerObject *self = reinterpret_cast<EulerObject *>(
      Euler_CreatePyObject(nullptr, order, nullptr));
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
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Euler.cc · L1056—L1073</summary>

<!-- original:25d64c7aade5cb:source/blender/python/mathutils/mathutils_Euler.cc:1056:1073 -->

```cpp
PyObject *Euler_CreatePyObject_cb(PyObject *cb_user,
                                  const short order,
                                  uchar cb_type,
                                  uchar cb_subtype)
{
  EulerObject *self = reinterpret_cast<EulerObject *>(
      Euler_CreatePyObject(nullptr, order, nullptr));
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

- `Euler_CreatePyObject` → [blender::Euler_CreatePyObject · L999](mathutils_Euler.cc.md#f-7a12eeb2beadb2ae)。
- `Py_INCREF` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1064。
- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `PyObject_GC_IsTracked` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1068。
- `PyObject_GC_Track` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1069。
