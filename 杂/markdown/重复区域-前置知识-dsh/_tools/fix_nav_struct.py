#!/usr/bin/env python3
"""修复导航条结构：把基准说明块包进紫色定位块，并删除重复的 Markdown 导航行。

输入文件应已含 HTML 导航条（<div font-family ...> 导航 </div>）。
本脚本做三件事：
1. 删除紧跟在导航 </div> 之后的纯 Markdown 导航行（以 [ 开头且含 ]( 的行）
2. 把其后的 > 引用行（基准说明）或首段说明，包进紫色定位块
3. 统一为：标题 → 导航条 → 紫色定位块 → 分隔线 → 正文

只补不删：如果文件已有紫色定位块（border-left:4px），跳过。
"""

import re
import sys
from pathlib import Path

PURPLE_OPEN = ('<div style="font-family:\'Segoe UI\',\'Microsoft YaHei\',system-ui,'
               '-apple-system,sans-serif;margin:18px 0 22px;padding:14px 18px;'
               'background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:10px">')
HR = ('<hr style="border:none;height:1px;'
      'background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">')

NAV_END = re.compile(r'^</div>\s*$')
MD_NAV = re.compile(r'^\s*\[.+\]\(.+\)')
QUOTE = re.compile(r'^\s*>\s?(.*)$')


def fix(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if 'border-left:4px' in text:
        return False
    if 'font-family' not in text:
        return False

    lines = text.split('\n')

    # 定位导航条的 </div>
    nav_end = None
    for i, ln in enumerate(lines):
        if NAV_END.match(ln) and any('font-family' in x for x in lines[max(0, i - 8):i]):
            nav_end = i
            break
    if nav_end is None:
        return False

    head = lines[:nav_end + 1]
    rest = lines[nav_end + 1:]

    # 去掉紧跟的空行
    while rest and rest[0].strip() == '':
        rest.pop(0)

    # 去掉重复的 Markdown 导航行
    while rest and MD_NAV.match(rest[0]):
        rest.pop(0)
        while rest and rest[0].strip() == '':
            rest.pop(0)

    # 收集引用型基准说明（> 开头）
    quote_lines = []
    while rest and QUOTE.match(rest[0]):
        quote_lines.append(QUOTE.match(rest[0]).group(1).strip())
        rest.pop(0)
    while rest and rest[0].strip() == '':
        rest.pop(0)

    # 去掉已有的旧 <hr>
    while rest and rest[0].strip().startswith('<hr'):
        rest.pop(0)
        while rest and rest[0].strip() == '':
            rest.pop(0)

    # 组装
    out = list(head)
    out.append('')
    if quote_lines:
        out.append(PURPLE_OPEN)
        out.append('')
        out.append(' '.join(q for q in quote_lines if q))
        out.append('')
        out.append('</div>')
        out.append('')
    out.append(HR)
    out.append('')
    out.extend(rest)

    path.write_text('\n'.join(out), encoding='utf-8')
    return True


def main():
    dry = '--dry' in sys.argv
    paths = [Path(p) for p in sys.argv[1:] if not p.startswith('--')]
    done = 0
    for p in paths:
        if not p.is_file() or p.suffix != '.md':
            continue
        name = p.name.encode('ascii', 'backslashreplace').decode()
        if dry:
            t = p.read_text(encoding='utf-8')
            mark = 'HAS_PURPLE' if 'border-left:4px' in t else (
                'NO_NAV' if 'font-family' not in t else 'NEED_FIX')
            print(f'[{mark}] {name}')
        else:
            if fix(p):
                done += 1
                print(f'修复 {name}')
    if not dry:
        print(f'\n共修复 {done} 个文件')


if __name__ == '__main__':
    main()
