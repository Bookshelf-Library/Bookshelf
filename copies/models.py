from django.db import models
from uuid import uuid4


class Copy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_avaliable = models.BooleanField(default=True)
    book = models.ForeignKey(
        "books.Book", related_name="copies", on_delete=models.CASCADE
    )

    account = models.ManyToManyField(
        "accounts.Account", through="copies.Loan", related_name="copies"
    )


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_active = models.BooleanField()
    loaned_at = models.DateTimeField(auto_now_add=True)
    deliver_in = models.DateTimeField()
    delivery_at = models.DateTimeField(null=True)
    copy = models.ForeignKey("copies.Copy", on_delete=models.CASCADE)
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
