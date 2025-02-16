from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from .models import CustomUser, UserProfile
from .forms import CustomUserCreationForm


def signup_view(request):
    """
    Handles user registration and sends email verification.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            UserProfile.objects.create(user=user)

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


def activate_view(request, uidb64, token):
    """
    Verifies email and activates the user.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            user_profile = UserProfile.objects.get(user=user)
            user_profile.is_email_verified = True
            user_profile.save()

            login(request, user)
            return redirect("dashboard")
        else:
            return HttpResponse("Invalid activation link.")
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, UserProfile.DoesNotExist):
        return HttpResponse("Activation link is invalid.")


def signin_view(request):
    """
    Handles user sign-in.
    """
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/signin.html', {'form': form})


@login_required
def signout_view(request):
    """
    Handles user sign-out.
    """
    logout(request)
    return redirect('signin')
