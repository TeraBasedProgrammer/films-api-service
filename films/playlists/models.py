from django.db import models


class Playlist(models.Model):
    title = models.CharField(max_length=50)
    user_id = models.IntegerField()
    films = models.ManyToManyField('films.Film')

    class Meta:
        unique_together = ['title', 'user_id']

    def __str__(self):
        return self.title
