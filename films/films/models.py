from django.db import models


# Refactor: Add model validations

class Film(models.Model):
    title = models.CharField(max_length=50)
    poster_name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2, editable=False)
    country = models.CharField(max_length=50)
    release_date = models.DateField()
    director = models.CharField(max_length=50)
    description = models.TextField()
    age_restriction = models.IntegerField()
    studio = models.CharField(max_length=50)

    
class Screenshot(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='screenshots')
    name = models.CharField(max_length=100) 
