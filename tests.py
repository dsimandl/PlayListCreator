from scraper import MusicScraper
import unittest
from http.client import HTTPResponse
from bs4 import BeautifulSoup


class TestWebScraper(unittest.TestCase):

    def setUp(self):
        self.MusicScraper = MusicScraper('http://thealternateside.org/')


    def test_url_is_correct_and_is_working(self):
        self.assertEqual(self.MusicScraper.url, "http://thealternateside.org/")

        soup_page = self.MusicScraper.open_get_and_close_page()
        self.assertIsInstance(self.MusicScraper.page, HTTPResponse)

        self.assertIsInstance(soup_page, BeautifulSoup)

        song_list = self.MusicScraper.soup_and_get_page_items([('find', ('div', 'view-top-albums')),
                                                               ('find', ('div', 'field-content')), ('find_all', 'p')], soup_page)

        self.assertIsInstance(song_list, list)


