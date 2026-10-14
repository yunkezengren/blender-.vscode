# 实现依赖专题：source/blender/blenloader/intern/undofile.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::BLO_memfile_chunk_add"]:::abstraction
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
  F["undofile.cc实现"]:::compute
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

<a id="f-69214f2a3cf341ed"></a>

### `blender::BLO_memfile_chunk_add`

实现位置：[source/blender/blenloader/intern/undofile.cc](../../../../../../../../source/blender/blenloader/intern/undofile.cc) · L135—L171。

接口参数：

- `MemFileWriteData *mem_data`
- `const char *buf`
- `size_t size`

**教学注释版**

<!-- annotated:ade6c0f26bb553 -->

```cpp
void BLO_memfile_chunk_add(MemFileWriteData *mem_data, const char *buf, size_t size)
{
  MemFile *memfile = mem_data->written_memfile;
  MemFileChunk **compchunk_step = &mem_data->reference_current_chunk;

  MemFileChunk *curchunk = MEM_new_uninitialized<MemFileChunk>("MemFileChunk");
  curchunk->size = size;
  curchunk->buf = nullptr;
  curchunk->is_identical = false;
  /* This is unsafe in the sense that an app handler or other code that does not
   * perform an undo push may make changes after the last undo push that
   * will then not be undo. Though it's not entirely clear that is wrong behavior. */
  curchunk->is_identical_future = true;
  curchunk->id_session_uid = mem_data->current_id_session_uid;
  BLI_addtail(&memfile->chunks, curchunk);

  /* we compare compchunk with buf */
  if (*compchunk_step != nullptr) {
    MemFileChunk *compchunk = *compchunk_step;
    if (compchunk->size == curchunk->size) {
      if (memcmp(compchunk->buf, buf, size) == 0) {
        curchunk->buf = compchunk->buf;
        curchunk->is_identical = true;
        compchunk->is_identical_future = true;
      }
    }
    *compchunk_step = static_cast<MemFileChunk *>(compchunk->next);
  }

  /* not equal... */
  if (curchunk->buf == nullptr) {
    char *buf_new = MEM_new_array_uninitialized<char>(size, "Chunk buffer");
    // [讲解] memcpy：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
    memcpy(buf_new, buf, size);
    curchunk->buf = buf_new;
    memfile->size += size;
  }
}
```

<details>
<summary>核对原始源码：source/blender/blenloader/intern/undofile.cc · L135—L171</summary>

<!-- original:ade6c0f26bb553:source/blender/blenloader/intern/undofile.cc:135:171 -->

```cpp
void BLO_memfile_chunk_add(MemFileWriteData *mem_data, const char *buf, size_t size)
{
  MemFile *memfile = mem_data->written_memfile;
  MemFileChunk **compchunk_step = &mem_data->reference_current_chunk;

  MemFileChunk *curchunk = MEM_new_uninitialized<MemFileChunk>("MemFileChunk");
  curchunk->size = size;
  curchunk->buf = nullptr;
  curchunk->is_identical = false;
  /* This is unsafe in the sense that an app handler or other code that does not
   * perform an undo push may make changes after the last undo push that
   * will then not be undo. Though it's not entirely clear that is wrong behavior. */
  curchunk->is_identical_future = true;
  curchunk->id_session_uid = mem_data->current_id_session_uid;
  BLI_addtail(&memfile->chunks, curchunk);

  /* we compare compchunk with buf */
  if (*compchunk_step != nullptr) {
    MemFileChunk *compchunk = *compchunk_step;
    if (compchunk->size == curchunk->size) {
      if (memcmp(compchunk->buf, buf, size) == 0) {
        curchunk->buf = compchunk->buf;
        curchunk->is_identical = true;
        compchunk->is_identical_future = true;
      }
    }
    *compchunk_step = static_cast<MemFileChunk *>(compchunk->next);
  }

  /* not equal... */
  if (curchunk->buf == nullptr) {
    char *buf_new = MEM_new_array_uninitialized<char>(size, "Chunk buffer");
    memcpy(buf_new, buf, size);
    curchunk->buf = buf_new;
    memfile->size += size;
  }
}
```

</details>

**沿实际写入检查状态**

- `curchunk->size = size;`
- `curchunk->buf = nullptr;`
- `curchunk->is_identical = false;`
- `curchunk->is_identical_future = true;`
- `curchunk->id_session_uid = mem_data->current_id_session_uid;`
- `curchunk->buf = compchunk->buf;`
- `curchunk->is_identical = true;`
- `compchunk->is_identical_future = true;`
- `curchunk->buf = buf_new;`
- `memfile->size += size;`

**继续追踪实现**

- `MEM_new_uninitialized<MemFileChunk>` → [MEM_new_uninitialized · L590](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-c773b2e5b8fe70e4)；[MEM_new_uninitialized · L124](../../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-28a7e00a1e67f699)。同名重载需按实参类型选择。
- `BLI_addtail` → [blender::BLI_addtail · L118](../../../01-BLI基础库/intern/listbase.cc.md#f-4fb027713fa3115b)。
- `memcmp` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `MEM_new_array_uninitialized<char>` → [MEM_new_array_uninitialized · L608](../../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-b7103eae8eb57b05)；[MEM_new_array_uninitialized · L129](../../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-bf6ef4ddcfb6e5df)。同名重载需按实参类型选择。
- `memcpy` → [外部契约](https://eel.is/c++draft/cstring.syn)：复制字节，源与目标不应重叠。类型生命周期、对齐和可复制表示须由调用者证明，不是任意对象的复制构造。
