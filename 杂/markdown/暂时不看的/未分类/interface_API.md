# Blender Interface API Notes

这份文档是对旧版 `doc/guides/interface_API.txt` 的中文 Markdown 整理版。

原文署名时间是 `2003 年 7 月`，作者为 Ton Roosendaal。它描述的是 Blender 早期 `interface.c` 风格 UI 工具包的设计思路、常见 API 和按钮类型。今天的代码已经发生了很多演进，所以这份文档更适合作为：

- 历史背景资料
- UI 框架设计思路参考
- 读老代码、老注释时的术语对照

不建议把它当作当前 Blender UI API 的唯一权威说明。

## 目录

1. 总体说明
2. Windows 与 Blocks
3. `ui::Block` API
4. `uiButton` API

## 1. 总体说明

### 1.1 这套 API 的定位

原文强调，这套接口是围绕 Blender 自身需求设计的，不是一个独立 SDK，也不是为了给其他应用直接复用。

它的一些基本特征：

- 设计时强烈依赖 Blender 的数据模型
- 大量按钮可以直接作用于 Blender 数据
- 底层完全基于 OpenGL 绘制
- 同时要兼顾下拉菜单、弹出菜单、普通按钮布局等多种 UI 形态

作者也明确提到，这套系统是在较大时间压力下发展出来的，因此内部会保留一些历史包袱和“为了兼容而存在”的实现痕迹。

### 1.2 为什么代码会显得难懂

原文里解释得很直接：

- 它试图统一多种 GUI 交互范式
- 这会带来很高的灵活性
- 但也让内部实现变复杂

所以你今天看到的很多 UI 代码如果显得“功能能理解，但结构不够直观”，这并不奇怪。

### 1.3 历史背景

文档里还提到几个历史点：

- 这套代码最初是为了替换旧的 1.8 按钮系统
- 有一段时间尝试过更高层的 API 封装
- 一些“浮动 blocks” 一类的扩展想法当时并未完全完成

这些内容说明：Blender UI 框架一直在演进，不是一次性定型的。

## 2. 相关源码位置

原文里列出的路径有明显的历史痕迹，和今天的目录结构不完全一致，但它想表达的是：

- `interface.c` 是核心实现
- `interface.h` / `BIF_interface.h` 之类头文件承担内外部接口划分
- `resources.c` 管理配色和图标
- `toolbox.c` 等文件在这个 API 之上再构建更高层 GUI 元素

今天如果你在当前仓库里联读，建议优先看现代路径下的这些目录：

- `source/blender/editors/interface/`
- `source/blender/editors/include/`
- `source/blender/windowmanager/`
- `source/blender/editors/screen/`

## 3. Windows 与 Blocks

### 3.1 核心概念

文档把 `ui::Block` 看成 Blender GUI 的基础组织单位：

- 一个 Area Window 里会维护一组 `ui::Block`
- 每个 `ui::Block` 内部再包含一组按钮或菜单项

原文示例的大意是：

```c
ui::Block *block = uiNewBlock(&curarea->uiblocks, "stuff", UI_EMBOSSX, UI_HELV, curarea->win);
```

也就是说：

- block 会被挂到当前窗口的 block 列表上
- block 有自己的名字、绘制风格、字体和目标窗口

### 3.2 `uiDoBlocks` 的角色

原文里提到：

```c
uiDoBlocks(&curarea->uiblocks, event);
```

它的含义可以理解成：

- 遍历当前窗口上的所有 blocks
- 让它们处理当前事件
- 必要时进入菜单等子循环

所以 block 不只是“画出来的容器”，它也是事件处理的组织单位。

### 3.3 内存分配模型

这部分非常值得记住，因为它解释了 Blender UI 代码为什么常常“在 draw 里创建界面”。

原文强调：

> 对这套工具包来说，“创建 block”和“绘制 block”几乎没有本质区别。

也就是说：

- 每次窗口 redraw 时，blocks 都会重新创建
- Blender 的按钮界面通常就在主绘制函数里搭建

对应的内存策略：

- 如果当前窗口里已经有同名 block，旧 block 会被释放
- 关闭窗口或退出 Blender 时，blocks 会被释放
- 复制或拆分窗口时，blocks 会被复制

