from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model using email for authentication."""
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"  # ✅ Use email for authentication
    REQUIRED_FIELDS = ["username"]  # Username still required

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """Extends the User model to store currency preferences and email verification."""
    
    CURRENCY_CHOICES = [
        ("USD", "US Dollar ($)"),
        ("EUR", "Euro (€)"),
        ("GBP", "British Pound (£)"),
        ("INR", "Indian Rupee (₹)"),
        ("JPY", "Japanese Yen (¥)"),
        ("AUD", "Australian Dollar (A$)"),
        ("BGN", "Bulgarian Lev (BGN)"),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}"