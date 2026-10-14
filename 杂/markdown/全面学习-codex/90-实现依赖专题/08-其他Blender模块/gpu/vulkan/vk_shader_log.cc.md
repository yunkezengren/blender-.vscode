# 实现依赖专题：source/blender/gpu/vulkan/vk_shader_log.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::gpu::VKLogParser::parse_line"]:::abstraction
  F1["blender::gpu::VKLogParser::skip_name"]:::compute
  F2["blender::gpu::VKLogParser::skip_severity_keyword"]:::compute
  F0 -->|"显式调用"| F1
  F0 -->|"显式调用"| F2
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
  F["vk_shader_log.cc实现"]:::compute
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

<a id="f-4c59fb7e99e2a338"></a>

### `blender::gpu::VKLogParser::parse_line`

实现位置：[source/blender/gpu/vulkan/vk_shader_log.cc](../../../../../../../../source/blender/gpu/vulkan/vk_shader_log.cc) · L15—L54。

接口参数：

- `const char *source_combined`
- `const char *log_line`
- `GPULogItem &log_item`

**教学注释版**

<!-- annotated:5090fa74dcb550 -->

```cpp
const char *VKLogParser::parse_line(const char *source_combined,
                                    const char *log_line,
                                    GPULogItem &log_item)
{
  /* Shader name. */
  log_line = skip_name(log_line);
  log_line = skip_separators(log_line, ":");

  /* Parse error line & char numbers. */
  if (at_number(log_line)) {
    const char *error_line_number_end;
    log_item.cursor.row = parse_number(log_line, &error_line_number_end);
    log_line = error_line_number_end;
    log_line = skip_separators(log_line, ": ");
  }
  if (at_number(log_line)) {
    const char *number_end;
    log_item.cursor.column = parse_number(log_line, &number_end);
    log_line = number_end;
  }
  log_line = skip_separators(log_line, ": ");

  /* Skip to message. Avoid redundant info. */
  log_line = skip_severity_keyword(log_line, log_item);
  log_line = skip_separators(log_line, ": ");

  if (log_item.cursor.row != -1) {
    /* Get to the wanted line. */
    size_t line_start_character = line_start_get(source_combined, log_item.cursor.row);
    StringRef filename = filename_get(source_combined, line_start_character);
    size_t line_number = source_line_get(source_combined, line_start_character);
    log_item.cursor.file_name_and_error_line = std::string(filename) + ':' +
                                               std::to_string(line_number);
    if (log_item.cursor.column != -1) {
      log_item.cursor.file_name_and_error_line += ':' + std::to_string(log_item.cursor.column + 1);
    }
  }

  return log_line;
}
```

<details>
<summary>核对原始源码：source/blender/gpu/vulkan/vk_shader_log.cc · L15—L54</summary>

<!-- original:5090fa74dcb550:source/blender/gpu/vulkan/vk_shader_log.cc:15:54 -->

```cpp
const char *VKLogParser::parse_line(const char *source_combined,
                                    const char *log_line,
                                    GPULogItem &log_item)
{
  /* Shader name. */
  log_line = skip_name(log_line);
  log_line = skip_separators(log_line, ":");

  /* Parse error line & char numbers. */
  if (at_number(log_line)) {
    const char *error_line_number_end;
    log_item.cursor.row = parse_number(log_line, &error_line_number_end);
    log_line = error_line_number_end;
    log_line = skip_separators(log_line, ": ");
  }
  if (at_number(log_line)) {
    const char *number_end;
    log_item.cursor.column = parse_number(log_line, &number_end);
    log_line = number_end;
  }
  log_line = skip_separators(log_line, ": ");

  /* Skip to message. Avoid redundant info. */
  log_line = skip_severity_keyword(log_line, log_item);
  log_line = skip_separators(log_line, ": ");

  if (log_item.cursor.row != -1) {
    /* Get to the wanted line. */
    size_t line_start_character = line_start_get(source_combined, log_item.cursor.row);
    StringRef filename = filename_get(source_combined, line_start_character);
    size_t line_number = source_line_get(source_combined, line_start_character);
    log_item.cursor.file_name_and_error_line = std::string(filename) + ':' +
                                               std::to_string(line_number);
    if (log_item.cursor.column != -1) {
      log_item.cursor.file_name_and_error_line += ':' + std::to_string(log_item.cursor.column + 1);
    }
  }

  return log_line;
}
```

</details>

**沿实际写入检查状态**

