# Generated by Django 4.0.2 on 2022-09-01 20:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kitchen', '0016_alter_food_kitchen_offered_alter_ordered_kitchen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitchen',
            name='attendants',
            field=models.ManyToManyField(blank=True, related_name='kitchen', to=settings.AUTH_USER_MODEL),
        ),
    ]