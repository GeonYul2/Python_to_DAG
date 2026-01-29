from typing import Tuple, List, Optional


class RewriteEngine:
    """
    Handles P2-1 Rewrite Rules.
    Currently focuses on string/pattern mapping for Operator names and imports.
    """

    # Rule 2.1: PythonOperator Import path (If used in Python code, but here we enforce generation)
    # Rule 2.2: DummyOperator -> EmptyOperator

    @staticmethod
    def map_operator_type(task_type: str) -> str:
        """
        Maps legacy operator types to modern ones.
        SAFE_REWRITE rules.
        """
        normalized = task_type.lower()

        if normalized in [
            "dummyoperator",
            "dummy",
            "airflow.operators.dummy_operator.dummyoperator",
        ]:
            return "EmptyOperator"

        if normalized in [
            "python",
            "pythonoperator",
            "airflow.operators.python_operator.pythonoperator",
        ]:
            return "PythonOperator"

        # Default pass-through (assume it's valid or custom)
        return task_type

    @staticmethod
    def get_import_path(operator_class: str) -> str:
        """
        Returns the modern import path for standard operators.
        """
        if operator_class == "EmptyOperator":
            return "airflow.operators.empty"
        if operator_class == "PythonOperator":
            return "airflow.operators.python"

        # Fallback / TODO: Add more mappings
        return "airflow.operators.python"  # Default for now as we mostly support Python
