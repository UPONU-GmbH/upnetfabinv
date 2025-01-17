# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

from upnetfabinv.inventoryfacts import InventoryFacts


from functools import cached_property

from upnetfabinv.shared_utils.shared_utils import SharedUtils
from upnetfabinv.utils import get

from .tenants import TennantsMixin


class NetworkServices(InventoryFacts, TennantsMixin):
    def __init__(self, shared_utils: SharedUtils) -> None:
        super().__init__(shared_utils)

    @cached_property
    def _filename(self):
        return "NETWORK_SERVICES.yml"
    
    @cached_property
    def _dirname(self):
        return "NETWORK_SERVICES"
