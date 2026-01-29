from typing import Dict, Any


class ValidationEngine:
    """
    Handles P2-2 Quality Rules (Anti-Patterns).
    """

    @staticmethod
    def validate_task_kwargs(task_type: str, kwargs: Dict[str, Any]):
        """
        Validates task arguments for forbidden patterns.
        """
        # N-04: provide_context usage
        if task_type == "PythonOperator" and kwargs.get("provide_context") is True:
            raise ValueError(
                "Detected 'provide_context=True'. This is deprecated in Airflow 2.0+. "
                "Please use TaskFlow API (@task) or standard kwargs."
            )
