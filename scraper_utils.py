from urllib.error import HTTPError
from rdio import Rdio
from rdio_api_config import RDIO_CREDENTIALS


class ScraperUtils:

    def autheniticate_me(self):
        rdio = Rdio(RDIO_CREDENTIALS)
        try:
            url = rdio.begin_authentication('oob')
            print('Go to: ' + url)
            verifier = input('Then enter code: ').strip()
            rdio.complete_authentication(verifier)
            return rdio

        except HTTPError as e:
            print(e.read())


    def rdio_api_call(self, myrdio, method, params):
        call_result = myrdio.call(method, params)
        return call_result

