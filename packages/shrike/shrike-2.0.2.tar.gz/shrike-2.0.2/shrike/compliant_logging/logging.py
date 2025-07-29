# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Utilities around logging data which may or may not contain private content.
"""


from shrike.compliant_logging.exceptions import PublicRuntimeError
from typing import Optional, Iterable
from shrike.compliant_logging.constants import DataCategory
from shrike.compliant_logging.data_conversions import (
    collect_pandas_dataframe,
    collect_spark_dataframe,
    collect_vaex_dataframe,
    is_numpy_array,
    is_pandas_dataframe,
    is_pandas_series,
    is_spark_dataframe,
    is_vaex_dataframe,
    get_numpy_array_info,
    get_pandas_dataframe_info,
    get_pandas_series_info,
    get_spark_dataframe_info,
    get_vaex_dataframe_info,
    numpy_array_to_list,
    pandas_series_to_list,
)
from shrike._core import is_eyesoff_helper
from datetime import datetime
from time import time
from mlflow import active_run, start_run, MlflowClient, ActiveRun
from mlflow.entities import Metric
import logging
import sys
import os
from threading import Lock

_LOCK = Lock()
_PREFIX = None
_SCRUB_MESSAGE = "**Log message scrubbed**"
_SCRUB_LOGGING = False
_ML_FLOW_RUN = None


def set_scrubbed_logging(value: bool) -> None:
    """
    Set the global scrubbed logging functionality settings.

    This method is thread-safe.
    """
    with _LOCK:
        global _SCRUB_LOGGING
        _SCRUB_LOGGING = value


def set_prefix(prefix: str) -> None:
    """
    Set the global prefix to use when logging data.

    This method is thread-safe.
    """
    with _LOCK:
        global _PREFIX
        _PREFIX = prefix


def set_scrub_message(scrub_message: str) -> None:
    """
    Set the global scrub message to use when logging private (non-public) data.

    This method is thread-safe.
    """
    with _LOCK:
        global _SCRUB_MESSAGE
        # Make the passed in value string as additional safety measure
        _SCRUB_MESSAGE = str(scrub_message)


def get_scrubbed_logging() -> bool:
    """
    Obtain the current global scrubbed logging functionality settings.
    """
    return _SCRUB_LOGGING


def get_prefix() -> Optional[str]:
    """
    Obtain the current global prefix to use when logging data.
    """
    return _PREFIX


def get_scrub_message() -> str:
    """
    Obtain the current global scrub message to use when logging private (non-public)
    data.
    """
    return _SCRUB_MESSAGE


def get_or_start_mlflow_run() -> ActiveRun:
    """
    Get the current active run if it exists, otherwise start a new one.

    Returns:
        ActiveRun: The active run
    """
    run = active_run()
    if run is None:
        run = start_run()
    return run


def set_mlflow_run() -> None:
    """
    Set the global mlflow run context.

    This method is thread-safe.
    """
    global _ML_FLOW_RUN

    _ML_FLOW_RUN = get_or_start_mlflow_run()


def get_mlflow_run() -> Optional[ActiveRun]:
    """
    Obtain the current global mlflow run context.
    """
    return _ML_FLOW_RUN


def floating_range(buckets):
    """
    Computes an equal distributed list of bucket thresholds

    Args:
        buckets (int): Number of buckets

    Returns:
        List: List of bucket thresholds of length buckets
    """
    return [x / 100 for x in list(range(0, 100, int(100 / (buckets - 1)))) + [100]]


class CompliantLogger(logging.getLoggerClass()):  # type: ignore
    """
    Subclass of the default logging class with an explicit `category` parameter
    on all logging methods. It will pass an `extra` param with `prefix` key
    (value depending on whether `category` is public or private) to the
    handlers.

    The default value for data `category` is `PRIVATE` for all methods.

    Implementation is inspired by:
    https://github.com/python/cpython/blob/3.8/Lib/logging/__init__.py
    """

    def __init__(self, name: str, use_aml_metrics: bool = False, handlers=None):
        super().__init__(name)  # type: ignore

        if handlers:
            self.handlers = handlers

        self.start_time = datetime.now()
        self.metric_count = 1
        self._figure_count = 1
        # number of iterable items that are logged
        self.max_iter_items = 10

        if use_aml_metrics:
            run = get_mlflow_run()
            if run is None:
                try:
                    set_mlflow_run()
                    self.info(
                        "AML Metrics:" + f"{get_mlflow_run()}",  # type: ignore
                        category=DataCategory.PUBLIC,
                    )
                except Exception:
                    self.warning(
                        "AML writer failed to initialize.", category=DataCategory.PUBLIC
                    )

    def _convert_obj(self, obj, category=DataCategory.PRIVATE):
        """
        Converts the given object into a string type.

        Args:
            obj ([type]): Object to convert

        Returns:
            str: Info String about the object
        """
        # pass through for strings
        if isinstance(obj, str):
            return obj

        # check through different types of objects
        try:
            if is_spark_dataframe(obj):
                return get_spark_dataframe_info(obj)

            if is_vaex_dataframe(obj):
                return get_vaex_dataframe_info(obj)

            if is_pandas_dataframe(obj):
                return get_pandas_dataframe_info(obj)

            if is_pandas_series(obj):
                return get_pandas_series_info(obj)

            if is_numpy_array(obj):
                return get_numpy_array_info(obj)

            if isinstance(obj, Iterable):
                list_str = f"List (Count: {len(obj)})"  # type: ignore
                if category == DataCategory.PUBLIC:
                    list_str += " | "
                    if len(obj) < self.max_iter_items:  # type: ignore
                        list_str += str(obj)
                    else:
                        list_str += (
                            str(obj[: self.max_iter_items]) + "..."  # type: ignore
                        )
                return list_str

            if isinstance(obj, Exception):
                exc_type, exc_obj, exc_tb = sys.exc_info()
                obj_str = str(type(obj))
                if category == DataCategory.PUBLIC:
                    obj_str = str(obj)
                return f"Exception ({str(exc_type)}) for object {obj_str}"

        except Exception as ex:
            return f"Unknown DataType ({obj} > {type(ex)})"

        # default add the type of object
        if category == DataCategory.PUBLIC:
            return f"{type(obj)} | {str(obj)}"
        return str(type(obj))

    def _get_mlflow_run_id(self) -> Optional[str]:
        """
        Obtains the MLFlow Run and log warning messages
        if unable to retrieve MLFlow Run
        """
        run = get_mlflow_run()
        if run is None:
            self.warning(
                "Unable to retrieve MLFlow run info, will print to logs",
                category=DataCategory.PUBLIC,
            )
            return None
        return run.info.run_id

    def _log(
        self,
        level,
        msg,
        args=None,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1,
        items=None,
        category=DataCategory.PRIVATE,
    ):
        if not get_scrubbed_logging() and category == DataCategory.PRIVATE:
            p = ""
        else:
            p = get_prefix()

        if get_scrubbed_logging() and category == DataCategory.PRIVATE:
            msg = get_scrub_message()
            items = None
            stack_info = False
            exc_info = None

        if extra:
            extra.update({"prefix": p})
        else:
            extra = {"prefix": p}

        # update message accordingly to items
        if items is not None:
            if not isinstance(items, list):
                items = [items]
            msg += " | " + " | ".join(
                [self._convert_obj(item, category) for item in items]
            )

        if sys.version_info[1] <= 7:
            super(CompliantLogger, self)._log(
                level=level,
                msg=msg,
                args=args,
                exc_info=exc_info,
                extra=extra,
                stack_info=stack_info,
            )
        else:
            super(CompliantLogger, self)._log(
                level=level,
                msg=msg,
                args=args,
                exc_info=exc_info,
                extra=extra,
                stack_info=stack_info,
                stacklevel=stacklevel,  # type: ignore
            )

    def metric(
        self,
        value,
        step=None,
        name=None,
        category=DataCategory.PRIVATE,
    ):
        """
        Converts most datatypes into a metric and logs them to AML Metric
        for the current MLFlow run (if available) or directly to log

        Note: Private Data will not be sent to metrics!
        Note2: Tables will also be logged as artifacts

        Args:
            value (Any): The value to log
                (can be vaex/pandas/spark dataframe, numpy array, list, dict, int/float)
            step (str | int, optional): Step value used for single value items.
                Defaults to None.
            name (str, optional): Name under which the metric should be logged.
                Defaults to None.
            category (DataCategory, optional): Category of the data
                (logging to AML requires this to be set to PUBLIC explicitly).
                Defaults to DataCategory.PRIVATE.
        """
        # check for name
        if name is None:
            name = f"metric_{self.metric_count}"
            self.metric_count += 1

        # retrieve MLFlow Run
        mlflow_run_id = self._get_mlflow_run_id()

        # check if value provided
        if value is None:
            self.error(
                f"Value provided for metric {name} is None, skipping (step: {step})",
                category=category,
            )
            return

        # check different data-types
        if isinstance(value, (float, int)):
            # log the data
            if mlflow_run_id is not None and category == DataCategory.PUBLIC:
                MlflowClient().log_metric(
                    run_id=mlflow_run_id, key=name, value=value, step=step
                )
            self.info(
                f"NumberMetric  | {name}:{step} | {value}",
                category=category,
            )

            return

        # collect dataframes
        if is_vaex_dataframe(value):
            value = collect_vaex_dataframe(value)
        elif is_spark_dataframe(value):
            value = collect_spark_dataframe(value)
        elif is_pandas_dataframe(value):
            value = collect_pandas_dataframe(value)

        # log dictionary data
        if isinstance(value, dict):
            # check if values are present
            if len(value) == 0:
                self.warning(
                    f"Dictionary Value for Metric {name} is empty. Skipping.",
                    category=category,
                )
                return

            # check the value types of the dict
            type_set = list(set([type(v) for v in value.values()]))

            # check for mixed types
            if len(type_set) > 1:
                pass
            else:
                type_set = type_set[0]

            # check types
            if type_set == list:
                if mlflow_run_id is not None and category == DataCategory.PUBLIC:
                    # Split each list (column) into a separate metric and log it:
                    start_step = step if step is not None else 0
                    metrics = []
                    for column_name, column_values in value.items():
                        non_numeric_type = any(
                            [not isinstance(v, (int, float)) for v in column_values]
                        )
                        if non_numeric_type:
                            self.warning(
                                f"Column {column_name} of table {name} contains "
                                f"non-numeric types. Skipping.",
                                category=category,
                            )
                            continue

                        metrics.extend(
                            [
                                Metric(
                                    key=f"{name}.{column_name}",
                                    value=step_value,
                                    timestamp=int(time() * 1000),
                                    step=metric_step,
                                )
                                for (metric_step, step_value) in enumerate(
                                    column_values, start=start_step
                                )
                            ]
                        )
                    MlflowClient().log_batch(run_id=mlflow_run_id, metrics=metrics)

                    # Also log the table as an artifact file
                    artifact_file = f"tables/{name}.json"
                    self.info(
                        f"Logging table {name} as artifact {artifact_file}",
                        category=category,
                    )
                    MlflowClient().log_table(
                        run_id=mlflow_run_id, data=value, artifact_file=artifact_file
                    )
                # log the matrix manually
                col_names = " | ".join(
                    [f"{('' if col is None else col):15}" for col in value.keys()]
                )
                header = f"TableMetric     | Index | {col_names} |"
                self.info(f"TableMetric     | {name}", category=category)
                self.info(header, category=category)
                self.info("-" * len(header), category=category)

                # generate the rows
                max_rows = max([len(value[col]) for col in value])
                for i in range(max_rows):
                    row_str = f"TableMetric     | {i:05}"
                    for key in value:
                        col = value[key]
                        col = col[i] if i < len(col) and col[i] is not None else ""
                        row_str += f" | {str(col):15}"
                    self.info(row_str, category=category)
            elif type_set in [int, float]:
                for key, val in value.items():
                    key = name + "/" + key
                    self.metric(val, step, key, category)
            else:
                self.warning(
                    (
                        "The provided dictionary for metric"
                        f" {name} appears to be unstructured!"
                    ),
                    category=category,
                )

            return

        # collect list wise datatypes
        if is_numpy_array(value):
            value = numpy_array_to_list(value)
        if is_pandas_series(value):
            value = pandas_series_to_list(value)

        # log list data
        if isinstance(value, (list, tuple)):
            value = list(value)
            non_numeric_type = any([not isinstance(v, (int, float)) for v in value])
            if non_numeric_type:
                self.warning(
                    f"List Value for Metric {name} contains non-numeric types. "
                    f"Skipping.",
                    category=category,
                )
                return

            # check if values are present
            if len(value) == 0:
                self.warning(
                    f"List Value for Metric {name} is empty. Skipping.",
                    category=category,
                )
                return

            # log data to run context
            if mlflow_run_id is not None and category == DataCategory.PUBLIC:
                start_step = step if step is not None else 0
                metrics = [
                    Metric(
                        key=name,
                        value=val,
                        timestamp=int(time() * 1000),
                        step=metric_step,
                    )
                    for (metric_step, val) in enumerate(value, start=start_step)
                ]
                MlflowClient().log_batch(run_id=mlflow_run_id, metrics=metrics)
            self.info(f"ListMetric      | {name} | {value}", category=category)

            return

        self.warning(
            f"Value {value} of the provided metric {name} has an unknown type",
            category=category,
        )

    def metric_value(self, name, value, step=None, category=DataCategory.PRIVATE):
        """
        Equivalent to the `Run.log` function.
        Logs a single value to a metric
        Note that this is only possible for public data when MLFlow run is available

        Note: Private Data will not be sent to metrics!

        Args:
            name (str): name of the metric
            value (Any): value to log
            step (int, optional): Step of the current metric. Defaults to None.
            category (DataCategory, optional): Data category to make sure no data leaks.
                Defaults to DataCategory.PRIVATE.
        """
        self.metric(value, step, name, category=category)

    def artifact_image(
        self,
        plot,
        name=None,
        category=DataCategory.PRIVATE,
    ):
        """
        Logs an image to the AML artifacts.
        Note that this is only possible for public data when MLFlow run is available

        Note: Private Data will not be sent to metrics!

        Args:
            plot (pyplot.Plot): The plot that should be logged
            name (str, optional): Name of the image. Defaults to None.
            category (DataCategory, optional): Category under which this image is logged
                Defaults to DataCategory.PRIVATE.
        """
        # retrieve the run context
        mlflow_run_id = self._get_mlflow_run_id()

        # check if parameters are correct
        if category != DataCategory.PUBLIC:
            self.warning(
                f"Unable to log image metric {name} as private, skipping.",
                category=DataCategory.PUBLIC,
            )
            return
        elif mlflow_run_id is None:
            self.warning(
                f"Unable to log image metric {name} without MLFlow run id, skipping.",
                category=category,
            )
            return

        # check for name
        if name is None:
            name = f"figure_{self._figure_count}"
            self._figure_count += 1

        # log the image
        MlflowClient().log_figure(
            run_id=mlflow_run_id, figure=plot.gcf(), artifact_file=f"figures/{name}.png"
        )

    def metric_list(self, name, value, category=DataCategory.PRIVATE):
        """
        Equivalent to the `Run.log_list`.
        Logs a list of values for a single metric.

        Note: Private Data will not be sent to metrics!

        Args:
            value (list): List values to log
            name (str, optional): Name of the metric. Defaults to None.
            category (DataCategory, optional): DataCategory to log the data as.
                Defaults to DataCategory.PRIVATE.
        """
        self.metric(value, name=name, category=category)

    def _compute_truth_matrix(self, predict, target, class_id, thresholds):
        """
        Computes the truth matrix for the given class in a one-vs-rest fashion.

        Args:
            predict (pd.Series): Series of probability values for the target class
            target (pd.Series): Series of target classes
            class_id (int): id of the current class
            thresholds (list): List of thresholds of length P to be used for the
                computation

        Returns:
            Matrix: A truth matrix in format [P, 4] that contains tp, fp, tn, fn for
                each of the thresholds
        """
        cl_table = []
        for threshold in thresholds:
            cl_res = [
                (predict >= threshold) & (target == class_id),
                (predict >= threshold) & (target != class_id),
                (predict < threshold) & (target != class_id),
                (predict < threshold) & (target == class_id),
            ]
            cl_table.append([x.sum() for x in cl_res])
        return cl_table

    def artifact_accuracy_table(
        self,
        name,
        value,
        col_predict=None,
        col_target=None,
        probability_thresholds=5,
        percentile_thresholds=None,
        class_labels=None,
        category=DataCategory.PRIVATE,
    ):
        """
        Equivalent of the `Run.log_accuracy_table` function.
        Logs the data for an accuracy table to the artifacts.

        In the dataframe case, the `col_predict` value has to contain the prediction
        probabilities for the **target** class!

        Note: Private Data will not be sent to artifacts!

        Args:
            value (dict | table): Either dictionary in AML defined format
                or table that provides accuracy values.
            name (str, optional): Name of the metric. Defaults to None.
            col_predict (str | int, optional): Name or ID of the predicted probabilities
                for the target class. This is only required if DataFrame is passed.
                Defaults to None.
            col_target (str | int, optional): Name or id of the target value column.
                This is only required if DataFrame is passed. Defaults to None.
            probability_thresholds (list | int, optional): Either a list of thresholds
                or a number of evenly spaced threshold points. Defaults to 5.
            percentile_thresholds (list | int, optional): Either a list of thresholds
                or a number of evenly spaced threshold points. Defaults to
                [0.1, 0.25, 0.5, 0.75, 0.9].
            class_labels (list, optional): List of class labels. Defaults to None.
            category (DataCategory, optional): Classification of the data category.
                Defaults to DataCategory.PRIVATE.
        """
        # retrieve mlflow run id
        mlflow_run_id = self._get_mlflow_run_id()

        if percentile_thresholds is None:
            percentile_thresholds = [0.1, 0.25, 0.5, 0.75, 0.9]

        # convert data if not already pre-computed
        if not isinstance(value, dict) or "schema_type" not in value:
            # check the data
            if is_vaex_dataframe(value):
                value = collect_vaex_dataframe(value)
            if is_spark_dataframe(value):
                value = collect_spark_dataframe(value)
            if is_pandas_dataframe(value):
                value = collect_pandas_dataframe(value)

            # check if datatype matches
            if not isinstance(value, dict):
                raise PublicRuntimeError("Unknown value-type passed to accuracy_table!")

            # convert the data
            try:
                import pandas as pd

                # create the dataframe
                df = pd.DataFrame.from_dict(value)

                # column checks
                if None in [col_predict, col_target]:
                    raise PublicRuntimeError(
                        "If table is passed to accuracy_table it requires all "
                        + "columns to be present!"
                    )

                # check the class list (sort to make sure it is aligned)
                class_list = list(df[col_target].unique())
                class_list.sort()
                if class_labels is None:
                    class_labels = class_list

                # compute ranges
                if isinstance(probability_thresholds, int):
                    probability_thresholds = floating_range(probability_thresholds)
                if isinstance(percentile_thresholds, int):
                    percentile_thresholds = floating_range(percentile_thresholds)

                # compute one-vs-rest labels for the class
                prob_tables = []
                perc_tables = []
                for cl in class_list:
                    # compute the thresholds
                    prob_tables.append(
                        self._compute_truth_matrix(
                            df[col_predict], df[col_target], cl, probability_thresholds
                        )
                    )

                    # compute per class percentiles
                    cl_proba = (df[col_predict] * (df[col_target] == cl)) + (
                        (1 - df[col_predict]) * (df[col_target] != cl)
                    )
                    cl_percentile = list(cl_proba.quantile(percentile_thresholds))
                    perc_tables.append(
                        self._compute_truth_matrix(
                            df[col_predict], df[col_target], cl, cl_percentile
                        )
                    )

                # generate data
                value = {
                    "schema_type": "accuracy_table",
                    "schema_version": "1.0.1",
                    "data": {
                        "probability_tables": prob_tables,
                        "percentile_tables": perc_tables,
                        "probability_thresholds": probability_thresholds,
                        "percentile_thresholds": percentile_thresholds,
                        "class_labels": class_labels,
                    },
                }
            except Exception:
                raise PublicRuntimeError(
                    "Unable to import pandas and parse the given data table! "
                    + "Make sure that libraries are available and "
                    + "correct data is passed."
                )

        # log the data
        if category == DataCategory.PUBLIC and mlflow_run_id is not None:
            artifact_file = f"tables/{name}.json"
            self.info(
                f"Logging Accuracy Table as artifact '{artifact_file}'",
                category=category,
            )
            MlflowClient().log_dict(
                run_id=mlflow_run_id, dictionary=value, artifact_file=artifact_file
            )
        else:
            self.warning(
                "Logging Accuracy Tables to text is not yet implemented",
                category=DataCategory.PUBLIC,
            )

    def artifact_confusion_matrix(
        self,
        name,
        value,
        idx_true=None,
        idx_pred=None,
        labels=None,
        category=DataCategory.PRIVATE,
    ):
        """
        Equivalent of the `Run.log_confusion_matrix` function.
        Logs or generates a confusion matrix to the AML artifacts logs.

        Note: Private Data will not be sent to artifacts!

        Args:
            value (dict | DataFrame): Data to be used for the confusion_matrix
            idx_true (int | str, optional): Name or id of the target column.
                Defaults to None.
            idx_pred (int | str, optional): Name or id of the prediction column.
                Defaults to None.
            labels (list, optional): List of labels used for the rows. Defaults to None.
            name (str, optional): Name of the metric. Defaults to None.
            category (DataCategory, optional): Classification of the data.
                Defaults to DataCategory.PRIVATE.

        Raises:
            PublicRuntimeError: [description]
            PublicRuntimeError: [description]
        """
        # retrieve mlflow run id
        mlflow_run_id = self._get_mlflow_run_id()

        # convert data if not already pre-computed
        if (
            not isinstance(value, dict)
            or "schema_type" not in value
            or "schema_version" not in value
        ):
            # check the data
            if is_vaex_dataframe(value):
                value = collect_vaex_dataframe(value)
            if is_spark_dataframe(value):
                value = collect_spark_dataframe(value)
            if is_pandas_dataframe(value):
                value = collect_pandas_dataframe(value)

            # check if datatype matches
            if not isinstance(value, dict):
                raise PublicRuntimeError(
                    "Unknown value-type passed to Run.log_confusion_matrix!"
                )

            # convert the data
            try:
                # try to import libs
                import numpy as np
                from sklearn.metrics import confusion_matrix

                # update row names
                if isinstance(idx_true, str):
                    idx_true = list(value.keys()).index(idx_true)
                if isinstance(idx_pred, str):
                    idx_pred = list(value.keys()).index(idx_pred)

                # retrieve left right
                val_true, val_pred = None, None
                value = np.array(list(value.values()))
                val_true = value[idx_true]
                val_pred = value[idx_pred]

                # compute matrix
                mat = confusion_matrix(val_true, val_pred)

                # generate labels as distinct
                if labels is None:
                    labels = np.unique(val_true)

                # generate the dict
                value = {
                    "schema_type": "confusion_matrix",
                    "schema_version": "1.0.0",
                    "data": {"class_labels": labels, "matrix": mat},
                }
            except Exception:
                raise PublicRuntimeError(
                    "Unable to import numpy & scikit and parse the given data table! "
                    + "Make sure that libraries are available and correct "
                    + "data is passed."
                )

        # log the data
        if category == DataCategory.PUBLIC and mlflow_run_id is not None:
            artifact_file = f"tables/{name}.json"
            self.info(
                f"Logging Confusion Matrix as artifact '{artifact_file}'",
                category=category,
            )
            MlflowClient().log_dict(
                run_id=mlflow_run_id, dictionary=value, artifact_file=artifact_file
            )
        else:
            self.warning(
                "Logging Confusion Matrices to text is not yet implemented",
                category=DataCategory.PUBLIC,
            )

    def artifact_predictions(
        self,
        name,
        value,
        col_predict=None,
        col_target=None,
        bin_edges=5,
        category=DataCategory.PRIVATE,
    ):
        """
        Equivalent of `Run.log_predictions` function.
        This will log regression prediction histogram from dict or dataframe.

        Note: Private Data will not be sent to artifacts!

        For the dataframe case the prediction error is computed as the absolute
        difference between prediction and target.

        Args:
            name (str): Name of the metric
            value (dict | DataFrame): The data to log
            col_predict (str | int, optional): ID or Name of the predict column.
                Defaults to None.
            col_target (str | int, optional): ID or Name of the target column.
            bin_edges (list, optional): List of edge boundaries for logging.
                Defaults to None.
            category (DataCategory, optional): Privacy Classification of the data.
                Defaults to DataCategory.PRIVATE.

        Raises:
            PublicRuntimeError: If the data is not in the right format or required
                parameters are not passed.
        """
        # retrieve mlflow run id
        mlflow_run_id = self._get_mlflow_run_id()

        # convert data if not already pre-computed
        if (
            not isinstance(value, dict)
            or "schema_type" not in value
            or "schema_version" not in value
        ):
            # check the data
            if is_vaex_dataframe(value):
                value = collect_vaex_dataframe(value)
            if is_spark_dataframe(value):
                value = collect_spark_dataframe(value)
            if is_pandas_dataframe(value):
                value = collect_pandas_dataframe(value)

            # check if datatype matches
            if not isinstance(value, dict):
                raise PublicRuntimeError("Unknown value-type passed to predictions!")

            # convert the data
            try:
                import pandas as pd

                # create the dataframe
                df = pd.DataFrame.from_dict(value)

                # column checks
                if None in [col_predict, col_target]:
                    raise PublicRuntimeError(
                        "The col_predict and col_target columns are both required."
                    )

                # compute edges automatically
                if isinstance(bin_edges, int):
                    bin_edges = floating_range(bin_edges)

                # compute groupings in bins
                df["bin"] = pd.cut(df[col_target], bin_edges)
                df["error"] = (df[col_predict] - df[col_target]).abs()

                # generate data
                value = {
                    "schema_type": "predictions",
                    "schema_version": "1.0.0",
                    "data": {
                        "bin_averages": list(df.groupby("bin")[col_target].mean()),
                        "bin_errors": list(df.groupby("bin")["error"].sum()),
                        "bin_counts": list(df.groupby("bin")[col_target].count()),
                        "bin_edges": bin_edges,
                    },
                }
            except Exception:
                raise PublicRuntimeError(
                    "Unable to import pandas and parse the given data! "
                    + "Make sure that libraries are available and correct "
                    + "data is passed."
                )

        # log the data
        if category == DataCategory.PUBLIC and mlflow_run_id is not None:
            artifact_file = f"tables/{name}.json"
            self.info(
                f"Logging Predictions Matrix as artifact '{artifact_file}'",
                category=category,
            )
            MlflowClient().log_dict(
                run_id=mlflow_run_id, dictionary=value, artifact_file=artifact_file
            )
        else:
            self.warning(
                "Logging Predictions to text is not yet implemented",
                category=DataCategory.PUBLIC,
            )

    def artifact_residual(
        self,
        name,
        value,
        col_predict=None,
        col_target=None,
        bin_edges=5,
        category=DataCategory.PRIVATE,
    ):
        """
        Equivalent on the `Run.log_residuals` functions.
        Logs residual values for a list of edges

        Note: Private Data will not be sent to artifacts!

        Args:
            name (str): Name of the metric
            value (dict | DataFrame): Values to contain the residuals
            col_predict (str, optional): Name of the prediction column
                (if value is a df).
            col_target (str, optional): Name of the target column (if value is a df).
                Defaults to None.
            bin_edges (list | int, optional): List of edges towards the bins.
                Defaults to 5.
            category (DataCategory, optional): Privacy Classification of the data.
                Defaults to DataCategory.PRIVATE.

        Raises:
            PublicRuntimeError: Thrown when data is in unknown format or required params
                not provided
        """
        # retrieve mlflow run id
        mlflow_run_id = self._get_mlflow_run_id()

        # convert data if not already pre-computed
        if (
            not isinstance(value, dict)
            or "schema_type" not in value
            or "schema_version" not in value
        ):
            # check the data
            if is_vaex_dataframe(value):
                value = collect_vaex_dataframe(value)
            if is_spark_dataframe(value):
                value = collect_spark_dataframe(value)
            if is_pandas_dataframe(value):
                value = collect_pandas_dataframe(value)

            # check if datatype matches
            if not isinstance(value, dict):
                raise PublicRuntimeError(
                    "Unknown value-type passed to Run.log_residuals()!"
                )

            # convert the data
            try:
                import pandas as pd

                # create the dataframe
                df = pd.DataFrame.from_dict(value)

                # column checks
                if None in [col_predict, col_target]:
                    raise PublicRuntimeError(
                        "The col_predict and col_target columns are both required."
                    )

                # check if bins should be generated automatically
                if isinstance(bin_edges, int):
                    bin_edges = floating_range(bin_edges)

                # compute the values
                df["residual"] = df[col_predict] - df[col_target]
                df["bin"] = pd.cut(df[col_target], bin_edges)

                # generate data
                value = {
                    "schema_type": "residuals",
                    "schema_version": "1.0.0",
                    "data": {
                        "bin_edges": bin_edges,
                        "bin_counts": list(df.groupby("bin")["residual"].sum()),
                    },
                }
            except Exception:
                raise PublicRuntimeError(
                    "Unable to import pandas and parse the given data! "
                    + "Make sure that libraries are available and correct "
                    + "data is passed."
                )

        # log the data
        if category == DataCategory.PUBLIC and mlflow_run_id is not None:
            artifact_file = f"tables/{name}.json"
            self.info(
                f"Logging Residuals as artifact '{artifact_file}'", category=category
            )
            MlflowClient().log_dict(
                run_id=mlflow_run_id, dictionary=value, artifact_file=artifact_file
            )
        else:
            self.warning(
                "Logging Residuals to text is not yet implemented",
                category=DataCategory.PUBLIC,
            )

    def metric_row(self, name, category=DataCategory.PRIVATE, **kwargs):
        """
        Equivalent of the `Run.log_row` function.
        Logs a single row of a table to the metrics.

        Note: Private Data will not be sent to metrics!

        Args:
            name (str): Name of the metric.
            category (DataCategory, optional): Classification of the data.
                Defaults to DataCategory.PRIVATE.
        """
        # retrieve mlflow run id
        mlflow_run_id = self._get_mlflow_run_id()

        # log the data
        if category == DataCategory.PUBLIC and mlflow_run_id is not None:
            timestamp = int(time() * 1000)
            step = kwargs.get("step", 0)
            metrics = [
                Metric(key=f"{name}.{key}", value=val, timestamp=timestamp, step=step)
                for key, val in kwargs.items()
            ]
            MlflowClient().log_batch(run_id=mlflow_run_id, metrics=metrics)
        row_str = f"RowMetric      | {name} | "
        row_str += " | ".join([f"{r}:{c}" for r, c in kwargs.items()])
        self.info(row_str, category=category)

    def metric_table(self, name, value, category=DataCategory.PRIVATE):
        """
        Equivalent to the `Run.log_table` function.
        Logs a table in dict format {rows: [values]} to metrics and artifacts.

        Note: Private Data will not be sent to metrics!

        Args:
            name (str): Name of the metric.
            value (dict): Dictionary representation of the table.
            category (DataCategory, optional): Category to log the data.
                Default to DataCategory.PRIVATE.
        """
        self.metric(value=value, name=name, category=category)


def is_eyesoff() -> bool:
    """
    Returns a boolean whether current workspace is eyes-off.
    For unified workspace, check env var `IsUnifiedEyesOn`.
    """
    if os.environ.get("IsUnifiedEyesOn", ""):
        return False
    else:
        tenant_id = os.environ.get("AZ_BATCHAI_CLUSTER_TENANT_ID", "")
        subscription_id = os.environ.get("AZUREML_ARM_SUBSCRIPTION", "")
        return is_eyesoff_helper(tenant_id, subscription_id)


_logging_basic_config_set_warning = """
********************************************************************************
The root logger already has handlers set! As a result, the behavior of this
library is undefined. If running in Python >= 3.8, this library will attempt to
call logging.basicConfig(force=True), which will remove all existing root
handlers. See https://stackoverflow.com/q/20240464 and
https://github.com/Azure/confidential-ml-utils/issues/33 for more information.
********************************************************************************
"""


def enable_compliant_logging(
    prefix: str = "SystemLog:",
    scrub_message: str = "**Log message scrubbed**",
    use_aml_metrics: bool = False,
    enable_scrubbed_logging: bool = False,
    **kwargs,
) -> None:
    """
    The default format is `logging.BASIC_FORMAT` (`%(levelname)s:%(name)s:%(message)s`).
    All other kwargs are passed to `logging.basicConfig`. Sets the default
    logger class and root logger to be compliant. This means the format
    string `%(prefix)` will work.

    Set the format using the `format` kwarg.

    If running in Python >= 3.8, will attempt to add `force=True` to the kwargs
    for logging.basicConfig.

    After calling this method, use the kwarg `category` to pass in a value of
    `DataCategory` to denote data category. The default is `PRIVATE`. That is,
    if no changes are made to an existing set of log statements, the log output
    should be the same.

    The standard implementation of the logging API is a good reference:
    https://github.com/python/cpython/blob/3.9/Lib/logging/__init__.py
    """
    set_prefix(prefix)
    set_scrub_message(scrub_message)

    if enable_scrubbed_logging:
        set_scrubbed_logging(True)

    if "format" not in kwargs:
        kwargs["format"] = f"%(prefix)s{logging.BASIC_FORMAT}"

    # Ensure that all loggers created via `logging.getLogger` are instances of
    # the `CompliantLogger` class.
    logging.setLoggerClass(CompliantLogger)

    if len(logging.root.handlers) > 0:
        p = get_prefix()
        for line in _logging_basic_config_set_warning.splitlines():
            print(f"{p}{line}", file=sys.stderr)

    if "force" not in kwargs and sys.version_info >= (3, 8):
        kwargs["force"] = True

    root = CompliantLogger(
        logging.root.name, use_aml_metrics, handlers=logging.root.handlers
    )

    logging.root = root
    logging.Logger.root = root  # type: ignore
    logging.Logger.manager = logging.Manager(root)  # type: ignore

    # https://github.com/kivy/kivy/issues/6733
    logging.basicConfig(**kwargs)


def enable_confidential_logging(
    prefix: str = "SystemLog:",
    scrub_message: str = "**Log message scrubbed**",
    use_aml_metrics: bool = False,
    enable_scrubbed_logging: bool = False,
    **kwargs,
) -> None:
    """
    This function is a duplicate of the function `enable_compliant_logging`.
    We encourage users to use `enable_compliant_logging`.
    """
    print(
        f"{prefix} The function enable_confidential_logging() is on the way"
        " to deprecation. Please use enable_compliant_logging() instead.",
        file=sys.stderr,
    )
    enable_compliant_logging(
        prefix, scrub_message, use_aml_metrics, enable_scrubbed_logging, **kwargs
    )
