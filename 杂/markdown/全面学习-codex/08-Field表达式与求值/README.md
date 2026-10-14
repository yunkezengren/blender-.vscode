# 08-Field表达式与求值

[总入口](../README.md) · [几何节点专题](../13-几何节点专题/README.md) · [实现依赖](../90-实现依赖专题/README.md)

## 阅读顺序

- [08-01 Field语义与表达式](01-Field语义与表达式.md)
- [08-02 GField存储表示](02-GField存储表示.md)
- [08-03 Field类型接口](03-Field类型接口.md)
- [08-04 FieldInput输入节点](04-FieldInput输入节点.md)
- [08-05 FieldOperation运算节点](05-FieldOperation运算节点.md)
- [08-06 FieldContext上下文](06-FieldContext上下文.md)
- [08-07 FieldEvaluator接口与使用](07-FieldEvaluator接口与使用.md)
- [08-08 表达式分析与共享子图](08-表达式分析与共享子图.md)
- [08-09 生成Procedure与执行](09-生成Procedure与执行.md)
- [08-10 几何上下文与属性域](10-几何上下文与属性域.md)
- [08-11 SetPosition完整调用链](11-SetPosition完整调用链.md)
- [08-12 Field重构与深链销毁](12-Field重构与深链销毁.md)

```mermaid
flowchart TB
  E["08-Field表达式与求值"]:::input
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
