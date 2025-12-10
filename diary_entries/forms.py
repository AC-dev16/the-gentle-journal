from django import forms
from django.forms.widgets import NumberInput
from .models import DiaryEntry, ContactEmail


class RangeInput(NumberInput):
    input_type = 'range'

    def build_attrs(self, base_attrs, extra_attrs=None):
        # Build the attributes normally
        attrs = super().build_attrs(base_attrs, extra_attrs)
        # Remove the required attribute for range inputs
        attrs.pop('required', None)
        return attrs


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
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where is your pain today?',
                'maxlength': '25'
            }),
            'pain_level': RangeInput(attrs={  # ← Use custom widget
                'min': 0,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'id': 'painLevelSlider'
            }),
            'mood_level': RangeInput(attrs={  # ← Use custom widget
                'min': 1,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'id': 'moodLevelSlider'
            }),
            'sleep_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.5,
                'min': 0,
                'max': 24
            }),
            'triggers': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': 300,
                'placeholder': 'What triggered your pain today?'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': 1000,
                'placeholder': 'Additional notes about your day...'
            }),
        }


class QuickEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['location', 'pain_level', 'mood_level']
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where is your pain today?',
                'maxlength': '25'
            }),
            'pain_level': RangeInput(attrs={  # ← Use custom widget
                'min': 0,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'id': 'quickPainLevelSlider'
            }),
            'mood_level': RangeInput(attrs={  # ← Use custom widget
                'min': 1,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'id': 'quickMoodLevelSlider'
            }),
        }


class ContactEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ('name', 'email', 'message',)
