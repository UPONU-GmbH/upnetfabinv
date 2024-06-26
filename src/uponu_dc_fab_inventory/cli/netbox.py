# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import click
from ..resources import NetboxClient
from pynetbox import RequestError

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from click import Context
    from ..resources import Config
    from pynetbox import api as NetboxApi

import logging
logger = logging.getLogger(__name__)

"""Device ID definition. An integer number used for internal calculations """

from pprint import pprint

@click.group
@click.pass_context
def netbox(ctx: Context):

    config: Config = ctx.obj["conf"]
    # Initialize the pynetbox API client
    ctx.obj["netbox_client"] = NetboxClient(config.get("netbox.NETBOX_URL"), config.get("netbox.NETBOX_API_TOKEN"), config.get("netbox.dcim_devices_default_filter"))

@netbox.command
@click.pass_context
def setup(ctx: Context):

    api: NetboxApi = ctx.obj["netbox_client"].netbox
    
    # Define the custom field parameters
    

    custom_field_choice_sets_data = [
        {
            "name": "avd_nos_family",
            "description": "Possible AVD NOS families",
            "order_alphabetically": False,
            "extra_choices": [
                ["EOS", "EOS"],
                ["OS10", "OS10"]
            ]
        },
        {
            "name": "avd_switch_groups",
            "description": "Possible AVD switch groups",
            "order_alphabetically": False,
            "extra_choices": [
                ["l3leaf", "l3leaf"],
                ["l3leaf_os10", "l3leaf_os10"],
                ["l2leaf", "l2leaf"],
                ["spine", "spine"]
            ]
        }
    ]
    
    for custom_field_choice_set_data in custom_field_choice_sets_data:
        try:
            api.extras.custom_field_choice_sets.create(custom_field_choice_set_data)
        except RequestError as e:
            logger.warn(e.message)

    #"default": "",
    custom_fields_data = [
        {
            "content_types": ["dcim.device"],
            "name": "avd_nos_family",
            "label": "Switch NOS family",
            "group_name": "AVD",
            "type": "select",
            "description": "",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
            "choice_set": api.extras.custom_field_choice_sets.get(name="avd_nos_family").id
        },
        {
            "content_types": ["dcim.device"],
            "name": "avd_switch_group",
            "label": "Switch Group",
            "group_name": "AVD",
            "type": "select",
            "description": "",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
            "choice_set": api.extras.custom_field_choice_sets.get(name="avd_switch_groups").id
        },
        {
            "content_types": ["dcim.device"],
            "name": "avd_switch_id",
            "label": "Switch Id",
            "group_name": "AVD",
            "type": "select",
            "description": "Unique Switch ID",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
            "choice_set": api.extras.custom_field_choice_sets.get(name="avd_nos_family").id
        }
    ]

    for custom_field_data in custom_fields_data:
        try:
            api.extras.custom_fields.create(custom_field_data)
        except RequestError as e:
            logger.warn(e.message)

    #custom_field = api.extras.custom_fields.create(custom_field_data)
