from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.messages import get_messages
from django.utils import timezone
from datetime import timedelta
from .forms import DiaryEntryForm, QuickEntryForm, ContactEmailForm
from .models import DiaryEntry, ContactEmail
import json

# Create your tests here.

class TestKeyViewFunctionality(TestCase):
    """Test key functionality of all views without complex data dependencies"""
    
    def setUp(self):
        """Set up basic test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test'
        )
        
        # Create a basic entry for testing
        self.entry = DiaryEntry.objects.create(
            user=self.user,
            location='Test Location',
            pain_level=5,
            mood_level=7,
            sleep_hours=8.0,
            triggers='Test triggers',
            notes='Test notes'
        )

    # Homepage Tests
    def test_homepage_loads(self):
        """Test homepage loads successfully"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to')

    def test_homepage_accessible_without_login(self):
        """Test homepage works without authentication"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    # Dashboard Tests
    def test_dashboard_requires_login(self):
        """Test dashboard redirects unauthenticated users"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_dashboard_loads_for_authenticated_user(self):
        """Test dashboard loads for logged-in users"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Good')
        self.assertContains(response, 'Test')

    def test_dashboard_quick_entry_creation(self):
        """Test quick entry form submission works"""
        self.client.login(username='testuser', password='testpass123')
        
        quick_entry_data = {
            'location': 'Quick Location',
            'pain_level': 3,
            'mood_level': 8
        }
        
        response = self.client.post(reverse('dashboard'), quick_entry_data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Verify entry was created
        self.assertTrue(DiaryEntry.objects.filter(
            user=self.user,
            location='Quick Location'
        ).exists())

    # Entry Creation Tests
    def test_entry_create_requires_login(self):
        """Test entry creation requires authentication"""
        response = self.client.get(reverse('entry_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_entry_create_loads_form(self):
        """Test entry creation form loads"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entry_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], DiaryEntryForm)

    def test_entry_create_success(self):
        """Test successful entry creation"""
        self.client.login(username='testuser', password='testpass123')
        
        entry_data = {
            'location': 'New Location',
            'pain_level': 6,
            'mood_level': 5,
            'sleep_hours': 7.5,
            'triggers': 'New triggers',
            'notes': 'New notes'
        }
        
        response = self.client.post(reverse('entry_create'), entry_data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Verify entry was created
        self.assertTrue(DiaryEntry.objects.filter(
            user=self.user,
            location='New Location'
        ).exists())

    # Entry List Tests
    def test_entry_list_requires_login(self):
        """Test entry list requires authentication"""
        response = self.client.get(reverse('entries'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_entry_list_shows_user_entries(self):
        """Test entry list shows user's entries only"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entries'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Location')

    def test_entry_list_hides_other_user_entries(self):
        """Test entry list doesn't show other users' entries"""
        # Create another user and entry
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        DiaryEntry.objects.create(
            user=other_user,
            location='Other User Location',
            pain_level=1,
            mood_level=1,
            sleep_hours=1.0
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entries'))
        
        # Should see own entry
        self.assertContains(response, 'Test Location')
        # Should not see other user's entry
        self.assertNotContains(response, 'Other User Location')

    # Entry Edit Tests
    def test_entry_edit_requires_login(self):
        """Test entry editing requires authentication"""
        response = self.client.get(reverse('edit_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_entry_edit_loads_existing_data(self):
        """Test edit form loads with existing entry data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Location')

    def test_entry_edit_success(self):
        """Test successful entry update"""
        self.client.login(username='testuser', password='testpass123')
        
        updated_data = {
            'location': 'Updated Location',
            'pain_level': 8,
            'mood_level': 4,
            'sleep_hours': 6.0,
            'triggers': 'Updated triggers',
            'notes': 'Updated notes'
        }
        
        response = self.client.post(reverse('edit_entry', args=[self.entry.id]), updated_data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Verify entry was updated
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.location, 'Updated Location')

    def test_user_cannot_edit_other_users_entries(self):
        """Test users cannot edit other users' entries"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        other_entry = DiaryEntry.objects.create(
            user=other_user,
            location='Other Location',
            pain_level=1,
            mood_level=1,
            sleep_hours=1.0
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_entry', args=[other_entry.id]))
        self.assertEqual(response.status_code, 404)

    # Entry Delete Tests
    def test_entry_delete_requires_login(self):
        """Test entry deletion requires authentication"""
        response = self.client.get(reverse('delete_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_entry_delete_success(self):
        """Test successful entry deletion"""
        self.client.login(username='testuser', password='testpass123')
        entry_id = self.entry.id
        
        response = self.client.get(reverse('delete_entry', args=[entry_id]))
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Verify entry was deleted
        self.assertFalse(DiaryEntry.objects.filter(id=entry_id).exists())

    def test_user_cannot_delete_other_users_entries(self):
        """Test users cannot delete other users' entries"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        other_entry = DiaryEntry.objects.create(
            user=other_user,
            location='Other Location',
            pain_level=1,
            mood_level=1,
            sleep_hours=1.0
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('delete_entry', args=[other_entry.id]))
        self.assertEqual(response.status_code, 404)
        
        # Verify entry still exists
        self.assertTrue(DiaryEntry.objects.filter(id=other_entry.id).exists())

    # Contact Form Tests
    def test_contact_form_loads(self):
        """Test contact form loads without authentication"""
        response = self.client.get(reverse('contact_email'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['contact_form'], ContactEmailForm)

    def test_contact_form_submission(self):
        """Test contact form submission works"""
        contact_data = {
            'name': 'Test Contact',
            'email': 'contact@test.com',
            'message': 'Test message'
        }
        
        response = self.client.post(reverse('contact_email'), contact_data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Verify contact was saved
        self.assertTrue(ContactEmail.objects.filter(
            name='Test Contact',
            email='contact@test.com'
        ).exists())

    # Analytics Tests
    def test_analytics_requires_login(self):
        """Test analytics requires authentication"""
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_analytics_loads_for_authenticated_user(self):
        """Test analytics loads for logged-in users"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
        
        # Check basic context variables exist
        self.assertIn('total_entries', response.context)
        self.assertIn('avg_pain', response.context)
        self.assertIn('avg_mood', response.context)
        self.assertIn('avg_sleep', response.context)

    def test_analytics_api_requires_login(self):
        """Test analytics API requires authentication"""
        response = self.client.get(reverse('analytics_data_api'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_analytics_api_returns_json(self):
        """Test analytics API returns JSON data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('analytics_data_api'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Verify JSON structure
        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('pain_data', data)
        self.assertIn('mood_data', data)
        self.assertIn('sleep_data', data)
        self.assertIn('entry_count', data)

    # Message Testing
    def test_success_messages_work(self):
        """Test success messages appear after actions"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test entry creation message
        entry_data = {
            'location': 'Message Test',
            'pain_level': 5,
            'mood_level': 5,
            'sleep_hours': 8.0
        }
        
        response = self.client.post(reverse('entry_create'), entry_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully' in str(m) for m in messages))

    # Template Testing
    def test_views_use_correct_templates(self):
        """Test views use the correct templates"""
        # Homepage
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'diary_entries/homepage.html')
        
        # Contact
        response = self.client.get(reverse('contact_email'))
        self.assertTemplateUsed(response, 'diary_entries/contact_form.html')
        
        # Authenticated views
        self.client.login(username='testuser', password='testpass123')
        
        # Dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'diary_entries/dashboard.html')
        
        # Entries
        response = self.client.get(reverse('entries'))
        self.assertTemplateUsed(response, 'diary_entries/entries.html')
        
        # Analytics
        response = self.client.get(reverse('analytics'))
        self.assertTemplateUsed(response, 'diary_entries/analytics.html')

class TestFormIntegrationWithViews(TestCase):
    """Test form integration with views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='formtestuser',
            password='testpass123'
        )

    def test_invalid_form_submission_shows_errors(self):
        """Test invalid form submissions show appropriate errors"""
        self.client.login(username='formtestuser', password='testpass123')
        
        # Submit invalid entry (missing required fields)
        invalid_data = {
            'location': '',  # Required field
            'pain_level': '',  # Required field
            'mood_level': '',  # Required field
        }
        
        response = self.client.post(reverse('entry_create'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Should stay on page
        self.assertFormError(response, 'form', 'location', 'This field is required.')

    def test_form_field_validation_in_views(self):
        """Test form field validation works through views"""
        self.client.login(username='formtestuser', password='testpass123')
        
        # Test with data that's too long
        invalid_data = {
            'location': 'a' * 30,  # Over 25 character limit
            'pain_level': 5,
            'mood_level': 5,
            'sleep_hours': 8.0
        }
        
        response = self.client.post(reverse('entry_create'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Should stay on page
        # Form should not be valid
        self.assertFalse(response.context['form'].is_valid())

class TestUserDataSecurity(TestCase):
    """Test user data security and isolation"""
    
    def setUp(self):
        self.client = Client()
        
        # Create two users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='testpass123'
        )
        
        # Create entries for each user
        self.user1_entry = DiaryEntry.objects.create(
            user=self.user1,
            location='User1 Location',
            pain_level=1,
            mood_level=1,
            sleep_hours=1.0
        )
        
        self.user2_entry = DiaryEntry.objects.create(
            user=self.user2,
            location='User2 Location', 
            pain_level=2,
            mood_level=2,
            sleep_hours=2.0
        )

    def test_user_data_isolation_in_analytics(self):
        """Test analytics only shows current user's data"""
        # Login as user1
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('analytics_data_api'))
        
        data = json.loads(response.content)
        
        # Should only see user1's data
        self.assertEqual(data['entry_count'], 1)
        self.assertEqual(data['pain_data'][0], 1)  # user1's pain level
        
        # Login as user2
        self.client.logout()
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('analytics_data_api'))
        
        data = json.loads(response.content)
        
        # Should only see user2's data
        self.assertEqual(data['entry_count'], 1)
        self.assertEqual(data['pain_data'][0], 2)  # user2's pain level

    def test_dashboard_shows_only_user_entries(self):
        """Test dashboard only shows current user's entries"""
        # Login as user1
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        # Should see user1's entry
        self.assertContains(response, 'User1 Location')
        # Should not see user2's entry
        self.assertNotContains(response, 'User2 Location')