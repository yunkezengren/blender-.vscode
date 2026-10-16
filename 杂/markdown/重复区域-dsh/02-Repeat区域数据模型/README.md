# 02-Repeat区域数据模型

[总入口](../README.md) · [课程指南](../00-课程指南/README.md) · [上一章](../01-Zone系统基础/README.md)

本章回答：Repeat 节点如何注册、它的用户可见数据（Repeat Items）存在哪里、如何被通用框架管理。

## 阅读顺序

- [02-01 Repeat节点注册与UI](01-Repeat节点注册与UI.md)
- [02-02 DNA存储与NodeRepeatItem](02-DNA存储与NodeRepeatItem.md)
- [02-03 SocketItems通用条目框架](03-SocketItems通用条目框架.md)

## 本章问题

- Repeat Input/Output 的类型如何注册？UI 面板如何绘制条目列表？
- `NodeRepeatItem` 的 `identifier` 为什么必须稳定？
- `NodeGeometryRepeatOutput` 的存储布局与 blend 读写全链路？
- `NOD_socket_items.hh` 的访问器协议如何把重复逻辑抽出来？

```mermaid
flowchart TB
  E["02-Repeat区域数据模型"]:::input
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
