# 01-Zone系统基础

本章回答：Repeat 区域在节点树数据层面是什么？两个看起来独立的节点如何组成一个区域，区域内的 socket 与连线如何表示。

## 阅读顺序

- [01-01 NodeTreeZone区域表示与配对](01-NodeTreeZone区域表示与配对.md)
- [01-02 Zone输入输出与bundle迁移语义](02-Zone输入输出与bundle迁移语义.md)

## 本章问题

- `bNodeTreeZone` 如何表示一个区域，`parent_zone`/`child_zones` 如何形成嵌套树？
- Repeat Input 与 Repeat Output 如何配对？
- 区域的动态 socket（Item_X）如何生成、为何改名不断链接？
- 区域内的值在编辑器追踪（trace）时如何穿过区域边界？

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"\"Segoe UI\",\"Microsoft YaHei\",sans-serif","fontSize":"15px","lineColor":"#94A3B8","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F8FAFC","clusterBorder":"#CBD5E1"},"flowchart":{"htmlLabels":false,"curve":"basis","nodeSpacing":52,"rankSpacing":64,"padding":14,"diagramPadding":16,"useMaxWidth":true},"sequence":{"useMaxWidth":true,"wrap":true,"mirrorActors":false,"messageMargin":36}}}%%
flowchart TB
  E["01-Zone系统基础"]:::input
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

