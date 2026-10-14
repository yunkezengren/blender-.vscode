# 实现依赖专题：source/blender/bmesh/intern/bmesh_marking.hh

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  S["bmesh_marking.hh"]:::abstraction
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
  F["bmesh_marking.hh实现"]:::compute
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

<a id="m-a2f5e4b7b380"></a>

## 宏 `BM_select_history_remove`

<!-- annotated:0cfc2d908af5c4 -->

```cpp
#define BM_select_history_remove(bm, ele) _bm_select_history_remove(bm, &(ele)->head)
#define BM_select_history_store_notest(bm, ele) _bm_select_history_store_notest(bm, &(ele)->head)
```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_marking.hh · L178—L179</summary>

<!-- original:0cfc2d908af5c4:source/blender/bmesh/intern/bmesh_marking.hh:178:179 -->

```cpp
#define BM_select_history_remove(bm, ele) _bm_select_history_remove(bm, &(ele)->head)
#define BM_select_history_store_notest(bm, ele) _bm_select_history_store_notest(bm, &(ele)->head)
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-d2d3015c5864"></a>

## 宏 `BM_select_history_store_notest`

<!-- annotated:380a6618a30ceb -->

```cpp
#define BM_select_history_store_notest(bm, ele) _bm_select_history_store_notest(bm, &(ele)->head)
#define BM_select_history_store(bm, ele) _bm_select_history_store(bm, &(ele)->head)
```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_marking.hh · L179—L180</summary>

<!-- original:380a6618a30ceb:source/blender/bmesh/intern/bmesh_marking.hh:179:180 -->

```cpp
#define BM_select_history_store_notest(bm, ele) _bm_select_history_store_notest(bm, &(ele)->head)
#define BM_select_history_store(bm, ele) _bm_select_history_store(bm, &(ele)->head)
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

<a id="m-e79eb8084035"></a>

## 宏 `BM_select_history_store_after_notest`

<!-- annotated:f905d07702eddc -->

```cpp
#define BM_select_history_store_after_notest(bm, ese_ref, ele) \
  _bm_select_history_store_after_notest(bm, ese_ref, &(ele)->head)
#define BM_select_history_store_after(bm, ese, ese_ref) \
```

<details>
<summary>核对原始源码：source/blender/bmesh/intern/bmesh_marking.hh · L184—L186</summary>

<!-- original:f905d07702eddc:source/blender/bmesh/intern/bmesh_marking.hh:184:186 -->

```cpp
#define BM_select_history_store_after_notest(bm, ese_ref, ele) \
  _bm_select_history_store_after_notest(bm, ese_ref, &(ele)->head)
#define BM_select_history_store_after(bm, ese, ese_ref) \
```

</details>

宏在预处理阶段展开，参数替换、重复求值和条件编译应直接从该定义检查。与普通函数不同，宏不会自动提供参数类型检查；构建配置选择哪个定义需结合外围条件。

## 完整成员与函数实现
