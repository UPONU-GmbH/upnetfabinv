# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from uponu_dc_fab_inventory.inventoryfacts import InventoryFacts


from functools import cached_property

from uponu_dc_fab_inventory.shared_utils.shared_utils import SharedUtils


class Spines(
    InventoryFacts,
):
    def __init__(self, shared_utils: SharedUtils, avialability_zone: str) -> None:
        super().__init__(shared_utils)

        self._avialability_zone = avialability_zone

    @cached_property
    def type(self):
        return "spine"

    @cached_property
    def _filename(self):
        return f"{self._avialability_zone}_SPINES.yml"
    
    @cached_property
    def _dirname(self):
        return f"{self._avialability_zone}_SPINES"
