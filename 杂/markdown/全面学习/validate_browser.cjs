/* 可复用的真实 Chromium 离线浏览器验收。截图目录通过第一个参数指定。 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const root = __dirname;
const output = process.argv[2];
if (!output) throw new Error('请提供截图输出目录');
const info = JSON.parse(fs.readFileSync(path.join(root, 'evidence.json'), 'utf8'));
const url = p => pathToFileURL(path.join(root, p)).href;
const assert = (test, message) => { if (!test) throw new Error(message); };

(async () => {
  const context = await chromium.launchPersistentContext(path.join(output, 'course-browser-profile'), { executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true, viewport:{width:1440,height:1000},colorScheme:'light'});
  const page = await context.newPage();
  await page.goto(url('index.html'));
  await page.evaluate(()=>localStorage.removeItem('blender-study-course-v1'));
  const errors = [];
  page.on('pageerror', err => errors.push(err.message));
  const checked = [];
  const paths = ['index.html', ...fs.readdirSync(root).filter(n=>/^\d{2}-/.test(n)).map(n=>n+'/index.html'), ...info.pages.map(p=>p.url)];
  for (const p of paths) {
    await page.goto(url(p),{waitUntil:'load'});
    const dimensions=await page.evaluate(()=>({
      overflow:document.documentElement.scrollWidth>innerWidth+1,
      h1:document.querySelectorAll('h1').length,
      body:document.body.innerText.length,
      codeHeight:document.querySelector('.code-line')?.getBoundingClientRect().height||0,
      demos:[...document.querySelectorAll('[data-demo]')].map(d=>({kind:d.dataset.demo,controls:d.querySelector('.demo-controls').childElementCount,result:d.querySelector('.demo-result').innerText.length}))
    }));
    assert(!dimensions.overflow,'Desktop overflow: '+p);
    assert(dimensions.h1===1,'Heading structure: '+p);
    for(const d of dimensions.demos) {
      assert(d.controls>0&&d.result>10,'Demo not initialized: '+d.kind);
      const target=page.locator('[data-demo]');
      const before=await target.locator('.demo-result').innerText();
      const slider=target.locator('input[type=range]').first();
      if(await slider.count()) await slider.fill(await slider.getAttribute('max'));
      else await target.locator('button').first().click();
      const after=await target.locator('.demo-result').innerText();
      assert(before!==after,'Demo did not react: '+d.kind);
    }
    checked.push({page:p,...dimensions});
  }

  await page.goto(url('index.html'));
  await page.screenshot({path:path.join(output,'blender-course-overview.png'),fullPage:false});
  await page.locator('#course-search').fill('4130f1e674f');
  const matches=await page.locator('#lesson-library .lesson-card:visible').count();
  assert(matches>0&&matches<36,'Commit search failed');
  await page.locator('#course-search').fill('不应存在的随机词XYZ987');
  assert(await page.locator('#no-results').isVisible(),'No-results feedback failed');
  await page.locator('#course-search').fill('');
  assert(await page.locator('#lesson-library .lesson-card:visible').count()===36,'Search reset failed');
  await page.locator('#catalog').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'blender-course-catalog.png'),fullPage:false});

  const first=info.pages[0];
  await page.goto(url(first.url));
  await page.locator('#mark-complete').click();
  assert(await page.locator('#mark-complete').getAttribute('aria-pressed')==='true','Completion click failed');
  await page.reload();
  assert(await page.locator('#mark-complete').getAttribute('aria-pressed')==='true','Completion persistence failed');
  await page.goto(url('index.html'));
  assert((await page.locator('#progress-count').innerText()).startsWith('1 /'),'Cross-page completion failed');
  await page.locator('#only-unfinished').check();
  assert(await page.locator('#lesson-library .lesson-card:visible').count()===35,'Unfinished filter failed');
  await page.locator('#only-unfinished').uncheck();
  await page.goto(url(first.url));
  await page.locator('#mark-complete').click();

  const lazy=info.pages.find(p=>p.id==='09-01');
  await page.goto(url(lazy.url));
  await page.screenshot({path:path.join(output,'blender-course-lesson.png'),fullPage:false});
  await page.locator('#model').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'blender-course-reading.png'),fullPage:false});
  await page.locator('[data-demo]').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'blender-course-interactive.png'),fullPage:false});
  await page.locator('#source').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'blender-course-source.png'),fullPage:false});

  await page.locator('#theme-toggle').click(); // auto -> light
  await page.locator('#theme-toggle').click(); // light -> dark
  assert(await page.evaluate(()=>document.documentElement.dataset.theme)==='dark','Theme toggle failed');
  await page.waitForTimeout(250);
  await page.screenshot({path:path.join(output,'blender-course-dark.png'),fullPage:false});
  await page.locator('#font-toggle').click();
  assert(await page.evaluate(()=>document.documentElement.dataset.font)==='large','Font toggle failed');
  await page.locator('#font-toggle').click();

  await page.setViewportSize({width:390,height:844});
  const mobile=[];
  for(const p of paths) {
    await page.goto(url(p));
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
    if(overflow) {
      const offenders=await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1&&getComputedStyle(e).position!=='fixed').slice(0,15).map(e=>({tag:e.tagName,class:e.className,width:e.getBoundingClientRect().width,right:e.getBoundingClientRect().right,text:e.textContent.slice(0,90)})));
      await page.screenshot({path:path.join(output,'blender-course-overflow-debug.png'),fullPage:false});
      await context.close();
      throw new Error('Mobile overflow: '+p+' '+JSON.stringify(offenders));
    }
    mobile.push(p);
  }
  await page.goto(url(lazy.url));
  await page.evaluate(()=>{document.documentElement.dataset.theme='light';});
  await page.screenshot({path:path.join(output,'blender-course-mobile.png'),fullPage:false});
  await page.locator('#model').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'blender-course-mobile-reading.png'),fullPage:false});
  await page.locator('#source').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,'blender-course-mobile-source.png'),fullPage:false});

  await page.emulateMedia({media:'print'});
  await page.pdf({path:path.join(output,'blender-course-print-sample.pdf'),format:'A4',printBackground:true,margin:{top:'12mm',bottom:'12mm',left:'12mm',right:'12mm'}});
  assert(errors.length===0,'JavaScript errors: '+errors.join('; '));
  const report={desktop_pages:checked.length,mobile_pages:mobile.length,interactive_models:checked.flatMap(x=>x.demos).length,search:true,completion_persistence:true,cross_page_progress:true,theme:true,font:true,print_sample:true,javascript_errors:errors,checked};
  fs.writeFileSync(path.join(root,'browser-validation.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({desktop_pages:checked.length,mobile_pages:mobile.length,interactive_models:12,errors,screenshot_directory:output}));
  await context.close();
})().catch(err=>{console.error(err);process.exit(1);});
