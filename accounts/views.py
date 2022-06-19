from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError

# Create your views here.

def email_clean(variable):
    for x in variable:
        for y in variable:
            if x == "@" and y == ".":
                return True

def accounts(request):
    current_user = request.user.id
    fetch_user = User.objects.filter(id=current_user)
    context = {"account_info": fetch_user}
    return render(request, "accounts/accounts.html", context)

def log_out(request):
    logout(request)
    return redirect("index")

def log_in(request):
    context = {}
    if request.method == "POST":
        email = request.POST["email"]
        if email_clean(email):
            username = User.objects.get(email=email)
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
        else:
            email_error = {"email": "Please enter a valid Email address!"}
            context.update(email_error)
            return render(request, "accounts/login.html", context)
        if user is not None:
            login(request, user)
    return render(request, "accounts/login.html")

def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        
        if password == password2:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name )
            new_user.save()
            return redirect("log_in")

    return render(request, "accounts/sign_up.html")
