# 实现依赖专题：source/blender/blenlib/intern/filereader_gzip.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::BLI_filereader_new_gzip"]:::abstraction
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
  F["filereader_gzip.cc实现"]:::compute
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

<a id="f-442cd4abbcd382f5"></a>

### `blender::BLI_filereader_new_gzip`

实现位置：[source/blender/blenlib/intern/filereader_gzip.cc](../../../../../../../source/blender/blenlib/intern/filereader_gzip.cc) · L77—L95。

接口参数：

- `FileReader *base`

**教学注释版**

<!-- annotated:0444c9b2c00a2e -->

```cpp
FileReader *BLI_filereader_new_gzip(FileReader *base)
{
  GzipReader *gzip = MEM_new_zeroed<GzipReader>(__func__);
  gzip->base = base;

  if (inflateInit2(&gzip->strm, 16 + MAX_WBITS) != Z_OK) {
    MEM_delete(gzip);
    return nullptr;
  }

  gzip->in_size = 256 * 2014;
  gzip->in_buf = MEM_new_array_uninitialized<Bytef>(gzip->in_size, "gzip in buf");

  gzip->reader.read = gzip_read;
  gzip->reader.seek = nullptr;
  gzip->reader.close = gzip_close;

  return reinterpret_cast<FileReader *>(gzip);
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/filereader_gzip.cc · L77—L95</summary>

<!-- original:0444c9b2c00a2e:source/blender/blenlib/intern/filereader_gzip.cc:77:95 -->

```cpp
FileReader *BLI_filereader_new_gzip(FileReader *base)
{
  GzipReader *gzip = MEM_new_zeroed<GzipReader>(__func__);
  gzip->base = base;

  if (inflateInit2(&gzip->strm, 16 + MAX_WBITS) != Z_OK) {
    MEM_delete(gzip);
    return nullptr;
  }

  gzip->in_size = 256 * 2014;
  gzip->in_buf = MEM_new_array_uninitialized<Bytef>(gzip->in_size, "gzip in buf");

  gzip->reader.read = gzip_read;
  gzip->reader.seek = nullptr;
  gzip->reader.close = gzip_close;

  return reinterpret_cast<FileReader *>(gzip);
}
```

</details>

**沿实际写入检查状态**

- `gzip->base = base;`
- `gzip->in_size = 256 * 2014;`
- `gzip->in_buf = MEM_new_array_uninitialized<Bytef>(gzip->in_size, "gzip in buf");`
- `gzip->reader.read = gzip_read;`
- `gzip->reader.seek = nullptr;`
- `gzip->reader.close = gzip_close;`

**结果出口**

- `return nullptr;`
- `return reinterpret_cast<FileReader *>(gzip);`

**继续追踪实现**

- `MEM_new_zeroed<GzipReader>` → [MEM_new_zeroed · L550](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-eeb1e2a7f57dd231)；[MEM_new_zeroed · L114](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-e04cf01c64c8b180)。同名重载需按实参类型选择。
- `inflateInit2` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L82。
- `MEM_delete` → [MEM_delete · L400](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
- `MEM_new_array_uninitialized<Bytef>` → [MEM_new_array_uninitialized · L608](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-b7103eae8eb57b05)；[MEM_new_array_uninitialized · L129](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-bf6ef4ddcfb6e5df)。同名重载需按实参类型选择。
