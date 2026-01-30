import os
import pytest
from python_to_dag.parser import PipelineParser
from python_to_dag.generator import PipelineGenerator
from python_to_dag.ir import PipelineIR


def test_programmatic_rewrite_integration(tmp_path):
    # 1. Setup Input YAML
    yaml_content = """
pipeline_id: pipeline__int_test__rewrite
schedule_interval: "@once"
tasks:
  - task_id: t1
    task_type: DummyOperator
  - task_id: t2
    task_type: PythonOperator
    upstream_task_ids: ["t1"]
"""
    input_file = tmp_path / "rewrite_test.yaml"
    input_file.write_text(yaml_content, encoding="utf-8")

    # 2. Parse (Logic Check)
    parser = PipelineParser()
    pipeline_ir = parser.parse_file(str(input_file))

    # Check IR Rewrite
    t1 = next(t for t in pipeline_ir.tasks if t.task_id == "t1")
    assert (
        t1.task_type == "EmptyOperator"
    ), "Parser should rewrite DummyOperator to EmptyOperator"

    # 3. Generate (Template Check)
    generator = PipelineGenerator()
    out_file = tmp_path / "out_dag.py"
    generator.generate(pipeline_ir, str(out_file))

    generated_code = out_file.read_text(encoding="utf-8")

    # Check Imports
    assert "from airflow.providers.standard.operators.empty import EmptyOperator" in generated_code
    assert "from airflow.providers.standard.operators.python import PythonOperator" in generated_code

    # Check Instantiation
    assert "t1 = EmptyOperator(" in generated_code
