/**
 * Timesheet Modules Index (REQ-044)
 * 
 * Exports all timesheet sub-modules for easy importing.
 * 
 * Usage in HTML:
 *   <script src="/static/js/timesheet/state.js"></script>
 *   <script src="/static/js/timesheet/dates.js"></script>
 *   <script src="/static/js/timesheet/entries.js"></script>
 *   <script src="/static/js/timesheet/attachments.js"></script>
 *   <script src="/static/js/timesheet/index.js"></script>
 *   
 * Or for bundlers:
 *   import { TimesheetState, DateUtils, EntriesModule } from './timesheet';
 */

// Make modules available globally for non-bundled usage
if (typeof window !== 'undefined') {
    window.TimesheetModules = {
        state: typeof TimesheetState !== 'undefined' ? TimesheetState : null,
        dates: typeof DateUtils !== 'undefined' ? DateUtils : null,
        entries: typeof EntriesModule !== 'undefined' ? EntriesModule : null,
        attachments: typeof AttachmentsModule !== 'undefined' ? AttachmentsModule : null,
    };
}

// Module bundler exports
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        TimesheetState: require('./state'),
        DateUtils: require('./dates'),
        EntriesModule: require('./entries'),
        AttachmentsModule: require('./attachments'),
    };
}

/**
 * Initialize all timesheet modules
 * Call this after DOM is ready
 * 
 * @param {string} weekStart - Initial week start date (YYYY-MM-DD)
 */
function initTimesheetModules(weekStart = null) {
    // Initialize state
    if (typeof TimesheetState !== 'undefined') {
        TimesheetState.init(weekStart);
    }
    
    // Setup entry row handlers
    if (typeof EntriesModule !== 'undefined') {
        EntriesModule.populateSelector();
        EntriesModule.setupAddButton();
    }
    
    // Setup attachment handlers
    if (typeof AttachmentsModule !== 'undefined') {
        AttachmentsModule.setupUploadHandler();
    }
    
    console.log('Timesheet modules initialized');
}

// Make init function globally available
if (typeof window !== 'undefined') {
    window.initTimesheetModules = initTimesheetModules;
}
