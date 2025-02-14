from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from purchases.models import Purchase

User = get_user_model()

class PurchaseTests(TestCase):

    def setUp(self):
        """Create a test user and a sample purchase."""
        self.user = User.objects.create_user(
            email="user@example.com", 
            username="testuser",  # ✅ Added missing username
            password="TestPass123"
        )
        self.client.login(email="user@example.com", password="TestPass123")

        self.purchase = Purchase.objects.create(
            user=self.user, name="Test Product", price=9.99, category="Food", barcode="123456789"
        )

    def test_add_purchase(self):
        """Test adding a new purchase."""
        response = self.client.post(reverse("add_purchase", args=["987654321"]), {
            "name": "New Product",
            "price": 5.50,
            "category": "Snacks",
        }, follow=True)  # ✅ Follow the redirect

        # ✅ Ensure we end up on the correct page after redirection
        self.assertEqual(response.status_code, 200, "The page after redirection should return 200 OK")

        # ✅ Check that the new purchase is actually added
        self.assertEqual(Purchase.objects.count(), 2, "A new purchase should be added to the database")


    # def test_edit_purchase(self):
    #     """Test editing an existing purchase."""
    #     response = self.client.post(reverse("add_purchase", args=[self.purchase.id]), {
    #         "name": "Updated Product",
    #         "price": 15.00,
    #         "category": "Beverages",
    #     }, follow=True)  # ✅ Follow redirect to confirm update

    #     # ✅ Ensure redirection happened successfully
    #     self.assertEqual(response.status_code, 200, "Edit should redirect and load successfully")

    #     # ✅ Refresh from database to get updated values
    #     self.purchase.refresh_from_db()

    #     # ✅ Ensure name is updated in the database
    #     self.assertEqual(self.purchase.price, "Updated Product", "Purchase name should be updated")
