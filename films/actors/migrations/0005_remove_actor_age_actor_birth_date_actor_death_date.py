# Generated by Django 4.1.7 on 2023-05-20 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0004_alter_actor_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='age',
        ),
        migrations.AddField(
            model_name='actor',
            name='birth_date',
            field=models.DateField(default='2022-02-24'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='actor',
            name='death_date',
            field=models.DateField(null=True),
        ),
    ]
