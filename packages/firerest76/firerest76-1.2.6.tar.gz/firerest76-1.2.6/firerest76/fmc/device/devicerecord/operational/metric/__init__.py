from firerest76 import utils
from firerest76.defaults import API_RELEASE_660
from firerest76.fmc import ChildResource


class Metric(ChildResource):
    CONTAINER_NAME = 'DeviceRecord'
    CONTAINER_PATH = '/devices/devicerecords/{uuid}'
    PATH = '/devices/devicerecords/{container_uuid}/operational/metrics'
    SUPPORTED_FILTERS = ['metric']

    @utils.support_params
    @utils.resolve_by_name
    @utils.minimum_version_required(version=API_RELEASE_660)
    def get(self, metric: str, container_uuid=None, container_name=None, params=None):
        url = self.url(self.PATH.format(container_uuid=container_uuid))
        return self.conn.get(url=url, params=params)
