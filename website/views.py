from django.shortcuts import render, redirect
from .models import Posts, Templates
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

def core_templates(request):
    if request.user.id:
        return {"templates": Templates.objects.get(user_id=request.user.id)}
    else:
        return {"templates": Templates.objects.get(user_id=1)}

def index(request):
    last_5_posts = Posts.objects.all().order_by("-id")[:5]
    context = {"last_5_posts":last_5_posts}
    return render(request, "website/index.html", context)

def all_posts(request):
    all_posts = Posts.objects.all()
    context = {"all_posts":all_posts}
    if request.method == "POST":
        post_id_to_delete = request.POST["delete_post"]
        post_instance = Posts.objects.get(id=post_id_to_delete)
        post_instance.delete()
    return render(request, "website/all_posts.html", context)

@login_required(login_url="log_in")
def add_post(request):
    if request.method == "POST":
        current_poster_id = request.user.id
        current_poster_instance = User.objects.get(id=current_poster_id)
        new_post_message = request.POST["new_post"]
        new_post = Posts.objects.create(user_id=current_poster_instance, message=new_post_message)
        new_post.save()
        return redirect("user_posts")
    return render(request, "website/add_post.html")

@login_required(login_url="log_in")
def user_posts(request):
    current_user_id = request.user.id
    current_user_posts = Posts.objects.filter(user_id=current_user_id)
    context = {"current_user_posts":current_user_posts}
    if request.method == "POST":
        post_id_to_delete =request.POST["delete_post"]
        post_instance = Posts.objects.get(id=post_id_to_delete)
        post_instance.delete()
    return render(request, "website/user_posts.html", context)

@login_required(login_url="log_in")
def edit_post(request, post_id):
    post_to_edit = Posts.objects.filter(id=post_id)
    context = {"post_edit": post_to_edit}
    if request.method == "POST":
        post_edit = request.POST["edit_post"]
        post_to_edit = Posts.objects.get(id=post_id)
        post_to_edit.message = post_edit
        post_to_edit.save()
        return redirect("user_posts")
    return render(request, "website/edit_post.html", context)

def public_posts(request, user_id):
    public_post = Posts.objects.filter(user_id=user_id)
    context = {"public_post": public_post}
    return render(request, "website/public_posts.html", context)
