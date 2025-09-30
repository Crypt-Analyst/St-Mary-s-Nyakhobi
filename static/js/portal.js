// Portal JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        setTimeout(function() {
            card.classList.add('fade-in');
        }, index * 100);
    });

    // Handle form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-action="delete"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const item = this.dataset.item || 'this item';
            if (confirm(`Are you sure you want to delete ${item}?`)) {
                // Proceed with delete action
                if (this.href) {
                    window.location.href = this.href;
                } else if (this.dataset.url) {
                    window.location.href = this.dataset.url;
                }
            }
        });
    });

    // Search functionality
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(function(input) {
        const targetSelector = input.dataset.search;
        const searchTargets = document.querySelectorAll(targetSelector);
        
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            searchTargets.forEach(function(target) {
                const text = target.textContent.toLowerCase();
                const shouldShow = text.includes(searchTerm);
                target.style.display = shouldShow ? '' : 'none';
            });
        });
    });

    // Load unread message count
    loadUnreadMessageCount();
    
    // Refresh unread count every 30 seconds
    setInterval(loadUnreadMessageCount, 30000);
});

// Function to load unread message count
function loadUnreadMessageCount() {
    const badge = document.getElementById('unread-count');
    if (!badge) return;

    // This would typically make an AJAX call to get the count
    // For now, we'll use a placeholder implementation
    fetch('/portal/api/unread-messages-count/')
        .then(response => response.json())
        .then(data => {
            const count = data.count || 0;
            if (count > 0) {
                badge.textContent = count;
                badge.style.display = 'inline';
                badge.classList.remove('d-none');
            } else {
                badge.style.display = 'none';
                badge.classList.add('d-none');
            }
        })
        .catch(error => {
            // Silently fail - don't show errors for this
            console.log('Could not load message count:', error);
        });
}

// Function to mark message as read
function markMessageAsRead(messageId) {
    fetch(`/portal/api/messages/${messageId}/mark-read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadUnreadMessageCount();
        }
    })
    .catch(error => {
        console.error('Error marking message as read:', error);
    });
}

// Function to get CSRF token
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    return cookieValue ? cookieValue.split('=')[1] : '';
}

// Grade color helper
function getGradeColor(percentage) {
    if (percentage >= 90) return 'success';
    if (percentage >= 80) return 'info';
    if (percentage >= 70) return 'warning';
    if (percentage >= 60) return 'secondary';
    return 'danger';
}

// Format date helper
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format datetime helper
function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// Show loading state
function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

// Hide loading state
function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }

    const toastHtml = `
        <div class="toast align-items-center text-bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    const toastElement = document.createElement('div');
    toastElement.innerHTML = toastHtml;
    document.getElementById('toast-container').appendChild(toastElement.firstElementChild);

    const toast = new bootstrap.Toast(toastElement.firstElementChild);
    toast.show();
}

// File upload preview
function previewFile(input, previewElement) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Form submission with loading state
function submitFormWithLoading(form, submitButton) {
    showLoading(submitButton);
    
    // Add timeout in case form submission fails
    setTimeout(function() {
        hideLoading(submitButton);
    }, 10000);
}

// Dynamic table sorting
function sortTable(tableId, columnIndex, isNumeric = false) {
    const table = document.getElementById(tableId);
    const tbody = table.getElementsByTagName('tbody')[0];
    const rows = Array.from(tbody.getElementsByTagName('tr'));
    
    let isAscending = table.dataset.sortDirection !== 'asc';
    table.dataset.sortDirection = isAscending ? 'asc' : 'desc';
    
    rows.sort(function(a, b) {
        const aValue = a.getElementsByTagName('td')[columnIndex].textContent.trim();
        const bValue = b.getElementsByTagName('td')[columnIndex].textContent.trim();
        
        if (isNumeric) {
            return isAscending ? 
                parseFloat(aValue) - parseFloat(bValue) : 
                parseFloat(bValue) - parseFloat(aValue);
        } else {
            return isAscending ? 
                aValue.localeCompare(bValue) : 
                bValue.localeCompare(aValue);
        }
    });
    
    // Re-append sorted rows
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
    
    // Update sort indicators
    const headers = table.getElementsByTagName('th');
    Array.from(headers).forEach(function(header, index) {
        header.classList.remove('sort-asc', 'sort-desc');
        if (index === columnIndex) {
            header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
        }
    });
}

// Export table to CSV
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tr');
    
    let csvContent = '';
    
    rows.forEach(function(row) {
        const cells = row.querySelectorAll('th, td');
        const rowData = Array.from(cells).map(function(cell) {
            return `"${cell.textContent.replace(/"/g, '""')}"`;
        });
        csvContent += rowData.join(',') + '\n';
    });
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

// Print functionality
function printContent(elementId) {
    const element = document.getElementById(elementId);
    const printWindow = window.open('', '_blank');
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Print</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-family: Arial, sans-serif; }
                @media print { 
                    .no-print { display: none !important; }
                }
            </style>
        </head>
        <body>
            ${element.innerHTML}
            <script>
                window.onload = function() {
                    window.print();
                    window.onafterprint = function() {
                        window.close();
                    };
                };
            </script>
        </body>
        </html>
    `);
    
    printWindow.document.close();
}

// Utility functions for common tasks
const PortalUtils = {
    formatGrade: function(score, maxScore) {
        const percentage = (score / maxScore) * 100;
        return {
            percentage: Math.round(percentage * 10) / 10,
            letter: this.getLetterGrade(percentage),
            color: getGradeColor(percentage)
        };
    },
    
    getLetterGrade: function(percentage) {
        if (percentage >= 90) return 'A';
        if (percentage >= 80) return 'B';
        if (percentage >= 70) return 'C';
        if (percentage >= 60) return 'D';
        return 'E';
    },
    
    isOverdue: function(dueDate) {
        return new Date(dueDate) < new Date();
    },
    
    getDaysUntilDue: function(dueDate) {
        const due = new Date(dueDate);
        const now = new Date();
        const diffTime = due - now;
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }
};