from django.shortcuts import render
from django.views import generic
from .models import DiaryEntry

# Create your views here.
def homepage(request):
    """Homepage with site information and auth buttons"""
    return render(request, 'diary_entries/homepage.html')

class DiaryEntryListView(generic.ListView):
    model = DiaryEntry
    template_name = 'diary_entries/entries.html'
    
