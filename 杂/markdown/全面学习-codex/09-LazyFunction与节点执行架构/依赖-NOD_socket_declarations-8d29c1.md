# 实现依赖专题：source/blender/nodes/NOD_socket_declarations.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["NOD_socket_declarations.hh"]:::abstraction
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
  F["NOD_socket_declarations.hh实现"]:::compute
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

## 相关类型布局与成员入口

<a id="t-244cfac6be12"></a>

### `blender::nodes::decl::Vector`

原始声明：[source/blender/nodes/NOD_socket_declarations.hh](../../../../../source/blender/nodes/NOD_socket_declarations.hh) · L94—L112。

成员布局：

- `eNodeSocketDatatype static_socket_type`
- `float4 default_value`
- `float soft_min_value`
- `float soft_max_value`
- `int dimensions`
- `PropertySubType subtype`
- `bNodeSocket build`
- `bool matches`
- `bNodeSocket update_or_build`
- `bool can_connect`

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:254592b0ffdd7a -->

```cpp
class Vector : public SocketDeclaration {
 public:
  static constexpr eNodeSocketDatatype static_socket_type = SOCK_VECTOR;

  float4 default_value = {0, 0, 0, 0};
  float soft_min_value = -FLT_MAX;
  float soft_max_value = FLT_MAX;
  int dimensions = 3;
  PropertySubType subtype = PROP_NONE;

  friend VectorBuilder;

  using Builder = VectorBuilder;

  bNodeSocket &build(bNodeTree &ntree, bNode &node) const override;
  bool matches(const bNodeSocket &socket) const override;
  bNodeSocket &update_or_build(bNodeTree &ntree, bNode &node, bNodeSocket &socket) const override;
  bool can_connect(const bNodeSocket &socket) const override;
};
```

<details>
<summary>核对原始源码：source/blender/nodes/NOD_socket_declarations.hh · L94—L112</summary>

<!-- original:254592b0ffdd7a:source/blender/nodes/NOD_socket_declarations.hh:94:112 -->

```cpp
class Vector : public SocketDeclaration {
 public:
  static constexpr eNodeSocketDatatype static_socket_type = SOCK_VECTOR;

  float4 default_value = {0, 0, 0, 0};
  float soft_min_value = -FLT_MAX;
  float soft_max_value = FLT_MAX;
  int dimensions = 3;
  PropertySubType subtype = PROP_NONE;

  friend VectorBuilder;

  using Builder = VectorBuilder;

  bNodeSocket &build(bNodeTree &ntree, bNode &node) const override;
  bool matches(const bNodeSocket &socket) const override;
  bNodeSocket &update_or_build(bNodeTree &ntree, bNode &node, bNodeSocket &socket) const override;
  bool can_connect(const bNodeSocket &socket) const override;
};
```

</details>


<a id="t-44e5dc0a269f"></a>

### `blender::nodes::decl::Color`

原始声明：[source/blender/nodes/NOD_socket_declarations.hh](../../../../../source/blender/nodes/NOD_socket_declarations.hh) · L185—L199。

成员布局：

- `eNodeSocketDatatype static_socket_type`
- `ColorGeometry4f default_value`
- `bNodeSocket build`
- `bool matches`
- `bNodeSocket update_or_build`
- `bool can_connect`

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:c65ea55f732726 -->

```cpp
class Color : public SocketDeclaration {
 public:
  static constexpr eNodeSocketDatatype static_socket_type = SOCK_RGBA;

  ColorGeometry4f default_value{0.8f, 0.8f, 0.8f, 1.0f};

  friend ColorBuilder;

  using Builder = ColorBuilder;

  bNodeSocket &build(bNodeTree &ntree, bNode &node) const override;
  bool matches(const bNodeSocket &socket) const override;
  bNodeSocket &update_or_build(bNodeTree &ntree, bNode &node, bNodeSocket &socket) const override;
  bool can_connect(const bNodeSocket &socket) const override;
};
```

<details>
<summary>核对原始源码：source/blender/nodes/NOD_socket_declarations.hh · L185—L199</summary>

<!-- original:c65ea55f732726:source/blender/nodes/NOD_socket_declarations.hh:185:199 -->

```cpp
class Color : public SocketDeclaration {
 public:
  static constexpr eNodeSocketDatatype static_socket_type = SOCK_RGBA;

  ColorGeometry4f default_value{0.8f, 0.8f, 0.8f, 1.0f};

  friend ColorBuilder;

  using Builder = ColorBuilder;

  bNodeSocket &build(bNodeTree &ntree, bNode &node) const override;
  bool matches(const bNodeSocket &socket) const override;
  bNodeSocket &update_or_build(bNodeTree &ntree, bNode &node, bNodeSocket &socket) const override;
  bool can_connect(const bNodeSocket &socket) const override;
};
```

</details>


## 完整成员与函数实现
