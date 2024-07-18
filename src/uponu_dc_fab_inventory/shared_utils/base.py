# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shared_utils import SharedUtils


class BaseMixin:
    @cached_property
    def az_name(self: SharedUtils) -> str:
        return "DC1"
