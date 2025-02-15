import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from purchases.models import Purchase
from accounts.models import UserProfile


User = get_user_model()


class StatisticsTests(TestCase):

    def setUp(self):
        """
        Create a test user and set up user profile.
        """
        self.user = User.objects.create_user(
            email="statsuser@example.com",
            username="statsuser",
            password="TestPass123"
        )
        self.client.login(email="statsuser@example.com", password="TestPass123")
        self.profile = UserProfile.objects.create(user=self.user, currency="USD")
        Purchase.objects.create(user=self.user, name="Apple", price=1.20, category="Food", barcode="1001")
        Purchase.objects.create(user=self.user, name="Bread", price=2.50, category="Food", barcode="1002")
    
    def test_statistics_view_loads_correctly(self):
        """
        Test statistics page loads correctly.
        """
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_statistics_data_returns_200(self):
        """
        Test that the statistics API returns 200 OK.
        """
        response = self.client.get(reverse("stats_data"))
        self.assertEqual(response.status_code, 200)

    def test_statistics_data_not_empty(self):
        """
        Test that the statistics API returns non-empty content.
        """
        response = self.client.get(reverse("stats_data"))
        self.assertTrue(response.content)

    def test_statistics_data_is_valid_json(self):
        """
        Test that the statistics API returns valid JSON.
        """
        response = self.client.get(reverse("stats_data"))
        try:
            json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON!")

    def test_statistics_data_contains_required_keys(self):
        """
        Test that the statistics API response contains required keys.
        """
        response = self.client.get(reverse("stats_data"))
        data = json.loads(response.content)
        self.assertIn("monthly", data)
        self.assertIn("weekly", data)
        self.assertIn("daily", data)
        self.assertIn("category", data)
        self.assertIn("most_bought", data)
        self.assertIn("least_bought", data)
        self.assertIn("currency_symbol", data)

    def test_statistics_data_currency_symbol(self):
        """
        Test that the currency symbol in the statistics API response matches the user profile.
        """
        response = self.client.get(reverse("stats_data"))
        data = json.loads(response.content)
        self.assertEqual(data["currency_symbol"][-2], "$")

    def test_statistics_data_contains_numeric_values(self):
        """
        Test that the statistics API response contains numeric values in categories.
        """
        response = self.client.get(reverse("stats_data"))
        data = json.loads(response.content)
        self.assertTrue(isinstance(data["monthly"], dict))
        self.assertTrue(isinstance(data["weekly"], dict))
        self.assertTrue(isinstance(data["daily"], dict))
        self.assertTrue(isinstance(data["category"], dict))
