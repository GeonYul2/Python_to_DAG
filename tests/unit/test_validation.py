import pytest
from python_to_dag.ir import TaskIR
from pydantic import ValidationError


def test_task_id_max_length():
    """Task ID must be 50 characters or less."""
    # 50 chars ok
    valid_id = "a" * 50
    t = TaskIR(task_id=valid_id, task_type="python")
    assert t.task_id == valid_id

    # 51 chars fails
    invalid_id = "a" * 51
    with pytest.raises(ValidationError) as excinfo:
        TaskIR(task_id=invalid_id, task_type="python")

    # Check error message (approximate match)
    assert "String should have at most 50 characters" in str(
        excinfo.value
    ) or "less than or equal to 50" in str(excinfo.value)
