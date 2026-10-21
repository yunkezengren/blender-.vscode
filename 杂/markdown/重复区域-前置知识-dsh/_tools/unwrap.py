#!/usr/bin/env python3
"""把 Markdown 中"中文段落的硬换行"合并为单行。

规则：
- 代码围栏内（``` / ~~~）不动
- 表格行（以 | 开头或结尾）不动
- 标题（#）、分隔线（--- ===）、HTML 标签、数学块不动
- 列表项：新项以 (- * + 数字.) 开头；其后续缩进行合并到该项
- 普通段落：连续行合并为一行

合并空格规则（关键）：
- 若两行交界处任一侧是"中文标点或汉字"且另一侧也是同类 → 直接拼接
- 若交界处涉及反引号 `、链接 ](/[)、括号、数字字母等 ASCII 符号
  → 保留一个空格（这些符号在 CJK 语境里仍需要空格分隔，否则渲染粘连）
  例外：中文标点（，。；：！？、）紧邻任何内容时不加空格
"""

import re
import sys
from pathlib import Path

CJK_CHAR = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
CJK_PUNCT = re.compile(r'[\u3000-\u303f\uff00-\uffef]')
# 渲染上紧贴即可、不需要空格的 CJK 标点
TIGHT_PUNCT = set('，。、；：！？（）《》〈〉“”‘’【】—…·％￥')

FENCE = re.compile(r'^\s{0,3}(```|~~~)')
TABLE = re.compile(r'^\s*\|')
HEADING = re.compile(r'^\s{0,3}#{1,6}\s')
HR = re.compile(r'^\s{0,3}([-*_])\1{2,}\s*$')
HTML_BLOCK = re.compile(r'^\s{0,3}<[a-zA-Z/!]')
MATH_BLOCK = re.compile(r'^\s{0,3}\$\$')
LIST_ITEM = re.compile(r'^(\s{0,3})([-*+]|\d+[.)])\s')


def is_cjk_char(ch):
    return bool(CJK_CHAR.match(ch))


def is_tight(ch):
    return ch in TIGHT_PUNCT


def join_lines(prev, nxt):
    """把两行拼成一行，按边界字符决定是否补空格。

    优先级：
    1. 若前一行以 Markdown 链接/行内代码结尾，且下一行以链接/代码/文字开头
       → 补空格（避免 )[[ 粘连成不可解析的语法）
    2. 紧贴型 CJK 标点（，。、；：！？（）等）→ 不空格
    3. 两侧都是 CJK 汉字 → 不空格
    4. 其余 → 补一个空格
    """
    if not prev:
        return nxt
    if not nxt:
        return prev
    a, b = prev[-1], nxt[0]

    # 规则 1：紧邻处出现 Markdown 结构符号时必须留空格
    structural = set('`)]>*_')
    if a in structural or b in structural:
        # 中文标点紧邻结构符号时仍不加空格（如"见（`x`）"）
        if is_tight(a) and b not in structural:
            return prev + nxt
        if is_tight(b) and a not in structural:
            return prev + nxt
        return prev + ' ' + nxt

    # 规则 2：紧贴型 CJK 标点
    if is_tight(a) or is_tight(b):
        return prev + nxt

    # 规则 3：两侧 CJK 汉字
    if is_cjk_char(a) and is_cjk_char(b):
        return prev + nxt

    # 规则 4：默认补空格
    return prev + ' ' + nxt


def merge_block(lines):
    out = ''
    for ln in lines:
        out = join_lines(out, ln.strip())
    return out


def fix_text(text):
    lines = text.split('\n')
    result = []
    i, n = 0, len(lines)
    in_fence = False
    fence_marker = None

    while i < n:
        line = lines[i]

        m = FENCE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence, fence_marker = True, marker
                result.append(line)
                i += 1
                continue
            if marker == fence_marker:
                in_fence, fence_marker = False, None
                result.append(line)
                i += 1
                continue

        if in_fence:
            result.append(line)
            i += 1
            continue

        stripped = line.strip()

        if (not stripped or TABLE.match(line) or HEADING.match(line)
                or HR.match(line) or HTML_BLOCK.match(line)
                or MATH_BLOCK.match(line)):
            result.append(line)
            i += 1
            continue

        # 列表项（含任务列表 - [ ]）：合并缩进续行
        lm = LIST_ITEM.match(line)
        if lm:
            indent, bullet = lm.group(1), lm.group(2)
            block = [line]
            i += 1
            while i < n:
                nxt = lines[i]
                ns = nxt.strip()
                if (not ns or TABLE.match(nxt) or HEADING.match(nxt)
                        or HR.match(nxt) or HTML_BLOCK.match(nxt)
                        or FENCE.match(nxt) or MATH_BLOCK.match(nxt)
                        or LIST_ITEM.match(nxt)):
                    break
                if not nxt.startswith((' ', '\t')):
                    break
                block.append(nxt)
                i += 1
            if len(block) == 1:
                result.append(block[0])
            else:
                head = f'{indent}{bullet} '
                rest = block[0][len(head):]
                merged = merge_block([rest] + [b.strip() for b in block[1:]])
                result.append(head + merged)
            continue

        # 普通段落
        block = [line]
        i += 1
        while i < n:
            nxt = lines[i]
            ns = nxt.strip()
            if (not ns or TABLE.match(nxt) or HEADING.match(nxt)
                    or HR.match(nxt) or HTML_BLOCK.match(nxt)
                    or FENCE.match(nxt) or LIST_ITEM.match(nxt)
                    or MATH_BLOCK.match(nxt)):
                break
            block.append(nxt)
            i += 1

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
        fixed = fix_text(original)
        b, a = original.count('\n'), fixed.count('\n')
        tb += b
        ta += a
        name = p.name.encode('ascii', 'backslashreplace').decode()
        print(f'{"[dry] " if dry else ""}{b:6d} -> {a:6d}  (-{b-a:5d})  {name}')
        if not dry and b != a:
            p.write_text(fixed, encoding='utf-8')
    print(f'\n合计: {tb} -> {ta}  (-{tb-ta})')


if __name__ == '__main__':
    main()
