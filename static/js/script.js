document.addEventListener('DOMContentLoaded', function() {
    // Only run on pages with diary entry forms
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

    // SINGLE MODAL HANDLING APPROACH
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
                const location = this.getAttribute('data-location');
                const painLevel = this.getAttribute('data-pain-level');
                const moodLevel = this.getAttribute('data-mood-level');
                const sleepHours = this.getAttribute('data-sleep-hours');
                const triggers = this.getAttribute('data-triggers');
                const notes = this.getAttribute('data-notes');
                const createdAt = this.getAttribute('data-created-at');
                
                // Update modal content
                const modal = document.getElementById('readEntryModal');
                if (modal) {
                    document.getElementById('modalLocation').textContent = location;
                    document.getElementById('modalPainLevel').textContent = painLevel + '/10';
                    document.getElementById('modalMoodLevel').textContent = moodLevel + '/10';
                    document.getElementById('modalSleepHours').textContent = sleepHours + ' hours';
                    document.getElementById('modalTriggers').textContent = triggers;
                    document.getElementById('modalNotes').textContent = notes;
                    document.getElementById('modalCreatedAt').textContent = createdAt;
                    
                    // Show the modal
                    const bootstrapModal = new bootstrap.Modal(modal);
                    bootstrapModal.show();
                }
            });
        });
    }
});
