from typing import Any, Literal, Mapping, Optional, Sequence, Union
from warnings import warn

from airflow.models import BaseOperator
from airflow.models.xcom import XCOM_RETURN_KEY

from conveyor.secrets import SecretValue as SecretValue


class ConveyorContainerOperatorV2(BaseOperator):
    def __init__(
        self,
        *,
        instance_type: Optional[str] = None,
        airflow_worker_instance_type: Optional[str] = None,
        validate_docker_image_exists=True,
        image: str = "{{ macros.conveyor.default_image(dag) }}",
        command: Optional[Sequence[str]] = None,
        arguments: Optional[Sequence[str]] = None,
        env_vars: Optional[Mapping[str, Union[str, SecretValue]]] = None,
        aws_role: Optional[str] = None,
        azure_application_client_id: Optional[str] = None,
        instance_life_cycle: Optional[Literal["spot", "on_demand"]] = None,
        disk_size: Optional[int] = None,
        disk_mount_path: str = "/var/data",
        xcom_push: bool = False,
        xcom_key: str = XCOM_RETURN_KEY,
        **kwargs,
    ) -> None: ...


class ConveyorSparkSubmitOperatorV2(BaseOperator):
    def __init__(
        self,
        *,
        application: str = "",
        application_args: Optional[Sequence[Any]] = None,
        conf: Optional[Mapping[str, str]] = None,
        java_class: Optional[str] = None,
        num_executors: Optional[int] = None,
        spark_main_version: Optional[int] = None,
        validate_docker_image_exists=True,
        driver_instance_type: Optional[str] = None,
        executor_instance_type: Optional[str] = None,
        aws_role: Optional[str] = None,
        azure_application_client_id: Optional[str] = None,
        image: str = "{{ macros.conveyor.default_image(dag) }}",
        env_vars: Optional[Mapping[str, Union[str, SecretValue]]] = None,
        instance_life_cycle: Optional[
            Literal["spot", "on-demand", "driver-on-demand-executors-spot"]
        ] = None,
        airflow_worker_instance_type: Optional[str] = None,
        s3_committer: Optional[Literal["file", "magic"]] = None,
        abfs_committer: Optional[Literal["file", "manifest"]] = None,
        executor_disk_size: Optional[int] = None,
        mode: Optional[Literal["local", "cluster", "cluster-v2"]] = None,
        aws_availability_zone: Optional[str] = None,
        verbose: bool = False,
        **kwargs,
    ) -> None:
        if spark_main_version is not None:
            warn(
                "Setting spark main version is deprecated, "
                "the version is automatically detected from the container image",
                DeprecationWarning,
            )
