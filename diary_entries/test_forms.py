from django.test import TestCase
from .forms import DiaryEntryForm, QuickEntryForm, ContactEmailForm


# Create your tests here.

class TestDiaryEntryForm(TestCase):

    # Validation tests
    def test_form_is_valid(self):
        """ Test for all fields """
        entry_form = DiaryEntryForm({
            'location': 'location',
            'pain_level': '5',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': 'This is a note',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid(self):
        """ Test for all fields """
        entry_form = DiaryEntryForm({
            'location': '',
            'pain_level': '',
            'mood_level': '',
            'sleep_hours': '',
            'triggers': '',
            'notes': '',
        })
        self.assertFalse(entry_form.is_valid(), msg="Form is valid")

    # Required test
    def test_location_is_required(self):
        """ Test for required location """
        entry_form = DiaryEntryForm({
            'location': '',
            'pain_level': '5',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': 'This is a note',
        })
        self.assertFalse(entry_form.is_valid(), msg='Form is not valid')

    # Boundary tests
    def test_pain_level_min_boundary(self):
        """ Test pain level minimum boundary (0) """
        entry_form = DiaryEntryForm({
            'location': 'home',
            'pain_level': '0',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': 'This is a note',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with pain level 0')

    def test_pain_level_max_boundary(self):
        """ Test pain level maximum boundary (10) """
        entry_form = DiaryEntryForm({
            'location': 'home',
            'pain_level': '10',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': 'This is a note',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with pain level 10')

    def test_mood_level_min_boundary(self):
        """ Test mood level minimum boundary (1) """
        entry_form = DiaryEntryForm({
            'location': 'home',
            'pain_level': '5',
            'mood_level': '1',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': 'This is a note',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with mood level 1')

    def test_mood_level_max_boundary(self):
        """ Test mood level maximum boundary (10) """
        entry_form = DiaryEntryForm({
            'location': 'home',
            'pain_level': '5',
            'mood_level': '10',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': 'This is a note',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with mood level 10')

    # Max character length tests
    def test_location_max_length(self):
        """ Test location field respects max length of 25 characters """
        long_location = 'a' * 26  # 26 characters - should be invalid
        entry_form = DiaryEntryForm({
            'location': long_location,
            'pain_level': '5',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': 'This is a note',
        })
        self.assertFalse(entry_form.is_valid(), msg='Form should be invalid with location longer than 25 characters')

    def test_location_valid_length(self):
        """ Test location field accepts valid length """
        valid_location = 'a' * 25  # 25 characters - should be valid
        entry_form = DiaryEntryForm({
            'location': valid_location,
            'pain_level': '5',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': 'This is a note',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with location at max length')

    def test_triggers_max_length(self):
        """ Test triggers field respects max length of 300 characters """
        long_triggers = 'a' * 301  # 301 characters - should be invalid
        entry_form = DiaryEntryForm({
            'location': 'home',
            'pain_level': '5',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': long_triggers,
            'notes': 'This is a note',
        })
        self.assertFalse(entry_form.is_valid(), msg='Form should be invalid with triggers longer than 300 characters')

    def test_triggers_valid_length(self):
        """ Test triggers field accepts valid length """
        valid_triggers = 'a' * 300  # 300 characters - should be valid
        entry_form = DiaryEntryForm({
            'location': 'home',
            'pain_level': '5',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': valid_triggers,
            'notes': 'This is a note',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with triggers at max length')

    def test_notes_max_length(self):
        """ Test notes field respects max length of 1000 characters """
        long_notes = 'a' * 1001  # 1001 characters - should be invalid
        entry_form = DiaryEntryForm({
            'location': 'home',
            'pain_level': '5',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': long_notes,
        })
        self.assertFalse(entry_form.is_valid(), msg='Form should be invalid with notes longer than 1000 characters')

    def test_notes_valid_length(self):
        """ Test notes field accepts valid length """
        valid_notes = 'a' * 1000  # 1000 characters - should be valid
        entry_form = DiaryEntryForm({
            'location': 'home',
            'pain_level': '5',
            'mood_level': '8',
            'sleep_hours': '9',
            'triggers': 'none',
            'notes': valid_notes,
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with notes at max length')


class TestQuickEntryForm(TestCase):

    # Validation tests
    def test_form_is_valid(self):
        """ Test for all fields """
        entry_form = QuickEntryForm({
            'location': 'location',
            'pain_level': '5',
            'mood_level': '4',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid(self):
        """ Test for all fields """
        entry_form = QuickEntryForm({
            'location': '',
            'pain_level': '',
            'mood_level': '',
        })
        self.assertFalse(entry_form.is_valid(), msg="Location was not provided, but the form is valid")

    # Required test
    def test_location_is_required(self):
        """ Test location field is required """
        entry_form = QuickEntryForm({
            'location': '',
            'pain_level': '5',
            'mood_level': '4',
        })
        self.assertFalse(entry_form.is_valid(), msg="Location was not provided, but the form is valid")

    # Boundary tests
    def test_pain_level_boundaries(self):
        """ Test pain level accepts valid range 0-10 """
        # Test minimum
        entry_form = QuickEntryForm({
            'location': 'home',
            'pain_level': '0',
            'mood_level': '4',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with pain level 0')

        # Test maximum
        entry_form = QuickEntryForm({
            'location': 'home',
            'pain_level': '10',
            'mood_level': '4',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with pain level 10')

    def test_mood_level_boundaries(self):
        """ Test mood level accepts valid range 1-10 """
        # Test minimum
        entry_form = QuickEntryForm({
            'location': 'home',
            'pain_level': '5',
            'mood_level': '1',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with mood level 1')

        # Test maximum
        entry_form = QuickEntryForm({
            'location': 'home',
            'pain_level': '5',
            'mood_level': '10',
        })
        self.assertTrue(entry_form.is_valid(), msg='Form should be valid with mood level 10')

    # Max character length test
    def test_location_max_length(self):
        """ Test location field respects max length of 25 characters """
        long_location = 'a' * 26  # 26 characters - should be invalid
        entry_form = QuickEntryForm({
            'location': long_location,
            'pain_level': '5',
            'mood_level': '4',
        })
        self.assertFalse(entry_form.is_valid(), msg='Form should be invalid with location longer than 25 characters')


class TestContactEmailForm(TestCase):

    # Validation tests
    def test_form_is_valid(self):
        """ Test for all fields """
        contact_form = ContactEmailForm({
            'name': 'John',
            'email': 'test@test.com',
            'message': 'This is a message',
        })
        self.assertTrue(contact_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid(self):
        """ Test for all fields """
        contact_form = ContactEmailForm({
            'name': '',
            'email': '',
            'message': '',
        })
        self.assertFalse(contact_form.is_valid(), msg='Form is valid')

    def test_email_is_invalid(self):
        """ Test for invalid email """
        contact_form = ContactEmailForm({
            'name': 'John',
            'email': '',
            'message': 'This is a message',
        })
        self.assertFalse(contact_form.is_valid(), msg="Email was not provided, but the form is valid")

    # Required test
    def test_name_is_required(self):
        """ Test for required fields"""
        contact_form = ContactEmailForm({
            'name': '',
            'email': 'test@test.com',
            'message': 'This is a message',
        })
        self.assertFalse(contact_form.is_valid(), msg="Name was not provided, but the form is valid")

    def test_email_is_required(self):
        """ Test for required fields"""
        contact_form = ContactEmailForm({
            'name': 'Amy',
            'email': '',
            'message': 'This is a message',
        })
        self.assertFalse(contact_form.is_valid(), msg="Email was not provided, but the form is valid")

    def test_message_is_required(self):
        """ Test for required fields"""
        contact_form = ContactEmailForm({
            'name': 'Amy',
            'email': 'test@test.com',
            'message': '',
        })
        self.assertFalse(contact_form.is_valid(), msg="Message was not provided, but the form is valid")

    # Max character length test
    def test_name_max_length(self):
        """ Test name field respects max length of 200 characters """
        long_name = 'a' * 201  # 201 characters - should be invalid
        contact_form = ContactEmailForm({
            'name': long_name,
            'email': 'test@test.com',
            'message': 'This is a message',
        })
        self.assertFalse(contact_form.is_valid(), msg='Form should be invalid with name longer than 200 characters')

    def test_name_valid_length(self):
        """ Test name field accepts valid length """
        valid_name = 'a' * 200  # 200 characters - should be valid
        contact_form = ContactEmailForm({
            'name': valid_name,
            'email': 'test@test.com',
            'message': 'This is a message',
        })
        self.assertTrue(contact_form.is_valid(), msg='Form should be valid with name at max length')

    def test_message_accepts_long_text(self):
        """ Test that message field accepts long text """
        long_message = 'a' * 5000  # Very long message
        contact_form = ContactEmailForm({
            'name': 'John',
            'email': 'test@test.com',
            'message': long_message,
        })
        self.assertTrue(contact_form.is_valid(), msg='Form should be valid with long message')
