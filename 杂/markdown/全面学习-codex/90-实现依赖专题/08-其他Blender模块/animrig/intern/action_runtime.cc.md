# 实现依赖专题：source/blender/animrig/intern/action_runtime.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::animrig::internal::rebuild_slot_user_cache"]:::abstraction
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
  F["action_runtime.cc实现"]:::compute
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

<a id="f-c3b5ccf359ab038c"></a>

### `blender::animrig::internal::rebuild_slot_user_cache`

实现位置：[source/blender/animrig/intern/action_runtime.cc](../../../../../../../../source/blender/animrig/intern/action_runtime.cc) · L28—L99。

接口参数：

- `Main &bmain`

**教学注释版**

<!-- annotated:1b1d4d9ef4f28f -->

```cpp
void rebuild_slot_user_cache(Main &bmain)
{
  /* Loop over all Actions and clear their slots' user cache. */
  for (bAction &dna_action : bmain.actions) {
    Action &action = dna_action.wrap();
    for (Slot *slot : action.slots()) {
      BLI_assert_msg(slot->runtime, "Slot::runtime should always be allocated");
      slot->runtime->users.clear();
    }
  }

  /* Mark all Slots as clear. This is a bit of a lie, because the code below still has to run.
   * However, this is a necessity to make the `slot.users_add(*id)` call work without triggering
   * an infinite recursion.
   *
   * The alternative would be to go around the `slot.users_add()` function and access the
   * runtime directly, but this is IMO a bit cleaner. */
  bmain.is_action_slot_to_id_map_dirty = false;

  /* Visit any ID to see which Action+Slot it is using. Returns whether the ID
   * was visited for the first time. */
  Set<ID *> visited_ids;
  auto visit_id = [&visited_ids](ID *id) -> bool {
    BLI_assert(id);

    // [讲解] visited_ids.add：按哈希与相等关系加入键或键值。
    if (!visited_ids.add(id)) {
      return false;
    }

    foreach_action_slot_use(*id, [&](Action &action, slot_handle_t slot_handle) {
      Slot *slot = action.slot_for_handle(slot_handle);
      if (!slot) {
        return true;
      }
      slot->users_add(*id);
      return true;
    });

    return true;
  };

  /* Loop over all IDs to cache their slot usage. */
  ListBaseT<ID> *ids_of_idtype;
  ID *id;
  FOREACH_MAIN_LISTBASE_BEGIN (&bmain, ids_of_idtype) {
    /* Check whether this ID type can be animated. If not, just skip all IDs of this type. */
    id = ids_of_idtype->first();
    if (!id || !id_type_can_have_animdata(GS(id->name))) {
      continue;
    }

    FOREACH_MAIN_LISTBASE_ID_BEGIN (ids_of_idtype, id) {
      BLI_assert(id_can_have_animdata(id));

      /* Process the ID itself. */
      if (!visit_id(id)) {
        continue;
      }

      /* Process embedded IDs, as these are not listed in bmain, but still can
       * have their own Action+Slot. Unfortunately there is no generic looper
       * for embedded IDs. At this moment the only animatable embedded ID is a
       * node tree. */
      bNodeTree *node_tree = bke::node_tree_from_id(id);
      if (node_tree) {
        visit_id(&node_tree->id);
      }
    }
    FOREACH_MAIN_LISTBASE_ID_END;
  }
  FOREACH_MAIN_LISTBASE_END;
}
```

<details>
<summary>核对原始源码：source/blender/animrig/intern/action_runtime.cc · L28—L99</summary>

<!-- original:1b1d4d9ef4f28f:source/blender/animrig/intern/action_runtime.cc:28:99 -->

