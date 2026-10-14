# 09-LazyFunction与节点执行架构

[总入口](../README.md) · [几何节点专题](../13-几何节点专题/README.md) · [实现依赖](../90-实现依赖专题/README.md)

## 阅读顺序

- [09-01 按需执行模型](01-按需执行模型.md)
- [09-02 LazyFunction接口](02-LazyFunction接口.md)
- [09-03 Params与ValueUsage](03-Params与ValueUsage.md)
- [09-04 Context与执行状态](04-Context与执行状态.md)
- [09-05 Graph与Socket](05-Graph与Socket.md)
- [09-06 GraphExecutor对外接口](06-GraphExecutor对外接口.md)
- [09-07 执行器内部状态](07-执行器内部状态.md)
- [09-08 输入请求与调度](08-输入请求与调度.md)
- [09-09 几何节点图构建器](09-几何节点图构建器.md)
- [09-10 普通节点与函数适配](10-普通节点与函数适配.md)
- [09-11 Switch与MenuSwitch](11-Switch与MenuSwitch.md)
- [09-12 嵌套图副作用日志与测试](12-嵌套图副作用日志与测试.md)

```mermaid
flowchart TB
  E["09-LazyFunction与节点执行架构"]:::input
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
