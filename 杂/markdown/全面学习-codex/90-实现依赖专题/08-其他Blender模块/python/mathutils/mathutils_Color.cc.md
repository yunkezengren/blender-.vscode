# 实现依赖专题：source/blender/python/mathutils/mathutils_Color.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::Color_CreatePyObject"]:::abstraction
  F1["blender::Color_CreatePyObject_cb"]:::compute
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
  F["mathutils_Color.cc实现"]:::compute
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

<a id="f-44be93e4cf0749c8"></a>

### `blender::Color_CreatePyObject`

实现位置：[source/blender/python/mathutils/mathutils_Color.cc](../../../../../../../../source/blender/python/mathutils/mathutils_Color.cc) · L1415—L1451。

接口参数：

- `const float col[3]`
- `PyTypeObject *base_type`

**教学注释版**

<!-- annotated:9cc2298c2288be -->

```cpp
PyObject *Color_CreatePyObject(const float col[3], PyTypeObject *base_type)
{
  ColorObject *self;
  float *col_alloc;

  col_alloc = static_cast<float *>(PyMem_Malloc(COLOR_SIZE * sizeof(float)));
  if (col_alloc == nullptr) [[unlikely]] {
    PyErr_SetString(PyExc_MemoryError,
                    "Color(): "
                    "problem allocating data");
    return nullptr;
  }

  self = BASE_MATH_NEW(ColorObject, color_Type, base_type);
  if (self) {
    self->col = col_alloc;

    /* init callbacks as nullptr */
    self->cb_user = nullptr;
    self->cb_type = self->cb_subtype = 0;

    /* NEW */
    if (col) {
      copy_v3_v3(self->col, col);
    }
    else {
      zero_v3(self->col);
    }

    self->flag = BASE_MATH_FLAG_DEFAULT;
  }
  else {
    PyMem_Free(col_alloc);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

<details>
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Color.cc · L1415—L1451</summary>

<!-- original:9cc2298c2288be:source/blender/python/mathutils/mathutils_Color.cc:1415:1451 -->

```cpp
PyObject *Color_CreatePyObject(const float col[3], PyTypeObject *base_type)
{
  ColorObject *self;
  float *col_alloc;

  col_alloc = static_cast<float *>(PyMem_Malloc(COLOR_SIZE * sizeof(float)));
  if (col_alloc == nullptr) [[unlikely]] {
    PyErr_SetString(PyExc_MemoryError,
                    "Color(): "
                    "problem allocating data");
    return nullptr;
  }

  self = BASE_MATH_NEW(ColorObject, color_Type, base_type);
  if (self) {
    self->col = col_alloc;

    /* init callbacks as nullptr */
    self->cb_user = nullptr;
    self->cb_type = self->cb_subtype = 0;

    /* NEW */
    if (col) {
      copy_v3_v3(self->col, col);
    }
    else {
      zero_v3(self->col);
    }

    self->flag = BASE_MATH_FLAG_DEFAULT;
  }
  else {
    PyMem_Free(col_alloc);
  }

  return reinterpret_cast<PyObject *>(self);
}
```

</details>

**沿实际写入检查状态**

- `col_alloc = static_cast<float *>(PyMem_Malloc(COLOR_SIZE * sizeof(float)));`
- `self = BASE_MATH_NEW(ColorObject, color_Type, base_type);`
- `self->col = col_alloc;`
- `self->cb_user = nullptr;`
- `self->cb_type = self->cb_subtype = 0;`
- `self->flag = BASE_MATH_FLAG_DEFAULT;`

**结果出口**

- `return nullptr;`
- `return reinterpret_cast<PyObject *>(self);`

**继续追踪实现**

- `PyMem_Malloc` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1420。
- `PyErr_SetString` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1422。
- `BASE_MATH_NEW` → [BASE_MATH_NEW · L29](mathutils.hh.md#m-c1b2025904e4)。宏定义由构建条件选择。
- `copy_v3_v3` → [blender::copy_v3_v3 · L47](../../../01-BLI基础库/intern/math_vector_inline.cc.md#f-037a0d5fa5060bd6)。
- `zero_v3` → [blender::zero_v3 · L26](../../../01-BLI基础库/intern/math_vector_inline.cc.md#f-13235b08fdecb098)。
- `PyMem_Free` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1447。

<a id="f-907919d7b6dcfe02"></a>

### `blender::Color_CreatePyObject_cb`

实现位置：[source/blender/python/mathutils/mathutils_Color.cc](../../../../../../../../source/blender/python/mathutils/mathutils_Color.cc) · L1471—L1484。

接口参数：

- `PyObject *cb_user`
- `uchar cb_type`
- `uchar cb_subtype`

**教学注释版**

<!-- annotated:127ad9a9b66a3f -->

```cpp
PyObject *Color_CreatePyObject_cb(PyObject *cb_user, uchar cb_type, uchar cb_subtype)
{
  ColorObject *self = reinterpret_cast<ColorObject *>(Color_CreatePyObject(nullptr, nullptr));
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
<summary>核对原始源码：source/blender/python/mathutils/mathutils_Color.cc · L1471—L1484</summary>

<!-- original:127ad9a9b66a3f:source/blender/python/mathutils/mathutils_Color.cc:1471:1484 -->

```cpp
PyObject *Color_CreatePyObject_cb(PyObject *cb_user, uchar cb_type, uchar cb_subtype)
{
  ColorObject *self = reinterpret_cast<ColorObject *>(Color_CreatePyObject(nullptr, nullptr));
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

- `Color_CreatePyObject` → [blender::Color_CreatePyObject · L1415](mathutils_Color.cc.md#f-44be93e4cf0749c8)。
- `Py_INCREF` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1475。
- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `PyObject_GC_IsTracked` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1479。
- `PyObject_GC_Track` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：配置相关检测或外部运行时接口。调用位置L1480。
