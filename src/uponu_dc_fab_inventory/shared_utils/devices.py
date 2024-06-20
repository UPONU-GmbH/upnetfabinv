# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from pprint import pprint

if TYPE_CHECKING:
    from .shared_utils import SharedUtils

class DevicesMixin():
    
    @cached_property
    def devices(self: SharedUtils) -> list:

        # Get devices by site ID and role ID
        devices = self.netbox.dcim_devices_filter()

        return devices
    