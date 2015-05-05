import re
from urllib import request
from bs4 import BeautifulSoup

class TASMusicScraper:

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

    def get_page_items(self, layout, soup_page):
        try:
            while layout:
                if not soup_page:
                    find_result = getattr(find_result, layout[0]['method'])(layout[0]['element'], attrs=layout[0]['identifier'])
                else:
                    find_result = getattr(soup_page, layout[0]['method'])(layout[0]['element'], attrs=layout[0]['identifier'])
                    soup_page = None
                del layout[0]
            return find_result
        except TypeError:
            print('Invalid format for method and vars list')
        except Exception:
            print('Something went wrong! %s' % str(Exception))

class SOMAFMMusicScraper(TASMusicScraper):

    def get_page_items(self, layout, soup_page):
        result = TASMusicScraper.get_page_items(self, layout, soup_page)
        song_page_part = result.string[result.string.find('Top 30 Tracks BY SPINS'):result.string.find('Top 30 Tracks BY LISTENERS')-3]
        song_page_part_list = song_page_part.splitlines()
        return [re.split(r'\s*(?:\d+\.|\s\-\s|\s\(\d+\))\s*', song_page_part_list[i]) for i in range(1, len(song_page_part_list))]
