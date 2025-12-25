# todo 树视图多选:
新建时是否要取消全部的选中状态?
+ 设为活动项时要同步设置选中吧
多选后删除,新的活动项位置很奇怪
Should New / Make / Unlink Panel Toggle be updated to handle multi-selection?
空白处单击不要更改活动项的选中状态

#
<!-- todo 悬浮 -->
菜单 item 的悬浮

```c++
const float light_factor = (srgb_to_grayscale_byte(wt->wcol.text) > 96) ? 0.8f : 1.2f;
color_mul_hsl_v3(wt->wcol.inner, 1.0f, 1.0f, light_factor);
color_blend_v3_v3(wt->wcol.inner, wt->wcol.text, 0.2f);      // 不行,text是黑色时,导致混合的蓝色变暗
color_blend_v3_v3(wt->wcol.inner, wt->wcol.text_sel, 0.2f);  // 不行,亮色的text_sel也亮才行
color_blend_v3_v3(wt->wcol.inner, wt->wcol.inner_sel, 0.2f); // 不行,暗色主题不友好,无法保持现状
copy_v4_v4_uchar(wt->wcol.inner, wt->wcol.inner_sel);        // 不行,菜单枚举 活动 和 选中 一个颜色了
```

其他元素的悬浮会加亮,但是我已经是白色了啊 大纲视图,资产,文件视图
列分割线也要能配置
还有框选,还有编辑器区域移动/拆分/替换

#
树视图修改name后,tab 要循环下一个啊

#
todo 节点编辑器路径导航: 材质里点击顶层会崩

# 获取扩展里面的搜索不好用啊,模糊搜索弱?
Clean Blue, 用Clea Blue, C B ,cb搜不到啊
WindowManager.extension_search
scripts\addons_core\bl_pkg\__init__.py

WindowManager.addon_search
scripts\startup\bl_ui\__init__.py


#
<!-- + todo(w) 区域节点 插入连线 -->

todo 特殊情况: 选择了两个没连线的节点, 是区域输入和输出
todo 目前只有一个转接点才能插入, 如果是两个转接点就不能任意插入了
todo 但是起点终点多个同高优先级, 如果有区域输入出, 或者位置在边界那就是它了
todo 只选了节点框, 框内节点没全选, 插入到连线会有问题
todo 不应删旧线, 应设INVALID, 如Geo接口添加了采样编号
todo 如果鼠标在边界框内, 应该选距离鼠标最近的线
todo 节点偏移量改进
todo 遍历连线时排除选中的连线
todo 是否有更简单的凸包算法, 线段和凸包是否相交
todo 支持多输入的话还要考虑不要造成循环线
todo(w) 插入连线,
如果连线是向左下走的, 节点向下偏移不合适?
插入连线时可能的话更改数据类型?
移动节点过程中 按某个键 可以无视现有连线插入到别的连线里, 替换主连线, 保持次要连线
改进带扩展接口节点的插入, 比如烘焙, 材质节点添加的重复区域
输出接口隐藏的话还要考虑吗?
现在是找到输入输出的主接口, 根据优先级, 并不好,
应该是先找到输出的主接口, 然后再输入里找到匹配的(不一定是最高优先级), 这样也不对, 比如采样编号
todo ctrl x 后连线不应消失


todo 隐藏接口的问题
todo 从预设新添加节点可能不符合目前的规则(已连线接口在选中里,不符合)
todo const 修饰问题

todo 已连线能允许插入吗?
todo 非几何数据/最高优先级,已连线允许插入吗?

#

