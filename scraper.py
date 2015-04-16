from urllib import request
from bs4 import BeautifulSoup

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
                        id_, class_ = id_and_maybe_class
                        find_result = getattr(find_result, method)(str(
                            id_), class_=class_)
                    else:
                        find_result = getattr(find_result, method)(str(id_and_maybe_class))
                else:
                    if isinstance(id_and_maybe_class, tuple):
                        id_, class_ = id_and_maybe_class
                        find_result = getattr(soup_page, method)(
                            id_, class_=class_)
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