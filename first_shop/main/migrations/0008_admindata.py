# Generated by Django 5.2 on 2025-04-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_comment_created_at_comment_updated_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("username", models.CharField(max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
