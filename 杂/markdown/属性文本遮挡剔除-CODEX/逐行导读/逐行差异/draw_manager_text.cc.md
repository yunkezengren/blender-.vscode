# `source/blender/draw/intern/draw_manager_text.cc`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文；有语义的修改行旁带中文注释与新行号。
> 结构性空行、括号及原有英文源码注释保持原貌，便于顺着代码阅读。删除的旧行以注释显示；原始 diff 放在折叠区。
> 这些代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `struct DRWTextStore {`

下面按源码顺序阅读本块的 5 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  Vector<ViewCachedString> cache_strings;
  /** Backing storage for owned copies referenced by #ViewCachedString::str. */
  LinearAllocator<> string_allocator;
  /**
   * Scene depth read back by the caller before drawing overlays that write depth.
   * Borrowed through #DRW_text_cache_depth_set and refreshed for every frame that needs it.
   */
  // 新第 76 行：文字缓存只借用深度指针；分配、按帧刷新与释放由 Overlay Instance 负责。
  const ViewDepths *depths = nullptr;
};

DRWTextStore *DRW_text_cache_create()
```

<details>
<summary>核对本块原始 diff（5 条修改）</summary>

```diff
@@ -69,6 +69,11 @@ struct DRWTextStore {
   Vector<ViewCachedString> cache_strings;
   /** Backing storage for owned copies referenced by #ViewCachedString::str. */
   LinearAllocator<> string_allocator;
+  /**
+   * Scene depth read back by the caller before drawing overlays that write depth.
+   * Borrowed through #DRW_text_cache_depth_set and refreshed for every frame that needs it.
+   */
+  const ViewDepths *depths = nullptr;
 };
 
 DRWTextStore *DRW_text_cache_create()
