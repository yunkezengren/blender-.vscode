# 实现依赖专题：source/blender/imbuf/movie/intern/movie_read.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["MOV_close"]:::abstraction
  F1["probe_video_colorspace"]:::compute
  F2["MOV_open_file"]:::compute
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
  F["movie_read.cc实现"]:::compute
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

<a id="f-3180d117d9011594"></a>

### `MOV_close`

实现位置：[source/blender/imbuf/movie/intern/movie_read.cc](../../../../../source/blender/imbuf/movie/intern/movie_read.cc) · L70—L83。

接口参数：

- `MovieReader *anim`

**教学注释版**

<!-- annotated:3113307265606f -->

```cpp
void MOV_close(MovieReader *anim)
{
  if (anim == nullptr) {
    return;
  }

#ifdef WITH_FFMPEG
  free_anim_ffmpeg(anim);
#endif
  MOV_close_proxies(anim);
  IMB_metadata_free(anim->metadata);

  MEM_delete(anim);
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/movie/intern/movie_read.cc · L70—L83</summary>

<!-- original:3113307265606f:source/blender/imbuf/movie/intern/movie_read.cc:70:83 -->

```cpp
void MOV_close(MovieReader *anim)
{
  if (anim == nullptr) {
    return;
  }

#ifdef WITH_FFMPEG
  free_anim_ffmpeg(anim);
#endif
  MOV_close_proxies(anim);
  IMB_metadata_free(anim->metadata);

  MEM_delete(anim);
}
```

</details>

**继续追踪实现**

- `free_anim_ffmpeg` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L77。
- `MOV_close_proxies` → [blender::MOV_close_proxies · L892](%E4%BE%9D%E8%B5%96-movie_proxy_indexer-c32f88.md#f-e32184b78e7894d6)。
- `IMB_metadata_free` → [blender::IMB_metadata_free · L89](%E4%BE%9D%E8%B5%96-metadata-bcdcfd.md#f-e318fa37c302cbb8)。
- `MEM_delete` → [MEM_delete · L400](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-9049ffdd1682887c)。

<a id="f-dbe4ebcb4ea703b2"></a>

### `probe_video_colorspace`

实现位置：[source/blender/imbuf/movie/intern/movie_read.cc](../../../../../source/blender/imbuf/movie/intern/movie_read.cc) · L113—L143。

接口参数：

- `MovieReader *anim`
- `char r_colorspace_name[IM_MAX_SPACE]`

**教学注释版**

<!-- annotated:2ea6d54d4f7f9b -->

```cpp
static void probe_video_colorspace(MovieReader *anim, char r_colorspace_name[IM_MAX_SPACE])
{
  /* Use default role as fallback (i.e. it is an unknown combination of colorspace and primaries)
   */
  BLI_strncpy_utf8(r_colorspace_name,
                   IMB_colormanagement_role_colorspace_name_get(COLOR_ROLE_DEFAULT_BYTE),
                   IM_MAX_SPACE);

  if (anim->state == MovieReader::State::Uninitialized) {
    if (!anim_getnew(anim)) {
      return;
    }
  }

#ifdef WITH_FFMPEG
  /* Note that the ffmpeg enums are documented to match CICP codes. */
  const int cicp[4] = {anim->codec_ctx->color_primaries,
                       anim->codec_ctx->color_trc,
                       anim->codec_ctx->colorspace,
                       anim->codec_ctx->color_range};
  const ColorSpace *colorspace = IMB_colormanagement_space_from_cicp(
      cicp, ColorManagedFileOutput::Video);

  if (colorspace == nullptr) {
    return;
  }

  BLI_strncpy_utf8(
      r_colorspace_name, IMB_colormanagement_colorspace_get_name(colorspace), IM_MAX_SPACE);
#endif /* WITH_FFMPEG */
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/movie/intern/movie_read.cc · L113—L143</summary>

<!-- original:2ea6d54d4f7f9b:source/blender/imbuf/movie/intern/movie_read.cc:113:143 -->

```cpp
static void probe_video_colorspace(MovieReader *anim, char r_colorspace_name[IM_MAX_SPACE])
{
  /* Use default role as fallback (i.e. it is an unknown combination of colorspace and primaries)
   */
  BLI_strncpy_utf8(r_colorspace_name,
                   IMB_colormanagement_role_colorspace_name_get(COLOR_ROLE_DEFAULT_BYTE),
                   IM_MAX_SPACE);

  if (anim->state == MovieReader::State::Uninitialized) {
    if (!anim_getnew(anim)) {
      return;
    }
  }

#ifdef WITH_FFMPEG
  /* Note that the ffmpeg enums are documented to match CICP codes. */
  const int cicp[4] = {anim->codec_ctx->color_primaries,
                       anim->codec_ctx->color_trc,
                       anim->codec_ctx->colorspace,
                       anim->codec_ctx->color_range};
  const ColorSpace *colorspace = IMB_colormanagement_space_from_cicp(
      cicp, ColorManagedFileOutput::Video);

  if (colorspace == nullptr) {
    return;
  }

  BLI_strncpy_utf8(
      r_colorspace_name, IMB_colormanagement_colorspace_get_name(colorspace), IM_MAX_SPACE);
#endif /* WITH_FFMPEG */
}
```

</details>

**继续追踪实现**

- `BLI_strncpy_utf8` → [blender::BLI_strncpy_utf8 · L404](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-string_utf8-3c62ca.md#f-ff7c5f28742085a0)。
- `IMB_colormanagement_role_colorspace_name_get` → [blender::IMB_colormanagement_role_colorspace_name_get · L1247](%E4%BE%9D%E8%B5%96-colormanagement-d4733d.md#f-f2cf0e85682f0fd8)。
- `anim_getnew` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L122。
- `IMB_colormanagement_space_from_cicp` → [blender::IMB_colormanagement_space_from_cicp · L1635](%E4%BE%9D%E8%B5%96-colormanagement-d4733d.md#f-2ac618084b77c16d)。
- `IMB_colormanagement_colorspace_get_name` → [blender::IMB_colormanagement_colorspace_get_name · L3153](%E4%BE%9D%E8%B5%96-colormanagement-d4733d.md#f-32fc2ecf4cf93fd6)。

<a id="f-1582d0c5cead9266"></a>

### `MOV_open_file`

实现位置：[source/blender/imbuf/movie/intern/movie_read.cc](../../../../../source/blender/imbuf/movie/intern/movie_read.cc) · L145—L180。

接口参数：

- `const char *filepath`
- `const ImBufFlags ib_flags`
- `const int streamindex`
- `const bool keep_original_colorspace`
- `ColorManagedColorspaceSettings *colorspace_settings`

**教学注释版**

<!-- annotated:cc7e8e34a52721 -->

```cpp
MovieReader *MOV_open_file(const char *filepath,
                           const ImBufFlags ib_flags,
                           const int streamindex,
                           const bool keep_original_colorspace,
                           ColorManagedColorspaceSettings *colorspace_settings)
{
  MovieReader *anim;

  BLI_assert(!BLI_path_is_rel(filepath));

  anim = MEM_new<MovieReader>("anim struct");
  if (anim != nullptr) {

    STRNCPY(anim->filepath, filepath);
    anim->ib_flags = ib_flags;
    anim->streamindex = streamindex;
    anim->keep_original_colorspace = keep_original_colorspace;

    if (colorspace_settings && colorspace_settings->name[0] != '\0') {
      /* Use colorspace from argument, if provided. */
      STRNCPY_UTF8(anim->colorspace, colorspace_settings->name);
    }
    else {
      /* Try to initialize colorspace from the FFmpeg stream by interpreting color information from
       * it. */
      char file_colorspace[IM_MAX_SPACE];
      probe_video_colorspace(anim, file_colorspace);
      STRNCPY_UTF8(anim->colorspace, file_colorspace);
      if (colorspace_settings) {
        /* Copy the used colorspace into output argument. */
        IMB_colormanagement_colorspace_settings_set(colorspace_settings, file_colorspace);
      }
    }
  }
  return anim;
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/movie/intern/movie_read.cc · L145—L180</summary>

<!-- original:cc7e8e34a52721:source/blender/imbuf/movie/intern/movie_read.cc:145:180 -->

```cpp
MovieReader *MOV_open_file(const char *filepath,
                           const ImBufFlags ib_flags,
                           const int streamindex,
                           const bool keep_original_colorspace,
                           ColorManagedColorspaceSettings *colorspace_settings)
{
  MovieReader *anim;

  BLI_assert(!BLI_path_is_rel(filepath));

  anim = MEM_new<MovieReader>("anim struct");
  if (anim != nullptr) {

    STRNCPY(anim->filepath, filepath);
    anim->ib_flags = ib_flags;
    anim->streamindex = streamindex;
    anim->keep_original_colorspace = keep_original_colorspace;

    if (colorspace_settings && colorspace_settings->name[0] != '\0') {
      /* Use colorspace from argument, if provided. */
      STRNCPY_UTF8(anim->colorspace, colorspace_settings->name);
    }
    else {
      /* Try to initialize colorspace from the FFmpeg stream by interpreting color information from
       * it. */
      char file_colorspace[IM_MAX_SPACE];
      probe_video_colorspace(anim, file_colorspace);
      STRNCPY_UTF8(anim->colorspace, file_colorspace);
      if (colorspace_settings) {
        /* Copy the used colorspace into output argument. */
        IMB_colormanagement_colorspace_settings_set(colorspace_settings, file_colorspace);
      }
    }
  }
  return anim;
}
```

</details>

**沿实际写入检查状态**

- `anim = MEM_new<MovieReader>("anim struct");`
- `anim->ib_flags = ib_flags;`
- `anim->streamindex = streamindex;`
- `anim->keep_original_colorspace = keep_original_colorspace;`

**结果出口**

- `return anim;`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-57a88495704d)；[BLI_assert · L63](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_assert-cc98e8.md#m-d07050020cb5)。宏定义由构建条件选择。
- `BLI_path_is_rel` → [BLI_path_is_rel · L536](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-path_utils-b4d26a.md#f-d938443d331ba72c)。
- `MEM_new<MovieReader>` → [MEM_new · L351](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-115f9b6784f89912)。
- `STRNCPY` → [blender::STRNCPY · L690](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_string-b43058.md#f-6b2d861724026be6)。
- `STRNCPY_UTF8` → [STRNCPY_UTF8 · L335](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_string_utf8-bcc961.md#m-222967f0ab6a)。宏定义由构建条件选择。
- `probe_video_colorspace` → [probe_video_colorspace · L113](%E4%BE%9D%E8%B5%96-movie_read-4cc1f5.md#f-dbe4ebcb4ea703b2)。
- `IMB_colormanagement_colorspace_settings_set` → [blender::IMB_colormanagement_colorspace_settings_set · L3164](%E4%BE%9D%E8%B5%96-colormanagement-d4733d.md#f-85d2536cb6c79b87)。
