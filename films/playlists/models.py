from django.db import models


class Playlist(models.Model):
    title = models.CharField(max_length=50, unique=True)
    films = models.ManyToManyField('films.Film')

    def __str__(self):
        return self.title
