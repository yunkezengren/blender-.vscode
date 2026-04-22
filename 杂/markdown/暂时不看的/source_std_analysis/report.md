# Blender 源码 std:: 使用详细报告

## 执行摘要

| 指标 | 数值 |
|------|------|
| 分析路径 | source/blender/ |
| 总匹配数 | 23,012 |

## 目录分布 (Top 20)

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
| freestyle | 201 |
| bmesh | 193 |
| blenloader | 178 |
| depsgraph | 177 |
| sequencer | 175 |

## 文件分布 (Top 30)

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
| editors/interface/regions/interface_region_tooltip.cc | 75 |
| blenkernel/intern/bake_items_socket.cc | 74 |
| modifiers/intern/MOD_nodes.cc | 73 |
| blenlib/BLI_map.hh | 72 |
| functions/FN_multi_function_builder.hh | 70 |
| draw/intern/draw_command.cc | 70 |
| blenkernel/intern/grease_pencil.cc | 70 |
| compositor/cached_resources/intern/van_vliet_gaussian_coefficients.cc | 67 |
| blenlib/tests/BLI_map_test.cc | 67 |
| editors/grease_pencil/intern/grease_pencil_edit.cc | 65 |

## 组件使用频率 (Top 50)

| 组件 | 使用次数 |
|------|----------|
| std::string | 5031 |
| std::optional | 3220 |
| std::nullopt | 2383 |
| std::move | 1705 |
| std::unique_ptr | 1353 |
| std::max | 1003 |
| std::min | 736 |
| std::make_unique | 716 |
| std::cout | 690 |
| std::array | 653 |
| std::swap | 417 |
| std::endl | 356 |
| std::vector | 336 |
| std::shared_ptr | 334 |
| std::ostream | 298 |
| std::pair | 294 |
| std::stringstream | 265 |
| std::numeric_limits | 246 |
| std::get | 237 |
| std::clamp | 227 |
| std::make_shared | 223 |
| std::to_string | 199 |
| std::is_same_v | 194 |
| std::lock_guard | 167 |
| std::forward | 148 |
| std::get_if | 146 |
| std::scoped_lock | 138 |
| std::atomic | 137 |
| std::function | 129 |
| std::sort | 108 |
| std::string_view | 101 |
| std::abs | 98 |
| std::cerr | 84 |
| std::string::npos | 81 |
| std::memory_order_relaxed | 77 |
| std::complex | 76 |
| std::variant | 75 |
| std::any_of | 68 |
| std::byte | 61 |
| std::decay_t | 55 |
| std::sqrt | 52 |
| std::holds_alternative | 50 |
| std::destroy_at | 50 |
| std::unique_lock | 42 |
| std::reference_wrapper | 38 |
| std::all_of | 34 |
| std::mutex | 33 |
| std::is_same | 33 |
| std::visit | 32 |
| std::is_void_v | 31 |

---
报告由 OpenCode 自动生成
