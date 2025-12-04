document.addEventListener('DOMContentLoaded', function() {
    // Form validation and focus handling
    if (document.querySelector('.entry-form-card') || document.querySelector('input[name="location"]')) {
        
        // Auto-focus on location input when page loads
        const locationInput = document.querySelector('input[name="location"]');
        if (locationInput) {
            locationInput.focus();
        }
        
        // Add validation for pain level and sleep hours
        const painInput = document.querySelector('input[name="pain_level"]');
        const moodInput = document.querySelector('input[name="mood_level"]');
        const sleepInput = document.querySelector('input[name="sleep_hours"]');
        
        if (painInput) {
            painInput.addEventListener('input', function() {
                const value = parseInt(this.value);
                if (value < 0) this.value = 0;
                if (value > 10) this.value = 10;
            });
        }

        if (moodInput) {
            moodInput.addEventListener('input', function() {
                const value = parseInt(this.value);
                if (value < 0) this.value = 0;
                if (value > 10) this.value = 10;
            });
        }
        
        if (sleepInput) {
            sleepInput.addEventListener('input', function() {
                const value = parseFloat(this.value);
                if (value < 0) this.value = 0;
                if (value > 24) this.value = 24;
            });
        }
        
        // Smooth scroll to new entry after form submission
        if (window.location.hash === '#new-entry') {
            const entryFormCard = document.querySelector('.entry-form-card');
            if (entryFormCard) {
                entryFormCard.scrollIntoView({ 
                    behavior: 'smooth' 
                });
            }
        }
    }

    // UNIFIED SLIDER INITIALIZATION
    initializeAllSliders();

    // MODAL HANDLING
    initializeModalHandling();

    // CHARACTER COUNTERS
    addCharacterCounters();
});

function initializeAllSliders() {
    // Define all possible slider configurations
    const sliderConfigs = [
        // Dashboard sliders
        {
            sliderId: 'quickPainLevelSlider',
            valueId: 'painSliderValue',
            containerId: 'painSliderContainer',
            type: 'pain',
            min: 0,
            max: 10
        },
        {
            sliderId: 'quickMoodLevelSlider',
            valueId: 'moodSliderValue',
            containerId: 'moodSliderContainer',
            type: 'mood',
            min: 1,
            max: 10
        },
        // Detail form sliders
        {
            sliderId: 'painLevelSlider',
            valueId: 'detailPainSliderValue',
            containerId: 'detailPainSliderContainer',
            type: 'pain',
            min: 0,
            max: 10
        },
        {
            sliderId: 'moodLevelSlider',
            valueId: 'detailMoodSliderValue',
            containerId: null, // No container for detail mood slider
            type: 'mood',
            min: 1,
            max: 10
        }
    ];

    sliderConfigs.forEach(config => {
        initializeSlider(config);
    });
}

function initializeSlider(config) {
    const slider = document.getElementById(config.sliderId);
    const valueDisplay = document.getElementById(config.valueId);
    const container = config.containerId ? document.getElementById(config.containerId) : null;

    if (!slider || !valueDisplay) return;

    function updateSlider() {
        const value = parseInt(slider.value);
        valueDisplay.textContent = value;

        // Calculate position based on slider type
        let percent;
        if (config.type === 'mood' && config.min === 1) {
            percent = ((value - 1) / (config.max - config.min)) * 100;
        } else {
            percent = (value / config.max) * 100;
        }
        
        valueDisplay.style.left = percent + '%';

        // Apply color coding for pain sliders
        if (config.type === 'pain' && container) {
            updatePainColorCoding(container, value);
        }
    }

    slider.addEventListener('input', updateSlider);
    updateSlider(); // Initialize
}

function updatePainColorCoding(container, value) {
    // Remove existing classes
    container.classList.remove('pain-slider-0-2', 'pain-slider-3-5', 'pain-slider-6-8', 'pain-slider-9-10');
    
    // Add appropriate class based on value
    if (value <= 2) container.classList.add('pain-slider-0-2');
    else if (value <= 5) container.classList.add('pain-slider-3-5');
    else if (value <= 8) container.classList.add('pain-slider-6-8');
    else container.classList.add('pain-slider-9-10');
}

