from django.db.models.query import QuerySet

from .models import Playlist


def filter_playlists(queryset: QuerySet[Playlist], request):
    user_id = request.get('user_id')
    return queryset.filter(user_id=user_id)