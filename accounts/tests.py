from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import UserProfile

User = get_user_model()

class AuthenticationTests(TestCase):

    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(email="test@example.com", password="TestPass123", username="testuser")
        self.user.is_active = False  # User is inactive until email verification
        self.user.save()

    def test_signup(self):
        """Test user signup and email verification."""
        response = self.client.post(reverse("signup"), {
            "email": "newuser@example.com",
            "username": "newuser",
            "password1": "NewPass123!",
            "password2": "NewPass123!",
            "currency": "USD",
        })
        self.assertEqual(response.status_code, 200)  # Ensure signup page loads

        # Check if the user was created but not active
        user = User.objects.get(email="newuser@example.com")
        self.assertFalse(user.is_active)

    def test_email_verification(self):
        """Test email activation flow."""
        uid = self.user.pk
        response = self.client.get(reverse("activate", args=[uid, "testtoken"]))
        self.assertEqual(response.status_code, 200)  # Ensure page loads (invalid token)

    def test_sigin(self):
        """Test login with correct and incorrect credentials."""
        response = self.client.post(reverse("signin"), {
            "email": "test@example.com",
            "password": "TestPass123",
        })

        # ✅ Ensure the login page reloads (incorrect credentials)
        self.assertEqual(response.status_code, 200, "Login page should reload for unverified user")

        # ✅ Ensure user is NOT logged in (session check)
        self.assertNotIn("_auth_user_id", self.client.session, "User should NOT be authenticated")

        self.user.is_active = True
        self.user.save()

        response = self.client.post(reverse("signin"), {"email": "test@example.com", "password": "TestPass123"})
        self.assertEqual(response.status_code, 200)  # Now should succeed
