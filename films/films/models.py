from django.db import models


class Film(models.Model):

    # Add model validations

    # Validation: text validation
    title = models.CharField(max_length=50)

    # Validation: text validation
    poster_name = models.CharField(max_length=100)
    
    # Validation: should be from 0.00 to 10.00 ✅
    rating = models.DecimalField(max_digits=4, decimal_places=2)

    # Validation: validated in serializer ✅
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2, editable=False)
    
    # Validation: text validation
    country = models.CharField(max_length=50)

    # Validation: text validation
    release_date = models.DateField()

    # Validation: text validation
    director = models.CharField(max_length=50)

    # Validation: text validation
    description = models.TextField()

    # Validation: should be from 0 to 21
    age_restriction = models.IntegerField()

    # Validation: text validation
    studio = models.CharField(max_length=50)

    
    


class Screenshot(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='screenshots')
    name = models.CharField(max_length=100)
