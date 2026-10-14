# 实现依赖专题：source/blender/sequencer/intern/modifiers/modifier.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::seq::modifier_has_persistent_uid"]:::abstraction
  F1["blender::seq::modifier_persistent_uid_init"]:::compute
  F2["blender::seq::modifier_type_info_get"]:::compute
  F3["blender::seq::modifier_set_active"]:::compute
  F4["blender::seq::foreach_strip_modifier_id"]:::compute
  F1 -->|"显式调用"| F0
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
  F["modifier.cc实现"]:::compute
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

<a id="f-c321a7e1cf6803e0"></a>

### `blender::seq::modifier_has_persistent_uid`

实现位置：[source/blender/sequencer/intern/modifiers/modifier.cc](../../../../../source/blender/sequencer/intern/modifiers/modifier.cc) · L52—L60。

接口参数：

- `const Strip &strip`
- `int uid`

**教学注释版**

<!-- annotated:cb67d7982abfe8 -->

```cpp
static bool modifier_has_persistent_uid(const Strip &strip, int uid)
{
  for (StripModifierData &smd : strip.modifiers) {
    if (smd.persistent_uid == uid) {
      return true;
    }
  }
  return false;
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/modifiers/modifier.cc · L52—L60</summary>

<!-- original:cb67d7982abfe8:source/blender/sequencer/intern/modifiers/modifier.cc:52:60 -->

```cpp
static bool modifier_has_persistent_uid(const Strip &strip, int uid)
{
  for (StripModifierData &smd : strip.modifiers) {
    if (smd.persistent_uid == uid) {
      return true;
    }
  }
  return false;
}
```

</details>

**结果出口**

- `return true;`
- `return false;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-08629f38ab2827df"></a>

### `blender::seq::modifier_persistent_uid_init`

实现位置：[source/blender/sequencer/intern/modifiers/modifier.cc](../../../../../source/blender/sequencer/intern/modifiers/modifier.cc) · L62—L77。

接口参数：

- `const Strip &strip`
- `StripModifierData &smd`

**教学注释版**

<!-- annotated:80487c7ef67c04 -->

