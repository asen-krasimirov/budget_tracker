from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class AuthenticationTests(TestCase):

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def setUp(self):
        """
        Create a test user.
        """
        self.user = User.objects.create_user(
            email="test@example.com",
            password="TestPass123",
            username="testuser"
        )
        self.user.is_active = False
        self.user.save()

    def test_signup(self):
        """
        Test user signup and email verification.
        """
        response = self.client.post(reverse("signup"), {
            "email": "newuser@example.com",
            "username": "newuser",
            "password1": "NewPass123!",
            "password2": "NewPass123!",
            "currency": "USD",
        })
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(email="newuser@example.com")
        self.assertFalse(user.is_active)

    def test_email_verification_invalid_token(self):
        """
        Test email activation flow with an invalid token.
        """
        uid = self.user.pk
        response = self.client.get(reverse("activate", args=[uid, "testtoken"]))
        self.assertEqual(response.status_code, 200)

    def test_signin_with_incorrect_credentials(self):
        """
        Test login with incorrect credentials.
        """
        response = self.client.post(reverse("signin"), {
            "email": "test@example.com",
            "password": "WrongPass123",
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
