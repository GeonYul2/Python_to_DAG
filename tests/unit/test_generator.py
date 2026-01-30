import os
import pytest
from python_to_dag.generator import PipelineGenerator
from python_to_dag.ir import PipelineIR, TaskIR, PipelineDefaultIR


def test_generator_creates_output(tmp_path):
    # Mock IR
    pipeline = PipelineIR(
        pipeline_id="pipeline__test__mk1",
        default_args=PipelineDefaultIR(owner="test"),
        tasks=[
            TaskIR(task_id="t1", task_type="python"),
            TaskIR(task_id="t2", task_type="python", upstream_task_ids=["t1"]),
        ],
    )

    output_path = tmp_path / "gen_test.py"

    generator = PipelineGenerator()
    generator.generate(pipeline, str(output_path))

    assert output_path.exists()
    content = output_path.read_text("utf-8")
    assert 'dag_id="pipeline__test__mk1"' in content
    assert "t1 >> t2" in content
