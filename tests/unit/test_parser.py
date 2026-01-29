import os
import pytest
from python_to_dag.parser import PipelineParser
from python_to_dag.ir import PipelineIR


@pytest.fixture
def sample_yaml_path():
    # Helper to get the path of the sample yaml
    base_dir = os.path.dirname(__file__)
    return os.path.join(
        base_dir, "..", "..", "pipelines", "yaml", "example_pipeline.yaml"
    )


def test_parser_loads_valid_yaml(sample_yaml_path):
    parser = PipelineParser()
    pipeline = parser.parse_file(sample_yaml_path)

    assert isinstance(pipeline, PipelineIR)
    assert pipeline.pipeline_id == "pipeline__example__data_processing"
    assert len(pipeline.tasks) == 3
    assert pipeline.tasks[0].task_id == "extract_data"


def test_parser_validates_task_id_format():
    parser = PipelineParser()
    # Create invalid data manually to test IR validation directly
    from python_to_dag.ir import TaskIR

    with pytest.raises(ValueError, match="must be lowercase"):
        TaskIR(task_id="Invalid_task_id", task_type="python")
