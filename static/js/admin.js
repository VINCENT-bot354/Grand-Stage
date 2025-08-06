/**
 * Grand Stage Productions - Admin Panel JavaScript
 * Enhanced functionality for the CMS admin interface
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Grand Stage Productions Admin Panel Initialized');
    
    // Initialize all admin functionality
    initializeImagePreview();
    initializeVideoPreview();
    initializeFormValidation();
    initializeContentEditor();
    initializeTooltips();
    initializeSortableElements();
    initializeConfirmDialogs();
    initializeAutoSave();
    initializeLivePreview();
});

/**
 * Image Preview Functionality
 */
function initializeImagePreview() {
    const imageUrlFields = document.querySelectorAll('input[name="image_url"]');
    
    imageUrlFields.forEach(field => {
        const previewContainer = document.getElementById('imagePreview');
        if (!previewContainer) return;
        
        // Initial preview load
        if (field.value) {
            updateImagePreview(field.value, previewContainer);
        }
        
        // Live preview on input
        field.addEventListener('input', debounce(function() {
            const url = this.value.trim();
            updateImagePreview(url, previewContainer);
        }, 500));
        
        // Validate URL on blur
        field.addEventListener('blur', function() {
            validateImageUrl(this);
        });
    });
}

function updateImagePreview(url, container) {
    if (!url || (!url.startsWith('http://') && !url.startsWith('https://'))) {
        container.innerHTML = `
            <div class="preview-placeholder p-4">
                <i class="fas fa-image fa-3x text-muted mb-2"></i>
                <p class="text-muted">Enter an image URL to see preview</p>
            </div>
        `;
        return;
    }
    
    // Show loading state
    container.innerHTML = `
        <div class="preview-placeholder p-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted mt-2">Loading preview...</p>
        </div>
    `;
    
    // Create image element to test loading
    const img = new Image();
    img.onload = function() {
        container.innerHTML = `
            <img src="${url}" alt="Preview" class="img-fluid rounded shadow mb-2" style="max-height: 200px;">
            <p class="small text-muted">Image preview</p>
        `;
    };
    
    img.onerror = function() {
        container.innerHTML = `
            <div class="preview-placeholder p-4">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-2"></i>
                <p class="text-warning">Invalid image URL or image not accessible</p>
                <small class="text-muted">Please check the URL and try again</small>
            </div>
        `;
    };
    
    img.src = url;
}

function validateImageUrl(field) {
    const url = field.value.trim();
    const feedbackElement = field.parentElement.querySelector('.invalid-feedback') || 
                           createFeedbackElement(field);
    
    if (!url) {
        field.classList.remove('is-invalid', 'is-valid');
        return;
    }
    
    if (!isValidUrl(url)) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        feedbackElement.textContent = 'Please enter a valid URL (must start with http:// or https://)';
    } else {
        field.classList.add('is-valid');
        field.classList.remove('is-invalid');
        feedbackElement.textContent = '';
    }
}

/**
 * Video Preview Functionality
 */
function initializeVideoPreview() {
    const videoUrlFields = document.querySelectorAll('input[name="video_url"]');
    const videoTypeFields = document.querySelectorAll('select[name="video_type"]');
    
    videoUrlFields.forEach(field => {
        const previewContainer = document.getElementById('videoPreview');
        if (!previewContainer) return;
        
        const typeField = document.querySelector('select[name="video_type"]');
        
        // Initial preview load
        if (field.value && typeField && typeField.value) {
            updateVideoPreview(field.value, typeField.value, previewContainer);
        }
        
        // Live preview on input
        field.addEventListener('input', debounce(function() {
            const url = this.value.trim();
            const type = typeField ? typeField.value : 'youtube';
            updateVideoPreview(url, type, previewContainer);
        }, 500));
        
        // Validate URL on blur
        field.addEventListener('blur', function() {
            validateVideoUrl(this);
        });
    });
    
    // Update preview when video type changes
    videoTypeFields.forEach(field => {
        field.addEventListener('change', function() {
            const urlField = document.querySelector('input[name="video_url"]');
            const previewContainer = document.getElementById('videoPreview');
            if (urlField && previewContainer) {
                updateVideoPreview(urlField.value, this.value, previewContainer);
            }
        });
    });
}

