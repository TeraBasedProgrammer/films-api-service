from django.db import models
from .validators import validate_name, validate_age
from films.validators import validate_text


class Actor(models.Model):
    name = models.CharField(max_length=50, validators=[validate_name])
    age = models.IntegerField(validators=[validate_age])
    description = models.TextField(validators=[validate_text])

    # Format of the actor image (it has the same name, format can only change)
    photo_format = models.CharField(max_length=4)

    def __str__(self):
        return self.name
