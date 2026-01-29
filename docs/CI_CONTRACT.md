# CI Contract (CLI + GitHub Actions Gates)

목표: “Airflow에서 깨지는 DAG”이 main에 들어오지 못하게 한다.

---

## 1) CLI Contract

### build
- python -m python_to_dag build --input <pipeline_def> --out dags/

산출:
- dags/<dag_id>.py
- (선택) artifacts/rewrite_report.json

### validate
- python -m python_to_dag validate --input <pipeline_def>

---

## 2) Gates

### Pre Gate (로직/규칙)
- unit tests
- rewrite rules tests
- schema validation tests
- golden diff (생성 DAG 변경 감지)

### Post Gate (Airflow import)
- DagBag import test (import error == 0)

---

## 3) GitHub Actions Requirements (요건만 고정)
- PR마다 Pre+Post Gate 자동 수행
- 실패 시:
  - 어떤 gate에서 실패했는지 명확히 출력
  - rewrite_report가 있으면 artifact로 업로드(옵션)

(워크플로우 yaml은 코드 산출물로 관리한다. 이 문서는 “계약”만 규정한다.)
