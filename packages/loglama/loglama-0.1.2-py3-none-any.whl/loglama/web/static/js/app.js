/**
 * LogLama Viewer JavaScript
 * Enhanced version with real-time updates and improved UI
 */

// State management
const state = {
    currentPage: 1,
    pageSize: 100,
    filters: {
        level: '',
        component: '',
        search: '',
        startDate: '',
        endDate: ''
    },
    totalLogs: 0,
    totalPages: 0,
    autoRefresh: true, // Set auto-refresh to true by default
    refreshInterval: null,
    refreshRate: 5000, // 5 seconds
    darkMode: window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches,
    lastLogId: 0, // Track the last log ID for real-time updates
    sortColumn: 'timestamp', // Default sort column
    sortDirection: 'desc' // Default sort direction (newest first)
};

// DOM elements
const elements = {
    logsTableBody: document.getElementById('logs-table-body'),
    pagination: document.getElementById('pagination'),
    paginationInfo: document.getElementById('pagination-info'),
    filterForm: document.getElementById('filter-form'),
    levelFilter: document.getElementById('level-filter'),
    componentFilter: document.getElementById('component-filter'),
    searchFilter: document.getElementById('search'),
    startDateFilter: document.getElementById('start-date'),
    endDateFilter: document.getElementById('end-date'),
    resetFiltersBtn: document.getElementById('reset-filters'),
    pageSizeSelect: document.getElementById('page-size'),
    refreshLogsBtn: document.getElementById('refresh-logs'),
    autoRefreshBtn: document.getElementById('auto-refresh'),
    autoRefreshIndicator: document.getElementById('auto-refresh-indicator'),
    darkModeToggle: document.getElementById('dark-mode-toggle'),
    statsLink: document.getElementById('stats-link'),
    statsPanel: document.getElementById('stats-panel'),
    levelStats: document.getElementById('level-stats'),
    componentStats: document.getElementById('component-stats'),
    dateRangeStats: document.getElementById('date-range-stats'),
    totalLogsStats: document.getElementById('total-logs'),
    logDetailModal: new bootstrap.Modal(document.getElementById('log-detail-modal')),
    exportLogsBtn: document.getElementById('export-logs'),
    notificationArea: document.getElementById('notification-area')
};

// Initialize the application
async function init() {
    // Apply dark mode if needed
    if (state.darkMode) {
        document.body.classList.add('dark-mode');
        if (elements.darkModeToggle) {
            elements.darkModeToggle.checked = true;
        }
    }
    
    // Set auto-refresh checkbox to match the default state
    if (elements.autoRefreshBtn) {
        elements.autoRefreshBtn.checked = state.autoRefresh;
        // Enable auto-refresh if it's set to true by default
        if (state.autoRefresh) {
            toggleAutoRefresh(true);
        }
    }
    
    // Load initial data
    try {
        await Promise.all([
            loadLogs(),
            loadLevels(),
            loadComponents(),
            loadStats()
        ]);
        
        // Show success notification
        showNotification('LogLama viewer initialized successfully', 'success');
    } catch (error) {
        showNotification('Failed to initialize LogLama viewer: ' + error.message, 'error');
    }

    // Set up event listeners
    setupEventListeners();
}

// Load logs from the API
async function loadLogs() {
    try {
        const params = new URLSearchParams({
            page: state.currentPage,
            page_size: state.pageSize
        });

        // Add filters if they are set
        if (state.filters.level) params.append('level', state.filters.level);
        if (state.filters.component) params.append('component', state.filters.component);
        if (state.filters.search) params.append('search', state.filters.search);
        if (state.filters.startDate) params.append('start_date', state.filters.startDate);
        if (state.filters.endDate) params.append('end_date', state.filters.endDate);
        
        // Add sorting parameters
        params.append('sort_by', state.sortColumn);
        params.append('sort_direction', state.sortDirection);

        const response = await fetch(`/api/logs?${params.toString()}`);
        const data = await response.json();

        if (data.error) {
            showError(data.error);
            return;
        }

        // Update state
        state.totalLogs = data.total;
        state.totalPages = data.pages;

        // Render logs
        renderLogs(data.logs);
        renderPagination();
        updatePaginationInfo();
        
        // Update sort indicators
        updateSortIndicators();
    } catch (error) {
        showError(`Failed to load logs: ${error.message}`);
    }
}

