# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from uponu_dc_fab_inventory.inventoryfacts import InventoryFacts


from functools import cached_property

from uponu_dc_fab_inventory.shared_utils.shared_utils import SharedUtils

from .servers import ServersMixin


class ConnectedEndpoints(InventoryFacts, ServersMixin):
    def __init__(self, shared_utils: SharedUtils) -> None:
        super().__init__(shared_utils)

    @cached_property
    def _filename(self):
        return "CONNECTED_EDNPOINTS.yml"
