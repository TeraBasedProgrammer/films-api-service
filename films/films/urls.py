from django.urls import path

from .views import (film_list_create, film_retrieve, film_update, film_delete, film_search,
                    genre_list_create, genre_retrieve, genre_update, genre_delete, genre_search,
                    country_list_view)

urlpatterns = [
    # countries
    path('countries/', country_list_view),

    # genres
    path('genres/', genre_list_create),
    path('genres/<slug:slug>/', genre_retrieve),
    path('genres/<slug:slug>/update/', genre_update),
    path('genres/<slug:slug>/delete/', genre_delete),
    path('genres/search/', genre_search),

    # films
    path('', film_list_create),
    path('<slug:slug>/', film_retrieve, name='film_retrieve'),
    path('<slug:slug>/update/', film_update),
    path('<slug:slug>/delete/', film_delete),
    path('search/', film_search),
]
