# 属性文本遮挡剔除 · CODEX 核对版

> **范围**：Blender `attribute-text-depth-culling` 分支。
> **基准**：`origin/main` 的 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`。
> **当前提交**：`39009b48098`、`eb97266f783`。
> **写作快照**：2026-09-27。
> **状态**：代码已编译，近距离网格点遮挡稳定性仍未解决。

---

## 为什么另建这个目录

`.markdown/属性文本遮挡剔除-DS` 已有大量参考文档。
本目录独立记录**当前分支的已提交行为**，并对照源码纠正不准确或过时的结论。
不会覆盖参考目录。
后续源码若改变，应把本目录当成有版本范围的快照，而不是永远正确的规范。

> [!IMPORTANT]
> 本目录与整个 `.markdown` 路径被项目 `.gitignore` 忽略。
> 它们是本地文档；若想纳入 Git，需要另作明确决定。

## 十三章导航

```mermaid
flowchart LR
  START[先读 01 总览] --> CORE[02 深度缓存]
  START --> ANCHOR[03 锚点与包围盒]
  CORE --> DEBUG[04 误判诊断]
  ANCHOR --> OPTIONS[07 方案取舍]
  DEBUG --> TEST[06 验证矩阵]
  CORE --> API[05 API 速查]
  API --> TRACE[08 代码导读]
  TRACE --> MATH[09 数学专题]
  TRACE --> TYPES[10 生命周期]
  TEST --> EXAMPLES[11 数值例题]
  EXAMPLES --> GLOSSARY[12 术语]
  GLOSSARY --> REVIEW[13 审查问答]
  classDef intro fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A,stroke-width:2px;
  classDef core fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef verify fill:#D1FAE5,stroke:#059669,color:#064E3B,stroke-width:2px;
  classDef refs fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  class START intro;
  class CORE,ANCHOR,DEBUG,OPTIONS,API,TRACE core;
  class TEST,EXAMPLES verify;
  class MATH,TYPES,GLOSSARY,REVIEW refs;
```

```mermaid
flowchart LR
  START[先读 01 总览] --> CORE[02 深度缓存]
  START --> ANCHOR[03 锚点与包围盒]
  CORE --> DEBUG[04 误判诊断]
  ANCHOR --> OPTIONS[07 方案取舍]
  DEBUG --> TEST[06 验证矩阵]
  CORE --> API[05 API 速查]
  API --> TRACE[08 代码导读]
  TRACE --> MATH[09 数学专题]
  TRACE --> TYPES[10 生命周期]
  TEST --> EXAMPLES[11 数值例题]
  EXAMPLES --> GLOSSARY[12 术语]
  GLOSSARY --> REVIEW[13 审查问答]
  classDef intro fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A,stroke-width:2px;
  classDef core fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef verify fill:#D1FAE5,stroke:#059669,color:#064E3B,stroke-width:2px;
  classDef refs fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  class START intro;
  class CORE,ANCHOR,DEBUG,OPTIONS,API,TRACE core;
  class TEST,EXAMPLES verify;
  class MATH,TYPES,GLOSSARY,REVIEW refs;
