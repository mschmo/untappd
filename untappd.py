import requests

get_endpoints = ['thepub', 'thepub/local', 'checkin/recent',
                 'beer/trending', 'user/pending', 'notifications', 
                 'heartbeat', 'user/checkins', 'venue/checkins', 
                 'beer/checkins', 'brewery/checkins', 'brewery/info', 
                 'beer/info', 'venue/info', 'checkin/view', 
                 'user/info', 'user/badges', 'user/friends', 
                 'user/wishlist', 'user/beers', 'checkin/toast', 
                 'friend/remove', 'friend/request']

endpoints_with_requires = [('user/wishlist/add', 'bid'),
                           ('user/wishlist/delete', 'bid'),
                           ('search/beer', 'q'),
                           ('search/brewery', 'q')]

post_endpoints = ['checkin/add', 'friend/accept', 'friend/reject']


class Untappd:

    access_token = None
    base_uri = 'http://api.untappd.com/v4/'
    authorize_uri = 'https://untappd.com/oauth/authenticate/'
    redirect_uri = ''
    client_id = ''
    client_secret = ''

    def __init__(self, client_id, client_secret, baseuri=base_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_uri = baseuri

        for endpoint in get_endpoints:
            fun = self.__make_get_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)
        for endpoint in endpoints_with_requires:
            fun = self.__make_endpoint_with_requires_fun(endpoint)
            setattr(self, endpoint[0].replace('/', '_'), fun)
        for endpoint in post_endpoints:
            fun = self.__make_post_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)

    def __make_get_endpoint_fun(self, name):
        def _function(id=None, options={}):
            request = '{}'.format(name)
            if id:
                request += '/{}'.format(id)
            return self._get(request, options)
        return _function

    def __make_endpoint_with_requires_fun(self, name_and_required):
        name, required_param = name_and_required

        def _function(required_attribute, options={}):
            options.update({required_param: required_attribute})
            return self._get(name, options)
        return _function

    def __make_post_endpoint_fun(self, name):
        def _function(id, options={}):
            request = '{}/{}'.format(name, id)
            return self._post(request, options)
        return _function

    def _get(self, request, options):
        options.update({'client_id': self.client_id,
                        'client_secret': self.client_secret})
        return requests.get(self.base_uri + request, params=options).json()

    def _post(self, request, options):
        options.update({'client_id': self.client_id,
                        'client_secret': self.client_secret})
        return requests.post(self.base_uri + request, params=options).json()

    def authenticate(self, redirect_uri=redirect_uri):
        pass
