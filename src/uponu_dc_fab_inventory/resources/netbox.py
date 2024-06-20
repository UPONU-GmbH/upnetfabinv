# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

import pynetbox

from pprint import pprint


from uponu_dc_fab_inventory.utils import merge

class NetboxClient():

    def __init__(self,
        url: str, 
        token: str, 
        default_dcim_device_filter: dict = {}) -> None:
        
        self.netbox = pynetbox.api(url, token)
        self.default_dcim_device_filter = default_dcim_device_filter

    def dcim_devices_filter(self, **filter) -> list[dict]:

        filter = merge(self.default_dcim_device_filter, filter, destructive_merge=False)

        res = []

        netbox_res = self.netbox.dcim.devices.filter(**filter)

        for el in netbox_res:
            res.append(dict(el))

        return res
