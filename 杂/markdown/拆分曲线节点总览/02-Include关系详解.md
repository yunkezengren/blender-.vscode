# 拆分曲线节点 Include 关系详解

## 问题：为什么有些类需要显式 include，有些不需要？

## 完整 Include 链分析

### 文件中的 6 个显式 include

```cpp
#include "BLI_array_utils.hh"           // 需要
#include "BKE_attribute.hh"             // 需要
#include "BKE_curves.hh"                // 需要
#include "BKE_curves_utils.hh"          // 需要
#include "BKE_deform.hh"                // 需要
#include "BKE_grease_pencil.hh"         // 需要
#include "GEO_curves_remove_and_split.hh" // 需要
#include "GEO_foreach_geometry.hh"      // 需要
#include "node_geometry_util.hh"        // 基础框架
```

---

## 通过 `node_geometry_util.hh` 间接引入的类

### 引入链：
```
node_geometry_util.hh
├── BKE_node.hh
├── BKE_node_legacy_types.hh
├── BKE_node_socket_value.hh
├── NOD_geometry_exec.hh          ← 最重要的中转站
│   ├── FN_field.hh               ← Field, FieldContext
│   ├── FN_lazy_function.hh
│   ├── FN_multi_function_builder.hh
│   ├── BKE_attribute_filter.hh   ← AttributeFilter
│   ├── BKE_geometry_fields.hh    ← CurvesFieldContext
│   ├── BKE_geometry_set.hh       ← GeometrySet
│   └── ...
├── NOD_register.hh
├── NOD_socket_declarations.hh
├── NOD_socket_declarations_geometry.hh  ← NodeDeclarationBuilder
└── node_util.hh
```

### 因此自动获得的类（无需显式 include）：

| 类名 | 来源路径 |
|------|---------|
| `NodeDeclarationBuilder` | `NOD_socket_declarations_geometry.hh` |
| `GeoNodeExecParams` | `NOD_geometry_exec.hh` |
| `Field<bool>` | `FN_field.hh` |
| `FieldContext` | `FN_field.hh` |
| `FieldEvaluator` | `FN_field_evaluation.hh` (被 `FN_field.hh` 引入) |
| `GeometrySet` | `BKE_geometry_set.hh` |
| `GeometryComponent` | `BKE_geometry_set.hh` |
| `AttributeFilter` | `BKE_attribute_filter.hh` |
| `NodeAttributeFilter` | `NOD_geometry_exec.hh` |
| `CurvesFieldContext` | `BKE_geometry_fields.hh` |
| `GreasePencilLayerFieldContext` | `BKE_geometry_fields.hh` |
| `SocketValueVariant` | `BKE_node_socket_value.hh` |

---

## 需要显式 include 的情况分析

### 1. `BLI_array_utils.hh`

**原因**: 使用 `array_utils::copy` 和 `offset_indices::accumulate_counts_to_offsets`

```cpp
// 代码中使用：
array_utils::copy(dst_curve_counts.as_span(), new_curve_offsets.drop_back(1));
offset_indices::accumulate_counts_to_offsets(new_curve_offsets);
```

**为什么需要显式 include**:
- `BKE_curves.hh` 引入了 `BLI_array_utils.hh` 吗？检查：
- `BKE_curves.hh` 第 12 行：`#include "BLI_array_utils.hh"` ✓
- 但实际上 `array_utils` 命名空间的函数可能需要完整定义

**实际情况**: 虽然 `BKE_curves.hh` 引入了 `BLI_array_utils.hh`，但 `array_utils` 命名空间中的某些工具函数可能需要显式引入。

---

### 2. `BKE_attribute.hh`

**原因**: 使用 `bke::gather_attributes` 和 `AttrDomain`

```cpp
// 代码中使用：
bke::gather_attributes(src_attributes,
                       bke::AttrDomain::Curve,
                       bke::AttrDomain::Curve,
                       ...);
```

**为什么需要显式 include**:
- `NOD_geometry_exec.hh` 引入了 `BKE_geometry_fields.hh`
- `BKE_geometry_fields.hh` 可能前向声明了 `AttrDomain` 但没有完整定义
- `gather_attributes` 函数定义在 `BKE_attribute.hh` 中

---

### 3. `BKE_curves.hh`

**原因**: `bke::CurvesGeometry` 的完整定义

**为什么需要显式 include**:
- 虽然可能通过其他头文件前向声明了 `CurvesGeometry`
- 但节点实现需要调用 `CurvesGeometry` 的方法（如 `points_by_curve()`, `attributes_for_write()` 等）
- 需要完整类定义而不仅是前向声明

---

### 4. `BKE_curves_utils.hh` 和 `BKE_deform.hh`

**原因**: 使用 `BKE_defgroup_copy_list`

```cpp
// 代码中使用：
BKE_defgroup_copy_list(&dst_curves.vertex_group_names, &src_curves.vertex_group_names);
```

**为什么需要显式 include**:
- 这是具体的工具函数，不在核心类定义中
- 顶点组（vertex group）相关的功能

---

### 5. `BKE_grease_pencil.hh`

**原因**: `GreasePencil` 和 `Drawing` 类的完整定义

```cpp
// 代码中使用：
if (GreasePencil *grease_pencil = geometry_set.get_grease_pencil_for_write()) {
    Drawing *drawing = grease_pencil->get_eval_drawing(...);
    drawing->strokes_for_write() = std::move(dst_curves);
    drawing->tag_topology_changed();
}
```