// Load available log levels
async function loadLevels() {
    try {
        const response = await fetch('/api/levels');
        const levels = await response.json();

        // Clear existing options except the first one
        while (elements.levelFilter.options.length > 1) {
            elements.levelFilter.remove(1);
        }

        // Add new options
        levels.forEach(level => {
            const option = document.createElement('option');
            option.value = level;
            option.textContent = level;
            elements.levelFilter.appendChild(option);
        });
    } catch (error) {
        showError(`Failed to load log levels: ${error.message}`);
    }
}

// Load available components
async function loadComponents() {
    try {
        const response = await fetch('/api/components');
        const components = await response.json();

        // Clear existing options except the first one
        while (elements.componentFilter.options.length > 1) {
            elements.componentFilter.remove(1);
        }

        // Add new options
        components.forEach(component => {
            const option = document.createElement('option');
            option.value = component;
            option.textContent = component;
            elements.componentFilter.appendChild(option);
        });
    } catch (error) {
        showError(`Failed to load components: ${error.message}`);
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();

        if (stats.error) {
            showError(stats.error);
            return;
        }

        renderStats(stats);
    } catch (error) {
        showError(`Failed to load statistics: ${error.message}`);
    }
}

// Render logs in the table
function renderLogs(logs) {
    elements.logsTableBody.innerHTML = '';

    if (logs.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `<td colspan="5" class="text-center">No logs found</td>`;
        elements.logsTableBody.appendChild(row);
        return;
    }

    logs.forEach(log => {
        const row = document.createElement('tr');
        
        // Format timestamp
        const timestamp = new Date(log.timestamp);
        const formattedTimestamp = timestamp.toLocaleString();
        
        // Create level badge
        const levelBadge = `<span class="level-badge level-${log.level.toLowerCase()}">${log.level}</span>`;
        
        // Handle message display with truncation indicator
        let messageHtml = `<div class="message-content">${escapeHtml(log.message)}</div>`;
        if (log.truncated) {
            messageHtml = `<div class="message-content truncated" title="Message was truncated. Click View to see full content.">${escapeHtml(log.message)} <span class="truncation-indicator">[truncated]</span></div>`;
        }
        
        // Improve logger name display
        let loggerName = log.logger_name;
        if (loggerName === 'unknown' || loggerName.endsWith('.unknown')) {
            // Try to extract a better logger name from the message
            const message = log.message.trim();
            if (message.includes('/home/tom/github/py-lama/')) {
                // Extract component name from path
                const pathMatch = message.match(/\/home\/tom\/github\/py-lama\/([^/]+)/);
                if (pathMatch && pathMatch[1]) {
                    loggerName = pathMatch[1];
                }
            }
        }
        
        row.innerHTML = `
            <td>${formattedTimestamp}</td>
            <td>${levelBadge}</td>
            <td>${loggerName}</td>
            <td>${messageHtml}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary view-log" data-log-id="${log.id}">
                    View
                </button>
            </td>
        `;
        
        elements.logsTableBody.appendChild(row);
    });

    // Add event listeners to view buttons
    document.querySelectorAll('.view-log').forEach(button => {
        button.addEventListener('click', () => {
            const logId = button.getAttribute('data-log-id');
            viewLogDetail(logId);
        });
    });
}

// Render pagination controls
function renderPagination() {
    const paginationElement = document.querySelector('#pagination ul');
    paginationElement.innerHTML = '';

    // Previous button
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${state.currentPage === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#" data-page="${state.currentPage - 1}">Previous</a>`;
    paginationElement.appendChild(prevLi);

    // Page numbers
    const startPage = Math.max(1, state.currentPage - 2);
    const endPage = Math.min(state.totalPages, startPage + 4);

    for (let i = startPage; i <= endPage; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === state.currentPage ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
        paginationElement.appendChild(li);
    }

    // Next button
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${state.currentPage === state.totalPages ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#" data-page="${state.currentPage + 1}">Next</a>`;
    paginationElement.appendChild(nextLi);

    // Add event listeners to pagination links
    document.querySelectorAll('#pagination .page-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = parseInt(link.getAttribute('data-page'));
            if (page >= 1 && page <= state.totalPages) {
                state.currentPage = page;
                loadLogs();
            }
        });
    });
}

// Update pagination info text
function updatePaginationInfo() {
    const start = (state.currentPage - 1) * state.pageSize + 1;
    const end = Math.min(state.currentPage * state.pageSize, state.totalLogs);
    elements.paginationInfo.textContent = `Showing ${start}-${end} of ${state.totalLogs} logs`;
}

