from django.db import models
from uuid import uuid4


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=120)
    pages = models.IntegerField()
    author = models.CharField(max_length=120)
    publisher = models.CharField(max_length=120)

    account = models.ManyToManyField(
        "accounts.account", through="books.Follow", related_name="following"
    )


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
