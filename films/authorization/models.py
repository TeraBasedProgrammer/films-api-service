import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from playlists.models import Playlist

logger = logging.getLogger('logger')

@receiver(post_save, sender=User, dispatch_uid='create_default_playlists')
def create_default_playlists(sender, instance, **kwargs):
    logger.info(f'Creating user {instance.username} default playlists...')
    Playlist.objects.create(title='Watch later', user=instance, is_default=True)
    Playlist.objects.create(title='Favourites', user=instance, is_default=True)
    logger.info(f'Successfully created user {instance.username} default playlists')


