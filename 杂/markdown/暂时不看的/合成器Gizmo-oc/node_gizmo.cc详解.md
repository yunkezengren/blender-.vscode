这是一份关于 Blender 节点编辑器中 **2D Gizmo (交互饰件/小部件)** 的实现代码,主要用于在合成器(Compositor)的背景图(Backdrop)上直接操作节点参数(如移动遮罩、裁剪图像等).

下面是逐行/逐块的详细解释,包含代码翻译和逻辑说明.

### 📚 术语简洁翻译对照 (Concise Translations)

*   **Gizmo**: 饰件 / 小部件 / 交互手柄 / 控件
*   **Backdrop**: 背景图 / 背景板 / 幕布
*   **Socket**: 接口 / 插座 / 端口 / 节点输入输出
*   **Poll**: 轮询 / 检查 / 激活判定
*   **Callback**: 回调函数 / 钩子
*   **Matrix**: 矩阵 / 变换矩阵
*   **Bounding Box (BBox)**: 边界框 / 包围盒
*   **Compositor**: 合成器 / 后期合成

---

### 1. 文件头与包含库 (Includes)

```cpp
/* SPDX-FileCopyrightText: 2023 Blender Authors
 * SPDX-License-Identifier: GPL-2.0-or-later */
```
📄 **解释**: 版权声明,遵循 GPL-2.0 或更高版本协议.

```cpp
/** \file
 * \ingroup spnode
 */
```
📂 **解释**: Doxygen 文档标记,表明此文件属于 `spnode` (Space Node, 节点编辑器空间)组.

```cpp
#include <cmath>
// ... (包含一系列 BLI 头文件)
#include "BLI_listbase.h"       // 🔧 链表操作
#include "BLI_math_matrix.h"    // 🧮 矩阵运算
#include "BLI_math_rotation.h"  // 🔄 旋转计算
#include "BLI_math_vector.h"    // 📐 向量运算
#include "BLI_rect.h"           // 📦 矩形区域定义
#include "BLI_string.h"         // 📝 字符串操作
#include "BLI_utildefines.h"    // ⚙️ 通用定义
```
🧱 **解释**: 引入 Blender 基础库 (BLI),用于处理数学、数据结构等底层操作.

```cpp
#include "BKE_context.hh"       // 🌍 上下文访问 (获取当前场景、编辑器等)
#include "BKE_image.hh"         // 🖼️ 图像数据处理
#include "BKE_node_runtime.hh"  // 🧩 节点运行时数据
```
🧠 **解释**: 引入 Blender 内核库 (BKE),处理核心数据结构.

```cpp
#include "ED_gizmo_library.hh"  // 🎮 编辑器 Gizmo 库 (定义了基础的移动、旋转控件)
#include "ED_screen.hh"         // 🖥️ 屏幕/区域管理
```
🎨 **解释**: 引入编辑器库 (ED),用于 UI 交互和 Gizmo 系统.

```cpp
#include "IMB_imbuf_types.hh"   // 🎞️ 图像缓冲区类型
#include "MEM_guardedalloc.h"   // 💾 内存管理 (防泄漏分配器)
#include "RNA_access.hh"        // 🧬 RNA 属性访问 (Blender 的数据反射系统)
#include "RNA_prototypes.hh"    // 🧬 RNA 原型声明
#include "WM_types.hh"          // 🪟 窗口管理器类型
#include "node_intern.hh"       // 🔒 节点编辑器内部头文件
```
⚙️ **解释**: 其他必要的系统级头文件.

```cpp
namespace blender::ed::space_node {
```
🏷️ **解释**: 代码位于 `blender::ed::space_node` 命名空间下,避免命名冲突.

---

### 2. 本地工具函数 (Local Utilities)

#### 📐 计算 Gizmo 空间矩阵
```cpp
static void node_gizmo_calc_matrix_space(const SpaceNode *snode,
                                         const ARegion *region,
                                         float matrix_space[4][4])
{
  unit_m4(matrix_space); // 1️⃣ 初始化为单位矩阵
  mul_v3_fl(matrix_space[0], snode->zoom); // 2️⃣ 应用缩放 (X轴)
  mul_v3_fl(matrix_space[1], snode->zoom); // 2️⃣ 应用缩放 (Y轴)
  matrix_space[3][0] = (region->winx / 2) + snode->xof; // 3️⃣ 计算平移 X (屏幕中心 + 偏移)
  matrix_space[3][1] = (region->winy / 2) + snode->yof; // 3️⃣ 计算平移 Y
}
```
🧮 **解释**: 计算从节点视图空间到屏幕空间的变换矩阵. 让 Gizmo 跟随节点编辑器的缩放和平移.