function updateVideoPreview(url, type, container) {
    if (!url || !isValidUrl(url)) {
        container.innerHTML = `
            <div class="preview-placeholder p-4">
                <i class="fas fa-video fa-3x text-muted mb-2"></i>
                <p class="text-muted">Enter a video URL to see preview</p>
            </div>
        `;
        return;
    }
    
    const embedUrl = convertToEmbedUrl(url, type);
    if (!embedUrl) {
        container.innerHTML = `
            <div class="preview-placeholder p-4">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-2"></i>
                <p class="text-warning">Invalid ${type} URL</p>
                <small class="text-muted">Please check the URL format</small>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div class="video-embed-container">
            <iframe src="${embedUrl}" 
                    title="Video Preview" 
                    frameborder="0" 
                    allowfullscreen
                    loading="lazy"></iframe>
        </div>
        <p class="small text-muted mt-2">Video preview</p>
    `;
}

function convertToEmbedUrl(url, type) {
    if (type === 'youtube') {
        if (url.includes('watch?v=')) {
            const videoId = url.split('watch?v=')[1].split('&')[0];
            return `https://www.youtube.com/embed/${videoId}`;
        } else if (url.includes('youtu.be/')) {
            const videoId = url.split('youtu.be/')[1].split('?')[0];
            return `https://www.youtube.com/embed/${videoId}`;
        }
    } else if (type === 'instagram') {
        if (url.includes('/p/') || url.includes('/reel/')) {
            return url.endsWith('/') ? url + 'embed/' : url + '/embed/';
        }
    }
    return null;
}

function validateVideoUrl(field) {
    const url = field.value.trim();
    const typeField = document.querySelector('select[name="video_type"]');
    const type = typeField ? typeField.value : 'youtube';
    const feedbackElement = field.parentElement.querySelector('.invalid-feedback') || 
                           createFeedbackElement(field);
    
    if (!url) {
        field.classList.remove('is-invalid', 'is-valid');
        return;
    }
    
    if (!isValidUrl(url)) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        feedbackElement.textContent = 'Please enter a valid URL';
        return;
    }
    
    const embedUrl = convertToEmbedUrl(url, type);
    if (!embedUrl) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        feedbackElement.textContent = `Please enter a valid ${type} URL`;
    } else {
        field.classList.add('is-valid');
        field.classList.remove('is-invalid');
        feedbackElement.textContent = '';
    }
}

/**
 * Form Validation Enhancement
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            // Clear validation state on focus
            input.addEventListener('focus', function() {
                this.classList.remove('is-invalid', 'is-valid');
                const feedback = this.parentElement.querySelector('.invalid-feedback');
                if (feedback) feedback.textContent = '';
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fix the errors before submitting', 'error');
                
                // Focus first invalid field
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');
    const feedbackElement = field.parentElement.querySelector('.invalid-feedback') || 
                           createFeedbackElement(field);
    
    // Required field validation
    if (required && !value) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        feedbackElement.textContent = 'This field is required';
        return false;
    }
    
    // Skip validation if field is empty and not required
    if (!value && !required) {
        field.classList.remove('is-invalid', 'is-valid');
        return true;
    }
    
    // Type-specific validation
    let isValid = true;
    let errorMessage = '';
    
    switch (type) {
        case 'email':
            if (!isValidEmail(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
            break;
            
        case 'url':
            if (!isValidUrl(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid URL (must start with http:// or https://)';
            }
            break;
            
        case 'number':
            if (isNaN(value) || value < 0) {
                isValid = false;
                errorMessage = 'Please enter a valid positive number';
            }
            break;
    }
    
    // Field-specific validation
    if (field.name === 'sort_order' && value && (isNaN(value) || value < 0 || value > 999)) {
        isValid = false;
        errorMessage = 'Sort order must be a number between 0 and 999';
    }
    
    // Update field state
    if (isValid) {
        field.classList.add('is-valid');
        field.classList.remove('is-invalid');
        feedbackElement.textContent = '';
    } else {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        feedbackElement.textContent = errorMessage;
    }
    
    return isValid;
}

/**
 * Content Editor Enhancement
 */
