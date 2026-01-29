# Coding Conventions (Project-Wide)

## 1) Naming
### task_id
- 소문자 + 언더스코어
- 동사_목적어 구조 권장
  - 예: `extract_transcript`, `clean_text`, `summarize_chunks`, `render_report`

### pipeline_id / dag_id
- `pipeline__{domain}__{name}` 형태 권장
  - 예: `pipeline__youtube__transcript_report`

## 2) Logging
- 모든 로그는 structured logging 형태(가능하면 JSON)
- 필수 필드:
  - `correlation_id`, `pipeline_id`, `dag_id`, `task_id`, `run_id`, `ds`
- 이벤트:
  - `task_start`, `task_end`, `task_fail`, `output_written`

## 3) File/Path Rules
- 로컬 개발: `./data/{pipeline_id}/{ds}/...`
- 운영: 스토리지(prefix) + `{pipeline_id}/{ds}/...`
- 임시 파일은 run 완료 후 삭제 정책 명시

## 4) Error Handling
- 예외는 삼키지 않는다.
- 외부 API 실패:
  - status_code, response snippet(민감정보 제외), retryable 여부 로그
- 데이터 계약 실패:
  - 어떤 컬럼/타입/규칙이 깨졌는지 “사람이 읽을 수 있게” 출력

## 5) Determinism
- dict/set 순회 금지(정렬 없이)
- time.now() 같은 비결정 요소는 생성 단계에서 사용 금지
- 생성 파일 상단에 generator 버전 고정 표기

## 6) Formatting & Lint
- black/ruff(또는 동등)로 일괄 포맷
- import 정렬 isort(또는 ruff 규칙)
