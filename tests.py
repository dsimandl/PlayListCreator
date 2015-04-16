import unittest
import os
import json
from spotipy import Spotify
from unittest.mock import Mock, MagicMock, patch

from scraper import MusicScraper
from rdio_playlist_creator import TrackListCreator, PlaylistPopulator
from spotify_playlist_creator import SpotifyPlaylistCreator
from bs4 import BeautifulSoup

class TestWebScraper(unittest.TestCase):

    def setUp(self):
        self.altside_html = open(
           os.path.join(os.path.dirname(__file__), 'testdata/altsideexample.html')
        ).read()
        self.track_json = open(
           os.path.join(os.path.dirname(__file__), 'testdata/artist_song.json')
        ).read()
        self.playlists_json = open(
           os.path.join(os.path.dirname(__file__), 'testdata/simandl_playlists.json')
        ).read()
        self.spotify_playlist_results_no_TAS_playlist = open(
            os.path.join(os.path.dirname(__file__), 'testdata/spotify_query_results_no_playlist.json')
        ).read()
        self.spotify_playlist_results = open(
            os.path.join(os.path.dirname(__file__), 'testdata/spotify_playlist_query_results.json')
        ).read()
        self.spotify_playlist_create_result_json = open(
            os.path.join(os.path.dirname(__file__), 'testdata/spotify_playlist_create_results.json')
        ).read()
        self.spotify_track_list_results_json = open(
            os.path.join(os.path.dirname(__file__), 'testdata/spotify_artist_song_search_result.json')
        ).read()
        self.spotify_add_to_playlist_result_json = open(
            os.path.join(os.path.dirname(__file__), 'testdata/spotify_add_to_playlist_result.json')
        ).read()

        self.rdio_instance = Mock(return_value='')

    def _get_some_results_for_tests(self):
        html = BeautifulSoup('<p>1.       <strong>Built To Spill</strong><br/>“Car”</p>')
        results = html.find_all('p')
        return results

    def _get_spotify_playlist_creator_instance(self):
        results = self._get_some_results_for_tests()
        my_spotify_playlist_creator_for_test = SpotifyPlaylistCreator(results)
        return my_spotify_playlist_creator_for_test

    def test_get_page_items(self):
        soup_page = BeautifulSoup(self.altside_html)
        song_list = MusicScraper('example.com').get_page_items([('find', ('div', 'view-top-albums')),
                                                               ('find', ('div', 'field-content')), ('find_all', 'p')],
                                                     soup_page)

        self.assertIsInstance(song_list, list)

    @patch('rdio_playlist_creator.TrackListCreator._call_rdio_api_util')
    def test_check_artist_and_set_track_list(self, my_rdio_search):
        results = self._get_some_results_for_tests()
        my_track_string_test = TrackListCreator(results)
        my_rdio_search.return_value = json.loads(self.track_json)
        valid_track_list = my_track_string_test.check_artist_and_set_track_list(self.rdio_instance)
        self.assertIsInstance(valid_track_list, str)

    @patch('rdio_playlist_creator.PlaylistPopulator._call_rdio_api_util')
    def test_get_playlist_keys(self, my_rdio_search):
        my_playlist_populator_test = PlaylistPopulator('jenny')
        my_rdio_search.return_value = json.loads(self.playlists_json)
        playlist_key_test = my_playlist_populator_test.get_playlist_keys(self.rdio_instance)
        self.assertTrue(playlist_key_test)

    @patch('rdio_playlist_creator.PlaylistPopulator._call_rdio_api_util')
    def test_update_playlist(self, my_rdio_search):
        my_playlist_populator_test_update = PlaylistPopulator('jenny')
        my_rdio_search.return_value = 'Success!'
        result = my_playlist_populator_test_update.create_or_update_playlist(self.rdio_instance, ['t123456'],
                                                                             't998899', 'My playlist for testing')
        self.assertEqual(result, 'Playlist updated!')

    @patch('rdio_playlist_creator.PlaylistPopulator._call_rdio_api_util')
    def test_create_playlist(self, my_rdio_search):
        my_playlist_populator_test_create = PlaylistPopulator('TAS Top 20')
        my_playlist_populator_test_create.rdio = ''
        my_rdio_search.return_value = 'Success!'
        result = my_playlist_populator_test_create.create_or_update_playlist(self.rdio_instance, ['t123456'],
                                                                             None, 'My playlist for testing')
        self.assertEqual(result, 'Playlist updated!')

    @patch('spotify_playlist_creator.SpotifyPlaylistCreator._get_sp_instance')
    def test_spotify_playlist_creation(self, my_spotify_authenticator):
        my_spotify_instance = MagicMock()
        my_spotify_instance.user_playlists.return_value = json.loads(self.spotify_playlist_results_no_TAS_playlist)
        my_spotify_instance.user_playlist_create.return_value = json.loads(self.spotify_playlist_create_result_json)
        my_spotify_authenticator.return_value = my_spotify_instance
        my_spotify_playlist_creator_for_test = self._get_spotify_playlist_creator_instance()
        create_result = my_spotify_playlist_creator_for_test.check_playlist('julessurm')
        self.assertEqual(create_result, '5VUoTLGSRJSdMeakNP57fi')

    @patch('spotify_playlist_creator.SpotifyPlaylistCreator._get_sp_instance')
    def test_spotify_playlist_return_id(self, my_spotify_authenticator):
        my_spotify_instance = MagicMock()
        my_spotify_instance.user_playlists.return_value = json.loads(self.spotify_playlist_results)
        my_spotify_authenticator.return_value = my_spotify_instance
        my_spotify_playlist_creator_for_test = self._get_spotify_playlist_creator_instance()
        create_result = my_spotify_playlist_creator_for_test.check_playlist('julessurm')
        self.assertEqual(create_result, '5VUoTLGSRJSdMeakNP57fi')

    @patch('spotify_playlist_creator.SpotifyPlaylistCreator._get_sp_instance')
    def test_set_spotify_track_list(self, my_spotify_authenticator):
        my_spotify_instance = MagicMock()
        my_spotify_instance.search.return_value = json.loads(self.spotify_track_list_results_json)
        my_spotify_authenticator.return_value = my_spotify_instance
        my_spotify_playlist_creator_for_test = self._get_spotify_playlist_creator_instance()
        valid_track_list = my_spotify_playlist_creator_for_test.check_artist_and_set_track_list()
        self.assertIsInstance(valid_track_list, list)

    @patch('spotify_playlist_creator.SpotifyPlaylistCreator._get_sp_instance')
    def test_add_to_spotify_playlist(self, my_spotify_authenticator):
        my_spotify_instance = MagicMock()
        my_spotify_instance.user_playlist_add_tracks.return_value = json.loads(self.spotify_add_to_playlist_result_json)
        my_spotify_authenticator.return_value = my_spotify_instance
        my_spotify_playlist_creator_for_test = self._get_spotify_playlist_creator_instance()
        playlist_updated = my_spotify_playlist_creator_for_test.update_playlist('julessurm', '5VUoTLGSRJSdMeakNP57fi',
                                                                                ['1GNc7hEr1ktdYzYegVXOPK'] )
        self.assertEqual(list(playlist_updated.keys())[0], 'snapshot_id')





