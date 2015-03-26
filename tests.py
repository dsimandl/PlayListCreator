import unittest
import os
import json
from unittest.mock import Mock, patch

from scraper import MusicScraper
from rdio_playlist_creator import TrackListCreator, PlaylistPopulator
from bs4 import BeautifulSoup

class TestWebScraper(unittest.TestCase):

    def setUp(self):
        self.altside_html = open(
           os.path.join(os.path.dirname(__file__), 'altsideexample.html')
        ).read()
        self.track_json = open(
           os.path.join(os.path.dirname(__file__), 'artist_song.json')
        ).read()
        self.playlists_json = open(
           os.path.join(os.path.dirname(__file__), 'simandl_playlists.json')
        ).read()

        self.rdio_instance = Mock(return_value='')

    def test_get_page_items(self):
        soup_page = BeautifulSoup(self.altside_html)
        song_list = MusicScraper('example.com').get_page_items([('find', ('div', 'view-top-albums')),
                                                               ('find', ('div', 'field-content')), ('find_all', 'p')],
                                                     soup_page)

        self.assertIsInstance(song_list, list)

    @patch('rdio_playlist_creator.TrackListCreator._call_rdio_api_util')
    def test_check_artist_and_set_track_list(self, my_rdio_search):
        html = BeautifulSoup('<p>1.       <strong>Built To Spill</strong><br/>“Car”</p>')
        results = html.find_all('p')
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


