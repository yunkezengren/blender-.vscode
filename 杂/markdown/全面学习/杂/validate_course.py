"""静态验收：页面结构、链接、锚点、课程数量和源码摘录证据。"""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).absolute().parent
REPO = next(p for p in ROOT.parents if (p/'source/blender').is_dir() and (p/'.git').exists())

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.h1, self.title = path, [], [], 0, 0
        self.demo, self.lesson, self.lang = 0, None, None
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.title += 1
        if tag == 'html': self.lang = a.get('lang')
        if 'data-demo' in a: self.demo += 1
        if 'data-lesson-id' in a: self.lesson = a['data-lesson-id']
        for attr in ('href', 'src'):
            if attr in a: self.links.append(a[attr])

pages = {p.absolute():Page(p) for p in ROOT.rglob('*.html')}
errors=[]
link_count=0
for p, obj in pages.items():
    if obj.h1 != 1 or obj.title != 1: errors.append(f'{p.name}: h1/title count')
    if obj.lang != 'zh-CN': errors.append(f'{p.name}: lang')
    if len(obj.ids) != len(set(obj.ids)): errors.append(f'{p.name}: duplicate IDs')
    for url in obj.links:
        u=urlsplit(url)
        if u.scheme == 'file':
            local_file = Path(unquote(u.path).lstrip('/'))
            if not local_file.is_file(): errors.append(f'{p.name}: missing source {url}')
            link_count += 1
            continue
        if u.scheme or u.netloc: continue
        target=(p.parent/unquote(u.path)).absolute() if u.path else p
        # resolve 用于存在性与锚点匹配，不改变输出目录。
        resolved=target.resolve()
        if not resolved.is_file(): errors.append(f'{p.name}: missing {url}'); continue
        if resolved.suffix=='.html' and u.fragment:
            other=next((v for k,v in pages.items() if k.resolve()==resolved), None)
            if not other or unquote(u.fragment) not in other.ids: errors.append(f'{p.name}: bad anchor {url}')
        link_count+=1
evidence=json.loads((ROOT/'evidence.json').read_text(encoding='utf-8'))
for path, info in evidence['sources'].items():
    if hashlib.sha256((REPO/path).read_bytes()).hexdigest()!=info['sha256']:
        errors.append(f'source changed after generation: {path}')
lessons=[p for p in pages.values() if p.lesson]
folders=[p for p in ROOT.iterdir() if p.is_dir() and re.match(r'^\d{2}-',p.name)]
assert len(pages)==49, len(pages)
assert len(lessons)==36, len(lessons)
assert len(folders)==12, len(folders)
assert sum(p.demo for p in lessons)==12
assert len({p.lesson for p in lessons})==36
deep=evidence['deep_readings']
assert len({u['lesson'] for u in deep})==36, 'Every lesson must have line explanations'
for lesson in lessons:
    source=lesson.path.read_text(encoding='utf-8')
    assert 'class="deep-reading"' in source, lesson.path
    assert 'class="syntax-' in source, lesson.path
report={
    'pages':len(pages), 'lessons':len(lessons), 'module_folders':len(folders),
    'local_links_checked':link_count, 'interactive_models':12,
    'commit_count':len(evidence['commits']), 'source_files':len(evidence['sources']),
    'authored_characters':sum(e['characters'] for e in evidence['pages']),
    'lessons_with_line_explanations':len({u['lesson'] for u in deep}),
    'complete_source_units':len(deep),
    'explained_source_lines':sum(u['explained_lines'] for u in deep),
    'html_lines_min':min(len(p.path.read_text(encoding='utf-8').splitlines()) for p in lessons),
    'html_lines_max':max(len(p.path.read_text(encoding='utf-8').splitlines()) for p in lessons),
    'errors':errors
}
(ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
