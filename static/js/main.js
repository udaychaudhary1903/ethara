// Main JavaScript file for Admin Dashboard

// Dark mode toggle
function toggleDarkMode() {
    const body = document.body;
    const isDarkMode = body.classList.toggle('dark-mode');
    
    // Save preference to localStorage
    localStorage.setItem('darkMode', isDarkMode);
    
    // Update icon
    const icon = document.querySelector('.fa-moon');
    if (icon) {
        icon.className = isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Load dark mode preference
document.addEventListener('DOMContentLoaded', function() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        const icon = document.querySelector('.fa-moon');
        if (icon) {
            icon.className = 'fas fa-sun';
        }
    }
});

// AJAX helper function
function makeAjaxRequest(url, method = 'POST', data = {}, successCallback = null, errorCallback = null) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: new URLSearchParams(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && successCallback) {
            successCallback(data);
        } else if (data.error && errorCallback) {
            errorCallback(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (errorCallback) {
            errorCallback('An unexpected error occurred.');
        }
    });
}

// Task status update
function updateTaskStatus(taskId, newStatus) {
    const url = `/tasks/${taskId}/update-status/`;
    const data = { status: newStatus };
    
    makeAjaxRequest(url, 'POST', data, 
        function(response) {
            // Update the status badge
            const statusBadge = document.querySelector(`#task-${taskId}-status`);
            if (statusBadge) {
                statusBadge.textContent = response.status;
                statusBadge.className = `badge bg-${getStatusColor(response.status_value)}`;
            }
            showAlert('success', 'Task status updated successfully!');
        },
        function(error) {
            showAlert('danger', error);
        }
    );
}

// Add task comment
function addTaskComment(taskId, comment) {
    const url = `/tasks/${taskId}/add-comment/`;
    const data = { comment: comment };
    
    makeAjaxRequest(url, 'POST', data,
        function(response) {
            // Add the new comment to the list
            const commentsList = document.querySelector('#comments-list');
            if (commentsList) {
                const commentHtml = `
                    <div class="d-flex mb-3">
                        <div class="flex-shrink-0">
                            <i class="fas fa-user-circle fa-2x text-muted"></i>
                        </div>
                        <div class="flex-grow-1 ms-3">
                            <h6 class="fw-bold mb-1">${response.comment.user}</h6>
                            <p class="mb-1">${response.comment.comment}</p>
                            <small class="text-muted">${response.comment.created_at}</small>
                        </div>
                    </div>
                `;
                commentsList.insertAdjacentHTML('afterbegin', commentHtml);
            }
            
            // Clear the comment form
            const commentForm = document.querySelector('#comment-form');
            if (commentForm) {
                commentForm.reset();
            }
            
            showAlert('success', 'Comment added successfully!');
        },
        function(error) {
            showAlert('danger', error);
        }
    );
}

// Get status color for badges
function getStatusColor(status) {
    const colors = {
        'todo': 'secondary',
        'in_progress': 'warning',
        'completed': 'success',
        'cancelled': 'danger',
        'planning': 'secondary',
        'active': 'primary',
        'on_hold': 'warning'
    };
    return colors[status] || 'secondary';
}

// Show alert messages
function showAlert(type, message, duration = 5000) {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertContainer = document.querySelector('.container-fluid');
    if (alertContainer) {
        alertContainer.insertAdjacentHTML('afterbegin', alertHtml);
        
        // Auto-dismiss after duration
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                alert.remove();
            }
        }, duration);
    }
}

// Confirm delete actions
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize popovers
document.addEventListener('DOMContentLoaded', function() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert && alert.parentNode) {
                alert.classList.remove('show');
                setTimeout(function() {
                    if (alert && alert.parentNode) {
                        alert.remove();
                    }
                }, 150);
            }
        }, 5000);
    });
});

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(function(input) {
        input.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                const form = input.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});

// Progress bar animation
function animateProgressBar(element, targetWidth) {
    let currentWidth = 0;
    const increment = targetWidth / 100;
    
    const timer = setInterval(function() {
        currentWidth += increment;
        element.style.width = currentWidth + '%';
        
        if (currentWidth >= targetWidth) {
            clearInterval(timer);
            element.style.width = targetWidth + '%';
        }
    }, 10);
}

// Initialize progress bars
document.addEventListener('DOMContentLoaded', function() {
    const progressBars = document.querySelectorAll('.progress-bar[data-width]');
    progressBars.forEach(function(bar) {
        const targetWidth = parseFloat(bar.getAttribute('data-width'));
        setTimeout(function() {
            animateProgressBar(bar, targetWidth);
        }, 500);
    });
});

// Export to CSV
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            let data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ');
            data = data.replace(/"/g, '""');
            row.push('"' + data + '"');
        }
        csv.push(row.join(','));
    }
    
    const csvString = csv.join('\n');
    const link = document.createElement('a');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvString));
    link.setAttribute('download', filename);
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
