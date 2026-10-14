# 实现依赖专题：intern/mikktspace/mikk_atomic_hash_set.hh

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["mikk::AtomicHashSet::tryUpdateCell"]:::abstraction
  F1["mikk::AtomicHashSet::tryUpdateCell"]:::compute
  F2["mikk::AtomicHashSet::emplace"]:::compute
  F3["mikk::AtomicHashSet::keyToAnchorIdx"]:::compute
  F2 -->|"显式调用"| F3
  F2 -->|"显式调用"| F0
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
  F["mikk_atomic_hash_set.hh实现"]:::compute
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

<a id="f-40574e10d93de87a"></a>

### `mikk::AtomicHashSet::tryUpdateCell`

实现位置：[intern/mikktspace/mikk_atomic_hash_set.hh](../../../../../../../intern/mikktspace/mikk_atomic_hash_set.hh) · L130—L138。

接口参数：

- `KeyT *cell`
- `KeyT &existingKey`
- `KeyT newKey`

**教学注释版**

<!-- annotated:a852511390acf6 -->

```cpp
  bool tryUpdateCell(KeyT *cell, KeyT &existingKey, KeyT newKey)
  {
    if (*cell == existingKey) {
      *cell = newKey;
      return true;
    }
    existingKey = *cell;
    return false;
  }
```

<details>
<summary>核对原始源码：intern/mikktspace/mikk_atomic_hash_set.hh · L130—L138</summary>

<!-- original:a852511390acf6:intern/mikktspace/mikk_atomic_hash_set.hh:130:138 -->

```cpp
  bool tryUpdateCell(KeyT *cell, KeyT &existingKey, KeyT newKey)
  {
    if (*cell == existingKey) {
      *cell = newKey;
      return true;
    }
    existingKey = *cell;
    return false;
  }
```

</details>

**沿实际写入检查状态**

- `existingKey = *cell;`

**结果出口**

- `return true;`
- `return false;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-6dfd3e4699759058"></a>

### `mikk::AtomicHashSet::tryUpdateCell`

实现位置：[intern/mikktspace/mikk_atomic_hash_set.hh](../../../../../../../intern/mikktspace/mikk_atomic_hash_set.hh) · L141—L144。

接口参数：

- `std::atomic<KeyT> *cell`
- `KeyT &existingKey`
- `KeyT newKey`

**教学注释版**

<!-- annotated:b6279606910efe -->

```cpp
  bool tryUpdateCell(std::atomic<KeyT> *cell, KeyT &existingKey, KeyT newKey)
  {
    return cell->compare_exchange_strong(existingKey, newKey, std::memory_order_acq_rel);
  }
```

<details>
<summary>核对原始源码：intern/mikktspace/mikk_atomic_hash_set.hh · L141—L144</summary>

<!-- original:b6279606910efe:intern/mikktspace/mikk_atomic_hash_set.hh:141:144 -->

```cpp
  bool tryUpdateCell(std::atomic<KeyT> *cell, KeyT &existingKey, KeyT newKey)
  {
    return cell->compare_exchange_strong(existingKey, newKey, std::memory_order_acq_rel);
  }
```

</details>

**结果出口**

- `return cell->compare_exchange_strong(existingKey, newKey, std::memory_order_acq_rel);`

**继续追踪实现**

- `cell->compare_exchange_strong` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。

<a id="f-094e153771fef601"></a>

### `mikk::AtomicHashSet::emplace`

实现位置：[intern/mikktspace/mikk_atomic_hash_set.hh](../../../../../../../intern/mikktspace/mikk_atomic_hash_set.hh) · L146—L175。

接口参数：

- `KeyT key`

**教学注释版**

<!-- annotated:15d1e1422cd883 -->

```cpp
  std::pair<KeyT, bool> emplace(KeyT key)
  {
    size_t idx = keyToAnchorIdx(key);
    size_t numProbes = 0;
    for (;;) {
      cell_type *cell = &cells_[idx];
      KeyT existingKey = kEmptyKey_;
      /* Try to replace empty cell with our key. */
      if (tryUpdateCell(cell, existingKey, key)) {
        /* Cell was empty, we're done. */
        return std::make_pair(key, true);
      }

      /* Cell was not empty, check if the existing key is equal. */
      if (equalityChecker_(existingKey, key)) {
        /* Found equal element, we're done. */
        return std::make_pair(existingKey, false);
      }

      /* Continue to next cell according to probe strategy. */
      ++numProbes;
      if (UNLIKELY(numProbes >= capacity_)) {
        // probed every cell...fail
        // [讲解] assert：检查开发者预期条件，配置可能关闭；不承担完整输入处理或自动修复。
        assert(false);
        return std::make_pair(kEmptyKey_, false);
      }

      idx = ProbeFcn()(idx, numProbes, capacity_);
    }
  }
