# Handoff Prompt for Antigravity — Implement PYTHON_TO_DAG Exactly

너는 이 프로젝트에서 “구현자”다.  
내가 제공한 문서 스펙을 그대로 만족하는 형태로 코드를 작성해야 하며,
**환경/버전/요구사항을 임의로 가정하거나 생략하면 실패**다.

---

## 0) Absolute Rules
1) Airflow 문법/패턴은 `docs/04_airflow_dag_guidelines.md`의 Compatibility Matrix 범위 안에서만 사용한다.
2) 생성 DAG는 운영 가능해야 한다:
   - retries/timeout/failure callback/logging/correlation_id/idempotency/backfill safety
3) 입력이 같으면 출력도 같아야 한다 (deterministic codegen).
4) secrets/paths를 하드코딩하지 않는다. (Variables/Connections/config로만)

---

## 1) Deliverables (Minimum)
- `src/python_to_dag/`:
  - parser (yaml/python) → IR
  - validator (hard fail rules)
  - generator (template 기반 DAG 생성)
- `src/python_to_dag/runtime_utils/`:
  - logging wrapper (correlation_id 포함)
  - failure callback interface
  - data contract validator interface
- `pipelines/`:
  - 샘플 2개 (youtube_transcript_to_report, daily_channel_digest)
- `tests/`:
  - unit tests
  - golden tests (generated DAG 비교)
- 생성된 DAG 예시 2개가 `dags/`에 존재

---

## 2) Implementation Constraints
- Python 파이프라인 정의는 “등록/데코레이터 방식”만 허용한다.
  - 코드 정적 분석으로 의존성을 추론하려고 하지 마라.
- YAML 스키마는 `docs/07_config_schema.md`를 따른다.
- XCom에는 경로/메타만 저장하고 본문/대용량 객체는 금지.

---

## 3) Acceptance Proof (What you must show)
- `python -m python_to_dag validate ...` 성공
- `python -m python_to_dag build ...` 성공 및 `dags/*.py` 생성
- 테스트:
  - unit + golden 통과 로그 제시
- failure scenario 최소 3개를 문서대로 재현 가능하게 남겨라.

---

## 4) Common Failure Traps (Do not repeat)
- “예전 버전 Airflow 예제”를 가져오지 말 것
- ENV/경로/권한/의존성을 암묵적으로 가정하지 말 것
- backfill 날짜 경계 포함/미포함 실수 유발하는 코드를 쓰지 말 것
