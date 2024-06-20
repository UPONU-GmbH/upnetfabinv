# Copyright (c) 2023-2024 Arista Networks, Inc.
# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from copy import deepcopy
from deepmerge import Merger

def _strategy_must_match(config, path, base, nxt):
    if base != nxt:
        raise ValueError(f"Values of {'.'.join(path)} do not match: {base} != {nxt}")
    return base

def merge(base, *nxt_list, recursive=True, list_merge="append", same_key_strategy="override", destructive_merge=True):
    """
    Merge two or more data sets using deepmerge

    Parameters
    ----------
    base : Any
        The base data set
    *nxt_list : *Any
        One or more data sets which are merged one by one onto the base data set
    recursive : bool, default=True
        Perform recursive merge of dicts or just override with nxt.
    list_merge : str, default="append"
        Valid values: "append, replace, keep, prepend, append_rp, prepend_rp"
    same_key_strategy : str, default="override"
        Valid values: "override", "use_existing"
        Controls how dictionary keys that are in both base and nxt are handled:
        - "override" means nxt value replace base value.
        - "use_existing" means base value is kept.
        - "must_match" means a ValueError will be raised if values are not matching.
    destructive_merge : bool, default=True
        To optimize performance the merge is done in-place and is destructive for both base and nxt data sets by default.
        Base will be in-place updated with objects from nxt and some objects in nxt will be modified during the merge.
        By setting "destructive_merge=False" both base and nxt data sets will be deep copied and no in-place merge
        will be happen. Instead the merge result will be returned.
    """

    if not destructive_merge:
        base = deepcopy(base)

    list_strategies = ["append"]

    dict_strategies = ["merge" if recursive else "override"]

    if same_key_strategy == "must_match":
        same_key_strategy = _strategy_must_match

    merger = Merger(
        # List of tuples with strategies for each type
        [(list, list_strategies), (dict, dict_strategies), (set, ["union"])],
        # Fallback strategy applied to all other types
        [same_key_strategy],
        # Strategy for type conflict
        [same_key_strategy],
    )
    for nxt in nxt_list:
        if isinstance(nxt, list):
            for nxt_item in nxt:
                if not destructive_merge:
                    nxt_item = deepcopy(nxt_item)
                merger.merge(base, nxt_item)
        else:
            if not destructive_merge:
                nxt = deepcopy(nxt)
            merger.merge(base, nxt)

    return base