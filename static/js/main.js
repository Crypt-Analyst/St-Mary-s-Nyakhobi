// Main JavaScript file for St. Mary's School Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initAnimations();
    
    // Initialize smooth scrolling
    initSmoothScroll();
    
    // Initialize form validations
    initFormValidation();
    
    // Initialize image lazy loading
    initLazyLoading();
    
    // Initialize carousel auto-play
    initCarousel();
});

// Animation on scroll
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.card, .quick-link-item, .faculty-card').forEach(el => {
        observer.observe(el);
    });
}

// Smooth scrolling for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Lazy loading for images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Carousel initialization
function initCarousel() {
    const carousel = document.querySelector('#heroCarousel');
    if (carousel) {
        const bsCarousel = new bootstrap.Carousel(carousel, {
            interval: 5000,
            wrap: true
        });
    }
}

// Contact form submission
function submitContactForm(formData) {
    // Show loading state
    const submitBtn = document.querySelector('#contactSubmit');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    submitBtn.disabled = true;
    
    // Simulate form submission (replace with actual AJAX call)
    setTimeout(() => {
        // Show success message
        showAlert('Thank you for your message! We will get back to you soon.', 'success');
        
        // Reset form
        document.querySelector('#contactForm').reset();
        
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 2000);
}

// Show alert messages
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Search functionality
function initSearch() {
    const searchInput = document.querySelector('#searchInput');
    const searchResults = document.querySelector('#searchResults');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            
            if (query.length > 2) {
                // Simulate search (replace with actual search implementation)
                performSearch(query);
            } else {
                searchResults.innerHTML = '';
            }
        });
    }
}

function performSearch(query) {
    // This would be replaced with actual search functionality
    const mockResults = [
        { title: 'Admission Process', url: '/admissions/', type: 'page' },
        { title: 'Academic Programs', url: '/academics/', type: 'page' },
        { title: 'Faculty Directory', url: '/faculty/', type: 'page' }
    ].filter(item => item.title.toLowerCase().includes(query));
    
    displaySearchResults(mockResults);
}

function displaySearchResults(results) {
    const searchResults = document.querySelector('#searchResults');
    
    if (results.length > 0) {
        const resultsHTML = results.map(result => `
            <div class="search-result-item">
                <a href="${result.url}" class="text-decoration-none">
                    <h6 class="mb-1">${result.title}</h6>
                    <small class="text-muted">${result.type}</small>
                </a>
            </div>
        `).join('');
        
        searchResults.innerHTML = resultsHTML;
    } else {
        searchResults.innerHTML = '<div class="text-muted">No results found</div>';
    }
}

// Gallery lightbox
function initGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item img');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            openLightbox(this.src, this.alt);
        });
    });
}

function openLightbox(src, alt) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <span class="lightbox-close">&times;</span>
            <img src="${src}" alt="${alt}" class="lightbox-image">
            <div class="lightbox-caption">${alt}</div>
        </div>
    `;
    
    document.body.appendChild(lightbox);
    
    // Close lightbox
    lightbox.querySelector('.lightbox-close').addEventListener('click', () => {
        lightbox.remove();
    });
    
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            lightbox.remove();
        }
    });
}

// Counter animation for statistics
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    const counterObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => counterObserver.observe(counter));
}

function animateCounter(element) {
    const target = parseInt(element.textContent);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Back to top button
function initBackToTop() {
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.className = 'back-to-top';
    backToTop.style.display = 'none';
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    });
    
    backToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize all features when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initCounters();
    initGallery();
    initBackToTop();
    initSearch();
});