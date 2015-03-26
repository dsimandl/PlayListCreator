from urllib import request
from bs4 import BeautifulSoup
from scraper_utils import ScraperUtils

class MusicScraper:

    def __init__(self, url):
        self.url = url

    def _open_page(self):
        self.page = request.urlopen(self.url)

    def _close_page(self):
        self.page.close()
    
    def get_soup_page(self):
        self._open_page()
        my_page = BeautifulSoup(self.page)
        self._close_page()
        return my_page

    def get_page_items(self, soup_method_and_vars_list, soup_page):
        try:
            for method, id_and_maybe_class in soup_method_and_vars_list:
                if not soup_page:
                    if isinstance(id_and_maybe_class, tuple):
                        find_result = getattr(find_result, method)(str(
                            id_and_maybe_class[0]), class_=id_and_maybe_class[1])
                    else:
                        find_result = getattr(find_result, method)(str(id_and_maybe_class))
                else:
                    if isinstance(id_and_maybe_class, tuple):
                        find_result = getattr(soup_page, method)(
                            id_and_maybe_class[0], class_=id_and_maybe_class[1])
                    else:
                        find_result = getattr(soup_page, method)(str(id_and_maybe_class))
                    soup_page = None
            # debugging....
            for result in find_result:
                for item in result:
                    print(item.string)
            return find_result
        except TypeError:
            print('Invalid format for method and vars list')
        except Exception:
            print('Something went wrong! %s' % str(Exception))

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
            self._call_rdio_api_util(rdio_instance, 'addToPlaylist', {'playlist': playlist_key, 'tracks': valid_track_string})
            return 'Playlist updated'
        else:
            self._call_rdio_api_util(rdio_instance, 'createPlaylist', {'name': self.playlist_name,
                                                                 'description': playlist_description,
                                                               'tracks': valid_track_string})
            return 'Playlist created'