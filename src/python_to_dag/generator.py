import os
import black
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from .ir import PipelineIR
from .rewrite import RewriteEngine


class PipelineGenerator:
    def __init__(self, template_dir: str = None):
        if template_dir is None:
            # Default to src/airflow_templates
            current_dir = Path(__file__).parent.resolve()
            template_dir = current_dir.parent / "airflow_templates"

        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

    def generate(self, pipeline: PipelineIR, output_path: str):
        """Generates a DAG python file from the PipelineIR."""
        template = self.env.get_template("dag_template.jinja2")

        # P2-1: Resolve imports
        imports = set()
        for task in pipeline.tasks:
            imports.add((task.task_type, RewriteEngine.get_import_path(task.task_type)))

        # P2-4: Organize tasks by Group
        # Structure: { 'group_id': [tasks...], None: [root_tasks...] }
        grouped_tasks = {}
        for task in pipeline.tasks:
            gid = task.task_group_id
            if gid not in grouped_tasks:
                grouped_tasks[gid] = []
            grouped_tasks[gid].append(task)

        # Ensure imports include TaskGroup if needed
        has_task_group = any(gid is not None for gid in grouped_tasks)
        if has_task_group:
            imports.add(("TaskGroup", "airflow.sdk"))

        # Render
        code = template.render(
            pipeline=pipeline,
            imports=sorted(list(imports)),
            grouped_tasks=grouped_tasks,
        )

        # Format with black
        try:
            code = black.format_str(code, mode=black.Mode())
        except black.InvalidInput:
            print("[WARN] Generated code is invalid, skipping formatting.")

        # Write to file
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"Generated DAG: {output_path}")
