# Phase 2 Backlog (Airflow Modernization & Quality)

이 문서는 Phase 2의 “정확도 고도화” 작업을 **작업 항목 + 수용 기준(AC) + 테스트 게이트**로 고정한다.
개발자는 기능을 추가하기 전에 반드시 해당 항목의 AC를 만족해야 한다.

---

## P2-1. Airflow 최신 버전 호환성 강제 (Rewrite Rules 강화)

### Goal
AI/기존 코드가 생성한 “구버전 스타일 DAG”을 최신 Airflow에서 import/parse 가능한 형태로 자동 치환한다.

### Acceptance Criteria (AC)
- AC1: 생성된 모든 DAG는 DagBag import 테스트에서 에러 0
- AC2: deprecated import/operator 경로가 코드에서 검출되면:
  - (a) 자동 치환되거나
  - (b) 명시적 에러로 fail-fast (침묵 금지)
- AC3: provider/operator 사용 시 요구 의존성(패키지)이 `docs/PROVIDER_DEPENDENCY_POLICY.md`에 명시됨

### Required Tests
- `tests/post/test_dag_import.py` (DagBag import error = 0)
- `tests/unit/test_rewrite_rules.py` (입력/출력 스냅샷 비교)

---

## P2-2. Few-shot/규칙 기반 품질 고도화 (깨지는 패턴 축적)

### Goal
“깨지는 패턴”을 예제로 축적하고, 변환기/생성기의 행동을 고정한다.  
예시는 문서(SSOT) + 테스트(회귀)로 잠근다.

### Acceptance Criteria (AC)
- AC1: `docs/FEW_SHOTS.md`에 Positive 10개 / Negative 10개 이상
- AC2: Negative 케이스는 변환 후 “정상 코드로 치환” 또는 “명시적 실패” 중 하나로 귀결
- AC3: 예시 추가 시 `tests/golden/` 또는 `tests/unit/`에 회귀 테스트가 반드시 1개 이상 추가됨

### Required Tests
- Golden test: `tests/golden/*.py` (생성 DAG 변경 감지)
- Pattern test: `tests/unit/test_negative_patterns.py`

---

## P2-3. CLI 도구화 + CI (GitHub Actions)

### Goal
로컬/CI에서 동일한 커맨드로 build/validate/import-test를 실행 가능하게 한다.

### Acceptance Criteria (AC)
- AC1: `python -m python_to_dag build --input ... --out dags/` 동작
- AC2: `python -m python_to_dag validate --input ...` 동작
- AC3: GitHub Actions에서
  - lint + unit + golden + dag_import 테스트가 자동 수행됨
- AC4: 실패 시 로그가 “어느 게이트에서 깨졌는지” 1줄로 식별 가능

### Required Tests/Gates
- Pre Gate: unit + schema + rewrite rules
- Post Gate: DagBag import

---

## P2-4. 고급 패턴 지원 (선택적 확장)

### Goal
실무에서 자주 쓰는 패턴을 안정적으로 지원한다.

### Priority Order (권장)
1) TaskGroup (가독성)
2) Branching / ShortCircuit (분기)
3) Sensor (대기)
4) TaskFlow API 확장 (dynamic mapping 포함은 최후)

### Acceptance Criteria (AC)
- AC1: 각 패턴별 샘플 파이프라인 1개 이상 제공
- AC2: 샘플은 DagBag import + 최소 스모크 테스트 통과
- AC3: 문서(`docs/AIRFLOW_PATTERNS.md`)에 “언제 쓰고 언제 쓰지 말아야 하는지” 명시
