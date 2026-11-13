import { test, expect } from '@playwright/test';

const geometry = page => page.locator('.map-dot').evaluateAll(dots =>
  dots.map(dot => [dot.getAttribute('cx'), dot.getAttribute('cy')]));

async function choosePost(page, key) {
  await page.locator(`.map-point[data-post="${key}"] .map-dot`).click();
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
  await page.getByText('References and similarity', { exact: true }).click();
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
  const available = await page.locator('.map-point[href]').evaluateAll(points => points.map(point => point.dataset.post));
  expect(available.length).toBeGreaterThan(0);
  await choosePost(page, available[0]);
  await page.locator('.map-details h3 a').focus();
  await page.keyboard.press('Escape');
  await expect(page.locator('.map-details')).toBeHidden();
  await choosePost(page, available[0]);
  await page.getByRole('searchbox').fill('zzzzmissing');
  await expect(page.locator('.map-point[href]')).toHaveCount(0);
  await expect(page.locator('.map-details')).toBeHidden();
  await expect(page.locator('.map-inspector')).toBeHidden();
});

test('clicking circles updates a persistent card and the heading opens the post', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto('/');
  const points = page.locator('.map-point');
  const first = points.first();
  const second = points.last();
  await first.locator('.map-dot').click();
  await expect(page).toHaveURL(/\/$/);
  await expect(first).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('.map-details h3 a')).toHaveText(await first.getAttribute('data-title'));
  await expect(page.locator('.map-detail-meta time')).toHaveText(await first.getAttribute('data-display-date'));
  expect(await page.locator('.map-detail-excerpt').textContent()).not.toBe('');
  await page.getByRole('searchbox').hover();
  await expect(page.locator('.map-details')).toBeVisible();
  await second.locator('.map-dot').click();
  await expect(first).toHaveAttribute('aria-expanded', 'false');
  await expect(second).toHaveAttribute('aria-expanded', 'true');
  const heading = page.locator('.map-details h3 a');
  await expect(heading).toHaveText(await second.getAttribute('data-title'));
  const url = await second.getAttribute('data-url');
  await page.screenshot({ path: 'test-results/point-inspect-desktop.png' });
  await heading.click();
  await expect(page).toHaveURL(new URL(url, page.url()).href);
});

test('phone clicks select each circle despite overlapping hit areas and ignore context circles', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 844 });
  await page.goto('/');
  for (const point of await page.locator('.map-point').all()) {
    const dot = await point.locator('.map-dot').boundingBox();
    await page.mouse.click(dot.x + dot.width / 2, dot.y + dot.height / 2);
    await expect(page.locator('.map-details h3 a')).toHaveText(await point.getAttribute('data-title'));
  }
  await page.goto('/logs/');
  const context = await page.locator('.map-point.is-context .map-dot').first().boundingBox();
  await page.mouse.click(context.x + context.width / 2, context.y + context.height / 2);
  await expect(page.locator('.map-inspector')).toBeHidden();
});

test('keyboard selection focuses the title, Escape returns to the point, and Space selects', async ({ page }) => {
  await page.goto('/');
  const point = page.locator('.map-point').first();
  await point.focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('.map-details h3 a')).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.locator('.map-inspector')).toBeHidden();
  await expect(point).toBeFocused();
  await page.keyboard.press('Space');
  await expect(page.locator('.map-details h3 a')).toBeFocused();
  const url = await point.getAttribute('data-url');
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(new URL(url, page.url()).href);
});

for (const width of [320, 1440]) {
  test(`tap a circle to inspect, then tap its title to read at ${width}px`, async ({ browser }) => {
    const context = await browser.newContext({ viewport: { width, height: 1000 }, hasTouch: true });
    const page = await context.newPage();
    await page.goto('/');
    const point = page.locator('.map-point').first();
    const url = await point.getAttribute('data-url');
    await point.locator('.map-dot').tap();
    const card = page.locator('.map-inspector');
    await expect(card).toBeVisible();
    const bounds = await card.boundingBox();
    const map = await page.locator('.embedding-map').boundingBox();
    expect(bounds.y).toBeGreaterThanOrEqual(map.y + map.height);
    expect(bounds.x).toBeGreaterThanOrEqual(0);
    expect(bounds.x + bounds.width).toBeLessThanOrEqual(width);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: `test-results/point-inspect-touch-${width}.png`, fullPage: true });
    await page.locator('.map-details h3 a').tap();
    await expect(page).toHaveURL(new URL(url, page.url()).href);
    await context.close();
  });
}

test('map circles open posts directly without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
  await page.goto('/');
  const point = page.locator('.map-point').first();
  const url = await point.getAttribute('href');
  await point.locator('.map-dot').click();
  await expect(page).toHaveURL(new URL(url, page.url()).href);
  await context.close();
});

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
