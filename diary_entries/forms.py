from django import forms
from .models import DiaryEntry

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['location', 'pain_level', 'mood_level', 'sleep_hours', 'triggers', 'notes']
        

class QuickEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['location', 'pain_level', 'mood_level']