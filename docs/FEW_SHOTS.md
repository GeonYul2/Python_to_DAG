# Few-shots for High-Precision DAG Output

이 문서는 “정확도”를 올리기 위한 SSOT이다.
- Positive: 기대 출력(정답 형태)
- Negative: 자주 깨지는 패턴(오답 형태) + 기대 처리(rewrite or fail)

예시는 반드시 테스트로 잠근다.
- Positive는 golden test로
- Negative는 rewrite unit test 또는 fail-fast test로

---

## A) Positive Examples (요약 템플릿)

### P-01: 최소 DAG (TaskFlow @task 기반)
요구:
- module-level DAG
- retries/timeout 명시
- parse-time side effect 없음
- task 간 dependency 명확

(예시는 코드/파일로 별도 examples/에 위치시키고,
여기서는 “필수 속성 체크리스트”로 고정한다.)

필수 체크:
- [ ] from airflow import DAG
- [ ] from airflow.decorators import task
- [ ] schedule/catchup/max_active_runs 명시
- [ ] retries/retry_delay/execution_timeout 명시

---

## B) Negative Examples (패턴 + 기대 처리)

### N-01: 구버전 PythonOperator import
패턴:
- airflow.operators.python_operator 경로 사용

기대 처리:
- SAFE_REWRITE로 최신 경로로 치환 (AIRFLOW_REWRITE_RULES.md 2.1)

테스트:
- tests/unit/test_rewrite_rules.py::test_python_operator_import_rewrite

---

### N-02: DummyOperator 사용
패턴:
- DummyOperator 또는 dummy_operator import

기대 처리:
- SAFE_REWRITE로 EmptyOperator로 치환 (2.2)

---

### N-03: DAG import 시 네트워크 호출
패턴:
- requests.get(...)가 DAG 파일 top-level에 존재

기대 처리:
- FAIL_FAST + “task 내부로 이동” 가이드 출력

---

### N-04: provide_context 혼용
패턴:
- PythonOperator(provide_context=True) 사용

기대 처리:
- (가능) @task 전환 + kwargs 제거
- (불가능) FAIL_FAST + 수정 가이드

---

## C) Example Expansion Policy
새 패턴이 2번 이상 반복되면:
1) 이 문서에 Negative로 추가
2) 대응 룰을 AIRFLOW_REWRITE_RULES.md에 추가
3) 회귀 테스트 추가
