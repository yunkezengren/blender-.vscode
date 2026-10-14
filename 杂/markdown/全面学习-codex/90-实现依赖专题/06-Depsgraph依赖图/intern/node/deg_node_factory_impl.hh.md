# 实现依赖专题：source/blender/depsgraph/intern/node/deg_node_factory_impl.hh

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::deg::DepsNodeFactoryImpl＜<br/>ModeObjectType＞::type"]:::abstraction
  F1["blender::deg::DepsNodeFactoryImpl＜<br/>ModeObjectType＞::id_recalc_tag"]:::compute
  F2["blender::deg::DepsNodeFactoryImpl＜<br/>ModeObjectType＞::create_node"]:::compute
  F2 -->|"显式调用"| F0
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
  F["deg_node_factory_impl.hh实现"]:::compute
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

<a id="f-05dd7d049c4d2af9"></a>

### `blender::deg::DepsNodeFactoryImpl<ModeObjectType>::type`

实现位置：[source/blender/depsgraph/intern/node/deg_node_factory_impl.hh](../../../../../../../../source/blender/depsgraph/intern/node/deg_node_factory_impl.hh) · L19—L22。

**教学注释版**

<!-- annotated:05318d13278eaf -->

```cpp
template<class ModeObjectType> NodeType DepsNodeFactoryImpl<ModeObjectType>::type() const
{
  return ModeObjectType::typeinfo.type;
}
```

<details>
<summary>核对原始源码：source/blender/depsgraph/intern/node/deg_node_factory_impl.hh · L19—L22</summary>

<!-- original:05318d13278eaf:source/blender/depsgraph/intern/node/deg_node_factory_impl.hh:19:22 -->

```cpp
template<class ModeObjectType> NodeType DepsNodeFactoryImpl<ModeObjectType>::type() const
{
  return ModeObjectType::typeinfo.type;
}
```

</details>

**结果出口**

- `return ModeObjectType::typeinfo.type;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-150f0311c1d40232"></a>

### `blender::deg::DepsNodeFactoryImpl<ModeObjectType>::id_recalc_tag`

实现位置：[source/blender/depsgraph/intern/node/deg_node_factory_impl.hh](../../../../../../../../source/blender/depsgraph/intern/node/deg_node_factory_impl.hh) · L29—L32。

**教学注释版**

<!-- annotated:91e66dffabd156 -->

```cpp
template<class ModeObjectType> int DepsNodeFactoryImpl<ModeObjectType>::id_recalc_tag() const
{
  return ModeObjectType::typeinfo.id_recalc_tag;
}
```

<details>
<summary>核对原始源码：source/blender/depsgraph/intern/node/deg_node_factory_impl.hh · L29—L32</summary>

<!-- original:91e66dffabd156:source/blender/depsgraph/intern/node/deg_node_factory_impl.hh:29:32 -->

```cpp
template<class ModeObjectType> int DepsNodeFactoryImpl<ModeObjectType>::id_recalc_tag() const
{
  return ModeObjectType::typeinfo.id_recalc_tag;
}
```

</details>

**结果出口**

- `return ModeObjectType::typeinfo.id_recalc_tag;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-dbf39120cc6cbb9b"></a>

### `blender::deg::DepsNodeFactoryImpl<ModeObjectType>::create_node`

实现位置：[source/blender/depsgraph/intern/node/deg_node_factory_impl.hh](../../../../../../../../source/blender/depsgraph/intern/node/deg_node_factory_impl.hh) · L34—L44。

接口参数：

- `const ID *id`
- `const char *subdata`
- `const StringRef name`

**教学注释版**

<!-- annotated:c8b17e1eb8b7eb -->

```cpp
template<class ModeObjectType>
Node *DepsNodeFactoryImpl<ModeObjectType>::create_node(const ID *id,
                                                       const char *subdata,
                                                       const StringRef name) const
{
  Node *node = new ModeObjectType();
  node->type = type();
  node->name = name;
  node->init(id, subdata);
  return node;
}
```

<details>
<summary>核对原始源码：source/blender/depsgraph/intern/node/deg_node_factory_impl.hh · L34—L44</summary>

<!-- original:c8b17e1eb8b7eb:source/blender/depsgraph/intern/node/deg_node_factory_impl.hh:34:44 -->

```cpp
template<class ModeObjectType>
Node *DepsNodeFactoryImpl<ModeObjectType>::create_node(const ID *id,
                                                       const char *subdata,
                                                       const StringRef name) const
{
  Node *node = new ModeObjectType();
  node->type = type();
  node->name = name;
  node->init(id, subdata);
  return node;
}
```

</details>

**沿实际写入检查状态**

- `node->type = type();`
- `node->name = name;`

**结果出口**

- `return node;`

**继续追踪实现**

- `type` → [blender::deg::DepsNodeFactoryImpl<ModeObjectType>::type · L19](deg_node_factory_impl.hh.md#f-05dd7d049c4d2af9)。
- `node->init` → [blender::deg::Node::init · L205](deg_node.hh.md#f-96ab30ad27861756)。