// Render statistics
function renderStats(stats) {
    // Level stats
    elements.levelStats.innerHTML = '';
    Object.entries(stats.level_counts).forEach(([level, count]) => {
        const div = document.createElement('div');
        div.className = 'stat-item';
        div.innerHTML = `
            <span class="stat-label">${level}</span>
            <span class="stat-value">
                <span class="level-badge level-${level.toLowerCase()}">${count}</span>
            </span>
        `;
        elements.levelStats.appendChild(div);
    });

    // Component stats
    elements.componentStats.innerHTML = '';
    Object.entries(stats.component_counts).forEach(([component, count]) => {
        const div = document.createElement('div');
        div.className = 'stat-item';
        div.innerHTML = `
            <span class="stat-label">${component}</span>
            <span class="stat-value">${count}</span>
        `;
        elements.componentStats.appendChild(div);
    });

    // Date range stats
    elements.dateRangeStats.innerHTML = '';
    if (stats.date_range.min_date && stats.date_range.max_date) {
        const minDate = new Date(stats.date_range.min_date).toLocaleString();
        const maxDate = new Date(stats.date_range.max_date).toLocaleString();
        const div = document.createElement('div');
        div.innerHTML = `<div>${minDate} to ${maxDate}</div>`;
        elements.dateRangeStats.appendChild(div);
    } else {
        elements.dateRangeStats.innerHTML = '<div>No logs available</div>';
    }

    // Total logs
    elements.totalLogsStats.innerHTML = `<div class="fw-bold">${stats.total}</div>`;
}

// View log detail
async function viewLogDetail(logId) {
    try {
        const response = await fetch(`/api/log/${logId}`);
        const log = await response.json();

        if (log.error) {
            showError(log.error);
            return;
        }

        // Populate modal with log details
        document.getElementById('detail-id').textContent = log.id;
        document.getElementById('detail-timestamp').textContent = new Date(log.timestamp).toLocaleString();
        document.getElementById('detail-level').innerHTML = `<span class="level-badge level-${log.level.toLowerCase()}">${log.level}</span>`;
        document.getElementById('detail-component').textContent = log.logger_name;
        document.getElementById('detail-thread').textContent = log.thread_name || 'N/A';
        document.getElementById('detail-process').textContent = log.process_name || 'N/A';
        document.getElementById('detail-file').textContent = log.file_path || 'N/A';
        document.getElementById('detail-line').textContent = log.line_number || 'N/A';
        document.getElementById('detail-message').textContent = log.message;
        
        // Format context as JSON if it's an object
        let contextContent = log.context || '{}';
        try {
            if (typeof contextContent === 'string') {
                contextContent = JSON.parse(contextContent);
            }
            document.getElementById('detail-context').textContent = JSON.stringify(contextContent, null, 2);
        } catch (e) {
            document.getElementById('detail-context').textContent = contextContent;
        }

        // Show the modal
        elements.logDetailModal.show();
    } catch (error) {
        showError(`Failed to load log details: ${error.message}`);
    }
}

