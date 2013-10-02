import requests
from urllib import urlencode

get_endpoints = ['thepub', 'thepub/local', 'checkin/recent',
                 'beer/trending', 'user/pending', 'notifications',
                 'heartbeat', 'user/checkins', 'venue/checkins',
                 'beer/checkins', 'brewery/checkins', 'brewery/info',
                 'beer/info', 'venue/info', 'checkin/view',
                 'user/info', 'user/badges', 'user/friends',
                 'user/wishlist', 'user/beers', 'checkin/toast',
                 'friend/remove', 'friend/request', 'user/wishlist/add',
                 'user/wishlist/delete', 'search/beer', 'search/brewery']

post_endpoints = ['checkin/add', 'friend/accept', 'friend/reject']


class Untappd:
    client_id = ''
    client_secret = ''
    base_url = 'http://api.untappd.com/v4/'
    authorize_url = 'https://untappd.com/oauth/authenticate/'
    token_url = 'https://untappd.com/oauth/authorize/'
    access_token = None
    redirect_url = None

    def __init__(self, client_id, client_secret, redirect_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url

        for endpoint in get_endpoints:
            fun = self.__make_get_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)
        for endpoint in post_endpoints:
            fun = self.__make_post_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)

    def __make_get_endpoint_fun(self, name):
        def _function(id=None, options={}):
            request = '{}'.format(name)
            if type(id) == dict and not options:
                options, id = id, options
            if id:
                request += '/{}'.format(id)
            return self.get(request, options)
        return _function

    def __make_post_endpoint_fun(self, name):
        def _function(id, options={}):
            request = '{}/{}'.format(name, id)
            return self.post(request, options)
        return _function

    def _get_token(self, code):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_url': self.redirect_url,
            'code': code
        }
        resp = requests.post(self.token_url, data=data).json()
        return resp['response']['access_token']

    def get(self, request, options):
        options.update({'client_id': self.client_id,
                        'client_secret': self.client_secret})
        return requests.get(self.base_url + request, params=options).json()

    def post(self, request, options):
        options.update({'client_id': self.client_id,
                        'client_secret': self.client_secret})
        return requests.post(self.base_url + request, params=options).json()

    def auth_url(self, redirect_url=None):
        if redirect_url:
            self.redirect_url = redirect_url
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_url': self.redirect_url
        }
        return '{}?{}'.format(self.authorize_url, urlencode(params))

    def set_token(self, code):
        access_token = self._get_token(code)
        self.access_token = access_token