```

</details>

## 差异块 2 · `static void drw_text_cache_draw_ex(DRWTextStore *dt, const ARegion *region)`

下面按源码顺序阅读本块的 109 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  GPU_matrix_projection_set(original_proj);
}

/**
 * Compute the window-space position and the [0..1] depth of a cached string anchor, using the
 * same math as #ed_view3d_project__internal so the depth is directly comparable to a read-back
 * of the viewport depth buffer.
 */
// 新第 187 行：将三维锚点投影为浮点屏幕位置和窗口深度，供像素采样与比较。
static bool text_anchor_project_with_depth(const ARegion &region,
                                           // 新第 188 行：输入组合投影矩阵；世界锚点使用 persmat，本地锚点使用 persmatob。
                                           const float perspmat[4][4],
                                           // 新第 189 行：输入三维文字锚点，单位及空间必须与选择的投影矩阵一致。
                                           const float co[3],
                                           // 新第 190 行：输出浮点屏幕坐标；保留子像素偏移，供后续平面补偿使用。
                                           float r_xy[2],
                                           // 新第 191 行：输出 [0,1] 窗口深度，供 CPU 锚点与 GPU 场景深度比较。
                                           float &r_depth)
{
  // 新第 193 行：为齐次坐标预留 x、y、z、w 四个分量。
  float vec4[4];
  // 新第 194 行：先复制锚点的三个位置分量，下一行再将 w 设为 1。
  copy_v3_v3(vec4, co);
  // 新第 195 行：齐次位置使用 w=1，使投影矩阵的平移项对它生效。
  vec4[3] = 1.0f;
  // 新第 196 行：用视图投影矩阵变换齐次坐标，得到裁剪空间四维向量。
  mul_m4_v4(perspmat, vec4);
  // 新第 197 行：齐次坐标 w 参与透视除法；零值不能作为除数。
  const float w = fabsf(vec4[3]);
  // 新第 198 行：防止透视除法除以零；这种锚点不能产生可靠屏幕坐标。
  if (w == 0.0f) {
    // 新第 199 行：投影输入不可用或在视口外；调用者会把这条文字标为裁剪。
    return false;
  }

  // 新第 202 行：预先计算 1/w，随后分别乘裁剪空间 x、y、z。
  const float scalar = 1.0f / w;
  /* Outside the near/far depth range: nothing to compare against. */
  // 新第 204 行：排除投影深度裁剪范围以外的锚点。
  if (vec4[2] <= -w || vec4[2] >= w) {
    // 新第 205 行：投影输入不可用或在视口外；调用者会把这条文字标为裁剪。
    return false;
  }

  // 新第 208 行：把 NDC 横纵坐标从 [-1,1] 映射到视口像素位置。
  const float fx = (float(region.winx) / 2.0f) * (1.0f + (vec4[0] * scalar));
  // 新第 209 行：把 NDC 横纵坐标从 [-1,1] 映射到视口像素位置。
  const float fy = (float(region.winy) / 2.0f) * (1.0f + (vec4[1] * scalar));
  // 新第 210 行：拒绝视口外的锚点，避免得到不可用的深度像素下标。
  if (fx <= 0.0f || fy <= 0.0f || fx >= float(region.winx) || fy >= float(region.winy)) {
    // 新第 211 行：投影输入不可用或在视口外；调用者会把这条文字标为裁剪。
    return false;
  }

  /* Normalized device depth, mapped the same way gl_FragCoord.z is written. */
  // 新第 215 行：把裁剪深度经透视除法与线性映射转成 [0,1] 窗口深度。
  const float ndc_z = vec4[2] * scalar;
  // 新第 216 行：把裁剪深度经透视除法与线性映射转成 [0,1] 窗口深度。
  const float depth = (ndc_z + 1.0f) * 0.5f;

  // 新第 218 行：把算好的浮点像素位置写到输出数组，供调用者选深度像素。
  r_xy[0] = fx;
  // 新第 219 行：把算好的浮点像素位置写到输出数组，供调用者选深度像素。
  r_xy[1] = fy;
  // 新第 220 行：把窗口深度写到输出引用，供后续遮挡比较。
  r_depth = depth;
  // 新第 221 行：浮点屏幕坐标与窗口深度均已写入输出参数。
  return true;
}

/** Allow small differences between CPU projection and rasterized surface depth. */
// 新第 225 行：最终遮挡比较容差，单位是 [0,1] 窗口深度。
static constexpr float text_depth_bias = 2.0e-5f;
/** Maximum residual when checking whether depth samples belong to the same plane. */
// 新第 227 行：局部平面九样本拟合残差容差，与最终遮挡容差用途不同。
static constexpr float text_depth_plane_tolerance = 2.0e-6f;

// 新第 229 行：统一背景深度和锚点深度的单像素基础判断。
static bool text_depth_is_occluded(const float anchor_depth, const float scene_depth)
{
  /* Cleared background never occludes text. */
  // 新第 232 行：最终遮挡比较容差，单位是 [0,1] 窗口深度。
  return scene_depth != 1.0f && anchor_depth > scene_depth + text_depth_bias;
}

/** Perspective depth test with local plane reconstruction at the anchor's subpixel position. */
// 新第 236 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
static bool text_anchor_is_occluded_perspective(const ViewDepths &depths,
                                                // 新第 237 行：输入锚点所在的整数像素坐标；调用前已检查是否在深度图内。
                                                const int x,
                                                // 新第 238 行：输入锚点所在的整数像素坐标；调用前已检查是否在深度图内。
                                                const int y,
                                                // 新第 239 行：输入未舍入的浮点屏幕位置，求与像素中心的差。
                                                const float xy[2],
                                                // 新第 240 行：输入锚点的 [0,1] 窗口深度，和采样或重建的场景深度比较。
                                                const float anchor_depth)
{
  // 新第 242 行：读取中心像素的场景深度；先用它做低成本基础判断。
  const float center = depths.depths[y * depths.w + x];
  // 新第 243 行：统一背景深度和锚点深度的单像素基础判断。
  if (!text_depth_is_occluded(anchor_depth, center)) {
    // 新第 244 行：发现可用的同表面平面，撤销中心像素造成的遮挡初判。
    return false;
  }

  // 新第 247 行：计算锚点相对像素中心的偏移；整数像素格中心位于索引加 0.5。
  const float dx = xy[0] - (float(x) + 0.5f);
  // 新第 248 行：计算锚点相对像素中心的偏移；整数像素格中心位于索引加 0.5。
  const float dy = xy[1] - (float(y) + 0.5f);
  /* Window depth on a projected triangle is affine in screen coordinates, including in
   * perspective. Reconstruct that plane instead of limiting its slope with a fixed threshold.
   * Try each quadrant so a crease does not require samples from both incident faces. */
  // 新第 252 行：尝试四个象限，让折角附近的单侧连续面也有机会通过检查。
  for (const int sy : {-1, 1}) {
    // 新第 253 行：尝试四个象限，让折角附近的单侧连续面也有机会通过检查。
    for (const int sx : {-1, 1}) {
      // 新第 254 行：一个候选象限需要向同一方向走两像素；越界时跳过，避免数组越界。
      if (x + 2 * sx < 0 || x + 2 * sx >= depths.w || y + 2 * sy < 0 || y + 2 * sy >= depths.h) {
        // 新第 255 行：结束本次循环处理，继续检查下一条文字或下一个候选。
        continue;
      }
      // 新第 257 行：由邻近像素估计平面沿屏幕 x/y 方向的每像素深度变化。
      const float step_x = depths.depths[y * depths.w + x + sx] - center;
      // 新第 258 行：由邻近像素估计平面沿屏幕 x/y 方向的每像素深度变化。
      const float step_y = depths.depths[(y + sy) * depths.w + x] - center;
      // 新第 259 行：由邻近像素估计平面沿屏幕 x/y 方向的每像素深度变化。
      const float reconstructed = center + step_x * (dx * sx) + step_y * (dy * sy);
      // 新第 260 行：最终遮挡比较容差，单位是 [0,1] 窗口深度。
      if (anchor_depth > reconstructed + text_depth_bias) {
        // 新第 261 行：结束本次循环处理，继续检查下一条文字或下一个候选。
        continue;
      }

      /* A 2x2 patch alone can mistake a silhouette step for a steep plane. Require three
       * samples along both axes, and reject background and inconsistent surface samples.
       * This tolerance checks planarity, not slope, so close-up surfaces remain eligible. */
      // 新第 267 行：记录候选 3×3 区域是否符合单一平面；只有通过时可放行文字。
      bool planar = true;
      // 新第 268 行：遍历候选象限 3×3 样本，验证它们能否由同一深度平面解释。
      for (int j = 0; j < 3 && planar; j++) {
        // 新第 269 行：遍历候选象限 3×3 样本，验证它们能否由同一深度平面解释。
        for (int i = 0; i < 3; i++) {
          // 新第 270 行：读取此格子的实际 GPU 深度；随后与局部平面预测值比较。
          const float sample = depths.depths[(y + j * sy) * depths.w + x + i * sx];
          // 新第 271 行：由邻近像素估计平面沿屏幕 x/y 方向的每像素深度变化。
          const float predicted = center + float(i) * step_x + float(j) * step_y;
          // 新第 272 行：局部平面九样本拟合残差容差，与最终遮挡容差用途不同。
          if (sample == 1.0f || fabsf(sample - predicted) > text_depth_plane_tolerance) {
            // 新第 273 行：发现背景或残差过大，当前象限不再可信。
            planar = false;
            // 新第 274 行：提前结束当前分支，避免继续处理不适用的对象或候选。
            break;
          }
        }
      }
      // 新第 278 行：只有九样本都通过一致性检查，才允许此候选纠正基础误判。
      if (planar) {
        // 新第 279 行：发现可用的同表面平面，撤销中心像素造成的遮挡初判。
        return false;
      }
    }
  }
  // 新第 283 行：四象限都没有通过检查，保留基础遮挡结论。
  return true;
}

void DRW_text_cache_draw(DRWTextStore *dt, const ARegion *region, const View3D *v3d)
{
  if (v3d) {
    RegionView3D *rv3d = static_cast<RegionView3D *>(region->regiondata);
    int tot = 0;

    /* Occlusion testing needs the scene depth read back to CPU memory. Only do this when at
     * least one string requested it, and only when a valid depth buffer was provided. */
    // 新第 294 行：只有借来的 ViewDepths 和像素数组都非空，才允许逐条深度测试。
    const bool use_occlusion_test = dt->depths != nullptr && dt->depths->depths != nullptr;

    /* project first and test */
    for (ViewCachedString &vos : dt->cache_strings) {
      if (ED_view3d_project_short_ex(
```

