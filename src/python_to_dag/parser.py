import yaml
import os
from typing import Dict, Any, Union
from pathlib import Path
from .ir import PipelineIR, TaskIR, PipelineDefaultIR
from .rewrite import RewriteEngine
from .validator import ValidationEngine


class PipelineParser:
    def __init__(self):
        pass

    def parse_yaml(self, file_path: str) -> PipelineIR:
        """Parses a YAML file into a PipelineIR object."""
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"Pipeline definition file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parse YAML file: {e}")

        return self._build_pipeline_ir(data)

    def _build_pipeline_ir(self, data: Dict[str, Any]) -> PipelineIR:
        """Converts raw dictionary data to PipelineIR, with validation."""

        # 1. Pipeline defaults
        raw_defaults = data.get("default_args", {})
        defaults = PipelineDefaultIR(**raw_defaults)

        # 2. Tasks
        raw_tasks = data.get("tasks", [])
        tasks_ir = []
        for t in raw_tasks:
            # P2-1: Apply Rewrite Rules
            if "task_type" in t:
                t["task_type"] = RewriteEngine.map_operator_type(t["task_type"])

            # P2-2: Validate Anti-Patterns
            ValidationEngine.validate_task_kwargs(
                t.get("task_type"), t.get("op_kwargs", {})
            )

            tasks_ir.append(TaskIR(**t))

        # 3. Pipeline
        pipeline = PipelineIR(
            pipeline_id=data.get("pipeline_id"),
            schedule_interval=data.get("schedule_interval"),
            schedule_datasets=data.get("schedule_datasets", []),
            default_args=defaults,
            tasks=tasks_ir,
            catchup=data.get("catchup", False),
            tags=data.get("tags", []),
        )

        return pipeline

    def parse_file(self, file_path: str) -> PipelineIR:
        """Main entry point to parse a file based on extension."""
        if file_path.endswith(".yaml") or file_path.endswith(".yml"):
            return self.parse_yaml(file_path)
        else:
            raise NotImplementedError("Only YAML parsing is currently supported.")
