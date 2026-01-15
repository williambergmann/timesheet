/**
 * Shared fixtures and utilities for E2E tests
 */
const playwrightTest = require('@playwright/test');

/**
 * Test credentials for dev login
 */
const TEST_USERS = {
  trainee: { username: 'trainee', password: 'trainee', role: 'trainee' },
  support: { username: 'support', password: 'support', role: 'support' },
  staff: { username: 'staff', password: 'staff', role: 'staff' },
  admin: { username: 'admin', password: 'password', role: 'admin' },
};

/**
 * Custom test fixture that provides authenticated page contexts
 */
const test = playwrightTest.test.extend({
  /**
   * Login as a specific user role
   */
  authenticatedPage: async ({ page, request }, use) => {
    // Helper function to login
    const login = async (role) => {
      const user = TEST_USERS[role];
      if (!user) {
        throw new Error(`Unknown role: ${role}`);
      }
      
      // Navigate to login page
      await page.goto('/login');
      
      // Wait for page to load
      await page.waitForLoadState('networkidle');
      
      // Click the dev login button for the role
      const buttonSelector = `button[name="username"][value="${user.username}"], input[name="username"][value="${user.username}"]`;
      const button = page.locator(`form[action="/auth/dev-login"] button:has-text("${role}")`, { timeout: 5000 });
      
      // If button click approach doesn't work, fill the form directly
      try {
        await button.first().click({ timeout: 3000 });
      } catch {
        // Fallback: Submit form directly
        await page.fill('input[name="username"]', user.username);
        await page.fill('input[name="password"]', user.password);
        await page.click('button[type="submit"]');
      }
      
      // Wait for redirect to dashboard
      await page.waitForURL('**/app**', { timeout: 10000 });
      
      return page;
    };
    
    // Expose login helper
    page.login = login;
    
    await use(page);
  },
  
  /**
   * Pre-authenticated as a staff user
   */
  staffPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.waitForLoadState('networkidle');
    
    // Click Staff login button - wait for it to be visible first
    const staffBtn = page.locator('button[value="staff"]');
    await playwrightTest.expect(staffBtn).toBeVisible({ timeout: 30000 });
    await staffBtn.click();
    await page.waitForURL('**/app**', { timeout: 10000 });
    
    await use(page);
  },
  
  /**
   * Pre-authenticated as an admin user
   */
  adminPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.waitForLoadState('networkidle');
    
    // Click Admin login button - wait for it to be visible first
    const adminBtn = page.locator('button[value="admin"]');
    await playwrightTest.expect(adminBtn).toBeVisible({ timeout: 30000 });
    await adminBtn.click();
    await page.waitForURL('**/app**', { timeout: 10000 });
    
    await use(page);
  },
});

/**
 * Helper to get the current week's Sunday (week start)
 */
function getCurrentWeekStart() {
  const today = new Date();
  const dayOfWeek = today.getDay(); // 0 = Sunday
  const sunday = new Date(today);
  sunday.setDate(today.getDate() - dayOfWeek);
  return sunday.toISOString().split('T')[0];
}

/**
 * Format date as MM/DD/YYYY
 */
function formatDate(date) {
  const d = new Date(date);
  return `${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getDate().toString().padStart(2, '0')}/${d.getFullYear()}`;
}

module.exports = {
  test,
  expect: playwrightTest.expect,
  TEST_USERS,
  getCurrentWeekStart,
  formatDate,
};
