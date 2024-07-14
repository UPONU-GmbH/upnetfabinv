# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property, cache
from typing import TYPE_CHECKING
from uponu_dc_fab_inventory.utils import get, get_all_items, get_all


if TYPE_CHECKING:
    from .shared_utils import SharedUtils

class DevicesMixin():
    
    @cached_property
    def devices(self: SharedUtils) -> list:

        # Get devices by site ID and role ID
        devices = self.netbox.dcim_devices_filter()

        for device in devices:
            device["interfaces"] = self._device_interfaces_and_ip(device)

        return devices
    
    @cache
    def device(self: SharedUtils, device_id: int):

        device = self.netbox.dcim_devices_get(device_id)

        return device
    

    def _device_interfaces_and_ip(self: SharedUtils, device: dict) -> list[dict]:
        
        interfaces = self.netbox.dcim_interfaces_filter(device_id=get(device, "id", required=True))
        ip_addresses = self.netbox.ipam_ip_addresses_filter(device_id=get(device, "id", required=True))


        res = []

        for interface in interfaces:

            res.append({
                "name": get(interface, "name", required=True),
                "ips": get_all(
                    get_all_items(ip_addresses, "assigned_object_id", get(interface, "id", required=True)),
                    "address"),
                "link_peers": get(interface, "link_peers", default=[])
            })

        return res
