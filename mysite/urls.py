"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', views.RedirectIndexView.as_view()),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_handler, name='logout'),
]
