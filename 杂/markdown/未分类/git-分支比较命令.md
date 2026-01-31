# Git 分支比较命令速查

> 在不切换分支的情况下比较当前分支与远程主分支的差异

---

## 1. 查看当前分支名称

```bash
git branch --show-current
```

**输出示例：**
```
improve-auto-view-instance
```

---

## 2. 查看与远程主分支的差异统计

```bash
git diff origin/main...HEAD --stat
```

**说明：**
- `origin/main...HEAD`：三点表示法，显示从 `origin/main` 到当前 HEAD 的所有更改
- `--stat`：仅显示统计信息（文件名、增删行数）

**输出示例：**
```
 source/blender/blenkernel/BKE_geometry_fields.hh   |  1 +
 .../blender/blenkernel/intern/geometry_fields.cc   | 42 ++++++++++++++++--
 .../draw/engines/overlay/overlay_attribute_text.hh |  2 --
 .../nodes/geometry/nodes/node_geo_viewer.cc        | 26 ++++++++++++--
 4 files changed, 64 insertions(+), 7 deletions(-)
```

---

## 3. 查看指定分支与远程主分支的差异

```bash
git diff origin/main...<分支名> --stat
```

**示例：**
```bash
git diff origin/main...alt-affect-selected-tree-items --stat
```

**输出示例：**
```
 source/blender/editors/interface/interface_ops.cc | 49 +++++++++++++++++++++++
 1 file changed, 49 insertions(+)
```

---

## 4. 查看提交历史（简洁模式）

```bash
git log origin/main..<分支名> --oneline
```

**说明：**
- `origin/main..<分支名>`：两点表示法，显示在分支但不在 main 的提交
- `--oneline`：单行显示提交哈希和消息

**示例：**
```bash
git log origin/main..alt-affect-selected-tree-items --oneline
```

**输出示例：**
```
f5d56db5296 Merge remote-tracking branch 'origin/main' into alt-affect-selected-tree-items
cea4e0c979a special handling for panel toggle
449f493a737 fix after merge
b7f371ec0d6 Merge remote-tracking branch 'origin/main' into alt-affect-selected-tree-items
1fd92b0b7b2 affect all selected items when holding alt
```

---

## 5. 查看详细差异内容

```bash
git diff origin/main...<分支名>
```

**示例：**
```bash
git diff origin/main...alt-affect-selected-tree-items
```

**输出示例：**
```diff
diff --git a/source/blender/editors/interface/interface_ops.cc b/source/blender/editors/interface/interface_ops.cc
index e36e933b01e..cb53a2e1bbe 100644
--- a/source/blender/editors/interface/interface_ops.cc
+++ b/source/blender/editors/interface/interface_ops.cc
@@ -75,6 +75,8 @@
 /* Only for #UI_OT_editsource. */
 #include "ED_screen.hh"
 
+#include "NOD_socket.hh"
+
 namespace blender {
...
```

---

## 三点表示法 vs 两点表示法

| 语法 | 含义 | 适用场景 |
|------|------|----------|
| `A...B` | 从 A 到 B 的所有更改 | 查看分支整体改动（包含合并提交） |
| `A..B` | 在 B 但不在 A 的提交 | 查看提交历史列表 |

---

## 常用参数速查

| 参数 | 功能 |
|------|------|
| `--stat` | 仅显示统计信息 |
| `--oneline` | 单行显示提交日志 |
| `--name-only` | 只显示文件名 |
| `-p` / `--patch` | 显示完整 diff（默认） |
| `--cached` / `--staged` | 比较暂存区与 HEAD |

---

## 完整工作流示例

```bash
# 1. 确认当前分支
git branch --show-current

# 2. 查看与 main 的差异概览
git diff origin/main...HEAD --stat

# 3. 查看提交历史
git log origin/main..HEAD --oneline

# 4. 查看详细代码差异
git diff origin/main...HEAD

# 5. 对比其他分支（不切换分支）
git diff origin/main...feature-branch --stat
git diff origin/main...feature-branch
```

---

*最后更新：2026-01-31*
