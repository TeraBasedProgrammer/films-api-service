from rest_framework import serializers
from .models import Playlist
from films.models import Film
from films.serializers import FilmListSerializer


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
            'pk',
            'title',
            'films',
        ]

    def create(self, validated_data):
        # Retrieving related films data
        films_data = validated_data.pop('films')

        playlist = Playlist.objects.create(**validated_data)
        playlist.films.set(films_data)
        return playlist

    # Changing representation of films field from just PK's to serialized objects
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['films'] = FilmListSerializer(instance.films.all(), many=True,
                                          context={'request': self.context.get('request')}).data
        return ret



