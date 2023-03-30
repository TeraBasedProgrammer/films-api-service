from django.urls import path
from .views import film_list_create, film_retrieve, film_update, film_delete

urlpatterns = [
    path('', film_list_create),
    path('<int:pk>/', film_retrieve, name='film_retrieve'),
    path('<int:pk>/update', film_update),
    path('<int:pk>/delete', film_delete),
]
