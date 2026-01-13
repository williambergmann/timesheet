/**
 * User Settings Module
 *
 * Handles notification preferences and contact methods (REQ-003).
 */

const SettingsModule = (() => {
    const state = {
        emails: [],
        phones: [],
        emailOptIn: true,
        smsOptIn: true,
        teamsOptIn: true,
        teamsAccount: '',
        themeAuto: false,
        themeDark: true,
    };

    function setState(data) {
        state.emails = Array.isArray(data.notification_emails) ? data.notification_emails : [];
        state.phones = Array.isArray(data.notification_phones) ? data.notification_phones : [];
        state.emailOptIn = data.email_opt_in !== false;
        state.smsOptIn = data.sms_opt_in !== false;
        state.teamsOptIn = data.teams_opt_in !== false;
        state.teamsAccount = data.teams_account || '';
    }

    function dedupe(values) {
        const seen = new Set();
        return values.filter(value => {
            if (seen.has(value)) {
                return false;
            }
            seen.add(value);
            return true;
        });
    }

    function renderList(containerId, values, type) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = '';

        if (!values.length) {
            container.innerHTML = `<div class="settings-empty">No ${type} added yet.</div>`;
            return;
        }

        values.forEach(value => {
            const chip = document.createElement('div');
            chip.className = 'settings-chip';
            chip.innerHTML = `
                <span class="settings-chip-text">${value}</span>
                <button type="button" class="settings-chip-remove" data-value="${value}" aria-label="Remove ${value}">
                    &times;
                </button>
            `;
            container.appendChild(chip);
        });
    }

    function updateToggles() {
        const emailToggle = document.getElementById('settings-email-toggle');
        const smsToggle = document.getElementById('settings-sms-toggle');
        const teamsToggle = document.getElementById('settings-teams-toggle');
        if (emailToggle) emailToggle.checked = state.emailOptIn;
        if (smsToggle) smsToggle.checked = state.smsOptIn;
        if (teamsToggle) teamsToggle.checked = state.teamsOptIn;

        const emailBody = document.getElementById('settings-email-body');
        const smsBody = document.getElementById('settings-sms-body');
        const teamsBody = document.getElementById('settings-teams-body');

        if (emailBody) emailBody.classList.toggle('settings-disabled', !state.emailOptIn);
        if (smsBody) smsBody.classList.toggle('settings-disabled', !state.smsOptIn);
        if (teamsBody) teamsBody.classList.toggle('settings-disabled', !state.teamsOptIn);

        // Theme toggles
        const themeAutoToggle = document.getElementById('settings-theme-auto');
        const themeDarkToggle = document.getElementById('settings-theme-dark');
        const darkModeRow = themeDarkToggle?.closest('.settings-toggle-row');

        if (themeAutoToggle) themeAutoToggle.checked = state.themeAuto;
        if (themeDarkToggle) {
            themeDarkToggle.checked = state.themeDark;
            themeDarkToggle.disabled = state.themeAuto;
        }
        if (darkModeRow) darkModeRow.classList.toggle('settings-disabled', state.themeAuto);
    }

    function renderTeamsStatus() {
        const status = document.getElementById('settings-teams-status');
        if (!status) return;
        if (state.teamsAccount) {
            status.textContent = `Connected as ${state.teamsAccount}`;
            status.classList.remove('settings-status-muted');
        } else {
            status.textContent = 'No Teams account connected';
            status.classList.add('settings-status-muted');
        }
    }

    function render() {
        renderList('settings-email-list', state.emails, 'emails');
        renderList('settings-phone-list', state.phones, 'phone numbers');

        const teamsInput = document.getElementById('settings-teams-account');
        if (teamsInput) {
            teamsInput.value = state.teamsAccount;
        }

        updateToggles();
        renderTeamsStatus();
    }

    function addEmail() {
        const input = document.getElementById('settings-email-input');
        if (!input) return;
        const value = input.value.trim().toLowerCase();
        if (!value) return;
        state.emails = dedupe([...state.emails, value]);
        input.value = '';
        render();
    }

    function addPhone() {
        const input = document.getElementById('settings-phone-input');
        if (!input) return;
        const value = input.value.trim();
        if (!value) return;
        state.phones = dedupe([...state.phones, value]);
        input.value = '';
        render();
    }

    function removeFromList(type, value) {
        if (type === 'email') {
            state.emails = state.emails.filter(item => item !== value);
        } else if (type === 'phone') {
            state.phones = state.phones.filter(item => item !== value);
        }
        render();
    }

    async function load() {
        try {
            const data = await API.getUserSettings();
            setState(data);
            render();
        } catch (error) {
            if (typeof showToast === 'function') {
                showToast(error.message || 'Failed to load settings', 'error');
            }
        }
    }

    async function save() {
        try {
            const teamsInput = document.getElementById('settings-teams-account');
            if (teamsInput) {
                state.teamsAccount = teamsInput.value.trim().toLowerCase();
            }

            if (state.emailOptIn && state.emails.length === 0) {
                if (typeof showToast === 'function') {
                    showToast('Add at least one email address for notifications', 'warning');
                }
                return;
            }

            if (state.smsOptIn && state.phones.length === 0) {
                if (typeof showToast === 'function') {
                    showToast('Add at least one phone number for SMS notifications', 'warning');
                }
                return;
            }

            if (state.teamsOptIn && !state.teamsAccount) {
                if (typeof showToast === 'function') {
                    showToast('Connect a Teams account before enabling notifications', 'warning');
                }
                return;
            }

            const payload = {
                notification_emails: state.emails,
                notification_phones: state.phones,
                email_opt_in: state.emailOptIn,
                sms_opt_in: state.smsOptIn,
                teams_opt_in: state.teamsOptIn,
                teams_account: state.teamsAccount,
            };

            const updated = await API.updateUserSettings(payload);
            setState(updated);
            render();

            if (typeof showToast === 'function') {
                showToast('Settings saved', 'success');
            }
        } catch (error) {
            if (typeof showToast === 'function') {
                showToast(error.message || 'Failed to save settings', 'error');
            }
        }
    }

    function init() {
        const emailAdd = document.getElementById('settings-email-add');
        if (emailAdd) {
            emailAdd.addEventListener('click', addEmail);
        }

        const phoneAdd = document.getElementById('settings-phone-add');
        if (phoneAdd) {
            phoneAdd.addEventListener('click', addPhone);
        }

        const emailInput = document.getElementById('settings-email-input');
        if (emailInput) {
            emailInput.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    addEmail();
                }
            });
        }

        const phoneInput = document.getElementById('settings-phone-input');
        if (phoneInput) {
            phoneInput.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    addPhone();
                }
            });
        }

        const emailList = document.getElementById('settings-email-list');
        if (emailList) {
            emailList.addEventListener('click', (event) => {
                const button = event.target.closest('.settings-chip-remove');
                if (!button) return;
                removeFromList('email', button.dataset.value);
            });
        }

        const phoneList = document.getElementById('settings-phone-list');
        if (phoneList) {
            phoneList.addEventListener('click', (event) => {
                const button = event.target.closest('.settings-chip-remove');
                if (!button) return;
                removeFromList('phone', button.dataset.value);
            });
        }

        const emailToggle = document.getElementById('settings-email-toggle');
        if (emailToggle) {
            emailToggle.addEventListener('change', (event) => {
                state.emailOptIn = event.target.checked;
                updateToggles();
            });
        }

        const smsToggle = document.getElementById('settings-sms-toggle');
        if (smsToggle) {
            smsToggle.addEventListener('change', (event) => {
                state.smsOptIn = event.target.checked;
                updateToggles();
            });
        }

        const teamsToggle = document.getElementById('settings-teams-toggle');
        if (teamsToggle) {
            teamsToggle.addEventListener('change', (event) => {
                state.teamsOptIn = event.target.checked;
                updateToggles();
            });
        }

        // Theme toggles
        const themeAutoToggle = document.getElementById('settings-theme-auto');
        if (themeAutoToggle) {
            themeAutoToggle.addEventListener('change', (event) => {
                state.themeAuto = event.target.checked;
                if (state.themeAuto) {
                    // Detect system preference when automatic is enabled
                    state.themeDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                }
                updateToggles();
            });
        }

        const themeDarkToggle = document.getElementById('settings-theme-dark');
        if (themeDarkToggle) {
            themeDarkToggle.addEventListener('change', (event) => {
                state.themeDark = event.target.checked;
                updateToggles();
            });
        }

        const saveBtn = document.getElementById('settings-save-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', (event) => {
                event.preventDefault();
                save();
            });
        }
    }

    return {
        init,
        load,
    };
})();
