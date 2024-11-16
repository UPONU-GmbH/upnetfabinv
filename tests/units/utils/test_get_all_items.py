# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

import pytest

from upnetfabinv.utils import get_all_items
from upnetfabinv.errors import UpnetfabinvMissingVariableError


from contextlib import contextmanager


@contextmanager
def does_not_raise():
    yield


GET_ALL_ITEMS_DATA = [
    {  # normal case
        "list": [
            {
                "id": 1,
                "key1": "value1",
                "key2": "value2",
                "dict_key": {
                    "sub_key1": "sub_value1",
                    "sub_key2": "sub_value2",
                },
            },
            {
                "id": 2,
                "key1": "value1",
                "key2": "value2",
                "dict_key": {
                    "sub_key1": "sub_value1",
                    "sub_key2": "sub_value2",
                },
            },
            {
                "id": 3,
                "key3": "value3",
                "key4": "value4",
                "dict_key": {
                    "sub_key2": "sub_value2",
                    "sub_key3": "sub_value3",
                    "sub_key4": "sub_value4",
                },
            },
            {
                "id": 4,
                "key4": "value4",
                "key3": "value3",
                "dict_key": {
                    "sub_key3": "sub_value3",
                    "sub_key4": "sub_value4",
                },
            },
            {
                "id": 5,
                "key4": "value3",
                "key3": "value4",
                "dict_key": {
                    "sub_key3": "sub_value3",
                    "sub_key4": "sub_value4",
                },
            },
        ],
        "key": "key3",
        "value": "value3",
        "required": False,
        "expected_result": [
            {
                "id": 3,
                "key3": "value3",
                "key4": "value4",
                "dict_key": {
                    "sub_key2": "sub_value2",
                    "sub_key3": "sub_value3",
                    "sub_key4": "sub_value4",
                },
            },
            {
                "id": 4,
                "key4": "value4",
                "key3": "value3",
                "dict_key": {
                    "sub_key3": "sub_value3",
                    "sub_key4": "sub_value4",
                },
            },
        ],
        "expected_length": 2,
        "expected_exception": does_not_raise(),
    },
    {  # required - missing
        "list": [
            {
                "id": 1,
                "key1": "value1",
                "key2": "value2",
                "dict_key": {
                    "sub_key1": "sub_value1",
                    "sub_key2": "sub_value2",
                },
            },
            {
                "id": 2,
                "key1": "value1",
                "key2": "value2",
                "dict_key": {
                    "sub_key1": "sub_value1",
                    "sub_key2": "sub_value2",
                },
            },
            {
                "id": 3,
                "key3": "value3",
                "key4": "value4",
                "dict_key": {
                    "sub_key2": "sub_value2",
                    "sub_key3": "sub_value3",
                    "sub_key4": "sub_value4",
                },
            },
            {
                "id": 4,
                "key4": "value4",
                "key3": "value3",
                "dict_key": {
                    "sub_key3": "sub_value3",
                    "sub_key4": "sub_value4",
                },
            },
            {
                "id": 5,
                "key4": "value3",
                "key3": "value4",
                "dict_key": {
                    "sub_key3": "sub_value3",
                    "sub_key4": "sub_value4",
                },
            },
        ],
        "key": "key5.missing_required",
        "value": "value3",
        "required": True,
        "expected_result": None,
        "expected_length": 0,
        "expected_exception": pytest.raises(
            UpnetfabinvMissingVariableError, match="key5.missing_required"
        ),
    },
]


class TestUtilsGetAllItems:
    @pytest.mark.parametrize("DATA", GET_ALL_ITEMS_DATA)
    def test_get_all_items(self, DATA):
        with DATA["expected_exception"]:
            res = get_all_items(
                DATA["list"], DATA["key"], DATA["value"], DATA["required"]
            )
            assert res == DATA["expected_result"]
            assert len(res) == DATA["expected_length"]
