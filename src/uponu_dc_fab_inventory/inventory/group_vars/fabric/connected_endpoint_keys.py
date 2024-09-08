# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from uponu_dc_fab_inventory.inventoryfacts import InventoryFacts


from functools import cached_property

from uponu_dc_fab_inventory.shared_utils.shared_utils import SharedUtils

DEFAULT_CONNECTED_ENDPOINTS = [
    {
        "key": "servers",
        "type": "server",
        "description": "Server"
    },
    {
        "key": "firewalls",
        "type": "firewall",
        "description": "Firewall"
    },
    {
        "key": "routers",
        "type": "router",
        "description": "Router"
    },
    {
        "key": "load_balancers",
        "type": "load_balancer",
        "description": "Load Balancer"
    },
    {
        "key": "storage_arrays",
        "type": "storage_array",
        "description": "Storage Array"
    },
    {
        "key": "cpes",
        "type": "cpe",
        "description": "CPE"
    },
    {
        "key": "workstations",
        "type": "workstation",
        "description": "Workstation"
    },
    {
        "key": "access_points",
        "type": "access_point",
        "description": "Access Point"
    },
    {
        "key": "phones",
        "type": "phone",
        "description": "Phone"
    },
    {
        "key": "printers",
        "type": "printer",
        "description": "Printer"
    },
    {
        "key": "cameras",
        "type": "camera",
        "description": "Camera"
    },
    {
        "key": "generic_devices",
        "type": "generic_device",
        "description": "Generic Device"
    }
]

UPNETFABINV_CONNECTED_ENDPOINTS = [
    {
        "key": "switches_oob",
        "type": "switch_oob",
        "description": "OOB switch interface"
    }
]


class ConnectedEndpointKeys(InventoryFacts):
    def __init__(self, shared_utils: SharedUtils) -> None:
        super().__init__(shared_utils)

    @cached_property
    def _filename(self):
        return "CONNECTED_ENDPOINT_KEYS.yml"
    
    @cached_property
    def _dirname(self):
        return "FABRIC"
    
    @cached_property
    def connected_endpoints_keys(self):

        return DEFAULT_CONNECTED_ENDPOINTS + UPNETFABINV_CONNECTED_ENDPOINTS


