# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Pipeline helper class to create pipelines loading modules from a flexible manifest.
"""
import argparse
from abc import ABC, abstractmethod
import os
import sys
import json
import logging
import re
import webbrowser
import shutil
import yaml
import jsonpath_ng
from typing import Callable
from dataclasses import dataclass
from functools import lru_cache

try:
    import hydra
    from hydra.core.config_store import ConfigStore
    from hydra.core.hydra_config import HydraConfig
    from omegaconf import DictConfig, OmegaConf, open_dict

except ImportError as error:
    raise ImportError(
        f"{error.msg}. Please install using `pip install shrike[pipeline]`."
    )

from shrike import __version__
from shrike.pipeline.canary_helper import get_repo_info
from shrike.pipeline.pipeline_config import (
    default_config_dict,
)
from shrike.pipeline.telemetry_utils import TelemetryLogger
from shrike.pipeline.exceptions import ShrikeUserErrorException
from shrike._core import POLYMER_FEED, O365_FEED

log = logging.getLogger(__name__)


@dataclass
class Data:
    datastore_name: str
    path: str


class AMLPipelineHelperBase(ABC):
    """Helper class for building pipelines"""

    BUILT_PIPELINE = None  # the hydra run decorator doesn't allow for return, we're using this variable instead (hack)

    def __init__(self, config, module_loader):
        """Constructs the pipeline helper.

        Args:
            config (DictConfig): config for this object
            module_loader (AMLModuleLoader): which module loader to (re)use
        """
        self.repository_info = {}
        self.config = config
        self.module_loader = module_loader

        self.unified_workspace = (
            "uw_config" in self.config and len(self.config.uw_config.computes) > 0
        )

        if self.unified_workspace:
            self.config.compute = self.config.uw_config
            self.config.run.skip_update_dc = True  # TODO: without this, all outputs will be set to default_datastore (per silo, dts_via_cosmos)

    ######################
    ### CUSTOM METHODS ###
    ######################

    @classmethod
    def get_config_class(cls):
        """Returns a dataclass containing config for this pipeline"""
        pass

    @classmethod
    def required_subgraphs(cls):
        """Dependencies on other subgraphs
        Returns:
            dict[str, AMLPipelineHelper]: dictionary of subgraphs used for building this one.
                keys are whatever string you want for building your graph
                values should be classes inherinting from AMLPipelineHelper.
        """
        return {}

    @classmethod
    def required_modules(cls):
        """Dependencies on modules/components

        Returns:
            dict[str, dict]: manifest
        """
        return {}

    def build(self, config):
        """Builds a pipeline function for this pipeline.

        Args:
            config (DictConfig): configuration object (see get_config_class())

        Returns:
            pipeline_function: the function to create your pipeline
        """
        raise NotImplementedError("You need to implement your build() method.")

    def extra_tags(self):
        """Additional tags to submit with the pipeline

        Returns:
            dict[str, str]: tags
        """
        return {}

    def pipeline_instance(self, pipeline_function, config):
        """Creates an instance of the pipeline using arguments.

        Args:
            pipeline_function (function): the pipeline function obtained from self.build()
            config (DictConfig): configuration object (see get_config_class())

        Returns:
            pipeline: the instance constructed using build() function
        """
        raise NotImplementedError(
            "You need to implement your pipeline_instance() method."
        )

    @abstractmethod
    def _get_job_status(self, job):
        """Gets the job status"""
        pass

    @abstractmethod
    def _wait_for_job_completion(self, job):
        """Waits for the completion of this job"""
        pass

    @abstractmethod
    def _publish_to_endpoint(self, pipeline):
        """Publishes pipeline as endpoint"""
        pass

    def canary(self, args, experiment, pipeline_run):
        """Tests the output of the pipeline"""
        pass

    ##################################
    ### USER FACING HELPER METHODS ###
    ##################################

    @abstractmethod
    @lru_cache()
    def ml_client(self):
        """Gets the current workspace"""
        pass

    @abstractmethod
    @lru_cache()
    def component_load(self, component_key) -> Callable[..., "Component"]:
        """Loads one component from the manifest"""
        pass

    @abstractmethod
    @lru_cache()
    def module_load(self, module_key):
        """Loads one module from the manifest"""
        pass

    @lru_cache()
    def subgraph_load(self, subgraph_key, custom_config=OmegaConf.create()) -> Callable:
        """Loads one subgraph from the manifest
        Args:
            subgraph_key (str): subgraph identifier that is used in the required_subgraphs() method
            custom_config (DictConfig): custom configuration object, this custom object will be
            added to the pipeline config

        """
        subgraph_class = self.required_subgraphs()[subgraph_key]

        subgraph_config = self.config.copy()
        if custom_config:
            with open_dict(subgraph_config):
                for key in custom_config:
                    subgraph_config[key] = custom_config[key]

        log.info(f"Building subgraph [{subgraph_key} as {subgraph_class.__name__}]...")
        # NOTE: below creates subgraph with updated pipeline_config
        subgraph_instance = subgraph_class(
            config=subgraph_config, module_loader=self.module_loader
        )
        # subgraph_instance.setup(self.pipeline_config)
        return subgraph_instance.build(subgraph_config)

    @abstractmethod
    @lru_cache()
    def dataset_load(
        self,
        name,
        version="latest",
        datastore=None,
        path_on_datastore=None,
        description=None,
        is_v1_single_file_data=False,
    ):
        """Loads a dataset by either id or name. If the workspace does not contain this dataset and path is given, create the dataset.

        Args:
            name (str): name or uuid of dataset to load
            version (str): if loading by name, used to specify version (default "latest")
            datastore (str): datastore for registering the dataset as <name>
            path_on_datastore (str): path for registering the dataset as <name>
            description (str): description of dataset to register
            is_v1_single_file_data (bool): set to True if the dataset is a File v1 dataset pointing to a single file
        """
        pass

    @abstractmethod
    def connect(self):
        """Connect to the AML workspace using internal config"""
        pass

    @staticmethod
    def validate_experiment_name(name):
        """
        Check whether the experiment name is valid. It's required that
        experiment names must be between 1 to 250 characters, start with
        letters or numbers. Valid characters are letters, numbers, "_",
        and the "-" character.
        """
        if len(name) < 1 or len(name) > 250:
            raise ValueError("Experiment names must be between 1 to 250 characters!")
        if not re.match("^[a-zA-Z0-9]$", name[0]):
            raise ValueError("Experiment names must start with letters or numbers!")
        if not re.match("^[a-zA-Z0-9_-]*$", name):
            raise ValueError(
                "Valid experiment names must only contain letters, numbers, underscore and dash!"
            )
        return True

    @staticmethod
    def validate_connection_attribute(connection_attribute, connection_attribute_type):
        """
        Function that will verify whether the given connection_attribute (Workspace name, RG name, or Subscription Id) matches the constraints on length, allowed characters, etc...
        """

        # initialize min_length and max_length
        min_length = 0
        max_length = sys.maxsize

        # populate the constraints based on connection_attribute_type
        if connection_attribute_type == "workspace":
            min_length = 3
            max_length = 33
            # from https://docs.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/workspaces?tabs=bicep#workspaces
            connection_attribute_type_constraints = (
                "only alphanumeric characters and hyphens"
            )
            regex_target = "^[a-zA-Z0-9-]*$"
        elif connection_attribute_type == "resource_group":
            # from https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/resource-name-rules#microsoftresources
            connection_attribute_type_constraints = "alphanumeric, underscore, parentheses, hyphen, period (except at end), and Unicode characters that match the allowed characters"
            regex_target = "^[-\w\._\(\)]+[-\w_\(\)]$"
        elif connection_attribute_type == "subscription_id":
            # can't find an official link for this...
            connection_attribute_type_constraints = "V4 GUID"
            # following regex taken from: https://stackoverflow.com/questions/19989481/how-to-determine-if-a-string-is-a-valid-v4-uuid
            regex_target = "^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
        else:
            regex_target = ""
            connection_attribute_type_constraints = ""
            raise ValueError(
                "connection_attribute_type must be one of 'workspace', 'resource_group', or 'subscription_id'"
            )

        # check the length first
        if (len(connection_attribute) < min_length) or (
            len(connection_attribute) > max_length
        ):
            raise ValueError(
                f"{connection_attribute} must be between {min_length} and {max_length} characters."
            )

        # check whether the regex matches
        if not re.match(regex_target, connection_attribute):
            raise ValueError(
                f"Valid {connection_attribute_type} names have the following constraints: {connection_attribute_type_constraints}"
            )

        return True

    @abstractmethod
    def is_eyesoff(self) -> bool:
        """ "
        Check whether the workspace is eyes-off.
        If it lives in a non-Torus tenant, then eyes-off;
        If in Torus tenant, check whether it is in the allow-list of eyes-on Torus subscriptions.
        """
        pass

    #######################
    ### HELPER BACKEND  ###
    #######################

    @classmethod
    def _default_config(cls):
        """Builds the default config for the pipeline class"""
        config_store = ConfigStore.instance()

        config_dict = default_config_dict()
        cls._build_config(config_dict)

        config_store.store(name="default", node=config_dict)
        return OmegaConf.structured(config_dict)

    @classmethod
    def _build_config(cls, config_dict, modules_config=None):
        """Builds the entire configuration object for this graph and all subgraphs."""
        self_config_class = cls.get_config_class()
        if self_config_class:
            config_dict[self_config_class.__name__] = self_config_class

        for subgraph_key, subgraph_class in cls.required_subgraphs().items():
            subgraph_class._build_config(config_dict)

    @abstractmethod
    def _dataset_load_by_name_or_id(self, name, version):
        """Loads a dataset by either id or name.

        Args:
            name (str): name or uuid of dataset to load
            version (str): if loading by name, used to specify version (default "latest")
        """
        pass

    @abstractmethod
    def apply_recommended_runsettings(
        self,
        module_name,
        module_instance,
        gpu=False,  # can't autodetect that
        hdi="auto",
        windows="auto",
        parallel="auto",
        mpi="auto",
        scope="auto",
        datatransfer="auto",
        sweep="auto",
        synapse="auto",
        **custom_runtime_arguments,
    ):
        """Applies regular settings for a given module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            gpu (bool): is the module using GPU?
            hdi (bool): is the module using HDI/Spark?
            windows (bool): is the module using Windows compute?
            parallel (bool): is the module using ParallelRunStep?
            mpi (bool): is the module using Mpi?
            scope (bool): is the component using scope?
            datatransfer (bool): is the component using datatransfer?
            sweep (bool): is the component using sweep?
            synapse (bool): is the component using Synapse?
            custom_runtime_arguments (dict): any additional custom args
        """
        pass

    def _parse_pipeline_tags(self):
        """Parse the tags specified in the pipeline yaml"""
        pipeline_tags = {}
        if self.config.run.tags:
            if isinstance(self.config.run.tags, str):
                try:
                    # json.load the tags string in the config
                    pipeline_tags = json.loads(self.config.run.tags)
                except ValueError:
                    log.warning(
                        f"The pipeline tags {self.config.run.tags} is not a valid json-style string."
                    )
            elif isinstance(self.config.run.tags, DictConfig):
                # NOTE: values for tags need to be str
                for key, value in self.config.run.tags.items():
                    pipeline_tags[key] = str(value)
            else:
                log.warning(
                    f"The pipeline tags {self.config.run.tags} is not a valid DictConfig or json-style string."
                )
        return pipeline_tags

    def _check_if_spec_yaml_override_is_needed(self):
        if self.config.module_loader.use_local == "":
            log.info(
                "All components are using remote copy, so override will not be executed. For components you want submission-time override of images/tags/etc., please specify them in `use_local`."
            )
            return False, None
        if not self.config.tenant_overrides.allow_override:
            log.info(
                "Spec yaml file override is not allowed. If you want to use this feature, please set `tenant_overrides.allow_override` to True in your pipeline yaml."
            )
            return False, None
        cur_tenant = self.config.aml.tenant
        for tenant in self.config.tenant_overrides.mapping.keys():
            if tenant == cur_tenant:
                log.info(
                    f"Your tenant is inconsistent with spec yaml, We will override relevant fields in your spec yaml files based on entry `{tenant}` in your pipeline yaml file."
                )
                return True, self.config.tenant_overrides.mapping[tenant]
            if self.config.run.config_dir:
                config_file_path = os.path.join(
                    self.config.run.config_dir, "aml", tenant + ".yaml"
                )
                log.info(f"config_file_path is {config_file_path}")
                if os.path.exists(config_file_path):
                    with open(config_file_path, "r") as file:
                        config = yaml.safe_load(file)
                    if config["tenant"] == cur_tenant:
                        log.info(
                            f"Your tenant is inconsistent with spec yaml, We will override relevant fields in your spec yaml files based on entry `{config_file_path}` in your pipeline yaml file."
                        )
                        return True, self.config.tenant_overrides.mapping[tenant]
        return False, None

    def _override_spec_yaml(self, spec_mapping):
        module_keys = self.module_loader.modules_manifest
        yaml_to_be_recovered = []
        env_yaml_override_is_needed = (
            spec_mapping.remove_polymer_pkg_idx
            if "remove_polymer_pkg_idx" in spec_mapping
            else False
        )
        for module_key in module_keys:
            if not self.module_loader.is_local(module_key):
                log.info(
                    f"Component {module_key} is using the remote copy. Skipping overrides."
                )
                continue
            log.info(f"Overriding for component: {module_key}.")
            module_entry = self.module_loader.modules_manifest[module_key]
            spec_path = os.path.join(
                self.module_loader.local_steps_folder, module_entry["yaml"]
            )
            (
                old_spec_path,
                old_env_file_path,
                new_env_file_path,
            ) = self._override_single_spec_yaml(
                spec_path, spec_mapping, env_yaml_override_is_needed
            )

            yaml_to_be_recovered.append(
                [old_spec_path, spec_path, old_env_file_path, new_env_file_path]
            )
        return yaml_to_be_recovered

    def _update_value_given_flattened_key(self, nested_dict, dot_key, new_val):
        log.info(f"Updating key {dot_key}")
        split_key = dot_key.split(".")
        res = nested_dict
        path = ""
        for key in split_key[:-1]:
            path += key + "."
            if not isinstance(res, dict) or key not in res:
                raise KeyError(
                    f"Key {dot_key} not in {nested_dict}. It failed at {path}."
                )
            res = res[key]
        if isinstance(res, dict) and split_key[-1] in res:
            res[split_key[-1]] = new_val
            log.info(f"The field {dot_key} has been updated to {new_val} successfully.")
        else:
            raise KeyError(f"Key {dot_key} not in {nested_dict}.")

    def _override_single_spec_yaml(
        self, spec_path, spec_mapping, env_yaml_override_is_needed
    ):
        spec_filename, spec_ext = os.path.splitext(spec_path)
        old_spec_path = (
            spec_filename + ".not_used"
        )  # remove ".yaml" extension to avoid confusion
        shutil.copyfile(
            spec_path, old_spec_path
        )  # need to recover after pipeline submission

        with open(spec_path) as file:
            spec = yaml.safe_load(file)
        for key in spec_mapping:
            match = jsonpath_ng.parse(key).find(spec)
            if match:
                try:
                    log.info(f"Find a matching field to override: {key}.")
                    original_val = match[0].value
                    log.info(
                        f"Original value is {original_val}. Looking for new value now..."
                    )
                    spec_mapping_to_use = spec_mapping[key]
                    if isinstance(original_val, str):
                        log.info(f"The field to be updated is str.")
                        if original_val in spec_mapping_to_use:
                            new_val = spec_mapping_to_use[original_val]
                            log.info(f"The new value is: {new_val}.")
                            self._update_value_given_flattened_key(spec, key, new_val)
                        else:
                            for pattern in spec_mapping_to_use:
                                if re.match(pattern, original_val):
                                    new_val = spec_mapping_to_use[pattern]
                                    log.info(f"The new pattern is: {new_val}.")
                                    self._update_value_given_flattened_key(
                                        spec,
                                        key,
                                        re.sub(pattern, new_val, original_val),
                                    )
                    elif isinstance(original_val, dict):
                        log.info("The field to be updated is dict")
                        for spec_mapping_key in spec_mapping_to_use:
                            self._update_value_given_flattened_key(
                                spec,
                                ".".join([key, spec_mapping_key]),
                                spec_mapping_to_use[spec_mapping_key],
                            )
                    else:
                        log.info(
                            f"Override for key {key} is not supported yet. Please open a [feature request](https://github.com/ai-platform-ml-platform/shrike/issues) if necessary."
                        )
                except KeyError:
                    log.info(f"Key {key} does not in file {spec_path}. Skip overrides.")
        new_env_file_path = None
        old_env_file_path = None
        if env_yaml_override_is_needed:
            spec_dirname = os.path.dirname(spec_path)
            log.info(
                f"Will remove {POLYMER_FEED} and {O365_FEED} from environment.conda."
            )
            try:
                if spec["type"] == "spark":
                    conda_dependencies_file = spec["environment"]["conda_file"]
                else:
                    conda_dependencies_file = spec["environment"]["conda"][
                        "conda_dependencies_file"
                    ]
                log.info("conda_dependencies_file exists.")
                (
                    found_index_url,
                    new_file,
                    new_env_file_path,
                    old_env_file_path,
                ) = self._remove_python_package_feed_if_exists_and_save_new(
                    spec_dirname, conda_dependencies_file, [POLYMER_FEED, O365_FEED]
                )
                if found_index_url:
                    if spec["type"] == "spark":
                        spec["environment"]["conda_file"] = new_file
                    else:
                        spec["environment"]["conda"][
                            "conda_dependencies_file"
                        ] = new_file
            except KeyError:
                # conda_dependencies_file does not exist
                pass
            try:
                if spec["type"] == "spark":
                    conda_dependencies = spec["conda_dependencies"]["dependencies"]
                else:
                    conda_dependencies = spec["environment"]["conda"][
                        "conda_dependencies"
                    ]["dependencies"]
                log.info("conda_dependencies_file exists.")
                for idx, dependency in enumerate(conda_dependencies):
                    if isinstance(dependency, dict) and "pip" in dependency:
                        pip_dependencies = dependency["pip"]
                        if POLYMER_FEED in pip_dependencies:
                            pip_dependencies.remove(POLYMER_FEED)
                        if O365_FEED in pip_dependencies:
                            pip_dependencies.remove(O365_FEED)
                        dependency["pip"] = pip_dependencies
                        conda_dependencies[idx] = dependency
                if spec["type"] == "spark":
                    spec["conda_dependencies"]["dependencies"] = conda_dependencies
                else:
                    spec["environment"]["conda"]["conda_dependencies"][
                        "dependencies"
                    ] = conda_dependencies
            except KeyError:
                # conda_dependencies does not exist
                pass
            try:
                pip_requirements_file = spec["environment"]["conda"][
                    "pip_requirements_file"
                ]
                log.info("pip_requirements_file exists.")
                (
                    found_index_url,
                    new_file,
                    new_env_file_path,
                    old_env_file_path,
                ) = self._remove_python_package_feed_if_exists_and_save_new(
                    spec_dirname, pip_requirements_file, [POLYMER_FEED, O365_FEED]
                )
                if found_index_url:
                    spec["environment"]["conda"]["pip_requirements_file"] = new_file
            except KeyError:
                # pip_requirements_file does not exist
                pass

        with open(spec_path, "w") as file:
            yaml.safe_dump(spec, file)
        return old_spec_path, old_env_file_path, new_env_file_path

    def _remove_python_package_feed_if_exists_and_save_new(
        self, spec_dirname, file, package_feeds
    ):
        found_index_url = False
        new_file = ""
        new_file_path = ""
        old_file_path = ""
        with open(os.path.join(spec_dirname, file), "r") as f:
            lines = f.readlines()
        for line in lines:
            for feed in package_feeds:
                if feed in line:
                    found_index_url = True
                    lines.remove(line)
                    break
        if found_index_url:
            file_name, file_ext = os.path.splitext(file)
            new_file = file_name + "_" + self.config.aml.tenant + file_ext
            new_file_path = os.path.join(spec_dirname, new_file)
            with open(new_file_path, "w") as f:
                f.writelines(lines)
            old_file_path = os.path.join(
                spec_dirname, os.path.splitext(file)[0] + ".not_used"
            )
            shutil.move(os.path.join(spec_dirname, file), old_file_path)
        return found_index_url, new_file, new_file_path, old_file_path

    def _recover_spec_yaml(self, spec_file_pairs, keep_modified_files):
        log.info(
            f"Reverting changes to spec yaml files. Keeping modified spec yaml files: {keep_modified_files}."
        )
        for (
            old_spec_path,
            new_spec_path,
            old_env_file_path,
            new_env_file_path,
        ) in spec_file_pairs:
            # Question: do we want to keep a copy of the modified files?
            if keep_modified_files:
                filename, ext = os.path.splitext(new_spec_path)
                shutil.move(
                    new_spec_path, filename + "_" + self.config.aml.tenant + ext
                )
                if os.path.exists(filename + ".additional_includes"):
                    shutil.copyfile(
                        filename + ".additional_includes",
                        filename
                        + "_"
                        + self.config.aml.tenant
                        + ".additional_includes",
                    )
            else:
                if new_env_file_path:
                    os.remove(new_env_file_path)
            shutil.move(old_spec_path, new_spec_path)
            if old_env_file_path:
                shutil.move(
                    old_env_file_path, os.path.splitext(old_env_file_path)[0] + ".yaml"
                )

    def _recover_tenant_overrides(
        self, override, yaml_to_be_recovered, keep_modified_files
    ):
        if override and yaml_to_be_recovered:
            try:
                self._recover_spec_yaml(yaml_to_be_recovered, keep_modified_files)
            except BaseException as e:
                log.error(f"An error occurred, recovery is not successful: {e}")

    @lru_cache()
    def _get_component_name_from_instance(self, component_instance):
        """
        We need to have this `_get_component_name_from_instance()` to get
        component name for `apply_smart_runsettings()`, and can't simply use
        `component_name = component_instance.name`. Otherwise
        `apply_smart_runsettings()` might work incorrectly for local
        components. See more detailed explanation and examples here:
        https://github.com/ai-platform-ml-platform/shrike/issues/411
        """
        component_manifest_list = self.config.modules.manifest
        component_name = self._get_component_name_helper(component_instance)

        for component_manifest_entry in component_manifest_list:
            try:
                if component_manifest_entry["name"].lower() == component_name.lower():
                    return component_manifest_entry["key"] or component_name
                if "namespace" in component_manifest_entry:
                    component_entry_name = (
                        component_manifest_entry["namespace"]
                        + "://"
                        + component_manifest_entry["name"]
                    )
                    if component_entry_name.lower() == component_name.lower():
                        return component_manifest_entry["key"] or component_name
            except ValueError:
                pass
        raise ValueError(
            f"Could not find component matching {component_name}. Please check your spelling."
        )

    def _check_module_runsettings_consistency(self, module_key, module_instance):
        """Verifies if entry at module_key matches the module instance description"""
        (
            module_manifest_entry,
            _,
            _,
        ) = self.module_loader.get_module_manifest_entry(
            module_key, modules_manifest=self.required_modules()
        )

        if "name" in module_manifest_entry:
            if ("source" in module_manifest_entry) and (module_manifest_entry.source):
                # This indicates that user is using the deprecated 'source' config in their yaml file, since
                # the default value of 'source' config has been override. Throw out warning and ask users to remove it.
                log.warning(
                    "!!IMPORTANT: Key word `source` is deprecated for module artifacts. Please remove it."
                )
            module_instance_name = self._get_component_name_helper(module_instance)

            if module_manifest_entry["name"].lower() == module_instance_name.lower():
                return
            if "namespace" in module_manifest_entry:
                module_entry_name = (
                    module_manifest_entry["namespace"]
                    + "://"
                    + module_manifest_entry["name"]
                )
                if module_entry_name.lower() == module_instance_name.lower():
                    return
            raise Exception(
                f"During build() of graph class {self.__class__.__name__}, call to self.apply_recommended_runsettings() is wrong: key used as first argument ('{module_key}') maps to a module reference {module_manifest_entry} which name is different from the module instance provided as 2nd argument (name={module_instance_name}), did you use the wrong module key as first argument?"
            )

    def _validate_tags(self, tags: dict):
        validated_tags = {}
        if isinstance(tags, dict):
            # NOTE: values for tags need to be str
            for key, value in tags.items():
                if not isinstance(key, str):
                    log.warning(f"The key for pipeline tag {key} is not string")
                else:
                    validated_tags[key] = str(value)
        else:
            log.warning(f"The pipeline tags {tags} value type is not a dict")
        return validated_tags

    ################
    ### MAIN/RUN ###
    ################

    @abstractmethod
    def _build_pipeline(self):
        pass

    @abstractmethod
    def _submit_pipeline(self, pipeline):
        pass

    def build_and_submit_new_pipeline(self):
        """Build the pipeline and submit it."""
        pipeline = self._build_pipeline()
        if pipeline is None:
            if not self.config.run.skip_pipeline_instance:
                raise Exception(
                    "Pipeline is None. Please check your pipeline build function."
                )

            log.info(
                "Exiting now, since skip_pipeline_instance is set to True. If you want to submit, please set it to False."
            )
            return None
        return self._submit_pipeline(pipeline)

    def run(self, pipeline=None) -> None:
        """Run pipeline using arguments.

        Args:
            pipeline: If set to `None`, the pipeline helper will take care of
              building a pipeline via it's `build` functions, otherwise the
              pipeline passed here will be used.
        """
        # set logging level
        if self.config.run.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        elif self.config.run.log_error_only:
            logging.getLogger().setLevel(logging.ERROR)

        # Log the telemetry information in the Azure Application Insights
        try:
            telemetry_logger = TelemetryLogger(
                enable_telemetry=not self.config.run.disable_telemetry
            )
            telemetry_logger.log_trace(
                message=f"shrike.pipeline=={__version__}",
                properties={"custom_dimensions": {"configuration": str(self.config)}},
            )
        except Exception as ex:
            log.debug(
                f"Sending trace log messages to application insight is not successful. The exception message: {ex}"
            )

        # Check whether the experiment name is valid
        self.validate_experiment_name(self.config.run.experiment_name)

        # Check whether the workspace name, resource group name, and subscription id are valid
        self.validate_connection_attribute(
            self.config.aml.workspace_name, "workspace"
        )  # self.config.aml.workspace_name
        self.validate_connection_attribute(
            self.config.aml.resource_group, "resource_group"
        )
        self.validate_connection_attribute(
            self.config.aml.subscription_id, "subscription_id"
        )

        self.repository_info = get_repo_info()
        log.info(f"Running from repository: {self.repository_info}")
        # TODO: log SDK version

        self.connect()

        pipeline_job = None
        if self.config.run.resume:
            if pipeline is not None:
                raise Exception(
                    "Did not expect a custom pipeline instance to be given when resuming a pipeline run ."
                    "Either pass `pipeline=None` or set `self.config.run.resume=False`."
                )
            if not self.config.run.pipeline_run_id:
                raise Exception(
                    "To be able to use --resume you need to provide both --experiment-name and --run-id."
                )

            log.info(f"Resuming Experiment {self.config.run.experiment_name}...")
            # experiment = Experiment(self.ml_client(), self.config.run.experiment_name)
            log.info(f"Resuming PipelineRun {self.config.run.pipeline_run_id}...")
            # pipeline_run is of the class "azureml.pipeline.core.PipelineRun"
            # pipeline_run = PipelineRun(experiment, self.config.run.pipeline_run_id)
            log.error(f"Resuming pipeline run is not supported yet.")
            raise NotImplementedError("Resuming pipeline run is not supported yet.")
        else:
            keep_modified_files, override = False, False
            yaml_to_be_recovered = []

            if self.config.tenant_overrides.allow_override:
                log.info("Check if tenant is consistent with spec yaml")
                override, mapping = self._check_if_spec_yaml_override_is_needed()
                if override:
                    try:
                        tenant = self.config.aml.tenant
                        log.info(
                            f"Performing spec yaml override to adapt to tenant: {tenant}."
                        )
                        yaml_to_be_recovered = self._override_spec_yaml(mapping)
                        keep_modified_files = (
                            self.config.tenant_overrides.keep_modified_files
                        )
                    except BaseException as e:
                        log.error(f"An error occurred, override is not successful: {e}")
                        raise e
            try:
                if pipeline is None:
                    pipeline_job = self.build_and_submit_new_pipeline()
                else:
                    pipeline_job = self._submit_pipeline(pipeline=pipeline)
            except BaseException as e:
                log.error(f"An error {e} occurred during pipeline submission.")
                if override:
                    log.info("Now trying to recover overrides.")
                self._recover_tenant_overrides(override, yaml_to_be_recovered, False)
                raise
            else:
                self._recover_tenant_overrides(
                    override, yaml_to_be_recovered, keep_modified_files
                )

        if not pipeline_job:
            # not submitting code, exit now
            return
        # launch the pipeline execution
        log.info(f"Pipeline Run Id: {pipeline_job.id}")
        log.info(
            f"""
