# 实现依赖专题：source/blender/sequencer/intern/cache/final_image_cache.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::seq::query_final_image_cache"]:::abstraction
  F1["blender::seq::final_image_cache_invalidate_frame_range"]:::compute
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
  F["final_image_cache.cc实现"]:::compute
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

<a id="t-88289eb9b31b"></a>

### `blender::seq::FinalImageCache::Key`

原始声明：[source/blender/sequencer/intern/cache/final_image_cache.cc](../../../../../source/blender/sequencer/intern/cache/final_image_cache.cc) · L31—L47。

成员布局：

- `int timeline_frame`
- `int view_id`
- `int display_channel`
- `int2 image_size`

以下保留类的数据声明与编译条件，成员函数实现通过后面的精确链接阅读。

<!-- annotated:f96cc191c5eed8 -->

```cpp
  struct Key {
    int timeline_frame;
    int view_id;
    int display_channel;
    int2 image_size;

```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/cache/final_image_cache.cc · L31—L36</summary>

<!-- original:f96cc191c5eed8:source/blender/sequencer/intern/cache/final_image_cache.cc:31:36 -->

```cpp
  struct Key {
    int timeline_frame;
    int view_id;
    int display_channel;
    int2 image_size;

```

</details>

<!-- annotated:fdc43a5c45d525 -->

```cpp

```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/cache/final_image_cache.cc · L41—L41</summary>

<!-- original:fdc43a5c45d525:source/blender/sequencer/intern/cache/final_image_cache.cc:41:41 -->

```cpp

```

</details>

<!-- annotated:14fc2e8e088ed0 -->

```cpp
  };
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/cache/final_image_cache.cc · L47—L47</summary>

<!-- original:14fc2e8e088ed0:source/blender/sequencer/intern/cache/final_image_cache.cc:47:47 -->

```cpp
  };
```

</details>


## 完整成员与函数实现

<a id="f-4fe8908dfc47d28e"></a>

### `blender::seq::query_final_image_cache`

实现位置：[source/blender/sequencer/intern/cache/final_image_cache.cc](../../../../../source/blender/sequencer/intern/cache/final_image_cache.cc) · L73—L79。

接口参数：

- `const Scene *scene`

**教学注释版**

<!-- annotated:e39d4baefa8ef9 -->

```cpp
static FinalImageCache *query_final_image_cache(const Scene *scene)
{
  if (scene == nullptr || scene->ed == nullptr) {
    return nullptr;
  }
  return scene->ed->runtime->final_image_cache;
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/cache/final_image_cache.cc · L73—L79</summary>

<!-- original:e39d4baefa8ef9:source/blender/sequencer/intern/cache/final_image_cache.cc:73:79 -->

```cpp
static FinalImageCache *query_final_image_cache(const Scene *scene)
{
  if (scene == nullptr || scene->ed == nullptr) {
    return nullptr;
  }
  return scene->ed->runtime->final_image_cache;
}
```

</details>

**结果出口**

- `return nullptr;`
- `return scene->ed->runtime->final_image_cache;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-25616fff0796700e"></a>

### `blender::seq::final_image_cache_invalidate_frame_range`

实现位置：[source/blender/sequencer/intern/cache/final_image_cache.cc](../../../../../source/blender/sequencer/intern/cache/final_image_cache.cc) · L142—L162。

接口参数：

- `Scene *scene`
- `const float timeline_frame_start`
- `const float timeline_frame_end`

**教学注释版**

<!-- annotated:84cfd01bc37130 -->

```cpp
void final_image_cache_invalidate_frame_range(Scene *scene,
                                              const float timeline_frame_start,
                                              const float timeline_frame_end)
{
  std::lock_guard lock(final_image_cache_mutex);
  FinalImageCache *cache = query_final_image_cache(scene);
  if (cache == nullptr) {
    return;
  }

  const int key_start = int(math::floor(timeline_frame_start));
  const int key_end = int(math::ceil(timeline_frame_end));

  for (auto it = cache->map_.items().begin(); it != cache->map_.items().end(); it++) {
    const int key = (*it).key.timeline_frame;
    if (key >= key_start && key <= key_end) {
      IMB_freeImBuf((*it).value);
      cache->map_.remove(it);
    }
  }
}
```

<details>
<summary>核对原始源码：source/blender/sequencer/intern/cache/final_image_cache.cc · L142—L162</summary>

<!-- original:84cfd01bc37130:source/blender/sequencer/intern/cache/final_image_cache.cc:142:162 -->

```cpp
void final_image_cache_invalidate_frame_range(Scene *scene,
                                              const float timeline_frame_start,
                                              const float timeline_frame_end)
{
  std::lock_guard lock(final_image_cache_mutex);
  FinalImageCache *cache = query_final_image_cache(scene);
  if (cache == nullptr) {
    return;
  }

  const int key_start = int(math::floor(timeline_frame_start));
  const int key_end = int(math::ceil(timeline_frame_end));

  for (auto it = cache->map_.items().begin(); it != cache->map_.items().end(); it++) {
    const int key = (*it).key.timeline_frame;
    if (key >= key_start && key <= key_end) {
      IMB_freeImBuf((*it).value);
      cache->map_.remove(it);
    }
  }
}
```

</details>

**继续追踪实现**

- `query_final_image_cache` → [blender::seq::query_final_image_cache · L73](%E4%BE%9D%E8%B5%96-final_image_cache-1c7855.md#f-4fe8908dfc47d28e)。
- `math::floor` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `math::ceil` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `cache->map_.items().begin` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L155。
- `cache->map_.items` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L155。
- `cache->map_.items().end` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L155。
- `IMB_freeImBuf` → [blender::IMB_freeImBuf · L144](%E4%BE%9D%E8%B5%96-allocimbuf-bc68dd.md#f-c830f56ede6f345b)。
- `cache->map_.remove` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L159。
