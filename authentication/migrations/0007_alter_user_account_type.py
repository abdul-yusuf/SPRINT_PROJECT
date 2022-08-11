# Generated by Django 4.0.2 on 2022-08-10 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('Staff', 'Staff'), ('Student', 'Student'), ('Other', 'Other')], default=('Student', 'Student'), max_length=7),
        ),
    ]
