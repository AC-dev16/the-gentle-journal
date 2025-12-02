from django import forms
from .models import DiaryEntry, ContactEmail

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['location', 'pain_level', 'mood_level', 'sleep_hours', 'triggers', 'notes']
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
            })
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