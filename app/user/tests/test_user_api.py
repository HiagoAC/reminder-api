"""
Tests for user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create a new user"""
    user = get_user_model().objects.create_user(**params)

    return user


class PublicUserAPITests(TestCase):
    """Tests for public endpoints of user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test user is created successfully"""

        payload = {
            'email': 'test@example.com',
            'phone_number': '+1-202-555-0111',
            'password': 'testPassword123',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(user.phone_number, payload['phone_number'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_non_unique_email_error(self):
        """Tests creating user with an existing email generates an error"""
        email = 'test@example.com'

        get_user_model().objects.create_user(
            email=email,
            phone_number='+1-202-555-0100',
            password='testPassword123',
        )

        res = self.client.post(CREATE_USER_URL, {
            'email': email,
            'phone_number': '+1-202-555-0101',
            'password': 'TestPassword123',
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_non_unique_phone_number_error(self):
        """
        Tests creating an user with a non unique
        phone number generates an error
        """
        phone_number = '+1-202-555-0102'

        get_user_model().objects.create_user(
            email='test1@example.com',
            phone_number=phone_number,
            password='testPassword123',
        )

        res = self.client.post(CREATE_USER_URL, {
            'email': 'test2@example.com',
            'phone_number': phone_number,
            'password': 'testPassword123'
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """
        Tests creating user with a password shorter than
        10 characters returns an error
        """
        short_password = 'nineChars'
        payload = {
            'email': 'test@example.com',
            'phone_number': '+1-202-555-0103',
            'password': short_password,
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)
