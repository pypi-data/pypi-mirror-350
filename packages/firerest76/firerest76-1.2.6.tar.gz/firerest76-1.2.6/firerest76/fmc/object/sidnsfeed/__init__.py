from firerest76.defaults import API_RELEASE_700
from firerest76.fmc import Resource


class SiDnsFeed(Resource):
    PATH = '/object/sidnsfeeds/{uuid}'
    MINIMUM_VERSION_REQUIRED_GET = API_RELEASE_700
