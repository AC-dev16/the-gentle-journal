from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.messages import get_messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import DiaryEntryForm, QuickEntryForm, ContactEmailForm
from .models import DiaryEntry, ContactEmail
import json

# Create your tests here.

class TestViews(TestCase):
    
    def setUp(self):
        """Set up test data for all test methods"""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com',
            first_name='Test'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123',
            email='other@test.com'
        )
        
        # Create test client
        self.client = Client()
        
        # Create test diary entries
        self.entry1 = DiaryEntry.objects.create(
            user=self.user,
            location='Test Location 1',
            pain_level=5,
            mood_level=7,
            sleep_hours=8.0,
            triggers='Test triggers 1',
            notes='Test notes 1'
        )
        
        self.entry2 = DiaryEntry.objects.create(
            user=self.user,
            location='Test Location 2',
            pain_level=3,
            mood_level=8,
            sleep_hours=7.5,
            triggers='Test triggers 2',
            notes='Test notes 2'
        )
        
        # Create entry for other user (to test user isolation)
        self.other_entry = DiaryEntry.objects.create(
            user=self.other_user,
            location='Other User Entry',
            pain_level=2,
            mood_level=9,
            sleep_hours=9.0,
            triggers='Other triggers',
            notes='Other notes'
        )
        
        # Test form data
        self.valid_entry_data = {
            'location': 'New Test Location',
            'pain_level': 6,
            'mood_level': 7,
            'sleep_hours': 8.5,
            'triggers': 'New test triggers',
            'notes': 'New test notes'
        }
        
        self.valid_quick_entry_data = {
            'location': 'Quick Entry Location',
            'pain_level': 4,
            'mood_level': 6
        }
        
        self.valid_contact_data = {
            'name': 'Test Contact',
            'email': 'contact@test.com',
            'message': 'Test contact message'
        }

class TestHomepageView(TestViews):
    """Test homepage view"""
    
    def test_homepage_loads_successfully(self):
        """Test homepage loads with status 200"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to')
        self.assertContains(response, 'The Gentle Journal')
    
    def test_homepage_uses_correct_template(self):
        """Test homepage uses correct template"""
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'diary_entries/homepage.html')
    
    def test_homepage_accessible_without_login(self):
        """Test homepage is accessible without authentication"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

class TestDashboardView(TestViews):
    """Test dashboard view"""
    
    def test_dashboard_requires_login(self):
        """Test dashboard redirects to login if user not authenticated"""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')
    
    def test_dashboard_loads_for_authenticated_user(self):
        """Test dashboard loads successfully for logged in user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Good')
        self.assertContains(response, 'Test')  # User's first name
    
    def test_dashboard_uses_correct_template(self):
        """Test dashboard uses correct template"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'diary_entries/dashboard.html')
    
    def test_dashboard_shows_user_entries(self):
        """Test dashboard displays user's recent entries"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Test Location 1')
        self.assertContains(response, 'Test Location 2')
        self.assertNotContains(response, 'Other User Entry')
    
    def test_dashboard_quick_entry_form(self):
        """Test quick entry form appears on dashboard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Quick Entry')
        self.assertIsInstance(response.context['form'], QuickEntryForm)
    
    def test_dashboard_quick_entry_submission(self):
        """Test quick entry form submission"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('dashboard'), self.valid_quick_entry_data)
        
        # Should redirect to dashboard after successful submission
        self.assertRedirects(response, reverse('dashboard'))
        
        # Check entry was created
        self.assertTrue(DiaryEntry.objects.filter(
            user=self.user,
            location='Quick Entry Location'
        ).exists())
    
    def test_dashboard_greeting_time_based(self):
        """Test dashboard shows time-appropriate greeting"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        # Should contain one of the time-based greetings
        greeting_found = any(greeting in response.content.decode() 
                           for greeting in ['morning', 'afternoon', 'evening'])
        self.assertTrue(greeting_found)

