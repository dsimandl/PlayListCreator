import spotipy
import json

from spotify_api_config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from spotipy import util


class SpotifyPlaylistCreator():

    def __init__(self, result_list):
        self.result_list = result_list

    def _get_sp_instance(self, scope):
        username = input("Enter your spotify username: ").strip()
        token = util.prompt_for_user_token(username, scope=scope, client_id=SPOTIFY_CLIENT_ID,
                                   client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='https://www.google.com')
        if token:
            sp = spotipy.Spotify(auth=token)
            return sp
        else:
            print("Can't get token for", username)

    def check_playlist(self, username):
        sp = self._get_sp_instance('playlist-read-private')
        if sp:
            playlists = sp.user_playlists(username)
            for playlist in playlists['items']:
                if playlist['name'] == 'TAS Top 20':
                    return playlist['id']
        else:
            print('Invalid Spotify instance for playlist read')
        sp = self._get_sp_instance('playlist-modify-private')
        if sp:
            results = sp.user_playlist_create(username, 'TAS Top 20', public=False)
            return results['id']
        else:
            print('Invalid Spotify instance for playlist create')

    def check_artist_and_set_track_list(self):
        valid_track_list = []
        sp = self._get_sp_instance('')
        for result in self.result_list:
            try:
                artist_song_search_result = sp.search(list(result)[1].string + " " + list(result)[3].string)
                if artist_song_search_result['tracks']['total'] == 0 \
                    or artist_song_search_result['tracks']['total'] > 10:
                    pass
                else:
                    valid_track_list.append(artist_song_search_result['tracks']['items']['id'])
            except IndexError:
                pass
        return valid_track_list

    def update_playlist(self, username, playlist_id, track_id_list):
        sp = self._get_sp_instance('playlist-modify-private')
        results = sp.user_playlist_add_tracks(username, playlist_id, track_id_list)
        return results






