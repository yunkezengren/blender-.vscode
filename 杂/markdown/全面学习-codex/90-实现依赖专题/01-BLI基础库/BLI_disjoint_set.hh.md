# 实现依赖专题：source/blender/blenlib/BLI_disjoint_set.hh

[实现依赖导航](../README.md) · [符号索引](../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::DisjointSet::join"]:::abstraction
  F1["blender::DisjointSet::find_root"]:::compute
  F2["blender::DisjointSet::find_root"]:::compute
  F0 -->|"显式调用"| F1
  F0 -->|"显式调用"| F2
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
  F["BLI_disjoint_set.hh实现"]:::compute
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

<a id="f-f2d8d8020d7e147e"></a>

### `blender::DisjointSet::join`

实现位置：[source/blender/blenlib/BLI_disjoint_set.hh](../../../../../../source/blender/blenlib/BLI_disjoint_set.hh) · L39—L60。

接口参数：

- `const T x`
- `const T y`

**教学注释版**

<!-- annotated:a426f5473276a4 -->

```cpp
  T join(const T x, const T y)
  {
    T root1 = this->find_root(x);
    T root2 = this->find_root(y);

    /* x and y are in the same set already. */
    if (root1 == root2) {
      return root1;
    }

    /* Implement union by rank heuristic. */
    if (ranks_[root1] < ranks_[root2]) {
      std::swap(root1, root2);
    }
    parents_[root2] = root1;

    if (ranks_[root1] == ranks_[root2]) {
      ranks_[root1]++;
    }

    return root1;
  }
```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_disjoint_set.hh · L39—L60</summary>

<!-- original:a426f5473276a4:source/blender/blenlib/BLI_disjoint_set.hh:39:60 -->

```cpp
  T join(const T x, const T y)
  {
    T root1 = this->find_root(x);
    T root2 = this->find_root(y);

    /* x and y are in the same set already. */
    if (root1 == root2) {
      return root1;
    }

    /* Implement union by rank heuristic. */
    if (ranks_[root1] < ranks_[root2]) {
      std::swap(root1, root2);
    }
    parents_[root2] = root1;

    if (ranks_[root1] == ranks_[root2]) {
      ranks_[root1]++;
    }

    return root1;
  }
```

</details>

**沿实际写入检查状态**

- `parents_[root2] = root1;`

**结果出口**

- `return root1;`

**继续追踪实现**

- `this->find_root` → [blender::DisjointSet::find_root · L75](BLI_disjoint_set.hh.md#f-b2db4b94d1f37228)；[blender::DisjointSet::find_root · L98](BLI_disjoint_set.hh.md#f-e3e7d5849d67bf64)。同名重载需按实参类型选择。
- `std::swap` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。

<a id="f-b2db4b94d1f37228"></a>

### `blender::DisjointSet::find_root`

实现位置：[source/blender/blenlib/BLI_disjoint_set.hh](../../../../../../source/blender/blenlib/BLI_disjoint_set.hh) · L75—L92。

接口参数：

- `const T x`

**教学注释版**

<!-- annotated:8464030da88af9 -->

```cpp
  T find_root(const T x)
  {
    /* Find root by following parents. */
    T root = x;
    while (parents_[root] != root) {
      root = parents_[root];
    }

    /* Compress path. */
    T to_root = x;
    while (parents_[to_root] != root) {
      const T parent = parents_[to_root];
      parents_[to_root] = root;
      to_root = parent;
    }

    return root;
  }
```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_disjoint_set.hh · L75—L92</summary>

<!-- original:8464030da88af9:source/blender/blenlib/BLI_disjoint_set.hh:75:92 -->

```cpp
  T find_root(const T x)
  {
    /* Find root by following parents. */
    T root = x;
    while (parents_[root] != root) {
      root = parents_[root];
    }

    /* Compress path. */
    T to_root = x;
    while (parents_[to_root] != root) {
      const T parent = parents_[to_root];
      parents_[to_root] = root;
      to_root = parent;
    }

    return root;
  }
```

</details>

**沿实际写入检查状态**

- `root = parents_[root];`
- `parents_[to_root] = root;`
- `to_root = parent;`

**结果出口**

- `return root;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-e3e7d5849d67bf64"></a>

### `blender::DisjointSet::find_root`

实现位置：[source/blender/blenlib/BLI_disjoint_set.hh](../../../../../../source/blender/blenlib/BLI_disjoint_set.hh) · L98—L107。

接口参数：

- `const T x`

**教学注释版**

<!-- annotated:6f05edbb12465e -->

```cpp
  T find_root(const T x) const
  {
    /* Find root by following parents. */
    T root = x;
    while (parents_[root] != root) {
      root = parents_[root];
    }

    return root;
  }
```

<details>
<summary>核对原始源码：source/blender/blenlib/BLI_disjoint_set.hh · L98—L107</summary>

<!-- original:6f05edbb12465e:source/blender/blenlib/BLI_disjoint_set.hh:98:107 -->

```cpp
  T find_root(const T x) const
  {
    /* Find root by following parents. */
    T root = x;
    while (parents_[root] != root) {
      root = parents_[root];
    }

    return root;
  }
```

</details>

**沿实际写入检查状态**

- `root = parents_[root];`

**结果出口**

- `return root;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
