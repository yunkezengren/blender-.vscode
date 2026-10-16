# 可运行示例

[返回课程总入口](../README.md)

## 独立语义参考模型

[reference_models.py](reference_models.py) 只使用 Python 标准库。

从 Blender 仓库根目录运行：

```powershell
python .markdown\重复区域-codex\示例\reference_models.py
```

它验证负轮数和零轮、状态链、仿射更新、双状态同时更新、轮次累计、牛顿迭代、累计位置、嵌套调用、边界需求 OR、副作用轮次过滤和简化参数映射。

它还构造断开跨轮链与错误顺序更新两个反例，证明这些案例能够区分错误实现。

该模型没有调用 bpy，也不覆盖 C++ 调度、字段寿命、几何写时复制、Result 引用计数或 GPU。

## 真实 Blender 节点示例

[build_repeat_demo.py](build_repeat_demo.py) 创建一个单点几何、两个正式配对的 Repeat 节点，以及 `x_next=2*x+1` 的体。

几何作为独立状态直通，x 作为浮点状态从1开始，最终值写入点域命名属性 `rz_state_x`。

脚本通过求值后的网格读取属性，验证0、1、2、3轮结果分别是1、3、7、15。

```powershell
blender --background --factory-startup --python .markdown\重复区域-codex\示例\build_repeat_demo.py
```

脚本使用专属名称 `RZ_Codex_Affine_Demo`，不保存blend文件。

推荐用后台出厂设置或新的临时文件运行，避免把教程示例与实际项目混在一起。

本机 Blender 5.2.0 LTS 已通过该脚本，具体输出保存在[二进制验证记录](../_evidence/blender-demo.json)。

这一程序不是本仓库当前提交的编译产物，不能将验证结果扩展为当前源码完整回归通过。

## 实测发现的 API 边界

C++ 的 NodeRepeatItem 包含内部 identifier，但当前实测 Python RepeatItem 没有同名公开属性。

因此脚本在创建唯一项目名 StateX 后，用该受控名称定位动态插槽。

若需要后续稳定查询，可以读取 `socket.identifier` 并保存；不要假定所有 DNA 字段都能直接从 bpy 对象访问。

默认几何插槽按类型查找，避免把本地化显示名当作唯一协议。

## 扩展实验

将主体改为使用 Iteration，验证 sum0=0、N=3 时结果为3。

建立a、b双状态并用旧值同时计算下一轮，验证五轮斐波那契结果为(5,8)。

将项目重命名后重查插槽，比较保存稳定identifier与使用旧显示名的差异。

保存并重开项目，核查项目顺序、插槽标识和最终属性值。

添加 Viewer 并切换 inspection_index，记录观察轮次与最终区域输出的区别。

这些扩展实验是后续操作建议，没有因基础仿射示例通过而被标记为已运行。
