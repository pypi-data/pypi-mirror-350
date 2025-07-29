from firerest76.defaults import API_RELEASE_700
from firerest76.fmc import Connection, Resource
from firerest76.fmc.policy.dnspolicy.allowdnsrule import AllowDnsRule
from firerest76.fmc.policy.dnspolicy.blockdnsrule import BlockDnsRule


class DnsPolicy(Resource):
    PATH = '/policy/dnspolicies/{uuid}'
    MINIMUM_VERSION_REQUIRED_GET = API_RELEASE_700

    def __init__(self, conn: Connection):
        super().__init__(conn)

        self.allowdnsrule = AllowDnsRule(conn)
        self.blockdnsrule = BlockDnsRule(conn)
