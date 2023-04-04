from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Film, Screenshot
from .services import get_cached_imdb_response, initialize_screenshots
from .validators import validate_imdb_id, validate_rating, validate_age_restriction, validate_text, validate_image


class ScreenshotSerializer(serializers.ModelSerializer):
    image = Base64ImageField(write_only=True, validators=[validate_image])

    # Should contain extracted filename from 'image' field
    file = serializers.SerializerMethodField(read_only=True)
    compressed_file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Screenshot
        fields = [
            'file',
            'compressed_file',
            'image',
        ]

    def get_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.film.pk}/{obj.file}'

    def get_compressed_file(self, obj):
        return f'https://films-compressed-screenshots.s3.eu-central-1.amazonaws.com/{obj.film.pk}/{obj.file}'


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

    title = serializers.CharField(validators=[validate_text])
    country = serializers.CharField(validators=[validate_text])
    director = serializers.CharField(validators=[validate_text])
    description = serializers.CharField(validators=[validate_text]) 
    studio = serializers.CharField(validators=[validate_text])
    
    imdb_id = serializers.CharField(write_only=True, validators=[validate_imdb_id])
    rating = serializers.DecimalField(max_digits=4, decimal_places=2, validators=[validate_rating])
    age_restriction = serializers.IntegerField(validators=[validate_age_restriction])
    screenshots = ScreenshotSerializer(many=True)

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
            'screenshots',
        ] 

    def create(self, validated_data):
        # Retrieving film imDb rating
        validated_data['imdb_rating'] = get_cached_imdb_response(validated_data)

        # Retrieving and initializing screenshots data
        screenshots_data = validated_data.pop('screenshots')
        film = Film.objects.create(**validated_data)
        initialize_screenshots(screenshots_data, film)
        return film
            
    # actors - дополнительное поле в сериализаторе (делать запрос на сторонний API или на свою модель)


