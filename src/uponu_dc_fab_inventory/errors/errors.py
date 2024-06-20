# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.

class UPONUDCFabInventoryError(Exception):

    def __init__(self, message="An error has occourd in a uponu_dc_fab_inventory module"):

        self.message = message
        super().__init__(self.message)

class UPONUDCFabInventoryMissingVariableError(UPONUDCFabInventoryError):
    pass