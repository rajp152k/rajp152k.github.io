import { test, expect } from '@playwright/test';

const geometry = page => page.locator('.map-dot').evaluateAll(dots =>
  dots.map(dot => [dot.getAttribute('cx'), dot.getAttribute('cy')]));

async function inspectSource(page) {
  const source = await page.locator('.map-reference').first().getAttribute('data-source');
  await page.getByLabel('Inspect', { exact: true }).selectOption(source);
  return source;
}

test.beforeEach(async ({ page }) => {
  await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
});

test('post references connect plotted posts and inspection exposes evidence and cosine scores', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto('/');
  const before = await geometry(page);
  const edges = await page.locator('.map-reference').evaluateAll(lines => lines.map(line => {
    const dot = key => [...document.querySelectorAll('.map-point')]
      .find(point => point.dataset.post === key).querySelector('.map-dot');
    const source = dot(line.dataset.source), target = dot(line.dataset.target);
    return [line.getAttribute('x1') === source.getAttribute('cx'),
      line.getAttribute('y1') === source.getAttribute('cy'),
      line.getAttribute('x2') === target.getAttribute('cx'),
      line.getAttribute('y2') === target.getAttribute('cy')];
  }));
  expect(edges.length).toBeGreaterThan(0);
  expect(edges.every(edge => edge.every(Boolean))).toBe(true);
  const source = await inspectSource(page);
  await expect(page.locator('.map-details')).toBeVisible();
  const active = page.locator('.map-reference.is-active');
  expect(await active.count()).toBeGreaterThan(0);
  expect(await active.evaluateAll((lines, slug) => lines.every(line =>
    [line.dataset.source, line.dataset.target].includes(slug)), source)).toBe(true);
  await expect(page.locator('.map-details .similarity-score')).toHaveCount(3);
  expect(await geometry(page)).toEqual(before);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: 'test-results/lab-inspect-desktop.png' });
  const passage = page.locator('.map-details .passage-link').first();
  const url = await passage.getAttribute('href');
  await passage.click();
  await expect(page).toHaveURL(new RegExp(url.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$'));
  await expect(page.locator(decodeURIComponent(new URL(page.url()).hash))).toBeVisible();
  await expect(page.locator('.post-relations')).toBeVisible();
  await page.screenshot({ path: 'test-results/lab-source-passage.png' });
});

for (const width of [320, 390]) {
  test(`inspection works in a ${width}px viewport with reduced motion`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.setViewportSize({ width, height: 844 });
    await page.goto('/');
    await inspectSource(page);
    await expect(page.locator('.map-details')).toBeVisible();
    expect((await page.locator('.embedding-map').boundingBox()).height).toBeGreaterThan(200);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await expect(page.locator('.map-reference').first()).toHaveCSS('transition-duration', '0s');
    await page.locator('.map-panel').scrollIntoViewIfNeeded();
    await page.screenshot({ path: `test-results/lab-inspect-${width}.png`, fullPage: true });
    await page.getByRole('button', { name: 'Clear inspected post' }).click();
    await expect(page.locator('.map-details')).toBeHidden();
  });
}

test('keyboard escape clears inspection and search restricts the selectable posts', async ({ page }) => {
  await page.goto('/search/?q=autolith');
  await expect(page.locator('tr[data-post]:visible')).not.toHaveCount(0);
  const available = await page.locator('#map-inspect option:not([disabled])').evaluateAll(options =>
    options.map(option => option.value).filter(Boolean));
  const matches = await page.locator('.map-point[href]').evaluateAll(points => points.map(point => point.dataset.post));
  expect([...available].sort()).toEqual([...matches].sort());
  await page.getByLabel('Inspect', { exact: true }).selectOption(available[0]);
  await page.getByLabel('Inspect', { exact: true }).focus();
  await page.keyboard.press('Escape');
  await expect(page.locator('.map-details')).toBeHidden();
  await page.getByLabel('Inspect', { exact: true }).selectOption(available[0]);
  await page.getByRole('searchbox').fill('zzzzmissing');
  await expect(page.locator('.map-point[href]')).toHaveCount(0);
  await expect(page.locator('.map-details')).toBeHidden();
  await expect(page.locator('#map-inspect')).toHaveValue('');
});

test('channel logos load locally and have named YouTube links', async ({ page }) => {
  await page.goto('/');
  for (const [name, handle] of [['Bit-Mage', 'The-Bit-Mage'], ['CognWare', 'CognWare']]) {
    const link = page.getByRole('link', { name: `${name} on YouTube`, exact: true });
    await expect(link).toHaveAttribute('href', `https://www.youtube.com/@${handle}`);
    const image = link.locator('img');
    await expect.poll(() => image.evaluate(img => img.naturalWidth)).toBe(128);
  }
});

test('article source passages and section links work without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
  await page.goto('/logs/2026-10-07-using-autolith/');
  await expect(page.locator('.post-relations')).toBeVisible();
  const anchor = page.locator('.article-content .headerlink').first();
  await anchor.click();
  await expect(page.locator(decodeURIComponent(new URL(page.url()).hash))).toBeVisible();
  await context.close();
});
