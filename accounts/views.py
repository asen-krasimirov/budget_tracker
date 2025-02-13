from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm

def signup_view(request):
    """Handles user registration, including currency selection."""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect("dashboard")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


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
