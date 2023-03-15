from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_colaborator = models.BooleanField(default=False)
    punishment = models.DateTimeField(null=True, default=None)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
