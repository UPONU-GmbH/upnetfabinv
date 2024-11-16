# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations


def _split_optional_netmask(address):
    """
    Helper function to split an address with netmask into the adddress and the subnet part.
    """

    addr = str(address).split("/")

    if len(addr) > 2:
        raise ValueError("Address with subnet contains more than one '/'")

    return addr


def strip_subnet(address: str):
    """
    Removes the subnet in the end of an ip address sting
    """

    return _split_optional_netmask(address)[0]
