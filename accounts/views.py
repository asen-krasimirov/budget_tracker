from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import login


from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser, UserProfile
from .forms import CustomUserCreationForm

from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser, UserProfile

def signup_view(request):
    """Handles user registration and sends email verification."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # ✅ Prevent login until email is verified
            user.save()

            # ✅ Create a UserProfile with default currency
            UserProfile.objects.create(user=user)

            # ✅ Send email confirmation
            current_site = get_current_site(request)
            mail_subject = "Activate Your Account"
            message = render_to_string(
                "accounts/email_verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            return render(request, "accounts/email_verification_sent.html")

    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


def activate(request, uidb64, token):
    """Verifies email and activates the user."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # ✅ Mark email as verified in UserProfile
            user_profile = UserProfile.objects.get(user=user)
            user_profile.is_email_verified = True
            user_profile.save()

            login(request, user)
            return redirect("dashboard")  # ✅ Redirect to dashboard after activation
        else:
            return HttpResponse("Invalid activation link.")
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, UserProfile.DoesNotExist):
        return HttpResponse("Activation link is invalid.")

# Login View
def signin_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/signin.html', {'form': form})


# Logout View
@login_required
def signout_view(request):
    logout(request)
    return redirect('signin')  # Redirect to login page after logout
