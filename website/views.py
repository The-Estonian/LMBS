from django.shortcuts import render
from .models import Posts
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    return render(request, "website/index.html")

def posts(request):
    all_posts = Posts.objects.all()
    context = {"all_posts":all_posts}
    return render(request, "website/view_posts.html", context)

def add_post(request):
    if request.method == "POST":
        current_poster_id = request.user.id
        current_poster_instance = User.objects.get(id=current_poster_id)
        new_post_message = request.POST["new_post"]
        new_post = Posts.objects.create(user_id=current_poster_instance, message=new_post_message)
        new_post.save()
        print(f"User {current_poster_instance.username} posts {new_post_message}")
    return render(request, "website/add_post.html")

