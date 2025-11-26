from django.shortcuts import render
from django.contrib import messages
from django.views import generic
from datetime import datetime
from .models import DiaryEntry

# Create your views here.
def homepage(request):
    """Homepage with site information and auth buttons"""
    return render(request, 'diary_entries/homepage.html')

class DiaryEntryListView(generic.ListView):
    queryset = DiaryEntry.objects.order_by('-created_at')
    template_name = 'diary_entries/entries.html'
    paginate_by = 10

def dashboard(request):
    """User dashboard showing personalized data"""
    user_entries = DiaryEntry.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'entries': user_entries,
        'user': request.user,
    }
    return render(request, 'diary_entries/dashboard.html', context)