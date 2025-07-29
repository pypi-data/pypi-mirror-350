# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Helper code for connecting to AzureML and sharing one workspace accross code.
"""

import argparse
from azure.ai.ml import MLClient
from collections import namedtuple
import logging
import os

log = logging.getLogger(__name__)

CURRENT_ML_CLIENT = None


class MLClientNotInitializedError(Exception):
    """Error raised when trying to get an uninitialized MLClient"""

    def __init__(self, message="MLClient not initialized"):
        self.message = message
        super().__init__(self.message)


def current_ml_client(ml_client=None):
    """Sets/Gets the current MLClient used all across code.

    Args:
        ml_client (azureml.core.Workspace): any given workspace

    Returns:
        azureml.core.Workspace: current (last) workspace given to current_workspace()
    """
    global CURRENT_ML_CLIENT
    if ml_client:
        CURRENT_ML_CLIENT = ml_client

    if not CURRENT_ML_CLIENT:
        raise MLClientNotInitializedError(
            "You need to initialize current_ml_client() with an MLClient object."
        )

    return CURRENT_ML_CLIENT


def get_registry_ml_client(registry_name):
    """Return a registry client with same auth with current ML Client."""
    ml_client: MLClient = current_ml_client()
    registry_client = MLClient(
        credential=ml_client._credential,
        registry_name=registry_name,
        # TODO: these args can be removed later.
        # subscription_id=ml_client.subscription_id,
        # workspace_name=ml_client.workspace_name,
        # resource_group_name=ml_client.resource_group_name,
    )
    return registry_client


def add_cli_args(parser):
    """Adds parser arguments for connecting to AzureML

    Args:
        parser (argparse.ArgumentParser): parser to add AzureML arguments to

    Returns:
        argparse.ArgumentParser: that same parser
    """
    parser.add_argument(
        "--aml-subscription-id",
        dest="aml_subscription_id",
        type=str,
        required=False,
        help="",
    )
    parser.add_argument(
        "--aml-resource-group",
        dest="aml_resource_group",
        type=str,
        required=False,
        help="",
    )
    parser.add_argument(
        "--aml-workspace", dest="aml_workspace_name", type=str, required=False, help=""
    )
    parser.add_argument(
        "--aml-config",
        dest="aml_config",
        type=str,
        required=False,
        help="path to aml config.json file",
    )

    parser.add_argument(
        "--aml-auth",
        dest="aml_auth",
        type=str,
        choices=["azurecli", "msi", "interactive", "aml_job"],
        default="interactive",
    )
    parser.add_argument(
        "--aml-tenant",
        dest="aml_tenant",
        type=str,
        default=None,
        help="tenant to use for auth (default: auto)",
    )
    parser.add_argument(
        "--aml-force",
        dest="aml_force",
        type=lambda x: (
            str(x).lower() in ["true", "1", "yes"]
        ),  # we want to use --aml-force True
        default=False,
        help="force tenant auth (default: False)",
    )

    return parser


def azureml_connect(**kwargs):
    """Calls azureml_connect_cli with an argparse-like structure
    based on keyword arguments"""
    keys = [
        "aml_subscription_id",
        "aml_resource_group",
        "aml_workspace_name",
        "aml_config",
        "aml_auth",
        "aml_tenant",
        "aml_force",
    ]
    aml_args = dict([(k, kwargs.get(k)) for k in keys])

    azureml_argparse_tuple = namedtuple("AzureMLArguments", aml_args)
    aml_argparse = azureml_argparse_tuple(**aml_args)
    return azureml_connect_cli(aml_argparse)


def azureml_connect_cli(args):
    """Connects to an AzureML workspace.

    Args:
        args (argparse.Namespace): arguments to connect to AzureML

    Returns:
        azureml.core.Workspace: AzureML workspace
    """
    if args.aml_auth == "msi":
        # TODO: verify if this works
        from azure.identity import ManagedIdentityCredential

        auth = ManagedIdentityCredential()
    elif args.aml_auth == "azurecli":
        from azure.identity import AzureCliCredential

        auth = AzureCliCredential()
    elif args.aml_auth == "interactive":
        from azure.identity import InteractiveBrowserCredential

        auth = InteractiveBrowserCredential(
            tenant_id=args.aml_tenant, force=args.aml_force
        )
    else:
        auth = None

    if args.aml_auth == "aml_job":
        raise TypeError("Getting workspace info from run is not supported currently.")
        # aml_ws = Run.get_context().experiment.workspace
    elif args.aml_config:
        config_dir = os.path.dirname(args.aml_config)
        config_file_name = os.path.basename(args.aml_config)

        ml_client = MLClient.from_config(
            path=config_dir, file_name=config_file_name, credential=auth
        )

    else:
        ml_client = MLClient(
            credential=auth,
            subscription_id=args.aml_subscription_id,
            workspace_name=args.aml_workspace_name,
            resource_group_name=args.aml_resource_group,
        )
    ml_client._tenant_id = args.aml_tenant

    log.info("Connected to workspace:")
    log.info(f"\tsubscription: {args.aml_subscription_id}")
    log.info(f"\tname: {args.aml_workspace_name}")
    log.info(f"\tresource group: {args.aml_resource_group}")

    # TODO: no need to get workspace here since v2 is workspace independent
    return current_ml_client(ml_client)


def main():
    """Main function (for testing)"""
    parser = argparse.ArgumentParser(description=__doc__)

    group = parser.add_argument_group("AzureML connect arguments")
    add_cli_args(group)

    args, unknown_args = parser.parse_known_args()

    if unknown_args:
        log.warning(f"You have provided unknown arguments {unknown_args}")

    return azureml_connect_cli(args)


if __name__ == "__main__":
    main()
