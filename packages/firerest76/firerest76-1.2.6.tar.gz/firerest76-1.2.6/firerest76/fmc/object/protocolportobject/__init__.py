from firerest76.defaults import API_RELEASE_610
from firerest76.fmc import Resource, Connection
from firerest76.fmc.object.protocolportobject.override import Override


class ProtocolPortObject(Resource):
    PATH = '/object/protocolportobjects/{uuid}'
    MINIMUM_VERSION_REQUIRED_CREATE = API_RELEASE_610
    MINIMUM_VERSION_REQUIRED_GET = API_RELEASE_610
    MINIMUM_VERSION_REQUIRED_UPDATE = API_RELEASE_610
    MINIMUM_VERSION_REQUIRED_DELETE = API_RELEASE_610

    def __init__(self, conn: Connection):
        super().__init__(conn)
        self.override = Override(conn)
