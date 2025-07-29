# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
APIs for federated learning.
"""
from shrike.pipeline.pipeline_helper import AMLPipelineHelper
from shrike.pipeline.module_helper import module_reference
from shrike._core import experimental
from coolname import generate_slug
from dataclasses import dataclass
from typing import List, Optional, Union
from azure.ml.component import dsl
from azure.ml.component.pipeline import Pipeline
from azure.ml.component.component import Component, Output
from azure.ml.component._pipeline_parameters import PipelineParameter
import logging
from omegaconf import OmegaConf, open_dict, DictConfig
from pathlib import Path
from typing import Callable, Dict
import collections.abc
from functools import lru_cache

log = logging.getLogger(__name__)

EXPERIMENTAL_WARNING_MSG = (
    "Federated APIs are experimental and could change at any time."
)


def dataset_name_to_reference(
    component_instance: Component, dataset_names: list
) -> Dict[str, Output]:
    res = {}
    if not dataset_names:
        return res
    for dataset in dataset_names:
        res[dataset] = component_instance.outputs[dataset]
    return res


@dataclass
class StepOutput:
    """Output object from preprocess/midprocess/postprocess/training step in a federated pipeline."""

    step: Union[Component, Pipeline] = None
    outputs: List[str] = None


class FederatedPipelineBase(AMLPipelineHelper):
    """
    Base class for Federated Learning pipelines.
    """

    def __init__(self, config, module_loader=None):
        super().__init__(config, module_loader=module_loader)

        package_path = Path(__file__).parent / "components"
        fedavg_component = DictConfig(
            module_reference(
                key="fl_fedavg_pytorch",
                name="fl_fedavg_pytorch",
                yaml=str(package_path) + "/fedavg/spec.yaml",
            )
        )
        self.config.modules.manifest.append(fedavg_component)
        self.module_loader.modules_manifest = OmegaConf.merge(
            self.module_loader.modules_manifest, {"fl_fedavg_pytorch": fedavg_component}
        )
        self.cur_fl_iteration: Optional[int] = None
        self.output_prefix = "fl_output_"
        self.orchestrator = self.config.federated_config.silos[
            self.config.federated_config.orchestrator
        ]
        if "datastore" not in self.orchestrator or not self.orchestrator.datastore:
            self.orchestrator.datastore = self._get_uw_datastores(
                location=self.orchestrator.location,
                environment=self.orchestrator.environment,
                dc=False,
            )

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def create_base_name(self) -> str:
        """The training outputs from each silo will be stored at <base_name>/<silo_name> on the central storage.
        By default, it will return a name of 2 word. User can override this method.

        Returns:
            base_name
        """
        rv = "fl-"
        rv += generate_slug(2)
        return rv

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def create_iteration_name(self) -> str:
        """Display name for each iteration's subgraph, containing letters, numbers, and underscores only. The default value is "iteration n"."""
        return f"iteration_{self.cur_fl_iteration}"

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def create_silo_specific_name(self, silo_name) -> str:
        """Display name for a silo's training in iteration n's subgraph, containing letters, numbers, and underscores only. The default value is "silo_<silo_name>__iteration_n"."""
        return f"silo_{silo_name}__iteration_{self.cur_fl_iteration}"

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def create_subgraph_name(self) -> str:
        """Display name for each subgraph"""
        return "Federated Learning Subgraph"

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def preprocess(self, config: DictConfig, **input) -> StepOutput:
        """
        Optional user-defined preprocess step. The outputs will be distributed to each silo's datastore.

        Returns:
            a component/subgraph instance, and a list of output dataset names to be passed to the downstream pipeline.
        """
        pass

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def midprocess(self, config: DictConfig, **input) -> StepOutput:
        """
        User-defined midprocess step which reads outputs from `train` in each silo. The outputs will be distributed to each silo's datastore.
        By default, it calls the built-in FedAvg component (un-signed).

        Returns:
            a component/subgraph instance, and a list of output dataset name to be passed to the downstream pipeline.
        """
        fedavg_component = self.component_load("fl_fedavg_pytorch")
        num_models = len(self.config.federated_config.silos)
        if len(input) != num_models:
            log.error(
                "The input model weights are inconsistent with the number of models."
            )
            raise Exception
        if "agg_weights" in self.config.federated_config.params:
            weights = self.config.federated_config.params.agg_weights
        else:
            weights = ",".join([str(1 / num_models)] * num_models)
        model_name = (
            self.config.federated_config.params.model_name
            if "model_name" in self.config.federated_config.params
            else None
        )
        updated_input = {}
        for k, v in input.items():
            idx = k[k.index("silo") + 4 : k.index("_")]
            updated_input["model_input_dir_" + idx] = v
        fedavg_step = fedavg_component(
            **updated_input,
            num_models=num_models,
            weights=weights,
            model_name=model_name,
        )
        if self.unified_workspace:
            self.apply_smart_runsettings(
                fedavg_step,
                location=self.orchestrator.location,
                environment=self.orchestrator.environment,
            )
        return StepOutput(fedavg_step, ["model_output_dir"])

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def postprocess(self, config: DictConfig, **kwargs) -> StepOutput:
        """
        Optional user-defined postprocess step which reads outputs from the final `midprocess` step and writes to the `compliant_datastore`.

        Returns:
            a component/subgraph instance, and a list of output dataset names.
        """
        pass

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def train(
        self, config: DictConfig, silo: DictConfig, input: Output = None, **kwargs
    ) -> StepOutput:
        """
        User-defined train step happening at each silo. This reads outputs from `preprocess` or `midprocess`, and sends outputs back to the `compliant_datastore`.

        Returns:
            a component/subgraph instance, and a list of output dataset names to be passed to the downstream pipeline.
        """
        pass

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def generate_noise(
        self, config: DictConfig, silo: DictConfig, input: Output = None, **kwargs
    ) -> StepOutput:
        """
        Optional user-defined generate_noise step (required only if users want to use secure aggregation). Each silo would
        generate (N-1) noisy weights, which would be transferred to the corresponding (N-1) remaining silos, separately.

        Returns:
            a component/subgraph instance, and a list of output dataset names to be passed to the downstream pipeline.
        """
        pass

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def anonymize_model_weights(
        self, config: DictConfig, silo: DictConfig, input: Output = None, **kwargs
    ) -> StepOutput:
        """
        Optional user-defined anonymize_model_weights step (required only if users want to use secure aggregation). It will take inputs from
        silo training step and generate_noise step, and generate the outputs that would be transferred to downstream midprocess pipeline for model weights aggregation.

        Returns:
            a component/subgraph instance, and a list of output dataset names to be passed to the downstream pipeline.
        """
        pass

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def outbound_data_transfer(self, input: Output = None, **kwargs) -> StepOutput:
        """
        Optional user-defined data transfer step to move data outside the compliant boundary.
        If subgraph auto-approval template is registered for the workspace, define and consume it here.

        Returns:
            a component/subgraph instance, and a list of output dataset names to be passed to the downstream pipeline.
        """
        raise NotImplementedError

    def _data_transfer(
        self,
        input_list: dict,
        base_name: str,
        destination_datastore: str = None,
        location: str = None,
        environment: str = None,
        via_cosmos: bool = False,
        orchestrator_to_silo: bool = True,
    ) -> dict:
        """Moves data `input_list` to `destination_datastore` with path prefixed by `base_name`."""
        # assume one shared ADF
        dts_name = self.config.federated_config.data_transfer_component
        try:
            data_transfer_component = self.component_load(
                dts_name  # this component is subject to change
            )
            log.info(f"Using {dts_name} as data transfer component.")
        except Exception as e:
            log.error(
                f"Please specify the data transfer component name registered in your workspace in module manifest and `federated_config.data_transfer_component` pipeline yaml."
            )
            raise (e)

        res = {}
        if not input_list:
            return res
        for name, input in input_list.items():
            if via_cosmos:
                log.info("Leveraging cosmos as the intermediate datastore.")

                @dsl.pipeline(
                    display_name=f"Data transfer to {location}-{environment} via cosmos"
                )
                def dts_via_cosmos_function(input):
                    data_in_noncompliant_datastore = None
                    try:
                        data_in_noncompliant_datastore = self.outbound_data_transfer(
                            input
                        )
                    except NotImplementedError:
                        data_transfer_to_cosmos_step = data_transfer_component(
                            source_data=input
                        )
                        self.apply_smart_runsettings(
                            data_transfer_to_cosmos_step,
                            datatransfer=True,
                            datastore_name=self.config.compute.noncompliant_datastore,
                            location=(
                                self.orchestrator.location
                                if orchestrator_to_silo
                                else location
                            ),
                            environment=(
                                self.orchestrator.environment
                                if orchestrator_to_silo
                                else environment
                            ),
                        )
                        data_in_noncompliant_datastore = (
                            data_transfer_to_cosmos_step.outputs.destination_data
                        )
                    data_transfer_from_cosmos_step = data_transfer_component(
                        source_data=data_in_noncompliant_datastore,
                    )
                    data_transfer_from_cosmos_step.outputs.destination_data.configure(
                        path_on_datastore=base_name + "/" + name,
                    )
                    self.apply_smart_runsettings(
                        data_transfer_from_cosmos_step,
                        datatransfer=True,
                        datastore_name=destination_datastore,
                        location=(
                            location
                            if orchestrator_to_silo
                            else self.orchestrator.location
                        ),
                        environment=(
                            environment
                            if orchestrator_to_silo
                            else self.orchestrator.environment
                        ),
                    )
                    return {
                        "output_data": data_transfer_from_cosmos_step.outputs.destination_data
                    }

                dts_via_cosmos = dts_via_cosmos_function(input)
                res[name] = dts_via_cosmos.outputs.output_data
            else:
                data_transfer_step = data_transfer_component(source_data=input)
                data_transfer_step.outputs.destination_data.configure(
                    path_on_datastore=base_name + "/" + name,
                )
                self.apply_smart_runsettings(
                    data_transfer_step,
                    datatransfer=True,
                    datastore_name=destination_datastore,
                    location=(
                        self.orchestrator.location if orchestrator_to_silo else location
                    ),
                    environment=(
                        self.orchestrator.environment
                        if orchestrator_to_silo
                        else environment
                    ),
                )
                res[name] = data_transfer_step.outputs.destination_data
        return res

    def _update_nested_dict_with_non_none_values(self, dict1, dict2):
        """Update dict1 with non-none values in dict2"""
        for k, v in dict2.items():
            if not v:
                continue
            if isinstance(v, collections.abc.Mapping):
                dict1[k] = self._update_nested_dict_with_non_none_values(
                    dict1.get(k, {}), v
                )
            else:
                log.info(f"Setting {k} to {v}.")
                dict1[k] = v
        return dict1

    def _get_user_defined_output_configs(self, component_instance):
        output_configs = {}
        for output_key in component_instance.outputs:
            output_instance = getattr(component_instance.outputs, output_key)
            config = {
                "datastore": output_instance._datastore,
                "mode": output_instance._mode,
                "path_on_compute": output_instance._path_on_compute,
                "path_on_datastore": (
                    output_instance._dataset_output_options.path_on_datastore
                    if output_instance._dataset_output_options
                    else None
                ),
            }
            for k, v in dict(config).items():
                if not v:
                    del config[k]
            if config:
                output_configs[output_instance._name] = config
        return output_configs

    def _apply_user_defined_output_configs(self, outputs, output_configs):
        for output_key in outputs:
            if output_key in output_configs:
                outputs[output_key].configure(**output_configs[output_key])
        return outputs

    def _merge_and_apply_runsettings(
        self, step: Component, prev_output: Dict[str, Output], orchestrator_or_silo
    ):
        log.info(f"Checking user override runsettings for {step.name}...")
        output_configs = self._get_user_defined_output_configs(step)

        runsettings = step.runsettings._get_values()
        self.apply_smart_runsettings(
            step,
            target=orchestrator_or_silo.compute,
            datastore_name=orchestrator_or_silo.datastore,
            location=orchestrator_or_silo.location,
            environment=orchestrator_or_silo.environment,
        )
        merged_runsettings = self._update_nested_dict_with_non_none_values(
            step.runsettings._get_values(), runsettings
        )
        step.runsettings._set_section_by_dict(merged_runsettings)
        prev_output = self._apply_user_defined_output_configs(
            prev_output, output_configs
        )
        unused_outputs = {
            k: step.outputs[k] for k in set(step.outputs) - set(prev_output)
        }
        self._apply_user_defined_output_configs(unused_outputs, output_configs)
        return prev_output

    def _process_at_orchestrator(self, prev: StepOutput) -> dict:
        """Processes outputs at the orchestrator."""
        step = prev.step
        if isinstance(step, Pipeline):
            prev_output = step.outputs
        elif isinstance(step, Component):
            prev_output = dataset_name_to_reference(step, prev.outputs)
            if self.unified_workspace:
                # no auto calling of apply_smart_runsettings
                prev_output = self._merge_and_apply_runsettings(
                    step, prev_output, self.orchestrator
                )
        else:
            raise Exception(
                f"The output of preprocess/midprocess/postprocess step must be a Pipeline object or a Component object. You are using {type(prev.step)}."
            )
        return prev_output

    def _merge_config(self):
        """Merges and simplifies federated_config."""
        # override priority: default_config < customized shared config < per-silo setting
        # everything in customized shared config have equal priority
        federated_config = self.config.federated_config
        if "config_group" not in federated_config or not federated_config.config_group:
            return
        default_config = federated_config.config_group.get("default_config", {})
        for silo_name, silo_config in federated_config.silos.items():
            customized_config = {}
            if "inherit" in silo_config:
                for inherit_config in silo_config["inherit"]:
                    customized_config = OmegaConf.merge(
                        customized_config, federated_config.config_group[inherit_config]
                    )
            log.info(
                f"=== Original config for silo {silo_name}: {self.config.federated_config.silos[silo_name]}"
            )
            with open_dict(default_config):
                merge = OmegaConf.merge(default_config, customized_config)
            log.info(f"=== Shared config {merge}")
            with open_dict(self.config.federated_config.silos[silo_name]):
                self.config.federated_config.silos[silo_name] = OmegaConf.merge(
                    merge, silo_config
                )
                self.config.federated_config.silos[silo_name].pop("inherit", None)
            if "location" not in self.config.federated_config.silos[silo_name]:
                self.config.federated_config.silos[silo_name].location = ""
            if "environment" not in self.config.federated_config.silos[silo_name]:
                self.config.federated_config.silos[silo_name].environment = ""
            log.info(
                f"=== Merged config for silo {silo_name}: {self.config.federated_config.silos[silo_name]}"
            )
        self.orchestrator = self.config.federated_config.silos[
            self.config.federated_config.orchestrator
        ]

    def _check_if_same_source_and_destination_datastore(
        self,
        input,
        destination_datastore=None,
        destination_location=None,
        destination_environment=None,
    ):
        # Check if the input data already lives in the destination datastore.
        # If source = DC datastore, destination = PROD datastore in the same region,
        # this function returns False. This can be improved but might overcomplicate the code.
        source_datastore = (
            input.default_value._datastore
            if isinstance(input, PipelineParameter)
            else input._datastore
        )
        if source_datastore == destination_datastore:
            return True
        elif "uw_config" not in self.config:
            return False
        else:
            for item in self.config.uw_config.datastores:
                if item["name"] == source_datastore:
                    source_location = item["location"]
                    source_environment = item["environment"]
                if destination_datastore and item["name"] == destination_datastore:
                    destination_location = item["location"]
                    destination_environment = item["environment"]
            return (
                destination_location == source_location
                and destination_environment == source_environment
            )

    def _check_if_data_transfer_is_activated_and_process(
        self,
        base_name,
        datastore_name=None,
        location=None,
        environment=None,
        via_cosmos=True,
        orchestrator_to_silo=True,
        **inputs,
    ):
        deactivate_data_transfer = self.config.federated_config.deactivate_data_transfer
        if deactivate_data_transfer:
            log.info("Data transfer is disabled; training outputs will remain in silo.")
            return inputs
        else:
            for input_key, input_value in inputs.items():
                pass
            if self._check_if_same_source_and_destination_datastore(
                input_value, datastore_name, location, environment
            ):
                # TODO: this simplifies the graph by removing redundant DTS. Do we need it?
                log.info("Trying to move data within the silo, skipping..")
                return inputs
            if datastore_name:
                log.info(f"Moving data {inputs.keys()} into {datastore_name}.")
            else:
                log.info(
                    f"Moving data {inputs.keys()} into {environment} in {location}."
                )
            return self._data_transfer(
                input_list=inputs,
                base_name=base_name,
                destination_datastore=datastore_name,
                location=location,
                environment=environment,
                via_cosmos=via_cosmos,
                orchestrator_to_silo=orchestrator_to_silo,
            )

    def _update_configs_in_silo(self, step, compute_target, datastore):
        log.info(
            f"Updating the compute target to {compute_target} and datastore to {datastore} for component {step.name}."
        )
        step.runsettings.configure(
            target=compute_target,
        )
        self._set_all_outputs_to(step, output_mode=None, datastore_name=datastore)

    def _train_in_silo_once(
        self, silo_name: str, silo: DictConfig, cool_name: str, **prev_output
    ) -> dict:
        """Runs the "training" step once at one silo."""
        if prev_output:
            prev_output = self._check_if_data_transfer_is_activated_and_process(
                base_name=cool_name,
                datastore_name=silo.datastore,
                location=silo.location,
                environment=silo.environment,
                orchestrator_to_silo=True,
                **prev_output,
            )
        if len(prev_output) == 1:
            prev_output = {"input": list(prev_output.values())[0]}
        train_step = self.train(self.config, silo=silo, **prev_output)

        step = train_step.step
        if isinstance(step, Pipeline):
            train_output = step.outputs
            step.node_name = self.create_silo_specific_name(silo_name)
            for node in step._expand_pipeline_nodes():
                if not self.unified_workspace:
                    self._update_configs_in_silo(node, silo.compute, silo.datastore)
        elif isinstance(step, Component):
            train_output = dataset_name_to_reference(step, train_step.outputs)
            if self.unified_workspace:
                # no auto calling of apply_smart_runsettings
                log.info(
                    f"Checking user override runsettings for {silo_name} / {step.name}..."
                )
                train_output = self._merge_and_apply_runsettings(
                    step, train_output, silo
                )
            step._node_name = self.create_silo_specific_name(silo_name)
            if not self.unified_workspace:
                self._update_configs_in_silo(step, silo.compute, silo.datastore)
        else:
            raise Exception(
                f"The output of train step must be a Pipeline object or a Component object. You are using {type(step)}"
            )

        # If users are not using secure aggregation, transfer raw model weight from silo to cenral server directly
        if not self.config.federated_config.use_secure_aggregation:
            silo_output = self._check_if_data_transfer_is_activated_and_process(
                base_name=cool_name + "/" + silo_name,
                datastore_name=self.orchestrator.datastore,
                location=silo.location,
                environment=silo.environment,
                orchestrator_to_silo=False,
                **train_output,
            )
        # Otherwise, keep the raw model weights output as input (without data_transfer) to downstream anonymize-weights step
        else:
            silo_output = train_output
        return silo_output

    def _generate_noise_in_silo_once(
        self, silo_name: str, silo: DictConfig, cool_name: str, **prev_output
    ) -> dict:
        """Runs the "generate_noise" step once at one silo."""
        prev_output = self._check_if_data_transfer_is_activated_and_process(
            base_name=cool_name,
            datastore_name=silo.datastore,
            location=silo.location,
            environment=silo.environment,
            orchestrator_to_silo=True,
            **prev_output,
        )
        if len(prev_output) == 1:
            prev_output = {"input": list(prev_output.values())[0]}
        generate_noise_step = self.generate_noise(self.config, silo=silo, **prev_output)

        step = generate_noise_step.step
        if isinstance(step, Pipeline):
            generate_noise_output = step.outputs
        elif isinstance(step, Component):
            generate_noise_output = dataset_name_to_reference(
                step, generate_noise_step.outputs
            )
            if self.unified_workspace:
                # no auto calling of apply_smart_runsettings
                generate_noise_output = self._merge_and_apply_runsettings(
                    step, generate_noise_output, silo
                )

        else:
            raise Exception(
                f"The output of generate_noise step must be a Pipeline object or a Component object. You are using {type(step)}"
            )
        return generate_noise_output

    def _anonymize_model_weights_in_silo_once(
        self,
        silo_name: str,
        silo: DictConfig,
        cool_name: str,
        **anonymize_model_input_for_current_silo,
    ) -> dict:
        """Runs the "anonymize_model_weights" step once at one silo."""
        anonymize_model_weights_step = self.anonymize_model_weights(
            self.config,
            silo=silo,
            **anonymize_model_input_for_current_silo,
        )

        step = anonymize_model_weights_step.step
        if isinstance(step, Pipeline):
            anonymize_model_weights_output = step.outputs
        elif isinstance(step, Component):
            anonymize_model_weights_output = dataset_name_to_reference(
                step, anonymize_model_weights_step.outputs
            )
            if self.unified_workspace:
                # no auto calling of apply_smart_runsettings
                anonymize_model_weights_output = self._merge_and_apply_runsettings(
                    step, anonymize_model_weights_output, silo
                )
        else:
            raise Exception(
                f"The output of anonymize_model_weights step must be a Pipeline object or a Component object. You are using {type(step)}"
            )

        silo_output = self._check_if_data_transfer_is_activated_and_process(
            base_name=cool_name + "/" + silo_name,
            datastore_name=self.orchestrator.datastore,
            location=silo.location,
            environment=silo.environment,
            orchestrator_to_silo=False,
            **anonymize_model_weights_output,
        )
        return silo_output

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def build(self, config: DictConfig):
        """Constructs the federated pipeline. User does not need to modify."""

        @lru_cache()
        @dsl.pipeline(display_name=self.create_subgraph_name())
        def _subpipeline_function(**kwargs):
            cool_name = self.create_base_name()
            midprocess_input = {}
            # if not using secure aggregation
            if (
                not self.config.federated_config.use_secure_aggregation
            ):  # use_secure_aggregation:
                i = 1
                for silo_name, silo in self.config.federated_config.silos.items():
                    train_output = self._train_in_silo_once(
                        silo_name,
                        silo,
                        cool_name,
                        **kwargs,
                    )
                    if len(train_output) == 1:
                        # if there's only one output, forcibly change the name to "<silo_name>_input"
                        midprocess_input[f"silo{i}_input"] = list(
                            train_output.values()
                        )[0]
                    else:
                        for k, v in train_output.items():
                            midprocess_input[f"silo{i}_" + k] = v
                    i += 1
            # if using secure aggregation
            else:
                anonymize_model_input = {}

                # i as index for silo
                i = 1
                for silo_name, silo in self.config.federated_config.silos.items():
                    train_output = self._train_in_silo_once(
                        silo_name,
                        silo,
                        cool_name,
                        **kwargs,
                    )
                    if len(train_output) == 1:
                        anonymize_model_input[f"silo{i}input_from_train_output"] = list(
                            train_output.values()
                        )[0]
                    else:
                        for k, v in train_output.items():
                            anonymize_model_input[
                                f"silo{i}input_from_train_output_" + k
                            ] = v
                    i += 1

                # i as index for source_silo
                i = 1
                for (
                    source_silo_name,
                    source_silo,
                ) in self.config.federated_config.silos.items():
                    # j as index for target_silo
                    j = 1
                    for (
                        target_silo_name,
                        target_silo,
                    ) in self.config.federated_config.silos.items():
                        if i >= j:
                            j += 1
                        elif i < j:
                            generate_noise_output = self._generate_noise_in_silo_once(
                                source_silo_name,
                                source_silo,
                                cool_name,
                                **kwargs,
                            )
                            if len(generate_noise_output) == 1:
                                anonymize_model_input[
                                    f"silo{i}input_secret_{i}_{j}"
                                ] = list(generate_noise_output.values())[0]
                                anonymize_model_input[
                                    f"silo{i}input_secret_{i}_{j}_sign"
                                ] = 1
                            else:
                                for k, v in generate_noise_output.items():
                                    anonymize_model_input[
                                        f"silo{i}input_secret_{i}_{j}_output_" + k
                                    ] = v
                                    anonymize_model_input[
                                        f"silo{i}input_secret_{i}_{j}_output_"
                                        + k
                                        + "_sign"
                                    ] = 1
                            generate_noise_output_transferred_to_target_silo = (
                                self._check_if_data_transfer_is_activated_and_process(
                                    base_name=cool_name + "/" + target_silo_name,
                                    datastore_name=target_silo.datastore,
                                    location=target_silo.location,
                                    environment=target_silo.environment,
                                    orchestrator_to_silo=True,
                                    **generate_noise_output,
                                )
                            )
                            if (
                                len(generate_noise_output_transferred_to_target_silo)
                                == 1
                            ):
                                anonymize_model_input[
                                    f"silo{j}input_secret_{i}_{j}"
                                ] = list(
                                    generate_noise_output_transferred_to_target_silo.values()
                                )[
                                    0
                                ]
                                anonymize_model_input[
                                    f"silo{j}input_secret_{i}_{j}_sign"
                                ] = -1
                            else:
                                for (
                                    k,
                                    v,
                                ) in (
                                    generate_noise_output_transferred_to_target_silo.items()
                                ):
                                    anonymize_model_input[
                                        f"silo{j}input_secret_{i}_{j}_output_" + k
                                    ] = v
                                    anonymize_model_input[
                                        f"silo{j}input_secret_{i}_{j}_output_"
                                        + k
                                        + "_sign"
                                    ] = -1

                            j += 1
                    i += 1

                # i as index for silo
                i = 1
                for silo_name, silo in self.config.federated_config.silos.items():
                    anonymize_model_input_for_current_silo = {}
                    secret_index = 1
                    for k, v in anonymize_model_input.items():
                        if f"silo{i}input_from_train_output" in k:
                            anonymize_model_input_for_current_silo[
                                k.replace(
                                    f"silo{i}input_from_train_output",
                                    f"silo_input_raw_model_weight",
                                )
                            ] = v
                        elif (f"silo{i}input_secret" in k) and (f"_sign" not in k):
                            anonymize_model_input_for_current_silo[
                                f"silo_input_secret_{secret_index}"
                            ] = v
                            if (
                                f"silo_input_secret_{secret_index}_sign"
                                not in anonymize_model_input_for_current_silo
                            ):
                                anonymize_model_input_for_current_silo[
                                    f"silo_input_secret_{secret_index}_sign"
                                ] = int(anonymize_model_input[k + "_sign"])
                            secret_index += 1

                    anonymize_model_output = self._anonymize_model_weights_in_silo_once(
                        silo_name,
                        silo,
                        cool_name,
                        **anonymize_model_input_for_current_silo,
                    )
                    if len(anonymize_model_output) == 1:
                        # if there's only one output, forcibly change the name to "<silo_name>_input"
                        midprocess_input[f"silo{i}_input"] = list(
                            anonymize_model_output.values()
                        )[0]
                    else:
                        for k, v in anonymize_model_output.items():
                            midprocess_input[f"silo{i}_" + k] = v
                    i += 1
            prev = self.midprocess(self.config, **midprocess_input)
            prev_output = self._process_at_orchestrator(prev)
            output = {
                self.output_prefix + name: prev_output[name] for name in prev_output
            }
            return output

        @dsl.pipeline()
        def pipeline_function():
            self._merge_config()
            prev = self.preprocess(self.config)
            if prev:
                prev_output = self._process_at_orchestrator(prev)
            else:
                prev_output = None
            assert isinstance(self.config.federated_config.use_secure_aggregation, bool)

            for iter in range(self.config.federated_config.max_iterations):
                self.cur_fl_iteration = iter
                if prev_output:
                    prev_output = {
                        output_name.replace(self.output_prefix, ""): prev_output[
                            output_name
                        ]
                        for output_name in prev_output.keys()
                    }
                    subpipeline = _subpipeline_function(
                        **prev_output,
                    )
                else:
                    subpipeline = _subpipeline_function()
                subpipeline.node_name = self.create_iteration_name()
                prev_output = subpipeline.outputs

            if len(prev_output) == 1:
                prev_output = {"input": list(prev_output.values())[0]}
            prev = self.postprocess(self.config, **prev_output)
            if prev:
                prev = self._process_at_orchestrator(prev)
            return prev

        return pipeline_function

    def pipeline_instance(self, pipeline_function, config):
        """Creates an instance of the pipeline using arguments. User does not need to modify."""
        pipeline = pipeline_function()
        return pipeline
