# Generated by Django 4.1.7 on 2023-03-21 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='film',
            old_name='realese_date',
            new_name='release_date',
        ),
    ]