```cpp
void modifier_persistent_uid_init(const Strip &strip, StripModifierData &smd)
{
  uint64_t hash = get_default_hash(StringRef(smd.name));
  RandomNumberGenerator rng{uint32_t(hash)};
  while (true) {
    const int new_uid = rng.get_int32();
    if (new_uid <= 0) {
      continue;
    }
    if (modifier_has_persistent_uid(strip, new_uid)) {
      continue;
    }
    smd.persistent_uid = new_uid;
    break;
  }
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/modifiers/modifier.cc · L62—L77</summary>

<!-- original:80487c7ef67c04:source/blender/sequencer/intern/modifiers/modifier.cc:62:77 -->

```cpp
void modifier_persistent_uid_init(const Strip &strip, StripModifierData &smd)
{
  uint64_t hash = get_default_hash(StringRef(smd.name));
  RandomNumberGenerator rng{uint32_t(hash)};
  while (true) {
    const int new_uid = rng.get_int32();
    if (new_uid <= 0) {
      continue;
    }
    if (modifier_has_persistent_uid(strip, new_uid)) {
      continue;
    }
    smd.persistent_uid = new_uid;
    break;
  }
}
```

</details>

**沿实际写入检查状态**

- `smd.persistent_uid = new_uid;`

**继续追踪实现**

- `get_default_hash` → [blender::get_default_hash · L251](../02-%E5%93%88%E5%B8%8C%E8%A1%A8%E4%B8%8E%E5%85%B3%E8%81%94%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/01-%E5%93%88%E5%B8%8C%E4%B8%8E%E7%9B%B8%E7%AD%89%E5%A5%91%E7%BA%A6.md#f-5f2c246aedf3dc0a)。
- `StringRef` → [blender::StringRef::StringRef · L555](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-f6aca324a36faa7e)；[blender::StringRef::StringRef · L560](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-ab9714781ca51bac)；[blender::StringRef::StringRef · L565](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-95f0b483bbdd7739)；[blender::StringRef::StringRef · L570](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-808d05699cb33334)；[blender::StringRef::StringRef · L631](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-37788e5f3fa3b736)；[blender::StringRef::StringRef · L641](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-11abd0510fb6b926)；[blender::StringRef::StringRef · L646](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-8437dbd8a582eefd)；[blender::StringRef::StringRef · L651](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/15-StringRef%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%A7%86%E5%9B%BE.md#f-70bcb338de0db978)。同名重载需按实参类型选择。
- `rng.get_int32` → [blender::RandomNumberGenerator::get_int32 · L52](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_rand-a32134.md#f-2241ace1b1d89483)；[blender::RandomNumberGenerator::get_int32 · L66](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_rand-a32134.md#f-749e1881a54f698a)。同名重载需按实参类型选择。
- `modifier_has_persistent_uid` → [blender::seq::modifier_has_persistent_uid · L52](%E4%BE%9D%E8%B5%96-modifier-39433f.md#f-c321a7e1cf6803e0)。

<a id="f-de48cd1b87918836"></a>

### `blender::seq::modifier_type_info_get`

实现位置：[source/blender/sequencer/intern/modifiers/modifier.cc](../../../../../source/blender/sequencer/intern/modifiers/modifier.cc) · L416—L422。

接口参数：

- `eStripModifierType type`

**教学注释版**

<!-- annotated:cc8ad8b075715e -->

```cpp
const StripModifierTypeInfo *modifier_type_info_get(eStripModifierType type)
{
  if (type <= 0 || type >= NUM_STRIP_MODIFIER_TYPES) {
    return nullptr;
  }
  return modifiersTypes[type];
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/modifiers/modifier.cc · L416—L422</summary>

<!-- original:cc8ad8b075715e:source/blender/sequencer/intern/modifiers/modifier.cc:416:422 -->

```cpp
const StripModifierTypeInfo *modifier_type_info_get(eStripModifierType type)
{
  if (type <= 0 || type >= NUM_STRIP_MODIFIER_TYPES) {
    return nullptr;
  }
  return modifiersTypes[type];
}
```

</details>

**结果出口**

- `return nullptr;`
- `return modifiersTypes[type];`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-6f8607a742a8479a"></a>

### `blender::seq::modifier_set_active`

实现位置：[source/blender/sequencer/intern/modifiers/modifier.cc](../../../../../source/blender/sequencer/intern/modifiers/modifier.cc) · L643—L653。

接口参数：

- `Strip *strip`
- `StripModifierData *smd`

**教学注释版**

<!-- annotated:68c13243a758bc -->

```cpp
void modifier_set_active(Strip *strip, StripModifierData *smd)
{
  for (StripModifierData &smd_iter : strip->modifiers) {
    smd_iter.flag &= ~STRIP_MODIFIER_FLAG_ACTIVE;
  }

  if (smd != nullptr) {
    BLI_assert(BLI_findindex(&strip->modifiers, smd) != -1);
    smd->flag |= STRIP_MODIFIER_FLAG_ACTIVE;
  }
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/modifiers/modifier.cc · L643—L653</summary>

<!-- original:68c13243a758bc:source/blender/sequencer/intern/modifiers/modifier.cc:643:653 -->

```cpp
void modifier_set_active(Strip *strip, StripModifierData *smd)
{
  for (StripModifierData &smd_iter : strip->modifiers) {
    smd_iter.flag &= ~STRIP_MODIFIER_FLAG_ACTIVE;
  }

  if (smd != nullptr) {
    BLI_assert(BLI_findindex(&strip->modifiers, smd) != -1);
    smd->flag |= STRIP_MODIFIER_FLAG_ACTIVE;
  }
}
```

</details>

**沿实际写入检查状态**

- `smd_iter.flag &= ~STRIP_MODIFIER_FLAG_ACTIVE;`
- `smd->flag |= STRIP_MODIFIER_FLAG_ACTIVE;`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `BLI_findindex` → [blender::BLI_findindex · L593](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-listbase-2816d9.md#f-cb9036f12bd486b7)。

<a id="f-6f66f3ccf1e06cf2"></a>

### `blender::seq::foreach_strip_modifier_id`

实现位置：[source/blender/sequencer/intern/modifiers/modifier.cc](../../../../../source/blender/sequencer/intern/modifiers/modifier.cc) · L662—L680。

接口参数：

- `Strip *strip`
- `const FunctionRef<void(ID *)> fn`
- `ID *`

**教学注释版**

<!-- annotated:38e0e4c3234ad7 -->

```cpp
void foreach_strip_modifier_id(Strip *strip, const FunctionRef<void(ID *)> fn)
{
  for (StripModifierData &smd : strip->modifiers) {
    if (smd.mask_id) {
      fn(reinterpret_cast<ID *>(smd.mask_id));
    }
    if (smd.type == eSeqModifierType_Compositor) {
      auto *modifier_data = reinterpret_cast<SequencerCompositorModifierData *>(&smd);
      if (modifier_data->node_group) {
        fn(reinterpret_cast<ID *>(modifier_data->node_group));
      }
    }
    if (smd.system_properties) {
      IDP_foreach_property(smd.system_properties, IDP_TYPE_FILTER_ID, [&](IDProperty *id_prop) {
        fn((ID *)id_prop->data.pointer);
      });
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/modifiers/modifier.cc · L662—L680</summary>

<!-- original:38e0e4c3234ad7:source/blender/sequencer/intern/modifiers/modifier.cc:662:680 -->

```cpp
void foreach_strip_modifier_id(Strip *strip, const FunctionRef<void(ID *)> fn)
{
  for (StripModifierData &smd : strip->modifiers) {
    if (smd.mask_id) {
      fn(reinterpret_cast<ID *>(smd.mask_id));
    }
    if (smd.type == eSeqModifierType_Compositor) {
      auto *modifier_data = reinterpret_cast<SequencerCompositorModifierData *>(&smd);
      if (modifier_data->node_group) {
        fn(reinterpret_cast<ID *>(modifier_data->node_group));
      }
    }
    if (smd.system_properties) {
      IDP_foreach_property(smd.system_properties, IDP_TYPE_FILTER_ID, [&](IDProperty *id_prop) {
        fn((ID *)id_prop->data.pointer);
      });
    }
  }
}
```

</details>

**继续追踪实现**

- `fn` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：局部可调用对象，须结合其初始化与捕获环境。调用位置L666。
- `IDP_foreach_property` → [blender::IDP_foreach_property · L1469](%E4%BE%9D%E8%B5%96-idprop-006c65.md#f-63095cdb2dc834a9)。
