# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import Any
from .get import get

from uponu_dc_fab_inventory.errors import UPONUDCFabInventoryMissingVariableError



def get_item(data, key: str, value: Any | None = None, required: bool = False, separator: str = ".") -> Any:
    """
    Get an item where a spicific path exists, returns only the first match

    Parameters
    ----------
    data : any
        Data to walk through
    key : str
        Data Path - supporting dot-notation for nested dictionaries/lists
    value : any
        Value that must match
    required : bool
        Fail if there is no match
    separator: str
        String to use as the separator parameter in the split function. Useful in cases when the key
        can contain variables with "." inside (e.g. hostnames)

    Returns
    -------
    Any

    Raises
    ------
    UPONUDCFabInventoryMissingVariableError
        If the key and value is not found and "required" == True
    """
    if isinstance(data, list):
        for item in data:
            item_value = get(item, key, required=False, separator=separator)
            if value is not None and value == item_value:
                return item
            elif isinstance(value, list):
                for val in value:
                    if val == item_value:
                        return item
    
    if required:
        raise UPONUDCFabInventoryMissingVariableError(key)