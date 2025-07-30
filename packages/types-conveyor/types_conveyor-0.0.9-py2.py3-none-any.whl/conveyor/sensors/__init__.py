import datetime
from typing import Callable, Iterable, Literal, Mapping, Optional, Sequence

from airflow.sensors.base import BaseSensorOperator


class ConveyorContainerSensor(BaseSensorOperator):
    def __init__(
        self,
        *,
        instance_type: Optional[str] = None,
        instance_life_cycle: Optional[Literal["spot", "on_demand"]] = None,
        image: str = "{{ macros.conveyor.default_image(dag) }}",
        command: Optional[Sequence[str]] = None,
        arguments: Optional[Sequence[str]] = None,
        env_vars: Optional[Mapping[str, str]] = None,
        aws_role: Optional[str] = None,
        azure_application_client_id: Optional[str] = None,
        **kwargs,
    ) -> None: ...


class ConveyorExternalTaskSensor(BaseSensorOperator):
    def __init__(
        self,
        *,
        external_dag_id: str,
        environment: Optional[str] = None,
        external_task_id: Optional[str] = None,
        external_task_ids: Optional[Iterable[str]] = None,
        allowed_states: Optional[Iterable[str]] = None,
        execution_delta: Optional[datetime.timedelta] = None,
        execution_date_fn: Optional[Callable] = None,
        instance_life_cycle: Optional[Literal["spot", "on_demand"]] = None,
        **kwargs,
    ) -> None: ...
