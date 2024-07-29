# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from uponu_dc_fab_inventory.utils import get_all_items, get_all, get

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class MLAGMixin:

    def mlag_interfaces(self: SharedUtils, node: dict, switch_group_name: str) -> list:

        self_name = get(node, "name")

        group_nodes = get_all_items(self.devices, "custom_fields.avd_switch_group_name", switch_group_name)

        node_names = get_all(group_nodes, "name")

        interface_names = []

        node_interfaces = get(node, "interfaces")

        for name in node_names:
            if self_name != name:

                for node_interface in node_interfaces:
                    connected_endpoint = get(node_interface, "interface.connected_endpoints")
                    if connected_endpoint is not None and name == get(connected_endpoint[0], "device.name"):
                        interface_names.append(get(node_interface, "name"))


        return interface_names
