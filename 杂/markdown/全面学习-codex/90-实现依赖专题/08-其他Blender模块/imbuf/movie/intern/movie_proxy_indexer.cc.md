# 实现依赖专题：source/blender/imbuf/movie/intern/movie_proxy_indexer.cc

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::MOV_close_proxies"]:::abstraction
  F1["blender::MOV_set_custom_proxy_dir"]:::compute
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
  F["movie_proxy_indexer.cc实现"]:::compute
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

<a id="f-e32184b78e7894d6"></a>

### `blender::MOV_close_proxies`

实现位置：[source/blender/imbuf/movie/intern/movie_proxy_indexer.cc](../../../../../../../../../source/blender/imbuf/movie/intern/movie_proxy_indexer.cc) · L892—L906。

接口参数：

- `MovieReader *anim`

**教学注释版**

<!-- annotated:68937c3e7e9426 -->

```cpp
void MOV_close_proxies(MovieReader *anim)
{
  if (anim == nullptr) {
    return;
  }

  for (int i = 0; i < IMB_PROXY_MAX_SLOT; i++) {
    if (anim->proxy_anim[i]) {
      MOV_close(anim->proxy_anim[i]);
      anim->proxy_anim[i] = nullptr;
    }
  }

  anim->proxies_tried = 0;
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/movie/intern/movie_proxy_indexer.cc · L892—L906</summary>

<!-- original:68937c3e7e9426:source/blender/imbuf/movie/intern/movie_proxy_indexer.cc:892:906 -->

```cpp
void MOV_close_proxies(MovieReader *anim)
{
  if (anim == nullptr) {
    return;
  }

  for (int i = 0; i < IMB_PROXY_MAX_SLOT; i++) {
    if (anim->proxy_anim[i]) {
      MOV_close(anim->proxy_anim[i]);
      anim->proxy_anim[i] = nullptr;
    }
  }

  anim->proxies_tried = 0;
}
```

</details>

**沿实际写入检查状态**

- `anim->proxy_anim[i] = nullptr;`
- `anim->proxies_tried = 0;`

**继续追踪实现**

- `MOV_close` → [MOV_close · L70](movie_read.cc.md#f-3180d117d9011594)。

<a id="f-a8ddbc25bdfb6dd4"></a>

### `blender::MOV_set_custom_proxy_dir`

实现位置：[source/blender/imbuf/movie/intern/movie_proxy_indexer.cc](../../../../../../../../../source/blender/imbuf/movie/intern/movie_proxy_indexer.cc) · L908—L916。

接口参数：

- `MovieReader *anim`
- `const char *dir`

**教学注释版**

<!-- annotated:c30f80d1dccd11 -->

```cpp
void MOV_set_custom_proxy_dir(MovieReader *anim, const char *dir)
{
  if (STREQ(anim->proxy_dir, dir)) {
    return;
  }
  STRNCPY(anim->proxy_dir, dir);

  MOV_close_proxies(anim);
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/movie/intern/movie_proxy_indexer.cc · L908—L916</summary>

<!-- original:c30f80d1dccd11:source/blender/imbuf/movie/intern/movie_proxy_indexer.cc:908:916 -->

```cpp
void MOV_set_custom_proxy_dir(MovieReader *anim, const char *dir)
{
  if (STREQ(anim->proxy_dir, dir)) {
    return;
  }
  STRNCPY(anim->proxy_dir, dir);

  MOV_close_proxies(anim);
}
```

</details>

**继续追踪实现**

- `STREQ` → [STREQ · L112](../../../../07-Intern运行时与平台/ghost/intern/GHOST_utildefines.hh.md#m-9549fb6aafd2)；[STREQ · L451](../../../../01-BLI基础库/BLI_utildefines.hh.md#m-c7b745bcfad2)；[STREQ · L55](../../../../07-Intern运行时与平台/clog/clog.cc.md#m-96e78f386894)。宏定义由构建条件选择。
- `STRNCPY` → [blender::STRNCPY · L690](../../../../01-BLI基础库/BLI_string.hh.md#f-6b2d861724026be6)。
- `MOV_close_proxies` → [blender::MOV_close_proxies · L892](movie_proxy_indexer.cc.md#f-e32184b78e7894d6)。
