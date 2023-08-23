from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Playlist
from .serializers import PlaylistListSerializer, PlaylistSerializer


# Playlists views
class PlaylistListCreateView(generics.ListCreateAPIView):
    lookup_field = 'slug'
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlaylistListSerializer
        elif self.request.method == 'POST':
            return PlaylistSerializer

    def get_queryset(self):
        queryset = Playlist.objects.filter(user=self.request.user)
        return queryset


playlist_list_create = PlaylistListCreateView.as_view()


class PlaylistDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PlaylistSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)


playlist_retrieve = PlaylistDetailAPIView.as_view()


class PlaylistUpdateAPIView(generics.UpdateAPIView):
    queryset = Playlist.objects.all()
    lookup_field = 'slug'
    serializer_class = PlaylistSerializer


playlist_update = PlaylistUpdateAPIView.as_view()


class PlaylistDeleteAPIView(generics.DestroyAPIView):
    lookup_field = 'slug'
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    # Overriden 'delete' method for prevention of deleting default playlists
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_default:
            raise PermissionDenied(detail="Cannot delete a default playlist.", code=403)

        return super().destroy(request, *args, **kwargs)


playlist_delete = PlaylistDeleteAPIView.as_view()


class PlaylistSearchView(generics.ListAPIView):
    model = Playlist
    serializer_class = PlaylistListSerializer

    def get_queryset(self):
        query = self.request.GET.get("q", default="")
        object_list = Playlist.objects.filter(
            Q(title__icontains=query) &
            Q(user=self.request.user)
        )
        return object_list


playlist_search = PlaylistSearchView.as_view()
