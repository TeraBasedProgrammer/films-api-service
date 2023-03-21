from django.db import models


class Film(models.Model):

    # Добавить базовую валидацию полей

    title = models.CharField(max_length=50)
    poster_name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    country = models.CharField(max_length=50)
    realese_date = models.DateField()
    director = models.CharField(max_length=50)
    description = models.TextField()
    age_restriction = models.IntegerField()
    studio = models.CharField(max_length=50)
    
    # imdb_film_id - cделать write_only field в сериализаторе, запрашивать fild + валидация на 'tt' в начале
    # imdb_rating  - cделать дополнительным полем в сериализаторе (парсить json-ответ от imdb)
    # actors - дополнительное поле в сериализаторе (делать запрос на сторонний API)

class Screenshot(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='screenshots')
    name = models.CharField(max_length=100)
