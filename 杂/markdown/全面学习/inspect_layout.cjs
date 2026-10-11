const {chromium}=require('playwright');
const path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
  const context=await chromium.launchPersistentContext(path.join(process.argv[2],'course-browser-profile'),{executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,viewport:{width:390,height:844}});
  const page=await context.newPage();
  await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  const result=await page.evaluate(()=>({width:innerWidth,root:document.documentElement.scrollWidth,body:document.body.scrollWidth,offenders:[...document.querySelectorAll('*')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>({tag:e.tagName,cls:e.className,id:e.id,w:e.clientWidth,s:e.scrollWidth,overflow:getComputedStyle(e).overflow,rect:e.getBoundingClientRect().toJSON(),text:e.textContent.slice(0,65)})).slice(0,30)}));
  console.log(JSON.stringify(result,null,2));
  await context.close();
})();
