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
        const moodInput = document.querySelector('input[name="mood_level"');
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
});

// Read entry modal
    const readEntryModal = document.getElementById('readEntryModal');
    
    if (readEntryModal) {
        readEntryModal.addEventListener('show.bs.modal', function(event) {
            // Get the clicked entry card
            const clickedCard = event.relatedTarget;
            
            // Extract data from data attributes
            const location = clickedCard.getAttribute('data-location');
            const painLevel = clickedCard.getAttribute('data-pain-level');
            const moodLevel = clickedCard.getAttribute('data-mood-level');
            const sleepHours = clickedCard.getAttribute('data-sleep-hours');
            const triggers = clickedCard.getAttribute('data-triggers');
            const notes = clickedCard.getAttribute('data-notes');
            const createdAt = clickedCard.getAttribute('data-created-at');
            
            // Update modal content
            document.getElementById('modalLocation').textContent = location;
            document.getElementById('modalPainLevel').textContent = painLevel + '/10';
            document.getElementById('modalMoodLevel').textContent = moodLevel + '/10';
            document.getElementById('modalSleepHours').textContent = sleepHours + ' hours';
            document.getElementById('modalTriggers').textContent = triggers;
            document.getElementById('modalNotes').textContent = notes;
            document.getElementById('modalCreatedAt').textContent = createdAt;
        });
    };