```

<details>
<summary>核对原始源码：intern/mikktspace/mikk_atomic_hash_set.hh · L146—L175</summary>

<!-- original:15d1e1422cd883:intern/mikktspace/mikk_atomic_hash_set.hh:146:175 -->

```cpp
  std::pair<KeyT, bool> emplace(KeyT key)
  {
    size_t idx = keyToAnchorIdx(key);
    size_t numProbes = 0;
    for (;;) {
      cell_type *cell = &cells_[idx];
      KeyT existingKey = kEmptyKey_;
      /* Try to replace empty cell with our key. */
      if (tryUpdateCell(cell, existingKey, key)) {
        /* Cell was empty, we're done. */
        return std::make_pair(key, true);
      }

      /* Cell was not empty, check if the existing key is equal. */
      if (equalityChecker_(existingKey, key)) {
        /* Found equal element, we're done. */
        return std::make_pair(existingKey, false);
      }

      /* Continue to next cell according to probe strategy. */
      ++numProbes;
      if (UNLIKELY(numProbes >= capacity_)) {
        // probed every cell...fail
        assert(false);
        return std::make_pair(kEmptyKey_, false);
      }

      idx = ProbeFcn()(idx, numProbes, capacity_);
    }
  }
```

</details>

**沿实际写入检查状态**

- `idx = ProbeFcn()(idx, numProbes, capacity_);`

**结果出口**

- `return std::make_pair(key, true);`
- `return std::make_pair(existingKey, false);`
- `return std::make_pair(kEmptyKey_, false);`

**继续追踪实现**

- `keyToAnchorIdx` → [mikk::AtomicHashSet::keyToAnchorIdx · L178](mikk_atomic_hash_set.hh.md#f-9b50abfc277a9310)。
- `tryUpdateCell` → [mikk::AtomicHashSet::tryUpdateCell · L130](mikk_atomic_hash_set.hh.md#f-40574e10d93de87a)；[mikk::AtomicHashSet::tryUpdateCell · L141](mikk_atomic_hash_set.hh.md#f-6dfd3e4699759058)。同名重载需按实参类型选择。
- `std::make_pair` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `equalityChecker_` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L160。
- `UNLIKELY` → [UNLIKELY · L52](../guardedalloc/intern/mallocn_intern.hh.md#m-b66d81651173)；[UNLIKELY · L55](../guardedalloc/intern/mallocn_intern.hh.md#m-43069123e9fe)；[UNLIKELY · L108](../cycles/util/defines.h.md#m-c50729f638e8)；[UNLIKELY · L111](../cycles/util/defines.h.md#m-08e633831622)；[UNLIKELY · L25](../../01-BLI基础库/intern/math_base_inline.cc.md#m-beab6e34c61e)；[UNLIKELY · L27](../../01-BLI基础库/intern/math_base_inline.cc.md#m-9b279ffdd95b)；[UNLIKELY · L544](../../01-BLI基础库/BLI_utildefines.hh.md#m-74644b8209a0)；[UNLIKELY · L547](../../01-BLI基础库/BLI_utildefines.hh.md#m-3a47ebab6298)。宏定义由构建条件选择。
- `assert` → [外部契约](https://eel.is/c++draft/assertions)：检查开发者预期条件，配置可能关闭；不承担完整输入处理或自动修复。
- `ProbeFcn()` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L173。
- `ProbeFcn` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L173。

<a id="f-9b50abfc277a9310"></a>

### `mikk::AtomicHashSet::keyToAnchorIdx`

实现位置：[intern/mikktspace/mikk_atomic_hash_set.hh](../../../../../../../intern/mikktspace/mikk_atomic_hash_set.hh) · L178—L183。

接口参数：

- `const KeyT k`

**教学注释版**

<!-- annotated:a898c3a400528e -->

```cpp
  size_t keyToAnchorIdx(const KeyT k) const
  {
    const size_t hashVal = hasher_(k);
    const size_t probe = hashVal & kAnchorMask_;
    return LIKELY(probe < capacity_) ? probe : hashVal % capacity_;
  }
```

<details>
<summary>核对原始源码：intern/mikktspace/mikk_atomic_hash_set.hh · L178—L183</summary>

<!-- original:a898c3a400528e:intern/mikktspace/mikk_atomic_hash_set.hh:178:183 -->

```cpp
  size_t keyToAnchorIdx(const KeyT k) const
  {
    const size_t hashVal = hasher_(k);
    const size_t probe = hashVal & kAnchorMask_;
    return LIKELY(probe < capacity_) ? probe : hashVal % capacity_;
  }
```

</details>

**结果出口**

- `return LIKELY(probe < capacity_) ? probe : hashVal % capacity_;`

**继续追踪实现**

- `hasher_` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L180。
- `LIKELY` → [LIKELY · L51](../guardedalloc/intern/mallocn_intern.hh.md#m-53ea5e2ff73b)；[LIKELY · L54](../guardedalloc/intern/mallocn_intern.hh.md#m-bb82bdeee493)；[LIKELY · L107](../cycles/util/defines.h.md#m-bd6166173f61)；[LIKELY · L110](../cycles/util/defines.h.md#m-2c2ad9a348a5)；[LIKELY · L543](../../01-BLI基础库/BLI_utildefines.hh.md#m-eeacc3e1dee8)；[LIKELY · L546](../../01-BLI基础库/BLI_utildefines.hh.md#m-26b4114d7b77)。宏定义由构建条件选择。
