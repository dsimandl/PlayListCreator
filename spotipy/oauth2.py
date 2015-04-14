from __future__ import print_function

import base64
import json
import time
import sys

import requests

try:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
    from urllib.parse import parse_qsl
except ImportError:
    from urllib2 import urlopen, Request
    from urllib import urlencode
    from urlparse import parse_qsl

class SpotifyOauthError(Exception):
    pass

class SpotifyOAuth(object):
    '''
    Implements Authorization Code Flow for Spotify's OAuth implementation.
    '''

    OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, redirect_uri,
            state=None, scope=None, cache_path=None,
            show_dialog=None):
        '''
            Creates a SpotifyOAuth object

            Parameters:
                 - client_id - the client id of your app
                 - client_secret - the client secret of your app
                 - redirect_uri - the redirect URI of your app
                 - state - security state
                 - scope - the desired scope of the request
                 - cache_path - path to location to save tokens
        '''

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state=state
        self.cache_path = cache_path
        self.scope=self._normalize_scope(scope)
        self.show_dialog = show_dialog

    def get_cached_token(self):
        ''' Gets a cached auth token
        '''
        token_info = None
        if self.cache_path:
            try:
                f = open(self.cache_path)
                token_info_string = f.read()
                f.close()
                token_info = json.loads(token_info_string)

                # if scopes don't match, then bail
                if 'scope' not in token_info or self.scope != token_info['scope']:
                    return None

                if self._is_token_expired(token_info):
                    token_info = self._refresh_access_token(token_info['refresh_token'])

            except IOError:
                pass
        return token_info

    def _save_token_info(self, token_info):
        if self.cache_path:
            try:
                f = open(self.cache_path, 'w')
                f.write(json.dumps(token_info))
                f.close()
            except IOError:
                self._warn("couldn't write token cache to " + self.cache_path)
                pass


    def _is_token_expired(self, token_info):
        now = int(time.time())
        return token_info['expires_at'] < now

    def get_authorize_url(self, state=None):
        """ Gets the URL to use to authorize this app
        """
        payload = {'client_id': self.client_id,
                   'response_type': 'code',
                   'redirect_uri': self.redirect_uri}
        if self.scope is not None:
            payload['scope'] = self.scope
        if state is None:
            state = self.state
        if state is not None:
            payload['state'] = state
        if self.show_dialog is not None:
            payload['show_dialog'] = str(self.show_dialog).lower()

        urlparams = urlencode(payload)

        return "%s?%s" % (self.OAUTH_AUTHORIZE_URL, urlparams)

    def parse_response_code(self, url):
        """ Parse the response code in the given response url

            Parameters:
                - url - the response url
        """

        try:
            return url.split("?code=")[1].split("&")[0]
        except IndexError:
            return None

    def get_access_token(self, code):
        """ Gets the access token for the app given the code

            Parameters:
                - code - the response code
        """

        payload = {
            'redirect_uri': self.redirect_uri,
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        response = requests.post(self.OAUTH_TOKEN_URL, data=payload, verify=True)
        if response.status_code is not 200:
            raise SpotifyOauthError(response.reason + '\n' + response.text)
        token_info = response.json()
        token_info = self._add_custom_values_to_token_info(token_info)
        self._save_token_info(token_info)
        return token_info

    def _normalize_scope(self, scope):
        if scope:
            scopes = scope.split()
            scopes.sort()
            return ' '.join(scopes)
        else:
            return None

    def _refresh_access_token(self, refresh_token):
        payload = { 'refresh_token': refresh_token,
                   'grant_type': 'refresh_token'}

        auth_header = self.client_id + ':' + self.client_secret
        headers = {'Authorization': 'Basic %s' % auth_header}

        response = requests.post(self.OAUTH_TOKEN_URL, data=payload,
            headers=headers)
        if response.status_code != 200:
            if False:  # debugging code
                print('headers', headers)
                print('request', response.url)
            self._warn("couldn't refresh token: code:%d reason:%s" \
                % (response.status_code, response.reason))
            return None
        token_info = response.json()
        token_info = self._add_custom_values_to_token_info(token_info)
        if not 'refresh_token' in token_info:
            token_info['refresh_token'] = refresh_token
        self._save_token_info(token_info)
        return token_info

    def _add_custom_values_to_token_info(self, token_info):
        '''
        Store some values that aren't directly provided by a Web API
        response.
        '''
        token_info['expires_at'] = int(time.time()) + token_info['expires_in']
        token_info['scope'] = self.scope
        return token_info

    def _warn(self, msg):
        print('warning:' + msg, file=sys.stderr)
