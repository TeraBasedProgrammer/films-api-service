from rest_framework.response import Response
from rest_framework import generics, mixins, authentication 
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


from .models import Film
from .serializers import FilmSerializer, FilmListSerializer


class FilmListCreateView(generics.ListCreateAPIView):
    queryset = Film.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FilmListSerializer
        elif self.request.method == 'POST':
            return FilmSerializer


film_list_create = FilmListCreateView.as_view()


class FilmDetailAPIView(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    # lookup_field = 'pk' 


film_retrieve = FilmDetailAPIView.as_view()


class FilmUpdateAPIView(generics.UpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


film_update = FilmUpdateAPIView.as_view()


class FilmDeleteAPIView(generics.DestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    # lookup_field = 'pk'


film_delete = FilmDeleteAPIView.as_view()