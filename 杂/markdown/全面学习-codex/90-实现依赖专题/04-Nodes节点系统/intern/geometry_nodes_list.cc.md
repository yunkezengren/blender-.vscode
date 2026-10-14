# 实现依赖专题：source/blender/nodes/intern/geometry_nodes_list.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::nodes::array_data_from_garray"]:::abstraction
  F1["blender::nodes::GList::copy"]:::compute
  F2["blender::nodes::GList::varray"]:::compute
  F3["blender::nodes::GList::create"]:::compute
  F4["blender::nodes::GList::from_garray"]:::compute
  F1 -->|"显式调用"| F3
  F4 -->|"显式调用"| F3
  F4 -->|"显式调用"| F0
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
  F["geometry_nodes_list.cc实现"]:::compute
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

<a id="f-a27232284cd4ce6b"></a>

### `blender::nodes::array_data_from_garray`

实现位置：[source/blender/nodes/intern/geometry_nodes_list.cc](../../../../../../../source/blender/nodes/intern/geometry_nodes_list.cc) · L18—L25。

接口参数：

- `GArray<> array`

**教学注释版**

<!-- annotated:74c19c9600071a -->

```cpp
static GList::ArrayData array_data_from_garray(GArray<> array)
{
  // [讲解] std::move：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
  auto *sharing_info = new ImplicitSharedValue<GArray<>>(std::move(array));
  GList::ArrayData data;
  data.data = sharing_info->data.data();
  data.sharing_info = ImplicitSharingPtr<>(sharing_info);
  return data;
}
```

<details>
<summary>核对原始源码：source/blender/nodes/intern/geometry_nodes_list.cc · L18—L25</summary>

<!-- original:74c19c9600071a:source/blender/nodes/intern/geometry_nodes_list.cc:18:25 -->

```cpp
static GList::ArrayData array_data_from_garray(GArray<> array)
{
  auto *sharing_info = new ImplicitSharedValue<GArray<>>(std::move(array));
  GList::ArrayData data;
  data.data = sharing_info->data.data();
  data.sharing_info = ImplicitSharingPtr<>(sharing_info);
  return data;
}
```

</details>

**沿实际写入检查状态**

- `data.data = sharing_info->data.data();`
- `data.sharing_info = ImplicitSharingPtr<>(sharing_info);`

**结果出口**

- `return data;`

**继续追踪实现**

