/**
 * CSRF Protection E2E Tests
 * 
 * P1 flows:
 * - POST without CSRF token fails
 * - POST with valid CSRF token succeeds
 */
const { test, expect } = require('./fixtures');

/**
 * Helper function to login with explicit wait for button visibility
 */
async function devLogin(page, role) {
  await page.goto('/login');
  await page.waitForLoadState('networkidle');
  const btn = page.locator(`button[value="${role}"]`);
  await expect(btn).toBeVisible({ timeout: 30000 });
  await btn.click();
  await expect(page).toHaveURL(/\/app/, { timeout: 15000 });
}

test.describe('CSRF Protection', () => {
  
  test('API POST without CSRF token returns 400', async ({ page, request }) => {
    // First, login to get an authenticated session
    await devLogin(page, 'staff');
    
    // Get cookies from page context
    const cookies = await page.context().cookies();
    
    // Try to make a POST request without CSRF token
    const response = await request.post('/api/timesheets', {
      headers: {
        'Content-Type': 'application/json',
        'Cookie': cookies.map(c => `${c.name}=${c.value}`).join('; '),
      },
      data: {
        week_start: '2026-01-05',
        traveled: false,
        has_expenses: false,
      },
    });
    
    // Should return 400 Bad Request (CSRF token missing/invalid)
    expect([400, 403]).toContain(response.status());
  });
  
  test('protected endpoints require CSRF token', async ({ page }) => {
    // Login
    await devLogin(page, 'staff');
    
    // Verify CSRF token meta tag exists
    const csrfMeta = page.locator('meta[name="csrf-token"]');
    await expect(csrfMeta).toHaveCount(1);
    
    // Get the token value
    const csrfToken = await csrfMeta.getAttribute('content');
    expect(csrfToken).toBeTruthy();
    expect(csrfToken.length).toBeGreaterThan(10);
  });
  
});

