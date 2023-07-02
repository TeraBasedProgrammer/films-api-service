from django.db import models
from django.utils.text import slugify
from django.db import IntegrityError
from rest_framework.serializers import ValidationError

from films.validators import validate_text, validate_names


class Actor(models.Model):
    name = models.CharField(max_length=50, validators=[validate_names], unique=True)
    birth_date = models.DateField(null=True)
    death_date = models.DateField(null=True)

    description = models.TextField(validators=[validate_text])

    # Many-to-many relation for listing related films
    films = models.ManyToManyField('films.Film', through='films.FilmActor')

    # Format of the actor image (it has the same name, format can only change)
    photo_format = models.CharField(max_length=4)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError({'name':['actor with this name already exists.']})
        
    def __str__(self):
        return self.name
