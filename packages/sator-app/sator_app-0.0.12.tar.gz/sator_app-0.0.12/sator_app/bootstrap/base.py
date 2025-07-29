from typing import List

from sator_core.ports.driven.gateways.oss import OSSGatewayPort
from sator_core.ports.driven.persistence.storage import StoragePersistencePort


class BaseBuilder:
    def __init__(self, oss_gateways: List[OSSGatewayPort], storage_port: StoragePersistencePort):
        self.storage_port = storage_port
        # TODO: temporary solution, should be moved somewhere else
        self.oss_gateways = oss_gateways
