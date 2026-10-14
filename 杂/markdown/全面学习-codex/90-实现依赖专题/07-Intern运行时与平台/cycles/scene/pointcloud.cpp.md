# 实现依赖专题：intern/cycles/scene/pointcloud.cpp

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["PointCloud::resize"]:::abstraction
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
  F["pointcloud.cpp实现"]:::compute
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

<a id="f-2bb9cba64d026563"></a>

### `PointCloud::resize`

实现位置：[intern/cycles/scene/pointcloud.cpp](../../../../../../../../intern/cycles/scene/pointcloud.cpp) · L98—L110。

接口参数：

- `const int numpoints`

**教学注释版**

<!-- annotated:069ef27e08ae8c -->

```cpp
void PointCloud::resize(const int numpoints)
{
  Attribute *attr_P = attributes.add(ATTR_STD_POSITION);
  attr_P->resize(numpoints);
  Attribute *attr_R = attributes.add(ATTR_STD_RADIUS);
  attr_R->resize(numpoints);
  shader.resize(numpoints);
  attributes.resize();

  tag_position_modified();
  tag_radius_modified();
  tag_shader_modified();
}
```

<details>
<summary>核对原始源码：intern/cycles/scene/pointcloud.cpp · L98—L110</summary>

<!-- original:069ef27e08ae8c:intern/cycles/scene/pointcloud.cpp:98:110 -->

```cpp
void PointCloud::resize(const int numpoints)
{
  Attribute *attr_P = attributes.add(ATTR_STD_POSITION);
  attr_P->resize(numpoints);
  Attribute *attr_R = attributes.add(ATTR_STD_RADIUS);
  attr_R->resize(numpoints);
  shader.resize(numpoints);
  attributes.resize();

  tag_position_modified();
  tag_radius_modified();
  tag_shader_modified();
}
```

</details>

**继续追踪实现**

- `attributes.add` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L100。
- `attr_P->resize` → [Attribute::resize · L122](attribute.cpp.md#f-62b6dd96d32875c0)；[Attribute::resize · L129](attribute.cpp.md#f-048dccdac3da2b83)。同名重载需按实参类型选择。
- `attr_R->resize` → [Attribute::resize · L122](attribute.cpp.md#f-62b6dd96d32875c0)；[Attribute::resize · L129](attribute.cpp.md#f-048dccdac3da2b83)。同名重载需按实参类型选择。
- `shader.resize` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L104。
- `attributes.resize` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L105。
- `tag_position_modified` → [Geometry::tag_position_modified · L98](geometry.cpp.md#f-fc4e7a818da1a4f6)。
- `tag_radius_modified` → [Geometry::tag_radius_modified · L125](geometry.cpp.md#f-35c30575efa7505d)。
- `tag_shader_modified` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L109。
