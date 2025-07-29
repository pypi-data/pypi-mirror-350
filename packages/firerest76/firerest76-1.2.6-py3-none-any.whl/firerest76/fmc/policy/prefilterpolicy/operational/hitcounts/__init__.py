from firerest76 import utils
from firerest76.defaults import API_RELEASE_640
from firerest76.fmc import ChildResource


class Hitcount(ChildResource):
    CONTAINER_NAME = 'PrefilterPolicy'
    CONTAINER_PATH = '/policy/prefilterpolicies/{uuid}'
    PATH = '/policy/prefilterpolicies/{container_uuid}/operational/hitcounts/{uuid}'
    MINIMUM_VERSION_REQUIRED_GET = API_RELEASE_640
    MINIMUM_VERSION_REQUIRED_UPDATE = API_RELEASE_640
    MINIMUM_VERSION_REQUIRED_DELETE = API_RELEASE_640

    @utils.support_params
    def update(self):
        return

    @utils.support_params
    def get(self):
        return

    @utils.support_params
    def delete(self):
        return
