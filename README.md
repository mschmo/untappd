Untappd API Python Wrapper
=======

Python wrapper for the Untappd.com API.

# Version
* 1.0 Initial release

# API
* [Documentaion](https://untappd.com/api/docs)
* [Register](https://untappd.com/api/register) for a client ID and client secret

# TODO
* Test authentication with OAuth to allow authorized calls
* Exception handling
* Parsing meta returns

# Dependencies
* [Requests](http://docs.python-requests.org/en/latest/)

# Usage
    from untappd import Untappd
    untappd_client = Untappd('CLIENT_ID', 'CLIENT_SECRET'[, 'REDIRECT_URL'])

# Code Examples
### Get trending beers:
    untappd_client.beer_trending()
[Trending](https://untappd.com/api/docs#trending)
### Get single beer info:
    untappd_client.beer_info(123)
[Beer Info](https://untappd.com/api/docs#beer_info)
### Get user info:
    untappd_client.user_info('mattyschmo')
[User Info](https://untappd.com/api/docs#user_info)
### Search for beer:
    untappd_client.search_beer({'q': 'coors'})
[Search for Beer](https://untappd.com/api/docs#beer_search)