#### 📐 考虑图像尺寸的矩阵计算
```cpp
static void node_gizmo_calc_matrix_space_with_image_dims(...)
{
  unit_m4(matrix_space);
  mul_v3_fl(matrix_space[0], snode->zoom * image_dims.x); // 1️⃣ 缩放包含图像尺寸
  mul_v3_fl(matrix_space[1], snode->zoom * image_dims.y);
  // 2️⃣ 计算平移,考虑了图像的中心点偏移和缩放
  matrix_space[3][0] = ((region->winx / 2) + snode->xof) -
                       ((image_dims.x / 2.0f - image_offset.x) * snode->zoom);
  matrix_space[3][1] = ((region->winy / 2) + snode->yof) -
                       ((image_dims.y / 2.0f - image_offset.y) * snode->zoom);
}
```
🖼️ **解释**: 专门用于那些依赖图像具体尺寸和偏移的 Gizmo (如 Glare 节点),确保 Gizmo 贴合在图像的正确像素位置上.

#### 👁️ 可见性检查
```cpp
static bool node_gizmo_is_set_visible(const bContext *C)
{
  // ... 获取 SpaceNode ...
  if ((snode->flag & SNODE_BACKDRAW) == 0) return false; // 1️⃣ 如果没开启背景图显示,返回 false
  if (!snode->edittree || snode->edittree->type != NTREE_COMPOSIT) return false; // 2️⃣ 必须是合成节点树
  // 3️⃣ 检查 Gizmo 是否被手动隐藏
  if (!(snode->gizmo_flag & (SNODE_GIZMO_HIDE | SNODE_GIZMO_HIDE_ACTIVE_NODE))) return true; 
  return false;
}
```
🕵️ **解释**: 判断是否应该显示 Gizmo. 必须开启 Backdrop 且当前是合成器模式.

#### 📏 安全尺寸计算
```cpp
static const float2 GIZMO_NODE_DEFAULT_DIMS{64.0f, 64.0f};
static float2 node_gizmo_safe_calc_dims(const ImBuf *ibuf, const float2 &fallback_dims)
{
  if (ibuf && ibuf->x > 0 && ibuf->y > 0) {
    return float2{float(ibuf->x), float(ibuf->y)}; // ✅ 有图像则返回图像尺寸
  }
  BLI_assert(!math::is_any_zero(fallback_dims));
  return fallback_dims; // 🛡️ 无图像则返回默认尺寸,防止除以零
}
```
🛡️ **解释**: 获取图像尺寸的辅助函数,防止空指针或零尺寸导致的崩溃.

---

### 3. 背景图变换 Gizmo (Backdrop Gizmo)

这部分控制背景图本身的缩放和平移.

```cpp
static void gizmo_node_backdrop_prop_matrix_get(...) 
{
  // ... (将 snode 的 zoom/xof/yof 转换为矩阵传给 Gizmo)
  matrix[0][0] = snode->zoom; 
  // ...
  matrix[3][0] = snode->xof;
}

static void gizmo_node_backdrop_prop_matrix_set(...) 
{
  // ... (Gizmo 移动后,将矩阵值写回 snode 的 zoom/xof/yof)
  snode->zoom = matrix[0][0];
  snode->xof = matrix[3][0];
}
```
🔄 **解释**: 这两个函数是数据绑定的桥梁(Getter/Setter). 使得 Gizmo 的移动直接修改 `snode` (节点空间) 的属性.

```cpp
static bool WIDGETGROUP_node_transform_poll(...) 
{
  // ... 
  if (node && node->is_type("CompositorNodeViewer")) return true; // ✅ 选中 Viewer 节点时激活
  return false;
}
```
🔍 **解释**: 激活条件检查. 只有当用户选中 "Viewer" 节点时,才显示调整背景图的框.

