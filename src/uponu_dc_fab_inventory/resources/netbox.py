# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations


import pynetbox

from .config import Config

from uponu_dc_fab_inventory.utils import merge, get_all

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pynetbox.core.response import RecordSet


import logging
logger = logging.getLogger(__name__)

class NetboxClient():

    def __init__(self,
        config: Config) -> None:
        
        self.netbox = pynetbox.api(config.get("netbox.NETBOX_URL"), config.get("netbox.NETBOX_API_TOKEN"))
    
        config.get("netbox.dcim_devices_default_filter")

        site_names = config.get("fabric.availability_zones")
        sites = response_as_list(self.netbox.dcim.sites.filter(name=site_names))

        if len(sites) == 0:
            logger.error("No sites found with the names {}".format(",".join(site_names)))
        elif len(sites) < len(site_names):
            logger.warn("Not all sites were found")
        
        default_dcim_device_filter = {
            "site_id": get_all(sites, "id", required=True)
        }

        default_dcim_interface_filter = {}

        self.default_dcim_device_filter = default_dcim_device_filter
        self.default_dcim_interface_filter = default_dcim_interface_filter

        merge(self.default_dcim_device_filter, config.get("netbox.dcim_devices_default_filter"))

    def dcim_devices_filter(self, **filter) -> list[dict]:

        filter = merge(self.default_dcim_device_filter, filter, destructive_merge=False)

        netbox_res = self.netbox.dcim.devices.filter(**filter)

        res = response_as_list(netbox_res)

        return res
    
    def dcim_devices_get(self, device_id) -> dict:

        #filter = merge(self.default_dcim_device_filter, filter, destructive_merge=False)

        netbox_res = self.netbox.dcim.devices.get(id=device_id)

        res = dict(netbox_res)

        return res
    
    def dcim_interfaces_filter(self, **filter) -> list[dict]:

        filter = merge(self.default_dcim_interface_filter, filter, destructive_merge=False)

        netbox_res = self.netbox.dcim.interfaces.filter(**filter)

        res = response_as_list(netbox_res)

        return res
    
    def ipam_ip_addresses_filter(self, **filter) -> list[dict]:

        netbox_res = self.netbox.ipam.ip_addresses.filter(**filter)

        res = response_as_list(netbox_res)

        return res

def response_as_list(response: RecordSet):

    res = []

    for item in response:
        res.append(dict(item))

    return res