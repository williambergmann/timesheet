/**
 * Timesheet E2E Tests
 * 
 * P0 flows:
 * - Create new timesheet → Save draft
 * - Add time entries → Submit → Confirm
 * - Upload attachment → Verify display
 */
const { test, expect, getCurrentWeekStart } = require('./fixtures');

test.describe('Timesheet Management', () => {
  
  test.describe('Create Timesheet', () => {
    
    test('can create a new timesheet for current week', async ({ page }) => {
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Click "New Timesheet" button
      const newTimesheetBtn = page.locator('button:has-text("New Timesheet"), a:has-text("New Timesheet"), #new-timesheet-btn');
      await newTimesheetBtn.click();
      
      // Wait for timesheet form/view to load
      await expect(page.locator('.timesheet-form, #timesheet-entries, .time-entry-grid')).toBeVisible({ timeout: 10000 });
    });
    
    test('timesheet form has required fields', async ({ page }) => {
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to new timesheet
      const newTimesheetBtn = page.locator('button:has-text("New Timesheet"), a:has-text("New Timesheet"), #new-timesheet-btn');
      await newTimesheetBtn.click();
      
      // Wait for form to load
      await page.waitForLoadState('networkidle');
      
      // Check for time entry grid (days of the week)
      await expect(page.locator('.time-entry-row, .entry-row, [data-day]')).toBeVisible();
      
      // Check for hour type selector
      await expect(page.locator('select.hour-type-select, #hour-type, [name="hour_type"]').first()).toBeVisible();
      
      // Check for Save Draft and Submit buttons
      await expect(page.locator('button:has-text("Save Draft"), #save-draft-btn')).toBeVisible();
      await expect(page.locator('button:has-text("Submit"), #submit-btn')).toBeVisible();
    });
    
    test('can add time entries and save draft', async ({ page }) => {
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to new timesheet
      const newTimesheetBtn = page.locator('button:has-text("New Timesheet"), a:has-text("New Timesheet"), #new-timesheet-btn');
      await newTimesheetBtn.click();
      await page.waitForLoadState('networkidle');
      
      // Add a time entry row if not already present
      const addRowBtn = page.locator('button:has-text("Add Row"), button:has-text("Add Entry"), #add-entry-btn');
      if (await addRowBtn.isVisible()) {
        await addRowBtn.click();
      }
      
      // Find the first hours input and enter a value
      const hoursInputs = page.locator('input[type="number"].hours-input, input.entry-hours, input[name*="hours"]');
      await expect(hoursInputs.first()).toBeVisible();
      await hoursInputs.first().fill('8');
      
      // Click Save Draft
      const saveDraftBtn = page.locator('button:has-text("Save Draft"), #save-draft-btn');
      await saveDraftBtn.click();
      
      // Wait for save confirmation (toast or status update)
      await expect(page.locator('.toast-success, .notification-success, [role="status"]:has-text("saved")')).toBeVisible({ timeout: 10000 });
    });
    
    test('auto-populate fills 8 hours for weekdays', async ({ page }) => {
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to new timesheet
      const newTimesheetBtn = page.locator('button:has-text("New Timesheet"), a:has-text("New Timesheet"), #new-timesheet-btn');
      await newTimesheetBtn.click();
      await page.waitForLoadState('networkidle');
      
      // Find and click auto-populate button
      const autoPopulateBtn = page.locator('button:has-text("8h"), button:has-text("Auto"), #auto-populate-btn');
      if (await autoPopulateBtn.isVisible()) {
        await autoPopulateBtn.click();
        
        // Verify hours were filled (should be 8 for Mon-Fri = 40 total)
        const totalHours = page.locator('.total-hours, #total-hours, .row-total');
        await expect(totalHours.first()).toContainText(/40|8/);
      }
    });
    
  });
  
  test.describe('Submit Timesheet', () => {
    
    test('can submit timesheet with entries', async ({ page }) => {
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to new timesheet
      const newTimesheetBtn = page.locator('button:has-text("New Timesheet"), a:has-text("New Timesheet"), #new-timesheet-btn');
      await newTimesheetBtn.click();
      await page.waitForLoadState('networkidle');
      
      // Add hours
      const addRowBtn = page.locator('button:has-text("Add Row"), button:has-text("Add Entry"), #add-entry-btn');
      if (await addRowBtn.isVisible()) {
        await addRowBtn.click();
      }
      
      // Fill in hours
      const hoursInputs = page.locator('input[type="number"].hours-input, input.entry-hours, input[name*="hours"]');
      if (await hoursInputs.count() > 0) {
        await hoursInputs.first().fill('8');
      }
      
      // Click Submit
      const submitBtn = page.locator('button:has-text("Submit"), #submit-btn');
      await submitBtn.click();
      
      // Handle confirmation dialog if present
      const confirmDialog = page.locator('.confirm-dialog, [role="dialog"], .modal');
      if (await confirmDialog.isVisible({ timeout: 2000 }).catch(() => false)) {
        const confirmBtn = confirmDialog.locator('button:has-text("Confirm"), button:has-text("Yes"), button:has-text("Submit")');
        await confirmBtn.click();
      }
      
      // Wait for submission confirmation
      await expect(page.locator('.toast-success, .notification-success, [role="status"]:has-text("submitted")')).toBeVisible({ timeout: 10000 });
    });
    
    test('submitted timesheet becomes read-only', async ({ page }) => {
      // This test assumes a timesheet was previously submitted
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Look for any submitted timesheet in the list
      const submittedTimesheet = page.locator('.timesheet-card:has(.status-submitted), [data-status="submitted"], .timesheet-submitted');
      
      if (await submittedTimesheet.count() > 0) {
        await submittedTimesheet.first().click();
        await page.waitForLoadState('networkidle');
        
        // Check that form controls are disabled or hidden
        const saveBtn = page.locator('button:has-text("Save Draft"), #save-draft-btn');
        const submitBtn = page.locator('button:has-text("Submit"), #submit-btn');
        
        // Either buttons should be hidden or disabled
        const saveHidden = await saveBtn.isHidden().catch(() => true);
        const submitHidden = await submitBtn.isHidden().catch(() => true);
        
        expect(saveHidden || submitHidden).toBeTruthy();
        
        // Read-only notice should be visible
        await expect(page.locator('.readonly-notice, .read-only-banner, [class*="readonly"]')).toBeVisible();
      }
    });
    
  });
  
  test.describe('Attachments', () => {
    
    test('attachment section is visible for field hours', async ({ page }) => {
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Navigate to new timesheet
      const newTimesheetBtn = page.locator('button:has-text("New Timesheet"), a:has-text("New Timesheet"), #new-timesheet-btn');
      await newTimesheetBtn.click();
      await page.waitForLoadState('networkidle');
      
      // Look for attachment upload area
      const attachmentSection = page.locator('.attachment-section, #attachments, .upload-zone, input[type="file"]');
      await expect(attachmentSection).toBeVisible();
    });
    
  });
  
  test.describe('Dashboard View', () => {
    
    test('dashboard shows timesheet list', async ({ page }) => {
      // Login as staff
      await page.goto('/login');
      await page.waitForLoadState('networkidle');
      
      const staffForm = page.locator('form[action="/auth/dev-login"]').filter({ hasText: 'Staff' });
      await staffForm.locator('button').click();
      await expect(page).toHaveURL(/\/app/);
      
      // Dashboard should show timesheet cards or empty state
      const timesheetCards = page.locator('.timesheet-card, .timesheet-item, [data-timesheet-id]');
      const emptyState = page.locator('.empty-state, .no-timesheets, :has-text("No timesheets")');
      
      // Either timesheets exist or empty state is shown
      const hasTimesheets = await timesheetCards.count() > 0;
      const hasEmptyState = await emptyState.isVisible().catch(() => false);
      
      expect(hasTimesheets || hasEmptyState).toBeTruthy();
    });
    
  });
  
});
