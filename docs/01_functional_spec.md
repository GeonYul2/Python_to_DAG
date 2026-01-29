# Functional Spec — PYTHON_TO_DAG

## A. Primary User
- “데이터 분석 유튜버 영상 자막 → 한국어 심층 요약 리포트” 파이프라인을 운영하는 한국인 데이터 분석가(사용자)
- 파이프라인이 늘어나도 **빠르게 DAG를 추가/변경**하고 싶음
- 운영 중 장애/백필/스키마 변경에 강해야 함

## B. Inputs
### B1) Pipeline Definition (Python)
- 사용자는 Python으로 파이프라인 단계를 정의 (예: extract → transform → load → report)
- 각 단계는:
  - task_id
  - operator type (PythonOperator, BashOperator, DockerOperator 등)
  - params/env
  - retries/timeout
  - upstream dependencies
  - data contract hooks (optional)

### B2) Pipeline Definition (YAML)
- 빠르게 선언적으로 정의 가능
- YAML은 내부적으로 동일한 중간 표현(IR)로 변환

## C. Outputs
- Airflow DAG python 파일 (1 pipeline = 1 DAG가 기본)
- DAG 메타데이터:
  - tags, owner, schedule, start_date, catchup, max_active_runs, concurrency
- 공통 유틸:
  - logging wrapper (correlation_id 포함)
  - failure callback (Slack/Email 등 “인터페이스”로 분리)

## D. Must Requirements (필수)
1) 결정적 생성
- 같은 입력 → 같은 출력(정렬/포맷 포함)

2) 멱등성 기본값 강제
- 출력 경로는 run_id/ds 파티션 기반 규칙을 기본 제공
- overwrite 정책 명시 없으면 “안전 모드” (중복 생성 방지)

3) 백필/캐치업 안전
- start_date/catchup 규칙 명확
- backfill 시 데이터 경계(날짜 포함/미포함) 실수 방지 가이드 포함

4) 장애/재시도/알림 표준화
- retries, retry_delay, execution_timeout, SLA(옵션)
- on_failure_callback 표준 제공(채널은 pluggable)

5) 데이터 계약(Data Contract) 훅
- 스키마(컬럼/타입), 파티션 규칙, 파일명 규칙을 “검증 단계”로 삽입 가능
- 계약 위반 시 태스크 실패 + 명확한 에러 메시지

6) 운영 로깅 표준
- 모든 태스크 로그에 correlation_id/pipeline_id/task_id/run_id/ds 포함
- 주요 이벤트: start/end/rowcount/output_path

## E. Should Requirements (권장)
- TaskGroup 지원
- Dynamic Task Mapping(가능하면) 지원
- Dataset 기반 스케줄(가능하면) 지원
- Lineage 메타(출력 테이블/파일) 기록

## F. Won’t (초기 제외)
- UI 기반 파이프라인 작성기
- 자동 스키마 진화/마이그레이션(단, 감지/경고는 가능)

## G. Acceptance Criteria (수용 기준)
- 샘플 파이프라인 2개가:
  - Python 정의/ YAML 정의 각각에서 DAG 생성
  - 골든 파일 테스트 통과
  - 가이드된 실패 시나리오 3개 재현 가능(예: API 실패, 스키마 변경, backfill)
