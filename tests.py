import scraper
import unittest
from http.client import HTTPResponse
from bs4 import BeautifulSoup


class TestWebScraper(unittest.TestCase):

    def test_url_is_correct_and_is_working(self):
        self.assertEqual(scraper.url, "http://thealternateside.org/")
        self.assertIsInstance(scraper.page, HTTPResponse)
        self.assertIsInstance(scraper.soup_altside, BeautifulSoup)
        self.assertIn('<div class="field-content">', str(scraper.top_albums_view))
        self.assertIn('<p>', str(scraper.top_songs))
        self.assertNotEqual(scraper.top_song_list, [])