- `std::move` → [外部契约](https://eel.is/c++draft/utility.forward)：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
- `sharing_info->data.data` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L22。
- `ImplicitSharingPtr<>` → [blender::ImplicitSharingPtr::ImplicitSharingPtr · L32](../../../06-隐式共享与缓存系统/03-Mixin与共享指针封装.md#f-d28a43dbb5ed8c05)；[blender::ImplicitSharingPtr::ImplicitSharingPtr · L34](../../../06-隐式共享与缓存系统/03-Mixin与共享指针封装.md#f-d27d5ebf676e244a)；[blender::ImplicitSharingPtr::ImplicitSharingPtr · L37](../../../06-隐式共享与缓存系统/03-Mixin与共享指针封装.md#f-17d0c5fe2b03a664)；[blender::ImplicitSharingPtr::ImplicitSharingPtr · L39](../../../06-隐式共享与缓存系统/03-Mixin与共享指针封装.md#f-1c8729ae57532370)；[blender::ImplicitSharingPtr::ImplicitSharingPtr · L44](../../../06-隐式共享与缓存系统/03-Mixin与共享指针封装.md#f-0b6be0142b98009e)；[blender::ImplicitSharingPtr::ImplicitSharingPtr · L49](../../../06-隐式共享与缓存系统/03-Mixin与共享指针封装.md#f-90c601ed9ed99045)；[blender::ImplicitSharingPtr::ImplicitSharingPtr · L57](../../../06-隐式共享与缓存系统/03-Mixin与共享指针封装.md#f-1625179ceae7a66d)。同名重载需按实参类型选择。

<a id="f-c576bfad57bf8958"></a>

### `blender::nodes::GList::copy`

实现位置：[source/blender/nodes/intern/geometry_nodes_list.cc](../../../../../../../source/blender/nodes/intern/geometry_nodes_list.cc) · L80—L83。

**教学注释版**

<!-- annotated:bc790c01270df6 -->

```cpp
GListPtr GList::copy() const
{
  return GList::create(cpp_type_, data_, size_);
}
```

<details>
<summary>核对原始源码：source/blender/nodes/intern/geometry_nodes_list.cc · L80—L83</summary>

<!-- original:bc790c01270df6:source/blender/nodes/intern/geometry_nodes_list.cc:80:83 -->

```cpp
GListPtr GList::copy() const
{
  return GList::create(cpp_type_, data_, size_);
}
```

</details>

**结果出口**

- `return GList::create(cpp_type_, data_, size_);`

**继续追踪实现**

- `GList::create` → [blender::nodes::GList::create · L263](geometry_nodes_list.cc.md#f-d98f24446264b506)。

<a id="f-2abf90eb8a1543ac"></a>

### `blender::nodes::GList::varray`

实现位置：[source/blender/nodes/intern/geometry_nodes_list.cc](../../../../../../../source/blender/nodes/intern/geometry_nodes_list.cc) · L85—L95。

**教学注释版**

<!-- annotated:73050a9a58ce6b -->

```cpp
GVArray GList::varray() const
{
  if (const auto *array_data = std::get_if<ArrayData>(&data_)) {
    return GVArray::from_span(GSpan(cpp_type_, array_data->data, size_));
  }
  if (const auto *single_data = std::get_if<SingleData>(&data_)) {
    return GVArray::from_single_ref(cpp_type_, size_, single_data->value);
  }
  BLI_assert_unreachable();
  return {};
}
```

<details>
<summary>核对原始源码：source/blender/nodes/intern/geometry_nodes_list.cc · L85—L95</summary>

<!-- original:73050a9a58ce6b:source/blender/nodes/intern/geometry_nodes_list.cc:85:95 -->

```cpp
GVArray GList::varray() const
{
  if (const auto *array_data = std::get_if<ArrayData>(&data_)) {
    return GVArray::from_span(GSpan(cpp_type_, array_data->data, size_));
  }
  if (const auto *single_data = std::get_if<SingleData>(&data_)) {
    return GVArray::from_single_ref(cpp_type_, size_, single_data->value);
  }
  BLI_assert_unreachable();
  return {};
}
```

</details>

**结果出口**

- `return GVArray::from_span(GSpan(cpp_type_, array_data->data, size_));`
- `return GVArray::from_single_ref(cpp_type_, size_, single_data->value);`
- `return {};`

**继续追踪实现**

- `std::get_if<ArrayData>` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `GVArray::from_span` → [blender::GVArray::from_span · L895](../../../04-虚拟数组与索引选择/05-GVArray运行时类型.md#f-e8b978ca15febb67)。
- `GSpan` → [blender::GSpan::GSpan · L26](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-9d0c95702007eea6)；[blender::GSpan::GSpan · L28](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-6650bd08c7eecc66)；[blender::GSpan::GSpan · L37](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-bf180950832673fb)；[blender::GSpan::GSpan · L39](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-cf949d5590ea9ab6)；[blender::GSpan::GSpan · L41](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-a66ab52ee0842aee)；[blender::GSpan::GSpan · L43](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-d9084fa10964390f)；[blender::GSpan::GSpan · L49](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-76e3de3cc3d65761)。同名重载需按实参类型选择。
- `std::get_if<SingleData>` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `GVArray::from_single_ref` → [blender::GVArray::from_single_ref · L885](../../../04-虚拟数组与索引选择/05-GVArray运行时类型.md#f-8208f854554701e4)。
- `BLI_assert_unreachable` → [BLI_assert_unreachable · L77](../../01-BLI基础库/BLI_assert.hh.md#m-7a2d91a67d8e)。宏定义由构建条件选择。

<a id="f-d98f24446264b506"></a>

### `blender::nodes::GList::create`

实现位置：[source/blender/nodes/intern/geometry_nodes_list.cc](../../../../../../../source/blender/nodes/intern/geometry_nodes_list.cc) · L263—L266。

接口参数：

- `const CPPType &type`
- `DataVariant data`
- `const int64_t size`

**教学注释版**

<!-- annotated:0177915e51ae9d -->

```cpp
GListPtr GList::create(const CPPType &type, DataVariant data, const int64_t size)
{
  // [讲解] std::move：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
  return GListPtr(MEM_new<GList>(__func__, type, std::move(data), size));
}
```

<details>
<summary>核对原始源码：source/blender/nodes/intern/geometry_nodes_list.cc · L263—L266</summary>

<!-- original:0177915e51ae9d:source/blender/nodes/intern/geometry_nodes_list.cc:263:266 -->

```cpp
GListPtr GList::create(const CPPType &type, DataVariant data, const int64_t size)
{
  return GListPtr(MEM_new<GList>(__func__, type, std::move(data), size));
}
```

</details>

**结果出口**

- `return GListPtr(MEM_new<GList>(__func__, type, std::move(data), size));`

**继续追踪实现**

- `GListPtr` → [blender::nodes::GListPtr::GListPtr · L152](../NOD_geometry_nodes_list.hh.md#f-15788b095b6a3bf7)；[blender::nodes::GListPtr::GListPtr · L153](../NOD_geometry_nodes_list.hh.md#f-5bf0d6a7a8c28ef4)；[blender::nodes::GListPtr::GListPtr · L154](../NOD_geometry_nodes_list.hh.md#f-aba6a4f613490f6a)。同名重载需按实参类型选择。
- `MEM_new<GList>` → [MEM_new · L351](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-115f9b6784f89912)。
- `std::move` → [外部契约](https://eel.is/c++draft/utility.forward)：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。

<a id="f-441f4cfe3d661e9d"></a>

### `blender::nodes::GList::from_garray`

实现位置：[source/blender/nodes/intern/geometry_nodes_list.cc](../../../../../../../source/blender/nodes/intern/geometry_nodes_list.cc) · L268—L273。

接口参数：

- `GArray<> array`

**教学注释版**

<!-- annotated:7cdf7e68d6fa3c -->

```cpp
GListPtr GList::from_garray(GArray<> array)
{
  const CPPType &type = array.type();
  const int64_t size = array.size();
  // [讲解] std::move：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
  return GList::create(type, array_data_from_garray(std::move(array)), size);
}
```

<details>
<summary>核对原始源码：source/blender/nodes/intern/geometry_nodes_list.cc · L268—L273</summary>

<!-- original:7cdf7e68d6fa3c:source/blender/nodes/intern/geometry_nodes_list.cc:268:273 -->

```cpp
GListPtr GList::from_garray(GArray<> array)
{
  const CPPType &type = array.type();
  const int64_t size = array.size();
  return GList::create(type, array_data_from_garray(std::move(array)), size);
}
```

</details>

**结果出口**

- `return GList::create(type, array_data_from_garray(std::move(array)), size);`

**继续追踪实现**

- `array.type` → [blender::GArray::type · L138](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-3c4bebd424df52cc)。
- `array.size` → [blender::GArray::size · L152](../../../03-内存分配与运行时类型/11-GSpan与GArray.md#f-8897580a87dde189)。
- `GList::create` → [blender::nodes::GList::create · L263](geometry_nodes_list.cc.md#f-d98f24446264b506)。
- `array_data_from_garray` → [blender::nodes::array_data_from_garray · L18](geometry_nodes_list.cc.md#f-a27232284cd4ce6b)。
- `std::move` → [外部契约](https://eel.is/c++draft/utility.forward)：把表达式转换成可供移动重载选择的值类别；不保证真的移动，不结束源对象寿命，对const值可能选择复制。
