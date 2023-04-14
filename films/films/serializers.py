from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Film, Screenshot, Actor, Genre
from .services import get_cached_imdb_response, initialize_images
from .validators import validate_imdb_id, validate_rating, validate_age_restriction, validate_text, validate_image


class ScreenshotSerializer(serializers.ModelSerializer):
    # Model fields
    file = serializers.SerializerMethodField(read_only=True)

    # Additional fields
    compressed_file = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(write_only=True, validators=[validate_image])

    class Meta:
        model = Screenshot
        fields = [
            # Model fields
            'file',

            # Additional fields
            'compressed_file',
            'image',
        ]

    def get_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.film.pk}/{obj.file}'

    def get_compressed_file(self, obj):
        return f'https://films-compressed-screenshots.s3.eu-central-1.amazonaws.com/{obj.film.pk}/{obj.file}'


class FilmListSerializer(serializers.ModelSerializer):
    # Additional fields
    url = serializers.HyperlinkedIdentityField(
        view_name='film_retrieve',
        lookup_field='pk'
    )
    poster_file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Film
        fields = [
            # Model fields
            'title',

            # Additional fields
            'poster_file',
            'url',
        ]

    def get_poster_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.pk}/poster.{obj.poster_format}'


class FilmSerializer(serializers.ModelSerializer):
    # Model fields
    title = serializers.CharField(validators=[validate_text])
    country = serializers.CharField(validators=[validate_text])
    director = serializers.CharField(validators=[validate_text])
    description = serializers.CharField(validators=[validate_text]) 
    studio = serializers.CharField(validators=[validate_text])
    rating = serializers.DecimalField(max_digits=4, decimal_places=2, validators=[validate_rating])
    age_restriction = serializers.IntegerField(validators=[validate_age_restriction])

    # Additional fields
    imdb_id = serializers.CharField(write_only=True, validators=[validate_imdb_id])
    screenshots = ScreenshotSerializer(many=True)
    poster_file = serializers.SerializerMethodField(read_only=True)
    poster_image = Base64ImageField(write_only=True, validators=[validate_image])

    class Meta:
        model = Film
        fields = [
            # Model fields
            'pk',
            'title',
            'poster_file',
            'poster_image',
            'rating',
            'country',
            'release_date',
            'actors',
            'genres',
            'director',
            'description',
            'age_restriction',
            'imdb_rating',
            'studio',

            # Additional fields
            'imdb_id',
            'screenshots',
        ]

    def get_poster_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.pk}/poster.{obj.poster_format}'

    def create(self, validated_data):
        # Retrieving and initializing film imDb rating
        imdb_id = validated_data.pop('imdb_id')
        validated_data['imdb_rating'] = get_cached_imdb_response(imdb_id)

        # Retrieving screenshots and poster data
        screenshots_data = validated_data.pop('screenshots')
        poster_image = validated_data.pop('poster_image')

        # Create film instance, manually set up poster_format field and many-to-many fields
        actors_data = validated_data.pop('actors')
        genres_data = validated_data.pop('genres')

        film = Film.objects.create(poster_format=poster_image.content_type.split("/")[1], **validated_data)
        film.actors.set(actors_data)
        film.genres.set(genres_data)

        initialize_images(poster_image, screenshots_data, film)
        return film
