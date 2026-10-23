# 00-课程指南

[总入口](../README.md)

## [01-学习路线与阶段验收](01-学习路线与阶段验收.md)

五个阶段：Zone 基础 → 数据模型 → 执行架构 → 运行时 → 跨后端与实战。每阶段给出可手算核对的最小练习与验收问题。

## [02-图表配色与阅读约定](02-图表配色与阅读约定.md)

全系列统一的 mermaid 配色 classDef、源码链接格式、教学注释代码与原始源码折叠区的阅读方法。

## [03-符号与源码索引](03-符号与源码索引.md)

全部关键符号（类、结构、函数、DNA 结构）到源码文件的定位表，以及各文件被哪些文档覆盖的覆盖矩阵。

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"\"Segoe UI\",\"Microsoft YaHei\",sans-serif","fontSize":"15px","lineColor":"#94A3B8","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F8FAFC","clusterBorder":"#CBD5E1"},"flowchart":{"htmlLabels":false,"curve":"basis","nodeSpacing":52,"rankSpacing":64,"padding":14,"diagramPadding":16,"useMaxWidth":true},"sequence":{"useMaxWidth":true,"wrap":true,"mirrorActors":false,"messageMargin":36}}}%%
flowchart TB
  E["课程指南"]:::input
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

