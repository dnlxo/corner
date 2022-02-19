from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', views.main.as_view()),
    path('logout', auth_views.LogoutView.as_view()),
    path('signup', views.signup.as_view()),
]