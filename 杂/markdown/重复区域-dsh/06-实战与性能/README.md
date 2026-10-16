# 06-实战与性能

[总入口](../README.md) · [课程指南](../00-课程指南/README.md) · [上一章](../05-跨后端实现/README.md)

本章从源码转向应用：Repeat 区域的典型使用模式、迭代设计纪律与性能成本模型。

## 阅读顺序

- [06-01 使用模式与迭代设计](01-使用模式与迭代设计.md)
- [06-02 性能模型与开销分析](02-性能模型与开销分析.md)

## 本章问题

- Repeat、Simulation、Foreach 都是循环，什么时候用哪个？
- "轮间传递的状态"与"每轮可见的外部值"（border link）如何区分使用？
- 一次 Repeat 求值的总成本由哪几项构成？哪些是固定开销、哪些随迭代数线性增长？
- 有哪些诊断工具能定位 Repeat 的性能问题？

```mermaid
flowchart TB
  E["06-实战与性能"]:::input
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
