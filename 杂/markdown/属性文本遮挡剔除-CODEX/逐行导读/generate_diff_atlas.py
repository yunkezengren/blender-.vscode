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
    if s == "prop,":
        return "继续配置刚创建的同一个 RNA 属性描述对象。"
    if "Hide Viewer attribute text when its anchor" in s:
        return "悬停提示明确说明判断对象是文字锚点与场景几何，不是每个字形像素。"
    if "occlusion_test_" in s and "=" in s:
        return "保存本帧是否要求遮挡测试，供后续锚点准备和文字标志传播使用。"
    if "occlusion_test_" in s:
        return "使用组件级遮挡开关，决定是否调整锚点或给文字附加测试标志。"
    if "DRW_TEXT_CACHE_OCCLUSION_TEST" in s:
        return "在文字标志中增加或检查遮挡测试位；只有带此位的缓存条目需要深度比较。"
    if "text_flags" in s:
        return "将世界坐标位与可选的遮挡位合成，传给所有类型的属性文字。"
    if "instances->attributes()" in s:
        return "传入 Instances 的属性访问器，之后只切出当前实例的 Viewer 值。"
    if "ob_ref.preview_instance_index()" in s:
        return "传入当前预览实例下标，避免为所有实例重复生成文字。"
    if s == "object,":
        return "传入实例对象，后续用它查询本地 AABB。"
    if s == "object_to_world,":
        return "传入本地到世界矩阵，最终用于实例锚点的世界变换。"
    if "add_instance_attributes_to_text_cache" in s:
        return "调用实例域专用入口，读取当前实例值并准备盒出口锚点。"
    if s == "attribute.varray,":
        return "Viewer 的虚拟值数组，与下方位置逐下标配对。"
    if "corner_positions.as_span()" in s:
        return "网格角域已经计算好的位置数组，以不拥有内存的只读 Span 传入。"
    if s == "position,":
        return "多行值共用同一个三维锚点，二维布局偏移在下一层单独计算。"
    if s.startswith("{StringRef("):
        return "把已格式化的各分量组合成多行字符串视图。"
    if s == "col,":
        return "继续传入当前主题文字颜色；它不参与遮挡比较。"
    if s == "flag,":
        return "继续传入文字位标志，保留是否进行深度测试的选择。"
    if "DRW_text_cache_add(dt, position" in s:
        return "把锚点、字符串、标志、颜色与布局参数登记到通用文字缓存。"
    if "add_text_to_cache" in s or "add_lines_to_cache" in s:
        return "把这一类型的属性值登记成一行或多行文字，并把共同的标志传到底层缓存。"
    if "add_values_to_text_cache" in s:
        return "复用统一的属性格式化入口；额外传入是否做遮挡测试或已调整的锚点数组。"
    if "add_pointcloud_attributes_to_text_cache" in s:
        return "点云改用专门入口，以便读取每点半径并把文字锚点移到圆盘前方。"
    if "pointcloud.radius()" in s:
        return "取得逐点半径；每条点云文字使用它对应点自己的半径。"
    if "const bke::AttributeAccessor attributes" in s:
        return "取得几何的只读属性访问器，下一步检查 `.viewer` 是否存在。"
    if 'attributes.contains(".viewer")' in s:
        return "没有 Viewer 属性就不生产文字，避免访问缺失数据。"
    if 'attributes.lookup(".viewer")' in s:
        return "读取 Viewer 属性，取得类型擦除的值数组。"
    if "Array<float3> anchors" in s:
        return "按点数分配临时世界锚点数组，循环中每个点独立填写。"
    if "math::transform_point(object_to_world, positions[i])" in s:
        return "将第 i 个点由对象本地变到世界空间。"
    if s == "state.camera_forward;":
        return "正交视图所有视线平行，使用本帧统一观察方向。"
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
    if "world_center = object_to_world.location()" in s:
        return "提取实例本地原点的世界位置，作为朝相机方向的起点。"
    if "isect_ray_aabb_v3_simple" in s:
        return "测试从本地原点出发的射线与轴对齐包围盒相交，并取得出口参数。"
    if "exit_t" in s:
        return "射线出口参数；透视方向未归一化，t=1 对应相机位置。"
    if "local_anchor" in s:
        return "实例文字本地锚点；初始在原点，条件满足时移向包围盒朝相机的出口。"
    if "const ViewDepths *depths" in s:
        return "文字缓存只借用深度指针；分配、按帧刷新与释放由 Overlay Instance 负责。"
    if "ViewDepths" in s or "text_depth_cache_" in s:
        return "处理 Instance 拥有的 CPU 深度缓存；对象可复用，像素数据必须按本帧刷新。"
    if "DRW_text_cache_depth_set" in s:
        return "把当前深度缓存的借用指针交给文字系统，传空值时解除借用。"
    if "dt->depths = depths" in s:
        return "仅保存调用者拥有的 ViewDepths 地址，没有复制整张深度图，也不转移所有权。"
    if "DRW_text_cache_needs_depth_test" in s:
        return "检查缓存里是否有任何需要遮挡测试的文字，决定是否值得 GPU 回读。"
    if "GPU_texture_read" in s:
        return "将本帧视口深度纹理回读到 CPU；有目标缓冲的重载会刷新已分配数组。"
    if "WM_draw_region_get_viewport" in s:
        return "从当前 ARegion 找到对应 GPUViewport；现有接口需要非 const 区域指针。"
    if "GPU_viewport_depth_texture" in s:
        return "取得这个 GPUViewport 的深度纹理，后续回读其本帧像素。"
    if "GPU_texture_width" in s or "GPU_texture_height" in s:
        return "读取当前深度纹理尺寸；尺寸变化时必须重建 CPU 数组。"
    if "update_text_depth" in s:
        return "在 prepass 之后、grid 之前读取场景深度，供后续文字绘制使用。"
    if "depths = nullptr" in s or "const ViewDepths *depths" in s:
        return "文字存储只借用由 Instance 维护的深度数据；默认空值表示不测试。"
    if "text_anchor_project_with_depth" in s:
        return "将三维锚点投影为浮点屏幕位置和窗口深度，供像素采样与比较。"
    if "const ARegion &region" in s:
        return "输入当前视口区域；其宽高用于把标准化投影坐标换算成像素。"
    if "const float perspmat[4][4]" in s:
        return "输入组合投影矩阵；世界锚点使用 persmat，本地锚点使用 persmatob。"
    if "const float co[3]" in s:
        return "输入三维文字锚点，单位及空间必须与选择的投影矩阵一致。"
    if "float r_xy[2]" in s:
        return "输出浮点屏幕坐标；保留子像素偏移，供后续平面补偿使用。"
    if "float &r_depth" in s:
        return "输出 [0,1] 窗口深度，供 CPU 锚点与 GPU 场景深度比较。"
    if "float vec4[4]" in s:
        return "为齐次坐标预留 x、y、z、w 四个分量。"
    if "copy_v3_v3(vec4, co)" in s:
        return "先复制锚点的三个位置分量，下一行再将 w 设为 1。"
    if "vec4[3] = 1.0f" in s:
        return "齐次位置使用 w=1，使投影矩阵的平移项对它生效。"
    if "mul_m4_v4" in s:
        return "用视图投影矩阵变换齐次坐标，得到裁剪空间四维向量。"
    if "vec4[3]" in s or "const float w" in s:
        return "齐次坐标 w 参与透视除法；零值不能作为除数。"
    if "vec4[2]" in s and ("<= " in s or ">=" in s):
        return "排除投影深度裁剪范围以外的锚点。"
    if "const float fx" in s or "const float fy" in s:
        return "把 NDC 横纵坐标从 [-1,1] 映射到视口像素位置。"
    if "if (w == 0.0f)" in s:
        return "防止透视除法除以零；这种锚点不能产生可靠屏幕坐标。"
    if "const float scalar" in s:
        return "预先计算 1/w，随后分别乘裁剪空间 x、y、z。"
    if "fx <= 0.0f" in s or "fy <= 0.0f" in s:
        return "拒绝视口外的锚点，避免得到不可用的深度像素下标。"
    if "r_xy[" in s:
        return "把算好的浮点像素位置写到输出数组，供调用者选深度像素。"
    if "r_depth =" in s:
        return "把窗口深度写到输出引用，供后续遮挡比较。"
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
    if "const ViewDepths &depths" in s:
        return "读取本帧 CPU 深度缓存，函数不取得其所有权。"
    if "const int x" in s or "const int y" in s:
        return "输入锚点所在的整数像素坐标；调用前已检查是否在深度图内。"
    if "const float xy[2]" in s:
        return "输入未舍入的浮点屏幕位置，求与像素中心的差。"
    if s == "float xy[2];":
        return "为第二次投影准备浮点屏幕坐标输出，保留子像素部分。"
    if s == "rv3d->persmatob;":
        return "不带 GLOBALSPACE 位时使用已经包含对象变换的投影矩阵。"
    if "const float anchor_depth" in s:
        return "输入锚点的 [0,1] 窗口深度，和采样或重建的场景深度比较。"
    if "const float center" in s:
        return "读取中心像素的场景深度；先用它做低成本基础判断。"
    if "if (!text_depth_is_occluded" in s:
        return "中心像素已允许显示时直接返回，不访问邻域。"
    if "x + 2 * sx" in s:
        return "一个候选象限需要向同一方向走两像素；越界时跳过，避免数组越界。"
    if "for (const int sy" in s or "for (const int sx" in s:
        return "尝试四个象限，让折角附近的单侧连续面也有机会通过检查。"
    if "step_x" in s or "step_y" in s:
        return "由邻近像素估计平面沿屏幕 x/y 方向的每像素深度变化。"
    if "reconstructed" in s:
        return "把中心像素深度外推到锚点真实子像素位置，并比较锚点是否仍在表面之后。"
    if "for (int j" in s or "for (int i" in s:
        return "遍历候选象限 3×3 样本，验证它们能否由同一深度平面解释。"
    if "const float sample" in s:
        return "读取此格子的实际 GPU 深度；随后与局部平面预测值比较。"
    if "const float predicted" in s:
        return "按横纵像素步数用同一斜率计算应有深度。"
    if "planar = false" in s:
        return "发现背景或残差过大，当前象限不再可信。"
    if "if (planar)" in s:
        return "只有九样本都通过一致性检查，才允许此候选纠正基础误判。"
    if "sample" in s or "predicted" in s:
        return "比较实际深度与候选平面预测值；背景或残差过大使候选失效。"
    if "planar" in s:
        return "记录候选 3×3 区域是否符合单一平面；只有通过时可放行文字。"
    if "scene_depth" in s:
        return "读取锚点所在像素的场景表面深度，作为遮挡基础比较。"
    if "use_occlusion_test =" in s:
        return "只有借来的 ViewDepths 和像素数组都非空，才允许逐条深度测试。"
    if "x < 0 || y < 0" in s:
        return "确保整数像素索引位于深度数组尺寸内，避免无效内存读取。"
    if s == "if (occluded) {":
        return "最终仍被遮挡时，把这条文字标记为裁剪并跳过绘制。"
    if "bool occluded =" in s:
        return "先得到单像素遮挡结论；只有需要时再调用透视局部补偿。"
    if "rv3d->is_persp" in s:
        return "用当前视图的真实投影类型决定是否运行透视专用补偿。"
    if "const float (&persmat)" in s:
        return "根据 GLOBALSPACE 位选择世界矩阵或对象本地矩阵的引用。"
    if "const int x = int(" in s or "const int y = int(" in s:
        return "把浮点屏幕位置转成深度图的整数像素下标。"
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
    if "const char" in s or "const StringRef" in s:
        return "传入要缓存的文字内容或只读字符串视图；后续缓存按标志处理存储。"
    if "const float3 &position" in s:
        return "输入每条文字的三维锚点；深度测试在此位置进行，不逐字形像素检测。"
    if "const uchar4 &color" in s:
        return "传入主题颜色，不改变锚点或深度判断。"
    if "const Span<StringRef> lines" in s:
        return "多行属性值共享锚点，各行只增加二维文本布局偏移。"
    if "const float4x4 &object_to_world" in s:
        return "输入本地到世界的变换；点云已转世界时改传单位矩阵。"
    if "const State &state" in s:
        return "读取本帧视图、相机位置/方向与文字缓存指针。"
    if "const Object &object" in s:
        return "输入正在预览的实例对象，以查询它自己的本地包围盒。"
    if "const PointCloud &pointcloud" in s:
        return "输入点云几何，读取位置、Viewer 值与逐点半径。"
    if "int instance_index" in s:
        return "只处理这一实例的 Viewer 值，不枚举整个实例集合。"
    if "const bool occlusion_test" in s:
        return "调用者指定是否给生成的文字附加遮挡测试位。"
    if "const GVArray &values" in s:
        return "输入类型擦除的 Viewer 属性值数组，函数内部再按实际类型格式化。"
    if "const Span<float3> positions" in s:
        return "输入与值逐下标配对的锚点位置数组；Span 本身不拥有内存。"
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
        "> 每个主代码块以源码顺序保留三行上下文；有语义的修改行旁带中文注释与新行号。",
        "> 结构性空行、括号及原有英文源码注释保持原貌，便于顺着代码阅读。删除的旧行以注释显示；原始 diff 放在折叠区。",
        "> 这些代码块是阅读材料，不用于直接编译。",
        "> 完整的背景、数学、所有权和风险请先读上一层专题。",
        "",
    ]
    old = new = 0
    hunk = 0
    changed = 0
    scope = ""
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
                if "text_anchor_project_with_depth(" in line:
                    scope = "project"
                elif "text_anchor_is_occluded_perspective(" in line:
                    scope = "perspective"
                elif "DRW_text_cache_needs_depth_test(" in line:
                    scope = "needs_depth"
                elif "DRW_text_cache_draw(" in line:
                    scope = "draw"
                if line[0] == " ":
                    annotated.append(line[1:])
                    old += 1
                    new += 1
                elif line[0] == "+":
                    changed += 1
                    changed_in_hunk += 1
                    source = line[1:]
                    indent = source[: len(source) - len(source.lstrip())]
                    stripped = source.strip()
                    structural = not stripped or stripped in {"{", "}", "};", "});", "})"}
                    source_comment = stripped.startswith(("/*", "*", "//"))
                    if not structural and not source_comment:
                        note = explain(file, source, "+")
                        if stripped == "return false;":
                            note = {
                                "project": "投影输入不可用或在视口外；调用者会把这条文字标为裁剪。",
                                "perspective": "发现可用的同表面平面，撤销中心像素造成的遮挡初判。",
                                "needs_depth": "扫描完全部文字，没有一条要求深度测试。",
                            }.get(scope, note)
                        elif stripped == "return true;":
                            note = {
                                "project": "浮点屏幕坐标与窗口深度均已写入输出参数。",
                                "perspective": "四象限都没有通过检查，保留基础遮挡结论。",
                                "needs_depth": "至少一条文字带深度测试位，本帧应准备场景深度。",
                            }.get(scope, note)
                        annotated.append(f"{indent}{comment_prefix} 新第 {new} 行：{note}")
                    annotated.append(source)
                    new += 1
                else:
                    changed += 1
                    changed_in_hunk += 1
                    source = line[1:]
                    indent = source[: len(source) - len(source.lstrip())]
                    stripped = source.strip()
                    if stripped and stripped not in {"{", "}", "};", "});", "})"}:
                        note = explain(file, source, "−")
                        annotated.append(f"{indent}{comment_prefix} 旧第 {old} 行已替换：{note}")
                        annotated.append(f"{indent}{comment_prefix} 原代码：{stripped}")
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
