# 实现依赖专题：source/blender/blenlib/intern/filereader_zstd.cc

[实现依赖导航](../../README.md) · [符号索引](../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::zstd_read_u32"]:::abstraction
  F1["blender::zstd_read_seek_table"]:::compute
  F2["blender::BLI_filereader_new_zstd"]:::compute
  F1 -->|"显式调用"| F0
  F2 -->|"显式调用"| F1
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
  F["filereader_zstd.cc实现"]:::compute
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

<a id="f-1deb478138ea6c19"></a>

### `blender::zstd_read_u32`

实现位置：[source/blender/blenlib/intern/filereader_zstd.cc](../../../../../../../source/blender/blenlib/intern/filereader_zstd.cc) · L39—L47。

接口参数：

- `FileReader *base`
- `uint32_t *val`

**教学注释版**

<!-- annotated:faf716a5a1aeb2 -->

```cpp
static bool zstd_read_u32(FileReader *base, uint32_t *val)
{
  if (base->read(base, val, sizeof(uint32_t)) != sizeof(uint32_t)) {
    return false;
  }
  /* NOTE: this is endianness-sensitive.
   * `val` would need to be switched on a big endian system. */
  return true;
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/filereader_zstd.cc · L39—L47</summary>

<!-- original:faf716a5a1aeb2:source/blender/blenlib/intern/filereader_zstd.cc:39:47 -->

```cpp
static bool zstd_read_u32(FileReader *base, uint32_t *val)
{
  if (base->read(base, val, sizeof(uint32_t)) != sizeof(uint32_t)) {
    return false;
  }
  /* NOTE: this is endianness-sensitive.
   * `val` would need to be switched on a big endian system. */
  return true;
}
```

</details>

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `base->read` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：由接收对象具体类型或运行时策略提供实现。调用位置L41。

<a id="f-ce297e1b3f4c2089"></a>

### `blender::zstd_read_seek_table`

实现位置：[source/blender/blenlib/intern/filereader_zstd.cc](../../../../../../../source/blender/blenlib/intern/filereader_zstd.cc) · L49—L133。

接口参数：

- `ZstdReader *zstd`

**教学注释版**

<!-- annotated:7295d691319b06 -->

```cpp
static bool zstd_read_seek_table(ZstdReader *zstd)
{
  FileReader *base = zstd->base;

  /* The seek table frame is at the end of the file, so seek there
   * and verify that there is enough data. */
  if (base->seek(base, -4, SEEK_END) < 13) {
    return false;
  }
  uint32_t magic;
  if (!zstd_read_u32(base, &magic) || magic != 0x8F92EAB1) {
    return false;
  }

  uint8_t flags;
  if (base->seek(base, -5, SEEK_END) < 0 || base->read(base, &flags, 1) != 1) {
    return false;
  }
  /* Bit 7 indicates check-sums. Bits 5 and 6 must be zero. */
  bool has_checksums = (flags & 0x80);
  if (flags & 0x60) {
    return false;
  }

  uint32_t frames_num;
  if (base->seek(base, -9, SEEK_END) < 0 || !zstd_read_u32(base, &frames_num)) {
    return false;
  }

  /* Each frame has either 2 or 3 uint32_t, and after that we have
   * frames_num, flags and magic for another 9 bytes. */
  uint32_t expected_frame_length = frames_num * (has_checksums ? 12 : 8) + 9;
  /* The frame starts with another magic number and its length, but these
   * two fields are not included when counting length. */
  off64_t frame_start_ofs = 8 + expected_frame_length;
  /* Sanity check: Before the start of the seek table frame,
   * there must be frames_num frames, each of which at least 8 bytes long. */
  off64_t seek_frame_start = base->seek(base, -frame_start_ofs, SEEK_END);
  if (seek_frame_start < frames_num * 8) {
    return false;
  }

  if (!zstd_read_u32(base, &magic) || magic != 0x184D2A5E) {
    return false;
  }

  uint32_t frame_length;
  if (!zstd_read_u32(base, &frame_length) || frame_length != expected_frame_length) {
    return false;
  }

  zstd->seek.frames_num = frames_num;
  zstd->seek.compressed_ofs = MEM_new_array_uninitialized<size_t>(frames_num + 1, __func__);
  zstd->seek.uncompressed_ofs = MEM_new_array_uninitialized<size_t>(frames_num + 1, __func__);

  size_t compressed_ofs = 0;
  size_t uncompressed_ofs = 0;
  for (int i = 0; i < frames_num; i++) {
    uint32_t compressed_size, uncompressed_size;
    if (!zstd_read_u32(base, &compressed_size) || !zstd_read_u32(base, &uncompressed_size)) {
      break;
    }
    if (has_checksums && base->seek(base, 4, SEEK_CUR) < 0) {
      break;
    }
    zstd->seek.compressed_ofs[i] = compressed_ofs;
    zstd->seek.uncompressed_ofs[i] = uncompressed_ofs;
    compressed_ofs += compressed_size;
    uncompressed_ofs += uncompressed_size;
  }
  zstd->seek.compressed_ofs[frames_num] = compressed_ofs;
  zstd->seek.uncompressed_ofs[frames_num] = uncompressed_ofs;

  /* Seek to the end of the previous frame for the following #BHead frame detection. */
  if (seek_frame_start != compressed_ofs || base->seek(base, seek_frame_start, SEEK_SET) < 0) {
    MEM_delete(zstd->seek.compressed_ofs);
    MEM_delete(zstd->seek.uncompressed_ofs);
    // [讲解] memset：填充字节，不调用T构造函数，也不保证任意类型的全零表示是合法或期望值。
    memset(&zstd->seek, 0, sizeof(zstd->seek));
    return false;
  }

  zstd->seek.cached_frame = -1;

  return true;
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/filereader_zstd.cc · L49—L133</summary>

<!-- original:7295d691319b06:source/blender/blenlib/intern/filereader_zstd.cc:49:133 -->

```cpp
static bool zstd_read_seek_table(ZstdReader *zstd)
{
  FileReader *base = zstd->base;

  /* The seek table frame is at the end of the file, so seek there
   * and verify that there is enough data. */
  if (base->seek(base, -4, SEEK_END) < 13) {
    return false;
  }
  uint32_t magic;
  if (!zstd_read_u32(base, &magic) || magic != 0x8F92EAB1) {
    return false;
  }

  uint8_t flags;
  if (base->seek(base, -5, SEEK_END) < 0 || base->read(base, &flags, 1) != 1) {
    return false;
  }
  /* Bit 7 indicates check-sums. Bits 5 and 6 must be zero. */
  bool has_checksums = (flags & 0x80);
  if (flags & 0x60) {
    return false;
  }

  uint32_t frames_num;
  if (base->seek(base, -9, SEEK_END) < 0 || !zstd_read_u32(base, &frames_num)) {
    return false;
  }

  /* Each frame has either 2 or 3 uint32_t, and after that we have
   * frames_num, flags and magic for another 9 bytes. */
  uint32_t expected_frame_length = frames_num * (has_checksums ? 12 : 8) + 9;
  /* The frame starts with another magic number and its length, but these
   * two fields are not included when counting length. */
  off64_t frame_start_ofs = 8 + expected_frame_length;
  /* Sanity check: Before the start of the seek table frame,
   * there must be frames_num frames, each of which at least 8 bytes long. */
  off64_t seek_frame_start = base->seek(base, -frame_start_ofs, SEEK_END);
  if (seek_frame_start < frames_num * 8) {
    return false;
  }

  if (!zstd_read_u32(base, &magic) || magic != 0x184D2A5E) {
    return false;
  }

  uint32_t frame_length;
  if (!zstd_read_u32(base, &frame_length) || frame_length != expected_frame_length) {
    return false;
  }

  zstd->seek.frames_num = frames_num;
  zstd->seek.compressed_ofs = MEM_new_array_uninitialized<size_t>(frames_num + 1, __func__);
  zstd->seek.uncompressed_ofs = MEM_new_array_uninitialized<size_t>(frames_num + 1, __func__);

  size_t compressed_ofs = 0;
  size_t uncompressed_ofs = 0;
  for (int i = 0; i < frames_num; i++) {
    uint32_t compressed_size, uncompressed_size;
    if (!zstd_read_u32(base, &compressed_size) || !zstd_read_u32(base, &uncompressed_size)) {
      break;
    }
    if (has_checksums && base->seek(base, 4, SEEK_CUR) < 0) {
      break;
    }
    zstd->seek.compressed_ofs[i] = compressed_ofs;
    zstd->seek.uncompressed_ofs[i] = uncompressed_ofs;
    compressed_ofs += compressed_size;
    uncompressed_ofs += uncompressed_size;
  }
  zstd->seek.compressed_ofs[frames_num] = compressed_ofs;
  zstd->seek.uncompressed_ofs[frames_num] = uncompressed_ofs;

  /* Seek to the end of the previous frame for the following #BHead frame detection. */
  if (seek_frame_start != compressed_ofs || base->seek(base, seek_frame_start, SEEK_SET) < 0) {
    MEM_delete(zstd->seek.compressed_ofs);
    MEM_delete(zstd->seek.uncompressed_ofs);
    memset(&zstd->seek, 0, sizeof(zstd->seek));
    return false;
  }

  zstd->seek.cached_frame = -1;

  return true;
}
```

</details>

**沿实际写入检查状态**

- `zstd->seek.frames_num = frames_num;`
- `zstd->seek.compressed_ofs = MEM_new_array_uninitialized<size_t>(frames_num + 1, __func__);`
- `zstd->seek.uncompressed_ofs = MEM_new_array_uninitialized<size_t>(frames_num + 1, __func__);`
- `zstd->seek.compressed_ofs[i] = compressed_ofs;`
- `zstd->seek.uncompressed_ofs[i] = uncompressed_ofs;`
- `compressed_ofs += compressed_size;`
- `uncompressed_ofs += uncompressed_size;`
- `zstd->seek.compressed_ofs[frames_num] = compressed_ofs;`
- `zstd->seek.uncompressed_ofs[frames_num] = uncompressed_ofs;`
- `zstd->seek.cached_frame = -1;`

**结果出口**

- `return false;`
- `return true;`

**继续追踪实现**

- `base->seek` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：由接收对象具体类型或运行时策略提供实现。调用位置L55。
- `zstd_read_u32` → [blender::zstd_read_u32 · L39](filereader_zstd.cc.md#f-1deb478138ea6c19)。
- `base->read` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：由接收对象具体类型或运行时策略提供实现。调用位置L64。
- `MEM_new_array_uninitialized<size_t>` → [MEM_new_array_uninitialized · L608](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-b7103eae8eb57b05)；[MEM_new_array_uninitialized · L129](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-bf6ef4ddcfb6e5df)。同名重载需按实参类型选择。
- `MEM_delete` → [MEM_delete · L400](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-9049ffdd1682887c)。
- `memset` → [外部契约](https://eel.is/c++draft/cstring.syn)：填充字节，不调用T构造函数，也不保证任意类型的全零表示是合法或期望值。

<a id="f-a6c6696faacade56"></a>

### `blender::BLI_filereader_new_zstd`

实现位置：[source/blender/blenlib/intern/filereader_zstd.cc](../../../../../../../source/blender/blenlib/intern/filereader_zstd.cc) · L299—L328。

接口参数：

- `FileReader *base`

**教学注释版**

<!-- annotated:f1f97e7762b9a8 -->

```cpp
FileReader *BLI_filereader_new_zstd(FileReader *base)
{
  ZstdReader *zstd = MEM_new_zeroed<ZstdReader>(__func__);

  zstd->ctx = ZSTD_createDCtx();
  zstd->base = base;

  if (zstd_read_seek_table(zstd)) {
    zstd->reader.read = zstd_read_seekable;
    zstd->reader.seek = zstd_seek;
  }
  else {
    zstd->reader.read = zstd_read;
    zstd->reader.seek = nullptr;

    zstd->in_buf_max_size = ZSTD_DStreamInSize();
    zstd->in_buf.src = MEM_new_array_uninitialized<std::byte>(zstd->in_buf_max_size,
                                                              "zstd in buf");
    zstd->in_buf.size = zstd->in_buf_max_size;
    /* This signals that the buffer has run out,
     * which will make the read function refill it on the first call. */
    zstd->in_buf.pos = zstd->in_buf_max_size;
  }
  zstd->reader.close = zstd_close;

  /* Rewind after the seek table check so that zstd_read starts at the file's start. */
  zstd->base->seek(zstd->base, 0, SEEK_SET);

  return reinterpret_cast<FileReader *>(zstd);
}
```

<details>
<summary>核对原始源码：source/blender/blenlib/intern/filereader_zstd.cc · L299—L328</summary>

<!-- original:f1f97e7762b9a8:source/blender/blenlib/intern/filereader_zstd.cc:299:328 -->

```cpp
FileReader *BLI_filereader_new_zstd(FileReader *base)
{
  ZstdReader *zstd = MEM_new_zeroed<ZstdReader>(__func__);

  zstd->ctx = ZSTD_createDCtx();
  zstd->base = base;

  if (zstd_read_seek_table(zstd)) {
    zstd->reader.read = zstd_read_seekable;
    zstd->reader.seek = zstd_seek;
  }
  else {
    zstd->reader.read = zstd_read;
    zstd->reader.seek = nullptr;

    zstd->in_buf_max_size = ZSTD_DStreamInSize();
    zstd->in_buf.src = MEM_new_array_uninitialized<std::byte>(zstd->in_buf_max_size,
                                                              "zstd in buf");
    zstd->in_buf.size = zstd->in_buf_max_size;
    /* This signals that the buffer has run out,
     * which will make the read function refill it on the first call. */
    zstd->in_buf.pos = zstd->in_buf_max_size;
  }
  zstd->reader.close = zstd_close;

  /* Rewind after the seek table check so that zstd_read starts at the file's start. */
  zstd->base->seek(zstd->base, 0, SEEK_SET);

  return reinterpret_cast<FileReader *>(zstd);
}
```

</details>

**沿实际写入检查状态**

- `zstd->ctx = ZSTD_createDCtx();`
- `zstd->base = base;`
- `zstd->reader.read = zstd_read_seekable;`
- `zstd->reader.seek = zstd_seek;`
- `zstd->reader.read = zstd_read;`
- `zstd->reader.seek = nullptr;`
- `zstd->in_buf_max_size = ZSTD_DStreamInSize();`
- `zstd->in_buf.src = MEM_new_array_uninitialized<std::byte>(zstd->in_buf_max_size,`
- `zstd->in_buf.size = zstd->in_buf_max_size;`
- `zstd->in_buf.pos = zstd->in_buf_max_size;`
- `zstd->reader.close = zstd_close;`

**结果出口**

- `return reinterpret_cast<FileReader *>(zstd);`

**继续追踪实现**

- `MEM_new_zeroed<ZstdReader>` → [MEM_new_zeroed · L550](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-eeb1e2a7f57dd231)；[MEM_new_zeroed · L114](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-e04cf01c64c8b180)。同名重载需按实参类型选择。
- `ZSTD_createDCtx` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L303。
- `zstd_read_seek_table` → [blender::zstd_read_seek_table · L49](filereader_zstd.cc.md#f-ce297e1b3f4c2089)。
- `ZSTD_DStreamInSize` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L314。
- `MEM_new_array_uninitialized<std::byte>` → [MEM_new_array_uninitialized · L608](../../07-Intern运行时与平台/guardedalloc/MEM_guardedalloc.h.md#f-b7103eae8eb57b05)；[MEM_new_array_uninitialized · L129](../../07-Intern运行时与平台/guardedalloc/intern/mallocn.cc.md#f-bf6ef4ddcfb6e5df)。同名重载需按实参类型选择。
- `zstd->base->seek` → [调用协议](../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L325。
