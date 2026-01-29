import os
import pytest
import difflib
from python_to_dag.parser import PipelineParser
from python_to_dag.generator import PipelineGenerator

GOLDEN_INPUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "pipelines", "yaml"
)
GOLDEN_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "dags")


def get_golden_cases():
    """Returns list of (yaml_path, expected_dag_path)"""
    cases = []
    if not os.path.exists(GOLDEN_INPUT_DIR):
        return []

    for f in os.listdir(GOLDEN_INPUT_DIR):
        if f.endswith(".yaml"):
            yaml_path = os.path.join(GOLDEN_INPUT_DIR, f)
            # Assumption: output file name derived from parsing (not known statically),
            # OR we enforce a naming convention.
            # For this test, we assume the example_pipeline.yaml generates pipeline__example__data_processing.py
            # To be more generic, we might need a mapping or parse first.
            if f == "example_pipeline.yaml":
                expected_dag = os.path.join(
                    GOLDEN_OUTPUT_DIR, "pipeline__example__data_processing.py"
                )
                cases.append((yaml_path, expected_dag))
    return cases


@pytest.mark.parametrize("yaml_path, expected_dag_path", get_golden_cases())
def test_golden_dag_generation(yaml_path, expected_dag_path, tmp_path):
    """
    Parses the YAML, generates the DAG to a temp file,
    and compares it bit-by-bit with the expected DAG in dags/ folder.
    """
    parser = PipelineParser()
    pipeline = parser.parse_file(yaml_path)

    generator = PipelineGenerator()

    # Generate to temp
    actual_dag_path = tmp_path / os.path.basename(expected_dag_path)
    generator.generate(pipeline, str(actual_dag_path))

    # Compare
    with open(expected_dag_path, "r", encoding="utf-8") as f:
        expected_content = f.read()

    with open(actual_dag_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    assert (
        actual_content == expected_content
    ), f"Generated DAG does not match golden file: {expected_dag_path}"
