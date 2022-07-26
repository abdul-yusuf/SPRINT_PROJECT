# Generated by Django 4.0.2 on 2022-08-28 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0009_alter_message_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetimestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='restaurantservice',
            name='activities',
            field=models.ManyToManyField(blank=True, to='administrator.Activity'),
        ),
    ]
