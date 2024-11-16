# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property, cache
from typing import TYPE_CHECKING
from upnetfabinv.utils import get, get_all_items, get_all
from upnetfabinv.errors import UPONUDCFabInventoryMissingVariableError


if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class VlansMixin:
    @cached_property
    def vlans(self: SharedUtils) -> list:
        # Get devices by site ID and role ID
        vlans = self.netbox.ipam_vlan_filter()

        return vlans

    def vlan(self: SharedUtils, vlan_id: int):
        """
        vlan_id is the netbox is, not the vlan id
        """

        vlan = get_all_items(self.vlans, "id", vlan_id)
        if len(vlan) == 0:
            raise UPONUDCFabInventoryMissingVariableError(
                f"VLAN with netbox id {vlan_id} does not exisis"
            )

        return vlan[0]
