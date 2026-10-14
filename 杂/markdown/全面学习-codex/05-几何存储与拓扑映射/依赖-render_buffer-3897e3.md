# 实现依赖专题：intern/cycles/hydra/render_buffer.cpp

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["HdCyclesRenderBuffer::Map"]:::abstraction
  F1["writePixels"]:::compute
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
  F["render_buffer.cpp实现"]:::compute
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

<a id="f-612f36a470bea05f"></a>

### `HdCyclesRenderBuffer::Map`

实现位置：[intern/cycles/hydra/render_buffer.cpp](../../../../../intern/cycles/hydra/render_buffer.cpp) · L70—L84。

**教学注释版**

<!-- annotated:f3838766e9a243 -->

```cpp
void *HdCyclesRenderBuffer::Map()
{
  // Mapping is not implemented when a resource is set
  if (!_resource.IsEmpty()) {
    return nullptr;
  }

  if (_data.size() != _dataSize) {
    _data.resize(_dataSize);
  }

  ++_mapped;

  return _data.data();
}
```

<details>
<summary>核对原始源码：intern/cycles/hydra/render_buffer.cpp · L70—L84</summary>

<!-- original:f3838766e9a243:intern/cycles/hydra/render_buffer.cpp:70:84 -->

```cpp
void *HdCyclesRenderBuffer::Map()
{
  // Mapping is not implemented when a resource is set
  if (!_resource.IsEmpty()) {
    return nullptr;
  }

  if (_data.size() != _dataSize) {
    _data.resize(_dataSize);
  }

  ++_mapped;

  return _data.data();
}
```

</details>

**结果出口**

- `return nullptr;`
- `return _data.data();`

**继续追踪实现**

- `_resource.IsEmpty` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L73。
- `_data.size` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L77。
- `_data.resize` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L78。
- `_data.data` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L83。

<a id="f-5899c2d3287c8046"></a>

### `writePixels`

实现位置：[intern/cycles/hydra/render_buffer.cpp](../../../../../intern/cycles/hydra/render_buffer.cpp) · L160—L181。

接口参数：

- `const SrcT *srcPtr`
- `const GfVec2i &srcSize`
- `const int srcChannelCount`
- `DstT *dstPtr`
- `const GfVec2i &dstSize`
- `const int dstChannelCount`
- `const Convertor &convertor = {}`

**教学注释版**

<!-- annotated:0ace395c795ac1 -->

```cpp
template<typename SrcT, typename DstT, typename Convertor = SimpleConversion>
void writePixels(const SrcT *srcPtr,
                 const GfVec2i &srcSize,
                 const int srcChannelCount,
                 DstT *dstPtr,
                 const GfVec2i &dstSize,
                 const int dstChannelCount,
                 const Convertor &convertor = {})
{
  const auto writeSize = GfVec2i(GfMin(srcSize[0], dstSize[0]), GfMin(srcSize[1], dstSize[1]));
  const auto writeChannelCount = GfMin(srcChannelCount, dstChannelCount);

  for (int y = 0; y < writeSize[1]; ++y) {
    for (int x = 0; x < writeSize[0]; ++x) {
      for (int c = 0; c < writeChannelCount; ++c) {
        dstPtr[x * dstChannelCount + c] = convertor.convert(srcPtr[x * srcChannelCount + c]);
      }
    }
    srcPtr += srcSize[0] * srcChannelCount;
    dstPtr += dstSize[0] * dstChannelCount;
  }
}
```

<details>
<summary>核对原始源码：intern/cycles/hydra/render_buffer.cpp · L160—L181</summary>

<!-- original:0ace395c795ac1:intern/cycles/hydra/render_buffer.cpp:160:181 -->

```cpp
template<typename SrcT, typename DstT, typename Convertor = SimpleConversion>
void writePixels(const SrcT *srcPtr,
                 const GfVec2i &srcSize,
                 const int srcChannelCount,
                 DstT *dstPtr,
                 const GfVec2i &dstSize,
                 const int dstChannelCount,
                 const Convertor &convertor = {})
{
  const auto writeSize = GfVec2i(GfMin(srcSize[0], dstSize[0]), GfMin(srcSize[1], dstSize[1]));
  const auto writeChannelCount = GfMin(srcChannelCount, dstChannelCount);

  for (int y = 0; y < writeSize[1]; ++y) {
    for (int x = 0; x < writeSize[0]; ++x) {
      for (int c = 0; c < writeChannelCount; ++c) {
        dstPtr[x * dstChannelCount + c] = convertor.convert(srcPtr[x * srcChannelCount + c]);
      }
    }
    srcPtr += srcSize[0] * srcChannelCount;
    dstPtr += dstSize[0] * dstChannelCount;
  }
}
```

</details>

**沿实际写入检查状态**

- `srcPtr += srcSize[0] * srcChannelCount;`
- `dstPtr += dstSize[0] * dstChannelCount;`

**继续追踪实现**

- `GfVec2i` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L169。
- `GfMin` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L169。
- `convertor.convert` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L175。
