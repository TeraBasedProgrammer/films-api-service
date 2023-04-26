from django.db import models

from .validators import validate_age
from films.validators import validate_text, validate_names


class Actor(models.Model):
    name = models.CharField(max_length=50, validators=[validate_names], unique=True)
    age = models.IntegerField(validators=[validate_age])
    description = models.TextField(validators=[validate_text])

    # Many-to-many relation for listing related films
    films = models.ManyToManyField('films.Film', through='films.FilmActor')

    # Format of the actor image (it has the same name, format can only change)
    photo_format = models.CharField(max_length=4)

    def __str__(self):
        return self.name
