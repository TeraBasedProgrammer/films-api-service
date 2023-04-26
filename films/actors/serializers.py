import logging

from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Actor
from films.models import Film
from films.validators import validate_image
from .services import initialize_photo


logger = logging.getLogger('logger')


class ActorListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='actor_retrieve',
        lookup_field='pk'
    )
    photo_file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Actor
        fields = [
            'pk',
            'name',
            'photo_file',
            'url',
        ]

    def get_photo_file(self, obj):
        return f'https://actors-screenshots.s3.eu-north-1.amazonaws.com/{obj.pk}/photo.{obj.photo_format}'


class ActorSerializer(serializers.ModelSerializer):
    photo_image = Base64ImageField(write_only=True, validators=[validate_image])
    photo_file = serializers.SerializerMethodField(read_only=True)

    # Field for listing related films (drf doesn't see this field from model, so it has to be in serializer)
    films = serializers.PrimaryKeyRelatedField(queryset=Film.objects.all(), many=True)

    class Meta:
        model = Actor
        fields = [
            'pk',
            'name',
            'age',
            'description',
            'photo_file',
            'photo_image',
            'films',
        ]

    def get_photo_file(self, obj):
        return f'https://actors-screenshots.s3.eu-north-1.amazonaws.com/{obj.pk}/photo.{obj.photo_format}'

    def create(self, validated_data):
        logger.info('Creating new Actor instance...')
        # Retrieving photo image
        photo_image = validated_data.pop('photo_image')

        films_data = validated_data.pop('films')

        actor = Actor.objects.create(photo_format=photo_image.content_type.split("/")[1], **validated_data)
        actor.films.set(films_data)

        initialize_photo(photo_image, actor)
        logger.info(f'Successfully created "{str(actor)}" instance')
        return actor

    def to_representation(self, instance):
        logger.info(f'Serializing "{str(instance)}" related films (for GET request)...')

        # Local import to avoid circular import
        from films.serializers import FilmListSerializer

        ret = super().to_representation(instance)
        ret['films'] = FilmListSerializer(instance.films.all(), many=True,
                                            context={'request': self.context.get('request')}).data
        logger.info(f'Successfully serialized "{str(instance)}" related films')
        return ret

