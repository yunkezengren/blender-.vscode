# `source/blender/draw/engines/overlay/overlay_instance.cc`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文；有语义的修改行旁带中文注释与新行号。
> 结构性空行、括号及原有英文源码注释保持原貌，便于顺着代码阅读。删除的旧行以注释显示；原始 diff 放在折叠区。
> 这些代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `void Instance::draw_v3d(Manager &manager, View &view)`

下面按源码顺序阅读本块的 4 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp

    infront.prepass.draw_line(resources.overlay_line_in_front_fb, manager, view);
  }

  /* Read scene depth before the grid and axes write their own one-pixel depth. */
  // 新第 939 行：在 prepass 之后、grid 之前读取场景深度，供后续文字绘制使用。
  update_text_depth();

  {
    /* Copy depth at the end of the prepass to avoid splitting the main render pass. */
    /* TODO(fclem): Better get rid of it. */
```

<details>
<summary>核对本块原始 diff（4 条修改）</summary>

```diff
@@ -934,6 +934,10 @@ void Instance::draw_v3d(Manager &manager, View &view)
 
     infront.prepass.draw_line(resources.overlay_line_in_front_fb, manager, view);
   }
+
+  /* Read scene depth before the grid and axes write their own one-pixel depth. */
+  update_text_depth();
+
   {
     /* Copy depth at the end of the prepass to avoid splitting the main render pass. */
     /* TODO(fclem): Better get rid of it. */
```

</details>

## 差异块 2 · `void Instance::draw_v3d(Manager &manager, View &view)`

下面按源码顺序阅读本块的 38 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  }
}

// 新第 1017 行：在 prepass 之后、grid 之前读取场景深度，供后续文字绘制使用。
void Instance::update_text_depth()
{
  // 新第 1019 行：检查缓存里是否有任何需要遮挡测试的文字，决定是否值得 GPU 回读。
  if (!state.show_text || !state.is_space_v3d() || !DRW_text_cache_needs_depth_test(state.dt)) {
    // 新第 1020 行：把当前深度缓存的借用指针交给文字系统，传空值时解除借用。
    DRW_text_cache_depth_set(state.dt, nullptr);
    // 新第 1021 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    if (text_depth_cache_ != nullptr) {
      // 新第 1022 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
      ED_view3d_depths_free(text_depth_cache_);
      // 新第 1023 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
      text_depth_cache_ = nullptr;
    }
    // 新第 1025 行：提前结束当前分支，避免继续处理不适用的对象或候选。
    return;
  }
  /* Refresh from this frame after the depth prepass, before grid and axes can alter depth.
   * The read-back is deliberately skipped when no text requested occlusion testing. */
  // 新第 1029 行：从当前 ARegion 找到对应 GPUViewport；现有接口需要非 const 区域指针。
  GPUViewport *viewport = WM_draw_region_get_viewport(const_cast<ARegion *>(state.region));
  // 新第 1030 行：取得这个 GPUViewport 的深度纹理，后续回读其本帧像素。
  gpu::Texture *depth_tx = GPU_viewport_depth_texture(viewport);
  // 新第 1031 行：读取当前深度纹理尺寸；尺寸变化时必须重建 CPU 数组。
  const int width = GPU_texture_width(depth_tx);
  // 新第 1032 行：读取当前深度纹理尺寸；尺寸变化时必须重建 CPU 数组。
  const int height = GPU_texture_height(depth_tx);
  // 新第 1033 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
  if (text_depth_cache_ != nullptr &&
      // 新第 1034 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
      (text_depth_cache_->w != width || text_depth_cache_->h != height))
  {
    // 新第 1036 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    ED_view3d_depths_free(text_depth_cache_);
    // 新第 1037 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    text_depth_cache_ = nullptr;
  }
  // 新第 1039 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
  if (text_depth_cache_ == nullptr) {
    // 新第 1040 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    text_depth_cache_ = MEM_new_zeroed<ViewDepths>("ViewDepths");
    // 新第 1041 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    text_depth_cache_->w = width;
    // 新第 1042 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    text_depth_cache_->h = height;
    // 新第 1043 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    text_depth_cache_->depths = static_cast<float *>(
        // 新第 1044 行：将本帧视口深度纹理回读到 CPU；有目标缓冲的重载会刷新已分配数组。
        GPU_texture_read(depth_tx, GPU_DATA_FLOAT, 0));
    // 新第 1045 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    text_depth_cache_->depth_range[0] = 0.0;
    // 新第 1046 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    text_depth_cache_->depth_range[1] = 1.0;
  }
  // 新第 1048 行：处理与紧邻 if 条件相反的路径；结合上方上下文读取。
  else {
    /* Refresh the contents with this frame's depth. */
    // 新第 1050 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
    GPU_texture_read(depth_tx, GPU_DATA_FLOAT, 0, text_depth_cache_->depths);
  }
  // 新第 1052 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
  DRW_text_cache_depth_set(state.dt, text_depth_cache_);
}

void Instance::draw_text(Framebuffer &framebuffer)
{
  if (state.show_text == false) {
```

<details>
<summary>核对本块原始 diff（38 条修改）</summary>

```diff
@@ -1010,6 +1014,44 @@ void Instance::draw_v3d(Manager &manager, View &view)
   }
 }
 
+void Instance::update_text_depth()
+{
+  if (!state.show_text || !state.is_space_v3d() || !DRW_text_cache_needs_depth_test(state.dt)) {
+    DRW_text_cache_depth_set(state.dt, nullptr);
+    if (text_depth_cache_ != nullptr) {
+      ED_view3d_depths_free(text_depth_cache_);
+      text_depth_cache_ = nullptr;
+    }
+    return;
+  }
+  /* Refresh from this frame after the depth prepass, before grid and axes can alter depth.
+   * The read-back is deliberately skipped when no text requested occlusion testing. */
+  GPUViewport *viewport = WM_draw_region_get_viewport(const_cast<ARegion *>(state.region));
+  gpu::Texture *depth_tx = GPU_viewport_depth_texture(viewport);
+  const int width = GPU_texture_width(depth_tx);
+  const int height = GPU_texture_height(depth_tx);
+  if (text_depth_cache_ != nullptr &&
+      (text_depth_cache_->w != width || text_depth_cache_->h != height))
+  {
+    ED_view3d_depths_free(text_depth_cache_);
+    text_depth_cache_ = nullptr;
+  }
+  if (text_depth_cache_ == nullptr) {
+    text_depth_cache_ = MEM_new_zeroed<ViewDepths>("ViewDepths");
+    text_depth_cache_->w = width;
+    text_depth_cache_->h = height;
+    text_depth_cache_->depths = static_cast<float *>(
+        GPU_texture_read(depth_tx, GPU_DATA_FLOAT, 0));
+    text_depth_cache_->depth_range[0] = 0.0;
+    text_depth_cache_->depth_range[1] = 1.0;
+  }
+  else {
+    /* Refresh the contents with this frame's depth. */
+    GPU_texture_read(depth_tx, GPU_DATA_FLOAT, 0, text_depth_cache_->depths);
+  }
+  DRW_text_cache_depth_set(state.dt, text_depth_cache_);
+}
+
 void Instance::draw_text(Framebuffer &framebuffer)
 {
   if (state.show_text == false) {
```

</details>

---

本文件列出 2 个差异块、42 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
