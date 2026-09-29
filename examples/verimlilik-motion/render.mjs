// node render.mjs <outDir> [fps=30] [t0=0] [t1=DUR] [workers=2] [times=comma list]
// Kareleri anim.html'in window.draw({t}) fonksiyonundan JPEG olarak yazar; ayrıca sfx.json'u (window.SFX) üretir.
// Tarayıcı: global playwright. Farklı bir Chromium için CHROMIUM=/yol/chrome.
import { createRequire } from 'module';
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const dir = path.dirname(new URL(import.meta.url).pathname);
const [outDir = '_frames', fpsA = '30', t0A = '0', t1A, wA = '2', timesA] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const url = 'file://' + path.join(dir, 'anim.html') + '?render';
const probe = await browser.newPage(); await probe.goto(url); await probe.evaluate(() => window.ready);
const DUR = await probe.evaluate(() => window.DUR);
fs.writeFileSync(path.join(dir, 'sfx.json'), JSON.stringify(await probe.evaluate(() => window.SFX)));
await probe.close();
const fps = +fpsA, t0 = +t0A, t1 = t1A ? +t1A : DUR, workers = +wA;
let jobs;
if (timesA) jobs = timesA.split(',').map(s => ({ t: +s, file: path.join(outDir, `t_${(+s).toFixed(2)}.jpg`) }));
else { jobs = []; const n0 = Math.round(t0 * fps), n1 = Math.round(t1 * fps);
  for (let n = n0; n < n1; n++) jobs.push({ t: n / fps, file: path.join(outDir, `${String(n).padStart(5, '0')}.jpg`) }); }
const t = Date.now();
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('[err]', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('[console]', m.text()); });
  await page.goto(url); await page.evaluate(() => window.ready);
  for (let i = w; i < jobs.length; i += workers) {
    const b64 = await page.evaluate(j => window.draw(j), jobs[i]);
    fs.writeFileSync(jobs[i].file, Buffer.from(b64, 'base64'));
  }
}));
await browser.close();
console.log('drew', jobs.length, 'in', ((Date.now() - t) / 1000).toFixed(1), 's');
