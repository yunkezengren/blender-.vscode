# 实现依赖专题：source/blender/editors/space_outliner/outliner_utils.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::ed::outliner::outliner_tree_traverse"]:::abstraction
  F0 -->|"显式调用"| F0
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
  F["outliner_utils.cc实现"]:::compute
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

<a id="f-b61df82f59e25d78"></a>

### `blender::ed::outliner::outliner_tree_traverse`

实现位置：[source/blender/editors/space_outliner/outliner_utils.cc](../../../../../../../../source/blender/editors/space_outliner/outliner_utils.cc) · L306—L346。

接口参数：

- `const SpaceOutliner *space_outliner`
- `ListBaseT<TreeElement> *tree`
- `int filter_te_flag`
- `int filter_tselem_flag`
- `TreeTraversalFunc func`
- `void *customdata`

**教学注释版**

<!-- annotated:868945d611cb21 -->

```cpp
bool outliner_tree_traverse(const SpaceOutliner *space_outliner,
                            ListBaseT<TreeElement> *tree,
                            int filter_te_flag,
                            int filter_tselem_flag,
                            TreeTraversalFunc func,
                            void *customdata)
{
  for (TreeElement *te = tree->first(), *te_next; te; te = te_next) {
    TreeTraversalAction func_retval = TRAVERSE_CONTINUE;
    /* in case te is freed in callback */
    TreeStoreElem *tselem = TREESTORE(te);
    ListBaseT<TreeElement> subtree = te->subtree;
    te_next = te->next;

    if (filter_te_flag && (te->flag & filter_te_flag) == 0) {
      /* skip */
    }
    else if (filter_tselem_flag && (tselem->flag & filter_tselem_flag) == 0) {
      /* skip */
    }
    else {
      func_retval = func(te, customdata);
    }
    /* Don't access te or tselem from now on! Might've been freed... */

    if (func_retval == TRAVERSE_BREAK) {
      return false;
    }

    if (func_retval == TRAVERSE_SKIP_CHILDS) {
      /* skip */
    }
    else if (!outliner_tree_traverse(
                 space_outliner, &subtree, filter_te_flag, filter_tselem_flag, func, customdata))
    {
      return false;
    }
  }

  return true;
}
```

<details>
<summary>核对原始源码：source/blender/editors/space_outliner/outliner_utils.cc · L306—L346</summary>

<!-- original:868945d611cb21:source/blender/editors/space_outliner/outliner_utils.cc:306:346 -->

```cpp
bool outliner_tree_traverse(const SpaceOutliner *space_outliner,
                            ListBaseT<TreeElement> *tree,
                            int filter_te_flag,
                            int filter_tselem_flag,
                            TreeTraversalFunc func,
                            void *customdata)
{
  for (TreeElement *te = tree->first(), *te_next; te; te = te_next) {
    TreeTraversalAction func_retval = TRAVERSE_CONTINUE;
    /* in case te is freed in callback */
    TreeStoreElem *tselem = TREESTORE(te);
    ListBaseT<TreeElement> subtree = te->subtree;
    te_next = te->next;

    if (filter_te_flag && (te->flag & filter_te_flag) == 0) {
      /* skip */
    }
    else if (filter_tselem_flag && (tselem->flag & filter_tselem_flag) == 0) {
      /* skip */
    }
    else {
      func_retval = func(te, customdata);
    }
    /* Don't access te or tselem from now on! Might've been freed... */

    if (func_retval == TRAVERSE_BREAK) {
      return false;
    }

    if (func_retval == TRAVERSE_SKIP_CHILDS) {
      /* skip */
    }
    else if (!outliner_tree_traverse(
                 space_outliner, &subtree, filter_te_flag, filter_tselem_flag, func, customdata))
    {
      return false;
    }
  }

  return true;
}
```

</details>

**沿实际写入检查状态**

- `te_next = te->next;`
- `func_retval = func(te, customdata);`

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `tree->first` → [blender::ListBaseT::first · L102](../../makesdna/DNA_listBase.h.md#f-3d12ff35da057c9e)；[blender::ListBaseT::first · L106](../../makesdna/DNA_listBase.h.md#f-0df87c3480e059f9)。同名重载需按实参类型选择。
- `TREESTORE` → [TREESTORE · L197](outliner_intern.hh.md#m-e90e76fc5e4d)。宏定义由构建条件选择。
- `func` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L327。
- `outliner_tree_traverse` → [blender::ed::outliner::outliner_tree_traverse · L306](outliner_utils.cc.md#f-b61df82f59e25d78)。