#################################
#################################
#################################

Follow link below to access your pipeline run directly:
-------------------------------------------------------

{self._get_run_url(pipeline_job)}

#################################
#################################
#################################
        """
        )

        if self.config.run.canary:
            log.info(
                "*** CANARY MODE ***\n----------------------------------------------------------"
            )
            self._wait_for_job_completion(pipeline_job)

            # azureml.pipeline.core.PipelineRun.get_status(): ["Running", "Finished", "Failed"]
            # azureml.core.run.get_status(): ["Running", "Completed", "Failed"]
            if self._get_job_status(pipeline_job) in ["Finished", "Completed"]:
                log.info("*** PIPELINE FINISHED, TESTING WITH canary() METHOD ***")
                self.canary(self.config, pipeline_job.experiment, pipeline_job)
                log.info("OK")
                step_runs = pipeline_job.get_steps()
                for step_run in step_runs:
                    pass
                try:
                    datasets = []
                    for output in step_run.get_details()["outputDatasets"]:
                        dataset = output["dataset"]
                        dataset_info = dataset._dataflow._steps[0].arguments._pod[
                            "datastores"
                        ][0]
                        print(f"Output dataset {dataset_info}.")
                        datasets.append(
                            Data(
                                datastore_name=dataset_info["datastoreName"],
                                path=dataset_info["path"],
                            )
                        )
                    return datasets
                except:
                    print("no output")
            elif self._get_job_status(pipeline_job) == "Failed":
                log.info("*** PIPELINE FAILED ***")
                raise Exception("Pipeline failed.")
            else:
                log.info("*** PIPELINE STATUS {} UNKNOWN ***")
                raise Exception("Pipeline status is unknown.")

        else:
            if not self.config.run.silent:
                webbrowser.open(url=self._get_run_url(pipeline_job))

            # This will wait for the completion of the pipeline execution
            # and show the full logs in the meantime
            if self.config.run.resume or self.config.run.wait:
                log.info(
                    "Below are the raw debug logs from your pipeline execution:\n----------------------------------------------------------"
                )
                pipeline_job.wait_for_completion(show_output=True)

    @lru_cache()
    def _get_datastore_name(self, module_instance, compliant, component_name=None):
        if compliant:
            component_name = component_name or self._get_component_name_from_instance(
                module_instance
            )
            if self.module_loader.is_local(component_name):
                datastore_name = self.config.compute.dc_datastore
                if not datastore_name:
                    if self.is_eyesoff():
                        raise ShrikeUserErrorException(
                            "Please specify `dc_datastore` in your compute yaml so that local components can write to it."
                        )
                    else:
                        log.warning(
                            "We recommend specifying `dc_datastore` in your compute yaml so that local components can write to it. Using `compliant_datastore` for now."
                        )
                        datastore_name = self.config.compute.compliant_datastore
            else:
                datastore_name = self.config.compute.compliant_datastore
        else:
            datastore_name = self.config.compute.noncompliant_datastore
        return datastore_name

    @abstractmethod
    def _get_pipeline_run(self, run_id: str):
        pass

    @abstractmethod
    def _get_run_url(self, pipeline_run) -> str:
        pass

    @abstractmethod
    def _set_all_inputs_to(self, module_instance, input_mode):
        pass

    @abstractmethod
    def _set_all_outputs_to(
        self, module_instance, output_mode, compliant=True, datastore_name=None
    ):
        pass

    @abstractmethod
    def _get_component_name_helper(self, component_instance):
        pass

    @classmethod
    def main(cls):
        """Pipeline helper main function, parses arguments and run pipeline."""
        config_dict = cls._default_config()

        @hydra.main(config_name="default")
        def hydra_run(cfg: DictConfig):
            # merge cli config with default config
            cfg = OmegaConf.merge(config_dict, cfg)

            arg_parser = argparse.ArgumentParser()
            arg_parser.add_argument("--config-dir")
            args, _ = arg_parser.parse_known_args()
            cfg.run.config_dir = os.path.join(
                HydraConfig.get().runtime.cwd, args.config_dir
            )

            log.info("*** CONFIGURATION ***")
            log.info(OmegaConf.to_yaml(cfg))

            # create class instance
            main_instance = cls(cfg)

            # run
            main_instance.run()

        hydra_run()

        return cls.BUILT_PIPELINE  # return so we can have some unit tests done
