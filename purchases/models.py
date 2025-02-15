from django.db import models
from django.conf import settings


class Purchase(models.Model):
    """
    Stores purchase details linked to a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "barcode", "date")

    def __str__(self):
        return f"{self.name} - {self.price} ({self.user.email})"