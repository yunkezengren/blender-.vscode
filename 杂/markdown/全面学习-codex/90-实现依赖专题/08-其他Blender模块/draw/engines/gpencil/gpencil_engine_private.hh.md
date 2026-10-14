# 实现依赖专题：source/blender/draw/engines/gpencil/gpencil_engine_private.hh

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["gpencil_engine_private.hh"]:::abstraction
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
  F["gpencil_engine_private.hh实现"]:::compute
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

<a id="m-2f50f8faa811"></a>

## 宏 `GPENCIL_SIMPLIFY_FILL`

<!-- annotated:4b6ebb53ef30f4 -->

```cpp
#define GPENCIL_SIMPLIFY_FILL(scene, playing) \
  ((GPENCIL_SIMPLIFY_ONPLAY(playing) && GPENCIL_SIMPLIFY(scene) && \
    (scene->r.simplify_gpencil & SIMPLIFY_GPENCIL_FILL)))
#define GPENCIL_SIMPLIFY_FX(scene, playing) \
```

<details>
<summary>核对原始源码：source/blender/draw/engines/gpencil/gpencil_engine_private.hh · L51—L54</summary>

<!-- original:4b6ebb53ef30f4:source/blender/draw/engines/gpencil/gpencil_engine_private.hh:51:54 -->

```cpp
#define GPENCIL_SIMPLIFY_FILL(scene, playing) \
  ((GPENCIL_SIMPLIFY_ONPLAY(playing) && GPENCIL_SIMPLIFY(scene) && \
    (scene->r.simplify_gpencil & SIMPLIFY_GPENCIL_FILL)))
#define GPENCIL_SIMPLIFY_FX(scene, playing) \
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-6c0eeba994f2"></a>

## 宏 `GPENCIL_SIMPLIFY_FX`

<!-- annotated:3545d06c240c26 -->

```cpp
#define GPENCIL_SIMPLIFY_FX(scene, playing) \
  ((GPENCIL_SIMPLIFY_ONPLAY(playing) && GPENCIL_SIMPLIFY(scene) && \
    (scene->r.simplify_gpencil & SIMPLIFY_GPENCIL_FX)))
#define GPENCIL_SIMPLIFY_TINT(scene) \
```

<details>
<summary>核对原始源码：source/blender/draw/engines/gpencil/gpencil_engine_private.hh · L54—L57</summary>

<!-- original:3545d06c240c26:source/blender/draw/engines/gpencil/gpencil_engine_private.hh:54:57 -->

```cpp
#define GPENCIL_SIMPLIFY_FX(scene, playing) \
  ((GPENCIL_SIMPLIFY_ONPLAY(playing) && GPENCIL_SIMPLIFY(scene) && \
    (scene->r.simplify_gpencil & SIMPLIFY_GPENCIL_FX)))
#define GPENCIL_SIMPLIFY_TINT(scene) \
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-fea076f8f12c"></a>

## 宏 `GPENCIL_SIMPLIFY_TINT`

<!-- annotated:c92c0771d0883a -->

```cpp
#define GPENCIL_SIMPLIFY_TINT(scene) \
  (GPENCIL_SIMPLIFY(scene) && (scene->r.simplify_gpencil & SIMPLIFY_GPENCIL_TINT))
#define GPENCIL_SIMPLIFY_AA(scene) \
```

<details>
<summary>核对原始源码：source/blender/draw/engines/gpencil/gpencil_engine_private.hh · L57—L59</summary>

<!-- original:c92c0771d0883a:source/blender/draw/engines/gpencil/gpencil_engine_private.hh:57:59 -->

```cpp
#define GPENCIL_SIMPLIFY_TINT(scene) \
  (GPENCIL_SIMPLIFY(scene) && (scene->r.simplify_gpencil & SIMPLIFY_GPENCIL_TINT))
#define GPENCIL_SIMPLIFY_AA(scene) \
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-b582329ba5a3"></a>

## 宏 `GPENCIL_SIMPLIFY_AA`

<!-- annotated:a327028b97cd54 -->

```cpp
#define GPENCIL_SIMPLIFY_AA(scene) \
  (GPENCIL_SIMPLIFY(scene) && (scene->r.simplify_gpencil & SIMPLIFY_GPENCIL_AA))

```

<details>
<summary>核对原始源码：source/blender/draw/engines/gpencil/gpencil_engine_private.hh · L59—L61</summary>

<!-- original:a327028b97cd54:source/blender/draw/engines/gpencil/gpencil_engine_private.hh:59:61 -->

```cpp
#define GPENCIL_SIMPLIFY_AA(scene) \
  (GPENCIL_SIMPLIFY(scene) && (scene->r.simplify_gpencil & SIMPLIFY_GPENCIL_AA))

```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
