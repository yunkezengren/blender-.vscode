#!/usr/bin/env python3
"""给 flowchart/graph 类型的 mermaid 块补齐六色 classDef；0 定义时按首=入、尾=果、中=算上色。"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CANON = {
    'input': 'fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px',
    'data': 'fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px',
    'abstraction': 'fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px',
    'compute': 'fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px',
    'result': 'fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px',
    'error': 'fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px',
}

def fix_block(block: str) -> str:
    body = re.sub(r'^```mermaid\s*', '', block.rstrip()).rstrip('`').strip()
    if not re.match(r'^(flowchart|graph)\b', body, re.M):
        return block
    present = set(re.findall(r'classDef\s+(\w+)', body))
    lines = block.rstrip().rstrip('`').rstrip()
    add = []
    if not present:
        ids = re.findall(r'^\s*([A-Z][A-Za-z0-9_]*)\[', body, re.M)
        if ids:
            mid = ids[1:-1]
            cls = [f'    class {ids[0]} input']
            if mid:
                cls.append('    class ' + ','.join(mid) + ' compute')
            if len(ids) > 1:
                cls.append(f'    class {ids[-1]} result')
            add += cls
        for name, style in CANON.items():
            add.append(f'    classDef {name} {style};')
    else:
        for name, style in CANON.items():
            if name not in present:
                add.append(f'    classDef {name} {style};')
    if not add:
        return block
    return lines + '\n' + '\n'.join(add) + '\n```\n'

changed = 0
root = Path('.markdown/重复区域-前置知识-dsh')
for p in root.rglob('*.md'):
    if '_tools' in str(p):
        continue
    text = p.read_text(encoding='utf-8')
    def repl(m):
        global changed
        nb = fix_block(m.group(0))
        if nb != m.group(0):
            changed += 1
        return nb
    new = re.sub(r'```mermaid[\s\S]*?```', repl, text)
    if new != text:
        p.write_text(new, encoding='utf-8')
        print(f'修补: {p.relative_to(root)}')
print(f'共修补 {changed} 个块')
