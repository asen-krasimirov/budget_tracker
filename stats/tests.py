import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from purchases.models import Purchase
from accounts.models import UserProfile

User = get_user_model()

class StatisticsTests(TestCase):

    def setUp(self):
        """Create a test user and set up user profile."""
        self.user = User.objects.create_user(
            email="statsuser@example.com",
            username="statsuser",  # ✅ Fix: Add username
            password="TestPass123"
        )
        self.client.login(email="statsuser@example.com", password="TestPass123")

        # ✅ Create user profile with currency
        self.profile = UserProfile.objects.create(user=self.user, currency="USD")

        # ✅ Add sample purchases
        Purchase.objects.create(user=self.user, name="Apple", price=1.20, category="Food", barcode="1001")
        Purchase.objects.create(user=self.user, name="Bread", price=2.50, category="Food", barcode="1002")
    
    def test_statistics_view(self):
        """Test statistics page loads correctly."""
        response = self.client.get(reverse("dashboard"))  # ✅ Updated for existing URL
        self.assertEqual(response.status_code, 200)


    def test_statistics_data(self):
        """Test that the statistics API returns valid JSON data."""
        response = self.client.get(reverse("stats_data"))
        self.assertEqual(response.status_code, 200, "Stats API did not return 200 OK")

        # ✅ Ensure response content is not empty
        self.assertTrue(response.content, "Response content is empty!")

        # ✅ Try parsing JSON
        try:
            data = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON!")

        # ✅ Ensure required keys exist
        self.assertIn("monthly", data)
        self.assertIn("weekly", data)
        self.assertIn("daily", data)
        self.assertIn("category", data)
        self.assertIn("most_bought", data)
        self.assertIn("least_bought", data)
        self.assertIn("currency_symbol", data)

        # ✅ Ensure currency symbol is correct
        self.assertEqual(data["currency_symbol"][-2], "$", "Currency symbol does not match user profile")

        # ✅ Ensure numeric values exist in categories
        self.assertTrue(isinstance(data["monthly"], dict))
        self.assertTrue(isinstance(data["weekly"], dict))
        self.assertTrue(isinstance(data["daily"], dict))
        self.assertTrue(isinstance(data["category"], dict))
