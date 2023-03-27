from django.db import models


# Refactor: Add model validations

class Film(models.Model):


    # Validation: text validation
    title = models.CharField(max_length=50)

    # Validation: text validation
    poster_name = models.CharField(max_length=100)
    
    rating = models.DecimalField(max_digits=4, decimal_places=2)

    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2, editable=False)
    
    # Validation: text validation
    country = models.CharField(max_length=50)

    # Validation: ? 
    release_date = models.DateField()

    # Validation: text validation
    director = models.CharField(max_length=50)

    # Validation: text validation
    description = models.TextField()

    # Refactor: implement CHOICES
    age_restriction = models.IntegerField()

    # Validation: text validation
    studio = models.CharField(max_length=50)

    
class Screenshot(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='screenshots')
    
    # Validation: text validation
    name = models.CharField(max_length=100)
