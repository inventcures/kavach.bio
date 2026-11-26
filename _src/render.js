const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const root='/home/claude/site';
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.svg':'image/svg+xml','.pdf':'application/pdf'};
const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';const f=path.join(root,p);
 if(!fs.existsSync(f)){r.writeHead(404);return r.end('404')}r.writeHead(200,{'content-type':types[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r)}).listen(8765);
(async()=>{const b=await chromium.launch();const pg=await b.newPage();
 const docs=[['white-paper','india-respirator-stockpile-white-paper-v0.1.pdf','A Respiratory Protection Stockpile for India · Draft v0.1'],['fit-panel-protocol','india-respirator-fit-panel-protocol-v0.1.pdf','India Respirator Fit Panel · Draft protocol v0.1']];
 for(const [d,pdf,label] of docs){await pg.goto(`http://localhost:8765/${d}/`,{waitUntil:'networkidle'});await pg.emulateMedia({media:'print'});
  await pg.pdf({path:`${root}/${d}/${pdf}`,format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
   footerTemplate:`<div style="font:8px system-ui,sans-serif;color:#666;width:100%;padding:0 16mm;display:flex;justify-content:space-between"><span>${label} · kavach.bio/${d}/</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
   margin:{top:'16mm',bottom:'18mm',left:'16mm',right:'16mm'}});await pg.emulateMedia({media:'screen'});}
 const shots=process.env.SHOTS==='1';
 for(const [u,n,w] of [['/','home',1280],['/','home-m',390],['/white-paper/','wp',1280],['/white-paper/','wp-m',390],['/fit-panel-protocol/','fp',1280],['/fit-panel-protocol/','fp-m',390]]){
  await pg.setViewportSize({width:w,height:900});await pg.goto('http://localhost:8765'+u);await pg.screenshot({path:`/tmp/claude-0/-home-claude/f30bba9a-dfb7-56d9-aadf-183e7462a896/scratchpad/${n}.png`});
  const sw=await pg.evaluate(()=>document.documentElement.scrollWidth);console.log(n,'scrollWidth',sw)}
 // link check
 for(const u of ['/','/white-paper/','/fit-panel-protocol/']){await pg.goto('http://localhost:8765'+u);const hrefs=await pg.$$eval('a[href]',a=>a.map(x=>x.getAttribute('href')));
  for(const h of hrefs){if(h.startsWith('#')){const ok=await pg.$(`[id="${h.slice(1)}"]`);if(!ok)console.log('BROKEN anchor',u,h)}else if(!/^https?:/.test(h)){const full=new URL(h,'http://localhost:8765'+u).pathname;let f=path.join(root,full.endsWith('/')?full+'index.html':full);if(!fs.existsSync(f))console.log('BROKEN',u,h)}}}
 await b.close();srv.close()})();
