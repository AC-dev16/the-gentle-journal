from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from datetime import datetime
from .forms import DiaryEntryForm, QuickEntryForm
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
    if request.method == 'POST':
        form = QuickEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.mood_level = entry.mood_level or 'Not specified'
            entry.sleep_hours = entry.sleep_hours or 0
            entry.save()
            messages.success(request, 'Quick entry added successfully!')
            return redirect('dashboard')
    else:
        form = QuickEntryForm()

    user_entries = DiaryEntry.objects.filter(user=request.user).order_by('-created_at')[:3]

    # Determine greeting based on time of day
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "morning"
    elif current_hour < 18:
        greeting = "afternoon"
    else:
        greeting = "evening"

    context = {
        'form': form,
        'entries': user_entries,
        'user': request.user,
        'greeting': greeting,
    }

    return render(request, 'diary_entries/dashboard.html', context)

def entry_create(request):
    """Create a new diary entry"""
    if request.method == 'POST':
        # Process form data here
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Diary entry created successfully!')
            return redirect('entries')
    else:
        form = DiaryEntryForm()

    # Get all user's entries
    entries = DiaryEntry.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'diary_entries/entry_form.html', {'form': form, 'entries': entries})