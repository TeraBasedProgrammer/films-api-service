from rest_framework import serializers
from .models import Film, Screenshot
from .validators import validate_imdb_id

import requests_cache
import json
import os

from .validators import validate_imdb_id, validate_rating, validate_age_restriction, validate_text


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = [
            'name',
        ]


class FilmListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='film_retrieve',
        lookup_field='pk'
    )

    class Meta:
        model = Film
        fields = [
            'title',
            'poster_name',
            'url',
        ]


class FilmSerializer(serializers.ModelSerializer):
    # screenshots = ScreenshotSerializer(many=True)
    
    title = serializers.CharField(validators=[validate_text])
    country = serializers.CharField(validators=[validate_text])
    director = serializers.CharField(validators=[validate_text])
    description = serializers.CharField(validators=[validate_text]) 
    studio = serializers.CharField(validators=[validate_text])
    
    imdb_id = serializers.CharField(write_only=True, validators=[validate_imdb_id])
    rating = serializers.DecimalField(max_digits=4, decimal_places=2, validators=[validate_rating])
    age_restriction = serializers.IntegerField(validators=[validate_age_restriction])

    class Meta:
        model = Film
        fields = [
            'pk',
            'title',
            'poster_name',
            'rating',
            'country',
            'release_date',
            'director',
            'description',
            'age_restriction',
            'studio',
            'imdb_id',
            'imdb_rating',
            # 'screenshots',
        ] 

    def create(self, validated_data):
        # Retrieving film imDb rating
        session = requests_cache.CachedSession(cache_name=f'{os.path.dirname(__file__)}/cache/imdb-cache', backend='sqlite', expire_after=600)
        response = json.loads((session.get('https://imdb-api.com/en/API/Ratings/k_92xc2azh/%s' % validated_data.pop('imdb_id')).content.decode('utf-8')))
        validated_data['imdb_rating'] = response['imDb']

        # Retrieving screenshots
        # screenshots_data = validated_data.pop('screenshots')
        film = Film.objects.create(**validated_data)
        # for screenshot_data in screenshots_data:
        #     Screenshot.objects.create(film=film, **screenshot_data)

        return film
            
    # actors - дополнительное поле в сериализаторе (делать запрос на сторонний API)