```c++
// todo(w) 节点在框上,却不属于框,要特殊绘制?
// todo(w) Zone Input Node
// todo(w) multi input ; for each link ?
// todo(w) 改进节点组界面bool接口的属性层选择: https://projects.blender.org/blender/blender/issues/146548
// todo(w) 从转接点创建节点组,不合适的宽度
// 拖动接口的鼠标样式在节点折叠按钮上效果不好
//       拖动后松开:立即改回默认
// todo(w) link route:
//      +改的竖线钳制重叠失效了
//      +多输入折叠的话 order 全改成一样
//      +竖线钳制重叠改成像横线那样微微位移?
//      +为什么有连线被面板折叠,其他线切/加转接点就崩溃
//      +通过一端接口是否可见来决定隐藏连线不太对,也可能是折叠进面板了
//      +从折叠输出面板 用VoronoiLinker连线崩溃
//      横向间距不够时竖线间距自动压缩
//      ?横线钳制怎么有时失效,好像又有效了
//      折叠近面板的类似多输入接口,把垂线钳制的特别近
//      多输入折叠,那些竖线不要钳制,要类似 origin 能识别到是一批
// todo(w) 鼠标悬浮到一些可点击项,不要轻微加亮,甚至要能改颜色
// todo(w) 改进查看器:背面剔除,面拐,更多选项
// todo(w) 改进查看器:文本重叠时逐渐减少小数位数
// todo(w) 改进查看器:网格线框网格点的颜色
// todo(w) 改进查看器:绘制矢量应该叠在网格线上
// todo(w) 改进查看器:绘制矢量 在面里有重叠;锯齿感太强;要叠在线框上才行
// todo(w) 改进查看器:绘制矢量 overlay_wireframe.hh 模仿改进 https://projects.blender.org/blender/blender/pulls/126242/files
// todo(w) 预览器: 增加的错误提示:比如网格,预览器选了曲线
// todo(w) 错误提示:捕捉属性或别的匿名属性 命名属性 用错/不存在给提示
// todo(w) 预览器: 鼠标连上线后是否自动切换数据类型
// todo(w) 预览器: 切换物体或节点树,活动查看器会失效
// todo(w) 几何节点搜索菜单: 支持搜索 浮点到整数; 比较节点的菜单(这个麻烦点,对于颜色,有更亮和更暗)
// todo(w) 匹配字符串的标签不会自动更新了
//+ todo(w) 调整转接点标签y位置
// todo(w) 整体UI缩放后,转接点位置会偏移
// todo(w) 同类型区域套区域,更改主题样式/颜色
// todo(w) 改进多输入接口移动顺序: 加一个 Item?
// todo(w) 主题里加上列分隔线,还是说根据文本颜色,亮的调暗,暗的调亮
// todo(w) 白色主题里: 编辑器边界操作颜色不明显;框选颜色也不明显,套索倒是明显
// todo(w) TH_BACK 资产/文件浏览器,大纲视图,悬浮高亮是加亮TH_BACK,但我已经是纯白了,以后改进
// todo(w) 电子表格: 加个选项 默认随预览器切换
// todo(w) 电子表格: 重排列时不要绘制列分割线,
// todo(w) 电子表格: 列分割线有时绘制了,该消失时不消失啊,因为工具提示? 改成拖动列分割线时才绘制?
// todo(w) 电子表格: 支持Ctrl 中键缩放表格
// todo(w) 电子表格: 域视图网格为空时不灰显啊
// todo(w) 电子表格: 进入编辑模式是否撤回灰显,网格和曲线不一致
// todo(w) 电子表格: float3, int3三列等宽,对于 1e10.00,0.00,0.00,效果不好
// todo(w) 电子表格: 预览器数据面板 加接口图标
// todo(w) 电子表格: 预览器数据面板,选中域 Item,3D试图切换预览的属性, 显示预览的列而不是只能第一项
// todo(w) 电子表格: Viewer 列显示所有连到预览器节点的值 column_display_name = column_id.name; 和 node_geo_viewer.cc
// todo(w) 菜单切换整数时默认值 0->n-1
// todo(w) 域/捕捉属性/预览器,获取不到属性时提示不存在该属性,将使用0
// todo(w) 存储属性二维矢量时绘制二维
// todo(w) 控制柄加到曲线节点
// todo(w) 如果N面板只剩文本,再按N应该是展开而不是关闭?要能保留活动状态
// todo(w) 群组接口列表,加一个自动展开全部?
// todo(w) 群组接口列表,支持多选,改进绘制
// todo(w) 未解算看不到输出值,但是控制接口灰显就不用解算,如何改进
// todo(w) 让合成器的gizmo在3D视图生效, 加到几何节点里?
// todo(w) 节点编辑器面包屑导航栏要像Directory Opus那样:顶层几何节点/合成修改器也要能切换
// todo(w) 把节点树标记为 Tool,一些bool属性全是False啊, 和新建Tool不一致
// todo(w) Ctrl G 接口默认属性继承所连的输入接口, 默认属性继承默认输入
// todo(w) 改进 N面板-群组接口 逻辑
//           几何数据输入不显示 隐藏值和在修改器隐藏
//           默认 改成 默认值?
// todo(w) 节点中的查找,有高亮效果更好
// todo(w) 对于接口连了别的线,却被菜单隐藏了,要特殊绘制?
// todo(w) 如果选中的节点只有一个,但不是活动节点,就重命名这一个
// todo(w) 如果面板折叠,绘制折叠节点时这些接口连线的话也绘制在一起
// todo(w) 折叠节点的话: 绘制接口文本,降低接口间距
//+ todo(w) 物体接口/物体数据块: 默认显示物体图标,选择后以及在选择列表里,换成对应物体
// todo(w) : 动画摄影部左列图标要和大纲一致
// todo(w) 改进: 三个编辑器三种合并颜色/分离颜色
// todo(w) 导入节点: 字符串,文件路径,选择后更改节点宽度
// todo(w) 菜单接口拖动搜索 编号切换 要初始化
// todo(w) 拆分为实例: 传一个位置接口,设置拆分后实例的位置
// todo(w) bug: 节点组Ctrl G后撤回,丢失视图位置
// todo(w) : J 可以从普通接口连向扩展接口,不能从扩展接口到普通接口
// todo(w) : J 长按会不停的新建连线吗?
// todo(w) : 融并节点时，有时连线不能保留(to和from可以存在连线)
// todo(w) : Gizmo Ctrl旋转刻度是白色的,不可配置?
// todo(w) : Gizmo 无法构造出内置的移动旋转工具
// todo(w) : Gizmo 摄像机 面光聚光上有圆形缩放和点Gizmo,图像的Gizmo真不错
// todo(w) : Gizmo 摄像机 面光聚光等聚光上还有悬浮提示
// todo(w) : Gizmo 合成器的Gizmo撤回/拖动时右键有问题
// todo(w) : Gizmo 合成器的遮罩Gizmo Shift可以等比放大
// todo 接口连线错误的错误按钮: 点击后应该添加节点
// todo 预览属性文本考虑遮挡:背景图像被物体遮挡或悬浮选中图像上Gizmo激活
// todo 添加接口属性,是否根据所属面板截短接口名:能解决多种语言的情况
// todo 为什么合并分离捆包,解算闭包,的接口是动态,不应该是单值吗
// todo 群组接口的搜索,显示为中文,但其实英文,英文才能搜索
// todo C++:几何节点耗时移到标题栏并叠加层里控制是否显示
// todo 启用输出无效时添加提示:只对菜单切换的输出生效
// todo 切换菜单导致连线断掉
// todo 列表/树视图,展开搜索箭头图标亮色主题兼容不好
// todo 列表/树视图,interface_template_list.cc  use_filter_invert 应该在搜索框为空时灰显
// todo 如何让界面缩放时,节点编辑器视图不偏移
// todo 节点附加到框前按了alt拖动,无法附加到框
// todo 拖动节点时滚轮缩放
// todo Voronoi在Python里做防循环线检测性能如何
// todo 节点编辑器,让滚轮缩放的更快
// todo NODE_OT_view_selected 为什么对只选一个节点的情况特殊处理,和3D视图也不一致.不合适吧
// todo TreeView 要和UIList 有点区分
// todo 内直节点暴露菜单接口
// todo 很多节点暴露菜单接口加的 is_default_link_socket() 不需要了
// todo 手册里的接口提示移动到接口上
```

