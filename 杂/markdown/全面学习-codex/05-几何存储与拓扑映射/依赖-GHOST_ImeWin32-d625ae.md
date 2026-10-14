# 实现依赖专题：intern/ghost/intern/GHOST_ImeWin32.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["GHOST_ImeWin32::GetString"]:::abstraction
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
  F["GHOST_ImeWin32.cc实现"]:::compute
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

<a id="f-6c9addf130e5dea1"></a>

### `GHOST_ImeWin32::GetString`

实现位置：[intern/ghost/intern/GHOST_ImeWin32.cc](../../../../../intern/ghost/intern/GHOST_ImeWin32.cc) · L343—L366。

接口参数：

- `HIMC imm_context`
- `WPARAM lparam`
- `int type`
- `ImeComposition *composition`

**教学注释版**

<!-- annotated:00d8647a1baaf4 -->

```cpp
bool GHOST_ImeWin32::GetString(HIMC imm_context,
                               WPARAM lparam,
                               int type,
                               ImeComposition *composition)
{
  bool result = false;
  if (lparam & type) {
    int string_size = ::ImmGetCompositionStringW(imm_context, type, nullptr, 0);
    if (string_size > 0) {
      int string_length = string_size / sizeof(wchar_t);
      wchar_t *string_data = new wchar_t[string_length + 1];
      string_data[string_length] = '\0';
      if (string_data) {
        /* Fill the given ImeComposition object. */
        ::ImmGetCompositionStringW(imm_context, type, string_data, string_size);
        composition->string_type = type;
        composition->ime_string = string_data;
        result = true;
      }
      delete[] string_data;
    }
  }
  return result;
}
```

<details>
<summary>核对原始源码：intern/ghost/intern/GHOST_ImeWin32.cc · L343—L366</summary>

<!-- original:00d8647a1baaf4:intern/ghost/intern/GHOST_ImeWin32.cc:343:366 -->

```cpp
bool GHOST_ImeWin32::GetString(HIMC imm_context,
                               WPARAM lparam,
                               int type,
                               ImeComposition *composition)
{
  bool result = false;
  if (lparam & type) {
    int string_size = ::ImmGetCompositionStringW(imm_context, type, nullptr, 0);
    if (string_size > 0) {
      int string_length = string_size / sizeof(wchar_t);
      wchar_t *string_data = new wchar_t[string_length + 1];
      string_data[string_length] = '\0';
      if (string_data) {
        /* Fill the given ImeComposition object. */
        ::ImmGetCompositionStringW(imm_context, type, string_data, string_size);
        composition->string_type = type;
        composition->ime_string = string_data;
        result = true;
      }
      delete[] string_data;
    }
  }
  return result;
}
```

</details>

**沿实际写入检查状态**

- `string_data[string_length] = '\0';`
- `composition->string_type = type;`
- `composition->ime_string = string_data;`
- `result = true;`

**结果出口**

- `return result;`

**继续追踪实现**

- `::ImmGetCompositionStringW` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L350。
