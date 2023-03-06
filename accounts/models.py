from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_colaborator = models.BooleanField(default=False)
