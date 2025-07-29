# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


class ShrikeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ShrikeUserErrorException(ShrikeException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
