"""生成离线 HTML 学习手册；只写入本目录，不修改 Blender 源码。"""
from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

sys.dont_write_bytecode = True
ROOT = Path(__file__).absolute().parent
REPO = next(p for p in ROOT.parents if (p/'source/blender').is_dir() and (p/'.git').exists())
REFERENCE = ROOT.parent / '属性文本遮挡剔除详细学习-DS' / '01-投影数学手册.html'
DATE = '2026-10-11'
from deep_reading import UNITS
import deep_reading_more
import deep_reading_vector
import deep_reading_foundations
import deep_reading_systems
import deep_reading_boundaries
import deep_reading_architecture
from source_comments import explain_comment

def git(*args):
    return subprocess.run(['git', *args], cwd=REPO, check=True, capture_output=True,
                          encoding='utf-8', errors='replace').stdout.strip()

def load_modules():
    result = []
    for name in ['content_01_04', 'content_05_08', 'content_09_12']:
        spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result.extend(mod.MODULES)
    return result

E = html.escape
def P(text):
    return '<p>' + E(text) + '</p>\n'

def link(path, label):
    return f'<a href="{quote(str(path).replace(chr(92), "/"), safe="/:#.-")}">{E(label)}</a>'

TOKEN = re.compile(r'(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)|(?P<string>"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27)|(?P<preprocessor>^[ \t]*\#[^\n]*)|(?P<number>\b(?:0[xX][\da-fA-F]+|\d+(?:\.\d+)?)\b)|(?P<identifier>\b[A-Za-z_]\w*\b)', re.M)
KEYWORDS = set('alignof auto bool break case catch char class const constexpr continue default delete double else enum explicit false float for friend if inline int int64_t mutable namespace new noexcept nullptr operator private protected public return short signed sizeof static static_cast struct switch template this throw true try typename union unsigned using virtual void volatile while'.split())
def highlight(code):
    result=[]; at=0
    for match in TOKEN.finditer(code):
        result.append(E(code[at:match.start()]))
        kind=match.lastgroup; value=match.group()
        if kind=='identifier':
            kind='keyword' if value in KEYWORDS else ('type' if value[0].isupper() else ('function' if re.match(r'\s*\(',code[match.end():]) else None))
        # Split tokens at physical line boundaries so each source line remains separately addressable.
        result.append('\n'.join(f'<span class="syntax-{kind}">{E(part)}</span>' if kind and part else E(part) for part in value.split('\n')))
        at=match.end()
    result.append(E(code[at:])); return ''.join(result)

def code_block(code, label='教学伪代码 · 非 Blender 原实现', start=None):
    lines = []
    for i, line in enumerate(highlight(code).splitlines()):
        n = (start or 1) + i
        lines.append(f'<span class="code-line" data-line="{n}">{line}</span>')
    return ('<div class="code"><div class="bar"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span class="path">{E(label)}</span><button class="copy-code" type="button">复制代码</button></div>'
            '<pre><code>' + '\n'.join(lines) + '</code></pre></div>\n')

def note(title, body, variant=''):
    return f'<aside class="note {variant}"><span class="ico" aria-hidden="true">i</span><div class="t">{E(title)}</div>{P(body)}</aside>\n'

def flow(items):
    return '<div class="flow" aria-label="本模块的概念关系">' + ''.join(
        f'<div class="flow-step"><span>{i+1:02}</span><strong>{E(x)}</strong></div>' for i,x in enumerate(items)) + '</div>'

def section(id_, n, title, content):
    return f'<section id="{id_}"><h2><span class="n">{n:02}</span>{E(title)}</h2>\n{content}</section>\n'

