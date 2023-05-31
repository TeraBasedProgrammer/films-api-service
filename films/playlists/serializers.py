import logging

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .models import Playlist
from films.models import Film
from films.serializers import FilmListSerializer, CustomHyperlinkedIdentityField


logger = logging.getLogger('logger')


class PlaylistListSerializer(serializers.ModelSerializer):
    url = CustomHyperlinkedIdentityField(
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
    films = serializers.PrimaryKeyRelatedField(queryset=Film.objects.all(), many=True, required=False)

    class Meta:
        model = Playlist
        fields = [
            # Model fields
            'pk',
            'title',
            'films',
            'user_id',
            'user_type',
        ]

    # def validate(self, attrs):
        # return attrs

    def create(self, validated_data):
        logger.info('Creating new Playlist instance')
        # Retrieving related films data
        films_data = validated_data.get('films')
        user_type = validated_data.get('user_type')

        # Set is_default for reserved titles
        is_default = False
        if validated_data['title'] in ['Watched', 'See later']:
            is_default = True

        related_playlists = Playlist.objects.filter(user_id=validated_data['user_id'])

        if user_type == 'basic' and len(related_playlists) == 2:
            raise PermissionDenied(detail='Playlist limit for this user has been exceeded', code=403)

        if len(related_playlists) == 10:
            raise PermissionDenied(detail='Films limit in this playlist has been exceeded', code=403)

        playlist = Playlist.objects.create(is_default=is_default, **validated_data)

        if films_data:
            films_sequence = set([film.pk for film in films_data])
            if validated_data['title'] != 'Watched':
                if playlist.user_type == 'basic' and len(films_sequence) > 10 or playlist.user_type in ['admin', 'premium'] and len(films_sequence) > 30:
                    raise PermissionDenied(detail='Films limit in this playlist has been exceeded', code=403)

            playlist.films.set(films_data)

        logger.info(f'Successfully created "{str(playlist)}" instance')

        return playlist

    def update(self, instance, validated_data):
        # Simple fields update
        if instance.is_default and validated_data.get('title'):
            raise PermissionDenied(detail="Cannot change title of default lists ('Watch', 'See later'.)", code=403)

        instance.title = validated_data.get('title', instance.title)
        instance.user_type = validated_data.get('user_type', instance.user_type)

        # Complicated fields update
        films_data = validated_data.get('films')

        if films_data:
            films_sequence = set([film.pk for film in films_data])
            if instance.title != 'Watched':
                print(instance.user_type)
                print(instance.user_type == 'basic', len(films_sequence) > 10, instance.user_type in ['admin', 'premium'],  len(films_sequence) > 30)
                if instance.user_type == 'basic' and len(films_sequence) > 10 or instance.user_type in ['admin', 'premium'] and len(films_sequence) > 30:
                    raise PermissionDenied(detail='Films limit in this playlist has been exceeded', code=403)

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



