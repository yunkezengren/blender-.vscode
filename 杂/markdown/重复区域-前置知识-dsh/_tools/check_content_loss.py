#!/usr/bin/env python3
"""对比 HEAD 与工作树：找出 HEAD 中存在、工作树中消失的正文文本（考虑 unwrap 合并）。"""
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(r"D:\Repository\blender-git\blender\.vscode")
DIR = "杂/markdown/重复区域-dsh"


def norm(s: str) -> str:
    s = re.sub(r'<[^>]+>', '', s)          # 去标签
    s = s.replace('&quot;', '"').replace('&amp;', '&').replace('&nbsp;', ' ')
    return re.sub(r'\s+', '', s)            # 去全部空白


def main():
    files = subprocess.run(
        ['git', 'ls-tree', '-r', '--name-only', 'HEAD', '--', DIR],
        cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.splitlines()
    total_missing = 0
    for rel in files:
        if not rel.endswith('.md'):
            continue
        head = subprocess.run(
            ['git', 'show', f'HEAD:{rel}'],
            cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout
        cur_path = ROOT / rel.replace('/', '\\')
        if not cur_path.exists():
            print(f"[缺失文件] {rel}")
            total_missing += 1
            continue
        cur = cur_path.read_text(encoding='utf-8')
        cur_norm = norm(cur)
        missing = []
        for line in head.splitlines():
            t = line.strip()
            if len(t) < 6:
                continue
            n = norm(t)
            if len(n) < 4:
                continue
            if not re.search(r'[\u4e00-\u9fffA-Za-z0-9]', n):
                continue
            if n not in cur_norm:
                missing.append(t)
        if missing:
            name = rel.split('/')[-1]
            print(f"\n=== {name}: {len(missing)} 段文本消失 ===")
            for m in missing[:12]:
                print(f"  - {m[:110]}")
            if len(missing) > 12:
                print(f"  ... 其余 {len(missing)-12} 段")
            total_missing += len(missing)
    print(f"\n总计消失文本行: {total_missing}")


if __name__ == '__main__':
    main()
