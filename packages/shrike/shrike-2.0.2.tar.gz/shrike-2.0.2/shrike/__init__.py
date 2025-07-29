# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Python utilities to aid "compliant experimentation" - training
machine learning models without seeing the training data.
"""

__version__ = "2.0.2"

import os

# enable internal components in v2
os.environ["AZURE_ML_INTERNAL_COMPONENTS_ENABLED"] = "True"
os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"] = "True"
