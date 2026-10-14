# 实现依赖专题：source/blender/nodes/texture/node_texture_util.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::tex_call_delegate"]:::abstraction
  F1["blender::tex_input"]:::compute
  F2["blender::tex_input_rgba"]:::compute
  F3["blender::params_from_cdata"]:::compute
  F4["blender::tex_output"]:::compute
  F5["blender::ntreeTexCheckCyclics"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F1
  F5 -->|"显式调用"| F5
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
  F["node_texture_util.cc实现"]:::compute
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

<a id="f-e2d62969c04f63f1"></a>

### `blender::tex_call_delegate`

实现位置：[source/blender/nodes/texture/node_texture_util.cc](../../../../../source/blender/nodes/texture/node_texture_util.cc) · L58—L63。

接口参数：

- `TexDelegate *dg`
- `float *out`
- `TexParams *params`
- `short thread`

**教学注释版**

<!-- annotated:5a3bbf9c546579 -->

```cpp
static void tex_call_delegate(TexDelegate *dg, float *out, TexParams *params, short thread)
{
  if (dg->node->runtime->need_exec) {
    dg->fn(out, params, dg->node, dg->in, thread);
  }
}
```

<details>
<summary>核对原始源码：source/blender/nodes/texture/node_texture_util.cc · L58—L63</summary>

<!-- original:5a3bbf9c546579:source/blender/nodes/texture/node_texture_util.cc:58:63 -->

```cpp
static void tex_call_delegate(TexDelegate *dg, float *out, TexParams *params, short thread)
{
  if (dg->node->runtime->need_exec) {
    dg->fn(out, params, dg->node, dg->in, thread);
  }
}
```

</details>

**继续追踪实现**

- `dg->fn` → [blender::fn::multi_function::CallInstruction::fn · L390](../07-MultiFunction%E4%B8%8E%E6%89%B9%E9%87%8F%E6%89%A7%E8%A1%8C/07-Procedure%E6%8C%87%E4%BB%A4%E4%B8%8E%E6%8E%A7%E5%88%B6%E6%B5%81.md#f-572ebb7362882f77)。

<a id="f-e66b4b8bc84e7766"></a>

### `blender::tex_input`

实现位置：[source/blender/nodes/texture/node_texture_util.cc](../../../../../source/blender/nodes/texture/node_texture_util.cc) · L65—L76。

接口参数：

- `float *out`
- `int num`
- `bNodeStack *in`
- `TexParams *params`
- `short thread`

**教学注释版**

<!-- annotated:1bf2253c8efa62 -->

```cpp
static void tex_input(float *out, int num, bNodeStack *in, TexParams *params, short thread)
{
  TexDelegate *dg = static_cast<TexDelegate *>(in->data);
  if (dg) {
    tex_call_delegate(dg, in->vec, params, thread);

    if (in->hasoutput && in->sockettype == SOCK_FLOAT) {
      in->vec[1] = in->vec[2] = in->vec[0];
    }
  }
  // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
  memcpy(out, in->vec, num * sizeof(float));
}
```

<details>
<summary>核对原始源码：source/blender/nodes/texture/node_texture_util.cc · L65—L76</summary>

<!-- original:1bf2253c8efa62:source/blender/nodes/texture/node_texture_util.cc:65:76 -->

```cpp
static void tex_input(float *out, int num, bNodeStack *in, TexParams *params, short thread)
{
  TexDelegate *dg = static_cast<TexDelegate *>(in->data);
  if (dg) {
    tex_call_delegate(dg, in->vec, params, thread);

    if (in->hasoutput && in->sockettype == SOCK_FLOAT) {
      in->vec[1] = in->vec[2] = in->vec[0];
    }
  }
  memcpy(out, in->vec, num * sizeof(float));
}
```

</details>

**沿实际写入检查状态**

- `in->vec[1] = in->vec[2] = in->vec[0];`

**继续追踪实现**

- `tex_call_delegate` → [blender::tex_call_delegate · L58](%E4%BE%9D%E8%B5%96-node_texture_util-0d1f2f.md#f-e2d62969c04f63f1)。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。

<a id="f-eb06e809e2a307a4"></a>

### `blender::tex_input_rgba`

实现位置：[source/blender/nodes/texture/node_texture_util.cc](../../../../../source/blender/nodes/texture/node_texture_util.cc) · L83—L98。

接口参数：

- `float *out`
- `bNodeStack *in`
- `TexParams *params`
- `short thread`

**教学注释版**

<!-- annotated:bdea26395646fd -->

```cpp
void tex_input_rgba(float *out, bNodeStack *in, TexParams *params, short thread)
{
  tex_input(out, 4, in, params, thread);

  if (in->hasoutput && in->sockettype == SOCK_FLOAT) {
    out[1] = out[2] = out[0];
    out[3] = 1;
  }

  if (in->hasoutput && in->sockettype == SOCK_VECTOR) {
    out[0] = out[0] * 0.5f + 0.5f;
    out[1] = out[1] * 0.5f + 0.5f;
    out[2] = out[2] * 0.5f + 0.5f;
    out[3] = 1;
  }
}
```

<details>
<summary>核对原始源码：source/blender/nodes/texture/node_texture_util.cc · L83—L98</summary>

<!-- original:bdea26395646fd:source/blender/nodes/texture/node_texture_util.cc:83:98 -->

```cpp
void tex_input_rgba(float *out, bNodeStack *in, TexParams *params, short thread)
{
  tex_input(out, 4, in, params, thread);

  if (in->hasoutput && in->sockettype == SOCK_FLOAT) {
    out[1] = out[2] = out[0];
    out[3] = 1;
  }

  if (in->hasoutput && in->sockettype == SOCK_VECTOR) {
    out[0] = out[0] * 0.5f + 0.5f;
    out[1] = out[1] * 0.5f + 0.5f;
    out[2] = out[2] * 0.5f + 0.5f;
    out[3] = 1;
  }
}
```

</details>

**沿实际写入检查状态**

- `out[1] = out[2] = out[0];`
- `out[3] = 1;`
- `out[0] = out[0] * 0.5f + 0.5f;`
- `out[1] = out[1] * 0.5f + 0.5f;`
- `out[2] = out[2] * 0.5f + 0.5f;`

**继续追踪实现**

- `tex_input` → [blender::tex_input · L65](%E4%BE%9D%E8%B5%96-node_texture_util-0d1f2f.md#f-e66b4b8bc84e7766)。

<a id="f-a3f2bcab6a2c00cd"></a>

### `blender::params_from_cdata`

实现位置：[source/blender/nodes/texture/node_texture_util.cc](../../../../../source/blender/nodes/texture/node_texture_util.cc) · L107—L113。

接口参数：

- `TexParams *out`
- `TexCallData *in`

**教学注释版**

<!-- annotated:6604522e896dbe -->

```cpp
void params_from_cdata(TexParams *out, TexCallData *in)
{
  out->co = in->co;
  out->previewco = in->co;
  out->cfra = in->cfra;
  out->mtex = in->mtex;
}
```

<details>
<summary>核对原始源码：source/blender/nodes/texture/node_texture_util.cc · L107—L113</summary>

<!-- original:6604522e896dbe:source/blender/nodes/texture/node_texture_util.cc:107:113 -->

```cpp
void params_from_cdata(TexParams *out, TexCallData *in)
{
  out->co = in->co;
  out->previewco = in->co;
  out->cfra = in->cfra;
  out->mtex = in->mtex;
}
```

</details>

**沿实际写入检查状态**

- `out->co = in->co;`
- `out->previewco = in->co;`
- `out->cfra = in->cfra;`
- `out->mtex = in->mtex;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-0b6a7176dbf05859"></a>

### `blender::tex_output`

实现位置：[source/blender/nodes/texture/node_texture_util.cc](../../../../../source/blender/nodes/texture/node_texture_util.cc) · L115—L143。

接口参数：

- `bNode *node`
- `bNodeExecData *`
- `bNodeStack **in`
- `bNodeStack *out`
- `TexFn texfn`
- `TexCallData *cdata`

**教学注释版**

<!-- annotated:e968f008468504 -->

```cpp
void tex_output(bNode *node,
                bNodeExecData * /*execdata*/,
                bNodeStack **in,
                bNodeStack *out,
                TexFn texfn,
                TexCallData *cdata)
{
  TexDelegate *dg;

  if (node->is_muted()) {
    /* do not add a delegate if the node is muted */
    return;
  }

  if (!out->data) {
    /* Freed in tex_end_exec (node.cc) */
    dg = MEM_new_zeroed<TexDelegate>("tex delegate");
    out->data = dg;
  }
  else {
    dg = static_cast<TexDelegate *>(out->data);
  }

  dg->cdata = cdata;
  dg->fn = texfn;
  dg->node = node;
  // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
  memcpy(dg->in, in, MAX_SOCKET * sizeof(bNodeStack *));
  dg->type = out->sockettype;
}
```

<details>
<summary>核对原始源码：source/blender/nodes/texture/node_texture_util.cc · L115—L143</summary>

<!-- original:e968f008468504:source/blender/nodes/texture/node_texture_util.cc:115:143 -->

```cpp
void tex_output(bNode *node,
                bNodeExecData * /*execdata*/,
                bNodeStack **in,
                bNodeStack *out,
                TexFn texfn,
                TexCallData *cdata)
{
  TexDelegate *dg;

  if (node->is_muted()) {
    /* do not add a delegate if the node is muted */
    return;
  }

  if (!out->data) {
    /* Freed in tex_end_exec (node.cc) */
    dg = MEM_new_zeroed<TexDelegate>("tex delegate");
    out->data = dg;
  }
  else {
    dg = static_cast<TexDelegate *>(out->data);
  }

  dg->cdata = cdata;
  dg->fn = texfn;
  dg->node = node;
  memcpy(dg->in, in, MAX_SOCKET * sizeof(bNodeStack *));
  dg->type = out->sockettype;
}
```

</details>

**沿实际写入检查状态**

- `dg = MEM_new_zeroed<TexDelegate>("tex delegate");`
- `out->data = dg;`
- `dg = static_cast<TexDelegate *>(out->data);`
- `dg->cdata = cdata;`
- `dg->fn = texfn;`
- `dg->node = node;`
- `dg->type = out->sockettype;`

**继续追踪实现**

- `node->is_muted` → [blender::bNode::is_muted · L886](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-BKE_node_runtime-ee561b.md#f-4d91efc4cc87d00d)。
- `MEM_new_zeroed<TexDelegate>` → [MEM_new_zeroed · L550](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-eeb1e2a7f57dd231)；[MEM_new_zeroed · L114](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-mallocn-afdcd4.md#f-e04cf01c64c8b180)。同名重载需按实参类型选择。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。

<a id="f-5aa70f1aeeb5c482"></a>

### `blender::ntreeTexCheckCyclics`

实现位置：[source/blender/nodes/texture/node_texture_util.cc](../../../../../source/blender/nodes/texture/node_texture_util.cc) · L145—L168。

接口参数：

- `bNodeTree *ntree`

**教学注释版**

<!-- annotated:adf7713ecab39b -->

```cpp
void ntreeTexCheckCyclics(bNodeTree *ntree)
{
  for (bNode &node : ntree->nodes) {

    if (node.type_legacy == TEX_NODE_TEXTURE && node.id) {
      /* custom2 stops the node from rendering */
      if (node.custom1) {
        node.custom2 = 1;
        node.custom1 = 0;
      }
      else {
        Tex *tex = id_cast<Tex *>(node.id);

        node.custom2 = 0;

        node.custom1 = 1;
        if (tex->use_nodes && tex->nodetree) {
          ntreeTexCheckCyclics(tex->nodetree);
        }
        node.custom1 = 0;
      }
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/nodes/texture/node_texture_util.cc · L145—L168</summary>

<!-- original:adf7713ecab39b:source/blender/nodes/texture/node_texture_util.cc:145:168 -->

```cpp
void ntreeTexCheckCyclics(bNodeTree *ntree)
{
  for (bNode &node : ntree->nodes) {

    if (node.type_legacy == TEX_NODE_TEXTURE && node.id) {
      /* custom2 stops the node from rendering */
      if (node.custom1) {
        node.custom2 = 1;
        node.custom1 = 0;
      }
      else {
        Tex *tex = id_cast<Tex *>(node.id);

        node.custom2 = 0;

        node.custom1 = 1;
        if (tex->use_nodes && tex->nodetree) {
          ntreeTexCheckCyclics(tex->nodetree);
        }
        node.custom1 = 0;
      }
    }
  }
}
```

</details>

**沿实际写入检查状态**

- `node.custom2 = 1;`
- `node.custom1 = 0;`
- `node.custom2 = 0;`
- `node.custom1 = 1;`

**继续追踪实现**

- `id_cast<Tex *>` → [blender::id_cast · L1417](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-DNA_ID-3eb091.md#f-6c8ac6412850ac5a)。
- `ntreeTexCheckCyclics` → [blender::ntreeTexCheckCyclics · L145](%E4%BE%9D%E8%B5%96-node_texture_util-0d1f2f.md#f-5aa70f1aeeb5c482)。
