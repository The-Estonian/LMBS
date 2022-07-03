from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from website.models import TemplateChoice, Templates
from django.contrib.auth.decorators import login_required
from re import match

# Create your views here.

def email_validator(variable):
    pat = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if match(pat,variable):
        return True
    return False

def username_validator(variable):
    pat = "^[a-zA-Z0-9_.-]+$"
    if match(pat, variable):
        return True
    return False

def name_validator(variable):
    pat = "^[a-zA-Z]+$"
    if match(pat, variable):
        return True
    return False

def name_cleaner(variable):
    return variable.capitalize()

@login_required(login_url="log_in")
def accounts(request):
    current_user = request.user.id
    fetch_user = User.objects.filter(id=current_user)
    context = {"account_info": fetch_user}
    user_template = Templates.objects.get(user_id=current_user)
    if request.method == "POST":
        if "delete-account" in request.POST:
            id_to_delete = request.POST["delete-account"]
            active_user = User.objects.get(id=id_to_delete)
            active_user.delete()
            return redirect("log_in")
        elif "orange" in request.POST:
            template_choice = TemplateChoice.objects.get(id=1)
            user_template.template_id = template_choice
            user_template.save()
            print(user_template.template_id)
        elif "green" in request.POST:
            template_choice = TemplateChoice.objects.get(id=2)
            user_template.template_id = template_choice
            user_template.save()
            print(user_template.template_id)
        elif "purple" in request.POST:
            template_choice = TemplateChoice.objects.get(id=3)
            user_template.template_id = template_choice
            user_template.save()
            print(user_template.template_id)
    return render(request, "accounts/accounts.html", context)

def log_out(request):
    logout(request)
    return redirect("index")

def log_in(request):
    context = {}
    if request.method == "POST":
        email = request.POST["email"].lower()
        if email_validator(email):
            try:
                username = User.objects.get(email=email)
                password = request.POST["password"]
                try:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect("user_posts")
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
        email = request.POST["email"].lower()
        password = request.POST["password"]
        password2 = request.POST["password2"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        if email_validator(email):
            if password == password2 and len(password) >= 6:
                if username_validator(username):
                    if name_validator(first_name) and name_validator(last_name):
                        new_user = User.objects.create_user(
                            username=username,
                            password=password,
                            email=email,
                            first_name=name_cleaner(first_name),
                            last_name=name_cleaner(last_name))
                        new_user.save()
                        user_template = Templates.objects.create(user_id=new_user)
                        user_template.save()
                        return redirect("reg_success")
                    else:
                        name_error = {"name_error": "First and Last name can only contain letters!"}
                        context.update(name_error)
                else:
                    username_error = {"username_error": "Please use only numbers and Upper/Lower case letters for username!"}
                    context.update(username_error)
            else:
                print("Password error")
                password_error = {"password_match": "Your passwords did not match or password too short. Min 6 characters!"}
                context.update(password_error)
        else:
            print("Email error")
            email_error = {"email": "Your email did not pass server validation. Please enter a correct email!"}
            context.update(email_error)

    return render(request, "accounts/sign_up.html", context)

def reg_success(request):
    return render(request, "accounts/reg_success.html")

@login_required
def edit_accounts(request):
    current_user = request.user.id
    fetch_user = User.objects.filter(id=current_user)
    context = {"account_info": fetch_user}
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        new2_password = request.POST["new2_password"]
        user_instance = User.objects.get(id=current_user)
        if user_instance.check_password(old_password):
            if email_validator(email):
                if username_validator(username):
                    user_instance.username = username
                    user_instance.first_name = first_name
                    user_instance.last_name = last_name
                    user_instance.email = email
                    user_instance.save()
                    if len(new_password) > 0:
                        if new_password == new2_password:
                            user_instance.set_password(new_password)
                            user_instance.save()
                        else:
                            password_error = {"password_missmatch": "Your entered passwords do not match!"}
                            context.update(password_error)
                else:
                    username_error = {"username_error": "Please use only numbers and Upper/Lower case letters for username!"}
                    context.update(username_error)
            else:
                email_error = {"email": "Your email did not pass server validation. Please enter a correct email!"}
                context.update(email_error)
        else:
            wrong_password = {"wrong_password": "Please provide account password to make changes!"}
            context.update(wrong_password)
    print(context)
    return render(request, "accounts/edit_accounts.html", context)


def public_account(request, user_id):
    user_account = User.objects.filter(id=user_id)
    context = {"user_account": user_account}
    return render(request, "accounts/public_account.html", context)

"""
'username': ['Second_user'], 
'first_name': ['Second'], 
'last_name': ['User'], 
'email': ['Second@user.com'], 
'old_password': ['asd'], 
'new_password': ['ssad'], 
'new2_password': ['ssad']}>
"""
