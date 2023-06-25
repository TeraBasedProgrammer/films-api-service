from django.urls import path
from .views import playlist_list_create, playlist_retrieve, playlist_update, playlist_delete, playlist_search


urlpatterns = [
    path('', playlist_list_create),
    path('search/', playlist_search),
    path('<pk>/', playlist_retrieve, name='playlist_retrieve'),
    path('<pk>/update/', playlist_update),
    path('<pk>/delete/', playlist_delete),
]
