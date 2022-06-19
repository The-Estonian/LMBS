from django.contrib import admin
from django.urls import path, include
from .views import accounts, log_out, log_in

urlpatterns = [
    path("accounts/", accounts, name="user_account_info"),
    path("logout/", log_out, name="log_out"),
    path("login/", log_in, name="log_in"),
]