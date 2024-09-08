# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from uponu_dc_fab_inventory.resources import NetboxClient

from .spines import SpinesMixin
from .leafs import LeafsMixin
from .devices import DevicesMixin
from .ip_addressing import IpAddressingMixin
from .tenants import TenatnsMixin
from .vlans import VlansMixin
from .servers import ServersMixin
from .node_groups import NodeGroupsMixin
from .mlag import MLAGMixin
from .switches import SwitchesMixin
from .interfaces import InterfacesMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uponu_dc_fab_inventory.resources import Config


class SharedUtils(
    SpinesMixin,
    LeafsMixin,
    DevicesMixin,
    IpAddressingMixin,
    TenatnsMixin,
    VlansMixin,
    ServersMixin,
    NodeGroupsMixin,
    MLAGMixin,
    SwitchesMixin,
    InterfacesMixin
):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.netbox = NetboxClient(config)
