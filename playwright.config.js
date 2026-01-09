// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Playwright E2E Test Configuration
 * 
 * See: https://playwright.dev/docs/test-configuration
 * 
 * Note: These tests are designed to run against a local Docker environment.
 * Ensure Docker containers are running before executing tests:
 *   cd docker && docker compose up -d
 */

module.exports = defineConfig({
  // Test directory
  testDir: './tests/e2e',
  
  // Run tests in parallel
  fullyParallel: true,
  
  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,
  
  // Retry on CI only
  retries: process.env.CI ? 2 : 0,
  
  // Opt out of parallel tests on CI
  workers: process.env.CI ? 1 : undefined,
  
  // Reporter to use
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report' }],
  ],
  
  // Shared settings for all the projects below
  use: {
    // Base URL to use in actions like `await page.goto('/')`
    baseURL: process.env.BASE_URL || 'http://localhost',
    
    // Collect trace when retrying the failed test
    trace: 'on-first-retry',
    
    // Screenshot on failure
    screenshot: 'only-on-failure',
    
    // Video recording on failure
    video: 'on-first-retry',
  },

  // Configure projects for major browsers
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // Uncomment to add more browsers
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],

  // Run local dev server before starting the tests (optional)
  // webServer: {
  //   command: 'cd docker && docker compose up -d',
  //   url: 'http://localhost',
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 120 * 1000,
  // },
  
  // Output folder for test artifacts
  outputDir: 'test-results/',
  
  // Timeout for each test (5 minutes for slower CI environments)
  timeout: 60000,
  
  // Expect timeout
  expect: {
    timeout: 10000,
  },
});
