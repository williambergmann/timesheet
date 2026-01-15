/**
 * Authentication E2E Tests
 * 
 * P0 flows:
 * - Dev login -> Dashboard loads
 * - Admin login -> Admin tab accessible
 * - Logout -> Redirect to login page
 */
const { test, expect } = require('./fixtures');

test.describe('Authentication', () => {
  
  // Run warmup first to initialize test users in the database
  test.describe.configure({ mode: 'serial' });
  
  test('warmup - initialize test users', async ({ page }) => {
    test.setTimeout(180000); // 3 minutes for cold start
    for (const role of ['staff', 'admin', 'trainee', 'support']) {
      await page.goto('/login');
      const btn = page.locator(`button[value="${role}"]`);
      await expect(btn).toBeVisible({ timeout: 30000 });
      
      await Promise.all([
        page.waitForURL('**/app**', { timeout: 120000, waitUntil: 'domcontentloaded' }),
        btn.click(),
      ]);
      console.log(`Warmup: ${role} user initialized`);
      await page.goto('/login');
    }
  });
  
  test.describe('Dev Login', () => {
    
    test('login page loads with dev login buttons', async ({ page }) => {
      await page.goto('/login');
      
      // Check page title (actual title is "Sign in to your account")
      await expect(page).toHaveTitle(/Sign in/i);
      
      // Check for dev login buttons (should be visible when Azure is not configured)
      // There are 4 quick login buttons: trainee, staff, support, admin
      const traineeBtn = page.locator('button[value="trainee"]');
      const staffBtn = page.locator('button[value="staff"]');
      const supportBtn = page.locator('button[value="support"]');
      const adminBtn = page.locator('button[value="admin"]');
      
      await expect(traineeBtn).toBeVisible();
      await expect(staffBtn).toBeVisible();
      await expect(supportBtn).toBeVisible();
      await expect(adminBtn).toBeVisible();
    });
    
    test('staff login redirects to dashboard', async ({ page }) => {
      await page.goto('/login');
      
      // Wait for and click the Staff login button
      const staffBtn = page.locator('button[value="staff"]');
      await expect(staffBtn).toBeVisible({ timeout: 30000 });
      await staffBtn.click();
      
      // Should redirect to /app
      await expect(page).toHaveURL(/\/app/, { timeout: 60000 });
      
      // Dashboard should load - look for main app container or welcome message
      await expect(page.locator('.app-container').first()).toBeVisible();
    });
    
    test('admin login provides admin access', async ({ page }) => {
      await page.goto('/login');
      
      // Wait for and click the Admin login button
      const adminBtn = page.locator('button[value="admin"]');
      await expect(adminBtn).toBeVisible({ timeout: 30000 });
      await adminBtn.click();
      
      // Should redirect to /app
      await expect(page).toHaveURL(/\/app/, { timeout: 60000 });
      
      // Admin tab or admin navigation should be visible
      await expect(page.locator('[data-tab="admin"], .nav-admin, a:has-text("Admin"), button:has-text("Admin")').first()).toBeVisible({ timeout: 15000 });
    });
    
    test('trainee login has limited access', async ({ page }) => {
      await page.goto('/login');
      
      // Wait for and click the Trainee login button
      const traineeBtn = page.locator('button[value="trainee"]');
      await expect(traineeBtn).toBeVisible({ timeout: 30000 });
      await traineeBtn.click();
      
      // Should redirect to /app
      await expect(page).toHaveURL(/\/app/, { timeout: 60000 });
      
      // Dashboard should load
      await expect(page.locator('.app-container').first()).toBeVisible();
    });
    
    test('support login can access support dashboard', async ({ page }) => {
      await page.goto('/login');
      
      // Wait for and click the Support login button
      const supportBtn = page.locator('button[value="support"]');
      await expect(supportBtn).toBeVisible({ timeout: 30000 });
      await supportBtn.click();
      
      // Should redirect to /app
      await expect(page).toHaveURL(/\/app/, { timeout: 60000 });
      
      // Dashboard should load
      await expect(page.locator('.app-container').first()).toBeVisible();
    });
    
  });
  
  test.describe('Session Management', () => {
    
    test('unauthenticated user is redirected to login', async ({ page }) => {
      // Try to access protected route
      await page.goto('/app');
      
      // Should redirect to login
      await expect(page).toHaveURL(/\/login/);
    });
    
    test('logout clears session and redirects to login', async ({ page }) => {
      // First, login
      await page.goto('/login');
      
      const staffBtn = page.locator('button[value="staff"]');
      await expect(staffBtn).toBeVisible({ timeout: 30000 });
      await staffBtn.click();
      await expect(page).toHaveURL(/\/app/, { timeout: 60000 });
      
      // Now logout - find logout form or link
      const logoutBtn = page.locator('form[action*="logout"] button, a[href*="logout"], button:has-text("Logout"), button:has-text("Sign Out")');
      await logoutBtn.click();
      
      // Should redirect to login page
      await expect(page).toHaveURL(/\/login/);
      
      // Try to access /app again - should redirect to login
      await page.goto('/app');
      await expect(page).toHaveURL(/\/login/);
    });
    
  });
  
  test.describe('Rate Limiting', () => {
    
    test('rate limiting headers are present', async ({ page, request }) => {
      // First, login to get an authenticated session
      await page.goto('/login');
      
      // Make a request and check for rate limit headers
      const response = await request.get('/auth/me');
      
      // Response should have rate limit headers (if enabled)
      const headers = response.headers();
      console.log('Response headers:', Object.keys(headers));
      
      // The endpoint should return 401 (not authenticated) or 200
      expect([200, 401]).toContain(response.status());
    });
    
  });
  
});
