/**
 * Main Vue application for Snaply
 * This file provides backup functionality if the inline Vue initialization fails
 */

// Only initialize if not already defined
if (!window.app) {
    const app = Vue.createApp({
        delimiters: ['${', '}'],
        data() {
            return {
                loading: false,
                activeSection: 'dashboard',
                notifications: [],
                currentTask: null,
                domains: [],
                selectedDomain: '',
                selectedDevice: 'desktop',
                screenshots: {},
                logs: [],
                screenshotModal: {
                    visible: false,
                    src: '',
                    domain: ''
                }
            };
        },
        methods: {
            showNotification(message, type = 'info') {
                const id = Date.now();
                this.notifications.push({ id, message, type });
                setTimeout(() => {
                    this.notifications = this.notifications.filter(n => n.id !== id);
                }, 5000);
            },
            getNotificationIcon(type) {
                switch(type) {
                    case 'success': return 'fas fa-check-circle';
                    case 'warning': return 'fas fa-exclamation-triangle';
                    case 'error': case 'danger': return 'fas fa-times-circle';
                    default: return 'fas fa-info-circle';
                }
            },
            startScreenshot(domain, deviceType) {
                if (!domain || !deviceType) return;
                
                this.loading = true;
                
                fetch('/zrobscreen', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ domain, deviceType })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.showNotification(data.message, 'success');
                        this.trackTaskProgress(data.task_id);
                    } else {
                        this.showNotification(data.error || 'Failed to start screenshot task', 'error');
                    }
                })
                .catch(error => {
                    this.showNotification(`Error: ${error.message}`, 'error');
                })
                .finally(() => {
                    this.loading = false;
                });
            },
            trackTaskProgress(taskId) {
                if (!taskId) return;
                
                this.currentTask = {
                    id: taskId,
                    progress: 0,
                    status: 'Starting...',
                    domain: '',
                    deviceType: ''
                };
                
                const checkStatus = () => {
                    fetch(`/task_status/${taskId}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.info) {
                                this.currentTask.status = data.info.status || 'Processing...';
                                this.currentTask.domain = data.info.domain || '';
                                this.currentTask.deviceType = data.info.device || '';
                            }
                            
                            if (data.state === 'SUCCESS') {
                                this.currentTask.progress = 100;
                                this.showNotification('Screenshot task completed successfully!', 'success');
                                setTimeout(() => {
                                    this.currentTask = null;
                                }, 3000);
                            } else if (data.state === 'FAILURE') {
                                this.currentTask.progress = 100;
                                this.showNotification(`Task failed: ${data.info?.error || 'Unknown error'}`, 'error');
                                setTimeout(() => {
                                    this.currentTask = null;
                                }, 3000);
                            } else {
                                // Still processing
                                if (data.state === 'PROCESSING') {
                                    this.currentTask.progress = 75;
                                } else if (data.state === 'STARTED') {
                                    this.currentTask.progress = 50;
                                } else {
                                    this.currentTask.progress = 25;
                                }
                                setTimeout(checkStatus, 2000);
                            }
                        })
                        .catch(error => {
                            console.error('Error checking task status:', error);
                            setTimeout(checkStatus, 5000);
                        });
                };
                
                checkStatus();
            },
            clearLogs() {
                fetch('/logs/delete', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            this.showNotification('Logs cleared successfully!', 'success');
                            setTimeout(() => location.reload(), 1000);
                        } else {
                            this.showNotification(data.error || 'Failed to clear logs', 'error');
                        }
                    })
                    .catch(error => {
                        this.showNotification(`Error: ${error.message}`, 'error');
                    });
            },
            openScreenshotModal(src, domain) {
                this.screenshotModal = {
                    visible: true,
                    src,
                    domain
                };
            },
            closeScreenshotModal() {
                this.screenshotModal.visible = false;
            }
        }
    });

    // Make the app globally available
    window.app = app;
    
    // Mount the app when DOM is ready if not already mounted
    document.addEventListener('DOMContentLoaded', () => {
        if (!window.vueInstance) {
            try {
                console.log("Mounting Vue app from app.js");
                window.vueInstance = app.mount('#app');
            } catch (err) {
                console.error('Error mounting Vue app from app.js:', err);
            }
        }
    });
}

// Always ensure showNotification is available
window.showNotification = window.showNotification || function(message, type) {
    if (window.vueInstance) {
        window.vueInstance.showNotification(message, type);
    } else if (window.app && window.app._instance) {
        window.app._instance.proxy.showNotification(message, type);
    } else {
        console.warn('Vue instance not available for notification');
        alert(`${type}: ${message}`);
    }
};
