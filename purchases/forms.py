from django import forms
from .models import Purchase

class ImageUploadForm(forms.Form):
    """Form for uploading barcode image"""
    image = forms.ImageField(required=True, label="Upload Barcode Image")

class PurchaseForm(forms.ModelForm):
    """Form for adding a purchase (barcode, name, category, price)."""
    
    class Meta:
        model = Purchase
        fields = ['name', 'category', 'price']

    def __init__(self, *args, **kwargs):
        """Ensure all fields are required."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # Makes all fields required
