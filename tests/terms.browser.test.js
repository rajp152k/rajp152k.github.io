import { test, expect } from '@playwright/test';

const article = '/logs/2026-11-06-orchestrating-autolith/';

test.beforeEach(async ({ page }) => {
  // These checks exercise local assets, not the external mathematics CDN.
  await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
});

test('desktop references open without navigation and return keyboard focus', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(article);
  const panel = page.locator('#terms-panel');
  await expect(panel).toBeVisible();
  await expect(panel.getByRole('heading', { name: 'Terms and references' })).toBeVisible();
  const orch = page.locator('.term-reference[data-term="orch"]');
  await orch.focus();
  await orch.press('Enter');
  await expect(panel.getByRole('heading', { name: 'Orch', exact: true })).toBeFocused();
  await expect(orch).toHaveAttribute('aria-expanded', 'true');
  await expect(panel.getByText(/coordinating agent/i).first()).toBeVisible();
  expect(new URL(page.url()).pathname).toBe(article);
  await page.screenshot({ path: 'test-results/terms-desktop.png', fullPage: false });
  await panel.getByRole('heading', { name: 'Orch', exact: true }).press('Escape');
  await expect(panel).toBeHidden();
  await expect(orch).toBeFocused();
  await expect(orch).toHaveAttribute('aria-expanded', 'false');
});

test('panel list and term pages provide an archive route', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(article);
  const panel = page.locator('#terms-panel');
  await panel.getByRole('button', { name: 'Orch', exact: true }).click();
  await panel.getByRole('heading', { name: 'Orch', exact: true }).press('Escape');
  await expect(panel).toBeHidden();
  const toggle = page.getByRole('button', { name: 'Terms and references', exact: true });
  await expect(toggle).toBeFocused();
  await toggle.click();
  await panel.getByRole('button', { name: 'Terms in this post' }).click();
  await expect(panel.getByRole('button', { name: 'Orch', exact: true })).toBeVisible();
  await panel.getByRole('button', { name: 'Autolith', exact: true }).click();
  await panel.getByRole('link', { name: 'Full reference' }).click();
  await expect(page).toHaveURL(/\/terms\/autolith\/$/);
  await expect(page.getByRole('heading', { name: 'Autolith', exact: true })).toBeVisible();
  await expect(page.locator('.term-sources a').first()).toBeVisible();
});

test('small desktop uses a closed panel until requested', async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto(article);
  await expect(page.locator('#terms-panel')).toBeHidden();
  await page.getByRole('button', { name: 'Terms and references', exact: true }).click();
  await expect(page.locator('#terms-panel')).toBeVisible();
  await page.locator('#terms-panel').getByRole('button', { name: 'Close references' }).click();
  await expect(page.locator('#terms-panel')).toBeHidden();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});

test('phone references are inert and resizing removes desktop controls', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(article);
  await page.locator('.term-reference[data-term="orch"]').click();
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(page.locator('#terms-panel')).toBeHidden();
  await expect(page.locator('[data-terms-toggle]')).toBeHidden();
  await expect(page.locator('.term-reference[role], .term-reference[tabindex]')).toHaveCount(0);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: 'test-results/terms-phone.png', fullPage: false });
  await page.locator('.term-reference[data-term="orch"]').click();
  await expect(page.locator('#terms-panel')).toBeHidden();
});

test('without JavaScript the article is readable and desktop term pages work', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  await page.goto(`http://127.0.0.1:8766${article}`);
  await expect(page.locator('.article-content')).toBeVisible();
  await expect(page.locator('.term-reference[role], .term-reference[tabindex]')).toHaveCount(0);
  await expect(page.locator('#terms-panel')).toBeHidden();
  await expect(page.locator('[data-terms-toggle]')).toBeHidden();
  await page.locator('.terms-navigation a').click();
  await expect(page.getByRole('heading', { name: 'Terms and references', exact: true })).toBeVisible();
  await context.close();
});