// Set up event listeners
async function setupEventListeners() {
    // Filter form submission
    elements.filterForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        state.filters.level = elements.levelFilter.value;
        state.filters.component = elements.componentFilter.value;
        state.filters.search = elements.searchFilter.value;
        state.filters.startDate = elements.startDateFilter.value;
        state.filters.endDate = elements.endDateFilter.value;
        state.currentPage = 1; // Reset to first page when applying filters
        await loadLogs();
    });

    // Reset filters
    elements.resetFiltersBtn.addEventListener('click', async () => {
        elements.levelFilter.value = '';
        elements.componentFilter.value = '';
        elements.searchFilter.value = '';
        elements.startDateFilter.value = '';
        elements.endDateFilter.value = '';
        state.filters = {
            level: '',
            component: '',
            search: '',
            startDate: '',
            endDate: ''
        };
        state.currentPage = 1;
        await loadLogs();
    });

    // Page size change
    elements.pageSizeSelect.addEventListener('change', async () => {
        state.pageSize = parseInt(elements.pageSizeSelect.value);
        state.currentPage = 1; // Reset to first page when changing page size
        await loadLogs();
    });

    // Manual refresh
    elements.refreshLogsBtn.addEventListener('click', async () => {
        await loadLogs();
        showNotification('Logs refreshed', 'info');
    });

    // Auto-refresh toggle
    elements.autoRefreshBtn.addEventListener('change', () => {
        toggleAutoRefresh(elements.autoRefreshBtn.checked);
    });

    // Dark mode toggle
    elements.darkModeToggle.addEventListener('change', () => {
        toggleDarkMode(elements.darkModeToggle.checked);
    });

    // Stats panel toggle
    elements.statsLink.addEventListener('click', (e) => {
        e.preventDefault();
        elements.statsPanel.style.display = elements.statsPanel.style.display === 'none' ? 'block' : 'none';
    });

    // Export logs
    elements.exportLogsBtn.addEventListener('click', exportLogs);
    
    // Clear logs button
    document.getElementById('clear-logs').addEventListener('click', async () => {
        if (confirm('Are you sure you want to clear all logs? This action cannot be undone.')) {
            await clearLogs();
        }
    });
    
    // Add click event listeners to sortable table headers
    document.querySelectorAll('th.sortable').forEach(header => {
        header.addEventListener('click', () => {
            const column = header.getAttribute('data-sort');
            
            // If clicking the same column, toggle sort direction
            if (state.sortColumn === column) {
                state.sortDirection = state.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                // If clicking a different column, set it as the new sort column with default direction
                state.sortColumn = column;
                // For timestamp, default to desc (newest first), for others default to asc
                state.sortDirection = column === 'timestamp' ? 'desc' : 'asc';
            }
            
            // Reset to first page when changing sort
            state.currentPage = 1;
            
            // Reload logs with new sort
            loadLogs();
        });
    });
}