```cpp
static void WIDGETGROUP_node_transform_setup(...) 
{
  // ...
  wwrapper->gizmo = WM_gizmo_new("GIZMO_GT_cage_2d", gzgroup, nullptr); // ✨ 创建一个 2D 笼子(Cage)类型的 Gizmo
  RNA_enum_set(..., ED_GIZMO_CAGE_XFORM_FLAG_TRANSLATE | ED_GIZMO_CAGE_XFORM_FLAG_SCALE_UNIFORM); // 允许平移和等比缩放
  // ...
}
```
🛠️ **解释**: 初始化 Gizmo,设置它为一个可以平移和缩放的 2D 框.

```cpp
static void WIDGETGROUP_node_transform_refresh(...) 
{
  // ... 获取 Viewer 节点的图像 buffer ...
  Image *ima = BKE_image_ensure_viewer(...);
  // ... 计算尺寸 ...
  // ... 设置 Gizmo 属性 ...
  WM_gizmo_target_property_def_func(cage, "matrix", &params); // 🔗 绑定 Getter/Setter 函数
}
```
🔄 **解释**: 每一帧刷新 Gizmo 的状态. 如果有图像,就让 Gizmo 贴合图像大小;如果没有图像,则隐藏.

---

### 4. 裁剪 Gizmo (Crop Gizmo)

用于 `CompositorNodeCrop` 节点.

```cpp
struct NodeBBoxWidgetGroup { ... }; // 定义裁剪 Gizmo 的数据结构
```

```cpp
static void node_input_to_rect(...) { ... } // 📥 将节点 Socket (X, Y, W, H) 转换为 0-1 范围的矩形
static void node_input_from_rect(...) { ... } // 📤 将 0-1 范围的矩形转换回像素值写入节点 Socket
```
🧮 **解释**: `Crop` 节点使用的是像素值,而 Gizmo 内部处理常归一化坐标或屏幕坐标,这两个函数负责数值转换.

```cpp
static void gizmo_node_crop_prop_matrix_set(...) 
{
  // ... 获取矩阵 ...
  // ... 调用 node_input_from_rect 写回节点 ...
  gizmo_node_bbox_update(crop_group); // 🔄 触发更新,让界面刷新
}
```
🖱️ **解释**: 用户拖动裁剪框时调用的回调,更新节点数值.

```cpp
static bool WIDGETGROUP_node_crop_poll(...) 
{
  // ...
  if (!node || !node->is_type("CompositorNodeCrop")) return false; // 必须是 Crop 节点
  // ... 检查 Socket 链接状态 ...
  // 如果 "Alpha Crop" 被激活且没有链接输入,则允许操作(因为此时尺寸是固定的)
}
```
🔍 **解释**: 只有选中 Crop 节点且条件满足(例如不是全自动裁剪模式)时才显示.

---

### 5. 遮罩 Gizmo (Box Mask & Ellipse Mask)

用于 `CompositorNodeBoxMask` 和 `CompositorNodeEllipseMask` 节点.

```cpp
static void gizmo_node_box_mask_prop_matrix_get(...) 
{
  // ...
  // 读取 Position, Size, Rotation Socket 的值
  // 结合背景图的偏移和缩放,计算出 Gizmo 在屏幕上的矩阵
  loc_rot_size_to_mat4(matrix, loc, rot, size);
}
```
📥 **解释**: 将遮罩节点的数据读取到 Gizmo 中.

```cpp
static void gizmo_node_box_mask_prop_matrix_set(...) 
{
  // ...
  // 从 Gizmo 矩阵反解出 loc, rot, size
  // 写入 Position, Size, Rotation Socket
  // 特别注意: 只有当尺寸不为0时才计算旋转,避免数学错误
}
```
📤 **解释**: 将 Gizmo 的操作结果写回遮罩节点.

```cpp
static void WIDGETGROUP_node_box_mask_setup(...) 
{
  // ...
  // 允许 平移、旋转、缩放
  RNA_enum_set(..., ED_GIZMO_CAGE_XFORM_FLAG_TRANSLATE | ..._ROTATE | ..._SCALE);
  // 显示中心点手柄和角手柄
  RNA_enum_set(..., ED_GIZMO_CAGE_DRAW_FLAG_XFORM_CENTER_HANDLE | ..._CORNER_HANDLES);
}
```
🛠️ **解释**: 设置 Box Mask 的交互方式.

