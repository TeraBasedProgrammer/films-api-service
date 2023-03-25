# Generated by Django 4.1.7 on 2023-03-21 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_film_imdb_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='imdb_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
    ]