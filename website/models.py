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
    