- `log_line = skip_name(log_line);`
- `log_line = skip_separators(log_line, ":");`
- `log_item.cursor.row = parse_number(log_line, &error_line_number_end);`
- `log_line = error_line_number_end;`
- `log_line = skip_separators(log_line, ": ");`
- `log_item.cursor.column = parse_number(log_line, &number_end);`
- `log_line = number_end;`
- `log_line = skip_severity_keyword(log_line, log_item);`
- `log_item.cursor.file_name_and_error_line = std::string(filename) + ':' +`
- `log_item.cursor.file_name_and_error_line += ':' + std::to_string(log_item.cursor.column + 1);`

**结果出口**

- `return log_line;`

**继续追踪实现**

- `skip_name` → [blender::gpu::VKLogParser::skip_name · L56](vk_shader_log.cc.md#f-d1ae002fce61c1c3)。
- `skip_separators` → [blender::gpu::GPULogParser::skip_separators · L297](../intern/gpu_shader_log.cc.md#f-cd8fc24d4e26a018)。
- `at_number` → [blender::gpu::GPULogParser::at_number · L317](../intern/gpu_shader_log.cc.md#f-e14d9a3b16837238)。
- `parse_number` → [blender::gpu::GPULogParser::parse_number · L327](../intern/gpu_shader_log.cc.md#f-b6bc341be2b6e2cf)。
- `skip_severity_keyword` → [blender::gpu::VKLogParser::skip_severity_keyword · L61](vk_shader_log.cc.md#f-f1994ed574ad7521)。
- `line_start_get` → [blender::gpu::GPULogParser::line_start_get · L332](../intern/gpu_shader_log.cc.md#f-b8c61af03e75cdbd)。
- `filename_get` → [blender::gpu::GPULogParser::filename_get · L348](../intern/gpu_shader_log.cc.md#f-ea9f94085e30c06b)。
- `source_line_get` → [blender::gpu::GPULogParser::source_line_get · L364](../intern/gpu_shader_log.cc.md#f-0aad1899e03c2525)。
- `std::string` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
- `std::to_string` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。

<a id="f-d1ae002fce61c1c3"></a>

### `blender::gpu::VKLogParser::skip_name`

实现位置：[source/blender/gpu/vulkan/vk_shader_log.cc](../../../../../../../../source/blender/gpu/vulkan/vk_shader_log.cc) · L56—L59。

接口参数：

- `const char *log_line`

**教学注释版**

<!-- annotated:9eefa6d6c72a09 -->

```cpp
const char *VKLogParser::skip_name(const char *log_line)
{
  return skip_until(log_line, ':');
}
```

<details>
<summary>核对原始源码：source/blender/gpu/vulkan/vk_shader_log.cc · L56—L59</summary>

<!-- original:9eefa6d6c72a09:source/blender/gpu/vulkan/vk_shader_log.cc:56:59 -->

```cpp
const char *VKLogParser::skip_name(const char *log_line)
{
  return skip_until(log_line, ':');
}
```

</details>

**结果出口**

- `return skip_until(log_line, ':');`

**继续追踪实现**

- `skip_until` → [blender::gpu::GPULogParser::skip_until · L305](../intern/gpu_shader_log.cc.md#f-b64198603624b9cb)。

<a id="f-f1994ed574ad7521"></a>

### `blender::gpu::VKLogParser::skip_severity_keyword`

实现位置：[source/blender/gpu/vulkan/vk_shader_log.cc](../../../../../../../../source/blender/gpu/vulkan/vk_shader_log.cc) · L61—L64。

接口参数：

- `const char *log_line`
- `GPULogItem &log_item`

**教学注释版**

<!-- annotated:df85b441daf1d9 -->

```cpp
const char *VKLogParser::skip_severity_keyword(const char *log_line, GPULogItem &log_item)
{
  return skip_severity(log_line, log_item, "error", "warning", "note");
}
```

<details>
<summary>核对原始源码：source/blender/gpu/vulkan/vk_shader_log.cc · L61—L64</summary>

<!-- original:df85b441daf1d9:source/blender/gpu/vulkan/vk_shader_log.cc:61:64 -->

```cpp
const char *VKLogParser::skip_severity_keyword(const char *log_line, GPULogItem &log_item)
{
  return skip_severity(log_line, log_item, "error", "warning", "note");
}
```

</details>

**结果出口**

- `return skip_severity(log_line, log_item, "error", "warning", "note");`

**继续追踪实现**

- `skip_severity` → [blender::gpu::GPULogParser::skip_severity · L276](../intern/gpu_shader_log.cc.md#f-30864ad1cb97f7fa)。
