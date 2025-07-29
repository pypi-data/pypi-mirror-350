from firerest76.defaults import API_RELEASE_610
from firerest76.fmc import ChildResource


class Override(ChildResource):
    CONTAINER_NAME = 'VlanTag'
    CONTAINER_PATH = '/object/vlantags/{uuid}'
    PATH = '/object/vlantags/{container_uuid}/overrides/{uuid}'
    MINIMUM_VERSION_REQUIRED_GET = API_RELEASE_610
