# `source/blender/makesrna/intern/rna_space.cc`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文，并在修改行前加入中文注释与行号。
> 删除的旧行在原位置以注释显示；原始 diff 放在折叠区，方便核对。代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `static void rna_def_space_view3d_overlay(BlenderRNA *brna)`

下面按源码顺序阅读本块的 10 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
      prop, "View Attribute Text", "Show attribute values as text in viewport");
  RNA_def_property_update(prop, NC_SPACE | ND_SPACE_VIEW3D, nullptr);

  // 新第 5438 行：使用同名设置；Python 属性名、RNA 注册名与 C++ 查询函数分别处于不同层。
  prop = RNA_def_property(srna, "viewer_text_occlusion_culling", PROP_BOOLEAN, PROP_NONE);
  // 新第 5439 行：把 RNA 布尔值映射到底层 `overlay.flag` 指定的掩码位。
  RNA_def_property_boolean_sdna(
      // 新第 5440 行：引用持久化选项位：DNA 定义它，RNA 映射它，State 通过位与运算查询它。
      prop, nullptr, "overlay.flag", V3D_OVERLAY_VIEWER_TEXT_OCCLUSION_CULLING);
  // 新第 5441 行：把视口开关标为非动画属性。
  RNA_def_property_clear_flag(prop, PROP_ANIMATABLE);
  // 新第 5442 行：配置用户看到的选项标题和悬停说明。
  RNA_def_property_ui_text(
      // 新第 5443 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
      prop,
      // 新第 5444 行：配置用户看到的选项标题和悬停说明。
      "Occlusion Culling",
      // 新第 5445 行：属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。
      "Hide Viewer attribute text when its anchor is occluded by scene geometry");
  // 新第 5446 行：属性变化后通知 3D 视图刷新，使下一帧读取新设置。
  RNA_def_property_update(prop, NC_SPACE | ND_SPACE_VIEW3D, nullptr);
// 新第 5447 行：空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。

  prop = RNA_def_property(srna, "show_paint_wire", PROP_BOOLEAN, PROP_NONE);
  RNA_def_property_boolean_sdna(prop, nullptr, "overlay.paint_flag", V3D_OVERLAY_PAINT_WIRE);
  RNA_def_property_ui_text(prop, "Show Wire", "Use wireframe display in painting modes");
```

<details>
<summary>核对本块原始 diff（10 条修改）</summary>

```diff
@@ -5435,6 +5435,16 @@ static void rna_def_space_view3d_overlay(BlenderRNA *brna)
       prop, "View Attribute Text", "Show attribute values as text in viewport");
   RNA_def_property_update(prop, NC_SPACE | ND_SPACE_VIEW3D, nullptr);
 
+  prop = RNA_def_property(srna, "viewer_text_occlusion_culling", PROP_BOOLEAN, PROP_NONE);
+  RNA_def_property_boolean_sdna(
+      prop, nullptr, "overlay.flag", V3D_OVERLAY_VIEWER_TEXT_OCCLUSION_CULLING);
+  RNA_def_property_clear_flag(prop, PROP_ANIMATABLE);
+  RNA_def_property_ui_text(
+      prop,
+      "Occlusion Culling",
+      "Hide Viewer attribute text when its anchor is occluded by scene geometry");
+  RNA_def_property_update(prop, NC_SPACE | ND_SPACE_VIEW3D, nullptr);
+
   prop = RNA_def_property(srna, "show_paint_wire", PROP_BOOLEAN, PROP_NONE);
   RNA_def_property_boolean_sdna(prop, nullptr, "overlay.paint_flag", V3D_OVERLAY_PAINT_WIRE);
   RNA_def_property_ui_text(prop, "Show Wire", "Use wireframe display in painting modes");
```

</details>

---

本文件列出 1 个差异块、10 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
