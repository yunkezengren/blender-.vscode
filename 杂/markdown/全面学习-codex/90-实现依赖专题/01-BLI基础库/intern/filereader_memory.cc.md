# 实现依赖专题：source/blender/blenlib/intern/filereader_memory.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::BLI_filereader_new_memory"]:::abstraction
  F1["blender::BLI_filereader_new_mmap"]:::compute
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
  F["filereader_memory.cc实现"]:::compute
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

<a id="f-4b87a7fee9b758dd"></a>

### `blender::BLI_filereader_new_memory`

实现位置：[source/blender/blenlib/intern/filereader_memory.cc](../../../../../../../source/blender/blenlib/intern/filereader_memory.cc) · L73—L85。

接口参数：

- `const void *data`
- `size_t len`

**教学注释版**

<!-- annotated:1bf45c430a7ef1 -->

```cpp
FileReader *BLI_filereader_new_memory(const void *data, size_t len)
{
  MemoryReader *mem = MEM_new_zeroed<MemoryReader>(__func__);

  mem->data = static_cast<const char *>(data);
  mem->length = len;

  mem->reader.read = memory_read_raw;
  mem->reader.seek = memory_seek;
  mem->reader.close = memory_close_raw;

  return reinterpret_cast<FileReader *>(mem);
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/filereader_memory.cc · L73—L85</summary>

<!-- original:1bf45c430a7ef1:source/blender/blenlib/intern/filereader_memory.cc:73:85 -->

```cpp
FileReader *BLI_filereader_new_memory(const void *data, size_t len)
{
  MemoryReader *mem = MEM_new_zeroed<MemoryReader>(__func__);

  mem->data = static_cast<const char *>(data);
  mem->length = len;

  mem->reader.read = memory_read_raw;
  mem->reader.seek = memory_seek;
  mem->reader.close = memory_close_raw;

  return reinterpret_cast<FileReader *>(mem);
}
```

</details>

**沿实际写入检查状态**

- `mem->data = static_cast<const char *>(data);`
- `mem->length = len;`
- `mem->reader.read = memory_read_raw;`
- `mem->reader.seek = memory_seek;`
- `mem->reader.close = memory_close_raw;`

**结果出口**

- `return reinterpret_cast<FileReader *>(mem);`

**继续追踪实现**

- `MEM_new_zeroed<MemoryReader>` → [MEM_new_zeroed · L550](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-eeb1e2a7f57dd231)；[MEM_new_zeroed · L114](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-e04cf01c64c8b180)。同名重载需按实参类型选择。

<a id="f-8227ddabcb0cb27a"></a>

### `blender::BLI_filereader_new_mmap`

实现位置：[source/blender/blenlib/intern/filereader_memory.cc](../../../../../../../source/blender/blenlib/intern/filereader_memory.cc) · L116—L133。

接口参数：

- `int filedes`

**教学注释版**

<!-- annotated:3150d703b53acd -->

```cpp
FileReader *BLI_filereader_new_mmap(int filedes)
{
  BLI_mmap_file *mmap = BLI_mmap_open(filedes);
  if (mmap == nullptr) {
    return nullptr;
  }

  MemoryReader *mem = MEM_new_zeroed<MemoryReader>(__func__);

  mem->mmap = mmap;
  mem->length = BLI_mmap_get_length(mmap);

  mem->reader.read = memory_read_mmap;
  mem->reader.seek = memory_seek;
  mem->reader.close = memory_close_mmap;

  return reinterpret_cast<FileReader *>(mem);
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/filereader_memory.cc · L116—L133</summary>

<!-- original:3150d703b53acd:source/blender/blenlib/intern/filereader_memory.cc:116:133 -->

```cpp
FileReader *BLI_filereader_new_mmap(int filedes)
{
  BLI_mmap_file *mmap = BLI_mmap_open(filedes);
  if (mmap == nullptr) {
    return nullptr;
  }

  MemoryReader *mem = MEM_new_zeroed<MemoryReader>(__func__);

  mem->mmap = mmap;
  mem->length = BLI_mmap_get_length(mmap);

  mem->reader.read = memory_read_mmap;
  mem->reader.seek = memory_seek;
  mem->reader.close = memory_close_mmap;

  return reinterpret_cast<FileReader *>(mem);
}
```

</details>

**沿实际写入检查状态**

- `mem->mmap = mmap;`
- `mem->length = BLI_mmap_get_length(mmap);`
- `mem->reader.read = memory_read_mmap;`
- `mem->reader.seek = memory_seek;`
- `mem->reader.close = memory_close_mmap;`

**结果出口**

- `return nullptr;`
- `return reinterpret_cast<FileReader *>(mem);`

**继续追踪实现**

- `BLI_mmap_open` → [blender::BLI_mmap_open · L369](BLI_mmap.cc.md#f-a87ee2ea19b3fd5a)。
- `MEM_new_zeroed<MemoryReader>` → [MEM_new_zeroed · L550](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-eeb1e2a7f57dd231)；[MEM_new_zeroed · L114](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-e04cf01c64c8b180)。同名重载需按实参类型选择。
- `BLI_mmap_get_length` → [blender::BLI_mmap_get_length · L484](BLI_mmap.cc.md#f-8c3e5c335f2b2102)。
