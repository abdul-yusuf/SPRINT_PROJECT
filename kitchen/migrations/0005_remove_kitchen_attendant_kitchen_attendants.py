# Generated by Django 4.0.2 on 2022-08-16 09:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kitchen', '0004_remove_kitchen_address_remove_kitchen_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kitchen',
            name='attendant',
        ),
        migrations.AddField(
            model_name='kitchen',
            name='attendants',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
