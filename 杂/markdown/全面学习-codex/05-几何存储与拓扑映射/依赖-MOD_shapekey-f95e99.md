# 实现依赖专题：source/blender/modifiers/intern/MOD_shapekey.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::deform_verts"]:::abstraction
  F1["blender::deform_matrices"]:::compute
  F2["blender::deform_verts_EM"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F0
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
  F["MOD_shapekey.cc实现"]:::compute
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

<a id="f-28f15a07a028259a"></a>

### `blender::deform_verts`

实现位置：[source/blender/modifiers/intern/MOD_shapekey.cc](../../../../../source/blender/modifiers/intern/MOD_shapekey.cc) · L26—L42。

接口参数：

- `ModifierData *`
- `const ModifierEvalContext *ctx`
- `Mesh *`
- `MutableSpan<float3> positions`

**教学注释版**

<!-- annotated:f6e8428f91fe64 -->

```cpp
static void deform_verts(ModifierData * /*md*/,
                         const ModifierEvalContext *ctx,
                         Mesh * /*mesh*/,
                         MutableSpan<float3> positions)
{
  Key *key = BKE_key_from_object(ctx->object);

  if (key && key->block.first_) {
    int deformedVerts_tot;
    BKE_key_evaluate_object_ex(ctx->object,
                               &deformedVerts_tot,
                               // [讲解] positions.data：返回借用范围的地址。
                               reinterpret_cast<float *>(positions.data()),
                               // [讲解] positions.size：查询视图长度或生成对应有效索引区间。
                               sizeof(float3) * positions.size(),
                               std::nullopt,
                               nullptr);
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_shapekey.cc · L26—L42</summary>

<!-- original:f6e8428f91fe64:source/blender/modifiers/intern/MOD_shapekey.cc:26:42 -->

```cpp
static void deform_verts(ModifierData * /*md*/,
                         const ModifierEvalContext *ctx,
                         Mesh * /*mesh*/,
                         MutableSpan<float3> positions)
{
  Key *key = BKE_key_from_object(ctx->object);

  if (key && key->block.first_) {
    int deformedVerts_tot;
    BKE_key_evaluate_object_ex(ctx->object,
                               &deformedVerts_tot,
                               reinterpret_cast<float *>(positions.data()),
                               sizeof(float3) * positions.size(),
                               std::nullopt,
                               nullptr);
  }
}
```

</details>

**继续追踪实现**

- `BKE_key_from_object` → [blender::BKE_key_from_object · L1311](%E4%BE%9D%E8%B5%96-key-2b3be3.md#f-c191304ae3a652d6)。
- `BKE_key_evaluate_object_ex` → [blender::BKE_key_evaluate_object_ex · L1009](%E4%BE%9D%E8%B5%96-key-2b3be3.md#f-2ee933fd9371726a)。
- `positions.data` → [blender::MutableSpan::data · L545](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-eb45a6e4d8211efd)；[blender::gpu::shader::parser::MutableSpan::data · L82](%E4%BE%9D%E8%B5%96-utils-06433d.md#f-ad0a09cec9741c65)。同名重载需按实参类型选择。
- `positions.size` → [blender::MutableSpan::size · L499](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-1de6a66839c304a8)；[blender::gpu::shader::parser::MutableSpan::size · L87](%E4%BE%9D%E8%B5%96-utils-06433d.md#f-5e684af6ee7990e9)。同名重载需按实参类型选择。

<a id="f-505b228175c965f9"></a>

### `blender::deform_matrices`

实现位置：[source/blender/modifiers/intern/MOD_shapekey.cc](../../../../../source/blender/modifiers/intern/MOD_shapekey.cc) · L44—L70。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `Mesh *mesh`
- `MutableSpan<float3> positions`
- `MutableSpan<float3x3> matrices`

**教学注释版**

<!-- annotated:be50a59f023067 -->

```cpp
static void deform_matrices(ModifierData *md,
                            const ModifierEvalContext *ctx,
                            Mesh *mesh,
                            MutableSpan<float3> positions,
                            MutableSpan<float3x3> matrices)
{
  Key *key = BKE_key_from_object(ctx->object);
  KeyBlock *kb = BKE_keyblock_from_object(ctx->object);

  // [讲解] positions.size：查询视图长度或生成对应有效索引区间。
  if (kb && kb->totelem == positions.size() && kb != key->refkey) {
    float scale[3][3];
    int a;

    if (ctx->object->shapeflag & OB_SHAPE_LOCK) {
      scale_m3_fl(scale, 1);
    }
    else {
      scale_m3_fl(scale, kb->curval);
    }

    for (a = 0; a < positions.size(); a++) {
      copy_m3_m3(matrices[a].ptr(), scale);
    }
  }

  deform_verts(md, ctx, mesh, positions);
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_shapekey.cc · L44—L70</summary>

<!-- original:be50a59f023067:source/blender/modifiers/intern/MOD_shapekey.cc:44:70 -->

```cpp
static void deform_matrices(ModifierData *md,
                            const ModifierEvalContext *ctx,
                            Mesh *mesh,
                            MutableSpan<float3> positions,
                            MutableSpan<float3x3> matrices)
{
  Key *key = BKE_key_from_object(ctx->object);
  KeyBlock *kb = BKE_keyblock_from_object(ctx->object);

  if (kb && kb->totelem == positions.size() && kb != key->refkey) {
    float scale[3][3];
    int a;

    if (ctx->object->shapeflag & OB_SHAPE_LOCK) {
      scale_m3_fl(scale, 1);
    }
    else {
      scale_m3_fl(scale, kb->curval);
    }

    for (a = 0; a < positions.size(); a++) {
      copy_m3_m3(matrices[a].ptr(), scale);
    }
  }

  deform_verts(md, ctx, mesh, positions);
}
```

</details>

**继续追踪实现**

- `BKE_key_from_object` → [blender::BKE_key_from_object · L1311](%E4%BE%9D%E8%B5%96-key-2b3be3.md#f-c191304ae3a652d6)。
- `BKE_keyblock_from_object` → [blender::BKE_keyblock_from_object · L1407](%E4%BE%9D%E8%B5%96-key-2b3be3.md#f-0b20126f099723f9)。
- `positions.size` → [blender::MutableSpan::size · L499](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/06-MutableSpan%E5%8F%AF%E5%86%99%E8%A7%86%E5%9B%BE.md#f-1de6a66839c304a8)；[blender::gpu::shader::parser::MutableSpan::size · L87](%E4%BE%9D%E8%B5%96-utils-06433d.md#f-5e684af6ee7990e9)。同名重载需按实参类型选择。
- `scale_m3_fl` → [blender::scale_m3_fl · L2090](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_matrix_c-004123.md#f-765dcf3106554985)。
- `copy_m3_m3` → [blender::copy_m3_m3 · L78](../12-%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E5%87%A0%E4%BD%95%E7%AE%97%E6%B3%95/%E4%BE%9D%E8%B5%96-math_matrix_c-004123.md#f-c73aa9bdf12f5c76)。
- `matrices[a].ptr` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L65。
- `deform_verts` → [blender::deform_verts · L26](%E4%BE%9D%E8%B5%96-MOD_shapekey-f95e99.md#f-28f15a07a028259a)。

<a id="f-84ba6503394dc262"></a>

### `blender::deform_verts_EM`

实现位置：[source/blender/modifiers/intern/MOD_shapekey.cc](../../../../../source/blender/modifiers/intern/MOD_shapekey.cc) · L72—L83。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `const BMEditMesh *`
- `Mesh *mesh`
- `MutableSpan<float3> positions`

**教学注释版**

<!-- annotated:aa3a320b810f34 -->

```cpp
static void deform_verts_EM(ModifierData *md,
                            const ModifierEvalContext *ctx,
                            const BMEditMesh * /*em*/,
                            Mesh *mesh,
                            MutableSpan<float3> positions)
{
  Key *key = BKE_key_from_object(ctx->object);

  if (key && key->type == KEY_RELATIVE) {
    deform_verts(md, ctx, mesh, positions);
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_shapekey.cc · L72—L83</summary>

<!-- original:aa3a320b810f34:source/blender/modifiers/intern/MOD_shapekey.cc:72:83 -->

```cpp
static void deform_verts_EM(ModifierData *md,
                            const ModifierEvalContext *ctx,
                            const BMEditMesh * /*em*/,
                            Mesh *mesh,
                            MutableSpan<float3> positions)
{
  Key *key = BKE_key_from_object(ctx->object);

  if (key && key->type == KEY_RELATIVE) {
    deform_verts(md, ctx, mesh, positions);
  }
}
```

</details>

**继续追踪实现**

- `BKE_key_from_object` → [blender::BKE_key_from_object · L1311](%E4%BE%9D%E8%B5%96-key-2b3be3.md#f-c191304ae3a652d6)。
- `deform_verts` → [blender::deform_verts · L26](%E4%BE%9D%E8%B5%96-MOD_shapekey-f95e99.md#f-28f15a07a028259a)。
