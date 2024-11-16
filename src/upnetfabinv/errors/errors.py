# Copyright (c) 2024 UPONU GmbH
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.


class UpnetfabinvError(Exception):
    def __init__(
        self, message="An error has occourd in a upnetfabinv module"
    ):
        self.message = message
        super().__init__(self.message)


class UpnetfabinvMissingVariableError(UpnetfabinvError):
    pass
