import requests

simple_endpoints = ['thepub', 'thepub/local', 'checkin/recent',
                    'beer/trending', 'user/pending',
                    'notifications', 'heartbeat']

simple_endpoints_with_requires = [('user/wishlist/add', 'bid'),
                                  ('user/wishlist/delete', 'bid'),
                                  ('search/beer', 'q'),
                                  ('search/brewery', 'q')]

single_param_endpoints = ['user/checkins', 'venue/checkins', 'beer/checkins',
                          'brewery/checkins', 'brewery/info', 'beer/info',
                          'venue/info', 'checkin/view', 'user/info',
                          'user/badges', 'user/friends', 'user/wishlist',
                          'user/beers', 'checkin/toast', 'friend/remove',
                          'friend/request']

post_endpoints = ['checkin/add', 'friend/accept', 'friend/reject']


class Untappd:

    access_token = None
    base_uri = 'http://api.untappd.com/v4'
    client_id = ''
    client_secret = ''

    def __init__(self, client_id, client_secret, baseuri=base_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_uri = baseuri

        for endpoint in simple_endpoints:
            fun = self.__make_simple_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)
        for endpoint in single_param_endpoints:
            fun = self.__make_singlearg_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)
        for endpoint in simple_endpoints_with_requires:
            fun = self.__make_simple_with_requires_fun(endpoint)
            setattr(self, endpoint[0].replace('/', '_'), fun)
        for endpoint in post_endpoints:
            fun = self.__make_post_endpoint_fun(endpoint)
            setattr(self, endpoint.replace('/', '_'), fun)

    def __make_simple_endpoint_fun(self, name):
        def _function(options={}):
            return self._get('/' + name, options)
        return _function

    def __make_singlearg_endpoint_fun(self, name):
        def _function(id, options={}):
            return self._get('/' + name + '/' + id, options)
        return _function

    def __make_simple_with_requires_fun(self, name_and_required):
        name, required_param = name_and_required

        def _function(required_attribute, options={}):
            options.update({required_param: required_attribute})
            return self._get('/' + name, options)
        return _function

    def __make_post_endpoint_fun(self, name):
        def _function(id, options={}):
            return self._post('/' + name + '/' + id, options)
        return _function

    def _get(self, request, options):
        options.update({'client_id': self.client_id,
                        'client_secret': self.client_secret})
        return requests.get(self.base_uri + request, params=options).json()

    def _post(self, request, options):
        options.update({'client_id': self.client_id,
                        'client_secret': self.client_secret})
        return requests.post(self.base_uri + request, params=options).json()

    def authenticate():
        pass
