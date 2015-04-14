from scraper_utils import ScraperUtils

class RdioAuthenticator:

    def set_rdio_instance(self):
        my_scraper_util = ScraperUtils()
        my_rdio_instance = my_scraper_util.autheniticate_me()
        return my_rdio_instance

    def _call_rdio_api_util(self, rdio, method, params):
        my_scraper_utils = ScraperUtils()
        call_result = my_scraper_utils.rdio_api_call(rdio, method, params)
        return call_result

class TrackListCreator(RdioAuthenticator):

    def __init__(self, result_list):
        self.result_list = result_list

    def check_artist_and_set_track_list(self, rdio_instance):
        valid_track_string = ''
        for result in self.result_list:
            # just using the positions for now....
            try:
                print(result.contents)
                artist_song_search_result = self._call_rdio_api_util(rdio_instance, 'search', {'query': "%s %s" % (list(result)[1].string,
                                                                                   list(result)[3].string),
                                                               'types': 'Artist, Song'})
                if artist_song_search_result['result']['track_count'] == 0 \
                    or artist_song_search_result['result']['track_count'] > 10:
                    pass
                else:
                    valid_track_string += ''.join(artist_song_search_result['result']['results'][0]['key'] + ',')
            except IndexError:
                pass

        return valid_track_string


class PlaylistPopulator(RdioAuthenticator):

    def __init__(self, playlist_name):
        self.playlist_name = playlist_name

    def get_playlist_keys(self, rdio_instance):
        playlist_key = None
        playlist_search_result = self._call_rdio_api_util(rdio_instance, 'getPlaylists', '')
        for i in range(len(playlist_search_result['result']['owned'])):
            if playlist_search_result['result']['owned'][i].get('name') == self.playlist_name:
                    playlist_key = playlist_search_result['result']['owned'][i].get('key')
        return playlist_key

    def create_or_update_playlist(self, rdio_instance, valid_track_string, playlist_key, playlist_description):
        if playlist_key:
            self._call_rdio_api_util(rdio_instance, 'deletePlaylist', {'playlist': playlist_key})
        self._call_rdio_api_util(rdio_instance, 'createPlaylist', {'name': self.playlist_name,
                                                                 'description': playlist_description,
                                                               'tracks': valid_track_string})
        return 'Playlist updated!'