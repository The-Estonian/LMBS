from django.db.models import (
    CASCADE,
    Model, 
    ForeignKey,
    CharField,
    TextField,
    )
from django.contrib.auth.models import User

# Create your models here.

class Posts(Model):
    user_id = ForeignKey(User, on_delete=CASCADE)
    message = TextField(max_length=255)

    class Meta:
        verbose_name_plural = "All available posts!"
    

class TemplateChoice(Model):
    template_choice = TextField(max_length=255)

    class Meta:
        verbose_name_plural = "Registered templates"
    
    def __str__(self):
        return self.template_choice



class Templates(Model):
    user_id = ForeignKey(User, on_delete=CASCADE)
    template = ForeignKey(TemplateChoice, on_delete=CASCADE, default=1)

    class Meta:
        verbose_name_plural = "User template picks"

