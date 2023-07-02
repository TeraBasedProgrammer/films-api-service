import re

from django.db.models.query import QuerySet

from .models import Film


def filter_films(queryset: QuerySet[Film], request) -> QuerySet[Film]:
    from_date_q = request.get('release_date_after')
    to_date_q = request.get('release_date_before')
    country = request.get('country')
    genres = request.getlist('genre')
    order_by = request.get('order_by')

    # Check if order_by query parameter is allowed (else set it to 'pk')
    if order_by not in ['release_date', '-release_date',
                        'rating', '-rating']:
        order_by = '-release_date'
    else:
        pass

    if from_date_q and to_date_q:
        from_date = 1 if not re.match(r'^[1-9][0-9]*$', from_date_q) else int(from_date_q)
        to_date = 9999 if not re.match(r'^[1-9][0-9]*$', to_date_q) else int(to_date_q)
        queryset = queryset.filter(release_date__year__gte=from_date,
                                   release_date__year__lte=to_date).order_by(order_by)

    if country:
        queryset = queryset.filter(country__icontains=country).order_by(order_by)

    if genres and genres[0]:
        queryset = queryset.filter(genres__title__in=genres).order_by(order_by).distinct()

    return queryset.order_by(order_by)
