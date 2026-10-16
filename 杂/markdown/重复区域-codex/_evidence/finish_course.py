"""Write course navigation and learning/verification material."""
from pathlib import Path
import json
import os
import subprocess
from build_docs import COURSE, OUT, ROOT, REV, COLORS, TERM_DEFS


def write(relative, content):
    path=OUT/relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip()+'\n', encoding='utf-8', newline='\n')


def main():
    stats=json.loads((OUT/'_evidence/document-stats.json').read_text(encoding='utf-8'))
    total=sum(s['lines'] for s in stats)
    nav=[]
    for ch,s in zip(COURSE,stats):
        nav.append(f'- **RZ-{ch["slug"][:2]} [{ch["slug"][3:]}]({ch["group"]}/{ch["slug"]}.md)** · {s["lines"]:,} 行。{ch["goal"]}')
    write('README.md', f'''
# Blender 重复区域源码学习

本套课程围绕 Repeat Zone，沿用“全面学习-codex”的组织方式：总入口、课程指南、主题分组、真实源码、机制推导、小数据反例、练习和校验证据。

正文共 **14 篇、{total:,} 行**，每篇 **{min(s['lines'] for s in stats):,}—{max(s['lines'] for s in stats):,} 行**。

行数包含说明文字、Mermaid 源码、练习和连续原始源码；没有把这些数量称为纯讲解文字行数。

源码摘录放在相关正文中，公共依赖会在不同专题中按问题重复引用，以便单篇可以独立阅读。

## 从这里开始

- [学习路线与阶段验收](00-课程指南/学习路线与阶段验收.md)：按使用、实现、调试三种目标进入。
- [阅读规范与图表约定](00-课程指南/阅读规范与图表约定.md)：分清源码事实、设计推导和运行证据。
- [源码版本与覆盖索引](00-课程指南/源码版本与覆盖索引.md)：本地源码基准、文件职责和摘录记录。
- [术语与符号速查](00-课程指南/术语与符号速查.md)：按编辑、构图、执行、观察和后端分层查找。
- [验收报告](00-课程指南/验收报告.md)：文档校验、参考模型与真实 Blender 测试的实际范围。
- [可运行示例](示例/README.md)：纯 Python 推演与 Blender 节点构建脚本。
- [证据与维护工具]( _evidence/README.md)：源码哈希、摘录清单和校验工具。

## 四个主题分组

- [01 · 语义与编辑表示](01-语义与编辑表示/README.md)：全景、数据结构、区域发现和编辑脚本。
- [02 · 构图与按需执行](02-构图与按需执行/README.md)：循环体提取、按轮数展开和需求传播。
- [03 · 值寿命与观察机制](03-值寿命与观察机制/README.md)：字段引用、内存拥有、日志、副作用和持久化。
- [04 · 实战后端与验收](04-实战后端与验收/README.md)：性能、算法案例、合成器/GPU与回归训练。

编号表示推荐阅读顺序；09 归在编辑表示组，10 归在值寿命组，因此按目录遍历不等于编号顺序。

## 十四篇正文

{chr(10).join(nav)}

## 四层理解模型

```mermaid
flowchart TB
  E["编辑表示：两端节点、Repeat Items、配对"]:::input
  Z["构图：区域树、体函数、包装器、轮次展开"]:::abstraction
  V["执行：值、需求、引用集合与storage"]:::compute
  O["观察：轮次上下文、日志、Viewer、副作用"]:::result
  E -->|"提取程序"| Z
  Z -->|"按需求值"| V
  V -->|"按调用身份记录"| O
{COLORS}
```

状态递推是 `S_(i+1)=F(S_i,i,B)`，最终结果是 `S_max(0,N)`。

`S` 是跨轮状态，`B` 是从区域外进入的输入，`i` 从零开始；`N=0` 不执行体，直接返回初始状态。

## 使用与证据边界

源码基准为 `{REV}`，具体字节内容由证据中的 SHA-256 记录。

本机已用独立安装的 Blender 5.2.0 LTS 验证附带仿射递推节点脚本；该可执行程序不是本仓库当前工作树的编译产物。

源码静态复核与二进制实测是互补证据，不声称二者版本相同，也不声称已运行合成器或 GPU 的完整回归。

本目录只编写课程和示例，没有修改 Blender C++ 实现。
'''.replace(']( _evidence', '](_evidence'))
    for group in dict.fromkeys(ch['group'] for ch in COURSE):
        entries=[ch for ch in COURSE if ch['group']==group]
        links='\n\n'.join(f'- [{ch["slug"]}]({ch["slug"]}.md)\n\n  {ch["goal"]}' for ch in entries)
        write(f'{group}/README.md',f'# {group[3:]}\n\n[返回总入口](../README.md)\n\n本组共 {len(entries)} 篇。章节仍按全局编号互相连接，可沿正文末尾的上一篇与下一篇连续学习。\n\n{links}\n\n每篇先读机制与案例，再按需展开源码。代码区间是完整文件或明确标注的连续区间，不省略中间分支。')

    write('00-课程指南/README.md','''
# 课程指南

[返回总入口](../README.md)

- [学习路线与阶段验收](学习路线与阶段验收.md)
- [阅读规范与图表约定](阅读规范与图表约定.md)
- [源码版本与覆盖索引](源码版本与覆盖索引.md)
- [术语与符号速查](术语与符号速查.md)
- [验收报告](验收报告.md)
''')
    glossary=['# 术语与符号速查','', '[返回课程指南](README.md)','',
              '本索引按课程首次出现的位置解释术语，符号的具体作用仍以对应正文和源文件为准。','']
    seen=set()
    for ch in COURSE:
        glossary.extend([f'## RZ-{ch["slug"][:2]} · {ch["slug"][3:]}','',
                         f'[打开正文](../{ch["group"]}/{ch["slug"]}.md)',''])
        for term in ch['terms'].split('|'):
            if term not in seen:
                glossary.extend([f'### `{term}`','',TERM_DEFS[term],''])
                seen.add(term)
    write('00-课程指南/术语与符号速查.md','\n'.join(glossary))
    write('00-课程指南/学习路线与阶段验收.md','''
# 学习路线与阶段验收

[返回课程指南](README.md) · [正文总入口](../README.md)

## 使用者路线

先读 RZ-01 建立状态模型，再读 RZ-12 做整数与几何案例，最后读 RZ-09 自动搭建节点。

这一条路线先解决“该怎样连线”，暂时不要求掌握执行器所有接口。

阶段验收不是能复述 Repeat 的定义，而是能完成以下任务。

1. 写出 `x_next=2*x+1`，初始 `x=1`，零到三轮的四个结果。
2. 说明为什么外部系数和跨轮状态应该走不同路径。
3. 建立累计几何时说清初始累计结果与追加时机。
4. 在 Python 中正式配对输入输出节点，并处理受控名称与稳定插槽标识。

## 实现者路线

按 01、02、03、04、05、06、07、08、10 阅读，再回到 11 和 14。

第一阶段读编辑表示：DNA、Accessor、动态声明、区域发现。

验收时画出节点存储、项目数组和项目名称字符串的拥有关系。

指出 `output_node_id`、`item.identifier`、`active_index`、LF 位置索引四者的区别。

第二阶段读程序提取：体函数、包装器、主值、跨界输入、需求和引用集合。

验收时在一张纸上画出两个状态项、一个外部输入、三轮调用的所有主值连线。

不要画入源码仍标为 TODO 的跨轮需求反向边。

第三阶段读求值与观察：storage 寿命、上下文、日志和副作用。

验收时说明同一个体节点在外层两个调用中为何需要不同父上下文。

指出默认值地址的拥有者，并说明其为何不会在构图循环结束时立即失效。

## 调试者路线

从 RZ-14 的症状分类进入，再按问题返回对应章节。

- 状态没有累计：先查 RZ-01 与 RZ-05，验证跨轮状态链。
- 两端插槽不同步：先查 RZ-02 与 RZ-09，验证配对、列表与声明刷新。
- 轮次观察错误：先查 RZ-08，验证父上下文、轮次与检查索引。
- 保存后项目异常：先查 RZ-10，区分项目序列化和完整区域复制。
- 大轮数变慢：先查 RZ-11，分别记录图规模与几何规模。
- 合成器取消或资源问题：直接查 RZ-13，不套用几何节点 storage 模型。

## 每篇推荐阅读方法

先写下“具体问题”的自己的答案，哪怕只是一句话。

读机制时把每个概念归到编辑、构图、执行、观察四层之一。

用实验里的最小输入手算；遇到数值差异先固定轮次索引与旧状态。

再打开源码，检查每个结论对应的实际字段、分支或调用。

做练习时不复制原文，改用一个不同初值或轮数验证理解。

最后明确本篇哪些结论是源码事实，哪些是数学推导，哪些已经有实测。

## 进阶任务

独立写一个顺序整数状态循环，并验证负轮数按零处理。

再将两状态更新写成元组递推，比较错误的顺序赋值实现。

加入独立 trace 输出，区分状态 `S_0` 和第一次调用 `i=0`。

构造每轮一个调用点的有向图，首先只实现主值通道。

再加入 usage 通道，说明哪些反向边可能形成循环依赖。

加入副作用执行根，测试没有普通输出需求时指定观察仍然可达。

最后讨论默认值拥有者、输入暂不可用时的恢复，以及嵌套调用身份。

这些是迁移训练，不声称一个几十行练习已经实现 Blender 的完整执行器。
''')
    write('00-课程指南/阅读规范与图表约定.md',f'''
# 阅读规范与图表约定

[返回课程指南](README.md)

## 事实、推导、实验的区别

“当前代码调用 add_function N 次”是源码事实。

“主状态连线约为 (N-1)K 条”是根据循环结构做的结构推导。

“在本机 Blender 中 N=3 得到 15”是运行观察，需要记录实际二进制版本与输入。

“这个改动将提速两倍”需要性能证据；本课程没有这样的无依据断言。

每篇的小数据案例除明确有运行记录者，均作为数学预期或待执行实验。

## 源码引用

正文使用完整文件或明确标注起止行的连续区间。

没有在原始代码块中插入会被误认为上游内容的中文解释。

教学说明放在代码块外，读者可以直接与原始文件逐行核对。

连续区间可能从函数内部开始，它不等于所涉函数已完整展示。

区间前后的源码应通过来源链接查看；证据中的文件哈希帮助发现后续漂移。

源码头中的 SPDX 许可保持上游原样，教材说明不更改源码授权。

## 命名约定

`N` 表示请求迭代次数，几何节点实际使用 `max(0,N)`。

`i` 表示当前体调用轮次，从零开始。

`S_i` 表示完成 i 次体调用后的状态，因此第一次调用读取 `S_0`，产生 `S_1`。

`B` 表示本次区域调用从外部取得的输入，不自动成为可更新状态。

`K` 表示 Repeat Items 数量；`B` 在复杂度讨论中也可能明确表示边界输入数量，具体以段落定义为准。

`body` 指一次体调用；`wrapper` 指实现整个区域语义的外层函数。

编辑节点的输出可以对应体函数输入；方向总是相对于当前边界而言。

## 图表配色

- 蓝色 input：问题、外部输入、编辑入口。
- 青色 data：真实源码、数据结构、值载体。
- 紫色 abstraction：接口、层级、拥有关系。
- 黄色 compute：执行、推导和实验步骤。
- 绿色 result：结果、能力和验收。
- 红色 error：失败条件与错误路径。

箭头旁文字说明关系。拥有、借用、调用和数据依赖不是同一种关系。

教程推导图不是调度事件记录；线程执行先后必须另用实际运行证据确认。

## 学习背景

C++ 部分需要理解引用、指针、RAII、模板、std::optional、Span 和动态数组。

字段与匿名引用部分需要区分表达式、几何上下文、属性域和底层承载数据。

若不熟悉这些概念，可回到参考课程的基础容器、内存类型、Field 和 LazyFunction 主线。

本课程聚焦 Repeat，公共依赖源码作为必要背景，不宣称对每个依赖库都做完整 API 教程。

## 版本约定

源码提交：`{REV}`。

正文中的“当前实现”指本次记录哈希的工作树文件。

Blender 5.2.0 LTS 实测用于验证示例，不代表该二进制与上述工作树同一构建。

发现公开 Python API 与 C++ DNA 字段不一致时，以实际公开接口与运行记录为准。
''')
    records=json.loads((OUT/'_evidence/source-excerpts.json').read_text(encoding='utf-8'))['excerpts']
    paths=sorted({r['path'] for r in records})
    lines=['# 源码版本与覆盖索引','', '[返回课程指南](README.md)','',f'基准提交：`{REV}`。','',
           '实际字节哈希与连续区间见[机器可读源码证据](../_evidence/source-excerpts.json)。','',
           '本索引是本课程所引用文件的覆盖索引，不宣称穷尽所有间接依赖或全部Repeat相关历史。','',
           '## 按源文件查正文','']
    for p in paths:
        rs=[r for r in records if r['path']==p]
        rel=Path(os.path.relpath(ROOT/p,OUT/'00-课程指南')).as_posix()
        lines.extend([f'### `{Path(p).name}`','',f'[打开源码]({rel})','',f'路径：`{p}`','',f'SHA-256：`{rs[0]["sha256"]}`',''])
        for r in rs:
            lines.extend([f'- [{Path(r["document"]).stem}](../{r["document"]}) · L{r["start"]}—L{r["end"]}。'])
        lines.append('')
    lines.extend(['## 可追踪的主调用链','',
                  '1. 节点声明与存储：`node_geo_repeat.cc`、`NOD_geo_repeat.hh`、DNA。',
                  '2. 区域发现：`node_tree_zones.cc` 与 `bNodeTreeZones`。',
                  '3. 构建体：`build_zone_body_function`。',
                  '4. 构建包装器：`build_repeat_zone_function` → `build_repeat_zone_lazy_function`。',
                  '5. 首次求值：`execute_impl` → `initialize_execution_graph`。',
                  '6. 执行展开图：`RemappedParams` → `GraphExecutor::execute`。',
                  '7. 体调用身份：`RepeatBodyNodeExecuteWrapper` → `RepeatZoneComputeContext`。',
                  '8. 副作用：`RepeatZoneSideEffectProvider` 返回需要执行的合法体调用。','',
                  '合成器从 `RepeatZoneOperation::execute` 进入逐轮操作；GPU 区段生成从节点 `gpu_fn` 进入相应宏。','',
                  '## 不在本次证据内的范围','',
                  '没有查询历史提交作者与演化日期，因此不提供编造的首次引入或重构版本。',
                  '没有运行完整 Blender C++ 测试套件，也没有验证所有图像精度、后端与硬件组合。',
                  '没有将所有间接依赖展开成独立文件，以免让Repeat课程变成无关模块源码镜像。'])
    write('00-课程指南/源码版本与覆盖索引.md','\n'.join(lines))
    write('示例/README.md',r'''
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
''')
    write('_evidence/README.md',r'''
# 证据与维护工具

[返回课程入口](../README.md)

- [source-excerpts.json](source-excerpts.json)：源文件、SHA-256、区间和对应正文。
- [document-stats.json](document-stats.json)：14篇正文的行数和字符数。
- [validation.json](validation.json)：源码摘录、链接、围栏和篇幅检查。
- [reference-models.json](reference-models.json)：独立参考模型的断言结果。
- [blender-demo.json](blender-demo.json)：独立安装Blender的版本、命令和真实输出。
- [build_docs.py](build_docs.py)：课程正文的作者说明、案例与源码区间配置。
- [finish_course.py](finish_course.py)：导航和课程指南的生成工具。
- [validate_docs.py](validate_docs.py)：只读文档校验并写出本目录验证记录。
- [run_examples.py](run_examples.py)：运行两类示例并保存输出。

从仓库根目录重建：

```powershell
python .markdown\重复区域-codex\_evidence\build_docs.py
python .markdown\重复区域-codex\_evidence\finish_course.py
python .markdown\重复区域-codex\_evidence\run_examples.py
python .markdown\重复区域-codex\_evidence\validate_docs.py
```

重建会覆写本课程生成的正文与导航。修改正文时应同步更新作者配置，避免下一次重建丢失修改。

源码漂移应先检查差异，再更新摘录区间与机制解释；不能只刷新哈希后声称语义仍然正确。

`.markdown` 在当前机器是目录联接，工具从实际父目录寻找Blender源码根，源码相对链接也按真实目录计算。

Mermaid已检查围栏与基本结构，没有安装渲染器时不声称所有图都做过像素级渲染验证。
''')


if __name__=='__main__':
    main()
