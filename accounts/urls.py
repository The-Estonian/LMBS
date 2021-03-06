from django.contrib import admin
from django.urls import path
from .views import (accounts, 
                    log_out, 
                    log_in, 
                    sign_up, 
                    reg_success, 
                    edit_accounts, 
                    public_account)

urlpatterns = [
    path("accounts/", accounts, name="user_account_info"),
    path("logout/", log_out, name="log_out"),
    path("login/", log_in, name="log_in"),
    path("sign_up/", sign_up, name="sign_up"),
    path("reg_success/", reg_success, name="reg_success"),
    path("edit_accounts/", edit_accounts, name="edit_accounts"),
    path("public_account/<int:user_id>", public_account, name="public_account"),
]