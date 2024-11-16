# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from upnetfabinv.errors import UpnetfabinvMissingVariableError


def get(dictionary, key, default=None, required=False, separator="."):
    """
    Get a value form a dictionarie or nested dictionary
    """

    if dictionary is None:
        if required:
            raise UpnetfabinvMissingVariableError(key)
        return default

    keys = str(key).split(separator)
    value = dictionary.get(keys[0])
    if value is None:
        if required:
            raise UpnetfabinvMissingVariableError(key)
        return default
    else:
        if len(keys) > 1:
            return get(
                value,
                separator.join(keys[1:]),
                default=default,
                required=required,
                separator=separator,
            )
        else:
            return value
