# 05-几何存储与拓扑映射

[总入口](../README.md) · [几何节点专题](../13-几何节点专题/README.md) · [实现依赖](../90-实现依赖专题/README.md)

## 阅读顺序

- [05-01 Mesh顶点边面角点](01-Mesh顶点边面角点.md)
- [05-02 OffsetIndices完整接口](02-OffsetIndices完整接口.md)
- [05-03 MPoly迁移与兼容](03-MPoly迁移与兼容.md)
- [05-04 CurvesGeometry存储](04-CurvesGeometry存储.md)
- [05-05 邻接关系与前缀和](05-邻接关系与前缀和.md)
- [05-06 拓扑映射构建](06-拓扑映射构建.md)
- [05-07 分组访问与反向索引](07-分组访问与反向索引.md)
- [05-08 AttributeAccessor接口](08-AttributeAccessor接口.md)
- [05-09 属性域与转换](09-属性域与转换.md)
- [05-10 布局兼容与几何实战](10-布局兼容与几何实战.md)

```mermaid
flowchart TB
  E["05-几何存储与拓扑映射"]:::input
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
