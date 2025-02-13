from django.db import models
from django.contrib.auth.models import User

class Purchase(models.Model):
    """Merged model for Products & Purchases"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each purchase belongs to a user
    barcode = models.CharField(max_length=50)  # Unique product identifier
    name = models.CharField(max_length=255)  # Product name
    category = models.CharField(max_length=100, blank=True, null=True)  # Optional category
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Purchase price
    date = models.DateTimeField(auto_now_add=True)  # Timestamp for purchase

    class Meta:
        unique_together = ('user', 'barcode', 'date')  # Ensures unique purchases per user & timestamp

    def __str__(self):
        return f"{self.name} - ${self.price} ({self.user.username})"
