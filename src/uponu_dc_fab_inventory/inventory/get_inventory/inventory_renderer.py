# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from pprint import pprint

import os
import yaml


from uponu_dc_fab_inventory.inventoryfacts import InventoryFacts
from uponu_dc_fab_inventory.shared_utils import SharedUtils
from uponu_dc_fab_inventory.utils import merge, get

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from uponu_dc_fab_inventory.resources import Config



from ..inventory import Inventory
from ..host_vars import AnsibleFacts

FAB_INVENTORY_CLASSES = [
    Inventory
]

FAB_INVENTORY_HOST_VARS_CLASSES = [
    AnsibleFacts
]

class InventoryRenderer():

    def __init__(self, config: Config):
        
        self.shared_utils = SharedUtils(config)
    
    def get_inventory(self, out_path = "examples/", override_path = "examples/override"):

        result = {}
        
        override = {}
        override_inventory_path = os.path.join(override_path, "inventory.yml")
        if os.path.exists(override_inventory_path):
            with open(override_inventory_path, "r") as fd:
                override = yaml.safe_load(fd)

        for cls in FAB_INVENTORY_CLASSES:

            fab_inventory_module: InventoryFacts = cls(self.shared_utils)

            result = fab_inventory_module.render()

        merge(result, override)

        with open(os.path.join(out_path, "inventory.yml"), "w") as fd:
                yaml.dump(result, fd)

    def get_host_vars(self, out_path = "examples/"):

        host_vars_paths = os.path.join(out_path, "host_vars")
        try:
            os.mkdir(os.path.join(out_path, "host_vars"))
        except FileExistsError:
            pass

        for device in self.shared_utils.devices:
            result = {}
            for cls in FAB_INVENTORY_HOST_VARS_CLASSES:

                fab_inventory_module: InventoryFacts = cls(self.shared_utils, device)

                merge(result, fab_inventory_module.render())

            hostname = get(device, "name", required=True)

            with open(os.path.join(host_vars_paths, f"{hostname}.yml"), "w") as fd:
                yaml.dump(result, fd)