这和很多“初始化一次，之后长期复用控件树”的 GUI 框架很不一样。

### 3.4 内部执行流程

原文把 `uiDoBlocks` 的内部过程描述成一个嵌套循环：

1. 先处理普通按钮 blocks
2. 如果出现菜单 block，则进入二级处理循环
3. 菜单循环里还可能递归地产生子菜单
4. 退出菜单时恢复 save-under，并清理菜单 blocks
5. 如果没有其他动作，再处理 tooltip

这一点说明 Blender 老 UI 系统把菜单也视为一种特殊的 block。

## 4. `ui::Block` API

### 4.1 创建 block

原文给出的核心接口是：

```c
ui::Block *uiNewBlock(ListBase *lb, char *name, short dt, short font, short win)
```

参数语义：

- `lb`: 要挂入的 block 列表
- `name`: block 唯一标识；若同名已存在，会释放旧 block
- `dt`: draw type
- `font`: 字体 ID
- `win`: Blender area-window ID

### 4.2 draw type

原文列出了一组历史绘制风格：

- `UI_EMBOSSX`: Blender 默认圆角凸起按钮
- `UI_EMBOSSW`: 更简单的凸起按钮
- `UI_EMBOSSN`: 无边框按钮
- `UI_EMBOSSF`: 方形凸起按钮
- `UI_EMBOSSM`: 用于下拉菜单的彩色样式
- `UI_EMBOSSP`: 简单无边框彩色按钮

这些名字今天未必一一保持不变，但“block 拥有一组绘制风格属性”这个概念仍然重要。

### 4.3 block 属性会影响后续按钮

文档里特别提醒：

- 一个 block 创建后
- 之后定义的每个 `uiButton`
- 都会继承这个 block 当前的属性

所以如果你在定义按钮的过程中修改 block 设置，那么修改之后声明的按钮行为可能会不同。

### 4.4 常见控制函数

原文列出的 `ui::Block` 控制接口可以整理成下面这些用途：

#### 绘制

- `uiDrawBlock(block)`: 绘制 block

#### 颜色

- `ui::BlockSetCol(ui::Block *block, int col)`

历史配色常量包括：

- `BUTGREY`
- `BUTGREEN`
- `BUTBLUE`
- `BUTSALMON`
- `MIDGREY`
- `BUTPURPLE`

#### 外观

- `ui::BlockSetEmboss(ui::Block *block, int emboss)`: 修改绘制风格

#### 菜单方向

- `ui::BlockSetDirection(ui::Block *block, int direction)`

方向值包括：

- `UI_TOP`
- `UI_DOWN`
- `UI_LEFT`
- `UI_RIGHT`

#### 菜单偏移

- `ui::BlockSetXOfs(ui::Block *block, int xofs)`

#### 菜单确认回调

- `ui::BlockSetButmFunc(ui::Block *block, void (*menufunc)(void *arg, int event), void *arg)`

当 menu block 被标记为 OK 时，会触发这个函数。

#### 自动布局

- `uiAutoBlock(ui::Block *block, float minx, float miny, float sizex, float sizey, BLOCK_ROWS)`

它的作用是：

- 让 block 内的按钮自动对齐
- 在边界范围内自动排布
- 支持多行多列布局

原文特别提醒：

- 此时 `uiDefBut` 的坐标参数不再单纯表示屏幕位置
- 第一个坐标值会被用作“行号”
- 宽高也可以表示相对尺寸

## 5. `ui::Block` 的内部 flag

原文把这一部分视为“内部知识”，因为当时主要由 `interface.c` 与 `toolbox.c` 自己使用。

主要标志包括：

- `BLOCK_LOOP`: 子循环 block，通常是菜单，画在 frontbuffer
- `BLOCK_REDRAW`: block 需要重绘
- `BLOCK_RET_1`: 发生特定事件值时关闭 block
- `BLOCK_BUSY`: 内部占用状态
- `BLOCK_NUMSELECT`: 可用数字键快速选择项目
- `BLOCK_ENTER_OK`: 回车可关闭 block 并确认

这能帮助你理解：

- 为什么菜单是一种特殊 block
- 为什么 block 处理经常伴随状态机语义

## 6. `uiButton` API

### 6.1 一个按钮可以做什么

