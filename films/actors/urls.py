from django.urls import path

from .views import *

urlpatterns = [
    path('', actor_list_create),
    path('search/', actor_search),
    path('<slug:slug>/', actor_retrieve, name='actor_retrieve'),
    path('<slug:slug>/update/', actor_update),
    path('<slug:slug>/delete/', actor_delete),
]
