from typing import Literal, Mapping, Optional, Sequence, Tuple, Union

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.task_group import TaskGroup

from conveyor.secrets import SecretValue


class ConveyorDbtTaskFactory(LoggingMixin):
    def __init__(
        self,
        *,
        manifest_file: str = "manifest.json",
        task_name_prefix: Optional[str] = None,
        task_name_suffix: Optional[str] = None,
        task_cmd: Sequence[str] = (),
        task_arguments: Sequence[str] = (
            "--no-use-colors",
            "{command}",
            "--target",
            "{{ macros.conveyor.env() }}",
            "--profiles-dir",
            "./..",
            "--select",
            "{model}",
        ),
        task_instance_type: str = "mx.micro",
        airflow_worker_instance_type: Optional[str] = None,
        task_instance_life_cycle: Optional[Literal["spot", "on-demand"]] = None,
        task_aws_role: Optional[str] = None,
        task_azure_application_client_id: Optional[str] = None,
        task_env_vars: Optional[Mapping[str, Union[str, SecretValue]]] = None,
        start_task_name_override: Optional[str] = None,
        end_task_name_override: Optional[str] = None,
    ) -> None: ...

    def add_tasks_to_dag(
        self,
        dag: DAG,
        *,
        tags: Sequence[str] = (),
        any_tag: bool = True,
        test_tasks: bool = True,
    ) -> Tuple[EmptyOperator, EmptyOperator]: ...

    def add_tasks_to_dag_v2(
        self,
        dag: DAG,
        *,
        select: Optional[str] = None,
        exclude: Optional[str] = None,
        test_tasks: bool = True,
    ) -> Tuple[EmptyOperator, EmptyOperator]: ...

    def add_tasks_to_task_group(
        self,
        dag: DAG,
        *,
        task_group_name: str = "dbt_run",
        test_task_group_name: str = "dbt_test",
        tags: Sequence[str] = (),
        any_tag: bool = True,
    ) -> Tuple[TaskGroup, TaskGroup]: ...

    def add_tasks_to_task_group_v2(
        self,
        dag: DAG,
        *,
        task_group_name: str = "dbt_run",
        test_task_group_name: str = "dbt_test",
        select: Optional[str] = None,
        exclude: Optional[str] = None,
    ) -> Tuple[TaskGroup, TaskGroup]: ...
