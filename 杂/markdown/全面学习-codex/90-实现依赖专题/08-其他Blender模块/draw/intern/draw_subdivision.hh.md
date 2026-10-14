# 实现依赖专题：source/blender/draw/intern/draw_subdivision.hh

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::draw::subdiv_edges_per_coarse_edge"]:::abstraction
  F1["blender::draw::subdiv_verts_per_coarse_edge"]:::compute
  F2["blender::draw::subdiv_loose_edges_num"]:::compute
  F3["blender::draw::subdiv_full_vbo_size"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F0
  F3 -->|"显式调用"| F2
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
  F["draw_subdivision.hh实现"]:::compute
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

<a id="t-900e0da6e1a8"></a>

### `blender::ToolSettings`

原始声明：[source/blender/draw/intern/draw_subdivision.hh](../../../../../../../../source/blender/draw/intern/draw_subdivision.hh) · L33—L33。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:813c2b9cc883fa -->

```cpp
struct ToolSettings;
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_subdivision.hh · L33—L33</summary>

<!-- original:813c2b9cc883fa:source/blender/draw/intern/draw_subdivision.hh:33:33 -->

```cpp
struct ToolSettings;
```

</details>


## 完整成员与函数实现

<a id="f-29b57ae81803ddc2"></a>

### `blender::draw::subdiv_edges_per_coarse_edge`

实现位置：[source/blender/draw/intern/draw_subdivision.hh](../../../../../../../../source/blender/draw/intern/draw_subdivision.hh) · L260—L263。

接口参数：

- `const DRWSubdivCache &cache`

**教学注释版**

<!-- annotated:175469373e021c -->

```cpp
inline int subdiv_edges_per_coarse_edge(const DRWSubdivCache &cache)
{
  return cache.resolution - 1;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_subdivision.hh · L260—L263</summary>

<!-- original:175469373e021c:source/blender/draw/intern/draw_subdivision.hh:260:263 -->

```cpp
inline int subdiv_edges_per_coarse_edge(const DRWSubdivCache &cache)
{
  return cache.resolution - 1;
}
```

</details>

**结果出口**

- `return cache.resolution - 1;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-57bd5b1d183a1da8"></a>

### `blender::draw::subdiv_verts_per_coarse_edge`

实现位置：[source/blender/draw/intern/draw_subdivision.hh](../../../../../../../../source/blender/draw/intern/draw_subdivision.hh) · L266—L269。

接口参数：

- `const DRWSubdivCache &cache`

**教学注释版**

<!-- annotated:822fc6d49605a7 -->

```cpp
inline int subdiv_verts_per_coarse_edge(const DRWSubdivCache &cache)
{
  return subdiv_edges_per_coarse_edge(cache) * 2;
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_subdivision.hh · L266—L269</summary>

<!-- original:822fc6d49605a7:source/blender/draw/intern/draw_subdivision.hh:266:269 -->

```cpp
inline int subdiv_verts_per_coarse_edge(const DRWSubdivCache &cache)
{
  return subdiv_edges_per_coarse_edge(cache) * 2;
}
```

</details>

**结果出口**

- `return subdiv_edges_per_coarse_edge(cache) * 2;`

**继续追踪实现**

- `subdiv_edges_per_coarse_edge` → [blender::draw::subdiv_edges_per_coarse_edge · L260](draw_subdivision.hh.md#f-29b57ae81803ddc2)。

<a id="f-d1a5e50512c1cd67"></a>

### `blender::draw::subdiv_loose_edges_num`

实现位置：[source/blender/draw/intern/draw_subdivision.hh](../../../../../../../../source/blender/draw/intern/draw_subdivision.hh) · L272—L275。

接口参数：

- `const MeshRenderData &mr`
- `const DRWSubdivCache &cache`

**教学注释版**

<!-- annotated:796c9cb0af69f6 -->

```cpp
inline int subdiv_loose_edges_num(const MeshRenderData &mr, const DRWSubdivCache &cache)
{
  return mr.loose_edges.size() * subdiv_edges_per_coarse_edge(cache);
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_subdivision.hh · L272—L275</summary>

<!-- original:796c9cb0af69f6:source/blender/draw/intern/draw_subdivision.hh:272:275 -->

```cpp
inline int subdiv_loose_edges_num(const MeshRenderData &mr, const DRWSubdivCache &cache)
{
  return mr.loose_edges.size() * subdiv_edges_per_coarse_edge(cache);
}
```

</details>

**结果出口**

- `return mr.loose_edges.size() * subdiv_edges_per_coarse_edge(cache);`

**继续追踪实现**

- `mr.loose_edges.size` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L274。
- `subdiv_edges_per_coarse_edge` → [blender::draw::subdiv_edges_per_coarse_edge · L260](draw_subdivision.hh.md#f-29b57ae81803ddc2)。

<a id="f-9ffb9094e78cfdac"></a>

### `blender::draw::subdiv_full_vbo_size`

实现位置：[source/blender/draw/intern/draw_subdivision.hh](../../../../../../../../source/blender/draw/intern/draw_subdivision.hh) · L278—L281。

接口参数：

- `const MeshRenderData &mr`
- `const DRWSubdivCache &cache`

**教学注释版**

<!-- annotated:7709073088cd21 -->

```cpp
inline int subdiv_full_vbo_size(const MeshRenderData &mr, const DRWSubdivCache &cache)
{
  return cache.num_subdiv_loops + subdiv_loose_edges_num(mr, cache) * 2 + mr.loose_verts.size();
}
```

<details>
<summary>核对原始源码：source/blender/draw/intern/draw_subdivision.hh · L278—L281</summary>

<!-- original:7709073088cd21:source/blender/draw/intern/draw_subdivision.hh:278:281 -->

```cpp
inline int subdiv_full_vbo_size(const MeshRenderData &mr, const DRWSubdivCache &cache)
{
  return cache.num_subdiv_loops + subdiv_loose_edges_num(mr, cache) * 2 + mr.loose_verts.size();
}
```

</details>

**结果出口**

- `return cache.num_subdiv_loops + subdiv_loose_edges_num(mr, cache) * 2 + mr.loose_verts.size();`

**继续追踪实现**

- `subdiv_loose_edges_num` → [blender::draw::subdiv_loose_edges_num · L272](draw_subdivision.hh.md#f-d1a5e50512c1cd67)。
- `mr.loose_verts.size` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L280。
