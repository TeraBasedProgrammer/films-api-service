from django.db.models import Q
from rest_framework import generics

from .models import Actor
from .serializers import ActorSerializer, ActorListSerializer


# Films views
class ActorListCreateView(generics.ListCreateAPIView):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActorListSerializer
        elif self.request.method == 'POST':
            return ActorSerializer


actor_list_create = ActorListCreateView.as_view()


class ActorDetailAPIView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


actor_retrieve = ActorDetailAPIView.as_view()


class ActorUpdateAPIView(generics.UpdateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


actor_update = ActorUpdateAPIView.as_view()


class ActorDeleteAPIView(generics.DestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


actor_delete = ActorDeleteAPIView.as_view()


class ActorSearchView(generics.ListAPIView):
    model = Actor
    serializer_class = ActorListSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Actor.objects.filter(
             Q(title__icontains=query)
        )
        return object_list


actor_search = ActorSearchView.as_view()
