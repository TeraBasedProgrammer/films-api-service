import logging

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from films.models import Film
from films.serializers import (CustomHyperlinkedIdentityField,
                               FilmListSerializer)

from .models import Playlist

logger = logging.getLogger('logger')


class PlaylistListSerializer(serializers.ModelSerializer):
    url = CustomHyperlinkedIdentityField(
        view_name='playlist_retrieve',
        lookup_field='slug',
    )

    class Meta:
        model = Playlist
        fields = [
            # Model fields
            'title',

            # Additional fields
            'url',
        ]


class PlaylistSerializer(serializers.ModelSerializer):
    films = serializers.SlugRelatedField(queryset=Film.objects.all(), many=True, required=False, slug_field='slug')
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Playlist
        extra_kwargs = {
            "slug": {"read_only": True},
            "user": {"read_only": True},
        }
        fields = [
            # Model fields
            'slug',
            'user',
            'title',
            'films',
            'is_default',
        ]

    def create(self, validated_data):
        logger.info('Creating new Playlist instance')
        # Retrieving related films data
        films_data = validated_data.pop('films', None)

        # Set is_default for reserved titles
        validated_data['is_default'] = False
        if validated_data['title'] in ['Watched', 'See later']:
            validated_data['is_default'] = True
        
        validated_data['user'] = self.context.get('request').user

        playlist = Playlist.objects.create(**validated_data)


        if films_data:
            playlist.films.set(films_data)
        logger.info(f'Successfully created "{str(playlist)}" instance')
        return playlist

    def update(self, instance, validated_data):
        # Simple fields update
        if instance.is_default and validated_data.get('title'):
            raise PermissionDenied(detail="Cannot change title of default lists ('Watch', 'See later'.)", code=403)

        instance.title = validated_data.get('title', instance.title)

        # Complicated fields update
        films_data = validated_data.get('films')

        if films_data:
            instance.films.set(films_data)

        instance.save()
        return instance

    # Changing representation of films field from just PK's to serialized objects
    def to_representation(self, instance):
        logger.info(f'Serializing "{str(instance)}" related films (for GET request)...')
        ret = super().to_representation(instance)
        ret['films'] = FilmListSerializer(instance.films.all(), many=True,
                                          context={'request': self.context.get('request')}).data

        logger.info(f'Successfully serialized "{str(instance)}" related films')
        return ret



