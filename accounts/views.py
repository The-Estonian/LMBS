from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from re import match

# Create your views here.

def email_cleaner(variable):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if match(pat,variable):
        return True
    return False

def username_cleaner(variable):
    pat = "^[a-zA-Z0-9_.-]+$"
    if match(pat, variable):
        return True
    return False

def accounts(request):
    current_user = request.user.id
    fetch_user = User.objects.filter(id=current_user)
    context = {"account_info": fetch_user}
    if request.method == "POST":
        id_to_delete = request.POST["delete-account"]
        active_user = User.objects.get(id=id_to_delete)
        # print(f"deleting", active_user)
        active_user.delete()
        return redirect("log_in")
    return render(request, "accounts/accounts.html", context)

def log_out(request):
    logout(request)
    return redirect("index")

def log_in(request):
    context = {}
    if request.method == "POST":
        email = request.POST["email"]
        if email_cleaner(email):
            try:
                username = User.objects.get(email=email)
                password = request.POST["password"]
                try:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect("posts")
                    else:
                        password_error = {"password_error": "Account and Password do not match."}
                        context.update(password_error)
                        return render(request, "accounts/login.html", context)

                except:
                    password_error = {"password_match": "No account in our system with the Email and Password that you provided!"}
                    context.update(password_error)
                    return render(request, "accounts/login.html", context)
            except:
                user_error = {"user_error": "User does not exist!"}
                context.update(user_error)
                return render(request, "accounts/login.html", context)
        else:
            email_error = {"email": "Your email did not pass server validation. Please enter a correct email!"}
            context.update(email_error)
            return render(request, "accounts/login.html", context)
        
    return render(request, "accounts/login.html")

def sign_up(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        if email_cleaner(email):
            print("Email correct")
            if password == password2:
                print("Password correct")
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name )
                new_user.save()
                return redirect("reg_success")
            else:
                print("Password error")
                password_error = {"password_match": "Your passwords did not match!"}
                context.update(password_error)
        else:
            print("Email error")
            email_error = {"email": "Your email did not pass server validation. Please enter a correct email!"}
            context.update(email_error)

    return render(request, "accounts/sign_up.html", context)

def reg_success(request):
    return render(request, "accounts/reg_success.html")
