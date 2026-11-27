// Render design.html to entry.png at exactly 1024x1024 with headless Chrome.
// The PNG is committed to the repository; the grader never runs this file.
// Usage: node render.mjs
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
// puppeteer-core is installed beside this repository (token-radar tools setup).
const require = createRequire(new URL('../token-radar-tools/package.json', import.meta.url));
const puppeteer = require('puppeteer-core');

const chrome = join(
  process.env.HOME,
  'workspace/makefun/token-radar-tools/chrome/linux-157.0.8103.78/chrome-linux64/chrome',
);

const browser = await puppeteer.launch({
  executablePath: chrome,
  headless: 'new',
  args: ['--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1024, height: 1024 });
await page.goto('file://' + join(here, 'design.html'), { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise((r) => setTimeout(r, 400));
await page.screenshot({ path: join(here, 'entry.png'), type: 'png' });
await browser.close();
console.log('rendered entry.png');
