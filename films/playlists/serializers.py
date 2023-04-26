import logging

from rest_framework import serializers

from .models import Playlist
from films.models import Film
from films.serializers import FilmListSerializer


logger = logging.getLogger('logger')


class PlaylistListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='playlist_retrieve',
        lookup_field='pk',
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
    films = serializers.PrimaryKeyRelatedField(queryset=Film.objects.all(), many=True)

    class Meta:
        model = Playlist
        fields = [
            # Model fields
            'pk',
            'title',
            'films',
        ]

    def create(self, validated_data):
        logger.info('Creating new Playlist instance')
        # Retrieving related films data
        films_data = validated_data.pop('films')

        playlist = Playlist.objects.create(**validated_data)
        playlist.films.set(films_data)

        logger.info(f'Successfully created "{str(playlist)}" instance')

    # Changing representation of films field from just PK's to serialized objects
    def to_representation(self, instance):
        logger.info(f'Serializing "{str(instance)}" related films (for GET request)...')
        ret = super().to_representation(instance)
        ret['films'] = FilmListSerializer(instance.films.all(), many=True,
                                          context={'request': self.context.get('request')}).data

        logger.info(f'Successfully serialized "{str(instance)}" related films')
        return ret



