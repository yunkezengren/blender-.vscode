# 实现依赖专题：source/blender/nodes/shader/node_shader_tree.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["ntreeShaderOutputNode"]:::abstraction
  F1["ntreeShaderEndExecTree_internal"]:::compute
  F2["ntreeShaderEndExecTree"]:::compute
  F2 -->|"显式调用"| F1
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
  F["node_shader_tree.cc实现"]:::compute
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

<a id="f-b8a16259d59b1716"></a>

### `ntreeShaderOutputNode`

实现位置：[source/blender/nodes/shader/node_shader_tree.cc](../../../../../../../source/blender/nodes/shader/node_shader_tree.cc) · L215—L255。

接口参数：

- `bNodeTree *ntree`
- `int target`

**教学注释版**

<!-- annotated:ee9f5030d1ee04 -->

```cpp
bNode *ntreeShaderOutputNode(bNodeTree *ntree, int target)
{
  /* Make sure we only have single node tagged as output. */
  bke::node_tree_set_output(*ntree);

  /* Find output node that matches type and target. If there are
   * multiple, we prefer exact target match and active nodes. */
  bNode *output_node = nullptr;

  for (bNode &node : ntree->nodes) {
    if (!ELEM(
            node.type_legacy, SH_NODE_OUTPUT_MATERIAL, SH_NODE_OUTPUT_WORLD, SH_NODE_OUTPUT_LIGHT))
    {
      continue;
    }

    if (node.custom1 == SHD_OUTPUT_ALL) {
      if (output_node == nullptr) {
        output_node = &node;
      }
      else if (output_node->custom1 == SHD_OUTPUT_ALL) {
        if ((node.flag & NODE_DO_OUTPUT) && !(output_node->flag & NODE_DO_OUTPUT)) {
          output_node = &node;
        }
      }
    }
    else if (node.custom1 == target) {
      if (output_node == nullptr) {
        output_node = &node;
      }
      else if (output_node->custom1 == SHD_OUTPUT_ALL) {
        output_node = &node;
      }
      else if ((node.flag & NODE_DO_OUTPUT) && !(output_node->flag & NODE_DO_OUTPUT)) {
        output_node = &node;
      }
    }
  }

  return output_node;
}
```

<details>
<summary>核对原始源码：source/blender/nodes/shader/node_shader_tree.cc · L215—L255</summary>

<!-- original:ee9f5030d1ee04:source/blender/nodes/shader/node_shader_tree.cc:215:255 -->

```cpp
bNode *ntreeShaderOutputNode(bNodeTree *ntree, int target)
{
  /* Make sure we only have single node tagged as output. */
  bke::node_tree_set_output(*ntree);

  /* Find output node that matches type and target. If there are
   * multiple, we prefer exact target match and active nodes. */
  bNode *output_node = nullptr;

  for (bNode &node : ntree->nodes) {
    if (!ELEM(
            node.type_legacy, SH_NODE_OUTPUT_MATERIAL, SH_NODE_OUTPUT_WORLD, SH_NODE_OUTPUT_LIGHT))
    {
      continue;
    }

    if (node.custom1 == SHD_OUTPUT_ALL) {
      if (output_node == nullptr) {
        output_node = &node;
      }
      else if (output_node->custom1 == SHD_OUTPUT_ALL) {
        if ((node.flag & NODE_DO_OUTPUT) && !(output_node->flag & NODE_DO_OUTPUT)) {
          output_node = &node;
        }
      }
    }
    else if (node.custom1 == target) {
      if (output_node == nullptr) {
        output_node = &node;
      }
      else if (output_node->custom1 == SHD_OUTPUT_ALL) {
        output_node = &node;
      }
      else if ((node.flag & NODE_DO_OUTPUT) && !(output_node->flag & NODE_DO_OUTPUT)) {
        output_node = &node;
      }
    }
  }

  return output_node;
}
```

</details>

**沿实际写入检查状态**

- `output_node = &node;`

**结果出口**

- `return output_node;`

**继续追踪实现**

