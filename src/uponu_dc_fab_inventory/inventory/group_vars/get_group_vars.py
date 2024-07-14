# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations


import os
import yaml

from .availability_zone import AvailabilityZone
from .availability_zone.spines import Spines
from .availability_zone.l2_leaves import L2Leaves
from .availability_zone.l3_leaves import L3LeavesEOS, L3LeavesOS10

from uponu_dc_fab_inventory.utils import merge

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from uponu_dc_fab_inventory.shared_utils import SharedUtils
    from uponu_dc_fab_inventory.inventoryfacts import InventoryFacts

FAB_INVENTORY_GROUP_VARS_CLASSES = [
    
]

FAB_INVENTORY_GROUP_VARS_CLASSES_AVAILABILITY_ZONE = [
    AvailabilityZone,
    Spines,
    L2Leaves,
    L3LeavesEOS,
    L3LeavesOS10
]

def get_group_vars(shared_utils: SharedUtils, out_path: str, override_path: str) -> None:
    """
    Renders the group vars

    Parameters
    ----------
    shared_utils : SharedUtils
    out_path : str
        The output path. Has to be a directory
    override_path : str
        The path with the overrides. Has to be a directory
    """


    group_vars_paths = os.path.join(out_path, "group_vars")
    try:
        os.mkdir(group_vars_paths)
    except FileExistsError:
        pass

    for az in shared_utils.config.get("fabric.availability_zones"):
        for cls in FAB_INVENTORY_GROUP_VARS_CLASSES_AVAILABILITY_ZONE:

            group_vars_module_module: InventoryFacts = cls(shared_utils, az)

            result = group_vars_module_module.render()

            override = {}
            override_inventory_path = os.path.join(override_path, group_vars_module_module._filename)
            if os.path.exists(override_inventory_path):
                with open(override_inventory_path, "r") as fd:
                    override = yaml.safe_load(fd) 

                merge(result, override)

            with open(os.path.join(group_vars_paths, group_vars_module_module._filename), "w") as fd:
                yaml.dump(result, fd)
