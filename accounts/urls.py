from django.contrib import admin
from django.urls import path, include
from .views import accounts, log_out, log_in, sign_up, reg_success

urlpatterns = [
    path("accounts/", accounts, name="user_account_info"),
    path("logout/", log_out, name="log_out"),
    path("login/", log_in, name="log_in"),
    path("sign_up/", sign_up, name="sign_up"),
    path("reg_success/", reg_success, name="reg_success"),
]