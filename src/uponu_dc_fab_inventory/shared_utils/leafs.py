# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from uponu_dc_fab_inventory.utils import get_all_items

from functools import cached_property
from typing import TYPE_CHECKING

from pprint import pprint

if TYPE_CHECKING:
    from .shared_utils import SharedUtils

class LeafsMixin():

    @cached_property
    def l3leafs(self: SharedUtils) -> list:

        avd_switch_group = ["l3leaf", "l3leaf_os10"]


        devices = get_all_items(self.devices, "custom_fields.avd_switch_group", avd_switch_group)

        return devices
    
    @cached_property
    def l2leafs(self: SharedUtils) -> list:

        avd_switch_group = ["l2leaf"]

        devices = get_all_items(self.devices, "custom_fields.avd_switch_group", avd_switch_group)


        return devices
    