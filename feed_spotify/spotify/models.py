from datetime import date

from django.db import models


class Artist(models.Model):
    """Naively holds featured artists as separate artists"""

    name = models.CharField(null=False, db_index=True, max_length=255)


class Track(models.Model):
    """
    https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/
    """

    name = models.CharField(null=False, db_index=True, max_length=255)
    artist = models.ForeignKey(Artist, null=False, on_delete=models.CASCADE, related_name='tracks')
    identifier = models.SlugField(null=False, db_index=True, unique=True)  # Spotify's Unique Track Identifer

    energy = models.FloatField(null=True)
    key = models.PositiveSmallIntegerField(null=True)
    loudness = models.FloatField(null=True)
    mode = models.PositiveSmallIntegerField(null=True)
    speechiness = models.FloatField(null=True)
    acousticness = models.FloatField(null=True)
    instrumentalness = models.FloatField(null=True)
    liveness = models.FloatField(null=True)
    valence = models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    liveness = models.FloatField(null=True)
    time_signature = models.PositiveSmallIntegerField(null=True)
    duration = models.PositiveIntegerField(null=True)

    # album. FF

    @staticmethod
    def get(track_name: str, track_id: int, artist_name: str):
        """Gets a track by spotify uri. Creates an artist if needed."""

        artist = Artist.objects.get_or_create(name=artist_name)
        track, created = artist.tracks.get_or_create(
            identifier=track_id, defaults={'name': track_name, 'identifier': track_id}
        )
        return track, created


class Hit(models.Model):
    """A position on a country's Top Charts. For this app, write only"""

    position = models.PositiveSmallIntegerField(null=False)
    track = models.ForeignKey(Track, null=False, on_delete=models.CASCADE, related_name='hits')
    streams = models.PositiveIntegerField(null=True)
    country = models.CharField(null=False, max_length=10)
    week_of = models.DateField(null=False)

    @staticmethod
    def set(track_name: str, track_id: int, artist_name: str, position: int, streams: int, country: str, week_of: date):

        track, _ = Track.get(track_name, track_id, artist_name)
        hit = track.hits.create(position=position, streams=streams, country=country, week_of=week_of)
        return hit




