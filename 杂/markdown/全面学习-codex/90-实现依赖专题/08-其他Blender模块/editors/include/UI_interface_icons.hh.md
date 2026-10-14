# 实现依赖专题：source/blender/editors/include/UI_interface_icons.hh

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["UI_interface_icons.hh"]:::abstraction
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
  F["UI_interface_icons.hh实现"]:::compute
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

## 相关类型布局与成员入口

<a id="t-1390cb9fb413"></a>

### `blender::ui::eIconSizes`

原始声明：[source/blender/editors/include/UI_interface_icons.hh](../../../../../../../../source/blender/editors/include/UI_interface_icons.hh) · L71—L71。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:9241c90e438a24 -->

```cpp
void icon_render_id(const bContext *C, Scene *scene, ID *id, enum eIconSizes size, bool use_job);
```

<details>
<summary>核对原始源码：source/blender/editors/include/UI_interface_icons.hh · L71—L71</summary>

<!-- original:9241c90e438a24:source/blender/editors/include/UI_interface_icons.hh:71:71 -->

```cpp
void icon_render_id(const bContext *C, Scene *scene, ID *id, enum eIconSizes size, bool use_job);
```

</details>


<a id="t-61aa9949b7e7"></a>

### `blender::ui::eIconSizes`

原始声明：[source/blender/editors/include/UI_interface_icons.hh](../../../../../../../../source/blender/editors/include/UI_interface_icons.hh) · L79—L79。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:7455af874ad7eb -->

```cpp
                       const enum eIconSizes size,
```

<details>
<summary>核对原始源码：source/blender/editors/include/UI_interface_icons.hh · L79—L79</summary>

<!-- original:7455af874ad7eb:source/blender/editors/include/UI_interface_icons.hh:79:79 -->

```cpp
                       const enum eIconSizes size,
```

</details>


<a id="t-d0e32d23ee45"></a>

### `blender::ui::eIconSizes`

原始声明：[source/blender/editors/include/UI_interface_icons.hh](../../../../../../../../source/blender/editors/include/UI_interface_icons.hh) · L86—L86。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:30d453cf223e8d -->

```cpp
int icon_preview_to_render_size(enum eIconSizes size);
```

<details>
<summary>核对原始源码：source/blender/editors/include/UI_interface_icons.hh · L86—L86</summary>

<!-- original:30d453cf223e8d:source/blender/editors/include/UI_interface_icons.hh:86:86 -->

```cpp
int icon_preview_to_render_size(enum eIconSizes size);
```

</details>


## 完整成员与函数实现
