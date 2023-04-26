from django.urls import path, include

from .views import *

urlpatterns = [
    path('', actor_list_create),
    path('<int:pk>/', actor_retrieve, name='actor_retrieve'),
    path('<int:pk>/update', actor_update),
    path('<int:pk>/delete', actor_delete),
    path('search/', actor_search),
]
