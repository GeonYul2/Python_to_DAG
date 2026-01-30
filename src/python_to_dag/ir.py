from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, field_validator


class TaskIR(BaseModel):
    task_id: str = Field(
        ..., description="Unique identifier for the task, snake_case", max_length=50
    )
    task_type: str = Field(
        ..., description="Type of the task (e.g., python, bash, sql)"
    )
    callable_name: Optional[str] = Field(
        None, description="Name of the python function to call"
    )
    callable_source: Optional[str] = Field(
        None, description="Source code of the function if embedded"
    )
    op_args: List[Any] = Field(default_factory=list, description="Positional arguments")
    op_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Keyword arguments"
    )
    upstream_task_ids: List[str] = Field(
        default_factory=list, description="List of task_ids this task depends on"
    )
    task_group_id: Optional[str] = Field(
        None, description="ID of the TaskGroup this task belongs to"
    )
    outlets: List[str] = Field(
        default_factory=list, description="List of dataset URIs to update (e.g. dataset://my-data)"
    )

    # Contract / Resources (Placeholder for now)
    # data_contract: Optional[DataContractIR] = None

    @field_validator("task_id")
    def validate_task_id(cls, v):
        if not v.islower() or " " in v:
            raise ValueError("task_id must be lowercase and contain no spaces")
        return v


class PipelineDefaultIR(BaseModel):
    owner: str = "airflow"
    retries: int = 1
    retry_delay_sec: int = 300
    start_date: Optional[str] = None  # ISO format date string
    other_args: Dict[str, Any] = Field(default_factory=dict)


class PipelineIR(BaseModel):
    pipeline_id: str
    schedule_interval: Optional[str] = "@daily"
    schedule_datasets: List[str] = Field(
        default_factory=list, description="List of upstream dataset URIs to trigger on"
    )
    default_args: PipelineDefaultIR = Field(default_factory=PipelineDefaultIR)
    tasks: List[TaskIR] = Field(default_factory=list)
    catchup: bool = False
    tags: List[str] = Field(default_factory=list)

    @field_validator("pipeline_id")
    def validate_pipeline_id(cls, v):
        # Example validation: ensure starts with pipeline__
        if not v.startswith("pipeline__"):
            raise ValueError("pipeline_id must start with 'pipeline__'")
        return v
