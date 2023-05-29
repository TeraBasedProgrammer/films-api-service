from django.db.models import Q
from rest_framework import generics
from rest_framework.serializers import ValidationError

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
    
    # def g``
    # if self.request.method == 'GET':
    #     user_id_q = self.request.GET.get("user_id")
    #     if not user_id_q:
    #         return ValidationError('You must provide "user_id" query parameter to get playlists of the specific user')
    #     else:
    #         try:
    #             user_id = int(user_id_q)
    #             return Playlist.objects.filter(user_id=user_id)
    #         except ValueError:
    #             return ValidationError('"user_id" query parameter must be Integer')
    def get_queryset(self):
        return super().get_queryset()


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
