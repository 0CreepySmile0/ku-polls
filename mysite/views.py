"""Store redirect, signup, login and logout view."""
import logging
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView


logger = logging.getLogger("polls")


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RedirectIndexView(generic.RedirectView):
    """Use to redirect the '/' url to index page."""

    url = "polls/"


class Login(LoginView):
    """Custom login view by adding logger"""
    def form_valid(self, form):
        response = super().form_valid(form)
        ip = get_client_ip(self.request)
        user = self.request.user
        logger.info(f"{user.username} logged in from {ip}")
        return response

    def form_invalid(self, form):
        ip = get_client_ip(self.request)
        logger.warning(f"{self.request.POST.get('username')} failed to login from {ip}")
        return super().form_invalid(form)


def signup(request):
    """Register a new user."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        ip = get_client_ip(request)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"{user.username} signed up and logged in from {ip}")
            return redirect("polls:index")
        logger.warning(f"{request.POST.get('username')} failed to sign up from {ip}")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def logout_handler(request):
    """Log out and redirect to index."""
    user = request.user
    ip = get_client_ip(request)
    logger.info(f"{user.username} logged out from {ip}")
    logout(request)
    return redirect("polls:index")
