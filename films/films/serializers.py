import logging

from actors.models import Actor
from django.conf import settings
from django.db import IntegrityError, transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Film, Genre, Screenshot
from .services import initialize_images
from .validators import validate_image

logger = logging.getLogger('logger')


# Custom URL class to handle remote AWS host
class CustomHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def __init__(self, *args, **kwargs):
        super(CustomHyperlinkedIdentityField, self).__init__(*args, **kwargs)
       
    def to_representation(self, value):
        request = self.context.get('request', None)
        if request is not None:
            scheme = 'http'
            if settings.DEBUG:
                host = request.get_host()
                if ':' not in host:
                    host += ':' + request.META['SERVER_PORT']
            else:
                host = settings.REMOTE_HOST
                if ':' not in host:
                    host += ':' + request.META['SERVER_PORT']
                scheme = 'http'
            self.context['request']._request.META['HTTP_HOST'] = host
            self.context['request']._request.META['wsgi.url_scheme'] = scheme
        return super(CustomHyperlinkedIdentityField, self).to_representation(value)


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
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.film.slug}/{obj.file}'

    def get_compressed_file(self, obj):
        return f'https://films-compressed-screenshots.s3.eu-central-1.amazonaws.com/{obj.film.slug}/{obj.file}'


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Genre
        fields = [
            'slug',
            'title',
        ]

    def create(self, validated_data):
        logger.info('Creating new Genre instance...')
        genre = Genre.objects.create(**validated_data)
        logger.info(f'Successfully created "{str(genre)}" instance')
        return genre


class FilmListSerializer(serializers.ModelSerializer):
    # Additional fields
    url = CustomHyperlinkedIdentityField(
        view_name='film_retrieve',
        lookup_field='slug'
    )

    poster_file = serializers.SerializerMethodField(read_only=True)
    compressed_poster_file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Film
        fields = [
            # Model fields
            'title',

            # Additional fields
            'poster_file',
            'compressed_poster_file',
            'url',
        ]

    def get_poster_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.slug}/poster.{obj.poster_format}'

    def get_compressed_poster_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.slug}/compressed-poster.{obj.poster_format}'


class FilmSerializer(serializers.ModelSerializer):
    # Additional fields
    screenshots = ScreenshotSerializer(many=True)
    # screenshots = serializers.ListField()
    poster_file = serializers.SerializerMethodField(read_only=True)
    compressed_poster_file = serializers.SerializerMethodField(read_only=True)
    poster_image = Base64ImageField(write_only=True, validators=[validate_image])

    # Field for listing related actors (drf doesn't see this field from model, so it has to be in serializer)
    actors = serializers.SlugRelatedField(queryset=Actor.objects.all(), many=True, slug_field='slug')
    genres = serializers.SlugRelatedField(queryset=Genre.objects.all(), many=True, slug_field='slug')
    slug = serializers.SlugField(read_only=True)
    

    class Meta:
        model = Film
        fields = [
            # Model fields
            'slug',
            'title',
            'poster_file',
            'compressed_poster_file',
            'poster_image',
            'rating',
            'country',
            'release_date',
            'genres',
            'actors',
            'director',
            'description',
            'content_rating',
            'studio',

            # Additional fields
            'screenshots',
        ]
    
    def get_poster_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.slug}/poster.{obj.poster_format}'

    def get_compressed_poster_file(self, obj):
        return f'https://films-screenshots.s3.eu-central-1.amazonaws.com/{obj.slug}/compressed-poster.{obj.poster_format}'


    def create(self, validated_data):
        logger.info('Creating new Film instance...')

        # Retrieving screenshots and poster data
        screenshots_data = validated_data.pop('screenshots')
        poster_image = validated_data.pop('poster_image')
        validated_data['poster_format'] = poster_image.content_type.split("/")[1]

        # Create film instance, manually set up poster_format field and many-to-many fields
        genres_data = validated_data.pop('genres')
        actors_data = validated_data.pop('actors')
        try:
            with transaction.atomic():
                film = Film.objects.create(**validated_data)
                film.actors.set(actors_data)
                film.genres.set(genres_data)

                initialize_images(poster_image, screenshots_data, film)
                if not film.screenshots.exists():
                    raise IntegrityError
                logger.info(f'Successfully created "{str(film)}" instance')
                return film
        except IntegrityError:
            raise APIException()

    def update(self, instance, validated_data):
        # Simple fields update
        instance.title = validated_data.get('title', instance.title)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.content_rating = validated_data.get('content_rating', instance.content_rating)
        instance.description = validated_data.get('description', instance.description)
        instance.director = validated_data.get('director', instance.director)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.country = validated_data.get('country', instance.country)
        instance.studio = validated_data.get('studio', instance.studio)

        # Complicated fields update
        actors_data = validated_data.get('actors')
        genres_data = validated_data.get('genres')

        if actors_data:
            instance.actors.set(actors_data)
        if genres_data:
            instance.genres.set(genres_data)

        poster_image = validated_data.get('poster_image')
        screenshots_data = validated_data.get('screenshots')

        if poster_image:
            poster_format = poster_image.content_type.split("/")[1]
            instance.poster_format = poster_format

        with transaction.atomic():
            if screenshots_data or poster_image:
                initialize_images(poster_image, screenshots_data, instance)

            instance.save()
            return instance

    # Changing representation of actors and genres fields from just PK's to serialized objects
    def to_representation(self, instance):
        logger.info(f'Serializing "{str(instance)}" related actors and genres (for GET request)...')

        # Local import to avoid circular import
        from actors.serializers import ActorListSerializer

        ret = super().to_representation(instance)
        ret['actors'] = ActorListSerializer(instance.actors.all(), many=True,
                                            context={'request': self.context.get('request')}).data
        ret['genres'] = GenreSerializer(instance.genres.all(), many=True).data

        logger.info(f'Successfully serialized "{str(instance)}" related actors and genres')
        return ret


