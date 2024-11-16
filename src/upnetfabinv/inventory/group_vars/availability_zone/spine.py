# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations


from functools import cached_property

from upnetfabinv.utils import get_all_items, get

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .availability_zone import AvailabilityZone


class SpineMixin:
    @cached_property
    def spine(self: AvailabilityZone):
        spines = self.shared_utils.spines
        nodes = []

        for spine in get_all_items(spines, "site.name", self._avialability_zone):
            nodes.append(self._get_spine_node(spine))

        return {"nodes": nodes}

    def _get_spine_node(self: AvailabilityZone, node):
        node_config = {
            "name": get(node, "name", required=True),
            "id": get(node, "custom_fields.avd_switch_id", required=True),
            "mgmt_ip": get(node, "oob_ip.address", required=True),
            "bgp_as": get(node, "custom_fields.avd_bgp_as", required=True)
        }

        if platform := get(node, "custom_fields.avd_platform"):
            node_config["platform"] = platform

        if loopback_ipv4_address := self.shared_utils.get_loopback_ip(node):
            node_config["loopback_ipv4_address"] = loopback_ipv4_address

        return node_config
