#!/usr/bin/env python3
"""规范化本系列 Markdown：
1. 删除代理写入的内联装饰 HTML（<div style> <hr style> <span style> <p style> 等块）
2. 把 <a href="X">text</a> 转成标准 Markdown 链接 [text](X)
3. 把 <br> / <br/> 转成空格或换行
4. 合并中文段落的硬换行（保留代码围栏/表格/标题/列表结构）

用法：
  python normalize.py --dry  <files...>
  python normalize.py        <files...>
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

# 装饰性块 HTML：整块删除（div 包住的导航条等）
HTML_BLOCK_DIV = re.compile(r'<div\b[^>]*>.*?</div>\s*', re.S | re.I)
# 单行装饰：删掉整行
HTML_LINE = re.compile(r'^\s*<(hr|br|p)\b[^>]*>\s*$', re.I)
# 行内 span/p 包裹：剥标签保内容
HTML_INLINE_STRIP = re.compile(r'</?(span|p|b|i|strong|em)\b[^>]*>', re.I)
# <a href="X" ...>text</a> → [text](X)
HTML_ANCHOR = re.compile(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.S | re.I)
# <br> → 空格
HTML_BR = re.compile(r'<br\s*/?>', re.I)


def strip_html(text: str) -> str:
    text = HTML_BLOCK_DIV.sub('', text)
    text = HTML_ANCHOR.sub(lambda m: f'[{m.group(2).strip()}]({m.group(1)})', text)
    text = HTML_BR.sub(' ', text)
    text = HTML_INLINE_STRIP.sub('', text)
    # 删除整行的 <hr>/<p>
    text = '\n'.join(
        '' if HTML_LINE.match(ln) else ln for ln in text.split('\n')
    )
    return text


def is_cjk(ch) -> bool:
    return bool(CJK_CHAR.match(ch))


def is_tight(ch) -> bool:
    return ch in TIGHT_PUNCT


def join_lines(prev: str, nxt: str) -> str:
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
    if a in TIGHT_PUNCT or b in TIGHT_PUNCT:
        return prev + nxt
    if is_cjk(a) and is_cjk(b):
        return prev + nxt
    return prev + ' ' + nxt


def merge_block(lines):
    out = ''
    for ln in lines:
        out = join_lines(out, ln.strip())
    return out


def unwrap(text: str) -> str:
    lines = text.split('\n')
    result, i, n = [], 0, len(lines)
    in_fence, fence_marker = False, None

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

        stripped = line.strip()
        if (not stripped or TABLE.match(line) or HEADING.match(line)
                or HR.match(line) or MATH_BLOCK.match(line)):
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
                        or MATH_BLOCK.match(nxt) or LIST_ITEM.match(nxt)):
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
                    or LIST_ITEM.match(nxt) or MATH_BLOCK.match(nxt)):
                break
            block.append(nxt); i += 1

        if len(block) == 1:
            result.append(block[0])
        else:
            result.append(merge_block([b.strip() for b in block]))

    return '\n'.join(result)


def normalize(text: str) -> str:
    text = strip_html(text)
    text = unwrap(text)
    # 压缩 3+ 连续空行为 2 个
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def main():
    dry = '--dry' in sys.argv
    paths = [Path(p) for p in sys.argv[1:] if not p.startswith('--')]
    tb = ta = 0
    for p in paths:
        if not p.is_file() or p.suffix != '.md':
            continue
        original = p.read_text(encoding='utf-8')
        fixed = normalize(original)
        b, a = original.count('\n'), fixed.count('\n')
        tb += b; ta += a
        name = p.name.encode('ascii', 'backslashreplace').decode()
        print(f'{"[dry] " if dry else ""}{b:6d} -> {a:6d}  (-{b-a:5d})  {name}')
        if not dry and b != a:
            p.write_text(fixed, encoding='utf-8')
    print(f'\n合计: {tb} -> {ta}  (-{tb-ta})')


if __name__ == '__main__':
    main()
