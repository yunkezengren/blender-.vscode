"""Capture reproducible semantic and installed-Blender evidence."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json
import shutil
import subprocess
import sys

OUT=Path(__file__).resolve().parents[1]


def write(name, data):
    (OUT/'_evidence'/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')


def main():
    model=subprocess.run([sys.executable,str(OUT/'示例/reference_models.py')],capture_output=True,text=True,encoding='utf-8',check=True)
    write('reference-models.json',json.loads(model.stdout))
    executable=shutil.which('blender')
    if not executable:
        raise RuntimeError('No Blender executable found; do not report integration as passed')
    command=[executable,'--background','--factory-startup','--python-exit-code','1',
             '--python',str(OUT/'示例/build_repeat_demo.py')]
    run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
    prefix='RZ_DEMO_RESULT '
    results=[json.loads(line[len(prefix):]) for line in run.stdout.splitlines() if line.startswith(prefix)]
    passed=run.returncode==0 and len(results)==1 and len(results[0])==4
    version=next((line for line in run.stdout.splitlines() if line.startswith('Blender ')), 'unknown')
    write('blender-demo.json',{'time_asia_shanghai':datetime.now(timezone(timedelta(hours=8))).isoformat(),
                            'scope':'installed Blender affine Repeat node example; not a build of the documented checkout',
                            'executable':executable,'version':version,'command':command,
                            'exit_code':run.returncode,'passed':passed,'observations':results,
                            'stdout':run.stdout,'stderr':run.stderr})
    if not passed:
        raise RuntimeError(run.stdout+'\n'+run.stderr)
    print(json.dumps({'reference_checks':json.loads(model.stdout)['passed'],'blender_cases':len(results[0]),
                      'version':version,'passed':True},ensure_ascii=False))


if __name__=='__main__':
    main()