class TestEntryCreateView(TestViews):
    """Test entry create view"""
    
    def test_entry_create_requires_login(self):
        """Test entry create redirects to login if user not authenticated"""
        response = self.client.get(reverse('entry_create'))
        self.assertRedirects(response, '/accounts/login/?next=/entries/new/')
    
    def test_entry_create_get_loads_form(self):
        """Test entry create GET request loads empty form"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entry_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], DiaryEntryForm)
        self.assertFalse(response.context['form'].is_bound)
    
    def test_entry_create_uses_correct_template(self):
        """Test entry create uses correct template"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entry_create'))
        self.assertTemplateUsed(response, 'diary_entries/entry_details.html')
    
    def test_entry_create_post_valid_data(self):
        """Test entry creation with valid data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('entry_create'), self.valid_entry_data)
        
        # Should redirect to entries list after successful creation
        self.assertRedirects(response, reverse('entries'))
        
        # Check entry was created
        self.assertTrue(DiaryEntry.objects.filter(
            user=self.user,
            location='New Test Location'
        ).exists())
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Diary entry created successfully!')
    
    def test_entry_create_post_invalid_data(self):
        """Test entry creation with invalid data"""
        self.client.login(username='testuser', password='testpass123')
        invalid_data = self.valid_entry_data.copy()
        invalid_data['location'] = ''  # Required field
        
        response = self.client.post(reverse('entry_create'), invalid_data)
        
        # Should not redirect (stays on same page)
        self.assertEqual(response.status_code, 200)
        
        # Should not create entry
        self.assertFalse(DiaryEntry.objects.filter(
            location=''
        ).exists())

class TestEditEntryView(TestViews):
    """Test edit entry view"""
    
    def test_edit_entry_requires_login(self):
        """Test edit entry redirects to login if user not authenticated"""
        response = self.client.get(reverse('edit_entry', args=[self.entry1.id]))
        self.assertRedirects(response, f'/accounts/login/?next=/entries/edit/{self.entry1.id}/')
    
    def test_edit_entry_get_loads_form_with_data(self):
        """Test edit entry GET request loads form with existing data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_entry', args=[self.entry1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], DiaryEntryForm)
        self.assertEqual(response.context['entry'], self.entry1)
        self.assertContains(response, 'Test Location 1')
    
    def test_edit_entry_user_can_only_edit_own_entries(self):
        """Test user can only edit their own entries"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_entry', args=[self.other_entry.id]))
        self.assertEqual(response.status_code, 404)
    
    def test_edit_entry_post_valid_data(self):
        """Test editing entry with valid data"""
        self.client.login(username='testuser', password='testpass123')
        updated_data = self.valid_entry_data.copy()
        updated_data['location'] = 'Updated Location'
        
        response = self.client.post(reverse('edit_entry', args=[self.entry1.id]), updated_data)
        
        # Should redirect to entries list
        self.assertRedirects(response, reverse('entries'))
        
        # Check entry was updated
        self.entry1.refresh_from_db()
        self.assertEqual(self.entry1.location, 'Updated Location')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Diary entry updated successfully!')
    
    def test_edit_nonexistent_entry(self):
        """Test editing non-existent entry returns 404"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_entry', args=[99999]))
        self.assertEqual(response.status_code, 404)

class TestDeleteEntryView(TestViews):
    """Test delete entry view"""
    
    def test_delete_entry_requires_login(self):
        """Test delete entry redirects to login if user not authenticated"""
        response = self.client.get(reverse('delete_entry', args=[self.entry1.id]))
        self.assertRedirects(response, f'/accounts/login/?next=/entries/delete/{self.entry1.id}/')
    
    def test_delete_entry_success(self):
        """Test successful entry deletion"""
        self.client.login(username='testuser', password='testpass123')
        entry_id = self.entry1.id
        
        response = self.client.get(reverse('delete_entry', args=[entry_id]))
        
        # Should redirect to entries list
        self.assertRedirects(response, reverse('entries'))
        
        # Check entry was deleted
        self.assertFalse(DiaryEntry.objects.filter(id=entry_id).exists())
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Diary entry deleted successfully!')
    
    def test_delete_entry_user_can_only_delete_own_entries(self):
        """Test user can only delete their own entries"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('delete_entry', args=[self.other_entry.id]))
        self.assertEqual(response.status_code, 404)
        
        # Check other user's entry still exists
        self.assertTrue(DiaryEntry.objects.filter(id=self.other_entry.id).exists())
    
    def test_delete_nonexistent_entry(self):
        """Test deleting non-existent entry returns 404"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('delete_entry', args=[99999]))
        self.assertEqual(response.status_code, 404)

