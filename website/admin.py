from django.contrib import admin
from .models import Posts, TemplateChoice, Templates
# Register your models here.

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "message"]


@admin.register(TemplateChoice)
class TemplateChoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "template_choice"]


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "template"]