**为什么需要显式 include**:
- 需要调用 `Drawing` 类的方法
- 需要 `GreasePencil` 的完整定义

---

### 6. `GEO_curves_remove_and_split.hh`

**原因**: 使用 `geometry::remove_points_and_split`

```cpp
// 代码中使用：
dst_curves = geometry::remove_points_and_split(src_curves, selection);
```

**为什么需要显式 include**:
- 这是 `geometry` 命名空间中的独立函数
- 不属于任何核心类的成员

---

### 7. `GEO_foreach_geometry.hh`

**原因**: 使用 `geometry::foreach_real_geometry`

```cpp
// 代码中使用：
geometry::foreach_real_geometry(geometry_set, [&](GeometrySet &geometry_set) {
    // ...
});
```

**为什么需要显式 include**:
- 独立的工具函数
- 用于遍历实例化几何

---

## Include 决策流程图

```
使用某个类/函数时：
    │
    ▼
是否需要完整类定义（调用方法/访问成员）？
    │
    ├── 是 → 该类定义在哪个头文件？
    │         │
    │         ├── 是否已被 node_geometry_util.hh 间接引入？
    │         │       │
    │         │       ├── 是 → 可能不需要显式 include
    │         │       │       （但如果使用特定命名空间的函数，仍可能需要）
    │         │       │
    │         │       └── 否 → 必须显式 include
    │         │
    │         └── 检查前向声明是否足够
    │
    └── 否（只需要指针/引用）→ 使用前向声明即可
```

---

## 实际检查：BKE_curves.hh 引入了哪些文件？

```cpp
// BKE_curves.hh 的 includes:
#include "BLI_array_utils.hh"           // array_utils::copy
#include "BLI_bounds_types.hh"
#include "BLI_implicit_sharing_ptr.hh"
#include "BLI_index_mask_fwd.hh"        // IndexMask 前向声明
#include "BLI_math_matrix_types.hh"
#include "BLI_math_vector_types.hh"
#include "BLI_memory_counter_fwd.hh"
#include "BLI_offset_indices.hh"        // OffsetIndices
#include "BLI_shared_cache.hh"
#include "BLI_span.hh"                  // Span, MutableSpan
#include "BLI_vector.hh"                // Vector
#include "BLI_virtual_array_fwd.hh"     // VArray 前向声明

#include "BKE_attribute_math.hh"
#include "BKE_attribute_storage.hh"
#include "BKE_curves.h"                 // C 结构体定义
```

### 结论：

| 头文件 | 是否被 BKE_curves.hh 引入 | 是否被 node_geometry_util.hh 引入 | 是否需要显式 include |
|--------|--------------------------|----------------------------------|---------------------|
| `BLI_array_utils.hh` | ✓ | ? | 是（使用特定函数） |
| `BLI_span.hh` | ✓ | ? | 否 |
| `BLI_vector.hh` | ✓ | ? | 否 |
| `BLI_offset_indices.hh` | ✓ | ? | 否 |
| `BKE_attribute.hh` | ✗ | ? | 是（需要 gather_attributes） |
| `BKE_curves.hh` | - | ? | 是（核心依赖） |
| `BKE_grease_pencil.hh` | ✗ | ? | 是 |
| `GEO_*.hh` | ✗ | ✗ | 是 |

---

## 最佳实践总结

### 1. 基础框架头文件
```cpp
#include "node_geometry_util.hh"  // 必须，提供节点基础框架
```

### 2. 几何数据头文件
```cpp
#include "BKE_curves.hh"          // 如果使用 CurvesGeometry
#include "BKE_grease_pencil.hh"   // 如果使用 GreasePencil
#include "BKE_mesh.hh"            // 如果使用 Mesh
#include "BKE_pointcloud.hh"      // 如果使用 PointCloud
```

### 3. 属性系统头文件
```cpp
#include "BKE_attribute.hh"       // 如果需要 gather_attributes 等函数
```

### 4. 几何工具头文件
```cpp
#include "GEO_*.hh"               // 使用具体的几何算法
```

### 5. 工具头文件
```cpp
#include "BLI_array_utils.hh"     // 数组工具函数
#include "BLI_math_*.hh"          // 数学工具
```

---

## 常见模式

### 最小节点模板

```cpp
/* SPDX-FileCopyrightText: 2026 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

#include "node_geometry_util.hh"  // 基础框架

// 根据需要使用：
// #include "BKE_curves.hh"
// #include "BKE_mesh.hh"
// #include "BKE_attribute.hh"
// #include "GEO_*.hh"

namespace blender::nodes::node_geo_example_cc {

static void node_declare(NodeDeclarationBuilder &b)
{
    b.add_input<decl::Geometry>("Geometry"_ustr);
    b.add_output<decl::Geometry>("Geometry"_ustr);
}

static void node_geo_exec(GeoNodeExecParams params)
{
    GeometrySet geometry_set = params.extract_input<GeometrySet>("Geometry"_ustr);
    // ... 处理逻辑 ...
    params.set_output("Geometry"_ustr, std::move(geometry_set));
}

static void node_register()
{
    static bke::bNodeType ntype;
    geo_node_type_base(&ntype, "GeometryNodeExample"_ustr);
    ntype.ui_name = "Example";
    ntype.nclass = NODE_CLASS_GEOMETRY;
    ntype.declare = node_declare;
    ntype.geometry_node_execute = node_geo_exec;
    bke::node_register_type(ntype);
}
NOD_REGISTER_NODE(node_register)

}  // namespace blender::nodes::node_geo_example_cc
```
