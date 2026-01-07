# Responsive Design Documentation

> **Last Updated:** January 7, 2026  
> **Status:** Initial Release

This document outlines the responsive design implementation for the Northstar Timesheet App, including current features, breakpoint architecture, and recommendations for future development.

---

## Table of Contents

1. [Current Responsive Features](#current-responsive-features)
2. [Breakpoint Architecture](#breakpoint-architecture)
3. [Component Responsiveness](#component-responsiveness)
4. [View-Specific Layouts](#view-specific-layouts)
5. [Audit Findings](#audit-findings)
6. [Future Recommendations](#future-recommendations)

---

## Current Responsive Features

### Recently Implemented (January 2026)

| Feature                     | Description                                                     | Status      |
| --------------------------- | --------------------------------------------------------------- | ----------- |
| **Hamburger Navigation**    | Mobile-only menu that appears next to the logo at < 768px       | ✅ Complete |
| **Three-State Snap Layout** | Admin detail card snaps between 450px, 680px, and 1100px widths | ✅ Complete |
| **Sidebar Auto-Hide**       | Sidebar hidden on mobile, full navigation via hamburger menu    | ✅ Complete |
| **Grid Horizontal Scroll**  | Time entry grids scroll horizontally on narrow viewports        | ✅ Complete |
| **Status Filter Default**   | Admin status filter defaults to "All Statuses"                  | ✅ Complete |

---

## Breakpoint Architecture

The application uses a **mobile-first** approach with the following primary breakpoints:

```css
/* Mobile First (Base Styles) */
/* All base styles target mobile devices */

/* Tablet / Small Desktop */
@media (min-width: 768px) {
  /* Sidebar appears */
  /* Desktop navigation visible */
  /* Hamburger menu hidden */
}

/* Standard Desktop */
@media (min-width: 850px) {
  /* Medium snap point for admin detail card */
}

/* Large Desktop */
@media (min-width: 1300px) {
  /* Wide snap point for admin detail card */
  /* Full grid layouts enabled */
}
```

### CSS Variables for Layout

```css
:root {
  --header-height: 64px;
  --sidebar-width: 240px; /* 0 on mobile */
}
```

---

## Component Responsiveness

### Header

| Viewport              | Behavior                                                       |
| --------------------- | -------------------------------------------------------------- |
| **Desktop (≥ 768px)** | Full header with username, admin link, logout button           |
| **Mobile (< 768px)**  | Hamburger menu (☰) visible, username hidden, admin link hidden |

### Hamburger Menu

- **Location:** Left of the Northstar star logo
- **Visibility:** Only on viewports < 768px
- **Animation:** Transforms to "X" when open
- **Close Triggers:** Click outside, click menu link, click hamburger again
- **Menu Items:**
  - 📋 My Timesheets
  - ✨ New Timesheet
  - 👥 Admin Dashboard (admin users only)

### Sidebar

| Viewport              | Behavior                                  |
| --------------------- | ----------------------------------------- |
| **Desktop (≥ 768px)** | Fixed 240px sidebar with navigation links |
| **Mobile (< 768px)**  | Completely hidden (`display: none`)       |

### Timesheet Cards Grid

| Viewport    | Behavior                                                           |
| ----------- | ------------------------------------------------------------------ |
| **Desktop** | Multi-column grid layout (`repeat(auto-fill, minmax(320px, 1fr))`) |
| **Mobile**  | Single column stack                                                |

### Admin Detail Card (Three-State Snap)

Instead of fluid resizing, the admin detail card **snaps** between three fixed widths:

| Viewport Width     | Card Width      | Description                 |
| ------------------ | --------------- | --------------------------- |
| **< 768px**        | 450px (max 92%) | Mobile: Centered, compact   |
| **769px - 1299px** | 680px           | Medium: Fits with sidebar   |
| **≥ 1300px**       | 1100px          | Large: Full week visibility |

**Why Snap?**  
Fluid layouts caused a "postage stamp" effect where the card appeared too small in the middle of large empty space. Fixed snap points create a more deliberate, professional appearance.

### Time Entries Grid

| Viewport    | Behavior                                            |
| ----------- | --------------------------------------------------- |
| **Desktop** | Full 8-column grid (Hour Type + 7 days)             |
| **Mobile**  | Horizontal scroll wrapper, minimum 700px grid width |

---

## View-Specific Layouts

### Login Page

- **Center-aligned** login card with `max-width: 420px`
- Scales gracefully to 100% width on small screens
- Logo and form elements maintain consistent padding

### My Timesheets

- **Desktop:** Multi-column card grid
- **Mobile:** Single-column stacked cards
- Status filter dropdown remains full-width on mobile

### New Timesheet Editor

- **Desktop:** Centered form with comfortable margins
- **Mobile:** Full-width form, time entry grid scrollable
- Form controls stack vertically on mobile

### Admin Dashboard

- **Desktop:** KPI cards in row, filters side-by-side
- **Mobile:** KPI cards stacked, filters stacked
- Timesheet cards in single column

### Admin Detail

- Uses **three-state snap layout** (documented above)
- Employee info, hours summary adapt via flexbox wrap
- Time entries grid scrollable on narrow viewports

---

## Audit Findings

A comprehensive DOM audit was performed on January 7, 2026, testing all views at 1200px (desktop) and 400px (mobile) widths.

### Desktop (1200px)

| View            | Sidebar | Content Width | Issues |
| --------------- | ------- | ------------- | ------ |
| Login           | N/A     | 420px card    | None   |
| My Timesheets   | 240px   | ~960px        | None   |
| New Timesheet   | 240px   | ~800px card   | None   |
| Admin Dashboard | 240px   | ~960px        | None   |
| Admin Detail    | 240px   | 680px card    | None   |

### Mobile (400px)

| View            | Sidebar | Hamburger | Content Width   | Issues |
| --------------- | ------- | --------- | --------------- | ------ |
| Login           | N/A     | N/A       | 100%            | None   |
| My Timesheets   | Hidden  | Visible   | 100%            | None   |
| New Timesheet   | Hidden  | Visible   | 100%            | None   |
| Admin Dashboard | Hidden  | Visible   | 100%            | None   |
| Admin Detail    | Hidden  | Visible   | 92% (450px cap) | None   |

### Key Observations

1. **No Layout Breakage:** All views render correctly at both extremes
2. **No Horizontal Overflow:** Content is contained or scrollable
3. **Touch Targets:** Buttons and links maintain adequate size for touch
4. **Readability:** Font sizes remain legible on mobile

---

## Future Recommendations

### Short-Term (P1)

1. **Swipe Gestures for Mobile Navigation**

   - Add swipe-right to open hamburger menu
   - Add swipe-left to close

2. **Orientation Support**

   - Test and optimize for landscape mobile orientation
   - Consider different layouts for landscape tablets

3. **Print Styles**
   - Add `@media print` rules for timesheet printing
   - Hide navigation, optimize for paper

### Medium-Term (P2)

4. **Bottom Navigation for Mobile**

   - Consider a fixed bottom nav bar for key actions
   - Common pattern in mobile-first apps

5. **Pull-to-Refresh**

   - Implement native-feeling refresh on My Timesheets
   - Matches mobile app expectations

6. **Responsive Images**
   - Use `srcset` for logo at different resolutions
   - Optimize attachment thumbnails for mobile

### Long-Term (P3)

7. **Progressive Web App (PWA)**

   - Add manifest.json for installability
   - Implement service worker for offline support

8. **Dark Mode Toggle**

   - Currently dark-mode only
   - Add light mode option with system preference detection

9. **Accessibility Audit**
   - Test with screen readers
   - Ensure keyboard navigation works with hamburger menu
   - Add focus indicators for mobile interactions

---

## Testing Responsive Layouts

### Manual Testing

```bash
# Open browser DevTools (F12)
# Use device toolbar (Ctrl+Shift+M)
# Test at these widths:
# - 375px (iPhone SE)
# - 414px (iPhone 12)
# - 768px (iPad)
# - 1024px (iPad Pro / Small Laptop)
# - 1280px (Standard Desktop)
# - 1920px (Large Desktop)
```

### Automated Testing

Consider adding viewport-specific tests:

```javascript
// Cypress example
describe("Responsive Layout", () => {
  it("shows hamburger menu on mobile", () => {
    cy.viewport(400, 800);
    cy.get("#hamburger-btn").should("be.visible");
    cy.get(".sidebar").should("not.be.visible");
  });

  it("shows sidebar on desktop", () => {
    cy.viewport(1200, 800);
    cy.get("#hamburger-btn").should("not.be.visible");
    cy.get(".sidebar").should("be.visible");
  });
});
```

---

## Changelog

| Date       | Change                                               |
| ---------- | ---------------------------------------------------- |
| 2026-01-07 | Initial responsive documentation                     |
| 2026-01-07 | Added hamburger menu for mobile navigation           |
| 2026-01-07 | Implemented three-state snap layout for admin detail |
| 2026-01-07 | Fixed admin status filter default to "All Statuses"  |