class TestEntryListView(TestViews):
    """Test entry list view (DiaryEntryListView)"""
    
    def test_entry_list_requires_login(self):
        """Test entry list redirects to login if user not authenticated"""
        response = self.client.get(reverse('entries'))
        self.assertRedirects(response, '/accounts/login/?next=/entries/')
    
    def test_entry_list_loads_successfully(self):
        """Test entry list loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entries'))
        self.assertEqual(response.status_code, 200)
    
    def test_entry_list_uses_correct_template(self):
        """Test entry list uses correct template"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entries'))
        self.assertTemplateUsed(response, 'diary_entries/entries.html')
    
    def test_entry_list_shows_only_user_entries(self):
        """Test entry list shows only current user's entries"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entries'))
        
        # Should contain user's entries
        self.assertContains(response, 'Test Location 1')
        self.assertContains(response, 'Test Location 2')
        
        # Should not contain other user's entries
        self.assertNotContains(response, 'Other User Entry')
    
    def test_entry_list_pagination(self):
        """Test entry list pagination functionality"""
        # Create additional entries to test pagination
        for i in range(12):  # More than paginate_by (10)
            DiaryEntry.objects.create(
                user=self.user,
                location=f'Location {i}',
                pain_level=5,
                mood_level=5,
                sleep_hours=8.0
            )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entries'))
        
        # Check pagination is working
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['entries']), 10)
    
    def test_entry_list_ordering(self):
        """Test entries are ordered by creation date (newest first)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entries'))
        
        entries = response.context['entries']
        # Should be ordered by -created_at
        for i in range(len(entries) - 1):
            self.assertGreaterEqual(entries[i].created_at, entries[i + 1].created_at)

