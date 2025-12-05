from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Avg, Count
from django.utils import timezone
from .forms import DiaryEntryForm, QuickEntryForm, ContactEmailForm
from .models import DiaryEntry, ContactEmail

# Create your views here.
def homepage(request):
    """Homepage with site information and auth buttons"""
    return render(request, 'diary_entries/homepage.html')

def contact(request):
    """
    Contact page with enquires form

    **Context**
    ''contact_form''
        An instance of :form: 'diary_entries.ContactEmailForm'.

    **Template**
        :template:'diary_entries/contact_form.html'.
    """

    if request.method == "POST":
        contact_form = ContactEmailForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your message has been received! I endeavour to respond within 2 working days.'
            )
            return redirect('contact_email')  # Redirect after successful submission
    else:
        contact_form = ContactEmailForm()

    return render(request, 'diary_entries/contact_form.html', {'contact_form': contact_form})

class DiaryEntryListView(generic.ListView):
    model = DiaryEntry
    template_name = 'diary_entries/entry_details.html'
    context_object_name = 'entries'
    paginate_by = 10
    
    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user).order_by('-created_at')

# User dashboard view with quick entry form
@login_required
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
        greeting_message = "Hope you're having a great start to your day!"
    elif current_hour < 18:
        greeting = "afternoon"
        greeting_message = "Hope your day is going well!"
    else:
        greeting = "evening"
        greeting_message = "Hope you've had a wonderful day!"

    context = {
        'form': form,
        'entries': user_entries,
        'user': request.user,
        'greeting': greeting,
        'greeting_message': greeting_message,
    }

    return render(request, 'diary_entries/dashboard.html', context)

# Create a new diary entry
@login_required
def entry_create(request):
    """Create a new diary entry"""
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Diary entry created successfully!')
            return redirect('entries')
    else:
        form = DiaryEntryForm()

    return render(request, 'diary_entries/entry_details.html', {'form': form})

# Edit an existing diary entry
@login_required
def edit_entry(request, entry_id):
    """Edit a diary entry belonging to the current user"""
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Diary entry updated successfully!')
            return redirect('entries')
        else:
            messages.error(request, 'Error updating entry.')
    else:
        form = DiaryEntryForm(instance=entry)

    return render(request, 'diary_entries/entry_details.html', {'form': form, 'entry': entry})

# List all entries
@login_required
def entry_list(request):
    """List all user entries"""
    entries = DiaryEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'diary_entries/entries.html', {'entries': entries})

# Delete an entry
@login_required
def delete_entry(request, entry_id):
    """Delete a diary entry"""
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    entry.delete()
    messages.success(request, 'Diary entry deleted successfully!')
    return redirect('entries')

@login_required
def analytics_view(request):
    """Analytics dashboard with interactive charts"""
    user_entries = DiaryEntry.objects.filter(user=request.user).order_by('-created_at')
    
    # Basic statistics
    total_entries = user_entries.count()
    avg_pain = user_entries.aggregate(avg_pain=Avg('pain_level'))['avg_pain'] or 0
    avg_mood = user_entries.aggregate(avg_mood=Avg('mood_level'))['avg_mood'] or 0
    avg_sleep = user_entries.aggregate(avg_sleep=Avg('sleep_hours'))['avg_sleep'] or 0
    
    context = {
        'total_entries': total_entries,
        'avg_pain': round(avg_pain, 1),
        'avg_mood': round(avg_mood, 1),
        'avg_sleep': round(avg_sleep, 1),
    }
    
    return render(request, 'diary_entries/analytics.html', context)

@login_required
def analytics_data_api(request):
    """API endpoint for chart data with date filtering"""
    days = request.GET.get('days', '30')  # Default to 30 days
    
    try:
        days_int = int(days)
    except ValueError:
        days_int = 30
    
    # Calculate date range
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days_int)
    
    # Get user entries within date range
    user_entries = DiaryEntry.objects.filter(
        user=request.user,
        created_at__gte=start_date,
        created_at__lte=end_date
    ).order_by('created_at')
    
    # Prepare chart data
    chart_data = {
        'labels': [],
        'pain_data': [],
        'mood_data': [],
        'sleep_data': [],
        'entry_count': user_entries.count(),
        'date_range': {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'days': days_int
        }
    }
    
    # Format data for charts
    for entry in user_entries:
        chart_data['labels'].append(entry.created_at.strftime('%m/%d'))
        chart_data['pain_data'].append(entry.pain_level)
        chart_data['mood_data'].append(entry.mood_level)
        chart_data['sleep_data'].append(entry.sleep_hours)
    
    return JsonResponse(chart_data)