from django.contrib import admin
from django.urls import path, include
from .views import index, all_posts, add_post, user_posts, edit_post, public_posts

urlpatterns = [
    path("", index, name="index"),
    path("all_posts/", all_posts, name="all_posts"),
    path("add_post/", add_post, name="add_post"),
    path("edit_post/<int:post_id>", edit_post, name="edit_post"),
    path("user_posts/", user_posts, name="user_posts"),
    path("public_posts/<int:user_id>", public_posts, name="public_posts"),
]