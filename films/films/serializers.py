import logging

from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Film, Screenshot, Genre
from .services import get_cached_imdb_response, initialize_images
from .validators import validate_imdb_id, validate_image
from actors.models import Actor



logger = logging.getLogger('logger')


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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'pk',
            'title',
        ]

    def create(self, validated_data):
        logger.info('Creating new Genre instance...')
        genre = Genre.objects.create(**validated_data)
        logger.info(f'Successfully created "{str(genre)}" instance')
        return genre


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
    # Additional fields
    imdb_id = serializers.CharField(write_only=True, validators=[validate_imdb_id])
    screenshots = ScreenshotSerializer(many=True)
    poster_file = serializers.SerializerMethodField(read_only=True)
    poster_image = Base64ImageField(write_only=True, validators=[validate_image])

    # Field for listing related actors (drf doesn't see this field from model, so it has to be in serializer)
    actors = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True)

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

    # General instance validation by 3 fields
    def validate(self, data):
        existing_film = Film.objects.filter(title__iexact=data['title'],
                                            release_date=data['release_date'],
                                            director__iexact=data['director'])
        if existing_film:
            validation_error_message = 'Film with such parameters (title, director, release date) already exists'
            logger.warning(f'Validation error - {validation_error_message}')
            raise serializers.ValidationError(validation_error_message)
        return data

    def create(self, validated_data):
        logger.info('Creating new Film instance...')

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
        logger.info(f'Successfully created "{str(film)}" instance')
        return film

    # Changing representation of actors and genres fields from just PK's to serialized objects
    def to_representation(self, instance):
        logger.info(f'Serializing "{str(instance)}" related actors and geres (for GET request)...')

        # Local import to avoid circular import
        from actors.serializers import ActorListSerializer

        ret = super().to_representation(instance)
        ret['actors'] = ActorListSerializer(instance.actors.all(), many=True,
                                            context={'request': self.context.get('request')}).data
        ret['genres'] = GenreSerializer(instance.genres.all(), many=True).data

        logger.info(f'Successfully serialized "{str(instance)}" related actors and genresS')
        return ret


