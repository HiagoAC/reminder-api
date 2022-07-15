"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class TestModels(TestCase):
    """Test models."""
    def test_create_user_with_email_and_phone_number_successful(self):
        """Test creating user with an email and phone is succesful"""
        email = 'email@example.com'
        phone_number = '+1-202-555-0111'
        password = 'testPassword'
        user = get_user_model().objects.create_user(
            email = email,
            phone_number = phone_number,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.phone_number, phone_number)
        self.assertTrue(user.check_password(password))