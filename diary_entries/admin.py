from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import DiaryEntry, ContactEmail


# Register your models here.
@admin.register(DiaryEntry)
class Admin(SummernoteModelAdmin):
    list_display = ('user',
                    'location',
                    'pain_level',
                    'mood_level',
                    'sleep_hours',
                    'created_at')
    search_fields = ['user__username', 'created_at']
    list_filter = ('created_at', 'user__username')
    summernote_fields = ('notes', 'triggers')


@admin.register(ContactEmail)
class ContactEmailAdmin(admin.ModelAdmin):

    list_display = ('message', 'read',)
