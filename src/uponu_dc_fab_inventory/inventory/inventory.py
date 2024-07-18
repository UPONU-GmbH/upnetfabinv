from ..inventoryfacts import InventoryFacts
from ..utils import get

from functools import cached_property


class Inventory(InventoryFacts):
    @cached_property
    def all(self) -> dict:
        inventory_tree = {
            "FABRIC": {"children": {}},
            "NETWORK_SERVICES": {},
            "CONNECTED_ENDPOINTS": {},
            "EOS_DEVICES": {},
            "OS10_DEVICES": {},
        }

        # for fab in self.shared_utils.fabs:
        fab = "DC01"
        inventory_tree["FABRIC"]["children"][fab] = {"children": self._get_fabric(fab)}

        inventory_tree["NETWORK_SERVICES"] = {"children": dict()}

        for leaf in self.shared_utils.l3leafs:
            inventory_tree["NETWORK_SERVICES"]["children"][
                get(leaf, "name", required=True)
            ] = dict()

        return {"children": inventory_tree}

    def _get_fabric(self, fab: str) -> dict:
        children = {
            f"{fab}_SPINES": {"hosts": self._get_spines(fab)},
            f"{fab}_L3_LEAVES": {"hosts": self._get_l3leafs(fab)},
            f"{fab}_L2_LEAVES": {"hosts": self._get_l2leafs(fab)},
        }

        return children

    def _get_spines(self, fab: str) -> dict:
        spines = {}

        for spine in self.shared_utils.spines:
            spines[get(spine, "name", required=True)] = dict()

        return spines

    def _get_l3leafs(self, fab: str) -> dict:
        leafs = {}

        for leaf in self.shared_utils.l3leafs:
            leafs[get(leaf, "name", required=True)] = dict()

        return leafs

    def _get_l2leafs(self, fab: str) -> dict:
        leafs = {}

        for leaf in self.shared_utils.l2leafs:
            leafs[get(leaf, "name", required=True)] = dict()

        return leafs
