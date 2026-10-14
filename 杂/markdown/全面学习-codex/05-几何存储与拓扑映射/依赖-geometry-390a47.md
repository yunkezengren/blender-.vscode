# 实现依赖专题：intern/cycles/scene/geometry.cpp

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["Geometry::tag_position_modified"]:::abstraction
  F1["Geometry::tag_radius_modified"]:::compute
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
  F["geometry.cpp实现"]:::compute
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

<a id="f-fc4e7a818da1a4f6"></a>

### `Geometry::tag_position_modified`

实现位置：[intern/cycles/scene/geometry.cpp](../../../../../intern/cycles/scene/geometry.cpp) · L98—L103。

**教学注释版**

<!-- annotated:83ffe5f9d8f21a -->

```cpp
void Geometry::tag_position_modified()
{
  Attribute *attr = attributes.add(ATTR_STD_POSITION);
  attr->modified = true;
  tag_modified();
}
```

<details>
<summary>核对原始源码：intern/cycles/scene/geometry.cpp · L98—L103</summary>

<!-- original:83ffe5f9d8f21a:intern/cycles/scene/geometry.cpp:98:103 -->

```cpp
void Geometry::tag_position_modified()
{
  Attribute *attr = attributes.add(ATTR_STD_POSITION);
  attr->modified = true;
  tag_modified();
}
```

</details>

**沿实际写入检查状态**

- `attr->modified = true;`

**继续追踪实现**

- `attributes.add` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L100。
- `tag_modified` → [AttributeSet::tag_modified · L1181](%E4%BE%9D%E8%B5%96-attribute-dd7b4e.md#f-6b0eba2bfed32329)。

<a id="f-35c30575efa7505d"></a>

### `Geometry::tag_radius_modified`

实现位置：[intern/cycles/scene/geometry.cpp](../../../../../intern/cycles/scene/geometry.cpp) · L125—L130。

**教学注释版**

<!-- annotated:9b75e29deb8706 -->

```cpp
void Geometry::tag_radius_modified()
{
  Attribute *attr = attributes.add(ATTR_STD_RADIUS);
  attr->modified = true;
  tag_modified();
}
```

<details>
<summary>核对原始源码：intern/cycles/scene/geometry.cpp · L125—L130</summary>

<!-- original:9b75e29deb8706:intern/cycles/scene/geometry.cpp:125:130 -->

```cpp
void Geometry::tag_radius_modified()
{
  Attribute *attr = attributes.add(ATTR_STD_RADIUS);
  attr->modified = true;
  tag_modified();
}
```

</details>

**沿实际写入检查状态**

- `attr->modified = true;`

**继续追踪实现**

- `attributes.add` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L127。
- `tag_modified` → [AttributeSet::tag_modified · L1181](%E4%BE%9D%E8%B5%96-attribute-dd7b4e.md#f-6b0eba2bfed32329)。
