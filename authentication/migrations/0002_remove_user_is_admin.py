# Generated by Django 4.0.2 on 2022-08-15 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
    ]