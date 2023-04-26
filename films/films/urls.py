from django.urls import path

from .views import (film_list_create, film_retrieve, film_update, film_delete, film_search,
                    genre_list_create, genre_retrieve, genre_update, genre_delete, genre_search)

urlpatterns = [
    # films
    path('', film_list_create),
    path('<int:pk>/', film_retrieve, name='film_retrieve'),
    path('<int:pk>/update', film_update),
    path('<int:pk>/delete', film_delete),
    path('search/', film_search),

    # genres
    path('genres/', genre_list_create),
    path('genres/<int:pk>/', genre_retrieve),
    path('genres/<int:pk>/update', genre_update),
    path('genres/<int:pk>/delete', genre_delete),
    path('genres/search/', genre_search),

]
