// node capture.mjs <kaynak.html> → ui/*.png  (gerçek ekrandan 2x çözünürlükte parça görüntüleri)
import { createRequire } from 'module'; import { execSync } from 'child_process'; import path from 'path'; import fs from 'fs';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const dir = path.dirname(new URL(import.meta.url).pathname), out = path.join(dir, 'ui'); fs.mkdirSync(out, { recursive: true });
const src = path.resolve(process.argv[2] || 'Verimlilik_ve_Karlilik.html');
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await p.goto('file://' + src); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
// animasyon/geçişleri kapat, odak halkası olmasın
await p.addStyleTag({ content: '*{transition:none!important;animation:none!important;caret-color:transparent!important}' });
const shot = async (sel, name, i = 0) => { const el = p.locator(sel).nth(i); await el.screenshot({ path: path.join(out, name + '.png'), animations: 'disabled' }); };
const full = async name => { await p.locator('.app').screenshot({ path: path.join(out, name + '.png') }); };
await full('genel'); await shot('.top', 'topbar'); await shot('.hero', 'hero');
for (let i = 0; i < 5; i++) await shot('.hero .tile', 'tile' + i, i);
await shot('.ccard', 'card0', 0); await shot('.ccard', 'card1', 1);
await shot('.ccard .signal', 'signal0', 0); await shot('.ccard .signal', 'signal1', 1);
await shot('aside.side .panel', 'bulten', 0); await shot('aside.side .panel', 'nabiz', 1);
await p.click('.ccard a.btn'); await p.waitForTimeout(500);
for (const [tab, name, parts] of [['ozet', 'ozet', [['.kunye', 'kunye'], ['.kpis', 'kpis'], ['.wallet', 'wallet'], ['.htab', 'hareket']]],
  ['karlilik', 'karlilik', [['.card.wf', 'waterfall'], ['.eq', 'denklem'], ['.card.tcard', 'urun-tablo']]],
  ['taahhut', 'taahhut', [['.sum4', 'tsum'], ['.sum4 .dk', 'tring'], ['.card.tcard', 'ttablo']]]]) {
  await p.click(`[data-tab=${tab}]`); await p.waitForTimeout(500); await p.evaluate(() => scrollTo(0, 0)); await full(name);
  for (const [sel, n] of parts) await shot(sel, n);
}
await b.close(); console.log('ok', fs.readdirSync(out).length, 'görüntü');
