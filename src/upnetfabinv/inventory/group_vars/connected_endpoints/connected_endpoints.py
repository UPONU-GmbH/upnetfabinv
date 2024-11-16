# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from upnetfabinv.inventoryfacts import InventoryFacts


from functools import cached_property

from upnetfabinv.shared_utils.shared_utils import SharedUtils

from .servers import ServersMixin
from .switches_oob import SwitchesOOBMixin


class ConnectedEndpoints(InventoryFacts, ServersMixin, SwitchesOOBMixin):
    def __init__(self, shared_utils: SharedUtils) -> None:
        super().__init__(shared_utils)

    @cached_property
    def _filename(self):
        return "CONNECTED_ENDPOINTS.yml"
    
    @cached_property
    def _dirname(self):
        return "CONNECTED_ENDPOINTS"
