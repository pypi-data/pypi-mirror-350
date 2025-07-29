# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Constant values used by this library.
"""

from azure.ai.ml._logging.compliant_logger import DataCategory  # noqa

# Keep the file path for backwards compatibility,
# but import the class directly from AML SDK V2 and expose it here
__all__ = ["DataCategory"]
