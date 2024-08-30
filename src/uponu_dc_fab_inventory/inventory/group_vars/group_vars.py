# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import yaml
import os

from uponu_dc_fab_inventory.inventoryfacts import InventoryFacts

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uponu_dc_fab_inventory.shared_utils import SharedUtils


class GroupVars(InventoryFacts):
    def __init__(self, dirname, filename, shared_utils: SharedUtils) -> None:
        super().__init__(shared_utils)
        self._dirname = dirname
        self._filename = filename

    def save(self, our_path: str, override_path: str):
        """
        Renders the class and
        """

        result = self.render()

        with open(os.path.join(our_path, self.filename), "w") as fd:
            yaml.dump(result, fd)
