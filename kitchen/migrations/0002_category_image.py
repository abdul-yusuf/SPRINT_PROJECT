# Generated by Django 4.0.2 on 2022-07-31 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