原文总结 Blender 按钮有四种基本用途：

1. 直接显示并写回数据
2. 把事件码重新塞回事件队列
3. 调用用户自定义函数
4. 创建并调用另一个 block，比如菜单

### 6.2 通用定义接口

原文里的抽象形式是：

```c
ui_def_but(block, type, retval, str, x1, y1, x2, y2, poin, min, max, a1, a2, tip);
```

它非常通用，所以也非常“底层”。

文档里提到，正因为这里做了很多泛化复用，代码会显得比较晦涩，因此后来才逐步出现了更具体、更高层的按钮定义形式。

### 6.3 `UiDefBut[CSIF]`

原文列出了几种按数据类型区分的版本：

- `UiDefButC`: 作用于 `char`
- `UiDefButS`: 作用于 `short`
- `UiDefButI`: 作用于 `int`
- `UiDefButF`: 作用于 `float`

参数语义整理如下：

- `block`: 当前 `ui::Block`
- `type`: 按钮类型
- `retval`: 回传到事件队列的值
- `str`: 按钮名称
- `x1, y1`: 左下角坐标
- `x2, y2`: 宽高
- `poin`: 目标数据指针
- `min, max`: slider 等控件使用
- `a1, a2`: 某些按钮类型的额外信息
- `tip`: tooltip 文字

## 7. 按钮类型说明

### 7.1 `BUT`

激活型按钮，例如“Render”。

- 不一定需要绑定数据指针
- 更像动作触发按钮

### 7.2 `TOG` / `TOGN`

切换按钮，例如“Lock”。

- 指针值通常在 `0` 和 `1` 之间切换
- `TOGN` 是反逻辑形式

原文还提到可以叠加：

- `|BIT|<nr>`

表示只操作某一个 bit。

### 7.3 `ROW`

一组互斥选项中的某一项。

- `min` 里放 row ID
- `max` 里放按下后赋给 `*poin` 的值

### 7.4 `NUMSLI` / `HSVSLI`

滑条式数值控件或颜色相关滑条。

### 7.5 `NUM`

普通数字输入控件。

### 7.6 `TEX`

文本输入控件。

### 7.7 `LABEL`

纯标签，不承担修改数据的职责。

### 7.8 `SEPR`

分隔用元素。

### 7.9 `MENU`

菜单按钮。

### 7.10 `COLOR`

颜色按钮。

## 8. 图标按钮、菜单按钮和特殊按钮

### 8.1 图标按钮

原文单独列出 icon button，说明图标在这套系统中是独立重要的表现层能力，而不是普通按钮的附带功能。

### 8.2 下拉菜单 / block 按钮

原文中 `BLOCK` 一类按钮的核心思想是：

- 按下一个按钮
- 创建另一个 `ui::Block`
- 作为菜单或弹出内容继续处理

这也解释了为什么前面要强调：

- block 不仅是绘制容器
- 也是交互和子循环的载体

### 8.3 `KEYEVT`

与按键事件绑定的特殊按钮。

### 8.4 `LINK` / `INLINK`

原文把它们归入 special，用于带连线语义的 UI 元素。

如果你在旧代码里看到类似节点连接、关系链接一类的特殊交互，这一类按钮语义会有帮助。

## 9. 怎么使用这份文档

如果你今天在读 Blender 当前 UI 代码，建议这样用：

1. 把它当作历史背景资料
2. 当你看到老注释里的 `uiBlock`、`uiDoBlocks`、`UiDefBut`、`BLOCK_LOOP` 等术语时，用它做语义对照
3. 不要机械照抄这里的旧接口去理解现代 UI API

更具体地说：

- 读现代 `source/blender/editors/interface/` 代码时，这份文档帮你建立历史心智模型
- 真正确定当前 API 行为时，仍然要回到当前头文件和实现文件

## 10. 一句话总结

这份旧文档最有价值的地方，不在于告诉你“今天具体该怎么调用 UI API”，而在于让你理解 Blender 这套 UI 系统为什么会长成现在这样：

- block 是组织单位
- redraw 时重建 UI 是常见做法
- 按钮、菜单、事件处理在同一套机制中被统一起来
- 为了灵活性，底层 API 会显得很泛化、很底层
