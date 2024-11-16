# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import Any
from .get import get

from upnetfabinv.errors import UPONUDCFabInventoryMissingVariableError


def get_all_items(
    data,
    key: str,
    value: Any | None = None,
    required: bool = False,
    separator: str = ".",
) -> list[Any]:
    """
    Get all items where a spicific path exists

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
    list [any]

    Raises
    ------
    UPONUDCFabInventoryMissingVariableError
        If the key and value is not found and "required" == True
    """

    output = []
    if isinstance(data, list):
        for item in data:
            item_value = get(item, key, required=False, separator=separator)
            if value is not None and value == item_value:
                output.append(item)
            elif isinstance(value, list):
                for val in value:
                    if val == item_value:
                        output.append(item)
            elif value is None and item_value is not None:
                output.append(item)

    if required and len(output) == 0:
        raise UPONUDCFabInventoryMissingVariableError(key)

    return output
