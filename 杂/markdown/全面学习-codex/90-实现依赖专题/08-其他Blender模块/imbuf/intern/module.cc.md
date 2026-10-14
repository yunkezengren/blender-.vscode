# 实现依赖专题：source/blender/imbuf/intern/module.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::IMB_activate_gpu_context"]:::abstraction
  F1["blender::IMB_deactivate_gpu_context"]:::compute
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  C["调用者提供参数与有效对象"]:::input
  F["module.cc实现"]:::compute
  R["结果与被修改状态"]:::result
  C -->|"进入"| F
  F -->|"返回或提交"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  T["具体类型与模板实参"]:::abstraction
  B["分支与构建条件"]:::data
  I["匹配的实现"]:::compute
  E["标准库或系统契约边界"]:::result
  T -->|"静态选择"| I
  B -->|"配置选择"| I
  I -->|"到达外部接口"| E
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  S["完整源码单元"]:::input
  A["教学注释与推导"]:::abstraction
  D["被调用实现专题"]:::compute
  V["原文与token一致性检查"]:::result
  S -->|"就近阅读"| A
  A -->|"继续深入"| D
  A -->|"核对"| V
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

## 完整成员与函数实现

<a id="f-fc08077469a8d55a"></a>

### `blender::IMB_activate_gpu_context`

实现位置：[source/blender/imbuf/intern/module.cc](../../../../../../../../source/blender/imbuf/intern/module.cc) · L53—L59。

**教学注释版**

<!-- annotated:c5c35836d32aa7 -->

```cpp
void IMB_activate_gpu_context()
{
  BLI_assert(g_gpu_context.gpu_context);

  g_gpu_context_mutex.lock();
  gpu::GPU_activate_secondary_context(g_gpu_context);
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/intern/module.cc · L53—L59</summary>

<!-- original:c5c35836d32aa7:source/blender/imbuf/intern/module.cc:53:59 -->

```cpp
void IMB_activate_gpu_context()
{
  BLI_assert(g_gpu_context.gpu_context);

  g_gpu_context_mutex.lock();
  gpu::GPU_activate_secondary_context(g_gpu_context);
}
```

</details>

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `g_gpu_context_mutex.lock` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L57。
- `gpu::GPU_activate_secondary_context` → [blender::gpu::GPU_activate_secondary_context · L725](../../gpu/intern/gpu_context.cc.md#f-0ecb32b1429d3b5c)。

<a id="f-b81ab806194c6a8a"></a>

### `blender::IMB_deactivate_gpu_context`

实现位置：[source/blender/imbuf/intern/module.cc](../../../../../../../../source/blender/imbuf/intern/module.cc) · L61—L67。

**教学注释版**

<!-- annotated:8ec0641a01ebed -->

```cpp
void IMB_deactivate_gpu_context()
{
  BLI_assert(g_gpu_context.gpu_context);

  gpu::GPU_deactivate_secondary_context(g_gpu_context);
  g_gpu_context_mutex.unlock();
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/intern/module.cc · L61—L67</summary>

<!-- original:8ec0641a01ebed:source/blender/imbuf/intern/module.cc:61:67 -->

```cpp
void IMB_deactivate_gpu_context()
{
  BLI_assert(g_gpu_context.gpu_context);

  gpu::GPU_deactivate_secondary_context(g_gpu_context);
  g_gpu_context_mutex.unlock();
}
```

</details>

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `gpu::GPU_deactivate_secondary_context` → [blender::gpu::GPU_deactivate_secondary_context · L731](../../gpu/intern/gpu_context.cc.md#f-2e947eed0260f1b8)。
- `g_gpu_context_mutex.unlock` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L66。
