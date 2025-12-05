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

    // BUILT-IN CHARACTER COUNTERS AND SPEECH BUTTONS
    initializeBuiltInControls();

    // SPEECH-TO-TEXT (if you still have the old version, remove it)
    // Remove the old setTimeout speech initialization
});

// Initialize built-in character counters and speech buttons
function initializeBuiltInControls() {
    initializeCharacterCounters();
    initializeSpeechButtons();
}

function initializeCharacterCounters() {
    const counters = document.querySelectorAll('.character-counter');
    
    counters.forEach(counter => {
        const maxLength = parseInt(counter.getAttribute('data-max'));
        const fieldContainer = counter.closest('.mb-3, .mb-4');
        const textarea = fieldContainer.querySelector('textarea');
        
        if (textarea && maxLength) {
            function updateCounter() {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = `${remaining} characters remaining`;
                
                // Add warning class when getting low
                if (remaining < 50) {
                    counter.classList.add('warning');
                } else {
                    counter.classList.remove('warning');
                }
            }
            
            textarea.addEventListener('input', updateCounter);
            updateCounter(); // Initialize
        }
    });
}

function initializeSpeechButtons() {
    // Initialize speech handler if not already done
    if (typeof speechHandler === 'undefined') {
        speechHandler = new ProgressiveSpeechHandler();
    }
    
    const speechButtons = document.querySelectorAll('.speech-btn');
    
    speechButtons.forEach(button => {
        const fieldContainer = button.closest('.mb-3, .mb-4');
        const textarea = fieldContainer.querySelector('textarea');
        
        if (!textarea) return;
        
        // Update button appearance based on support
        if (!speechHandler.hasSupport) {
            button.classList.add('speech-unsupported');
            button.innerHTML = '<i class="bi bi-keyboard"></i> <span class="btn-text d-none d-sm-inline ms-1">Type</span>';
            button.title = 'Add text (voice not supported)';
        }
        
        // Add click event listener - simplified
        button.addEventListener('click', function(e) {
            e.preventDefault();
            speechHandler.toggleListening(textarea, this);
        });
    });
}

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
        // Detailed form sliders
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
                    document.getElementById('modalUpdatedAt').textContent = updatedAt;
                    
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

        // REPLACE THE OLD DELETE BUTTON HANDLING WITH THIS NEW VERSION
        initializeDeleteModal();
    }
}

// NEW FUNCTION: Handle custom delete confirmation modal
function initializeDeleteModal() {
    const deleteButtons = document.querySelectorAll('.delete-entry-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Get entry information
            const deleteUrl = this.getAttribute('href');
            const entryLocation = this.getAttribute('data-entry-location');
            const entryDate = this.getAttribute('data-entry-date');
            
            // Update modal content with entry details
            const modal = document.getElementById('deleteConfirmModal');
            const modalBody = modal.querySelector('.modal-body p');
            modalBody.innerHTML = `Are you sure you want to delete your diary entry from <strong>${entryLocation}</strong> on <strong>${entryDate}</strong>?`;
            
            // Set the delete URL on the confirm button
            const confirmButton = document.getElementById('confirmDeleteButton');
            confirmButton.href = deleteUrl;
            
            // Show the custom modal
            const deleteModal = new bootstrap.Modal(modal);
            deleteModal.show();
        });
    });
}

// Enhanced speech handler with better state management
class ProgressiveSpeechHandler {
    constructor() {
        this.hasSupport = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
        this.isListening = false;
        this.currentField = null;
        this.activeButton = null;
        this.activeFieldContainer = null;
        
        if (this.hasSupport) {
            this.initializeRecognition();
        }
    }
    
    initializeRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateActiveButton();
            this.updateVisualFeedback();
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            this.updateActiveButton();
            this.updateVisualFeedback();
            this.resetActiveState();
        };
        
        this.recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            this.isListening = false;
            this.updateActiveButton();
            this.updateVisualFeedback();
            this.resetActiveState();
        };
        
        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript + ' ';
                }
            }
            
            if (this.currentField && finalTranscript.trim()) {
                const currentText = this.currentField.value;
                this.currentField.value = currentText ? currentText + ' ' + finalTranscript.trim() : finalTranscript.trim();
                this.currentField.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };
    }
    
    toggleListening(field, button) {
        // Only proceed if speech is supported
        if (!this.hasSupport) {
            return;
        }
        
        // If already listening to a different field, stop first
        if (this.isListening && this.activeButton !== button) {
            this.recognition.stop();
            return;
        }
        
        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.currentField = field;
            this.activeButton = button;
            this.activeFieldContainer = button.closest('.mb-3, .mb-4');
            this.recognition.start();
        }
    }
    
    updateActiveButton() {
        if (!this.activeButton) return;
        
        const icon = this.activeButton.querySelector('i');
        const text = this.activeButton.querySelector('.btn-text');
        
        if (this.isListening) {
            this.activeButton.classList.add('listening');
            this.activeButton.title = 'Stop recording';
            icon.className = 'fa-solid fa-microphone-slash';
            if (text) text.textContent = 'Stop Recording';
        } else {
            this.activeButton.classList.remove('listening');
            this.activeButton.title = 'Start voice input';
            icon.className = 'fa-solid fa-microphone';
            if (text) text.textContent = 'Start Recording';
        }
    }
    
    resetActiveState() {
        this.activeButton = null;
        this.activeFieldContainer = null;
        this.currentField = null;
    }
}

// Initialize speech handler
let speechHandler;
