# Generated by Django 4.1.7 on 2023-07-03 19:13

from django.db import migrations, models

import films.validators


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0031_remove_film_imdb_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[films.validators.validate_rating]),
        ),
    ]
