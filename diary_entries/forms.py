from django import forms
from .models import DiaryEntry, ContactEmail


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = [
            'location',
            'pain_level',
            'mood_level',
            'sleep_hours',
            'triggers',
            'notes'
            ]
        widgets = {
            'pain_level': forms.NumberInput(attrs={
                'type': 'range',
                'min': 0,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'id': 'painLevelSlider'
            }),
            'mood_level': forms.NumberInput(attrs={
                'type': 'range',
                'min': 1,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'id': 'moodLevelSlider'
            }),
            'triggers': forms.Textarea(attrs={
                'rows': 5,
                'maxlength': 300,
                'class': 'form-control',
                'placeholder': 'What triggered your pain today? (max: 300 characters)'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 5,
                'maxlength': 1000,
                'class': 'form-control',
                'placeholder': 'Additional notes about your condition... (max: 1000 characters)'
            })
        }

        # Remove help_texts to eliminate hint elements
        help_texts = {
            'triggers': '',
            'notes': '',
        }


class QuickEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['location', 'pain_level', 'mood_level']
        widgets = {
            'pain_level': forms.NumberInput(attrs={
                'type': 'range',
                'min': 0,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'id': 'quickPainLevelSlider'
            }),
            'mood_level': forms.NumberInput(attrs={
                'type': 'range',
                'min': 1,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'id': 'quickMoodLevelSlider'
            })
        }


class ContactEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ('name', 'email', 'message',)
