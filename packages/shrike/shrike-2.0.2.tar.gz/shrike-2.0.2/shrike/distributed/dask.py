# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Helper code to run Dask distributed scripts [EXPERIMENTAL]
"""
import asyncio
import os
import socket
import sys
from typing import Optional, cast

import psutil
from shrike._core import experimental
from shrike.compliant_logging import DataCategory
from shrike.distributed import EXPERIMENTAL_WARNING_MSG
from shrike.distributed.cluster_auto_setup import ClusterAutoSetupHandler

from dask.distributed import Client, Nanny, Scheduler, Worker, performance_report


# pragma: no cover
class DaskClusterSetupHandler(ClusterAutoSetupHandler):
    def __init__(
        self,
        process_count_per_node: Optional[int] = None,
        thread_count_per_process: Optional[int] = None,
        dask_report_link: Optional[str] = None,
        nanny: bool = False,
        public_log: bool = False,
    ):
        """Constructor for Dask Cluster
        Args:
            process_count_per_node (int): Number of processes available per node.
                Defaults to `None`.
                If `None` the machine cpu count defines the number of processes.
            thread_count_per_process (int): Number of threads available per process.
                Defaults to `None`. If `None` the number of threads is defined by the
                division of cpu count by number of processes.
            dask_report_link (str): Path where dask dashboard report will be written to.
                Defaults to None. When None, dask dashboard is not reported/written to
                a file.
            Nanny (bool): Whether to use Nanny or not. Defaults to False.
                The nanny spins up Worker processes, watches then, and kills or restarts
                them as necessary. It is necessary if you want to use
                the Client.restart method, or to restart the worker automatically if
                it gets to the terminate fraction of its memory limit
            public_log (bool): Whether to log information to the compliant public log.
                If used call `shrike.compliant_logging.enable_compliant_logging()` to
                initialize compliant logging beforehand. Defaults to False.

        Example:
            - Starts a Cluster using as many processes as cpu count
                (Ideal to avoid workloads suffering from GIL lock):

            >>> from shrike.distributed import DaskClusterSetupHandler
            >>> with DaskClusterSetupHandler() as azure_cluster:
            ...     client = azure_cluster.client
            ...     logger.info(f"Dask {client}")

            - Starts a Cluster using 1 process per machine,
                and give to it as many threads as cpu count:

            >>> from shrike.distributed import DaskClusterSetupHandler
            >>> with DaskClusterSetupHandler(process_count_per_node=1) as azure_cluster:
            ...     client = azure_cluster.client
            ...     logger.info(f"Dask {client}")
        """
        super().__init__()
        self.public_log = public_log
        self.head_port = 45462
        if nanny is True:
            self.constructor = Nanny
        else:
            self.constructor = Worker

        self.node_count = int(cast(str, os.getenv("OMPI_COMM_WORLD_SIZE")))
        self.rank = int(cast(str, os.getenv("OMPI_COMM_WORLD_RANK")))
        self.ip = socket.gethostbyname(socket.gethostname())

        self.head_address = None
        if process_count_per_node is None:
            self.process_count_per_node = psutil.cpu_count()
        else:
            self.process_count_per_node = process_count_per_node

        # How many threads is available per worker
        if thread_count_per_process is None:
            self.thread_count_per_process = int(
                psutil.cpu_count() / self.process_count_per_node
            )
        else:
            self.thread_count_per_process = int(thread_count_per_process)
        self.worker_ram = int(
            0.90 * psutil.virtual_memory().available / self.process_count_per_node
        )
        self.worker_count = (self.node_count - 1) * self.process_count_per_node

        self.dask_performance_report_file: Optional[str] = None
        # output dashboard
        if dask_report_link is not None:
            self.dask_performance_report_file = os.path.join(
                dask_report_link, "dask-report.html"
            )

    def _log_info_publicly(self, message):
        """Logs a message to the public log.
        When compliant logging is enabled, this will log to the public log.
        Otherwise, this will log to info
        """
        if self.public_log:
            self.logger.info(message, category=DataCategory.PUBLIC)
        else:
            self.logger.info(message)

    #################
    # SETUP METHODS #
    #################

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def setup_head_node(self):
        """Setup to run only on head node"""
        self._log_info_publicly(EXPERIMENTAL_WARNING_MSG)
        self._log_info_publicly(
            f"{self.__class__.__name__}.setup_head_node() called to set up HEAD node."
        )
        # create setup config
        self.head_address = socket.gethostbyname(socket.gethostname())

        # record what's needed to setup cluster nodes
        self.setup_config_add_key("head_address", self.head_address)

        self.pid = os.fork()  # type: ignore
        if self.pid > 0:
            self.rank = "0.1"

            async def run_scheduler():
                async with Scheduler(
                    port=self.head_port, scheduler_file="scheduler.json"
                ) as scheduler:
                    await scheduler.finished()

            asyncio.get_event_loop().run_until_complete(run_scheduler())
            self._log_info_publicly(f"[R{self.rank}]SCHEDULER IS OFFLINE")
            self.multinode_driver.finalize()
            sys.exit(0)

    @experimental(message=EXPERIMENTAL_WARNING_MSG)
    def setup_cluster_node(self):
        """Setup to run only on non-head cluster nodes"""
        self._log_info_publicly(EXPERIMENTAL_WARNING_MSG)

        self._log_info_publicly(
            f"{self.__class__.__name__}.setup_cluster_node() called"
        )
        self.head_address = self.setup_config_get_key("head_address")

    def __enter__(self):
        self.initialize_run()

        for line in self.__repr__().split("\n"):
            self._log_info_publicly(line)

        if self.rank != 0:
            self._log_info_publicly("Running worker...")

            async def run_worker():
                async with self.constructor(
                    scheduler_ip=self.head_address,
                    scheduler_port=self.head_port,
                    nthreads=self.thread_count_per_process,
                    memory_limit=self.worker_ram,
                    local_directory=os.getenv("AZ_BATCHAI_JOB_TEMP"),
                    name=f"{self.rank}",
                ) as worker:
                    self._log_info_publicly(f"[R{self.rank}] - {worker}")
                    await worker.finished()

            if self.process_count_per_node > 1:
                for i in range(self.process_count_per_node - 1):
                    pid = os.fork()
                    if pid > 0:
                        self.rank = f"{self.rank}_{i}"
                        asyncio.get_event_loop().run_until_complete(run_worker())
                        self._log_info_publicly(f"[R{self.rank}]Worker IS OFFLINE")
                        self.multinode_driver.finalize()
                        sys.exit(0)

            # Shut down when down
            asyncio.get_event_loop().run_until_complete(run_worker())
            self._log_info_publicly(f"[R{self.rank}]Worker IS OFFLINE")
            self.multinode_driver.finalize()
            sys.exit(0)
        else:
            self._log_info_publicly("Starting Dask Client...")
            self.client = Client(f"tcp://{self.head_address}:{self.head_port}")
            self._log_info_publicly(
                f"Waiting for {self.worker_count} workers up to 10s"
            )
            self.client.wait_for_workers(self.worker_count, 10)

            if self.dask_performance_report_file is not None:
                self.dask_performance_report = performance_report(
                    filename=self.dask_performance_report_file
                )
                self.dask_performance_report.__enter__()

        return self

    def __repr__(self) -> str:
        string = (
            "Cluster info\n"
            f"\t├─>\t\t rank = {self.rank} \n"
            f"\t├─>\t\t ip = {self.ip} \n"
            f"\t├─>\t\t scheduler_ip = {self.head_address} \n"
            f"\t├─>\t\t node_count = {self.node_count} \n"
            f"\t├─>\t\t process_count_per_node = {self.process_count_per_node} \n"
            f"\t├─>\t\t thread_count_per_process = {self.thread_count_per_process} \n"
            f"\t├─>\t\t worker_ram = {(self.worker_ram/(2**30)):.2f} GB \n"
            f"\t├─>\t\t worker_count = {self.worker_count} \n"
        )
        return string

    def __exit__(self, type, value, traceback):

        self._log_info_publicly(f"Exiting context from rank {self.rank}")
        if self.rank == 0:

            self._log_info_publicly(
                f"Dask dashboard saved to {self.dask_performance_report_file}"
            )
            self._log_info_publicly("Shutting dask down...")
            self.client.shutdown()  # This will also close the workers

            if os.path.exists("scheduler.json"):
                os.remove("scheduler.json")
            # self.multinode_driver.finalize()
            if self.dask_performance_report_file is not None:
                self.dask_performance_report.__exit__(type, value, traceback)
