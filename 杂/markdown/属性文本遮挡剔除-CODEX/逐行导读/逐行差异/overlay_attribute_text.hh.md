# `source/blender/draw/engines/overlay/overlay_attribute_text.hh`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文，并在修改行前加入中文注释与行号。
> 删除的旧行在原位置以注释显示；原始 diff 放在折叠区，方便核对。代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `文件局部上下文`

下面按源码顺序阅读本块的 6 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp

#pragma once

// 新第 11 行：加入直接依赖 `<algorithm>`，供本文件新用到的声明、容器或算法使用。
#include <algorithm>
// 新第 12 行：空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。

// 新第 13 行：加入直接依赖 `"BLI_array.hh"`，供本文件新用到的声明、容器或算法使用。
#include "BLI_array.hh"
#include "BLI_color.hh"
// 新第 15 行：加入直接依赖 `"BLI_math_geom_c.hh"`，供本文件新用到的声明、容器或算法使用。
#include "BLI_math_geom_c.hh"
// 新第 16 行：加入直接依赖 `"BLI_math_matrix.hh"`，供本文件新用到的声明、容器或算法使用。
#include "BLI_math_matrix.hh"
#include "BLI_math_quaternion_types.hh"
// 新第 18 行：加入直接依赖 `"BLI_math_vector.hh"`，供本文件新用到的声明、容器或算法使用。
#include "BLI_math_vector.hh"
#include "BLI_string_utf8.hh"

#include "DNA_curve_types.h"
```

<details>
<summary>核对本块原始 diff（6 条修改）</summary>

```diff
@@ -8,8 +8,14 @@
 
 #pragma once
 
+#include <algorithm>
+
+#include "BLI_array.hh"
 #include "BLI_color.hh"
+#include "BLI_math_geom_c.hh"
+#include "BLI_math_matrix.hh"
 #include "BLI_math_quaternion_types.hh"
+#include "BLI_math_vector.hh"
 #include "BLI_string_utf8.hh"
 
 #include "DNA_curve_types.h"
```

</details>

## 差异块 2 · `文件局部上下文`

下面按源码顺序阅读本块的 1 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
#include "BKE_geometry_set.hh"
#include "BKE_instances.hh"
#include "BKE_mesh.hh"
// 新第 29 行：加入直接依赖 `"BKE_object.hh"`，供本文件新用到的声明、容器或算法使用。
#include "BKE_object.hh"

#include "DRW_render.hh"

```

<details>
<summary>核对本块原始 diff（1 条修改）</summary>

```diff
@@ -20,6 +26,7 @@
 #include "BKE_geometry_set.hh"
 #include "BKE_instances.hh"
 #include "BKE_mesh.hh"
+#include "BKE_object.hh"
 
 #include "DRW_render.hh"
 
```

</details>

