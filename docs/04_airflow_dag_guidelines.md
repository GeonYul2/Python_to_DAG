# Airflow DAG Guidelines (Do/Don't)

## 1) Compatibility Matrix (Project Contract)
아래는 “우리 프로젝트에서 허용하는 범위”를 문서화하기 위한 섹션이다.
실제 구현 전, 이 범위를 코드 상수로도 고정한다.

- Python: 3.10+ (필수) - Airflow 3.x 지원을 위함
- Airflow: 3.x (이 프로젝트는 최신 stable 버전을 따른다)
- Providers: 사용 커넥터별로 최소 버전 명시

✅ 핵심: 구현자는 “모르겠으면 최신처럼” 가정하지 말고 **이 범위에 맞춰** 코드를 생성한다.

---

## 2) DAG Defaults (Standard)
- `catchup`: 원칙적으로 False (백필은 backfill 명령/전용 DAG로 수행)
- `max_active_runs`: 1~2 권장 (중복 실행으로 비용/중복 산출 방지)
- `retries`: 2~3 권장
- `retry_delay`: 5~10m 권장
- `execution_timeout`: 태스크 성격별 명시 (무한 실행 금지)
- `depends_on_past`: 기본 False (의도한 경우만 True)

---

## 3) Idempotency Rules
- 출력 경로는 반드시 `ds` 또는 `data_interval_start` 기반 파티션
- overwrite 정책은 명시적으로:
  - `append` / `overwrite_partition` / `fail_if_exists`
- 외부 API 호출은:
  - request_id, cursor, pagination state를 로그에 남김
  - rate limit/backoff 정책을 표준화

---

## 4) Backfill Safety
- 날짜 경계는 “inclusive/exclusive”를 고정:
  - `[start, end)` 권장 (end 미포함)
- `BETWEEN` 같은 포함 경계 함정은 회피:
  - `>= start` AND `< next_day` 패턴 권장
- 백필 시나리오 문서(`docs/06_failure_scenarios.md`)의 절차를 따른다.

---

## 5) XCom & Data Passing
❌ 금지:
- 대용량 데이터프레임/텍스트 본문을 XCom에 저장
✅ 권장:
- 경로/키/메타데이터만 XCom (예: s3_path, rowcount)

---

## 6) Secrets & Config
- 코드에 토큰/키 하드코딩 금지
- Airflow Connections/Variables/ENV로 주입
- 로컬 경로 하드코딩 금지 (config 기반)

---

## 7) Observability
- 모든 태스크는 correlation_id 포함 로그
- 실패 시 on_failure_callback에서:
  - pipeline_id, dag_id, task_id, run_id, exception 요약
  - 재시도 가능 여부 힌트
---

## 8) Friendly Documentation (Kindergarten Guide)
- **원칙**: 모든 DAG은 '어린아이도 이해할 수 있는' 설명을 포함해야 한다.
- **포맷**: 파일 최상단에 주석 블록(Triple Quotes)으로 작성.
- **필수 포함 내용**:
  - **비유(Analogy)**: DAG을 지도, 로봇, 공장 등으로 비유
  - **역할(Role)**: Operators는 도구/로봇으로 표현
  - **흐름(Flow)**: 의존성은 순서/약속으로 설명
- **목표**: 비개발자/주니어 엔지니어가 코드만 보고도 흐름을 100% 이해할 것.

---

## 9) Decoupling with Datasets
- **원칙**: 서로 다른 비즈니스 도메인이나 실패 영향도가 다른 파이프라인은 **Airflow Dataset**을 사용하여 분리한다.
- **Producer (Ingest)**: 데이터 수집/가공을 담당하며, 완료 시 Dataset을 업데이트(outlets)한다.
- **Consumer (Service)**: Dataset 업데이트를 감지(schedule=[Dataset(...)])하여 서비스 로직을 실행한다.
- **장점**:
  - **장애 격리**: 서비스 배포가 실패해도 데이터 수집은 계속된다.
  - **이벤트 기반**: 데이터가 준비되는 즉시 후속 작업이 실행된다.