function initializeModalHandling() {
    // Handle entry cards modal - only on entries page
    const entryCards = document.querySelectorAll('.entry-card');
    
    if (entryCards.length > 0) {
        entryCards.forEach(card => {
            // Remove any Bootstrap data attributes to prevent conflicts
            card.removeAttribute('data-bs-toggle');
            card.removeAttribute('data-bs-target');
            
            // Add click event to the entire card
            card.addEventListener('click', function(e) {
                // Don't trigger if clicking on action buttons
                if (e.target.closest('.entry-actions')) {
                    return;
                }
                
                // Get data from the clicked card
                const entryId = this.getAttribute('data-entry-id');
                const location = this.getAttribute('data-location');
                const painLevel = this.getAttribute('data-pain-level');
                const moodLevel = this.getAttribute('data-mood-level');
                const sleepHours = this.getAttribute('data-sleep-hours');
                const triggers = this.getAttribute('data-triggers');
                const notes = this.getAttribute('data-notes');
                const createdAt = this.getAttribute('data-created-at');
                const updatedAt = this.getAttribute('data-updated-at');
                
                // Update modal content
                const modal = document.getElementById('readEntryModal');
                if (modal) {
                    document.getElementById('modalLocation').textContent = location;
                    document.getElementById('modalPainLevel').textContent = painLevel + '/10';
                    document.getElementById('modalMoodLevel').textContent = moodLevel + '/10';
                    document.getElementById('modalSleepHours').textContent = sleepHours + ' hours';
                    document.getElementById('modalTriggers').value = triggers || 'No triggers specified';
                    document.getElementById('modalNotes').value = notes || 'No additional notes';
                    document.getElementById('modalCreatedAt').textContent = createdAt;
                    document.getElementById('modalUpdatedAt').textContent = updatedAt; // Add this line
                    
                    // Update the Edit button URL dynamically
                    const editButton = document.getElementById('modalEditButton');
                    if (editButton && entryId) {
                        editButton.href = `/entries/edit/${entryId}/`;
                    }
                    
                    // Show the modal
                    const bootstrapModal = new bootstrap.Modal(modal);
                    bootstrapModal.show();
                }
            });
        });

        // Handle delete button hover state reset
        const deleteButtons = document.querySelectorAll('a[href*="delete"]');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                const entryCard = this.closest('.entry-card');
                const deleteUrl = this.getAttribute('href');
                
                if (confirm('Are you sure you want to delete this entry?')) {
                    window.location.href = deleteUrl;
                } else {
                    // Reset hover state cleanly
                    entryCard.blur();
                    setTimeout(() => {
                        entryCard.style.transform = '';
                        entryCard.style.boxShadow = '';
                        entryCard.style.borderColor = '';
                    }, 50);
                }
            });
        });
    }
}

function addCharacterCounters() {
    const triggersField = document.querySelector('textarea[name="triggers"]');
    const notesField = document.querySelector('textarea[name="notes"]');
    
    if (triggersField) {
        addCounter(triggersField, 300);
    }
    
    if (notesField) {
        addCounter(notesField, 1000);
    }
}

function addCounter(field, maxLength) {
    const counter = document.createElement('div');
    counter.className = 'character-counter text-muted small';
    counter.style.textAlign = 'right';
    
    function updateCounter() {
        const remaining = maxLength - field.value.length;
        counter.textContent = `${remaining} characters remaining`;
        
        if (remaining < 50) {
            counter.style.color = '#dc3545'; // Red warning
        } else {
            counter.style.color = '#6c757d'; // Normal gray
        }
    }
    
    field.addEventListener('input', updateCounter);
    field.parentNode.appendChild(counter);
    updateCounter(); // Initialize
}
