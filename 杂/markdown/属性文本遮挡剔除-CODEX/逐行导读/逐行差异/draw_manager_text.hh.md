# `source/blender/draw/intern/draw_manager_text.hh`：逐行差异与上下文

> 基准 `bba93a5d6df198bcdb31b7b92cdbe514945ba2ad`；当前工作树。`+` 为新行，`−` 为旧行。
> 每个主代码块以源码顺序保留三行上下文；有语义的修改行旁带中文注释与新行号。
> 结构性空行、括号及原有英文源码注释保持原貌，便于顺着代码阅读。删除的旧行以注释显示；原始 diff 放在折叠区。
> 这些代码块是阅读材料，不用于直接编译。
> 完整的背景、数学、所有权和风险请先读上一层专题。

## 差异块 1 · `struct DRWTextStore;`

下面按源码顺序阅读本块的 1 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
struct Object;
struct UnitSettings;
struct View3D;
// 新第 20 行：处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。
struct ViewDepths;

DRWTextStore *DRW_text_cache_create();
void DRW_text_cache_destroy(DRWTextStore *dt);
```

<details>
<summary>核对本块原始 diff（1 条修改）</summary>

```diff
@@ -17,6 +17,7 @@ struct DRWTextStore;
 struct Object;
 struct UnitSettings;
 struct View3D;
+struct ViewDepths;
 
 DRWTextStore *DRW_text_cache_create();
 void DRW_text_cache_destroy(DRWTextStore *dt);
```

</details>

## 差异块 2 · `void DRW_text_cache_add(DRWTextStore *dt,`

下面按源码顺序阅读本块的 13 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp

void DRW_text_cache_draw(DRWTextStore *dt, const ARegion *region, const View3D *v3d);

/**
 * Provide the scene depth read-back used by strings flagged with
 * #DRW_TEXT_CACHE_OCCLUSION_TEST. The store does not take ownership; the caller keeps the
 * #ViewDepths alive until the next #DRW_text_cache_draw. Pass null to disable the tests.
 */
// 新第 46 行：文字缓存只借用深度指针；分配、按帧刷新与释放由 Overlay Instance 负责。
void DRW_text_cache_depth_set(DRWTextStore *dt, const ViewDepths *depths);

/**
 * True when at least one cached string is flagged with #DRW_TEXT_CACHE_OCCLUSION_TEST, meaning
 * the caller should provide the scene depth with #DRW_text_cache_depth_set before drawing.
 */
// 新第 52 行：检查缓存里是否有任何需要遮挡测试的文字，决定是否值得 GPU 回读。
bool DRW_text_cache_needs_depth_test(const DRWTextStore *dt);

void DRW_text_edit_mesh_measure_stats(const ARegion *region,
                                      const View3D *v3d,
                                      const Object *ob,
```

<details>
<summary>核对本块原始 diff（13 条修改）</summary>

```diff
@@ -37,6 +38,19 @@ void DRW_text_cache_add(DRWTextStore *dt,
 
 void DRW_text_cache_draw(DRWTextStore *dt, const ARegion *region, const View3D *v3d);
 
+/**
+ * Provide the scene depth read-back used by strings flagged with
+ * #DRW_TEXT_CACHE_OCCLUSION_TEST. The store does not take ownership; the caller keeps the
+ * #ViewDepths alive until the next #DRW_text_cache_draw. Pass null to disable the tests.
+ */
+void DRW_text_cache_depth_set(DRWTextStore *dt, const ViewDepths *depths);
+
+/**
+ * True when at least one cached string is flagged with #DRW_TEXT_CACHE_OCCLUSION_TEST, meaning
+ * the caller should provide the scene depth with #DRW_text_cache_depth_set before drawing.
+ */
+bool DRW_text_cache_needs_depth_test(const DRWTextStore *dt);
+
 void DRW_text_edit_mesh_measure_stats(const ARegion *region,
                                       const View3D *v3d,
                                       const Object *ob,
```

</details>

## 差异块 3 · `enum {`

下面按源码顺序阅读本块的 5 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。

```cpp
  DRW_TEXT_CACHE_LOCALCLIP = (1 << 2),
  /* reference the string by pointer */
  DRW_TEXT_CACHE_STRING_PTR = (1 << 3),
  /**
   * Test the anchor against the scene depth before drawing: when the surface of the scene is in
   * front of the anchor, the string is skipped. Only supported while drawing in 3D space.
   */
  // 新第 70 行：在文字标志中增加或检查遮挡测试位；只有带此位的缓存条目需要深度比较。
  DRW_TEXT_CACHE_OCCLUSION_TEST = (1 << 4),
};

}  // namespace blender
```

<details>
<summary>核对本块原始 diff（5 条修改）</summary>

```diff
@@ -49,6 +63,11 @@ enum {
   DRW_TEXT_CACHE_LOCALCLIP = (1 << 2),
   /* reference the string by pointer */
   DRW_TEXT_CACHE_STRING_PTR = (1 << 3),
+  /**
+   * Test the anchor against the scene depth before drawing: when the surface of the scene is in
+   * front of the anchor, the string is skipped. Only supported while drawing in 3D space.
+   */
+  DRW_TEXT_CACHE_OCCLUSION_TEST = (1 << 4),
 };
 
 }  // namespace blender
```

</details>

---

本文件列出 3 个差异块、19 条新增或删除行。
行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。
