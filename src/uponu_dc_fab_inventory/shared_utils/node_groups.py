# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from uponu_dc_fab_inventory.utils import get_all

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class NodeGroupsMixin:

    def get_node_groups(self: SharedUtils, nodes: list[dict]) -> list:
        return set(get_all(nodes, "custom_fields.avd_switch_group_name"))