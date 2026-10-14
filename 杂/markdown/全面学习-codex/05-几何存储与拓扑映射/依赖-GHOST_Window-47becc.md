# 实现依赖专题：intern/ghost/intern/GHOST_Window.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["GHOST_Window::getNativePixelSize"]:::abstraction
  F1["GHOST_Window::getCursorVisibility"]:::compute
  F2["GHOST_Window::getCursorShape"]:::compute
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
  F["GHOST_Window.hh实现"]:::compute
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

<a id="f-2e3e47958eb26427"></a>

### `GHOST_Window::getNativePixelSize`

实现位置：[intern/ghost/intern/GHOST_Window.hh](../../../../../intern/ghost/intern/GHOST_Window.hh) · L230—L236。

**教学注释版**

<!-- annotated:bfd82b09544c63 -->

```cpp
  float getNativePixelSize() override
  {
    if (native_pixel_size_ > 0.0f) {
      return native_pixel_size_;
    }
    return 1.0f;
  }
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_Window.hh · L230—L236</summary>

<!-- original:bfd82b09544c63:intern/ghost/intern/GHOST_Window.hh:230:236 -->

```cpp
  float getNativePixelSize() override
  {
    if (native_pixel_size_ > 0.0f) {
      return native_pixel_size_;
    }
    return 1.0f;
  }
```

</details>

**结果出口**

- `return native_pixel_size_;`
- `return 1.0f;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-06d7c551f0b47223"></a>

### `GHOST_Window::getCursorVisibility`

实现位置：[intern/ghost/intern/GHOST_Window.hh](../../../../../intern/ghost/intern/GHOST_Window.hh) · L398—L401。

**教学注释版**

<!-- annotated:14459610c8514e -->

```cpp
inline bool GHOST_Window::getCursorVisibility() const
{
  return cursor_visible_;
}
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_Window.hh · L398—L401</summary>

<!-- original:14459610c8514e:intern/ghost/intern/GHOST_Window.hh:398:401 -->

```cpp
inline bool GHOST_Window::getCursorVisibility() const
{
  return cursor_visible_;
}
```

</details>

**结果出口**

- `return cursor_visible_;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。

<a id="f-b36ec0d0be63c6a4"></a>

### `GHOST_Window::getCursorShape`

实现位置：[intern/ghost/intern/GHOST_Window.hh](../../../../../intern/ghost/intern/GHOST_Window.hh) · L436—L439。

**教学注释版**

<!-- annotated:cdc3d052fe5aa2 -->

```cpp
inline GHOST_TStandardCursor GHOST_Window::getCursorShape() const
{
  return cursor_shape_;
}
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_Window.hh · L436—L439</summary>

<!-- original:cdc3d052fe5aa2:intern/ghost/intern/GHOST_Window.hh:436:439 -->

```cpp
inline GHOST_TStandardCursor GHOST_Window::getCursorShape() const
{
  return cursor_shape_;
}
```

</details>

**结果出口**

- `return cursor_shape_;`

**继续追踪实现**

本实现没有需要继续展开的显式调用；检查返回表达式、对象转换和调用者前置条件。
