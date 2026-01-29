# Observability Standard

## 1) Logging (Required)
모든 태스크는 최소 다음 메타를 로그에 포함한다:
- correlation_id (run 단위로 생성)
- pipeline_id, dag_id, task_id
- run_id, ds
- attempt, duration_ms
- output_paths (있다면)

## 2) Metrics (Recommended)
- task_success_count / task_failure_count
- task_duration_seconds (histogram)
- api_call_count, api_error_count (by status_code)
- produced_rows / produced_bytes (가능하면)

## 3) Alerting (Required Interface)
- on_failure_callback은 “플러그인” 형태
  - Slack, Email, PagerDuty 등은 구현체로 분리
- 알림 내용 최소 포함:
  - 실패 태스크/원인 요약/재시도 남은 횟수/로그 링크(가능하면)

## 4) Correlation
- 하나의 DAG run에서 생성된 산출물은 correlation_id를 파일 메타(또는 sidecar json)로 기록 가능하면 좋음
