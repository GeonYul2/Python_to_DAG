
---

## 10) `docs/08_testing_strategy.md`
```md
# Testing Strategy

## 1) Goals
- 변환기/생성기의 결정성 보장
- 스펙 위반을 PR 단계에서 차단
- “구버전 DAG 생성” 재발 방지

## 2) Test Lifecycle (TDD)
1.  **Red**: Write a failing test case in `tests/` that reflects a new requirement.
2.  **Green**: Implement the minimal code to pass the test.
3.  **Refactor**: Improve code quality while keeping tests green.

## 3) Test Layers
### 2.1 Unit
- YAML parser → IR 생성 테스트
- IR validator 테스트 (순환 의존성, naming 위반, required missing)
- template renderer 테스트 (핵심 필드 존재 여부)

### 2.2 Golden File (Mandatory)
- 샘플 pipeline 입력에 대해 생성된 DAG를 `tests/golden/*.py`와 비교
- diff가 발생하면:
  - 의도된 변경인지 확인
  - 의도된 변경이면 golden 갱신 + 변경 이유를 문서화

### 2.3 Smoke (Optional)
- 최소한 import 가능한 DAG인지 (syntax check)
- (가능하면) `airflow dags list` 수준 검증

## 3) CI Gate (권장)
- lint + unit + golden 통과 필수
- 실패 시:
  - 어떤 규칙을 위반했는지 명확한 메시지

## 4) Forbidden Regression Checklist
- task ordering 흔들림
- Airflow 문법/파라미터 deprecated 사용
- hardcoded path/secret 재등장
