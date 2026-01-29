import pytest
from python_to_dag.validator import ValidationEngine


def test_fail_fast_provide_context():
    with pytest.raises(ValueError, match="Detected 'provide_context=True'"):
        ValidationEngine.validate_task_kwargs(
            "PythonOperator", {"provide_context": True}
        )


def test_allow_clean_kwargs():
    # Should not raise
    ValidationEngine.validate_task_kwargs("PythonOperator", {"op_kwargs": "clean"})
