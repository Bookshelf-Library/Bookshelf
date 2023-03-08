# Generated by Django 4.1.7 on 2023-03-07 17:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("copies", "0002_rename_user_loan_account_copy_last_loan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="copy",
            name="account",
            field=models.ManyToManyField(
                related_name="loans", through="copies.Loan", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
