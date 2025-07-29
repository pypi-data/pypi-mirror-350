# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Pipeline helper class to create pipelines loading modules from a flexible manifest.
"""
from shrike.pipeline.module_helper_base import AMLModuleLoaderBase

try:
    from azure.ai.ml import load_component, MLClient
except ImportError as error:
    raise ImportError(
        f"{error.msg}. Please install v2 dependency `pip install azure-ai-ml`."
    )
import logging
from packaging.specifiers import SpecifierSet
from packaging.version import Version, InvalidVersion

from shrike.pipeline.aml_connect import current_ml_client, get_registry_ml_client

log = logging.getLogger(__name__)


class AMLModuleLoader(AMLModuleLoaderBase):
    """Helper class to load modules from within an AMLPipelineHelper in dpv2."""

    def load_local_module_helper(self, module_spec_path):
        return load_component(source=module_spec_path)

    def solve_module_version_and_load(
        self, module_name, module_version, module_cache_key, registry=None
    ):
        """Loads module class if exists
        Args:
            module_name (str): name of the module to load
            module_version (str): version of the module to load
            module_cache_key (str): cache key of the module after loading
            registry (str): registry name if loading from a registry
        """
        ml_client = (
            current_ml_client()
            if registry is None
            else get_registry_ml_client(registry_name=registry)
        )
        module_version = self.solve_module_version(
            module_name, module_version, client=ml_client
        )

        # TODO(1989862): change when component support get default version
        if module_version is not None:
            loaded_module_class = ml_client.components.get(
                name=module_name,
                version=module_version,
            )
        else:
            log.info(
                f"No version specified for {module_name}, trying to load with 'latest' label."
            )
            loaded_module_class = ml_client.components.get(
                name=module_name,
                label="latest",
            )

        self.put_in_cache(module_cache_key, loaded_module_class)
        return loaded_module_class

    def solve_module_version(self, module_name, module_version, client: MLClient):
        if module_version is None:
            return module_version

        try:
            module_version_PEP440 = Version(module_version)
            if str(module_version_PEP440) != module_version:
                log.warning(
                    "We suggest adopting PEP440 versioning for your component {module_name}!"
                )

        except InvalidVersion as e:
            log.info(f"{module_version} is a version constraint. Try to solve it...")

            spec = SpecifierSet(module_version)
            components = client.components.list(name=module_name)

            versions = []
            for component in components:
                version = component.version
                version_PEP440 = Version(version)
                if str(version_PEP440) != version:
                    log.warning(
                        f"Version {version} does not follow PEP440 versioning, skipping ..."
                    )
                else:
                    versions.append(version_PEP440)

            compatible_versions = list(spec.filter(versions))
            if compatible_versions:
                module_version = max(compatible_versions)
                log.info(f"Solved version for {module_name} is {module_version}.")

            else:
                raise ValueError(
                    f"No version exists for the constraint {module_version}. Existing versions: {versions}"
                )

        return str(module_version)
