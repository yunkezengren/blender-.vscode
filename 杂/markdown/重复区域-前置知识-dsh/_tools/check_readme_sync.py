#!/usr/bin/env python3
"""核对各章 README 规划表与实际落盘文件是否一致。"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
root = Path(r'.markdown/重复区域-前置知识-dsh')

total_plan = total_have = 0
for ch in sorted(d for d in root.iterdir() if d.is_dir() and d.name != '_tools'):
    readme = ch / 'README.md'
    if not readme.exists():
        print(f'{ch.name}: 缺 README')
        continue
    text = readme.read_text(encoding='utf-8')
    planned = [m.group(2) for m in re.finditer(r'\|\s*\d+\s*\|\s*\[([^\]]+)\]\(([^)]+\.md)\)', text)]
    actual = sorted(p.name for p in ch.glob('*.md') if p.name != 'README.md')
    missing = [p for p in planned if p not in actual]
    extra = [a for a in actual if a not in planned]
    total_plan += len(planned)
    total_have += len(actual)
    status = 'OK' if not missing and not extra else 'DIFF'
    print(f'{ch.name:<24} 计划{len(planned)} 实际{len(actual)} [{status}]')
    if missing:
        print(f'    缺: {missing}')
    if extra:
        print(f'    额外(README 未列): {extra}')
print(f'\n合计: 计划 {total_plan} 篇, 实际 {total_have} 篇')
