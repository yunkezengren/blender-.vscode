# `scripts/startup/bl_ui/space_view3d.py`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文，并在修改行前加入中文注释与行号。
> 删除的旧行在原位置以注释显示；原始 diff 放在折叠区，方便核对。代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `class VIEW3D_PT_overlay_viewer_node(Panel):`

下面按源码顺序阅读本块的 4 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```python
        row.active = view.show_viewer and overlay.show_text
        row.prop(overlay, "show_viewer_text", text="Attribute Text")

        # 新第 7324 行：在 Viewer Overlay 面板中新建一行控件。
        row = col.row(align=True)
        # 新第 7325 行：三个上游显示条件同时成立时才允许用户操作这个子选项。
        row.active = view.show_viewer and overlay.show_text and overlay.show_viewer_text
        # 新第 7326 行：使用同名设置；Python 属性名、RNA 注册名与 C++ 查询函数分别处于不同层。
        row.prop(overlay, "viewer_text_occlusion_culling", text="Occlusion Culling")
# 新第 7327 行：空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。


class VIEW3D_PT_overlay_motion_tracking(Panel):
    bl_space_type = 'VIEW_3D'
```

<details>
<summary>核对本块原始 diff（4 条修改）</summary>

```diff
@@ -7321,6 +7321,10 @@ class VIEW3D_PT_overlay_viewer_node(Panel):
         row.active = view.show_viewer and overlay.show_text
         row.prop(overlay, "show_viewer_text", text="Attribute Text")
 
+        row = col.row(align=True)
+        row.active = view.show_viewer and overlay.show_text and overlay.show_viewer_text
+        row.prop(overlay, "viewer_text_occlusion_culling", text="Occlusion Culling")
+
 
 class VIEW3D_PT_overlay_motion_tracking(Panel):
     bl_space_type = 'VIEW_3D'
```

</details>

---

本文件列出 1 个差异块、4 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
