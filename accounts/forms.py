from django import forms
from .models import UserProfile

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    currency = forms.ChoiceField(choices=UserProfile.CURRENCY_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "currency"]

    def save(self, commit=True):
        """Creates a user and a UserProfile with selected currency."""
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, currency=self.cleaned_data["currency"])
        return user