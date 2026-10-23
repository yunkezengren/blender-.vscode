#!/usr/bin/env python3
"""扫描前置知识系列中的疑似段内硬换行（连续两行中文散文）。"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

root = Path(r'.markdown/重复区域-前置知识-dsh')
bad = 0
for p in sorted(root.rglob('*.md')):
    if '_tools' in str(p):
        continue
    lines = p.read_text(encoding='utf-8').split('\n')
    in_fence = False
    prev_text = None
    prev_no = 0
    for i, ln in enumerate(lines):
        s = ln.rstrip()
        if s.startswith('```'):
            in_fence = not in_fence
            prev_text = None
            continue
        if in_fence or not s.strip():
            prev_text = None
            continue
        stripped = s.lstrip()
        skip_starts = ('|', '#', '-', '*', '   ', '\t', '>', '<')
        if any(stripped.startswith(x) for x in skip_starts) or re.match(r'^\d+\.', stripped):
            prev_text = None
            continue
        if prev_text is not None and re.search(r'[\u4e00-\u9fff]', s) and re.search(r'[\u4e00-\u9fff]', prev_text):
            print(f'{p.parent.name}/{p.name}:{prev_no}-{i+1} 疑似硬换行: ...{prev_text[-25:]} || {s[:25]}...')
            bad += 1
        prev_text = s
        prev_no = i + 1
print(f'\n疑似硬换行总数: {bad}')
