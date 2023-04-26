from django.db.models import Q
from rest_framework import generics

from .models import Film, Genre
from .serializers import FilmSerializer, FilmListSerializer, GenreSerializer
from .services import clean_s3_model_data


# Films views
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


film_retrieve = FilmDetailAPIView.as_view()


class FilmUpdateAPIView(generics.UpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


film_update = FilmUpdateAPIView.as_view()


class FilmDeleteAPIView(generics.DestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    def delete(self, request, *args, **kwargs):
        clean_s3_model_data(self.get_object())
        return self.destroy(request, *args, **kwargs)


film_delete = FilmDeleteAPIView.as_view()


class FilmSearchView(generics.ListAPIView):
    model = Film
    serializer_class = FilmListSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Film.objects.filter(
             Q(title__icontains=query)
        )
        return object_list


film_search = FilmSearchView.as_view()


# Genre views
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


genre_list_create = GenreListCreateView.as_view()


class GenreDetailAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


genre_retrieve = GenreDetailAPIView.as_view()


class GenreUpdateAPIView(generics.UpdateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


genre_update = GenreUpdateAPIView.as_view()


class GenreDeleteAPIView(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


genre_delete = GenreDeleteAPIView.as_view()


class GenreSearchView(generics.ListAPIView):
    model = Genre
    serializer_class = GenreSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Film.objects.filter(
             Q(title__icontains=query)
        )
        return object_list


genre_search = GenreSearchView.as_view()
