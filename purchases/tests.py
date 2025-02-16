from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from purchases.models import Purchase


User = get_user_model()


class PurchaseTests(TestCase):

    def setUp(self):
        """
        Create a test user and a sample purchase.
        """
        self.user = User.objects.create_user(
            email="user@example.com", 
            username="testuser",
            password="TestPass123"
        )
        self.client.login(email="user@example.com", password="TestPass123")

        self.purchase = Purchase.objects.create(
            user=self.user, name="Test Product", price=9.99, category="Food", barcode="123456789"
        )

    def test_add_purchase(self):
        """
        Test adding a new purchase.
        """
        response = self.client.post(reverse("add_purchase", args=["987654321"]), {
            "name": "New Product",
            "price": 5.50,
            "category": "Snacks",
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Purchase.objects.count(), 2)

    def test_add_purchase_redirect(self):
        """
        Test redirection after adding a new purchase.
        """
        response = self.client.post(reverse("add_purchase", args=["987654321"]), {
            "name": "New Product",
            "price": 5.50,
            "category": "Snacks",
        }, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_delete_purchase(self):
        """
        Test deleting a purchase.
        """
        response = self.client.post(reverse("delete_purchase", args=[self.purchase.id]), follow=True)
        self.assertEqual(Purchase.objects.filter(id=self.purchase.id).count(), 0)
        self.assertRedirects(response, reverse("dashboard"))

    def test_delete_purchase_redirect(self):
        """
        Test redirection after deleting a purchase.
        """
        response = self.client.post(reverse("delete_purchase", args=[self.purchase.id]), follow=True)
        self.assertRedirects(response, reverse("dashboard"))