## 差异块 3 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 1 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  void begin_sync(Resources &res, const State &state) final
  {
    enabled_ = !res.is_selection() && state.show_attribute_viewer_text();
    // 新第 53 行：使用同名设置；Python 属性名、RNA 注册名与 C++ 查询函数分别处于不同层。
    occlusion_test_ = state.viewer_text_occlusion_culling();
  }

  void object_sync(Manager & /*manager*/,
```

<details>
<summary>核对本块原始 diff（1 条修改）</summary>

```diff
@@ -43,6 +50,7 @@ class AttributeTexts : Overlay {
   void begin_sync(Resources &res, const State &state) final
   {
     enabled_ = !res.is_selection() && state.show_attribute_viewer_text();
+    occlusion_test_ = state.viewer_text_occlusion_culling();
   }
 
   void object_sync(Manager & /*manager*/,
```

</details>

## 差异块 4 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 7 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
    if (ob_ref.preview_instance_index() >= 0) {
      const bke::Instances *instances = ob_ref.preview_base_geometry()->get_instances();
      if (instances->attributes().contains(".viewer")) {
        // 旧第 69 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
        // 原代码：add_instance_attributes_to_text_cache(
            // 旧第 70 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
            // 原代码：dt, instances->attributes(), object_to_world, ob_ref.preview_instance_index());
        // 新第 77 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
        add_instance_attributes_to_text_cache(state,
                                              // 新第 78 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                              instances->attributes(),
                                              // 新第 79 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                              object,
                                              // 新第 80 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                              object_to_world,
                                              // 新第 81 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                              ob_ref.preview_instance_index());

        return;
      }
```

<details>
<summary>核对本块原始 diff（7 条修改）</summary>

```diff
@@ -66,8 +74,11 @@ class AttributeTexts : Overlay {
     if (ob_ref.preview_instance_index() >= 0) {
       const bke::Instances *instances = ob_ref.preview_base_geometry()->get_instances();
       if (instances->attributes().contains(".viewer")) {
-        add_instance_attributes_to_text_cache(
-            dt, instances->attributes(), object_to_world, ob_ref.preview_instance_index());
+        add_instance_attributes_to_text_cache(state,
+                                              instances->attributes(),
+                                              object,
+                                              object_to_world,
+                                              ob_ref.preview_instance_index());
 
         return;
       }
```

</details>

## 差异块 5 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 2 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
      }
      case OB_POINTCLOUD: {
        const PointCloud &pointcloud = DRW_object_get_data_for_drawing<PointCloud>(object);
        // 旧第 84 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
        // 原代码：add_attributes_to_text_cache(dt, pointcloud.attributes(), object_to_world);
        // 新第 95 行：点云改用专门入口，以便读取每点半径并把文字锚点移到圆盘前方。
        add_pointcloud_attributes_to_text_cache(state, pointcloud, object_to_world);
        break;
      }
      case OB_CURVES_LEGACY: {
```

<details>
<summary>核对本块原始 diff（2 条修改）</summary>

```diff
@@ -81,7 +92,7 @@ class AttributeTexts : Overlay {
       }
       case OB_POINTCLOUD: {
         const PointCloud &pointcloud = DRW_object_get_data_for_drawing<PointCloud>(object);
-        add_attributes_to_text_cache(dt, pointcloud.attributes(), object_to_world);
+        add_pointcloud_attributes_to_text_cache(state, pointcloud, object_to_world);
         break;
       }
       case OB_CURVES_LEGACY: {
```

</details>

## 差异块 6 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 40 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  }

 private:
  // 新第 118 行：保留源码说明：When the Overlay option is enabled, anchor positions are tested against the；相邻代码的中文推导见专题章节。
  /* When the Overlay option is enabled, anchor positions are tested against the scene
   // 新第 119 行：保留源码说明：depth buffer while drawing, so text hidden behind geometry is skipped. The ；相邻代码的中文推导见专题章节。
   * depth buffer while drawing, so text hidden behind geometry is skipped. The test itself
   // 新第 120 行：保留源码说明：happens in #DRW_text_cache_draw and works for every geometry type (mesh, po；相邻代码的中文推导见专题章节。
   * happens in #DRW_text_cache_draw and works for every geometry type (mesh, point cloud,
   // 新第 121 行：保留源码说明：instances, curves...).；相邻代码的中文推导见专题章节。
   * instances, curves...). */
  // 新第 122 行：保存本帧是否要求遮挡测试，供后续锚点准备和文字标志传播使用。
  bool occlusion_test_ = false;
// 新第 123 行：空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。

  // 新第 124 行：点云改用专门入口，以便读取每点半径并把文字锚点移到圆盘前方。
  void add_pointcloud_attributes_to_text_cache(const State &state,
                                               // 新第 125 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                               const PointCloud &pointcloud,
                                               // 新第 126 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                               const float4x4 &object_to_world)
  // 新第 127 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
  {
    // 新第 128 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
    const bke::AttributeAccessor attributes = pointcloud.attributes();
    // 新第 129 行：用条件保护后续步骤，阻止无效数据、越界或不满足要求的绘制路径。
    if (!attributes.contains(".viewer")) {
      // 新第 130 行：提前结束当前分支，避免继续处理不适用的对象或候选。
      return;
    // 新第 131 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
    }
    // 新第 132 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
    const bke::GAttributeReader attribute = attributes.lookup(".viewer");
    // 新第 133 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
    const Span<float3> positions = pointcloud.positions();
    // 新第 134 行：使用组件级遮挡开关，决定是否调整锚点或给文字附加测试标志。
    if (!occlusion_test_) {
      // 新第 135 行：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
      add_values_to_text_cache(state.dt, attribute.varray, positions, object_to_world);
      // 新第 136 行：提前结束当前分支，避免继续处理不适用的对象或候选。
      return;
    // 新第 137 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
    }
// 新第 138 行：空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。

    // 新第 139 行：点云中心在自身有半径的圆盘后方，应为每个点前移锚点。
    /* Match the world-space radius used by point-cloud drawing. A center anchor is behind its
     // 新第 140 行：点云中心在自身有半径的圆盘后方，应为每个点前移锚点。
     * own camera-facing disk, so move each label to the front of its own point. */
    // 新第 141 行：取得逐点半径；每条点云文字使用它对应点自己的半径。
    const VArray<float> radii = pointcloud.radius();
    // 新第 142 行：点云中心在自身有半径的圆盘后方，应为每个点前移锚点。
    /* Root-mean-square object scale, matching the point-cloud shader. */
    // 新第 143 行：把对象三个轴的缩放折合为点云 shader 使用的世界半径尺度。
    const float radius_scale = math::length(math::to_scale(object_to_world)) * 0.577350269f;
    // 新第 144 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
    const bool is_perspective = state.rv3d != nullptr && state.rv3d->is_persp;
    // 新第 145 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
    Array<float3> anchors(positions.size());
    // 新第 146 行：逐个处理集合元素；上方专题说明循环对象与成本。
    for (const int i : positions.index_range()) {
      // 新第 147 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
      const float3 center = math::transform_point(object_to_world, positions[i]);
      // 新第 148 行：透视从点指向相机位置；正交使用统一观察方向。
      const float3 to_camera = is_perspective ? state.camera_position - center :
                                                // 新第 149 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                                state.camera_forward;
      // 新第 150 行：透视从点指向相机位置；正交使用统一观察方向。
      const float distance = math::length(to_camera);
      // 新第 151 行：透视从点指向相机位置；正交使用统一观察方向。
      const float3 direction = distance > 1.0e-20f ? to_camera / distance : state.camera_forward;
      // 新第 152 行：把对象三个轴的缩放折合为点云 shader 使用的世界半径尺度。
      anchors[i] = center + direction * (std::max(radii[i], 0.0f) * radius_scale);
    // 新第 153 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
    }
    // 新第 154 行：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
    add_values_to_text_cache(
        // 新第 155 行：锚点已在世界空间，传单位矩阵避免公共函数重复应用对象变换。
        state.dt, attribute.varray, anchors.as_span(), float4x4::identity(), true);
  // 新第 156 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
  }
// 新第 157 行：空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。

  void add_attributes_to_text_cache(DRWTextStore *dt,
                                    bke::AttributeAccessor attribute_accessor,
                                    const float4x4 &object_to_world)
```

<details>
<summary>核对本块原始 diff（40 条修改）</summary>

```diff
@@ -104,6 +115,46 @@ class AttributeTexts : Overlay {
   }
 
  private:
+  /* When the Overlay option is enabled, anchor positions are tested against the scene
+   * depth buffer while drawing, so text hidden behind geometry is skipped. The test itself
+   * happens in #DRW_text_cache_draw and works for every geometry type (mesh, point cloud,
+   * instances, curves...). */
+  bool occlusion_test_ = false;
+
+  void add_pointcloud_attributes_to_text_cache(const State &state,
+                                               const PointCloud &pointcloud,
+                                               const float4x4 &object_to_world)
+  {
+    const bke::AttributeAccessor attributes = pointcloud.attributes();
+    if (!attributes.contains(".viewer")) {
+      return;
+    }
+    const bke::GAttributeReader attribute = attributes.lookup(".viewer");
+    const Span<float3> positions = pointcloud.positions();
+    if (!occlusion_test_) {
+      add_values_to_text_cache(state.dt, attribute.varray, positions, object_to_world);
+      return;
+    }
+
+    /* Match the world-space radius used by point-cloud drawing. A center anchor is behind its
+     * own camera-facing disk, so move each label to the front of its own point. */
+    const VArray<float> radii = pointcloud.radius();
+    /* Root-mean-square object scale, matching the point-cloud shader. */
+    const float radius_scale = math::length(math::to_scale(object_to_world)) * 0.577350269f;
+    const bool is_perspective = state.rv3d != nullptr && state.rv3d->is_persp;
+    Array<float3> anchors(positions.size());
+    for (const int i : positions.index_range()) {
+      const float3 center = math::transform_point(object_to_world, positions[i]);
+      const float3 to_camera = is_perspective ? state.camera_position - center :
+                                                state.camera_forward;
+      const float distance = math::length(to_camera);
+      const float3 direction = distance > 1.0e-20f ? to_camera / distance : state.camera_forward;
+      anchors[i] = center + direction * (std::max(radii[i], 0.0f) * radius_scale);
+    }
+    add_values_to_text_cache(
+        state.dt, attribute.varray, anchors.as_span(), float4x4::identity(), true);
+  }
+
   void add_attributes_to_text_cache(DRWTextStore *dt,
                                     bke::AttributeAccessor attribute_accessor,
                                     const float4x4 &object_to_world)
```

</details>

## 差异块 7 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 2 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
    const VArraySpan<float3> positions = *attribute_accessor.lookup<float3>("position",
                                                                            attribute.domain);

    // 旧第 119 行已替换：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
    // 原代码：add_values_to_text_cache(dt, attribute.varray, positions, object_to_world);
    // 新第 170 行：使用组件级遮挡开关，决定是否调整锚点或给文字附加测试标志。
    add_values_to_text_cache(dt, attribute.varray, positions, object_to_world, occlusion_test_);
  }

  void add_mesh_attributes_to_text_cache(const State &state,
```

<details>
<summary>核对本块原始 diff（2 条修改）</summary>

```diff
@@ -116,7 +167,7 @@ class AttributeTexts : Overlay {
     const VArraySpan<float3> positions = *attribute_accessor.lookup<float3>("position",
                                                                             attribute.domain);
 
-    add_values_to_text_cache(dt, attribute.varray, positions, object_to_world);
+    add_values_to_text_cache(dt, attribute.varray, positions, object_to_world, occlusion_test_);
   }
 
   void add_mesh_attributes_to_text_cache(const State &state,
```

</details>

## 差异块 8 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 13 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
          }
        }
      });
      // 旧第 171 行已替换：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
      // 原代码：add_values_to_text_cache(
          // 旧第 172 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
          // 原代码：state.dt, attribute.varray, corner_positions.as_span(), object_to_world);
      // 新第 222 行：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
      add_values_to_text_cache(state.dt,
                               // 新第 223 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                               attribute.varray,
                               // 新第 224 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                               corner_positions.as_span(),
                               // 新第 225 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                               object_to_world,
                               // 新第 226 行：使用组件级遮挡开关，决定是否调整锚点或给文字附加测试标志。
                               occlusion_test_);
    }
    else {
      // 旧第 175 行已替换：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
      // 原代码：add_values_to_text_cache(state.dt, attribute.varray, positions, object_to_world);
      // 新第 229 行：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
      add_values_to_text_cache(
          // 新第 230 行：使用组件级遮挡开关，决定是否调整锚点或给文字附加测试标志。
          state.dt, attribute.varray, positions, object_to_world, occlusion_test_);
    }
  }

  // 旧第 179 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
  // 原代码：void add_instance_attributes_to_text_cache(DRWTextStore *dt,
  // 新第 234 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
  void add_instance_attributes_to_text_cache(const State &state,
                                             bke::AttributeAccessor attribute_accessor,
                                             // 新第 236 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                             const Object &object,
                                             const float4x4 &object_to_world,
                                             int instance_index)
  {
```

<details>
<summary>核对本块原始 diff（13 条修改）</summary>

```diff
@@ -168,16 +219,21 @@ class AttributeTexts : Overlay {
           }
         }
       });
-      add_values_to_text_cache(
-          state.dt, attribute.varray, corner_positions.as_span(), object_to_world);
+      add_values_to_text_cache(state.dt,
+                               attribute.varray,
+                               corner_positions.as_span(),
+                               object_to_world,
+                               occlusion_test_);
     }
     else {
-      add_values_to_text_cache(state.dt, attribute.varray, positions, object_to_world);
+      add_values_to_text_cache(
+          state.dt, attribute.varray, positions, object_to_world, occlusion_test_);
     }
   }
 
-  void add_instance_attributes_to_text_cache(DRWTextStore *dt,
+  void add_instance_attributes_to_text_cache(const State &state,
                                              bke::AttributeAccessor attribute_accessor,
+                                             const Object &object,
                                              const float4x4 &object_to_world,
                                              int instance_index)
   {
```

</details>

## 差异块 9 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 46 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
    const GVArray attribute = attribute_accessor.lookup(".viewer").varray.slice(
        IndexRange(instance_index, 1));

    // 旧第 189 行已替换：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
    // 原代码：add_values_to_text_cache(dt, attribute, {float3(0, 0, 0)}, object_to_world);
    // 新第 245 行：实例文字本地锚点；初始在原点，条件满足时移向包围盒朝相机的出口。
    float3 local_anchor(0.0f);
    // 新第 246 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
    const bool is_perspective = state.rv3d != nullptr && state.rv3d->is_persp;
    // 新第 247 行：使用组件级遮挡开关，决定是否调整锚点或给文字附加测试标志。
    if (occlusion_test_) {
      // 新第 248 行：实例原点可能位于自身内部，盒出口是轻量的前表面近似。
      /* The instance origin is often behind its own geometry. Move the depth-test anchor along
       // 新第 249 行：实例原点可能位于自身内部，盒出口是轻量的前表面近似。
       * the view ray to the front of its local bounds; its screen position stays the same. */
      // 新第 250 行：查询实例对象的本地 AABB；结果可能不存在，需先检查 optional。
      const std::optional<Bounds<float3>> bounds = BKE_object_boundbox_get(&object);
      // 新第 251 行：只在实例原点落于包围盒内部时使用向相机的盒出口。
      if (bounds && bounds->contains(local_anchor) &&
          // 新第 252 行：排除不可可靠求逆的退化对象矩阵。
          math::abs(math::determinant(object_to_world)) > 1.0e-20f)
      // 新第 253 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
      {
        // 新第 254 行：对象矩阵求逆，把朝相机的射线方向转换回包围盒所在的本地空间。
        const float4x4 world_to_object = math::invert(object_to_world);
        // 新第 255 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
        const float3 world_center = object_to_world.location();
        // 新第 256 行：透视从点指向相机位置；正交使用统一观察方向。
        const float3 toward_camera = is_perspective ? state.camera_position - world_center :
                                                      // 新第 257 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                                      state.camera_forward;
        // 新第 258 行：透视从点指向相机位置；正交使用统一观察方向。
        const float3 local_direction = math::transform_direction(world_to_object, toward_camera);
        // 新第 259 行：保留源码说明：Start inside the bounds and use the exit toward the camera. In perspective,；相邻代码的中文推导见专题章节。
        /* Start inside the bounds and use the exit toward the camera. In perspective,
         // 新第 260 行：透视射线保留原点到相机的完整向量，因此参数 1 对应相机。
         * the unnormalized direction places the camera at t = 1. */
        // 新第 261 行：射线出口参数；透视方向未归一化，t=1 对应相机位置。
        float exit_t;
        // 新第 262 行：避免对零长度或近零向量归一化，防止数值无效。
        if (math::length_squared(local_direction) > 1.0e-20f &&
            // 新第 263 行：测试从本地原点出发的射线与轴对齐包围盒相交，并取得出口参数。
            isect_ray_aabb_v3_simple(
                // 新第 264 行：射线出口参数；透视方向未归一化，t=1 对应相机位置。
                local_anchor, local_direction, bounds->min, bounds->max, nullptr, &exit_t) &&
            // 新第 265 行：射线出口参数；透视方向未归一化，t=1 对应相机位置。
            exit_t > 0.0f && (!is_perspective || exit_t < 1.0f))
        // 新第 266 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
        {
          // 新第 267 行：射线出口参数；透视方向未归一化，t=1 对应相机位置。
          local_anchor += local_direction * exit_t;
        // 新第 268 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
        }
      // 新第 269 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
      }
    // 新第 270 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
    }
    // 新第 271 行：复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。
    add_values_to_text_cache(
        // 新第 272 行：使用组件级遮挡开关，决定是否调整锚点或给文字附加测试标志。
        state.dt, attribute, {local_anchor}, object_to_world, occlusion_test_);
  }

  static void add_text_to_cache(DRWTextStore *dt,
                                const float3 &position,
                                const StringRef text,
                                // 旧第 195 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                                // 原代码：const uchar4 &color)
                                // 新第 278 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                const uchar4 &color,
                                // 新第 279 行：将每条文字的坐标空间与遮挡要求保存在位标志里。
                                const short flag)
  {
    // 旧第 197 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
    // 原代码：DRW_text_cache_add(dt,
                       // 旧第 198 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：position,
                       // 旧第 199 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：text.data(),
                       // 旧第 200 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：text.size(),
                       // 旧第 201 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：0,
                       // 旧第 202 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：0,
                       // 旧第 203 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：DRW_TEXT_CACHE_GLOBALSPACE,
                       // 旧第 204 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：color,
                       // 旧第 205 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：true,
                       // 旧第 206 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                       // 原代码：true);
    // 新第 281 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
    DRW_text_cache_add(dt, position, text.data(), text.size(), 0, 0, flag, color, true, true);
  }

  static void add_lines_to_cache(DRWTextStore *dt,
                                 const float3 &position,
                                 const Span<StringRef> lines,
                                 // 旧第 212 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                                 // 原代码：const uchar4 &color)
                                 // 新第 287 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                 const uchar4 &color,
                                 // 新第 288 行：将每条文字的坐标空间与遮挡要求保存在位标志里。
                                 const short flag)
  {
    const float text_size = ui::style_get()->widget.points;
    const float line_height = text_size * 1.1f * UI_SCALE_FAC;
```

<details>
<summary>核对本块原始 diff（46 条修改）</summary>

```diff
@@ -186,30 +242,50 @@ class AttributeTexts : Overlay {
     const GVArray attribute = attribute_accessor.lookup(".viewer").varray.slice(
         IndexRange(instance_index, 1));
 
-    add_values_to_text_cache(dt, attribute, {float3(0, 0, 0)}, object_to_world);
+    float3 local_anchor(0.0f);
+    const bool is_perspective = state.rv3d != nullptr && state.rv3d->is_persp;
+    if (occlusion_test_) {
+      /* The instance origin is often behind its own geometry. Move the depth-test anchor along
+       * the view ray to the front of its local bounds; its screen position stays the same. */
+      const std::optional<Bounds<float3>> bounds = BKE_object_boundbox_get(&object);
+      if (bounds && bounds->contains(local_anchor) &&
+          math::abs(math::determinant(object_to_world)) > 1.0e-20f)
+      {
+        const float4x4 world_to_object = math::invert(object_to_world);
+        const float3 world_center = object_to_world.location();
+        const float3 toward_camera = is_perspective ? state.camera_position - world_center :
+                                                      state.camera_forward;
+        const float3 local_direction = math::transform_direction(world_to_object, toward_camera);
+        /* Start inside the bounds and use the exit toward the camera. In perspective,
+         * the unnormalized direction places the camera at t = 1. */
+        float exit_t;
+        if (math::length_squared(local_direction) > 1.0e-20f &&
+            isect_ray_aabb_v3_simple(
+                local_anchor, local_direction, bounds->min, bounds->max, nullptr, &exit_t) &&
+            exit_t > 0.0f && (!is_perspective || exit_t < 1.0f))
+        {
+          local_anchor += local_direction * exit_t;
+        }
+      }
+    }
+    add_values_to_text_cache(
+        state.dt, attribute, {local_anchor}, object_to_world, occlusion_test_);
   }
 
   static void add_text_to_cache(DRWTextStore *dt,
                                 const float3 &position,
                                 const StringRef text,
-                                const uchar4 &color)
+                                const uchar4 &color,
+                                const short flag)
   {
-    DRW_text_cache_add(dt,
-                       position,
-                       text.data(),
-                       text.size(),
-                       0,
-                       0,
-                       DRW_TEXT_CACHE_GLOBALSPACE,
-                       color,
-                       true,
-                       true);
+    DRW_text_cache_add(dt, position, text.data(), text.size(), 0, 0, flag, color, true, true);
   }
 
   static void add_lines_to_cache(DRWTextStore *dt,
                                  const float3 &position,
                                  const Span<StringRef> lines,
-                                 const uchar4 &color)
+                                 const uchar4 &color,
+                                 const short flag)
   {
     const float text_size = ui::style_get()->widget.points;
     const float line_height = text_size * 1.1f * UI_SCALE_FAC;
```

</details>

## 差异块 10 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 2 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
                         line.size(),
                         0,
                         (center_offset - i) * line_height,
                         // 旧第 225 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                         // 原代码：DRW_TEXT_CACHE_GLOBALSPACE,
                         // 新第 301 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                         flag,
                         color,
                         true,
                         true);
```

<details>
<summary>核对本块原始 diff（2 条修改）</summary>

```diff
@@ -222,7 +298,7 @@ class AttributeTexts : Overlay {
                          line.size(),
                          0,
                          (center_offset - i) * line_height,
-                         DRW_TEXT_CACHE_GLOBALSPACE,
+                         flag,
                          color,
                          true,
                          true);
```

</details>

## 差异块 11 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 8 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  void add_values_to_text_cache(DRWTextStore *dt,
                                const GVArray &values,
                                const Span<float3> positions,
                                // 旧第 235 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                                // 原代码：const float4x4 &object_to_world)
                                // 新第 311 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                const float4x4 &object_to_world,
                                // 新第 312 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                                const bool occlusion_test = false)
  {
    uchar col[4];
    ui::theme::get_color_4ubv(TH_TEXT_HI, col);

    // 新第 317 行：保留源码说明：The flag is picked up by #DRW_text_cache_draw, which skips anchors that the；相邻代码的中文推导见专题章节。
    /* The flag is picked up by #DRW_text_cache_draw, which skips anchors that the scene
     // 新第 318 行：保留源码说明：depth buffer reports as occluded.；相邻代码的中文推导见专题章节。
     * depth buffer reports as occluded. */
    // 新第 319 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
    const short text_flags = DRW_TEXT_CACHE_GLOBALSPACE |
                             // 新第 320 行：在文字标志中增加或检查遮挡测试位；只有带此位的缓存条目需要深度比较。
                             (occlusion_test ? DRW_TEXT_CACHE_OCCLUSION_TEST : 0);
// 新第 321 行：空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。

    bke::attribute_math::to_static_type(values.type(), [&]<typename T>() {
      const VArray<T> &values_typed = values.typed<T>();
      for (const int i : values.index_range()) {
```

<details>
<summary>核对本块原始 diff（8 条修改）</summary>

```diff
@@ -232,11 +308,17 @@ class AttributeTexts : Overlay {
   void add_values_to_text_cache(DRWTextStore *dt,
                                 const GVArray &values,
                                 const Span<float3> positions,
-                                const float4x4 &object_to_world)
+                                const float4x4 &object_to_world,
+                                const bool occlusion_test = false)
   {
     uchar col[4];
     ui::theme::get_color_4ubv(TH_TEXT_HI, col);
 
+    /* The flag is picked up by #DRW_text_cache_draw, which skips anchors that the scene
+     * depth buffer reports as occluded. */
+    const short text_flags = DRW_TEXT_CACHE_GLOBALSPACE |
+                             (occlusion_test ? DRW_TEXT_CACHE_OCCLUSION_TEST : 0);
+
     bke::attribute_math::to_static_type(values.type(), [&]<typename T>() {
       const VArray<T> &values_typed = values.typed<T>();
       for (const int i : values.index_range()) {
```

</details>

## 差异块 12 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 22 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
        if constexpr (std::is_same_v<T, bool>) {
          char numstr[64];
          const size_t numstr_len = STRNCPY_UTF8_RLEN(numstr, value ? "True" : "False");
          // 旧第 249 行已替换：把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。
          // 原代码：add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col);
          // 新第 331 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col, text_flags);
        }
        else if constexpr (std::is_same_v<T, int8_t>) {
          char numstr[64];
          const size_t numstr_len = SNPRINTF_UTF8_RLEN(numstr, "%d", int(value));
          // 旧第 254 行已替换：把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。
          // 原代码：add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col);
          // 新第 336 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col, text_flags);
        }
        else if constexpr (std::is_same_v<T, int>) {
          char numstr[64];
          const size_t numstr_len = SNPRINTF_UTF8_RLEN(numstr, "%d", value);
          // 旧第 259 行已替换：把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。
          // 原代码：add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col);
          // 新第 341 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col, text_flags);
        }
        else if constexpr (std::is_same_v<T, int2>) {
          char x_str[64], y_str[64];
          const size_t x_str_len = SNPRINTF_UTF8_RLEN(x_str, "X: %d", value.x);
          const size_t y_str_len = SNPRINTF_UTF8_RLEN(y_str, "Y: %d", value.y);
          // 旧第 265 行已替换：把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。
          // 原代码：add_lines_to_cache(
              // 旧第 266 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
              // 原代码：dt, position, {StringRef(x_str, x_str_len), StringRef(y_str, y_str_len)}, col);
          // 新第 347 行：把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。
          add_lines_to_cache(dt,
                             // 新第 348 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             position,
                             // 新第 349 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             {StringRef(x_str, x_str_len), StringRef(y_str, y_str_len)},
                             // 新第 350 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             col,
                             // 新第 351 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
                             text_flags);
        }
        else if constexpr (std::is_same_v<T, float>) {
          char numstr[64];
          const size_t numstr_len = SNPRINTF_UTF8_RLEN(numstr, "%g", value);
          // 旧第 271 行已替换：把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。
          // 原代码：add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col);
          // 新第 356 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col, text_flags);
        }
        else if constexpr (std::is_same_v<T, float2>) {
          char x_str[64], y_str[64];
          const size_t x_str_len = SNPRINTF_UTF8_RLEN(x_str, "X: %g", value.x);
          const size_t y_str_len = SNPRINTF_UTF8_RLEN(y_str, "Y: %g", value.y);
          // 旧第 277 行已替换：把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。
          // 原代码：add_lines_to_cache(
              // 旧第 278 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
              // 原代码：dt, position, {StringRef(x_str, x_str_len), StringRef(y_str, y_str_len)}, col);
          // 新第 362 行：把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。
          add_lines_to_cache(dt,
                             // 新第 363 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             position,
                             // 新第 364 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             {StringRef(x_str, x_str_len), StringRef(y_str, y_str_len)},
                             // 新第 365 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             col,
                             // 新第 366 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
                             text_flags);
        }
        else if constexpr (std::is_same_v<T, float3>) {
          char x_str[64], y_str[64], z_str[64];
```

<details>
<summary>核对本块原始 diff（22 条修改）</summary>

```diff
@@ -246,36 +328,42 @@ class AttributeTexts : Overlay {
         if constexpr (std::is_same_v<T, bool>) {
           char numstr[64];
           const size_t numstr_len = STRNCPY_UTF8_RLEN(numstr, value ? "True" : "False");
-          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col);
+          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col, text_flags);
         }
         else if constexpr (std::is_same_v<T, int8_t>) {
           char numstr[64];
           const size_t numstr_len = SNPRINTF_UTF8_RLEN(numstr, "%d", int(value));
-          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col);
+          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col, text_flags);
         }
         else if constexpr (std::is_same_v<T, int>) {
           char numstr[64];
           const size_t numstr_len = SNPRINTF_UTF8_RLEN(numstr, "%d", value);
-          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col);
+          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col, text_flags);
         }
         else if constexpr (std::is_same_v<T, int2>) {
           char x_str[64], y_str[64];
           const size_t x_str_len = SNPRINTF_UTF8_RLEN(x_str, "X: %d", value.x);
           const size_t y_str_len = SNPRINTF_UTF8_RLEN(y_str, "Y: %d", value.y);
-          add_lines_to_cache(
-              dt, position, {StringRef(x_str, x_str_len), StringRef(y_str, y_str_len)}, col);
+          add_lines_to_cache(dt,
+                             position,
+                             {StringRef(x_str, x_str_len), StringRef(y_str, y_str_len)},
+                             col,
+                             text_flags);
         }
         else if constexpr (std::is_same_v<T, float>) {
           char numstr[64];
           const size_t numstr_len = SNPRINTF_UTF8_RLEN(numstr, "%g", value);
-          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col);
+          add_text_to_cache(dt, position, StringRef(numstr, numstr_len), col, text_flags);
         }
         else if constexpr (std::is_same_v<T, float2>) {
           char x_str[64], y_str[64];
           const size_t x_str_len = SNPRINTF_UTF8_RLEN(x_str, "X: %g", value.x);
           const size_t y_str_len = SNPRINTF_UTF8_RLEN(y_str, "Y: %g", value.y);
-          add_lines_to_cache(
-              dt, position, {StringRef(x_str, x_str_len), StringRef(y_str, y_str_len)}, col);
+          add_lines_to_cache(dt,
+                             position,
+                             {StringRef(x_str, x_str_len), StringRef(y_str, y_str_len)},
+                             col,
+                             text_flags);
         }
         else if constexpr (std::is_same_v<T, float3>) {
           char x_str[64], y_str[64], z_str[64];
```

</details>

## 差异块 13 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 3 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
                             {StringRef(x_str, x_str_len),
                              StringRef(y_str, y_str_len),
                              StringRef(z_str, z_str_len)},
                             // 旧第 290 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                             // 原代码：col);
                             // 新第 378 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             col,
                             // 新第 379 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
                             text_flags);
        }
        else if constexpr (std::is_same_v<T, ColorGeometry4b>) {
          const ColorGeometry4f color = color::decode(value);
```

<details>
<summary>核对本块原始 diff（3 条修改）</summary>

```diff
@@ -287,7 +375,8 @@ class AttributeTexts : Overlay {
                              {StringRef(x_str, x_str_len),
                               StringRef(y_str, y_str_len),
                               StringRef(z_str, z_str_len)},
-                             col);
+                             col,
+                             text_flags);
         }
         else if constexpr (std::is_same_v<T, ColorGeometry4b>) {
           const ColorGeometry4f color = color::decode(value);
```

</details>

## 差异块 14 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 3 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
                              StringRef(g_str, g_str_len),
                              StringRef(b_str, b_str_len),
                              StringRef(a_str, a_str_len)},
                             // 旧第 305 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                             // 原代码：col);
                             // 新第 394 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             col,
                             // 新第 395 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
                             text_flags);
        }
        else if constexpr (std::is_same_v<T, ColorGeometry4f>) {
          char r_str[64], g_str[64], b_str[64], a_str[64];
```

<details>
<summary>核对本块原始 diff（3 条修改）</summary>

```diff
@@ -302,7 +391,8 @@ class AttributeTexts : Overlay {
                               StringRef(g_str, g_str_len),
                               StringRef(b_str, b_str_len),
                               StringRef(a_str, a_str_len)},
-                             col);
+                             col,
+                             text_flags);
         }
         else if constexpr (std::is_same_v<T, ColorGeometry4f>) {
           char r_str[64], g_str[64], b_str[64], a_str[64];
```

</details>

## 差异块 15 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 3 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
                              StringRef(g_str, g_str_len),
                              StringRef(b_str, b_str_len),
                              StringRef(a_str, a_str_len)},
                             // 旧第 319 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                             // 原代码：col);
                             // 新第 409 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             col,
                             // 新第 410 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
                             text_flags);
        }
        else if constexpr (std::is_same_v<T, math::Quaternion>) {
          char w_str[64], x_str[64], y_str[64], z_str[64];
```

<details>
<summary>核对本块原始 diff（3 条修改）</summary>

```diff
@@ -316,7 +406,8 @@ class AttributeTexts : Overlay {
                               StringRef(g_str, g_str_len),
                               StringRef(b_str, b_str_len),
                               StringRef(a_str, a_str_len)},
-                             col);
+                             col,
+                             text_flags);
         }
         else if constexpr (std::is_same_v<T, math::Quaternion>) {
           char w_str[64], x_str[64], y_str[64], z_str[64];
```

</details>

## 差异块 16 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 3 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
                              StringRef(x_str, x_str_len),
                              StringRef(y_str, y_str_len),
                              StringRef(z_str, z_str_len)},
                             // 旧第 333 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                             // 原代码：col);
                             // 新第 424 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             col,
                             // 新第 425 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
                             text_flags);
        }
        else if constexpr (std::is_same_v<T, float4x4>) {
          float3 location;
```

<details>
<summary>核对本块原始 diff（3 条修改）</summary>

```diff
@@ -330,7 +421,8 @@ class AttributeTexts : Overlay {
                               StringRef(x_str, x_str_len),
                               StringRef(y_str, y_str_len),
                               StringRef(z_str, z_str_len)},
-                             col);
+                             col,
+                             text_flags);
         }
         else if constexpr (std::is_same_v<T, float4x4>) {
           float3 location;
```

</details>

## 差异块 17 · `class AttributeTexts : Overlay {`

下面按源码顺序阅读本块的 3 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
                             {StringRef(location_str, location_str_len),
                              StringRef(rotation_str, rotation_str_len),
                              StringRef(scale_str, scale_str_len)},
                             // 旧第 358 行已替换：旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。
                             // 原代码：col);
                             // 新第 450 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
                             col,
                             // 新第 451 行：将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。
                             text_flags);
        }
        else {
          BLI_assert_unreachable();
```

<details>
<summary>核对本块原始 diff（3 条修改）</summary>

```diff
@@ -355,7 +447,8 @@ class AttributeTexts : Overlay {
                              {StringRef(location_str, location_str_len),
                               StringRef(rotation_str, rotation_str_len),
                               StringRef(scale_str, scale_str_len)},
-                             col);
+                             col,
+                             text_flags);
         }
         else {
           BLI_assert_unreachable();
```

</details>

---

本文件列出 17 个差异块、165 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
