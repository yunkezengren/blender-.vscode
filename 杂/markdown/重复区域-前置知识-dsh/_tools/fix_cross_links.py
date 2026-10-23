#!/usr/bin/env python3
"""修复前置知识目录中指向主系列（重复区域-dsh）的相对链接。

前置知识原位于 .markdown/重复区域-dsh/00-前置知识/，用 ../../XX 回主系列。
现在独立为 .markdown/重复区域-前置知识-dsh/，正确前缀是 ../../重复区域-dsh/XX。

本脚本只改链接目标，不动任何内容。
"""

import re
import sys
from pathlib import Path

CHAPTERS = [
    '00-课程指南',
    '01-Zone系统基础',
    '02-Repeat区域数据模型',
    '03-几何节点执行架构',
    '04-运行时机制',
    '05-跨后端实现',
    '06-实战与性能',
    '90-实现依赖专题',
    '91-验收报告',
]

# 匹配 ](../../CHAP/...  — 只替换目标为 ../../重复区域-dsh/CHAP/...
PATTERN = re.compile(
    r'\]\(\.\./\.\./(' + '|'.join(re.escape(c) for c in CHAPTERS) + r')'
)


def fix(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    new_text, n = PATTERN.subn(lambda m: '](../../重复区域-dsh/' + m.group(1), text)
    if n:
        path.write_text(new_text, encoding='utf-8')
    return n


def main():
    dry = '--dry' in sys.argv
    root = Path('.markdown/重复区域-前置知识-dsh')
    total = 0
    for p in sorted(root.rglob('*.md')):
        if '_tools' in str(p):
            continue
        if dry:
            t = p.read_text(encoding='utf-8')
            n = len(PATTERN.findall(t))
            if n:
                name = p.name.encode('ascii', 'backslashreplace').decode()
                print(f'[dry] {n} 处  {name}')
                total += n
        else:
            n = fix(p)
            if n:
                name = p.name.encode('ascii', 'backslashreplace').decode()
                print(f'修复 {n} 处  {name}')
                total += n
    print(f'\n共 {"将修复" if dry else "已修复"} {total} 处')


if __name__ == '__main__':
    main()
