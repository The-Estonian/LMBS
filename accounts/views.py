from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def accounts(request):
    current_user = request.user.id
    print(current_user)
    fetch_user = User.objects.filter(id=current_user)
    print(fetch_user)
    context = {"account_info": fetch_user}
    return render(request, "accounts/accounts.html", context)

def log_out(request):
    logout(request)
    return redirect("index")

def log_in(request):
    if request.method == "post":
        print(request.method.POST)
    return render(request, "accounts/login.html")
