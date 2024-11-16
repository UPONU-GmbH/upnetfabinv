# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from upnetfabinv.inventoryfacts import InventoryFacts


from functools import cached_property

from upnetfabinv.shared_utils.shared_utils import SharedUtils


class L3LeavesOS10(
    InventoryFacts,
):
    def __init__(self, shared_utils: SharedUtils, avialability_zone: str) -> None:
        super().__init__(shared_utils)

        self._avialability_zone = avialability_zone

    @cached_property
    def type(self):
        return "l3leaf_os10"

    @cached_property
    def overlay_rd_type(self):
        """
        Overlay rd type to use vtep for RD.
        Forr vlti the RDs must be the same on the vlti peers
        """

        return {"admin_subfield": "vtep_loopback"}

    @cached_property
    def _filename(self):
        return f"{self._avialability_zone}_L3_LEAVES_OS10.yml"
    
    @cached_property
    def _dirname(self):
        return f"{self._avialability_zone}_L3_LEAVES_OS10"
