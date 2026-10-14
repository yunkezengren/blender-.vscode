# 02-哈希表与关联数据结构

[总入口](../README.md) · [几何节点专题](../13-几何节点专题/README.md) · [实现依赖](../90-实现依赖专题/README.md)

## 阅读顺序

- [02-01 哈希与相等契约](01-哈希与相等契约.md)
- [02-02 Map总体布局](02-Map总体布局.md)
- [02-03 槽位状态与探测](03-槽位状态与探测.md)
- [02-04 Map查找与键访问](04-Map查找与键访问.md)
- [02-05 Map插入与回调](05-Map插入与回调.md)
- [02-06 删除墓碑与值销毁](06-删除墓碑与值销毁.md)
- [02-07 重建与摊还复杂度](07-重建与摊还复杂度.md)
- [02-08 Set与集合语义](08-Set与集合语义.md)
- [02-09 MultiValueMap一键多值](09-MultiValueMap一键多值.md)
- [02-10 浮点修复与基础库对比](10-浮点修复与基础库对比.md)

```mermaid
flowchart TB
  E["02-哈希表与关联数据结构"]:::input
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
