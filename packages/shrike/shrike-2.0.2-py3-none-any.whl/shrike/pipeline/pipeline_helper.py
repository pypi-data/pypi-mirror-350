# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Pipeline helper class to create pipelines loading modules from a flexible manifest.
"""
from abc import ABC
import json
import logging
import yaml
from typing import Any, Callable, Dict, List, Optional, Set, Union

from toposort import toposort_flatten
import datetime
import time
from dataclasses import dataclass
from functools import lru_cache, wraps

from shrike.pipeline.pipeline_helper_base import AMLPipelineHelperBase

try:
    from omegaconf import DictConfig, OmegaConf, MISSING
    from flatten_dict import flatten

    from azure.ai.ml import Input
    from azure.ai.ml.entities._builders import BaseNode
    from azure.ai.ml.entities import (
        # Component types
        Spark,
        Parallel,
        Sweep,
        Command,
        # Concepts types
        Component,
        PipelineJob,
        Job,
        PipelineComponent,
        Pipeline,
        BatchEndpoint,
        PipelineComponentBatchDeployment,
        JobSchedule,
        RecurrenceTrigger,
        RecurrencePattern,
        CronTrigger,
    )

    from azure.ai.ml.exceptions import ValidationException, UserErrorException
    from azure.ai.ml._internal.entities import (
        Command as InternalCommand,
        Distributed,
        Parallel as InternalParallel,
        Scope,
        DataTransfer,
        Ae365exepool,
        HDInsight,
        Starlite,
        Hemera,
    )
    from azure.ai.ml.entities._job.sweep.early_termination_policy import (
        BanditPolicy,
        MedianStoppingPolicy,
        TruncationSelectionPolicy,
    )
    from azure.ai.ml.entities._job.pipeline._io import (
        NodeInput,
        NodeOutput,
        InputOutputBase,
    )
    from azure.ai.ml.entities._job.job_resource_configuration import (
        JobResourceConfiguration,
    )
    from azure.ai.ml.entities._job.parallel.retry_settings import RetrySettings
    from azure.ai.ml.entities._job.distribution import DistributionConfiguration
except ImportError as error:
    raise ImportError(
        f"{error.msg}. Please install v2 dependency `pip install azure-ai-ml`."
    )

from shrike import __version__
from shrike.pipeline.aml_connect import (
    azureml_connect,
    current_ml_client,
    get_registry_ml_client,
    MLClientNotInitializedError,
)
from shrike.pipeline.module_helper import AMLModuleLoader
from shrike.pipeline.pipeline_config import (
    default_config_dict,
    HDI_DEFAULT_CONF,
)
from shrike._core import is_eyesoff_helper

log = logging.getLogger(__name__)


@dataclass
class Data:
    datastore_name: str
    path: str


class AMLPipelineHelper(AMLPipelineHelperBase, ABC):
    """Helper class for building v2 pipelines"""

    BUILT_PIPELINE = None  # the hydra run decorator doesn't allow for return, we're using this variable instead (hack)

    def __init__(self, config, module_loader=None):
        """Constructs the pipeline helper.

        Args:
            config (DictConfig): config for this object
            module_loader (AMLModuleLoader): which module loader to (re)use
        """
        if module_loader is None:
            log.info(
                f"Creating instance of AMLModuleLoader for {self.__class__.__name__}"
            )
            module_loader = AMLModuleLoader(config)
        super(AMLPipelineHelper, self).__init__(
            config=config, module_loader=module_loader
        )
        self.__datastores = dict()

    def _get_job_status(self, job):
        return self.ml_client().jobs.get(job.name).status

    def _wait_for_job_completion(self, job):
        return self.ml_client().jobs.stream(job.name)

    ##################################
    ### USER FACING HELPER METHODS ###
    ##################################

    @lru_cache()
    def component_load(self, component_key) -> Callable[..., "Component"]:
        """Loads one component from the manifest"""
        try:
            component_func = self.module_loader.load_module(
                component_key, self.required_modules()
            )
        except ValidationException as e:
            raise RuntimeError(
                e.message
                + f"The type of {component_key} is not supported in v2, need to convert it to v2 format."
            )
        self._check_component_supported(component_func)

        @wraps(component_func)
        def wrapper(*args, **kwargs):
            component_step = component_func(*args, **kwargs)
            log.info(
                f"Now try applying the smart runsettting as component post load operation after component initialize: "
            )
            self.apply_smart_runsettings(component_step)
            log.info(f"Successfully applied the smart runsettting. ")
            return component_step

        return wrapper

    @lru_cache()
    def module_load(self, module_key):
        """Loads one module from the manifest"""
        try:
            module_func = self.module_loader.load_module(
                module_key, self.required_modules()
            )
        except ValidationException as e:
            raise RuntimeError(
                e.message
                + f"The type of {module_key} is not supported in v2, need to convert it to v2 format."
            )
        self._check_component_supported(module_func)

        @wraps(module_func)
        def wrapper(*args, **kwargs):
            module_step = module_func(*args, **kwargs)
            self.apply_smart_runsettings(module_step)
            return module_step

        return wrapper

    @lru_cache()
    def dataset_load(
        self,
        name,
        version="latest",
        datastore=None,
        path_on_datastore=None,
        description=None,
        use_named_asset_uri=True,
        is_v1_single_file_data=False,
    ):
        """Loads a dataset by either id or name. If the workspace does not contain this dataset and path is given, create the dataset.

        Args:
            name (str): name or uuid of dataset to load
            version (str): if loading by name, used to specify version (default "latest")
            datastore (str): datastore for registering the dataset as <name>
            path_on_datastore (str): path for registering the dataset as <name>
            description (str): description of dataset to register
            use_named_asset_uri (bool): if True, use the dataset as a named asset uri
            is_v1_single_file_data (bool): if True, remove trailing slashes from the path
        """
        try:
            dataset = self._dataset_load_by_name_or_id(name, version)
            if use_named_asset_uri:
                # If the dataset is already registered, we can use it directly
                log.info(
                    f"Dataset {name} found in workspace. Using it as a data asset reference."
                )
                return Input(path=f"azureml:{dataset.name}:{dataset.version}")
            if hasattr(dataset, "properties") and "v1_type" in dataset.properties:
                if (
                    dataset.properties["v1_type"].lower() == "file"
                    and is_v1_single_file_data
                ):
                    log.info(
                        f"Dataset {name} is a v1 dataset and treat_v1_file_data is set to True. Forcing it to be a uri_file input."
                    )
                    return Input(path=dataset.path.strip("/"), type="uri_file")
                return Input(path=dataset.path)
            return dataset
        except Exception:
            log.info(
                f"Dataset {name} not found. Try registering from {path_on_datastore} on {datastore}..."
            )
            if not datastore or not path_on_datastore:
                raise RuntimeError(
                    f"Dataset {name} not found and no path or datastore given."
                )
            # No need to create data if it comes from path on datastore, pipeline can directly consume it.
            data = Input(
                path=f"azureml://datastores/{datastore}/paths/{path_on_datastore}"
            )
            return data

    @lru_cache()
    def ml_client(self):
        """Gets the current ml_client"""
        return current_ml_client()

    def connect(self):
        """Connect to the AML workspace using internal config"""
        # Only call azureml_connect if there is not an already a pre-existing workspace
        try:
            return self.ml_client()
        except MLClientNotInitializedError:
            return azureml_connect(
                aml_subscription_id=self.config.aml.subscription_id,
                aml_resource_group=self.config.aml.resource_group,
                aml_workspace_name=self.config.aml.workspace_name,
                aml_auth=self.config.aml.auth,
                aml_tenant=self.config.aml.tenant,
                aml_force=self.config.aml.force,
            )  # NOTE: this also stores aml workspace in internal global variable

    def __get_datastore(self, datastore_name):
        if datastore_name in self.__datastores:
            return self.__datastores[datastore_name]
        datastore = self.ml_client().datastores.get(datastore_name)
        self.__datastores[datastore_name] = datastore
        return datastore

    def set_output_to(
        self,
        module_instance,
        output_name,
        output_mode=None,
        datastore_name=None,
        path_on_datastore=None,
        use_abfss_scheme=False,
        compliant=True,
    ):
        if not datastore_name:
            datastore_name = self._get_datastore_name(
                module_instance,
                compliant,
                self._get_component_name_from_instance(module_instance),
            )
        if not path_on_datastore:
            path_on_datastore = "azureml/${{name}}/outputs/${{output_name}}"

        if not hasattr(module_instance.outputs, output_name):
            raise ValueError(
                f"Output {output_name} not found in {self._get_component_name_from_instance(module_instance)}"
            )

        output_instance = getattr(module_instance.outputs, output_name)
        if not isinstance(output_instance, NodeOutput):
            raise TypeError(
                f"Output {output_name} of {self._get_component_name_from_instance(module_instance)} is not a NodeOutput, but {type(output_instance)}"
            )

        if output_mode is not None:
            output_instance.mode = output_mode

        path_prefix = f"azureml://datastores/{datastore_name}/paths/"
        if use_abfss_scheme:
            datastore = self.__get_datastore(datastore_name)
            path_prefix = f"abfss://{datastore.filesystem}@{datastore.account_name}.dfs.core.windows.net/"
        output_instance.path = path_prefix + path_on_datastore
        log.info(
            f"Configured output {output_name} to use mode {output_mode} and datastore {datastore_name}"
        )

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
        sweep=False,  # can't autodetect that
        synapse="auto",
        **custom_runtime_arguments,
    ):
        """Applies regular settings for a given module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            gpu (bool): is the module using GPU?
            hdi (bool): is the module using HDI?
            windows (bool): is the module using Windows compute?
            parallel (bool): is the module using ParallelRunStep?
            mpi (bool): is the module using Mpi?
            scope (bool): is the component using scope?
            datatransfer (bool): is the component using datatransfer?
            sweep (bool): is the component using sweep?
            synapse (bool): is the component using Synapse?
            custom_runtime_arguments (dict): any additional custom args
        """
        # Verifies if module_name corresponds to module_instance when component's available
        if isinstance(module_instance.component, Component):
            self._check_module_runsettings_consistency(module_name, module_instance)

        # Skips if this is a PipelineComponent
        if str(module_instance.type) in ["PipelineComponent", "pipeline"]:
            log.info(f"Component {module_name} detected as PipelineComponent.")
            return

        # Auto detects runsettings
        if hdi == "auto":
            hdi = str(module_instance.type) == "HDInsightComponent"
            if hdi:
                log.info(f"Module {module_name} detected as HDI: {hdi}")

        if parallel == "auto":
            parallel = str(module_instance.type) in ["ParallelComponent", "parallel"]
            if parallel:
                log.info(f"Module {module_name} detected as PARALLEL: {parallel}")

        if mpi == "auto":
            mpi = str(module_instance.type) == "DistributedComponent"
            if mpi:
                log.info(f"Module {module_name} detected as MPI: {mpi}")

        if scope == "auto":
            scope = str(module_instance.type) == "ScopeComponent"
            if scope:
                log.info(f"Module {module_name} detected as SCOPE: {scope}")

        if sweep == "auto":
            sweep = False
            log.warning(
                "Sweep components cannot be auto-detected. Please set `sweep=True` in `apply_smart_runsettings`."
            )

        if synapse == "auto":
            synapse = (
                str(module_instance.type) == "spark"
                or str(module_instance.type) == "SparkComponent"
            )
            if synapse:
                log.info(f"Module {module_name} detected as spark (Synapse): {synapse}")

        if windows == "auto":
            if (
                str(module_instance.type) == "HDInsightComponent"
                or str(module_instance.type) == "ScopeComponent"
                or str(module_instance.type) == "DataTransferComponent"
                or str(module_instance.type) == "sweep"
            ):
                # HDI/scope/datatransfer/sweep modules might not have that environment object
                windows = False
            else:
                os = getattr(
                    module_instance.component.environment, "os", "Linux"
                ) or getattr(module_instance.component.environment, "os_type", "Linux")
                # to fix AttributeError: 'NoneType' object has no attribute 'lower'
                windows = os and os.lower() == "windows"

                if windows:
                    log.info(f"Module {module_name} detected as WINDOWS: {windows}")

        if datatransfer == "auto":
            datatransfer = str(module_instance.type) == "DataTransferComponent"
            if datatransfer:
                log.info(
                    f"Module {module_name} detected as DATATRANSFER: {datatransfer}"
                )

        if parallel:
            self._apply_parallel_runsettings(
                module_name,
                module_instance,
                windows=windows,
                gpu=gpu,
                **custom_runtime_arguments,
            )
            return

        if sweep:
            self._apply_sweep_runsettings(
                module_name,
                module_instance,
                windows=windows,
                gpu=gpu,
                **custom_runtime_arguments,
            )
            return

        if windows:
            self._apply_windows_runsettings(
                module_name,
                module_instance,
                mpi=mpi,
                **custom_runtime_arguments,
            )
            return

        if hdi:
            self._apply_hdi_runsettings(
                module_name,
                module_instance,
                **custom_runtime_arguments,
            )
            return

        if scope:
            self._apply_scope_runsettings(
                module_name, module_instance, **custom_runtime_arguments
            )
            return

        if datatransfer:
            self._apply_datatransfer_runsettings(
                module_name, module_instance, **custom_runtime_arguments
            )
            return

        if synapse:
            self._apply_synapse_runsettings(
                module_name, module_instance, **custom_runtime_arguments
            )
            return

        self._apply_linux_runsettings(
            module_name,
            module_instance,
            mpi=mpi,
            gpu=gpu,
            **custom_runtime_arguments,
        )

    def apply_smart_runsettings(
        self,
        component_instance,
        gpu=False,  # can't autodetect that
        hdi="auto",
        windows="auto",
        parallel="auto",
        mpi="auto",
        scope="auto",
        datatransfer="auto",
        sweep=False,
        synapse="auto",
        **custom_runtime_arguments,
    ):
        """Applies regular settings for a given component.

        Args:
            component_instance (Component): the AML component we need to add settings to
            gpu (bool): is the component using GPU?
            hdi (bool): is the component using HDI?
            windows (bool): is the component using Windows compute?
            parallel (bool): is the component using ParallelRunStep?
            mpi (bool): is the component using Mpi?
            scope (bool): is the component using scope?
            datatransfer (bool): is the component using datatransfer?
            sweep (bool): is the component using sweep?
            synapse (bool): is the component using Synapse?
            custom_runtime_arguments (dict): any additional custom args
        """
        # infer component_name
        try:
            component_name = self._get_component_name_from_instance(component_instance)
        except Exception as e:
            # seeing error for PipelineComponent: descriptor '__str__' of 'object' object needs an argument
            component_name = self._get_component_name_helper(component_instance)
        self.apply_recommended_runsettings(
            component_name,
            component_instance,
            gpu,
            hdi,
            windows,
            parallel,
            mpi,
            scope,
            datatransfer,
            sweep,
            synapse,
            **custom_runtime_arguments,
        )

    def is_eyesoff(self) -> bool:
        """ "
        Check whether the workspace is eyes-off.
        If it lives in a non-Torus tenant, then eyes-off;
        If in Torus tenant, check whether it is in the allow-list of eyes-on Torus subscriptions.
        """
        ml_client = self.ml_client()
        # sc = SubscriptionClient(ml_client._credential)
        # for t in sc.tenants.list():
        #     pass
        tenant_id = ml_client._tenant_id
        subscription_id = ml_client.subscription_id
        return is_eyesoff_helper(tenant_id, subscription_id)

    ################
    ### MAIN/RUN ###
    ################

    def _build_pipeline(self) -> PipelineJob:
        log.info(f"Building Pipeline [{self.__class__.__name__}]...")
        pipeline_function = self.build(self.config)

        # publishing needs a Pipeline, not PipelineJob
        if self.config.run.publish:
            raise NotImplementedError(
                "Publishing pipeline endpoint is not supported in v2 yet. Please consider publishing the pipeline component instead."
            )
            # _component = self.ml_client().components.create_or_update(pipeline_function)
            # self._publish_to_endpoint(_component)

        if self.config.run.publish_component:
            log.warning(
                "EXPERIMENTAL: publishing a pipeline using sdk v2 in shrike is experimental, do not take prod dependency on this."
            )
            log.info("Publishing pipeline as a component...")
            ml_client = self.ml_client()
            if self.config.run.publish_component_registry:
                ml_client = get_registry_ml_client(
                    self.config.run.publish_component_registry
                )
                log.info(
                    f"Publishing to registry '{self.config.run.publish_component_registry}'"
                )

            registered_component = ml_client.components.create_or_update(
                pipeline_function, version=self.config.run.publish_component_version
            )
            log.info(
                f"Pipeline component registered as '{registered_component.name}' with version '{registered_component.version}'"
            )

        if self.config.run.skip_pipeline_instance:
            log.info("Skipping pipeline instance creation, returning None.")
            return None

        log.info("Creating Pipeline Instance...")
        pipeline = self.pipeline_instance(pipeline_function, self.config)

        if not self.config.run.skip_update_dc and self.is_eyesoff():
            log.info("Overriding compute target if upstream steps use DC...")
            pipeline = self._update_dc_configs(pipeline)

        if not self.config.run.skip_validation:
            log.info("Validating...")
            self.ml_client().jobs.validate(pipeline)

        if self.config.run.display_name:
            pipeline.display_name = self.config.run.display_name
        if self.config.run.experiment_name:
            pipeline.experiment_name = self.config.run.experiment_name
        if self.config.run.regenerate_outputs:
            pipeline.settings.force_rerun = True
        if self.config.run.continue_on_failure:
            pipeline.settings.continue_on_step_failure = True

        if self.config.run.export:
            raise RuntimeError("Export pipeline is not supported in v2 yet.")

        if self.config.run.create_schedule:
            self._create_schedule(pipeline)

        return pipeline

    def _publish_to_endpoint(self, pipeline: Pipeline):
        endpoint_name = self.config.run.endpoint_name or self.config.run.experiment_name
        endpoint_description = (
            self.config.run.endpoint_description
            or self.config.run.experiment_description
        )
        endpoint = BatchEndpoint(name=endpoint_name, description=endpoint_description)
        self.ml_client().batch_endpoints.begin_create_or_update(endpoint)
        log.info(f"Created BatchEndpoint endpoint {endpoint.id}")

        # loop on endpoint.state until it is in "Ready" state or timeout 5 minutes
        log.info("Waiting (timeout=5mins) for endpoint to be Succeeded.")
        timeout = 300
        while timeout > 0:
            endpoint = self.ml_client().batch_endpoints.get(endpoint_name)
            if endpoint.provisioning_state == "Succeeded":
                break
            else:
                log.info(
                    f"Endpoint is not ready yet ({endpoint.provisioning_state}), waiting 1 second..."
                )
            timeout -= 1
            time.sleep(1)

        deployment_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        deployment_name = f"batch-deployment-{deployment_id}"
        deployment = PipelineComponentBatchDeployment(
            name=deployment_name,
            description="EXPERIMENTAL",
            endpoint_name=endpoint.name,
            component=pipeline,
        )

        deployment = self.ml_client().batch_deployments.begin_create_or_update(
            deployment
        )
        log.info(f"Created PipelineComponentBatchDeployment {deployment_name}")

    def _submit_pipeline(self, pipeline: PipelineJob) -> Optional[Job]:
        """Publish and submit the given pipeline.

        Args:
            pipeline: pipeline to be submitted
        """
        if self.config.run.submit:
            pipeline_tags = self._create_pipeline_tags()
            log.info(f"Submitting Experiment... [tags={pipeline_tags}]")
            ml_client = self.ml_client()

            pipeline_job = ml_client.jobs.create_or_update(
                job=pipeline,
                experiment_name=self.config.run.experiment_name,
                description=self.config.run.experiment_description,
                tags=pipeline_tags,
                # compute=self.config.compute.default_compute_target,
                skip_validation=self.config.run.skip_validation,
            )

            return pipeline_job

        else:
            log.info(
                "Exiting now, if you want to submit please override run.submit=True"
            )
            self.__class__.BUILT_PIPELINE = (
                pipeline  # return so we can have some unit tests done
            )
            return

    def _create_schedule(self, pipeline_job: PipelineJob):
        """Create a schedule for the given pipeline.

        Args:
            pipeline_job: pipeline to be scheduled
        """
        if self.config.run.schedule_name is None:
            raise ValueError("Schedule name must be provided.")

        if self.config.schedule_trigger.cron_expression and (
            self.config.schedule_trigger.recurrence_frequency
            or self.config.schedule_trigger.recurrence_interval
        ):
            raise ValueError(
                "When setting up a schedule, both cron_expression and recurrence_frequency/recurrence_interval are provided, please only provide one of them."
            )

        if self.config.schedule_trigger.cron_expression is None and (
            self.config.schedule_trigger.recurrence_frequency is None
            or self.config.schedule_trigger.recurrence_interval is None
        ):
            raise ValueError(
                "When setting up an schedule, either cron_expression or recurrence_frequency and recurrence_interval must be provided."
            )

        if self.config.schedule_trigger.cron_expression:
            schedule_trigger = CronTrigger(
                expression=self.config.schedule_trigger.cron_expression,
                start_time=self.config.schedule_trigger.start_time,
                end_time=self.config.schedule_trigger.end_time,
                time_zone=self.config.schedule_trigger.time_zone,
            )
        else:
            recurrence_pattern = None
            if self.config.schedule_trigger.recurrence_pattern:
                pattern_params = {
                    key: OmegaConf.to_container(value)
                    for (
                        key,
                        value,
                    ) in self.config.schedule_trigger.recurrence_pattern.items()
                    if value is not None
                }
                recurrence_pattern = RecurrencePattern(**pattern_params)

            schedule_trigger = RecurrenceTrigger(
                frequency=self.config.schedule_trigger.recurrence_frequency,
                interval=self.config.schedule_trigger.recurrence_interval,
                schedule=recurrence_pattern,
                start_time=self.config.schedule_trigger.start_time,
                end_time=self.config.schedule_trigger.end_time,
                time_zone=self.config.schedule_trigger.time_zone,
            )

        schedule_tags = self._create_pipeline_tags()
        schedule = JobSchedule(
            name=self.config.run.schedule_name,
            description=self.config.run.schedule_description,
            trigger=schedule_trigger,
            create_job=pipeline_job,
            tags=schedule_tags,
        )

        log.info(
            f"Creating Schedule for PipelineJob... [name={schedule.name}][tags={schedule_tags}][trigger={schedule_trigger}]"
        )
        self.ml_client().schedules.begin_create_or_update(schedule)

    def _get_pipeline_run(self, run_id):
        return self.ml_client().jobs.get(name=run_id)

    def _get_run_url(self, pipeline_run):
        return pipeline_run.studio_url

    def _dataset_load_by_name_or_id(self, name, version):
        """Loads a dataset by either id or name.

        Args:
            name (str): name or uuid of dataset to load
            version (str): if loading by name, used to specify version (default "latest")

        NOTE: in AzureML SDK there are 2 different methods for loading dataset
        one for id, one for name. This method just wraps them up in one."""
        # test if given name is a uuid

        # TODO(1989877): Support get data by id
        # hack here: dpv2 use tag for "latest" instead of version
        if version == "latest":
            log.info(f"Getting a dataset [name={name}] with latest label...")

            return self.ml_client().data.get(name=name, label=version)
        else:
            log.info(f"Getting a dataset [name={name}, version={version}]...")

            return self.ml_client().data.get(name=name, version=version)

    def _create_pipeline_tags(self) -> Dict[str, str]:
        pipeline_tags = self._parse_pipeline_tags()
        pipeline_tags.update({"shrike": __version__})
        pipeline_tags.update(self.repository_info)
        pipeline_tags.update(self._validate_tags(self.extra_tags()))
        return pipeline_tags

    @classmethod
    def _check_node_type(cls, node, supported_types):
        if not isinstance(node, supported_types):
            raise TypeError(
                f"Only {supported_types} is supported, got {type(node)} for node instead."
            )

    @staticmethod
    def _check_component_supported(component: Union[Component, BaseNode]):
        """Check if given component/node is supported in v2."""
        # Some component need to change to v2 format, eg: SweepComponent, SparkComponent

        if component.type == "SweepComponent":
            raise RuntimeError(
                f"{component.name} with type {component.type} is not supported in v2, need to convert it to v2 format."
            )

        supported_legacy_component_types = [
            "CommandComponent",
            "DataTransferComponent",
            "DistributedComponent",
            "HDInsightComponent",
            "ParallelComponent",
            "ScopeComponent",
            "StarliteComponent",
            "PipelineComponent",
            "HemeraComponent",
            "AE365ExePoolComponent",
            "IntellectualPropertyProtectedComponent",
        ]
        # for other v2 types: eg: automl, import, need to check if need to introduce apply_xxx_runsettings for them.
        supported_new_component_types = [
            "command",
            "sweep",
            "parallel",
            "pipeline",
            "spark",
        ]
        supported_component_types = (
            supported_legacy_component_types + supported_new_component_types
        )
        if component.type not in supported_component_types:
            raise RuntimeError(
                f"{component.name} with type {component.type} is not supported currently, "
                f"all supported types: {supported_component_types}"
            )

    def _set_all_inputs_to(self, module_instance, input_mode):
        """Sets all module inputs to a given intput mode"""
        input_names = []
        for a, val in module_instance.inputs.items():
            if isinstance(val, NodeInput):
                if isinstance(val._data, (int, bool, float, str)) or val._data is None:
                    # For primitive input, no need to set mode
                    continue
                elif isinstance(val._data, (Input, InputOutputBase)):
                    # For data input or data binding, set mode
                    input_names.append(a)
                else:
                    # Need to check if input's valid, if valid, need to support set mode.
                    raise RuntimeError(
                        f"Not supported input {a} for {self._get_component_name_from_instance(module_instance)} with value {type(val._data)}"
                    )

        for input_key in input_names:
            input_instance = getattr(module_instance.inputs, input_key)
            input_instance.mode = input_mode
            log.info(f"Configured input {input_key} to use mode {input_mode}")

    def _set_all_outputs_to(
        self, module_instance, output_mode=None, compliant=True, datastore_name=None
    ):
        """Sets all module outputs to a given output mode"""
        output_names = [
            a
            for a, val in module_instance.outputs.items()
            if isinstance(val, NodeOutput)  # and isinstance(val._data, Output)
        ]
        if not datastore_name:
            datastore_name = self._get_datastore_name(
                module_instance,
                compliant,
                self._get_component_name_from_instance(module_instance),
            )
        for output_key in output_names:
            self.set_output_to(
                module_instance,
                output_key,
                output_mode=output_mode,
                datastore_name=datastore_name,
            )

    def _get_process_count_per_node(
        self, process_count_per_node, process_count_per_instance
    ):
        if not process_count_per_instance and process_count_per_node:
            log.warning(
                "`process_count_per_node` is deprecated. Please use `process_count_per_instance`."
            )
            return process_count_per_node
        else:
            return process_count_per_instance

    def _get_parallel_process_count_per_node(self):
        if (
            "parallel_process_count_per_node" in self.config.compute
            and "parallel_process_count_per_instance" not in self.config.compute
        ):
            parallel_process_count_per_instance = (
                self.config.compute.parallel_process_count_per_node
            )
            log.warning(
                "`parallel_process_count_per_node` is deprecated. Please use `parallel_process_count_per_instance` in your compute file."
            )
        else:
            parallel_process_count_per_instance = (
                self.config.compute.parallel_process_count_per_instance
                if "parallel_process_count_per_instance" in self.config.compute
                else None
            )
        return parallel_process_count_per_instance

    def _apply_windows_runsettings(
        self,
        module_name,
        module_instance,
        mpi=False,
        target=None,
        node_count=None,
        process_count_per_node=None,
        process_count_per_instance=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a windows module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            mpi (bool): is job mpi ?
            target (str): force target compute over hydra conf
            node_count (int): force node_count over hydra conf
            process_count_per_node (int): deprecated, please use `process_count_per_instance`
            process_count_per_instance (int): force process_count_per_node over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            custom_runtime_arguments (dict): any additional custom args
        """
        if self.module_loader.is_local(module_name):
            target = (
                target
                if target is not None
                else self.config.compute.windows_cpu_dc_target
            )
        else:
            target = (
                target
                if target is not None
                else self.config.compute.windows_cpu_prod_target
            )

        log.info(
            f"Using windows compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            raise RuntimeError(
                f"Unhandled custom_runtime_arguments: {custom_runtime_arguments}"
            )
        process_count_per_instance = self._get_process_count_per_node(
            process_count_per_node, process_count_per_instance
        )

        module_instance.compute = target
        if mpi:
            node_count = node_count if node_count is not None else 1
            process_count_per_instance = (
                process_count_per_instance
                if process_count_per_instance is not None
                else 1
            )
            log.info(
                f"Using mpi with node_count={node_count} process_count_per_instance={process_count_per_instance}"
            )

            if module_instance.resources is None:
                module_instance.resources = JobResourceConfiguration()
            module_instance.resources.instance_count = node_count
            if module_instance.distribution is None:
                module_instance.distribution = DistributionConfiguration()
            module_instance.distribution.process_count_per_instance = (
                process_count_per_instance
            )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        else:
            self._set_all_inputs_to(
                module_instance, self.config.compute.windows_input_mode
            )

        if output_mode:
            self._set_all_outputs_to(
                module_instance, output_mode, datastore_name=datastore_name
            )
        else:
            self._set_all_outputs_to(
                module_instance,
                self.config.compute.windows_output_mode,
                datastore_name=datastore_name,
            )

    def _apply_hdi_runsettings(
        self,
        module_name,
        module_instance: HDInsight,
        target=None,
        driver_cores=None,
        driver_memory=None,
        executor_memory=None,
        executor_cores=None,
        number_executors=None,
        conf=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a HDI module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            target (str): force target compute over hydra conf
            driver_cores (int): force driver_cores over hydra conf
            driver_memory (str): force driver_memory over hydra conf
            executor_memory (int): force executor_memory over hydra conf
            executor_cores (int): force executor_cores over hydra conf
            number_executors (int): force number_executors over hydra conf
            conf (str): force conf over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            custom_runtime_arguments (dict): any additional custom args
        """

        # check if node type is supported
        self._check_node_type(node=module_instance, supported_types=HDInsight)

        if self.module_loader.is_local(module_name):
            target = target if target is not None else self.config.compute.hdi_dc_target
            if not self.config.compute.hdi_dc_target:
                raise Exception(
                    f"Your HDI component {module_name} is using local version. Please specify hdi_dc_target"
                )
        else:
            target = (
                target if target is not None else self.config.compute.hdi_prod_target
            )
        log.info(
            f"Using HDI compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            raise RuntimeError(
                f"Unsupported custom runtime arguments {custom_runtime_arguments}"
            )

        merged_conf = json.loads(HDI_DEFAULT_CONF)
        new_conf = (
            self.config.compute.hdi_conf if "hdi_conf" in self.config.compute else None
        )
        if conf is not None:
            new_conf = conf
        if new_conf is not None:
            if isinstance(new_conf, str):
                new_conf = json.loads(new_conf)
            elif isinstance(new_conf, DictConfig):
                new_conf = flatten(dict(new_conf), reducer="dot")
            else:
                raise ValueError(
                    "computed.hdi_conf is not a valid json string or a single tested configuration."
                )
            merged_conf.update(new_conf)

        module_instance.compute_name = target

        module_instance.driver_memory = (
            driver_memory
            if driver_memory is not None
            else self.config.compute.hdi_driver_memory
        )
        module_instance.driver_cores = (
            driver_cores
            if driver_cores is not None
            else self.config.compute.hdi_driver_cores
        )
        module_instance.executor_memory = (
            executor_memory
            if executor_memory is not None
            else self.config.compute.hdi_executor_memory
        )
        module_instance.executor_cores = (
            executor_cores
            if executor_cores is not None
            else self.config.compute.hdi_executor_cores
        )
        module_instance.number_executors = (
            number_executors
            if number_executors is not None
            else self.config.compute.hdi_number_executors
        )
        module_instance.conf = merged_conf

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode, datastore_name=datastore_name
        )

    def _apply_synapse_runsettings(
        self,
        module_name,
        module_instance: Spark,
        target=None,
        driver_cores=None,
        driver_memory=None,
        executor_memory=None,
        executor_cores=None,
        number_executors=None,
        conf=None,
        input_mode="direct",
        output_mode="direct",
        datastore_name=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a Synapse component. Shrike will not set default runsettings except for spark_identity.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            target (str): force target compute over hydra conf
            driver_cores (int): force driver_cores over hydra conf
            driver_memory (str): force driver_memory over hydra conf
            executor_memory (int): force executor_memory over hydra conf
            executor_cores (int): force executor_cores over hydra conf
            number_executors (int): force number_executors over hydra conf
            conf (str): force conf over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            custom_runtime_arguments (dict): any additional custom args
        """

        # check if node type is supported
        self._check_node_type(node=module_instance, supported_types=Spark)

        if self.module_loader.is_local(module_name):
            target = (
                target if target is not None else self.config.compute.synapse_dc_target
            )
            if not self.config.compute.synapse_dc_target:
                raise Exception(
                    f"Your Spark (Synapse) component {module_name} is using local version. Please specify synapse_dc_target"
                )
        else:
            target = (
                target
                if target is not None
                else self.config.compute.synapse_prod_target
            )
        log.info(
            f"Using Synapse compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            raise RuntimeError(
                f"Unhandled custom_runtime_arguments: {custom_runtime_arguments}"
            )

        new_conf = (
            self.config.compute.synapse_conf
            if "synapse_conf" in self.config.compute
            else None
        )
        if conf is not None:
            new_conf = conf
        if new_conf is not None:
            if isinstance(new_conf, str):
                new_conf = json.loads(new_conf)
            elif isinstance(new_conf, DictConfig) or isinstance(new_conf, dict):
                new_conf = flatten(dict(new_conf), reducer="dot")
            else:
                raise TypeError(
                    f"compute.synapse_conf of type {type(new_conf)} is not a valid json string or a single tested configuration."
                )
            module_instance.conf = new_conf

        module_instance.compute = target
        module_instance.identity = {"type": "managed_identity"}

        if "synapse_driver_memory" in self.config.compute:
            driver_memory = driver_memory or self.config.compute.synapse_driver_memory
        if driver_memory:
            module_instance.driver_memory = driver_memory
        if "synapse_driver_cores" in self.config.compute:
            driver_cores = driver_cores or self.config.compute.synapse_driver_cores
        if driver_cores:
            module_instance.driver_cores = driver_cores
        if "synapse_executor_memory" in self.config.compute:
            executor_memory = (
                executor_memory or self.config.compute.synapse_executor_memory
            )
        if executor_memory:
            module_instance.executor_memory = executor_memory
        if "synapse_number_executors" in self.config.compute:
            number_executors = (
                number_executors or self.config.compute.synapse_number_executors
            )
        if number_executors:
            module_instance.executor_instances = number_executors
        if "synapse_executor_cores" in self.config.compute:
            executor_cores = (
                executor_cores or self.config.compute.synapse_executor_cores
            )
        if executor_cores:
            module_instance.executor_cores = executor_cores

        self._set_all_inputs_to(module_instance, input_mode=input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode=output_mode, datastore_name=datastore_name
        )

    def _apply_parallel_runsettings(
        self,
        module_name,
        module_instance: Union[InternalParallel, Parallel],
        windows=False,
        gpu=False,
        target=None,
        node_count=None,
        process_count_per_node=None,
        process_count_per_instance=None,
        mini_batch_size=None,
        run_invocation_timeout=None,
        run_max_try=None,
        error_threshold=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a ParallelRunStep linux module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            windows (bool): is the module using Windows compute?
            gpu (bool): is the module using GPU compute?
            target (str): force target compute over hydra conf
            node_count (int): force node_count over hydra conf
            process_count_per_node (int): deprecated, please use `process_count_per_instance`
            process_count_per_instance (int): force process_count_per_node over hydra conf
            mini_batch_size (int): force mini_batch_size over hydra conf
            run_invocation_timeout (int): force run_invocation_timeout over hydra conf
            run_max_try (int): force run_max_try over hydra conf
            error_threshold (int): The number of file failures for the input FileDataset that should be ignored during processing.
                If the error count goes above this value, then the job will be aborted.
                Error threshold is for the entire input and not for individual mini-batches sent to run() method.
                The range is [-1, int.max]. -1 indicates ignoring all failures during processing.
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            custom_runtime_arguments (dict): any additional custom args
        """

        # check if node type is supported
        self._check_node_type(
            node=module_instance, supported_types=(InternalParallel, Parallel)
        )

        if self.module_loader.is_local(module_name):
            if windows:
                if gpu:
                    raise ValueError(
                        "A GPU compute target with Windows OS is not available yet!"
                    )
                else:
                    _target = self.config.compute.windows_cpu_dc_target
            else:
                if gpu:
                    _target = self.config.compute.linux_gpu_dc_target
                else:
                    _target = self.config.compute.linux_cpu_dc_target
        else:
            if windows:
                if gpu:
                    raise ValueError(
                        "A GPU compute target with Windows OS is not available yet!"
                    )
                else:
                    _target = self.config.compute.windows_cpu_prod_target
            else:
                if gpu:
                    _target = self.config.compute.linux_gpu_prod_target
                else:
                    _target = self.config.compute.linux_cpu_prod_target

        target = target if target is not None else _target

        log.info(
            f"Using parallelrunstep compute target {target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            raise RuntimeError(
                f"Unsupported custom runtime arguments {custom_runtime_arguments}"
            )

        module_instance.compute = target

        process_count_per_instance = self._get_process_count_per_node(
            process_count_per_node, process_count_per_instance
        )

        # Some runsettings API is different between InternalParallel and Parallel
        if isinstance(module_instance, InternalParallel):
            module_instance.resources.instance_count = (
                node_count
                if node_count is not None
                else self.config.compute.parallel_node_count
            )
            module_instance.max_concurrency_per_instance = (
                process_count_per_instance
                if process_count_per_instance is not None
                else self._get_parallel_process_count_per_node()
            )
            module_instance.mini_batch_size = str(
                mini_batch_size
                if mini_batch_size is not None
                else self.config.compute.parallel_mini_batch_size
            )

            module_instance.retry_settings.timeout = (
                run_invocation_timeout
                if run_invocation_timeout is not None
                else self.config.compute.parallel_run_invocation_timeout
            )
            module_instance.retry_settings.max_tries = (
                run_max_try
                if run_max_try is not None
                else self.config.compute.parallel_run_max_try
            )
            module_instance.error_threshold = (
                error_threshold
                if error_threshold is not None
                else self.config.compute.parallel_error_threshold
            )
        else:
            module_instance.set_resources(
                instance_count=(
                    node_count
                    if node_count is not None
                    else self.config.compute.parallel_node_count
                )
            )
            module_instance.max_concurrency_per_instance = (
                process_count_per_instance
                if process_count_per_instance is not None
                else self._get_parallel_process_count_per_node()
            )
            module_instance.mini_batch_size = str(
                mini_batch_size
                if mini_batch_size is not None
                else self.config.compute.parallel_mini_batch_size
            )

            if module_instance.retry_settings is None:
                module_instance.retry_settings = RetrySettings()
            module_instance.retry_settings.timeout = (
                run_invocation_timeout
                if run_invocation_timeout is not None
                else self.config.compute.parallel_run_invocation_timeout
            )
            module_instance.retry_settings.max_tries = (
                run_max_try
                if run_max_try is not None
                else self.config.compute.parallel_run_max_try
            )
            module_instance.error_threshold = (
                error_threshold
                if error_threshold is not None
                else self.config.compute.parallel_error_threshold
            )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode, datastore_name=datastore_name
        )

    def _apply_linux_runsettings(
        self,
        module_name,
        module_instance,
        mpi=False,
        gpu=False,
        target=None,
        node_count=None,
        process_count_per_node=None,
        process_count_per_instance=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for linux module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            mpi (bool): is the job mpi?
            gpu (bool): is the job using GPU?
            target (str): force target compute over hydra conf
            node_count (int): force node_count over hydra conf
            process_count_per_node (int): deprecated, please use `process_count_per_instance`
            process_count_per_instance (int): force process_count_per_node over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            custom_runtime_arguments (dict): any additional custom args
        """
        if self.module_loader.is_local(module_name) and gpu:
            target = (
                target
                if target is not None
                else self.config.compute.linux_gpu_dc_target
            )
            log.info(
                f"Using target {target} for local code GPU module {module_name} from pipeline class {self.__class__.__name__}"
            )
        elif not self.module_loader.is_local(module_name) and gpu:
            target = (
                target
                if target is not None
                else self.config.compute.linux_gpu_prod_target
            )
            log.info(
                f"Using target {target} for registered GPU module {module_name} from pipeline class {self.__class__.__name__}"
            )
        elif self.module_loader.is_local(module_name) and not gpu:
            target = (
                target
                if target is not None
                else self.config.compute.linux_cpu_dc_target
            )
            log.info(
                f"Using target {target} for local CPU module {module_name} from pipeline class {self.__class__.__name__}"
            )
        elif not self.module_loader.is_local(module_name) and not gpu:
            target = (
                target
                if target is not None
                else self.config.compute.linux_cpu_prod_target
            )
            log.info(
                f"Using target {target} for registered CPU module {module_name} from pipeline class {self.__class__.__name__}"
            )

        if custom_runtime_arguments:
            raise RuntimeError(
                f"Unhandled custom_runtime_arguments: {custom_runtime_arguments}"
            )

        module_instance.compute = target

        process_count_per_instance = self._get_process_count_per_node(
            process_count_per_node, process_count_per_instance
        )

        if mpi:
            node_count = node_count if node_count is not None else 1
            process_count_per_instance = (
                process_count_per_instance
                if process_count_per_instance is not None
                else 1
            )
            log.info(
                f"Using mpi with node_count={node_count} process_count_per_instance={process_count_per_instance}"
            )
            if module_instance.resources is None:
                module_instance.resources = JobResourceConfiguration()
            module_instance.resources.instance_count = node_count
            if module_instance.distribution is None:
                module_instance.distribution = DistributionConfiguration()
            module_instance.distribution.process_count_per_instance = (
                process_count_per_instance
            )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        else:
            self._set_all_inputs_to(
                module_instance, self.config.compute.linux_input_mode
            )
        if output_mode:
            self._set_all_outputs_to(
                module_instance, output_mode, datastore_name=datastore_name
            )
        else:
            self._set_all_outputs_to(
                module_instance,
                self.config.compute.linux_output_mode,
                datastore_name=datastore_name,
            )

    def _apply_scope_runsettings(
        self,
        module_name,
        module_instance: Scope,
        input_mode=None,
        output_mode=None,
        scope_param=None,
        custom_job_name_suffix=None,
        adla_account_name=None,
        priority=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a scope module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            scope_param (str): Parameters to pass to scope e.g. Nebula parameters, VC allocation parameters etc.
            custom_job_name_suffix (str): Optional parameter defining custom string to append to job name
            adla_account_name (str): The name of the Cosmos-migrated Azure Data Lake Analytics account to submit scope job
            custom_runtime_arguments (dict): any additional custom args
        """
        # check if node type is supported
        self._check_node_type(node=module_instance, supported_types=Scope)

        log.info(
            f"Using scope compute target to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            raise RuntimeError(
                f"Unhandled custom_runtime_arguments: {custom_runtime_arguments}"
            )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(module_instance, output_mode, compliant=False)

        module_instance.adla_account_name = adla_account_name
        module_instance.scope_param = scope_param
        module_instance.custom_job_name_suffix = custom_job_name_suffix
        module_instance.priority = priority

    def _apply_datatransfer_runsettings(
        self,
        module_name,
        module_instance: DataTransfer,
        compliant=True,
        target=None,
        input_mode=None,
        output_mode=None,
        datastore_name=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a HDI module.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            compliant (bool): destination datastore, `compliant_datastore` if True, else `noncompliant_datastore`
            target (str): force target compute over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf
            custom_runtime_arguments (dict): any additional custom args
        """
        # check if node type is supported
        self._check_node_type(node=module_instance, supported_types=DataTransfer)

        log.info(
            f"Using datatransfer compute target {self.config.compute.datatransfer_target} to run {module_name} from pipeline class {self.__class__.__name__}"
        )
        if custom_runtime_arguments:
            raise RuntimeError(
                f"Unhandled custom_runtime_arguments: {custom_runtime_arguments}"
            )

        module_instance.compute = (
            target if target is not None else self.config.compute.datatransfer_target
        )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode, compliant, datastore_name
        )

    def _apply_sweep_runsettings(
        self,
        module_name,
        module_instance: Sweep,
        windows=False,
        gpu=False,
        target=None,
        input_mode=None,
        output_mode=None,
        node_count=None,
        process_count_per_node=None,
        process_count_per_instance=None,
        algorithm=None,
        # primary_metric=None,
        # goal=None,
        policy_type=None,
        evaluation_interval=None,
        delay_evaluation=None,
        slack_factor=None,
        slack_amount=None,
        truncation_percentage=None,
        max_total_trials=None,
        max_concurrent_trials=None,
        timeout_seconds=None,
        timeout_minutes=None,
        datastore_name=None,
        **custom_runtime_arguments,
    ):
        """Applies settings for a sweep component.

        Args:
            module_name (str): name of the module from the module manifest (required_modules() method)
            module_instance (Module): the AML module we need to add settings to
            target (str): force target compute over hydra conf
            input_mode (str): force input_mode over hydra conf
            output_mode (str): force output_mode over hydra conf

            # For below sweep specific parameters configurations, see below doc link for more info:
            # https://componentsdk.azurewebsites.net/components/sweep_component.html#set-runsettings
            algorithm (str): sweep sampling method
            primary_metric (str): the primary metric of the hyperparameter tuning to optimize
            goal (str): whether the primary metric will be maximize or minimize when evaluating the trials
            policy_type (str): sweep early termination policy type
            evaluation_interval (int): frequency of applying the policy
            delay_evaluation (int): delays the first policy evaluation for a specified number of intervals
            slack_factor (float): the slack allowed with respect to the best performing training run, as a ratio
            slack_amount (float): the slack allowed with respect to the best performing training run, as an absolute ampunt. You should only specify either slack_factor or slack_amount, but not both.
            truncation_percentage (int): the percentage of lowest performing runs to terminate at each evaluation interval. An integer value between 1 and 99.
            max_total_trials (int): maximum number of trial runs. Must be an integer between 1 and 1000.
            max_concurrent_trials (int): maximum number of runs that can run concurrently. If not specified, all runs launch in parallel. If specified, must be an integer between 1 and 100.
            timeout_minutes (int): maximum duration, in minutes, of the hyperparameter tuning experiment. Runs after this duration are canceled.

            custom_runtime_arguments (dict): any additional custom args
        """

        # check if node type is supported
        self._check_node_type(node=module_instance, supported_types=Sweep)

        if target is not None:
            target = target
        elif self.module_loader.is_local(module_name):
            if windows:
                if gpu:
                    raise ValueError(
                        "A GPU compute target with Windows OS is not available yet!"
                    )
                else:
                    target = self.config.compute.windows_cpu_dc_target
            else:
                if gpu:
                    target = self.config.compute.linux_gpu_dc_target
                else:
                    target = self.config.compute.linux_cpu_dc_target
        else:
            if windows:
                if gpu:
                    raise ValueError(
                        "A GPU compute target with Windows OS is not available yet!"
                    )
                else:
                    target = self.config.compute.windows_cpu_prod_target
            else:
                if gpu:
                    target = self.config.compute.linux_gpu_prod_target
                else:
                    target = self.config.compute.linux_cpu_prod_target
        log.info(
            f"Using target {target} to run sweep component {module_name} from pipeline class {self.__class__.__name__}"
        )

        module_instance.compute = target

        process_count_per_instance = self._get_process_count_per_node(
            process_count_per_node, process_count_per_instance
        )

        if node_count:
            log.info(
                f"Setting node_count={node_count} and process_count_per_instance={process_count_per_instance} as run settings for sweep component {module_name} from pipeline class {self.__class__.__name__}"
            )

            if module_instance.trial.resources is None:
                module_instance.trial.resources = JobResourceConfiguration()
            module_instance.trial.resources.instance_count = node_count
            if module_instance.trial.distribution is None:
                module_instance.trial.distribution = DistributionConfiguration()
            module_instance.trial.distribution.process_count_per_instance = (
                process_count_per_instance
            )

        if input_mode:
            self._set_all_inputs_to(module_instance, input_mode)
        self._set_all_outputs_to(
            module_instance, output_mode, datastore_name=datastore_name
        )

        if "bandit" in policy_type.lower():
            early_termination_policy = BanditPolicy(
                evaluation_interval=evaluation_interval,
                delay_evaluation=delay_evaluation,
                slack_factor=slack_factor,
                slack_amount=slack_amount,
            )
        if "median" in policy_type.lower():
            early_termination_policy = MedianStoppingPolicy(
                evaluation_interval=evaluation_interval,
                delay_evaluation=delay_evaluation,
            )
        if "trancation" in policy_type.lower():
            early_termination_policy = TruncationSelectionPolicy(
                evaluation_interval=evaluation_interval,
                delay_evaluation=delay_evaluation,
                truncation_percentage=truncation_percentage,
            )
        if timeout_minutes and not timeout_seconds:
            log.warn(
                "Please use timeout_seconds for sweep components, instead of timeout_seconds"
            )
            timeout_seconds = timeout_minutes * 60

        module_instance.sampling_algorithm = algorithm
        # module_instance.objective.primary_metric = primary_metric
        # module_instance.objective.goal = goal
        module_instance.early_termination = early_termination_policy
        module_instance.set_limits(
            timeout=timeout_seconds,
            max_total_trials=max_total_trials,
            max_concurrent_trials=max_concurrent_trials,
        )
        for k, v in custom_runtime_arguments.items():
            setattr(module_instance, k, v)

    def _get_component_name_helper(self, component_instance):
        if isinstance(component_instance, Sweep):
            return component_instance.trial.name
        else:
            return component_instance.component.name

    def _update_dc_configs(
        self, pipeline: PipelineJob, debug: bool = False
    ) -> PipelineJob:
        # collect the known DC targets
        # workaround for missing "throw_on_missing" in currently used omegaconf
        compute_config_as_dict = yaml.safe_load(OmegaConf.to_yaml(self.config.compute))
        dc_targets: Set[str] = {
            target
            for key, target in compute_config_as_dict.items()
            if key.endswith("_dc_target") and target and target != str(MISSING)
        }
        dc_datastore = self.config.compute.dc_datastore
        if not dc_targets:
            # This is kind of pointless because if one local component exists
            # then one of the `apply_*` methods wil fail if no dc target is not
            # specified. And if no local component exists, then there is no
            # point in outputting this. But let's do it anyway:
            log.info("The compute config does not contain any DC targets.")
            return pipeline

        log.info("Overriding compute target if upstream steps use DC...")

        # build and parse the dependency graph
        dependency_graph = _DependencyGraph(dc_targets)

        should_use_dc = dependency_graph.determine_dc_nodes(pipeline)
        log.info(f"Need to configure the following for DC: {sorted(should_use_dc)}")

        target_map: Dict[str, str] = {}
        for prod_target in [
            "hdi_prod_target",
            "linux_cpu_prod_target",
            "linux_gpu_prod_target",
            "windows_cpu_prod_target",
            "synapse_prod_target",
        ]:
            if prod_target not in self.config.compute:
                continue
            target_map[self.config.compute[prod_target]] = self.config.compute.get(
                prod_target.replace("_prod_", "_dc_"), None
            )

        for id in should_use_dc:
            node = dependency_graph.id_2_node[id]
            if str(node.type) == "ScopeComponent":
                # scope component doesn't need to configure compute target
                # output datastore has to be cosmos (ADLSg1), while dc_datastore is ADLSg2
                continue
            compute_property_name = (
                "compute_name" if str(node.type) == "HDInsightComponent" else "compute"
            )
            current_compute_target = getattr(node, compute_property_name)
            if (
                isinstance(current_compute_target, str)
                and current_compute_target in target_map
            ):
                setattr(node, compute_property_name, target_map[current_compute_target])
                log.info(
                    f"Updating compute target for {node.name} to {target_map[current_compute_target]}"
                )
            else:
                log.error(
                    f"Node {node} is using an unknown target: "
                    f"{current_compute_target}. "
                    f"Please move this to DC manually, or re-run "
                    f"this after adding the target to the compute config."
                )
            self._set_all_outputs_to(node, datastore_name=dc_datastore)
            log.info(f"Writing outputs of {node.name} to dc_datastore {dc_datastore}")
        return pipeline


class _DependencyGraph:
    # modified from https://github.com/Azure/DesignerPrivatePreviewFeatures/blob/master/azure-ai-ml/samples/inputs_and_outputs/det_ch_sample/pipeline.ipynb

    def __init__(self, dc_targets):
        self.dc_targets = dc_targets
        self.id_2_node = {}
        self.id_2_dc = {}

    def determine_dc_nodes(self, pipeline):
        """Determine which nodes should use dc."""
        should_use_dc = set()
        graph = self.build_graph(pipeline)
        for node_id in toposort_flatten(graph):
            node = self.id_2_node[node_id]
            if self.should_use_dc(node, graph[node_id]):
                should_use_dc.add(node_id)
        return should_use_dc

    def get_predecessors(self, node) -> List[BaseNode]:
        """Return list of predecessors for current node.

        Note: Only non-control flow nodes in @pipeline are supported.
        Node: For sub-graph node, we will trace back to inner node and return.
        Example:
            @pipeline
            def sub_pipeline():
                inner_node = component_func()
                return inner_node.outputs
            @pipeline
            def root_pipeline():
                pipeline_node = sub_pipeline()
                node1 = component_func(input1=pipeline_node.outputs.output1)
                node2 = component_func(
                    input1=pipeline_node.outputs.output1
                    input2=node1.outputs.output1
                )
                # pipeline_node.self.get_predecessors() will return []
                # node1.self.get_predecessors() will return [inner_node]
                # node2.self.get_predecessors() will return [inner_node, node1]
        """

        # use {id: instance} dict to avoid nodes with component and parameters being duplicated
        predecessors = {}
        for _, input_value in node.inputs.items():
            if not isinstance(input_value, NodeInput):
                continue
            owner = input_value._get_data_owner()
            if owner is not None:
                predecessors[owner._instance_id] = owner
        return list(predecessors.values())

    def expand_pipeline_nodes(self, pipeline: Union[PipelineJob, PipelineComponent]):
        """Expand pipeline nodes to a list of nodes. All sub-graphs will be expanded."""
        nodes = []
        for node in pipeline.jobs.values():
            if isinstance(node, Pipeline):
                pipeline_component = node.component
                if not isinstance(pipeline_component, PipelineComponent):
                    raise RuntimeError(
                        "Pipeline component must be a PipelineComponent object, but got {}".format(
                            type(pipeline_component)
                        )
                    )
                nodes.extend(self.expand_pipeline_nodes(pipeline_component))
            else:
                nodes.append(node)
        return nodes

    def map_to_id(self, item: BaseNode) -> Optional[str]:
        """Maps the given item to an id."""
        if isinstance(item, BaseNode):
            # directly use node instance id
            node_id = item._instance_id
            self.id_2_node[node_id] = item
            return node_id
        raise ValueError(
            f"Please report this. Could not map {item} to dependency graph id."
        )

    def build_graph(self, pipeline):
        """Build a graph to toposort"""
        graph = {}

        nodes = self.expand_pipeline_nodes(pipeline)

        for node in nodes:
            node_id = self.map_to_id(node)
            predecessors = self.get_predecessors(node)
            for predecessor in predecessors:
                predecessor_id = self.map_to_id(predecessor)
                if node_id not in graph:
                    graph[node_id] = set()
                if predecessor_id not in graph:
                    graph[predecessor_id] = set()
                graph[node_id].add(predecessor_id)

        return graph

    def should_use_dc(self, node, predecessors_ids):
        """Return True if a node should use dc."""
        node_id = self.map_to_id(node)
        # If specified dc compute, use dc
        if (
            hasattr(node, "compute")
            and isinstance(node.compute, str)
            and node.compute in self.dc_targets
        ):
            self.id_2_dc[node_id] = True
            return True
        elif (
            hasattr(node, "compute_name")
            and isinstance(node.compute_name, str)
            and node.compute_name in self.dc_targets
        ):
            self.id_2_dc[node_id] = True
            return True
        # Otherwise, determine by its predecessors
        for predecessor_id in predecessors_ids:
            if self.id_2_dc.get(predecessor_id, False):
                self.id_2_dc[node_id] = True
                return True
        self.id_2_dc[node_id] = False
        return False
