# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from uponu_dc_fab_inventory.inventoryfacts import InventoryFacts


from functools import cached_property

from uponu_dc_fab_inventory.shared_utils.shared_utils import SharedUtils
from uponu_dc_fab_inventory.utils import get

from .spine import SpineMixin
from .l3leaf import L3leafMixin


class AvailabilityZone(InventoryFacts, SpineMixin, L3leafMixin):
    def __init__(self, shared_utils: SharedUtils, avialability_zone: str) -> None:
        super().__init__(shared_utils)

        self._avialability_zone = avialability_zone

    @cached_property
    def _filename(self):
        return f"{self._avialability_zone}.yml"
