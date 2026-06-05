# Blender 几何节点列表(List)功能相关提交分析

> **注意**: 提交 `35a07467e0f60c1e2d21f9bd161cc328acd314d6` 在当前仓库中不存在。该仓库是本地克隆，可能缺少部分远程引用。以下分析基于所有可访问分支中的相关提交。

---

## 主分支(main)上的提交 — 按时间顺序

### 阶段1: 初始实现 (2025年7月)

| 提交 | 日期 | 描述 |
|------|------|------|
| [`4f372d64d44`](https://projects.blender.org/blender/blender/commit/4f372d64d44) | 2025-07-24 | **Geometry Nodes: Initial very basic list support** — 初始列表支持，包含 List、Get List Item、List Length 三个节点，隐藏在实验功能后 |

### 阶段2: 功能扩展 (2025年10月)

| 提交 | 日期 | 描述 |
|------|------|------|
| [`a60e0cd44b7`](https://projects.blender.org/blender/blender/commit/a60e0cd44b7) | 2025-10-08 | Geometry Nodes: Support lists and grids in more function nodes |
| [`4f4de01f797`](https://projects.blender.org/blender/blender/commit/4f4de01f797) | 2025-10-31 | Geometry Nodes: Support for baking lists of primitive values and bundles |
| [`132b55d2153`](https://projects.blender.org/blender/blender/commit/132b55d2153) | 2025-10-28 | Fix: Memory leak in currently unused Geometry Nodes list code |

### 阶段3: 节点重命名与清理 (2026年1月)

| 提交 | 日期 | 描述 |
|------|------|------|
| [`a6ff48575cc`](https://projects.blender.org/blender/blender/commit/a6ff48575cc) | 2026-01-16 | Fix #152050: Enable Output node don't keep List socket shape |
| [`0feaea2b9e7`](https://projects.blender.org/blender/blender/commit/0feaea2b9e7) | 2026-01-20 | Geometry Nodes: Remove list type restriction |
| [`1797d32181d`](https://projects.blender.org/blender/blender/commit/1797d32181d) | 2026-01-21 | **Change "List" to "Field to List"** — 重命名节点 |
| [`fd8306791bb`](https://projects.blender.org/blender/blender/commit/fd8306791bb) | 2026-01-28 | Various fixes for "Get List Item" node |
| [`f1e4c9fc997`](https://projects.blender.org/blender/blender/commit/f1e4c9fc997) | 2026-01-28 | Cleanup: make list data pointers const |
| [`14e50fcf993`](https://projects.blender.org/blender/blender/commit/14e50fcf993) | 2026-01-28 | Refactor: add convenience value accessors for lists |
| [`43f24ad0010`](https://projects.blender.org/blender/blender/commit/43f24ad0010) | 2026-01-28 | Cleanup: simplify constructing lists from containers |
| [`8d58228319f`](https://projects.blender.org/blender/blender/commit/8d58228319f) | 2026-01-28 | Cleanup: add List::copy method |

### 阶段4: 架构重构 (2026年4月)

| 提交 | 日期 | 描述 |
|------|------|------|
| [`d45c766353d`](https://projects.blender.org/blender/blender/commit/d45c766353d) | 2026-04-21 | Fix: Check for invalid list type in link-drag-search |
| [`ba8781fe300`](https://projects.blender.org/blender/blender/commit/ba8781fe300) | 2026-04-21 | Fix: Implement missing data ownership for lists |
| [`7725f1b61b3`](https://projects.blender.org/blender/blender/commit/7725f1b61b3) | 2026-04-29 | **Refactor: Split List into typed List and GList** — 核心架构变更 |
| [`273ee80a021`](https://projects.blender.org/blender/blender/commit/273ee80a021) | 2026-04-30 | **Move lists out of experimental** — 列表功能正式启用 |
| [`f0ecd72f38c`](https://projects.blender.org/blender/blender/commit/f0ecd72f38c) | 2026-04-30 | Refactor: improve ListPtr implementation |

### 阶段5: 新节点与Bug修复 (2026年5月)

| 提交 | 日期 | 描述 |
|------|------|------|
| [`21a2b1341f5`](https://projects.blender.org/blender/blender/commit/21a2b1341f5) | 2026-05-18 | Fix: viewer node crash with geometry list |
| [`fc2eb36d03c`](https://projects.blender.org/blender/blender/commit/fc2eb36d03c) | 2026-05-18 | Fix: viewer node crash with geometry list (second fix) |
| [`207d331f708`](https://projects.blender.org/blender/blender/commit/207d331f708) | 2026-05-21 | **Geometry Nodes: Filter List node** — 新增过滤列表节点 |
| [`f6ae6f7368a`](https://projects.blender.org/blender/blender/commit/f6ae6f7368a) | 2026-05-27 | Support empty exclusion list in Transfer Attributes node |
| [`e7e84d44608`](https://projects.blender.org/blender/blender/commit/e7e84d44608) | 2026-05-28 | **Geometry Nodes: Closure to List node** — 新增闭包转列表节点 |
| [`a62bcf847a3`](https://projects.blender.org/blender/blender/commit/a62bcf847a3) | 2026-06-03 | **Geometry Nodes: Sort List node** — 新增排序列表节点，从 Sort Elements 提取共享排序算法 |

---

## 演变路径总结

```
4f372d64d44  (2025-07-24) Initial List support: List + Get List Item + List Length
    │
    ├── a60e0cd44b7  (2025-10-08) Support lists in more function nodes
    ├── 4f4de01f797  (2025-10-31) Support baking lists
    │
    ├── 1797d32181d  (2026-01-21) Rename "List" → "Field to List" (在main上)
    ├── 7725f1b61b3  (2026-04-29) Split List → typed List + GList (核心架构重构)
    ├── 273ee80a021  (2026-04-30) Move lists out of experimental
    │
    ├── 207d331f708  (2026-05-21) Filter List node (新节点)
    ├── e7e84d44608  (2026-05-28) Closure to List node (新节点)
    └── a62bcf847a3  (2026-06-03) Sort List node (新节点，共享排序算法)
```

---

## 主要修改/新增文件

### 节点实现文件

| 文件路径 | 说明 |
|----------|------|
| `source/blender/nodes/geometry/nodes/node_geo_list.cc` | 原始 List 节点实现（后拆分） |
| `source/blender/nodes/geometry/nodes/node_geo_field_to_list.cc` | "Field to List" 节点（由 List 重命名） |
| `source/blender/nodes/geometry/nodes/node_geo_list_get_item.cc` | "Get List Item" 节点 |
| `source/blender/nodes/geometry/nodes/node_geo_list_length.cc` | "List Length" 节点 |
| `source/blender/nodes/geometry/nodes/node_geo_closure_to_list.cc` | "Closure to List" 节点（新增） |
| `source/blender/nodes/geometry/nodes/node_geo_sort_list.cc` | "Sort List" 节点（新增） |
| `source/blender/nodes/geometry/nodes/node_geo_items_to_list.cc` | "Items to List" 节点（新增） |

### 核心实现文件

| 文件路径 | 说明 |
|----------|------|
| `source/blender/nodes/intern/geometry_nodes_list.cc` | 列表核心实现 |
| `source/blender/nodes/intern/list_function_eval.cc` | 列表函数求值 |
| `source/blender/nodes/intern/list_function_eval.hh` | 列表函数求值头文件 |
| `source/blender/nodes/NOD_geometry_nodes_list.hh` | 列表节点声明头文件 |
| `source/blender/nodes/NOD_geometry_nodes_list_fwd.hh` | 列表节点前向声明 |

### 内核与数据结构

| 文件路径 | 说明 |
|----------|------|
| `source/blender/blenkernel/intern/node_socket_value.cc` | 节点 Socket 值处理 |
| `source/blender/blenkernel/intern/node_tree_update.cc` | 节点树更新逻辑 |
| `source/blender/blenkernel/intern/node_tree_structure_type_inferencing.cc` | 结构类型推断 |
| `source/blender/makesdna/DNA_node_tree_interface_types.h` | 节点树接口 DNA 定义 |
| `source/blender/makesdna/DNA_node_types.h` | 节点 DNA 定义 |
| `source/blender/makesdna/DNA_userdef_types.h` | 用户偏好 DNA 定义 |
| `source/blender/makesrna/intern/rna_nodetree.cc` | 节点树 RNA 定义 |
| `source/blender/makesrna/intern/rna_node_tree_interface.cc` | 节点树接口 RNA 定义 |
| `source/blender/makesrna/intern/rna_userdef.cc` | 用户偏好 RNA 定义 |

### UI 与着色器

| 文件路径 | 说明 |
|----------|------|
| `scripts/startup/bl_ui/node_add_menu_geometry.py` | 几何节点添加菜单 |
| `scripts/startup/bl_ui/space_userpref.py` | 用户偏好界面 |
| `source/blender/editors/space_node/node_socket_tooltip.cc` | 节点 Socket 提示 |
| `source/blender/gpu/shaders/gpu_shader_2D_node_socket_frag.glsl` | GPU 节点 Socket 着色器 |

### 修改器与测试

| 文件路径 | 说明 |
|----------|------|
| `source/blender/modifiers/intern/MOD_nodes.cc` | 节点修改器 |
| `source/blender/nodes/CMakeLists.txt` | 节点 CMake 配置 |
| `source/blender/nodes/geometry/CMakeLists.txt` | 几何节点 CMake 配置 |
| `source/blender/nodes/NOD_geometry_exec.hh` | 几何节点执行头文件 |
| `source/blender/nodes/NOD_geometry_nodes_log.hh` | 几何节点日志头文件 |
| `source/blender/nodes/NOD_geometry_nodes_values.hh` | 几何节点值头文件 |
| `tests/filesystem/node_group_tests/geometry_nodes/list/*.blend` | 测试文件 |
| `tests/python/CMakeLists.txt` | 测试 CMake 配置 |
