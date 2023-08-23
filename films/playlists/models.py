from django.contrib.auth.models import User
from django.db import IntegrityError, models
from django.utils.text import slugify
from rest_framework.serializers import ValidationError


class Playlist(models.Model):
    title = models.CharField(max_length=50)

    # Id of the owner of the playlist
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    films = models.ManyToManyField('films.Film', blank=True)
    is_default = models.BooleanField(default=False)
    slug = models.SlugField()

    class Meta:
        unique_together = ['title', 'user']

    def save(self, *args, **kwargs):
        try:
            self.slug =  slugify(f'{self.title} {self.user.username}')
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError({"errors":["the user already has the playlist with this title"]})

    def __str__(self):
        return self.title
