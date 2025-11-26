from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    location = models.CharField(max_length=100)
    pain_level = models.IntegerField()
    mood_level = models.IntegerField()
    sleep_hours = models.IntegerField()
    triggers = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Diary Entry by {self.user.username}"
    
