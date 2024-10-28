# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from __future__ import annotations


from functools import cached_property

from uponu_dc_fab_inventory.utils import get_all_items, get, get_item, merge

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .availability_zone import AvailabilityZone


class L2leafMixin:

    @cached_property
    def l2leaf(self: AvailabilityZone):
        l2leafs = get_all_items(
            self.shared_utils.l2leafs,
            "site.name",
            self._avialability_zone,
        )

        node_groups = []

        for node_group in self.shared_utils.get_node_groups(l2leafs):
            node_groups.append(self._get_l2leaf_node_group(node_group, l2leafs))

        res = {"node_groups": node_groups}

        return res

    def _get_l2leaf_all_node(self: AvailabilityZone, node: dict) -> dict:
        """
        Get node config for all nodes.
        """

        node_config = {
            "name": get(node, "name", required=True),
            "id": get(node, "custom_fields.avd_switch_id", required=True),
            "mgmt_ip": get(node, "oob_ip.address", required=True),
        }

        if platform := get(node, "custom_fields.avd_platform"):
            node_config["platform"] = platform

        return node_config


    def _get_l2leaf_node_group(
        self: AvailabilityZone, node_group: str, all_nodes: list[dict]
    ):
        group_nodes = get_all_items(
            all_nodes, "custom_fields.avd_switch_group_name", node_group
        )

        nodes = []

        for node in group_nodes:
            l2leaf_node = self._get_l2leaf_all_node(node)

            merge(l2leaf_node, self._get_l2leaf_all_uplink_connections(node))

            nodes.append(l2leaf_node)

        res = {"group": node_group, "nodes": nodes}

        return res

    def _get_l2leaf_all_uplink_connections(self: AvailabilityZone, node: list[dict]):
        uplinks = {
            "uplink_switches": [],
            "uplink_switch_interfaces": [],
            "uplink_interfaces": [],
        }

        for interface in get(node, "interfaces"):
            for connected_endpoint in get(
                interface, "interface.connected_endpoints", default=[]
            ):
                
                if peer_device := get(connected_endpoint, "device"):
                    peer = get_item(
                        self.shared_utils.devices, "id",get(peer_device, "id")
                    )

                    peer_interface = get_item(get(peer, "interfaces"), "interface.name", get(connected_endpoint, "name"))

                    if get(peer_interface, "interface.mgmt_only", default=False):
                        continue


                    if get(peer, "custom_fields.avd_node_type") in ["l3leaf", "l3leaf_os10"]:
                        uplinks["uplink_switches"].append(get(peer, "name"))
                        uplinks["uplink_switch_interfaces"].append(
                            get(connected_endpoint, "name")
                        )
                        uplinks["uplink_interfaces"].append(get(interface, "name"))

                        # TODO: check if interfaces speed is the same for all uplinks
                        if speed := self.shared_utils.get_interface_speed_value(get(peer_interface, "interface.speed")):
                            uplinks["uplink_switch_interface_speed"] = speed

        return uplinks
