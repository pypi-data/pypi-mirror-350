# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
"""A dummy module for backward compatability for code like e.g.
`from shrike.pipeline.argparser_utils import get_args_from_component_spec`.
Until `shrike<=1.34.0`, `argparser_utils` module existed under `shrike.pipeline`.
"""
from shrike.compliant_logging.argparser_utils import *
