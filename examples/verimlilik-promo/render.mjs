// node render.mjs <outDir> [fps=30] [t0=0] [t1=DUR] [workers=4] [times=virgüllü liste]
// promo.html?render sayfasında her kare için seek(t) çağırır, JPEG ekran görüntüsü alır; sfx.json'u (window.SFX + BEATS) yazar.
import { createRequire } from 'module'; import { execSync } from 'child_process'; import fs from 'fs'; import path from 'path';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const dir = path.dirname(new URL(import.meta.url).pathname);
const [outDir = '_frames', fpsA = '30', t0A = '0', t1A = '', wA = '4', timesA] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ ...(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {}), args: ['--disable-gpu-vsync', '--force-color-profile=srgb'] });
const url = 'file://' + path.join(dir, 'promo.html') + '?render';
const open = async () => { const pg = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  pg.on('pageerror', e => console.log('[err]', e.message)); await pg.goto(url); await pg.evaluate(() => window.ready); return pg; };
const probe = await open(); const DUR = await probe.evaluate(() => window.DUR);
fs.writeFileSync(path.join(dir, 'sfx.json'), JSON.stringify(await probe.evaluate(() => ({ events: window.SFX, beats: window.BEATS, dur: window.DUR }))));
await probe.close();
const fps = +fpsA, t0 = +t0A, t1 = t1A ? +t1A : DUR, workers = +wA;
let jobs;
if (timesA) jobs = timesA.split(',').map(s => ({ t: +s, file: path.join(outDir, `t_${(+s).toFixed(2)}.jpg`) }));
else { jobs = []; for (let n = Math.round(t0 * fps); n < Math.round(t1 * fps); n++) jobs.push({ t: n / fps, file: path.join(outDir, `${String(n).padStart(5, '0')}.jpg`) }); }
const st = Date.now(); let done = 0;
await Promise.all(Array.from({ length: Math.min(workers, jobs.length) }, async (_, w) => {
  const pg = await open();
  for (let i = w; i < jobs.length; i += workers) {
    await pg.evaluate(t => window.seek(t), jobs[i].t);
    await pg.screenshot({ path: jobs[i].file, type: 'jpeg', quality: 92 });
    if (++done % 150 === 0) console.log(done, '/', jobs.length);
  }
}));
await browser.close(); console.log('drew', jobs.length, 'in', ((Date.now() - st) / 1000).toFixed(1), 's');