def source_card(spec, source_id, page_depth):
    path, needle, why = spec
    source_path = REPO / path
    if not source_path.is_file():
        raise ValueError(f'Missing source: {path}')
    text = source_path.read_text(encoding='utf-8')
    lines = text.splitlines()
    matches = [i for i,s in enumerate(lines) if needle in s]
    if not matches:
        raise ValueError(f'Symbol not found: {path}: {needle}')
    at = matches[0]
    start = max(0, at-3)
    excerpt = '\n'.join(lines[start:start+32])
    sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
    evidence['sources'][path] = {'sha256':sha, 'lines':len(lines)}
    # .markdown 在此工作区是目录联接；绝对文件 URL 避免经物理路径打开时相对路径偏移。
    local = source_path.absolute().as_uri()
    out = f'<article class="source-card" id="{source_id}"><div class="source-title"><span class="pill">CURRENT SOURCE</span>{link(local, Path(path).name)}</div>'
    out += P(why) + f'<p class="source-meta">源码定位入口 · 符号位于第 {at+1} 行 · SHA-256 {sha[:12]}</p>'
    out += f'<details><summary>完整路径与继续阅读方法</summary><p><code>{E(path)}</code></p>'
    out += P('这里仅提供进一步追踪的源码入口，不再放入没有逐行讲解的截断代码窗口。正文所展示的真实实现均在上面的精读单元中逐行解释。点击文件名可查看本地完整文件。')
    out += code_block(f'git log --oneline -- "{path}"\ngit blame -L {start+1},{min(start+32,len(lines))} -- "{path}"', 'PowerShell · 在仓库根目录执行')
    return out + '</details></article>\n'

def deep_card(unit, uid):
    path=REPO/unit['path']; lines=path.read_text(encoding='utf-8').splitlines()
    evidence['sources'][unit['path']]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'lines':len(lines)}
    matches=[i for i,line in enumerate(lines) if unit['anchor'] in line and not line.rstrip().endswith(';')]
    if unit.get('within'):
        lower=next(i for i,line in enumerate(lines) if unit['within'] in line)
        matches=[i for i in matches if i>lower]
    start=matches[unit.get('occurrence',0)]
    depth=0; opened=False; end=start
    for end in range(start,len(lines)):
        # Ignore default arguments such as allocator = {} until the real body opens.
        if not opened and not lines[end].rstrip().endswith('{'): continue
        opened=True
        depth += lines[end].count('{')-lines[end].count('}')
        if opened and depth==0: break
    numbered=[(i+1,lines[i]) for i in range(start,end+1) if lines[i].strip()]
    if 'semantic_notes' in unit:
        comment_notes={}
        raw='\n'.join(lines[start:end+1])
        for match in re.finditer(r'/\*[\s\S]*?\*/',raw):
            first=start+1+raw[:match.start()].count('\n')
            if not lines[first-1].strip().startswith('/*'): continue
            translated=explain_comment(match.group())
            for offset,_ in enumerate(match.group().splitlines()):
                comment_notes[first+offset]=translated if offset==0 else f'续接 L{first} 的同一注释块，完整译解见该行；这部分不生成可执行语句。'
        notes=[]; semantic=iter(unit['semantic_notes']); consumed=0; scopes=[]; previous=unit['title']
        for n,line in numbered:
            stripped=line.strip()
            if n in comment_notes:
                notes.append(comment_notes[n])
            elif stripped in ('{','}','};', 'else {'):
                if stripped=='{': notes.append('打开 '+previous+' 的语句体；后续构造的局部对象受此作用域约束。')
                elif stripped=='else {': notes.append('进入前一个条件不成立时的路径；两条路径分别检查对象与存储状态。')
                else: notes.append('结束 '+(scopes[-1] if scopes else unit['title'])+' 的作用域。局部拥有者在此按其类型执行析构。')
            else:
                try: notes.append(next(semantic)); consumed+=1
                except StopIteration: raise ValueError(f'Missing semantic note {uid} L{n}: {stripped}')
            if n not in comment_notes:
                delta=stripped.count('{')-stripped.count('}')
                if delta>0: scopes.extend([previous if stripped=='{' else stripped]*delta)
                elif delta<0:
                    for _ in range(min(-delta,len(scopes))): scopes.pop()
                previous=stripped
        remaining=list(semantic)
        if remaining: raise ValueError(f'Extra semantic notes {uid}: {remaining}; source='+str(numbered))
        unit['notes']=notes
    if len(numbered)!=len(unit['notes']):
        raise ValueError(f"Line explanation mismatch {uid}: {len(numbered)} source lines / {len(unit['notes'])} notes")
    evidence.setdefault('deep_readings',[]).append({'lesson':uid,'path':unit['path'],'start':start+1,'end':end+1,'explained_lines':len(numbered)})
    out='<article class="deep-reading"><h3>'+E(unit['title'])+'</h3>'+P(unit['intro'])
    out+=P(f"完整源码单元 · {unit['path']} · L{start+1}–L{end+1}。空行仅用于分段；下表逐条覆盖所有非空源码行，包括边界与注释。")
    out+=code_block('\n'.join(lines[start:end+1]),unit['path'],start+1)
    out+='<div class="line-explanations">'
    for (n,line),explanation in zip(numbered,unit['notes']):
        out+=f'<div class="line-explanation"><span class="line-number">L{n}</span><div><code>{highlight(line.strip())}</code>{P(explanation)}</div></div>'
    out+='</div><h4>用具体输入推演状态</h4>'+P(unit['trace'])+'<h4>调用关系与设计判断</h4>'+P(unit['design'])+'</article>'
    return out

