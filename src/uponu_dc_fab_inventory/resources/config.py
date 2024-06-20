# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations


import tomllib

from uponu_dc_fab_inventory.utils import get


class Config:

    def __init__(self, config_path: str) -> None:
        
        with open(config_path, "rb") as fd:

            self.conf = tomllib.load(fd)

    
    def get(self, key: str, default: str | None = None, requried: bool = False) -> None:

        return get(self.conf, key, default, requried)