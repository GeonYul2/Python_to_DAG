# Airflow Rewrite Rules (Modern Compatibility)

목표:
- 입력 코드가 구버전/AI 생성 실수 패턴을 포함하더라도,
  최신 Airflow에서 import/parse 가능한 형태로 **자동 치환**한다.
- 자동 치환이 위험하거나 모호하면 **명시적으로 실패**한다 (silent fix 금지).

---

## 1) Rewrite Strategy

### 1.1 Two Modes
- SAFE_REWRITE: 의미가 명확히 동일한 경우만 자동 치환
- FAIL_FAST: 의미 변경 가능성이 있는 경우는 에러로 중단

### 1.2 Detection
- 문자열 기반 단순 치환 금지(오탐 위험)
- AST/토큰 단위(최소)로 import 경로/이름을 탐지

---

## 2) Must-Rewrite Rules (SAFE_REWRITE)

아래는 “치환해도 의미가 바뀌지 않는” 항목만 포함한다.

### 2.1 PythonOperator import 경로
- from airflow.operators.python_operator import PythonOperator
  -> from airflow.operators.python import PythonOperator

### 2.2 DummyOperator -> EmptyOperator
- from airflow.operators.dummy_operator import DummyOperator
  -> from airflow.operators.empty import EmptyOperator
- DummyOperator(task_id="x")
  -> EmptyOperator(task_id="x")

---

## 3) Must-Fail Rules (FAIL_FAST)

### 3.1 Parse-time side effects
DAG import 시점에 아래가 감지되면 실패:
- 네트워크 호출
- 대용량 파일 로드
- 환경 의존 경로 접근

### 3.2 provide_context 사용/혼용
- provide_context=True가 발견되면:
  - “TaskFlow @task로 전환”이 가능한 경우만 rewrite
  - 그렇지 않으면 fail-fast + 해결 가이드 출력

---

## 4) Provider Dependency Policy Hook

Operator가 특정 provider를 요구하면:
- 해당 provider 패키지명/최소 버전을 `docs/PROVIDER_DEPENDENCY_POLICY.md`에 등록해야 한다.
- 등록 없으면 build 단계에서 실패한다.

---

## 5) Rewrite Report (필수 산출물)
build 수행 시 아래 리포트를 남긴다:
- rewrites_applied: [rule_id...]
- rewrites_failed: [rule_id + reason...]
- deprecated_detected: [pattern + file + lineno...]

리포트는 콘솔 + (선택) artifacts/rewrite_report.json 형태로 저장한다.
