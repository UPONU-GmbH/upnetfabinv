# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from uponu_dc_fab_inventory.utils import get_all_items


from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class TenatnsMixin:
    @cached_property
    def tenants(self: SharedUtils) -> list:
        tenants = self.netbox.tenancy_tenants_filter(tag=["avd"])

        return tenants

    @cached_property
    def vrfs(self: SharedUtils) -> list:
        vrfs = self.netbox.ipam_vrfs_filter(tag=["avd"])

        return vrfs
