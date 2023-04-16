from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Actor
from films.models import Film
from films.validators import validate_image
from .services import initialize_photo


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
        # Retrieving photo image
        photo_image = validated_data.pop('photo_image')

        films_data = validated_data.pop('films')

        actor = Actor.objects.create(photo_format=photo_image.content_type.split("/")[1], **validated_data)
        actor.films.set(films_data)

        initialize_photo(photo_image, actor)
        return actor