function initializeContentEditor() {
    const contentEditor = document.getElementById('contentEditor');
    if (!contentEditor) return;
    
    // Auto-resize textarea
    contentEditor.style.minHeight = '400px';
    contentEditor.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.max(400, this.scrollHeight) + 'px';
    });
    
    // Add formatting buttons
    addFormattingToolbar(contentEditor);
    
    // Add character count
    addCharacterCounter(contentEditor);
    
    // Add HTML syntax highlighting (basic)
    addBasicSyntaxHighlighting(contentEditor);
}

function addFormattingToolbar(textarea) {
    const toolbar = document.createElement('div');
    toolbar.className = 'editor-toolbar mb-2';
    toolbar.innerHTML = `
        <div class="btn-group btn-group-sm" role="group">
            <button type="button" class="btn btn-outline-secondary" data-format="h2" title="Heading">
                <i class="fas fa-heading"></i>
            </button>
            <button type="button" class="btn btn-outline-secondary" data-format="p" title="Paragraph">
                <i class="fas fa-paragraph"></i>
            </button>
            <button type="button" class="btn btn-outline-secondary" data-format="strong" title="Bold">
                <i class="fas fa-bold"></i>
            </button>
            <button type="button" class="btn btn-outline-secondary" data-format="em" title="Italic">
                <i class="fas fa-italic"></i>
            </button>
            <button type="button" class="btn btn-outline-secondary" data-format="link" title="Link">
                <i class="fas fa-link"></i>
            </button>
        </div>
    `;
    
    textarea.parentNode.insertBefore(toolbar, textarea);
    
    // Add click handlers
    toolbar.addEventListener('click', function(e) {
        const button = e.target.closest('button[data-format]');
        if (button) {
            insertFormatting(textarea, button.dataset.format);
        }
    });
}

function insertFormatting(textarea, format) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);
    let replacement = '';
    
    switch (format) {
        case 'h2':
            replacement = `<h2 class="text-theatrical mb-3">${selectedText || 'Heading'}</h2>`;
            break;
        case 'p':
            replacement = `<p>${selectedText || 'Paragraph text'}</p>`;
            break;
        case 'strong':
            replacement = `<strong>${selectedText || 'Bold text'}</strong>`;
            break;
        case 'em':
            replacement = `<em>${selectedText || 'Italic text'}</em>`;
            break;
        case 'link':
            const url = prompt('Enter URL:', 'https://');
            if (url) {
                replacement = `<a href="${url}">${selectedText || 'Link text'}</a>`;
            } else {
                return;
            }
            break;
    }
    
    textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
    textarea.focus();
    
    // Set cursor position after inserted text
    const newPos = start + replacement.length;
    textarea.setSelectionRange(newPos, newPos);
    
    // Trigger input event for auto-resize
    textarea.dispatchEvent(new Event('input'));
}

function addCharacterCounter(textarea) {
    const counter = document.createElement('small');
    counter.className = 'text-muted character-counter';
    textarea.parentNode.appendChild(counter);
    
    function updateCounter() {
        const length = textarea.value.length;
        counter.textContent = `${length} characters`;
        
        if (length > 10000) {
            counter.className = 'text-warning character-counter';
        } else if (length > 15000) {
            counter.className = 'text-danger character-counter';
        } else {
            counter.className = 'text-muted character-counter';
        }
    }
    
    textarea.addEventListener('input', updateCounter);
    updateCounter();
}

function addBasicSyntaxHighlighting(textarea) {
    // Simple HTML tag highlighting on focus out
    textarea.addEventListener('blur', function() {
        const content = this.value;
        const htmlTags = content.match(/<[^>]+>/g);
        
        if (htmlTags) {
            // Add visual feedback for HTML tags (could be enhanced with a proper syntax highlighter)
            console.log('HTML tags detected:', htmlTags.length);
        }
    });
}

/**
 * Tooltips Initialization
 */
