# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import re
import sys

from functools import cached_property
from upnetfabinv.utils import get, get_item, get_all, merge, get_all_items
from upnetfabinv.errors import UpnetfabinvError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .connected_endpoints import ConnectedEndpoints


class SwitchesOOBMixin:

    @cached_property
    def switches_oob(self: ConnectedEndpoints) -> list[dict]:
        switches_oob = []

        for switch in self.shared_utils.switches:
            switches_oob.append(self._get_switch_oob(switch))

        return switches_oob

    def _get_switch_oob(self: ConnectedEndpoints, switch: dict) -> list[dict]:
        res = {
            "name": get(switch, "name", required=True),
            "adapters": self._get_swicth_oob_adapters_interfces(switch),
        }

        return res

    def _get_swicth_oob_adapters_interfces(
        self: ConnectedEndpoints, switch: dict
    ) -> list[dict]:
        res = []

        switch_interfaces = get(switch, "interfaces")

        oob_interfaces = get_all_items(switch_interfaces, "interface.mgmt_only", True)

        for interface in oob_interfaces:

            if len(get(interface, "interface.connected_endpoints", [])) == 0:
                continue
            
            connected_endpoint = get(interface, "interface.connected_endpoints")[0]
            link_peer = get(interface, "interface.link_peers")[0]
            peer_switch = get_item(
                self.shared_utils.devices, "id", get(connected_endpoint, "device.id")
            )
            peer_interface = self.shared_utils.get_peer_interface(peer_switch, connected_endpoint, link_peer)

            try:
                vlan_settings = self._get_swtich_oob_adapters_interfces_vlan(peer_interface)
            except Exception as e:
                print(f"device {get(peer_switch, "name")}")
                print(e)
                sys.exit(1)

            res.append(
                merge({
                    "endpoint_ports": [get(interface, "name")],
                    "switch_ports": [get(connected_endpoint, "name")],
                    "switches": [get(connected_endpoint, "device.name")],
                    "spanning_tree_portfast": "edge",
                }, vlan_settings)
            )

        return res

    def _get_swtich_oob_adapters_interfces_vlan(
        self: ConnectedEndpoints, interface: dict
    ) -> dict:
        vlan_settings = {}

        MODE_MAP_NETBOX_AVD = {
            "tagged": "trunk",
            "access": "access",
        }

        mode = get(
            MODE_MAP_NETBOX_AVD, get(interface, "interface.mode.value"), default=None
        )

        if mode is None:
            raise UpnetfabinvError(
                f"Interface mode not allowed, Netbox mode is '{get(interface, "interface.mode.value")}' interface '{get(interface, "name")}'"
            )

        vlan_settings = {
            "mode": mode,
        }

        if mode == "trunk":
            vlan_settings["native_vlan"] = get(interface, "interface.untagged_vlan.vid")
            vlan_settings["vlans"] = ",".join(
                map(
                    str,
                    sorted(
                        get_all(get(interface, "interface.tagged_vlans"), "vid")
                        + [get(interface, "interface.untagged_vlan.vid")]
                    ),
                )
            )

        if mode == "access":
            vlan_settings["vlans"] = get(interface, "interface.untagged_vlan.vid")

        return vlan_settings
