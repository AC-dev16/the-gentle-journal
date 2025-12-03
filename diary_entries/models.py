from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    location = models.CharField(max_length=25)
    pain_level = models.IntegerField()
    mood_level = models.IntegerField()
    sleep_hours = models.IntegerField()
    triggers = models.TextField(
        max_length=300, 
        blank=True, 
        null=True,
        help_text="Describe any triggers that may have affected your pain (max 300 characters)"
    )
    notes = models.TextField(
        max_length=1000, 
        blank=True, 
        null=True,
        help_text="Additional notes about your condition and wellbeing (max 1000 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        super().clean()
        if self.triggers and len(self.triggers) > 300:
            raise ValidationError({'triggers': 'Triggers field cannot exceed 300 characters.'})
        if self.notes and len(self.notes) > 1000:
            raise ValidationError({'notes': 'Notes field cannot exceed 1000 characters.'})

    def __str__(self):
        return f"Diary Entry by {self.user.username}"
    
class ContactEmail(models.Model):
    """
    Stores email enquiries from users.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Enquiry from {self.name}"