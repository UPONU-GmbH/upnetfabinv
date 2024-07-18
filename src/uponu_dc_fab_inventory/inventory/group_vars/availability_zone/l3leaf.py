# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from __future__ import annotations


from functools import cached_property

from uponu_dc_fab_inventory.utils import get_all_items, get, get_all, merge

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .availability_zone import AvailabilityZone


class L3leafMixin:
    @cached_property
    def l3leaf_os10(self: AvailabilityZone):
        l3leafs_os10 = get_all_items(
            get_all_items(
                self.shared_utils.l3leafs, "custom_fields.avd_node_type", "l3leaf_os10"
            ),
            "site.name",
            self._avialability_zone,
        )

        node_groups = []

        for node_group in self._get_node_groups(l3leafs_os10):
            node_groups.append(
                self._get_l3leaf_os10_node_group(node_group, l3leafs_os10)
            )

        res = {"node_groups": node_groups}

        return res

    @cached_property
    def l3leaf(self: AvailabilityZone):
        l3leafs = get_all_items(
            get_all_items(
                self.shared_utils.l3leafs, "custom_fields.avd_node_type", "l3leaf"
            ),
            "site.name",
            self._avialability_zone,
        )

        node_groups = []

        for node_group in self._get_node_groups(l3leafs):
            node_groups.append(self._get_l3leaf_node_group(node_group, l3leafs))

        res = {"node_groups": node_groups}

        return res

    def _get_l3leaf_all_node(self: AvailabilityZone, node: dict) -> dict:
        """
        Get node config for all nodes. Same for l3leaf and l3leaf_os10.
        """

        node_config = {
            "name": get(node, "name", required=True),
            "id": get(node, "custom_fields.avd_switch_id", required=True),
            "mgmt_ip": get(node, "oob_ip.address", required=True),
        }

        if platform := get(node, "custom_fields.avd_platform"):
            node_config["platform"] = platform

        if loopback_ipv4_address := self.shared_utils.get_loopback_ip(node):
            node_config["loopback_ipv4_address"] = loopback_ipv4_address

        if vtep_ipv4_address := self.shared_utils.get_vtep_ip(node):
            node_config["vtep_ipv4_address"] = vtep_ipv4_address

        return node_config

    def _get_node_groups(self: AvailabilityZone, nodes: list[dict]) -> dict:
        return set(get_all(nodes, "custom_fields.avd_switch_group_name"))

    def _get_l3leaf_os10_node_group(
        self: AvailabilityZone, node_group: str, all_nodes: list[dict]
    ):
        group_nodes = get_all_items(
            all_nodes, "custom_fields.avd_switch_group_name", node_group
        )

        nodes = []

        for node in group_nodes:
            l3leaf_os10_node = self._get_l3leaf_all_node(node)

            merge(l3leaf_os10_node, self._get_l3leaf_all_uplink_connections(node))

            nodes.append(l3leaf_os10_node)

        res = {"group": node_group, "nodes": nodes}

        return res

    def _get_l3leaf_node_group(
        self: AvailabilityZone, node_group: str, all_nodes: list[dict]
    ):
        group_nodes = get_all_items(
            all_nodes, "custom_fields.avd_switch_group_name", node_group
        )

        nodes = []

        for node in group_nodes:
            l3leaf_node = self._get_l3leaf_all_node(node)

            merge(l3leaf_node, self._get_l3leaf_all_uplink_connections(node))

            nodes.append(l3leaf_node)

        res = {"group": node_group, "nodes": nodes}

        return res

    def _get_l3leaf_all_uplink_connections(self: AvailabilityZone, node: list[dict]):
        uplinks = {
            "uplink_switches": [],
            "uplink_switch_interfaces": [],
            "uplink_interfaces": [],
        }

        for interface in get(node, "interfaces"):
            for link_peer in get(interface, "link_peers"):
                if peer_device := get(link_peer, "device"):
                    peer = self.shared_utils.device(get(peer_device, "id"))

                    if get(peer, "custom_fields.avd_node_type") == "spine":
                        uplinks["uplink_switches"].append(get(peer, "name"))
                        uplinks["uplink_switch_interfaces"].append(
                            get(link_peer, "name")
                        )
                        uplinks["uplink_interfaces"].append(get(interface, "name"))

        return uplinks
