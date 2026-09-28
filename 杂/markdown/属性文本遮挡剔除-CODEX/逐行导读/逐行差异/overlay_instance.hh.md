# `source/blender/draw/engines/overlay/overlay_instance.hh`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文，并在修改行前加入中文注释与行号。
> 删除的旧行在原位置以注释显示；原始 diff 放在折叠区，方便核对。代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `class Instance : public DrawEngine {`

下面按源码顺序阅读本块的 4 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  const SelectionType selection_type_;
  bool clipping_enabled_;

  // 新第 61 行：保留源码说明：Scene depth for text occlusion, refreshed after the prepass and before grid；相邻代码的中文推导见专题章节。
  /** Scene depth for text occlusion, refreshed after the prepass and before grid drawing.
   // 新第 62 行：保留源码说明：Reuse the allocation until the viewport resizes or depth testing is disable；相邻代码的中文推导见专题章节。
   * Reuse the allocation until the viewport resizes or depth testing is disabled. */
  // 新第 63 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
  ViewDepths *text_depth_cache_ = nullptr;
// 新第 64 行：空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。

 public:
  ShapeCache shapes;

```

<details>
<summary>核对本块原始 diff（4 条修改）</summary>

```diff
@@ -58,6 +58,10 @@ class Instance : public DrawEngine {
   const SelectionType selection_type_;
   bool clipping_enabled_;
 
+  /** Scene depth for text occlusion, refreshed after the prepass and before grid drawing.
+   * Reuse the allocation until the viewport resizes or depth testing is disabled. */
+  ViewDepths *text_depth_cache_ = nullptr;
+
  public:
   ShapeCache shapes;
 
```

</details>

## 差异块 2 · `class Instance : public DrawEngine {`

下面按源码顺序阅读本块的 3 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  ~Instance() override
  {
    DRW_text_cache_destroy(state.dt);
    // 新第 123 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    if (text_depth_cache_ != nullptr) {
      // 新第 124 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
      ED_view3d_depths_free(text_depth_cache_);
    // 新第 125 行：控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。
    }
  }

  StringRefNull name_get() final
```

<details>
<summary>核对本块原始 diff（3 条修改）</summary>

```diff
@@ -116,6 +120,9 @@ class Instance : public DrawEngine {
   ~Instance() override
   {
     DRW_text_cache_destroy(state.dt);
+    if (text_depth_cache_ != nullptr) {
+      ED_view3d_depths_free(text_depth_cache_);
+    }
   }
 
   StringRefNull name_get() final
```

</details>

## 差异块 3 · `class Instance : public DrawEngine {`

下面按源码顺序阅读本块的 1 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  void draw_v2d(Manager &manager, View &view);
  void draw_v3d(Manager &manager, View &view);

  // 新第 164 行：在 prepass 之后、grid 之前读取场景深度，供后续文字绘制使用。
  void update_text_depth();
  void draw_text(Framebuffer &framebuffer);

  void ensure_weight_ramp_texture();
```

<details>
<summary>核对本块原始 diff（1 条修改）</summary>

```diff
@@ -154,6 +161,7 @@ class Instance : public DrawEngine {
   void draw_v2d(Manager &manager, View &view);
   void draw_v3d(Manager &manager, View &view);
 
+  void update_text_depth();
   void draw_text(Framebuffer &framebuffer);
 
   void ensure_weight_ramp_texture();
```

</details>

---

本文件列出 3 个差异块、8 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
