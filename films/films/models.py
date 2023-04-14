from django.db import models
from actors.models import Actor


class Film(models.Model):
    title = models.CharField(max_length=50)

    # Format of the poster image (poster name is hardcoded, so it's not stored in db)
    poster_format = models.CharField(max_length=4)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2, editable=False)

    # Many-to-many relations
    genres = models.ManyToManyField('Genre', db_table='FilmGenre')
    actors = models.ManyToManyField(Actor, db_table='FilmActor')

    country = models.CharField(max_length=50)
    release_date = models.DateField()
    director = models.CharField(max_length=50)
    description = models.TextField()
    age_restriction = models.IntegerField()
    studio = models.CharField(max_length=50)

    
class Screenshot(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='screenshots')
    file = models.CharField(max_length=100, blank=True, null=True)


class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


