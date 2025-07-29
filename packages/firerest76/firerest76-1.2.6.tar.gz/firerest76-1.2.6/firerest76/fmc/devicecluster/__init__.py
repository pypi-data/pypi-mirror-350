from firerest76.fmc import Connection
from firerest76.fmc.devicecluster.ftddevicecluster import FtdDeviceCluster


class DeviceCluster:
    def __init__(self, conn: Connection):
        self.ftddevicecluster = FtdDeviceCluster(conn)
