import requests

DEFAULT_BASE_URI = 'http://api.untappd.com/v4'
BASE_URI = ''
CLIENT_ID = ''
CLIENT_SECRET = ''

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

POSTS = ['checkin/add', 'friend/accept', 'friend/reject']

class Untappd:

    ACCESS_TOKEN = None

    @staticmethod
    def __make_simple_endpoint_fun(name):
        @staticmethod
        def _function(options={}):
            return Untappd._get('/' + name, options)
        return _function

    @staticmethod
    def __make_singlearg_endpoint_fun(name):
        @staticmethod
        def _function(id, options={}):
            return Untappd._get('/' + name + '/' + id, options)
        return _function

    @staticmethod
    def __make_simple_with_requires_fun(name_and_required):
        name, required_param = name_and_required
        @staticmethod
        def _function(required_attribute, options={}):
            options.update({required_param: required_attribute})
            return Untappd._get('/' + name, options)
        return _function

    @staticmethod
    def _get(request, options):
        options.update({'client_id': Untappd.CLIENT_ID,
                        'client_secret': Untappd.CLIENT_SECRET})
        return requests.get(Untappd.BASE_URI + request, params=options).json()

    @staticmethod
    def configure(client_id, client_secret, baseuri=DEFAULT_BASE_URI):
        Untappd.CLIENT_ID = client_id
        Untappd.CLIENT_SECRET = client_secret
        Untappd.BASE_URI = baseuri
        for endpoint in simple_endpoints:
            fun = Untappd.__make_simple_endpoint_fun(endpoint)
            setattr(Untappd, endpoint.replace('/', '_'), fun)
        for endpoint in single_param_endpoints:
            fun = Untappd.__make_singlearg_endpoint_fun(endpoint)
            setattr(Untappd, endpoint.replace('/', '_'), fun)
        for endpoint in simple_endpoints_with_requires:
            fun = Untappd.__make_simple_with_requires_fun(endpoint)
            setattr(Untappd, endpoint[0].replace('/', '_'), fun)

    @classmethod
    def authenticate():
        pass