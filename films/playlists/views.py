from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import ParseError

from .models import Playlist
from .filters import filter_playlists
from .serializers import PlaylistSerializer, PlaylistListSerializer


# Playlists views
class PlaylistListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlaylistListSerializer
        elif self.request.method == 'POST':
            return PlaylistSerializer

    def list(self, request, *args, **kwargs):
        if 'user_id' not in request.query_params:
            raise ParseError(detail="user_id query parameter is required.", code=400)
        try:
            int(request.query_params['user_id'])
        except ValueError:
            raise ParseError(detail="user_id must be an integer.", code=400)

        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Playlist.objects.all()
            filtered_queryset = filter_playlists(queryset, self.request.GET)
            return filtered_queryset
        else:
            return Playlist.objects.all()


playlist_list_create = PlaylistListCreateView.as_view()


class PlaylistDetailAPIView(generics.RetrieveAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


playlist_retrieve = PlaylistDetailAPIView.as_view()


class PlaylistUpdateAPIView(generics.UpdateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


playlist_update = PlaylistUpdateAPIView.as_view()


class PlaylistDeleteAPIView(generics.DestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


playlist_delete = PlaylistDeleteAPIView.as_view()


class PlaylistSearchView(generics.ListAPIView):
    model = Playlist
    serializer_class = PlaylistListSerializer

    def get_queryset(self):
        query = self.request.GET.get("q", default="")
        object_list = Playlist.objects.filter(
            Q(title__icontains=query)
        )
        return object_list


playlist_search = PlaylistSearchView.as_view()
