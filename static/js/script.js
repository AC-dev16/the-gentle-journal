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