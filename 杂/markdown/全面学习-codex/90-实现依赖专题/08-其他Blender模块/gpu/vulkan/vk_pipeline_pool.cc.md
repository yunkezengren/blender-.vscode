# 实现依赖专题：source/blender/gpu/vulkan/vk_pipeline_pool.cc

[实现依赖导航](../../../README.md) · [符号索引](../../../../00-课程指南/02-源码与提交索引/符号依赖与实现索引.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::gpu::VKGraphicsInfo::pipeline_info_source"]:::abstraction
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
  F["vk_pipeline_pool.cc实现"]:::compute
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

<a id="f-82a47663d2b27b7d"></a>

### `blender::gpu::VKGraphicsInfo::pipeline_info_source`

实现位置：[source/blender/gpu/vulkan/vk_pipeline_pool.cc](../../../../../../../../source/blender/gpu/vulkan/vk_pipeline_pool.cc) · L255—L490。

**教学注释版**

<!-- annotated:6d399ff4771044 -->

```cpp
std::string VKGraphicsInfo::pipeline_info_source() const
{
  std::stringstream result;
  result << "info.pipeline_state()\n";
  result << "  .primitive(";
  switch (vertex_in.vk_topology) {
    case VK_PRIMITIVE_TOPOLOGY_POINT_LIST:
      result << "GPU_PRIM_POINTS";
      break;
    case VK_PRIMITIVE_TOPOLOGY_LINE_LIST:
      result << "GPU_PRIM_LINES";
      break;
    case VK_PRIMITIVE_TOPOLOGY_LINE_STRIP:
      result << "GPU_PRIM_LINE_STRIP";
      break;
    case VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST:
      result << "GPU_PRIM_TRIS";
      break;
    case VK_PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP:
      result << "GPU_PRIM_TRI_STRIP";
      break;
    case VK_PRIMITIVE_TOPOLOGY_TRIANGLE_FAN:
      result << "GPU_PRIM_TRI_FAN";
      break;
    case VK_PRIMITIVE_TOPOLOGY_LINE_LIST_WITH_ADJACENCY:
      result << "GPU_PRIM_LINES_ADJ";
      break;
    case VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST_WITH_ADJACENCY:
      result << "GPU_PRIM_TRIS_ADJ";
      break;
    default:
      BLI_assert_unreachable();
  };
  result << ")\n";
  result << "  .state(";
  /* Write mask */
  Vector<std::string> write_masks;
  if (fragment_out.state.write_mask & GPU_WRITE_COLOR) {
    if ((fragment_out.state.write_mask & GPU_WRITE_COLOR) == GPU_WRITE_COLOR) {
      // [讲解] write_masks.append：在尾部建立新元素，必要时先扩大存储。
      write_masks.append("GPU_WRITE_COLOR");
    }
    else {
      if (fragment_out.state.write_mask & GPU_WRITE_RED) {
        write_masks.append("GPU_WRITE_RED");
      }
      if (fragment_out.state.write_mask & GPU_WRITE_GREEN) {
        write_masks.append("GPU_WRITE_GREEN");
      }
      if (fragment_out.state.write_mask & GPU_WRITE_BLUE) {
        write_masks.append("GPU_WRITE_BLUE");
      }
      if (fragment_out.state.write_mask & GPU_WRITE_ALPHA) {
        write_masks.append("GPU_WRITE_ALPHA");
      }
    }
  }
  if (fragment_out.state.write_mask & GPU_WRITE_DEPTH) {
    write_masks.append("GPU_WRITE_DEPTH");
  }
  if (fragment_out.state.write_mask & GPU_WRITE_STENCIL) {
    write_masks.append("GPU_WRITE_STENCIL");
  }
  if (write_masks.is_empty()) {
    write_masks.append("GPU_WRITE_NONE");
  }
  for (const std::string &write_mask : write_masks) {
    result << write_mask;
    // [讲解] write_masks.last：访问有效范围首端或末端元素。
    if (&write_mask != &write_masks.last()) {
      result << " | ";
    }
  }
  /* Blending mode */
  result << ",\n         ";
  switch (fragment_out.state.blend) {
    case GPU_BLEND_NONE:
      result << "GPU_BLEND_NONE";
      break;
    case GPU_BLEND_ALPHA:
      result << "GPU_BLEND_ALPHA";
      break;
    case GPU_BLEND_ALPHA_PREMULT:
      result << "GPU_BLEND_ALPHA_PREMULT";
      break;
    case GPU_BLEND_ADDITIVE:
      result << "GPU_BLEND_ADDITIVE";
      break;
    case GPU_BLEND_ADDITIVE_PREMULT:
      result << "GPU_BLEND_ADDITIVE_PREMULT";
      break;
    case GPU_BLEND_MULTIPLY:
      result << "GPU_BLEND_MULTIPLY";
      break;
    case GPU_BLEND_SUBTRACT:
      result << "GPU_BLEND_SUBTRACT";
      break;
    case GPU_BLEND_INVERT:
      result << "GPU_BLEND_INVERT";
      break;
    case GPU_BLEND_MIN:
      result << "GPU_BLEND_MIN";
      break;
    case GPU_BLEND_MAX:
      result << "GPU_BLEND_MAX";
      break;
    case GPU_BLEND_OIT:
      result << "GPU_BLEND_OIT";
      break;
    case GPU_BLEND_BACKGROUND:
      result << "GPU_BLEND_BACKGROUND";
      break;
    case GPU_BLEND_CUSTOM:
      result << "GPU_BLEND_CUSTOM";
      break;
    case GPU_BLEND_ALPHA_UNDER_PREMUL:
      result << "GPU_BLEND_ALPHA_UNDER_PREMUL";
      break;
    case GPU_BLEND_OVERLAY_MASK_FROM_ALPHA:
      result << "GPU_BLEND_OVERLAY_MASK_FROM_ALPHA";
      break;
    case GPU_BLEND_TRANSPARENCY:
      result << "GPU_BLEND_TRANSPARENCY";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Culling test */
  result << ",\n         ";
  switch (shaders.state.culling_test) {
    case GPU_CULL_NONE:
      result << "GPU_CULL_NONE";
      break;
    case GPU_CULL_FRONT:
      result << "GPU_CULL_FRONT";
      break;
    case GPU_CULL_BACK:
      result << "GPU_CULL_BACK";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Depth test */
  result << ",\n         ";
  switch (shaders.state.depth_test) {
    case GPU_DEPTH_NONE:
      result << "GPU_DEPTH_NONE";
      break;
    case GPU_DEPTH_LESS:
      result << "GPU_DEPTH_LESS";
      break;
    case GPU_DEPTH_LESS_EQUAL:
      result << "GPU_DEPTH_LESS_EQUAL";
      break;
    case GPU_DEPTH_EQUAL:
      result << "GPU_DEPTH_EQUAL";
      break;
    case GPU_DEPTH_GREATER:
      result << "GPU_DEPTH_GREATER";
      break;
    case GPU_DEPTH_GREATER_EQUAL:
      result << "GPU_DEPTH_GREATER_EQUAL";
      break;
    case GPU_DEPTH_ALWAYS:
      result << "GPU_DEPTH_ALWAYS";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Stencil test */
  result << ",\n         ";
  switch (shaders.state.stencil_test) {
    case GPU_STENCIL_NONE:
      result << "GPU_STENCIL_NONE";
      break;
    case GPU_STENCIL_ALWAYS:
      result << "GPU_STENCIL_ALWAYS";
      break;
    case GPU_STENCIL_EQUAL:
      result << "GPU_STENCIL_EQUAL";
      break;
    case GPU_STENCIL_NEQUAL:
      result << "GPU_STENCIL_NEQUAL";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Stencil operation */
  result << ",\n         ";
  switch (shaders.state.stencil_op) {
    case GPU_STENCIL_OP_NONE:
      result << "GPU_STENCIL_OP_NONE";
      break;
    case GPU_STENCIL_OP_REPLACE:
      result << "GPU_STENCIL_OP_REPLACE";
      break;
    case GPU_STENCIL_OP_COUNT_DEPTH_PASS:
      result << "GPU_STENCIL_OP_COUNT_DEPTH_PASS";
      break;
    case GPU_STENCIL_OP_COUNT_DEPTH_FAIL:
      result << "GPU_STENCIL_OP_COUNT_DEPTH_FAIL";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Provoking vertex */
  result << ",\n         ";
  switch (shaders.state.provoking_vert) {
    case GPU_VERTEX_FIRST:
      result << "GPU_VERTEX_FIRST";
      break;
    case GPU_VERTEX_LAST:
      result << "GPU_VERTEX_LAST";
      break;
    default:
      BLI_assert_unreachable();
  }
  result << ")\n";
  /* viewports */
  result << "  .viewports(" << shaders.viewport_count << ")\n";
  /* Depth format */
  if (fragment_out.depth_attachment_format != VK_FORMAT_UNDEFINED) {
    result << "  .depth_format(gpu::TextureTargetFormat::"
           << to_gpu_format_string(fragment_out.depth_attachment_format) << ")\n";
  }
  /* Stencil format */
  if (fragment_out.stencil_attachment_format != VK_FORMAT_UNDEFINED) {
    result << "  .stencil_format(gpu::TextureTargetFormat::"
           << to_gpu_format_string(fragment_out.stencil_attachment_format) << ")\n";
  }
  /* Color formats */
  for (const VkFormat format : fragment_out.color_attachment_formats) {
    result << "  .color_format(gpu::TextureTargetFormat::" << to_gpu_format_string(format)
           << ")\n";
  }
  result << ";";
  return result.str();
}
```

<details>
<summary>核对原始源码：source/blender/gpu/vulkan/vk_pipeline_pool.cc · L255—L490</summary>

<!-- original:6d399ff4771044:source/blender/gpu/vulkan/vk_pipeline_pool.cc:255:490 -->

```cpp
std::string VKGraphicsInfo::pipeline_info_source() const
{
  std::stringstream result;
  result << "info.pipeline_state()\n";
  result << "  .primitive(";
  switch (vertex_in.vk_topology) {
    case VK_PRIMITIVE_TOPOLOGY_POINT_LIST:
      result << "GPU_PRIM_POINTS";
      break;
    case VK_PRIMITIVE_TOPOLOGY_LINE_LIST:
      result << "GPU_PRIM_LINES";
      break;
    case VK_PRIMITIVE_TOPOLOGY_LINE_STRIP:
      result << "GPU_PRIM_LINE_STRIP";
      break;
    case VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST:
      result << "GPU_PRIM_TRIS";
      break;
    case VK_PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP:
      result << "GPU_PRIM_TRI_STRIP";
      break;
    case VK_PRIMITIVE_TOPOLOGY_TRIANGLE_FAN:
      result << "GPU_PRIM_TRI_FAN";
      break;
    case VK_PRIMITIVE_TOPOLOGY_LINE_LIST_WITH_ADJACENCY:
      result << "GPU_PRIM_LINES_ADJ";
      break;
    case VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST_WITH_ADJACENCY:
      result << "GPU_PRIM_TRIS_ADJ";
      break;
    default:
      BLI_assert_unreachable();
  };
  result << ")\n";
  result << "  .state(";
  /* Write mask */
  Vector<std::string> write_masks;
  if (fragment_out.state.write_mask & GPU_WRITE_COLOR) {
    if ((fragment_out.state.write_mask & GPU_WRITE_COLOR) == GPU_WRITE_COLOR) {
      write_masks.append("GPU_WRITE_COLOR");
    }
    else {
      if (fragment_out.state.write_mask & GPU_WRITE_RED) {
        write_masks.append("GPU_WRITE_RED");
      }
      if (fragment_out.state.write_mask & GPU_WRITE_GREEN) {
        write_masks.append("GPU_WRITE_GREEN");
      }
      if (fragment_out.state.write_mask & GPU_WRITE_BLUE) {
        write_masks.append("GPU_WRITE_BLUE");
      }
      if (fragment_out.state.write_mask & GPU_WRITE_ALPHA) {
        write_masks.append("GPU_WRITE_ALPHA");
      }
    }
  }
  if (fragment_out.state.write_mask & GPU_WRITE_DEPTH) {
    write_masks.append("GPU_WRITE_DEPTH");
  }
  if (fragment_out.state.write_mask & GPU_WRITE_STENCIL) {
    write_masks.append("GPU_WRITE_STENCIL");
  }
  if (write_masks.is_empty()) {
    write_masks.append("GPU_WRITE_NONE");
  }
  for (const std::string &write_mask : write_masks) {
    result << write_mask;
    if (&write_mask != &write_masks.last()) {
      result << " | ";
    }
  }
  /* Blending mode */
  result << ",\n         ";
  switch (fragment_out.state.blend) {
    case GPU_BLEND_NONE:
      result << "GPU_BLEND_NONE";
      break;
    case GPU_BLEND_ALPHA:
      result << "GPU_BLEND_ALPHA";
      break;
    case GPU_BLEND_ALPHA_PREMULT:
      result << "GPU_BLEND_ALPHA_PREMULT";
      break;
    case GPU_BLEND_ADDITIVE:
      result << "GPU_BLEND_ADDITIVE";
      break;
    case GPU_BLEND_ADDITIVE_PREMULT:
      result << "GPU_BLEND_ADDITIVE_PREMULT";
      break;
    case GPU_BLEND_MULTIPLY:
      result << "GPU_BLEND_MULTIPLY";
      break;
    case GPU_BLEND_SUBTRACT:
      result << "GPU_BLEND_SUBTRACT";
      break;
    case GPU_BLEND_INVERT:
      result << "GPU_BLEND_INVERT";
      break;
    case GPU_BLEND_MIN:
      result << "GPU_BLEND_MIN";
      break;
    case GPU_BLEND_MAX:
      result << "GPU_BLEND_MAX";
      break;
    case GPU_BLEND_OIT:
      result << "GPU_BLEND_OIT";
      break;
    case GPU_BLEND_BACKGROUND:
      result << "GPU_BLEND_BACKGROUND";
      break;
    case GPU_BLEND_CUSTOM:
      result << "GPU_BLEND_CUSTOM";
      break;
    case GPU_BLEND_ALPHA_UNDER_PREMUL:
      result << "GPU_BLEND_ALPHA_UNDER_PREMUL";
      break;
    case GPU_BLEND_OVERLAY_MASK_FROM_ALPHA:
      result << "GPU_BLEND_OVERLAY_MASK_FROM_ALPHA";
      break;
    case GPU_BLEND_TRANSPARENCY:
      result << "GPU_BLEND_TRANSPARENCY";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Culling test */
  result << ",\n         ";
  switch (shaders.state.culling_test) {
    case GPU_CULL_NONE:
      result << "GPU_CULL_NONE";
      break;
    case GPU_CULL_FRONT:
      result << "GPU_CULL_FRONT";
      break;
    case GPU_CULL_BACK:
      result << "GPU_CULL_BACK";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Depth test */
  result << ",\n         ";
  switch (shaders.state.depth_test) {
    case GPU_DEPTH_NONE:
      result << "GPU_DEPTH_NONE";
      break;
    case GPU_DEPTH_LESS:
      result << "GPU_DEPTH_LESS";
      break;
    case GPU_DEPTH_LESS_EQUAL:
      result << "GPU_DEPTH_LESS_EQUAL";
      break;
    case GPU_DEPTH_EQUAL:
      result << "GPU_DEPTH_EQUAL";
      break;
    case GPU_DEPTH_GREATER:
      result << "GPU_DEPTH_GREATER";
      break;
    case GPU_DEPTH_GREATER_EQUAL:
      result << "GPU_DEPTH_GREATER_EQUAL";
      break;
    case GPU_DEPTH_ALWAYS:
      result << "GPU_DEPTH_ALWAYS";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Stencil test */
  result << ",\n         ";
  switch (shaders.state.stencil_test) {
    case GPU_STENCIL_NONE:
      result << "GPU_STENCIL_NONE";
      break;
    case GPU_STENCIL_ALWAYS:
      result << "GPU_STENCIL_ALWAYS";
      break;
    case GPU_STENCIL_EQUAL:
      result << "GPU_STENCIL_EQUAL";
      break;
    case GPU_STENCIL_NEQUAL:
      result << "GPU_STENCIL_NEQUAL";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Stencil operation */
  result << ",\n         ";
  switch (shaders.state.stencil_op) {
    case GPU_STENCIL_OP_NONE:
      result << "GPU_STENCIL_OP_NONE";
      break;
    case GPU_STENCIL_OP_REPLACE:
      result << "GPU_STENCIL_OP_REPLACE";
      break;
    case GPU_STENCIL_OP_COUNT_DEPTH_PASS:
      result << "GPU_STENCIL_OP_COUNT_DEPTH_PASS";
      break;
    case GPU_STENCIL_OP_COUNT_DEPTH_FAIL:
      result << "GPU_STENCIL_OP_COUNT_DEPTH_FAIL";
      break;
    default:
      BLI_assert_unreachable();
  }
  /* Provoking vertex */
  result << ",\n         ";
  switch (shaders.state.provoking_vert) {
    case GPU_VERTEX_FIRST:
      result << "GPU_VERTEX_FIRST";
      break;
    case GPU_VERTEX_LAST:
      result << "GPU_VERTEX_LAST";
      break;
    default:
      BLI_assert_unreachable();
  }
  result << ")\n";
  /* viewports */
  result << "  .viewports(" << shaders.viewport_count << ")\n";
  /* Depth format */
  if (fragment_out.depth_attachment_format != VK_FORMAT_UNDEFINED) {
    result << "  .depth_format(gpu::TextureTargetFormat::"
           << to_gpu_format_string(fragment_out.depth_attachment_format) << ")\n";
  }
  /* Stencil format */
  if (fragment_out.stencil_attachment_format != VK_FORMAT_UNDEFINED) {
    result << "  .stencil_format(gpu::TextureTargetFormat::"
           << to_gpu_format_string(fragment_out.stencil_attachment_format) << ")\n";
  }
  /* Color formats */
  for (const VkFormat format : fragment_out.color_attachment_formats) {
    result << "  .color_format(gpu::TextureTargetFormat::" << to_gpu_format_string(format)
           << ")\n";
  }
  result << ";";
  return result.str();
}
```

</details>

**结果出口**

- `return result.str();`

**继续追踪实现**

- `BLI_assert_unreachable` → [BLI_assert_unreachable · L77](../../../01-BLI基础库/BLI_assert.hh.md#m-7a2d91a67d8e)。宏定义由构建条件选择。
- `write_masks.append` → [blender::Vector::append · L498](../../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-5bde268a69e443ec)；[blender::Vector::append · L502](../../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-591e0b15e6308532)。同名重载需按实参类型选择。
- `write_masks.is_empty` → [blender::Vector::is_empty · L792](../../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-937bbd9cb80bdcc8)。
- `write_masks.last` → [blender::Vector::last · L749](../../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-d32e1fd895e766b4)；[blender::Vector::last · L755](../../../../01-基础容器与现代CPP/11-Vector插入删除与重排.md#f-66b262993c080d9d)。同名重载需按实参类型选择。
- `to_gpu_format_string` → [blender::gpu::to_gpu_format_string · L138](vk_common.cc.md#f-5c92afcb170f9e8a)。
- `result.str` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
