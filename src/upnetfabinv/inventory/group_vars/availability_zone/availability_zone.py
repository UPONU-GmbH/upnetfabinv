# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from upnetfabinv.inventoryfacts import InventoryFacts


from functools import cached_property

from upnetfabinv.shared_utils.shared_utils import SharedUtils
from upnetfabinv.utils import get

from .spine import SpineMixin
from .l3leaf import L3leafMixin
from .l2leaf import L2leafMixin


class AvailabilityZone(InventoryFacts, SpineMixin, L3leafMixin, L2leafMixin):
    def __init__(self, shared_utils: SharedUtils, avialability_zone: str) -> None:
        super().__init__(shared_utils)

        self._avialability_zone = avialability_zone

    @cached_property
    def _filename(self):
        return f"{self._avialability_zone}.yml"
    
    @cached_property
    def _dirname(self):
        return f"{self._avialability_zone}"
