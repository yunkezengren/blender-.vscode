/* 无外部依赖：离线导航、主题、学习进度、代码复制与十二个教学模型。 */
(() => {
  'use strict';
  const KEY = 'blender-study-course-v1';
  let state = { done: {}, checks: {}, theme: 'auto', font: 'normal' };
  let storageOK = true;
  try { state = { ...state, ...JSON.parse(localStorage.getItem(KEY) || '{}') }; }
  catch { storageOK = false; }
  const toast = message => {
    const el = document.querySelector('#toast');
    if (!el) return;
    el.textContent = message;
    el.classList.add('show');
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => el.classList.remove('show'), 3500);
  };
  const save = () => {
    try { localStorage.setItem(KEY, JSON.stringify(state)); }
    catch { storageOK = false; toast('浏览器禁止本地存储：这次操作无法持久保存。'); }
  };
  const setAppearance = () => {
    document.documentElement.dataset.theme = state.theme;
    document.documentElement.dataset.font = state.font;
    document.querySelector('#font-toggle')?.setAttribute('aria-pressed', String(state.font === 'large'));
    const themeButton = document.querySelector('#theme-toggle');
    if (themeButton) {
      themeButton.textContent = { auto: '跟随系统', light: '浅色', dark: '深色' }[state.theme] || '跟随系统';
      themeButton.setAttribute('aria-label', '当前'+themeButton.textContent+'，点击切换配色');
    }
  };
  setAppearance();
  document.querySelector('#theme-toggle')?.addEventListener('click', () => {
    const modes = ['auto', 'light', 'dark'];
    state.theme = modes[(modes.indexOf(state.theme) + 1) % modes.length];
    setAppearance(); save();
  });
  document.querySelector('#font-toggle')?.addEventListener('click', () => {
    state.font = state.font === 'large' ? 'normal' : 'large';
    setAppearance(); save();
  });
  document.querySelector('#print-page')?.addEventListener('click', () => window.print());

  const entries = window.COURSE || [];
  const refreshProgress = () => {
    const count = entries.filter(e => state.done[e.id]).length;
    const counter = document.querySelector('#progress-count');
    if (counter) counter.textContent = `${count} / ${entries.length}`;
    document.querySelectorAll('[data-course-id]').forEach(el => {
      const done = !!state.done[el.dataset.courseId];
      el.classList.toggle('done', done);
      el.querySelector('.completion-label').textContent = done ? '✓ 已完成' : '待学习';
    });
    document.querySelectorAll('[data-module-progress]').forEach(el => {
      const n = entries.filter(e => e.module_id === el.dataset.moduleProgress && state.done[e.id]).length;
      el.textContent = `${n} / 3 已完成`;
    });
    const button = document.querySelector('#mark-complete');
    if (button) {
      const done = !!state.done[button.dataset.id];
      button.textContent = done ? '✓ 已完成 · 点击撤销' : '标记本篇完成';
      button.setAttribute('aria-pressed', String(done));
    }
  };
  refreshProgress();
  document.querySelector('#mark-complete')?.addEventListener('click', event => {
    const id = event.currentTarget.dataset.id;
    state.done[id] = !state.done[id];
    save(); refreshProgress();
    if (storageOK) toast(state.done[id] ? '已记录本篇完成。' : '已撤销完成标记。');
  });
  document.querySelectorAll('[data-check]').forEach(input => {
    input.checked = !!state.checks[input.dataset.check];
    input.addEventListener('change', () => { state.checks[input.dataset.check] = input.checked; save(); });
  });
  if (!storageOK) toast('当前浏览器不允许本地进度存储，正文和交互仍可使用。');

  const search = document.querySelector('#course-search');
  const filter = () => {
    if (!search) return;
    const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    const unfinished = document.querySelector('#only-unfinished').checked;
    let count = 0;
    document.querySelectorAll('#lesson-library [data-course-id]').forEach(card => {
      const item = entries.find(e => e.id === card.dataset.courseId);
      const match = !!item && terms.every(t => item.search.includes(t)) && !(unfinished && state.done[item.id]);
      card.hidden = !match;
      if (match) count++;
    });
    document.querySelector('#search-count').textContent = `${count} / ${entries.length} 篇专题`;
    document.querySelector('#no-results').hidden = count !== 0;
  };
  search?.addEventListener('input', filter);
  document.querySelector('#only-unfinished')?.addEventListener('change', filter);
  window.addEventListener('storage', event => {
    if (event.key !== KEY) return;
    try { state = { ...state, ...JSON.parse(event.newValue || '{}') }; refreshProgress(); filter(); setAppearance(); }
    catch { /* 保留当前有效状态。 */ }
  });
  document.querySelectorAll('.copy-code').forEach(button => {
    button.addEventListener('click', async () => {
      const code = [...button.closest('.code').querySelectorAll('.code-line')].map(e => e.textContent).join('\n');
      try {
        if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(code);
        else {
          const area = document.createElement('textarea');
          area.value = code;
          area.style.position = 'fixed'; area.style.opacity = '0';
          document.body.append(area); area.select();
          const ok = document.execCommand('copy'); area.remove();
          if (!ok) throw new Error('copy denied');
        }
        toast('已复制代码，不包含行号。');
      } catch { toast('浏览器未允许复制，请直接选择代码文本。'); }
    });
  });
  if ('IntersectionObserver' in window) {
    const links = [...document.querySelectorAll('nav.toc a[href^="#"]')];
    const observer = new IntersectionObserver(items => {
      const visible = items.filter(e => e.isIntersecting).sort((a,b) => a.boundingClientRect.top-b.boundingClientRect.top);
      if (!visible.length) return;
      links.forEach(a => a.classList.toggle('active', a.hash === '#'+visible[0].target.id));
    }, { rootMargin: '-10% 0px -65% 0px', threshold: 0 });
    document.querySelectorAll('main > section').forEach(s => observer.observe(s));
  }

  // 下列模型用于推演语义；不是 Blender 的实际求值器或性能测量。
  const cells = (n, active, label = i => String(i)) => '<div class="cells">'+Array.from({length:n},(_,i)=>`<span class="cell ${active(i)?'on':''}">${label(i)}</span>`).join('')+'</div>';
  const paragraph = text => `<p>${text}</p>`;
  const slider = (controls, label, min, max, value, update) => {
    const wrap = document.createElement('label');
    const text = document.createElement('span'); text.textContent = label;
    const input = document.createElement('input'); input.type='range'; input.min=min; input.max=max; input.value=value;
    input.setAttribute('aria-label',label);
    const output = document.createElement('output'); output.textContent=value;
    wrap.append(text,input,output); controls.append(wrap);
    input.addEventListener('input',()=>{output.textContent=input.value;update(Number(input.value));});
    return input;
  };
  const button = (controls, label, action) => {
    const b=document.createElement('button'); b.type='button'; b.textContent=label; b.addEventListener('click',action); controls.append(b); return b;
  };
  document.querySelectorAll('[data-demo]').forEach(demo => {
    const controls=demo.querySelector('.demo-controls');
    const result=demo.querySelector('.demo-result');
    const kind=demo.dataset.demo;
    if(kind==='vector') {
      const update=n=>{
        const capacity=n<=4?4:n<=8?8:16;
        result.innerHTML=`<strong>size = ${n} · capacity = ${capacity} · ${n<=4?'内嵌':'堆上'}存储</strong>`+cells(capacity,i=>i<n,i=>i<n?'T':'·')+paragraph('蓝色表示存活对象，灰色表示尚未构造的容量。跨过 4、8 时教学模型会迁移存储；旧视图需要重新取得。');
      };
      slider(controls,'元素数量',0,12,3,update); update(3);
    } else if(kind==='hash') {
      let removed=false;
      const update=()=>{result.innerHTML='<strong>教学线性探测 · A、B、C 的起始槽均为 2</strong>'+cells(8,i=>i>=2&&i<=4,i=>i===2?(removed?'删':'A'):i===3?'B':i===4?'C':'空')+paragraph(removed?'查找 C：槽 2 是 Removed，继续；槽 3 不相等；槽 4 找到。若错误地把槽 2 当成 Empty，查找会提前结束。':'先在槽 2、3、4 放入碰撞的 A、B、C。删除 A 后仍要保留继续探测的信息。');};
      button(controls,'删除 / 恢复 A',()=>{removed=!removed;update();}); update();
    } else if(kind==='allocator') {
      const update=p=>{const aligned=Math.ceil(p/8)*8;result.innerHTML=`<strong>cursor = ${p} · alignment = 8</strong>`+paragraph(`向上对齐到 ${aligned}，填充 ${aligned-p} 字节；分配 5 字节后游标为 ${aligned+5}。`)+cells(32,i=>i>=aligned&&i<aligned+5,i=>i>=p&&i<aligned?'垫':String(i))+paragraph('此模型只演示小整数地址与对齐，不处理真实地址空间、溢出或新缓冲块。');};
      slider(controls,'当前游标',0,23,9,update); update(9);
    } else if(kind==='mask') {
      const update=n=>{result.innerHTML=`<strong>逻辑长度 24 · 选中前 ${n} 个索引</strong>`+cells(24,i=>i<n)+paragraph(`单值数组只需保存一个值及长度。当前选择是连续范围 [0, ${n})；普通 int64 索引列表的元素载荷为 ${n*8} 字节。真实 IndexMask 还有段元数据与范围复用，不能用此数直接估算完整对象大小。`);};
      slider(controls,'选择数量',0,24,8,update);update(8);
    } else if(kind==='offsets') {
      const offsets=[0,3,7,10];
      const update=i=>{result.innerHTML='<strong>offsets = [0, 3, 7, 10]</strong>'+cells(10,j=>j>=offsets[i]&&j<offsets[i+1])+paragraph(`面 ${i} 的范围是 [${offsets[i]}, ${offsets[i+1]})，包含 ${offsets[i+1]-offsets[i]} 个角点。这里的编号是角点索引，不是顶点索引。`);};
      slider(controls,'选择面',0,2,1,update);update(1);
    } else if(kind==='sharing') {
      let detached=false;
      const update=()=>{result.innerHTML=detached?'<strong>A → 缓冲 X [1,2,3]　B → 缓冲 Y [9,2,3]</strong>'+paragraph('B 先分离再修改。A 的源数据与兼容缓存仍然有效；B 的相关派生缓存需要失效。'):'<strong>A ─┐<br>B ─┴→ 共享缓冲 X [1,2,3]</strong>'+paragraph('两个强用户，只读共享。复制描述对象没有立即复制整个数据数组。');};
      button(controls,'让 B 修改首元素',()=>{detached=true;update();});button(controls,'重置共享',()=>{detached=false;update();});update();
    } else if(kind==='batch') {
      const update=n=>{const calls=n===0?0:1;result.innerHTML=`<strong>处理 ${n} 个元素</strong>`+paragraph(`标量接口可需要 ${n} 次调用；教学批量接口使用 ${calls} 次调用，内部仍需要处理 ${n} 个元素。`)+cells(n,()=>true,i=>String(i+2))+paragraph('调用次数减少不等于固定倍数加速；准备成本、循环优化和工作量共同决定结果。这里不计时，也不模拟真实线程数。');};
      slider(controls,'元素数量',0,24,12,update);update(12);
    } else if(kind==='field') {
      let alternate=false,scale=2;
      const update=()=>{const p=alternate?[10,20,30]:[0,1,2];result.innerHTML=`<strong>表达式：Position × ${scale} + 1</strong>`+paragraph(`上下文位置：[${p.join(', ')}]`)+paragraph(`求值结果：[${p.map(x=>x*scale+1).join(', ')}]`)+paragraph('表达式描述不绑定这次具体数组；上下文改变了 Position 的解释。');};
      slider(controls,'Scale',0,5,2,n=>{scale=n;update();});button(controls,'切换上下文',()=>{alternate=!alternate;update();});update();
    } else if(kind==='lazy') {
      let step=0,cond=true;
      const update=()=>{const branch=cond?'A':'B';const lines=['输出被请求，条件尚未到达。','请求 condition，并把控制权交回执行器。',`条件为 ${cond}，只请求分支 ${branch}。`,`${branch} 到达，发布输出；另一分支执行次数为 0。`];result.innerHTML=`<strong>阶段 ${step}/3 · 选择 ${branch}</strong>`+cells(4,i=>i<=step,i=>String(i))+paragraph(lines[step]);};
      button(controls,'推进一步',()=>{step=Math.min(3,step+1);update();});button(controls,'切换条件并重置',()=>{cond=!cond;step=0;update();});button(controls,'重置',()=>{step=0;update();});update();
    } else if(kind==='closure') {
      let source=2,captured=2,x=3;
      const update=()=>{result.innerHTML=`<strong>源 scale = ${source} · 捕获快照 = ${captured}</strong>`+paragraph(`closure(${x}) = ${captured*x}`)+paragraph('该教学模型按值捕获。改变源变量不会改变已有闭包；重新创建闭包才捕获新值。真实系统还要考虑共享数据和执行图的所有权。');};
      slider(controls,'源 scale',1,8,2,n=>{source=n;update();});button(controls,'重新捕获',()=>{captured=source;update();});slider(controls,'调用参数 x',1,8,3,n=>{x=n;update();});update();
    } else if(kind==='deps') {
      let disabled=false;
      const update=()=>{result.innerHTML='<strong>Condition → Enabled；Geometry → Modifier → Result</strong>'+paragraph(disabled?'修改器禁用：仍更新 Condition / Enabled，以获得本次条件；在无其他消费者的教学前提下，昂贵 Modifier 工作可跳过。':'修改器启用：条件确认后，需要满足 Geometry 依赖，Modifier 才能执行。')+paragraph('“已脏”“依赖已满足”“本次被需要”是不同状态。该模型假定没有其他消费者需要 Geometry。');};
      button(controls,'切换修改器启用状态',()=>{disabled=!disabled;update();});update();
    } else if(kind==='kdtree') {
      const update=q=>{const lo=6,hi=9,best=2;const bound=Math.max(lo-q,0,q-hi);const prune=bound>best;result.innerHTML=`<strong>一维区域 [6,9] · 查询 q=${q} · 当前最佳距离=2</strong>`+cells(12,i=>i>=lo&&i<=hi,i=>i===q?'Q':String(i))+paragraph(`区域距离下界 = ${bound}，平方下界 = ${bound*bound}；${prune?'大于当前最佳平方距离 4，可以剪枝。':'不大于当前最佳平方距离 4，保留该区域继续检查。'}`)+paragraph('相等时这里保留候选以支持边界情况；真实查询的包含语义由其接口决定。');};
      slider(controls,'查询位置',0,11,2,update);update(2);
    }
  });
})();
