/* Verify source text round trips, highlighting and wide-screen paragraph layout. */
const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
 const output=process.argv[2];
 const context=await chromium.launchPersistentContext(path.join(output,'course-browser-profile'),{executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await context.newPage();
 const info=JSON.parse(fs.readFileSync(path.join(__dirname,'evidence.json'),'utf8'));
 const results=[];
 for(const width of [1440,1920,2560]){
  await page.setViewportSize({width,height:1080});
  await page.goto(pathToFileURL(path.join(__dirname,info.pages.find(p=>p.id==='01-02').url)).href);
  const result=await page.evaluate(()=>{
   const main=document.querySelector('main').getBoundingClientRect();
   const para=document.querySelector('#model > p').getBoundingClientRect();
   const outer=document.querySelector('.wrap').getBoundingClientRect();
   return {width:innerWidth,mainWidth:main.width,paragraphWidth:para.width,rightGap:outer.right-main.right,highlightedTokens:document.querySelectorAll('.deep-reading [class^="syntax-"]').length,overflow:document.documentElement.scrollWidth>innerWidth};
  });
  if(result.rightGap>2||result.mainWidth-result.paragraphWidth>2||result.overflow||result.highlightedTokens<10)throw Error(JSON.stringify(result));
  results.push(result);
 }
 let root=__dirname;
 while(!fs.existsSync(path.join(root,'source/blender'))){const parent=path.dirname(root);if(parent===root)throw Error('repo not found');root=parent;}
 let units=0, lines=0;
 for(const entry of info.pages){
  await page.goto(pathToFileURL(path.join(__dirname,entry.url)).href);
  const blocks=await page.locator('.deep-reading').evaluateAll(els=>els.map(e=>({lines:[...e.querySelectorAll('.code-line')].map(l=>({number:+l.dataset.line,text:l.textContent})),notes:e.querySelectorAll('.line-explanation').length})));
  const expected=info.deep_readings.filter(u=>u.lesson===entry.id);
  if(blocks.length!==expected.length)throw Error('unit count '+entry.id);
  for(let i=0;i<blocks.length;i++){
   const source=fs.readFileSync(path.join(root,expected[i].path),'utf8').split(/\r?\n/);
   for(const l of blocks[i].lines)if(l.text!==source[l.number-1])throw Error('highlight changed source '+entry.id+' '+l.number);
   if(blocks[i].notes!==expected[i].explained_lines)throw Error('annotation count '+entry.id);
   units++;lines+=blocks[i].notes;
  }
 }
 await page.setViewportSize({width:1920,height:1080});
 await page.goto(pathToFileURL(path.join(__dirname,info.pages.find(p=>p.id==='01-02').url)).href);
 await page.evaluate(()=>{document.documentElement.dataset.theme='light'; document.querySelector('#source').scrollIntoView();});
 await page.screenshot({path:path.join(output,'blender-vector-wide-source.png')});
 await page.locator('.line-explanations').first().scrollIntoViewIfNeeded();
 await page.screenshot({path:path.join(output,'blender-vector-line-explanations.png')});
 const report={wide_layouts:results,verified_complete_units:units,verified_explained_lines:lines,source_roundtrip:'passed'};
 fs.writeFileSync(path.join(__dirname,'reading-validation.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));
 await context.close();
})().catch(e=>{console.error(e);process.exit(1)});
