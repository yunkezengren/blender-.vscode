#!/usr/bin/env python3
"""按样板格式，为主系列与前置知识文档重建导航条 + 定位块 + 分隔线。

只做"补回"，不改动正文任何内容。

用法：
  python reapply_nav.py --dry
  python reapply_nav.py
"""

import re
import sys
from pathlib import Path

NAV_DIV_OPEN = ('<div style="font-family:\'Segoe UI\',\'Microsoft YaHei\',system-ui,'
                '-apple-system,sans-serif;display:flex;flex-wrap:wrap;align-items:center;'
                'gap:8px;margin:16px 0 20px;padding:10px 14px;background:#F8FAFC;'
                'border:1px solid #E2E8F0;border-radius:12px">')
SPAN_LABEL = ('<span style="font-size:11px;font-weight:700;letter-spacing:.1em;'
              'color:#64748B;margin-right:2px">导航</span>')
S_GRAY = ('font-size:13px;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0;'
          'border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap')
S_BLUE = ('font-size:13px;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE;'
          'border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap')
S_PURPLE = ('font-size:13px;color:#7C3AED;background:#F5F3FF;border:1px solid #DDD6FE;'
            'border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap')
HR = ('<hr style="border:none;height:1px;'
      'background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">')

NUM = re.compile(r'^(\d+)')

# 每篇的定位块文案（按文件名前缀+目录匹配）
INTRO = {
    # 00-课程指南
    '01-学习路线与阶段验收':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列的学习路线与阶段验收篇。'
         '它给出六个阶段的阅读顺序、每阶段的交付物与验收问题，用于自测是否真的读懂了前文。'),
    '03-符号与源码索引':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列的符号与源码索引篇。'
         '它把全系列出现的关键类、函数、DNA 结构按文件分组列出，并给出覆盖矩阵与逐符号追踪指南。'),
    # 01-Zone系统基础
    '01-NodeTreeZone区域表示与配对':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 01 章第 1 篇。'
         '它回答一个基础问题：Repeat Input 与 Repeat Output 两个独立的节点，'
         'Blender 怎么知道它们属于同一个区域？'),
    '02-Zone输入输出与bundle迁移语义':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 01 章第 2 篇。'
         '它回答：Repeat 区域的输入输出 socket 是怎么动态生成的，为什么改名不会断链接。'),
    # 02-Repeat区域数据模型
    '01-Repeat节点注册与UI':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 02 章第 1 篇。'
         '它逐函数精读 node_geo_repeat.cc：节点如何注册、动态 socket 如何声明、'
         'link 搜索如何一键建对、GPU 回调如何配对。'),
    '02-DNA存储与NodeRepeatItem':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 02 章第 2 篇。'
         '它回答：Repeat 的条目数据存在哪里、如何被 .blend 持久化、'
         '为什么 identifier 必须在改名与排序后保持不变。'),
    '03-SocketItems通用条目框架':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 02 章第 3 篇。'
         '它剖析 NOD_socket_items.hh 的访问器协议：一套模板如何同时支撑 '
         'Repeat、Simulation、Foreach 等节点的动态条目。'),
    # 03-几何节点执行架构
    '01-ZoneBodyFunction与ZoneBuildInfo':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 03 章第 1 篇。'
         '它讲 ZoneBuildInfo 与 ZoneBodyFunction 这两个结构，以及 zone 如何一步步被翻译成 '
         'LazyFunction 图再插回父图。'),
    '02-Repeat循环体函数构建详解':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 03 章第 2 篇。'
         '它逐段解剖 build_zone_body_function：main、border link、reference set 三组索引'
         '如何登记，usage 如何回填，环如何打断。'),
    '03-执行图按迭代展开':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 03 章第 3 篇，也是全系列核心篇。'
         '它逐段解剖 initialize_execution_graph：body 节点如何复制、成对如何串联、'
         '零轮如何直通、索引映射如何对齐。'),
    # 04-运行时机制
    '01-RepeatEvalStorage与一次求值':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 04 章第 1 篇。'
         '它回答：一次求值的全部可变状态存在哪里、何时创建、何时销毁、嵌套时如何不共享。'),
    '02-ComputeContext与迭代身份':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 04 章第 2 篇。'
         '它回答：同一个循环体节点执行 N 次，日志、Viewer、副作用如何区分是哪一轮。'),
    '03-副作用迭代与按需执行':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 04 章第 3 篇。'
         '它回答：Viewer 挂第 5 轮时哪些轮必须执行、后续轮为何可跳过、'
         '两张副作用表各管什么。'),
    # 05-跨后端实现
    '01-合成器RepeatZoneOperation':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 05 章第 1 篇。'
         '它回答：几何节点把循环体复制 N 份拼图，合成器为什么不这么干。'),
    '02-GPU着色器与GPU_stack_link_zone':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 05 章第 2 篇。'
         '它回答：同一个 Repeat 区域，GPU 后端如何编译成着色器循环。'),
    # 06-实战与性能
    '01-使用模式与迭代设计':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 06 章第 1 篇。'
         '它从源码转向应用：累积、批次、分形、物理积分等模式，以及迭代设计纪律。'),
    '02-性能模型与开销分析':
        ('系列定位：本篇是《重复区域（Repeat Zone）全面学习》系列 06 章第 2 篇。'
         '它回答：Repeat 为什么不能像 for 循环那样便宜，成本由哪几项构成，如何诊断与优化。'),
    # 前置知识
    '01-惰性求值模型与状态机':
        ('系列定位：本篇是《重复区域前置知识》系列 01 章第 1 篇。'
         '它回答一个最基础的问题：什么叫"惰性求值"，为什么它天然长得像一台状态机。'),
    '02-LazyFunction接口契约':
        ('系列定位：本篇是《重复区域前置知识》系列 01 章第 2 篇。'
         '它回答：写一个自定义惰性函数，最少要实现哪几个方法，各自的契约是什么。'),
    '03-Params调用约定':
        ('系列定位：本篇是《重复区域前置知识》系列 01 章第 3 篇。'
         '它回答：惰性函数在 execute 里怎么要一个输入、怎么给一个输出、'
         '请求与提交的协议是什么。'),
    '04-ValueUsage三值与需求传播':
        ('系列定位：本篇是《重复区域前置知识》系列 01 章第 4 篇。'
         '它回答：一个节点的输出没人用，它是怎么知道不用算的——'
         '静态推断与动态传播两层机制。'),
    '05-lf-Graph图结构':
        ('系列定位：本篇是《重复区域前置知识》系列 01 章第 5 篇。'
         '它讲 lf::Graph：节点、socket、连接规则、索引维护与图导出。'),
    '06-GraphExecutor调度机制':
        ('系列定位：本篇是《重复区域前置知识》系列 01 章第 6 篇。'
         '它讲 GraphExecutor：一张几百节点的图，执行器凭什么知道先跑谁、'
         '谁可跳过、谁能并行。'),
    '07-执行钩子与副作用接口':
        ('系列定位：本篇是《重复区域前置知识》系列 01 章第 7 篇。'
         '它讲三个钩子：为什么执行器不能直接调 fn.execute，'
         '而要留 wrapper、side effect provider、logger 三个入口。'),
    '02-Span只读视图':
        ('系列定位：本篇是《重复区域前置知识》系列 03 章第 2 篇。'
         '它讲 Span&lt;T&gt;：一个函数需要遍历"别人拥有的数组"时，参数应该怎么写。'),
}


