
# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from uponu_dc_fab_inventory.utils import get, get_item


if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class InterfacesMixin:


    def get_peer_interface(self: SharedUtils, peer_switch: dict, connected_endpoint: dict, link_peer: dict) -> dict:
        """
        Returns the correct peer interface, also works with breakout interfaces

        In Netbox it is not possible to directly use breakout interfaces and connecting them.
        As a workaround we create normal interfaces and only connect the main (parent) interface.
        The correct interface number is then retrieved by exploiting the number of the breakout cable in the link_peer.

        For now this only works with a breakout box which is an actual device in netbox with front and backend ports.
        """

        # netbox creates a colon and the breakout number at the of the interface name
        # Ex: LC:4
        if get(link_peer, "id") != get(connected_endpoint, "id") and len(interface_name_split:=get(link_peer, "name").split(":")) > 1:
            
            subinterface_number = interface_name_split[-1]

            subinterface_name = re.sub(r"(Ethernet\s*\d*\/)\d*$", r"\1", get(connected_endpoint, "name")) + subinterface_number

            peer_interface = get_item(
                get(peer_switch, "interfaces"),
                "interface.name",
                subinterface_name
            )


        else:

            peer_interface = get_item(
                get(peer_switch, "interfaces"),
                "interface.id",
                get(connected_endpoint, "id"),
            )

        return peer_interface