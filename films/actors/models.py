from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    description = models.TextField()

    # Format of the actor image (it has the same name, format can only change)
    photo_format = models.CharField(max_length=4)

    def __str__(self):
        return self.name