// Helper function to show error messages
function showError(message) {
    console.error(message);
    showNotification(message, 'error');
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Toggle auto-refresh functionality
function toggleAutoRefresh(enabled) {
    // Only take action if the state is changing
    if (state.autoRefresh === enabled) {
        return;
    }
    
    state.autoRefresh = enabled;
    
    // Update UI
    if (elements.autoRefreshBtn) {
        elements.autoRefreshBtn.checked = enabled;
    }
    
    if (elements.autoRefreshIndicator) {
        elements.autoRefreshIndicator.style.display = enabled ? 'inline-block' : 'none';
    }
    
    // Show notification only if triggered by user action (not on page load)
    const isUserAction = document.readyState === 'complete' && document.visibilityState === 'visible';
    
    if (isUserAction) {
        if (enabled) {
            showNotification('Auto-refresh enabled');
        } else {
            showNotification('Auto-refresh disabled');
        }
    }
    
    // Manage the refresh interval
    if (enabled) {
        // Start auto-refresh interval
        if (state.refreshInterval) {
            clearInterval(state.refreshInterval);
        }
        
        state.refreshInterval = setInterval(() => {
            checkForNewLogs();
        }, state.refreshRate);
    } else {
        // Clear auto-refresh interval
        if (state.refreshInterval) {
            clearInterval(state.refreshInterval);
            state.refreshInterval = null;
        }
        
        showNotification('Auto-refresh disabled', 'info');
    }
}

// Check for new logs (used by auto-refresh)
async function checkForNewLogs() {
    try {
        // Only check for new logs if we're on the first page
        if (state.currentPage !== 1) return;
        
        const params = new URLSearchParams({
            page: 1,
            page_size: 10, // Just get a few logs to check
            newest_first: true
        });
        
        const response = await fetch(`/api/logs?${params.toString()}`);
        
        // Check if response is ok before trying to parse JSON
        if (!response.ok) {
            console.error(`Error checking for new logs: ${response.status} ${response.statusText}`);
            return;
        }
        
        // Check if response has content before parsing JSON
        const text = await response.text();
        if (!text || text.trim() === '') {
            console.error('Empty response from server');
            return;
        }
        
        // Parse JSON from text
        const data = JSON.parse(text);
        
        if (data.error) {
            console.error(`Error checking for new logs: ${data.error}`);
            return;
        }
        
        // Check if there are new logs
        if (data.logs && data.logs.length > 0) {
            const newestLogId = parseInt(data.logs[0].id);
            
            if (state.lastLogId === 0) {
                // First time checking, just store the ID
                state.lastLogId = newestLogId;
            } else if (newestLogId > state.lastLogId) {
                // New logs found
                const newLogsCount = newestLogId - state.lastLogId;
                
                // Only show notification if there are actually new logs and more than 0
                if (newLogsCount > 0) {
                    showNotification(`${newLogsCount} new log${newLogsCount > 1 ? 's' : ''} available`, 'info');
                    
                    // Reload logs
                    loadLogs();
                    loadStats();
                }
                
                // Update the last log ID regardless
                state.lastLogId = newestLogId;
            }
        }
    } catch (error) {
        console.error(`Error in auto-refresh: ${error.message}`);
    }
}

// Toggle dark mode
function toggleDarkMode(enabled) {
    state.darkMode = enabled;
    
    if (enabled) {
        document.body.classList.add('dark-mode');
        showNotification('Dark mode enabled', 'info');
    } else {
        document.body.classList.remove('dark-mode');
        showNotification('Dark mode disabled', 'info');
    }
    
    // Store preference in localStorage
    localStorage.setItem('loglama_dark_mode', enabled ? 'true' : 'false');
}

// Show notification
function showNotification(message, type = 'info') {
    // Don't show empty notifications
    if (!message || message.trim() === '') {
        console.warn('Attempted to show empty notification');
        return;
    }
    
    // Clear existing notifications of the same type
    const existingNotifications = elements.notificationArea.querySelectorAll(`.notification.${type}`);
    existingNotifications.forEach(notification => {
        notification.remove();
    });
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Create notification content
    const content = document.createElement('div');
    content.className = 'notification-content';
    content.innerHTML = `<strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> ${message}`;
    
    // Create close button
    const closeBtn = document.createElement('span');
    closeBtn.className = 'notification-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.addEventListener('click', () => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Add content and close button to notification
    notification.appendChild(content);
    notification.appendChild(closeBtn);
    
    // Add notification to notification area
    elements.notificationArea.appendChild(notification);
    
    // Auto-remove notification after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.add('fade-out');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000); // 5 seconds
}

// Export logs to CSV or JSON
async function exportLogs() {
    try {
        // Get all logs with current filters
        const params = new URLSearchParams({
            page: 1,
            page_size: 10000 // Get a large number of logs
        });
        
        // Add filters if they are set
        if (state.filters.level) params.append('level', state.filters.level);
        if (state.filters.component) params.append('component', state.filters.component);
        if (state.filters.search) params.append('search', state.filters.search);
        if (state.filters.startDate) params.append('start_date', state.filters.startDate);
        if (state.filters.endDate) params.append('end_date', state.filters.endDate);
        
        showNotification('Preparing logs for export...', 'info');
        
        const response = await fetch(`/api/logs?${params.toString()}`);
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // Create CSV content
        let csvContent = 'data:text/csv;charset=utf-8,';
        csvContent += 'ID,Timestamp,Level,Component,Message,Context\n';
        
        data.logs.forEach(log => {
            // Format fields for CSV
            const id = log.id;
            const timestamp = log.timestamp;
            const level = log.level;
            const component = log.logger_name;
            const message = `"${log.message.replace(/"/g, '""')}"`; // Escape quotes
            const context = `"${(log.context || '').replace(/"/g, '""')}"`; // Escape quotes
            
            csvContent += `${id},${timestamp},${level},${component},${message},${context}\n`;
        });
        
        // Create download link
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', `loglama_export_${new Date().toISOString().slice(0, 10)}.csv`);
        document.body.appendChild(link);
        
        // Trigger download
        link.click();
        document.body.removeChild(link);
        
        showNotification(`Exported ${data.logs.length} logs to CSV`, 'success');
    } catch (error) {
        showError(`Failed to export logs: ${error.message}`);
    }
}

// Clear all logs from the database
async function clearLogs() {
    try {
        const response = await fetch('/api/logs/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.error) {
            showNotification('Failed to clear logs: ' + data.error, 'error');
            return;
        }
        
        // Reload logs and stats
        await Promise.all([
            loadLogs(),
            loadStats()
        ]);
        
        showNotification('All logs cleared successfully', 'success');
    } catch (error) {
        showNotification('Failed to clear logs: ' + error.message, 'error');
    }
}

// Update sort indicators in the table headers
function updateSortIndicators() {
    // Remove all existing sort classes
    document.querySelectorAll('th.sortable').forEach(header => {
        header.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Add the appropriate sort class to the current sort column
    const currentSortHeader = document.querySelector(`th[data-sort="${state.sortColumn}"]`);
    if (currentSortHeader) {
        currentSortHeader.classList.add(state.sortDirection === 'asc' ? 'sort-asc' : 'sort-desc');
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', init);
