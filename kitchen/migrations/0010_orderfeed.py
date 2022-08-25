# Generated by Django 4.0.2 on 2022-08-25 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0009_remove_ordered_delivered_remove_ordered_kitchen'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kitchen_feed', to='kitchen.ordered')),
            ],
        ),
    ]