import re

from django.db.models.query import QuerySet

from .models import Actor


def filter_actors(queryset: QuerySet[Actor], request) -> QuerySet[Actor]:
    ...