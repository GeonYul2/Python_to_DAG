# Config Schema (YAML) — v1

## 1) Top-level
```yaml
version: 1
pipeline_id: "pipeline__youtube__transcript_report"
description: "YouTube transcript to Korean deep summary report"
schedule: "0 9 * * *"
start_date: "2025-01-01"   # ISO date
catchup: false
defaults:
  owner: "data-team"
  retries: 3
  retry_delay_minutes: 10
  execution_timeout_minutes: 60
  tags: ["youtube", "llm", "report"]

tasks:
  - task_id: "extract_transcript"
    type: "python"
    entrypoint: "pipelines.python.youtube.extract:run"
    params:
      channel_id: "UCxxxx"
    outputs:
      - name: "raw_transcript"
        uri_template: "s3://bucket/youtube/raw/{ds}/transcript.json"
    upstream: []

  - task_id: "clean_text"
    type: "python"
    entrypoint: "pipelines.python.youtube.clean:run"
    inputs:
      - name: "raw_transcript"
        from_task: "extract_transcript"
    outputs:
      - name: "clean_text"
        uri_template: "s3://bucket/youtube/clean/{ds}/clean.txt"
    upstream: ["extract_transcript"]

  - task_id: "summarize"
    type: "python"
    entrypoint: "pipelines.python.youtube.summarize:run"
    params:
      model: "gpt-4.1-mini"  # example; 실제는 config/variable로
    inputs:
      - name: "clean_text"
        from_task: "clean_text"
    contract:
      type: "markdown_report"
      rules:
        - "must_include_sections: [핵심요약, 실무팁, 주의점]"
    outputs:
      - name: "report_md"
        uri_template: "s3://bucket/youtube/report/{ds}/report.md"
    upstream: ["clean_text"]

## 2) Validation Notes

entrypoint는 module:function 형태

uri_template는 {ds}(YYYY-MM-DD) 기반 파티션을 기본으로 함

secrets(키/토큰)는 params에 직접 넣지 말고 Airflow Variable/Connection으로 주입