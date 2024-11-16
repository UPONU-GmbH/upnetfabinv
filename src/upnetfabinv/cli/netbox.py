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


@click.group
@click.pass_context
def netbox(ctx: Context):
    config: Config = ctx.obj["conf"]
    # Initialize the pynetbox API client
    ctx.obj["netbox_client"] = NetboxClient(config)


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
            "extra_choices": [["EOS", "EOS"], ["OS10", "OS10"]],
        },
        {
            "name": "avd_node_types",
            "description": "Possible AVD node types",
            "order_alphabetically": False,
            "extra_choices": [
                ["l3leaf", "l3leaf"],
                ["l3leaf_os10", "l3leaf_os10"],
                ["l2leaf", "l2leaf"],
                ["spine", "spine"],
            ],
        },
        {
            "name": "avd_platforms",
            "description": "Possible AVD device platforms",
            "order_alphabetically": False,
            "extra_choices": [
                ["S4148-ON", "S4148-ON"],
            ],
        },
        {
            "name": "avd_endpoint_types",
            "description": "Possible AVD endpoints types",
            "order_alphabetically": False,
            "extra_choices": [["server", "server"]],
        },
    ]

    for custom_field_choice_set_data in custom_field_choice_sets_data:
        try:
            api.extras.custom_field_choice_sets.create(custom_field_choice_set_data)
        except RequestError as e:
            logger.warn(e.message)

    # "default": "",
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
            "choice_set": api.extras.custom_field_choice_sets.get(
                name="avd_nos_family"
            ).id,
        },
        {
            "content_types": ["dcim.device"],
            "name": "avd_node_type",
            "label": "Node Type",
            "group_name": "AVD",
            "type": "select",
            "description": "",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
            "choice_set": api.extras.custom_field_choice_sets.get(
                name="avd_node_types"
            ).id,
        },
        {
            "content_types": ["dcim.device"],
            "name": "avd_switch_id",
            "label": "Switch Id",
            "group_name": "AVD",
            "type": "integer",
            "description": "Unique Switch ID",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": False,
        },
        {
            "content_types": ["dcim.device"],
            "name": "avd_switch_platform",
            "label": "Switch Platform",
            "group_name": "AVD",
            "type": "select",
            "description": "",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
            "choice_set": api.extras.custom_field_choice_sets.get(
                name="avd_platforms"
            ).id,
        },
        {
            "content_types": ["dcim.device"],
            "name": "avd_switch_group_name",
            "label": "Switch Group Name",
            "group_name": "AVD",
            "type": "text",
            "description": "Name for switch group. Only two devices are allowed to be in one group",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
        },
        {
            "content_types": ["dcim.device"],
            "name": "avd_bgp_as",
            "label": "BGP AS number",
            "group_name": "AVD",
            "type": "integer",
            "description": "The bgp as number for a decive",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
        },
        {
            "content_types": ["ipam.vrf"],
            "name": "avd_vrf_vni",
            "label": "VRF VNI",
            "group_name": "AVD",
            "type": "integer",
            "description": "The VNI for the VRF",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
        },
        {
            "content_types": ["ipam.vrf"],
            "name": "avd_svi_ids",
            "label": "SVI interface id and VLAN ids",
            "group_name": "AVD",
            "type": "multiobject",
            "object_type": "ipam.vlan",
            "description": "",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": False,
        },
        {
            "content_types": ["tenancy.tenant"],
            "name": "avd_mac_vrf_vni_base",
            "label": "MAC vrf vni base",
            "group_name": "AVD",
            "type": "integer",
            "description": "Start VNI for the MAC vrfs",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
        },
        {
            "content_types": ["ipam.vlan"],
            "name": "avd_svi_ip_address_virtual",
            "label": "ip_address_virtual",
            "group_name": "AVD",
            "type": "object",
            "object_type": "ipam.ipaddress",
            "description": "IPv4 VXLAN Anycast IP address",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
        },
        {
            "content_types": ["ipam.vlan"],
            "name": "avd_is_l2vlan",
            "label": "Is l2vlan",
            "group_name": "AVD",
            "type": "boolean",
            "description": "",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
        },
        {
            "content_types": ["dcim.device"],
            "name": "avd_endpoint_type",
            "label": "Endpoint Type",
            "group_name": "AVD",
            "type": "select",
            "description": "",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
            "choice_set": api.extras.custom_field_choice_sets.get(
                name="avd_endpoint_types"
            ).id,
        },
        {
            "content_types": ["dcim.interface"],
            "name": "avd_lacp_fallback_enabled",
            "label": "LACP Fallback",
            "group_name": "AVD",
            "type": "boolean",
            "description": "Only applicable for port-channel interfaces",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": True,
        },
        {
            "content_types": ["dcim.interface"],
            "name": "avd_lacp_fallback_timeout",
            "label": "LACP Fallback timeout",
            "group_name": "AVD",
            "type": "integer",
            "description": "Only applicable for port-channel interfaces",
            "search_weight": 1000,
            "filter_logic": "loose",
            "ui_visibility": "visible",
            "ui_editable": "yes",
            "weight": 100,
            "is_cloneable": False,
        },
    ]

    for custom_field_data in custom_fields_data:
        try:
            api.extras.custom_fields.create(custom_field_data)
            logger.info(f"Created new custem field: {custom_field_data["name"]}")
        except RequestError as e:
            logger.warn(e.message)
