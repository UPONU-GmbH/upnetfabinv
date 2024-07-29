from ..inventoryfacts import InventoryFacts
from ..utils import get, get_all_items

from functools import cached_property


class Inventory(InventoryFacts):
    @cached_property
    def all(self) -> dict:
        inventory_tree = {
            "FABRIC": {"children": {}},
            "NETWORK_SERVICES": {"children": {}},
            "CONNECTED_ENDPOINTS": {"children": {}},
            "EOS_DEVICES": {"hosts": {}},
            "OS10_DEVICES": {"hosts": {}},
        }

        for az in self.shared_utils.config.get("fabric.availability_zones"):
            inventory_tree["FABRIC"]["children"][az] = {"children": self._get_fabric_az(az)}
            inventory_tree["NETWORK_SERVICES"]["children"][
                f"{az}_L3_LEAVES"
            ] = dict()
            inventory_tree["NETWORK_SERVICES"]["children"][
                f"{az}_L2_LEAVES"
            ] = dict()
            inventory_tree["CONNECTED_ENDPOINTS"]["children"][
                f"{az}_L3_LEAVES"
            ] = dict()
            inventory_tree["CONNECTED_ENDPOINTS"]["children"][
                f"{az}_L2_LEAVES"
            ] = dict()

        
        for device in get_all_items(self.shared_utils.devices, "custom_fields.avd_nos_family", "EOS"):
            inventory_tree["EOS_DEVICES"]["hosts"][
                get(device, "name")
            ] = dict()
        for device in get_all_items(self.shared_utils.devices, "custom_fields.avd_nos_family", "OS10"):
            inventory_tree["OS10_DEVICES"]["hosts"][
                get(device, "name")
            ] = dict()

        return {"children": inventory_tree}

    def _get_fabric_az(self, az: str) -> dict:
        children = {
            f"{az}_SPINES": {"hosts": self._get_spines(az)},
            f"{az}_L3_LEAVES": {"children": self._get_l3leaf_groups(az)},
            f"{az}_L2_LEAVES": {"hosts": self._get_l2leafs(az)},
        }

        return children

    def _get_spines(self, az: str) -> dict:

        az_spines = get_all_items(self.shared_utils.spines, "site.name", az)

        spines = {}

        for spine in az_spines:
            spines[get(spine, "name", required=True)] = dict()

        return spines

    def _get_l3leaf_groups(self, az: str) -> dict:

        az_leafs = get_all_items(self.shared_utils.l3leafs, "site.name", az)

        leafs = {
            f"{az}_L3_LEAVES_OS10": {
                "hosts": dict()
            },
            f"{az}_L3_LEAVES_EOS": {
                "hosts": dict()
            },
        }

        for leaf in get_all_items(az_leafs, "custom_fields.avd_node_type", "l3leaf_os10"):
            leafs[f"{az}_L3_LEAVES_OS10"]["hosts"][get(leaf, "name", required=True)] = dict()

        for leaf in get_all_items(az_leafs, "custom_fields.avd_node_type", "l3leaf"):
            leafs[f"{az}_L3_LEAVES_EOS"]["hosts"][get(leaf, "name", required=True)] = dict()

        return leafs

    def _get_l2leafs(self, az: str) -> dict:

        az_leafs = get_all_items(self.shared_utils.l2leafs, "site.name", az)

        leafs = {}

        for leaf in az_leafs:
            leafs[get(leaf, "name", required=True)] = dict()

        return leafs
