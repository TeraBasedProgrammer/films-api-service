from django.urls import path

from .views import (country_list_view, film_delete, film_list_create,
                    film_retrieve, film_search, film_update, genre_delete,
                    genre_list_create, genre_retrieve, genre_search,
                    genre_update)

urlpatterns = [
    # countries
    path('countries/', country_list_view),

    # genres
    path('genres/', genre_list_create),
    path('genres/search/', genre_search),
    path('genres/<slug:slug>/', genre_retrieve),
    path('genres/<slug:slug>/update/', genre_update),
    path('genres/<slug:slug>/delete/', genre_delete),

    # films
    path('', film_list_create),
    path('search/', film_search),
    path('<slug:slug>/', film_retrieve, name='film_retrieve'),
    path('<slug:slug>/update/', film_update),
    path('<slug:slug>/delete/', film_delete),
]
