from django.db.models import Q
from rest_framework import generics

from .models import Playlist
from .serializers import PlaylistSerializer, PlaylistListSerializer


# Playlists views
class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlaylistListSerializer
        elif self.request.method == 'POST':
            return PlaylistSerializer


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


class FilmSearchView(generics.ListAPIView):
    model = Playlist
    serializer_class = PlaylistListSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Playlist.objects.filter(
            Q(title__icontains=query)
        )
        return object_list


playlist_search = FilmSearchView.as_view()
