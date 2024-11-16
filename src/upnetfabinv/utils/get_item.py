# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import Any
from .get import get

from upnetfabinv.errors import UpnetfabinvMissingVariableError


def get_item(
    data,
    key: str,
    value: Any | None = None,
    required: bool = False,
    separator: str = ".",
    value_case_sensitive: bool = True,
) -> Any:
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
    value_case_sensitive: bool
        Make the value match case sensitive.
        Value must be a string or castable to string if set to False
        

    Returns
    -------
    Any

    Raises
    ------
    UpnetfabinvMissingVariableError
        If the key and value is not found and "required" == True
    """
    if isinstance(data, list):
        for item in data:
            item_value = get(item, key, required=False, separator=separator)
            if item_value is not None and not value_case_sensitive:
                item_value = str(item_value).lower()

            if value is not None and not isinstance(value, list) and not value_case_sensitive:
                value = str(value).lower()
                
            if value is not None and value == item_value:
                return item
            elif isinstance(value, list):
                for val in value:
                    if val is not None and not value_case_sensitive:
                        val = str(val).lower()
                    if val == item_value:
                        return item

    if required:
        raise UpnetfabinvMissingVariableError(key)
