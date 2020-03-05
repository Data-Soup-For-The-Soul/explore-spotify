import requests
from datetime import date

from django.db import models

from feed_spotify.settings import SPOTIFY_AUDIO_FEATURES_URL
from spotify.auth import get_auth

SPOTIFY_HEADERS = get_auth()


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
    danceability = models.FloatField(null=True)
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

    def set_metrics(self):

        """
        {
          "duration_ms" : 255349,
          "key" : 5,
          "mode" : 0,
          "time_signature" : 4,
          "acousticness" : 0.514,
          "danceability" : 0.735,
          "energy" : 0.578,
          "instrumentalness" : 0.0902,
          "liveness" : 0.159,
          "loudness" : -11.840,
          "speechiness" : 0.0461,
          "valence" : 0.624,
          "tempo" : 98.002,
          "id" : "06AKEBrKUckW0KREUWRnvT",
          "uri" : "spotify:track:06AKEBrKUckW0KREUWRnvT",
          "track_href" : "https://api.spotify.com/v1/tracks/06AKEBrKUckW0KREUWRnvT",
          "analysis_url" : "https://api.spotify.com/v1/audio-analysis/06AKEBrKUckW0KREUWRnvT",
          "type" : "audio_features"
        }
        """
        url = SPOTIFY_AUDIO_FEATURES_URL.format(id=self.identifier)
        response = requests.get(url, headers=SPOTIFY_HEADERS)
        if response and response.code == 200:
            self.duration = response.get('duration_ms')
            self.key = response.get('key')
            self.mode = response.get('mode')
            self.time_signature = response.get('time_signature')
            self.acousticness = response.get('acousticness')
            self.danceability = response.get('danceability')
            self.instrumentalness = response.get('instrumentalness')
            self.liveness = response.get('liveness')
            self.loudness = response.get('loudness')
            self.speechiness = response.get('speechiness')
            self.valence = response.get('valence')
            self.tempo = response.get('tempo')
            self.save()
            return True
        else:
            print('API Miss for', self.identifier)
            return False


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





