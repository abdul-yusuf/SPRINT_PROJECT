# Generated by Django 4.0.2 on 2022-08-18 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0008_delete_news_remove_order_payment_delete_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordered',
            name='delivered',
        ),
        migrations.RemoveField(
            model_name='ordered',
            name='kitchen',
        ),
    ]