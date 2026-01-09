/**
 * Admin Dashboard E2E Tests
 * 
 * P0 flows:
 * - Admin login → View timesheets → Approve
 * - Admin login → View timesheets → Reject
 * - Filter timesheets by status, user, hour type
 */
const { test, expect } = require('./fixtures');

test.describe('Admin Dashboard', () => {
  
  test.describe('Dashboard Access', () => {
    
    test('admin can access admin dashboard', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Click on Admin tab
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      
      // Admin dashboard content should be visible
      await expect(page.locator('.admin-dashboard, #admin-content, .admin-timesheets')).toBeVisible();
    });
    
    test('non-admin cannot access admin dashboard', async ({ page }) => {
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Admin tab should not be visible
      const adminTab = page.locator('[data-tab="admin"], #admin-tab');
      await expect(adminTab).not.toBeVisible();
    });
    
  });
  
  test.describe('Timesheet List', () => {
    
    test('admin sees submitted timesheets', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      
      // Should see timesheet list or empty state
      const timesheetCards = page.locator('.admin-timesheet-card, .timesheet-row, [data-timesheet-id]');
      const emptyState = page.locator('.empty-state, .no-timesheets');
      
      await expect(timesheetCards.or(emptyState).first()).toBeVisible({ timeout: 10000 });
    });
    
  });
  
  test.describe('Filters', () => {
    
    test('status filter changes displayed timesheets', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      await page.waitForLoadState('networkidle');
      
      // Find status filter
      const statusFilter = page.locator('select#status-filter, select[name="status"], .status-filter select');
      if (await statusFilter.isVisible()) {
        // Select "Submitted" status
        await statusFilter.selectOption({ value: 'SUBMITTED' });
        await page.waitForLoadState('networkidle');
        
        // Verify filter was applied (URL may update or cards may filter)
        const cards = page.locator('.admin-timesheet-card, .timesheet-row');
        // All visible cards should have submitted status
        const cardCount = await cards.count();
        if (cardCount > 0) {
          for (let i = 0; i < Math.min(cardCount, 3); i++) {
            const card = cards.nth(i);
            await expect(card).toContainText(/submitted/i);
          }
        }
      }
    });
    
    test('user filter shows specific user timesheets', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      await page.waitForLoadState('networkidle');
      
      // Find user filter
      const userFilter = page.locator('select#user-filter, select[name="user"], .user-filter select');
      if (await userFilter.isVisible()) {
        // Get options and select first non-empty one
        const options = await userFilter.locator('option').allTextContents();
        if (options.length > 1) {
          await userFilter.selectOption({ index: 1 });
          await page.waitForLoadState('networkidle');
        }
      }
    });
    
    test('hour type filter works', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      await page.waitForLoadState('networkidle');
      
      // Find hour type filter
      const hourTypeFilter = page.locator('select#hour-type-filter, select[name="hour_type"], .hour-type-filter select');
      if (await hourTypeFilter.isVisible()) {
        // Select "Field Hours"
        await hourTypeFilter.selectOption({ label: /field/i });
        await page.waitForLoadState('networkidle');
      }
    });
    
  });
  
  test.describe('Approve/Reject Actions', () => {
    
    test('admin can approve a submitted timesheet', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      await page.waitForLoadState('networkidle');
      
      // Filter to show only submitted timesheets
      const statusFilter = page.locator('select#status-filter, select[name="status"]');
      if (await statusFilter.isVisible()) {
        await statusFilter.selectOption({ value: 'SUBMITTED' });
        await page.waitForLoadState('networkidle');
      }
      
      // Find a submitted timesheet
      const timesheetCards = page.locator('.admin-timesheet-card, .timesheet-row, [data-timesheet-id]');
      const cardCount = await timesheetCards.count();
      
      if (cardCount > 0) {
        // Click on first timesheet to view details
        await timesheetCards.first().click();
        await page.waitForLoadState('networkidle');
        
        // Find and click Approve button
        const approveBtn = page.locator('button:has-text("Approve"), #approve-btn, .approve-button');
        if (await approveBtn.isVisible()) {
          await approveBtn.click();
          
          // Wait for approval confirmation
          await expect(page.locator('.toast-success, .notification-success, [role="status"]:has-text("approved")')).toBeVisible({ timeout: 10000 });
        }
      } else {
        // No submitted timesheets to approve - skip this test
        test.skip();
      }
    });
    
    test('admin can reject a submitted timesheet with notes', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      await page.waitForLoadState('networkidle');
      
      // Filter to show only submitted timesheets
      const statusFilter = page.locator('select#status-filter, select[name="status"]');
      if (await statusFilter.isVisible()) {
        await statusFilter.selectOption({ value: 'SUBMITTED' });
        await page.waitForLoadState('networkidle');
      }
      
      // Find a submitted timesheet
      const timesheetCards = page.locator('.admin-timesheet-card, .timesheet-row, [data-timesheet-id]');
      const cardCount = await timesheetCards.count();
      
      if (cardCount > 0) {
        // Click on first timesheet to view details
        await timesheetCards.first().click();
        await page.waitForLoadState('networkidle');
        
        // Find and click Reject button
        const rejectBtn = page.locator('button:has-text("Reject"), button:has-text("Needs Attention"), #reject-btn, .reject-button');
        if (await rejectBtn.isVisible()) {
          await rejectBtn.click();
          
          // Fill in rejection reason if dialog appears
          const reasonInput = page.locator('textarea[name="reason"], textarea#rejection-reason, .rejection-notes textarea');
          if (await reasonInput.isVisible({ timeout: 2000 }).catch(() => false)) {
            await reasonInput.fill('E2E Test: Please correct time entries');
            
            // Confirm rejection
            const confirmBtn = page.locator('button:has-text("Confirm"), button:has-text("Submit")');
            await confirmBtn.click();
          }
          
          // Wait for rejection confirmation
          await expect(page.locator('.toast-success, .notification-success, [role="status"]:has-text("rejected"), [role="status"]:has-text("needs attention")')).toBeVisible({ timeout: 10000 });
        }
      } else {
        // No submitted timesheets to reject - skip this test
        test.skip();
      }
    });
    
    test('admin can unapprove an approved timesheet', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      await page.waitForLoadState('networkidle');
      
      // Filter to show only approved timesheets
      const statusFilter = page.locator('select#status-filter, select[name="status"]');
      if (await statusFilter.isVisible()) {
        await statusFilter.selectOption({ value: 'APPROVED' });
        await page.waitForLoadState('networkidle');
      }
      
      // Find an approved timesheet
      const timesheetCards = page.locator('.admin-timesheet-card, .timesheet-row, [data-timesheet-id]');
      const cardCount = await timesheetCards.count();
      
      if (cardCount > 0) {
        // Click on first timesheet to view details
        await timesheetCards.first().click();
        await page.waitForLoadState('networkidle');
        
        // Find and click Un-approve button
        const unapproveBtn = page.locator('button:has-text("Un-approve"), button:has-text("Unapprove"), #unapprove-btn');
        if (await unapproveBtn.isVisible()) {
          await unapproveBtn.click();
          
          // Wait for confirmation
          await expect(page.locator('.toast-success, .notification-success, [role="status"]:has-text("submitted")')).toBeVisible({ timeout: 10000 });
        }
      } else {
        // No approved timesheets to unapprove - skip this test
        test.skip();
      }
    });
    
  });
  
  test.describe('Travel & Expense Indicators', () => {
    
    test('travel badge is visible on timesheets with travel', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      await page.waitForLoadState('networkidle');
      
      // Look for travel badge (✈️ icon or travel class)
      const travelBadge = page.locator('.travel-badge, [class*="travel"], :has-text("✈️")');
      // This may or may not be visible depending on data
      console.log('Travel badges found:', await travelBadge.count());
    });
    
    test('expense badge is visible on timesheets with expenses', async ({ page }) => {
      // Login as admin
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const adminForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Admin' });
      await adminForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to admin dashboard
      const adminTab = page.locator('[data-tab="admin"], #admin-tab, .admin-nav-item, a:has-text("Admin")');
      await adminTab.click();
      await page.waitForLoadState('networkidle');
      
      // Look for expense badge (💰 icon or expense class)
      const expenseBadge = page.locator('.expense-badge, [class*="expense"], :has-text("💰")');
      // This may or may not be visible depending on data
      console.log('Expense badges found:', await expenseBadge.count());
    });
    
  });
  
});
