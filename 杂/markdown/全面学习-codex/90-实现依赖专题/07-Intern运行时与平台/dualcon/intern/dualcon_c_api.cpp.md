# 实现依赖专题：intern/dualcon/intern/dualcon_c_api.cpp

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["dualcon"]:::abstraction
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
  F["dualcon_c_api.cpp实现"]:::compute
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

<a id="f-5368118f05498460"></a>

### `dualcon`

实现位置：[intern/dualcon/intern/dualcon_c_api.cpp](../../../../../../../../intern/dualcon/intern/dualcon_c_api.cpp) · L144—L161。

接口参数：

- `const DualConInput *input_mesh`
- `DualConAllocOutput alloc_output`
- `DualConAddVert add_vert`
- `DualConAddQuad add_quad`
- `DualConFlags flags`
- `DualConMode mode`
- `float threshold`
- `float hermite_num`
- `float scale`
- `int depth`

**教学注释版**

<!-- annotated:c095b1b6ce14f1 -->

```cpp
void *dualcon(const DualConInput *input_mesh,
              /* callbacks for output */
              DualConAllocOutput alloc_output,
              DualConAddVert add_vert,
              DualConAddQuad add_quad,

              DualConFlags flags,
              DualConMode mode,
              float threshold,
              float hermite_num,
              float scale,
              int depth)
{
  DualConInputReader r(input_mesh, scale);
  Octree o(&r, alloc_output, add_vert, add_quad, flags, mode, depth, threshold, hermite_num);
  o.scanConvert();
  return o.getOutputMesh();
}
```

<details>
<summary>核对原始源码：intern/dualcon/intern/dualcon_c_api.cpp · L144—L161</summary>

<!-- original:c095b1b6ce14f1:intern/dualcon/intern/dualcon_c_api.cpp:144:161 -->

```cpp
void *dualcon(const DualConInput *input_mesh,
              /* callbacks for output */
              DualConAllocOutput alloc_output,
              DualConAddVert add_vert,
              DualConAddQuad add_quad,

              DualConFlags flags,
              DualConMode mode,
              float threshold,
              float hermite_num,
              float scale,
              int depth)
{
  DualConInputReader r(input_mesh, scale);
  Octree o(&r, alloc_output, add_vert, add_quad, flags, mode, depth, threshold, hermite_num);
  o.scanConvert();
  return o.getOutputMesh();
}
```

</details>

**结果出口**

- `return o.getOutputMesh();`

**继续追踪实现**

- `o.scanConvert` → [Octree::scanConvert · L97](octree.cpp.md#f-37a8c526eb3297e7)。
- `o.getOutputMesh` → [Octree::getOutputMesh · L279](octree.h.md#f-40b7872ee42b46ff)。
