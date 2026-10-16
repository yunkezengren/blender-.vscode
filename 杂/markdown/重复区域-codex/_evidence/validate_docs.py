"""Check documentation structure, local links, original source and examples syntax."""
from pathlib import Path
import ast
import hashlib
import json
import re
from datetime import datetime, timezone, timedelta

OUT=Path(__file__).resolve().parents[1]
ROOT=next(p for p in OUT.parents if (p/'source/blender/nodes').is_dir())


def main():
    issues=[]
    excerpt_data=json.loads((OUT/'_evidence/source-excerpts.json').read_text(encoding='utf-8'))
    records=excerpt_data['excerpts']
    docs=list(OUT.rglob('*.md'))
    stats=[]
    link_count=0
    mermaid_count=0
    source_lines=0
    for document in docs:
        text=document.read_text(encoding='utf-8')
        fences=re.findall(r'^```.*$',text,re.M)
        if len(fences)%2:
            issues.append(f'Unclosed fence: {document}')
        mermaid_count+=len(re.findall(r'^```mermaid$',text,re.M))
        prose=re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M|re.S)
        if '\ufffd' in prose:
            issues.append(f'Replacement character in prose: {document}')
        if '\r' in text:
            issues.append(f'Unexpected carriage return: {document}')
        for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',prose):
            url=url.strip().strip('<>')
            if re.match(r'^[a-zA-Z]+:',url) or url.startswith('#'):
                continue
            url=url.split('#')[0]
            link_count+=1
            if not (document.parent/url).exists():
                issues.append(f'Broken local link: {document.relative_to(OUT)} -> {url}')
        if re.match(r'^\d\d-',document.name) and document.name != 'README.md':
            total=len(text.splitlines())
            non_code=len([s for s in prose.splitlines() if s.strip()])
            if total < 1000:
                issues.append(f'Chapter below 1000 lines: {document.name} ({total})')
            stats.append({'path':document.relative_to(OUT).as_posix(),'lines':total,
                          'nonblank_noncode_lines':non_code,'characters':len(text)})
    if len(stats)!=14:
        issues.append(f'Expected 14 main chapters, found {len(stats)}')
    for record in records:
        source=(ROOT/record['path']).read_bytes()
        if hashlib.sha256(source).hexdigest()!=record['sha256']:
            issues.append(f'Source hash drift: {record["path"]}')
        expected='\n'.join(source.decode('utf-8').splitlines()[record['start']-1:record['end']])
        marker=f'<!-- source:{record["key"]}:{record["start"]}:{record["end"]} -->'
        text=(OUT/record['document']).read_text(encoding='utf-8')
        pattern=re.escape(marker)+r'\n\n```[^\n]*\n(.*?)\n```'
        matches=re.findall(pattern,text,re.S)
        if matches!=[expected]:
            issues.append(f'Source excerpt mismatch: {record["document"]} / {marker}')
        source_lines+=record['end']-record['start']+1
    scripts=list(OUT.rglob('*.py'))
    for path in scripts:
        try:
            ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
        except SyntaxError as exc:
            issues.append(str(exc))
    result={'time_asia_shanghai':datetime.now(timezone(timedelta(hours=8))).isoformat(),
            'passed':not issues,'main_chapters':len(stats),'markdown_files':len(docs),
            'main_total_lines':sum(s['lines'] for s in stats),
            'main_nonblank_noncode_lines':sum(s['nonblank_noncode_lines'] for s in stats),
            'source_excerpt_lines_including_reuse':source_lines,
            'unique_source_files':len({r['path'] for r in records}),
            'source_excerpts':len(records),'local_links_checked':link_count,
            'mermaid_blocks':mermaid_count,'mermaid_rendered':False,
            'python_syntax_checked':len(scripts),'chapters':sorted(stats,key=lambda s:Path(s['path']).name),
            'issues':issues}
    (OUT/'_evidence/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('chapters',)},ensure_ascii=False,indent=2))
    if issues:
        raise SystemExit(1)


if __name__=='__main__':
    main()
