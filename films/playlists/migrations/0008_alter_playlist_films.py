# Generated by Django 4.1.7 on 2023-05-31 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0025_delete_filmplaylist'),
        ('playlists', '0007_alter_playlist_films'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='films',
            field=models.ManyToManyField(blank=True, to='films.film'),
        ),
    ]
