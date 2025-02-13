from accounts.models import UserProfile

def user_currency(request):
    """Makes the logged-in user's currency available in templates."""
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        if profile:
            return {"USER_CURRENCY": profile.get_currency_display()}
    return {"USER_CURRENCY": "US Dollar ($)"}  # Default value
