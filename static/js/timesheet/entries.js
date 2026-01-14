/**
 * Entries Module (REQ-044)
 * 
 * Handles time entry rows - adding, removing, and collecting hour data.
 * Depends on: TimesheetState, DateUtils
 */

const EntriesModule = {
    // Hour type labels (synchronized with timesheet.js)
    HOUR_TYPES: {
        'Field': 'Field Hours',
        'Internal': 'Internal Hours',
        'Training': 'Training',
        'PTO': 'PTO',
        'Unpaid': 'Unpaid Leave',
        'Holiday': 'Holiday',
    },
    
    // All hour types available (non-trainees)
    ALL_HOUR_TYPES: ['Field', 'Internal', 'Training', 'PTO', 'Unpaid', 'Holiday'],
    
    // Trainee can only use Training
    TRAINEE_HOUR_TYPES: ['Training'],
    
    /**
     * Get available hour types for current user
     * @returns {string[]}
     */
    getAvailableHourTypes() {
        // Check if user is trainee (from app.js UserInfo)
        const isTrainee = typeof UserInfo !== 'undefined' && 
                          UserInfo.role === 'trainee';
        
        return isTrainee ? this.TRAINEE_HOUR_TYPES : this.ALL_HOUR_TYPES;
    },
    
    /**
     * Populate the hour type selector dropdown
     */
    populateSelector() {
        const selector = document.getElementById('hour-type-selector');
        if (!selector) return;
        
        selector.innerHTML = '<option value="">Select hour type...</option>';
        
        const availableTypes = this.getAvailableHourTypes();
        
        availableTypes.forEach(hourType => {
            // Skip if already added
            if (TimesheetState.hasHourType(hourType)) return;
            
            const option = document.createElement('option');
            option.value = hourType;
            option.textContent = this.HOUR_TYPES[hourType];
            selector.appendChild(option);
        });
    },
    
    /**
     * Update selector to hide already-added types
     */
    updateSelectorOptions() {
        const selector = document.getElementById('hour-type-selector');
        if (!selector) return;
        
        Array.from(selector.options).forEach(option => {
            if (option.value) {
                option.hidden = TimesheetState.hasHourType(option.value);
            }
        });
        
        // Reset selection
        selector.value = '';
    },
    
    /**
     * Add a new hour type row to the table
     * @param {string} hourType - Hour type to add
     * @param {Object} existingData - Existing entry data (for loading)
     */
    addRow(hourType, existingData = null) {
        if (TimesheetState.hasHourType(hourType)) {
            console.warn(`Hour type ${hourType} already added`);
            return;
        }
        
        const tbody = document.getElementById('entries-body');
        if (!tbody) return;
        
        // Track the hour type
        TimesheetState.addHourType(hourType);
        
        // Create row
        const row = document.createElement('tr');
        row.id = `row-${hourType}`;
        row.className = 'entry-row';
        row.dataset.hourType = hourType;
        
        // Build row HTML
        row.innerHTML = this._buildRowHTML(hourType, existingData);
        
        // Add to table
        tbody.appendChild(row);
        
        // Setup event handlers
        this._setupRowHandlers(row, hourType);
        
        // Update selector
        this.updateSelectorOptions();
        
        // Check if all types added (hide add controls)
        this._checkAllTypesAdded();
        
        // Show and update day totals row (REQ-054)
        this.showDayTotalsRow();
        this.updateColumnTotals();
    },
    
    /**
     * Build HTML for a row
     * @private
     */
    _buildRowHTML(hourType, existingData) {
        const isEditable = TimesheetState.isEditable();
        const readonlyAttr = isEditable ? '' : 'readonly';
        const disabledClass = isEditable ? '' : 'readonly-field';
        
        // Get week dates
        const weekStart = TimesheetState.currentWeekStart;
        const dates = DateUtils.getWeekDates(weekStart);
        
        // Build day inputs
        let dayInputs = '';
        for (let i = 0; i < 7; i++) {
            const dateStr = dates[i];
            const dayName = DateUtils.DAYS[i].toLowerCase();
            const value = existingData?.[dayName] || '';
            const isHoliday = DateUtils.isHoliday(dateStr);
            const holidayClass = isHoliday ? 'holiday-input' : '';
            
            dayInputs += `
                <td>
                    <input type="number" 
                           class="hour-input ${holidayClass} ${disabledClass}"
                           name="${hourType}-${dayName}"
                           data-day="${dayName}"
                           data-date="${dateStr}"
                           min="0" max="24" step="0.5"
                           value="${value}"
                           ${readonlyAttr}
                           placeholder="0">
                </td>
            `;
        }
        
        // Calculate existing total
        const total = existingData ? 
            ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
                .reduce((sum, day) => sum + (parseFloat(existingData[day]) || 0), 0) 
            : 0;
        
        return `
            <td class="hour-type-cell">
                <span class="hour-type-label">${this.HOUR_TYPES[hourType]}</span>
                ${isEditable ? `
                    <button type="button" class="remove-row-btn" title="Remove row">×</button>
                ` : ''}
            </td>
            ${dayInputs}
            <td class="row-total">${total.toFixed(1)}</td>
        `;
    },
    
    /**
     * Setup event handlers for a row
     * @private
     */
    _setupRowHandlers(row, hourType) {
        // Hour input change handlers
        row.querySelectorAll('.hour-input').forEach(input => {
            input.addEventListener('input', () => {
                this.updateRowTotal(hourType);
                TimesheetState.markChanged();
                this._checkHolidayInput(input);
            });
            
            input.addEventListener('change', () => {
                // Validate and clamp value
                let value = parseFloat(input.value) || 0;
                value = Math.max(0, Math.min(24, value));
                value = Math.round(value * 2) / 2; // Round to 0.5
                input.value = value || '';
            });
        });
        
        // Remove button handler
        const removeBtn = row.querySelector('.remove-row-btn');
        if (removeBtn) {
            removeBtn.addEventListener('click', () => {
                this.removeRow(hourType);
            });
        }
    },
    
    /**
     * Check if user is entering hours on a holiday and warn
     * @private
     */
    _checkHolidayInput(input) {
        const dateStr = input.dataset.date;
        if (!dateStr || !DateUtils.isHoliday(dateStr)) return;
        
        const value = parseFloat(input.value) || 0;
        if (value > 0) {
            const holidayName = DateUtils.getHolidayName(dateStr);
            // Could show a toast notification here
            console.log(`Note: Entering hours on ${holidayName}`);
        }
    },
    
    /**
     * Remove an hour type row
     * @param {string} hourType 
     */
    removeRow(hourType) {
        const row = document.getElementById(`row-${hourType}`);
        if (row) {
            row.remove();
            TimesheetState.removeHourType(hourType);
            this.updateSelectorOptions();
            this._checkAllTypesAdded();
            
            // Update totals and show/hide day totals row (REQ-054)
            this.updateColumnTotals();
            this.showDayTotalsRow();
        }
    },
    
    /**
     * Check if all hour types have been added
     * @private
     */
    _checkAllTypesAdded() {
        const addControls = document.getElementById('add-row-controls');
        if (!addControls) return;
        
        const availableTypes = this.getAvailableHourTypes();
        const allAdded = availableTypes.every(type => 
            TimesheetState.hasHourType(type)
        );
        
        addControls.style.display = allAdded ? 'none' : 'flex';
    },
    
    /**
     * Update row total when hours change
     * @param {string} hourType 
     */
    updateRowTotal(hourType) {
        const row = document.getElementById(`row-${hourType}`);
        if (!row) return;
        
        const inputs = row.querySelectorAll('.hour-input');
        let total = 0;
        
        inputs.forEach(input => {
            total += parseFloat(input.value) || 0;
        });
        
        const totalCell = row.querySelector('.row-total');
        if (totalCell) {
            totalCell.textContent = total.toFixed(1);
        }
        
        // Update column totals
        this.updateColumnTotals();
        
        // Update grand total
        this.updateGrandTotal();
    },
    
    /**
     * Update all column totals (REQ-054)
     */
    updateColumnTotals() {
        const rowsContainer = document.getElementById('hour-type-rows');
        const dayTotalsRow = document.getElementById('day-totals-row');
        if (!rowsContainer || !dayTotalsRow) return;
        
        const days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
        
        days.forEach((day, index) => {
            let columnTotal = 0;
            
            rowsContainer.querySelectorAll(`input[data-day="${day}"]`).forEach(input => {
                columnTotal += parseFloat(input.value) || 0;
            });
            
            // Update the day totals row cell (data-day is 0-6 for Sun-Sat)
            const totalCell = dayTotalsRow.querySelector(`.hour-type-day-cell[data-day="${index}"]`);
            if (totalCell) {
                totalCell.textContent = columnTotal > 0 ? columnTotal.toFixed(1) : '0';
            }
        });
        
        // Update grand total
        this.updateGrandTotal();
    },
    
    /**
     * Update grand total (REQ-054)
     */
    updateGrandTotal() {
        const rowsContainer = document.getElementById('hour-type-rows');
        const grandTotalCell = document.getElementById('grand-total');
        if (!rowsContainer || !grandTotalCell) return;
        
        let grandTotal = 0;
        
        // Sum all .hour-type-total-cell values from hour type rows
        rowsContainer.querySelectorAll('.hour-type-row .hour-type-total-cell').forEach(cell => {
            grandTotal += parseFloat(cell.textContent) || 0;
        });
        
        grandTotalCell.textContent = grandTotal > 0 ? grandTotal.toFixed(1) : '0';
    },
    
    /**
     * Show day totals row when there are entries (REQ-054)
     */
    showDayTotalsRow() {
        const dayTotalsRow = document.getElementById('day-totals-row');
        const rowsContainer = document.getElementById('hour-type-rows');
        
        if (!dayTotalsRow || !rowsContainer) return;
        
        const hasRows = rowsContainer.querySelectorAll('.hour-type-row').length > 0;
        
        if (hasRows) {
            dayTotalsRow.classList.remove('hidden');
        } else {
            dayTotalsRow.classList.add('hidden');
        }
    },
    
    /**
     * Hide day totals row (used when clearing)
     */
    hideDayTotalsRow() {
        const dayTotalsRow = document.getElementById('day-totals-row');
        if (dayTotalsRow) {
            dayTotalsRow.classList.add('hidden');
        }
    },
    
    /**
     * Collect all entries data from rows
     * @returns {Object[]} Array of entry objects
     */
    collectEntries() {
        const entries = [];
        const tbody = document.getElementById('entries-body');
        if (!tbody) return entries;
        
        tbody.querySelectorAll('.entry-row').forEach(row => {
            const hourType = row.dataset.hourType;
            const entry = { hour_type: hourType };
            
            row.querySelectorAll('.hour-input').forEach(input => {
                const day = input.dataset.day;
                const value = parseFloat(input.value) || 0;
                entry[day] = value;
            });
            
            // Only include if has any hours
            const hasHours = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
                .some(day => entry[day] > 0);
            
            if (hasHours) {
                entries.push(entry);
            }
        });
        
        return entries;
    },
    
    /**
     * Check if any Field hours exist
     * @returns {boolean}
     */
    hasFieldHours() {
        if (!TimesheetState.hasHourType('Field')) return false;
        
        const row = document.getElementById('row-Field');
        if (!row) return false;
        
        let total = 0;
        row.querySelectorAll('.hour-input').forEach(input => {
            total += parseFloat(input.value) || 0;
        });
        
        return total > 0;
    },
    
    /**
     * Clear all entry rows
     */
    clearAll() {
        // Clear entries-body (table format) if exists
        const tbody = document.getElementById('entries-body');
        if (tbody) {
            tbody.innerHTML = '';
        }
        
        // Clear hour-type-rows (grid format) if exists
        const rowsContainer = document.getElementById('hour-type-rows');
        if (rowsContainer) {
            rowsContainer.innerHTML = '';
        }
        
        // Reset state
        TimesheetState.addedHourTypes.clear();
        this.populateSelector();
        
        const addControls = document.getElementById('add-row-controls');
        if (addControls) {
            addControls.style.display = 'flex';
        }
        
        // Hide day totals row (REQ-054)
        this.hideDayTotalsRow();
    },
    
    /**
     * Set all inputs to readonly mode
     * @param {boolean} readonly 
     */
    setReadOnly(readonly) {
        const tbody = document.getElementById('entries-body');
        if (!tbody) return;
        
        tbody.querySelectorAll('.hour-input').forEach(input => {
            if (readonly) {
                input.setAttribute('readonly', 'readonly');
                input.classList.add('readonly-field');
            } else {
                input.removeAttribute('readonly');
                input.classList.remove('readonly-field');
            }
        });
        
        // Hide/show remove buttons
        tbody.querySelectorAll('.remove-row-btn').forEach(btn => {
            btn.style.display = readonly ? 'none' : 'inline-block';
        });
        
        // Hide/show add controls
        const addControls = document.getElementById('add-row-controls');
        if (addControls) {
            addControls.style.display = readonly ? 'none' : 'flex';
        }
    },
    
    /**
     * Setup add button click handler
     */
    setupAddButton() {
        const addBtn = document.getElementById('add-row-btn');
        const selector = document.getElementById('hour-type-selector');
        
        if (addBtn && selector) {
            addBtn.addEventListener('click', () => {
                const hourType = selector.value;
                if (hourType) {
                    this.addRow(hourType);
                    selector.value = '';
                }
            });
        }
    },
};

// Export for module bundlers (optional)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EntriesModule;
}
