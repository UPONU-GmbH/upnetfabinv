# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from upnetfabinv.utils import get_all_items


from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class ServersMixin:
    @cached_property
    def servers(self: SharedUtils) -> list:
        avd_endpoint_type = "server"

        devices = get_all_items(
            self.devices, "custom_fields.avd_endpoint_type", avd_endpoint_type
        )

        return devices
