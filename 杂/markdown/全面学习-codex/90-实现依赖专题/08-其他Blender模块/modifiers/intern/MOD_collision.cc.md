# 实现依赖专题：source/blender/modifiers/intern/MOD_collision.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::free_data"]:::abstraction
  F1["blender::depends_on_time"]:::compute
  F2["blender::deform_verts"]:::compute
  F3["blender::update_depsgraph"]:::compute
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
  F["MOD_collision.cc实现"]:::compute
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

<a id="f-fcbe875a78191865"></a>

### `blender::free_data`

实现位置：[source/blender/modifiers/intern/MOD_collision.cc](../../../../../../../../source/blender/modifiers/intern/MOD_collision.cc) · L45—L68。

接口参数：

- `ModifierData *md`

**教学注释版**

<!-- annotated:e5621d344a525c -->

```cpp
static void free_data(ModifierData *md)
{
  CollisionModifierData *collmd = reinterpret_cast<CollisionModifierData *>(md);

  if (collmd) { /* Seriously? */
    if (collmd->bvhtree) {
      BLI_bvhtree_free(collmd->bvhtree);
      collmd->bvhtree = nullptr;
    }

    MEM_SAFE_DELETE(collmd->x);
    MEM_SAFE_DELETE(collmd->xnew);
    MEM_SAFE_DELETE(collmd->current_x);
    MEM_SAFE_DELETE(collmd->current_xnew);
    MEM_SAFE_DELETE(collmd->current_v);

    MEM_SAFE_DELETE(collmd->vert_tris);

    collmd->time_x = collmd->time_xnew = -1000;
    collmd->mvert_num = 0;
    collmd->tri_num = 0;
    collmd->is_static = false;
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_collision.cc · L45—L68</summary>

<!-- original:e5621d344a525c:source/blender/modifiers/intern/MOD_collision.cc:45:68 -->

```cpp
static void free_data(ModifierData *md)
{
  CollisionModifierData *collmd = reinterpret_cast<CollisionModifierData *>(md);

  if (collmd) { /* Seriously? */
    if (collmd->bvhtree) {
      BLI_bvhtree_free(collmd->bvhtree);
      collmd->bvhtree = nullptr;
    }

    MEM_SAFE_DELETE(collmd->x);
    MEM_SAFE_DELETE(collmd->xnew);
    MEM_SAFE_DELETE(collmd->current_x);
    MEM_SAFE_DELETE(collmd->current_xnew);
    MEM_SAFE_DELETE(collmd->current_v);

    MEM_SAFE_DELETE(collmd->vert_tris);

    collmd->time_x = collmd->time_xnew = -1000;
    collmd->mvert_num = 0;
    collmd->tri_num = 0;
    collmd->is_static = false;
  }
}
```

</details>

**沿实际写入检查状态**

- `collmd->bvhtree = nullptr;`
- `collmd->time_x = collmd->time_xnew = -1000;`
- `collmd->mvert_num = 0;`
- `collmd->tri_num = 0;`
- `collmd->is_static = false;`

**继续追踪实现**

- `BLI_bvhtree_free` → [blender::BLI_bvhtree_free · L935](../../../01-BLI基础库/intern/BLI_kdopbvh.cc.md#f-7dcbdb0a7d2476fe)。
- `MEM_SAFE_DELETE` → [MEM_SAFE_DELETE · L436](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#m-eadb3bc5b902)。宏定义由构建条件选择。

<a id="f-65a0ea2aa8dfffe3"></a>

### `blender::depends_on_time`

实现位置：[source/blender/modifiers/intern/MOD_collision.cc](../../../../../../../../source/blender/modifiers/intern/MOD_collision.cc) · L70—L73。

接口参数：

- `Scene *`
- `ModifierData *`

**教学注释版**

<!-- annotated:644eeecbc98d7d -->

```cpp
static bool depends_on_time(Scene * /*scene*/, ModifierData * /*md*/)
{
  return true;
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_collision.cc · L70—L73</summary>

<!-- original:644eeecbc98d7d:source/blender/modifiers/intern/MOD_collision.cc:70:73 -->

```cpp
static bool depends_on_time(Scene * /*scene*/, ModifierData * /*md*/)
{
  return true;
}
```

</details>

**结果出口**

- `return true;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-cef5b0b08bece31a"></a>

### `blender::deform_verts`

实现位置：[source/blender/modifiers/intern/MOD_collision.cc](../../../../../../../../source/blender/modifiers/intern/MOD_collision.cc) · L75—L220。

接口参数：

- `ModifierData *md`
- `const ModifierEvalContext *ctx`
- `Mesh *mesh`
- `MutableSpan<float3> positions`

**教学注释版**

<!-- annotated:0d7cdf1ad65363 -->

```cpp
static void deform_verts(ModifierData *md,
                         const ModifierEvalContext *ctx,
                         Mesh *mesh,
                         MutableSpan<float3> positions)
{
  CollisionModifierData *collmd = reinterpret_cast<CollisionModifierData *>(md);
  Object *ob = ctx->object;

  /* If collision is disabled, free the stale data and exit. */
  if (!ob->pd || !ob->pd->deflect) {
    if (!ob->pd) {
      printf("CollisionModifier: collision settings are missing!\n");
    }

    free_data(md);
    return;
  }

  if (mesh) {
    float current_time = 0;
    int mvert_num = 0;

    mesh->vert_positions_for_write().copy_from(positions);
    mesh->tag_positions_changed();

    current_time = DEG_get_ctime(ctx->depsgraph);

    if (G.debug & G_DEBUG_SIMDATA) {
      printf("current_time %f, collmd->time_xnew %f\n", current_time, collmd->time_xnew);
    }

    mvert_num = mesh->verts_num;

    if (current_time < collmd->time_xnew) {
      free_data(reinterpret_cast<ModifierData *>(collmd));
    }
    else if (current_time == collmd->time_xnew) {
      if (mvert_num != collmd->mvert_num) {
        free_data(reinterpret_cast<ModifierData *>(collmd));
      }
    }

    /* check if mesh has changed */
    if (collmd->x && (mvert_num != collmd->mvert_num)) {
      free_data(reinterpret_cast<ModifierData *>(collmd));
    }

    if (collmd->time_xnew == -1000) { /* first time */

      mvert_num = mesh->verts_num;
      collmd->x = MEM_new_array_uninitialized<float[3]>(size_t(mvert_num), __func__);
      MutableSpan(reinterpret_cast<float3 *>(collmd->x), mvert_num)
          .copy_from(mesh->vert_positions());

      for (uint i = 0; i < mvert_num; i++) {
        /* we save global positions */
        mul_m4_v3(ob->object_to_world().ptr(), collmd->x[i]);
      }

      collmd->xnew = MEM_dupalloc(collmd->x);         /* Frame end position. */
      collmd->current_x = MEM_dupalloc(collmd->x);    /* Inter-frame. */
      collmd->current_xnew = MEM_dupalloc(collmd->x); /* Inter-frame. */
      collmd->current_v = MEM_dupalloc(collmd->x);    /* Inter-frame. */

      collmd->mvert_num = mvert_num;

      {
        const Span<int3> corner_tris = mesh->corner_tris();
        // [讲解] corner_tris.size：查询视图长度或生成对应有效索引区间。
        collmd->tri_num = corner_tris.size();
        int (*vert_tris)[3] = MEM_new_array_uninitialized<int[3]>(collmd->tri_num, __func__);
        bke::mesh::vert_tris_from_corner_tris(
            mesh->corner_verts(),
            corner_tris,
            {reinterpret_cast<int3 *>(vert_tris), collmd->tri_num});
        collmd->vert_tris = vert_tris;
      }

      /* create bounding box hierarchy */
      collmd->bvhtree = bvhtree_build_from_mvert(collmd->x,
                                                 reinterpret_cast<int3 *>(collmd->vert_tris),
                                                 collmd->tri_num,
                                                 ob->pd->pdef_sboft);

      collmd->time_x = collmd->time_xnew = current_time;
      collmd->is_static = true;
    }
    else if (mvert_num == collmd->mvert_num) {
      /* put positions to old positions */
      float (*temp)[3] = collmd->x;
      collmd->x = collmd->xnew;
      collmd->xnew = temp;
      collmd->time_x = collmd->time_xnew;

      // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
      memcpy(collmd->xnew, mesh->vert_positions().data(), mvert_num * sizeof(float[3]));

      bool is_static = true;

      for (uint i = 0; i < mvert_num; i++) {
        /* we save global positions */
        mul_m4_v3(ob->object_to_world().ptr(), collmd->xnew[i]);

        /* detect motion */
        is_static = is_static && equals_v3v3(collmd->x[i], collmd->xnew[i]);
      }

      memcpy(collmd->current_xnew, collmd->x, mvert_num * sizeof(float[3]));
      memcpy(collmd->current_x, collmd->x, mvert_num * sizeof(float[3]));

      /* check if GUI setting has changed for bvh */
      if (collmd->bvhtree) {
        if (ob->pd->pdef_sboft != BLI_bvhtree_get_epsilon(collmd->bvhtree)) {
          BLI_bvhtree_free(collmd->bvhtree);
          collmd->bvhtree = bvhtree_build_from_mvert(
              collmd->current_x,
              reinterpret_cast<const int3 *>(collmd->vert_tris),
              collmd->tri_num,
              ob->pd->pdef_sboft);
        }
      }

      /* Happens on file load (ONLY when I un-comment changes in `readfile.cc`). */
      if (!collmd->bvhtree) {
        collmd->bvhtree = bvhtree_build_from_mvert(
            collmd->current_x,
            reinterpret_cast<const int3 *>(collmd->vert_tris),
            collmd->tri_num,
            ob->pd->pdef_sboft);
      }
      else if (!collmd->is_static || !is_static) {
        /* recalc static bounding boxes */
        bvhtree_update_from_mvert(collmd->bvhtree,
                                  collmd->current_x,
                                  collmd->current_xnew,
                                  reinterpret_cast<const int3 *>(collmd->vert_tris),
                                  collmd->tri_num,
                                  true);
      }

      collmd->is_static = is_static;
      collmd->time_xnew = current_time;
    }
    else if (mvert_num != collmd->mvert_num) {
      free_data(reinterpret_cast<ModifierData *>(collmd));
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_collision.cc · L75—L220</summary>

<!-- original:0d7cdf1ad65363:source/blender/modifiers/intern/MOD_collision.cc:75:220 -->

```cpp
static void deform_verts(ModifierData *md,
                         const ModifierEvalContext *ctx,
                         Mesh *mesh,
                         MutableSpan<float3> positions)
{
  CollisionModifierData *collmd = reinterpret_cast<CollisionModifierData *>(md);
  Object *ob = ctx->object;

  /* If collision is disabled, free the stale data and exit. */
  if (!ob->pd || !ob->pd->deflect) {
    if (!ob->pd) {
      printf("CollisionModifier: collision settings are missing!\n");
    }

    free_data(md);
    return;
  }

  if (mesh) {
    float current_time = 0;
    int mvert_num = 0;

    mesh->vert_positions_for_write().copy_from(positions);
    mesh->tag_positions_changed();

    current_time = DEG_get_ctime(ctx->depsgraph);

    if (G.debug & G_DEBUG_SIMDATA) {
      printf("current_time %f, collmd->time_xnew %f\n", current_time, collmd->time_xnew);
    }

    mvert_num = mesh->verts_num;

    if (current_time < collmd->time_xnew) {
      free_data(reinterpret_cast<ModifierData *>(collmd));
    }
    else if (current_time == collmd->time_xnew) {
      if (mvert_num != collmd->mvert_num) {
        free_data(reinterpret_cast<ModifierData *>(collmd));
      }
    }

    /* check if mesh has changed */
    if (collmd->x && (mvert_num != collmd->mvert_num)) {
      free_data(reinterpret_cast<ModifierData *>(collmd));
    }

    if (collmd->time_xnew == -1000) { /* first time */

      mvert_num = mesh->verts_num;
      collmd->x = MEM_new_array_uninitialized<float[3]>(size_t(mvert_num), __func__);
      MutableSpan(reinterpret_cast<float3 *>(collmd->x), mvert_num)
          .copy_from(mesh->vert_positions());

      for (uint i = 0; i < mvert_num; i++) {
        /* we save global positions */
        mul_m4_v3(ob->object_to_world().ptr(), collmd->x[i]);
      }

      collmd->xnew = MEM_dupalloc(collmd->x);         /* Frame end position. */
      collmd->current_x = MEM_dupalloc(collmd->x);    /* Inter-frame. */
      collmd->current_xnew = MEM_dupalloc(collmd->x); /* Inter-frame. */
      collmd->current_v = MEM_dupalloc(collmd->x);    /* Inter-frame. */

      collmd->mvert_num = mvert_num;

      {
        const Span<int3> corner_tris = mesh->corner_tris();
        collmd->tri_num = corner_tris.size();
        int (*vert_tris)[3] = MEM_new_array_uninitialized<int[3]>(collmd->tri_num, __func__);
        bke::mesh::vert_tris_from_corner_tris(
            mesh->corner_verts(),
            corner_tris,
            {reinterpret_cast<int3 *>(vert_tris), collmd->tri_num});
        collmd->vert_tris = vert_tris;
      }

      /* create bounding box hierarchy */
      collmd->bvhtree = bvhtree_build_from_mvert(collmd->x,
                                                 reinterpret_cast<int3 *>(collmd->vert_tris),
                                                 collmd->tri_num,
                                                 ob->pd->pdef_sboft);

      collmd->time_x = collmd->time_xnew = current_time;
      collmd->is_static = true;
    }
    else if (mvert_num == collmd->mvert_num) {
      /* put positions to old positions */
      float (*temp)[3] = collmd->x;
      collmd->x = collmd->xnew;
      collmd->xnew = temp;
      collmd->time_x = collmd->time_xnew;

      memcpy(collmd->xnew, mesh->vert_positions().data(), mvert_num * sizeof(float[3]));

      bool is_static = true;

      for (uint i = 0; i < mvert_num; i++) {
        /* we save global positions */
        mul_m4_v3(ob->object_to_world().ptr(), collmd->xnew[i]);

        /* detect motion */
        is_static = is_static && equals_v3v3(collmd->x[i], collmd->xnew[i]);
      }

      memcpy(collmd->current_xnew, collmd->x, mvert_num * sizeof(float[3]));
      memcpy(collmd->current_x, collmd->x, mvert_num * sizeof(float[3]));

      /* check if GUI setting has changed for bvh */
      if (collmd->bvhtree) {
        if (ob->pd->pdef_sboft != BLI_bvhtree_get_epsilon(collmd->bvhtree)) {
          BLI_bvhtree_free(collmd->bvhtree);
          collmd->bvhtree = bvhtree_build_from_mvert(
              collmd->current_x,
              reinterpret_cast<const int3 *>(collmd->vert_tris),
              collmd->tri_num,
              ob->pd->pdef_sboft);
        }
      }

      /* Happens on file load (ONLY when I un-comment changes in `readfile.cc`). */
      if (!collmd->bvhtree) {
        collmd->bvhtree = bvhtree_build_from_mvert(
            collmd->current_x,
            reinterpret_cast<const int3 *>(collmd->vert_tris),
            collmd->tri_num,
            ob->pd->pdef_sboft);
      }
      else if (!collmd->is_static || !is_static) {
        /* recalc static bounding boxes */
        bvhtree_update_from_mvert(collmd->bvhtree,
                                  collmd->current_x,
                                  collmd->current_xnew,
                                  reinterpret_cast<const int3 *>(collmd->vert_tris),
                                  collmd->tri_num,
                                  true);
      }

      collmd->is_static = is_static;
      collmd->time_xnew = current_time;
    }
    else if (mvert_num != collmd->mvert_num) {
      free_data(reinterpret_cast<ModifierData *>(collmd));
    }
  }
}
```

</details>

**沿实际写入检查状态**

- `current_time = DEG_get_ctime(ctx->depsgraph);`
- `mvert_num = mesh->verts_num;`
- `collmd->x = MEM_new_array_uninitialized<float[3]>(size_t(mvert_num), __func__);`
- `collmd->xnew = MEM_dupalloc(collmd->x);         /* Frame end position. */`
- `collmd->current_x = MEM_dupalloc(collmd->x);    /* Inter-frame. */`
- `collmd->current_xnew = MEM_dupalloc(collmd->x); /* Inter-frame. */`
- `collmd->current_v = MEM_dupalloc(collmd->x);    /* Inter-frame. */`
- `collmd->mvert_num = mvert_num;`
- `collmd->tri_num = corner_tris.size();`
- `collmd->vert_tris = vert_tris;`
- `collmd->bvhtree = bvhtree_build_from_mvert(collmd->x,`
- `collmd->time_x = collmd->time_xnew = current_time;`
- `collmd->is_static = true;`
- `collmd->x = collmd->xnew;`
- `collmd->xnew = temp;`
- `collmd->time_x = collmd->time_xnew;`
- `is_static = is_static && equals_v3v3(collmd->x[i], collmd->xnew[i]);`
- `collmd->bvhtree = bvhtree_build_from_mvert(`
- `collmd->is_static = is_static;`
- `collmd->time_xnew = current_time;`

**继续追踪实现**

- `printf` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `free_data` → [blender::free_data · L45](MOD_collision.cc.md#f-fcbe875a78191865)。
- `mesh->vert_positions_for_write().copy_from` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L97。
- `mesh->vert_positions_for_write` → [Mesh::vert_positions_for_write · L1199](../../../../05-几何存储与拓扑映射/03-MPoly迁移与兼容.md#f-ae8d77205112d843)。
- `mesh->tag_positions_changed` → [blender::Mesh::tag_positions_changed · L407](../../../../06-隐式共享与缓存系统/10-局部更新与失效修复.md#f-90e852663d44ad53)。
- `DEG_get_ctime` → [blender::DEG_get_ctime · L105](../../../06-Depsgraph依赖图/intern/depsgraph_query.cc.md#f-156dee0918a22f2f)。
- `MEM_new_array_uninitialized<float[3]>` → [MEM_new_array_uninitialized · L608](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-b7103eae8eb57b05)；[MEM_new_array_uninitialized · L129](../../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-bf6ef4ddcfb6e5df)。同名重载需按实参类型选择。
- `MutableSpan(reinterpret_cast<float3 *>(collmd->x), mvert_num) .copy_from` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L126。
- `MutableSpan` → [blender::MutableSpan::MutableSpan · L462](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-0f07034aaffc3384)；[blender::MutableSpan::MutableSpan · L464](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-39977234ad0ce192)；[blender::MutableSpan::MutableSpan · L466](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-ee249b5042dd38aa)；[blender::MutableSpan::MutableSpan · L468](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-479c5f85921e531f)；[blender::MutableSpan::MutableSpan · L477](../../../../01-基础容器与现代CPP/06-MutableSpan可写视图.md#f-afcce5325e6f19e0)。同名重载需按实参类型选择。
- `mesh->vert_positions` → [Mesh::vert_positions · L1193](../../../../05-几何存储与拓扑映射/03-MPoly迁移与兼容.md#f-ae4177e5c5f2b371)。
- `mul_m4_v3` → [blender::mul_m4_v3 · L677](../../../01-BLI基础库/intern/math_matrix_c.cc.md#f-14a8c267710d47a3)。
- `ob->object_to_world().ptr` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L131。
- `ob->object_to_world` → [blender::Object::object_to_world · L5761](../../../02-BKE几何与数据/intern/object.cc.md#f-12fc20026327d50c)。
- `MEM_dupalloc` → [MEM_dupalloc · L627](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-78a72b71e3c57010)。
- `mesh->corner_tris` → [blender::Mesh::corner_tris · L264](../../../../06-隐式共享与缓存系统/10-局部更新与失效修复.md#f-9bb421790000fc20)。
- `corner_tris.size` → [blender::Span::size · L256](../../../../01-基础容器与现代CPP/05-Span只读连续视图.md#f-5f80fa006089c998)。
- `MEM_new_array_uninitialized<int[3]>` → [MEM_new_array_uninitialized · L608](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-b7103eae8eb57b05)；[MEM_new_array_uninitialized · L129](../../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-bf6ef4ddcfb6e5df)。同名重载需按实参类型选择。
- `bke::mesh::vert_tris_from_corner_tris` → [blender::bke::mesh::vert_tris_from_corner_tris · L238](../../../02-BKE几何与数据/intern/mesh_tessellate.cc.md#f-148011c2040a8b1e)。
- `mesh->corner_verts` → [Mesh::corner_verts · L1238](../../../../05-几何存储与拓扑映射/03-MPoly迁移与兼容.md#f-a59c61f583b64bc4)。
- `bvhtree_build_from_mvert` → [blender::bvhtree_build_from_mvert · L92](../../../02-BKE几何与数据/intern/collision.cc.md#f-22a69c1c8a174747)。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
- `mesh->vert_positions().data` → [调用协议](../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L168。
- `equals_v3v3` → [blender::equals_v3v3 · L1006](../../../01-BLI基础库/intern/math_vector_inline.cc.md#f-f49aac9436333b4a)。
- `BLI_bvhtree_get_epsilon` → [blender::BLI_bvhtree_get_epsilon · L1053](../../../01-BLI基础库/intern/BLI_kdopbvh.cc.md#f-65fb6578a78d4c5b)。
- `BLI_bvhtree_free` → [blender::BLI_bvhtree_free · L935](../../../01-BLI基础库/intern/BLI_kdopbvh.cc.md#f-7dcbdb0a7d2476fe)。
- `bvhtree_update_from_mvert` → [blender::bvhtree_update_from_mvert · L116](../../../02-BKE几何与数据/intern/collision.cc.md#f-6ac2b21f6e781ee3)。

<a id="f-9ccfa258531f3b93"></a>

### `blender::update_depsgraph`

实现位置：[source/blender/modifiers/intern/MOD_collision.cc](../../../../../../../../source/blender/modifiers/intern/MOD_collision.cc) · L222—L225。

接口参数：

- `ModifierData *`
- `const ModifierUpdateDepsgraphContext *ctx`

**教学注释版**

<!-- annotated:bc1d6eb04e6343 -->

```cpp
static void update_depsgraph(ModifierData * /*md*/, const ModifierUpdateDepsgraphContext *ctx)
{
  DEG_add_depends_on_transform_relation(ctx->node, "Collision Modifier");
}
```

<details>
<summary>核对原始源码：source/blender/modifiers/intern/MOD_collision.cc · L222—L225</summary>

<!-- original:bc1d6eb04e6343:source/blender/modifiers/intern/MOD_collision.cc:222:225 -->

```cpp
static void update_depsgraph(ModifierData * /*md*/, const ModifierUpdateDepsgraphContext *ctx)
{
  DEG_add_depends_on_transform_relation(ctx->node, "Collision Modifier");
}
```

</details>

**继续追踪实现**

- `DEG_add_depends_on_transform_relation` → [blender::DEG_add_depends_on_transform_relation · L240](../../../06-Depsgraph依赖图/intern/depsgraph_build.cc.md#f-47c32a354defa20d)。
