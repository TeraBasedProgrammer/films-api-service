from django.db import models


class Playlist(models.Model):
    title = models.CharField(max_length=50)

    # Id of the owner of the playlist
    user_id = models.IntegerField()
    is_default = models.BooleanField(default=False)

    films = models.ManyToManyField('films.Film', blank=True)
    user_type = models.CharField(max_length=7, default='basic')

    class Meta:
        unique_together = ['title', 'user_id']

    def __str__(self):
        return self.title
