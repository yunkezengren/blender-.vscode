# diagrams/ 目录说明

每张交互式架构图 = **两个文件**：`candidate.json`（我手写的图源，改图改它）+ `<编号>_<名>_架构图.html`（archify 生成的成品）。查看器引擎/样式/字体全部外链自 [`../_shared/`](../_shared/base.css.html)，所以每个 HTML 只有 ~70KB。

## 现役图

| 图 | 源 | 主题 | 被谁引用 |
| --- | --- | --- | --- |
| [06a_VectorSet_架构图.html](06a_VectorSet_架构图.html) | `06a_candidate.json` | VectorSet 双容器机制 | 06a 深度解析 / 06a 布局图解 |
| [06b1_Map_架构图.html](06b1_Map_架构图.html) | `06b1_candidate.json` | Map 单容器详细版（add 家族/CPython 探测/双槽型） | 06b md / 06b Map 布局图解 |
| [06b2_Set_架构图.html](06b2_Set_架构图.html) | `06b2_candidate.json` | Set 槽选择谱系 / HashedSetSlot | 06b md / 06b Set 布局图解 |

## 重新生成一张图

```bash
# 1. 改 candidate.json（组件/连线/坐标）
# 2. 重新生成（浏览器门禁）
set ARCHIFY_CHROME=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
node <archify.mjs> finalize architecture <candidate.json> <输出.html> --repo-root . --quality showcase --json
# 3. 外链化三件（fonts/样式/引擎 → _shared），注入 patch link
# 4. 门禁回执移入 _receipts/<编号>/
```

## `_receipts/`

archify 门禁回执（finalize/browser-check 证据），按图编号分目录；`retired/` 存放已退役的旧合图（06b_MapSet 合图被 06b1/06b2 取代）。回执不参与渲染，仅供追溯验证。
