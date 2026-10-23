#!/usr/bin/env python3
"""只做一件事：合并 Markdown 中文段落的硬换行。

不修改、不删除任何 HTML（导航条 <div>、分隔线 <hr>、徽章 <span>、
<a href> 链接等一律原样保留）。

保留结构：
- 代码围栏内（``` / ~~~）
- 表格行
- 标题、分隔线
- 块级 HTML（<div> <hr> <p> <details> <summary> 等整行或整块）
- 数学块

合并规则：
- 列表项的缩进续行合并到该项
- 普通段落的连续行合并为一行
- 空格：紧贴型中文标点或两侧汉字直接拼接；涉及 ` ) ] > * _ 等结构符号时补空格
"""

import re
import sys
from pathlib import Path

CJK_CHAR = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
TIGHT_PUNCT = set('，。、；：！？（）《》〈〉“”‘’【】—…·％￥')

FENCE = re.compile(r'^\s{0,3}(```|~~~)')
TABLE = re.compile(r'^\s*\|')
HEADING = re.compile(r'^\s{0,3}#{1,6}\s')
HR = re.compile(r'^\s{0,3}([-*_])\1{2,}\s*$')
MATH_BLOCK = re.compile(r'^\s{0,3}\$\$')
LIST_ITEM = re.compile(r'^(\s{0,3})([-*+]|\d+[.)])\s')

# 任何以 < 开头的行都当作块级 HTML，原样保留、不参与合并
HTML_LINE = re.compile(r'^\s*<')
# 闭合标签独占一行时，下一行若以它开头也应保留
HTML_CLOSE_LEAD = re.compile(r'^\s*</')

# <details>/<summary> 块：内部保留原文（避免破坏折叠区）
DETAILS_OPEN = re.compile(r'^\s*<details\b', re.I)
DETAILS_CLOSE = re.compile(r'^\s*</details>', re.I)


def is_cjk(ch):
    return bool(CJK_CHAR.match(ch))


def is_tight(ch):
    return ch in TIGHT_PUNCT


def join_lines(prev, nxt):
    if not prev:
        return nxt
    if not nxt:
        return prev
    a, b = prev[-1], nxt[0]
    structural = set('`)]>*_')
    if a in structural or b in structural:
        if is_tight(a) and b not in structural:
            return prev + nxt
        if is_tight(b) and a not in structural:
            return prev + nxt
        return prev + ' ' + nxt
    if is_tight(a) or is_tight(b):
        return prev + nxt
    if is_cjk(a) and is_cjk(b):
        return prev + nxt
    return prev + ' ' + nxt


def merge_block(lines):
    out = ''
    for ln in lines:
        out = join_lines(out, ln.strip())
    return out


def unwrap(text):
    lines = text.split('\n')
    result, i, n = [], 0, len(lines)
    in_fence, fence_marker = False, None
    in_details = False

    while i < n:
        line = lines[i]

        m = FENCE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence, fence_marker = True, marker
                result.append(line); i += 1; continue
            if marker == fence_marker:
                in_fence, fence_marker = False, None
                result.append(line); i += 1; continue

        if in_fence:
            result.append(line); i += 1; continue

        # <details> 折叠区：原样保留全部内容
        if DETAILS_OPEN.match(line):
            in_details = True
            result.append(line); i += 1; continue
        if in_details:
            result.append(line)
            if DETAILS_CLOSE.match(line):
                in_details = False
            i += 1
            continue

        stripped = line.strip()

        # 结构性行 / 块级 HTML：原样保留
        if (not stripped or TABLE.match(line) or HEADING.match(line)
                or HR.match(line) or MATH_BLOCK.match(line)
                or HTML_LINE.match(line)):
            result.append(line); i += 1; continue

        lm = LIST_ITEM.match(line)
        if lm:
            indent, bullet = lm.group(1), lm.group(2)
            block = [line]
            i += 1
            while i < n:
                nxt = lines[i]
                ns = nxt.strip()
                if (not ns or TABLE.match(nxt) or HEADING.match(nxt)
                        or HR.match(nxt) or FENCE.match(nxt)
                        or MATH_BLOCK.match(nxt) or LIST_ITEM.match(nxt)
                        or HTML_LINE.match(nxt)):
                    break
                if not nxt.startswith((' ', '\t')):
                    break
                block.append(nxt); i += 1
            if len(block) == 1:
                result.append(block[0])
            else:
                head = f'{indent}{bullet} '
                rest = block[0][len(head):]
                result.append(head + merge_block([rest] + [b.strip() for b in block[1:]]))
            continue

        block = [line]
        i += 1
        while i < n:
            nxt = lines[i]
            ns = nxt.strip()
            if (not ns or TABLE.match(nxt) or HEADING.match(nxt)
                    or HR.match(nxt) or FENCE.match(nxt)
                    or LIST_ITEM.match(nxt) or MATH_BLOCK.match(nxt)
                    or HTML_LINE.match(nxt)):
                break
            block.append(nxt); i += 1

        if len(block) == 1:
            result.append(block[0])
        else:
            result.append(merge_block([b.strip() for b in block]))

    return '\n'.join(result)


def main():
    dry = '--dry' in sys.argv
    paths = [Path(p) for p in sys.argv[1:] if not p.startswith('--')]
    tb = ta = 0
    for p in paths:
        if not p.is_file() or p.suffix != '.md':
            continue
        original = p.read_text(encoding='utf-8')
        fixed = unwrap(original)
        b, a = original.count('\n'), fixed.count('\n')
        tb += b; ta += a
        name = p.name.encode('ascii', 'backslashreplace').decode()
        print(f'{"[dry] " if dry else ""}{b:6d} -> {a:6d}  (-{b-a:5d})  {name}')
        if not dry and b != a:
            p.write_text(fixed, encoding='utf-8')
    print(f'\n合计: {tb} -> {ta}  (-{tb-ta})')


if __name__ == '__main__':
    main()
