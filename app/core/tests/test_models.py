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
            email=email,
            phone_number=phone_number,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.phone_number, phone_number)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """Test email adresses are normalized"""
        sample_emails = (
            ('Test1@example.com', 'Test1@example.com', '+1-202-555-0130'),
            ('test2@EXAMPLE.com', 'test2@example.com', '+1-202-555-0131'),
            ('Test3@EXAMPLE.COM', 'Test3@example.com', '+1-202-555-0132'),
            ('test4@example.com', 'test4@example.com', '+1-202-555-0133')
        )

        for original_email, normalized_email, phone_number in sample_emails:
            user = get_user_model().objects.create_user(
                email=original_email,
                phone_number=phone_number,
                password='testPassword'
            )
            self.assertEqual(user.email, normalized_email)

    def test_email_required_create_user(self):
        """Test user can't be created without an email adress"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '',
                password='testPassword'
            )

    def test_create_superuser(self):
        "Test superuser is created sucessfully"
        superuser = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testPassword'
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
