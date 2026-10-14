# 04-虚拟数组与索引选择

[总入口](../README.md) · [几何节点专题](../13-几何节点专题/README.md) · [实现依赖](../90-实现依赖专题/README.md)

## 阅读顺序

- [04-01 VArray表示与值语义](01-VArray表示与值语义.md)
- [04-02 VArrayImpl实现接口](02-VArrayImpl实现接口.md)
- [04-03 单值与Span表示](03-单值与Span表示.md)
- [04-04 所有权与小对象优化](04-所有权与小对象优化.md)
- [04-05 GVArray运行时类型](05-GVArray运行时类型.md)
- [04-06 切片与物化](06-切片与物化.md)
- [04-07 去虚拟化与优化](07-去虚拟化与优化.md)
- [04-08 IndexMask总体表示](08-IndexMask总体表示.md)
- [04-09 分段存储与遍历](09-分段存储与遍历.md)
- [04-10 IndexMask构建与并行](10-IndexMask构建与并行.md)
- [04-11 集合表达式与运算](11-集合表达式与运算.md)
- [04-12 重构历史与基准练习](12-重构历史与基准练习.md)

```mermaid
flowchart TB
  E["04-虚拟数组与索引选择"]:::input
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

```mermaid
flowchart TB
  M["主线学习"]:::input
  D["类与函数实现"]:::data
  H["历史提交与证据"]:::abstraction
  M -->|"深入"| D
  D -->|"核对演化"| H
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```
