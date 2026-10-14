# 06-隐式共享与缓存系统

[总入口](../README.md) · [几何节点专题](../13-几何节点专题/README.md) · [实现依赖](../90-实现依赖专题/README.md)

## 阅读顺序

- [06-01 所有权与写时复制](01-所有权与写时复制.md)
- [06-02 ImplicitSharingInfo计数](02-ImplicitSharingInfo计数.md)
- [06-03 Mixin与共享指针封装](03-Mixin与共享指针封装.md)
- [06-04 GeometryComponent共享](04-GeometryComponent共享.md)
- [06-05 GeometrySet读写与复制](05-GeometrySet读写与复制.md)
- [06-06 CacheMutex惰性初始化](06-CacheMutex惰性初始化.md)
- [06-07 SharedCache跨对象复用](07-SharedCache跨对象复用.md)
- [06-08 法线缓存的真实依赖](08-法线缓存的真实依赖.md)
- [06-09 BVH共享与运行时数据](09-BVH共享与运行时数据.md)
- [06-10 局部更新与失效修复](10-局部更新与失效修复.md)

```mermaid
flowchart TB
  E["06-隐式共享与缓存系统"]:::input
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
