import logging

from django.db import transaction
from django.utils.text import slugify
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from films.models import Film
from films.serializers import CustomHyperlinkedIdentityField
from films.validators import validate_image

from .models import Actor
from .services import initialize_photo

logger = logging.getLogger('logger')


class ActorListSerializer(serializers.ModelSerializer):
    url = CustomHyperlinkedIdentityField(
        view_name='actor_retrieve',
        lookup_field='slug'
    )
    photo_file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Actor
        fields = [
            'name',
            'photo_file',
            'url',
        ]

    def get_photo_file(self, obj):
        return f'https://actors-screenshots.s3.eu-north-1.amazonaws.com/{obj.slug}/photo.{obj.photo_format}'


class ActorSerializer(serializers.ModelSerializer):
    photo_image = Base64ImageField(write_only=True, validators=[validate_image])
    photo_file = serializers.SerializerMethodField(read_only=True)

    # Field for listing related films (drf doesn't see this field from model, so it has to be in serializer)
    films = serializers.SlugRelatedField(queryset=Film.objects.all(), many=True, slug_field='slug')
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Actor
        fields = [
            'slug',
            'name',
            'birth_date',
            'death_date',
            'description',
            'photo_file',
            'photo_image',
            'films',
        ]

    def get_photo_file(self, obj):
        return f'https://actors-screenshots.s3.eu-north-1.amazonaws.com/{obj.slug}/photo.{obj.photo_format}'
    
    def validate(self, data):
        birth_date = data.get('birth_date')
        death_date = data.get('death_date')

        if birth_date and death_date and death_date < birth_date:
            raise serializers.ValidationError("Death date cannot be earlier than birth date.")

        return data


    def create(self, validated_data):
        logger.info('Creating new Actor instance...')
        
        # Retrieving photo image
        photo_image = validated_data.pop('photo_image')

        films_data = validated_data.pop('films')

        with transaction.atomic():
            actor = Actor.objects.create(photo_format=photo_image.content_type.split("/")[1], **validated_data)
            actor.slug = slugify(actor.name)
            actor.films.set(films_data)

            initialize_photo(photo_image, actor)
            logger.info(f'Successfully created "{str(actor)}" instance')
            return actor

    def update(self, instance, validated_data):
        # Simple fields update
        instance.name = validated_data.get('name', instance.name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.death_date = validated_data.get('death_date', instance.death_date)
        instance.description = validated_data.get('description', instance.description)

        # Complicated fields update
        photo_image = validated_data.get('photo_image')
        films_data = validated_data.get('films')

        if films_data:
            instance.films.set(films_data)

        with transaction.atomic():
            if photo_image:
                initialize_photo(photo_image, instance)

            instance.save()
            return instance

    def to_representation(self, instance):
        logger.info(f'Serializing "{str(instance)}" related films (for GET request)...')

        # Local import to avoid circular import
        from films.serializers import FilmListSerializer

        ret = super().to_representation(instance)
        ret['films'] = FilmListSerializer(instance.films.all(), many=True,
                                            context={'request': self.context.get('request')}).data
        logger.info(f'Successfully serialized "{str(instance)}" related films')
        return ret

