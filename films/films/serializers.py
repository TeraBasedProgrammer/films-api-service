from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Film, Screenshot
from .services import get_cached_imdb_response, initialize_images
from .validators import validate_imdb_id, validate_rating, validate_age_restriction, validate_text, validate_image


class ScreenshotSerializer(serializers.ModelSerializer):
    image = Base64ImageField(write_only=True, validators=[validate_image])

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
    poster_file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Film
        fields = [
            'title',
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
            'studio',
            'imdb_id',
            'imdb_rating',
            'screenshots',
        ]

    def get_poster_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.pk}/poster.{obj.poster_format}'

    def create(self, validated_data):
        # Retrieving and initializing film imDb rating
        imdb_id = validated_data.pop('imdb_id')
        validated_data['imdb_rating'] = get_cached_imdb_response(imdb_id)

        # Retrieving and initializing screenshots and poster data
        screenshots_data = validated_data.pop('screenshots')
        poster_image = validated_data.pop('poster_image')

        # Creates film instance and manually sets up poster_format field
        film = Film.objects.create(poster_format=poster_image.content_type.split("/")[1], **validated_data)
        initialize_images(poster_image, screenshots_data, film)
        return film
