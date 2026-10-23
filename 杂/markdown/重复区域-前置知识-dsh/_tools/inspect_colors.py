#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CANON = set('#DBEAFE #2563EB #172554 #CFFAFE #0891B2 #164E63 #EDE9FE #7C3AED #3B0764 '
            '#FEF3C7 #D97706 #78350F #DCFCE7 #16A34A #14532D #FEE2E2 #DC2626 #7F1D1D '
            '#FFFFFF #1E293B'.split())
for f in sys.argv[1:]:
    text = open(f, encoding='utf-8').read()
    for i, block in enumerate(re.findall(r'```mermaid.*?```', text, re.S)):
        colors = set(c.upper() for c in re.findall(r'#[0-9A-Fa-f]{6}', block))
        extra = colors - CANON
        if extra:
            print(f'{f.split(chr(92))[-1]} 块{i}: 额外色 {sorted(extra)}')
            for ln in block.splitlines():
                if '#' in ln and any(x in ln.upper() for x in extra):
                    print('    ', ln.strip()[:120])
