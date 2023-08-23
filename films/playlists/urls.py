from django.urls import path

from .views import (playlist_delete, playlist_list_create, playlist_retrieve,
                    playlist_search, playlist_update)

urlpatterns = [
    path('', playlist_list_create),
    path('search/', playlist_search),
    path('<slug:slug>/', playlist_retrieve, name='playlist_retrieve'),
    path('<slug:slug>/update/', playlist_update),
    path('<slug:slug>/delete/', playlist_delete),
]
