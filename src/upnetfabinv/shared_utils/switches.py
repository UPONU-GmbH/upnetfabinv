# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations


from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class SwitchesMixin:

    @cached_property
    def switches(self: SharedUtils) -> list:
        
        switches = self.spines + self.l3leafs + self.l2leafs

        return switches
