# 实现依赖专题：source/blender/sequencer/intern/proxy.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::seq::rendersize_to_proxysize"]:::abstraction
  F1["blender::seq::rendersize_to_scale_factor"]:::compute
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
  F["proxy.cc实现"]:::compute
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

<a id="f-6dc1181f407c5fca"></a>

### `blender::seq::rendersize_to_proxysize`

实现位置：[source/blender/sequencer/intern/proxy.cc](../../../../../source/blender/sequencer/intern/proxy.cc) · L137—L151。

接口参数：

- `eSpaceSeq_Proxy_RenderSize render_size`

**教学注释版**

<!-- annotated:82cef59407cbc3 -->

```cpp
IMB_Proxy_Size rendersize_to_proxysize(eSpaceSeq_Proxy_RenderSize render_size)
{
  switch (render_size) {
    case SEQ_RENDER_SIZE_PROXY_25:
      return IMB_PROXY_25;
    case SEQ_RENDER_SIZE_PROXY_50:
      return IMB_PROXY_50;
    case SEQ_RENDER_SIZE_PROXY_75:
      return IMB_PROXY_75;
    case SEQ_RENDER_SIZE_PROXY_100:
      return IMB_PROXY_100;
    default:
      return IMB_PROXY_NONE;
  }
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/proxy.cc · L137—L151</summary>

<!-- original:82cef59407cbc3:source/blender/sequencer/intern/proxy.cc:137:151 -->

```cpp
IMB_Proxy_Size rendersize_to_proxysize(eSpaceSeq_Proxy_RenderSize render_size)
{
  switch (render_size) {
    case SEQ_RENDER_SIZE_PROXY_25:
      return IMB_PROXY_25;
    case SEQ_RENDER_SIZE_PROXY_50:
      return IMB_PROXY_50;
    case SEQ_RENDER_SIZE_PROXY_75:
      return IMB_PROXY_75;
    case SEQ_RENDER_SIZE_PROXY_100:
      return IMB_PROXY_100;
    default:
      return IMB_PROXY_NONE;
  }
}
```

</details>

**结果出口**

- `return IMB_PROXY_25;`
- `return IMB_PROXY_50;`
- `return IMB_PROXY_75;`
- `return IMB_PROXY_100;`
- `return IMB_PROXY_NONE;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-12b59564fd33774e"></a>

### `blender::seq::rendersize_to_scale_factor`

实现位置：[source/blender/sequencer/intern/proxy.cc](../../../../../source/blender/sequencer/intern/proxy.cc) · L153—L165。

接口参数：

- `eSpaceSeq_Proxy_RenderSize render_size`

**教学注释版**

<!-- annotated:3ed23fd7e3b30d -->

```cpp
float rendersize_to_scale_factor(eSpaceSeq_Proxy_RenderSize render_size)
{
  switch (render_size) {
    case SEQ_RENDER_SIZE_PROXY_25:
      return 0.25f;
    case SEQ_RENDER_SIZE_PROXY_50:
      return 0.5f;
    case SEQ_RENDER_SIZE_PROXY_75:
      return 0.75f;
    default:
      return 1.0f;
  }
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/proxy.cc · L153—L165</summary>

<!-- original:3ed23fd7e3b30d:source/blender/sequencer/intern/proxy.cc:153:165 -->

```cpp
float rendersize_to_scale_factor(eSpaceSeq_Proxy_RenderSize render_size)
{
  switch (render_size) {
    case SEQ_RENDER_SIZE_PROXY_25:
      return 0.25f;
    case SEQ_RENDER_SIZE_PROXY_50:
      return 0.5f;
    case SEQ_RENDER_SIZE_PROXY_75:
      return 0.75f;
    default:
      return 1.0f;
  }
}
```

</details>

**结果出口**

- `return 0.25f;`
- `return 0.5f;`
- `return 0.75f;`
- `return 1.0f;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
