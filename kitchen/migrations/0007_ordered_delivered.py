# Generated by Django 3.2.1 on 2022-08-16 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0006_auto_20220816_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordered',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]