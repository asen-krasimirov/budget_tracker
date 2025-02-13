from django.db import models
from django.contrib.auth.models import User

CURRENCY_CHOICES = [
    ("USD", "US Dollar ($)"),
    ("EUR", "Euro (€)"),
    ("GBP", "British Pound (£)"),
    ("INR", "Indian Rupee (₹)"),
    ("JPY", "Japanese Yen (¥)"),
    ("AUD", "Australian Dollar (A$)"),
    ("BGN", "Bulgarian Lev (BGN)"),
]

class UserProfile(models.Model):
    """Extends the User model to store currency preferences."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")

    def __str__(self):
        return f"{self.user.username} - {self.get_currency_display()}"