function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add custom tooltips for form help
    const helpTexts = document.querySelectorAll('.form-text');
    helpTexts.forEach(helpText => {
        helpText.style.cursor = 'help';
    });
}

/**
 * Sortable Elements (for future drag-and-drop functionality)
 */
function initializeSortableElements() {
    const sortableContainers = document.querySelectorAll('.sortable');
    
    sortableContainers.forEach(container => {
        // Basic visual feedback for sortable items
        const items = container.querySelectorAll('.sortable-item');
        items.forEach(item => {
            item.style.cursor = 'move';
            item.title = 'Drag to reorder';
        });
    });
}

/**
 * Confirmation Dialogs
 */
function initializeConfirmDialogs() {
    const deleteButtons = document.querySelectorAll('button[onclick*="confirm"], form[onsubmit*="confirm"]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.onclick && this.onclick.toString().includes('confirm')) {
                return; // Let the original onclick handle it
            }
            
            const action = this.textContent.toLowerCase();
            const isDelete = action.includes('delete') || action.includes('remove');
            
            if (isDelete) {
                const confirmed = confirm('Are you sure you want to delete this item? This action cannot be undone.');
                if (!confirmed) {
                    e.preventDefault();
                }
            }
        });
    });
}

/**
 * Auto-save Functionality
 */
function initializeAutoSave() {
    const forms = document.querySelectorAll('form[data-autosave]');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        let saveTimeout;
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    autoSaveForm(form);
                }, 2000);
            });
        });
    });
}

function autoSaveForm(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Save to localStorage
    const formId = form.id || 'autosave_form';
    localStorage.setItem(`autosave_${formId}`, JSON.stringify(data));
    
    showNotification('Draft saved automatically', 'info', 2000);
}

/**
 * Live Preview Functionality
 */
function initializeLivePreview() {
    const previewButtons = document.querySelectorAll('.btn[target="_blank"]');
    
    previewButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Opening...';
            this.disabled = true;
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 2000);
        });
    });
}

/**
 * Utility Functions
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function createFeedbackElement(field) {
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    field.parentNode.appendChild(feedback);
    return feedback;
}

function showNotification(message, type = 'info', duration = 5000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    `;
    
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

/**
 * Image Gallery Modal Enhancement
 */
document.addEventListener('DOMContentLoaded', function() {
    const galleryImages = document.querySelectorAll('.gallery-image[data-bs-toggle="modal"]');
    
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            // Add loading state to modal
            const modalId = this.getAttribute('data-bs-target');
            const modal = document.querySelector(modalId);
            if (modal) {
                const modalBody = modal.querySelector('.modal-body');
                const originalContent = modalBody.innerHTML;
                
                modalBody.innerHTML = `
                    <div class="text-center p-4">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <p class="mt-2">Loading image...</p>
                    </div>
                `;
                
                // Restore content after a brief delay
                setTimeout(() => {
                    modalBody.innerHTML = originalContent;
                }, 500);
            }
        });
    });
});

/**
 * Admin Dashboard Stats Animation
 */
document.addEventListener('DOMContentLoaded', function() {
    const statNumbers = document.querySelectorAll('.stat-info h4');
    
    const animateCounter = (element, target) => {
        let current = 0;
        const increment = target / 20;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 50);
    };
    
    // Animate counters on page load
    statNumbers.forEach(stat => {
        const target = parseInt(stat.textContent);
        if (!isNaN(target)) {
            stat.textContent = '0';
            setTimeout(() => animateCounter(stat, target), 200);
        }
    });
});

/**
 * Keyboard Shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + S to save form
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const submitButton = document.querySelector('form input[type="submit"], form button[type="submit"]');
        if (submitButton) {
            submitButton.click();
            showNotification('Form saved!', 'success');
        }
    }
    
    // Escape to cancel/go back
    if (e.key === 'Escape') {
        const backButton = document.querySelector('a[href*="dashboard"], a[href*="admin"]');
        if (backButton && confirm('Go back to dashboard?')) {
            window.location.href = backButton.href;
        }
    }
});

console.log('Grand Stage Productions Admin Panel JavaScript loaded successfully');