def commit_card(short, focus):
    c = commits[short]
    url = 'https://projects.blender.org/blender/blender/commit/' + c['hash']
    out = f'<article class="commit-card"><div class="commit-kicker"><span class="pill">HISTORY</span> <a href="{url}" target="_blank" rel="noopener">{short}</a> <span>{E(c["author"])} · {c["date"]}</span></div>'
    out += '<h3>' + E(c['subject']) + '</h3>' + P(focus)
    out += '<details><summary>展开提交原文、变更规模与阅读命令</summary>'
    out += '<div class="commit-body"><pre>' + E(c['body'] or c['subject']) + '</pre></div>'
    out += code_block(c['stat'], '真实 Git 变更统计')
    out += code_block(f'git show --stat {short}\ngit show {short}\n# 聚焦单个文件：git show {short} -- source/blender/…', 'PowerShell · 只读查看')
    return out + '</details></article>\n'

def demo(kind):
    return f'<div class="demo" data-demo="{kind}"><div class="demo-heading"><span class="pill">INTERACTIVE LAB</span><strong>改变一个条件，观察模型</strong></div><div class="demo-controls"></div><div class="demo-result" aria-live="polite"></div><p class="demo-caption">教学简化模型，帮助推演状态；不等同于 Blender 完整实现，也不执行性能基准。</p><noscript>开启 JavaScript 可使用交互；正文和源码仍可离线阅读。</noscript></div>'

def head(title, prefix, description):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{E(description)}">
<title>{E(title)} · Blender 全面学习</title>
<link rel="stylesheet" href="{prefix}course.css">
<script src="{prefix}course-index.js" defer></script>
<script src="{prefix}course.js" defer></script>
</head>
'''

def topbar(prefix, module=None):
    crumb = f' / <a href="index.html">{E(module["name"])}</a>' if module else ''
    return f'''<a class="skip-link" href="#main">跳到正文</a>
