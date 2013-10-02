import requests

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
    base_uri = 'http://api.untappd.com/v4/'
    authorize_uri = 'https://untappd.com/oauth/authenticate/'
    client_id = ''
    client_secret = ''

    def __init__(self, client_id, client_secret, baseuri=base_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_uri = baseuri

        for endpoint in get_endpoints:
            fun = self.__make_get_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)
        for endpoint in post_endpoints:
            fun = self.__make_post_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)

    def __make_get_endpoint_fun(self, name):
        def _function(id=None, options={}):
            request = '{}'.format(name)
            if id:
                request += '/{}'.format(id)
            return self.get(request, options)
        return _function

    def __make_post_endpoint_fun(self, name):
        def _function(id, options={}):
            request = '{}/{}'.format(name, id)
            return self.post(request, options)
        return _function

    def get(self, request, options):
        options.update({'client_id': self.client_id,
                        'client_secret': self.client_secret})
        return requests.get(self.base_uri + request, params=options).json()

    def post(self, request, options):
        options.update({'client_id': self.client_id,
                        'client_secret': self.client_secret})
        return requests.post(self.base_uri + request, params=options).json()

    def authenticate(self, redirect_url):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_url': redirect_url
        }
        return requests.get(self.authorize_uri, params=params)