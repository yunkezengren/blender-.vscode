# 实现依赖专题：source/blender/io/alembic/intern/abc_util.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::io::alembic::has_property"]:::abstraction
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
  F["abc_util.cc实现"]:::compute
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

<a id="f-cd9ad83a000b4b68"></a>

### `blender::io::alembic::has_property`

实现位置：[source/blender/io/alembic/intern/abc_util.cc](../../../../../source/blender/io/alembic/intern/abc_util.cc) · L77—L84。

接口参数：

- `const Alembic::Abc::ICompoundProperty &prop`
- `const std::string &name`

**教学注释版**

<!-- annotated:daa7e9cbe9f8a8 -->

```cpp
bool has_property(const Alembic::Abc::ICompoundProperty &prop, const std::string &name)
{
  if (!prop.valid()) {
    return false;
  }

  return prop.getPropertyHeader(name) != nullptr;
}
```

<details>
<summary>核对原始源码：source/blender/io/alembic/intern/abc_util.cc · L77—L84</summary>

<!-- original:daa7e9cbe9f8a8:source/blender/io/alembic/intern/abc_util.cc:77:84 -->

```cpp
bool has_property(const Alembic::Abc::ICompoundProperty &prop, const std::string &name)
{
  if (!prop.valid()) {
    return false;
  }

  return prop.getPropertyHeader(name) != nullptr;
}
```

</details>

**结果出口**

- `return false;`
- `return prop.getPropertyHeader(name) != nullptr;`

**继续追踪实现**

- `prop.valid` → [blender::io::alembic::AbcEmptyReader::valid · L34](%E4%BE%9D%E8%B5%96-abc_reader_transform-638c62.md#f-def716ba47aa8d38)；[blender::io::alembic::AbcPointsReader::valid · L64](%E4%BE%9D%E8%B5%96-abc_reader_points-9119bc.md#f-a63a60abd9d03476)；[blender::io::alembic::AbcNurbsReader::valid · L48](%E4%BE%9D%E8%B5%96-abc_reader_nurbs-d4825c.md#f-8f37fa0da06368eb)；[blender::io::alembic::AbcMeshReader::valid · L690](%E4%BE%9D%E8%B5%96-abc_reader_mesh-83c0a1.md#f-dd4fd62253b2751e)；[blender::io::alembic::AbcSubDReader::valid · L1110](%E4%BE%9D%E8%B5%96-abc_reader_mesh-83c0a1.md#f-00028e83487abdfe)；[blender::io::alembic::AbcCurveReader::valid · L424](%E4%BE%9D%E8%B5%96-abc_reader_curves-624d7e.md#f-8747d68e018b0a07)；[blender::io::alembic::AbcCameraReader::valid · L46](%E4%BE%9D%E8%B5%96-abc_reader_camera-973db2.md#f-9e83093bf7d0ba7b)；[blender::io::alembic::ArchiveReader::valid · L141](%E4%BE%9D%E8%B5%96-abc_reader_archive-9b15d1.md#f-ddd763b3a0b67620)。同名重载需按实参类型选择。
- `prop.getPropertyHeader` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：由接收对象具体类型或运行时策略提供实现。调用位置L83。
