# 实现依赖专题：source/blender/imbuf/movie/intern/movie_util.cc

[实现依赖导航](../../../../README.md) · [符号索引](../../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::isffmpeg"]:::abstraction
  F1["blender::MOV_is_movie_file"]:::compute
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
  F["movie_util.cc实现"]:::compute
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

<a id="f-80cfeed1ef73fe85"></a>

### `blender::isffmpeg`

实现位置：[source/blender/imbuf/movie/intern/movie_util.cc](../../../../../../../../../source/blender/imbuf/movie/intern/movie_util.cc) · L157—L219。

接口参数：

- `const char *filepath`

**教学注释版**

<!-- annotated:cae4fed5a23390 -->

```cpp
static int isffmpeg(const char *filepath)
{
  AVFormatContext *pFormatCtx = nullptr;
  uint i;
  int videoStream;
  const AVCodec *pCodec;

  if (BLI_path_extension_check_n(filepath,
                                 ".swf",
                                 ".jpg",
                                 ".jp2",
                                 ".j2c",
                                 ".png",
                                 ".dds",
                                 ".tga",
                                 ".bmp",
                                 ".tif",
                                 ".exr",
                                 ".cin",
                                 ".wav",
                                 nullptr))
  {
    return 0;
  }

  if (avformat_open_input(&pFormatCtx, filepath, nullptr, nullptr) != 0) {
    return 0;
  }

  if (avformat_find_stream_info(pFormatCtx, nullptr) < 0) {
    avformat_close_input(&pFormatCtx);
    return 0;
  }

  /* Find the first video stream */
  videoStream = -1;
  for (i = 0; i < pFormatCtx->nb_streams; i++) {
    if (pFormatCtx->streams[i] && pFormatCtx->streams[i]->codecpar &&
        (pFormatCtx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO))
    {
      videoStream = i;
      break;
    }
  }

  if (videoStream == -1) {
    avformat_close_input(&pFormatCtx);
    return 0;
  }

  AVCodecParameters *codec_par = pFormatCtx->streams[videoStream]->codecpar;

  /* Find the decoder for the video stream */
  pCodec = avcodec_find_decoder(codec_par->codec_id);
  if (pCodec == nullptr) {
    avformat_close_input(&pFormatCtx);
    return 0;
  }

  avformat_close_input(&pFormatCtx);

  return 1;
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/movie/intern/movie_util.cc · L157—L219</summary>

<!-- original:cae4fed5a23390:source/blender/imbuf/movie/intern/movie_util.cc:157:219 -->

```cpp
static int isffmpeg(const char *filepath)
{
  AVFormatContext *pFormatCtx = nullptr;
  uint i;
  int videoStream;
  const AVCodec *pCodec;

  if (BLI_path_extension_check_n(filepath,
                                 ".swf",
                                 ".jpg",
                                 ".jp2",
                                 ".j2c",
                                 ".png",
                                 ".dds",
                                 ".tga",
                                 ".bmp",
                                 ".tif",
                                 ".exr",
                                 ".cin",
                                 ".wav",
                                 nullptr))
  {
    return 0;
  }

  if (avformat_open_input(&pFormatCtx, filepath, nullptr, nullptr) != 0) {
    return 0;
  }

  if (avformat_find_stream_info(pFormatCtx, nullptr) < 0) {
    avformat_close_input(&pFormatCtx);
    return 0;
  }

  /* Find the first video stream */
  videoStream = -1;
  for (i = 0; i < pFormatCtx->nb_streams; i++) {
    if (pFormatCtx->streams[i] && pFormatCtx->streams[i]->codecpar &&
        (pFormatCtx->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO))
    {
      videoStream = i;
      break;
    }
  }

  if (videoStream == -1) {
    avformat_close_input(&pFormatCtx);
    return 0;
  }

  AVCodecParameters *codec_par = pFormatCtx->streams[videoStream]->codecpar;

  /* Find the decoder for the video stream */
  pCodec = avcodec_find_decoder(codec_par->codec_id);
  if (pCodec == nullptr) {
    avformat_close_input(&pFormatCtx);
    return 0;
  }

  avformat_close_input(&pFormatCtx);

  return 1;
}
```

</details>

**沿实际写入检查状态**

- `videoStream = -1;`
- `videoStream = i;`
- `pCodec = avcodec_find_decoder(codec_par->codec_id);`

**结果出口**

- `return 0;`
- `return 1;`

**继续追踪实现**

- `BLI_path_extension_check_n` → [BLI_path_extension_check_n · L1483](../../../../01-BLI基础库/intern/path_utils.cc.md#f-5f4ad72908476cfd)。
- `avformat_open_input` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L182。
- `avformat_find_stream_info` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L186。
- `avformat_close_input` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L187。
- `avcodec_find_decoder` → [调用协议](../../../../../00-课程指南/01-路线与规范/模板宏与动态分派协议.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L210。

<a id="f-4ffa8689509dcf0f"></a>

### `blender::MOV_is_movie_file`

实现位置：[source/blender/imbuf/movie/intern/movie_util.cc](../../../../../../../../../source/blender/imbuf/movie/intern/movie_util.cc) · L608—L621。

接口参数：

- `const char *filepath`

**教学注释版**

<!-- annotated:749d0e4b428f51 -->

```cpp
bool MOV_is_movie_file(const char *filepath)
{
  BLI_assert(!BLI_path_is_rel(filepath));

#ifdef WITH_FFMPEG
  if (isffmpeg(filepath)) {
    return true;
  }
#else
  UNUSED_VARS(filepath);
#endif

  return false;
}
```

<details>
<summary>核对原始源码：source/blender/imbuf/movie/intern/movie_util.cc · L608—L621</summary>

<!-- original:749d0e4b428f51:source/blender/imbuf/movie/intern/movie_util.cc:608:621 -->

```cpp
bool MOV_is_movie_file(const char *filepath)
{
  BLI_assert(!BLI_path_is_rel(filepath));

#ifdef WITH_FFMPEG
  if (isffmpeg(filepath)) {
    return true;
  }
#else
  UNUSED_VARS(filepath);
#endif

  return false;
}
```

</details>

**结果出口**

- `return true;`
- `return false;`

**继续追踪实现**

- `BLI_assert` → [BLI_assert · L48](../../../../01-BLI基础库/BLI_assert.hh.md#m-57a88495704d)；[BLI_assert · L63](../../../../01-BLI基础库/BLI_assert.hh.md#m-d07050020cb5)。宏定义由构建条件选择。
- `BLI_path_is_rel` → [BLI_path_is_rel · L536](../../../../01-BLI基础库/intern/path_utils.cc.md#f-d938443d331ba72c)。
- `isffmpeg` → [blender::isffmpeg · L157](movie_util.cc.md#f-80cfeed1ef73fe85)。
- `UNUSED_VARS` → [UNUSED_VARS · L522](../../../../01-BLI基础库/BLI_utildefines.hh.md#m-013582537634)；[UNUSED_VARS · L41](../../../gpu/GPU_shader_shared_utils.hh.md#m-05d9d7a33da0)；[UNUSED_VARS · L62](../../../gpu/GPU_shader_shared_utils.hh.md#m-e12c683a4aca)。宏定义由构建条件选择。
