# Generated by Django 4.1.7 on 2023-06-27 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0025_delete_filmplaylist'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='slug',
            field=models.SlugField(default='penis'),
        ),
    ]
