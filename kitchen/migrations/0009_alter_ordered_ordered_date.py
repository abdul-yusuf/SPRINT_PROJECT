# Generated by Django 4.0.2 on 2022-08-06 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0008_ordered_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordered',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
