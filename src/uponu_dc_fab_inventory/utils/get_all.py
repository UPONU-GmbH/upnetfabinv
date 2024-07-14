# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from .get import get

def get_all(items: list[dict], key, default=None, required=False, separator=".") -> list[dict]:
    """
    Get all values form a list of dictionaries
    Parameters
    ----------
    items : list[dict]
        Data to walk through
    key : str
        Data Path - supporting dot-notation for nested dictionaries/lists
    required : bool
        Fail if there is no match
    separator: str
        String to use as the separator parameter in the split function. Useful in cases when the key
        can contain variables with "." inside (e.g. hostnames)

    Returns
    -------
    list [dict]

    Raises
    ------
    UPONUDCFabInventoryMissingVariableError
        If the key and value is not found and "required" == True
    """

    result = []

    for dictionary in items:
        result.append(get(dictionary, key, default, required, separator))

    return result