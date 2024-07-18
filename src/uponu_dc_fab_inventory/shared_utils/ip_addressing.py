# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from uponu_dc_fab_inventory.utils import get, get_item
from uponu_dc_fab_inventory.utils.ip_addressing import strip_subnet

if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class IpAddressingMixin:
    def get_loopback_ip(self: SharedUtils, node: dict) -> str | None:
        """
        Returns the loopback address for a device
        """

        loopback_ips = get(
            get_item(get(node, "interfaces"), "name", "loopback0"), "ips", default=[]
        )

        if len(loopback_ips) > 0:
            return strip_subnet(loopback_ips[0])

        return None

    def get_vtep_ip(self: SharedUtils, node: dict) -> str | None:
        vtep_ips = get(
            get_item(get(node, "interfaces"), "name", "loopback1"), "ips", default=[]
        )

        if len(vtep_ips) > 0:
            return strip_subnet(vtep_ips[0])

        return None
