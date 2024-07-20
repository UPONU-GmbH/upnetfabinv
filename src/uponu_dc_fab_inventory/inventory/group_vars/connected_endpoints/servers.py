# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations


from functools import cached_property
from uponu_dc_fab_inventory.utils import get, get_all_items, get_item, get_all, merge
from uponu_dc_fab_inventory.errors import UPONUDCFabInventoryError

from pprint import pprint

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .connected_endpoints import ConnectedEndpoints


class ServersMixin:
    @cached_property
    def servers(self: ConnectedEndpoints) -> list[dict]:
        servers = []

        for server in self.shared_utils.servers:
            servers.append(self._get_server(server))

        return servers

    def _get_server(self: ConnectedEndpoints, server: dict) -> list[dict]:
        res = {
            "name": get(server, "name", required=True),
            "adapters": self._get_server_adapters(server),
        }

        return res

    def _get_server_adapters(self: ConnectedEndpoints, server: dict) -> list[dict]:
        res = []

        res += self._get_server_adapters_portchannels(server)
        res += self._get_server_adapters_interfces(server)

        return res

    def _get_server_adapters_portchannels(
        self: ConnectedEndpoints, server: dict
    ) -> list[dict]:
        lag_interfaces = get_all_items(get(server, "interfaces"), "interface.lag")

        port_channels = {}

        vlan_settings = {}

        for lag_interface in lag_interfaces:
            lag_name = get(lag_interface, "interface.lag.name")
            connected_endpoint = get(lag_interface, "interface.connected_endpoints")[0]
            if lag_name not in port_channels.keys():
                port_channels[lag_name] = {
                    "endpoint_ports": [],
                    "switch_ports": [],
                    "switches": [],
                    "spanning_tree_portfast": "edge",
                    "port_channel": {
                        "description": "PortChannel " + get(server, "name"),
                        "mode": "active",
                    },
                }

            if lag_name not in vlan_settings.keys():
                vlan_settings[lag_name] = {}

            peer_switch = get_item(
                self.shared_utils.devices, "id", get(connected_endpoint, "device.id")
            )
            peer_interface = get_item(
                get(peer_switch, "interfaces"),
                "interface.id",
                get(connected_endpoint, "id"),
            )
            peer_lag = get(peer_interface, "interface.lag", required=True)
            peer_portchannel_interface = get_item(
                get(peer_switch, "interfaces"), "interface.id", get(peer_lag, "id")
            )

            merge(
                vlan_settings[lag_name],
                self._get_server_adapters_interfces_vlan(peer_portchannel_interface),
                same_key_strategy="must_match",
            )

            port_channels[lag_name]["endpoint_ports"].append(get(lag_interface, "name"))
            port_channels[lag_name]["switches"].append(
                get(connected_endpoint, "device.name")
            )
            port_channels[lag_name]["switch_ports"].append(
                get(connected_endpoint, "name")
            )

        merge(port_channels, vlan_settings)
        return list(port_channels.values())

    def _get_server_adapters_interfces(
        self: ConnectedEndpoints, server: dict
    ) -> list[dict]:
        res = []

        non_physical_types = ["virtual", "lag", "bridge"]

        server_interfaces = get(server, "interfaces")

        physical_interfaces = [
            interface
            for interface in server_interfaces
            if get(interface, "interface.type.value") not in non_physical_types
            and get(interface, "interface.lag") is None
        ]

        for interface in physical_interfaces:
            connected_endpoint = get(interface, "interface.connected_endpoints")[0]

            res.append(
                {
                    "endpoint_ports": [get(interface, "name")],
                    "switch_ports": [get(connected_endpoint, "name")],
                    "switches": [get(connected_endpoint, "device.name")],
                    "spanning_tree_portfast": "edge",
                }
            )

        return res

    def _get_server_adapters_interfces_vlan(
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
            raise UPONUDCFabInventoryError(
                f"Interface mode not allowed, Netbox mode is {get(interface, "interface.mode.value")}"
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
