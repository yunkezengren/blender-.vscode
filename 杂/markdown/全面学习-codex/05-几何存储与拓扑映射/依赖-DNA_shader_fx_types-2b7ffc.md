# 实现依赖专题：source/blender/makesdna/DNA_shader_fx_types.h

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["DNA_shader_fx_types.h"]:::abstraction
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
  F["DNA_shader_fx_types.h实现"]:::compute
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

<a id="t-ac85e8b68fec"></a>

### `blender::ShaderFxType`

原始声明：[source/blender/makesdna/DNA_shader_fx_types.h](../../../../../source/blender/makesdna/DNA_shader_fx_types.h) · L90—L104。

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:df1c7126e64d3d -->

```cpp
enum ShaderFxType : int {
  eShaderFxType_None = 0,
  eShaderFxType_Blur = 1,
  eShaderFxType_Flip = 2,
  eShaderFxType_Light_deprecated = 3, /* DEPRECATED (replaced by scene lights) */
  eShaderFxType_Pixel = 4,
  eShaderFxType_Swirl = 5,
  eShaderFxType_Wave = 6,
  eShaderFxType_Rim = 7,
  eShaderFxType_Colorize = 8,
  eShaderFxType_Shadow = 9,
  eShaderFxType_Glow = 10,
  /* Keep last. */
  NUM_SHADER_FX_TYPES,
};
```

<details>
<summary>核对原始源码：source/blender/makesdna/DNA_shader_fx_types.h · L90—L104</summary>

<!-- original:df1c7126e64d3d:source/blender/makesdna/DNA_shader_fx_types.h:90:104 -->

```cpp
enum ShaderFxType : int {
  eShaderFxType_None = 0,
  eShaderFxType_Blur = 1,
  eShaderFxType_Flip = 2,
  eShaderFxType_Light_deprecated = 3, /* DEPRECATED (replaced by scene lights) */
  eShaderFxType_Pixel = 4,
  eShaderFxType_Swirl = 5,
  eShaderFxType_Wave = 6,
  eShaderFxType_Rim = 7,
  eShaderFxType_Colorize = 8,
  eShaderFxType_Shadow = 9,
  eShaderFxType_Glow = 10,
  /* Keep last. */
  NUM_SHADER_FX_TYPES,
};
```

</details>


## 完整成员与函数实现
