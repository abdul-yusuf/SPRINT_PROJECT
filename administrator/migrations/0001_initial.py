# Generated by Django 4.0.2 on 2022-08-04 19:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kitchen', '0009_alter_ordered_ordered_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('phone_no', models.CharField(max_length=15)),
                ('admins', models.ManyToManyField(related_name='managed_restaurant', to=settings.AUTH_USER_MODEL)),
                ('kitchens', models.ManyToManyField(related_name='restaurant', to='kitchen.Kitchen')),
            ],
        ),
    ]