<details>
<summary>核对本块原始 diff（109 条修改）</summary>

```diff
@@ -174,11 +179,120 @@ static void drw_text_cache_draw_ex(DRWTextStore *dt, const ARegion *region)
   GPU_matrix_projection_set(original_proj);
 }
 
+/**
+ * Compute the window-space position and the [0..1] depth of a cached string anchor, using the
+ * same math as #ed_view3d_project__internal so the depth is directly comparable to a read-back
+ * of the viewport depth buffer.
+ */
+static bool text_anchor_project_with_depth(const ARegion &region,
+                                           const float perspmat[4][4],
+                                           const float co[3],
+                                           float r_xy[2],
+                                           float &r_depth)
+{
+  float vec4[4];
+  copy_v3_v3(vec4, co);
+  vec4[3] = 1.0f;
+  mul_m4_v4(perspmat, vec4);
+  const float w = fabsf(vec4[3]);
+  if (w == 0.0f) {
+    return false;
+  }
+
+  const float scalar = 1.0f / w;
+  /* Outside the near/far depth range: nothing to compare against. */
+  if (vec4[2] <= -w || vec4[2] >= w) {
+    return false;
+  }
+
+  const float fx = (float(region.winx) / 2.0f) * (1.0f + (vec4[0] * scalar));
+  const float fy = (float(region.winy) / 2.0f) * (1.0f + (vec4[1] * scalar));
+  if (fx <= 0.0f || fy <= 0.0f || fx >= float(region.winx) || fy >= float(region.winy)) {
+    return false;
+  }
+
+  /* Normalized device depth, mapped the same way gl_FragCoord.z is written. */
+  const float ndc_z = vec4[2] * scalar;
+  const float depth = (ndc_z + 1.0f) * 0.5f;
+
+  r_xy[0] = fx;
+  r_xy[1] = fy;
+  r_depth = depth;
+  return true;
+}
+
+/** Allow small differences between CPU projection and rasterized surface depth. */
+static constexpr float text_depth_bias = 2.0e-5f;
+/** Maximum residual when checking whether depth samples belong to the same plane. */
+static constexpr float text_depth_plane_tolerance = 2.0e-6f;
+
+static bool text_depth_is_occluded(const float anchor_depth, const float scene_depth)
+{
+  /* Cleared background never occludes text. */
+  return scene_depth != 1.0f && anchor_depth > scene_depth + text_depth_bias;
+}
+
+/** Perspective depth test with local plane reconstruction at the anchor's subpixel position. */
+static bool text_anchor_is_occluded_perspective(const ViewDepths &depths,
+                                                const int x,
+                                                const int y,
+                                                const float xy[2],
+                                                const float anchor_depth)
+{
+  const float center = depths.depths[y * depths.w + x];
+  if (!text_depth_is_occluded(anchor_depth, center)) {
+    return false;
+  }
+
+  const float dx = xy[0] - (float(x) + 0.5f);
+  const float dy = xy[1] - (float(y) + 0.5f);
+  /* Window depth on a projected triangle is affine in screen coordinates, including in
+   * perspective. Reconstruct that plane instead of limiting its slope with a fixed threshold.
+   * Try each quadrant so a crease does not require samples from both incident faces. */
+  for (const int sy : {-1, 1}) {
+    for (const int sx : {-1, 1}) {
+      if (x + 2 * sx < 0 || x + 2 * sx >= depths.w || y + 2 * sy < 0 || y + 2 * sy >= depths.h) {
+        continue;
+      }
+      const float step_x = depths.depths[y * depths.w + x + sx] - center;
+      const float step_y = depths.depths[(y + sy) * depths.w + x] - center;
+      const float reconstructed = center + step_x * (dx * sx) + step_y * (dy * sy);
+      if (anchor_depth > reconstructed + text_depth_bias) {
+        continue;
+      }
+
+      /* A 2x2 patch alone can mistake a silhouette step for a steep plane. Require three
+       * samples along both axes, and reject background and inconsistent surface samples.
+       * This tolerance checks planarity, not slope, so close-up surfaces remain eligible. */
+      bool planar = true;
+      for (int j = 0; j < 3 && planar; j++) {
+        for (int i = 0; i < 3; i++) {
+          const float sample = depths.depths[(y + j * sy) * depths.w + x + i * sx];
+          const float predicted = center + float(i) * step_x + float(j) * step_y;
+          if (sample == 1.0f || fabsf(sample - predicted) > text_depth_plane_tolerance) {
+            planar = false;
+            break;
+          }
+        }
+      }
+      if (planar) {
+        return false;
+      }
+    }
+  }
+  return true;
+}
+
 void DRW_text_cache_draw(DRWTextStore *dt, const ARegion *region, const View3D *v3d)
 {
   if (v3d) {
     RegionView3D *rv3d = static_cast<RegionView3D *>(region->regiondata);
     int tot = 0;
+
+    /* Occlusion testing needs the scene depth read back to CPU memory. Only do this when at
+     * least one string requested it, and only when a valid depth buffer was provided. */
+    const bool use_occlusion_test = dt->depths != nullptr && dt->depths->depths != nullptr;
+
     /* project first and test */
     for (ViewCachedString &vos : dt->cache_strings) {
       if (ED_view3d_project_short_ex(
```

