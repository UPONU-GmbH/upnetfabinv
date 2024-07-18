# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations


from functools import cached_property

from uponu_dc_fab_inventory.utils import get_all_items, get, get_all, merge
from uponu_dc_fab_inventory.errors import UPONUDCFabInventoryError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .network_services import NetworkServices

from pprint import pprint


class TennantsMixin:
    @cached_property
    def tenants(self: NetworkServices):
        tenants = []

        for tenant in self.shared_utils.tenants:
            tenants.append(self._get_tenant(tenant))

        return tenants

    def _get_tenant(self: NetworkServices, tenant: dict):
        res = {}

        tenant_name = get(tenant, "name")

        res["name"] = tenant_name
        if mac_vrf_vni_base := get(tenant, "custom_fields.avd_mac_vrf_vni_base"):
            res["mac_vrf_vni_base"] = mac_vrf_vni_base

        vrfs = self._get_tenant_vrfs(tenant)
        if len(vrfs) > 0:
            res["vrfs"] = vrfs

        l2vlans = self._get_tenant_l2vlans(tenant)
        if len(l2vlans) > 0:
            res["l2vlans"] = l2vlans

        return res

    def _get_tenant_vrfs(self: NetworkServices, tenant: dict):
        vrfs = []

        tenant_name = get(tenant, "name")
        vrfs = []
        for vrf in get_all_items(self.shared_utils.vrfs, "tenant.name", tenant_name):
            vrfs.append(self._get_tenant_vrf(vrf))

        return vrfs

    def _get_tenant_vrf(self: NetworkServices, vrf: dict):
        return {
            "name": get(vrf, "name"),
            "vrf_vni": get(vrf, "custom_fields.avd_vrf_vni"),
            "svis": self._get_tenant_vrf_svis(vrf),
        }

    def _get_tenant_vrf_svis(self: NetworkServices, vrf: dict):
        svis = []

        for vlan_id in get_all(get(vrf, "custom_fields.avd_svi_ids", default=[]), "id"):
            vlan = self.shared_utils.vlan(vlan_id)

            if get(vlan, "custom_fields.avd_is_l2vlan"):
                raise UPONUDCFabInventoryError(
                    f"Vlan cannot be an svi and l2vlan at the same time, netbox_id: {vlan_id}"
                )

            svis.append(
                {
                    "id": get(vlan, "vid", required=True),
                    "name": get(vlan, "name", required=True),
                    "ip_address_virtual": get(
                        self.shared_utils.vlan(vlan_id),
                        "custom_fields.avd_svi_ip_address_virtual.address",
                        required=True,
                    ),
                }
            )

        return svis

    def _get_tenant_l2vlans(self: NetworkServices, tenant: dict):
        vlans = []

        for vlan in get_all_items(
            self.shared_utils.vlans, "tenant.id", get(tenant, "id")
        ):
            if get(vlan, "custom_fields.avd_is_l2vlan"):
                vlans.append(
                    {
                        "id": get(vlan, "vid", required=True),
                        "name": get(vlan, "name", required=True),
                    }
                )

        return vlans