```

| 章节 | 重点 | 建议读者 |
|---|---|---|
| [01 · 架构与状态](./01-当前分支架构与状态.md) | 两个提交、九个文件、完整数据流 | 第一次接触此功能 |
| [02 · 逐帧深度缓存](./02-深度缓存与文本绘制.md) | 回读时序、所有权、投影和比较 | Overlay / Draw 维护者 |
| [03 · 锚点与包围盒](./03-锚点与包围盒.md) | 点云半径、实例 AABB、射线参数 | 数学与几何实现者 |
| [04 · 故障与实验](./04-误判诊断与实验复盘.md) | 五类症状、贮藏实验、勘误 | 正在复现闪烁的人 |
| [05 · API 速查](./05-函数与数据结构速查.md) | 函数职责、参数和生命周期 | 查接口的人 |
| [06 · 验证矩阵](./06-验证矩阵与性能评估.md) | 视口用例、构建和帧时记录 | 测试与 review |
| [07 · 方案取舍](./07-方案取舍与后续设计.md) | 深度、BVH、GPU 可见性、ID 缓冲 | 决定下一版方案的人 |
| [08 · 代码导读](./08-代码导读与安全修改点.md) | 沿调用链阅读和安全修改 | 准备改代码的人 |
| [09 · 坐标与深度数学](./09-坐标空间与深度数学专题.md) | 投影、深度、误差与像素映射 | 排查数值边界的人 |
| [10 · C++ 生命周期](./10-C++类型生命周期与并行上下文.md) | 类型、所有权、容器与并行约束 | 审查实现的人 |
| [11 · 数值例题](./11-实例化推演与数值例题.md) | 用具体数值推演实例和射线 | 验证几何计算的人 |
| [12 · 术语表](./12-术语表与常见误解.md) | 关键名词及容易混淆的结论 | 需要快速查阅的人 |
| [13 · 审查问答](./13-代码审查问答.md) | 按审查问题串起设计与风险 | 准备评审的人 |

### 最短阅读路线

先读 01，建立总图。
遇到旋转时漏字，跳到 04，再按 06 复现。
要改实例域，先读 03 和 08。
准备提交前读 05 的约束与 06 的验证清单。

### 按具体问题查找

| 遇到的问题 | 先看 | 接着核对 |
|---|---|---|
| 实例文本被实例自身遮住 | 03 的 AABB 锚点 | 11 的射线例题、07 的局限 |
| 网格点编号随旋转消失 | 04 的症状记录 | 09 的投影与误差、06 的复现矩阵 |
| 远近缩放后显示异常 | 02 的缓存刷新 | 09 的深度范围与比较方向 |
| 想调整文字缓存结构 | 05 的 API | 10 的所有权与生命周期 |
| 想判断该用 BVH 还是深度 | 07 的取舍 | 04 的已观察问题 |
| 审查新提交 | 08 的调用链 | 13 的问题清单 |

阅读时先确认结论属于“当前代码”“实验观察”还是“下一版建议”。
尤其要把已贮藏的斜率和像素邻域实验，与已提交的固定容差实现区分开。
若本地分支增加提交，先更新上方的提交快照，再重新核对函数签名与调用顺序。

## 一句话理解实现

Geometry Nodes Viewer 的 `.viewer` 值被写入本帧文字缓存。
Overlay 在深度 prepass 后、grid/axes 写深度前回读视口深度。
绘制文字时，将每个锚点投影到屏幕，比较对应像素的场景深度。
点云和实例通过各自的锚点前移减少自身遮挡。

```text
Viewer 值
  → 属性域位置 / 特殊锚点
  → ViewCachedString
  → GPU depth 回读
  → 锚点深度比较
  → BLF 绘制或跳过
```

## 与参考文档的重要勘误

1. 当前视口源码请求 `SFLOAT_32_DEPTH_UINT_8`，不能断言是 D24 定点。
2. 实例代码变量名 `entry_distance` 实际接收 AABB 的 `tmax` 出口参数。
3. 透视时 `entry_distance < 1` 的 `1` 对应相机位置参数，不是“1 米”。
4. `ViewDepths` 对象可以复用，但其深度像素每帧都必须刷新。
5. 斜率与邻域实验已贮藏，当前提交仍为固定 `2e-5` 单像素比较。
6. `draw_manager_text.cc` 与 `overlay_instance.hh` 的个别注释仍描述旧回读时机，以实际调用链为准。
7. 两次投影是已确认结构；“必然偏移 1 像素”不是已确认事实。

这些更正不是对所有 GPU 后端行为的断言。
具体运行时仍需逐帧数据和视口复测。

## 当前实现的文件表

| 层 | 文件 |
|---|---|
| UI | `scripts/startup/bl_ui/space_view3d.py` |
| 持久数据 | `source/blender/makesdna/DNA_view3d_types.h` |
| RNA | `source/blender/makesrna/intern/rna_space.cc` |
| State | `source/blender/draw/engines/overlay/overlay_private.hh` |
| 属性锚点 | `source/blender/draw/engines/overlay/overlay_attribute_text.hh` |
| 深度生命周期 | `source/blender/draw/engines/overlay/overlay_instance.hh`、`.cc` |
| 通用文字 | `source/blender/draw/intern/draw_manager_text.hh`、`.cc` |

## 文档可信度约定

**已确认源码事实**：可以在本快照对应文件中直接找到。
**已观察现象**：来自用户实际截图或构建日志，但不必然指向唯一根因。
**推断**：有数学或执行路径支持，仍需复现实验。
**备选方案**：尚未实现，不应描述为当前分支行为。

阅读表格里的“待填”时，请把它理解为尚未做现场验证。
这比写一个没有证据的“已通过”更有用。

## 修改文档时的检查

1. 先记录当前 `git rev-parse HEAD`。
2. 运行 `git diff origin/main...HEAD --stat` 核对范围。
3. 逐一核对文中的函数名、参数方向和数据所有权。
4. 对数学公式说明坐标空间和单位。
5. 把用户截图观察与根因推断分开写。
6. 新实验若被撤回，更新“当前行为”而不是继续称其为修复。
7. 修改代码后同步更新验证矩阵与已知局限。

## 下一步推荐

对一个稳定复现的点 ID 记录显示帧和消失帧的投影与深度。
先确定它在哪一层失败，再设计下一版算法。
这样可以避免反复调一个全局容差，却在新的视角制造相反问题。
