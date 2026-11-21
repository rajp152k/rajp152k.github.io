import { test, expect } from '@playwright/test';

const article = '/logs/2026-11-06-orchestrating-autolith/';

test.beforeEach(async ({ page }) => {
  await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
});

for (const width of [320, 390, 768, 1024, 1440]) {
  test(`boxed pages fit a ${width}px viewport`, async ({ page }) => {
    await page.setViewportSize({ width, height: 844 });
    for (const path of ['/', '/search/?q=autolith', '/terms/', '/terms/simplified-technical-english/', '/embeddings/', article]) {
      await page.goto(path);
      await page.evaluate(() => document.fonts.ready);
      await expect(page.locator('.site-header')).toBeVisible();
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), path).toBe(true);
      const search = page.getByRole('searchbox');
      await expect(search).toBeVisible();
      expect((await search.boundingBox()).width, path).toBeGreaterThan(70);
      if (path === '/' && [390, 1440].includes(width)) {
        await page.screenshot({ path: `test-results/deck-index-${width}.png` });
      }
      if (path === '/terms/' && width === 1440) {
        await page.screenshot({ path: 'test-results/deck-terms.png' });
      }
      if (path === article && width === 1440) {
        const main = await page.locator('.article-content').boundingBox();
        const panel = await page.locator('#terms-panel').boundingBox();
        expect(main.x + main.width).toBeLessThanOrEqual(panel.x);
      }
    }
  });
}

test('short viewports allow scrolling in the archive and reference panel', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 400 });
  await page.goto('/');
  const archive = page.locator('.archive-scroll');
  await archive.hover();
  await page.mouse.wheel(0, 300);
  await expect.poll(() => archive.evaluate(element => element.scrollTop)).toBeGreaterThan(0);

  await page.goto(article);
  const panel = page.locator('#terms-panel');
  await panel.getByRole('button', { name: 'HMAS', exact: true }).click();
  await panel.hover();
  await page.mouse.wheel(0, 400);
  await expect.poll(() => panel.evaluate(element => element.scrollTop)).toBeGreaterThan(0);
  await expect(panel.getByRole('button', { name: 'Close references' })).toBeInViewport();
  await page.screenshot({ path: 'test-results/deck-scroll.png' });
  await panel.getByRole('button', { name: 'Close references' }).click();
  await expect(panel).toBeHidden();
});
