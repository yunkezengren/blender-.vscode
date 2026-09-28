"""Regenerate nine source-diff reading sheets from the current working tree."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "source/blender/draw/intern/draw_manager_text.cc").is_file()
)
OUT = Path(__file__).resolve().parent / "逐行差异"
OUT.mkdir(exist_ok=True)
FILES = [
    "source/blender/makesdna/DNA_view3d_types.h",
    "source/blender/makesrna/intern/rna_space.cc",
    "scripts/startup/bl_ui/space_view3d.py",
    "source/blender/draw/engines/overlay/overlay_private.hh",
    "source/blender/draw/engines/overlay/overlay_attribute_text.hh",
    "source/blender/draw/intern/draw_manager_text.hh",
    "source/blender/draw/engines/overlay/overlay_instance.hh",
    "source/blender/draw/engines/overlay/overlay_instance.cc",
    "source/blender/draw/intern/draw_manager_text.cc",
]
BASE = subprocess.check_output(
    ["git", "merge-base", "origin/main", "HEAD"], cwd=ROOT, text=True
).strip()


def explain(file: str, raw: str, action: str) -> str:
    s = raw.strip()
    if not s:
        return "空行用于隔开两个逻辑步骤，使下一段条件或函数更容易识别。"
    if s in {"{", "}", "};", "};", "})", "});"}:
        return "控制本段 C++ 作用域或调用闭合；变量生命周期和条件范围由这些括号决定。"
    if s.startswith(("/*", "*", "//")):
        comment = s.strip("/* ")
        if "Scene depth read back" in s:
            return "说明这份深度由调用者在画会改写深度的 Overlay 之前读回。"
        if "Borrowed through" in s:
            return "强调这里只借用指针，并且需要按帧刷新深度内容。"
        if "window-space position" in s:
            return "说明辅助函数同时给出屏幕浮点位置和窗口深度。"
        if "same math" in s:
            return "强调要与现有 View3D 投影路径使用一致的矩阵和坐标换算。"
        if "viewport depth buffer" in s:
            return "说明 CPU 计算出的深度要与 GPU 回读的视口深度比较。"
        if "Outside the near/far" in s:
            return "深度裁剪范围外的点没有可比较的有效视口像素。"
        if "Window depth" in s:
            return "同一投影三角形的窗口深度在屏幕坐标上可由局部平面表达。"
        if "Reconstruct that plane" in s:
            return "说明选择局部平面重建，而非给所有斜率施加固定上限。"
        if "quadrant" in s or "crease" in s:
            return "四个象限分别尝试，折角的一侧仍可能提供连续表面。"
        if "2x2 patch" in s:
            return "仅两个采样步长不足以排除物体轮廓产生的深度阶跃。"
        if "three" in s and "samples" in s:
            return "沿横纵各检查三个样本，确认深度变化持续符合一个平面。"
        if "planarity" in s or "slope" in s:
            return "容差限制的是九样本拟合残差，并不限制表面斜率大小。"
        if "before the grid" in s or "axes" in s:
            return "回读必须早于网格线和坐标轴写入深度，避免细线误挡文字。"
        if "point-cloud" in s or "camera-facing disk" in s:
            return "点云中心在自身有半径的圆盘后方，应为每个点前移锚点。"
        if "instance origin" in s or "local bounds" in s:
            return "实例原点可能位于自身内部，盒出口是轻量的前表面近似。"
        if "unnormalized direction" in s or "t = 1" in s:
            return "透视射线保留原点到相机的完整向量，因此参数 1 对应相机。"
        if "Root-mean-square" in s:
            return "说明点云半径使用与 shader 相同的对象缩放均方根。"
        return f"保留源码说明：{comment[:75]}；相邻代码的中文推导见专题章节。" if comment else "源码注释的起止符号。"
    if s.startswith("#include"):
        return f"加入直接依赖 `{s.split(maxsplit=1)[1]}`，供本文件新用到的声明、容器或算法使用。"
    if "V3D_OVERLAY_VIEWER_TEXT_OCCLUSION_CULLING" in s:
        return "引用持久化选项位：DNA 定义它，RNA 映射它，State 通过位与运算查询它。"
    if "viewer_text_occlusion_culling" in s:
        return "使用同名设置；Python 属性名、RNA 注册名与 C++ 查询函数分别处于不同层。"
    if "row.active" in s:
        return "三个上游显示条件同时成立时才允许用户操作这个子选项。"
    if "row = col.row" in s:
        return "在 Viewer Overlay 面板中新建一行控件。"
    if "RNA_def_property_boolean_sdna" in s or '"overlay.flag"' in s:
        return "把 RNA 布尔值映射到底层 `overlay.flag` 指定的掩码位。"
    if "RNA_def_property_update" in s:
        return "属性变化后通知 3D 视图刷新，使下一帧读取新设置。"
    if "PROP_ANIMATABLE" in s:
        return "把视口开关标为非动画属性。"
    if "RNA_def_property_ui_text" in s or '"Occlusion Culling"' in s:
        return "配置用户看到的选项标题和悬停说明。"
    if "occlusion_test_" in s and "=" in s:
        return "保存本帧是否要求遮挡测试，供后续锚点准备和文字标志传播使用。"
    if "occlusion_test_" in s:
        return "使用组件级遮挡开关，决定是否调整锚点或给文字附加测试标志。"
    if "DRW_TEXT_CACHE_OCCLUSION_TEST" in s:
        return "在文字标志中增加或检查遮挡测试位；只有带此位的缓存条目需要深度比较。"
    if "text_flags" in s:
        return "将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。"
    if "add_text_to_cache" in s or "add_lines_to_cache" in s:
        return "把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。"
    if "add_values_to_text_cache" in s:
        return "复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。"
    if "add_pointcloud_attributes_to_text_cache" in s:
        return "点云改用专门入口，以便读取每点半径并把文字锚点移到圆盘前方。"
    if "pointcloud.radius()" in s:
        return "取得逐点半径；每条点云文字使用它对应点自己的半径。"
    if "radius_scale" in s:
        return "把对象三个轴的缩放折合为点云 shader 使用的世界半径尺度。"
    if "to_camera" in s or "toward_camera" in s:
        return "透视从点指向相机位置；正交使用统一观察方向。"
    if "direction" in s and "1.0e-20" in s:
        return "避免对零长度或近零向量归一化，防止数值无效。"
    if "anchors[i]" in s:
        return "为第 i 个点设置独立世界坐标锚点：点中心加上朝相机方向的半径偏移。"
    if "float4x4::identity" in s:
        return "锚点已在世界空间，传单位矩阵避免公共函数重复应用对象变换。"
    if "BKE_object_boundbox_get" in s:
        return "查询实例对象的本地 AABB；结果可能不存在，需先检查 optional。"
    if "bounds->contains" in s:
        return "只在实例原点落于包围盒内部时使用向相机的盒出口。"
    if "determinant" in s:
        return "排除不可可靠求逆的退化对象矩阵。"
    if "world_to_object" in s or "math::invert" in s:
        return "对象矩阵求逆，把朝相机的射线方向转换回包围盒所在的本地空间。"
    if "isect_ray_aabb_v3_simple" in s:
        return "测试从本地原点出发的射线与轴对齐包围盒相交，并取得出口参数。"
    if "exit_t" in s:
        return "射线出口参数；透视方向未归一化，t=1 对应相机位置。"
    if "local_anchor" in s:
        return "实例文字本地锚点；初始在原点，条件满足时移向包围盒朝相机的出口。"
    if "ViewDepths" in s or "text_depth_cache_" in s:
        return "处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。"
    if "DRW_text_cache_depth_set" in s:
        return "把当前深度缓存的借用指针交给文字系统，传空值时解除借用。"
    if "DRW_text_cache_needs_depth_test" in s:
        return "检查缓存里是否有任何需要遮挡测试的文字，决定是否值得 GPU 回读。"
    if "GPU_texture_read" in s:
        return "将本帧视口深度纹理回读到 CPU；有目标缓冲的重载会刷新已分配数组。"
    if "GPU_texture_width" in s or "GPU_texture_height" in s:
        return "读取当前深度纹理尺寸；尺寸变化时必须重建 CPU 数组。"
    if "update_text_depth" in s:
        return "在 prepass 之后、grid 之前读取场景深度，供后续文字绘制使用。"
    if "depths = nullptr" in s or "const ViewDepths *depths" in s:
        return "文字存储只借用由 Instance 维护的深度数据；默认空值表示不测试。"
    if "text_anchor_project_with_depth" in s:
        return "将三维锚点投影为浮点屏幕位置和窗口深度，供像素采样与比较。"
    if "mul_m4_v4" in s:
        return "用视图投影矩阵变换齐次坐标，得到裁剪空间四维向量。"
    if "vec4[3]" in s or "const float w" in s:
        return "齐次坐标 w 参与透视除法；零值不能作为除数。"
    if "vec4[2]" in s and ("<= " in s or ">=" in s):
        return "排除投影深度裁剪范围以外的锚点。"
    if "const float fx" in s or "const float fy" in s:
        return "把 NDC 横纵坐标从 [-1,1] 映射到视口像素位置。"
    if "ndc_z" in s or "const float depth" in s:
        return "把裁剪深度经透视除法与线性映射转成 [0,1] 窗口深度。"
    if "text_depth_bias" in s:
        return "最终遮挡比较容差，单位是 [0,1] 窗口深度。"
    if "text_depth_plane_tolerance" in s:
        return "局部平面九样本拟合残差容差，与最终遮挡容差用途不同。"
    if "text_depth_is_occluded" in s:
        return "统一背景深度和锚点深度的单像素基础判断。"
    if "text_anchor_is_occluded_perspective" in s:
        return "仅透视视图初判遮挡时尝试子像素局部平面补偿。"
    if "const float dx" in s or "const float dy" in s:
        return "计算锚点相对像素中心的偏移；整数像素格中心位于索引加 0.5。"
    if "for (const int sy" in s or "for (const int sx" in s:
        return "尝试四个象限，让折角附近的单侧连续面也有机会通过检查。"
    if "step_x" in s or "step_y" in s:
        return "由邻近像素估计平面沿屏幕 x/y 方向的每像素深度变化。"
    if "reconstructed" in s:
        return "把中心像素深度外推到锚点真实子像素位置，并比较锚点是否仍在表面之后。"
    if "for (int j" in s or "for (int i" in s:
        return "遍历候选象限 3×3 样本，验证它们能否由同一深度平面解释。"
    if "sample" in s or "predicted" in s:
        return "比较实际深度与候选平面预测值；背景或残差过大使候选失效。"
    if "planar" in s:
        return "记录候选 3×3 区域是否符合单一平面；只有通过时可放行文字。"
    if "scene_depth" in s:
        return "读取锚点所在像素的场景表面深度，作为遮挡基础比较。"
    if "anchor_depth" in s:
        return "文字三维锚点经投影后的窗口深度，与场景像素或重建平面比较。"
    if "IS_CLIPPED" in s:
        return "标记这条缓存文字不可画；最终 BLF 绘制函数会跳过它。"
    if "continue;" in s:
        return "结束本次循环处理，继续检查下一条文字或下一个候选。"
    if "return false;" in s:
        return "此条件下判定不遮挡、无有效投影，或当前候选失效；具体含义看所属函数。"
    if "return true;" in s:
        return "当前函数返回成功、需要深度，或最终判定遮挡；具体含义看所属函数。"
    if "const short flag" in s or "const short text_flags" in s:
        return "将每条文字的坐标空间与遮挡要求保存在位标志里。"
    if s.startswith("else"):
        return "处理与紧邻 if 条件相反的路径；结合上方上下文读取。"
    if s.startswith("if ("):
        return "用条件保护后续步骤，阻止无效数据、越界或不满足要求的绘制路径。"
    if s.startswith("for ("):
        return "逐个处理集合元素；上方专题说明循环对象与成本。"
    if s.startswith("return "):
        return "返回当前函数的判断或计算结果。"
    if s in {"break;", "continue;", "return;"}:
        return "提前结束当前分支，避免继续处理不适用的对象或候选。"
    if action == "−":
        return "旧实现中的这一行被新的参数传播、命名或分支逻辑替换；对照同块新增行和专题解释。"
    return "属于紧邻函数的参数、数据准备或语句续行；结合展开的上下文与专题章节阅读。"


def escape(s: str) -> str:
    return s.replace("`", "\\`")


for file in FILES:
    diff = subprocess.check_output(
        ["git", "diff", BASE, "--unified=3", "--", file],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    lines = diff.splitlines()
    out = [
        f"# `{file}`：逐行差异与上下文",
        "",
        f"> 基准 `{BASE}`；当前工作树。`+` 为新行，`−` 为旧行。",
        "> 每个主代码块以源码顺序保留三行上下文，并在修改行前加入中文注释与行号。",
        "> 删除的旧行在原位置以注释显示；原始 diff 放在折叠区，方便核对。代码块是阅读材料，不用于直接编译。",
        "> 完整的背景、数学、所有权和风险请先读上一层专题。",
        "",
    ]
    old = new = 0
    hunk = 0
    changed = 0
    i = 0
    while i < len(lines):
        match = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)", lines[i])
        if not match:
            i += 1
            continue
        old, new = int(match[1]), int(match[3])
        hunk += 1
        heading = match[5].strip() or "文件局部上下文"
        out += [f"## 差异块 {hunk} · `{escape(heading)}`", ""]
        code = [lines[i]]
        annotated = []
        kind = "python" if file.endswith(".py") else "cpp"
        comment_prefix = "#" if kind == "python" else "//"
        changed_in_hunk = 0
        i += 1
        while i < len(lines) and not lines[i].startswith("@@ "):
            line = lines[i]
            if line.startswith("diff --git"):
                break
            if line.startswith("\\ No newline"):
                code.append(line)
                i += 1
                continue
            if line and line[0] in " +-":
                code.append(line)
                if line[0] == " ":
                    annotated.append(line[1:])
                    old += 1
                    new += 1
                elif line[0] == "+":
                    changed += 1
                    changed_in_hunk += 1
                    source = line[1:]
                    indent = source[: len(source) - len(source.lstrip())]
                    note = explain(file, source, "+")
                    annotated.append(f"{indent}{comment_prefix} 新第 {new} 行：{note}")
                    annotated.append(source)
                    new += 1
                else:
                    changed += 1
                    changed_in_hunk += 1
                    source = line[1:]
                    indent = source[: len(source) - len(source.lstrip())]
                    note = explain(file, source, "−")
                    annotated.append(f"{indent}{comment_prefix} 旧第 {old} 行已替换：{note}")
                    annotated.append(f"{indent}{comment_prefix} 原代码：{source.strip() or '（空行）'}")
                    old += 1
            i += 1
        out += [
            f"下面按源码顺序阅读本块的 {changed_in_hunk} 条修改。没有“新/旧”标记的行是帮助定位的原有上下文。",
            "",
            f"```{kind}",
            *annotated,
            "```",
            "",
            "<details>",
            f"<summary>核对本块原始 diff（{changed_in_hunk} 条修改）</summary>",
            "",
            "```diff",
            *code,
            "```",
            "",
            "</details>",
            "",
        ]
    out += [
        "---",
        "",
        f"本文件列出 {hunk} 个差异块、{changed} 条新增或删除行。",
        "行号对应生成时的工作树；之后若继续修改源码，应重新运行 `generate_diff_atlas.py`。",
        "",
    ]
    (OUT / (Path(file).name + ".md")).write_text("\n".join(out), encoding="utf-8")
    print(Path(file).name, hunk, changed)