</details>

## 差异块 3 · `void DRW_text_cache_draw(DRWTextStore *dt, const ARegion *region, const View3D *`

下面按源码顺序阅读本块的 28 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
              V3D_PROJ_TEST_CLIP_BB | V3D_PROJ_TEST_CLIP_WIN | V3D_PROJ_TEST_CLIP_NEAR) ==
          V3D_PROJ_RET_OK)
      {
        // 新第 307 行：在文字标志中增加或检查遮挡测试位；只有带此位的缓存条目需要深度比较。
        if (use_occlusion_test && (vos.flag & DRW_TEXT_CACHE_OCCLUSION_TEST) != 0) {
          /* Re-project keeping the depth so it can be compared with the scene depth. */
          // 新第 309 行：为第二次投影准备浮点屏幕坐标输出，保留子像素部分。
          float xy[2];
          // 新第 310 行：文字三维锚点经投影后的窗口深度，与场景像素或重建平面比较。
          float anchor_depth;
          // 新第 311 行：根据 GLOBALSPACE 位选择世界矩阵或对象本地矩阵的引用。
          const float (&persmat)[4][4] = (vos.flag & DRW_TEXT_CACHE_GLOBALSPACE) ? rv3d->persmat :
                                                                                   // 新第 312 行：不带 GLOBALSPACE 位时使用已经包含对象变换的投影矩阵。
                                                                                   rv3d->persmatob;
          // 新第 313 行：将三维锚点投影为浮点屏幕位置和窗口深度，供像素采样与比较。
          if (!text_anchor_project_with_depth(*region, persmat, vos.vec, xy, anchor_depth)) {
            // 新第 314 行：标记这条缓存文字不可画；最终 BLF 绘制函数会跳过它。
            vos.sco[0] = IS_CLIPPED;
            // 新第 315 行：结束本次循环处理，继续检查下一条文字或下一个候选。
            continue;
          }
          // 新第 317 行：输入锚点所在的整数像素坐标；调用前已检查是否在深度图内。
          const int x = int(xy[0]);
          // 新第 318 行：输入锚点所在的整数像素坐标；调用前已检查是否在深度图内。
          const int y = int(xy[1]);
          // 新第 319 行：确保整数像素索引位于深度数组尺寸内，避免无效内存读取。
          if (x < 0 || y < 0 || x >= dt->depths->w || y >= dt->depths->h) {
            // 新第 320 行：标记这条缓存文字不可画；最终 BLF 绘制函数会跳过它。
            vos.sco[0] = IS_CLIPPED;
            // 新第 321 行：结束本次循环处理，继续检查下一条文字或下一个候选。
            continue;
          }
          /* Apply local surface reconstruction only in perspective views, where subpixel
           * depth differences caused visible text to flicker. */
          // 新第 325 行：读取锚点所在像素的场景表面深度，作为遮挡基础比较。
          const float scene_depth = dt->depths->depths[y * dt->depths->w + x];
          // 新第 326 行：统一背景深度和锚点深度的单像素基础判断。
          bool occluded = text_depth_is_occluded(anchor_depth, scene_depth);
          // 新第 327 行：用当前视图的真实投影类型决定是否运行透视专用补偿。
          if (occluded && rv3d->is_persp) {
            // 新第 328 行：仅透视视图初判遮挡时尝试子像素局部平面补偿。
            occluded = text_anchor_is_occluded_perspective(*dt->depths, x, y, xy, anchor_depth);
          }
          // 新第 330 行：最终仍被遮挡时，把这条文字标记为裁剪并跳过绘制。
          if (occluded) {
            // 新第 331 行：标记这条缓存文字不可画；最终 BLF 绘制函数会跳过它。
            vos.sco[0] = IS_CLIPPED;
            // 新第 332 行：结束本次循环处理，继续检查下一条文字或下一个候选。
            continue;
          }
        }
        tot++;
      }
      else {
```

<details>
<summary>核对本块原始 diff（28 条修改）</summary>

```diff
@@ -190,6 +304,34 @@ void DRW_text_cache_draw(DRWTextStore *dt, const ARegion *region, const View3D *
               V3D_PROJ_TEST_CLIP_BB | V3D_PROJ_TEST_CLIP_WIN | V3D_PROJ_TEST_CLIP_NEAR) ==
           V3D_PROJ_RET_OK)
       {
+        if (use_occlusion_test && (vos.flag & DRW_TEXT_CACHE_OCCLUSION_TEST) != 0) {
+          /* Re-project keeping the depth so it can be compared with the scene depth. */
+          float xy[2];
+          float anchor_depth;
+          const float (&persmat)[4][4] = (vos.flag & DRW_TEXT_CACHE_GLOBALSPACE) ? rv3d->persmat :
+                                                                                   rv3d->persmatob;
+          if (!text_anchor_project_with_depth(*region, persmat, vos.vec, xy, anchor_depth)) {
+            vos.sco[0] = IS_CLIPPED;
+            continue;
+          }
+          const int x = int(xy[0]);
+          const int y = int(xy[1]);
+          if (x < 0 || y < 0 || x >= dt->depths->w || y >= dt->depths->h) {
+            vos.sco[0] = IS_CLIPPED;
+            continue;
+          }
+          /* Apply local surface reconstruction only in perspective views, where subpixel
+           * depth differences caused visible text to flicker. */
+          const float scene_depth = dt->depths->depths[y * dt->depths->w + x];
+          bool occluded = text_depth_is_occluded(anchor_depth, scene_depth);
+          if (occluded && rv3d->is_persp) {
+            occluded = text_anchor_is_occluded_perspective(*dt->depths, x, y, xy, anchor_depth);
+          }
+          if (occluded) {
+            vos.sco[0] = IS_CLIPPED;
+            continue;
+          }
+        }
         tot++;
       }
       else {
```

</details>

## 差异块 4 · `void DRW_text_cache_draw(DRWTextStore *dt, const ARegion *region, const View3D *`

下面按源码顺序阅读本块的 15 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  }
}

// 新第 376 行：文字缓存只借用深度指针；分配、按帧刷新与释放由 Overlay Instance 负责。
void DRW_text_cache_depth_set(DRWTextStore *dt, const ViewDepths *depths)
{
  // 新第 378 行：仅保存调用者拥有的 ViewDepths 地址，没有复制整张深度图，也不转移所有权。
  dt->depths = depths;
}

// 新第 381 行：检查缓存里是否有任何需要遮挡测试的文字，决定是否值得 GPU 回读。
bool DRW_text_cache_needs_depth_test(const DRWTextStore *dt)
{
  // 新第 383 行：逐个处理集合元素；上方专题说明循环对象与成本。
  for (const ViewCachedString &vos : dt->cache_strings) {
    // 新第 384 行：在文字标志中增加或检查遮挡测试位；只有带此位的缓存条目需要深度比较。
    if (vos.flag & DRW_TEXT_CACHE_OCCLUSION_TEST) {
      // 新第 385 行：至少一条文字带深度测试位，本帧应准备场景深度。
      return true;
    }
  }
  // 新第 388 行：扫描完全部文字，没有一条要求深度测试。
  return false;
}

void DRW_text_edit_mesh_measure_stats(const ARegion *region,
                                      const View3D *v3d,
                                      const Object *ob,
```

<details>
<summary>核对本块原始 diff（15 条修改）</summary>

```diff
@@ -231,6 +373,21 @@ void DRW_text_cache_draw(DRWTextStore *dt, const ARegion *region, const View3D *
   }
 }
 
+void DRW_text_cache_depth_set(DRWTextStore *dt, const ViewDepths *depths)
+{
+  dt->depths = depths;
+}
+
+bool DRW_text_cache_needs_depth_test(const DRWTextStore *dt)
+{
+  for (const ViewCachedString &vos : dt->cache_strings) {
+    if (vos.flag & DRW_TEXT_CACHE_OCCLUSION_TEST) {
+      return true;
+    }
+  }
+  return false;
+}
+
 void DRW_text_edit_mesh_measure_stats(const ARegion *region,
                                       const View3D *v3d,
                                       const Object *ob,
```

</details>

---

本文件列出 4 个差异块、157 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
