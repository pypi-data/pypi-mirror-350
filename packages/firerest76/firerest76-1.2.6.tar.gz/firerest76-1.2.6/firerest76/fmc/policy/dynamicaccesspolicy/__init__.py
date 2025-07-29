from firerest76.defaults import API_RELEASE_700
from firerest76.fmc import Resource


class DynamicAccessPolicy(Resource):
    PATH = '/policy/dynamicaccesspolicies/{uuid}'
    MINIMUM_VERSION_REQUIRED_CREATE = API_RELEASE_700
    MINIMUM_VERSION_REQUIRED_GET = API_RELEASE_700
    MINIMUM_VERSION_REQUIRED_UPDATE = API_RELEASE_700
    MINIMUM_VERSION_REQUIRED_DELETE = API_RELEASE_700
