// XYL-PHOS-CURE Dashboard JavaScript

// Global variables
let projectData = {};
let refreshInterval;

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    startAutoRefresh();
});

// Initialize dashboard components
function initializeDashboard() {
    loadProjectData();
    setupEventListeners();
    updateTimestamps();
}

// Load project data from API
function loadProjectData() {
    fetch('/api/project-status')
        .then(response => response.json())
        .then(data => {
            projectData = data;
            updateDashboardElements(data);
        })
        .catch(error => {
            console.error('Error loading project data:', error);
            showNotification('Error loading project data', 'error');
        });
}

// Update dashboard elements with project data
function updateDashboardElements(data) {
    // Update counters
    if (document.getElementById('days-to-results')) {
        document.getElementById('days-to-results').textContent = data.days_to_results || '--';
    }
    
    if (document.getElementById('days-to-stage2')) {
        document.getElementById('days-to-stage2').textContent = data.days_to_stage2 || '--';
    }
    
    // Update progress indicators
    updateProgressBars();
    updateStatusBadges();
}

// Update progress bars
function updateProgressBars() {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const width = bar.style.width;
        if (width) {
            // Animate progress bars
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        }
    });
}

// Update status badges
function updateStatusBadges() {
    document.querySelectorAll('.badge').forEach(badge => {
        const text = badge.textContent.toLowerCase();
        if (text.includes('completed')) {
            badge.classList.add('badge-pulse-success');
        } else if (text.includes('progress')) {
            badge.classList.add('badge-pulse-warning');
        }
    });
}

// Setup event listeners
function setupEventListeners() {
    // Refresh button
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            loadProjectData();
            showNotification('Dashboard refreshed', 'success');
        });
    }
    
    // Timeline items click events
    document.querySelectorAll('.timeline-item').forEach(item => {
        item.addEventListener('click', function() {
            const milestoneId = this.getAttribute('data-milestone');
            showMilestoneDetails(milestoneId);
        });
    });
    
    // Consortium partner cards
    document.querySelectorAll('.partner-card').forEach(card => {
        card.addEventListener('click', function() {
            showPartnerDetails(this);
        });
    });
}

// Auto-refresh functionality
function startAutoRefresh() {
    // Refresh every 5 minutes
    refreshInterval = setInterval(() => {
        loadProjectData();
        updateTimestamps();
    }, 300000);
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
}

// Update timestamps
function updateTimestamps() {
    const now = new Date();
    document.querySelectorAll('.timestamp').forEach(element => {
        element.textContent = now.toLocaleString();
    });
}

// Show milestone details
function showMilestoneDetails(milestoneId) {
    // This would typically show a modal with milestone details
    console.log('Showing details for milestone:', milestoneId);
}

// Show partner details
function showPartnerDetails(partnerCard) {
    // This would typically show a modal with partner details
    const partnerRole = partnerCard.querySelector('h6').textContent;
    console.log('Showing details for partner:', partnerRole);
}

// Notification system
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed notification`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

// Dashboard utilities
const DashboardUtils = {
    // Format numbers with commas
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    
    // Calculate days between dates
    daysBetween: function(date1, date2) {
        const oneDay = 24 * 60 * 60 * 1000;
        return Math.round(Math.abs((date1 - date2) / oneDay));
    },
    
    // Format file sizes
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    // Get status color class
    getStatusClass: function(status) {
        const statusMap = {
            'completed': 'success',
            'in_progress': 'warning',
            'pending': 'secondary',
            'searching': 'info',
            'contacted': 'warning',
            'confirmed': 'success'
        };
        return statusMap[status.toLowerCase()] || 'secondary';
    }
};

// Chart helpers
const ChartHelpers = {
    // Create progress circle chart
    createProgressCircle: function(elementId, percentage, color = '#198754') {
        const canvas = document.getElementById(elementId);
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = 60;
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Background circle
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.strokeStyle = '#e9ecef';
        ctx.lineWidth = 8;
        ctx.stroke();
        
        // Progress arc
        const angle = (percentage / 100) * 2 * Math.PI;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, -Math.PI / 2, -Math.PI / 2 + angle);
        ctx.strokeStyle = color;
        ctx.lineWidth = 8;
        ctx.lineCap = 'round';
        ctx.stroke();
        
        // Center text
        ctx.fillStyle = color;
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(percentage + '%', centerX, centerY);
    },
    
    // Create timeline progress chart
    createTimelineChart: function(elementId, data) {
        const canvas = document.getElementById(elementId);
        if (!canvas || !window.Chart) return;
        
        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'In Progress', 'Pending'],
                datasets: [{
                    data: data,
                    backgroundColor: ['#198754', '#ffc107', '#6c757d'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: { display: false }
                },
                cutout: '70%'
            }
        });
    }
};

// Animation helpers
const AnimationHelpers = {
    // Animate counter
    animateCounter: function(elementId, targetValue, duration = 2000) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        const startValue = 0;
        const startTime = Date.now();
        
        function updateCounter() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = Math.floor(startValue + (targetValue - startValue) * progress);
            
            element.textContent = currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        }
        
        updateCounter();
    },
    
    // Fade in element
    fadeIn: function(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = 'block';
        
        let opacity = 0;
        const timer = setInterval(() => {
            opacity += 50 / duration;
            if (opacity >= 1) {
                clearInterval(timer);
                opacity = 1;
            }
            element.style.opacity = opacity;
        }, 50);
    }
};

// Export for use in other scripts
window.DashboardApp = {
    loadProjectData,
    showNotification,
    DashboardUtils,
    ChartHelpers,
    AnimationHelpers
};

// CSS Animation classes
const style = document.createElement('style');
style.textContent = `
    .badge-pulse-success {
        animation: pulse-success 2s infinite;
    }
    
    .badge-pulse-warning {
        animation: pulse-warning 2s infinite;
    }
    
    @keyframes pulse-success {
        0% { box-shadow: 0 0 0 0 rgba(25, 135, 84, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(25, 135, 84, 0); }
        100% { box-shadow: 0 0 0 0 rgba(25, 135, 84, 0); }
    }
    
    @keyframes pulse-warning {
        0% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 193, 7, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0); }
    }
    
    .notification {
        animation: slideInRight 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    .card {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
    }
    
    .timeline-item {
        transition: all 0.2s ease;
    }
    
    .timeline-item:hover {
        background-color: rgba(13, 110, 253, 0.1);
        border-radius: 0.375rem;
        padding: 0.5rem;
        margin: -0.5rem;
    }
`;
document.head.appendChild(style);