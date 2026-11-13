import { test, expect } from '@playwright/test';

const geometry = page => page.locator('.map-dot').evaluateAll(dots =>
  dots.map(dot => [dot.getAttribute('cx'), dot.getAttribute('cy')]));

async function choosePost(page, key) {
  await page.getByRole('combobox', { name: /^Inspect/ }).click();
  const id = await page.locator('#map-inspect-options [role="option"]').evaluateAll((options, value) =>
    options.find(option => option.dataset.value === value)?.id, key);
  await page.locator(`#${id}`).click();
}

async function inspectSource(page) {
  const source = await page.locator('.map-reference').first().getAttribute('data-source');
  await choosePost(page, source);
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
  const available = await page.locator('#map-inspect-options [role="option"]:not([aria-disabled="true"])').evaluateAll(options =>
    options.map(option => option.dataset.value));
  const matches = await page.locator('.map-point[href]').evaluateAll(points => points.map(point => point.dataset.post));
  expect([...available].sort()).toEqual([...matches].sort());
  await choosePost(page, available[0]);
  await page.getByRole('combobox', { name: /^Inspect/ }).focus();
  await page.keyboard.press('Escape');
  await expect(page.locator('.map-details')).toBeHidden();
  await choosePost(page, available[0]);
  await page.getByRole('searchbox').fill('zzzzmissing');
  await expect(page.locator('.map-point[href]')).toHaveCount(0);
  await expect(page.locator('.map-details')).toBeHidden();
  await expect(page.locator('#map-inspect-value')).toHaveText('Choose a post');
});

test('themed picker supports keyboard navigation, typeahead and dismissal', async ({ page }) => {
  await page.goto('/');
  const picker = page.getByRole('combobox', { name: /^Inspect/ });
  const list = page.getByRole('listbox', { name: 'Inspect', exact: true });
  await picker.focus();
  await page.keyboard.press('ArrowDown');
  await expect(list).toBeVisible();
  await expect(picker).toBeFocused();
  await page.keyboard.press('End');
  const last = page.getByRole('option').last();
  await expect(picker).toHaveAttribute('aria-activedescendant', await last.getAttribute('id'));
  await page.keyboard.press('Home');
  const first = page.getByRole('option').first();
  await expect(picker).toHaveAttribute('aria-activedescendant', await first.getAttribute('id'));
  await page.keyboard.press('ArrowDown');
  await expect(picker).toHaveAttribute('aria-activedescendant', await page.getByRole('option').nth(1).getAttribute('id'));
  await page.keyboard.type('lisp');
  const match = page.getByRole('option', { name: /the lisp machine/ });
  await expect(picker).toHaveAttribute('aria-activedescendant', await match.getAttribute('id'));
  await page.keyboard.press('Enter');
  await expect(list).toBeHidden();
  await expect(page.locator('.map-details')).toBeVisible();
  await picker.click();
  await page.keyboard.press('Escape');
  await expect(list).toBeHidden();
  await expect(page.locator('.map-details')).toBeVisible();
  await picker.click();
  await page.getByRole('searchbox').click();
  await expect(list).toBeHidden();
  await picker.focus();
  await page.keyboard.press('Space');
  await expect(list).toBeVisible();
  await page.keyboard.press('Tab');
  await expect(list).toBeHidden();
  await expect(page.getByRole('button', { name: 'Clear inspected post' })).toBeFocused();
});

for (const width of [320, 1440]) {
  test(`themed picker opens within the panel at ${width}px and supports touch`, async ({ browser }) => {
    const context = await browser.newContext({ viewport: { width, height: 1000 }, hasTouch: true });
    const page = await context.newPage();
    await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
    await page.goto('/');
    await page.getByRole('combobox', { name: /^Inspect/ }).tap();
    const list = page.getByRole('listbox');
    await expect(list).toBeVisible();
    const menu = await list.boundingBox();
    const panel = await page.locator('.map-panel').boundingBox();
    expect(menu.x).toBeGreaterThanOrEqual(panel.x);
    expect(menu.y).toBeGreaterThanOrEqual(panel.y);
    expect(menu.x + menu.width).toBeLessThanOrEqual(panel.x + panel.width);
    expect(menu.y + menu.height).toBeLessThanOrEqual(panel.y + panel.height);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: `test-results/themed-inspect-${width}.png`, fullPage: true });
    await page.getByRole('option').first().tap();
    await expect(list).toBeHidden();
    await expect(page.locator('.map-details')).toBeVisible();
    await context.close();
  });
}

test('channel logos load locally and have named YouTube links', async ({ page }) => {
  await page.goto('/');
  for (const [name, handle] of [['Bit-Mage', 'The-Bit-Mage'], ['CognWare', 'CognWare']]) {
    const link = page.getByRole('link', { name: `${name} on YouTube`, exact: true });
    await expect(link).toHaveAttribute('href', `https://www.youtube.com/@${handle}`);
    const image = link.locator('img');
    await expect.poll(() => image.evaluate(img => img.naturalWidth)).toBe(128);
    const alpha = await image.evaluate(img => {
      const canvas = document.createElement('canvas');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const context = canvas.getContext('2d');
      context.drawImage(img, 0, 0);
      const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
      return [...pixels].filter((value, index) => index % 4 === 3);
    });
    expect(alpha[0]).toBe(0);
    expect(alpha.some(value => value > 0 && value < 255)).toBe(true);
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
