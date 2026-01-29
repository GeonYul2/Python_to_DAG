import os
import pytest
from click.testing import CliRunner
from python_to_dag.cli import cli


@pytest.fixture
def sample_yaml_path():
    base_dir = os.path.dirname(__file__)
    return os.path.join(
        base_dir, "..", "..", "pipelines", "yaml", "example_pipeline.yaml"
    )


def test_cli_validate_success(sample_yaml_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--input", sample_yaml_path])
    assert result.exit_code == 0
    assert "Validation Success" in result.output


def test_cli_validate_fail_no_file():
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--input", "non_existent.yaml"])
    assert result.exit_code != 0
    # Click handles parsing error before our try/except block usually, but let's check exit code


def test_cli_build_success(sample_yaml_path, tmp_path):
    runner = CliRunner()
    out_dir = tmp_path / "dags_out"
    result = runner.invoke(
        cli, ["build", "--input", sample_yaml_path, "--out", str(out_dir)]
    )

    assert result.exit_code == 0
    assert "Build Success" in result.output

    # Check if file created
    files = list(out_dir.glob("*.py"))
    assert len(files) == 1
    assert "pipeline__example__data_processing.py" in files[0].name
