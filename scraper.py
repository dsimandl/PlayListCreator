from urllib import request
from bs4 import BeautifulSoup

class MusicScraper:

    def __init__(self, url):
        self.url = url
        self.page = ''

    def open_get_and_close_page(self):
        self.page = request.urlopen(self.url)
        soup_page = BeautifulSoup(self.page)
        self.page.close()
        return soup_page

    def soup_and_get_page_items(self, soup_method_and_vars_list, soup_page):
        try:
            while soup_method_and_vars_list:
                if not soup_page:
                    if isinstance(soup_method_and_vars_list[0][1], tuple):
                        find_result = getattr(find_result, soup_method_and_vars_list[0][0])(str(
                            soup_method_and_vars_list[0][1][0]), class_=soup_method_and_vars_list[0][1][1])
                    else:
                        find_result = getattr(find_result, soup_method_and_vars_list[0][0])(str(soup_method_and_vars_list[0][1]))
                    soup_method_and_vars_list = soup_method_and_vars_list[1:]
                else:
                    if isinstance(soup_method_and_vars_list[0][1], tuple):
                        find_result = getattr(soup_page, soup_method_and_vars_list[0][0])(
                            soup_method_and_vars_list[0][1][0], class_=soup_method_and_vars_list[0][1][1])
                    else:
                        find_result = getattr(soup_page, soup_method_and_vars_list[0][0])(str(soup_method_and_vars_list[0][1]))
                    soup_page = None
                    soup_method_and_vars_list = soup_method_and_vars_list[1:]
            print(find_result)
            return find_result
        except TypeError:
            print('Invalid format for method and vars list')
        except Exception:
            print('Something went wrong! %s' % Exception)
