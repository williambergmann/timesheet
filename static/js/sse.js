/**
 * Server-Sent Events Handler
 * 
 * Manages real-time updates from the server.
 */

const SSE = {
    eventSource: null,
    reconnectAttempts: 0,
    maxReconnectAttempts: 5,
    reconnectDelay: 3000,
    
    /**
     * Initialize SSE connection
     */
    init() {
        if (!window.EventSource) {
            console.warn('SSE not supported in this browser');
            return;
        }
        
        this.connect();
    },
    
    /**
     * Connect to SSE endpoint
     */
    connect() {
        try {
            this.eventSource = new EventSource('/api/events');
            
            this.eventSource.onopen = () => {
                console.log('SSE connected');
                this.reconnectAttempts = 0;
            };
            
            this.eventSource.onmessage = (event) => {
                this.handleMessage(event);
            };
            
            this.eventSource.onerror = (error) => {
                console.error('SSE error:', error);
                this.eventSource.close();
                this.attemptReconnect();
            };
            
        } catch (error) {
            console.error('Failed to create SSE connection:', error);
        }
    },
    
    /**
     * Handle incoming SSE message
     */
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            
            switch (data.type) {
                case 'connected':
                    console.log('SSE: Connected to server');
                    break;
                    
                case 'timesheet_approved':
                    this.onTimesheetApproved(data);
                    break;
                    
                case 'timesheet_needs_approval':
                    this.onTimesheetNeedsApproval(data);
                    break;
                    
                case 'timesheet_submitted':
                    this.onTimesheetSubmitted(data);
                    break;
                    
                case 'new_note':
                    this.onNewNote(data);
                    break;
                    
                case 'error':
                    console.warn('SSE: Server error -', data.message);
                    break;
                    
                default:
                    console.log('SSE: Unknown message type', data);
            }
            
        } catch (error) {
            console.error('Failed to parse SSE message:', error);
        }
    },
    
    /**
     * Handle timesheet approved event
     */
    onTimesheetApproved(data) {
        showToast(`Your timesheet for ${data.week_start} has been approved! ✅`, 'success');
        
        // Refresh timesheets list if visible
        const timesheetsView = document.getElementById('view-timesheets');
        if (timesheetsView && timesheetsView.classList.contains('active')) {
            loadTimesheets();
        }
    },
    
    /**
     * Handle timesheet needs approval event
     */
    onTimesheetNeedsApproval(data) {
        showToast(`Your timesheet for ${data.week_start} needs an attachment. Please upload and resubmit.`, 'warning');
        
        // Refresh timesheets list if visible
        const timesheetsView = document.getElementById('view-timesheets');
        if (timesheetsView && timesheetsView.classList.contains('active')) {
            loadTimesheets();
        }
    },
    
    /**
     * Handle new timesheet submitted event (admin)
     */
    onTimesheetSubmitted(data) {
        if (window.currentUser && window.currentUser.is_admin) {
            showToast(`New timesheet submitted by ${data.user_name}`, 'info');
            
            // Refresh admin list if visible
            const adminView = document.getElementById('view-admin');
            if (adminView && adminView.classList.contains('active')) {
                loadAdminTimesheets();
            }
        }
    },
    
    /**
     * Handle new note event
     */
    onNewNote(data) {
        showToast(`New note on your timesheet from ${data.author_name}`, 'info');
    },
    
    /**
     * Attempt to reconnect after disconnection
     */
    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.warn('SSE: Max reconnection attempts reached');
            return;
        }
        
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * this.reconnectAttempts;
        
        console.log(`SSE: Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
        
        setTimeout(() => {
            this.connect();
        }, delay);
    },
    
    /**
     * Disconnect SSE
     */
    disconnect() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    },
};

// Initialize SSE when page loads
document.addEventListener('DOMContentLoaded', () => {
    SSE.init();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    SSE.disconnect();
});