- `bke::node_tree_set_output` → [blender::bke::node_tree_set_output · L5238](../../02-BKE几何与数据/intern/node.cc.md#f-c27c9a3470a4650d)。
- `ELEM` → [ELEM · L88](../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-d28724a15928)；[ELEM · L135](../../01-BLI基础库/BLI_utildefines.hh.md#m-d6572de7cae0)。宏定义由构建条件选择。

<a id="f-f53e55e4762a4173"></a>

### `ntreeShaderEndExecTree_internal`

实现位置：[source/blender/nodes/shader/node_shader_tree.cc](../../../../../../../source/blender/nodes/shader/node_shader_tree.cc) · L1159—L1176。

接口参数：

- `bNodeTreeExec *exec`

**教学注释版**

<!-- annotated:d1dbebda8096cd -->

```cpp
void ntreeShaderEndExecTree_internal(bNodeTreeExec *exec)
{
  if (exec->threadstack) {
    for (int a = 0; a < BLENDER_MAX_THREADS; a++) {
      for (bNodeThreadStack &nts : exec->threadstack[a]) {
        if (nts.stack) {
          MEM_delete(nts.stack);
        }
      }
      BLI_freelistN(&exec->threadstack[a]);
    }

    MEM_delete(exec->threadstack);
    exec->threadstack = nullptr;
  }

  ntree_exec_end(exec);
}
```

<details>
<summary>核对原始源码：source/blender/nodes/shader/node_shader_tree.cc · L1159—L1176</summary>

<!-- original:d1dbebda8096cd:source/blender/nodes/shader/node_shader_tree.cc:1159:1176 -->

```cpp
void ntreeShaderEndExecTree_internal(bNodeTreeExec *exec)
{
  if (exec->threadstack) {
    for (int a = 0; a < BLENDER_MAX_THREADS; a++) {
      for (bNodeThreadStack &nts : exec->threadstack[a]) {
        if (nts.stack) {
          MEM_delete(nts.stack);
        }
      }
      BLI_freelistN(&exec->threadstack[a]);
    }

    MEM_delete(exec->threadstack);
    exec->threadstack = nullptr;
  }

  ntree_exec_end(exec);
}
```

</details>

**沿实际写入检查状态**

- `exec->threadstack = nullptr;`

**继续追踪实现**

- `MEM_delete` → [MEM_delete · L400](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
- `BLI_freelistN` → [blender::BLI_freelistN · L504](../../01-BLI基础库/intern/listbase.cc.md#f-c250f5cf55fbcbe4)。
- `ntree_exec_end` → [blender::ntree_exec_end · L284](../intern/node_exec.cc.md#f-2d3e765beff71d62)。

<a id="f-f1d2dce22315b98a"></a>

### `ntreeShaderEndExecTree`

实现位置：[source/blender/nodes/shader/node_shader_tree.cc](../../../../../../../source/blender/nodes/shader/node_shader_tree.cc) · L1178—L1189。

接口参数：

- `bNodeTreeExec *exec`

**教学注释版**

<!-- annotated:f5de8df10eaf14 -->

```cpp
void ntreeShaderEndExecTree(bNodeTreeExec *exec)
{
  if (exec) {
    /* exec may get freed, so assign ntree */
    bNodeTree *ntree = exec->nodetree;
    ntreeShaderEndExecTree_internal(exec);

    /* XXX: clear node-tree back-pointer to exec data,
     * same problem as noted in #ntreeBeginExecTree. */
    ntree->runtime->execdata = nullptr;
  }
}
```

<details>
<summary>核对原始源码：source/blender/nodes/shader/node_shader_tree.cc · L1178—L1189</summary>

<!-- original:f5de8df10eaf14:source/blender/nodes/shader/node_shader_tree.cc:1178:1189 -->

```cpp
void ntreeShaderEndExecTree(bNodeTreeExec *exec)
{
  if (exec) {
    /* exec may get freed, so assign ntree */
    bNodeTree *ntree = exec->nodetree;
    ntreeShaderEndExecTree_internal(exec);

    /* XXX: clear node-tree back-pointer to exec data,
     * same problem as noted in #ntreeBeginExecTree. */
    ntree->runtime->execdata = nullptr;
  }
}
```

</details>

**沿实际写入检查状态**

- `ntree->runtime->execdata = nullptr;`

**继续追踪实现**

- `ntreeShaderEndExecTree_internal` → [ntreeShaderEndExecTree_internal · L1159](node_shader_tree.cc.md#f-f53e55e4762a4173)。
