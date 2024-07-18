# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from uponu_dc_fab_inventory.utils import get_all_items


from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class SpinesMixin:
    @cached_property
    def spines(self: SharedUtils) -> list:
        avd_node_type = "spine"

        devices = get_all_items(
            self.devices, "custom_fields.avd_node_type", avd_node_type
        )

        return devices
