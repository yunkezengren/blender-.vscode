# Blender 源码 std:: 使用分析报告（智能分类版）

## 执行摘要

| 指标 | 数值 |
|------|------|
| 分析路径 | source/blender/ |
| 总匹配数 | 23,012 |
| 原始组件数 | 402 |
| 分类后类别数 | 162 |

## 目录分布 (Top 15)

| 目录 | 使用次数 |
|------|----------|
| editors | 4900 |
| blenkernel | 3537 |
| blenlib | 2992 |
| nodes | 2866 |
| gpu | 1607 |
| io | 1313 |
| modifiers | 791 |
| draw | 772 |
| makesrna | 649 |
| geometry | 416 |
| asset_system | 367 |
| functions | 330 |
| compositor | 322 |
| windowmanager | 251 |
| imbuf | 232 |

## 智能分类统计 (Top 30)

| 分类 | 使用次数 | 说明 |
|------|----------|------|
| std::string  | 5121  | 见详细映射 |
| std::optional  | 3220  | 见详细映射 |
| std::algorithms  | 2973  | 见详细映射 |
| std::nullopt  | 2383  | 见详细映射 |
| std::move  | 1705  | 见详细映射 |
| std::memory  | 1427  | 见详细映射 |
| std::unique_ptr  | 1353  | 见详细映射 |
| std::cout  | 690  | 见详细映射 |
| std::array  | 653  | 见详细映射 |
| std::type_traits  | 612  | 见详细映射 |
| std::endl  | 356  | 见详细映射 |
| std::vector  | 346  | 见详细映射 |
| std::math  | 339  | 见详细映射 |
| std::shared_ptr  | 334  | 见详细映射 |
| std::ostream  | 298  | 见详细映射 |
| std::pair  | 294  | 见详细映射 |
| std::stringstream  | 265  | 见详细映射 |
| std::numeric_limits  | 246  | 见详细映射 |
| std::string_conversion  | 208  | 见详细映射 |
| std::lock_guard  | 167  | 见详细映射 |
| std::utility  | 162  | 见详细映射 |
| std::scoped_lock  | 138  | 见详细映射 |
| std::atomic  | 137  | 见详细映射 |

## 大类汇总

| 类别 | 总使用次数 | 包含组件 |
|------|----------|----------|
| 容器类 | 6,292 | string, vector, array, map, unordered_map 等 |
| 实用工具 | 3,621 | optional, variant, any, tuple, pair 等 |
| 算法 | 2,973 | sort, max, min, swap, clamp, copy 等 |
| 内存管理 | 1,427 | make_unique, make_shared, addressof 等 |
| 智能指针 | 1,693 | unique_ptr, shared_ptr, weak_ptr |
| 类型萃取 | 612 | is_same_v, enable_if_t, conditional_t 等 |
| IO流 | 574 | cout, cerr, ostream, stringstream 等 |
| 数学函数 | 339 | sqrt, abs, sin, cos, pow 等 |
| 并发 | 184 | lock_guard, atomic, thread 等 |
| 字符串 | 311 | string_view, to_string, stoi 等 |

## 文件分布 (Top 20)

| 文件 | 使用次数 |
|------|----------|
| blenlib/intern/mesh_boolean.cc | 306 |
| editors/interface/interface.cc | 204 |
| blenkernel/intern/bake_items_serialize.cc | 176 |
| blenlib/intern/mesh_intersect.cc | 166 |
| draw/tests/draw_pass_test.cc | 161 |
| gpu/vulkan/vk_to_string.cc | 128 |
| blenkernel/intern/idprop_serialize.cc | 120 |
| nodes/intern/geometry_nodes_lazy_function.cc | 112 |
| geometry/intern/mesh_boolean_manifold.cc | 104 |
| nodes/function/nodes/node_fn_format_string.cc | 100 |
| editors/space_node/node_draw.cc | 100 |
| editors/interface/interface_layout.cc | 96 |
| editors/space_spreadsheet/spreadsheet_data_source_geometry.cc | 95 |
| editors/sculpt_paint/mesh/sculpt.cc | 83 |
| editors/include/UI_interface_c.hh | 83 |
| editors/io/io_usd.cc | 82 |
| editors/sculpt_paint/mesh/sculpt_undo.cc | 78 |
| gpu/opengl/gl_shader.cc | 77 |
| blenlib/intern/delaunay_2d.cc | 77 |
| editors/geometry/node_group_operator.cc | 76 |

## 关键发现

1. **字符串处理最多**: `std::string` 相关共 5,121 次使用，是最常用的组件
2. **算法广泛使用**: 47种算法共 2,973 次，其中 `max`(1003次)、`min`(736次)、`swap`(417次) 最常用
3. **内存管理现代化**: `std::memory` 类别 1,427 次，大量使用 `make_unique`/`make_shared`
4. **类型萃取活跃**: 612 次类型萃取使用，显示大量使用模板元编程
5. **编辑器代码最多**: `editors/` 目录 4,900 次使用，其次是 `blenkernel/` 3,537 次

## 生成的文件

| 文件 | 说明 |
|------|------|
| `std_classified.txt` | 智能分类统计 |
| `std_classified.csv` | 分类统计 CSV |
| `std_classified_detail.txt` | 详细映射关系（每个分类包含哪些原始组件） |

---
*报告由 OpenCode 自动生成*
