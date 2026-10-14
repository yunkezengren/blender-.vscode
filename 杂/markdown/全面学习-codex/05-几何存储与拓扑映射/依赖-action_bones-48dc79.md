# 实现依赖专题：source/blender/blenkernel/intern/action_bones.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::bke::BKE_action_find_fcurves_with_bones"]:::abstraction
  F1["blender::bke::BKE_action_find_fcurves_with_bones"]:::compute
  F0 -->|"显式调用"| F0
  F0 -->|"显式调用"| F1
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
  F["action_bones.cc实现"]:::compute
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

<a id="f-9745e4376c100546"></a>

### `blender::bke::BKE_action_find_fcurves_with_bones`

实现位置：[source/blender/blenkernel/intern/action_bones.cc](../../../../../source/blender/blenkernel/intern/action_bones.cc) · L21—L30。

接口参数：

- `bAction *action`
- `const animrig::slot_handle_t slot_handle`
- `FoundFCurveCallback callback`

**教学注释版**

<!-- annotated:293a2115a16a9f -->

```cpp
void BKE_action_find_fcurves_with_bones(bAction *action,
                                        const animrig::slot_handle_t slot_handle,
                                        FoundFCurveCallback callback)
{
  auto const_callback = [&](const FCurve *fcurve, const char *bone_name) {
    callback(const_cast<FCurve *>(fcurve), bone_name);
  };
  BKE_action_find_fcurves_with_bones(
      const_cast<const bAction *>(action), slot_handle, const_callback);
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/action_bones.cc · L21—L30</summary>

<!-- original:293a2115a16a9f:source/blender/blenkernel/intern/action_bones.cc:21:30 -->

```cpp
void BKE_action_find_fcurves_with_bones(bAction *action,
                                        const animrig::slot_handle_t slot_handle,
                                        FoundFCurveCallback callback)
{
  auto const_callback = [&](const FCurve *fcurve, const char *bone_name) {
    callback(const_cast<FCurve *>(fcurve), bone_name);
  };
  BKE_action_find_fcurves_with_bones(
      const_cast<const bAction *>(action), slot_handle, const_callback);
}
```

</details>

**继续追踪实现**

- `callback` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L26。
- `BKE_action_find_fcurves_with_bones` → [blender::bke::BKE_action_find_fcurves_with_bones · L21](%E4%BE%9D%E8%B5%96-action_bones-48dc79.md#f-9745e4376c100546)；[blender::bke::BKE_action_find_fcurves_with_bones · L32](%E4%BE%9D%E8%B5%96-action_bones-48dc79.md#f-da05aab12ef96e57)。同名重载需按实参类型选择。

<a id="f-da05aab12ef96e57"></a>

### `blender::bke::BKE_action_find_fcurves_with_bones`

实现位置：[source/blender/blenkernel/intern/action_bones.cc](../../../../../source/blender/blenkernel/intern/action_bones.cc) · L32—L45。

接口参数：

- `const bAction *action`
- `const animrig::slot_handle_t slot_handle`
- `FoundFCurveCallbackConst callback`

**教学注释版**

<!-- annotated:000cf1e055423e -->

```cpp
void BKE_action_find_fcurves_with_bones(const bAction *action,
                                        const animrig::slot_handle_t slot_handle,
                                        FoundFCurveCallbackConst callback)
{
  for (const FCurve *fcu : animrig::fcurves_for_action_slot(action->wrap(), slot_handle)) {
    char bone_name[MAXBONENAME];
    if (!BLI_str_quoted_substr(
            fcu->rna_path().c_str(), "pose.bones[", bone_name, sizeof(bone_name)))
    {
      continue;
    }
    callback(fcu, bone_name);
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenkernel/intern/action_bones.cc · L32—L45</summary>

<!-- original:000cf1e055423e:source/blender/blenkernel/intern/action_bones.cc:32:45 -->

```cpp
void BKE_action_find_fcurves_with_bones(const bAction *action,
                                        const animrig::slot_handle_t slot_handle,
                                        FoundFCurveCallbackConst callback)
{
  for (const FCurve *fcu : animrig::fcurves_for_action_slot(action->wrap(), slot_handle)) {
    char bone_name[MAXBONENAME];
    if (!BLI_str_quoted_substr(
            fcu->rna_path().c_str(), "pose.bones[", bone_name, sizeof(bone_name)))
    {
      continue;
    }
    callback(fcu, bone_name);
  }
}
```

</details>

**继续追踪实现**

- `animrig::fcurves_for_action_slot` → [blender::animrig::fcurves_for_action_slot · L2544](%E4%BE%9D%E8%B5%96-action-a70714.md#f-78c71d42065fc00f)；[blender::animrig::fcurves_for_action_slot · L2554](%E4%BE%9D%E8%B5%96-action-a70714.md#f-c1c45d131d9cf075)。同名重载需按实参类型选择。
- `action->wrap` → [blender::bAction::wrap · L1929](%E4%BE%9D%E8%B5%96-ANIM_action-8e402f.md#f-f049614274fd7a45)；[blender::bAction::wrap · L1933](%E4%BE%9D%E8%B5%96-ANIM_action-8e402f.md#f-2d697d1983fd282f)。同名重载需按实参类型选择。
- `BLI_str_quoted_substr` → [blender::BLI_str_quoted_substr · L527](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-string-1d986f.md#f-1f02ab716623972c)。
- `fcu->rna_path().c_str` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L39。
- `fcu->rna_path` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L39。
- `callback` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L43。
