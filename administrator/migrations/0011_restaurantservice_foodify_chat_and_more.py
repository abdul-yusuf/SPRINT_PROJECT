# Generated by Django 4.0.2 on 2022-08-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0010_activity_restaurantservice_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantservice',
            name='foodify_chat',
            field=models.ManyToManyField(blank=True, related_name='restaurant', to='administrator.Message'),
        ),
        migrations.AddField(
            model_name='restaurantservice',
            name='staff_chat',
            field=models.ManyToManyField(blank=True, to='administrator.Message'),
        ),
    ]
