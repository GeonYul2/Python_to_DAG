from python_to_dag.rewrite import RewriteEngine


def test_rewrite_dummy_to_empty():
    assert RewriteEngine.map_operator_type("DummyOperator") == "EmptyOperator"
    assert RewriteEngine.map_operator_type("dummy") == "EmptyOperator"


def test_rewrite_python_import_path():
    assert RewriteEngine.get_import_path("PythonOperator") == "airflow.operators.python"
    assert RewriteEngine.get_import_path("EmptyOperator") == "airflow.operators.empty"
