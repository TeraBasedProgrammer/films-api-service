from django.db import models

from actors.models import Actor
from .validators import validate_text, validate_rating, validate_age_restriction, validate_names


class Film(models.Model):
    title = models.CharField(max_length=50, validators=[validate_text])

    # Format of the poster image (poster name is hardcoded, so it's not stored in db)
    poster_format = models.CharField(max_length=4)
    rating = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_rating])
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2, editable=False)

    # Many-to-many relations for listing related actors and genres
    genres = models.ManyToManyField('Genre', db_table='FilmGenre')
    actors = models.ManyToManyField(Actor, through='FilmActor')

    country = models.CharField(max_length=50, validators=[validate_names])
    release_date = models.DateField()
    director = models.CharField(max_length=50, validators=[validate_names])
    description = models.TextField(validators=[validate_text])
    age_restriction = models.IntegerField(validators=[validate_age_restriction])
    studio = models.CharField(max_length=50, validators=[validate_text])

    def __str__(self):
        return self.title


class FilmActor(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True)


class Screenshot(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='screenshots')
    file = models.CharField(max_length=100, blank=True, null=True)


class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