```cpp
void rebuild_slot_user_cache(Main &bmain)
{
  /* Loop over all Actions and clear their slots' user cache. */
  for (bAction &dna_action : bmain.actions) {
    Action &action = dna_action.wrap();
    for (Slot *slot : action.slots()) {
      BLI_assert_msg(slot->runtime, "Slot::runtime should always be allocated");
      slot->runtime->users.clear();
    }
  }

  /* Mark all Slots as clear. This is a bit of a lie, because the code below still has to run.
   * However, this is a necessity to make the `slot.users_add(*id)` call work without triggering
   * an infinite recursion.
   *
   * The alternative would be to go around the `slot.users_add()` function and access the
   * runtime directly, but this is IMO a bit cleaner. */
  bmain.is_action_slot_to_id_map_dirty = false;

  /* Visit any ID to see which Action+Slot it is using. Returns whether the ID
   * was visited for the first time. */
  Set<ID *> visited_ids;
  auto visit_id = [&visited_ids](ID *id) -> bool {
    BLI_assert(id);

    if (!visited_ids.add(id)) {
      return false;
    }

    foreach_action_slot_use(*id, [&](Action &action, slot_handle_t slot_handle) {
      Slot *slot = action.slot_for_handle(slot_handle);
      if (!slot) {
        return true;
      }
      slot->users_add(*id);
      return true;
    });

    return true;
  };

  /* Loop over all IDs to cache their slot usage. */
  ListBaseT<ID> *ids_of_idtype;
  ID *id;
  FOREACH_MAIN_LISTBASE_BEGIN (&bmain, ids_of_idtype) {
    /* Check whether this ID type can be animated. If not, just skip all IDs of this type. */
    id = ids_of_idtype->first();
    if (!id || !id_type_can_have_animdata(GS(id->name))) {
      continue;
    }

    FOREACH_MAIN_LISTBASE_ID_BEGIN (ids_of_idtype, id) {
      BLI_assert(id_can_have_animdata(id));

      /* Process the ID itself. */
      if (!visit_id(id)) {
        continue;
      }

      /* Process embedded IDs, as these are not listed in bmain, but still can
       * have their own Action+Slot. Unfortunately there is no generic looper
       * for embedded IDs. At this moment the only animatable embedded ID is a
       * node tree. */
      bNodeTree *node_tree = bke::node_tree_from_id(id);
      if (node_tree) {
        visit_id(&node_tree->id);
      }
    }
    FOREACH_MAIN_LISTBASE_ID_END;
  }
  FOREACH_MAIN_LISTBASE_END;
}
```

</details>

**沿实际写入检查状态**

- `bmain.is_action_slot_to_id_map_dirty = false;`
- `id = ids_of_idtype->first();`

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `dna_action.wrap` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L32。
- `action.slots` → [blender::animrig::Action::slots · L335](action.cc.md#f-09f0ee82f767ecad)；[blender::animrig::Action::slots · L339](action.cc.md#f-908f78ba1be8926d)。同名重载需按实参类型选择。
- `BLI_assert_msg` → [BLI_assert_msg · L55](../../../01-BLI基础库/BLI_assert.hh.md#m-695eed20dceb)；[BLI_assert_msg · L64](../../../01-BLI基础库/BLI_assert.hh.md#m-7de5563de4db)。宏定义由构建条件选择。
- `slot->runtime->users.clear` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L35。
- `BLI_assert` → [BLI_assert · L48](../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `visited_ids.add` → [blender::Set::add · L248](../../../../02-哈希表与关联数据结构/08-Set与集合语义.md#f-c7498809c2327fba)；[blender::Set::add · L252](../../../../02-哈希表与关联数据结构/08-Set与集合语义.md#f-e3ac8d1c52c03c2b)。同名重载需按实参类型选择。
- `foreach_action_slot_use` → [blender::animrig::foreach_action_slot_use · L94](action_iterators.cc.md#f-93353453550f639a)。
- `action.slot_for_handle` → [blender::animrig::Action::slot_for_handle · L352](action.cc.md#f-0ca66427ea102118)；[blender::animrig::Action::slot_for_handle · L358](action.cc.md#f-85ad4c7b53315484)。同名重载需按实参类型选择。
- `slot->users_add` → [blender::animrig::Slot::users_add · L1083](action.cc.md#f-83ebed02aaa1497e)。
- `FOREACH_MAIN_LISTBASE_BEGIN` → [FOREACH_MAIN_LISTBASE_BEGIN · L705](../../../02-BKE几何与数据/BKE_main.hh.md#m-85586e66025e)。宏定义由构建条件选择。
- `ids_of_idtype->first` → [blender::ListBaseT::first · L102](../../makesdna/DNA_listBase.h.md#f-3d12ff35da057c9e)；[blender::ListBaseT::first · L106](../../makesdna/DNA_listBase.h.md#f-0df87c3480e059f9)。同名重载需按实参类型选择。
- `id_type_can_have_animdata` → [blender::id_type_can_have_animdata · L69](../../../02-BKE几何与数据/intern/anim_data.cc.md#f-817565962e9ceb86)。
- `GS` → [blender::GS · L410](../../makesdna/DNA_ID.h.md#f-c3ff509f79f21b05)。
- `id_can_have_animdata` → [blender::id_can_have_animdata · L78](../../../02-BKE几何与数据/intern/anim_data.cc.md#f-006144b58a860d8d)。
- `visit_id` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L83。
- `bke::node_tree_from_id` → [blender::bke::node_tree_from_id · L5337](../../../02-BKE几何与数据/intern/node.cc.md#f-9bb7511df53d8493)。
