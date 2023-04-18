from django.urls import include, path
from .views import playlist_list_create, playlist_retrieve, playlist_update, playlist_delete, playlist_search


urlpatterns = [
    path('', playlist_list_create),
    path('<pk>/', playlist_retrieve, name='playlist_retrieve'),
    path('<pk>/update/', playlist_update),
    path('<pk>/delete/', playlist_delete),
    path('<pk>/search/', playlist_search),
]
