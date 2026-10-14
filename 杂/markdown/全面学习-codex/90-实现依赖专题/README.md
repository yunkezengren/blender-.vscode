# 实现依赖专题

[总入口](../README.md) · [符号索引](../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

这些是正文引用的辅助实现资料，按实际源码模块分类；不需要从头顺序阅读全部文件。文件名保留对应源码扩展名，便于识别头文件与实现文件。

- [01-BLI基础库 · 203份](01-BLI基础库/README.md)
- [02-BKE几何与数据 · 307份](02-BKE几何与数据/README.md)
- [03-FN函数与求值 · 4份](03-FN函数与求值/README.md)
- [04-Nodes节点系统 · 119份](04-Nodes节点系统/README.md)
- [05-Geometry几何算法 · 17份](05-Geometry几何算法/README.md)
- [06-Depsgraph依赖图 · 45份](06-Depsgraph依赖图/README.md)
- [07-Intern运行时与平台 · 167份](07-Intern运行时与平台/README.md)
- [08-其他Blender模块 · 890份](08-其他Blender模块/README.md)

```mermaid
flowchart TB
  E["实现依赖"]:::input
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
