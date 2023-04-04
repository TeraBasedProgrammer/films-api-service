from django.db.models import Q
from rest_framework import generics


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


film_retrieve = FilmDetailAPIView.as_view()


class FilmUpdateAPIView(generics.UpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


film_update = FilmUpdateAPIView.as_view()


class FilmDeleteAPIView(generics.DestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


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
