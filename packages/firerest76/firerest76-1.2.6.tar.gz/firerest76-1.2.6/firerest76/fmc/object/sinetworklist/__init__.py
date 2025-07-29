from firerest76.defaults import API_RELEASE_700
from firerest76.fmc import Resource


class SiNetworkList(Resource):
    PATH = '/object/sinetworklists/{uuid}'
    MINIMUM_VERSION_REQUIRED_GET = API_RELEASE_700