<header class="topbar"><div class="topbar-inner"><a class="wordmark" href="{prefix}index.html"><span class="brand-mark">B</span> BLENDER <span class="wordmark-soft">/ 全面学习</span></a><span class="crumb">{crumb}</span><div class="toolbar"><button type="button" id="theme-toggle" aria-label="切换配色主题">切换主题</button><button type="button" id="font-toggle" aria-label="切换大字阅读">大字</button><button type="button" id="print-page">打印</button></div></div></header>'''

def hero(eyebrow, title, lead, chips, side=''):
    return f'<div class="hero"><div class="hero-inner"><div class="eyebrow"><span class="dot"></span>{E(eyebrow)}</div><h1>{E(title)}</h1><p class="lede">{E(lead)}</p><div class="chips">' + ''.join(f'<span class="chip">{E(c)}</span>' for c in chips) + '</div>' + side + '</div></div>'

def footer(prefix):
    return f'<footer class="site-footer"><p>Blender 全面学习 · 本地源码研读手册 · {DATE}</p><p>源码基线 HEAD <code>{head_hash[:11]}</code>；摘录来自生成时工作区。教学伪代码与历史提交已分别标识。</p><p>{link(prefix+"index.html", "返回课程总览")} · {link(prefix+"evidence.json", "查看源码与提交证据清单")}</p></footer><div id="toast" role="status" aria-live="polite"></div></body></html>'

def aside(items, module=None):
    out = '<nav class="toc" aria-label="文档目录"><div class="toc-title">ON THIS PAGE / 本页</div>'
    out += ''.join(f'<a href="#{id_}" class="lv1">{E(label)}</a>' for id_,label in items)
    if module:
        out += '<div class="toc-title spaced">本方向 · 三篇课程</div>'
        out += ''.join(f'<a href="{quote(d["slug"])}.html">{i+1:02} {E(d["title"])}</a>' for i,d in enumerate(module['docs']))
        out += '<div class="toc-title spaced">学习建议</div><p class="toc-note">先推演，再读源码；先复现，再做优化。完成标记建议以练习验收为准。</p>'
    return out + '</nav>'

def page_card(entry, prefix=''):
    return f'<a class="lesson-card" data-course-id="{entry["id"]}" href="{quote(prefix+entry["url"])}"><div class="card-top"><span>{entry["module_id"]} / {entry["lesson_no"]:02}</span><span class="completion-label">待学习</span></div><h3>{E(entry["title"])}</h3><p>{E(entry["lead"])}</p><div class="card-bottom"><span>{entry["characters"]:,} 字符 · {entry["minutes"]} 分钟研读建议</span><b aria-hidden="true">↗</b></div></a>'

def write(path, text):
    path.write_text(text, encoding='utf-8', newline='\n')

modules = load_modules()
head_hash = git('rev-parse', 'HEAD')
evidence = {'generated_date':DATE, 'head':head_hash, 'source_basis':'current working tree; no C/C++ files modified', 'sources':{}, 'commits':{}, 'pages':[]}
commits = {}
for m in modules:
    for d in m['docs']:
        for short,_ in d['commits']:
            if short in commits:
                continue
            raw = git('show','-s','--format=%H%x00%an%x00%ad%x00%s%x00%b','--date=short',short).split('\0',4)
            commits[short] = dict(zip(['hash','author','date','subject','body'],raw))
            commits[short]['stat'] = git('show','--format=','--stat',short)
evidence['commits'] = commits

# 保留参考页面的配色、代码块、提示卡与表格风格，并追加课程站点布局。
ref = REFERENCE.read_text(encoding='utf-8')
base_css = re.search(r'<style>(.*?)</style>', ref, re.S).group(1)
overrides = (ROOT/'layout.css').read_text(encoding='utf-8')
write(ROOT/'course.css', '/* 基础视觉来自用户指定的投影数学手册；课程扩展见 layout.css。 */\n'+base_css+'\n'+overrides)

entries=[]
for m in modules:
    m['folder'] = m['id']+'-'+m['name']
    (ROOT/m['folder']).mkdir(exist_ok=True)
    for i,d in enumerate(m['docs']):
        prose = ' '.join([d['title'],d['lead'],d['trap']] + [x for s in d['sections'] for x in s] + d['lab'] + [x for q in d['qa'] for x in q])
        prose += ' '.join(' '.join([u['intro'],u['trace'],u['design']]+u.get('notes',u.get('semantic_notes',[]))) for u in UNITS.get(m['id']+'-'+str(i+1).zfill(2),[]))
        chars = len(re.sub(r'\s','',prose))
        entry={'id':m['id']+'-'+str(i+1).zfill(2),'module_id':m['id'],'module':m['name'],'lesson_no':i+1,'title':d['title'],'lead':d['lead'],'url':m['folder']+'/'+d['slug']+'.html','characters':chars,'minutes':max(15,round(chars/90))}
        entries.append(entry)
        d['entry']=entry

for idx,entry in enumerate(entries):
    m = next(m for m in modules if m['id']==entry['module_id'])
    d=m['docs'][entry['lesson_no']-1]
    toc=[('overview','01 学习目标与前置知识'),('model','02 原理与推演'),('source','03 当前源码精读'),('history','04 提交与设计演化'),('experiment','05 实验与验收'),('quiz','06 自测与参考答案')]
    out=head(d['title'],'../',d['lead']) + f'<body data-lesson-id="{entry["id"]}">'
    out+=topbar('../',m)
    out+=hero(f'{m["tag"]} / LESSON {entry["id"]}',d['title'],d['lead'],[f'方向 {m["id"]} · {m["name"]}',f'专题 {entry["lesson_no"]}/3',f'正文 {entry["characters"]:,} 字符',f'建议研读 {entry["minutes"]} 分钟 + 独立练习'])
    out+='<div class="wrap">'+aside(toc,m)+'<main id="main">'
    overview=P(m['intro'])+note('开始前需要掌握',m['prereq'])+flow(m['flow'])
    overview+=note('这一课的完成证据',d['lab'][-1], 'ok')
    out+=section('overview',1,'这一课要建立的能力',overview)
    model=''
    for s in d['sections']:
        model+='<h3>'+E(s[0])+'</h3>\n'+''.join(P(p) for p in s[1:])
    model+=note('原理模型与实际实现','下面的源码精读使用真实实现。请把原理中的数据、状态和不变量逐项映射到源码，不要用教学伪代码替代实际的对象生命周期或并发协议。')
    if d.get('demo'): model+=demo(d['demo'])
    model+=note('容易误判的边界',d['trap'],'warn')
    out+=section('model',2,'原理、状态与设计取舍',model)
    units=UNITS.get(entry['id'],[])
    source=P('本篇的逐行精读范围是下面明确列出的完整函数或类型定义。源码直接读取当前工作区，说明使用真实文件行号。先读代码，再对照解释，最后独立复述状态推演。' if units else '本篇目前保留原理与源码入口，尚未补齐逐行精读。下面是定位窗口，不代表完整函数；不要把它当成已经完成的逐行教程。')
    source+=''.join(deep_card(u,entry['id']) for u in units)
    source+='<details><summary>补充源码入口与本地文件链接</summary>'+''.join(source_card(s,f'source-{i+1}',1) for i,s in enumerate(d['sources']))+'</details>'
    out+=section('source',3,'从真实源码进入实现',source)
    history=P('按“原问题 → 不变量 → 方案 → 代价 → 验证”阅读。提交中的性能数字与行为描述属于当时的实现；本页不宣称已在本机复现实验。')
    history+=''.join(commit_card(short,why) for short,why in d['commits'])
    out+=section('history',4,'设计是怎样演化出来的',history)
    exp='<ol class="lab-steps">'+''.join(f'<li><strong>任务 {i+1:02}</strong>{P(x)}</li>' for i,x in enumerate(d['lab']))+'</ol>'
    exp+=note('提交你的学习结果','保留问题模型、最小实现、失败样例和验证记录。凡是伪代码中省略的类型、溢出、异常或并发处理，都应在自己的实现说明中列出。','ok')
    exp+='<div class="checklist">'+''.join(f'<label><input type="checkbox" data-check="{entry["id"]}-{i}"><span>{E(x)}</span></label>' for i,x in enumerate(['我能不看源码解释核心不变量。','我构造过至少一个边界或失败输入。','我的结果与独立基准对照过。']))+'</div>'
    out+=section('experiment',5,'独立实验与验收',exp)
    quiz=''.join(f'<details class="question"><summary>{E(q)}</summary>{P(a)}</details>' for q,a in d['qa'])
    quiz+=f'<div class="completion-panel"><div><strong>把理解变成可验证的能力</strong><p>建议完成练习后再标记；进度保存在当前浏览器。</p></div><button type="button" id="mark-complete" data-id="{entry["id"]}" aria-pressed="false">标记本篇完成</button></div>'
    out+=section('quiz',6,'自测：先回答，再展开',quiz)
    out+='<nav class="page-nav" aria-label="前后课程">'
    out+= link('../'+entries[idx-1]['url'],'← 上一篇：'+entries[idx-1]['title']) if idx else link('../index.html','← 课程总览')
    out+= link('../'+entries[idx+1]['url'],'下一篇：'+entries[idx+1]['title']+' →') if idx<len(entries)-1 else link('../index.html','完成第一轮，返回总览 →')
    out+='</nav></main></div>'+footer('../')
    write(ROOT/entry['url'],out)
    evidence['pages'].append(entry)

for m in modules:
    own=[e for e in entries if e['module_id']==m['id']]
    out=head(m['name'],'../',m['intro'])+'<body>'+topbar('../')
    out+=hero(m['tag'],m['id']+' / '+m['name'],m['intro'],['3 篇专题','当前源码 + 历史提交','可离线阅读'])
    out+='<div class="wrap">'+aside([('start','学习目标'),('chapters','三篇专题'),('deliver','完成标准')])+'<main id="main">'
    out+=section('start',1,'先建立模型，再走进源码',P(m['prereq'])+flow(m['flow'])+note('建议的阅读节奏','每次完成一篇原理阅读和一个最小实验。读完三个专题后，回到自己的 Blender 改动，寻找同类数据、所有权或依赖问题。'))
    out+=section('chapters',2,'这个方向的三次深入','<div class="lesson-grid module-grid">'+''.join(page_card({**e,'url':Path(e['url']).name}) for e in own)+'</div>')
    criteria='<ul>'+''.join('<li>'+E(d['lab'][-1])+'</li>' for d in m['docs'])+'</ul>'
    out+=section('deliver',3,'用这些成果验收',criteria+note('继续前的自检','选择一个这里研究过的提交，只看提交说明就提出自己的方案，再用 diff 和后续修复校验你的推演。','ok'))
    out+='</main></div>'+footer('../')
    write(ROOT/m['folder']/'index.html',out)

out=head('从读懂源码到独立设计','', '12 个方向，36 篇专题；围绕 Blender 的基础库、几何数据、函数系统与依赖图建立工程能力。')+'<body class="home">'+topbar('')
stats='<div class="hero-stats"><div><b>12</b><span>能力方向</span></div><div><b>36</b><span>专题正文</span></div><div><b>'+str(len(commits))+'</b><span>真实历史提交</span></div><div><b id="progress-count">0 / 36</b><span>已完成课程</span></div></div>'
out+=hero('BLENDER ENGINEERING / A SOURCE-LED CURRICULUM','从读懂源码，走向独立设计','沿着 Jacques、Hans 与其他开发者的真实设计演化，练习数据表示、所有权、求值、依赖和性能判断。',['基于本地仓库','离线优先 · 无外部依赖','先推演 · 再读实现 · 最后验证'],stats)
out+='<div class="wrap">'+aside([('routes','01 如何走这条路线'),('map','02 系统全景'),('catalog','03 十二个学习方向'),('library','04 搜索全部专题'),('method','05 提交阅读方法'),('versions','06 版本与来源')])+'<main id="main">'
routes='<div class="route-grid">'
for name, desc in [('打牢底层','01—04：视图、对象、哈希、分配、类型与数据表示。成果是一组可验证的小型基础组件。'),('把组件组成系统','05—09：几何存储、共享、批量函数、Field 与惰性图。成果是有清楚生命周期的小型求值器。'),('研究复杂边界','10—12：引用分析、闭包、场景依赖和空间查询。成果是一份独立设计与可复核实验报告。')]:
    routes+=f'<article class="route-card"><h3>{E(name)}</h3>{P(desc)}</article>'
routes+='</div>'+note('结合你已有的开发经验','可以先用 05—06 的几何映射与共享缓存建立实际联系，同时补齐 01—03 的基础；随后把 07—09 的函数与执行系统作为主线。进度以实验产出为准。')
out+=section('routes',1,'一条主线，三个阶段',routes)
architecture='<div class="architecture"><div class="arch-row"><b>场景层</b><span>Depsgraph：变化传播、条件与操作调度</span></div><div class="arch-row"><b>节点层</b><span>LazyFunction / GraphExecutor：按需请求输入、组合节点组</span></div><div class="arch-row"><b>表达式层</b><span>Field / FieldContext：表达式在具体几何上下文中解释</span></div><div class="arch-row"><b>批量执行层</b><span>MultiFunction / Procedure：选择上的批量计算与临时值</span></div><div class="arch-row"><b>基础设施</b><span>Span · Vector · CPPType · VArray · IndexMask · SharedCache</span></div></div>'
architecture+=note('三种图，三个问题','场景更新、节点按需求值、Field 表达式计算有不同职责。结构预处理的复用，也不等于把每个节点的结果跨次永久缓存。','warn')
out+=section('map',2,'先知道每一层负责什么',architecture)
catalog='<div class="module-catalog">'
for m in modules:
    catalog+=f'<a class="module-card" href="{quote(m["folder"])}/index.html"><span class="module-number">{m["id"]}</span><div><span class="module-tag">{E(m["tag"])}</span><h3>{E(m["name"])}</h3><p>{E(m["intro"])}</p><span class="module-meta">3 篇专题 · <span data-module-progress="{m["id"]}">0 / 3 已完成</span></span></div><span class="module-arrow" aria-hidden="true">↗</span></a>'
catalog+='</div>'
out+=section('catalog',3,'十二个方向，各自走到可验证的成果',catalog)
library='<div class="search-panel"><label for="course-search">搜索标题、概念、文件或提交</label><input id="course-search" type="search" placeholder="试试 Field、共享缓存、IndexMask、4130f1e674f…" autocomplete="off"><div class="filter-row"><label><input type="checkbox" id="only-unfinished"> 只看未完成</label><span id="search-count" role="status">36 篇专题</span></div></div><div class="lesson-grid" id="lesson-library">'+''.join(page_card(e) for e in entries)+'</div><p id="no-results" hidden>没有匹配专题。试试更短的类名，或清空筛选条件。</p><noscript>搜索和进度需要 JavaScript；所有专题链接始终可直接打开。</noscript>'
out+=section('library',4,'从你的当前问题进入',library)
method='<ol class="reading-method"><li><b>读说明，暂时遮住实现。</b>用自己的话写出触发条件和失败原因。</li><li><b>提出两个候选方案。</b>明确不变量、所有权、依赖以及预期成本。</li><li><b>对照 diff。</b>每个关键改动都应能对应到一个问题或约束。</li><li><b>构造最小反例。</b>测试必须能使旧方案失败，而不是只证明新实现能运行。</li><li><b>测量并复盘。</b>记录硬件、编译选项、输入、误差与仍未覆盖的范围。</li></ol>'
method+=code_block('git show --stat 4130f1e674f\ngit show 4130f1e674f -- source/blender/functions/FN_lazy_function.hh\ngit show 4130f1e674f:source/blender/functions/FN_lazy_function.hh','PowerShell · 在 E:/blender-git/blender 执行')
method+=note('每篇文档的范围','正文按一个完整学习任务组织，通常包含三个推演段落组、两个当前源码窗口、历史提交和独立练习。字数统计为手写正文字符，不含自动摘录、提交原文与导航。阅读时间包含推演，不是严格计时承诺。')
out+=section('method',5,'把一个提交读成一次设计训练',method)
version=P(f'文档生成日期为 {DATE}，仓库 HEAD 为 {head_hash}。源码窗口来自生成时工作区，证据清单记录文件 SHA-256、提交完整哈希和作者。若你继续修改源码，行号和片段可能变化；可重新运行构建脚本刷新摘录。')
version+=P('本仓库是浅仓库：这里使用的提交对象已可读取，但更早父链可能不完整。历史提交中的旧类名和路径不一定存在于当前版本；尤其 2026 年 Field 重构需要与旧资料区分。全部链接、交互与样式可在本地离线使用，外部提交页需要联网。')
version+=P('作者归属以 Git 元数据为准，合作署名和原始项目来源保留在提交原文中。路线中的学习方法与教学模型是为本课程编写的解释，不代表作者本人推荐的课程。源码摘录保留上游代码内容，完整版权与许可见对应仓库文件。')
version+=note('本地进度','完成标记与验收勾选保存在浏览器 localStorage。不同浏览器或不同打开地址的进度可能独立；如浏览器禁止本地存储，将提示进度无法持久保存。', 'ok')
version+='<p>'+link('evidence.json','查看证据清单')+' · '+link('build_course.py','查看构建脚本')+'</p>'
out+=section('versions',6,'知道你正在阅读哪个版本',version)
out+='</main></div>'+footer('')
write(ROOT/'index.html',out)

search=[]
for m in modules:
    for d in m['docs']:
        entry=d['entry'].copy()
        entry['search']=' '.join([m['name'], d['title'], d['lead']] + [s[0] for s in d['sections']] + [s[0] for s in d['sources']] + [c[0] for c in d['commits']]).lower()
        search.append(entry)
write(ROOT/'course-index.js','window.COURSE = '+json.dumps(search,ensure_ascii=False)+';\n')
write(ROOT/'evidence.json',json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'html_pages':len(list(ROOT.rglob('*.html'))),'modules':len(modules),'lessons':len(entries),'commits':len(commits),'source_files':len(evidence['sources']),'authored_characters':sum(e['characters'] for e in entries),'min_chars':min(e['characters'] for e in entries),'max_chars':max(e['characters'] for e in entries)},ensure_ascii=False))