class TestContactView(TestViews):
    """Test contact form view"""
    
    def test_contact_get_loads_form(self):
        """Test contact GET request loads empty form"""
        response = self.client.get(reverse('contact_email'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['contact_form'], ContactEmailForm)
    
    def test_contact_uses_correct_template(self):
        """Test contact uses correct template"""
        response = self.client.get(reverse('contact_email'))
        self.assertTemplateUsed(response, 'diary_entries/contact_form.html')
    
    def test_contact_accessible_without_login(self):
        """Test contact form is accessible without authentication"""
        response = self.client.get(reverse('contact_email'))
        self.assertEqual(response.status_code, 200)
    
    def test_contact_post_valid_data(self):
        """Test contact form submission with valid data"""
        response = self.client.post(reverse('contact_email'), self.valid_contact_data)
        
        # Should redirect to contact form after successful submission
        self.assertRedirects(response, reverse('contact_email'))
        
        # Check contact email was created
        self.assertTrue(ContactEmail.objects.filter(
            name='Test Contact',
            email='contact@test.com'
        ).exists())
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Your message has been received!', str(messages[0]))
    
    def test_contact_post_invalid_data(self):
        """Test contact form submission with invalid data"""
        invalid_data = self.valid_contact_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        response = self.client.post(reverse('contact_email'), invalid_data)
        
        # Should not redirect (stays on same page)
        self.assertEqual(response.status_code, 200)
        
        # Should not create contact email
        self.assertFalse(ContactEmail.objects.filter(
            name='Test Contact'
        ).exists())

class TestAnalyticsView(TestViews):
    """Test analytics view"""
    
    def test_analytics_requires_login(self):
        """Test analytics redirects to login if user not authenticated"""
        response = self.client.get(reverse('analytics'))
        self.assertRedirects(response, '/accounts/login/?next=/analytics/')
    
    def test_analytics_loads_successfully(self):
        """Test analytics loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
    
    def test_analytics_uses_correct_template(self):
        """Test analytics uses correct template"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics'))
        self.assertTemplateUsed(response, 'diary_entries/analytics.html')
    
    def test_analytics_context_data(self):
        """Test analytics view provides correct context data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics'))
        
        # Check required context variables
        self.assertIn('total_entries', response.context)
        self.assertIn('avg_pain', response.context)
        self.assertIn('avg_mood', response.context)
        self.assertIn('avg_sleep', response.context)
        
        # Check calculated values
        self.assertEqual(response.context['total_entries'], 2)  # User has 2 entries
        self.assertEqual(response.context['avg_pain'], 4.0)  # (5 + 3) / 2
        self.assertEqual(response.context['avg_mood'], 7.5)  # (7 + 8) / 2
        self.assertEqual(response.context['avg_sleep'], 7.8)  # (8.0 + 7.5) / 2 = 7.75, rounded to 7.8
    
    def test_analytics_with_no_entries(self):
        """Test analytics view with user who has no entries"""
        # Create user with no entries
        user_no_entries = User.objects.create_user(
            username='noentries',
            password='testpass123'
        )
        self.client.login(username='noentries', password='testpass123')
        response = self.client.get(reverse('analytics'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_entries'], 0)
        self.assertEqual(response.context['avg_pain'], 0)
        self.assertEqual(response.context['avg_mood'], 0)
        self.assertEqual(response.context['avg_sleep'], 0)

class TestAnalyticsDataAPIView(TestViews):
    """Test analytics data API view"""
    
    def test_analytics_api_requires_login(self):
        """Test analytics API redirects to login if user not authenticated"""
        response = self.client.get(reverse('analytics_data_api'))
        self.assertRedirects(response, '/accounts/login/?next=/api/analytics-data/')
    
    def test_analytics_api_returns_json(self):
        """Test analytics API returns JSON response"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics_data_api'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_analytics_api_default_period(self):
        """Test analytics API with default period (30 days)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics_data_api'))
        
        data = json.loads(response.content)
        
        # Check response structure
        self.assertIn('labels', data)
        self.assertIn('pain_data', data)
        self.assertIn('mood_data', data)
        self.assertIn('sleep_data', data)
        self.assertIn('entry_count', data)
        self.assertIn('date_range', data)
        
        # Check data values
        self.assertEqual(data['entry_count'], 2)
        self.assertEqual(len(data['pain_data']), 2)
        self.assertEqual(len(data['mood_data']), 2)
        self.assertEqual(len(data['sleep_data']), 2)
    
    def test_analytics_api_custom_period(self):
        """Test analytics API with custom period"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics_data_api') + '?days=7')
        
        data = json.loads(response.content)
        self.assertEqual(data['date_range']['days'], 7)
    
    def test_analytics_api_invalid_period(self):
        """Test analytics API with invalid period defaults to 30"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics_data_api') + '?days=invalid')
        
        data = json.loads(response.content)
        self.assertEqual(data['date_range']['days'], 30)
    
    def test_analytics_api_user_isolation(self):
        """Test analytics API only returns current user's data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics_data_api'))
        
        data = json.loads(response.content)
        
        # Should only show testuser's 2 entries, not other_user's 1 entry
        self.assertEqual(data['entry_count'], 2)
    
    def test_analytics_api_date_filtering(self):
        """Test analytics API filters entries by date range"""
        # Create an old entry (beyond 7 days)
        old_date = timezone.now() - timedelta(days=10)
        DiaryEntry.objects.create(
            user=self.user,
            location='Old Entry',
            pain_level=1,
            mood_level=1,
            sleep_hours=1.0,
            created_at=old_date
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        # Test 7-day filter
        response = self.client.get(reverse('analytics_data_api') + '?days=7')
        data = json.loads(response.content)
        
        # Should only include recent entries, not the old one
        self.assertEqual(data['entry_count'], 2)  # Only the 2 recent entries
    
    def test_analytics_api_empty_response(self):
        """Test analytics API with no entries in date range"""
        # Delete existing entries to ensure clean test
        DiaryEntry.objects.filter(user=self.user).delete()
        
        self.client.login(username='testuser', password='testpass123')
        
        # Request data for last 7 days when no entries exist
        response = self.client.get(reverse('analytics_data_api') + '?days=7')
        
        data = json.loads(response.content)
        self.assertEqual(data['entry_count'], 0)
        self.assertEqual(len(data['labels']), 0)
        self.assertEqual(len(data['pain_data']), 0)
        self.assertEqual(len(data['mood_data']), 0)
        self.assertEqual(len(data['sleep_data']), 0)

class TestViewPermissions(TestViews):
    """Test view permission and access control"""
    
    def test_authenticated_views_redirect_anonymous_users(self):
        """Test all authenticated views redirect anonymous users"""
        protected_urls = [
            reverse('dashboard'),
            reverse('entries'),
            reverse('entry_create'),
            reverse('edit_entry', args=[self.entry1.id]),
            reverse('delete_entry', args=[self.entry1.id]),
            reverse('analytics'),
            reverse('analytics_data_api'),
        ]
        
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)  # Redirect
                self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_public_views_accessible_to_anonymous_users(self):
        """Test public views are accessible without authentication"""
        public_urls = [
            reverse('homepage'),
            reverse('contact_email'),
        ]
        
        for url in public_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
