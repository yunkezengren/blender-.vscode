# `source/blender/draw/engines/overlay/overlay_private.hh`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文，并在修改行前加入中文注释与行号。
> 删除的旧行在原位置以注释显示；原始 diff 放在折叠区，方便核对。代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `struct State {`

下面按源码顺序阅读本块的 4 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  {
    return (this->overlay.flag & V3D_OVERLAY_VIEWER_ATTRIBUTE_TEXT);
  }
  // 新第 271 行：使用同名设置；Python 属性名、RNA 注册名与 C++ 查询函数分别处于不同层。
  bool viewer_text_occlusion_culling() const
  // 新第 272 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
  {
    // 新第 273 行：引用持久化选项位：DNA 定义它，RNA 映射它，State 通过位与运算查询它。
    return (this->overlay.flag & V3D_OVERLAY_VIEWER_TEXT_OCCLUSION_CULLING);
  // 新第 274 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
  }
  bool show_sculpt_mask() const
  {
    return (this->overlay.flag & V3D_OVERLAY_SCULPT_SHOW_MASK);
```

<details>
<summary>核对本块原始 diff（4 条修改）</summary>

```diff
@@ -268,6 +268,10 @@ struct State {
   {
     return (this->overlay.flag & V3D_OVERLAY_VIEWER_ATTRIBUTE_TEXT);
   }
+  bool viewer_text_occlusion_culling() const
+  {
+    return (this->overlay.flag & V3D_OVERLAY_VIEWER_TEXT_OCCLUSION_CULLING);
+  }
   bool show_sculpt_mask() const
   {
     return (this->overlay.flag & V3D_OVERLAY_SCULPT_SHOW_MASK);
```

</details>

---

本文件列出 1 个差异块、4 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
