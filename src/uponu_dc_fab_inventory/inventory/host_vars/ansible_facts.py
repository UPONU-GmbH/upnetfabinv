from uponu_dc_fab_inventory.inventoryfacts import InventoryFacts

from functools import cached_property

from uponu_dc_fab_inventory.shared_utils.shared_utils import SharedUtils
from uponu_dc_fab_inventory.utils import get


class AnsibleFacts(InventoryFacts):
    def __init__(self, shared_utils: SharedUtils, device: dict) -> None:
        super().__init__(shared_utils)

        self.device = device

    @cached_property
    def ansible_host(self):
        return get(self.device, "oob_ip.address")