def build_nav(path: Path, series_label: str) -> str:
    chapter = path.parent
    has_chapter_readme = (chapter / 'README.md').exists()
    siblings = sorted(p for p in chapter.glob('*.md') if p.name != 'README.md')

    links = []
    links.append(('..' if has_chapter_readme else '.', 'README.md',
                  '总入口', S_GRAY))
    if has_chapter_readme:
        links.append(('.', 'README.md', f'本章 {chapter.name}', S_BLUE))

    try:
        idx = siblings.index(path)
    except ValueError:
        idx = -1
    if idx > 0:
        links.append(('.', siblings[idx - 1].name,
                      '‹ ' + siblings[idx - 1].stem, S_BLUE))
    if 0 <= idx < len(siblings) - 1:
        links.append(('.', siblings[idx + 1].name,
                      siblings[idx + 1].stem + ' ›', S_PURPLE))

    a_tags = []
    for prefix, target, text, style in links:
        href = f'{prefix}/{target}' if prefix == '..' else f'./{target}'
        if prefix == '.' and target == 'README.md':
            href = './README.md'
        a_tags.append(f'<a href="{href}" style="{style}">{text}</a>')

    nav = '\n'.join([NAV_DIV_OPEN, SPAN_LABEL] + a_tags + ['</div>'])
    return nav


def build_intro(path: Path) -> str:
    intro = INTRO.get(path.stem)
    if not intro:
        return ''
    return ('<div style="font-family:\'Segoe UI\',\'Microsoft YaHei\',system-ui,'
            '-apple-system,sans-serif;margin:18px 0 22px;padding:14px 18px;'
            'background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:10px">\n\n'
            + intro + '\n\n</div>')


def apply(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if 'font-family' in text:
        return False
    lines = text.split('\n')
    hidx = next((i for i, ln in enumerate(lines) if re.match(r'^#\s', ln)), None)
    if hidx is None:
        return False

    head = lines[:hidx + 1]
    tail = lines[hidx + 1:]

    # 去掉紧随标题的空行与已有的纯 Markdown 导航行
    while tail:
        s = tail[0].strip()
        if s == '':
            tail.pop(0)
        elif s.startswith('[') and '](' in s:
            tail.pop(0)
        elif s.startswith('>') and '·' in s:
            tail.pop(0)
        else:
            break

    series_label = '前置知识' if '前置知识' in str(path) else ''
    nav = build_nav(path, series_label)
    intro = build_intro(path)

    body = '\n'.join(head) + '\n\n' + nav + '\n\n'
    if intro:
        body += intro + '\n\n'
    body += HR + '\n\n' + '\n'.join(tail)
    path.write_text(body, encoding='utf-8')
    return True


def main():
    dry = '--dry' in sys.argv
    roots = [
        Path(r'.markdown/重复区域-dsh'),
        Path(r'.markdown/重复区域-前置知识-dsh'),
    ]
    done = 0
    for root in roots:
        for p in sorted(root.rglob('*.md')):
            if '_tools' in str(p) or p.name == 'README.md' or p.name == '91-验收报告.md':
                continue
            if dry:
                t = p.read_text(encoding='utf-8')
                mark = 'HAS' if 'font-family' in t else 'NEED'
                name = p.name.encode('ascii', 'backslashreplace').decode()
                print(f'[{mark}] {name}')
            else:
                if apply(p):
                    done += 1
                    name = p.name.encode('ascii', 'backslashreplace').decode()
                    print(f'恢复 {name}')
    if not dry:
        print(f'\n共处理 {done} 个文件')


if __name__ == '__main__':
    main()
