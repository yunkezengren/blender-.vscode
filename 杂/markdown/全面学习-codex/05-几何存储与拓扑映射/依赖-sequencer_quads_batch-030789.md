# 实现依赖专题：source/blender/editors/space_sequencer/sequencer_quads_batch.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::ed::vse::SeqQuadsBatch::add_quad"]:::abstraction
  F1["blender::ed::vse::SeqQuadsBatch::add_quad"]:::compute
  F0 -->|"显式调用"| F0
  F0 -->|"显式调用"| F1
  F1 -->|"显式调用"| F0
  F1 -->|"显式调用"| F1
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
  F["sequencer_quads_batch.hh实现"]:::compute
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

<a id="f-2e8ac61d5a32adfb"></a>

### `blender::ed::vse::SeqQuadsBatch::add_quad`

实现位置：[source/blender/editors/space_sequencer/sequencer_quads_batch.hh](../../../../../source/blender/editors/space_sequencer/sequencer_quads_batch.hh) · L41—L44。

接口参数：

- `float x1`
- `float y1`
- `float x2`
- `float y2`
- `const uchar color[4]`

**教学注释版**

<!-- annotated:8a0fa3d72ea0f3 -->

```cpp
  void add_quad(float x1, float y1, float x2, float y2, const uchar color[4])
  {
    add_quad(x1, y1, x1, y2, x2, y1, x2, y2, color, color, color, color);
  }
```

<details>
<summary>核对原始源码：source/blender/editors/space_sequencer/sequencer_quads_batch.hh · L41—L44</summary>

<!-- original:8a0fa3d72ea0f3:source/blender/editors/space_sequencer/sequencer_quads_batch.hh:41:44 -->

```cpp
  void add_quad(float x1, float y1, float x2, float y2, const uchar color[4])
  {
    add_quad(x1, y1, x1, y2, x2, y1, x2, y2, color, color, color, color);
  }
```

</details>

**继续追踪实现**

- `add_quad` → [blender::ed::vse::SeqQuadsBatch::add_quad · L41](%E4%BE%9D%E8%B5%96-sequencer_quads_batch-030789.md#f-2e8ac61d5a32adfb)；[blender::ed::vse::SeqQuadsBatch::add_quad · L46](%E4%BE%9D%E8%B5%96-sequencer_quads_batch-030789.md#f-514c59e2224fe61c)。同名重载需按实参类型选择。

<a id="f-514c59e2224fe61c"></a>

### `blender::ed::vse::SeqQuadsBatch::add_quad`

实现位置：[source/blender/editors/space_sequencer/sequencer_quads_batch.hh](../../../../../source/blender/editors/space_sequencer/sequencer_quads_batch.hh) · L46—L57。

接口参数：

- `float x1`
- `float y1`
- `float x2`
- `float y2`
- `float x3`
- `float y3`
- `float x4`
- `float y4`
- `const uchar color[4]`

**教学注释版**

<!-- annotated:e756f406eeaa17 -->

```cpp
  void add_quad(float x1,
                float y1,
                float x2,
                float y2,
                float x3,
                float y3,
                float x4,
                float y4,
                const uchar color[4])
  {
    add_quad(x1, y1, x2, y2, x3, y3, x4, y4, color, color, color, color);
  }
```

<details>
<summary>核对原始源码：source/blender/editors/space_sequencer/sequencer_quads_batch.hh · L46—L57</summary>

<!-- original:e756f406eeaa17:source/blender/editors/space_sequencer/sequencer_quads_batch.hh:46:57 -->

```cpp
  void add_quad(float x1,
                float y1,
                float x2,
                float y2,
                float x3,
                float y3,
                float x4,
                float y4,
                const uchar color[4])
  {
    add_quad(x1, y1, x2, y2, x3, y3, x4, y4, color, color, color, color);
  }
```

</details>

**继续追踪实现**

- `add_quad` → [blender::ed::vse::SeqQuadsBatch::add_quad · L41](%E4%BE%9D%E8%B5%96-sequencer_quads_batch-030789.md#f-2e8ac61d5a32adfb)；[blender::ed::vse::SeqQuadsBatch::add_quad · L46](%E4%BE%9D%E8%B5%96-sequencer_quads_batch-030789.md#f-514c59e2224fe61c)。同名重载需按实参类型选择。
