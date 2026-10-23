# 05-跨后端实现

同一套 Repeat 区域语义，在三个执行后端里有三种截然不同的实现方式。本章逐个拆解。

## 阅读顺序

- [05-01 合成器RepeatZoneOperation](01-合成器RepeatZoneOperation.md)
- [05-02 GPU着色器与GPU_stack_link_zone](02-GPU着色器与GPU_stack_link_zone.md)

## 本章问题

- 几何节点把循环体复制 N 份拼成一张图，合成器为什么不这么干？
- 合成器逐轮之间如何传递数据（Result 共享）？取消时输出是什么？
- GPU 后端如何把 Repeat 区域编译成着色器循环（REPEAT_BEGIN/END 宏）？
- 三种后端各自的约束与限制是什么？

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"\"Segoe UI\",\"Microsoft YaHei\",sans-serif","fontSize":"15px","lineColor":"#94A3B8","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F8FAFC","clusterBorder":"#CBD5E1"},"flowchart":{"htmlLabels":false,"curve":"basis","nodeSpacing":52,"rankSpacing":64,"padding":14,"diagramPadding":16,"useMaxWidth":true},"sequence":{"useMaxWidth":true,"wrap":true,"mirrorActors":false,"messageMargin":36}}}%%
flowchart TB
  E["05-跨后端实现"]:::input
  Q["按主题选择正文"]:::abstraction
  S["按需追踪实现依赖"]:::compute
  R["回到调用点核对行为"]:::result
  E -->|"进入"| Q
  Q -->|"查实现"| S
  S -->|"带着问题返回"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

