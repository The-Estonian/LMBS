from django.contrib import admin
from django.urls import path, include
from .views import index, posts, add_post

urlpatterns = [
    path("", index, name="index"),
    path("posts/", posts, name="posts"),
    path("add_post/", add_post, name="add_post"),
]