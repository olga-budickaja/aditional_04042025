# Generated by Django 5.2 on 2025-04-08 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_category_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='categories', to='main.product'),
        ),
    ]