```c++
// Regular
// wcol_regular
// wcol_theme
// ButType::ButToggle
// text_hover
// state->but_flag & UI_HOVER
// show_viewer_text
//😭 show_attribute_viewer_text()
//🌺 V3D_OVERLAY_VIEWER_ATTRIBUTE_TEXT
//👊🏿 
// show_backface_culling
//🌺 V3D_SHADING_BACKFACE_CULLING
//🌺 DRW_STATE_CULL_BACK
// 
// 3D视图 Python api: show_viewer_attribute
//🌺 V3D_OVERLAY_VIEWER_ATTRIBUTE
//😭 show_attribute_viewer()
//🌺 MBC_VIEWER_ATTRIBUTE_OVERLAY
//  VBOType::AttrViewer
//🌺 AttrViewer
// 
// 编辑模式法向绘制
// show_face_nor = (edit_flag & V3D_OVERLAY_EDIT_FACE_NORMALS);
//😭 show_wireframes
//🌺 V3D_OVERLAY_WIREFRAMES
//👊🏿 overlay_facing.hh
// show_face_orientation
//🌺 V3D_OVERLAY_FACE_ORIENTATION
// 3D视图编辑模式网格点大小
// vertex_size
// rv3d->pixsize = len_px / len_sc;
// ED_view3d_pixel_size()
// show_face_normals
// V3D_OVERLAY_EDIT_FACE_NORMALS
// show_extra_face_angle
//🌺 V3D_OVERLAY_EDIT_FACE_ANG
```
