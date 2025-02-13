from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, CURRENCY_CHOICES

class SignupForm(forms.ModelForm):
    """User registration form with currency selection."""
    password = forms.CharField(widget=forms.PasswordInput)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES, label="Preferred Currency")

    class Meta:
        model = User
        fields = ["username", "email", "password", "currency"]

    def save(self, commit=True):
        """Save user and create UserProfile with currency."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, currency=self.cleaned_data["currency"])
        return user