```cpp
// ... Ellipse Mask 部分类似 ...
RNA_enum_set(mask_group->border->ptr, "draw_style", ED_GIZMO_CAGE2D_STYLE_CIRCLE); // ⚪ 区别在于绘制风格设为圆形
```
🎨 **解释**: 椭圆遮罩使用圆形的绘制风格,但底层逻辑(位置/旋转/缩放)与方块遮罩几乎一致.

---

### 6. 眩光 Gizmo (Glare)

用于 `CompositorNodeGlare` (仅限 Sun Beams 模式).

```cpp
static bool WIDGETGROUP_node_glare_poll(...) 
{
  // ...
  // 检查 Type 是否为 SUN_BEAMS (日辉/光束)
  if (type_socket... != CMP_NODE_GLARE_SUN_BEAMS) return false;
  // ...
}
```
🔍 **解释**: 只有在 Glare 节点选为 "Sun Beams" 模式时,才需要一个点来控制太阳位置.

```cpp
static void WIDGETGROUP_node_glare_setup(...) 
{
  // ...
  glare_group->gizmo = WM_gizmo_new("GIZMO_GT_move_3d", ...); // 使用 3D 移动 Gizmo (即使是在 2D 中)
  RNA_enum_set(gz->ptr, "draw_style", ED_GIZMO_MOVE_STYLE_CROSS_2D); // ❌ 样式设为 2D 十字准星
}
```
🛠️ **解释**: 创建一个十字准星,用于定位光源中心.

```cpp
static void WIDGETGROUP_node_glare_refresh(...) 
{
  // ...
  // 直接绑定 "Sun Position" Socket 到 Gizmo 的 offset 属性
  WM_gizmo_target_property_def_rna(gz, "offset", &socket_pointer, "default_value", -1);
}
```
🔗 **解释**: 利用 RNA 系统直接绑定,无需手写复杂的 Get/Set 回调,因为只是简单的 XY 坐标映射.

---

### 7. 边角定位 Gizmo (Corner Pin)

用于 `CompositorNodeCornerPin`.

```cpp
struct NodeCornerPinWidgetGroup {
  wmGizmo *gizmos[4]; // 4️⃣ 需要4个 Gizmo,对应4个角
  // ...
};
```
🧩 **解释**: Corner Pin 需要拉扯图像的四个角,所以管理了数组为 4 的 Gizmo 集合.

```cpp
static void WIDGETGROUP_node_corner_pin_refresh(...) 
{
  // ...
  for (bNodeSocket *sock = ...; sock && i < 4; sock = sock->next) {
    if (sock->type == SOCK_VECTOR) { // 找到前4个 Vector 类型的输入 (对应左上、右上等)
       // ... 绑定每个 Gizmo 到对应的 Socket ...
       WM_gizmo_target_property_def_rna(gz, "offset", &sockptr, "default_value", -1);
    }
  }
}
```
🔗 **解释**: 遍历节点的输入端口,动态绑定 4 个控制点.

---

### 8. 分屏 Gizmo (Split)

用于 `CompositorNodeSplit` (对比查看器).

```cpp
static void gizmo_node_split_prop_matrix_get(...) 
{
  // ...
  // 根据 Position 和 Rotation 计算分割线的位置和角度
  // 将其转换为一个极窄的矩形矩阵传给 Gizmo
  loc_rot_size_to_mat4(..., float3{gizmo_width, ..., 1.0f});
}
```
📏 **解释**: Split 节点本质上是一条线,但在 Gizmo 中被模拟为一个很窄的、可旋转平移的矩形 Cage.

```cpp
static void gizmo_node_split_prop_matrix_set(...) 
{
  // ...
  // 限制 Gizmo 不能移出图像范围
  pos_x = math::clamp(pos_x, 0.0f, dims.x);
  // ...
}
```
🛡️ **解释**: 增加边界检查,防止分割线跑到图像外面找不到了.

---

### 📝 总结
这个文件实现了 Blender 合成器中所有 **"所见即所得"** 的交互功能. 它通过监听特定的节点类型(Poll),并在背景图上绘制对应的控件(Setup/Draw),将用户的鼠标操作转换为节点 Socket 的数值变化(Get/Set callbacks).