"""
Tests for the user apo
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create') # this gets hold of the url for the create user endpoint

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    "Test public features of user api"

    def setUp(self): # need to create a 'fake' client to make the requests to the user api from
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successfull"""
        # 1: First actually testing making the post request to the endpoint
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload) # make a post request from our 'fake' client

        self.assertEqual(res.status_code, status.HTTP_201_CREATED) # ensure the status code returned was 201

        # 2: Now test that the user actually exists in the database
        # get hold of the user instance object of the User model (class)
        user = get_user_model().objects.get(email = payload['email'])
        # using the built in check_password method, check that the user's hashed password matches the one we passed when making him
        self.assertTrue(user.check_password(payload["password"]))
        # For security reasons, make sure to check password wasnt passed in with response
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test that an error returns if we try and create a user with an email that exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**payload)
        # we created the user, now try making a create POST request w same payload
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test that an error is returned if created password is less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # make sure user wasnt added to db
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)
