# `source/blender/makesdna/DNA_view3d_types.h`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文；有语义的修改行旁带中文注释与新行号。
> 结构性空行、括号及原有英文源码注释保持原貌，便于顺着代码阅读。删除的旧行以注释显示；原始 diff 放在折叠区。
> 这些代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `enum eView3DOverlay_Flag : int {`

下面按源码顺序阅读本块的 1 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  V3D_OVERLAY_SHOW_LIGHT_COLORS = (1 << 17),
  V3D_OVERLAY_VIEWER_ATTRIBUTE_TEXT = (1 << 18),
  V3D_OVERLAY_PERFORMANCE = (1 << 19),
  // 新第 310 行：引用持久化选项位：DNA 定义它，RNA 映射它，State 通过位与运算查询它。
  V3D_OVERLAY_VIEWER_TEXT_OCCLUSION_CULLING = (1 << 20),
};
ENUM_OPERATORS(eView3DOverlay_Flag)

```

<details>
<summary>核对本块原始 diff（1 条修改）</summary>

```diff
@@ -307,6 +307,7 @@ enum eView3DOverlay_Flag : int {
   V3D_OVERLAY_SHOW_LIGHT_COLORS = (1 << 17),
   V3D_OVERLAY_VIEWER_ATTRIBUTE_TEXT = (1 << 18),
   V3D_OVERLAY_PERFORMANCE = (1 << 19),
+  V3D_OVERLAY_VIEWER_TEXT_OCCLUSION_CULLING = (1 << 20),
 };
 ENUM_OPERATORS(eView3DOverlay_Flag)
 
```

</details>

---

本文件列出 1 个差异块、1 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
