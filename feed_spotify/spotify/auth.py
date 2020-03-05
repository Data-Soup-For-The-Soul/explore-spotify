from typing import Dict
from spotipy.oauth2 import SpotifyClientCredentials


def get_auth() -> Dict:
    return SpotifyClientCredentials().get_access_token(as_dict=False)
