#!/usr/bin/env python3
"""前置知识系列质量抽查：必备小节、mermaid 配色、<details>、反例数。"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

root = Path(r'.markdown/重复区域-前置知识-dsh')
CANON = set('#DBEAFE #2563EB #172554 #CFFAFE #0891B2 #164E63 #EDE9FE #7C3AED #3B0764 '
            '#FEF3C7 #D97706 #78350F #DCFCE7 #16A34A #14532D #FEE2E2 #DC2626 #7F1D1D '
            '#FFFFFF #1E293B #94A3B8 #CBD5E1 #F8FAFC #334155 #64748B #F1F5F9 #E2E8F0 '
            '#EFF6FF #BFDBFE #F5F3FF #DDD6FE'.split())

rows = []
for p in sorted(root.rglob('*.md')):
    if '_tools' in str(p) or p.name == 'README.md':
        continue
    text = p.read_text(encoding='utf-8')
    lines = text.count('\n') + 1
    has_q = '先回答一个具体问题' in text
    has_walk = re.search(r'用小数据走一遍', text) is not None
    # 反例计数：数"### 反例"或小节内条目
    fanli_sec = re.search(r'##\s*反例与边界(.*?)(?=\n## |\Z)', text, re.S)
    fanli_n = 0
    if fanli_sec:
        body = fanli_sec.group(1)
        fanli_n = len(re.findall(r'^### |^\*\*\d+\.|^\*\*[一二三四五六七八九十]+、|^\d+\. \*\*|^- \*\*(\d+\. )?|反例\s*\d', body, re.M))
    has_repeat = '对理解 Repeat 的帮助' in text
    has_read = '继续阅读' in text
    details_n = len(re.findall(r'<details>', text))
    # mermaid 配色
    mer_n = len(re.findall(r'```mermaid', text))
    bad_colors = []
    for block in re.findall(r'```mermaid.*?```', text, re.S):
        block_no_init = '\n'.join(ln for ln in block.splitlines() if not ln.strip().startswith('%%{init'))
        colors = re.findall(r'#[0-9A-Fa-f]{6}', block_no_init)
        for c in set(colors):
            cu = c.upper()
            if cu not in CANON and cu not in ('#FFFFFF', '#1E293B'):
                bad_colors.append(cu)
    rows.append((str(p.relative_to(root)), lines, has_q, has_walk, fanli_n, has_repeat, has_read, details_n, mer_n, bad_colors))

print(f'{"文件":<52} {"行":>5} {"问":>3} {"走":>3} {"例":>3} {"帮":>3} {"读":>3} {"折":>3} {"图":>3} 异常配色')
issues = 0
for r in rows:
    flag = ''
    probs = []
    if not r[2]: probs.append('缺先回答')
    if not r[3]: probs.append('缺走查')
    if r[4] < 3: probs.append(f'反例{r[4]}')
    if not r[5]: probs.append('缺Repeat帮助')
    if not r[6]: probs.append('缺继续阅读')
    if r[9]: probs.append('配色:' + ','.join(set(r[9])))
    if probs:
        flag = ' ← ' + '; '.join(probs)
        issues += 1
    print(f'{r[0]:<52} {r[1]:>5} {"✓" if r[2] else "✗":>3} {"✓" if r[3] else "✗":>3} {r[4]:>3} {"✓" if r[5] else "✗":>3} {"✓" if r[6] else "✗":>3} {r[7]:>3} {r[8]:>3}{flag}')
print(f'\n{len(rows)} 篇，其中 {issues} 篇有缺失项')
