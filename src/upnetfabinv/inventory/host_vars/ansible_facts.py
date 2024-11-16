from upnetfabinv.inventoryfacts import InventoryFacts

from functools import cached_property

from upnetfabinv.shared_utils.shared_utils import SharedUtils
from upnetfabinv.utils import get


class AnsibleFacts(InventoryFacts):
    def __init__(self, shared_utils: SharedUtils, device: dict) -> None:
        super().__init__(shared_utils)

        self.device = device

    @cached_property
    def ansible_host(self):
        return get(self.device, "oob_ip.address")
