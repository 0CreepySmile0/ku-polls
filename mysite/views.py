"""Store redirect view and signup view."""
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm


class RedirectIndexView(generic.RedirectView):
    """Use to redirect the '/' url to index page."""

    url = "polls/"


def signup(request):
    """Register a new user."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("polls:index")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def logout_handler(request):
    """Log out and redirect to index."""
    logout(request)
    return redirect("polls:index")