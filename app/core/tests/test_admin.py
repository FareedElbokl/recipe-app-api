"""
Test for the django admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSitetests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client() # create an instance of the Client class to make GET and POST reqs
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass123"
        ) # create a super user

        self.client.force_login(self.admin_user) # using the client instance, login as the superuser
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123",
            name="Test User"
        ) # create a regular user

    def test_users_list(self):
        """Test that users are listed on page"""
        url = reverse("admin:core_user_changelist") # reverse creates a url from the given string
        res = self.client.get(url) # make a get request to this url, giving us all the users listen on admin page

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
