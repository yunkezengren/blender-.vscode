# 03-几何节点执行架构

本章回答：几何节点求值器如何把一个 Repeat 区域"编译"成可执行的 LazyFunction 图。这是全系列的核心章。

## 阅读顺序

- [03-01 ZoneBodyFunction与ZoneBuildInfo](01-ZoneBodyFunction与ZoneBuildInfo.md)
- [03-02 Repeat循环体函数构建详解](02-Repeat循环体函数构建详解.md)
- [03-03 执行图按迭代展开](03-执行图按迭代展开.md)

## 本章问题

- zone 构建顺序为什么按深度排序（先内后外）？
- 循环体函数（ZoneBodyFunction）的输入/输出分组：main、border_links、output_usages、reference_sets 各是什么？
- 为什么迭代数要等运行时才知道，执行图如何在第一次求值时按迭代数展开？
- 成对串联（body N → body N+1）与 LogicalOr 节点分别解决什么问题？

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"\"Segoe UI\",\"Microsoft YaHei\",sans-serif","fontSize":"15px","lineColor":"#94A3B8","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F8FAFC","clusterBorder":"#CBD5E1"},"flowchart":{"htmlLabels":false,"curve":"basis","nodeSpacing":52,"rankSpacing":64,"padding":14,"diagramPadding":16,"useMaxWidth":true},"sequence":{"useMaxWidth":true,"wrap":true,"mirrorActors":false,"messageMargin":36}}}%%
flowchart TB
  E["03-几何节点执行架构"]:::input
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

