import { test, expect } from '@playwright/test';

const geometry = page => page.locator('.map-dot').evaluateAll(dots =>
  dots.map(dot => [dot.getAttribute('cx'), dot.getAttribute('cy'), getComputedStyle(dot).transform]));

for (const reducedMotion of ['no-preference', 'reduce']) {
  for (const width of [1440, 390]) {
    test(`local feedback and panel entry at ${width}px, motion ${reducedMotion}`, async ({ browser }) => {
      const context = await browser.newContext({ viewport: { width, height: 1000 }, reducedMotion, hasTouch: width === 390 });
      const page = await context.newPage();
      await page.goto('/');
      const before = await geometry(page);
      const point = page.locator('.map-point').first();
      const dot = point.locator('.map-dot');
      if (width === 390) await dot.tap();
      else await dot.click();
      await expect(point).toHaveAttribute('aria-expanded', 'true');
      const inspector = page.locator('.map-inspector');
      await expect(inspector).toBeVisible();
      await expect(inspector).toHaveCSS('animation-name', reducedMotion === 'reduce' ? 'none' : 'panel-entry');
      await expect(inspector).toHaveCSS('animation-duration', reducedMotion === 'reduce' ? '0s' : '0.18s');
      await expect(page.locator('.map-reference').first()).toHaveCSS('transition-duration', reducedMotion === 'reduce' ? '0s' : '0.1s, 0.1s');
      expect(await geometry(page)).toEqual(before);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: `test-results/motion-inspect-${width}-${reducedMotion}.png`, fullPage: true, animations: 'disabled' });
      await context.close();
    });
  }

  test(`term panel entry and focus with motion ${reducedMotion}`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion });
    await page.setViewportSize({ width: 1024, height: 900 });
    await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
    await page.goto('/logs/2026-11-06-orchestrating-autolith/');
    const reference = page.locator('.term-reference[data-term="hmas"]').first();
    await reference.focus();
    await reference.press('Enter');
    const panel = page.locator('#terms-panel');
    await expect(panel).toBeVisible();
    await expect(panel).toHaveCSS('animation-name', reducedMotion === 'reduce' ? 'none' : 'panel-entry');
    await expect(panel).toHaveCSS('animation-duration', reducedMotion === 'reduce' ? '0s' : '0.18s');
    await expect(panel.locator('h3')).toBeFocused();
    await page.screenshot({ path: `test-results/motion-terms-${reducedMotion}.png`, animations: 'disabled' });
    await panel.locator('h3').press('Escape');
    await expect(panel).toBeHidden();
    await expect(reference).toBeFocused();
  });
}

test('hover and keyboard preview show direct references without replacing Inspect selection', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto('/');
  const before = await geometry(page);
  const previewKey = await page.locator('.map-reference').first().getAttribute('data-source');
  const preview = page.locator(`.map-point[data-post="${previewKey}"]`);
  const selected = page.locator(`.map-point:not([data-post="${previewKey}"])`).first();
  // Send a real click at the dot center. Adjacent SVG hit areas can overlap.
  const bounds = await selected.locator('.map-dot').boundingBox();
  await page.mouse.click(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2);
  const selectedTitle = await selected.getAttribute('data-title');
  const previewSlug = await preview.getAttribute('data-post');
  const previewTitle = await preview.getAttribute('data-title');
  await preview.locator('.map-dot').hover();
  await expect(page.locator('.map-readout-title')).toHaveText(previewTitle);
  await expect(page.locator('.map-readout-title')).toHaveCSS('color', 'rgb(255, 255, 255)');
  await expect(page.locator('.map-details h3 a')).toHaveText(selectedTitle);
  await expect(selected).toHaveAttribute('aria-expanded', 'true');
  const highlighted = await page.locator('.map-reference.is-active').evaluateAll(edges => edges.map(edge => [edge.dataset.source, edge.dataset.target]));
  const incident = await page.locator('.map-reference').evaluateAll((edges, slug) => edges.filter(edge => [edge.dataset.source, edge.dataset.target].includes(slug)).map(edge => [edge.dataset.source, edge.dataset.target]), previewSlug);
  expect(highlighted).toEqual(incident);
  expect(incident.length).toBeGreaterThan(0);
  await page.screenshot({ path: 'test-results/motion-hover-desktop.png', animations: 'disabled' });
  await page.getByRole('searchbox').hover();
  await expect(page.locator('.map-readout-title')).toHaveText(selectedTitle);
  await preview.focus();
  // Use real keyboard navigation to enter :focus-visible mode after mouse input.
  await page.keyboard.press('Tab');
  await page.keyboard.press('Shift+Tab');
  await expect(preview).toBeFocused();
  await expect(page.locator('.map-readout-title')).toHaveText(previewTitle);
  await expect(page.locator('.map-details h3 a')).toHaveText(selectedTitle);
  expect(await geometry(page)).toEqual(before);
  await page.keyboard.press('Escape');
  await expect(page.locator('.map-inspector')).toBeHidden();
  await expect(preview).toBeFocused();
  await preview.press('Enter');
  await expect(page.locator('.map-details h3 a')).toHaveText(previewTitle);
  await expect(page.locator('.map-details h3 a')).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.locator('.map-inspector')).toBeHidden();
  await expect(preview).toBeFocused();
});
